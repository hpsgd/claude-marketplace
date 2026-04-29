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

## Output expectations

- [ ] PASS: Output's problem definition table cites evidence specific to Planora users — what the current pain is for project managers managing many tasks, why CSV import is the chosen affordance, and what the cost of inaction is
- [ ] PASS: Output's user stories follow the As-a / I-want / So-that format and have RICE scores with explicit Reach, Impact, Confidence, Effort numbers — not just a final RICE total
- [ ] PASS: Output's acceptance criteria for the import story include happy path (valid CSV, all rows imported), at least 2 error cases (file too large, invalid file format), and at least 2 edge cases (empty CSV, all rows invalid, rows with unknown assignee email, exact max-row boundary)
- [ ] PASS: Output's API contract specifies the upload endpoint with method (POST), path, content type (`multipart/form-data`), file size limit, accepted MIME types, success response shape (count imported, count skipped, errors array), and error responses with status codes
- [ ] PASS: Output's data model covers the Task entity with the fields from the prompt — name, assignee (foreign key by email lookup), due date, priority enum (low/medium/high) — plus an Import or ImportRun entity capturing import history with row counts and errors
- [ ] PASS: Output's NFR table specifies measurable targets for performance (e.g. "1,000-row CSV imports in under 10 seconds") and accessibility (e.g. WCAG 2.1 AA on the upload UI)
- [ ] PASS: Output's edge case table has at least 10 entries covering empty file, malformed CSV (mismatched delimiters), duplicate rows within the file, unknown assignee email, max file size, concurrent imports by the same user, very wide rows, BOM-prefixed UTF-8, mixed line endings, and CSV with header row vs without
- [ ] PASS: Output's open-questions section lists blocking questions with named owners and target resolution dates — e.g. "Should imports support partial commit on failure? Owner: Product. Decide by: Friday."
- [ ] PASS: Output's invalid-row reporting requirement (from the prompt) is captured concretely — the user sees which row numbers failed and why, with the valid rows still imported
- [ ] PARTIAL: Output's three amigos review section has a sign-off tracker with Product Owner, Architect, QA Lead listed and a check-box state per role
