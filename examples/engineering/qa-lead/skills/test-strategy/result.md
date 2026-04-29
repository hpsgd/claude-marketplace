# Output: Define test strategy for a document signing feature

**Verdict:** PARTIAL
**Score:** 16.5/19 criteria met (87%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill starts by understanding what is being tested — Step 1 explicitly covers feature description, critical user flows, failure modes, external dependencies, and risk profile
- [x] PASS: Risk profile explicitly identifies legal/data integrity as high risk — Step 1 item 5 names "legal admissibility" and "data integrity" as risk categories; the failure modes instruction says "Name them concretely — not 'data integrity' but 'signature forged'" which directly applies to this feature
- [x] PASS: Skill defines test levels with tools, coverage targets, and estimated test counts — the Test Levels table includes Level, What it tests, Tools, Coverage target, and the output format adds Est. Tests column
- [x] PASS: E2E tests are limited to the top critical flows — pyramid notes "Few, slow, expensive — critical flows only" and the table says "Top 5-10 flows"
- [x] PASS: Skill identifies specific gaps — Step 5 lists five gap categories with concrete examples
- [x] PASS: Quality gates are specific and measurable — Step 4 explicitly instructs replacing generic items with feature-specific thresholds ("'Coverage above threshold' becomes '100% line coverage on signing/ module'"; "'All tests pass' becomes 'Playwright tamper-detection suite green, 0 audit-log gaps in 500 simulated flows'")
- [x] PASS: Security testing is called out separately — the Test Levels table has a dedicated Security row with OWASP, auth/authz, input validation
- [x] PASS: Skill addresses the testing pyramid allocation for this risk profile — Step 2 explicitly states HIGH-risk features run 50-60% unit / 25-30% integration / 15-20% E2E with lifted unit coverage to 90%+ on the risky module, with instruction to "justify the shift against the named HIGH-risk failure modes"
- [x] PASS: Output follows the format: Risk Assessment, Test Levels table, Quality Gates (pre-merge + pre-release), Gaps, and Recommendations — the Output Format section matches exactly

### Output expectations

- [x] PASS: Output's risk assessment classifies legal admissibility and tamper-evidence as HIGH risk naming specific failure modes — Step 1 instructs naming failure modes concretely ("not 'data integrity' but 'signature forged'") and Step 1.5 names "legal admissibility" explicitly; a well-formed response would classify forged signature, post-signing modification, and audit trail gap as HIGH
- [~] PARTIAL: Output's test levels table names Vitest (unit), Vitest + integration test (component + integration), and Playwright (E2E) with explicit coverage targets per level including a 90%+ Vitest unit threshold and Playwright scenario count — Step 2 says to lift unit coverage to 90%+ for HIGH-risk features; the skill names Vitest and Playwright explicitly; the output would include these tools with elevated thresholds. However the skill's Test Levels table still shows a generic "80%+ changed code" unit target and does not prescribe a named Playwright scenario count, so a practitioner may produce the correct threshold from the Step 2 prose but the table template defaults could pull in the wrong direction — 0.5
- [x] PASS: Output's E2E set is limited to highest-value flows — the skill constrains E2E to "Top 5-10 flows" with "critical flows only"; a focused E2E set with explicit exclusions would follow
- [~] PARTIAL: Output's quality gates are specific and measurable with feature-specific thresholds — Step 4 now explicitly instructs this with the "Playwright tamper-detection suite green, 0 audit-log gaps in 500 simulated flows" example; a practitioner following this skill would produce measurable gates. However the pre-merge and pre-release checklists still show generic defaults ("Coverage above threshold", "Performance benchmarks met") that contradict the instruction immediately above them — a practitioner may follow the examples or may follow the template, creating inconsistency — 0.5
- [x] PASS: Output's pyramid allocation justifies a non-default mix — Step 2 explicitly prescribes 50-60/25-30/15-20 for HIGH-risk features and requires justification against named HIGH-risk failure modes
- [x] PASS: Output identifies at least one specific testing gap — Step 5 covers "Missing edge cases — concurrent" and "Missing levels"; applied to the signing feature this would surface at least one concrete gap
- [x] PASS: Output addresses external dependency testing — the Test Levels table includes Contract tests for API compatibility and the anti-patterns section says "mock only external boundaries"; PDF library, signature library, and email delivery would be covered
- [-] SKIP: Output addresses long-term legal evidence requirements as a regression concern — the skill has no guidance on long-term artefact retention or replay verification; this is absent and would not appear in output

## Notes

The skill has been materially strengthened since an earlier evaluation. The three biggest prior gaps are now addressed: Step 1 explicitly names concrete failure modes (forged signature as the canonical example), Step 2 prescribes the non-default HIGH-risk pyramid allocation (50-60/25-30/15-20) with a 90%+ unit coverage lift, and Step 4 explicitly instructs practitioners to replace generic thresholds with feature-specific ones using tamper-detection and audit-log examples. The remaining tension is between the Step 4 prose instruction (good) and the pre-merge/pre-release checklists below it (still generic defaults). A practitioner reading carefully would follow the instruction; one skimming might follow the checklist template. Aligning the checklist defaults with the instruction — or marking them as placeholders to be replaced — would close this gap.
