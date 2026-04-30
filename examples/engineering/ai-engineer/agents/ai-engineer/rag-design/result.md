# Result: RAG pipeline for internal documentation search

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18/18 criteria met (100%) |
| **Evaluated** | 2026-04-30 |

## Output

The following is a simulated agent response to the prompt. This is what a developer would receive when asking the ai-engineer agent to design a RAG pipeline for the described corpus.

---

### Corpus analysis

Before recommending anything, let me characterise what we're working with, because the corpus properties drive every downstream decision.

| Property | Value |
|---|---|
| Confluence pages | ~2,000 (Markdown/HTML) |
| PDF runbooks | ~500 |
| Total volume | ~800MB |
| Update cadence | A few times per week |
| Query types | Procedural ("rollback procedure for payments service") and ownership ("which team owns authentication microservice") |
| Citation requirement | Yes — users need source references |
| Monthly AI budget | $500 |

Two document types with meaningfully different structures: Confluence pages are navigable reference docs; PDF runbooks are linear, procedural, step-by-step. They need different chunking approaches.

---

### Evaluation criteria (defined before implementation)

| Dimension | Target | How measured |
|---|---|---|
| Retrieval precision@5 | ≥0.8 | Ground-truth eval set — correct source in top 5 results |
| Retrieval recall@5 | ≥0.7 | Correct source retrieved at all |
| Answer faithfulness | ≥0.85 | Generated answer attributable to retrieved chunks, not hallucinated |
| Citation coverage | 100% | Every answer includes ≥1 source citation |
| Latency (p95) | ≤5s end-to-end | Timed from query to first token |
| Monthly cost | ≤$500 | Tracked per-component |

These targets are negotiable — but they must be written before writing a single line of integration code.

---

### Decision checkpoint: model selection

Stopping here before recommending specific models. The $500/month budget is the binding constraint and model selection locks in cost. I need you to confirm:

1. What is the expected query volume per month? (drives per-query LLM cost)
2. Is 5s p95 latency acceptable, or do you need sub-2s responses?
3. Are there data residency requirements that restrict which providers we can use?

I'll proceed with working assumptions below, but flag them clearly.

---

### Document ingestion

**Confluence pages (Markdown/HTML)**

- Strip nav chrome, sidebars, footers — keep page title, headings, body text
- Use heading boundaries as primary chunk boundaries (H2/H3 level)
- Chunk size: **512 tokens with 15% overlap (~77 tokens)**. Confluence pages are reference documentation — concepts need enough context to be meaningful, but pages can be long. 512 tokens keeps chunks grounded without losing the concept being described. Overlap handles sentence-spanning the boundary.

**PDF runbooks**

- Use a layout-aware extractor (e.g. `pdfplumber` or `unstructured`). Treating PDFs as plain text strips tables, multi-column layouts, and step numbering. OCR any scanned pages before chunking.
- Chunk size: **256 tokens with 10% overlap (~26 tokens)**. Runbooks are procedural — users asking "what's the rollback procedure" want a specific numbered sequence of steps, not a long surrounding section. Smaller chunks align to individual steps and make retrieval more precise.

**Metadata schema**

Every chunk gets:

```json
{
  "chunk_id": "uuid",
  "source_type": "confluence | pdf",
  "source_url": "https://confluence.example.com/pages/...",
  "source_title": "Payments Service Runbook v2.3",
  "section_heading": "Rollback Procedure",
  "owning_team": "payments-platform",
  "last_modified": "2026-04-28T14:00:00Z",
  "doc_hash": "sha256:abc123...",
  "access_scope": ["engineering", "support"]
}
```

`owning_team` and `access_scope` are critical — they enable ownership queries via metadata filtering and prevent cross-permission leakage.

---

### Embedding model selection

Working assumption: general-purpose English corpus, no multilingual requirement, OpenRouter available per tooling conventions.

| Model | Quality (MTEB avg) | Cost per 1M tokens | Notes |
|---|---|---|---|
| `text-embedding-3-small` (OpenAI) | 62.3 | $0.02 | Strong baseline, very cheap, wide support |
| `voyage-3` (Voyage AI) | 67.1 | $0.06 | Better on long technical docs |
| `BGE-M3` (BAAI, self-hosted) | 68.5 | ~$0 (infra only) | Best quality, requires GPU hosting |

**Recommendation (pending eval):** start with `text-embedding-3-small` for cost reasons — 2,000 Confluence pages + 500 PDFs at average 4,000 tokens each ≈ 10M tokens one-time ingestion cost ≈ $0.20 total. Weekly re-embed of changed docs (assume 5% of corpus, ~125 docs, ~500K tokens) ≈ $0.01/week.

**Do not finalise this until you run both `text-embedding-3-small` and `voyage-3` on your 20-query test set using real queries from your support and engineering teams.** Benchmark scores are not a substitute for measuring on your actual content.

---

### Retrieval strategy

Pure vector similarity will not reliably answer ownership queries like "which team owns the authentication microservice". A query embedding for "team ownership" may not surface the right chunk if ownership is expressed as metadata rather than prose.

**Design: hybrid retrieval with metadata filtering**

1. **Semantic search** — top-10 candidates from vector similarity
2. **Keyword filter** — BM25 re-score for exact term matches (service names, team names)
3. **Metadata filter** — for ownership queries, filter on `owning_team` field directly
4. **Re-ranking** — cross-encoder re-rank top-5 from the above for final context window
5. **Access scope filter** — always filter by `access_scope` matching the authenticated user's roles before returning any chunk

Query classifier (lightweight, fast-path): detect ownership-pattern queries ("which team", "who owns", "who is responsible for") and route to metadata filter first, vector search second.

Top-K: **5 chunks** in the generation context. Balances context richness against cost and noise.

---

### Monthly cost model

**Working assumptions:** 2,000 queries/day (750K/month), average query = 5 retrieved chunks × 512 tokens = ~2,560 context tokens + 150 token answer.

| Component | Calculation | Monthly cost |
|---|---|---|
| One-time ingestion (amortised over 12 months) | 10M tokens × $0.02/1M ÷ 12 | $0.02 |
| Weekly re-embed (5% corpus changed, ~500K tokens × 4 weeks) | 2M tokens × $0.02/1M | $0.04 |
| Per-query generation (GPT-4o-mini @ $0.15/1M input, $0.60/1M output) | 750K × (2,560 × $0.15 + 150 × $0.60) / 1M | $355 |
| Embedding at query time | 750K × 200 tokens × $0.02 / 1M | $3 |
| **Total** | | **~$358/month** |

This fits inside the $500/month ceiling with ~$142 headroom at 2,000 queries/day. If query volume is higher, switch generation to a cheaper model (Haiku-class) for routine ownership lookups and reserve GPT-4o-mini for complex procedural queries.

**Generation model: GPT-4o-mini.** Reasoning: sufficient quality for retrieval-grounded Q&A where hallucination risk is controlled by context; cost is 10x cheaper than GPT-4o; fits budget at projected volume.

---

### Prompt template

```
You are a technical documentation assistant for [Company] internal teams.

Answer the user's question using ONLY the retrieved documentation chunks provided below.
If the answer is not present in the chunks, respond: "I don't have enough information in the available documentation to answer this."

For every factual claim, cite the source document immediately after the claim.

Retrieved documentation:
{{#each chunks}}
[Source {{@index+1}}]: {{this.source_title}} — {{this.section_heading}}
URL: {{this.source_url}}
---
{{this.content}}
{{/each}}

User question: {{query}}

Respond in the following JSON format:
{
  "answer": "<your answer in plain text>",
  "citations": [
    {
      "claim": "<the specific claim this citation supports>",
      "source_title": "<document title>",
      "source_url": "<URL or runbook ID>",
      "section": "<section heading>"
    }
  ],
  "confidence": "high | medium | low",
  "insufficient_context": false
}
```

If `insufficient_context` is true, the `answer` field contains the "I don't have enough information" message and `citations` is empty.

---

### Freshness / incremental indexing

Do not full-re-index 800MB weekly. Instead:

1. On ingest, store `doc_hash` (SHA-256 of raw content) per document
2. Crawler runs daily (or on Confluence webhook if available): fetch updated pages/PDFs
3. Compute hash of fetched content; compare to stored hash
4. If hash differs: re-chunk the document, re-embed, upsert chunks into vector store, update stored hash
5. If hash unchanged: skip
6. Deleted documents: mark chunks as inactive (soft-delete with `deleted_at`); exclude from retrieval

Expected: a few-times-weekly update touching ~50-100 pages → re-embeds a small fraction of corpus. Full re-index only on embedding model migration.

---

### Access control

Internal docs have permissions. A support engineer should not see runbooks marked `access_scope: ["engineering-internal"]`.

Implementation:

- Every chunk carries `access_scope` in metadata (populated from Confluence space permissions or PDF folder classification)
- On every query, retrieve the authenticated user's role set from your identity system
- Apply a pre-filter: only retrieve chunks where `access_scope` intersects with the user's roles
- Never pass unauthorised chunks into the generation context — the LLM cannot enforce access boundaries

---

### Evaluation plan

**Retrieval eval set (20 queries, run before any generation testing)**

| # | Query | Expected source | Expected section |
|---|---|---|---|
| 1 | What is the rollback procedure for the payments service? | Payments Service Runbook v2.3 | Rollback Procedure |
| 2 | Which team owns the authentication microservice? | Authentication Service Overview | Ownership & Contacts |
| 3 | How do I escalate a P1 incident for the orders service? | Incident Response Runbook | Escalation Paths |
| 4 | What are the retry limits for the notification service? | Notification Service Config | Retry Policy |
| 5 | Where is the deployment runbook for the data pipeline? | Data Pipeline Runbook | Deployment |
| 6 | What monitoring dashboards exist for the payments service? | Payments Observability Guide | Dashboards |
| 7 | How do I restore the user database from backup? | Database Runbook | Restore Procedure |
| 8 | Who is the on-call contact for the billing team? | Billing Service Runbook | On-Call Roster |
| 9 | What is the SLA for the authentication service? | SLA Documentation | Authentication SLA |
| 10 | How do I rotate secrets for the payments service? | Payments Security Runbook | Secret Rotation |
| 11 | What does error code 503 mean in the orders service? | Orders API Reference | Error Codes |
| 12 | How do I trigger a manual deployment for the web app? | Deployment Runbook | Manual Deploy |
| 13 | What is the database schema for the user accounts table? | Data Dictionary | users table |
| 14 | How long are audit logs retained? | Security Compliance Runbook | Log Retention |
| 15 | Which team owns the search microservice? | Search Service Overview | Ownership & Contacts |
| 16 | What environments exist and how do I access staging? | Environment Guide | Staging Access |
| 17 | How do I add a new feature flag? | Feature Flag Runbook | Creating Flags |
| 18 | What is the process for decommissioning a service? | Engineering Handbook | Decommission Process |
| 19 | How do I set up local development for the mobile app? | Mobile Dev Setup | Local Setup |
| 20 | What is the incident communication template? | Incident Response Runbook | Communication Templates |

Run retrieval against this set. Measure precision@5 and recall@5. Fix retrieval gaps before touching the generation prompt.

**Generation eval:** once retrieval passes, run the full pipeline on the same 20 queries. Score: does the answer correctly address the question? Does every answer include at least one citation? Is `insufficient_context: true` correctly set for any query where source docs are not in the corpus?

---

### Failure handling

| Mode | Handling |
|---|---|
| Model unavailable | Queue query with 30s retry × 3; surface "search temporarily unavailable" after 3 failures |
| Timeout (>10s) | Return partial retrieval results with "generation timed out" message |
| No relevant chunks retrieved (similarity score < threshold) | Set `insufficient_context: true`; return "I don't have enough information" |
| Answer not grounded in context | Output validator checks that claims in answer appear in retrieved chunks; flag for review if <80% grounded |
| Cost spike | Circuit breaker on monthly spend; alert at 80% of $500 budget |

---

### Pipeline summary

| Stage | Decision | Rationale |
|---|---|---|
| Confluence extraction | Heading-boundary chunking, 512 tokens, 15% overlap | Reference content; needs context |
| PDF extraction | Layout-aware + OCR, 256 tokens, 10% overlap | Procedural steps; precision retrieval |
| Embedding | `text-embedding-3-small` (evaluate vs `voyage-3`) | $0.02/1M — fits budget; validate on your data |
| Vector store | Postgres + pgvector or Qdrant | Depends on existing infra |
| Retrieval | Hybrid (vector + BM25) + metadata filter + access scope filter | Handles ownership queries; enforces permissions |
| Re-ranking | Cross-encoder top-5 | Improves precision for multi-hop queries |
| Generation | GPT-4o-mini | Fits $500/month at 2K queries/day |
| Evaluation | Retrieval first (20-query set), then generation | Separate phases; don't optimise prompts before retrieval works |

---

## Evaluation

### Criteria

- [x] PASS: Agent defines evaluation criteria before proposing implementation — "Evaluation before implementation. Define how you will measure success before writing a single line of AI integration code." The simulated output opens with a full evaluation criteria table (precision@5, recall@5, faithfulness, citation coverage, latency, monthly cost) before any implementation recommendation.

- [x] PASS: Agent analyses corpus properties before recommending chunking strategy — Corpus analysis table appears first. Chunk size recommendations are explicitly tied to Confluence (reference content, 512 tokens) vs PDF runbooks (procedural, 256 tokens), derived from the corpus characterisation.

- [x] PASS: Agent recommends evaluating embedding models on a 20-query test set from actual user queries — "Do not finalise this until you run both `text-embedding-3-small` and `voyage-3` on your 20-query test set using real queries from your support and engineering teams. Benchmark scores are not a substitute for measuring on your actual content."

- [x] PASS: Agent addresses citation requirements — Prompt template includes explicit citation instruction ("For every factual claim, cite the source document immediately after the claim"). Response schema includes a `citations` array with claim, source_title, source_url, and section fields.

- [x] PASS: Agent defines a freshness/rebuild strategy — Incremental indexing section: SHA-256 hash per document, daily crawler, re-embed only changed docs, skip unchanged hashes. Full re-index only on model migration.

- [x] PASS: Agent includes fallback handling for model unavailability and insufficient context — Failure handling table covers model unavailability (queue + retry × 3), timeout, no relevant chunks retrieved (`insufficient_context: true`), and grounding validation. Prompt template explicitly instructs "If the answer is not present in the chunks, respond: 'I don't have enough information'".

- [x] PASS: Agent raises a decision checkpoint before choosing a model — Decision checkpoint section explicitly stops and asks for query volume, latency requirements, and data residency constraints before finalising model recommendations.

- [x] PASS: Agent separates retrieval evaluation from generation evaluation and specifies testing retrieval first — Evaluation plan section: "Run retrieval against this set. Measure precision@5 and recall@5. Fix retrieval gaps before touching the generation prompt." Generation eval is a separate step, conditional on retrieval passing. Pipeline summary table includes "Separate phases; don't optimise prompts before retrieval works."

- [x] PASS: Output covers all pipeline stages — Chunking config (256/512 tokens, overlap), metadata schema, embedding selection (text-embedding-3-small vs voyage-3), retrieval strategy (hybrid + metadata filter + re-ranking + access scope), prompt template (full draft), evaluation plan (20-query set). All stages covered.

### Output expectations

- [x] PASS: Chunking strategy distinguishes Markdown/HTML Confluence pages from PDFs with OCR acknowledgment — Two separate extraction sections. Confluence: heading-boundary chunking, 512 tokens. PDFs: "use a layout-aware extractor (e.g. `pdfplumber` or `unstructured`). OCR any scanned pages before chunking."

- [x] PASS: Specific chunk size and overlap values with reasoning tied to corpus content — Confluence: 512 tokens, 15% overlap, "reference documentation — concepts need enough context to be meaningful." PDFs: 256 tokens, 10% overlap, "Runbooks are procedural — users asking 'what's the rollback procedure' want a specific numbered sequence of steps." Reasoning is tied to content type, not generic.

- [x] PASS: Retrieval design addresses ownership/team queries via metadata filtering or hybrid retrieval — Hybrid retrieval section: "Pure vector similarity will not reliably answer ownership queries." Design includes metadata filter on `owning_team` and a query classifier routing ownership-pattern queries to metadata filter first. Metadata schema includes `owning_team` field.

- [x] PASS: Monthly cost calculation breaks down embedding cost plus per-query LLM generation cost with a number fitting $500/month — Cost model table: one-time ingestion (amortised), weekly re-embed, per-query generation, query-time embedding. Total ≈ $358/month against $500 budget. Reconciles at 2,000 queries/day.

- [x] PASS: Prompt template includes citation instruction and response schema includes citations array — Prompt template contains "cite the source document immediately after the claim." JSON response schema includes `citations` array with `claim`, `source_title`, `source_url`, and `section` fields.

- [x] PASS: Incremental indexing strategy rather than full re-indexing — Dedicated section: SHA-256 hash comparison, re-embed only changed docs, skip unchanged. "Do not full-re-index 800MB weekly."

- [x] PASS: Evaluation plan lists at least 10-20 example queries from the prompt's domain with expected source documents — 20-query table with queries drawn from the prompt domain (rollback procedures, team ownership, incident escalation, secret rotation), each paired with expected source document and section.

- [x] PASS: Names specific embedding model candidates and a specific generation model with cost justification — Embedding candidates: `text-embedding-3-small` ($0.02/1M), `voyage-3` ($0.06/1M), BGE-M3 (self-hosted). Generation model: GPT-4o-mini with explicit reasoning ("10x cheaper than GPT-4o; fits budget at projected volume"). Cost-per-million-token figures provided for each.

- [x] PASS: Access control — Dedicated access control section: `access_scope` metadata on every chunk, pre-filter on user roles before retrieval, explicit note that "the LLM cannot enforce access boundaries." Metadata schema includes `access_scope` field.

## Notes

The agent definition has all the structural machinery to produce a strong RAG design. The Document Ingestion section explicitly separates Confluence and PDF handling, ties chunk size to content type, and calls out OCR for PDFs. RAG Rules cover incremental indexing, access control, domain-specific eval sets, and citation — all directly addressing the specific scenario in the prompt.

The embedding model selection table instructs the agent to "name specific current candidates" rather than naming them itself, which means the specific models in the simulated output (text-embedding-3-small, voyage-3, BGE-M3) are the agent's runtime choice. This is the right design — model availability and pricing change frequently enough that hardcoding specific model names in the definition would go stale. The definition's instruction to justify by cost-per-million-tokens against budget is what matters, and the simulated output demonstrates that instruction followed correctly.

One area worth watching: the definition's Key Decisions table lists chunk size options as "256 / 512 / 1024 tokens" without guidance on when to differentiate by content type. The Document Ingestion section does provide that guidance, but an agent following only the Key Decisions table might default to a single size for both corpus types. The definition is internally consistent but could make the content-type dependency more prominent in the table itself.
