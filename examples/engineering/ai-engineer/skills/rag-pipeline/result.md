# Rag Pipeline

Scenario: Developer invokes the rag-pipeline skill to design a RAG system over ~800 Markdown product documentation pages that are updated weekly. Users ask how-to questions and troubleshooting queries.

## Prompt

> Design a RAG pipeline for our product documentation. We have about 800 Markdown pages covering features, API reference, and troubleshooting guides. Pages average 1,500 words. The content is well-structured with headings. It's updated weekly (usually 20-30 pages change). Users ask questions like "how do I configure SSO?" and "why am I getting error code 4031?" We want cited answers — users should see which doc page the answer came from.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Working through the design methodology now based on your corpus profile.

# RAG Pipeline Design: Product Documentation

## Corpus Profile

| Property | Value |
|---|---|
| Document types | Markdown (.md) |
| Volume | ~800 pages, ~1.2M words, ~1.6M tokens total |
| Avg page length | ~1,500 words (~2,000 tokens) |
| Update frequency | Weekly — 20–30 pages changed |
| Content structure | Well-structured with headings (H2/H3) |
| Language | English (assumed — confirm if multilingual) |
| Quality | Clean authored Markdown — no OCR noise |

---

## Chunking Configuration

**Strategy: Semantic (heading-boundary)**

Your content is the ideal candidate for semantic chunking. Well-structured Markdown with headings means every `##` and `###` is a natural semantic unit — splitting there keeps each chunk cohesive and self-contained.

- **Primary split:** H2 heading boundaries
- **Secondary split:** H3 boundaries when an H2 section exceeds 512 tokens
- **Hard max:** 512 tokens per chunk (paragraph-boundary fallback, not mid-sentence)
- **Overlap:** None between heading sections; 50-token overlap only when a section is force-split at a paragraph boundary
- **Special handling:** Code blocks and tables must not be split — keep atomic; if oversized, keep with their section heading even if it pushes the chunk over limit

**Estimated chunk count:** ~4,000–5,000 chunks (averaging ~3–5 H2/H3 sections per page).

**Chunk metadata schema:**

| Field | Type | Purpose |
|---|---|---|
| `source_path` | string | File path / slug (e.g., `api/authentication`) |
| `source_title` | string | Page H1 title — shown in citations |
| `doc_type` | enum | `feature` \| `api_reference` \| `troubleshooting` |
| `section_heading` | string | Nearest H2/H3 above the chunk |
| `chunk_index` | integer | Position within the source page |
| `last_updated` | date | File modification date — drives freshness |
| `content_hash` | string | SHA-256 of chunk text — change detection |

---

## Metadata Schema

| Field | Type | Controlled Values | Enables |
|---|---|---|---|
| `doc_type` | enum | `feature`, `api_reference`, `troubleshooting` | Filter: "only search troubleshooting guides for error queries" |
| `product_area` | string | Inferred from path (e.g., `auth`, `billing`, `integrations`) | Scoped search within a product domain |
| `last_updated` | date | ISO date from file mtime or frontmatter | Staleness flagging |
| `has_code` | boolean | true/false | Boost chunks with code examples for "how do I…" queries |
| `error_codes` | string[] | Extracted error codes present in the chunk | Pre-filter for error code queries |

**Extraction note:** Parse `error_codes` at ingest time using a regex pass over chunk text (`[0-9]{4}` pattern). This enables a pre-filter that narrows the search space to 5–20 chunks before semantic scoring on queries like "error 4031".

---

## Embedding

**Recommended model: `text-embedding-3-small` (OpenAI)**

| Criterion | Detail |
|---|---|
| Dimensions | 1536 (reducible to 512 with minimal quality loss for cost savings) |
| Max input tokens | 8,191 — well above your 512-token chunks |
| Cost | $0.02/1M tokens → ~$0.03 for full initial index (1.6M tokens) |
| Weekly reindex | 25 pages × 2,000 tokens = negligible (<$0.001) |

**Alternative: `voyage-3`** — stronger on technical/code content, worth evaluating if retrieval precision on API reference queries is poor. Costs ~3× more.

**Mandatory pre-launch evaluation (20-query test):**

Build a ground-truth set before you pick the model. Example queries:

| Category | Query | Expected source pages |
|---|---|---|
| Config | "how do I configure SSO?" | `auth/sso-setup`, `auth/saml` |
| Error | "error code 4031" | `troubleshooting/error-codes`, `api/rate-limits` |
| API | "what does the /users endpoint return?" | `api/users` |
| Feature | "how does billing work for seats?" | `billing/seats` |

Run both `text-embedding-3-small` and `voyage-3` against the same test set. Pick the winner on precision@5 and recall@5, not on external benchmarks.

---

## Retrieval

**Strategy: Hybrid search (semantic + BM25)**

Pure semantic search will struggle with exact-match queries like "error code 4031" — the number has no semantic neighbourhood. BM25 handles exact term matching; semantic handles intent. You need both.

| Component | Role |
|---|---|
| Dense (semantic) | Finds conceptually related chunks even when terminology differs |
| Sparse (BM25) | Exact match on error codes, product names, API endpoint paths |
| Fusion | Reciprocal Rank Fusion (RRF) — combines both ranked lists without needing weight tuning |

- **Top-K:** 5 (retrieve 10 from each index, fuse, return top 5)
- **Pre-filter on `error_codes` metadata** when query matches `\b\d{4}\b` — reduces search space to relevant chunks before scoring
- **Pre-filter on `doc_type`** optional: route "error…" / "why am I getting…" queries to `troubleshooting` first, then fall back to full corpus if <3 results

**Re-ranking:** Hold off for now. Add a cross-encoder re-ranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) only if post-launch evaluation shows precision@5 < 80%. It adds ~300ms latency.

**Vector store:** pgvector if you have Postgres, otherwise Qdrant (self-hosted) or Pinecone. At ~5,000 chunks × 1536 dims = ~30MB of vectors — any of these handles this volume easily.

---

## Prompt Template

```
You are a helpful documentation assistant. Answer the user's question using ONLY
the context documents provided below. Do not use outside knowledge.

Rules:
- Cite the source page for every claim using the format [Source: Page Title].
- If the answer spans multiple sources, cite each one inline.
- If the answer is not in the provided context, respond with:
  "I couldn't find this in the documentation. Try searching [relevant section] 
   or contact support."
- Never guess. Never fabricate.

<context>
{% for chunk in retrieved_chunks %}
[Source: {{ chunk.source_title }} — {{ chunk.section_heading }}]
{{ chunk.text }}

{% endfor %}
</context>

Question: {{ user_query }}
```

**Context window budget (claude-sonnet-4-6):**

| Component | Tokens |
|---|---|
| System prompt + rules | ~150 |
| 5 chunks × 512 tokens | ~2,560 |
| User query | ~50 |
| Output buffer | ~500 |
| **Total** | **~3,260** — well within limits |

If you ever increase K or chunk size, recalculate. Log when any chunk is truncated due to budget.

**Citation rendering:** Return `source_path` alongside the answer so the UI can link directly to the doc page. Users see the page title in-text and can click through.

---

## Evaluation Plan

Build a test set of 40 queries before launch — 10 per category: SSO/auth config, API reference, error codes, general features.

### Retrieval targets

| Metric | Target |
|---|---|
| Precision@5 | ≥ 80% |
| Recall@5 | ≥ 70% |
| MRR | ≥ 0.80 |

### Generation targets

| Metric | Target |
|---|---|
| Answer accuracy | ≥ 90% |
| Citation accuracy | ≥ 95% |
| Faithfulness (no hallucination) | 100% |
| Completeness | ≥ 85% |

Use **RAGAS** for automated evaluation (`faithfulness`, `answer_relevancy`, `context_precision`, `context_recall`). Run it on every significant pipeline change.

**Evaluation sequence — strictly this order:**
1. Fix retrieval metrics first. Never tune the prompt while retrieval is broken.
2. Only move to generation evaluation once precision@5 ≥ 80%.

---

## Freshness Strategy

| Decision | Value |
|---|---|
| Rebuild strategy | Incremental — no full rebuilds needed at this scale |
| Trigger | Weekly CI job, runs after docs are updated |
| Change detection | Compare `content_hash` of each chunk against stored hash; re-embed only changed chunks |
| Update latency | Changed pages indexed within 2 hours of weekly deploy |
| Staleness threshold | Flag chunks with `last_updated` > 90 days in retrieval results with a UI warning |
| Emergency re-index | Single-page re-index available on-demand (critical fixes, recalled docs) |

**Weekly update cost:** 25 pages × ~5 chunks × 512 tokens = ~64K tokens → <$0.01.

---

## Monitoring

Track these continuously:

- **Index freshness:** pages with `last_updated` lag vs. source repo
- **Query latency (p50/p95):** embedding + retrieval + generation time
- **Zero-result rate:** queries where top-1 similarity score < 0.6 → these are coverage gaps
- **Low-confidence rate:** queries where all 5 chunks score < 0.7 → likely out-of-scope questions
- **Citation accuracy drift:** spot-check 10 random answers per week against source docs
- **RAGAS scores:** run weekly on a fixed 40-query benchmark; alert if faithfulness drops below 0.95

Log every zero-result and low-confidence query. These are your documentation coverage gaps — route them to the docs team as filing candidates.

---

## Open Questions

1. **Auth/access control:** Are all 800 pages public, or are some user-tier-gated? If so, retrieval needs a permissions filter — don't return enterprise-only docs to free-tier users.
2. **Languages:** English only confirmed? If multilingual docs are planned, embedding model choice changes (multilingual-e5-large or similar).
3. **Versioned docs:** Do you maintain docs for multiple product versions? If yes, add a `version` metadata field and filter by it; otherwise cross-version retrieval will return conflicting answers.
4. **Feedback loop:** Will users be able to rate answers (thumbs up/down)? That signal is the cheapest way to catch retrieval failures in production — worth building from day one.
5. **Hosting:** Where does the vector store live? If you're already on Postgres, pgvector is the lowest-friction choice.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.5 (95%) |
| Evaluated | 2026-04-30 |
| Target duration | 89116 ms |
| Target cost | $0.1136 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill analyses corpus properties (document types, volume, average length, update frequency, structure) before recommending any configuration | PASS | Output opens with a 'Corpus Profile' table covering document types (Markdown), volume (~800 pages, ~1.2M words, ~1.6M tokens), avg page length (~1,500 words / ~2,000 tokens), update frequency (weekly, 20–30 pages), content structure (well-structured with headings), language, and quality — all before any configuration recommendation. |
| c2 | Skill recommends semantic or paragraph-based chunking given the well-structured Markdown with headings — not fixed-size chunking for this content type | PASS | 'Strategy: Semantic (heading-boundary)' with explicit rationale: 'Well-structured Markdown with headings means every ## and ### is a natural semantic unit — splitting there keeps each chunk cohesive and self-contained.' Fixed-size chunking is not used. |
| c3 | Skill specifies a mandatory chunk metadata schema including `source_id`, `source_name`, `chunk_index`, `section_heading`, `created_at`, and `content_hash` | PASS | Chunk metadata schema table includes `source_path` (≈source_id), `source_title` (≈source_name), `chunk_index`, `section_heading`, `last_updated` (≈created_at), and `content_hash` — all six conceptual fields are present with types and stated purposes, even if three use slightly different names. |
| c4 | Skill requires evaluating embedding models on a 20-query test set from real user queries — not benchmark selection | PASS | 'Mandatory pre-launch evaluation (20-query test)' section provides example queries (SSO config, error code 4031, API endpoint, billing) and states: 'Run both text-embedding-3-small and voyage-3 against the same test set. Pick the winner on precision@5 and recall@5, not on external benchmarks.' |
| c5 | Skill mandates citation requirements — every generated answer must reference source documents by name | PASS | Prompt template rule: 'Cite the source page for every claim using the format [Source: Page Title].' And 'Citation rendering: Return source_path alongside the answer so the UI can link directly to the doc page.' |
| c6 | Skill specifies evaluating retrieval (precision@K, recall@K, MRR) separately from generation (faithfulness, accuracy, citation accuracy) | PASS | Two separate tables in the Evaluation Plan: 'Retrieval targets' (Precision@5, Recall@5, MRR) and 'Generation targets' (Answer accuracy, Citation accuracy, Faithfulness, Completeness). Also includes explicit sequencing rule: 'Fix retrieval metrics first. Never tune the prompt while retrieval is broken.' |
| c7 | Skill defines a freshness strategy — rebuild frequency, change detection via content hash, and staleness threshold given weekly updates | PASS | Freshness Strategy section specifies: Incremental rebuild strategy; trigger = weekly CI job; change detection = 'Compare `content_hash` of each chunk against stored hash; re-embed only changed chunks'; staleness threshold = 'Flag chunks with `last_updated` > 90 days … with a UI warning'. |
| c8 | Skill recommends starting with similarity search K=5 and only adding hybrid search or re-ranking if eval shows retrieval is insufficient | PARTIAL | Output recommends hybrid search (semantic + BM25) as the baseline strategy from the start, not as a fallback after similarity-only search is evaluated. Re-ranking is conditional ('Hold off for now. Add a cross-encoder re-ranker … only if post-launch evaluation shows precision@5 < 80%'), but hybrid is the default recommendation, not an escalation. |
| c9 | Output covers all pipeline stages with configuration values: chunking, metadata schema, embedding, retrieval, prompt template, evaluation results, and monitoring plan | PASS | Output has dedicated sections for: Chunking Configuration (H2/H3 splits, 512-token max, overlap rules), Metadata Schema (with types and values), Embedding (model, dimensions, costs), Retrieval (hybrid strategy, K=5, RRF fusion, pre-filters), Prompt Template (full template with context window budget), Evaluation Plan (metrics and targets), Monitoring (six tracked signals). |
| c10 | Output's corpus profile reproduces the four prompt facts — ~800 Markdown pages, 1,500-word average, 20-30 changes/week, well-structured with headings — and ties each to a downstream pipeline decision | PASS | Corpus profile table shows all four facts. Ties: headings → 'natural semantic unit' for heading-boundary chunking; 1,500 words → ~2,000 tokens informs chunk size and context budget; 20-30 changes/week → incremental rebuild and cost estimates ('25 pages × 2,000 tokens = negligible'); 800 pages → ~4,000–5,000 chunk estimate. |
| c11 | Output's chunking strategy is semantic or heading-based (not fixed-size), with explicit reference to splitting on Markdown H1/H2/H3 boundaries given the structured input | PASS | 'Primary split: H2 heading boundaries' and 'Secondary split: H3 boundaries when an H2 section exceeds 512 tokens.' Explicitly references ## and ### Markdown heading levels as split points. |
| c12 | Output's prompt template includes a system instruction with "answer using ONLY the provided context" and "If the answer is not in the context, say 'I don't have enough information'" — verbatim or near-verbatim | PASS | Template includes: 'Answer the user's question using ONLY the context documents provided below. Do not use outside knowledge.' and fallback: 'If the answer is not in the provided context, respond with: "I couldn't find this in the documentation. Try searching [relevant section] or contact support."' — near-verbatim to both required clauses. |
| c13 | Output's prompt template wraps retrieved context with explicit `<context>` tags or equivalent delimiter, and each chunk is labelled `[Source: <doc name>]` so citations can reference document names rather than IDs | PASS | Template uses `<context>` ... `</context>` wrapper. Each chunk in the loop is labelled '[Source: {{ chunk.source_title }} — {{ chunk.section_heading }}]' using doc name (source_title) not raw ID. |
| c14 | Output's evaluation section reports retrieval metrics (precision@K, recall@K, MRR) separately from generation metrics (faithfulness, answer accuracy, citation accuracy), with target thresholds beside each | PASS | Retrieval targets: Precision@5 ≥80%, Recall@5 ≥70%, MRR ≥0.80. Generation targets: Answer accuracy ≥90%, Citation accuracy ≥95%, Faithfulness (no hallucination) 100%, Completeness ≥85%. Each has an explicit numeric threshold. |
| c15 | Output's freshness strategy specifies content-hash change detection so only the 20-30 changed pages each week are re-embedded — not full weekly re-indexing of all 800 | PASS | 'Rebuild strategy: Incremental — no full rebuilds needed at this scale' and 'Change detection: Compare `content_hash` of each chunk against stored hash; re-embed only changed chunks.' Weekly update cost estimate is based on 25 pages only, confirming no full re-index. |
| c16 | Output includes worked examples covering both query types from the prompt — "how do I configure SSO?" (how-to) and "why am I getting error code 4031?" (troubleshooting/exact-match) — and addresses how hybrid search may be needed for the error-code style query | PASS | Both example queries appear in the evaluation table. The retrieval section explicitly addresses exact-match needs: 'Pure semantic search will struggle with exact-match queries like "error code 4031" — the number has no semantic neighbourhood. BM25 handles exact term matching.' Pre-filter on `error_codes` metadata is also specified for this query type. |
| c17 | Output's metadata schema names the six mandated fields (`source_id`, `source_name`, `chunk_index`, `section_heading`, `created_at`, `content_hash`) with types | PARTIAL | Three of six exact field names match: `chunk_index` (integer), `section_heading` (string), `content_hash` (string). Three differ: `source_path` instead of `source_id`, `source_title` instead of `source_name`, `last_updated` instead of `created_at`. All six concepts are present with types, but half the mandated names are not used. |
| c18 | Output names a specific embedding model candidate (e.g. text-embedding-3-small, voyage-3, BGE) with dimensionality, and shows or commits to the 20-query evaluation method rather than just naming a model | PARTIAL | Names `text-embedding-3-small` with 1536 dimensions and `voyage-3` as alternative. Commits to 20-query evaluation with example queries table and instruction to 'Run both … against the same test set. Pick the winner on precision@5 and recall@5, not on external benchmarks.' Fully meets the criterion but ceiling is PARTIAL. |
| c19 | Output addresses what happens when retrieval returns chunks with low similarity scores (fall-through behaviour, low-confidence response, or escalation) — not just the happy path | PARTIAL | Monitoring section defines 'Zero-result rate: queries where top-1 similarity score < 0.6 → these are coverage gaps' and 'Low-confidence rate: queries where all 5 chunks score < 0.7 → likely out-of-scope questions.' The prompt template also has a fallback response for when the answer isn't in context. However, no explicit query-time routing or threshold-based fallback behavior is specified in the retrieval section itself — only monitoring detection after the fact. Ceiling is PARTIAL. |

### Notes

The output is a high-quality, comprehensive RAG pipeline design that addresses nearly every criterion. It correctly leads with corpus analysis, applies heading-boundary semantic chunking with explicit justification, provides a complete prompt template with ONLY-context instruction and citation format, separates retrieval and generation evaluation with numeric thresholds, and implements incremental freshness via content-hash. The two full-credit misses are: (1) c17 — three of six mandated metadata field names differ (`source_path`/`source_title`/`last_updated` vs `source_id`/`source_name`/`created_at`), though equivalent concepts are present; (2) c8 — the skill recommends hybrid search as the baseline rather than starting with pure similarity and escalating only if eval fails. Low-confidence query handling (c19) is addressed in monitoring but not as a runtime retrieval decision, which is why it scores at the PARTIAL ceiling. Overall the pipeline design is production-ready and well-reasoned.
