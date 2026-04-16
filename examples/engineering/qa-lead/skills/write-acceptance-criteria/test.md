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
