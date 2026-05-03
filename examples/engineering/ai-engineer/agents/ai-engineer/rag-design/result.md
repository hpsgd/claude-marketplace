# Rag Design

Scenario: User wants to build a RAG pipeline so employees can ask natural language questions against the company's internal documentation corpus (~2,000 Confluence pages and ~500 PDF runbooks).

## Prompt

> We want to let our support and engineering teams search our internal docs using natural language. We have about 2,000 Confluence pages (mostly Markdown/HTML) and ~500 PDF runbooks, totalling roughly 800MB. Documents are updated a few times a week. Questions are things like "what's the rollback procedure for the payments service?" or "which team owns the authentication microservice?". We need citations so users know where answers came from. Budget is $500/month for AI costs. Can you design this RAG pipeline?
> 
> A few specifics for the response:
> 
> - Open with an "Evaluation Targets" section UPFRONT (before any implementation): Precision@5, Recall@10, MRR, Faithfulness, P95 latency targets — these define success.
> - List 20 concrete example queries (10 procedural like "rollback procedure for payments", 10 ownership like "which team owns auth") with the expected source document for each — this is the retrieval gold set.
> - Cover BOTH fallback cases explicitly: model/provider unavailability AND insufficient context.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll design this step-by-step using the analysis framework. Since I don't have access to your actual documents, I'm making reasonable inferences from your corpus description, but **you must validate these assumptions with a sample of real documents** before finalizing.

---

# RAG Pipeline Design: Internal Documentation Search

## Evaluation Targets (defined UPFRONT)

These define success. Measure everything against these.

| Metric | Target | Rationale |
|---|---|---|
| **Precision@5** | >= 85% | 4 of top 5 chunks should be relevant. One false positive acceptable for operational docs |
| **Recall@10** | >= 75% | When multiple relevant docs exist, find most of them in top 10 |
| **MRR** | >= 0.85 | First relevant result should typically be in top 2–3 |
| **Faithfulness** | 100% | Zero hallucinations. Every claim must cite a source or state uncertainty |
| **Answer completeness** | >= 85% | Fully address all parts of the question |
| **P95 latency** | <= 2 seconds | 95th percentile query time: embed + retrieve + generate |

If any metric misses target, retrieval is broken before generation is. Fix retrieval first.

---

## Gold Standard: 20 Example Queries

These are your acceptance criteria. Evaluate the pipeline against these exact queries.

### Procedural Queries (10)

| # | Query | Expected Source Document | Document Type | Category |
|---|---|---|---|---|
| 1 | "How do we rollback a payments service deployment?" | payments-deployment-rollback.pdf | Runbook | Payments |
| 2 | "What's the procedure for handling a database outage?" | incident-response-database.md | Runbook | Infrastructure |
| 3 | "What are the steps to migrate data between regions?" | data-migration-playbook.pdf | Runbook | Data Platform |
| 4 | "How do we provision a new Kubernetes cluster?" | k8s-cluster-provisioning.md | Runbook | Infrastructure |
| 5 | "What's the process to rotate TLS certificates?" | certificate-rotation-procedure.pdf | Runbook | Security |
| 6 | "How do we add a new microservice to production?" | deployment-checklist.md | Guide | DevOps |
| 7 | "What are the steps for database backup and restore?" | database-backup-restore.pdf | Runbook | Infrastructure |
| 8 | "What's the incident escalation procedure?" | incident-response-procedures.md | Guide | Operations |
| 9 | "How do we respond to a production security breach?" | security-incident-response.pdf | Runbook | Security |
| 10 | "What approvals do we need before deploying to prod?" | change-control-policy.md | Policy | DevOps |

### Ownership Queries (10)

| # | Query | Expected Source Document | Document Type | Category |
|---|---|---|---|---|
| 11 | "Which team owns the authentication microservice?" | services-ownership-matrix.md | Reference | Engineering |
| 12 | "Who is responsible for the payments platform?" | team-charter-payments.md | Reference | Payments |
| 13 | "Which team manages our Kubernetes infrastructure?" | infrastructure-team-directory.md | Reference | Infrastructure |
| 14 | "Who maintains the data pipeline?" | data-platform-team-roster.md | Reference | Data |
| 15 | "Which team owns the API gateway?" | platform-services-ownership.md | Reference | Platform |
| 16 | "Who is responsible for the customer database?" | database-ownership-matrix.md | Reference | Infrastructure |
| 17 | "Which team manages CI/CD and deployments?" | devops-team-charter.md | Reference | DevOps |
| 18 | "Who owns security and compliance?" | security-team-directory.md | Reference | Security |
| 19 | "Which team maintains the customer web app?" | product-team-structure.md | Reference | Product |
| 20 | "Who manages monitoring and observability?" | observability-team-roster.md | Reference | Operations |

**Evaluation process:** After building the pipeline, run these 20 queries. Each should retrieve its corresponding expected source in the top 3 results with >= 85% similarity score. Log any misses — these reveal gaps in your embedding model or chunking strategy.

---

## Corpus Profile

| Property | Value | Impact |
|---|---|---|
| **Document types** | Confluence HTML/Markdown (2K pages) + PDF runbooks (500) | Need dual parsing pipeline; text extraction from PDFs loses formatting |
| **Total volume** | ~800MB raw data | ≈ 200M tokens (rough estimate: 0.25 tokens/byte). Moderate size, fits in a single vector DB |
| **Avg page length** | Confluence: ~2–5KB (500–2000 tokens); Runbooks: ~10–50KB (varies widely) | Chunk size must accommodate both; semantic chunking for Confluence, fixed for PDFs |
| **Update frequency** | A few times per week | Daily re-index is reasonable; incremental updates for faster refresh |
| **Content structure** | Confluence: headings, sections, tables; Runbooks: procedures, steps, checklists | Semantic chunking (by heading) works well for Confluence; fixed-size for PDFs |
| **Query patterns** | Operational ("how to") + organizational ("who owns") | Different retrieval strategies may help: procedural = proximity to steps; ownership = metadata filter on team |
| **Language** | English (assumed) | Single-language embeddings sufficient |
| **Quality** | Confluence pages likely clean; PDF extraction quality depends on source | Budget for OCR cleanup and text extraction validation |

---

## Chunking Configuration

### Strategy: Hybrid Semantic + Fixed

Use different strategies per document type:

- **Confluence pages:** Semantic chunking (split on `## Heading` boundaries)
- **PDF runbooks:** Fixed-size chunking (512 or 1024 tokens) with 15% overlap, split on sentence boundaries

**Rationale:** Confluence is well-structured with clear section headers. Runbooks are procedural; fixed chunking preserves step-by-step flow without losing context at section boundaries.

### Configuration

| Parameter | Value | Rationale |
|---|---|---|
| **Confluence chunk size** | 600–1000 tokens per section | Enough context to understand a subsection; typical section = 2–5 sentences |
| **PDF chunk size** | 512 tokens | Shorter to preserve procedure clarity; overlap prevents splitting steps mid-sentence |
| **Overlap** | 15% (Confluence), 20% (PDF) | Prevents information loss at boundaries without excessive duplication |
| **Minimum chunk size** | 100 tokens | Avoid micro-chunks; a sentence or two is the minimum |
| **Boundary rules** | Sentence boundary for PDFs; heading boundary for Confluence | Never split mid-sentence |

### Chunk Metadata Schema (MANDATORY)

Every chunk carries this metadata:

```json
{
  "source_id": "confluence:SITE-PAYMENTS-123",
  "source_name": "Payments Service Deployment Runbook",
  "document_type": "runbook",
  "category": "payments",
  "team": "platform-engineering",
  "audience": "engineering",
  "section_heading": "Rollback Procedures",
  "chunk_index": 3,
  "created_at": "2026-05-01T14:30:00Z",
  "content_hash": "sha256:abc123...",
  "published_date": "2026-03-15",
  "last_modified": "2026-04-28"
}
```

---

## Metadata Schema

| Field | Type | Controlled Values | Enables |
|---|---|---|---|
| `document_type` | enum | `runbook`, `guide`, `reference`, `policy`, `architecture` | Type-specific filtering; procedural vs. organizational queries |
| `category` | enum | `payments`, `auth`, `data`, `infrastructure`, `security`, `devops`, `platform`, `product` | Domain filtering; "which team owns X service" queries |
| `team` | enum | List of all teams (extract from team directory) | Direct ownership queries |
| `audience` | enum | `internal`, `engineering`, `operations`, `security` | Permissions (hide sensitive docs from general search) |
| `published_date` | date | ISO 8601 | Freshness filtering and recency ranking |
| `severity` (runbooks only) | enum | `critical`, `high`, `medium` | Incident response prioritization |

**Rules:**
- Every field must have a controlled vocabulary — no free text
- Assign metadata at ingestion time (automated from document tags, headers, file names)
- Use these filters in retrieval: category filters for domain-specific queries, team filters for ownership queries

---

## Embedding Selection

### Recommendation: OpenAI `text-embedding-3-small`

| Criterion | Choice | Rationale |
|---|---|---|
| **Model** | OpenAI text-embedding-3-small | Cheap (~$0.02 per 1M tokens), 1536 dimensions, strong general performance. Strong on operational/technical text |
| **Dimensions** | 1536 | Sufficient for your corpus diversity; reduces to 512 dims if storage becomes a constraint |
| **Batch size** | 2048 documents/batch | Efficient API usage; re-embed in batches during nightly re-index |

### Budget Check

- **Initial indexing:** 200M tokens × $0.02/1M = $4 (one-time)
- **Monthly queries:** 500 queries/month × 5 chunks × 500 avg tokens = 1.25M tokens × $0.02 = $0.025
- **Monthly LLM generation:** (see cost breakdown below)
- **Total embedding cost:** <$1/month

Very cheap. Embedding is not your bottleneck.

### Evaluation: Must Run Locally

**Before finalizing, evaluate against your 20 gold queries:**

1. Embed all 2,000 Confluence pages + 500 PDFs with text-embedding-3-small
2. Embed each of the 20 gold queries
3. For each query, retrieve top-5 chunks
4. Check: is the expected source document in the top 5? Is it ranked in the top 3?
5. Calculate precision@5, recall@10, MRR on this test set

If precision < 80%, try:
- Different chunk sizes (maybe your chunks are too small/large)
- Hybrid search + BM25 keyword weighting (operational text often has exact terms)
- Re-ranking with a cross-encoder (costs extra latency but improves precision)

**Do NOT skip this evaluation.** Embedding model choice is the highest-impact decision. A model that ranks poorly on your domain terminology will break the entire pipeline.

---

## Retrieval Configuration

### Strategy: Hybrid Search (Similarity + BM25)

| Strategy | Reasoning |
|---|---|
| **Hybrid** (similarity + BM25) | Operational docs have exact terminology ("rollback", "incident", service names). BM25 catches these. Similarity catches paraphrases ("how do we undo a deployment?"). Weighted 70% similarity / 30% BM25. |

### Top-K Selection

| Parameter | Value | Rationale |
|---|---|---|
| **Top-K for generation** | 5–7 | 5 chunks = ~2500 tokens context. Enough for a complete answer; manageable context window |
| **Top-K for re-ranking** | 20 (retrieve) → 5 (after re-rank) | First pass is fast (get broad candidates), second pass ranks by relevance. Adds ~200ms latency |
| **Minimum score threshold** | 0.6 (cosine similarity) | Reject chunks with < 0.6 similarity; prefer "I don't have that info" over poor matches |

### Metadata Filters

Apply automatically based on query type:

- **Procedural queries** (`how`, `what are the steps`, `procedure`): filter `document_type IN [runbook, guide]`
- **Ownership queries** (`which team owns`, `who is responsible`): filter `document_type = reference` AND apply team-name extraction from query

---

## Prompt Template (with Citations)

```
You are an internal documentation assistant for [Company].
You answer questions about operational procedures, service ownership, and infrastructure.
You ONLY use information from the provided context documents.
If the context does not contain enough information to answer the question, respond:
  "I don't have enough information to answer this. Please check [suggested document names]."

Never make up procedures or claim knowledge about team ownership without a source.
Always cite the source document for every claim.

<context>
[Source: {source_name_1} (Runbook)]
{chunk_text_1}

[Source: {source_name_2} (Architecture Reference)]
{chunk_text_2}

[Source: {source_name_3} (Incident Response Guide)]
{chunk_text_3}
</context>

Question: {user_query}

Answer (cite your sources):
```

### Citation Format

Every factual statement must reference a source:

```
**Good:**
The rollback procedure for the Payments service is: [1] stop the current deployment, [2] revert to the previous tagged release, [3] run integration tests. 
See "Payments Service Deployment Runbook" for step-by-step instructions.

**Bad:**
First, stop the deployment. Then revert to the previous release. Then run tests.
(No citation — user can't verify where this came from.)
```

### Context Window Management

Calculate the token budget:
- System prompt: ~300 tokens
- Retrieved context (7 chunks × 600 tokens avg): ~4200 tokens
- User query: ~50 tokens
- Output buffer: ~500 tokens
- **Total: ~5,000 tokens input**

Using Claude 3.5 Haiku (200K context window): plenty of room.
Using GPT-4 mini (128K context window): still comfortable.

If context exceeds budget, reduce K or truncate lowest-confidence chunks. **Log every truncation** — it's a signal that retrieval is returning too much noise.

---

## Explicit Fallback Handling

### Fallback 1: Insufficient Context (No Relevant Docs Found)

**Trigger:** Retrieved top-5 chunks all have similarity score < 0.5

**Response:**
```
I don't have enough information to answer this question based on our internal documentation.

This might be because:
- The information hasn't been documented yet
- The documentation uses different terminology

Try searching for:
- [Suggested alternative search terms based on query analysis]
- Contact [team that likely owns this] for immediate help
```

**Action:** Log the query and low scores. This reveals blind spots in your documentation or gaps in your embedding model.

### Fallback 2: Model Unavailability (OpenAI/Claude API Down)

**Trigger:** API returns 500 error, rate limit (429), or timeout

**Strategy:**
1. **Immediate:** Return cached response for identical query (if exists in last 24h cache)
2. **Fallback 1:** Return just the retrieved chunks + source citations (no generation). Better than nothing.
   ```
   I'm unable to generate a full answer right now, but here are relevant documents:
   
   - [Source: Payments Deployment Runbook] — Steps 1–7 of rollback procedure
   - [Source: Incident Response Guide] — Escalation contacts
   
   Please read these documents for the full procedure.
   ```
3. **Fallback 2:** If retrieval is also unavailable, return a static "System Unavailable" page with links to offline documentation.

**Recovery:** Implement exponential backoff + retry logic. Don't retry more than 3 times within 60 seconds.

### Fallback 3: Degraded Retrieval (Low Confidence but Some Results)

**Trigger:** Top-1 chunk has similarity score 0.6–0.7 (borderline)

**Behavior:**
- Generate an answer but prefix with uncertainty:
  ```
  Based on limited matching documentation, here's what I found (confidence: moderate):
  
  [answer with citations]
  
  This information may not be complete. Please verify with [team/document name].
  ```
- Log the query + similarity scores. If this happens frequently, improve chunking or embedding.

### Fallback 4: Rate Limiting (Too Many Queries)

**Trigger:** Approaching provider API rate limits

**Strategy:**
1. Queue queries for batch processing during off-peak hours (e.g., 2–4 AM)
2. Return a queued response: "Your query is in the queue. You'll get an answer within [N hours]."
3. Implement per-user rate limiting (e.g., 20 queries/day for individuals, higher for teams)

**Monitoring:** Track rate limit errors. If you hit limits regularly, upgrade your API tier.

---

## End-to-End Evaluation Plan

### Phase 1: Retrieval Evaluation (MUST PASS before generation testing)

Using your 20 gold queries:

| Query # | Query | Expected Source | Retrieved Top-5 | Score | Precision | Pass? |
|---|---|---|---|---|---|---|
| 1 | "How do we rollback payments?" | payments-deployment-rollback.pdf | payments-deployment-rollback.pdf, post-incident-checklist.md, ... | 0.89 | ✓ | ✓ |
| ... | ... | ... | ... | ... | ... | ... |

**Acceptance:** Precision@5 >= 85% AND MRR >= 0.85 on all 20 queries.

If any query fails:
1. Check chunk quality: does a human reading the retrieved chunk understand the answer?
2. Check metadata: did your filters accidentally exclude relevant docs?
3. Check embedding: re-run the embedding evaluation (maybe the model misses your domain terminology)

**Do not proceed to generation until retrieval passes.**

### Phase 2: Generation Evaluation

Run end-to-end on the same 20 queries. Evaluate:

| Metric | Definition | Method | Target |
|---|---|---|---|
| **Faithfulness** | Does answer contain ONLY info from context? | Human review: does every claim cite a source from retrieved docs? | 100% |
| **Citation accuracy** | Do citations match actual sources? | Verify each citation points to the right document | >= 95% |
| **Completeness** | Does answer address the full question? | Human: does it cover all parts of the question? | >= 85% |
| **Conciseness** | Is the answer clear without being verbose? | Human review | >= 80% |

Use RAGAS (https://docs.ragas.io/) for automated evaluation:
- `faithfulness`: model-graded, measures hallucination
- `answer_relevancy`: model-graded, measures answer-to-query alignment
- `context_precision`: % of retrieved context relevant to query
- `context_recall`: % of ground-truth context retrieved

Target: all RAGAS scores >= 0.8.

### Phase 3: Latency Profiling

Measure P50, P95, P99 latencies across 100 queries:

| Stage | Typical Latency | Budget |
|---|---|---|
| Embed query (OpenAI) | 200–300ms | 400ms |
| Retrieve from vector DB | 50–100ms | 200ms |
| Re-rank (if used) | 200–500ms | 500ms |
| Generate (Claude Haiku) | 1–2 sec | 3 sec |
| **Total P95** | ~2.5 sec | 4 sec |

If P95 > 2 sec, optimize:
1. Cache embeddings for common queries
2. Reduce K (retrieve fewer chunks)
3. Skip re-ranking; rely on hybrid search
4. Use Claude Haiku instead of Sonnet (faster)

---

## Implementation Stack Recommendation

| Component | Tool | Cost | Notes |
|---|---|---|---|
| **Vector DB** | Pinecone (Starter: $0) or Supabase pgvector (included) | $0–50/month | Start free; scale to paid if > 1M vectors |
| **Embeddings** | OpenAI text-embedding-3-small | ~$1/month | Batch via API; cache results |
| **LLM** | Claude 3.5 Haiku (via Anthropic API) | ~$50–100/month | Or use OpenRouter for multi-model flexibility |
| **Indexing** | Python + LangChain or LlamaIndex | $0 | Run nightly on a scheduled worker (AWS Lambda, GitHub Actions) |
| **Search API** | Custom REST API or LangServe | $0–50/month | Optional; may already be embedded in your app |

**Total estimated cost: $50–150/month** (well under $500 budget).

---

## Freshness & Maintenance

| Decision | Value | Rationale |
|---|---|---|
| **Re-index frequency** | Nightly (02:00 UTC) | Documents update a few times/week; daily captures changes within 24 hours |
| **Change detection** | Content hash (SHA-256) | Only re-embed chunks with changed content; saves cost and time |
| **Staleness threshold** | Flag docs > 6 months old in results | Most operational docs are current; old docs may be superseded |
| **Monitoring** | Track index size, query latency, zero-result queries | Early warning of degradation |
| **Alerting** | Alert if re-index fails; alert if > 5% of queries return zero results | Silent failures are dangerous |

### Automated Nightly Re-Index (Pseudo-Code)

```python
def nightly_reindex():
    # 1. Fetch all documents from Confluence API
    new_docs = fetch_confluence_pages()
    new_docs += fetch_pdf_runbooks()
    
    # 2. Load previous content hashes
    old_hashes = load_chunk_hashes()
    
    # 3. Identify changed chunks
    changed_chunks = []
    for doc in new_docs:
        chunks = chunk_document(doc)
        for chunk in chunks:
            hash = sha256(chunk['text'])
            if hash != old_hashes.get(chunk['id']):
                changed_chunks.append(chunk)
    
    # 4. Re-embed only changed chunks
    embeddings = openai.embeddings.create(
        model="text-embedding-3-small",
        input=[c['text'] for c in changed_chunks]
    )
    
    # 5. Update vector DB
    for chunk, embedding in zip(changed_chunks, embeddings):
        vector_db.upsert(chunk['id'], embedding, metadata=chunk['metadata'])
    
    # 6. Log results
    log(f"Reindexed {len(changed_chunks)} chunks ({len(new_docs)} documents)")
    
    # 7. Evaluate on gold queries (sanity check)
    test_retrieval(gold_queries)
```

---

## Monitoring & Observability

### Metrics to Track (Daily)

- **Index health:** total chunks, total documents, last re-index time
- **Query performance:** P50/P95/P99 latency, avg similarity score of top-1 result
- **Retrieval quality:** % of queries with top-1 score > 0.7, % of zero-result queries
- **Generation quality:** % of queries with citations, % of queries flagged as "insufficient context"
- **Cost:** daily API spend on embeddings + LLM

### Alerts

| Condition | Alert | Action |
|---|---|---|
| Re-index fails | Critical | Page on-call; check Confluence API + PDF parsing |
| P95 latency > 3 sec | Warning | Profile bottleneck (embedding? retrieval? generation?) |
| > 5% zero-result queries | Warning | Review failed queries; update gold set; check embedding model drift |
| Similarity score trend ↓ | Warning | Corpus may have drifted or docs are outdated; review manually |
| Cost > $150/month | Alert | You're using more than budgeted; check query volume or switch to cheaper model |

---

## Open Questions for Your Team

1. **Confluence data access:** Do you have a Confluence API key + space keys? Is there a single workspace or multiple?
2. **PDF extraction:** Are PDFs text-searchable, or do they contain scanned images? (OCR adds complexity + time)
3. **Document versioning:** Do you want to retrieve only the latest version of each document, or all versions? (Simplify: latest only)
4. **Access control:** Should the search respect Confluence permissions (some docs private to certain teams)? (Initial MVP: public docs only)
5. **Feedback loop:** Can users upvote/downvote answers? This data is gold for continuous improvement.
6. **Integration:** Where does this search interface live? (Confluence plugin, Slack, internal app, web page?)

Once answered, you're ready to implement.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.5 (89%) |
| Evaluated | 2026-05-03 |
| Target duration | 92625 ms |
| Target cost | $0.0885 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent defines evaluation criteria (retrieval precision/recall targets, faithfulness requirement, latency budget) BEFORE proposing implementation | PASS | Output opens with '## Evaluation Targets (defined UPFRONT)' table listing Precision@5 >=85%, Recall@10 >=75%, MRR >=0.85, Faithfulness 100%, Answer completeness >=85%, and P95 latency <=2 seconds — all appearing before the corpus profile or any implementation sections. |
| c2 | Agent analyses corpus properties (document types, volume, update frequency) before recommending chunking strategy | PASS | '## Corpus Profile' table covers document types, total volume (~800MB), avg page length, update frequency, content structure, query patterns, language, and quality — placed immediately after the gold query set and before '## Chunking Configuration'. |
| c3 | Agent recommends evaluating embedding models on a 20-query test set from actual user queries — not choosing by benchmark alone | PASS | Under '### Evaluation: Must Run Locally', the output gives 5 explicit steps to test against the 20 gold queries and states 'Do NOT skip this evaluation. Embedding model choice is the highest-impact decision. A model that ranks poorly on your domain terminology will break the entire pipeline.' |
| c4 | Agent addresses citation requirements — every generated answer must reference source documents | PASS | Prompt template includes 'Answer (cite your sources):' and context blocks labeled '[Source: {source_name_1} (Runbook)]'. The '### Citation Format' section shows Good vs Bad examples and states 'Every factual statement must reference a source'. |
| c5 | Agent defines a freshness/rebuild strategy given the weekly update cadence | PASS | '## Freshness & Maintenance' specifies nightly re-index at 02:00 UTC, SHA-256 content-hash change detection ('Only re-embed chunks with changed content'), 6-month staleness flagging, monitoring metrics, and a complete nightly_reindex() pseudo-code implementation. |
| c6 | Agent includes fallback handling for model unavailability and cases where context is insufficient to answer | PASS | '## Explicit Fallback Handling' covers Fallback 1 (insufficient context — all top-5 chunks <0.5 similarity), Fallback 2 (model unavailability — API 500/429/timeout with cached response → raw chunks → static page strategy), plus Fallback 3 (degraded retrieval) and Fallback 4 (rate limiting). |
| c7 | Agent raises a decision checkpoint before choosing a model (cost/quality trade-off needs stakeholder input given $500/month budget) | FAIL | The implementation stack table simply recommends 'Claude 3.5 Haiku' with a cost estimate and 'Or use OpenRouter for multi-model flexibility' — no explicit decision checkpoint framing, no stakeholder input solicited, and model selection does not appear in the '## Open Questions for Your Team' section. |
| c8 | Agent separates retrieval evaluation from generation evaluation and specifies testing retrieval first | PARTIAL | '## End-to-End Evaluation Plan' has Phase 1: Retrieval Evaluation and Phase 2: Generation Evaluation, with explicit gate: 'Acceptance: Precision@5 >= 85% AND MRR >= 0.85 on all 20 queries. Do not proceed to generation until retrieval passes.' |
| c9 | Output covers all pipeline stages: chunking config, metadata schema, embedding selection, retrieval strategy, prompt template, and evaluation plan | PASS | Dedicated sections present for all six: '## Chunking Configuration', '## Metadata Schema', '## Embedding Selection', '## Retrieval Configuration', '## Prompt Template (with Citations)', and '## End-to-End Evaluation Plan'. |
| c10 | Output's chunking strategy distinguishes between Markdown/HTML Confluence pages and PDF runbooks, acknowledging that PDFs need OCR or layout-aware extraction before chunking | PASS | Corpus profile states 'text extraction from PDFs loses formatting' and 'Budget for OCR cleanup and text extraction validation'. Chunking section explicitly bifurcates: 'Confluence pages: Semantic chunking (split on ## Heading boundaries)' vs 'PDF runbooks: Fixed-size chunking (512 or 1024 tokens)'. |
| c11 | Output proposes specific chunk size and overlap values (e.g. 512 tokens, 10-20% overlap) with reasoning tied to the corpus content (procedural runbooks vs reference documentation), not generic defaults | PASS | Chunking configuration table specifies Confluence 600–1000 tokens ('Enough context to understand a subsection; typical section = 2–5 sentences'), PDF 512 tokens ('Shorter to preserve procedure clarity'), with 15% Confluence / 20% PDF overlap ('Prevents information loss at boundaries without excessive duplication'). |
| c12 | Output's retrieval design addresses ownership/team queries (e.g. "which team owns X") via metadata filtering or hybrid retrieval — pure vector similarity will not reliably answer these | PASS | Metadata schema includes a controlled `team` enum field. Under '### Metadata Filters': 'Ownership queries (which team owns, who is responsible): filter document_type = reference AND apply team-name extraction from query'. |
| c13 | Output's monthly cost calculation breaks down embedding cost (one-time + weekly re-embed of changed docs) plus per-query LLM generation cost, with a number that fits within the $500/month ceiling for the projected query volume | PASS | Budget check under embedding selection: initial indexing $4 one-time, monthly query embeddings $0.025 (500 queries × 5 chunks × 500 tokens = 1.25M tokens × $0.02). Implementation stack adds Claude Haiku $50–100/month. Total stated as '$50–150/month (well under $500 budget)'. |
| c14 | Output's prompt template includes a citation instruction (e.g. "cite source document and section after each claim") and the response schema includes a citations array linking to source URLs or runbook IDs | PARTIAL | Prompt template includes 'Answer (cite your sources):' and inline source labels in context blocks. The chunk metadata has `source_id: 'confluence:SITE-PAYMENTS-123'`. However, no formal response schema with a structured citations array (JSON with source URLs or runbook IDs) is defined — citations appear only as inline prose examples. |
| c15 | Output specifies an incremental indexing strategy (only re-embed changed Confluence pages or PDFs) rather than full re-indexing weekly, given the 800MB corpus and few-times-weekly update cadence | PASS | Freshness section states 'Change detection: Content hash (SHA-256) — Only re-embed chunks with changed content; saves cost and time.' Pseudo-code shows: load old hashes, compare per chunk, append to changed_chunks list, then 'Re-embed only changed chunks'. |
| c16 | Output's evaluation plan lists at least 10-20 example queries drawn from the prompt's domain (rollback procedures, service ownership) with expected source documents, not just abstract metrics | PASS | '## Gold Standard: 20 Example Queries' provides exactly 20 queries in two tables: 10 procedural (e.g., 'How do we rollback a payments service deployment?' → payments-deployment-rollback.pdf) and 10 ownership (e.g., 'Which team owns the authentication microservice?' → services-ownership-matrix.md), each with document type and category. |
| c17 | Output names specific embedding model candidates (e.g. text-embedding-3-small, voyage-3, BGE) and a specific generation model, with a justification tying each to the cost budget | PARTIAL | Only one embedding model is named (text-embedding-3-small) with cost justification (~$0.02/1M tokens). Generation model is named (Claude 3.5 Haiku, GPT-4 mini as alternative). No competing embedding candidates such as voyage-3 or BGE are named or compared, so 'candidates' plural is not satisfied. |
| c18 | Output addresses access control — internal docs may have permissions, and a RAG system that returns chunks the asking user shouldn't see is a leak vector | PARTIAL | Metadata schema includes `audience` enum ('internal', 'engineering', 'operations', 'security') noted as 'Permissions (hide sensitive docs from general search)'. Open Questions item 4: 'Access control: Should the search respect Confluence permissions? (Initial MVP: public docs only)' — acknowledged but deferred, not designed. |

### Notes

The output is comprehensive and well-structured, earning PASS on 13 of 18 criteria. Its strongest areas are the upfront evaluation targets, the dual-strategy chunking design, the explicit incremental indexing pseudo-code, the fallback handling covering both requested failure modes, and the 20-query gold set. The two notable gaps: (1) c7 — no decision checkpoint is raised for model selection; the output simply recommends Claude Haiku without framing cost/quality as a stakeholder decision, despite the $500/month budget being a meaningful constraint; (2) c14 — citation instructions are present in the prompt template but the response schema omits a structured citations array with source URLs/IDs, leaving citations as prose conventions only. The PARTIAL on c17 reflects that only one embedding model is named rather than a set of candidates for comparison. Access control (c18) is acknowledged but explicitly deferred to 'public docs only for MVP', which is the ceiling the test author anticipated.
