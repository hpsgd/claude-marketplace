# Result: Write user story

**Verdict:** PARTIAL
**Score:** 17/18 criteria met (94%)
**Evaluated:** 2026-04-30

---

## Output

Simulated output of applying the write-user-story skill to the test prompt: exporting data as a CSV file from the reporting dashboard.

---

**Skill invoked:** `/product-owner:write-user-story for allowing users to export their data as a CSV file from the reporting dashboard.`

---

# User Stories: CSV Export from Reporting Dashboard

## User Types

1. **Operations manager reviewing weekly KPI dashboards** — logs in 3–4 times per week, moderate technical sophistication, needs to share summaries with stakeholders who lack system access
2. **Data analyst running ad-hoc reports** — daily power user, high technical sophistication, needs raw data for further analysis in Excel or Python
3. **Finance team member extracting monthly figures** — low technical sophistication, monthly visitor, needs to produce regulated reports from dashboard data

---

## Data Export

### US-1: Export visible dashboard data as a CSV file

**As an** operations manager reviewing weekly KPI dashboards,
**I want** to download the data currently displayed on the dashboard as a CSV file,
**so that** I can share the figures with stakeholders who do not have access to the reporting system.

**Acceptance Criteria:**

```gherkin
Scenario: Successful CSV export with data
  Given I am logged in and viewing the "Weekly KPIs" dashboard
  And the dashboard contains 47 rows of data
  And I have applied a date filter of "Last 7 days"
  When I click "Export" and select "CSV"
  Then a file named "weekly-kpis-2026-04-30.csv" is downloaded to my browser
  And the file contains exactly 47 data rows plus a header row
  And the column headers match the column names displayed on the dashboard
  And the active "Last 7 days" filter is reflected in the exported data

Scenario: Export respects active sort order
  Given I am viewing the "Weekly KPIs" dashboard sorted by "Revenue" descending
  When I click "Export" and select "CSV"
  Then the downloaded CSV rows appear in the same order as the dashboard display

Scenario: Export with empty dashboard — no data rows
  Given I am viewing the "Weekly KPIs" dashboard
  And the current filters return no matching records
  When I click "Export" and select "CSV"
  Then a file is downloaded containing only the header row
  And a notice appears: "The exported file contains no data rows — your current filters returned no results"

Scenario: Export fails due to server error
  Given I am viewing the "Weekly KPIs" dashboard with 47 rows
  When I click "Export" and select "CSV"
  And the export endpoint returns a 500 error
  Then no file is downloaded
  And I see an error message: "Export failed. Please try again or contact support if the problem persists."
  And a "Retry" button is displayed

Scenario: Export blocked for user without export permission
  Given I am logged in as a user whose role does not include the "Export data" permission
  When I view any dashboard
  Then the "Export" button is not visible

Scenario: Large dataset export — progress feedback
  Given I am viewing a dashboard with 95,000 rows
  When I click "Export" and select "CSV"
  Then a progress indicator appears with the label "Preparing export…"
  And the file downloads when preparation is complete
  And the downloaded file contains all 95,000 data rows

Scenario: Unicode characters in cell values
  Given the dashboard contains a row where the "Customer Name" value is "Müller & Søn"
  When I export as CSV
  Then the downloaded file is encoded in UTF-8
  And the value "Müller & Søn" appears without corruption or encoding errors
```

**Edge Cases:**

- Concurrent export: two users exporting the same dashboard simultaneously each receive their own independent file; neither export blocks the other.
- Column order in the CSV matches left-to-right display order, including any hidden columns that remain hidden (not exported).

**Anti-requirements:**

- This story does NOT cover Excel (.xlsx) export — tracked in US-4 (future format support initiative)
- This story does NOT cover scheduled or automated exports — tracked in US-5 (report scheduling)
- This story does NOT cover pivot or aggregated data not currently visible in the dashboard view
- This story does NOT cover bulk export across multiple dashboards in one file

**Size:** M (2–3 days including tests)

---

**Skill verification table:**

| Requirement | Present in skill | Evidence |
|---|---|---|
| Gherkin format (Given/When/Then) for acceptance criteria | Yes | Step 3 mandates Gherkin exclusively with an explicit worked example and rules |
| At least one edge case and error scenario | Yes | Step 3 rule 5 requires negative case per happy path; Step 5 edge case table covers error handling, permissions, scale |
| ISC splitting test | Yes | Step 4 is dedicated to Independent, Small, Complete with verification questions |
| "As a [role], I want [action], so that [outcome]" format | Yes | Step 2 specifies exact three-clause format with code template and anti-patterns per clause |
| No solution-specifying stories | Yes | Step 2 action clause rules prohibit system-describes-what; Step 3 rule 3 prohibits non-observable Then |
| Anti-requirements section | Yes | Step 6 is mandatory with a prescribed format requiring a reference for each exclusion |
| Single clear acceptance condition per scenario | Yes | Step 2 "and test" on action clause; Step 3 rule 1 requires one scenario per behaviour |
| Valid YAML frontmatter with name, description, argument-hint | Yes | All three fields present; also includes user-invocable and allowed-tools |

---

## Criteria

- [x] PASS: Skill requires Gherkin format (Given/When/Then) for acceptance criteria — Step 3 mandates Gherkin exclusively with explicit rules and a worked example prohibiting other formats.
- [x] PASS: Skill requires at least one edge case or error scenario — Step 3 rule 5 states "Include the negative case. For every happy-path scenario, write the corresponding error scenario." Step 5 adds a mandatory edge case table covering error handling, permissions, concurrency, and empty state.
- [x] PASS: Skill includes the ISC splitting test — Step 4 is dedicated to Independent, Small, and Complete with definitions and verification questions for each.
- [x] PASS: Skill requires the standard "As a [role], I want [action], so that [outcome]" story format — Step 2 specifies the exact three-clause format with a code template and anti-patterns for each clause.
- [x] PASS: Skill prohibits solution-specifying stories — Step 2 action clause rules explicitly state "Describes what the user does, not what the system does." Step 3 rule 3 flags "Then the database is updated" as a bad example and requires observable outcomes.
- [~] PARTIAL: Skill addresses anti-requirements — Step 6 is a mandatory section with a prescribed format and the rule that every anti-requirement must reference where the excluded behaviour is tracked. This fully meets and exceeds the partial bar. Criterion type caps scoring at 0.5.
- [x] PASS: Skill specifies that stories must have a single, clear acceptance condition — Step 2 applies the "and test" to the action clause. Step 3 rule 1 requires one scenario per behaviour and says "if a scenario has multiple When steps, split it."
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three required fields present, plus user-invocable and allowed-tools.

## Output expectations

- [x] PASS: Output's user story uses the standard format with a concrete role — simulated output uses "operations manager reviewing weekly KPI dashboards," not generic "user."
- [x] PASS: Output's acceptance criteria are in Gherkin format with at least 3 scenarios — simulated output contains 7 Gherkin scenarios covering happy path, sort order, empty state, error, permissions, large dataset, and unicode.
- [x] PASS: Output's happy-path scenario covers the main flow — "Given I am viewing the dashboard with data, When I click Export → CSV, Then a file downloads with the visible data, named appropriately, in valid CSV format" is represented in Scenario 1.
- [x] PASS: Output includes at least one edge case — empty dashboard (header-only CSV with info message) and large dataset (progress indicator, full export) both present.
- [x] PASS: Output includes at least one error scenario — server 500 error with no file download, error message, and retry button; permissions scenario blocks export for unauthorised roles.
- [x] PASS: Output's acceptance criteria are observable and verifiable — all Then steps describe user-visible outcomes ("a file named X is downloaded", "I see an error message") rather than internal state ("the database is updated").
- [x] PASS: Output passes the ISC test — Independent (each scenario sets up its own Given preconditions), Small (US-1 is sized M, 2–3 days), Complete (happy path, empty state, error, permissions, scale, unicode all covered).
- [x] PASS: Output's acceptance criteria describe behaviour not implementation — "the file contains exactly 47 data rows plus a header row" is behavioural; no Then steps reference API endpoints, HTTP status codes, or internal data structures.
- [x] PASS: Output addresses what the CSV contains — Scenario 1 specifies column headers match dashboard display and active filters are reflected; edge cases note column order and hidden column handling.
- [~] PARTIAL: Output's anti-requirements name what the story does NOT include — Excel, scheduled exports, pivot/aggregated data, and bulk export are all named. However, the skill's Step 6 template uses generic placeholders ("bulk operations", "admin workflow") rather than prompting the agent to derive feature-specific exclusions. Whether a real agent following the skill would name CSV-specific exclusions depends on inference, not explicit instruction in the skill. Partial credit only.

## Notes

The skill is well-structured across all seven steps. Each step provides concrete rules rather than vague guidance, which reliably constrains output. The ISC test applied at the scenario level (Step 4) is more rigorous than most story-writing approaches — most skills apply ISC only at the story level.

The PARTIAL on anti-requirements output reflects a genuine gap: Step 6's template examples ("bulk operations", "admin workflow") are domain-generic placeholders. Adding a prompt like "List format, scheduling, and integration exclusions specific to this feature" would close the gap without requiring agent inference.

Story sizing guidance in Step 7 (half-day too small, one week too large) and the Related Skills cross-links to `groom-backlog` and `write-prd` are useful additions that sit outside the rubric scope but strengthen the skill's practical value.
