# Test Strategy

Scenario: Developer invokes the test-strategy skill for a new document signing feature. Users can upload a PDF, place signature fields, send to signatories, and track completion. This is a legally significant feature with data integrity requirements.

## Prompt

> Define a test strategy for our new document signing feature. Users can: upload a PDF, drag and drop signature fields onto pages, add signatories by email, send for signing, track who has signed, and download the completed document. Legally, the signed document must be tamper-evident and the audit trail must be accurate. We use TypeScript/Vitest for unit tests and Playwright for E2E. Data integrity is critical.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Test Strategy: Document Signing Feature

I've created a comprehensive test strategy in `docs/quality/test-strategy-document-signing.md` with the following structure:

### Key Decisions

**Risk profile → Test allocation:** Your feature has HIGH risk (legal, data integrity, reputation), so I shifted from the default 70/20/10 pyramid to **55% unit / 28% integration / 17% E2E**. This weights toward integration and E2E while keeping unit tests tight on the critical audit trail path (100% coverage required there, non-negotiable).

**Concrete failure modes** (not generic "data integrity"):
- Signature forged (Alice claimed, Bob actually signed) → audit event mismatch
- Document tampered post-signature → hash ≠ audit trail hash
- Audit trail incomplete → missing required fields
- Token reused (signatory identity spoofed) → second sign succeeds with same token
- Audit log loss (DB delete/rollback) → append works, read returns empty

**Test count:** 45 unit + 30 integration + 8 E2E = **83 tests total**

### Quality Gates (Named, Not Generic)

**Pre-merge:**
- Coverage ≥95% on `signing/`, **100% on `audit-trail/`** (append-only critical path)
- Database schema enforces immutability: `ON DELETE RESTRICT`, `ON UPDATE RESTRICT` on audit table
- No PDF operations without validation

**Pre-release:**
- Manual tamper test: modify signed PDF post-download, verify system detects corruption
- Manual audit consistency: 10 multi-signatory workflows, audit events match final state
- Email delivery: invite received within 2min, token single-use, 7-day expiry
- Performance: p95 upload + field injection < 3 seconds

### Gaps (What's Currently Untested)

1. Audit trail immutability under 1000 concurrent appends
2. Timezone edge cases across UTC boundaries
3. Email retry logic on SES timeout
4. Session hijacking during signing
5. Batch operations (100+ concurrent invitations)

### Recommendations (Prioritised)

| P1 | Audit trail immutability tests | 3 days | Core legal requirement |
| P1 | Tamper detection E2E tests | 2 days | Document integrity |
| P1 | Concurrent append ordering | 1 day | Multi-signatory norm |
| P2 | Email dispatch integration | 2 days | Signatory UX |
| P2 | PDF edge cases (50MB+, corrupted) | 2 days | Tampering exposure |

The strategy includes concrete Vitest/Playwright patterns, database schema for immutability enforcement, and success criteria tied to business outcomes (zero audit gaps, tamper detection working, multi-signatory ordering correct).

### Artifacts written

#### `work/docs/quality/test-strategy-document-signing.md`

```
# Test Strategy: Document Signing Feature

## Risk Assessment

**Risk profile:** Legal, data integrity, reputation

A signed document is a legal artifact. Tampering, missing audit trails, or forged signatures expose the platform to fraud liability and destroy customer trust. Audit trail accuracy is non-negotiable.

**Critical flows:**
1. Upload PDF → position signature fields → send invitations
2. Signatory receives email → signs document → audit logged
3. Download completed document with signature metadata
4. Verify audit trail (who signed, when, from where)
5. Detect tampering: compare document hash to audit trail

**Failure modes (concrete, testable):**

| Failure | Risk | Detection |
|---|---|---|
| Signature forged (Alice claimed, Bob signed) | HIGH | Audit event doesn't match document metadata |
| Document tampered post-signature | HIGH | PDF hash ≠ audit trail hash |
| Audit trail incomplete (missing timestamps) | HIGH | Audit event missing required fields |
| Signatory identity spoofed (email reuse) | HIGH | Token reused across signings |
| Audit log loss (DB delete/rollback) | HIGH | Append operation succeeds, read returns empty |
| Downloaded document diverges from audit trail | HIGH | Hash mismatch on final delivery |
| PDF corruption on save (fields lost) | MEDIUM | Field injection not idempotent |
| Race condition on multi-signatory | MEDIUM | Two signers claim same field simultaneously |
| Email interception (link leaked) | MEDIUM | Token reused by unintended recipient |
| Revocation ignored (still signable post-cancel) | LOW | Document downloadable after revocation |

---

## Test Levels

**Allocation:** 55% unit / 28% integration / 17% E2E (shifted from default 70/20/10 due to HIGH-risk constraints)

| Level | Scope | Tools | Coverage Target | Est. Tests |
|---|---|---|---|---|
| **Unit** | Signature validation logic, audit event formatting, hash generation, field positioning, email templates, token generation | Vitest + `vi.mock()` / `vi.hoisted()` | 95% on `signing/` module; 100% on `audit-trail/` | 45 |
| **Integration** | PDF field injection (real pdfjs), audit trail append (real DB), email dispatch, token validation, document hash verification, concurrent writes | Vitest + PostgreSQL testcontainer | All critical paths; 85% on handlers | 30 |
| **E2E** | Complete signing flow (upload → position → invite → sign → download → verify). Tamper detection (modify PDF post-sign → detect). Multi-signatory. Revocation. | Playwright (Chromium) on staging | Top 5 flows + 3 tamper scenarios | 8 |
| **Contract** | API response shape: `/documents/{id}/audit-trail`, `/sign/{token}` | OpenAPI validation (typebox) | All public endpoints | 6 assertions |
| **Security** | Input validation (PDF filename, field count), token expiry, email validation, SQL injection prevention | SAST + manual review | Public API boundary | Covered in integration |
| **Performance** | PDF upload + field injection latency; audit trail query latency @ 1000+ events | k6 spike test | p95 < 3s upload; p95 < 200ms audit query | 2 baselines |

---

## Quality Gates

### Pre-Merge (MUST pass — automated in CI)

- [ ] `CI=true npx vitest run` — all 75 unit+integration tests pass
- [ ] Coverage ≥95% on `src/signing/` module
- [ ] Coverage **100%** on `src/audit-trail/` module (append-only, critical path)
- [ ] `npx tsc --noEmit --strict` — no type errors on public APIs
- [ ] No new security suppressions (`@ts-ignore`, `// eslint-disable`) without justification on signing code
- [ ] Database schema: audit table has `ON DELETE RESTRICT`, `ON UPDATE RESTRICT` (immutability enforced)
- [ ] PDF validation: all input parsed and validated; no raw file operations

### Pre-Release (MUST pass — manual verification on staging)

- [ ] `npx playwright test` — all 8 E2E scenarios pass on staging
- [ ] **Tamper detection manual verification:** Download signed PDF, modify with PDF editor, re-upload, verify system rejects with "document tampered" error
- [ ] **Audit trail consistency manual verification:** Execute 10 multi-signatory workflows; audit trail events match final document state (no gaps, correct ordering)
- [ ] **Email delivery verified:** Signatory receives invite within 2 minutes; signing link works once; token expires after 7 days
- [ ] **Performance baseline met:** PDF upload + field injection @ p95 < 3 seconds (measured on staging hardware)
- [ ] **Security review passed:** Code reviewed for OWASP Top 10 (input validation, XSS, CSRF, SQL injection, sensitive data exposure, auth/authz on signing endpoints)
- [ ] **Accessibility verified:** Email content and web UI signing flow pass WCAG 2.1 AA

---

## Gaps (Currently Untested)

1. **Audit trail immutability under load** — what if 1000 signing events append simultaneously? Ordering preserved? Database constraint enforcement?
2. **Timezone edge cases** — signings across UTC boundaries; timestamp validation and ordering across timezones
3. **Signatory revocation recovery** — document state after revocation; re-invitation behavior; audit trail shows revocation event
4. **PDF corruption resilience** — malformed PDF input; partial upload; truncated file handling
5. **Email delivery failure & retry** — SES/SendGrid timeout; retry logic; exponential backoff testing
6. **Session hijacking during signing** — steal signatory session cookie after email click, before signature submission
7. **Batch operations** — sending 100+ documents for signing simultaneously; rate limiting
8. **Audit trail query performance** — retrieving audit for document with 10,000+ signing events
9. **Unicode handling** — signatory name with emoji or non-ASCII characters; email validation
10. **Token edge cases** — expired token re-used; double-signing on same token; token collision

---

## Recommendations (Prioritised)

| Priority | Item | Justification | Effort | Owner |
|---|---|---|---|---|
| **P1** | **Audit trail immutability tests** | Core legal requirement; any mutation is fraud exposure | 3 days | QA Lead + Engineering |
| **P1** | **Tamper detection E2E tests** | Document integrity is make-or-break; must detect all post-sign modifications | 2 days | QA Engineer (Playwright) |
| **P1** | **Audit trail ordering under concurrent appends** | Multi-signatory docs are the norm; race conditions destroy legal defensibility | 1 day | Engineering |
| **P2** | **Email dispatch integration tests** | Signatory experience hinges on timely, reliable email; retry logic must work | 2 days | Engineering |
| **P2** | **PDF field injection edge cases** — multi-page, large files (50MB+), corrupted input | Field positioning bugs expose signatures to tampering | 2 days | Engineering |
| **P2** | **Performance baseline & regression tests** | Upload latency impacts UX; drift undetected without baseline | 1 day | Engineering |
| **P3** | **Session hijacking scenario** — steal token post-email, pre-signature | Medium-risk vector; token expiry + single-use mitigates but needs test | 1 day | QA Lead (security review) |
| **P3** | **Batch operations load test** — 100+ concurrent signing invitations | Identify load limits before launch | 1 day | DevOps / Performance |

---

## Implementation Notes

### TypeScript / Vitest Patterns

**Signature validation (unit):**
```typescript
describe('signatureValidator', () => {
  it('rejects signature if timestamp outside audit trail bounds', () => {
    const signature = { timestamp: futureDate, signedBy: 'alice@example.com' }
    const auditLog = [
      { timestamp: pastDate, event: 'DocumentCreated' },
      { timestamp: earlyFutureDate, event: 'InvitationSent' }
    ]
    expect(() => validateSignature(signature, auditLog))
      .toThrow(/timestamp.*outside.*audit.*window/)
  })
})
```

**PDF field injection (integration):**
```typescript
describe('pdfFieldInjector', () => {
  let pdfBuffer: Buffer
  
  beforeEach(() => {
    pdfBuffer = loadFixture('sample.pdf')
  })
  
  it('injects signature field idempotently', async () => {
    const injected = await injectFields(pdfBuffer, [
      { page: 1, x: 100, y: 200, width: 50, height: 20, name: 'sig_1' }
    ])
    const hash1 = await hashPdf(injected)
    const hash2 = await hashPdf(injected) // second call
    expect(hash1).toBe(hash2) // idempotent
  })
})
```

**Audit trail (integration with real PostgreSQL):**
```typescript
describe('auditTrailRepository', () => {
  let db: Database
  
  beforeEach(async () => {
    db = await startPostgresTestContainer()
  })
  
  it('enforces immutability: rejects UPDATE on audit events', async () => {
    const inserted = await db.audit.append({
      documentId: 'doc-1',
      event: 'SIGNED',
      signerEmail: 'alice@example.com',
      timestamp: new Date()
    })
    
    const updateAttempt = await db.audit.update(inserted.id, {
      event: 'UNSIGNED'
    })
    expect(updateAttempt.error).toMatch(/immutable|constraint/)
  })
  
  it('maintains event ordering under concurrent appends', async () => {
    const [r1, r2] = await Promise.all([
      db.audit.append({ documentId: 'doc-1', event: 'SIGNED_BY_ALICE' }),
      db.audit.append({ documentId: 'doc-1', event: 'SIGNED_BY_BOB' })
    ])
    
    const events = await db.audit.getByDocument('doc-1')
    const eventNames = events.map(e => e.event)
    expect(eventNames).toEqual(['SIGNED_BY_ALICE', 'SIGNED_BY_BOB'])
  })
})
```

**E2E (Playwright):**
```typescript
test('complete signing flow: upload → position → invite → sign → download → verify', async ({ page }) => {
  // 1. Upload PDF
  await page.goto('/documents/new')
  await page.locator('input[type="file"]').setInputFiles('sample.pdf')
  
  // 2. Position signature field
  await page.locator('[data-testid="pdf-canvas"]').hover({ position: { x: 100, y: 200 } })
  await page.locator('button:has-text("Add Signature Field")').click()
  
  // 3. Send invitation
  await page.locator('input[placeholder="Email"]').fill('alice@example.com')
  await page.locator('button:has-text("Send for Signature")').click()
  
  // 4. Verify email received (mock)
  expect(mockSES.sendEmail).toHaveBeenCalledWith(
    expect.objectContaining({ to: 'alice@example.com' })
  )
  
  // 5. Signatory signs (in new page context)
  const signingLink = mockSES.sendEmail.mock.calls[0][0].body.match(/http.+\/sign\/[a-z0-9]+/)[0]
  const signPage = await browser.newPage()
  await signPage.goto(signingLink)
  await signPage.locator('[data-testid="signature-pad"]').click()
  await signPage.locator('button:has-text("Confirm Signature")').click()
  
  // 6. Verify audit trail updated
  const auditTrail = await db.audit.getByDocument('doc-1')
  expect(auditTrail).toContainEqual(
    expect.objectContaining({
      event: 'SIGNED',
      signerEmail: 'alice@example.com'
    })
  )
  
  // 7. Download and verify hash
  await page.goto('/documents/doc-1')
  const downloadPromise = page.waitForEvent('download')
  await page.locator('button:has-text("Download Signed Document")').click()
  const download = await downloadPromise
  const downloadedPdf = await download.path()
  const downloadHash = await hashPdf(downloadedPdf)
  
  const auditHash = auditTrail.find(e => e.event === 'SIGNED')?.documentHash
  expect(downloadHash).toBe(auditHash)
})
```

### Database Schema (Immutability Enforced)

```sql
CREATE TABLE audit_trail (
  id BIGSERIAL PRIMARY KEY,
  document_id UUID NOT NULL REFERENCES documents(id),
  event TEXT NOT NULL CHECK (event IN ('CREATED', 'INVITED', 'SIGNED', 'REVOKED', 'DOWNLOADED')),
  signer_email VARCHAR(255),
  timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  signature_hash VARCHAR(64) NOT NULL,
  ip_address INET,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  -- Immutability constraints
  CONSTRAINT audit_no_update CHECK (FALSE), -- Prevents UPDATE
  CONSTRAINT audit_no_delete CHECK (FALSE)  -- Prevents DELETE
);

-- Alternative: use triggers to prevent mutation
CREATE OR REPLACE FUNCTION prevent_audit_mutation()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP IN ('UPDATE', 'DELETE') THEN
    RAISE EXCEPTION 'Audit trail is immutable';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_immutable
BEFORE UPDATE OR DELETE ON audit_trail
FOR EACH ROW EXECUTE FUNCTION prevent_audit_mutation();
```

---

## Success Criteria

This test strategy is successful when:

1. **Audit trail immutability verified:** No UPDATE or DELETE ever succeeds on audit_trail table
2. **Tamper detection working:** Modified PDF post-signature is detected and rejected
3. **Multi-signatory ordering correct:** Concurrent signings maintain event order in audit trail
4. **Email delivery reliable:** Invitations sent within 2 minutes; tokens single-use
5. **Performance acceptable:** Upload + field injection < 3s at p95
6. **Zero audit gaps:** All signing flows generate complete audit trail (no missing events)
7. **Tests maintained:** Pre-merge gates passing consistently; flaky tests eliminated

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/15.5 (97%) |
| Evaluated | 2026-05-04 |
| Target duration | 105131 ms |
| Target cost | $0.1613 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill starts by understanding what is being tested — describes the feature, critical user flows, failure modes, external dependencies, and risk profile | PASS | Risk Assessment section lists 5 critical flows (upload→position→invite→sign→download, verify audit trail, detect tampering), a 10-row failure mode table with specific scenarios (forged signature, tampered post-sign, audit trail incomplete), and risk profile 'Legal, data integrity, reputation'. External dependencies appear implicitly in Test Levels (pdfjs, PostgreSQL, SES). |
| c2 | Risk profile explicitly identifies legal/data integrity as high risk — this influences the coverage targets and test level choices | PASS | Risk profile opens with 'A signed document is a legal artifact. Tampering, missing audit trails, or forged signatures expose the platform to fraud liability.' The 55/28/17 pyramid shift is directly attributed to 'HIGH-risk constraints', and 100% coverage on audit-trail/ is called 'non-negotiable' and tied to the legal profile. |
| c3 | Skill defines test levels with tools, coverage targets, and estimated test counts — not just a list of level names | PASS | Test Levels table has six rows, each with Tools column (e.g. 'Vitest + vi.mock() / vi.hoisted()', 'Vitest + PostgreSQL testcontainer', 'Playwright (Chromium) on staging'), Coverage Target column (95% signing/, 100% audit-trail/, 85% handlers), and Est. Tests column (45, 30, 8, 6, and qualitative for remaining rows). |
| c4 | E2E tests are limited to the top critical flows (not every scenario) — full signing flow, tamper detection, audit trail | PASS | E2E scope is stated as 'Complete signing flow (upload → position → invite → sign → download → verify). Tamper detection (modify PDF post-sign → detect). Multi-signatory. Revocation.' with 8 total tests, capped at 'Top 5 flows + 3 tamper scenarios'. Chat response confirms the 8-test ceiling. |
| c5 | Skill identifies specific gaps — areas currently untested or under-tested given the risk profile | PASS | Gaps section lists 10 named, specific items: 'Audit trail immutability under load', 'Timezone edge cases', 'Signatory revocation recovery', 'PDF corruption resilience', 'Email delivery failure & retry', 'Session hijacking during signing', 'Batch operations', 'Audit trail query performance', 'Unicode handling', 'Token edge cases'. |
| c6 | Quality gates are specific and measurable — not generic ("tests pass") but specific thresholds with pass/fail criteria | PASS | Pre-merge gates include exact commands ('CI=true npx vitest run'), numeric thresholds ('Coverage ≥95% on src/signing/', 'Coverage 100% on src/audit-trail/'), and schema constraints ('ON DELETE RESTRICT, ON UPDATE RESTRICT'). Pre-release gates include 'invite received within 2 minutes', 'token expires after 7 days', 'p95 < 3 seconds'. |
| c7 | Security testing is called out separately — auth/authz checks, signed document integrity, and audit trail accuracy | PASS | Test Levels table has a dedicated Security row: 'Input validation (PDF filename, field count), token expiry, email validation, SQL injection prevention \| SAST + manual review'. Pre-release quality gates include 'Security review passed: Code reviewed for OWASP Top 10 (input validation, XSS, CSRF, SQL injection, sensitive data exposure, auth/authz on signing endpoints)'. |
| c8 | Skill addresses the testing pyramid allocation for this risk profile — likely higher than default 70/20/10 toward integration and E2E given legal requirements | PARTIAL | Explicitly states 'Allocation: 55% unit / 28% integration / 17% E2E (shifted from default 70/20/10 due to HIGH-risk constraints)'. Chat response explains the reasoning: HIGH risk justifies shifting from standard pyramid. Ceiling is PARTIAL so maximum score applies. |
| c9 | Output follows the format: Risk Assessment, Test Levels table with tools and coverage, Quality Gates (pre-merge + pre-release), Gaps, and Recommendations | PASS | File has: '## Risk Assessment', '## Test Levels' (tabular with tools and coverage), '## Quality Gates' with '### Pre-Merge' and '### Pre-Release' subsections, '## Gaps (Currently Untested)', '## Recommendations (Prioritised)'. All five required sections present. |
| c10 | Output's risk assessment classifies legal admissibility and tamper-evidence as HIGH risk — naming the specific failure modes (forged signature, post-signing modification, audit trail gap) rather than generic "data integrity" | PASS | Failure modes table explicitly names: 'Signature forged (Alice claimed, Bob signed) \| HIGH', 'Document tampered post-signature \| HIGH' (PDF hash ≠ audit trail hash), 'Audit trail incomplete (missing timestamps) \| HIGH', and 'Audit log loss (DB delete/rollback) \| HIGH'. These match the criterion's named scenarios exactly. |
| c11 | Output's test levels table names Vitest (unit), Vitest + integration test (component + integration), and Playwright (E2E), with explicit coverage targets per level — Vitest unit coverage threshold (e.g. 90%+ given high risk) and Playwright scenario count | PASS | Unit row: 'Vitest + vi.mock() / vi.hoisted()' with '95% on signing/ module; 100% on audit-trail/'. Integration row: 'Vitest + PostgreSQL testcontainer' with '85% on handlers'. E2E row: 'Playwright (Chromium) on staging' with '8' test count ('Top 5 flows + 3 tamper scenarios'). |
| c12 | Output's E2E set is limited to the highest-value flows (full sign cycle, tamper detection, audit trail accuracy) and explicitly excludes lower-value flows that should remain at integration or unit level | PASS | E2E is scoped to 8 tests (full signing flow, tamper detection, multi-signatory, revocation). The Test Levels allocation places field positioning, email template rendering, hash generation, and token generation in the Unit row; PDF field injection and token validation in Integration. The layered allocation functionally excludes those from E2E. |
| c13 | Output's quality gates are specific and measurable — not "all tests pass" but e.g. "100% coverage on the signing module", "0 audit trail gaps in 500 simulated signing flows", "Playwright tamper-detection suite green" | PASS | Pre-merge: 'Coverage 100% on src/audit-trail/ module (append-only, critical path)', exact commands with flags. Pre-release: 'all 8 E2E scenarios pass on staging', '10 multi-signatory workflows; audit trail events match final document state (no gaps, correct ordering)', 'p95 < 3 seconds (measured on staging hardware)'. |
| c14 | Output's pyramid allocation justifies a non-default mix (likely 60/25/15 or 50/30/20 unit/integration/E2E rather than the standard 70/20/10) given the legal risk profile, with reasoning | PASS | 'Allocation: 55% unit / 28% integration / 17% E2E (shifted from default 70/20/10 due to HIGH-risk constraints)'. Chat response adds: 'Your feature has HIGH risk (legal, data integrity, reputation), so I shifted from the default 70/20/10 pyramid.' The specific mix (55/28/17) is non-default and the legal-risk reasoning is explicit in both locations. |
| c15 | Output identifies at least one specific testing gap — e.g. no PDF-tampering test fixtures yet, no cross-signatory race condition coverage, or no key-rotation scenario for the signing certificate | PASS | 10 specific gaps listed. Directly relevant examples: 'Audit trail immutability under load — what if 1000 signing events append simultaneously? Ordering preserved?', 'PDF corruption resilience — malformed PDF input; partial upload; truncated file handling', 'Token edge cases — expired token re-used; double-signing on same token; token collision'. |
| c16 | Output addresses external dependency testing — PDF rendering library, signature library, email delivery — and how each is faked or contract-tested | PARTIAL | PDF library (pdfjs): Integration test uses 'real pdfjs' — method documented. Email delivery (SES): Integration test uses real dispatch; E2E code shows 'mockSES.sendEmail' mock. However, the signature/cryptography library used for tamper-evidence and hash generation is never named as a distinct external dependency, and no faking or contract-testing strategy is described for it. Two of three named dependency types covered. |

### Notes

The output is a strong test strategy response that demonstrates clear understanding of the legal risk profile and translates it into concrete, measurable artefacts. The explicit pyramid shift (55/28/17 vs default 70/20/10) with stated reasoning is a standout. Quality gates are genuinely specific — exact commands, numeric thresholds, time-bounded manual checks. The failure mode table naming Alice/Bob forgery scenarios and hash-mismatch tamper detection is precisely what the criteria ask for. The only material gap is c16: while PDF (pdfjs) and email (SES mock + integration) external dependencies are addressed with testing strategies, the signing/cryptography library responsible for hash generation and tamper detection is never called out as an external dependency requiring its own isolation or contract test. Everything else meets or exceeds the rubric.
