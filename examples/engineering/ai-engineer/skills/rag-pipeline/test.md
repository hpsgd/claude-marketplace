# Test: RAG pipeline design for product documentation

Scenario: Developer invokes the rag-pipeline skill to design a RAG system over ~800 Markdown product documentation pages that are updated weekly. Users ask how-to questions and troubleshooting queries.

## Prompt

Design a RAG pipeline for our product documentation. We have about 800 Markdown pages covering features, API reference, and troubleshooting guides. Pages average 1,500 words. The content is well-structured with headings. It's updated weekly (usually 20-30 pages change). Users ask questions like "how do I configure SSO?" and "why am I getting error code 4031?" We want cited answers — users should see which doc page the answer came from.

## Criteria

- [ ] PASS: Skill analyses corpus properties (document types, volume, average length, update frequency, structure) before recommending any configuration
- [ ] PASS: Skill recommends semantic or paragraph-based chunking given the well-structured Markdown with headings — not fixed-size chunking for this content type
- [ ] PASS: Skill specifies a mandatory chunk metadata schema including `source_id`, `source_name`, `chunk_index`, `section_heading`, `created_at`, and `content_hash`
- [ ] PASS: Skill requires evaluating embedding models on a 20-query test set from real user queries — not benchmark selection
- [ ] PASS: Skill mandates citation requirements — every generated answer must reference source documents by name
- [ ] PASS: Skill specifies evaluating retrieval (precision@K, recall@K, MRR) separately from generation (faithfulness, accuracy, citation accuracy)
- [ ] PASS: Skill defines a freshness strategy — rebuild frequency, change detection via content hash, and staleness threshold given weekly updates
- [ ] PARTIAL: Skill recommends starting with similarity search K=5 and only adding hybrid search or re-ranking if eval shows retrieval is insufficient
- [ ] PASS: Output covers all pipeline stages with configuration values: chunking, metadata schema, embedding, retrieval, prompt template, evaluation results, and monitoring plan

## Output expectations

- [ ] PASS: Output's corpus profile reproduces the four prompt facts — ~800 Markdown pages, 1,500-word average, 20-30 changes/week, well-structured with headings — and ties each to a downstream pipeline decision
- [ ] PASS: Output's chunking strategy is semantic or heading-based (not fixed-size), with explicit reference to splitting on Markdown H1/H2/H3 boundaries given the structured input
- [ ] PASS: Output's prompt template includes a system instruction with "answer using ONLY the provided context" and "If the answer is not in the context, say 'I don't have enough information'" — verbatim or near-verbatim
- [ ] PASS: Output's prompt template wraps retrieved context with explicit `<context>` tags or equivalent delimiter, and each chunk is labelled `[Source: <doc name>]` so citations can reference document names rather than IDs
- [ ] PASS: Output's evaluation section reports retrieval metrics (precision@K, recall@K, MRR) separately from generation metrics (faithfulness, answer accuracy, citation accuracy), with target thresholds beside each
- [ ] PASS: Output's freshness strategy specifies content-hash change detection so only the 20-30 changed pages each week are re-embedded — not full weekly re-indexing of all 800
- [ ] PASS: Output includes worked examples covering both query types from the prompt — "how do I configure SSO?" (how-to) and "why am I getting error code 4031?" (troubleshooting/exact-match) — and addresses how hybrid search may be needed for the error-code style query
- [ ] PASS: Output's metadata schema names the six mandated fields (`source_id`, `source_name`, `chunk_index`, `section_heading`, `created_at`, `content_hash`) with types
- [ ] PARTIAL: Output names a specific embedding model candidate (e.g. text-embedding-3-small, voyage-3, BGE) with dimensionality, and shows or commits to the 20-query evaluation method rather than just naming a model
- [ ] PARTIAL: Output addresses what happens when retrieval returns chunks with low similarity scores (fall-through behaviour, low-confidence response, or escalation) — not just the happy path
