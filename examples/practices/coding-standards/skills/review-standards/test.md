# Test: review-standards dead code and writing violations

Scenario: A developer submits a PR with commented-out code, an unjustified lint suppression, and a README update containing several banned phrases. The review-standards skill covers cross-cutting concerns across all these file types.

## Prompt

Review this PR. `src/auth/session.ts` has a block of 8 lines commented out with `// old session logic` above it, plus a `// eslint-disable-next-line @typescript-eslint/no-explicit-any` with no justification comment. The `README.md` update contains: "In today's rapidly evolving landscape, our platform leverages cutting-edge synergies to streamline the developer experience. It's important to note that comprehensive documentation fosters a robust ecosystem." Also, the PR touches two bounded contexts — `src/ingestion/service.ts` uses `failProcess()` while `src/extraction/service.ts` uses `recordFailed()` for the same semantic operation.

A few specifics for the response (output structured per the review-standards template):

- **Run all 4 passes** in order: **Pass 1 (Dead code & redundancy)**, **Pass 2 (Lint suppressions & type escapes)**, **Pass 3 (Naming consistency across contexts)**, **Pass 4 (Writing style — banned vocab/phrases)**. Even passes with zero findings get a "Pass N: 0 findings" line.
- **Per-pass summary table at top**:
  ```
  | Pass | Topic | Findings |
  |------|-------|----------|
  | 1 | Dead code & redundancy | 1 |
  | 2 | Lint suppressions & type escapes | 1 |
  | 3 | Naming consistency across contexts | 1 |
  | 4 | Writing style (banned vocab/phrases) | (count) |
  ```
- **Each finding uses structured format**: `**Severity:** CRITICAL/IMPORTANT/SUGGESTION | **Pass:** N | **File:** path:line-range | **Evidence:** \`exact code or text\` | **Rule violated:** [named rule from project standards] | **Fix:** [concrete fix or rewrite]`.
- **Pass 1 finding**: `src/auth/session.ts` — 8 commented-out lines marked with `// old session logic`. Severity IMPORTANT. Fix: delete (git history preserves it). Rule: "no commented-out code; git history is the archive."
- **Pass 2 finding**: same file, `// eslint-disable-next-line @typescript-eslint/no-explicit-any` without justification comment. Severity IMPORTANT. Fix: add inline justification (`// eslint-disable-next-line @typescript-eslint/no-explicit-any -- third-party type stub forces unknown shape`) OR remove suppression and refactor to drop `any`. Rule: "all lint suppressions require an inline justification comment."
- **Pass 3 finding**: `src/ingestion/service.ts::failProcess()` vs `src/extraction/service.ts::recordFailed()` — same semantic operation, two names. Severity IMPORTANT. Fix: pick one canonical name (`recordFailed()` recommended) and rename across both contexts. Rule: "naming consistency across bounded contexts."
- **Pass 4 findings (one per banned word/phrase, individually listed)**:
  - `leverages` — Tier 1 banned vocab (verb form). Replace with `uses`.
  - `cutting-edge` — Tier 1 banned vocab. Delete.
  - `synergies` — Tier 1 banned vocab. Replace or delete.
  - `streamline` — Tier 1 banned vocab. Replace with `simplify` or delete.
  - `comprehensive` — Tier 1 banned vocab. Delete.
  - `fosters` — Tier 1 banned vocab. Replace with `builds` or `supports`.
  - `robust` — Tier 1 banned vocab (outside technical contexts). Delete.
  - `ecosystem` — Tier 2 contextual flag. Replace with `community`, `tools`, etc.
  - **Banned phrase**: `"In today's rapidly evolving landscape"` — banned phrase pattern.
  - **Banned phrase**: `"It's important to note that"` — banned phrase pattern.
  - **AI-tells in rhythm**: uniform sentence length, abstract claims with no concrete referent.
- **Rewritten README sentence** (mandatory): provide a lean on-voice replacement, e.g. "Good documentation makes onboarding faster — this update adds the worked examples developers asked for." Show the rewrite, don't just say "delete the paragraph."
- **Cross-references at end**: `## Related skills` listing `/coding-standards:review-typescript`, `/coding-standards:review-git`, `/writing-style:style-guide`.

## Criteria

- [ ] PASS: Skill executes all four mandatory passes for the file types in scope
- [ ] PASS: Commented-out code block is flagged as a Pass 1 dead code finding with file reference and the specific comment as evidence
- [ ] PASS: Lint suppression without justification comment is flagged as a Pass 2 finding
- [ ] PASS: Banned words in README (leverage, cutting-edge, synergies, streamline, robust, ecosystem, comprehensive, fosters) are flagged individually in Pass 6
- [ ] PASS: Banned phrases ("In today's rapidly evolving", "It's important to note", "best practices" pattern) are flagged in Pass 6
- [ ] PASS: Every finding includes exact file, line evidence, the specific rule violated, and a concrete fix
- [ ] PASS: Output uses the defined summary template with counts by severity (critical, important, suggestion)
- [ ] PASS: Inconsistent naming across bounded contexts is flagged — `failProcess()` vs `recordFailed()` for the same operation violates the naming consistency rule
- [ ] PARTIAL: Zero-finding gate is applied correctly — skill does not pad findings with acceptable patterns listed in the anti-patterns section

## Output expectations

- [ ] PASS: Output flags the commented-out code block in `src/auth/session.ts` with the line range and the `// old session logic` marker as evidence — recommendation is to delete (git history preserves it), not "consider removing"
- [ ] PASS: Output flags the `// eslint-disable-next-line @typescript-eslint/no-explicit-any` without justification as a Pass 2 finding — naming the project rule that lint suppressions require an inline justification comment
- [ ] PASS: Output flags each banned word individually in Pass 6 — `leverages`, `cutting-edge`, `synergies`, `streamline`, `robust`, `comprehensive`, `fosters`, `ecosystem` — with the specific banned-vocab tier each falls under
- [ ] PASS: Output flags banned phrases — "In today's rapidly evolving landscape", "It's important to note that" — separately from the banned single-words
- [ ] PASS: Output provides a rewritten README sentence demonstrating the lean, on-voice version — not just listing what's wrong
- [ ] PASS: Output flags the cross-context naming inconsistency — `failProcess()` vs `recordFailed()` for the same semantic operation — citing both files and recommending which name to standardise on, with reasoning
- [ ] PASS: Output's findings each include exact file, line evidence, the specific rule violated (named or quoted), and a concrete fix
- [ ] PASS: Output uses the defined summary template with counts by severity (critical / important / suggestion) at the top — not a flat unranked list
- [ ] PASS: Output runs all four mandatory passes for the file types in scope and reports per-pass finding counts even where zero findings
- [ ] PARTIAL: Output addresses the README content beyond just banned words — flags the AI-tells in sentence rhythm (uniform sentence length, abstract claims) per the writing-style rules, not only vocabulary
