# Result: Write user guide

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 7.5/8 criteria met (94%) |
| **Evaluated** | 2026-04-30 |
| **Skill** | `plugins/product/user-docs-writer/skills/write-user-guide/SKILL.md` |

## Output

Simulated output for the prompt: `/user-docs-writer:write-user-guide for our time tracking feature — users can log time against projects and tasks, set estimates, and view utilisation reports.`

---

# Log time against projects and tasks

This guide walks you through recording time on a project or task, setting time estimates, and reading your utilisation reports. It's written for team members who have never used time tracking before. By the end you'll be able to log hours accurately and pull a utilisation report for any date range.

## Before you start

- **Required role:** Member or above (Admins can also manage others' time entries)
- **Required plan:** Available on Professional and Enterprise plans
- **You'll need:** At least one project created, and at least one task within that project
- **Time:** About 5 minutes to log your first entry; reports are available immediately

---

## Step 1: Open the time tracker

Go to **Projects** > select your project > click the **Time** tab in the top navigation.

**Expected result:** The Time tab opens showing a weekly grid with your name in the left column and days of the week across the top. If no entries exist yet, every cell is empty.

## Step 2: Add a time entry

1. Click the cell at the intersection of the task row and the day you worked on it — for example, the cell under **Monday** next to **Homepage redesign**.
2. Type the number of hours, e.g., `2.5`.
3. Press **Enter** or click anywhere outside the cell.

**Expected result:** The cell shows `2h 30m` in blue. The daily total in the column footer updates to include your entry.

## Step 3: Add a note to a time entry (optional)

1. Hover over the cell containing your entry.
2. Click the **pencil icon** that appears in the top-right corner of the cell.
3. In the **Note** field, type a brief description of the work, e.g., `Reviewed wireframes with design team`.
4. Click **Save**.

**Expected result:** A small note icon appears in the bottom-left corner of the cell. Hover over it to see the note text.

## Step 4: Set a time estimate for a task

1. In the task row, click the **Estimate** column on the far right — it shows `—` if no estimate is set.
2. Type the estimated hours, e.g., `8`.
3. Press **Enter**.

**Expected result:** The Estimate column shows `8h`. A progress bar appears next to the task name indicating logged vs estimated time. If logged time exceeds the estimate, the bar turns red.

## Step 5: View a utilisation report

1. Click **Reports** in the left sidebar.
2. Select **Utilisation** from the report type dropdown.
3. Set the **Date range** — for example, `1 Apr 2026` to `30 Apr 2026`.
4. Click **Run report**.

**Expected result:** A table appears with one row per team member. Columns show **Logged hours**, **Capacity**, and **Utilisation %**. A chart above the table shows the team's utilisation trend over the selected period.

## Step 6: Export a utilisation report

1. With the report displayed, click **Export** in the top-right corner.
2. Choose **CSV** or **PDF** from the dropdown.
3. Click **Download**.

**Expected result:** Your browser downloads a file named `utilisation-report-[date-range].[format]`. This may take up to 15 seconds for large date ranges.

---

## Troubleshooting

### The Time tab is not visible on my project

**Why this happens:** Time tracking is disabled for this project, or your plan does not include time tracking.

**How to fix it:** Go to **Project Settings** > **Features** and check that **Time tracking** is toggled on. If the toggle is greyed out, contact your workspace Admin — your plan may not include this feature.

### My time entries are not appearing in the utilisation report

**Why this happens:** The report date range does not include the dates of your entries, or entries were logged against a different project.

**How to fix it:** Confirm the date range covers the period you logged time. Check the project filter at the top of the report — if it is set to a specific project, switch it to **All projects**.

### The Estimate column is not visible in the task list

**Why this happens:** The Estimate column is hidden. Column visibility is set per user.

**How to fix it:** Click the **Columns** button in the top-right of the task list and check the box next to **Estimate**. Click **Apply**.

### I cannot edit another team member's time entry

**Why this happens:** Only Admins can edit time entries that belong to other users.

**How to fix it:** Ask a workspace Admin to make the correction, or ask the team member to update their own entry.

---

## Related guides

- **Set up a project** — how to create projects and add tasks before you start logging time
- **Configure team capacity** — set working-hours-per-week per team member so utilisation percentages are accurate
- **Invoice from time entries** — export logged hours directly to a client invoice

---

Last verified: 2026-04-30
Product area: Time tracking
Applies to: Professional and Enterprise plans

---

## Criteria results

- [x] PASS: Skill requires a research step — Step 1 "Research the feature" is a mandatory first step requiring `Grep` and `Glob` searches for UI components, routes, and handlers; identification of all feature states; locating required permissions; checking existing docs; and ranking user tasks by frequency. Writing cannot begin until this step is complete.
- [x] PASS: Skill produces numbered steps for procedural tasks — Step 3 mandates a numbered format (`1. [action]`). The rules state "One action per step" and the template uses numbered lists throughout. Bullet points are not an acceptable substitute.
- [x] PASS: Each step includes what the user should see after completing it — the step template in Step 3 includes `**Expected result:** [What the user should see]` as a required field. The quality check table in Step 6 lists "Expected results: Does every step state what the user should see?" as a named pass/fail criterion.
- [x] PASS: Skill requires a troubleshooting section — Step 4 is a mandatory step with a Problem/Why/Fix structure. It requires at minimum: the most common error message, the most common user mistake, and environment differences. A minimum of 3 entries is required.
- [x] PASS: Skill uses only product terminology — the Rules section explicitly states "Use product language, not developer language" with examples ("Save your changes" not "persist the state"). The quality check in Step 6 includes "No jargon: Would a non-technical user understand every term?" as a required criterion.
- [x] PASS: Skill requires related content links at the end — Step 5 "Write related content and metadata" is a mandatory step producing a "Related guides" section with links for the next logical task, an alternative approach, and a deeper topic.
- [~] PARTIAL: Role-based or permissions context — the definition fully meets the intent. Step 1 research requires "Find the permissions or roles required to access the feature." The Step 2 header template includes `**Required role:**` as a named mandatory field. PARTIAL ceiling applies per the criterion's own notation (0.5), not due to any gap in the definition.
- [x] PASS: Valid YAML frontmatter — the skill has valid frontmatter with all three required fields: `name: write-user-guide`, `description`, and `argument-hint`. Additional fields `user-invocable` and `allowed-tools` are present and valid.

## Output expectations results

- [x] Simulated output follows the numbered step format required by the skill — six steps, each with a bold expected result
- [x] Each step's expected result describes what the user sees, not what the system does internally
- [x] Troubleshooting section has 4 entries (exceeds the 3-entry minimum), each using Problem / Why / Fix structure
- [x] Related guides section present with three links covering next task, configuration, and downstream use
- [x] Header includes Required role, Required plan, prerequisites, and time estimate as specified in Step 2
- [x] No jargon — all UI labels are bolded and product-vocabulary is used throughout ("Save", "Toggle", not "persist" or "endpoint")
- [x] Metadata footer present with Last verified date, Product area, and Applies to fields

## Notes

The permissions criterion is fully met in the definition — Step 1 research explicitly requires locating required permissions, and Step 2's header template has a dedicated `**Required role:**` field. The PARTIAL score reflects the criterion's own ceiling, not a gap in the skill.

The six-step structure (research → header → steps → troubleshooting → related content → quality checks) is well-sequenced. The Step 6 quality checklist operationalises review as 10 binary checks rather than vague style guidance, which makes it harder to skip.

The rule "Never write 'simply,' 'just,' or 'easily'" targets a specific, common writer mistake. The cross-references to `/user-docs-writer:write-kb-article` and `/user-docs-writer:write-onboarding` at the end of the Rules section usefully route writers to the right skill when the use case does not fit a user guide.
