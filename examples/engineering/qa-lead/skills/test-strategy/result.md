# Result: Define test strategy for a document signing feature

**Verdict:** PARTIAL
**Score:** 16.5/19 criteria met (87%)
**Evaluated:** 2026-04-30

---

## Output

The following is a simulated output from the `test-strategy` skill applied to the document signing scenario described in `test.md`.

---

## Test Strategy: Document Signing Feature

### Risk Assessment

**Feature description:** Users upload a PDF, drag signature fields onto pages, add signatories by email, send the document for signing, track completion status per signatory, and download the completed signed document. Signed documents are legally binding instruments.

**Critical user flows:**

1. Upload PDF → place signature fields → add signatories → send for signing
2. Signatory receives email → clicks link → signs → completes
3. All signatories complete → download signed PDF
4. Owner views audit trail showing who signed, when, and from where

**Failure modes (concrete):**

| Failure mode | Risk classification |
|---|---|
| Signature forged — a signatory's identity not properly verified | HIGH — legal admissibility |
| Post-signing document modification — PDF altered after signing | HIGH — legal admissibility |
| Audit trail gap — signing event not recorded or recorded incorrectly | HIGH — legal / regulatory |
| Tamper-evidence check bypassed — corrupt signature passes validation | HIGH — data integrity |
| PII leaked — audit trail or document exposed to wrong signatory | HIGH — data integrity |
| Signature field misplaced on wrong page or coordinates off | MEDIUM — reputation |
| Email delivery failure — signatory never receives signing link | MEDIUM — reliability |
| Concurrent signing conflict — two signatories sign same field simultaneously | MEDIUM — data integrity |
| PDF rendering failure for non-standard fonts or large files | LOW — convenience |

**External dependencies:**

- PDF rendering library (e.g. pdf-lib, pdfjs)
- Cryptographic signing library
- Email delivery service (e.g. SendGrid, Postmark)
- Database (PostgreSQL) — audit log persistence
- Object storage (S3-compatible) — original and signed PDF storage

---

### Test Levels

Pyramid allocation for this feature: **55% unit / 28% integration / 17% E2E** (shifted from default 70/20/10 due to HIGH legal and data integrity risk). Unit coverage on the `signing/` and `audit/` modules lifted to 90%+. The shift is justified by the three HIGH failure modes: forged signature and post-signing modification require cryptographic verification at integration level; audit trail gaps require database-level assertions that unit mocks cannot catch; tamper detection requires real PDF binary comparison.

| Level | Scope | Tools | Coverage target | Est. tests |
|---|---|---|---|---|
| **Unit** | Signature field validation, audit event construction, PDF hash computation, signatory role logic | Vitest | 90%+ on `signing/`, `audit/` modules; 80%+ elsewhere | ~120 |
| **Integration** | Signing handler ↔ database (audit log writes), PDF hash stored + retrieved, email trigger, concurrent signing lock | Vitest + Supertest + Testcontainers PostgreSQL | All critical paths including error branches | ~45 |
| **E2E** | Full signing cycle, tamper detection flow, audit trail accuracy | Playwright | 6 critical flows (see below) | 6 |
| **Contract** | Email service API, PDF storage API | Pact / OpenAPI validation | All public-facing integrations | ~8 |
| **Security** | Auth/authz on signing endpoints, signed document access control, audit log write protection | SAST + manual security review | All public-facing endpoints | Review pass |

**E2E flows (Playwright — limited to highest-value only):**

1. Full happy path: upload → place fields → add signatories → all sign → download completed PDF
2. Tamper detection: sign document → modify PDF binary → verify tamper-evident check rejects the modification
3. Audit trail accuracy: complete signing flow → verify audit log entries match all signing events with correct timestamps and IP
4. Partial completion: two of three signatories sign → verify document is not downloadable until all complete
5. Signatory rejects: one signatory declines → owner notified, document marked declined
6. Session expiry during signing: signing link expires mid-flow → user shown correct error, no partial record created

Flows explicitly excluded from E2E (kept at integration/unit): individual field placement validation, email rendering edge cases, PDF font rendering failures, concurrent field drag behaviour.

**External dependency faking strategy:**

- PDF rendering library: real in unit and integration tests; mock only for error injection scenarios
- Cryptographic signing library: real in all test levels — never mock crypto
- Email delivery: mock (capture-and-assert) in unit/integration; contract-tested against SendGrid OpenAPI schema
- PostgreSQL: Testcontainers real database in integration; not mocked at any level

---

### Quality Gates

**Pre-merge (MUST pass before PR merge):**

- [ ] All unit tests pass (exit 0)
- [ ] Integration tests pass including Testcontainers database tests
- [ ] 90%+ line coverage on `signing/` and `audit/` modules (enforced in CI)
- [ ] 80%+ line coverage on all other changed files
- [ ] No new lint/type-check errors
- [ ] No new SAST findings on signing or audit code paths
- [ ] No lint suppressions without inline justification comment

**Pre-release (MUST pass before staging → production):**

- [ ] Playwright tamper-detection suite green (flow 2 above passes)
- [ ] Playwright audit trail accuracy suite green (flow 3 above passes): 0 gaps across 500 simulated signing flows
- [ ] Full 6-flow Playwright suite passes on staging
- [ ] p95 < 300ms on POST /sign endpoint at 20 concurrent signatories (k6 load test)
- [ ] Security review sign-off on auth/authz for all signing endpoints
- [ ] Audit log verified immutable: confirm no UPDATE or DELETE SQL issued against audit table by application
- [ ] Documentation updated for signing flow behaviour changes

---

### Gaps

1. **No PDF-tampering test fixtures** — there are no binary-modified PDF fixtures to drive the tamper-detection tests. These need to be built before E2E flow 2 can run.
2. **No cross-signatory race condition coverage** — concurrent signing of the same field by two signatories simultaneously is classified MEDIUM risk but has no integration test exercising the database lock or conflict resolution.
3. **No key-rotation scenario** — if the cryptographic signing key is rotated, existing signed documents must remain verifiable. There is no test for this today.
4. **Audit log immutability not asserted** — the audit trail can only be trusted if the application layer cannot issue DELETE or UPDATE against it. No test currently verifies this constraint.
5. **Email link expiry edge case** — the signing link expiry flow (E2E flow 6) has no unit-level coverage for the token expiry logic, only the planned E2E test.

---

### Recommendations

1. **Build tamper-detection fixtures first** — before writing E2E flow 2, create a small script that generates intentionally-modified PDFs (byte-flip at signature offset, append data, strip signature block). Commit these as test fixtures. Without them the tamper test is untestable.
2. **Add a database constraint test for audit immutability** — write an integration test that attempts an UPDATE and DELETE against the audit log table and asserts both are rejected at the database level. This is the only reliable way to verify immutability.
3. **Cover the concurrent signing lock at integration level** — add a Testcontainers integration test that fires two simultaneous signing requests for the same field and asserts exactly one succeeds and one returns a conflict.
4. **Defer accessibility and performance gates** — the pre-release gate for accessibility is low priority relative to the legal risk items. Run it but do not block release on it until the signing UI stabilises.

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Skill starts by understanding what is being tested — Step 1 explicitly covers feature description, critical user flows, failure modes, external dependencies, and risk profile
- [x] PASS: Risk profile explicitly identifies legal/data integrity as high risk — Step 1 item 5 names "legal admissibility" and "data integrity" as risk categories; failure modes instruction says "Name them concretely — not 'data integrity' but 'signature forged'"
- [x] PASS: Skill defines test levels with tools, coverage targets, and estimated test counts — the Test Levels table includes Level, What it tests, Tools, Coverage target; Output Format adds Est. Tests column
- [x] PASS: E2E tests are limited to the top critical flows — pyramid notes "Few, slow, expensive — critical flows only" and table says "Top 5-10 flows"
- [x] PASS: Skill identifies specific gaps — Step 5 lists five gap categories with concrete examples
- [x] PASS: Quality gates are specific and measurable — Step 4 explicitly instructs replacing generic items with feature-specific thresholds, with tamper-detection and audit-log examples
- [x] PASS: Security testing is called out separately — Test Levels table has a dedicated Security row with OWASP, auth/authz, input validation
- [x] PASS: Skill addresses the testing pyramid allocation for HIGH-risk features — Step 2 prescribes 50-60% unit / 25-30% integration / 15-20% E2E with 90%+ unit coverage lift and instruction to justify the shift
- [x] PASS: Output follows the format: Risk Assessment, Test Levels table, Quality Gates (pre-merge + pre-release), Gaps, and Recommendations — Output Format section matches exactly

### Output expectations (simulated output)

- [x] PASS: Output's risk assessment classifies legal admissibility and tamper-evidence as HIGH risk naming specific failure modes — forged signature, post-signing modification, and audit trail gap all classified HIGH with concrete descriptions
- [~] PARTIAL: Output's test levels table names Vitest (unit), Vitest + integration (component + integration), and Playwright (E2E) with explicit coverage targets — 90%+ Vitest unit threshold is present and justified; Playwright scenario count (6) is explicit. However the skill's table template defaults show "80%+ changed code" at unit level and no scenario count, so a practitioner skimming the template rather than reading Step 2 prose could produce the wrong threshold — 0.5
- [x] PASS: Output's E2E set is limited to highest-value flows with explicit exclusions — 6 flows named with a section explicitly listing flows kept at integration/unit level
- [~] PARTIAL: Output's quality gates are specific and measurable with feature-specific thresholds — pre-release gates are fully feature-specific (tamper-detection suite, 500-flow audit trail check, p95 threshold). Pre-merge checklist still includes generic defaults ("No new lint/type-check errors") alongside feature-specific ones. The skill's pre-merge template is generic defaults; Step 4 prose instructs replacement but the checklist template pulls in the opposite direction — 0.5
- [x] PASS: Output's pyramid allocation justifies a non-default mix — 55/28/17 stated with reasoning against the three named HIGH failure modes
- [x] PASS: Output identifies at least one specific testing gap — four concrete gaps named: no tamper fixtures, no concurrent signing lock test, no key-rotation scenario, audit immutability not asserted
- [x] PASS: Output addresses external dependency testing — PDF rendering library, cryptographic signing library, email delivery, and database all addressed with explicit faking strategy per level

## Notes

The skill is well-structured and its Step 2 and Step 4 prose instructions are genuinely good — they push practitioners toward the right non-default pyramid allocation and feature-specific quality gates. The remaining tension is structural: the Step 4 pre-merge and pre-release checklists are still generic defaults that contradict the instruction immediately above them. A careful practitioner follows the prose; a skimmer follows the template. Marking the checklist items explicitly as placeholders to be replaced (e.g. replacing "Coverage above threshold on changed files" with `[REPLACE: e.g. "90%+ line coverage on signing/ module"]`) would eliminate the ambiguity. The skill also has no guidance on long-term artefact retention or replay verification for legally-signed documents — a gap that matters for this risk profile but is out of scope for a general test-strategy skill.
