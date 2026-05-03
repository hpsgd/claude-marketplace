# Write Spec

Scenario: A user invokes the skill to write a spec for a non-trivial backend feature. Does the skill produce all mandatory sections — problem definition with evidence, INVEST-compliant user stories with RICE scores, Given/When/Then acceptance criteria covering error and edge cases, API contract, data model, NFRs, edge case table, and open questions?

## Prompt

> /coordinator:write-spec "CSV Import for Planora — allow project managers to bulk-import tasks from a CSV file. Each row becomes a task with a name, assignee (email), due date, and priority (low/medium/high). Invalid rows should be reported back to the user, not silently skipped."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The spec is complete. Here's a summary of what was written to `docs/specs/csv-import.md`:

---

**Spec: CSV Import for Planora** covers all 9 required sections:

1. **Problem Definition** — project managers can't bulk-onboard backlogs from spreadsheets; high activation barrier
2. **User Stories** (5, RICE-scored, P0/P1) — upload CSV, row-by-row error report, template download, partial import, email-based assignee resolution
3. **Acceptance Criteria** — each story has ≥1 happy path, 2 error cases, 2 edge cases
4. **API Contract** — `GET /api/tasks/import/template` and `POST /api/projects/{id}/tasks/import` with full request/response schemas and all error codes
5. **Data Model** — `tasks` fields the import touches + `task_import_logs` audit table (flagged as an additive design choice for reviewer confirmation)
6. **Non-Functional Requirements** — performance, security (CSV injection, file validation), observability, accessibility
7. **Edge Cases** — 15 entries covering encoding, quoting, case sensitivity, formula injection, concurrency, and more
8. **Open Questions** — 6 blockers including Q4 (sync vs async), Q6 (HTTP 207 vs 200), and Q5 (pending invite handling)
9. **Three Amigos Review** — tracker in place, status Draft

### Artifacts written

#### `work/docs/specs/csv-import.md`

```
# Specification: CSV Import for Planora

**Version:** 1.0  |  **Date:** 2026-05-01  |  **Status:** Draft

---

## 1. Problem Definition

| Question | Answer |
|---|---|
| **What problem are we solving?** | Project managers cannot create tasks in bulk — they must enter each task manually one by one, which is impractical when migrating from spreadsheets or when kicking off large projects |
| **Who has this problem?** | Project managers who maintain task lists in Excel/Google Sheets and need to onboard them into Planora without re-entering every row manually |
| **How do we know it's a problem?** | CSV export is the lowest-common-denominator output format of every spreadsheet tool; any team migrating to Planora arrives with a spreadsheet. Without bulk import, the activation barrier is high and churn risk increases at the "aha moment" |
| **What does success look like?** | A project manager can import a 200-row CSV and have all valid tasks created in under 10 seconds, with a clear, line-by-line error report for any invalid rows — no manual copy-paste required |
| **What happens if we don't solve it?** | Teams with large backlogs will not complete onboarding; they will continue using the spreadsheet as their source of truth, reducing Planora's stickiness and retention |

---

## 2. User Stories

| ID | Story | RICE Score | Priority |
|---|---|---|---|
| US-1 | As a project manager, I want to upload a CSV file of tasks so that I can bulk-create my backlog without entering each task manually | R:500 I:2 C:80% E:2 = 400 | P0 |
| US-2 | As a project manager, I want to see a row-by-row error report after upload so that I know exactly which rows failed and why, and can fix them | R:500 I:2 C:80% E:1 = 800 | P0 |
| US-3 | As a project manager, I want to download a CSV template so that I know the exact column format before I upload | R:500 I:1 C:100% E:0.5 = 1000 | P0 |
| US-4 | As a project manager, I want valid rows imported even when some rows are invalid so that I don't have to fix everything before getting any value | R:500 I:2 C:80% E:0.5 = 1600 | P0 |
| US-5 | As a project manager, I want assignees resolved by email so that I can reference team members without knowing their internal user IDs | R:500 I:1 C:80% E:0.5 = 800 | P1 |

---

## 3. Acceptance Criteria

### US-1: Upload a CSV file of tasks

#### Happy path
- **Given** a project manager is authenticated and viewing a project
- **When** they upload a well-formed CSV with at least one valid row
- **Then** all valid rows are created as tasks in that project, and the response reports the count of tasks created

#### Error cases
- **Given** a project manager uploads a file that is not a CSV (e.g., `.xlsx`, `.pdf`)
- **When** the file is submitted
- **Then** the API returns HTTP 422 with code `UNSUPPORTED_FILE_TYPE` and no tasks are created

- **Given** a project manager uploads a CSV that exceeds 5 MB
- **When** the file is submitted
- **Then** the API returns HTTP 413 with code `FILE_TOO_LARGE` and no tasks are created

#### Edge cases
- **Given** a CSV with only a header row and no data rows
- **When** the file is submitted
- **Then** the API returns HTTP 422 with code `NO_DATA_ROWS` and no tasks are created

- **Given** a CSV with 1,000 rows
- **When** the file is submitted
- **Then** all valid rows are processed; the response includes both created tasks and any row-level errors

---

### US-2: Row-by-row error report

#### Happy path
- **Given** a CSV where some rows are valid and some are invalid
- **When** the import completes
- **Then** the response body includes an `errors` array where each entry identifies the 1-based row number, the failing field, and a human-readable reason

#### Error cases
- **Given** a row where the `due_date` value is not a recognisable date (e.g., `"next friday"`)
- **When** that row is processed
- **Then** `errors` contains `{ "row": N, "field": "due_date", "reason": "Invalid date format — expected YYYY-MM-DD" }`

- **Given** a row where the `priority` value is not one of `low`, `medium`, or `high`
- **When** that row is processed
- **Then** `errors` contains `{ "row": N, "field": "priority", "reason": "Invalid priority — must be low, medium, or high" }`

#### Edge cases
- **Given** a row where the `name` field is blank or whitespace-only
- **When** that row is processed
- **Then** `errors` contains `{ "row": N, "field": "name", "reason": "Task name is required" }`

- **Given** a row where the `assignee_email` does not match any user in the workspace
- **When** that row is processed
- **Then** `errors` contains `{ "row": N, "field": "assignee_email", "reason": "No workspace member found with this email" }` — the row is still skipped (not created with an unresolved assignee)

---

### US-3: Download CSV template

#### Happy path
- **Given** a project manager is authenticated
- **When** they request `GET /api/tasks/import/template`
- **Then** they receive a downloadable CSV file with the correct headers and one example row

#### Error cases
- **Given** an unauthenticated request to the template endpoint
- **When** the request is made
- **Then** the API returns HTTP 401 with no file body

- **Given** an authenticated user whose token has expired
- **When** they request the template
- **Then** the API returns HTTP 401 with `code: TOKEN_EXPIRED` so the client can prompt re-authentication

#### Edge cases
- **Given** the template is downloaded
- **When** the user opens it in Excel on Windows
- **Then** the headers and example row render correctly — UTF-8 BOM is included so Excel does not misinterpret non-ASCII characters

- **Given** the template is downloaded
- **When** the user adds a row with commas in the task name and re-uploads it
- **Then** the upload parses the quoted field correctly, confirming the template's format is round-trip safe

---

### US-4: Partial import — valid rows succeed when invalid rows exist

#### Happy path
- **Given** a CSV with 10 rows where 8 are valid and 2 are invalid
- **When** the import runs
- **Then** 8 tasks are created, 2 errors are reported, and the response body includes both `tasks` (created) and `errors` (rejected)

#### Error cases
- **Given** a CSV where every row is invalid
- **When** the import runs
- **Then** 0 tasks are created, all rows appear in `errors`, and the response status is HTTP 422 `ALL_ROWS_FAILED`

- **Given** the server loses its database connection mid-import after 5 rows have been created
- **When** the connection drops
- **Then** the 5 already-created tasks remain (rows are committed individually, not in one transaction); the response reflects what was created before the failure and surfaces a server error for the remainder

#### Edge cases
- **Given** a valid row where the `assignee_email` column is empty
- **When** that row is processed
- **Then** the task is created with no assignee (`assignee_id: null`); unassigned is a valid state

- **Given** a valid row where the `due_date` column is empty
- **When** that row is processed
- **Then** the task is created with no due date (`due_date: null`)

---

### US-5: Assignees resolved by email

#### Happy path
- **Given** a row with `assignee_email` matching a confirmed workspace member
- **When** the row is processed
- **Then** the created task has `assignee_id` set to that member's user ID

#### Error cases
- **Given** `assignee_email` is syntactically valid but the user is not in the workspace
- **When** the row is processed
- **Then** the row is rejected with `{ "field": "assignee_email", "reason": "No workspace member found with this email" }` — the task is not created with an unresolved assignee

- **Given** `assignee_email` is not a valid email format (e.g., `"bob"` or `"missing@"`)
- **When** the row is processed
- **Then** the row is rejected with `{ "field": "assignee_email", "reason": "Invalid email format" }` without attempting a workspace lookup

#### Edge cases
- **Given** `assignee_email` is provided in mixed case (`Alice@Example.COM`)
- **When** the row is processed
- **Then** the email is normalised to lowercase before lookup, so the member is found and the task is assigned correctly

- **Given** the workspace has two members whose emails differ only in case (a data-integrity anomaly)
- **When** a row references that email after normalisation
- **Then** the import rejects the row with `{ "field": "assignee_email", "reason": "Ambiguous email — multiple workspace members matched" }` rather than assigning to an arbitrary account

---

## 4. API Contract

### GET /api/tasks/import/template

**Purpose:** Download a CSV template with headers and one example row.

**Request:** No body. Requires `Authorization: Bearer <token>` header.

**Response (200):**
```
Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename="planora-tasks-template.csv"

name,assignee_email,due_date,priority
"Write onboarding guide",alice@example.com,2026-06-01,high
```

**Error responses:**
| Status | Code | When |
|---|---|---|
| 401 | UNAUTHORIZED | Missing or invalid bearer token |

---

### POST /api/projects/{project_id}/tasks/import

**Purpose:** Upload a CSV file and bulk-create tasks in the specified project.

**Request:**
- `Content-Type: multipart/form-data`
- Requires `Authorization: Bearer <token>` header

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `file` | file | Yes | `.csv` extension, `text/csv` MIME, max 5 MB | The CSV file to import |

**CSV row fields:**

| Column | Type | Required | Validation | Description |
|---|---|---|---|---|
| `name` | string | Yes | 1–255 characters, non-blank | Task name |
| `assignee_email` | string | No | Valid RFC 5322 email if provided; must match a workspace member | Assignee lookup by email |
| `due_date` | string | No | `YYYY-MM-DD` format if provided | Task due date |
| `priority` | string | No, default `medium` | `low` \| `medium` \| `high` (case-insensitive) | Task priority |

**Response (207 — partial success):**
```json
{
  "imported": 8,
  "failed": 2,
  "tasks": [
    {
      "id": "uuid",
      "name": "Write onboarding guide",
      "assignee_id": "uuid-or-null",
      "due_date": "2026-06-01",
      "priority": "high",
      "project_id": "uuid",
      "created_at": "2026-05-01T10:00:00Z"
    }
  ],
  "errors": [
    {
      "row": 3,
      "field": "due_date",
      "reason": "Invalid date format — expected YYYY-MM-DD"
    },
    {
      "row": 7,
      "field": "priority",
      "reason": "Invalid priority — must be low, medium, or high"
    }
  ]
}
```

**Response (200 — all rows succeeded):**
Same body shape with `"failed": 0` and `"errors": []`.

**Error responses:**
| Status | Code | When |
|---|---|---|
| 400 | MISSING_FILE | No `file` field in the multipart body |
| 401 | UNAUTHORIZED | Missing or invalid bearer token |
| 403 | FORBIDDEN | Authenticated user does not have write access to this project |
| 404 | PROJECT_NOT_FOUND | `project_id` does not exist or is not visible to the caller |
| 413 | FILE_TOO_LARGE | File exceeds 5 MB |
| 422 | UNSUPPORTED_FILE_TYPE | File is not a CSV |
| 422 | NO_DATA_ROWS | CSV has a header but no data rows |
| 422 | INVALID_HEADERS | CSV is missing required column `name`, or has unrecognised columns that suggest a wrong file |
| 422 | ALL_ROWS_FAILED | Every row failed validation; no tasks created |

---

## 5. Data Model

No new tables are required — the import endpoint creates rows in the existing `tasks` table. The data model below documents the fields the import touches.

### tasks (existing table — fields used by import)

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK, generated | Primary identifier |
| `project_id` | UUID | NOT NULL, FK → projects.id | Project this task belongs to |
| `name` | varchar(255) | NOT NULL | Task name — sourced from CSV `name` column |
| `assignee_id` | UUID | NULLABLE, FK → users.id | Resolved from `assignee_email`; NULL if column is blank |
| `due_date` | date | NULLABLE | Sourced from CSV `due_date` column |
| `priority` | enum | NOT NULL, DEFAULT 'medium', CHECK IN ('low','medium','high') | Sourced from CSV `priority` column |
| `created_at` | timestamptz | NOT NULL, DEFAULT now() | Set at import time |

### task_import_logs (new table — audit trail, additive design choice)

> **Design note:** This table is not strictly required by the user stories, but provides an audit trail for support and compliance. The three amigos review should confirm whether this is in scope for v1 or deferred.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK, generated | Primary identifier |
| `project_id` | UUID | NOT NULL, FK → projects.id | Project targeted by this import |
| `imported_by` | UUID | NOT NULL, FK → users.id | User who triggered the import |
| `filename` | varchar(255) | NOT NULL | Original filename as uploaded |
| `row_count` | integer | NOT NULL | Total rows in the CSV (excluding header) |
| `imported_count` | integer | NOT NULL | Rows successfully created as tasks |
| `failed_count` | integer | NOT NULL | Rows rejected due to validation errors |
| `error_detail` | jsonb | NULLABLE | Full `errors` array for audit/support |
| `created_at` | timestamptz | NOT NULL, DEFAULT now() | When the import ran |

#### Indexes
| Index | Columns | Type | Rationale |
|---|---|---|---|
| `idx_task_import_logs_project` | `project_id, created_at DESC` | btree | Look up import history for a project |
| `idx_task_import_logs_user` | `imported_by, created_at DESC` | btree | Look up what a user has imported |

#### Migration notes
- `task_import_logs` is a new table — additive migration, no backfill required.
- `tasks` table is assumed to already exist; this spec does not alter its schema. If `priority` is not yet an enum column, that migration must be sequenced before this feature ships.

---

## 6. Non-Functional Requirements

| Category | Requirement | Measurement | Target |
|---|---|---|---|
| **Performance** | Import processing time | Wall-clock time for 200-row CSV | < 5 seconds end-to-end |
| **Performance** | Template download latency | p95 response time | < 100 ms |
| **Scalability** | Maximum rows per import | Validated at parse time | 1,000 rows (configurable via env var `CSV_IMPORT_MAX_ROWS`) |
| **Scalability** | Concurrent imports | Load test | System remains stable under 20 simultaneous imports |
| **Security** | Authentication | Bearer token, validated on every request | All endpoints require auth |
| **Security** | Authorisation | Project-level write permission check | User must have write access to the target project |
| **Security** | File validation | MIME type + extension check; content scanned for CSV structure | Reject non-CSV files before parsing |
| **Security** | File size limit | Enforced before parsing begins | 5 MB hard limit |
| **Security** | CSV injection | Sanitise cell values starting with `=`, `+`, `-`, `@` | Strip or escape leading special characters to prevent formula injection |
| **Reliability** | Import atomicity per row | Row-level transaction | A failed row does not roll back successful rows |
| **Reliability** | Import atomicity overall | If the server crashes mid-import, the `task_import_logs` entry records partial state | Partial imports are visible in audit log |
| **Observability** | Structured logging | Log per-import: `project_id`, `imported_by`, `row_count`, `imported_count`, `failed_count`, duration | Every import is logged |
| **Observability** | Metrics | Counter: `csv_import.rows.created`, `csv_import.rows.failed` | Emitted per import |
| **Accessibility** | File upload UI | WCAG 2.1 AA | Upload control is keyboard-accessible and screen-reader labelled |

---

## 7. Edge Cases

| # | Category | Scenario | Expected Behaviour |
|---|---|---|---|
| E1 | Empty state | CSV has only a header row, no data | HTTP 422 `NO_DATA_ROWS` |
| E2 | Encoding | CSV is UTF-16 or Windows-1252 encoded | Attempt to decode as UTF-8; if it fails, return HTTP 422 `ENCODING_ERROR` with guidance to save as UTF-8 |
| E3 | Line endings | CSV uses Windows `\r\n` line endings | Parse correctly — `\r\n` and `\n` both accepted |
| E4 | Quoted fields | A task name contains a comma: `"Build thing, fast"` | Parsed correctly per RFC 4180 quoting rules |
| E5 | Trailing newline | CSV file ends with a blank line | Blank final line is ignored, not treated as an invalid row |
| E6 | Extra columns | CSV contains columns beyond the four specified (e.g., `tags`, `notes`) | Extra columns are silently ignored; only `name`, `assignee_email`, `due_date`, `priority` are read |
| E7 | Missing optional columns | CSV has only `name` and `priority` columns, no `assignee_email` or `due_date` | Valid — missing optional columns default to NULL |
| E8 | Case sensitivity | `priority` value is `"High"` or `"HIGH"` | Normalised to lowercase before validation; `"High"` → `"high"` is valid |
| E9 | Date edge case | `due_date` is in the past (e.g., yesterday) | Allowed — no restriction on past due dates at import time |
| E10 | Duplicate name | Two rows have identical `name` values | Both tasks are created; Planora does not enforce unique task names within a project |
| E11 | Very long name | `name` exceeds 255 characters | Row rejected: `{ "field": "name", "reason": "Task name must be 255 characters or fewer" }` |
| E12 | Max rows exceeded | CSV has 1,001 rows when limit is 1,000 | HTTP 422 `ROW_LIMIT_EXCEEDED` before any rows are processed |
| E13 | Formula injection | A cell value starts with `=SUM(...)` | Leading `=` is stripped or the value is prefixed with a `'` apostrophe before storage |
| E14 | Concurrent import | Same user submits two imports to the same project simultaneously | Both are processed independently; no row-level locking conflict since rows are inserts |
| E15 | Email case | `assignee_email` is `Alice@Example.COM` | Normalised to lowercase before workspace member lookup |

---

## 8. Open Questions & Out of Scope

### Open Questions (BLOCKS development)

| # | Question | Owner | Deadline | Impact if unresolved |
|---|---|---|---|---|
| Q1 | What is Planora's existing auth mechanism (JWT, session cookie, API key)? The spec assumes Bearer JWT — if different, the `Authorization` header format changes | Engineering lead | Before API development starts | Blocks endpoint authentication implementation |
| Q2 | Does the `tasks` table already exist with the columns specified, or is this a greenfield build where the full schema is TBD? | Engineering lead | Before migration is written | Blocks migration planning |
| Q3 | What is the maximum file size limit acceptable to the infrastructure (load balancer, API gateway)? 5 MB is proposed but may need tuning | DevOps / Engineering | Before going to staging | Blocks NFR for file size |
| Q4 | Should the import be synchronous (respond when done) or asynchronous (return a job ID, poll for results)? For ≤1,000 rows the synchronous approach is viable; if the row limit is raised later, async becomes necessary | Product / Engineering | Before API design is finalised | Blocks API contract (sync vs async changes the response shape significantly) |
| Q5 | Are there workspace member invitation states to consider? (e.g., invited-but-not-accepted) Should pending-invite emails resolve to an assignee or be rejected? | Product | Before US-5 development | Blocks assignee resolution logic |
| Q6 | HTTP 207 (Multi-Status) is used for partial success, but it originates from WebDAV and is non-standard for REST JSON APIs. Some teams prefer HTTP 200 with a body that signals partial outcomes. Should we use 207 or 200 here? | Engineering lead | Before API design is finalised | Affects client-side response handling |

### Out of Scope

| Item | Reason | Future consideration? |
|---|---|---|
| Updating existing tasks via CSV | Import creates only new tasks; update-by-import requires matching logic (by ID or name) which adds significant complexity | Yes — v2 |
| Deleting tasks via CSV | Destructive bulk operations require a separate safety review | Yes — v2, with confirmation step |
| Importing other entity types (projects, milestones) | Scope limited to tasks for this iteration | Yes — future |
| Async import with progress bar | Synchronous import is sufficient for ≤1,000 rows at current scale | Yes — when row limit is raised |
| Duplicate detection / deduplication | Planora allows multiple tasks with the same name; deduplication logic is out of scope | Revisit if users report accidental double-imports |
| CSV export of tasks | Separate feature; not part of this spec | Yes — companion feature |
| Import from Google Sheets or Notion directly | Only CSV upload is in scope; direct third-party integrations are a separate initiative | Yes — future integrations workstream |

---

## 9. Review Status

### Three Amigos Review

| Role | Reviewer | Status | Comments |
|---|---|---|---|
| **Product** | [Project Manager / Product Owner] | Pending | — |
| **Architecture** | [Engineering Lead] | Pending | Q1–Q4 above must be resolved before review can be completed |
| **QA** | [QA Lead] | Pending | — |

**Review date:** TBD  
**Spec status:** Draft — awaiting three amigos sign-off and resolution of open questions Q1–Q5

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.0/19.0 (95%) |
| Evaluated | 2026-05-01 |
| Target duration | 252671 ms |
| Target cost | $0.6573 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 produces a problem definition table — what problem, who has it, evidence, success criteria, cost of inaction | PASS | Section 1 table has five explicit rows: 'What problem' (manual entry impractical), 'Who has it' (PMs migrating from spreadsheets), evidence ('CSV is lowest-common-denominator output format'), success ('200-row CSV in under 10 seconds'), cost of inaction ('Teams with large backlogs will not complete onboarding'). |
| c2 | User stories follow the "As a [type], I want [capability] so that [benefit]" format and include RICE scores | PASS | All 5 stories in Section 2 use the exact format, e.g., 'As a project manager, I want to upload a CSV file of tasks so that I can bulk-create my backlog without entering each task manually'. Every row includes a RICE score formatted as 'R:500 I:2 C:80% E:2 = 400'. |
| c3 | Each user story has acceptance criteria in Given/When/Then format covering happy path, at least 2 error cases, and at least 2 edge cases | PASS | Section 3 provides ACs for all 5 stories. Each has one happy path block, an 'Error cases' subsection with ≥2 GWT scenarios, and an 'Edge cases' subsection with ≥2 GWT scenarios. For example, US-1: error cases are UNSUPPORTED_FILE_TYPE (422) and FILE_TOO_LARGE (413); edge cases are header-only CSV and 1,000-row CSV. |
| c4 | API contract covers the upload endpoint — request schema (file type, size limits), success response, and error responses with status codes | PASS | Section 4 'POST /api/projects/{project_id}/tasks/import' documents Content-Type multipart/form-data, .csv extension + text/csv MIME, 5 MB hard limit. Success response shows 207 body with `imported`, `failed`, `tasks`, and `errors` fields. Error table covers 400 through 422 with 9 distinct error codes. |
| c5 | Data model covers the task entity and any import/validation state — with constraints, indexes, and migration notes | PASS | Section 5 documents `tasks` (existing, with PK/FK constraints, enum for priority, nullable fields) and `task_import_logs` (new, with full field list, two btree indexes, and migration notes stating 'additive migration, no backfill required' and sequencing caveat for the priority enum). |
| c6 | NFR table includes measurable targets for at least performance and accessibility | PASS | Section 6 performance rows: '< 5 seconds end-to-end' for 200-row CSV and '< 100 ms' p95 for template download. Accessibility row: 'WCAG 2.1 AA — Upload control is keyboard-accessible and screen-reader labelled'. |
| c7 | Edge case table has at least 10 entries covering empty file, malformed CSV, duplicate rows, unknown assignee email, max file size, concurrent imports | PASS | Section 7 has 15 entries (E1–E15). Covered: empty file (E1), malformed/quoted CSV (E2 encoding, E4 quoting), duplicate name (E10), concurrent import (E14). Note: unknown assignee email appears in ACs rather than this table, and max file size is in NFR/error responses rather than as a dedicated edge case row; but the count of 15 and overall coverage clear the ≥10 threshold. |
| c8 | Open questions section identifies blocking questions with owners and deadlines | PASS | Section 8 lists 6 open questions (Q1–Q6) in a table with 'Owner' and 'Deadline' columns. Examples: Q1 Owner 'Engineering lead', Deadline 'Before API development starts'; Q5 Owner 'Product', Deadline 'Before US-5 development'; Q4 Owner 'Product / Engineering', Deadline 'Before API design is finalised'. |
| c9 | Three amigos review section is present with sign-off tracker | PARTIAL | Section 9 'Three Amigos Review' table lists Product (Project Manager/Product Owner), Architecture (Engineering Lead), and QA (QA Lead) rows, all with Status 'Pending'. Sign-off tracker structure is present; ceiling is PARTIAL. |
| c10 | Spec is written to a file, not only returned as conversation text | PASS | Artifact `work/docs/specs/csv-import.md` is present as a written file containing the full spec, confirmed by the ARTIFACTS WRITTEN section. |
| c11 | Output's problem definition table cites evidence specific to Planora users — what the current pain is for project managers managing many tasks, why CSV import is the chosen affordance, and what the cost of inaction is | PASS | Pain: 'must enter each task manually one by one, which is impractical when migrating from spreadsheets or when kicking off large projects'. Why CSV: 'CSV export is the lowest-common-denominator output format of every spreadsheet tool; any team migrating to Planora arrives with a spreadsheet'. Cost of inaction: 'Teams with large backlogs will not complete onboarding... reducing Planora's stickiness and retention'. |
| c12 | Output's user stories follow the As-a / I-want / So-that format and have RICE scores with explicit Reach, Impact, Confidence, Effort numbers — not just a final RICE total | PASS | Section 2 RICE column shows all four components labeled individually, e.g., 'R:500 I:2 C:80% E:2 = 400' and 'R:500 I:1 C:100% E:0.5 = 1000'. All five stories expose individual R, I, C, E values, not just the total. |
| c13 | Output's acceptance criteria for the import story include happy path (valid CSV, all rows imported), at least 2 error cases (file too large, invalid file format), and at least 2 edge cases (empty CSV, all rows invalid, rows with unknown assignee email, exact max-row boundary) | PASS | US-1 happy path: 'well-formed CSV... all valid rows are created'. US-1 error cases: HTTP 413 FILE_TOO_LARGE and HTTP 422 UNSUPPORTED_FILE_TYPE. US-1 edge cases: header-only CSV (NO_DATA_ROWS) and 1,000-row CSV. US-4 error case covers ALL_ROWS_FAILED (HTTP 422). E12 covers ROW_LIMIT_EXCEEDED. |
| c14 | Output's API contract specifies the upload endpoint with method (POST), path, content type (`multipart/form-data`), file size limit, accepted MIME types, success response shape (count imported, count skipped, errors array), and error responses with status codes | PASS | Section 4: method POST, path `/api/projects/{project_id}/tasks/import`, Content-Type multipart/form-data, max 5 MB, `.csv` + `text/csv` MIME. 207 response body: `imported` (count), `failed` (count), `tasks` array, `errors` array. Error table: 9 status/code pairs from 400 to 422. |
| c15 | Output's data model covers the Task entity with the fields from the prompt — name, assignee (foreign key by email lookup), due date, priority enum (low/medium/high) — plus an Import or ImportRun entity capturing import history with row counts and errors | PASS | Section 5 tasks table: name varchar(255) NOT NULL, assignee_id UUID NULLABLE FK resolved from assignee_email, due_date date NULLABLE, priority enum CHECK IN ('low','medium','high'). task_import_logs table: row_count, imported_count, failed_count, error_detail jsonb for full errors array. |
| c16 | Output's NFR table specifies measurable targets for performance (e.g. "1,000-row CSV imports in under 10 seconds") and accessibility (e.g. WCAG 2.1 AA on the upload UI) | PASS | Section 6 Performance row: '< 5 seconds end-to-end' for 200-row CSV (measurable, with method 'Wall-clock time'). Accessibility row: 'WCAG 2.1 AA — Upload control is keyboard-accessible and screen-reader labelled' with measurement criterion stated. |
| c17 | Output's edge case table has at least 10 entries covering empty file, malformed CSV (mismatched delimiters), duplicate rows within the file, unknown assignee email, max file size, concurrent imports by the same user, very wide rows, BOM-prefixed UTF-8, mixed line endings, and CSV with header row vs without | PARTIAL | Table has 15 entries. Covered: empty file (E1), duplicate rows (E10), concurrent imports (E14), mixed line endings (E3). Not covered as edge case table rows: malformed CSV with mismatched delimiters (E4 handles RFC4180 quoting but not delimiter mismatch), unknown assignee email (in ACs, not table), max file size (in NFR, not table), very wide rows (absent), BOM-prefixed UTF-8 (mentioned in US-3 ACs, not table), CSV without header row (absent — E1 is header-only, not headerless). |
| c18 | Output's open-questions section lists blocking questions with named owners and target resolution dates — e.g. "Should imports support partial commit on failure? Owner: Product. Decide by: Friday." | PARTIAL | Section 8 has an Owner column (role-based: 'Engineering lead', 'Product') consistent with the criterion's own example format. However, the Deadline column uses milestone references ('Before API development starts', 'Before migration is written') rather than specific calendar dates. The criterion example 'Decide by: Friday' implies an actionable calendar date; milestone-relative deadlines cannot be placed on a calendar and reduce accountability. |
| c19 | Output's invalid-row reporting requirement (from the prompt) is captured concretely — the user sees which row numbers failed and why, with the valid rows still imported | PASS | US-2 explicitly models row-by-row error reporting. API response shows `errors` array with `{ "row": N, "field": "...", "reason": "..." }` schema. US-4 + Section 4 confirm partial import: valid rows are committed, failed rows appear in errors. Error response example shows `"row": 3` and `"row": 7` with specific field and reason. |
| c20 | Output's three amigos review section has a sign-off tracker with Product Owner, Architect, QA Lead listed and a check-box state per role | PARTIAL | Section 9 table lists Product (Project Manager/Product Owner), Architecture (Engineering Lead), QA (QA Lead) with a Status column showing 'Pending' for all three. Status is text ('Pending') rather than checkboxes, but the sign-off tracker structure with all three roles is present. Ceiling is PARTIAL. |

### Notes

The spec is comprehensive and well-structured, earning PASS on 16 of 20 criteria. The two partial scores on non-capped criteria (c17 and c18) reflect specific gaps: the edge case table omits mismatched delimiter handling, unknown-assignee-email as a dedicated row, max file size as an edge case entry, very wide rows, BOM-prefixed UTF-8, and the headerless CSV scenario; and open-question deadlines are milestone-relative rather than calendar-dated. The two PARTIAL-capped criteria (c9, c20) are both satisfied at their ceiling. The spec's strongest areas are the API contract (method, path, content-type, file/MIME limits, 207 partial-success shape, 9 error codes), the data model (tasks + task_import_logs with indexes and migration sequencing notes), and the acceptance criteria structure (every story has the required happy/error/edge breakdown in GWT form).
