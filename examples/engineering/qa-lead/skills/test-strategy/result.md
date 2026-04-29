# Output: Define test strategy for a document signing feature

**Verdict:** PARTIAL
**Score:** 14.5/19 criteria met (76%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill starts by understanding what is being tested — Step 1 explicitly covers feature description, critical user flows, failure modes, external dependencies, and risk profile
- [x] PASS: Risk profile explicitly identifies legal/data integrity as high risk — Step 1 lists "data integrity" as a named risk category; the payment flow example shows all six levels apply to high-risk scenarios, establishing that legal/data integrity triggers elevated testing
- [x] PASS: Skill defines test levels with tools, coverage targets, and estimated test counts — the Test Levels table includes Level, What it tests, Tools, Coverage target, and the output format adds Est. Tests column
- [x] PASS: E2E tests are limited to the top critical flows — pyramid notes "Few, slow, expensive — critical flows only" and the table says "Top 5-10 flows"
- [x] PASS: Skill identifies specific gaps — Step 5 lists five gap categories with concrete examples
- [~] PARTIAL: Quality gates are specific and measurable — pre-merge and pre-release checklists exist but thresholds are generic ("Coverage above threshold on changed files", "Performance benchmarks met") rather than feature-specific measurable numbers — 0.5
- [x] PASS: Security testing is called out separately — the Test Levels table has a dedicated Security row with OWASP, auth/authz, input validation
- [~] PARTIAL: Skill addresses the testing pyramid allocation for this risk profile — default 70/20/10 is stated with "Adjust based on risk" but no prescription for how much to adjust for legal/data-integrity risk profiles — 0.5
- [x] PASS: Output follows the format: Risk Assessment, Test Levels table, Quality Gates (pre-merge + pre-release), Gaps, and Recommendations — the Output Format section matches exactly

### Output expectations

- [~] PARTIAL: Output's risk assessment classifies legal admissibility and tamper-evidence as HIGH risk naming specific failure modes — the skill's Step 1 includes "data integrity" as a risk category but does not name specific legal failure modes (forged signature, post-signing modification, audit trail gap); a well-formed response following this skill would produce a generic risk list rather than legally-specific failure modes — 0.5
- [ ] FAIL: Output's test levels table names Vitest (unit), Vitest + integration (component + integration), and Playwright (E2E) with explicit coverage targets per level including a 90%+ Vitest unit threshold and Playwright scenario count — the skill's table uses generic tool options ("Vitest / xUnit / pytest", "Playwright / Cypress") and a generic "80%+ changed code" threshold; it would not elevate the unit threshold to 90%+ for high-risk features or produce a named Playwright scenario count
- [x] PASS: Output's E2E set is limited to highest-value flows — the skill constrains E2E to "Top 5-10 flows" with "critical flows only"; the output format would produce a focused E2E set with explicit exclusions
- [ ] FAIL: Output's tamper-detection testing is called out as a security concern with adversarial scenarios — the skill's Security row lists "OWASP, auth/authz, input validation" but mentions nothing about tamper-detection, byte-modification, page-swapping, or identity-swapping adversarial scenarios; these would not appear in output
- [ ] FAIL: Output's audit trail testing asserts every action is captured with actor, timestamp, and document hash — the skill has no guidance on audit trail testing; nothing in the skill would produce assertions about upload, field placement, send, view, sign, and download events each captured with actor, timestamp, and document hash
- [ ] FAIL: Output's quality gates are specific and measurable with feature-specific thresholds — the skill produces generic checklists ("Coverage above threshold", "Performance benchmarks met") not thresholds like "100% coverage on the signing module" or "0 audit trail gaps in 500 simulated signing flows"
- [x] PASS: Output's pyramid allocation justifies a non-default mix — "Adjust based on risk" is explicit and the payment flow example establishes that high-risk features deviate; the skill would produce a reallocation with some reasoning
- [x] PASS: Output identifies at least one specific testing gap — Step 5 covers "Missing edge cases — concurrent" and "Missing levels"; applied to the signing feature this would surface at least one concrete gap
- [x] PASS: Output addresses external dependency testing — the Test Levels table includes Contract tests for API compatibility and the skill's anti-patterns section says "mock only external boundaries"; PDF library, signature library, and email delivery would be covered
- [-] PARTIAL: Output addresses long-term legal evidence requirements as a regression concern with a recommendation to retain signing artefacts for replay verification — the skill has no guidance on long-term artefact retention or replay verification; this would not appear in output — 0

## Notes

The skill is structurally solid for general test strategy work. Its main weakness for legally-significant features is the absence of domain-specific escalation paths: the risk profile step names "data integrity" but does not wire elevated risk into tighter, named quality gates or adversarial security scenarios. A practitioner following this skill for a document signing feature would produce a competent general strategy but miss the adversarial tamper-detection scenarios, the per-action audit trail assertions, and the long-term artefact retention concern that a legal feature demands. The generic quality gate thresholds ("coverage above threshold") are the single biggest gap — the skill gives no mechanism to elevate them when risk is HIGH.
