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
