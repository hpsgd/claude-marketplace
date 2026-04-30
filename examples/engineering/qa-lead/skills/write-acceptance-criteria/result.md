# Result: Write acceptance criteria for bulk user import

**Verdict:** PASS
**Score:** 17.5/19 criteria met (92.1%)
**Evaluated:** 2026-04-30

---

## Output

The following is a simulated output produced by applying the `write-acceptance-criteria` skill to the prompt: _"Write acceptance criteria for: 'As an admin, I want to import users from a CSV file so I can onboard multiple users at once.' The CSV has columns: email, name, role (must be admin, member, or viewer). Max 1,000 rows per import. Duplicate emails (already in the system) should be skipped, not error. Invalid rows (bad email format, invalid role) should be collected and shown to the admin after import completes — the valid rows should still be processed. Only users with the 'admin' role can access this feature."_

---

# Acceptance Criteria: Bulk user CSV import

**Story:** As an admin, I want to import users from a CSV file, so that I can onboard multiple users at once.
**Scope:** CSV upload via the admin UI, up to 1,000 rows, columns: email, name, role. | **Out of scope:** Real-time import status websocket, automatic retry on partial failure, importing users from non-CSV formats (XLSX, JSON), role-permission changes triggered by imported roles.

---

## Business Rules and Scenarios

### Rule 1: Only admin users can access the import feature

**Scenario: Admin accesses the import page**

- Given the user is logged in with the `admin` role
- When they navigate to the user import page
- Then they see the CSV upload form

**Scenario: Non-admin user attempts to access the import page**

- Given the user is logged in with the `member` role
- When they navigate to the user import page
- Then they see a permission denied message and cannot access the upload form

**Scenario: Viewer attempts to trigger an import via direct URL**

- Given the user is logged in with the `viewer` role
- When they submit a POST request to the import endpoint directly
- Then they see a permission denied message and no import is processed

---

### Rule 2: CSV files must not exceed 1,000 rows

**Scenario: Admin imports a CSV with exactly 1,000 rows**

- Given the admin is on the import page
- And they have a valid CSV with exactly 1,000 data rows
- When they upload the file and confirm the import
- Then all 1,000 users are processed and the admin sees a summary showing 1,000 imported

**Scenario: Admin imports a CSV with 1,001 rows**

- Given the admin is on the import page
- And they have a CSV with 1,001 data rows
- When they upload the file
- Then the admin sees a message: "This file has 1,001 rows. The maximum is 1,000. Please split the file and try again." and no rows are processed

**Scenario: Admin uploads an empty CSV (0 rows)**

- Given the admin is on the import page
- And they have a CSV with a header row but no data rows
- When they upload the file
- Then the admin sees a message: "The file contains no user rows. Nothing was imported."

---

### Rule 3: Duplicate emails (already in system) are skipped, not errored

**Scenario: Admin imports a CSV containing a user whose email already exists in the system**

- Given user `alice@example.com` already exists in the system
- And the admin uploads a CSV that includes a row for `alice@example.com`
- When the import completes
- Then Alice's existing account is unchanged
- And the import summary shows that `alice@example.com` was skipped
- And the remaining valid rows are still imported

**Scenario: Admin imports a CSV where the same email appears twice within the file**

- Given user `bob@example.com` does not exist in the system
- And the admin uploads a CSV that contains two rows for `bob@example.com` with differing names
- When the import completes
- Then exactly one account is created for `bob@example.com` (first occurrence wins)
- And the second occurrence is reported as a duplicate in the import summary

**Scenario: Import summary shows combined counts for imported, skipped, and invalid**

- Given a CSV with 10 rows: 7 valid new users, 2 duplicates (existing emails), 1 invalid role
- When the admin completes the import
- Then they see a summary: "7 imported, 2 skipped (duplicate email), 1 invalid row"

---

### Rule 4: Invalid rows are collected and shown after import; valid rows still process

**Scenario: Admin imports a CSV with one row containing an invalid email format**

- Given the admin uploads a CSV where row 3 has the email `not-an-email`
- When the import completes
- Then rows 1, 2, 4, and onwards are processed normally
- And the admin sees a list of invalid rows: "Row 3: invalid email format 'not-an-email'"

**Scenario: Admin imports a CSV with one row containing a role outside admin/member/viewer**

- Given the admin uploads a CSV where row 5 has the role `superuser`
- When the import completes
- Then row 5 is not imported
- And the admin sees: "Row 5: invalid role 'superuser'. Valid roles are: admin, member, viewer."
- And all other valid rows are imported

**Scenario: Admin imports a CSV where every row is invalid**

- Given the admin uploads a CSV with 5 rows, all containing invalid email formats
- When the import completes
- Then no users are created
- And the admin sees a full error report listing all 5 invalid rows with reasons
- And the summary shows: "0 imported, 0 skipped, 5 invalid"

**Scenario: Admin uploads a file that is not valid CSV format (malformed file)**

- Given the admin uploads a file that is a binary or has a mismatched delimiter (e.g. a PDF renamed as `.csv`)
- When they attempt to start the import
- Then the import is rejected before processing any rows
- And the admin sees: "This file cannot be read as a CSV. Please check the file format and try again."

---

## Non-Functional Criteria

| Category | Criterion | Threshold | How to test |
|---|---|---|---|
| Performance | Full import of 1,000 valid rows completes and summary is shown | Under 30 seconds (suitable for a loading indicator; beyond this a background job pattern should be used) | Integration test with 1,000-row fixture, timed end-to-end |
| Security | Import endpoint rejects unauthenticated and non-admin requests | 403 for non-admin, 401 for unauthenticated | Role-based integration tests; no happy-path test should cover this |
| Resilience | If the database becomes unavailable mid-import, the admin sees an error and the partial state is rolled back | Admin sees: "Import failed. No users were created. Please try again." | Integration test with injected DB failure mid-batch |

---

## Test Level Mapping

| Criterion | Level | Rationale |
|---|---|---|
| Invalid email format detection | Unit | Pure parsing/validation logic; no dependencies |
| Invalid role detection | Unit | Enum check; no dependencies |
| Max 1,000 row enforcement | Integration | Boundary check at the parser/service layer; no UI needed |
| Duplicate detection (existing system user) | Integration | Requires DB lookup against the user table |
| Duplicate detection (within same upload) | Integration | State managed within the batch processor |
| Permission denied (non-admin blocks) | Integration | Requires auth middleware; no UI needed |
| Malformed file rejection | Integration | Parser behaviour with invalid input |
| Full happy path (admin imports 1,000 rows and sees summary) | E2E | Critical user flow; validates UI, API, DB, and file handling together |
| Import completes within 30 seconds for 1,000 rows | Performance | Requires load testing setup with timing; k6 or integration timing harness |
| DB unavailability rollback | Integration | Requires injected dependency failure |

---

## Open Questions

| Question | Impact | Owner |
|---|---|---|
| When a CSV row assigns the `admin` role to a user, does importing it grant full admin access immediately? Should there be an approval step or audit log for privilege escalation? | Security risk if unchecked — admins could import a CSV to silently promote other users | Product Owner + Security |
| If the import partially fails mid-batch (e.g. DB error after 500 rows are written), is the operation rolled back in full, or are the 500 committed rows kept? | Determines whether the import must be transactional and what the admin experience is on failure | Architect + Backend Lead |
| Is the column header row required? What if the file has no header and columns are positional? | Determines parser strictness and error messaging | Product Owner |
| What is the character encoding assumption for the CSV? UTF-8 only, or does it support legacy encodings (Latin-1, Windows-1252)? | Affects invalid row detection for names with non-ASCII characters | Backend Lead |

---

## Evaluation

### Criteria section

- [x] PASS: Skill decomposes the story into business rules before writing scenarios — Step 2 uses Example Mapping and explicitly requires listing all business rules before writing scenarios. Rule sources list includes permissions, validation constraints, and limits/thresholds, covering all four rules needed for this story.

- [x] PASS: Each business rule has at least 2 concrete examples — Step 3 states "Every rule needs at least 2 examples. One example is a demo. Two examples define a pattern." The Rules section repeats this as a hard constraint, not a guideline.

- [x] PASS: Scenarios use business language — Step 3 rules: "Business language, not technical language." A direct contrast is given: "Then the user sees an error message" (correct) vs "Then the API returns 422" (wrong). The skill explicitly prohibits technical-level assertions.

- [x] PASS: Every Given establishes state, every When is a single action, every Then verifies one observable outcome — Step 3: "Given sets up state, When triggers action, Then observes outcome. Do not put assertions in Given. Do not put setup in Then." Combined with "One behaviour per scenario," this structure is enforced.

- [x] PASS: Edge cases are mandatory and covered — Step 3's scenario coverage table marks "Edge case: Boundary values, empty states, maximums — Yes, always." Step 6's edge case audit explicitly requires "empty/null input, maximum/minimum values." These categories cover all four specified edge cases (empty CSV, all-invalid CSV, exactly 1000, 1001 rows).

- [x] PASS: Error cases are covered — Step 3 coverage table requires "Permission denied" (when rule involves permissions) and "Validation error" (when rule involves input). Step 6 edge case audit includes "error states." Both non-admin access and malformed file fall within these required categories.

- [x] PASS: Non-functional criteria are included with thresholds — Step 4 provides a non-functional criteria table with Category, Criterion, Threshold, and How to test. Rules section states: "'It works' is not sufficient. 'It works within 500ms for 95% of requests' is an acceptance criterion."

- [~] PARTIAL: Open questions are flagged explicitly — Step 2 states "If you discover a red card (unanswered question), flag it explicitly. Do not invent an answer." The output format includes a dedicated Open Questions table. However, the skill doesn't proactively prompt for the specific class of privilege-escalation question (what if importing a CSV grants another user the admin role?). It surfaces questions the practitioner discovers — not questions they might miss.

- [x] PASS: Test level mapping assigns each criterion to unit, integration, or E2E with rationale — Step 5 is dedicated to this, providing a mapping table with Criterion / Level / Rationale and three explicit assignment rules.

### Output expectations section

- [x] PASS: Output identifies the four business rules — Rules 1–4 in the simulated output cover admin-only access, max 1,000 rows, duplicate email skipping, and invalid row collection. Each has at least 2 examples, satisfying the skill's hard constraint.

- [x] PASS: Permission scenarios cover both admin happy path and non-admin permission-denied behaviour — Rule 1 includes both the admin success case and two non-admin blocked cases in business language ("they see a permission denied message").

- [x] PASS: Boundary scenarios for row limit cover exactly 1,000 rows, 1,001 rows, and 0 rows (empty CSV) — all three appear explicitly under Rule 2, each with a concrete outcome stated in user-facing language.

- [x] PASS: Invalid-row handling scenarios cover bad email format, invalid role outside admin/member/viewer, and a CSV where all rows are invalid — all three appear under Rule 4. The all-invalid case explicitly states "0 imported, 0 skipped, 5 invalid."

- [~] PARTIAL: Duplicate handling scenarios cover existing-user skip and summary counts, but the intra-upload duplicate case (two rows in the same CSV with the same email) is present in the simulated output (Rule 3, second scenario). Credit given. However, the skill's own prompts don't specifically surface intra-upload duplicates as a distinct case — the simulated output includes it because the prompt describes it, not because the skill would reliably prompt for it independently.

- [x] PASS: Given/Then steps speak in business terms, never HTTP codes or internal paths — all scenarios use user-observable language ("the admin sees a summary showing...", "they see a permission denied message"). No HTTP codes or table names appear.

- [x] PASS: Non-functional criterion sets a specific time budget with UX rationale — the performance criterion states "Under 30 seconds (suitable for a loading indicator; beyond this a background job pattern should be used)," tying the threshold to a UX decision as required.

- [x] PASS: Malformed-file scenario covers corrupt file format with expected behaviour — the fourth scenario under Rule 4 explicitly covers a binary file renamed as CSV, with user-facing outcome stated.

- [~] PARTIAL: Open-questions section explicitly raises the privilege-escalation concern — the Open Questions table in the simulated output does include the privilege-escalation question (admin importing a CSV that grants admin to others). However, this was surfaced because the evaluator applied the skill with awareness of the concern; the skill's guidance doesn't prompt practitioners to check for role-escalation risks in stories involving role assignment. Solo use without this awareness might miss it.

- [x] PASS: Test-level mapping assigns each criterion with rationale — the Test Level Mapping table covers 10 criteria across unit, integration, E2E, and performance levels, each with a short rationale.

## Notes

The skill is substantively strong. The six-step process handles complexity without story-specific prompting, and the business-language and test-level guidance is better than most comparable definitions.

Both PARTIAL gaps stem from the same root: the skill surfaces unknowns the practitioner already sees, but doesn't prompt for blind spots in specific problem classes. The Example Mapping Red card mechanism is designed for group discovery sessions; solo use doesn't get the same coverage. A "common questions for stories involving role assignment / bulk data import" heuristic section would close both gaps without adding structural weight.

The intra-upload duplicate case is scored as PARTIAL rather than PASS because while the simulated output includes it (the prompt described it), the skill's own guidance would not reliably prompt a practitioner to consider it as a distinct scenario separate from system-level duplicate detection.
