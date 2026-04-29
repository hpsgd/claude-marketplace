# Test: review-standards dead code and writing violations

Scenario: A developer submits a PR with commented-out code, an unjustified lint suppression, and a README update containing several banned phrases. The review-standards skill covers cross-cutting concerns across all these file types.

## Prompt

Review this PR. `src/auth/session.ts` has a block of 8 lines commented out with `// old session logic` above it, plus a `// eslint-disable-next-line @typescript-eslint/no-explicit-any` with no justification comment. The `README.md` update contains: "In today's rapidly evolving landscape, our platform leverages cutting-edge synergies to streamline the developer experience. It's important to note that comprehensive documentation fosters a robust ecosystem." Also, the PR touches two bounded contexts — `src/ingestion/service.ts` uses `failProcess()` while `src/extraction/service.ts` uses `recordFailed()` for the same semantic operation.

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
