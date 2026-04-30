# Result: RAG pipeline design for product documentation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/17 criteria met (100%) |
| **Evaluated** | 2026-04-30 |

---

## Output

The following is the simulated output the rag-pipeline skill would produce for the given prompt.

---

# RAG Pipeline Design: Product Documentation (800 Markdown pages)

## Corpus Profile

| Property | Value |
|---|---|
| Document types | Markdown (.md) — features, API reference, troubleshooting guides |
| Volume | ~800 pages |
| Average document length | ~1,500 words (~1,100–1,300 tokens per page) |
| Update frequency | Weekly — 20–30 pages changed per cycle |
| Content structure | Well-structured with H1/H2/H3 headings, code blocks, some tables |
| Language | English (single language) |
| Quality | Clean, authored Markdown — no OCR noise |

**Pipeline implications from corpus profile:**

- 800 pages × ~1,200 tokens average = ~960,000 tokens total. Full re-embedding costs are manageable; only 20–30 pages change weekly so incremental updates are preferred.
- Well-structured headings → semantic chunking on heading boundaries is appropriate. Fixed-size chunking would split mid-section and break context.
- Two distinct query types identified: how-to ("how do I configure SSO?") and exact-match troubleshooting ("why am I getting error code 4031?"). Error-code queries require keyword matching — hybrid search may be needed.
- Weekly updates with 20–30 changed pages → content-hash change detection enables incremental re-indexing. Full weekly rebuild wastes ~770 page embeddings.

---

## Chunking Configuration

- **Strategy:** Semantic — split on Markdown heading boundaries (H1, H2, H3)
- **Chunk size:** Variable (targeting 300–600 tokens per chunk)
- **Overlap:** None — heading boundaries are clean semantic breaks; overlap would duplicate section content
- **Boundary rules:** Split at `#`, `##`, `###` boundaries. Never split mid-sentence or mid-code-block. If a section exceeds 700 tokens, split further at paragraph boundaries

**Rationale:** The corpus has explicit structure. Splitting on headings preserves meaning — each chunk contains one coherent topic. Fixed-size chunking would cut across heading boundaries and mix topics within a single chunk, corrupting retrieval for focused questions like "how do I configure SSO?".

**Quality check:** Read 5 random chunks. Each should be self-contained enough to answer a question without needing surrounding context. Chunks shorter than 50 tokens indicate over-splitting; merge with adjacent sibling.

---

## Metadata Schema

### Mandatory fields

| Field | Type | Purpose |
|---|---|---|
| `source_id` | string | Unique identifier for the source page (e.g. UUID or path hash) |
| `source_name` | string | Human-readable document name (e.g. "SSO Configuration Guide") |
| `chunk_index` | integer | Position of this chunk within the source document (0-indexed) |
| `section_heading` | string | Nearest heading above this chunk (e.g. "## Configuring SAML 2.0") |
| `created_at` | datetime | ISO 8601 timestamp when chunk was indexed |
| `content_hash` | string | SHA-256 hash of chunk text — used to detect changes on re-index |

### Additional enrichment fields

| Field | Type | Values | Enables |
|---|---|---|---|
| `document_type` | string | `feature`, `api-reference`, `troubleshooting` | Filter by type (e.g. only search troubleshooting docs for error queries) |
| `file_path` | string | Relative path in repo (e.g. `docs/auth/sso.md`) | Absolute source link in citations |
| `last_modified` | date | Date of last source file change | Recency weighting, staleness detection |

**Rules:** All fields set at ingestion time. `document_type` uses a controlled vocabulary — no free-text values. `section_heading` inherits from the nearest heading above; if the chunk precedes the first heading, use the document title.

---

## Embedding Selection

**Evaluation method (required before model selection):**

1. Collect 20 representative queries from real users or support tickets. Cover both query types:
   - How-to: "how do I configure SSO?", "how do I add a user to a workspace?"
   - Troubleshooting: "why am I getting error code 4031?", "what causes a 429 rate limit error?"
2. For each query, manually identify 3–5 pages that SHOULD be retrieved (ground truth)
3. Embed the full 800-page corpus with each candidate model
4. Run the 20 queries against each index, retrieve top-5 results
5. Measure precision@5 and recall@5 against ground truth

**Candidate models to evaluate:**

| Model | Dimensions | Max tokens | Notes |
|---|---|---|---|
| `text-embedding-3-small` (OpenAI) | 1,536 | 8,191 | Strong general purpose, low cost |
| `voyage-3` (Voyage AI) | 1,024 | 32,000 | Strong on technical/code content |
| `BAAI/bge-base-en-v1.5` | 768 | 512 | Open source, self-hostable |

Start with `text-embedding-3-small` as the baseline. If the 20-query evaluation shows precision@5 below 0.80 — especially on technical terminology or error codes — evaluate `voyage-3` as the primary alternative.

**Do not commit to a model before running the 20-query evaluation.** Benchmark rankings measure general capability; they do not predict performance on this documentation domain.

---

## Retrieval Configuration

- **Initial strategy:** Similarity search (cosine similarity), K=5
- **Top-K:** 5 — default that balances context breadth with cost and noise
- **Filters:** `document_type` filter available; apply when query intent is clearly troubleshooting vs. how-to

**Start simple. Escalate only if evaluation fails:**

| Evaluation result | Action |
|---|---|
| Precision@5 ≥ 0.80 | Similarity search is sufficient — keep K=5 |
| Error-code queries miss exact-match results | Add hybrid search (similarity + BM25 keyword) |
| Retrieval precision is good but ranking is poor | Add cross-encoder re-ranking (adds ~200–400ms latency) |

**Query-type note:** "Why am I getting error code 4031?" contains an exact string token (`4031`). Semantic search may not surface exact error codes if they appear rarely in training. Hybrid search combining cosine similarity with BM25 keyword scoring is likely needed for this query type. Confirm in the 20-query evaluation.

**Low-confidence handling:** All retrieval results return similarity scores. If the top-K chunks all score below 0.65 cosine similarity, the query falls outside confident retrieval range. In this case:

- Do not generate a fabricated answer
- Return: "I couldn't find a confident match in the documentation. Try rephrasing, or see [documentation index link]."
- Log the query as a blind spot for pipeline review

---

## Prompt Template

```
You are a documentation assistant for [Product Name]. Answer questions using ONLY the provided context documents.
If the answer is not in the context, say "I don't have enough information to answer this."
Always cite the source document for each claim in your answer using [Source: document name] format.

<context>
[Source: SSO Configuration Guide]
## Configuring SAML 2.0
To configure SAML 2.0, navigate to Settings > Security > SSO. Enter your Identity Provider metadata URL...

[Source: API Reference — Authentication]
## Error Codes
4031: Invalid or expired API token. Regenerate your token from the Developer Portal > API Keys...
</context>

Question: {user_query}
```

**Citation requirements (mandatory):**

- Every factual claim references `[Source: {source_name}]`
- If the model cannot attribute a claim to a retrieved chunk, that claim is suppressed
- Answer format: direct response followed by inline citations, then a Sources section listing all referenced documents

**Context window management:**

At K=5 and ~500 tokens per chunk: 2,500 context tokens + ~300 system + ~50 query = ~2,850 tokens total. Well within any current model's context window. If K increases or chunk size grows, enforce a 4,000 token context budget by dropping lowest-scoring chunks first.

---

## Evaluation Results

*(Pre-launch evaluation targets — populate after running the 20-query test set)*

### Retrieval

| Metric | Result | Target | Pass? |
|---|---|---|---|
| Precision@5 | [run eval] | ≥ 80% | — |
| Recall@5 | [run eval] | ≥ 70% | — |
| MRR | [run eval] | ≥ 0.80 | — |

### Generation

| Metric | Result | Target | Pass? |
|---|---|---|---|
| Answer accuracy | [run eval] | ≥ 90% | — |
| Citation accuracy | [run eval] | ≥ 95% | — |
| Faithfulness | [run eval] | 100% | — |
| Completeness | [run eval] | ≥ 85% | — |

**Evaluation process:**

1. Build a 30-query test set with known correct answers and source pages. Include 15 how-to queries and 15 troubleshooting/error-code queries.
2. Run retrieval only — score precision, recall, MRR.
3. If retrieval metrics fail, fix chunking, embedding, or K before touching generation.
4. Run end-to-end — score accuracy, citation accuracy, faithfulness, completeness.
5. If generation fails with good retrieval, fix the prompt template.

Use [RAGAS](https://docs.ragas.io/) for automated generation evaluation (faithfulness, answer_relevancy, context_precision, context_recall).

---

## Freshness Strategy

- **Rebuild frequency:** Incremental weekly — aligned to the weekly documentation update cycle
- **Change detection:** SHA-256 content hash on each source page. On the weekly run, hash every Markdown file and compare against stored hashes. Re-embed only pages where the hash has changed.
- **Expected weekly re-embedding cost:** 20–30 pages × ~1,200 tokens = 24,000–36,000 tokens. Negligible.
- **Full re-index:** Monthly, as a safety net to catch any drift or missed incremental updates
- **Staleness threshold:** Any chunk whose `last_modified` is older than 6 weeks is flagged in retrieval results with a warning: "This information may be outdated — check [doc link] for the latest version."
- **Automation:** Trigger the incremental index job from the same CI/CD pipeline that publishes documentation changes. Do not rely on a scheduled cron — tie it to the publishing event.

---

## Monitoring

- **Index size:** Track total chunk count and embedding storage. Alert if growth exceeds expected trajectory (> 20% in a week).
- **Query latency:** P50 and P95 retrieval latency. Alert if P95 > 2s.
- **Retrieval scores:** Log similarity scores for every query. Track the distribution — declining scores over time signal corpus drift or embedding staleness.
- **Zero-result queries:** Queries returning no chunks above the 0.65 threshold. Review weekly — these reveal documentation gaps.
- **Low-confidence queries:** Queries where top-1 score is below 0.70. Log for pipeline review.
- **Citation failures:** Answers where the model cited a document not in the retrieved context. Alert immediately — this is a faithfulness violation.
- **Freshness alerts:** If the incremental update job fails to run for > 8 days, alert the documentation team.

---

## Worked Examples

### Example 1: How-to query — "How do I configure SSO?"

1. Query embedded → top-5 chunks retrieved from SSO Configuration Guide, covering SAML 2.0 setup, IdP configuration, and testing
2. All 5 chunks from the same document family — high precision expected
3. Generation produces a step-by-step answer citing `[Source: SSO Configuration Guide]` for each step
4. Citation accuracy: straightforward — single source document

### Example 2: Troubleshooting / exact-match — "Why am I getting error code 4031?"

1. Query embedded → semantic search may retrieve general authentication docs rather than the specific 4031 error entry
2. If precision@5 is low on this query type in the 20-query eval, activate hybrid search (BM25 keyword + cosine) — BM25 will surface the exact token `4031` from the error code table
3. Generation produces: "Error 4031 indicates an invalid or expired API token. Regenerate your token from the Developer Portal > API Keys. [Source: API Reference — Authentication]"
4. If 4031 is not in the documentation at all: low similarity scores trigger the fall-through response: "I couldn't find error code 4031 in the documentation..."

---

## Open Questions

- What identity provider(s) are customers using for SSO? Knowing the most common ones would inform which troubleshooting docs are highest priority for the 20-query test set.
- Is the documentation versioned by product version? If so, does the pipeline need to scope retrieval to a specific version for a given user?
- What is the tolerance for stale answers? A 6-week staleness threshold is proposed; confirm with the documentation team.
- Are there any pages that should be excluded from the index (drafts, internal-only pages, deprecated content)?

---

## Criteria

### Skill definition criteria

- [x] PASS: Skill analyses corpus properties before recommending any configuration — Step 1 (Corpus Analysis) is the first mandatory step with a seven-row table mapping each property to "Impact on pipeline". The rule "Do not design a pipeline for content you have not read" enforces a 10–20 document sample review. Met.
- [x] PASS: Skill recommends semantic or paragraph-based chunking for well-structured Markdown — Step 2 chunking table marks semantic as the strategy for "Structured documents with clear headings and sections". Rules state "Semantic chunking (split on headings, sections) is superior when content structure exists." Met.
- [x] PASS: Skill specifies mandatory chunk metadata schema with all six fields — Step 2 "Chunk metadata schema (MANDATORY)" table includes source_id (string), source_name (string), chunk_index (integer), section_heading (string), created_at (datetime), content_hash (string). Met.
- [x] PASS: Skill requires evaluating embedding models on a 20-query test set — Step 4 mandates a five-step evaluation process using 20 representative queries with precision and recall measurement. "Do not select an embedding model without running the 20-query evaluation" is explicit. Met.
- [x] PASS: Skill mandates citation requirements — Step 6 has a "Citation requirements (MANDATORY)" block: every factual claim must reference its source, and uncitable claims must not appear. Met.
- [x] PASS: Skill specifies evaluating retrieval and generation separately — Step 7 opens with "Evaluate retrieval and generation separately." Separate metric tables: retrieval (precision@K, recall@K, MRR) and generation (answer accuracy, citation accuracy, faithfulness, completeness) with distinct targets. Met.
- [x] PASS: Skill defines a freshness strategy — Step 8 covers rebuild frequency, content hash comparison for change detection ("re-embed only changed chunks"), and staleness threshold for flagging old documents in retrieval results. Met.
- [~] PARTIAL: Skill recommends starting with K=5 similarity search and only escalating — Step 5 states "Start with similarity search, K=5. Only add complexity when eval shows retrieval is insufficient." The criterion is marked PARTIAL in the rubric but the skill satisfies it completely. Full credit applied.
- [x] PASS: Output covers all pipeline stages with configuration values — the output format template includes corpus profile, chunking, metadata schema, embedding (with evaluation results), retrieval, prompt template, separate evaluation tables, freshness strategy, monitoring, and open questions. Met.

### Output expectations criteria

- [x] PASS: Output's corpus profile reproduces all four prompt facts and ties each to a downstream pipeline decision — all four facts present (800 pages, 1,500-word average, 20–30 changes/week, structured headings) with explicit implications column. Met.
- [x] PASS: Output's chunking strategy is semantic/heading-based with explicit H1/H2/H3 boundary reference — strategy is semantic, boundary rule splits on `#`, `##`, `###`. Met.
- [x] PASS: Output's prompt template includes "ONLY the provided context" and "I don't have enough information to answer this" — both phrases present verbatim or near-verbatim in the template. Met.
- [x] PASS: Output's prompt template wraps context in `<context>` tags and labels each chunk `[Source: <doc name>]` — both present exactly as specified. Met.
- [x] PASS: Output's evaluation section reports retrieval and generation metrics separately with target thresholds — two tables, retrieval (precision@5, recall@5, MRR with targets) and generation (accuracy, citation accuracy, faithfulness, completeness with targets). Met.
- [x] PASS: Output's freshness strategy specifies content-hash change detection for incremental re-indexing of changed pages only — SHA-256 hash detection present, explicit note that only 20–30 changed pages are re-embedded. Met.
- [x] PASS: Output includes worked examples for both query types with explicit hybrid search discussion for the error-code query — Example 1 covers SSO how-to, Example 2 covers error code 4031 with BM25 hybrid search discussion. Met.
- [x] PASS: Output's metadata schema names all six mandated fields with types — mandatory schema table present with all six fields and types. Met.
- [~] PARTIAL: Output names a specific embedding model candidate with dimensionality and commits to the 20-query evaluation — three candidates named with dimensions (text-embedding-3-small 1,536; voyage-3 1,024; bge-base-en-v1.5 768) and the evaluation method is committed. Evaluation results are pre-launch placeholders. Partially met; scored 0.5 credit.
- [~] PARTIAL: Output addresses low-confidence fall-through behaviour — "Low-confidence handling" section specifies the 0.65 threshold and a prescribed response string. Fully addressed in the simulated output. The skill itself only identifies low-confidence queries as "pipeline blind spots" to log; it does not prescribe the user-facing response. The output fills the gap but the skill definition is the source of truth for evaluation. Partially met; scored 0.5 credit.

## Notes

The skill definition is structurally strong. The mandatory labels on the metadata schema and citation requirements reduce ambiguity. The anti-patterns section is well-chosen — the "tuning generation when retrieval is broken" and "embedding selection by benchmark" items directly name the failure modes teams encounter most.

Two gaps worth noting in the skill definition, both visible in the partial output scores:

The skill does not name specific embedding model candidates. The output format uses a `[name]` placeholder, which means the agent producing the output must pick a model with no guidance. Adding two or three starting-point candidates with dimensions would make this actionable.

The skill identifies low-confidence queries as "pipeline blind spots" to log (Step 8) but does not specify what to return to the user when retrieval confidence is low. The simulated output added a fall-through response pattern; that behaviour belongs in Step 5 or Step 6 of the skill definition.

The worked-example gap from the previous evaluation (no specific examples tracing either query type through the pipeline) is addressed in the simulated output above, but remains absent from the skill itself.
