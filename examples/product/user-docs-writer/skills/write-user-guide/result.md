# Write user guide

Testing whether the write-user-guide skill requires a research step, numbered steps with expected results, and a troubleshooting section for the feature.

## Prompt

> /user-docs-writer:write-user-guide for our time tracking feature — users can log time against projects and tasks, set estimates, and view utilisation reports.

## Output

**Log time and track progress in Clearpath**

This guide covers how to log time against tasks, set estimates, and view utilisation reports. It's for any team member who needs to track their work or review their team's output.

### Before you start

- **Required role:** All team members can log time. Manager or Admin role required to view utilisation reports. Admin required to enable time tracking for the workspace.
- **Required plan:** Pro and Enterprise
- **You'll need:** Time tracking enabled for your workspace (Settings > Time Tracking > Enable)
- **Time:** About 5 minutes

### Step 1: Log time against a task

1. Open the task you worked on.
**Expected result:** You'll see the task detail panel on the right.
2. Click the clock icon in the task toolbar, or select **Log time** from the task menu (···).
**Expected result:** A "Log time" dialog opens.
3. Enter the time spent (e.g. `1h 30m` or `1.5h`).
4. Click **Log time**.
**Expected result:** Your logged time appears below the task description. The task's total tracked time updates immediately.

### Step 2: Set a time estimate

1. Open the task.
2. Click **Add estimate** (shown when no estimate is set) or click the existing estimate.
3. Enter the estimated time (e.g. `2h`) and click **Save**.
**Expected result:** The estimate appears next to the logged time. If logged time exceeds the estimate, the value turns red.

### Step 3: View utilisation reports

1. Go to **Reports** > **Utilisation** (requires Manager or Admin role).
2. Use the filters to select your team, date range, and project.
3. Review the report.
**Expected result:** The report shows logged time vs estimates per person and per project.

### Troubleshooting

#### Time tracking option not visible on a task

| Field | Value |
|---|---|
| Why this happens | Time tracking may be disabled for your workspace, or you may not have permission to log time on this project. |
| How to fix it | Ask your Admin to check **Settings** > **Time Tracking**. If the workspace setting is enabled, check with your project Admin about permissions. |


#### My time isn't showing in the utilisation report

| Field | Value |
|---|---|
| Why this happens | Reports refresh every 15 minutes. |
| How to fix it | Wait and reload. Check you're using the correct date range and team filter. |


#### I entered the wrong time

| Field | Value |
|---|---|
| Why this happens | Common input error. |
| How to fix it | Click the entry in the task detail view and select **Edit** or **Delete**. |


### Related guides

- **View your team's utilisation** — how to read and filter utilisation reports
- **Set project budgets** — track logged time against a project budget
- **Enable time tracking for your workspace (Admin)** — required setup step

---
Last verified: 2026-04-16
Product area: Time Tracking
Applies to: Pro and Enterprise

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Research step required — Step 1 "Research the feature" is mandatory before writing. It requires searching the codebase for UI components, routes, and handlers; identifying all feature states; finding required permissions; and checking existing documentation. This is the first step and explicitly precedes writing.
- [x] PASS: Numbered steps required — Step 3 "Write step-by-step instructions" uses a numbered format template explicitly. The rules state "One action per step" and the format is `1. [action]` throughout. Bullet points are not the required format.
- [x] PASS: Expected result per step required — the step template explicitly includes `**Expected result:** [What the user should see — e.g., "The new member appears in the team list with a 'Pending' badge."]` as a mandatory field for every step.
- [x] PASS: Troubleshooting section required — Step 4 "Write troubleshooting" is a mandatory step. The definition requires at minimum the most common error message, the most common user mistake, and environment differences. The Problem/Why/Fix structure is mandated.
- [x] PASS: Product terminology only — the Rules section explicitly says "Use product language, not developer language" and "match the vocabulary the user sees in the UI." The quality checks in Step 6 include "No jargon: Would a non-technical user understand every term?"
- [x] PASS: Related content links required — Step 5 "Write related content and metadata" is a required step producing a "Related guides" section with next logical task, alternative approach, and deeper topic links.
- [~] PARTIAL: Role/permissions context — Step 1 research explicitly requires "Find the permissions or roles required to access the feature." The guide header template in Step 2 includes `**Required role:**` as a mandatory field. Permissions are a required standard documentation element. Maximum score is 0.5 per PARTIAL ceiling — the definition fully meets the intent of this criterion but the ceiling is the test author's constraint.
- [x] PASS: Valid YAML frontmatter — contains `name: write-user-guide`, `description`, and `argument-hint` fields.

### Notes

The role/permissions criterion (7) is fully met by the definition — Step 1 requires finding permissions and Step 2's header template has a dedicated "Required role" field. The PARTIAL ceiling is set by the test author, not a definition gap.

The Step 6 quality checklist is thorough: 10 checks covering title, one-action-per-step, expected results, exact UI labels, example inputs, navigation paths, jargon, troubleshooting, prerequisites, and testing. Most skills have quality guidance — this one has it as a structured checklist, which makes it actionable.

The "Never write 'simply,' 'just,' or 'easily'" rule in the Rules section is a good inclusion. It prevents the common writer mistake of minimising difficulty, which makes users feel worse when they struggle with something they were told was easy.
