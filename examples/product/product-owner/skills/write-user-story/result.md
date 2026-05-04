# Write User Story

Scenario: Testing whether the write-user-story skill definition produces stories in Gherkin format with proper acceptance criteria and ISC splitting guidance.

## Prompt

> /product-owner:write-user-story for allowing users to export their data as a CSV file from the reporting dashboard.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through each step to write comprehensive user stories for CSV export functionality.

## Step 1: Identify User Types

1. **Finance Manager reviewing monthly reports** — monthly user, needs accurate data exports for reconciliation and stakeholder presentations
2. **Data Analyst doing deeper analysis** — regular user, needs raw data to work with in Excel/Python, handles large datasets
3. **Sales Operations Coordinator** — daily user, exports filtered datasets for team meetings and CRM sync, limited technical skill
4. **First-time user discovering the export button** — occasional, needs clear guidance on what will be exported
5. **Manager with row-level permissions** — power user who can only see/export their team's data, needs to trust what's included

---

## Step 2-7: User Stories

# User Stories: CSV Data Export

## User Types
1. **Finance Manager reviewing monthly reports** — monthly user who needs accurate, traceable data exports for stakeholder reporting and reconciliation
2. **Data Analyst doing deeper analysis** — regular power user who exports raw data to Excel or Python for advanced calculations
3. **Sales Operations Coordinator** — daily user who exports filtered data for team meetings and third-party integrations
4. **First-time user discovering export** — occasional visitor who stumbles onto the feature and needs clarity on what's included
5. **Manager with row-level permissions** — power user who can only view/export their team's subset of data

---

## Basic Export

### US-1: Export visible report data as CSV

**As a** Sales Operations Coordinator exporting filtered data for a team meeting,
**I want** to click "Export to CSV" and download the current report view,
**so that** I can share the data with team members and import it into our meeting tools without manually copying rows.

**Acceptance Criteria:**

```gherkin
Scenario: Successful export of filtered report
  Given I am viewing a report with 50 rows of data
  And the report is filtered to show only "completed" status rows
  And the date range is set to "March 2026"
  When I click the "Export to CSV" button
  Then a file named "report-2026-03-completed.csv" is downloaded
  And the CSV contains exactly 50 rows (plus header)
  And all rows in the CSV match the current filter (only "completed" status)
  And the CSV date columns show values within March 2026

Scenario: Export with no filters applied
  Given I am viewing a report with all filters cleared
  And the report contains 1,500 rows total
  When I click "Export to CSV"
  Then the CSV file contains all 1,500 data rows
  And the filename includes a timestamp: "report-2026-05-04-143022.csv"

Scenario: Export empty report
  Given I am viewing a report that matches zero rows after filtering
  When I click "Export to CSV"
  Then I see a message "No data to export — your filters returned 0 rows"
  And no file is downloaded

Scenario: Column order in export matches display order
  Given the report displays columns in this order: Name, Amount, Date, Status
  When I export to CSV
  Then the CSV header row is: Name,Amount,Date,Status
  And data columns appear in that same order
```

**Edge Cases:**
- Very large exports (10,000+ rows) — tested under load, file generation doesn't time out (see scale scenario in Step 5)
- Special characters in data (quotes, commas, newlines) — properly escaped in CSV per RFC 4180
- Unicode characters in text fields — exported correctly and readable in Excel
- Empty cells — exported as blank fields, not as "null" or "N/A" strings
- Report with calculated/derived columns — exported as calculated values, not formulas

**Anti-requirements:**
- This story does NOT cover custom column selection — that is US-2
- This story does NOT include scheduled/automated exports — tracked separately in backlog
- This story does NOT cover email delivery of exports — out of scope for this release
- This story does NOT include historical snapshots — exports the current state only

**Size:** M

---

### US-2: Select which columns to include in CSV export

**As a** Data Analyst exporting for advanced analysis in Python,
**I want** to select which columns appear in the export (hide irrelevant ones),
**so that** the CSV is leaner and I don't have to clean up extra columns before analysis.

**Acceptance Criteria:**

```gherkin
Scenario: Choose columns before export
  Given I am viewing a report with 15 available columns
  And I click "Export to CSV"
  Then a column selection dialog appears
  And all 15 columns are shown with checkboxes, all checked by default
  When I uncheck "Internal ID" and "Last Modified Timestamp"
  And I click "Download CSV"
  Then the CSV is downloaded with only 13 columns
  And "Internal ID" and "Last Modified Timestamp" are not in the header row

Scenario: Deselect all columns and attempt export
  Given the column selection dialog is open
  When I uncheck all 15 columns
  And I click "Download CSV"
  Then I see an error: "Select at least one column to export"
  And no file is downloaded

Scenario: Column order in selection dialog matches report display
  Given the report displays columns in order: Name, Email, Phone, Status, Created Date
  When I open the column selection dialog
  Then the columns appear in that same order in the dialog
  And when I export with all selected, the CSV header matches that order
```

**Edge Cases:**
- User selects only one column — exported successfully as single-column CSV
- User closes dialog without selecting anything — no export initiated, current state preserved
- Large number of columns (50+) — dialog remains usable, searchable if needed (future enhancement)
- Timestamp/date columns selected — exported in the dashboard's configured timezone

**Anti-requirements:**
- This story does NOT cover reordering columns in the export — fixed to display order only
- This story does NOT save column preferences for future exports — each export is independent
- This story does NOT cover column renaming — exports use original column names

**Size:** M

---

## Handling Permissions & Scale

### US-3: Respect data permissions when exporting

**As a** Manager with row-level permissions viewing only my team's data,
**I want** the export to include only the rows I'm permitted to see,
**so that** I don't accidentally share data from other teams that I shouldn't have access to.

**Acceptance Criteria:**

```gherkin
Scenario: Export respects row-level filter
  Given I am logged in as "Team Lead: Sales East"
  And my permissions limit me to viewing only rows where region="Sales East"
  And the report shows 45 rows matching my region
  When I export to CSV
  Then the export contains exactly 45 rows (my team's data only)
  And no rows from "Sales West" or other regions appear in the CSV

Scenario: No visible columns = no export allowed
  Given I am viewing a report
  And due to my column-level permissions, I cannot see any columns
  When I click "Export to CSV"
  Then I see an error: "You do not have permission to export this report"
  And no file is downloaded

Scenario: Partial column permissions in export
  Given I have permission to see columns: Name, Email, Status, Amount
  And I do NOT have permission to see: Cost, Margin, Internal Notes
  When I export to CSV
  Then only the 4 permitted columns appear in the export
  And "Cost", "Margin", "Internal Notes" are not present
```

**Edge Cases:**
- User's permissions change between viewing and export click — export honours current permissions
- Report has inherited permissions from parent folder — export respects full permission hierarchy
- Export includes audit trail of who exported what (see anti-requirements)

**Anti-requirements:**
- This story does NOT include audit logging of exports — tracked in US-X
- This story does NOT mask sensitive data (e.g., redact PII) — permissions control access entirely
- This story does NOT email exports — out of scope

**Size:** M

---

### US-4: Handle large dataset exports without hanging

**As a** Data Analyst exporting a full year of transaction data (50,000 rows),
**I want** the export to complete without the page hanging or timing out,
**so that** I can reliably work with large datasets and don't have to stare at a spinning loader for 5 minutes.

**Acceptance Criteria:**

```gherkin
Scenario: Large export with progress indication
  Given I am exporting a report with 50,000 rows
  When I click "Download CSV"
  Then a progress dialog appears immediately showing "Generating export... 0%"
  And the progress updates every 2-3 seconds: "20%", "40%", "60%", "80%", "100%"
  And after 60 seconds or less, the download starts automatically
  And the page remains interactive (I can navigate away if I want)

Scenario: Very large export completes successfully
  Given I am exporting 100,000 rows × 20 columns
  When I click "Download CSV"
  Then the export completes within 120 seconds
  And the CSV file is readable in Excel without performance issues
  And the file size is reasonable (no bloat, efficient compression not required)

Scenario: Export timeout after excessive delay
  Given the export is still generating after 5 minutes
  When the backend hits a timeout threshold
  Then the user sees: "Export took too long. Try filtering to fewer rows."
  And the partial file is NOT downloaded (no incomplete data)
```

**Edge Cases:**
- User clicks "Download CSV" twice in rapid succession — second click is disabled/shows "Already generating"
- User closes browser tab while export is in progress — graceful cleanup on backend
- Network connection drops mid-export — user sees "Download interrupted" and can retry
- Concurrent exports by same user — handled sequentially or with clear messaging

**Anti-requirements:**
- This story does NOT implement background export jobs (email-later pattern) — real-time download only
- This story does NOT include export scheduling — manual download only
- This story does NOT implement database query optimization — use existing report performance; if reports are slow, that's a separate issue

**Size:** L

---

## First-Time Experience

### US-5: Guide first-time users through their first export

**As a** First-time user discovering the "Export to CSV" button,
**I want** to understand what happens when I click it before I do,
**so that** I'm not surprised by what's included or how the file appears.

**Acceptance Criteria:**

```gherkin
Scenario: Tooltip on export button for new users
  Given I am viewing a report for the first time
  And I have never clicked "Export to CSV" before (tracked in session)
  When I hover over the "Export to CSV" button for 1.5 seconds
  Then a tooltip appears: "Download the data you see as a CSV file. Includes all rows and columns currently visible."

Scenario: First export shows confirmation
  Given I am a first-time exporter
  When I click "Download CSV"
  Then before the download, a confirmation dialog appears:
    "Your CSV will include:
     • [Number] rows matching your filters
     • [Number] columns you've selected
     Ready to download?"
  And there are two buttons: "Download" and "Cancel"
  When I click "Download", the file downloads
  When I click "Cancel", I return to the report with no file downloaded

Scenario: Confirmation not shown to repeat exporters
  Given I have previously exported data from this report
  When I click "Export to CSV" again
  Then the download happens immediately, no confirmation dialog
  And the tooltip no longer appears on hover
```

**Edge Cases:**
- User blocks tooltips in browser — tooltip never shows, but first-export confirmation still appears
- Mobile user (touch screen) — hover tooltip not applicable; confirmation dialog is primary UX
- User clears browser storage — first-time state resets, confirmation shows again

**Anti-requirements:**
- This story does NOT include in-app tutorials or guided tours — single confirmation dialog only
- This story does NOT persist first-export state across accounts/devices — per-session only
- This story does NOT include help documentation links in the dialog — simple messaging only

**Size:** S

---

## Error Handling & Recovery

### US-6: Handle export errors gracefully with clear messaging

**As a** Finance Manager who needs the export to complete for an important meeting,
**I want** to know immediately if something went wrong and have a clear next step,
**so that** I'm not left with a blank screen wondering whether the export will arrive.

**Acceptance Criteria:**

```gherkin
Scenario: Report backend error during export
  Given I click "Export to CSV"
  When the backend encounters a database error
  Then within 3 seconds, I see: "Export failed: Unable to fetch data. Please try again."
  And a "Retry" button appears below the message
  When I click "Retry", the export is attempted again
  And if successful, the download starts

Scenario: User loses internet connection mid-export
  Given an export is in progress (progress dialog shows 45%)
  When the user's internet connection drops
  Then the progress dialog shows: "Connection lost. Trying to reconnect..."
  And if reconnected within 30 seconds, the export resumes from where it left off
  And if not reconnected, the user sees: "Download interrupted. Please try again."

Scenario: Browser disallows file download
  Given the export completes successfully on the backend
  When the browser's download is blocked by security policy
  Then the user sees: "Your browser blocked the download. Check your download settings and try again."
  And a "Help" link explains browser download settings

Scenario: Insufficient permissions during export
  Given I start an export with valid permissions
  When my permissions are revoked before the export completes
  Then the export is cancelled
  And I see: "Your access to this report has changed. Please refresh the page."
```

**Edge Cases:**
- Export succeeds but file is corrupted/unreadable — user should validate by spot-checking in Excel (no automated recovery)
- Filename conflict (file already exists in Downloads) — browser handles as usual (appends "1", "2", etc.)
- Disk full on user's machine — browser download shows "Not enough space" (system-level, not our responsibility)

**Anti-requirements:**
- This story does NOT include retry logic for network timeouts — manual retry via button only
- This story does NOT implement exponential backoff — simple retry strategy
- This story does NOT log errors to a support dashboard — error logging is infrastructure, not user-facing

**Size:** M

---

## Sizing Summary

| Story | Size | Rationale |
|-------|------|-----------|
| US-1 | M | Basic feature; two implementation paths (filtered + unfiltered export) |
| US-2 | M | Dialog + column filtering logic; moderate complexity |
| US-3 | M | Permission checks integrate with existing auth; moderate scope |
| US-4 | L | Backend streaming, progress updates, performance testing required |
| US-5 | S | Tooltip + confirmation dialog; straightforward UX |
| US-6 | M | Error handling across multiple failure modes; testing required |

All stories are in the **1-5 day range** per sizing constraints. Story 4 (large exports) may approach 5 days with performance testing included.

---

This story set is ready to hand to an engineer. Each story includes:
- Specific user context
- Concrete acceptance criteria in Gherkin
- Edge cases documented
- Clear anti-requirements (no scope creep)
- Reasonable sizing for 1-sprint delivery

Next step: prioritize within the backlog and assign 3 amigos (Product Owner + Architect + QA) for sign-off before implementation begins.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-05-04 |
| Target duration | 42739 ms |
| Target cost | $0.0572 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires Gherkin format (Given/When/Then) for acceptance criteria — not free-form bullet points | PASS | Every user story (US-1 through US-6) uses fenced Gherkin blocks with Given/When/Then/And syntax. No acceptance criteria appear as free-form bullets — e.g. US-1 has 'Scenario: Successful export of filtered report / Given I am viewing a report with 50 rows of data / And the report is filtered... / When I click the "Export to CSV" button / Then a file named...' |
| c2 | Skill requires at least one edge case or error scenario in the acceptance criteria, not just the happy path | PASS | Every story contains a dedicated 'Edge Cases' bullet list, and US-6 is entirely an error-handling story with four Gherkin scenarios covering backend errors, network drops, browser download blocks, and mid-export permission revocation. |
| c3 | Skill includes the ISC splitting test — Independent, Small, Complete — to verify stories are appropriately sized | PARTIAL | A 'Sizing Summary' table appears at the end with S/M/L ratings and rationale per story, and the closing paragraph states 'All stories are in the 1-5 day range per sizing constraints' and 'reasonable sizing for 1-sprint delivery.' Anti-requirements separate stories (Independence). Each story covers happy path + edges + errors (Completeness). However, the ISC framework is never named explicitly, and no step in the output calls out 'Independent / Small / Complete' as a structured test. |
| c4 | Skill requires the standard "As a [role], I want [action], so that [outcome]" story format | PASS | All six stories open with the three-part format, e.g. US-1: 'As a Sales Operations Coordinator exporting filtered data for a team meeting, I want to click "Export to CSV" and download the current report view, so that I can share the data with team members...' |
| c5 | Skill prohibits solution-specifying stories — acceptance criteria must describe behaviour, not implementation | PASS | No Gherkin step specifies API endpoints, HTTP status codes, database queries, or code paths. Criteria stay user-visible: 'Then a file named "report-2026-03-completed.csv" is downloaded', 'Then the CSV contains exactly 50 rows (plus header)', 'Then a progress dialog appears immediately showing "Generating export... 0%"'. |
| c6 | Skill addresses anti-requirements (things the story explicitly should NOT do) — partial credit if mentioned but not required as a mandatory section | PARTIAL | Every story contains a clearly labelled 'Anti-requirements' section with 3–4 named exclusions, e.g. US-1: 'This story does NOT cover custom column selection', 'does NOT include scheduled/automated exports', 'does NOT cover email delivery of exports', 'does NOT include historical snapshots.' The ceiling caps this at 0.5. |
| c7 | Skill specifies that stories must have a single, clear acceptance condition — not "and/or" compound criteria | PASS | Each Gherkin scenario is scoped to one behaviour. No scenario uses OR-branching or combines unrelated conditions in a single Then clause. For example, US-1 separates 'filtered export', 'no-filter export', 'empty report', and 'column order' into four distinct scenarios rather than a compound criterion. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is the chat response only — the skill definition file and its YAML frontmatter are not shown. There is no text in the output that quotes or references frontmatter fields. The invocation succeeded, but that alone does not confirm all three required fields (name, description, argument-hint) are present. |
| c9 | Output's user story uses the standard format — "As a [role e.g. report viewer], I want [to export the current dashboard view as a CSV file], so that [I can analyse the data offline / share with stakeholders who don't have access]" — with the role concrete, not "user" | PASS | Roles are specific and contextual across all stories: 'Sales Operations Coordinator exporting filtered data for a team meeting', 'Data Analyst exporting for advanced analysis in Python', 'Manager with row-level permissions', 'Finance Manager reviewing monthly reports', 'First-time user discovering the export button'. None use the generic term 'user'. |
| c10 | Output's acceptance criteria are in Gherkin format (Given / When / Then) — at least 3 scenarios — not bullet points | PASS | US-1 alone has four Gherkin scenarios. US-6 has four. Every story has a minimum of three fenced Gherkin scenarios with proper Given/When/Then/And structure. |
| c11 | Output's happy-path scenario covers the main flow — "Given I'm viewing a dashboard with data, When I click Export → CSV, Then a file downloads with the visible data, named appropriately, in valid CSV format" | PASS | US-1, Scenario 1: 'Given I am viewing a report with 50 rows of data / And the report is filtered to show only "completed" status rows / And the date range is set to "March 2026" / When I click the "Export to CSV" button / Then a file named "report-2026-03-completed.csv" is downloaded / And the CSV contains exactly 50 rows (plus header) / And all rows in the CSV match the current filter.' |
| c12 | Output includes at least one edge case — empty dashboard (export creates a CSV with headers only and an info message), very large dataset (export shows progress indicator and either streams or queues a job), unicode characters in values (escaped correctly) | PASS | US-1 'Export empty report' scenario: shows message 'No data to export — your filters returned 0 rows' and no file downloaded. US-4 has three scenarios for 50,000-row and 100,000-row exports with progress dialogs. US-1 Edge Cases bullet: 'Unicode characters in text fields — exported correctly and readable in Excel'. |
| c13 | Output includes at least one error scenario — export endpoint fails (user sees a clear error message and can retry), permissions error (user without dashboard access cannot export), network drop mid-download | PASS | US-6 covers all three named error types: 'Report backend error during export' (shows retry button), 'User loses internet connection mid-export' (progress shows reconnect message), and 'Insufficient permissions during export'. US-3 additionally has 'No visible columns = no export allowed' permission scenario. |
| c14 | Output's acceptance criteria are observable / verifiable — "Then a CSV file is downloaded" is testable; "Then the system handles it correctly" is not, and is rejected | PASS | All Then clauses are concrete and testable: 'Then a file named "report-2026-03-completed.csv" is downloaded', 'Then the CSV contains exactly 50 rows (plus header)', 'Then a progress dialog appears immediately showing "Generating export... 0%"', 'Then I see a message "No data to export — your filters returned 0 rows"'. No vague 'handled correctly' language appears. |
| c15 | Output passes the ISC test — Independent (this story doesn't depend on a parallel story in flight), Small (deliverable in a single sprint), Complete (covers happy path, edges, and errors) | PASS | Independent: anti-requirements explicitly separate stories (US-1 excludes column selection → US-2; US-3 excludes audit logging → 'US-X'). Small: sizing summary rates stories S/M/L within 'the 1-5 day range per sizing constraints.' Complete: each story has a happy-path scenario, an Edge Cases section, and error scenarios. |
| c16 | Output's acceptance criteria describe behaviour, not implementation — "Then the file contains all rows visible in the dashboard" is good; "Then the API endpoint returns a 200 with text/csv content type" is too implementation-specific for a user story | PASS | No scenario references HTTP status codes, API endpoints, database queries, or internal functions. Criteria stay at the user-observable level: 'Then the CSV contains exactly 50 rows', 'Then a progress dialog appears', 'Then a Retry button appears below the message'. US-4 anti-requirements explicitly exclude infrastructure: 'This story does NOT implement database query optimization.' |
| c17 | Output addresses what the CSV contains — exactly the data visible in the dashboard at export time, with column headers matching the displayed columns; respects active filters and sorts at export time | PASS | US-1 Scenario 1: 'And all rows in the CSV match the current filter (only "completed" status)'. US-1 'Column order in export matches display order' scenario: 'Given the report displays columns in this order: Name, Amount, Date, Status / When I export to CSV / Then the CSV header row is: Name,Amount,Date,Status / And data columns appear in that same order.' US-1 also states exported values match the current view including filters. |
| c18 | Output's anti-requirements section names what the story does NOT include — e.g. "does NOT support Excel format", "does NOT support scheduled exports", "does NOT include pivoted/aggregated data unless visible in the dashboard" | PARTIAL | Every story has a named 'Anti-requirements' section with specific exclusions. US-1: 'does NOT cover custom column selection', 'does NOT include scheduled/automated exports', 'does NOT cover email delivery of exports', 'does NOT include historical snapshots'. US-4: 'does NOT implement background export jobs', 'does NOT include export scheduling', 'does NOT implement database query optimization'. Ceiling caps this at 0.5. |

### Notes

The output is high quality and meets nearly all criteria. Gherkin is used consistently throughout all six stories; roles are concrete; anti-requirements are present and detailed in every story; happy path, edge cases, and error scenarios are all covered with observable, behaviour-level assertions. The two shortfalls: c8 (YAML frontmatter) cannot be verified from the chat response alone — the skill definition file is not surfaced in the captured output; and c3 (ISC splitting test) is only partially met because the ISC framework is not named or applied as an explicit structured test, even though the underlying concepts (independence via anti-requirements, smallness via sizing table, completeness via story structure) are all demonstrably present. The overall quality of the user stories produced is strong and the output would be immediately usable by an engineering team.
