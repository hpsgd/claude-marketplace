# Review Standards

Scenario: A developer submits a PR with commented-out code, an unjustified lint suppression, and a README update containing several banned phrases. The review-standards skill covers cross-cutting concerns across all these file types.

## Prompt

> Review this PR. `src/auth/session.ts` has a block of 8 lines commented out with `// old session logic` above it, plus a `// eslint-disable-next-line @typescript-eslint/no-explicit-any` with no justification comment. The `README.md` update contains: "In today's rapidly evolving landscape, our platform leverages cutting-edge synergies to streamline the developer experience. It's important to note that comprehensive documentation fosters a robust ecosystem." Also, the PR touches two bounded contexts — `src/ingestion/service.ts` uses `failProcess()` while `src/extraction/service.ts` uses `recordFailed()` for the same semantic operation.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Four issues to raise:

---

**1. Dead code — `src/auth/session.ts`**

Delete the 8 commented-out lines. Commented-out code with a label like `// old session logic` is clutter — if that logic is ever needed again, git history is the right place to recover it, not the source file.

---

**2. Unsupported ESLint suppression — `src/auth/session.ts`**

`// eslint-disable-next-line @typescript-eslint/no-explicit-any` without explanation is a code smell hidden behind a linter bypass. Either fix the type, or add a justification comment explaining *why* `any` is unavoidable (e.g. "third-party SDK returns untyped payload"). Suppressions without rationale rot silently.

---

**3. README filler — `README.md`**

The paragraph starting "In today's rapidly evolving landscape..." is content-free marketing copy. Remove it entirely. Every sentence in documentation should answer a concrete question a reader might have; "fosters a robust ecosystem" answers none.

---

**4. Semantic inconsistency across bounded contexts**

`failProcess()` in `src/ingestion/service.ts` and `recordFailed()` in `src/extraction/service.ts` represent the same operation. This split will force readers to hold two mental models for one concept and will create friction when searching or cross-referencing. Agree on one name before merging — `recordFailed` is more descriptive of what the function does rather than what to do next, which is the better framing.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 6.0/18.0 (33%) |
| Evaluated | 2026-05-01 |
| Target duration | 24841 ms |
| Target cost | $0.0550 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all four mandatory passes for the file types in scope | FAIL | Output is a flat four-bullet list with no mention of structured passes, pass numbering, or pass-scoped execution. No pass structure is present anywhere in the output. |
| c2 | Commented-out code block is flagged as a Pass 1 dead code finding with file reference and the specific comment as evidence | PARTIAL | Output references `src/auth/session.ts` and quotes `// old session logic` as the marker — file reference and evidence present. However, 'Pass 1' is never mentioned; no pass label or pass-scoped structure exists. |
| c3 | Lint suppression without justification comment is flagged as a Pass 2 finding | PARTIAL | Output flags `// eslint-disable-next-line @typescript-eslint/no-explicit-any` in `src/auth/session.ts` and explains why it is problematic. But 'Pass 2' is never mentioned and no pass-scoped structure exists. |
| c4 | Banned words in README (leverage, cutting-edge, synergies, streamline, robust, ecosystem, comprehensive, fosters) are flagged individually in Pass 6 | FAIL | Output calls the paragraph 'content-free marketing copy' but lists no banned words individually. None of the eight words (leverages, cutting-edge, synergies, streamline, robust, ecosystem, comprehensive, fosters) are named, and there is no Pass 6 structure. |
| c5 | Banned phrases ("In today's rapidly evolving", "It's important to note", "best practices" pattern) are flagged in Pass 6 | PARTIAL | Output quotes "In today's rapidly evolving landscape..." in the README bullet, implicitly flagging it. However, "It's important to note that" is not flagged separately; "best practices" is not addressed; and no Pass 6 label exists. |
| c6 | Every finding includes exact file, line evidence, the specific rule violated, and a concrete fix | PARTIAL | File names are present for findings 1, 2, 4 but absent for 3 (README). No line numbers are given for any finding. No rule names or rule IDs are cited. Concrete fixes are provided (delete, add justification, remove paragraph, standardise name), so that element is met. |
| c7 | Output uses the defined summary template with counts by severity (critical, important, suggestion) | FAIL | Output contains no summary template, no severity labels (critical/important/suggestion), and no finding counts. It is a flat unranked four-item list. |
| c8 | Inconsistent naming across bounded contexts is flagged — `failProcess()` vs `recordFailed()` for the same operation violates the naming consistency rule | PASS | Finding 4 explicitly names both `failProcess()` in `src/ingestion/service.ts` and `recordFailed()` in `src/extraction/service.ts`, states they represent the same operation, and flags the naming split as a problem. |
| c9 | Zero-finding gate is applied correctly — skill does not pad findings with acceptable patterns listed in the anti-patterns section | PASS | Output raises exactly four findings, all of which correspond to real issues described in the prompt. No padding with non-issues or acceptable patterns is observed. |
| c10 | Output flags the commented-out code block in `src/auth/session.ts` with the line range and the `// old session logic` marker as evidence — recommendation is to delete (git history preserves it), not "consider removing" | PARTIAL | Output says "Delete the 8 commented-out lines" (not hedged as 'consider') and references `// old session logic` as the marker with the git-history rationale. However, no line range is given. |
| c11 | Output flags the `// eslint-disable-next-line @typescript-eslint/no-explicit-any` without justification as a Pass 2 finding — naming the project rule that lint suppressions require an inline justification comment | PARTIAL | Output flags the suppression and says to 'add a justification comment explaining why `any` is unavoidable' — the required behaviour is identified. But there is no 'Pass 2' label and no named project rule cited. |
| c12 | Output flags each banned word individually in Pass 6 — `leverages`, `cutting-edge`, `synergies`, `streamline`, `robust`, `comprehensive`, `fosters`, `ecosystem` — with the specific banned-vocab tier each falls under | FAIL | No banned word is named individually. No vocab tiers are mentioned. The README paragraph is dismissed as a whole as 'content-free marketing copy'. |
| c13 | Output flags banned phrases — "In today's rapidly evolving landscape", "It's important to note that" — separately from the banned single-words | FAIL | "In today's rapidly evolving landscape" is quoted as part of the paragraph description but not flagged as a discrete banned phrase. "It's important to note that" is not mentioned at all. No separation from single-word findings exists (since single-word findings are absent). |
| c14 | Output provides a rewritten README sentence demonstrating the lean, on-voice version — not just listing what's wrong | FAIL | Output recommends removal entirely and states what good documentation should do, but provides no rewritten example sentence demonstrating the lean, on-voice version. |
| c15 | Output flags the cross-context naming inconsistency — `failProcess()` vs `recordFailed()` for the same semantic operation — citing both files and recommending which name to standardise on, with reasoning | PASS | Finding 4 names both files, both function names, explains they represent the same operation, recommends `recordFailed`, and gives explicit reasoning: 'more descriptive of what the function does rather than what to do next'. |
| c16 | Output's findings each include exact file, line evidence, the specific rule violated (named or quoted), and a concrete fix | FAIL | No finding includes a line number. No finding names a specific rule (named or quoted from a standard). File names appear in 3 of 4 findings only. All four required elements are not present for any single finding. |
| c17 | Output uses the defined summary template with counts by severity (critical / important / suggestion) at the top — not a flat unranked list | FAIL | Output is a flat four-item unranked list. No severity classification, no counts, no summary template appears anywhere. |
| c18 | Output runs all four mandatory passes for the file types in scope and reports per-pass finding counts even where zero findings | FAIL | No pass structure exists in the output. No pass labels, no per-pass counts, no zero-finding acknowledgements for any pass. |
| c19 | Output addresses the README content beyond just banned words — flags the AI-tells in sentence rhythm (uniform sentence length, abstract claims) per the writing-style rules, not only vocabulary | PARTIAL | Output notes the paragraph is 'content-free' and that 'every sentence in documentation should answer a concrete question a reader might have', which goes beyond vocabulary to address abstraction. However, 'AI-tells in sentence rhythm' and 'uniform sentence length' are not explicitly mentioned. |

### Notes

The captured output demonstrates basic triage competence — it correctly identifies all four real issues and provides reasonable plain-English explanations. However, it fails almost every structural requirement of the review-standards skill. There is no pass framework (Pass 1 / Pass 2 / Pass 6), no severity summary template, no per-pass counts, no line numbers, and no named rule citations. The README finding is the weakest: none of the eight banned words are listed individually, 'It's important to note that' is not flagged, no rewritten replacement sentence is provided, and the analysis does not reach AI-tells in sentence rhythm. The skill appears to have been invoked but executed as a freeform opinion rather than following its structured methodology, costing it on the majority of criteria that require that structure.
