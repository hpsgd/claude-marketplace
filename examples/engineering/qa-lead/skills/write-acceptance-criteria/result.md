# Write Acceptance Criteria

Scenario: Developer invokes the write-acceptance-criteria skill for a story: "As an admin, I want to import users from a CSV file so that I can onboard multiple users at once." The CSV supports up to 1,000 rows with columns: email, name, role (admin/member/viewer).

## Prompt

> /qa-lead:write-acceptance-criteria "As an admin, I want to import users from a CSV file so I can onboard multiple users at once." The CSV has columns: email, name, role (must be admin, member, or viewer). Max 1,000 rows per import. Duplicate emails (already in the system) should be skipped, not error. Invalid rows (bad email format, invalid role) should be collected and shown to the admin after import completes — the valid rows should still be processed. Only users with the 'admin' role can access this feature.
> 
> Execution requirements (follow these when writing the criteria):
> 
> - Each of the four core business rules — admin-only access, max 1,000 rows, duplicate-email-skipped, invalid-row-collection — must be its OWN top-level Rule block (separate `### Rule N:` heading). Do not embed duplicate handling inside an email-validation rule; it gets its own block with at least 2 scenarios.
> - Every Then step verifies exactly ONE observable outcome. If two outcomes happen, write them as separate `And` steps. No compound Thens like "Then they see X and are redirected to Y" — split into two lines.
> - Speak in business language. NEVER write HTTP status codes (no `403`, `200`, `500`) inside Given/When/Then steps. For permission-denied scenarios use phrases like "the admin sees a permission-denied message" and redirect behaviour as a separate observable outcome.
> - Summary counts in scenarios must differentiate the three buckets: imported / skipped-duplicate / invalid (e.g. `the admin sees a summary: "847 imported, 3 skipped (already exist), 2 invalid (validation errors)"`). Do not lump "skipped" and "invalid" together.
> - Non-functional time budgets must be tied to a UX expectation. E.g. "under 30 seconds — keeps the import in a synchronous flow with a loading indicator; over this requires a background job and progress notification." State the rationale, not just the number.
> - Include a malformed-file scenario for a corrupt file format — binary garbage uploaded with a `.csv` extension, AND a wrong-delimiter file (e.g. semicolons instead of commas). Each gets its own scenario with explicit expected behaviour.
> - The Open Questions section MUST raise the privilege-escalation concern explicitly: "What happens when an admin imports a CSV that grants the `admin` role to other users? Is this allowed silently, gated behind a confirmation, or rejected?" — flagged as a question for the product owner, not silently allowed in any rule.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've written comprehensive acceptance criteria for the CSV user import feature. Here's what I included:

**Key Structure:**
- **Four core business rules** as separate sections (admin-only access, 1,000-row limit, duplicate handling, invalid-row collection)
- **Multiple scenarios per rule** including happy path, error cases, and edge cases
- **Business language throughout** — no HTTP status codes, clear observable outcomes
- **Detailed summary format** differentiating the three buckets: imported / skipped-duplicate / invalid

**Coverage includes:**
- Privilege escalation red flag in Open Questions (what if an admin imports a CSV granting admin roles?)
- Two malformed file scenarios: binary garbage (.csv extension) and semicolon delimiters
- Validation errors for email format, role values, missing columns, missing required fields
- Mixed scenarios showing all three outcome categories in a single import
- Duplicate detection both from existing DB and within the same file

**Non-Functional Criteria:**
- Performance tied to UX (under 10s → synchronous flow; under 30s → avoid background job requirement)
- File size limit (5 MB), accessibility, security baseline

**Test Levels** map each criterion to unit/integration/E2E so the team knows where to verify it.

The criteria are now ready for a 3 amigos review (Product Owner + Architect + QA) before implementation starts.

### Artifacts written

#### `work/acceptance-criteria-csv-import.md`

```
# Acceptance Criteria: CSV User Import

**Story:** As an admin, I want to import users from a CSV file so I can onboard multiple users at once.

**Scope:** Admin can upload a CSV file containing email, name, and role; the system processes rows, handles duplicates and validation errors, and reports results. | **Out of scope:** Bulk editing of imported users after import, scheduled/queued imports, CSV templates or generation, role-based permissions beyond "admin" designation, audit logging (handled by system audit mechanism separately).

---

## Business Rules and Scenarios

### Rule 1: Only admins can access the import feature

**Scenario: Admin user can access the import page**
- Given a user with admin role is logged in
- When they navigate to the user import page
- Then the page loads successfully
- And they see a form to upload a CSV file

**Scenario: Member user cannot access the import feature**
- Given a user with member role is logged in
- When they attempt to navigate to the user import page
- Then they are redirected to a page they have permission to access
- And they see a permission-denied message

**Scenario: Viewer user cannot access the import feature**
- Given a user with viewer role is logged in
- When they attempt to navigate to the user import page
- Then they are redirected to a page they have permission to access
- And they see a permission-denied message

---

### Rule 2: Maximum 1,000 rows per import

**Scenario: CSV with 500 rows imports successfully**
- Given an admin is on the import page
- And they have a valid CSV file with 500 rows (1 header row, 499 data rows)
- When they upload the file and initiate the import
- Then the import begins processing
- And all valid rows are imported

**Scenario: CSV with exactly 1,000 data rows imports successfully**
- Given an admin is on the import page
- And they have a valid CSV file with 1,001 total rows (1 header, 1,000 data rows)
- When they upload the file and initiate the import
- Then the import begins processing
- And all 1,000 data rows are processed

**Scenario: CSV with more than 1,000 data rows is rejected**
- Given an admin is on the import page
- And they have a CSV file with 1,002 total rows (1 header, 1,001 data rows)
- When they upload the file and initiate the import
- Then the file is rejected
- And they see an error message: "CSV exceeds maximum of 1,000 rows (you provided 1,001 data rows)"

---

### Rule 3: Duplicate emails are skipped without error

**Scenario: CSV with one duplicate email skips the duplicate and imports the new user**
- Given 5 users already exist in the system with emails: alice@example.com, bob@example.com, carol@example.com, dave@example.com, eve@example.com
- And an admin is on the import page
- And they have a CSV file with 4 rows:
  - alice@example.com, Alice Smith, member
  - frank@example.com, Frank Wu, admin
  - grace@example.com, Grace Lee, viewer
  - bob@example.com, Bob Johnson, admin
- When they upload the file and initiate the import
- And the import completes
- Then they see a summary: "2 imported, 2 skipped (already exist), 0 invalid (validation errors)"
- And the new users frank@example.com and grace@example.com are added to the system
- And alice@example.com and bob@example.com remain unchanged (no update, no duplicate entry)

**Scenario: CSV with all duplicate emails skips all rows**
- Given 3 users already exist in the system: alice@example.com, bob@example.com, carol@example.com
- And an admin is on the import page
- And they have a CSV file with 3 rows, all with existing emails
- When they upload the file and initiate the import
- And the import completes
- Then they see a summary: "0 imported, 3 skipped (already exist), 0 invalid (validation errors)"
- And no new users are added

**Scenario: CSV with duplicate emails within the same file skips extras**
- Given an admin is on the import page
- And they have a CSV file with 4 rows:
  - alice@example.com, Alice Smith, member
  - frank@example.com, Frank Wu, admin
  - alice@example.com, Alice Different, viewer
  - grace@example.com, Grace Lee, viewer
- When they upload the file and initiate the import
- And the import completes
- Then they see a summary: "2 imported, 1 skipped (duplicate in file), 0 invalid (validation errors)"
- And the system imports the first occurrence of alice@example.com and skips the second occurrence within the same file
- And frank@example.com and grace@example.com are imported

---

### Rule 4: Invalid rows are collected and shown to admin after import

**Scenario: CSV with invalid email format is collected and reported**
- Given an admin is on the import page
- And they have a CSV file with 4 rows:
  - alice@example.com, Alice Smith, member
  - not-an-email, Bob Johnson, member
  - carol@example.com, Carol White, admin
  - bob@invalid, Dave Lee, viewer
- When they upload the file and initiate the import
- And the import completes
- Then they see a summary: "2 imported, 0 skipped (already exist), 2 invalid (validation errors)"
- And the valid rows (alice@example.com and carol@example.com) are imported into the system
- And the invalid rows are listed with the reason: "Row 2: invalid email format 'not-an-email'" and "Row 4: invalid email format 'bob@invalid'"

**Scenario: CSV with invalid role is collected and reported**
- Given an admin is on the import page
- And they have a CSV file with 4 rows:
  - alice@example.com, Alice Smith, member
  - bob@example.com, Bob Johnson, superuser
  - carol@example.com, Carol White, admin
  - dave@example.com, Dave Lee, owner
- When they upload the file and initiate the import
- And the import completes
- Then they see a summary: "2 imported, 0 skipped (already exist), 2 invalid (validation errors)"
- And the valid rows (alice@example.com and carol@example.com) are imported into the system
- And the invalid rows are listed with the reason: "Row 2: invalid role 'superuser' (must be admin, member, or viewer)" and "Row 4: invalid role 'owner' (must be admin, member, or viewer)"

**Scenario: CSV with mixed valid, invalid, and duplicate rows reports all categories separately**
- Given 1 user already exists: existing@example.com
- And an admin is on the import page
- And they have a CSV file with 8 rows:
  - new1@example.com, New User 1, member
  - invalid-email, Bad User 2, member
  - existing@example.com, Existing User, admin
  - new2@example.com, New User 3, admin
  - new3@example.com, New User 4, invalid-role
  - new1@example.com, Duplicate New User 5, viewer
  - new4@example.com, New User 6, viewer
  - , Missing Email User, member
- When they upload the file and initiate the import
- And the import completes
- Then they see a summary: "4 imported, 1 skipped (already exist), 3 invalid (validation errors)"
- And new1@example.com, new2@example.com, new4@example.com are imported on their first occurrence
- And the invalid rows are listed separately:
  - "Row 2: invalid email format 'invalid-email'"
  - "Row 5: invalid role 'invalid-role' (must be admin, member, or viewer)"
  - "Row 6: duplicate email 'new1@example.com' within file (first occurrence at row 1 already imported)"
  - "Row 8: missing required field 'email'"

**Scenario: CSV with all invalid rows shows results without importing anything**
- Given an admin is on the import page
- And they have a CSV file with 3 rows, all invalid:
  - bad-email-1, User One, invalid-role
  - bad-email-2, User Two, member
  - , User Three, admin
- When they upload the file and initiate the import
- And the import completes
- Then they see a summary: "0 imported, 0 skipped (already exist), 3 invalid (validation errors)"
- And no rows are imported
- And all 3 invalid rows are displayed with their error reasons

**Scenario: CSV with missing required columns is rejected as malformed**
- Given an admin is on the import page
- And they have a CSV file with headers: email, name (missing the role column)
- When they upload the file and initiate the import
- Then the file is rejected
- And they see an error message: "CSV is missing required columns: role"

**Scenario: CSV with binary garbage uploaded as .csv extension**
- Given an admin is on the import page
- And they have a file named "data.csv" containing binary garbage (not valid text)
- When they upload the file and initiate the import
- Then the file is rejected
- And they see an error message: "File could not be read as CSV. Please ensure the file is in valid CSV format."

**Scenario: CSV with semicolon delimiters instead of comma**
- Given an admin is on the import page
- And they have a CSV file using semicolons (;) as delimiters instead of commas:
  - email;name;role
  - alice@example.com;Alice Smith;member
  - bob@example.com;Bob Johnson;admin
- When they upload the file and initiate the import
- Then the file is rejected
- And they see an error message: "CSV format not recognized. Please ensure the file uses comma delimiters and standard CSV format."

---

## Non-Functional Criteria

| Category | Criterion | Threshold | Rationale |
|---|---|---|---|
| **Performance** | Import completes for 500-row file | Under 10 seconds at p95 | Keeps import in synchronous flow with a simple loading indicator; admin stays on the page and sees results immediately. Larger files may require background processing (future enhancement). |
| **Performance** | Import completes for 1,000-row file | Under 30 seconds at p95 | At this scale, a background job may become necessary if the sync time exceeds 30s; if sync stays under 30s, keeps admin in the UI without needing progress notifications. |
| **Accessibility** | File upload form navigable by keyboard | Full form completion without mouse | Tab through upload field, select file, submit form. |
| **Accessibility** | Error summary readable by screen reader | All error rows announced with row number and reason | Screen reader users must understand which rows failed and why without viewing the table visually. |
| **Security** | File size limit enforced | Max 5 MB | Prevents abuse (DOS via large file upload) and unintended scenarios. |
| **Security** | No sensitive data (passwords, tokens) in import | Import does not create passwords or expose auth tokens | CSV import sets only: email, name, role. No password generation or token exposure. |

---

## Test Level Mapping

| Criterion | Level | Notes |
|---|---|---|
| Admin-only access (permission checks) | Integration | Requires auth middleware to verify role before allowing access. |
| Non-admin user redirected | Integration | Requires auth + route protection. |
| Row limit validation (under 1,000) | Unit | Pure logic; can test with in-memory CSV parser. |
| Row limit validation (over 1,000) | Unit | Pure logic; can test with in-memory CSV parser. |
| Duplicate email detection (existing in DB) | Integration | Requires database lookup. |
| Duplicate email detection (within file) | Unit | Pure logic; can test with in-memory CSV. |
| Email format validation | Unit | Regex or validator library; no dependencies. |
| Role validation (against enum) | Unit | Pure logic; check against allowed values. |
| Invalid rows collected and reported | Integration | Requires database (duplicate check) + file parsing (validation). |
| Mixed results summary | Integration | Requires database + full processing flow. |
| Malformed file rejection (binary) | Unit | File type detection (magic bytes). |
| Malformed file rejection (wrong delimiter) | Unit | CSV parser should detect unexpected format; unit-testable. |
| Missing required columns rejection | Unit | Header validation before processing. |
| Happy path end-to-end (valid CSV imported) | E2E | Full flow: upload → process → verify in DB. |
| Performance threshold (500 rows, <10s) | Performance | Benchmark test under load. |
| Performance threshold (1,000 rows, <30s) | Performance | Benchmark test under load. |
| Keyboard navigation (upload form) | Manual + E2E | Playwright can test keyboard flow; manual review for screen reader parity. |

---

## Open Questions

| Question | Impact | Owner |
|---|---|---|
| **Privilege escalation concern:** What happens when an admin imports a CSV that grants the `admin` role to other users? Is this allowed silently, gated behind a confirmation, or rejected entirely? | Blocks security design. An admin could escalate another user to admin silently, or accidentally grant admin during a bulk import. | Product Owner / Security Lead |
| What is the expected behavior when an email is invalid but structurally resemble a valid format (e.g., user@localhost, user+tag@example.com)? Should these be accepted or rejected? | Affects email validation rules and may cause false rejections if too strict. | Product Owner / Architect |
| Should the system allow importing users with the same name but different emails, or enforce unique names? | Affects validation rules; current spec does not mention name uniqueness. | Product Owner |
| When duplicates are skipped, should the admin have an option to review and update the existing user instead of skipping? | Affects UX flow; current spec only skips. May need a follow-up feature. | Product Owner |
| Should imported users receive a welcome email or notification? | Affects post-import workflow; current spec is silent on this. | Product Owner |
| Is there a confirmation step before the import is finalized, or does the import execute immediately upon file submission? | Affects UX flow; clarifies whether admin can cancel after reviewing invalid rows. | Product Owner / UX Lead |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.5 (95%) |
| Evaluated | 2026-05-03 |
| Target duration | 52737 ms |
| Target cost | $0.1215 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill decomposes the story into business rules before writing scenarios — identifies: permission rule, duplicate handling rule, invalid row rule, max row limit rule | PASS | The artifact has four separate `### Rule N:` blocks: Rule 1 (admin-only access), Rule 2 (max 1,000 rows), Rule 3 (duplicate emails skipped), Rule 4 (invalid rows collected). All four rules from the prompt are identified. |
| c2 | Each business rule has at least 2 concrete examples (not just one) | PASS | Rule 1 has 3 scenarios, Rule 2 has 3 scenarios, Rule 3 has 3 scenarios, Rule 4 has 7 scenarios. Every rule exceeds the minimum of 2 concrete examples. |
| c3 | Scenarios use business language — "Then the admin sees a summary showing 847 imported and 3 skipped" not "Then the API returns 200" | PASS | All Then steps use business language, e.g. "Then they see a summary: '2 imported, 2 skipped (already exist), 0 invalid (validation errors)'" and "Then they are redirected to a page they have permission to access". No HTTP status codes appear anywhere in the scenarios. |
| c4 | Every Given establishes state, every When is a single action, every Then verifies one observable outcome | PASS | Each scenario follows the pattern correctly. Multiple outcomes are split into separate And steps, e.g. "Then the file is rejected" / "And they see an error message: ..." and "Then they are redirected to a page they have permission to access" / "And they see a permission-denied message". No compound Thens like "Then X and Y" in a single step. |
| c5 | Edge cases are mandatory and covered: empty CSV, CSV with all invalid rows, exactly 1000 rows (boundary), 1001 rows (over limit) | PARTIAL | Three of the four required edge cases are present: 'Scenario: CSV with all invalid rows shows results without importing anything', 'Scenario: CSV with exactly 1,000 data rows imports successfully', and 'Scenario: CSV with more than 1,000 data rows is rejected' (1,001 rows). The empty CSV (0 data rows) scenario is entirely absent — there is no scenario specifying whether an empty CSV is rejected or accepted as a no-op. |
| c6 | Error cases are covered: non-admin attempting import (403 behaviour), malformed CSV file (not just bad data but bad file format) | PASS | Rule 1 includes 'Scenario: Member user cannot access the import feature' and 'Scenario: Viewer user cannot access the import feature' using permission-denied language. Rule 4 includes 'Scenario: CSV with binary garbage uploaded as .csv extension' and 'Scenario: CSV with semicolon delimiters instead of comma' — both covering corrupt file format (not just bad data). |
| c7 | Non-functional criteria are included with thresholds — import of 1,000 rows should complete within a specific time budget | PASS | The Non-Functional Criteria table includes 'Import completes for 1,000-row file \| Under 30 seconds at p95' and 'Import completes for 500-row file \| Under 10 seconds at p95', each with a Rationale column explaining the UX implication. |
| c8 | Open questions are flagged explicitly — e.g. what happens if an admin imports a CSV that would give another user the admin role? | PARTIAL | The Open Questions section includes: 'Privilege escalation concern: What happens when an admin imports a CSV that grants the `admin` role to other users? Is this allowed silently, gated behind a confirmation, or rejected entirely?' Flagged as owned by 'Product Owner / Security Lead'. Ceiling is PARTIAL per rubric. |
| c9 | Test level mapping assigns each criterion to unit, integration, or E2E with rationale | PASS | A full 'Test Level Mapping' table is present, mapping 17 criteria to Unit/Integration/E2E with a Notes column explaining rationale, e.g. 'Row limit validation (under 1,000) \| Unit \| Pure logic; can test with in-memory CSV parser' and 'Happy path end-to-end \| E2E \| Full flow: upload → process → verify in DB'. |
| c10 | Output identifies the four business rules from the prompt — admin-only access, max 1,000 rows per import, duplicate emails skipped (not error), invalid rows collected and shown to admin while valid rows process — each as a separate Rule block with at least 2 examples | PASS | The artifact has four separate `### Rule N:` headings mapping exactly to the four prompt rules. Each has at least 2 scenarios: Rule 1 (3), Rule 2 (3), Rule 3 (3), Rule 4 (7). |
| c11 | Output's permission scenarios cover both admin can access (happy path) and non-admin gets 403/permission-denied behaviour (in business language — "the user sees a permission denied message") | PASS | 'Scenario: Admin user can access the import page' shows the happy path. 'Scenario: Member user cannot access the import feature' and 'Scenario: Viewer user cannot access the import feature' both include 'And they see a permission-denied message' in business language. |
| c12 | Output's boundary scenarios for the row limit cover exactly 1,000 rows (succeeds), 1,001 rows (fails — over limit), 0 rows (empty CSV — explicit behaviour: rejected vs accepted as no-op) | PARTIAL | 'Scenario: CSV with exactly 1,000 data rows imports successfully' and 'Scenario: CSV with more than 1,000 data rows is rejected' (1,001 rows) are both present. The 0-row (empty CSV) boundary case is absent — there is no scenario defining whether an empty CSV is rejected or treated as a no-op. |
| c13 | Output's invalid-row handling scenarios cover bad email format (invalid row collected, valid rows still processed), invalid role outside admin/member/viewer (invalid row collected), and a CSV where ALL rows are invalid (admin sees full error report, no users created) | PASS | 'Scenario: CSV with invalid email format is collected and reported' shows valid rows still processed. 'Scenario: CSV with invalid role is collected and reported' covers role values like 'superuser' and 'owner'. 'Scenario: CSV with all invalid rows shows results without importing anything' shows '0 imported, 0 skipped, 3 invalid' and 'no rows are imported'. |
| c14 | Output's duplicate handling scenarios cover an existing user (skipped, reported in summary), a duplicate within the same CSV upload (one of the duplicates skipped, behaviour explicit), and the resulting summary counts (e.g. "847 imported, 3 skipped, 2 invalid") | PASS | Rule 3 covers all three: 'Scenario: CSV with one duplicate email skips the duplicate' (existing DB duplicate), 'Scenario: CSV with duplicate emails within the same file skips extras' (within-file duplicate with explicit first-occurrence behaviour), and both scenarios show three-bucket summary counts e.g. '2 imported, 2 skipped (already exist), 0 invalid (validation errors)'. |
| c15 | Output's Given/Then steps speak in business terms — "the admin sees a summary showing 847 imported and 3 skipped" — never HTTP codes, table names, or internal API paths | PASS | No HTTP codes, table names, or internal API paths appear anywhere in the Gherkin steps. All outcomes are described in user-facing terms: 'they see a summary', 'they are redirected', 'they see a permission-denied message', 'the file is rejected', 'they see an error message'. |
| c16 | Output's non-functional criterion sets a specific time budget for importing 1,000 rows (e.g. "under 30 seconds") with the threshold tied to UX expectation (loading indicator vs background job) | PASS | The Non-Functional Criteria table entry reads: 'Import completes for 1,000-row file \| Under 30 seconds at p95 \| At this scale, a background job may become necessary if the sync time exceeds 30s; if sync stays under 30s, keeps admin in the UI without needing progress notifications.' The UX rationale (background job vs. staying in UI) is explicit. |
| c17 | Output's malformed-file scenario covers not just bad data but a corrupt file format (e.g. binary garbage uploaded as CSV, mismatched delimiter), with the expected behaviour stated | PASS | 'Scenario: CSV with binary garbage uploaded as .csv extension' — rejected with 'File could not be read as CSV. Please ensure the file is in valid CSV format.' 'Scenario: CSV with semicolon delimiters instead of comma' — rejected with 'CSV format not recognized. Please ensure the file uses comma delimiters and standard CSV format.' Both have explicit expected behaviour. |
| c18 | Output's open-questions section explicitly raises the privilege-escalation concern — what happens when an admin imports a CSV that grants the `admin` role to other users — as a question for the product owner, not silently allowed | PASS | Open Questions table row: 'Privilege escalation concern: What happens when an admin imports a CSV that grants the `admin` role to other users? Is this allowed silently, gated behind a confirmation, or rejected entirely? \| Blocks security design... \| Product Owner / Security Lead'. Framed as an open question for the product owner, not resolved silently in any rule. |
| c19 | Output's test-level mapping assigns each criterion to unit, integration, or E2E with rationale (e.g. "max 1000 rows" → integration on the parser, "permission denied" → E2E, "row validation rules" → unit on validators) | PASS | The Test Level Mapping table provides rationale for each: 'Row limit validation (under 1,000) \| Unit \| Pure logic; can test with in-memory CSV parser', 'Admin-only access (permission checks) \| Integration \| Requires auth middleware to verify role before allowing access', 'Email format validation \| Unit \| Regex or validator library; no dependencies', 'Happy path end-to-end \| E2E \| Full flow: upload → process → verify in DB'. |

### Notes

The output is a high-quality, structured acceptance criteria document that satisfies nearly all rubric requirements. The four core business rules are cleanly separated into distinct Rule blocks, each with multiple concrete scenarios written in business language, with single-outcome Thens split into And steps. The malformed-file scenarios (binary garbage and semicolon delimiter) are both present and explicit. The privilege-escalation open question is correctly flagged as a product-owner decision rather than silently resolved. The non-functional criteria tie time thresholds to UX expectations (synchronous vs. background-job flow). The only meaningful gap is the empty CSV / 0-row boundary case, which is absent from both Rule 2 and the overall edge-case coverage, causing partial scores on c5 and c12. This omission is consistent across both criteria and represents a single missing scenario rather than a systemic weakness.
