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
