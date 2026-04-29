# Test: Define test strategy for a document signing feature

Scenario: Developer invokes the test-strategy skill for a new document signing feature. Users can upload a PDF, place signature fields, send to signatories, and track completion. This is a legally significant feature with data integrity requirements.

## Prompt

Define a test strategy for our new document signing feature. Users can: upload a PDF, drag and drop signature fields onto pages, add signatories by email, send for signing, track who has signed, and download the completed document. Legally, the signed document must be tamper-evident and the audit trail must be accurate. We use TypeScript/Vitest for unit tests and Playwright for E2E. Data integrity is critical.

## Criteria

- [ ] PASS: Skill starts by understanding what is being tested — describes the feature, critical user flows, failure modes, external dependencies, and risk profile
- [ ] PASS: Risk profile explicitly identifies legal/data integrity as high risk — this influences the coverage targets and test level choices
- [ ] PASS: Skill defines test levels with tools, coverage targets, and estimated test counts — not just a list of level names
- [ ] PASS: E2E tests are limited to the top critical flows (not every scenario) — full signing flow, tamper detection, audit trail
- [ ] PASS: Skill identifies specific gaps — areas currently untested or under-tested given the risk profile
- [ ] PASS: Quality gates are specific and measurable — not generic ("tests pass") but specific thresholds with pass/fail criteria
- [ ] PASS: Security testing is called out separately — auth/authz checks, signed document integrity, and audit trail accuracy
- [ ] PARTIAL: Skill addresses the testing pyramid allocation for this risk profile — likely higher than default 70/20/10 toward integration and E2E given legal requirements
- [ ] PASS: Output follows the format: Risk Assessment, Test Levels table with tools and coverage, Quality Gates (pre-merge + pre-release), Gaps, and Recommendations

## Output expectations

- [ ] PASS: Output's risk assessment classifies legal admissibility and tamper-evidence as HIGH risk — naming the specific failure modes (forged signature, post-signing modification, audit trail gap) rather than generic "data integrity"
- [ ] PASS: Output's test levels table names Vitest (unit), Vitest + integration test (component + integration), and Playwright (E2E), with explicit coverage targets per level — Vitest unit coverage threshold (e.g. 90%+ given high risk) and Playwright scenario count
- [ ] PASS: Output's E2E set is limited to the highest-value flows (full sign cycle, tamper detection, audit trail accuracy) and explicitly excludes lower-value flows that should remain at integration or unit level
- [ ] PASS: Output's tamper-detection testing is called out as a security concern with adversarial scenarios — modifying a byte after signing, swapping a page, replacing a signatory's identity — each as a Playwright or integration test
- [ ] PASS: Output's audit trail testing asserts every action is captured (upload, field placement, send, view, sign, download) with the actor, timestamp, and document hash recorded
- [ ] PASS: Output's quality gates are specific and measurable — not "all tests pass" but e.g. "100% coverage on the signing module", "0 audit trail gaps in 500 simulated signing flows", "Playwright tamper-detection suite green"
- [ ] PASS: Output's pyramid allocation justifies a non-default mix (likely 60/25/15 or 50/30/20 unit/integration/E2E rather than the standard 70/20/10) given the legal risk profile, with reasoning
- [ ] PASS: Output identifies at least one specific testing gap — e.g. no PDF-tampering test fixtures yet, no cross-signatory race condition coverage, or no key-rotation scenario for the signing certificate
- [ ] PASS: Output addresses external dependency testing — PDF rendering library, signature library, email delivery — and how each is faked or contract-tested
- [ ] PARTIAL: Output addresses long-term legal evidence requirements (e.g. signed documents must verify years later) as a regression concern, with a recommendation to retain signing artefacts for replay verification
