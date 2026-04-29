# Test: Write acceptance criteria for bulk user import

Scenario: Developer invokes the write-acceptance-criteria skill for a story: "As an admin, I want to import users from a CSV file so that I can onboard multiple users at once." The CSV supports up to 1,000 rows with columns: email, name, role (admin/member/viewer).

## Prompt

Write acceptance criteria for: "As an admin, I want to import users from a CSV file so I can onboard multiple users at once." The CSV has columns: email, name, role (must be admin, member, or viewer). Max 1,000 rows per import. Duplicate emails (already in the system) should be skipped, not error. Invalid rows (bad email format, invalid role) should be collected and shown to the admin after import completes — the valid rows should still be processed. Only users with the 'admin' role can access this feature.

## Prompt

Write acceptance criteria for the bulk user CSV import story above.

## Criteria

- [ ] PASS: Skill decomposes the story into business rules before writing scenarios — identifies: permission rule, duplicate handling rule, invalid row rule, max row limit rule
- [ ] PASS: Each business rule has at least 2 concrete examples (not just one)
- [ ] PASS: Scenarios use business language — "Then the admin sees a summary showing 847 imported and 3 skipped" not "Then the API returns 200"
- [ ] PASS: Every Given establishes state, every When is a single action, every Then verifies one observable outcome
- [ ] PASS: Edge cases are mandatory and covered: empty CSV, CSV with all invalid rows, exactly 1000 rows (boundary), 1001 rows (over limit)
- [ ] PASS: Error cases are covered: non-admin attempting import (403 behaviour), malformed CSV file (not just bad data but bad file format)
- [ ] PASS: Non-functional criteria are included with thresholds — import of 1,000 rows should complete within a specific time budget
- [ ] PARTIAL: Open questions are flagged explicitly — e.g. what happens if an admin imports a CSV that would give another user the admin role?
- [ ] PASS: Test level mapping assigns each criterion to unit, integration, or E2E with rationale

## Output expectations

- [ ] PASS: Output identifies the four business rules from the prompt — admin-only access, max 1,000 rows per import, duplicate emails skipped (not error), invalid rows collected and shown to admin while valid rows process — each as a separate Rule block with at least 2 examples
- [ ] PASS: Output's permission scenarios cover both admin can access (happy path) and non-admin gets 403/permission-denied behaviour (in business language — "the user sees a permission denied message")
- [ ] PASS: Output's boundary scenarios for the row limit cover exactly 1,000 rows (succeeds), 1,001 rows (fails — over limit), 0 rows (empty CSV — explicit behaviour: rejected vs accepted as no-op)
- [ ] PASS: Output's invalid-row handling scenarios cover bad email format (invalid row collected, valid rows still processed), invalid role outside admin/member/viewer (invalid row collected), and a CSV where ALL rows are invalid (admin sees full error report, no users created)
- [ ] PASS: Output's duplicate handling scenarios cover an existing user (skipped, reported in summary), a duplicate within the same CSV upload (one of the duplicates skipped, behaviour explicit), and the resulting summary counts (e.g. "847 imported, 3 skipped, 2 invalid")
- [ ] PASS: Output's Given/Then steps speak in business terms — "the admin sees a summary showing 847 imported and 3 skipped" — never HTTP codes, table names, or internal API paths
- [ ] PASS: Output's non-functional criterion sets a specific time budget for importing 1,000 rows (e.g. "under 30 seconds") with the threshold tied to UX expectation (loading indicator vs background job)
- [ ] PASS: Output's malformed-file scenario covers not just bad data but a corrupt file format (e.g. binary garbage uploaded as CSV, mismatched delimiter), with the expected behaviour stated
- [ ] PASS: Output's open-questions section explicitly raises the privilege-escalation concern — what happens when an admin imports a CSV that grants the `admin` role to other users — as a question for the product owner, not silently allowed
- [ ] PASS: Output's test-level mapping assigns each criterion to unit, integration, or E2E with rationale (e.g. "max 1000 rows" → integration on the parser, "permission denied" → E2E, "row validation rules" → unit on validators)
