---
name: rag-pipeline
description: Design a RAG pipeline — chunking strategy, embedding selection, retrieval configuration, and end-to-end evaluation.
argument-hint: "[document corpus or knowledge base for the RAG system]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Design a RAG pipeline for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Corpus Analysis

Understand the content before designing the pipeline. The corpus dictates every downstream decision.

| Property | Question | Impact on pipeline |
|---|---|---|
| Document types | What formats? (PDF, HTML, Markdown, plain text, code) | Determines parsing and extraction strategy |
| Volume | How many documents? Total size? | Storage, indexing time, cost projections |
| Average length | Typical document size in tokens? | Chunk size and overlap decisions |
| Update frequency | Static, daily, hourly, real-time? | Index rebuild strategy, freshness requirements |
| Content structure | Headings, sections, tables, code blocks? | Semantic chunking boundaries |
| Language | Single or multilingual? | Embedding model selection |
| Quality | Clean text or noisy (OCR, scraped HTML)? | Preprocessing pipeline requirements |

Examine a representative sample of 10-20 documents. Do not design a pipeline for content you have not read.

### Step 2: Chunking Strategy

Chunking is the highest-impact decision in the pipeline. Wrong chunk sizes corrupt retrieval regardless of everything downstream.

| Strategy | Chunk size | Overlap | When to use |
|---|---|---|---|
| Fixed-size | 256 tokens | 10% | Short, uniform documents. Simple but lossy at boundaries |
| Fixed-size | 512 tokens | 10-20% | General purpose default. Start here |
| Fixed-size | 1024 tokens | 20% | Long-form content where context within a chunk matters |
| Semantic | Variable | None | Structured documents with clear headings and sections |
| Paragraph-based | Variable | None | Well-formatted text with meaningful paragraph breaks |

**Chunking rules:**
- Never split mid-sentence. Sentence boundaries are the minimum atomic unit
- Prefer paragraph or section boundaries when document structure allows
- Overlap prevents information loss at chunk edges — 10-20% is the practical range
- Semantic chunking (split on headings, sections) is superior when content structure exists
- Test chunk quality: can a human read a random chunk and understand it without context? If no, chunks are too small

**Chunk metadata schema (MANDATORY):**

| Field | Type | Purpose |
|---|---|---|
| source_id | string | Reference to the original document |
| source_name | string | Human-readable document name |
| chunk_index | integer | Position within the source document |
| section_heading | string | Nearest heading above this chunk |
| created_at | datetime | When the chunk was created |
| content_hash | string | Hash of chunk content — detect changes on re-index |

### Step 3: Metadata Enrichment

Metadata enables filtered retrieval — searching within a category, date range, or document type rather than the full corpus.

Define the metadata schema based on corpus analysis:

| Field | Type | Values | Enables |
|---|---|---|---|
| category | string | [domain-specific categories] | Filtered search within a topic |
| document_type | string | policy, guide, reference, FAQ | Type-specific retrieval |
| date | date | Document publication or effective date | Recency-weighted retrieval |
| audience | string | internal, customer, developer | Audience-appropriate results |
| [custom] | [type] | [domain-specific values] | [domain-specific filtering] |

**Rules:**
- Every chunk inherits metadata from its source document
- Metadata fields must have controlled vocabularies — free-text metadata is unsearchable
- Add metadata at ingestion time, not retrieval time. Retrieval must be fast

### Step 4: Embedding Selection

Evaluate embedding models on YOUR data. Benchmark rankings do not predict performance on your domain.

**Evaluation method:**
1. Select 20 representative queries users will actually ask
2. For each query, identify the 3-5 documents that SHOULD be retrieved (ground truth)
3. Embed the corpus with each candidate model
4. Run the 20 queries against each index
5. Measure retrieval precision and recall against ground truth

| Criterion | Question | Trade-off |
|---|---|---|
| Domain fit | Does the model understand your domain vocabulary? | General models miss domain-specific semantics |
| Dimensionality | 384 / 768 / 1024 / 1536 dimensions? | Higher = more nuance, more storage, slower search |
| Max input tokens | Does it handle your chunk sizes? | Chunks exceeding the limit are silently truncated |
| Cost | Per-token embedding cost × corpus size × rebuild frequency | Adds up fast on large, frequently updated corpora |
| Speed | Embedding throughput (tokens/second) | Matters for initial indexing and real-time updates |

**Do not select an embedding model without running the 20-query evaluation.** An embedding model that scores well on academic benchmarks but misses your domain terminology will return irrelevant results.

### Step 5: Retrieval Configuration

| Strategy | How it works | When to use |
|---|---|---|
| Similarity search | Cosine similarity between query and chunk embeddings | Default starting point. Works when queries match document language |
| Hybrid search | Similarity + keyword (BM25) combined with weighted scoring | When users search with exact terms (product names, codes, error messages) |
| Re-ranking | Retrieve top-N candidates, re-rank with a cross-encoder model | When initial retrieval precision is insufficient. Adds latency |

**Top-K selection:**

| Top-K | Trade-off |
|---|---|
| 3 | Minimal context, lowest cost. Use when documents are highly relevant and focused |
| 5 | Default. Balances context breadth with cost and noise |
| 10 | Maximum context. Use when relevance is uncertain or topic requires synthesis across documents |

**Rules:**
- Start with similarity search, K=5. Only add complexity when eval shows retrieval is insufficient
- Hybrid search improves results when the corpus contains exact-match terminology (codes, product names, technical terms)
- Re-ranking adds 200-500ms latency. Use only when the quality improvement justifies the cost
- Always return similarity scores with results — they are the confidence signal for downstream logic

### Step 6: Prompt Construction

How retrieved context is injected into the generation prompt determines output quality and faithfulness.

**Template structure:**

```
[System instruction — role, task, constraints]

You are a [role] that answers questions using ONLY the provided context documents.
If the answer is not in the context, say "I don't have enough information to answer this."
Always cite the source document for each claim in your answer.

[Retrieved context — clearly delimited]

<context>
[Source: {source_name_1}]
{chunk_text_1}

[Source: {source_name_2}]
{chunk_text_2}
</context>

[User query]

Question: {user_query}
```

**Citation requirements (MANDATORY):**
- Every factual claim in the output must reference its source document
- Use a consistent citation format: [Source: document name] or numbered references
- If the model cannot cite a source for a claim, that claim must not appear in the output

**Context window management:**
- Calculate: system prompt tokens + context tokens + query tokens + output buffer
- If retrieved context exceeds the budget, reduce K or truncate lowest-scoring chunks
- Never silently truncate context — track when it happens and log it

### Step 7: End-to-End Evaluation

Evaluate retrieval and generation separately. If retrieval returns wrong documents, better prompts will not help.

**Retrieval evaluation:**

| Metric | Definition | Target |
|---|---|---|
| Precision@K | Of the K retrieved chunks, how many are relevant? | >= 80% |
| Recall@K | Of all relevant chunks in the corpus, how many were retrieved? | >= 70% |
| MRR | Mean Reciprocal Rank — is the best result near the top? | >= 0.8 |

**Generation evaluation:**

| Metric | Definition | Target |
|---|---|---|
| Answer accuracy | Is the generated answer factually correct? | >= 90% |
| Citation accuracy | Do citations match the actual source of the information? | >= 95% |
| Faithfulness | Does the answer contain ONLY information from the context? | 100% — any hallucination is a failure |
| Completeness | Does the answer address the full question? | >= 85% |

Use [RAGAS](https://docs.ragas.io/) as the industry-standard RAG evaluation framework. The standard RAGAS metrics are: faithfulness, answer_relevancy, context_precision, and context_recall.

**Evaluation process:**
1. Build a test set: 30+ queries with known correct answers and source documents
2. Run retrieval — measure precision, recall, MRR
3. If retrieval metrics fail, fix retrieval (chunking, embedding, K) BEFORE touching generation
4. Run end-to-end — measure accuracy, citations, faithfulness
5. If generation metrics fail with good retrieval, fix the prompt

### Step 8: Freshness and Maintenance

A RAG pipeline that returns stale information is worse than no pipeline — it gives users false confidence.

| Property | Decision |
|---|---|
| Rebuild frequency | Full re-index: [daily / weekly / monthly]. Based on corpus update frequency |
| Incremental updates | New/modified documents indexed within [timeframe]. Requires change detection |
| Change detection | Content hash comparison — re-embed only changed chunks |
| Stale content handling | Documents older than [threshold] flagged in retrieval results |
| Monitoring | Track: index size, query latency, retrieval scores, generation quality over time |

**Rules:**
- Define the freshness SLA: how old can retrieved information be before it causes harm?
- Automate index rebuilds — manual rebuilds will be forgotten
- Monitor retrieval quality over time — corpus drift degrades performance silently
- Log every query that returns zero results or low-confidence results. These are your pipeline's blind spots

## Anti-Patterns (NEVER do these)

- **Evaluating generation without checking retrieval** — if the wrong documents are retrieved, no prompt will save you. Always evaluate retrieval first
- **Fixed chunk sizes for all content types** — a 512-token chunk works for articles but destroys tables and code blocks. Match chunking to content structure
- **No citation requirements** — without citations, users cannot verify answers and hallucinations go undetected
- **No freshness strategy** — an index that is never rebuilt returns increasingly stale answers. Define and automate rebuild frequency
- **Tuning generation when retrieval is broken** — better prompts cannot compensate for irrelevant retrieved context. Fix the retrieval layer first
- **Embedding selection by benchmark** — evaluate on your data, your queries, your domain. Academic benchmarks measure general capability, not your use case
- **Skipping metadata** — without metadata, every query searches the entire corpus. Metadata enables filtered, faster, more relevant retrieval

## Output Format

```markdown
# RAG Pipeline Design: [corpus/knowledge base name]

## Corpus Profile
| Property | Value |
|---|---|
| Document types | [formats] |
| Volume | [count, total size] |
| Update frequency | [cadence] |
| Language | [languages] |

## Chunking Configuration
- **Strategy:** [fixed / semantic / paragraph]
- **Chunk size:** [tokens]
- **Overlap:** [percentage]
- **Boundary rules:** [sentence / paragraph / section]

## Metadata Schema
| Field | Type | Values |
|---|---|---|

## Embedding
- **Model:** [name]
- **Dimensions:** [N]
- **Evaluation results:** [precision/recall on 20-query test]

## Retrieval
- **Strategy:** [similarity / hybrid / re-ranking]
- **Top-K:** [N]
- **Filters:** [metadata filters applied]

## Prompt Template
[Full generation prompt with context injection]

## Evaluation Results

### Retrieval
| Metric | Result | Target | Pass? |
|---|---|---|---|

### Generation
| Metric | Result | Target | Pass? |
|---|---|---|---|

## Freshness Strategy
- **Rebuild frequency:** [cadence]
- **Change detection:** [method]
- **Staleness threshold:** [age limit]

## Monitoring
- [Metrics tracked]
- [Alert conditions]

## Open Questions
- [Decisions pending data or stakeholder input]
```
