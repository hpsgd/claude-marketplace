# Rag Pipeline

Scenario: Developer invokes the rag-pipeline skill to design a RAG system over ~800 Markdown product documentation pages that are updated weekly. Users ask how-to questions and troubleshooting queries.

## Prompt

> Design a RAG pipeline for our product documentation. We have about 800 Markdown pages covering features, API reference, and troubleshooting guides. Pages average 1,500 words. The content is well-structured with headings. It's updated weekly (usually 20-30 pages change). Users ask questions like "how do I configure SSO?" and "why am I getting error code 4031?" We want cited answers — users should see which doc page the answer came from.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll design this RAG pipeline step-by-step. Since I haven't examined your actual documentation, I'll note assumptions and flag where you should validate with real content samples.

## Step 1: Corpus Analysis

Based on your description, here's what we know:

| Property | Value | Impact |
|---|---|---|
| Document types | Markdown (structured with headings) | Semantic chunking on heading hierarchy is ideal |
| Volume | 800 docs × 1.5K words ≈ 1.2M words ≈ 1.6M tokens | Medium-sized corpus. Full re-index takes minutes, not hours |
| Average length | 1.5K words ≈ 2,000 tokens per page | Long-form content; chunking prevents losing context at boundaries |
| Update frequency | Weekly, 20-30 pages (~2-3% churn) | Incremental updates feasible; full re-index acceptable weekly |
| Structure | Hierarchical headings, sections | Semantic chunking on heading boundaries works well |
| Quality | Well-maintained docs (implied) | No OCR noise or cleanup required |
| Domains | Features, API reference, troubleshooting | Three distinct content types with different patterns |

**Next step:** Share 3-5 sample pages (one from each domain: feature guide, API reference, troubleshooting) so I can validate chunking boundaries and metadata categories against real content.

---

## Step 2: Chunking Strategy

**Recommended: Semantic chunking on heading hierarchy** (not fixed-size).

Here's why: Your docs have structure — headings are semantic markers. A troubleshooting section about error 4031 should not be split mid-sentence across a heading boundary.

**Chunking rules:**

1. **Split on headings** — each `##` section is a chunk boundary
2. **Sub-chunks for long sections** — if a section under a heading exceeds 800 tokens, split further on `###` boundaries
3. **Never split mid-sentence**
4. **Preserve code blocks intact** — a code example should not be truncated
5. **Metadata: inherit from nearest heading** — track which heading(s) contain this chunk

**Chunk size targets:**

- Minimum: 150 tokens (readable without excessive context-switching)
- Target: 400–700 tokens (sweet spot for API references and feature guides)
- Maximum: 1000 tokens (troubleshooting guides can be longer for context)

**Metadata schema (append to each chunk):**

```json
{
  "source_id": "features/sso-configuration",
  "source_name": "SSO Configuration Guide",
  "document_type": "feature_guide",
  "chunk_index": 2,
  "section_path": ["SSO Configuration", "OAuth 2.0 Setup"],
  "section_heading": "OAuth 2.0 Setup",
  "created_at": "2026-05-04T00:00:00Z",
  "content_hash": "sha256_...",
  "category": "authentication",
  "audience": "customer",
  "api_version": "v1"
}
```

**Metadata categories (domain-specific for product docs):**

| Field | Type | Values | Why |
|---|---|---|---|
| document_type | enum | `feature_guide`, `api_reference`, `troubleshooting`, `faq` | Retrieval weights guides differently from API refs |
| category | enum | `authentication`, `integration`, `data-management`, `monitoring`, `errors` | Scope searches to topic areas |
| audience | enum | `customer`, `internal`, `developer` | Hide internal-only docs from public users |
| error_codes | list | e.g., `["4031", "4032"]` | Direct error-code lookups |
| feature_tags | list | e.g., `["SSO", "OAuth2"]` | Tag-based retrieval |
| api_version | string | `v1`, `v2` | Deprecation tracking |

---

## Step 3: Metadata Enrichment

At ingestion, extract and assign metadata automatically:

```python
# Pseudocode for metadata extraction
def extract_metadata(markdown_source, source_id):
    metadata = {
        "source_id": source_id,
        "source_name": extract_title(markdown_source),
        "document_type": infer_type(markdown_source),  # FAQ pattern? Error codes? → infer type
        "category": infer_category(markdown_source),    # Keywords → category
        "error_codes": extract_codes(markdown_source),  # Match pattern: /(?:error|code|4\d{3})/i
        "feature_tags": extract_tags(markdown_source),  # Headings, links
        "audience": "customer",  # Default; override if internal markers found
        "api_version": extract_version(markdown_source),
        "created_at": now(),
    }
    return metadata
```

---

## Step 4: Embedding Selection

**Recommendation: Start with OpenAI's `text-embedding-3-small`** (384 dimensions, $0.02/1M tokens).

**But validate on your domain first.** Run this 20-query benchmark:

**Test queries (mix of real user patterns):**

1. "How do I configure SSO with Okta?"
2. "Why am I getting error 4031?"
3. "What's the difference between API v1 and v2?"
4. "How do I set up data retention policies?"
5. "How do I debug webhook failures?"
6. "What are the rate limits for the API?"
7. "How do I export data in bulk?"
8. "Can I use SSO with Azure AD?"
9. "Error code 5002 — what does it mean?"
10. "How do I monitor API usage?"
11. "What's the maximum payload size?"
12. "How do I revoke an API token?"
13. "Can I use multiple authentication methods?"
14. "How do I set up alerts for quota limits?"
15. "What's the difference between webhooks and polling?"
16. "How do I migrate from v1 to v2?"
17. "Error 4031 on every request — help!"
18. "What permissions does the 'editor' role have?"
19. "How do I backup my configuration?"
20. "Can I use this offline?"

**For each query, identify 3–5 documents that SHOULD be retrieved** (ground truth).

Then embed your corpus with:
- `text-embedding-3-small` (384 dims, fast, cheap)
- `text-embedding-3-large` (1536 dims, slower, more expensive)

Run both models against your 20 queries and measure:
- **Precision@5**: Of top 5 retrieved chunks, how many are correct?
- **Recall@5**: Of all relevant chunks, how many are in the top 5?

**Expected results:**
- Small model: ~75–85% precision (good enough for hybrid search)
- Large model: ~85–95% precision (overkill if small model is sufficient)

If small model hits 80%+ precision on your domain, use it. If it drops below 75%, upgrade to the large model.

---

## Step 5: Retrieval Configuration

**Recommended: Hybrid search (similarity + keyword)** with re-ranking.

Why? Your queries contain exact terms:
- Error codes: "4031"
- Feature names: "SSO", "OAuth", "Okta"
- Technical terms: "webhook", "API", "rate limits"

BM25 keyword search will boost these exact matches. Combined with embedding similarity, you get both semantic understanding ("why is this failing?") and exact-term matching ("error 4031").

**Configuration:**

```python
def hybrid_retrieve(query: str, top_k: int = 5):
    # 1. Semantic similarity
    query_embedding = embed(query)
    semantic_results = vector_db.search(
        query_embedding, 
        top_k=10,  # Retrieve more candidates for re-ranking
        filters={"audience": "customer"}  # Only customer-facing docs
    )
    
    # 2. Keyword search (BM25)
    keyword_results = bm25_index.search(
        query,
        top_k=10,
        filters={"audience": "customer"}
    )
    
    # 3. Fuse rankings (RRF or weighted blend)
    fused = reciprocal_rank_fusion(
        semantic_results,
        keyword_results,
        weights={"semantic": 0.6, "keyword": 0.4}
    )
    
    # 4. Re-rank top candidates with cross-encoder
    reranked = rerank(fused[:10], query, model="cross-encoder/qnli-distilroberta-base")
    
    return reranked[:top_k]
```

**Hyperparameters:**

| Parameter | Value | Rationale |
|---|---|---|
| Top-K | 5 | Typical answer requires context from 3-5 sources; 5 gives confidence margin |
| Semantic weight | 0.6 | Semantic similarity is primary signal |
| Keyword weight | 0.4 | Error codes and feature names boost exact matches |
| Re-ranker | `cross-encoder/qnli-distilroberta-base` | Fast (< 50ms), good for QA |

---

## Step 6: Prompt Construction

**Prompt template with mandatory citations:**

```
system:
You are a helpful documentation assistant. Answer questions using ONLY the provided documentation.

CRITICAL RULES:
1. If information is not in the provided context, say: "I don't have information about that in the documentation."
2. Every claim must cite its source. Format: [Source: Document Name, Section]
3. Never make up information or use knowledge outside the provided context.
4. If you're unsure about an answer, say so.

---

Context Documents:
<context>
[Source: SSO Configuration Guide, OAuth 2.0 Setup]
To configure OAuth 2.0 with your identity provider:
1. Create an OAuth application in your provider's admin console
2. Copy the Client ID and Client Secret
3. In our platform, navigate to Settings > Authentication > OAuth
4. Paste your credentials and save
...

[Source: Error Reference, Error 4031]
Error 4031: Invalid OAuth credentials

This error occurs when:
- The Client ID or Secret is incorrect
- The OAuth provider has revoked the application
- The token has expired

Solution:
1. Verify your Client ID and Secret in your OAuth provider's console
2. If unchanged, try re-authorizing the application
3. Contact your OAuth provider if the issue persists
...
</context>

---

user:
Question: Why am I getting error 4031?

assistant:
Error 4031 occurs when your OAuth credentials are invalid or have been revoked. Here are the most common causes:

**Incorrect Credentials:** [Source: Error Reference, Error 4031] Double-check that your Client ID and Secret match exactly what's shown in your OAuth provider's admin console. Even a single character difference will trigger this error.

**Provider Revoked Access:** [Source: Error Reference, Error 4031] Your OAuth provider may have revoked the application. Check your provider's console to confirm the application is still active.

**Expired Token:** [Source: Error Reference, Error 4031] If you recently updated your OAuth provider settings, try re-authorizing the application.

**Configuration Steps:** [Source: SSO Configuration Guide, OAuth 2.0 Setup] To reconfigure:
1. Go to Settings > Authentication > OAuth
2. Paste your current Client ID and Secret (from your OAuth provider)
3. Save and retry

If you've verified all of these and still see the error, contact your OAuth provider's support team.
```

**Citation format rules:**
- `[Source: Document Name, Section Name]` for each claim
- Group related claims under one citation when possible
- Never cite a source without quoting or paraphrasing that specific section

---

## Step 7: End-to-End Evaluation

**Build a test set of 30 queries with ground truth.**

For each query, a human identifies:
- The correct source document(s)
- The specific section(s) that answer it
- What a good answer looks like

**Example test case:**

```
Query: "Why am I getting error 4031?"

Ground truth documents:
- [Error Reference: Error 4031]
- [SSO Configuration Guide: OAuth 2.0 Setup] (for reconfiguration steps)

Expected answer elements:
- Explanation of what 4031 means (invalid OAuth credentials)
- Root causes (wrong credentials, provider revoked, expired token)
- Troubleshooting steps (verify in provider console, re-authorize, contact provider)

Correct source attribution required:
- "why this happens" → cite Error Reference
- "how to fix it" → cite SSO Configuration Guide
```

**Evaluation metrics:**

| Phase | Metric | How to measure | Target |
|---|---|---|---|
| **Retrieval** | Precision@5 | # correct chunks in top 5 / 5 | ≥ 80% |
| **Retrieval** | Recall@5 | # retrieved relevant chunks / total relevant chunks | ≥ 70% |
| **Retrieval** | MRR | Avg rank position of first correct chunk | ≥ 0.8 |
| **Generation** | Accuracy | Is the answer factually correct? (human eval) | ≥ 90% |
| **Generation** | Citation match | Does every claim have correct source attribution? (human eval) | ≥ 95% |
| **Generation** | Faithfulness | Does answer contain ONLY info from context? (use RAGAS metric) | 100% |
| **Generation** | Completeness | Does answer address the full question? | ≥ 85% |

**Evaluation process:**

1. **Retrieval eval (automated):**
   - Embed query
   - Hybrid search → top 5
   - Check: are the right documents ranked high?

2. **Generation eval (human + automated):**
   - Feed retrieved context into prompt
   - LLM generates answer
   - Human judge: is it accurate? Are citations correct?
   - Use [RAGAS faithfulness](https://docs.ragas.io/en/latest/concepts/metrics/faithfulness.html) to detect hallucinations

**If retrieval fails (< 80% precision):**
- Check chunk size — are chunks too small/large?
- Check embedding model — re-run the 20-query benchmark
- Try hybrid search with different keyword weights

**If generation fails but retrieval is good:**
- Check prompt — is context clearly delimited?
- Check model — does it follow "cite sources" instruction? (Sonnet > Haiku)
- Add system instruction: "Do not answer from general knowledge. Answer ONLY using the provided context."

---

## Step 8: Freshness & Maintenance

Weekly updates (20–30 pages) require incremental indexing, not full rebuilds.

**Change detection:**

```python
def index_updates(modified_documents: List[Path]):
    """
    Triggered weekly by your docs deployment pipeline.
    """
    for doc_path in modified_documents:
        chunks = semantic_chunk(read_markdown(doc_path))
        for chunk in chunks:
            # Compute hash of chunk content
            content_hash = sha256(chunk.text)
            
            # Check if this chunk already exists
            existing = chunk_db.find_by(
                source_id=chunk.source_id,
                chunk_index=chunk.chunk_index
            )
            
            if existing and existing.content_hash == content_hash:
                # No change, skip
                continue
            
            if existing:
                # Content changed, delete old embedding, insert new
                vector_db.delete(existing.embedding_id)
            
            # Embed and insert new chunk
            embedding = embed(chunk.text)
            chunk_db.insert({
                **chunk.metadata,
                "embedding": embedding,
                "content_hash": content_hash,
                "indexed_at": now()
            })
    
    # After update, validate
    log_index_stats()
```

**Automation (integrate with your docs release):**

```yaml
# Example: GitHub Actions trigger on docs deploy
on:
  push:
    paths:
      - "docs/**/*.md"

jobs:
  update-rag-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Detect changed docs
        id: changed
        run: |
          git diff --name-only ${{ github.event.before }}..HEAD docs/
      - name: Reindex changed documents
        run: |
          python scripts/index_updates.py --documents "${{ steps.changed.outputs.files }}"
      - name: Validate freshness
        run: python scripts/validate_index.py
```

**Monitoring (track over time):**

```
Metrics to log:
- Index size (# chunks, total tokens)
- Query latency (p50, p95, p99)
- Retrieval scores (avg similarity of top result)
- Generation quality (% queries with ≥2 citations, avg citation accuracy)
- Errors/failures (queries returning 0 results, low-confidence matches)

Alert conditions:
- Generation accuracy drops below 85%
- Citation accuracy drops below 90%
- Query latency exceeds 2 seconds (p95)
- Queries with 0 results exceed 5% (blind spots in corpus)
```

---

## Summary: Implementation Roadmap

| Phase | Effort | Outcome |
|---|---|---|
| **Phase 1: Setup** | 1-2 days | Corpus extraction, semantic chunking, metadata schema |
| **Phase 2: Embedding eval** | 3-5 days | 20-query benchmark, embedding model selected |
| **Phase 3: Retrieval** | 2-3 days | Hybrid search + re-ranker implemented, indexed |
| **Phase 4: Generation** | 1-2 days | Prompt finalized, citation validation working |
| **Phase 5: Evaluation** | 2-3 days | Test set built, precision/recall/faithfulness measured |
| **Phase 6: Automation** | 1-2 days | Weekly reindex pipeline, monitoring dashboards |
| **Total** | 10-17 days | Production RAG system |

---

**Next steps for you:**

1. **Share 3–5 sample pages** (one from each content type) so I can refine chunking boundaries and test metadata extraction
2. **Define query evaluation baseline** — what's your current support volume? How many queries/week would this handle?
3. **Decide on embedding model cost tolerance** — `text-embedding-3-small` ($0.02/1M tokens) vs `text-embedding-3-large` ($0.13/1M tokens)

Once you provide samples, I can design the chunking and metadata schemas to your actual content structure.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.5 (97%) |
| Evaluated | 2026-05-04 |
| Target duration | 55057 ms |
| Target cost | $0.0718 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill analyses corpus properties (document types, volume, average length, update frequency, structure) before recommending any configuration | PASS | Step 1 'Corpus Analysis' table explicitly covers document types (Markdown, structured with headings), volume (800 docs × 1.5K words ≈ 1.6M tokens), average length (1.5K words ≈ 2,000 tokens/page), update frequency (Weekly, 20-30 pages, ~2-3% churn), and structure (Hierarchical headings, sections), each with an 'Impact' column tying the property to downstream decisions. |
| c2 | Skill recommends semantic or paragraph-based chunking given the well-structured Markdown with headings — not fixed-size chunking for this content type | PASS | Step 2 states: 'Recommended: Semantic chunking on heading hierarchy (not fixed-size).' and explicitly justifies: 'Your docs have structure — headings are semantic markers. A troubleshooting section about error 4031 should not be split mid-sentence across a heading boundary.' |
| c3 | Skill specifies a mandatory chunk metadata schema including `source_id`, `source_name`, `chunk_index`, `section_heading`, `created_at`, and `content_hash` | PASS | Step 2 JSON schema shows all six required fields: `source_id` ('features/sso-configuration'), `source_name` ('SSO Configuration Guide'), `chunk_index` (2), `section_heading` ('OAuth 2.0 Setup'), `created_at` ('2026-05-04T00:00:00Z'), and `content_hash` ('sha256_...'). |
| c4 | Skill requires evaluating embedding models on a 20-query test set from real user queries — not benchmark selection | PASS | Step 4 provides exactly 20 numbered test queries drawn from realistic user patterns ('How do I configure SSO with Okta?', 'Why am I getting error 4031?', etc.) and instructs: 'Run both models against your 20 queries and measure: Precision@5, Recall@5.' |
| c5 | Skill mandates citation requirements — every generated answer must reference source documents by name | PASS | Step 6 system prompt states: 'Every claim must cite its source. Format: [Source: Document Name, Section]'. A 'Citation format rules' sub-section further specifies '[Source: Document Name, Section Name] for each claim' and 'Never cite a source without quoting or paraphrasing that specific section.' |
| c6 | Skill specifies evaluating retrieval (precision@K, recall@K, MRR) separately from generation (faithfulness, accuracy, citation accuracy) | PASS | Step 7 evaluation table separates Phase 'Retrieval' (Precision@5, Recall@5, MRR) from Phase 'Generation' (Accuracy, Citation match, Faithfulness, Completeness), each with distinct target thresholds. |
| c7 | Skill defines a freshness strategy — rebuild frequency, change detection via content hash, and staleness threshold given weekly updates | PASS | Step 8 'Freshness & Maintenance' includes Python code computing `content_hash = sha256(chunk.text)` and checking `existing.content_hash == content_hash` to skip unchanged chunks. A GitHub Actions YAML triggers incremental reindexing on `docs/**/*.md` changes. Monitoring alerts if generation accuracy drops below 85% or query latency exceeds 2s. |
| c8 | Skill recommends starting with similarity search K=5 and only adding hybrid search or re-ranking if eval shows retrieval is insufficient | FAIL | Step 5 opens directly with 'Recommended: Hybrid search (similarity + keyword) with re-ranking' and immediately provides a full hybrid + cross-encoder implementation. The output never recommends starting with simple similarity-only search and escalating to hybrid only if evaluation shows retrieval is insufficient — it recommends the full stack from the outset. |
| c9 | Output covers all pipeline stages with configuration values: chunking, metadata schema, embedding, retrieval, prompt template, evaluation results, and monitoring plan | PASS | All stages present with explicit configuration values: chunking (150-1000 token targets in Step 2), metadata schema (JSON in Step 2), embedding (text-embedding-3-small at 384 dims, $0.02/1M tokens in Step 4), retrieval (semantic 0.6 / keyword 0.4 weights, top-K=5 in Step 5), prompt template (full template with context tags and citation rules in Step 6), evaluation (metrics with thresholds in Step 7), monitoring (alert conditions and metrics to log in Step 8). |
| c10 | Output's corpus profile reproduces the four prompt facts — ~800 Markdown pages, 1,500-word average, 20-30 changes/week, well-structured with headings — and ties each to a downstream pipeline decision | PASS | Step 1 table maps all four facts to decisions: 800 docs → 'Medium-sized corpus. Full re-index takes minutes'; 1.5K words average → 'Long-form content; chunking prevents losing context at boundaries'; 20-30 pages/week → 'Incremental updates feasible; full re-index acceptable weekly'; headings → 'Semantic chunking on heading boundaries works well'. |
| c11 | Output's chunking strategy is semantic or heading-based (not fixed-size), with explicit reference to splitting on Markdown H1/H2/H3 boundaries given the structured input | PASS | Step 2 chunking rules: 'Split on headings — each `##` section is a chunk boundary' and 'Sub-chunks for long sections — if a section under a heading exceeds 800 tokens, split further on `###` boundaries.' Explicit reference to H2 (`##`) and H3 (`###`) Markdown boundaries. |
| c12 | Output's prompt template includes a system instruction with "answer using ONLY the provided context" and "If the answer is not in the context, say 'I don't have enough information'" — verbatim or near-verbatim | PASS | Step 6 system prompt includes: 'Answer questions using ONLY the provided documentation.' and 'If information is not in the provided context, say: "I don't have information about that in the documentation."' — both are near-verbatim matches to the criterion requirements. |
| c13 | Output's prompt template wraps retrieved context with explicit `<context>` tags or equivalent delimiter, and each chunk is labelled `[Source: <doc name>]` so citations can reference document names rather than IDs | PASS | Step 6 prompt template uses `<context>` and `</context>` tags to wrap all retrieved chunks. Each chunk is prefixed with `[Source: SSO Configuration Guide, OAuth 2.0 Setup]` and `[Source: Error Reference, Error 4031]`, using document name rather than ID. |
| c14 | Output's evaluation section reports retrieval metrics (precision@K, recall@K, MRR) separately from generation metrics (faithfulness, answer accuracy, citation accuracy), with target thresholds beside each | PASS | Step 7 evaluation table lists Retrieval: Precision@5 (≥80%), Recall@5 (≥70%), MRR (≥0.8); and Generation: Accuracy (≥90%), Citation match (≥95%), Faithfulness (100%), Completeness (≥85%). Each has a 'Target' column with explicit thresholds. |
| c15 | Output's freshness strategy specifies content-hash change detection so only the 20-30 changed pages each week are re-embedded — not full weekly re-indexing of all 800 | PASS | Step 8 function `index_updates(modified_documents: List[Path])` iterates only over changed documents. The hash check `if existing and existing.content_hash == content_hash: continue` skips unchanged chunks. The GitHub Actions trigger on `docs/**/*.md` changes passes only the diff (`git diff --name-only`) to the indexing script. |
| c16 | Output includes worked examples covering both query types from the prompt — "how do I configure SSO?" (how-to) and "why am I getting error code 4031?" (troubleshooting/exact-match) — and addresses how hybrid search may be needed for the error-code style query | PASS | Step 4 test queries include 'How do I configure SSO with Okta?' and 'Why am I getting error 4031?' Step 5 explicitly addresses error codes: 'Error codes: "4031"' listed under exact-term queries, with the explanation that 'BM25 keyword search will boost these exact matches.' Step 6 provides a full worked answer for the error 4031 query with citations. |
| c17 | Output's metadata schema names the six mandated fields (`source_id`, `source_name`, `chunk_index`, `section_heading`, `created_at`, `content_hash`) with types | PASS | Step 2 JSON schema names all six fields with unambiguous types from example values: `source_id` (string), `source_name` (string), `chunk_index` (integer: 2), `section_heading` (string), `created_at` (ISO datetime string), `content_hash` (string: 'sha256_...'). Types are unambiguously determinable from the example values in this design-document context. |
| c18 | Output names a specific embedding model candidate (e.g. text-embedding-3-small, voyage-3, BGE) with dimensionality, and shows or commits to the 20-query evaluation method rather than just naming a model | PARTIAL | Step 4 names `text-embedding-3-small` (384 dimensions, $0.02/1M tokens) and `text-embedding-3-large` (1536 dimensions, $0.13/1M tokens) with full cost comparison. The 20 test queries are listed in full with the instruction to run both models and measure Precision@5 and Recall@5. Fully meets the criterion content; ceiling caps at 0.5. |
| c19 | Output addresses what happens when retrieval returns chunks with low similarity scores (fall-through behaviour, low-confidence response, or escalation) — not just the happy path | PARTIAL | The output partially addresses this: the Step 6 system prompt instructs 'If information is not in the provided context, say: I don't have information about that' (generation-level fallback). Step 8 monitoring lists 'low-confidence matches' as an error condition and alerts when 'Queries with 0 results exceed 5%'. However, there is no explicit retrieval-time similarity threshold (e.g., discard chunks below cosine similarity 0.7) or a defined escalation path for low-score retrievals. Coverage is partial. |

### Notes

The output is an exceptionally thorough RAG pipeline design covering all eight stages with concrete configuration values, worked examples, pseudocode, and evaluation targets. It correctly identifies the corpus structure and maps each property to a pipeline decision, recommends heading-based semantic chunking with explicit H2/H3 boundaries, provides a complete metadata schema, specifies a 20-query domain evaluation methodology, includes a full citation-enforcing prompt template with <context> tags, separates retrieval from generation metrics with explicit thresholds, and implements content-hash incremental indexing. The only meaningful gap is c8: the output recommends full hybrid search + cross-encoder re-ranking from the start rather than the 'start simple, escalate if eval fails' approach the criterion expected. The low-similarity fallback (c19) is partially addressed through generation-level prompting and monitoring alerts but lacks explicit retrieval-time threshold filtering. Both are minor relative to the breadth and depth of the design.
