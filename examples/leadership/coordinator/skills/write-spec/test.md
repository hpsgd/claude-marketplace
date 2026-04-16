# Test: write-spec

Scenario: A user invokes the skill to write a spec for a non-trivial backend feature. Does the skill produce all mandatory sections — problem definition with evidence, INVEST-compliant user stories with RICE scores, Given/When/Then acceptance criteria covering error and edge cases, API contract, data model, NFRs, edge case table, and open questions?

## Prompt

/coordinator:write-spec "CSV Import for Planora — allow project managers to bulk-import tasks from a CSV file. Each row becomes a task with a name, assignee (email), due date, and priority (low/medium/high). Invalid rows should be reported back to the user, not silently skipped."

## Criteria

- [ ] PASS: Step 1 produces a problem definition table — what problem, who has it, evidence, success criteria, cost of inaction
- [ ] PASS: User stories follow the "As a [type], I want [capability] so that [benefit]" format and include RICE scores
- [ ] PASS: Each user story has acceptance criteria in Given/When/Then format covering happy path, at least 2 error cases, and at least 2 edge cases
- [ ] PASS: API contract covers the upload endpoint — request schema (file type, size limits), success response, and error responses with status codes
- [ ] PASS: Data model covers the task entity and any import/validation state — with constraints, indexes, and migration notes
- [ ] PASS: NFR table includes measurable targets for at least performance and accessibility
- [ ] PASS: Edge case table has at least 10 entries covering empty file, malformed CSV, duplicate rows, unknown assignee email, max file size, concurrent imports
- [ ] PASS: Open questions section identifies blocking questions with owners and deadlines
- [ ] PARTIAL: Three amigos review section is present with sign-off tracker
- [ ] PASS: Spec is written to a file, not only returned as conversation text
