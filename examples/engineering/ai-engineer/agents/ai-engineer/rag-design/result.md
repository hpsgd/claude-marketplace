# Rag Design

Scenario: User wants to build a RAG pipeline so employees can ask natural language questions against the company's internal documentation corpus (~2,000 Confluence pages and ~500 PDF runbooks).

## Prompt

> We want to let our support and engineering teams search our internal docs using natural language. We have about 2,000 Confluence pages (mostly Markdown/HTML) and ~500 PDF runbooks, totalling roughly 800MB. Documents are updated a few times a week. Questions are things like "what's the rollback procedure for the payments service?" or "which team owns the authentication microservice?". We need citations so users know where answers came from. Budget is $500/month for AI costs. Can you design this RAG pipeline?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# RAG Pipeline Design: Internal Knowledge Base

## Corpus Profile

| Property | Value |
|---|---|
| Document types | Confluence pages (Markdown/HTML), PDF runbooks |
| Volume | 2,500 documents, ~800 MB |
| Estimated chunks | 12,000–18,000 (5–7 chunks/doc average) |
| Update frequency | A few times per week |
| Language | English |
| Content structure | Headings, numbered procedures, tables, code blocks |
| Query pattern | Procedural ("how do I…") and ownership ("which team…") |

---

## Chunking Configuration

Two content types, two strategies. Do not apply a single strategy across the whole corpus.

**Confluence pages (Markdown/HTML):**
- **Strategy:** Semantic — split on heading boundaries (`##`, `###`)
- **Chunk size:** 512 tokens target, hard cap 768
- **Overlap:** 64 tokens (one paragraph) across heading boundaries only
- **Boundary rules:** Never split mid-sentence. Tables and code blocks are atomic — never split them. If a section exceeds 768 tokens, split at paragraph boundaries within it.

**PDF runbooks:**
- **Strategy:** Paragraph-based with procedure awareness
- **Chunk size:** 512 tokens target, hard cap 640
- **Overlap:** 15% (keep last step of previous chunk as context)
- **Boundary rules:** Numbered steps (`1. … 2. …`) must not be split mid-sequence. A procedure step is atomic even if it exceeds the target. If a full numbered procedure fits within 768 tokens, keep it as one chunk.

**Rationale:** Ownership queries ("which team owns X?") are answered by single-sentence facts — small chunks retrieve them precisely. Procedural queries ("rollback procedure for payments?") need step sequences intact — procedure-aware chunking prevents returning half a rollback procedure.

---

## Metadata Schema

| Field | Type | Source | Purpose |
|---|---|---|---|
| `source_id` | string | Confluence page ID / PDF filename | Deduplication, update detection |
| `source_name` | string | Page title / PDF filename | Citation display |
| `source_url` | string | Confluence URL / runbook path | Clickable citation link |
| `document_type` | enum | Classifier at ingest | Filter: `confluence_page` \| `pdf_runbook` |
| `confluence_space` | string | Confluence API | Filter by team space (e.g. `PAYMENTS`, `INFRA`) |
| `team_owner` | string | Confluence `owner` field / PDF header extraction | Ownership queries, filtered search |
| `service_name` | string[] | Extracted via NER or title parsing | Service-scoped retrieval |
| `section_heading` | string | Nearest `#` heading above chunk | Citation granularity ("Payments Service > Rollback") |
| `chunk_index` | integer | Ingest pipeline | Reconstruct document order |
| `content_hash` | string | SHA-256 of chunk text | Change detection — only re-embed modified chunks |
| `last_updated` | datetime | Confluence `modified` / PDF metadata | Staleness flagging |
| `page_number` | integer | PDF only | Citation: "Runbook, p. 4" |

`team_owner` and `service_name` are the two highest-value metadata fields for your query types. Invest time in extracting them reliably at ingest rather than relying on free-text matching at query time.

---

## Embedding

**Recommended model:** `text-embedding-3-small` (OpenAI)
- 1,536 dimensions (use Matryoshka truncation to 768 if storage is a concern)
- 8,192 token input limit — comfortably covers your 768-token max chunk
- Cost: $0.02 / 1M tokens → initial index of ~800MB ≈ 9M tokens ≈ **$0.18 one-time**
- Incremental updates (5% of corpus weekly) ≈ **$0.04/month**

**Before committing:** Run the 20-query evaluation below. If retrieval precision is below 80%, evaluate `voyage-code-2` as an alternative — it outperforms `text-embedding-3-small` on technical documentation with service names, error codes, and CLI commands.

**20-query evaluation protocol:**
1. Select 10 procedural queries and 10 ownership queries representative of real user behaviour
2. Manually identify the 3–5 chunks that *should* be returned for each
3. Embed corpus, run queries, measure Precision@5 and Recall@5
4. If results are below target, switch to `voyage-code-2` before building the rest of the pipeline

---

## Retrieval Configuration

**Strategy: Hybrid search (semantic + BM25), with optional ownership fast-path**

Your query patterns make hybrid retrieval the right default:
- Procedural queries contain natural language ("rollback procedure") → semantic search excels
- Ownership queries contain exact service names ("authentication microservice") → BM25 keyword search excels
- Many queries contain both → hybrid wins over either alone

**Implementation:** PostgreSQL + pgvector for semantic search, PostgreSQL `tsvector` full-text search for BM25. Combine results using **Reciprocal Rank Fusion (RRF)**. This runs on infrastructure you almost certainly already have — no additional vector database service required.

```
RRF score = Σ 1 / (k + rank_i)   where k = 60
```

**Top-K:** 5 for ownership queries, 7 for procedural queries. Detect query type with a lightweight classifier (single embedding comparison against "what/who owns X" vs "how do I X" centroids) or a simple regex heuristic.

**Metadata filters applied at query time:**

| Trigger in query | Filter applied |
|---|---|
| Service name matched | `service_name = [matched_service]` |
| Team name matched | `team_owner = [matched_team]` or `confluence_space = [space]` |
| "runbook" / "procedure" | `document_type = pdf_runbook` |

Filters are additive and optional — if no service name is detected, no filter is applied. Never silently discard results because a filter matched zero chunks; fall back to unfiltered search and log the event.

---

## Prompt Template

```
You are an internal knowledge base assistant for the engineering and support teams.
Answer questions using ONLY the context documents provided below.
If the answer is not in the context, say: "I don't have enough information to answer this question. Try searching Confluence directly or contact the relevant team."
Do not infer or extrapolate beyond what is explicitly stated in the context.
For every factual claim, include a citation in the format [Source: document name, section].

<context>
{% for chunk in retrieved_chunks %}
[Source: {{ chunk.source_name }}{% if chunk.section_heading %} > {{ chunk.section_heading }}{% endif %}{% if chunk.page_number %}, p.{{ chunk.page_number }}{% endif %}]
{{ chunk.text }}

{% endfor %}
</context>

Question: {{ user_query }}

Answer (cite sources for every claim):
```

**Prompt caching:** Mark the system instruction block as a cache breakpoint. At ~200 queries/day, this reduces input token costs by 30–40% on cache hits.

**Citation format rendered to users:**
> The rollback procedure for the payments service involves... [Payments Service Runbook > Rollback Steps, p. 3]

Make citations clickable links to `source_url`. This is the most important trust signal for your users.

---

## Cost Projection

| Component | Model/Service | Est. monthly cost |
|---|---|---|
| Embeddings | text-embedding-3-small | ~$0.05 |
| Generation — 200 queries/day | Claude Sonnet 4.6, ~2.5K input + 500 output tokens/query | ~$90 |
| Generation — 500 queries/day | Same | ~$225 |
| Generation — 1,100 queries/day | Same | ~$495 (budget ceiling) |
| PostgreSQL + pgvector | Self-hosted or RDS | Infrastructure cost, not AI budget |

**At 200–500 queries/day you are well within the $500/month cap.** You have room to move to Claude Opus if answer quality on complex procedural queries is insufficient — revisit after evaluation.

---

## Freshness Strategy

| Property | Decision |
|---|---|
| Incremental updates | Confluence webhook → re-index changed pages within 1 hour of modification |
| PDF runbooks | Weekly scheduled scan comparing file hashes; re-index changed files |
| Change detection | SHA-256 hash of raw page content. Only re-embed chunks whose parent document changed |
| Staleness threshold | Flag documents not updated in 180 days in the citation display ("Last updated: 8 months ago") |
| Full re-index | Monthly, to catch any missed webhook events |

**Webhook setup:** Confluence Cloud supports page `updated` and `created` webhooks natively. Route to an ingest worker that fetches the updated page, rechunks it, diffs chunk hashes against the current index, and re-embeds only changed chunks. Cost per incremental update: negligible.

---

## Evaluation Targets

### Retrieval (measure before touching generation)

| Metric | Target | How to measure |
|---|---|---|
| Precision@5 | ≥ 80% | Hand-label 30 queries; count relevant in top 5 |
| Recall@5 | ≥ 70% | Same set; count relevant retrieved / total relevant |
| MRR | ≥ 0.8 | Is the best result in position 1 or 2? |

### Generation (measure only after retrieval passes)

| Metric | Target | How to measure |
|---|---|---|
| Answer accuracy | ≥ 90% | Human spot-check against source documents |
| Citation accuracy | ≥ 95% | Do cited sources contain the stated claim? |
| Faithfulness | 100% | Any answer not traceable to context is a failure |
| "I don't know" precision | ≥ 90% | Does it refuse correctly when answer is absent? |

Use [RAGAS](https://docs.ragas.io/) for automated faithfulness, answer_relevancy, context_precision, and context_recall metrics on the 30-query test set.

---

## Monitoring

Track these in production from day one:

- **Zero-result queries** — queries where top-5 similarity scores are all below 0.6. These reveal gaps in the corpus.
- **Query latency** — retrieval + generation end-to-end. Alert if P95 exceeds 8 seconds.
- **"I don't know" rate** — if it climbs, the corpus has gaps or the retrieval is degrading.
- **Low-confidence retrievals** — log every query where max similarity score < 0.65 for manual review.
- **Index freshness** — alert if any Confluence webhook has not fired in 24 hours (webhook failure detection).

---

## Open Questions

1. **Service name extraction:** Do Confluence pages have a consistent metadata field for `service_name`, or does this need to be extracted from titles/headings via NER? The quality of ownership query results depends heavily on this.
2. **Access control:** Do support and engineering teams have the same access rights to all 2,500 documents? If not, the retrieval layer needs to filter by user permissions before returning chunks.
3. **PDF quality:** Are the PDF runbooks machine-generated (clean text extraction) or scanned (requires OCR)? Scanned PDFs need a preprocessing step (Tesseract or AWS Textract) before chunking.
4. **Feedback loop:** Is there a plan to capture thumbs up/down signals from users? This is the fastest way to build the 30-query evaluation set and detect retrieval failures in production.
5. **On-premises requirement:** If data cannot leave your infrastructure, OpenAI embeddings are off the table — evaluate `nomic-embed-text` (self-hosted) and replace Claude with an on-prem model.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 13.5/17.0 (79%) |
| Evaluated | 2026-04-30 |
| Target duration | 109130 ms |
| Target cost | $0.1237 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent defines evaluation criteria (retrieval precision/recall targets, faithfulness requirement, latency budget) BEFORE proposing implementation | FAIL | The output's structure is: Corpus Profile → Chunking → Metadata → Embedding → Retrieval → Prompt → Cost → Freshness → Evaluation → Monitoring. Specific metrics (Precision@5 ≥ 80%, MRR ≥ 0.8, P95 latency ≤ 8s) appear in the final two sections, well after implementation decisions are made. No evaluation targets are stated upfront. |
| c2 | Agent analyses corpus properties (document types, volume, update frequency) before recommending chunking strategy | PASS | The first section is a 'Corpus Profile' table covering document types (Confluence Markdown/HTML, PDF runbooks), volume (2,500 docs, ~800 MB, 12,000–18,000 estimated chunks), update frequency ('a few times per week'), language, content structure, and query pattern. This precedes the Chunking Configuration section. |
| c3 | Agent recommends evaluating embedding models on a 20-query test set from actual user queries — not choosing by benchmark alone | PASS | 'Before committing: Run the 20-query evaluation below.' The protocol specifies 'Select 10 procedural queries and 10 ownership queries representative of real user behaviour', manually identify relevant chunks, measure Precision@5 and Recall@5, and switch to voyage-code-2 if below target. |
| c4 | Agent addresses citation requirements — every generated answer must reference source documents | PASS | Prompt template includes 'For every factual claim, include a citation in the format [Source: document name, section].' The metadata schema includes source_url. Output states 'Make citations clickable links to source_url. This is the most important trust signal for your users.' Example citation rendered is shown. |
| c5 | Agent defines a freshness/rebuild strategy given the weekly update cadence | PASS | Dedicated 'Freshness Strategy' section: Confluence webhook re-indexes changed pages within 1 hour, weekly PDF hash scan, SHA-256 change detection to re-embed only changed chunks, 180-day staleness flagging, and monthly full re-index as a safety net. |
| c6 | Agent includes fallback handling for model unavailability and cases where context is insufficient to answer | PARTIAL | Context-insufficient fallback is explicit in the prompt template: 'If the answer is not in the context, say: I don't have enough information to answer this question. Try searching Confluence directly or contact the relevant team.' Model unavailability fallback is entirely absent from the output. |
| c7 | Agent raises a decision checkpoint before choosing a model (cost/quality trade-off needs stakeholder input given $500/month budget) | PARTIAL | Claude Sonnet 4.6 is selected without an explicit stakeholder decision checkpoint. The cost projection mentions 'You have room to move to Claude Opus if answer quality on complex procedural queries is insufficient — revisit after evaluation,' which acknowledges the tradeoff but does not frame it as a required decision before proceeding. |
| c8 | Agent separates retrieval evaluation from generation evaluation and specifies testing retrieval first | PARTIAL | Evaluation section has two explicit subsections: 'Retrieval (measure before touching generation)' and 'Generation (measure only after retrieval passes)' — directly addressing the ordering requirement. |
| c9 | Output covers all pipeline stages: chunking config, metadata schema, embedding selection, retrieval strategy, prompt template, and evaluation plan | PASS | All six stages are present as dedicated sections: 'Chunking Configuration', 'Metadata Schema', 'Embedding', 'Retrieval Configuration', 'Prompt Template', and 'Evaluation Targets'. |
| c10 | Output's chunking strategy distinguishes between Markdown/HTML Confluence pages and PDF runbooks, acknowledging that PDFs need OCR or layout-aware extraction before chunking | PASS | Chunking section has separate subsections for 'Confluence pages (Markdown/HTML)' and 'PDF runbooks'. OCR is raised in Open Question #3: 'Scanned PDFs need a preprocessing step (Tesseract or AWS Textract) before chunking.' |
| c11 | Output proposes specific chunk size and overlap values (e.g. 512 tokens, 10-20% overlap) with reasoning tied to the corpus content (procedural runbooks vs reference documentation), not generic defaults | PASS | Confluence: 512-token target, 768 hard cap, 64-token overlap. PDFs: 512-token target, 640 hard cap, 15% overlap. Rationale explicitly tied to query types: 'Ownership queries are answered by single-sentence facts — small chunks retrieve them precisely. Procedural queries need step sequences intact.' |
| c12 | Output's retrieval design addresses ownership/team queries (e.g. 'which team owns X') via metadata filtering or hybrid retrieval — pure vector similarity will not reliably answer these | PASS | 'Ownership queries contain exact service names → BM25 keyword search excels.' Metadata filters at query time: service_name and team_owner filters applied when matched. Hybrid RRF combining semantic + BM25. team_owner and service_name flagged as 'highest-value metadata fields for your query types.' |
| c13 | Output's monthly cost calculation breaks down embedding cost (one-time + weekly re-embed of changed docs) plus per-query LLM generation cost, with a number that fits within the $500/month ceiling for the projected query volume | PASS | Cost Projection table: embeddings ~$0.05/month, generation $90/month at 200 queries/day to $495/month at 1,100 queries/day. One-time initial indexing cost of $0.18 stated. '$500/month cap. You have room to move to Claude Opus' confirms the budget fit is explicit. |
| c14 | Output's prompt template includes a citation instruction (e.g. 'cite source document and section after each claim') and the response schema includes a citations array linking to source URLs or runbook IDs | PASS | Prompt template: 'For every factual claim, include a citation in the format [Source: document name, section].' Chunk context template includes source_url field. 'Make citations clickable links to source_url.' Rendered example: '[Payments Service Runbook > Rollback Steps, p. 3]'. |
| c15 | Output specifies an incremental indexing strategy (only re-embed changed Confluence pages or PDFs) rather than full re-indexing weekly, given the 800MB corpus and few-times-weekly update cadence | PASS | Metadata field content_hash: 'SHA-256 of chunk text — Change detection — only re-embed modified chunks.' Freshness strategy: 'Only re-embed chunks whose parent document changed.' Confluence webhook fires within 1 hour of modification; PDF weekly scan compares file hashes. |
| c16 | Output's evaluation plan lists at least 10-20 example queries drawn from the prompt's domain (rollback procedures, service ownership) with expected source documents, not just abstract metrics | FAIL | The evaluation protocol instructs to 'Select 10 procedural queries and 10 ownership queries' and 'Manually identify the 3–5 chunks that should be returned for each,' but the output does not actually list any example queries or map them to expected source documents. Only abstract metric targets (Precision@5, MRR) are given. |
| c17 | Output names specific embedding model candidates (e.g. text-embedding-3-small, voyage-3, BGE) and a specific generation model, with a justification tying each to the cost budget | PARTIAL | Embedding: text-embedding-3-small (primary, cost $0.02/1M tokens) and voyage-code-2 (alternative for technical docs). Generation: Claude Sonnet 4.6 with cost breakdown ($90–$495/month). Cost justification is present. Ceiling is PARTIAL. |
| c18 | Output addresses access control — internal docs may have permissions, and a RAG system that returns chunks the asking user shouldn't see is a leak vector | PARTIAL | Open Question #2: 'Do support and engineering teams have the same access rights to all 2,500 documents? If not, the retrieval layer needs to filter by user permissions before returning chunks.' Raised as a risk but no design solution provided. Ceiling is PARTIAL. |

### Notes

The output is comprehensive and technically strong across most pipeline dimensions — chunking strategy, metadata schema, hybrid retrieval, cost projection, and freshness handling are all well-executed. The two notable failures are: (1) evaluation criteria are defined at the end rather than as design constraints upfront (c1), and (2) the evaluation plan instructs users to create a query test set but doesn't populate it with actual domain-specific example queries and expected sources (c16). Model unavailability handling is also absent. The output narrowly misses the 80% threshold at 79.4%, primarily due to the ordering of evaluation criteria and the missing concrete test query examples.
