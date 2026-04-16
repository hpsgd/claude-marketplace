# Test: RAG pipeline for internal documentation search

Scenario: User wants to build a RAG pipeline so employees can ask natural language questions against the company's internal documentation corpus (~2,000 Confluence pages and ~500 PDF runbooks).

## Prompt

We want to let our support and engineering teams search our internal docs using natural language. We have about 2,000 Confluence pages (mostly Markdown/HTML) and ~500 PDF runbooks, totalling roughly 800MB. Documents are updated a few times a week. Questions are things like "what's the rollback procedure for the payments service?" or "which team owns the authentication microservice?". We need citations so users know where answers came from. Budget is $500/month for AI costs. Can you design this RAG pipeline?

## Criteria

- [ ] PASS: Agent defines evaluation criteria (retrieval precision/recall targets, faithfulness requirement, latency budget) BEFORE proposing implementation
- [ ] PASS: Agent analyses corpus properties (document types, volume, update frequency) before recommending chunking strategy
- [ ] PASS: Agent recommends evaluating embedding models on a 20-query test set from actual user queries — not choosing by benchmark alone
- [ ] PASS: Agent addresses citation requirements — every generated answer must reference source documents
- [ ] PASS: Agent defines a freshness/rebuild strategy given the weekly update cadence
- [ ] PASS: Agent includes fallback handling for model unavailability and cases where context is insufficient to answer
- [ ] PASS: Agent raises a decision checkpoint before choosing a model (cost/quality trade-off needs stakeholder input given $500/month budget)
- [ ] PARTIAL: Agent separates retrieval evaluation from generation evaluation and specifies testing retrieval first
- [ ] PASS: Output covers all pipeline stages: chunking config, metadata schema, embedding selection, retrieval strategy, prompt template, and evaluation plan
