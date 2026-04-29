# Output: RAG pipeline for internal documentation search

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Agent defines evaluation criteria before proposing implementation — Principles explicitly state: "Evaluation before implementation. Define how you will measure success before writing a single line of AI integration code."

- [x] PASS: Agent analyses corpus properties before recommending chunking strategy — Step 3 classification orders the RAG pipeline as "Document corpus → chunking strategy → embedding → retrieval → generation → evaluation." Corpus analysis is the first stage.

- [x] PASS: Agent recommends evaluating embedding models on actual user queries rather than benchmarks — Key Decisions: "Evaluate on YOUR data, not benchmarks." What You Don't Do: "Choose models based on hype — evaluate on YOUR data, YOUR use case, YOUR budget."

- [x] PASS: Agent addresses citation requirements — RAG Rules: "Citation. Generated output should reference which source documents it used. Without citations, users can't verify."

- [x] PASS: Agent defines a freshness/rebuild strategy — RAG Rules: "Freshness via incremental indexing. Re-embed only changed documents (track by hash or modified date), not full re-index on every update. Define cadence and what triggers it."

- [x] PASS: Agent includes fallback handling for model unavailability and insufficient context — Failure Modes table covers "Model unavailable" (graceful degradation, queue and retry). Prompt Engineering rules: "If the answer isn't in the context, say 'I don't have enough information.'"

- [x] PASS: Agent raises a decision checkpoint before choosing a model — Decision Checkpoints: "Choosing between 2+ models for a use case → STOP and ask before proceeding. Model selection has cost, latency, and quality trade-offs that need stakeholder input."

- [x] PASS: Agent separates retrieval evaluation from generation evaluation and specifies testing retrieval first — RAG Rules: "Evaluate retrieval before generation. Test retrieval in isolation first — if retrieval returns the wrong documents, better prompts won't help." Both the separation and the sequencing instruction are explicit.

- [x] PASS: Output covers all pipeline stages — Document Ingestion covers chunking config; Key Decisions covers embedding selection, retrieval strategy (similarity, hybrid, re-ranking, Top-K); RAG Rules add metadata enrichment, citation, freshness, access control, cost model; Prompt Structure covers prompt construction; Model Evaluation covers the evaluation plan.

### Output expectations

- [x] PASS: Chunking strategy distinguishes Markdown/HTML Confluence pages from PDFs with OCR acknowledgment — Document Ingestion section explicitly addresses each format: "Markdown/HTML: preserve heading structure as chunk boundaries; strip nav/boilerplate" and "PDFs: use a layout-aware extractor; OCR scanned pages before chunking. Treating a PDF as plain text loses tables, columns, and headings."

- [x] PASS: Specific chunk size and overlap values with reasoning tied to corpus content — Document Ingestion: "Tie chunk size to content type. Procedural content (runbooks, step-by-step guides) prefers smaller chunks aligned to steps; reference content prefers larger chunks that keep concepts together. State the chosen size and overlap with reasoning, not generic defaults." This directly maps to runbooks vs Confluence pages.

- [x] PASS: Retrieval design addresses ownership/team queries via metadata filtering or hybrid retrieval — Key Decisions: "Hybrid or metadata filtering is required for ownership/attribute queries (e.g. 'which team owns X')." RAG Rules add metadata enrichment including owning team.

- [x] PASS: Monthly cost calculation breaks down embedding cost plus per-query LLM generation cost — RAG Rules: "Break costs into one-time ingestion embedding, incremental re-embed on changes, and per-query generation. A monthly figure must reconcile against the budget at projected query volume." The three-part structure is explicit.

- [x] PASS: Prompt template includes citation instruction and response schema includes citations array — RAG Rules mandate citation for every answer. Principles: "Structured output over free text. Use JSON mode, function calling, or schema validation to enforce output format." The combination mandates a citations array in structured output.

- [x] PASS: Incremental indexing strategy rather than full re-indexing — RAG Rules: "Re-embed only changed documents (track by hash or modified date), not full re-index on every update." Directly addresses the criterion.

- [x] PASS: Evaluation plan lists named queries from the prompt's domain with expected source documents — RAG Rules: "List named queries from real user questions, each paired with the source documents that should answer them. The eval set is part of the design output, not an afterthought." The requirement to name queries and pair with source documents is explicit.

- [~] PARTIAL: Names specific embedding model candidates and a specific generation model with cost justification — Key Decisions instructs the agent to "Name specific current candidates" and "Justify each by cost-per-million-tokens against the budget." The definition prescribes the behaviour but does not itself name candidates (text-embedding-3-small, voyage-3, BGE, etc.). A response following the definition would name models; whether it names the right ones depends on what the agent picks at runtime. 0.5 per PARTIAL rubric.

- [x] PASS: Access control — RAG Rules: "Internal corpora often have permissions. Filter retrieval by the asking user's access scope, or chunks become a leak vector. Never return content the user isn't entitled to see." Also: RAG Rules include "owning team, and access scope" in metadata enrichment.

## Notes

The agent definition was substantially updated since the previous evaluation. The Document Ingestion section now explicitly handles PDF extraction and OCR, ties chunk size to content type (procedural vs reference), and the RAG Rules section added six new rules covering incremental indexing, access control, a structured cost model, and a domain-specific eval set requirement. These additions resolved four previously-failing criteria.

The one remaining gap: the definition instructs the agent to name specific embedding model candidates, but does not itself name any (just says "Name specific current candidates"). This means the criterion is partially met — the behaviour is prescribed but the specific names are not guaranteed. Any well-formed response following the definition should name models; the definition just doesn't constrain which ones.

The definition is now a strong RAG engineering guide. The access control rule, incremental indexing, and domain-specific eval set requirements move it well beyond generic AI engineering advice into production-grade RAG design territory.
