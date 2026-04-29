# Output: RAG pipeline for internal documentation search

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 13/18 criteria met (72%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Agent defines evaluation criteria before proposing implementation — Principles explicitly state: "Evaluation before implementation. Define how you will measure success before writing a single line of AI integration code." This fires before any configuration is recommended.

- [x] PASS: Agent analyses corpus properties before recommending chunking strategy — Step 3 classification orders the RAG pipeline as "Document corpus → chunking strategy → embedding → retrieval → generation → evaluation." Corpus analysis is the first stage in the prescribed sequence.

- [x] PASS: Agent recommends evaluating embedding models on actual user queries rather than benchmarks — RAG Key Decisions: "Match to your content domain. Evaluate on YOUR data, not benchmarks." What You Don't Do: "Choose models based on hype — evaluate on YOUR data, YOUR use case, YOUR budget." The 20-query number isn't in the definition, but the behavioural requirement (real queries, not benchmarks) is explicit.

- [x] PASS: Agent addresses citation requirements — RAG Rules include a dedicated "Citation" rule: "Generated output should reference which source documents it used. Without citations, users can't verify."

- [x] PASS: Agent defines a freshness/rebuild strategy — RAG Rules: "Freshness. Define how often the index is rebuilt. Stale indexes give stale answers." Directly maps to the weekly update cadence in the scenario.

- [x] PASS: Agent includes fallback handling for model unavailability and insufficient context — Failure Modes table covers "Model unavailable" (graceful degradation, queue and retry). Prompt Engineering rules cover insufficient context: "If the answer isn't in the context, say 'I don't have enough information.'"

- [x] PASS: Agent raises a decision checkpoint before choosing a model — Decision Checkpoints: "Choosing between 2+ models for a use case → STOP and ask before proceeding. Model selection has cost, latency, and quality trade-offs that need stakeholder input." The $500/month budget is a direct trigger.

- [~] PARTIAL: Agent separates retrieval evaluation from generation evaluation and specifies testing retrieval first — RAG Rules: "Evaluate retrieval separately from generation. If retrieval returns the wrong documents, better prompts won't help." Principle is explicit; the specific sequencing instruction is implied. 0.5 per PARTIAL rubric.

- [x] PASS: Output covers all pipeline stages — Key Decisions table covers chunking config, embedding selection, retrieval strategy (similarity, hybrid, re-ranking, Top-K); RAG Rules add metadata enrichment, citation, and freshness; Prompt Structure covers prompt construction; Model Evaluation framework covers evaluation. All required stages addressed.

### Output expectations

- [ ] FAIL: Chunking strategy distinguishes Markdown/HTML Confluence pages from PDFs with OCR acknowledgment — the agent definition is silent on PDF extraction, OCR, or layout-aware parsing. Key Decisions gives generic chunk size options with no document-type-specific handling. A response following the definition would not reliably address this.

- [~] PARTIAL: Specific chunk size and overlap values with reasoning tied to corpus content — Key Decisions lists "256/512/1024 tokens" and "0/10%/20% overlap" as options with generic trade-off notes ("Smaller = more precise retrieval, larger = more context per chunk"). No reasoning is tied to procedural runbooks vs reference documentation specifically. Options present, domain-specific reasoning absent. 0.5.

- [x] PASS: Retrieval design addresses ownership/team queries via metadata filtering or hybrid retrieval — RAG Key Decisions explicitly includes hybrid retrieval (similarity + keyword) and re-ranking. RAG Rules include "Metadata enrichment. Add source, date, category to chunks — enables filtered retrieval." Both handles are in the definition.

- [~] PARTIAL: Monthly cost calculation breaks down embedding cost (one-time + weekly re-embed) plus per-query LLM generation cost — the Model Evaluation framework includes cost as a dimension ("Per-token cost × average tokens per request × request volume") and Principles call cost a first-class metric. However, the RAG-specific breakdown (one-time ingestion embed vs. incremental re-embed vs. per-query generation) is not prescribed. Generic cost tracking present; structured breakdown absent. 0.5.

- [x] PASS: Prompt template includes citation instruction and response schema includes citations array — RAG Rules mandate citation for every answer. Principles: "Structured output over free text. Use JSON mode, function calling, or schema validation to enforce output format." The combination strongly implies a citations array in structured output; both elements are in the definition.

- [ ] FAIL: Incremental indexing strategy (only re-embed changed docs) rather than full re-indexing — RAG Rules say "Define how often the index is rebuilt" but say nothing about incremental vs full re-indexing. The definition addresses freshness cadence only. A response following the definition would define a rebuild schedule without necessarily reasoning about incremental change detection.

- [ ] FAIL: Evaluation plan lists 10-20 example queries from the prompt's domain with expected source documents — the definition mandates evaluation on real queries but specifies no count, no domain tie, and no expectation that the eval set be presented as part of the design output. The substance of this criterion (named queries, expected sources) is absent.

- [~] PARTIAL: Names specific embedding model candidates (e.g. text-embedding-3-small, voyage-3, BGE) and specific generation model with cost justification — the definition says "Various" for embedding models and describes generation models only by class ("Haiku-class", "Sonnet-class"). No specific model names appear anywhere. 0.5 per PARTIAL rubric.

- [ ] FAIL: Access control — the definition covers guardrails (input validation, PII redaction, audit trail, cost controls) but is entirely silent on document-level permissions and the risk of returning restricted chunks to unauthorised users. 0 per PARTIAL rubric (criterion not met at all).

## Notes

The agent definition has strong AI engineering principles — evaluation-first, citation as mandatory, fallbacks everywhere, decision checkpoints on model selection. These carry the Criteria section convincingly.

The Output expectations section reveals a gap between principles and RAG-engineering specifics. Three areas the definition does not address at all: PDF extraction and OCR handling before chunking, incremental indexing of changed documents, and access control on retrieved content. A well-designed RAG system for internal docs needs all three — the definition's silence here is a real gap, not a minor omission.

Two areas are partially covered: chunk size options are listed but not reasoned against corpus type, and cost tracking is generic rather than split across the RAG cost structure (ingestion embed vs re-embed vs per-query generation). Both would produce adequate but imprecise outputs.

The definition would benefit from a RAG-specific subsection that covers: document ingestion (format-aware extraction), incremental indexing strategies, access control integration, and a cost model template that separates ingestion from query costs.
