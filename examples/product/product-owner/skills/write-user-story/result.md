# Write User Story

Scenario: Testing whether the write-user-story skill definition produces stories in Gherkin format with proper acceptance criteria and ISC splitting guidance.

## Prompt

> /product-owner:write-user-story for allowing users to export their data as a CSV file from the reporting dashboard.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Written to `docs/stories-csv-export.md`. Here's what was produced:

**5 stories across the CSV export feature:**

| # | Title | Size |
|---|-------|------|
| US-1 | Export current dashboard view as CSV | M |
| US-2 | Export with active filters applied | M |
| US-3 | Select columns before exporting | M |
| US-4 | Async background export for large datasets | L |
| US-5 | Re-download previously generated exports | M |

**4 user types identified:** analyst, team manager, compliance officer, operations lead — each with distinct goals and interaction frequency.

Key decisions worth flagging:
- The async threshold (10,000 rows) is deliberately noted as server-side configurable, not hardcoded
- Download links require authentication — no public S3 URLs
- Export history is user-scoped with ownership checks on all download endpoints
- Column order follows dashboard display order, not selection order

### Artifacts written

#### `work/docs/stories-csv-export.md`

```
# User Stories: CSV Export from Reporting Dashboard

## User Types

1. **Analyst running weekly performance reviews** — pulls dashboard data into Excel/Google Sheets for offline analysis and custom charting; daily power user; high technical sophistication.
2. **Team manager distributing reports to stakeholders** — shares data summaries with colleagues who lack dashboard access; weekly user; moderate technical sophistication.
3. **Compliance officer auditing historical activity** — needs exportable records for regulatory review or internal audit; infrequent user (monthly); expects exact, complete data.
4. **Operations lead working with a scoped date range and applied filters** — applies dimension filters (e.g. region, product line, status) before exporting to avoid post-processing in spreadsheets; daily power user; high technical sophistication.

---

## CSV Export

### US-1: Export current dashboard view as a CSV file

**As an** analyst running weekly performance reviews,
**I want** to download the data currently displayed in the reporting dashboard as a CSV file,
**so that** I can analyse and chart it offline without manually copying rows.

**Acceptance Criteria:**

```gherkin
Scenario: Successful CSV download of current view
  Given I am authenticated and on the reporting dashboard
  And the report contains at least one row of data
  When I click "Export CSV"
  Then a CSV file is downloaded to my browser
  And the filename follows the pattern "report-YYYY-MM-DD.csv"
  And the first row contains the column headers matching those visible in the dashboard
  And every row visible in the current view is present in the file
  And no rows outside the current view are included

Scenario: Export preserves all visible columns and their order
  Given I am on the reporting dashboard showing columns "Date", "Region", "Revenue", "Units"
  When I click "Export CSV"
  Then the CSV headers are "Date,Region,Revenue,Units" in that order

Scenario: Export with no data in current view
  Given I am on the reporting dashboard
  And the report returns zero rows (e.g. filtered to a future date range with no data)
  When I click "Export CSV"
  Then a CSV file is downloaded containing only the header row
  And a toast notification reads "Export complete — no data rows matched your current view"

Scenario: Export button unavailable when report has not yet loaded
  Given I am on the reporting dashboard
  And the report data is still loading
  Then the "Export CSV" button is disabled
  And a tooltip reads "Waiting for report to load"
```

**Edge Cases:**
- Column values containing commas or double-quotes must be properly escaped per RFC 4180 (values wrapped in double-quotes, internal quotes doubled).
- Numeric values must not include locale-specific formatting (no thousands separators, no currency symbols) so spreadsheet tools parse them as numbers.
- Date values must be exported in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ) to avoid regional ambiguity.
- If the dashboard is in a loading/error state, the export button must remain disabled until the report resolves.

**Anti-requirements:**
- This story does NOT cover exporting with a custom column selection — tracked in US-3.
- This story does NOT cover large datasets requiring async generation — tracked in US-4.
- This story does NOT cover scheduled or recurring exports — out of scope entirely for this initiative.
- This story does NOT cover export formats other than CSV (Excel, PDF, JSON) — out of scope entirely.

**Size:** M

---

### US-2: Export dashboard data with active filters applied

**As an** operations lead working with a scoped date range and applied filters,
**I want** to export only the rows that match my current filter selections,
**so that** I receive a file scoped to exactly the segment I am analysing without post-processing in my spreadsheet.

**Acceptance Criteria:**

```gherkin
Scenario: Export respects active date range filter
  Given I am on the reporting dashboard
  And I have set the date range filter to "2026-04-01" through "2026-04-30"
  And the report displays 47 rows for that range
  When I click "Export CSV"
  Then the downloaded CSV contains exactly 47 data rows
  And every row has a date value between "2026-04-01" and "2026-04-30" inclusive

Scenario: Export respects active dimension filters
  Given I am on the reporting dashboard
  And I have filtered by Region = "APAC" and Status = "Completed"
  And the report displays 12 rows
  When I click "Export CSV"
  Then the downloaded CSV contains exactly 12 data rows
  And every row has Region "APAC" and Status "Completed"

Scenario: Export with multiple filters applied simultaneously
  Given I have applied a date range filter "2026-01-01" to "2026-03-31"
  And I have applied a dimension filter Region = "EMEA"
  And the report displays 8 rows
  When I click "Export CSV"
  Then the CSV contains exactly 8 rows matching both filter criteria

Scenario: Export when all filters are cleared (no active filters)
  Given I am on the reporting dashboard with no filters applied
  And the report displays 5,000 rows
  When I click "Export CSV"
  Then the CSV contains all 5,000 rows
  And the filename indicates no filter scope, e.g. "report-2026-05-01.csv"

Scenario: Filter metadata not injected into data rows
  Given I have active filters for Region = "APAC"
  When I click "Export CSV"
  Then the CSV rows contain only data columns
  And no row contains a column named "Applied Filters" or equivalent metadata
```

**Edge Cases:**
- If the user changes filters while an export is in progress, the in-flight export must not be affected — it must complete using the filter state captured at the moment "Export CSV" was clicked.
- Filter state must be reflected in the filename or a summary row only if a product decision to do so is made; omit otherwise to keep downstream parsing simple. (Captured as anti-requirement below.)

**Anti-requirements:**
- This story does NOT embed filter metadata into the CSV file itself — that decision belongs to US-1 filename conventions.
- This story does NOT cover saving a named filter preset — out of scope entirely.
- This story does NOT cover exporting multiple filter configurations at once — out of scope entirely.

**Size:** M

---

### US-3: Select which columns to include before exporting

**As an** analyst running weekly performance reviews,
**I want** to choose which columns are included in my CSV export before downloading,
**so that** I receive a file that maps directly to the template I paste it into, without having to delete columns in my spreadsheet.

**Acceptance Criteria:**

```gherkin
Scenario: Column selector opens when I initiate export
  Given I am on the reporting dashboard with data loaded
  When I click "Export CSV"
  Then a column selection panel appears
  And every column visible in the dashboard is listed with a checkbox
  And all checkboxes are checked by default

Scenario: Export includes only selected columns
  Given the column selection panel is open
  And available columns are "Date", "Region", "Revenue", "Units", "Margin"
  When I uncheck "Units" and "Margin"
  And I click "Download"
  Then the CSV headers are "Date,Region,Revenue" in their original display order
  And no "Units" or "Margin" columns appear in any row

Scenario: Export button disabled when no columns are selected
  Given the column selection panel is open
  When I uncheck all columns
  Then the "Download" button is disabled
  And a validation message reads "Select at least one column to export"

Scenario: Column selection is reset to default on next export session
  Given I previously exported with only "Date" and "Revenue" selected
  When I click "Export CSV" again in the same or a new session
  Then all columns are checked by default again
  And my previous selection is not persisted

Scenario: Column order in export matches display order, not selection order
  Given I check columns in the order "Revenue", then "Date", then "Region"
  When I click "Download"
  Then the CSV headers are "Date,Region,Revenue" (dashboard display order)
  And not "Revenue,Date,Region" (selection order)
```

**Edge Cases:**
- If a column is hidden in the dashboard view (e.g. via a separate column visibility toggle), it must also be absent from the column selector.
- If the dashboard has more than 20 columns, the selector panel must support scrolling — columns must not be clipped.
- Keyboard navigation: all checkboxes must be reachable and toggleable via Tab and Space keys.

**Anti-requirements:**
- This story does NOT cover saving a named column preset — out of scope entirely.
- This story does NOT cover reordering columns in the export — out of scope entirely.
- This story does NOT cover adding calculated or derived columns not present in the dashboard — out of scope entirely.

**Size:** M

---

### US-4: Export a large dataset via asynchronous background generation

**As a** compliance officer auditing historical activity,
**I want** to request a full data export that runs in the background and notifies me when it is ready,
**so that** I can continue working in the dashboard without waiting for a large file to generate, and retrieve a complete, untruncated record.

**Acceptance Criteria:**

```gherkin
Scenario: Large export triggers async generation instead of immediate download
  Given I am on the reporting dashboard
  And the current report view contains more than 10,000 rows
  When I click "Export CSV"
  Then I see a notification: "Your export is being prepared. We'll notify you when it's ready."
  And the dashboard remains fully interactive
  And no file download begins immediately

Scenario: In-app notification when export is ready
  Given I requested a large CSV export
  And the export has completed processing
  When I am on any page within the application
  Then I receive an in-app notification: "Your CSV export is ready to download"
  And the notification contains a "Download" link

Scenario: Download link is valid for 24 hours
  Given my export completed and I received a download notification
  When I click the "Download" link within 24 hours of generation
  Then the CSV file downloads successfully

Scenario: Download link expired
  Given my export completed more than 24 hours ago
  When I click the "Download" link
  Then I see the message "This export link has expired. Return to the dashboard to generate a new export."
  And no file is downloaded

Scenario: Export fails during background processing
  Given I requested a large CSV export
  And the background job encounters an error during processing
  Then I receive an in-app notification: "Your CSV export failed. Please try again."
  And a "Retry" action is available in the notification
  And no partial file is made available for download

Scenario: Small dataset still downloads immediately
  Given I am on the reporting dashboard
  And the current report view contains 500 rows
  When I click "Export CSV"
  Then the file downloads immediately without an async notification
```

**Edge Cases:**
- The threshold for async vs. immediate download (10,000 rows) must be configurable server-side without a code deploy.
- If the user navigates away or closes the browser before the export completes, the background job must continue and the notification must appear on next login.
- If the user requests a second export while one is already processing, they must be informed of the in-progress export rather than queuing a duplicate.
- The generated file must be stored in a private, authenticated location — a direct S3-style public URL is not acceptable. The download link must require authentication.
- Email notification as an alternative delivery channel is out of scope (see anti-requirements) but the notification system must not preclude adding it later.

**Anti-requirements:**
- This story does NOT cover email delivery of the export file — out of scope for this initiative; flagged as a future enhancement.
- This story does NOT cover an exports history page — tracked as a follow-on story (US-5).
- This story does NOT cover scheduling recurring exports — out of scope entirely.

**Size:** L

---

### US-5: Re-download a previously generated export

**As a** team manager distributing reports to stakeholders,
**I want** to access and re-download exports I have previously generated,
**so that** I can share the same file with multiple stakeholders without regenerating it, and recover if I accidentally close the download notification.

**Acceptance Criteria:**

```gherkin
Scenario: Exports history lists recent exports
  Given I have generated at least one CSV export in the past 24 hours
  When I navigate to the exports history panel
  Then I see a list of my exports in reverse chronological order
  And each entry shows: export date/time, row count, filter summary, and expiry time
  And each entry has a "Download" button

Scenario: Re-download a non-expired export
  Given my exports history shows an export generated 2 hours ago
  When I click "Download" on that entry
  Then the original CSV file is downloaded
  And the file is identical to the one generated at initial export time

Scenario: Expired export shown but not downloadable
  Given my exports history shows an export generated 25 hours ago
  Then that entry is marked "Expired"
  And the "Download" button is replaced with "Re-generate"
  When I click "Re-generate"
  Then a new export is queued using the same filter configuration

Scenario: Exports history is user-scoped
  Given two users share access to the same dashboard
  When I view my exports history
  Then I see only my own exports
  And I do not see exports generated by the other user

Scenario: Empty exports history
  Given I have never generated a CSV export
  When I navigate to the exports history panel
  Then I see the message "No exports yet. Go to the dashboard and click Export CSV to get started."
  And no list items are displayed
```

**Edge Cases:**
- Exports history must not expose export files from other users, even if a URL is guessed — all download endpoints must enforce ownership checks.
- History is limited to the last 10 exports per user to keep the list actionable; older entries are automatically pruned (no user-facing deletion needed).
- If an export is still processing, it appears in the history as "Generating…" with no download button, and auto-refreshes status without a full page reload.

**Anti-requirements:**
- This story does NOT cover sharing an export link with another user — out of scope for this initiative.
- This story does NOT cover an admin-level view of all users' exports — out of scope entirely.
- This story does NOT cover deleting individual exports from history — out of scope entirely (pruning is automatic after 24 hours).

**Size:** M

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/16.0 (97%) |
| Evaluated | 2026-05-01 |
| Target duration | 87240 ms |
| Target cost | $0.1717 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires Gherkin format (Given/When/Then) for acceptance criteria — not free-form bullet points | PASS | All five stories use Gherkin scenarios exclusively. US-1 opens with 'Scenario: Successful CSV download of current view / Given I am authenticated and on the reporting dashboard / ... / When I click "Export CSV" / Then a CSV file is downloaded to my browser'. No free-form bullet acceptance criteria appear anywhere in the file. |
| c2 | Skill requires at least one edge case or error scenario in the acceptance criteria, not just the happy path | PASS | Every story has a dedicated 'Edge Cases' section and many have explicit error/empty-state Gherkin scenarios. US-1 includes 'Scenario: Export with no data in current view' and 'Scenario: Export button unavailable when report has not yet loaded'. US-4 includes 'Scenario: Export fails during background processing' with a Retry action. |
| c3 | Skill includes the ISC splitting test — Independent, Small, Complete — to verify stories are appropriately sized | PARTIAL | The output shows ISC-consistent behaviour — 5 stories are split with explicit independence enforced via anti-requirements (e.g. 'This story does NOT cover exporting with a custom column selection — tracked in US-3'), each has a Size field (M/L), and each is complete with happy-path + edge + error scenarios. However, the ISC framework is never named or explicitly applied as a verification step in the output. |
| c4 | Skill requires the standard "As a [role], I want [action], so that [outcome]" story format | PASS | All five stories use the exact three-part format. Example — US-2: 'As an operations lead working with a scoped date range and applied filters, I want to export only the rows that match my current filter selections, so that I receive a file scoped to exactly the segment I am analysing without post-processing in my spreadsheet.' |
| c5 | Skill prohibits solution-specifying stories — acceptance criteria must describe behaviour, not implementation | PASS | Gherkin Then-clauses are uniformly behavioural: 'Then a CSV file is downloaded to my browser', 'Then the CSV headers are "Date,Region,Revenue" in that order', 'Then I see a notification: "Your export is being prepared"'. No API endpoints, HTTP status codes, or database operations appear in the scenarios. Some implementation language in Edge Cases sections ('server-side configurable', 'authenticated location') is confined to non-scenario prose. |
| c6 | Skill addresses anti-requirements (things the story explicitly should NOT do) — partial credit if mentioned but not required as a mandatory section | PARTIAL | Every story has a mandatory 'Anti-requirements' section with multiple named exclusions. US-1: 'This story does NOT cover exporting with a custom column selection', 'does NOT cover large datasets requiring async generation', 'does NOT cover scheduled or recurring exports', 'does NOT cover export formats other than CSV'. Ceiling capped at PARTIAL. |
| c7 | Skill specifies that stories must have a single, clear acceptance condition — not "and/or" compound criteria | PASS | Each Gherkin scenario has a single named purpose (e.g. 'Scenario: Export respects active date range filter', 'Scenario: Column selector opens when I initiate export'). While scenarios contain multiple Then/And assertion steps (standard Gherkin), no scenario conflates unrelated outcomes or uses vague 'and/or' compound conditions. Scenarios are scoped and distinguishable. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | PARTIAL | The skill was successfully invoked as '/product-owner:write-user-story for allowing users to export...' and accepted a free-text argument, implying frontmatter exists and argument-hint is wired. However, the captured output (chat response + artifact) does not display the skill file's YAML frontmatter, so name, description, and argument-hint fields cannot be individually confirmed. |
| c9 | Output's user story uses the standard format — "As a [role e.g. report viewer], I want [to export the current dashboard view as a CSV file], so that [I can analyse the data offline / share with stakeholders who don't have access]" — with the role concrete, not "user" | PASS | All five roles are persona-specific: 'analyst running weekly performance reviews', 'operations lead working with a scoped date range and applied filters', 'compliance officer auditing historical activity', 'team manager distributing reports to stakeholders'. None use the generic 'user' role. |
| c10 | Output's acceptance criteria are in Gherkin format (Given / When / Then) — at least 3 scenarios — not bullet points | PASS | US-1 alone contains 4 Gherkin scenarios. US-2 has 5, US-3 has 5, US-4 has 6, US-5 has 5. All use Given/When/Then syntax exclusively with no bullet-list acceptance criteria. |
| c11 | Output's happy-path scenario covers the main flow — "Given I'm viewing a dashboard with data, When I click Export → CSV, Then a file downloads with the visible data, named appropriately, in valid CSV format" | PASS | US-1's first scenario 'Scenario: Successful CSV download of current view' opens with 'Given I am authenticated and on the reporting dashboard / And the report contains at least one row of data / When I click "Export CSV" / Then a CSV file is downloaded to my browser / And the filename follows the pattern "report-YYYY-MM-DD.csv" / And the first row contains the column headers matching those visible in the dashboard / And every row visible in the current view is present in the file'. |
| c12 | Output includes at least one edge case — empty dashboard (export creates a CSV with headers only and an info message), very large dataset (export shows progress indicator and either streams or queues a job), unicode characters in values (escaped correctly) | PASS | Empty dashboard: US-1 'Scenario: Export with no data in current view' — 'Then a CSV file is downloaded containing only the header row / And a toast notification reads "Export complete — no data rows matched your current view"'. Large dataset: US-4 is entirely dedicated to async background export for >10,000 rows. Unicode not explicitly named but RFC 4180 escaping of commas and double-quotes is covered in US-1 Edge Cases. |
| c13 | Output includes at least one error scenario — export endpoint fails (user sees a clear error message and can retry), permissions error (user without dashboard access cannot export), network drop mid-download | PASS | US-4 'Scenario: Export fails during background processing': 'Then I receive an in-app notification: "Your CSV export failed. Please try again." / And a "Retry" action is available in the notification / And no partial file is made available for download'. Clear error message and retry path both present. |
| c14 | Output's acceptance criteria are observable / verifiable — "Then a CSV file is downloaded" is testable; "Then the system handles it correctly" is not, and is rejected | PASS | All Then-clauses are specific and testable: 'Then the CSV headers are "Date,Region,Revenue" in that order', 'Then I see the message "This export link has expired..."', 'Then I see only my own exports / And I do not see exports generated by the other user'. No vague 'handles it correctly' language appears. |
| c15 | Output passes the ISC test — Independent (this story doesn't depend on a parallel story in flight), Small (deliverable in a single sprint), Complete (covers happy path, edges, and errors) | PASS | Independent: anti-requirements explicitly carve out scope between stories (e.g. US-1 references US-3 and US-4 as separate). Small: all rated M or L, single-sprint deliverable. Complete: each story has a happy-path scenario, Edge Cases section, and at least one error/boundary scenario (US-4 has explicit failure scenario with retry). |
| c16 | Output's acceptance criteria describe behaviour, not implementation — "Then the file contains all rows visible in the dashboard" is good; "Then the API endpoint returns a 200 with text/csv content type" is too implementation-specific for a user story | PASS | Gherkin Then-clauses uniformly describe user-observable outcomes: 'Then a CSV file is downloaded to my browser', 'Then that entry is marked "Expired" / And the "Download" button is replaced with "Re-generate"'. No HTTP status codes, API endpoint paths, SQL, or internal system state appear in the scenarios. |
| c17 | Output addresses what the CSV contains — exactly the data visible in the dashboard at export time, with column headers matching the displayed columns; respects active filters and sorts at export time | PASS | US-1: 'the first row contains the column headers matching those visible in the dashboard' and 'every row visible in the current view is present in the file / And no rows outside the current view are included'. US-2 is entirely dedicated to filter-scoped exports, with scenarios verifying 'every row has a date value between... inclusive' and filter combinations. |
| c18 | Output's anti-requirements section names what the story does NOT include — e.g. "does NOT support Excel format", "does NOT support scheduled exports", "does NOT include pivoted/aggregated data unless visible in the dashboard" | PARTIAL | Every story has an explicit Anti-requirements section. US-1 names: 'does NOT cover exporting with a custom column selection', 'does NOT cover large datasets requiring async generation', 'does NOT cover scheduled or recurring exports', 'does NOT cover export formats other than CSV (Excel, PDF, JSON)'. US-4: 'does NOT cover email delivery', 'does NOT cover scheduling recurring exports'. Ceiling capped at PARTIAL. |

### Notes

An exceptionally thorough output that earns near-perfect marks. The five-story split is well-scoped, the Gherkin scenarios are clean and behavioural, and every story has a complete Anti-requirements section. The two deductions: c3 loses half a point because the ISC framework is never explicitly named or applied as a discrete verification step (the behaviour is consistent with ISC but the test itself is absent from the output); c8 loses half a point because the skill's YAML frontmatter (name, description, argument-hint) cannot be verified from the captured output alone. Minor note: edge cases occasionally touch implementation language ('server-side configurable', 'no public S3 URLs') but this is confined to prose sections rather than Gherkin scenarios, so c5 and c16 are unaffected. Unicode escaping is not explicitly covered in edge cases, but the three specific examples in c12 only require 'at least one' so that criterion still passes.
