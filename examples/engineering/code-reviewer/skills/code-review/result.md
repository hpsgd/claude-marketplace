# Output: code-review skill structure

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines four passes in sequence — Context, Correctness, Security, Quality — and requires reading full file context not just the diff — met. "Before Starting" step 2 states explicitly: "For every changed file, read the entire file — not just the diff." Passes are named and sequenced: Pass 1 Context and Intent, Pass 2 Correctness, Pass 3 Security, Pass 4 Quality and Maintainability.
- [x] PASS: Skill distinguishes HARD signals (blockers — will cause wrong behaviour in production) from SOFT signals (important but conditional) — met. Defined under Pass 2 Scoring: HARD = "will cause wrong behavior in production" (blockers), SOFT = "might cause issues under specific conditions" (important, not blocking).
- [x] PASS: Skill's correctness pass covers logic errors, null/undefined handling, race conditions, edge cases, and error propagation — met. All five areas are explicitly listed as numbered sub-items in Pass 2. Error handling is item 5, covering happy path, propagation, and actionability.
- [x] PASS: Skill's security pass covers injection, auth/authz, data exposure, and cryptography — met. Pass 3 has four numbered items matching exactly: Injection, Authentication and authorization, Data exposure, Cryptography.
- [x] PASS: Skill includes a friction scan assessing developer experience, debuggability, rollback safety, and feature flag need — met. The Friction Scan section lists all four as numbered items: Developer experience, Debugging, Rollback, Feature flags.
- [x] PASS: Skill defines a zero-finding gate — if clean, must name a specific positive assertion with file:line to prove review depth — met. The Zero-Finding Gate section requires naming "one positive assertion with a `file:line` reference" and provides a concrete example.
- [x] PASS: Skill's output format includes a verdict (APPROVE, REQUEST_CHANGES, NEEDS_DISCUSSION) with a count of blockers, important, and suggestion findings — met. Output template includes all three verdict options with their conditions, and a summary line `Files reviewed: N | Blockers: X | Important: Y | Suggestions: Z`.
- [x] PASS: Skill's calibration rules prohibit findings without evidence, findings without fix suggestions, and style preferences not codified in team standards — met. Calibration Rules section states all three prohibitions explicitly.

### Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample code review — met. This output verifies each criterion against the skill definition.
- [x] PASS: Output verifies the four passes are named in sequence — Context, Correctness, Security, Quality — and that the Context pass requires reading full files, not just diff hunks — met. Pass 1 is "Context and Intent." "Before Starting" step 2 explicitly requires reading the entire file for every changed file.
- [x] PASS: Output confirms HARD vs SOFT signal taxonomy is defined, with HARD as production-incorrect-behaviour blockers and SOFT as conditional/important — met. SKILL.md: HARD = "will cause wrong behavior in production," SOFT = "might cause issues under specific conditions."
- [x] PASS: Output verifies the correctness pass coverage list — logic errors, null/undefined, race conditions, edge cases, error propagation — and the security pass list — injection, auth/authz, data exposure, cryptography — met. Both lists confirmed present and complete in the skill.
- [x] PASS: Output confirms the friction scan covers DX, debuggability, rollback safety, and feature flag need — met. All four items confirmed present in the Friction Scan section.
- [x] PASS: Output verifies the zero-finding gate forces a positive assertion with file:line citation when nothing is found, preventing rubber-stamp approvals — met. The skill provides an inline example showing exactly this pattern.
- [x] PASS: Output confirms the verdict format names APPROVE / REQUEST_CHANGES / NEEDS_DISCUSSION exactly, with counts of blockers / important / suggestions — met. Both the verdict options and the summary count line are confirmed present in the output template.
- [x] PASS: Output verifies calibration rules: no finding without evidence, no finding without fix suggestion, no style preference unless codified in team standards — met. All three confirmed present in the Calibration Rules section.
- [~] PARTIAL: Output identifies any gaps — e.g. no explicit guidance on how to handle large diffs (review prioritisation), no documented behaviour for review of tests-only or generated-code PRs — partially met. No triage guidance exists for large diffs: "Before Starting" counts files and lines but gives no instruction on how to prioritise or sequence review when the diff is large. No documented behaviour for tests-only or generated-code PRs where the standard passes don't apply cleanly.

## Notes

The skill is well-constructed. The four-pass structure, HARD/SOFT taxonomy, zero-finding gate, and calibration rules are all present and specific. The friction scan is a genuine differentiator — most code review definitions fold operational concerns into the quality pass or omit them entirely.

The calibration rule "'Consider whether...' is not a finding. Either it is a problem or it is not." closes the most common escape hatch for vague reviewers.

The zero-finding gate inverts the usual failure mode: requiring a named positive assertion with a file reference is a concrete mechanism against rubber-stamp approvals.

The one substantive gap: no triage guidance for large diffs. The skill instructs reading every full file, which breaks down on a 50-file refactor, a generated migration, or a vendored dependency update. A brief prioritisation note — HARD signals first, security pass before quality pass — would close this. Similarly, no mention of tests-only or generated-code PRs where the correctness and security passes are largely inapplicable.
