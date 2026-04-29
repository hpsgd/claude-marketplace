# Test: code-review skill structure

Scenario: Checking that the code-review skill enforces a structured four-pass methodology with HARD/SOFT signal distinction, mandatory adversarial analysis, and a friction scan — not just a diff skim.

## Prompt

Review the code-review skill definition and verify it produces systematic, evidence-based reviews rather than informal feedback.

## Criteria

- [ ] PASS: Skill defines four passes in sequence — Context, Correctness, Security, Quality — and requires reading full file context not just the diff
- [ ] PASS: Skill distinguishes HARD signals (blockers — will cause wrong behaviour in production) from SOFT signals (important but conditional)
- [ ] PASS: Skill's correctness pass covers logic errors, null/undefined handling, race conditions, edge cases, and error propagation
- [ ] PASS: Skill's security pass covers injection, auth/authz, data exposure, and cryptography
- [ ] PASS: Skill includes a friction scan assessing developer experience, debuggability, rollback safety, and feature flag need
- [ ] PASS: Skill defines a zero-finding gate — if clean, must name a specific positive assertion with file:line to prove review depth
- [ ] PASS: Skill's output format includes a verdict (APPROVE, REQUEST_CHANGES, NEEDS_DISCUSSION) with a count of blockers, important, and suggestion findings
- [ ] PASS: Skill's calibration rules prohibit findings without evidence, findings without fix suggestions, and style preferences not codified in team standards

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample code review
- [ ] PASS: Output verifies the four passes are named in sequence — Context, Correctness, Security, Quality — and that the Context pass requires reading full files, not just diff hunks
- [ ] PASS: Output confirms HARD vs SOFT signal taxonomy is defined, with HARD as production-incorrect-behaviour blockers and SOFT as conditional/important
- [ ] PASS: Output verifies the correctness pass coverage list — logic errors, null/undefined, race conditions, edge cases, error propagation — and the security pass list — injection, auth/authz, data exposure, cryptography
- [ ] PASS: Output confirms the friction scan covers DX, debuggability, rollback safety, and feature flag need
- [ ] PASS: Output verifies the zero-finding gate forces a positive assertion with file:line citation when nothing is found, preventing rubber-stamp approvals
- [ ] PASS: Output confirms the verdict format names APPROVE / REQUEST_CHANGES / NEEDS_DISCUSSION exactly, with counts of blockers / important / suggestions
- [ ] PASS: Output verifies calibration rules: no finding without evidence, no finding without fix suggestion, no style preference unless codified in team standards
- [ ] PARTIAL: Output identifies any gaps — e.g. no explicit guidance on how to handle large diffs (review prioritisation), no documented behaviour for review of tests-only or generated-code PRs
