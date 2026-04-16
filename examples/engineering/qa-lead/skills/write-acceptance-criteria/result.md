# Write acceptance criteria for bulk user import

Developer invokes the write-acceptance-criteria skill for a story: "As an admin, I want to import users from a CSV file so that I can onboard multiple users at once." The CSV supports up to 1,000 rows with columns: email, name, role (admin/member/viewer).

## Prompt

> Write acceptance criteria for: "As an admin, I want to import users from a CSV file so I can onboard multiple users at once." The CSV has columns: email, name, role (must be admin, member, or viewer). Max 1,000 rows per import. Duplicate emails (already in the system) should be skipped, not error. Invalid rows (bad email format, invalid role) should be collected and shown to the admin after import completes — the valid rows should still be processed. Only users with the 'admin' role can access this feature.
>
>
> Write acceptance criteria for the bulk user CSV import story above.

## Output

**Step 1 — Story decomposition:**

Actor: admin user (role = 'admin'). Goal: onboard multiple users without manual entry. Value: reduces onboarding time for organisations adding teams. Out of scope: bulk edit, bulk delete, export, user management after import.

**Step 2 — Business rules via Example Mapping:**

- Rule 1: Only users with the 'admin' role may access the CSV import feature
- Rule 2: Duplicate emails (already registered in the system) are skipped silently and counted in the post-import summary
- Rule 3: Rows with invalid email format or invalid role value are collected and displayed to the admin after import; valid rows still process
- Rule 4: Maximum 1,000 rows per import file; files exceeding this limit are rejected before processing begins

**Step 3 — Scenarios per rule (each rule has ≥2 examples):**

**Rule 1: Permission**

Scenario: admin imports successfully
- Given I am logged in as a user with the 'admin' role
- When I upload a valid CSV file
- Then the import begins and I see a progress indicator

Scenario: non-admin cannot access import
- Given I am logged in as a user with the 'member' role
- When I navigate to the user import page
- Then I see an access denied message and the import form is not shown

**Rule 2: Duplicate handling**

Scenario: CSV with one duplicate
- Given user 'alice@example.com' already exists in the system
- And I upload a CSV containing 'alice@example.com' and 9 new users
- When the import completes
- Then the summary shows: 9 users imported, 1 skipped (duplicate)

Scenario: CSV with majority duplicates
- Given 80 of 100 CSV rows contain emails already registered
- When the import completes
- Then the summary shows: 20 users imported, 80 skipped (duplicates)

**Rule 3: Invalid row handling**

Scenario: rows with invalid email
- Given a CSV containing 97 valid rows and 3 rows with malformed email addresses
- When the import completes
- Then the summary shows: 97 users imported, 3 errors — and the 3 invalid rows are listed with the specific validation error

Scenario: rows with invalid role value
- Given a CSV containing a row with role value 'superuser' (not in admin/member/viewer)
- When the import completes
- Then that row is listed as an error ("invalid role: superuser") and all other valid rows are imported

**Rule 4: Row limit**

Scenario: exactly 1,000 rows (boundary — accepted)
- Given a CSV containing exactly 1,000 data rows
- When I upload it
- Then the import is accepted and all valid rows are processed

Scenario: 1,001 rows (over limit — rejected)
- Given a CSV containing 1,001 data rows
- When I upload it
- Then I see an error: "File exceeds maximum of 1,000 rows. No users were imported."

**Edge cases:**

Empty CSV (0 rows): upload a CSV with headers but no data rows → "No users to import" message, no changes made.

All-invalid CSV: upload a CSV where every row has an invalid role → import completes, 0 users imported, all rows listed as errors.

**Error cases:**

Malformed file: upload a `.csv` file that is not valid CSV (binary, truncated, encoding error) → "File could not be parsed. Please check the file format and try again." Zero rows imported.

**Non-functional:**

Performance: import of 1,000 rows completes and summary is displayed within 30 seconds on standard hardware.

**Open questions flagged:**

| Question | Impact | Owner |
|---|---|---|
| What happens if a CSV row assigns the 'admin' role to a new user — does the importing admin need additional permissions to grant admin? | Blocks Rule 3 edge case testing and Rule 1 boundary | Product Owner |
| Should duplicate email matching be case-sensitive? | Affects Rule 2 behaviour | Product Owner |

**Test level mapping:**

| Criterion | Level | Rationale |
|---|---|---|
| Permission check (admin only) | Integration | Requires auth middleware |
| Duplicate email detection | Integration | Requires database lookup |
| Invalid row collection | Unit | Pure validation logic, no dependencies |
| Row limit check | Unit | Count check, no dependencies |
| Full import flow | E2E | Critical user journey |
| Performance (30s for 1,000 rows) | Performance | Requires load testing tool |

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Skill decomposes into business rules before writing scenarios — write-acceptance-criteria SKILL.md Step 2 uses Example Mapping and explicitly requires listing every business rule (permissions, validation, state transitions, limits) before writing scenarios. All four rules (permission, duplicate, invalid row, max limit) map to categories in the skill's rule sources list.
- [x] PASS: Each business rule has ≥2 concrete examples — write-acceptance-criteria SKILL.md Step 3: "Every rule needs at least 2 examples. One example is a demo. Two examples define a pattern." This is an explicit rule, not a guideline.
- [x] PASS: Scenarios use business language — write-acceptance-criteria SKILL.md Step 3 rules: "Business language, not technical language. Acceptance criteria are a contract with product, not a test script for QA." The skill explicitly prohibits "Then the API returns 422."
- [x] PASS: Given=state, When=single action, Then=single outcome — write-acceptance-criteria SKILL.md Step 3: "Given sets up state, When triggers action, Then observes outcome. Do not put assertions in Given. Do not put setup in Then." And: "One behaviour per scenario."
- [x] PASS: Edge cases mandatory and all four covered — write-acceptance-criteria SKILL.md Step 3 scenario coverage table: "Edge case: Boundary values, empty states, maximums — Yes, always." Step 6 edge case audit requires "empty/null input, maximum/minimum values." The skill mandates these categories, supporting all four specified edge cases.
- [x] PASS: Error cases covered including malformed CSV file — write-acceptance-criteria SKILL.md Step 3: "Error case: Invalid input is rejected correctly — Yes, if the rule involves input." Step 6 edge case audit requires "error states." A malformed file (not parseable) is an error state requiring explicit coverage.
- [x] PASS: Non-functional criteria with specific thresholds — write-acceptance-criteria SKILL.md Step 4 provides a non-functional criteria table with Performance as a category requiring a threshold and how to test it. The rule states: "Non-functional criteria are acceptance criteria too. 'It works' is not sufficient."
- [~] PARTIAL: Open questions flagged explicitly — write-acceptance-criteria SKILL.md Step 2: "If you discover a red card (unanswered question), flag it explicitly. Do not invent an answer. Unresolved questions block development." The output format includes an Open Questions table with Question / Impact / Owner columns. This is explicitly required by the definition.
- [x] PASS: Test level mapping with rationale — write-acceptance-criteria SKILL.md Step 5 requires a mapping table with Criterion / Test level / Rationale, with the rule: "Default to the lowest sufficient level. Unit over integration over E2E."

### Notes

The open questions criterion (8) has explicit and strong support in the definition — "red cards" are required outputs of the Example Mapping process and the output format has a dedicated Open Questions table. The PARTIAL ceiling is the test author's design choice, not a quality gap in the definition. The test level mapping criterion (9) is particularly well-supported: Step 5 provides an explicit table format and rules about choosing the lowest sufficient level.
