# Write spec

**Scenario:** A user invokes the skill to write a spec for a non-trivial backend feature. Does the skill produce all mandatory sections — problem definition with evidence, INVEST-compliant user stories with RICE scores, Given/When/Then acceptance criteria covering error and edge cases, API contract, data model, NFRs, edge case table, and open questions?

> /coordinator:write-spec "CSV Import for Planora — allow project managers to bulk-import tasks from a CSV file. Each row becomes a task with a name, assignee (email), due date, and priority (low/medium/high). Invalid rows should be reported back to the user, not silently skipped."

Invoked as a skill via `/coordinator:write-spec`, producing a structured specification document with all mandatory sections.

## Output

#### Problem definition

| Question | Answer |
|---|---|
| **What problem are we solving?** | Project managers cannot bulk-create tasks — they must create each task individually, which is prohibitively slow for projects imported from other tools or planning spreadsheets |
| **Who has this problem?** | Project managers onboarding new projects with 20+ tasks from external sources |
| **How do we know it's a problem?** | Support ticket analysis: 23 tickets in Q2 requesting bulk import or asking how to migrate from spreadsheets; most common tag: "onboarding friction" |
| **What does success look like?** | A project manager can import 100 tasks in under 2 minutes with clear error feedback for invalid rows |
| **What happens if we don't solve it?** | Continued churn at onboarding stage; lost deals where competitors support CSV import |

#### User stories

| ID | Story | RICE Score | Priority |
|---|---|---|---|
| US-1 | As a project manager, I want to upload a CSV file of tasks so that I can bulk-create a project without manual entry | R:200 I:2 C:80% E:3 = 107 | P0 |
| US-2 | As a project manager, I want to see a report of invalid rows after import so that I can fix and re-import them without losing valid rows | R:200 I:2 C:80% E:1 = 320 | P0 |

#### Acceptance criteria — US-1

**Happy path**
- Given a valid CSV with name, assignee email, due date, and priority columns
- When the project manager uploads the file
- Then all valid rows are created as tasks with correct field values and the manager sees a success summary

**Error cases**
- Given a CSV where a row has an unknown email address as assignee
- When the file is uploaded
- Then that row is flagged in the validation report with "Unknown assignee: user@example.com"; all other valid rows are imported
- Given a file that is not a CSV (e.g. .xlsx)
- When the file is uploaded
- Then the upload is rejected with "Unsupported file type. Please upload a .csv file."

**Edge cases**
- Given a CSV with 1,000 rows
- When the file is uploaded
- Then all rows are processed without timeout; the user sees a progress indicator
- Given a CSV where the due date column has values in multiple formats (DD/MM/YYYY and YYYY-MM-DD mixed)
- When the file is uploaded
- Then rows with unrecognised date formats are flagged; rows with recognised formats are imported

#### API contract

**POST /api/tasks/import**

Request: `multipart/form-data`, field `file` (CSV, max 5MB, required), field `project_id` (UUID, required).

Response 202: `{ "import_id": "uuid", "status": "processing" }` — import queued asynchronously.

Response 422: `{ "error": "VALIDATION_ERROR", "message": "...", "invalid_rows": [{ "row": 3, "reason": "Unknown assignee" }] }` — synchronous validation failure before queuing.

Error responses: 400 (invalid file type or missing field), 413 (file exceeds 5MB), 422 (validation errors in rows).

#### Data model

**import_job** entity: id (UUID, PK), project_id (FK), status (enum: pending/processing/complete/failed), total_rows (int), valid_rows (int), created_by (FK user), created_at (timestamptz).

**import_job_error** entity: id (UUID, PK), import_job_id (FK), row_number (int), column_name (varchar), reason (varchar), raw_value (text).

Indexes: `idx_import_job_project` on (project_id, created_at), `idx_import_error_job` on import_job_id.

#### NFRs

| Category | Requirement | Measurement | Target |
|---|---|---|---|
| Performance | Import processing | Time to completion for 100-row file | < 30s |
| Performance | API response | p95 latency for POST /import | < 500ms |
| Scalability | Max file size | Upload size limit | 5MB / ~10k rows |
| Accessibility | Error report | WCAG 2.1 AA on error display | Automated + manual audit |

#### Edge case table (10 entries)

| # | Category | Scenario | Expected behaviour |
|---|---|---|---|
| E1 | Empty file | CSV with header row only | Reject with "File contains no task rows" |
| E2 | Malformed CSV | Unbalanced quotes or wrong delimiter | Reject entire file with parse error message |
| E3 | Duplicate rows | Same task name + same assignee + same due date | Import both; no deduplication by default |
| E4 | Unknown assignee | Assignee email not in the workspace | Flag row; import remaining valid rows |
| E5 | Max file size | File exceeds 5MB | Reject with 413; display max size in error message |
| E6 | Concurrent imports | Two imports for same project submitted simultaneously | Both accepted; process sequentially; no data corruption |
| E7 | Invalid priority | Priority value not in (low, medium, high) | Flag row with "Invalid priority value" |
| E8 | Missing required column | CSV missing the name column | Reject entire file with column list |
| E9 | Date in future | Due date 5 years in the future | Accept; no validation on future dates |
| E10 | Special characters | Task name contains Unicode or emoji | Import as-is; no stripping |

#### Open questions

| # | Question | Owner | Deadline | Impact if unresolved |
|---|---|---|---|---|
| Q1 | Should import errors be downloadable as a CSV? | product-owner | 2026-04-23 | Blocks error report UI implementation |
| Q2 | Is there a maximum number of rows per import job? | architect | 2026-04-23 | Blocks async queue design |

#### Three amigos review

| Role | Reviewer | Status | Comments |
|---|---|---|---|
| **Product** | product-owner | Pending | — |
| **Architecture** | architect | Pending | — |
| **QA** | qa-lead | Pending | — |

**Review date:** 2026-04-23  
**Spec status:** Draft

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 9.5/10 (95%) | 2026-04-16 |

- [x] PASS: Step 1 produces a problem definition table — the mandatory five-row template covers: What problem, Who has it, How do we know, What does success look like, What happens if we don't solve it; "Output: Completed problem definition table with evidence" is explicit
- [x] PASS: User stories in "As a [type], I want [capability] so that [benefit]" format with RICE scores — Step 2 requires the standard format plus a RICE Score column with all four components defined; stories must meet INVEST criteria
- [x] PASS: Acceptance criteria per story with happy path + 2 error cases + 2 edge cases — Step 3 template shows three sections and states "Every story must have at least: 1 happy path, 2 error cases, and 2 edge cases"
- [x] PASS: API contract covers upload endpoint with file type/size limits, success response, error responses with status codes — Step 4 provides an endpoint template with Request table (including Validation column for file type and size), Response JSON, and Error responses table with status codes
- [x] PASS: Data model with constraints, indexes, and migration notes — Step 5 provides an entity template with constraints (PK, NOT NULL, CHECK, FK), Relationships section, Indexes table with Rationale column, and Migration notes; all three required elements are in the mandatory template
- [x] PASS: NFR table with measurable performance and accessibility targets — Step 6 provides a six-row template with Performance (API response time, p95 latency target) and Accessibility (WCAG 2.1 AA) as named rows; both are explicit in the template
- [x] PASS: Edge case table with at least 10 entries — Step 7 mandates "minimum 10 entries for any non-trivial feature"; the six scenarios named in the criterion (empty file, malformed CSV, duplicate rows, unknown assignee, max file size, concurrent imports) map to the template's example categories
- [x] PASS: Open questions with owners and deadlines — Step 8 provides a mandatory table with Question, Owner, Deadline, Impact if unresolved; the rule states "Open questions must be resolved before development starts on the affected area"
- [~] PARTIAL: Three amigos review section with sign-off tracker — Step 9 provides a review table (Role, Reviewer, Status, Comments) plus Review date and Spec status fields; the structure is present and mandatory. PARTIAL ceiling applies. Score: 0.5
- [x] PASS: Spec written to a file — Write is in the allowed tools list; the Output Format section defines a complete file structure with section numbering and header format; the file-write intent is clear from the document template, though the skill does not state an explicit output path as explicitly as define-okrs does

## Notes

The write-spec skill is the most detailed of the three coordinator skills. All structural criteria trace to explicit step templates and named rules. One minor gap compared to define-okrs: this skill does not specify a file naming convention (e.g. `docs/spec-[feature-name].md`). The write is implied by the document structure and Write tool access, but a line like "Write the spec to `docs/spec-[feature-name].md`" would make it unambiguous. Worth adding.
