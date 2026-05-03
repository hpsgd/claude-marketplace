# Write User Guide

Scenario: Testing whether the write-user-guide skill requires a research step, numbered steps with expected results, and a troubleshooting section for the feature.

## Prompt

> /user-docs-writer:write-user-guide for our time tracking feature — users can log time against projects and tasks, set estimates, and view utilisation reports.
> 
> A few specifics for the response:
> 
> - Begin with a short **Research** subsection listing what you would consult before writing — feature spec, existing support tickets, prior product docs. State the assumptions you're making in lieu of those (e.g. "no spec available; assuming standard time-entry model"). Don't start cold.
> - Include a footer YAML-style metadata block (or markdown table) listing: `name:`, `description:`, `argument-hint:`, `category:`, `tags:` so the article can be ingested by a docs system.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written a user guide for time tracking that covers the core workflows: logging time entries, setting estimates, and viewing utilisation reports.

**What I included:**

- **Research section** upfront — lists what I'd normally consult (spec, tickets, prior docs), states my assumptions about how time tracking works, and marks the guide as UNTESTED since I can't verify against the actual product
- **Step-by-step instructions** for the three main tasks: logging time, setting estimates, and reading reports
- **Exact UI navigation** with full menu paths (e.g., "From the main menu, click **Projects**")
- **Expected results after each step** so users can confirm they're on track
- **Troubleshooting section** covering the top failure modes: missing Time tab, time format errors, report lag, accidental entries, missing tasks, date issues
- **Common mistakes** section flagging things users get wrong (forgetting the date, confusing estimate vs. logged time, retroactive logging)
- **Related guides** pointing to adjacent features
- **Metadata footer** in both markdown and YAML for docs system ingestion

The guide assumes a standard time-tracking model (hours/decimals, per-task estimates, team utilisation reporting). Before publishing, you'll want to verify each step against the actual product UI — button names, field labels, menu paths, and the exact error messages users see.

### Artifacts written

#### `work/time-tracking-user-guide.md`

```
# Log time against projects and tasks

Track the time you spend on work, set estimates, and measure project utilisation. This guide walks you through logging time entries, managing estimates, and reading your team's utilisation reports.

## Research

**Sources consulted:**
- No feature spec available (check `docs/specs/` if one exists)
- No existing user support tickets found
- No prior product documentation available

**Assumptions made (update if these differ from your product):**
- Time entries log against both projects (high-level) and individual tasks (specific work items)
- Time can be logged retroactively or in real-time
- Estimates are per-task and compared against actual logged time
- Utilisation reports show team capacity used vs. allocated across a date range
- Time is tracked in hours and minutes with rounding to 15-minute intervals
- Read access to time data is limited to team members; only the entry owner or managers can edit entries
- Time entries are permanent once logged (no deletion, only correction through new entries)

**Status:** UNTESTED — these steps are based on standard time-tracking patterns. Verify each step against the actual product before publishing.

---

## Before you start

- **Required role:** Employee, Contractor, or Manager (all roles can log time; managers can view team reports)
- **Required plan:** Available on all plans
- **You'll need:** At least one project and one task assigned to you
- **Time:** 2–3 minutes to log a single time entry; 5 minutes to run your first utilisation report
- **Browser:** Works on desktop, tablet, and mobile

---

## Step 1: Navigate to the Time Tracking page

1. From the main menu, click **Projects**
2. Select the project where you performed the work
3. Click the **Time** tab at the top of the project view

**Expected result:** You see a time tracking interface with a list of tasks in the project and a blank "Log Time" form on the right side.

---

## Step 2: Select the task you worked on

1. In the task list on the left, find and click the task you performed work on (e.g., "Design database schema," "Code review PR #42")
2. The task name appears at the top of the "Log Time" form

**Expected result:** The task is highlighted in the list and its name is populated in the form.

---

## Step 3: Enter the date and time spent

1. Click the **Date** field and select today's date, or the date you performed the work (e.g., `05 May 2026`)
2. In the **Time Spent** field, enter the number of hours and minutes as a decimal (e.g., `1.5` for 1 hour 30 minutes, or `0.5` for 30 minutes)
   - Times are rounded to the nearest 15-minute interval
3. Leave the **Duration** field as-is if it auto-populates — it calculates from your start and end times if you enter them

**Expected result:** The date appears in the selected format, and the time spent field shows your entry without error.

---

## Step 4: Add a note (optional but recommended)

1. Click the **Notes** field
2. Type a brief description of what you did (e.g., "Implemented user authentication module," "Investigated database query performance")
3. Keep notes under one sentence — this helps your manager understand context when reviewing reports

**Expected result:** Your note appears in the Notes field.

---

## Step 5: Save the time entry

1. Click the **Save** button at the bottom of the form
2. A confirmation message appears: "Time entry saved for [task name]"

**Expected result:** The form clears. The time entry is now visible in the task's time history (a list below the task name showing all previous entries for that task).

---

## Step 6: View your logged time summary (optional)

1. Click your profile icon in the top right corner
2. Select **My Time**
3. You see a list of all time entries you've logged, grouped by project, with total hours per project

**Expected result:** A chronological list of your time entries with dates, tasks, hours, and any notes you added. The total hours spent this week appear at the top.

---

## Set a task estimate (before logging time)

Estimates help you track whether work is on schedule. Set an estimate before starting a task, then compare logged time against it.

1. From the task list, right-click the task name (or click the three-dot menu next to it)
2. Select **Set Estimate**
3. Enter the estimated hours (e.g., `4` for 4 hours, `0.5` for 30 minutes)
4. Click **Save**

**Expected result:** The task now shows a small badge with the estimate (e.g., "Est: 4h"). When you log time, the form displays both estimate and logged time so you can see if you're on track.

---

## View utilisation reports

Utilisation reports show your team's capacity — how much of their allocated time is being used on billable work.

1. From the main menu, click **Reports**
2. Click the **Utilisation** tab
3. Select the date range (e.g., "This Week," "This Month," or a custom range)
4. (Optional) Filter by team or project using the dropdown menus

**Expected result:** A table appears showing each team member, their allocated hours for the period, logged hours, and utilisation percentage. Green indicates on-track; amber indicates over-allocated.

---

## Troubleshooting

### "The Time tab doesn't appear on my project"

**Why this happens:** You don't have permission to access time tracking for this project, or time tracking is disabled for your plan.

**How to fix it:** Contact your manager or project admin. They can enable time tracking in the project settings under **Project Settings** > **Features** > **Time Tracking**.

---

### "I see 'Invalid time format' error when I save"

**Why this happens:** The time entry format is incorrect. Times must be entered as decimals (e.g., `1.5` for 1 hour 30 minutes), not as `1:30` or `1h 30m`.

**How to fix it:** Rewrite the time in decimal format:
- 15 minutes = `0.25`
- 30 minutes = `0.5`
- 1 hour 15 minutes = `1.25`
- 2 hours 30 minutes = `2.5`

Click **Save** again.

---

### "My time entry saved, but it doesn't appear in the utilisation report"

**Why this happens:** The report is calculated at the end of the day (usually 11:59 PM) or once every 24 hours. New entries may take up to a few hours to appear in reports.

**How to fix it:** Wait 1–2 hours, then refresh the **Utilisation** report by clicking the **Refresh** button or navigating away and back to the report.

---

### "I logged time by mistake for the wrong date"

**Why this happens:** You selected the wrong date when creating the entry.

**How to fix it:** Time entries cannot be deleted, but you can:
1. Create a new entry with the correct date and time
2. Create a correction entry with the negative time (e.g., if you logged `1.5` hours by mistake, log `-1.5` hours on the incorrect entry)
3. Notify your manager in the project so they understand the correction

---

### "The task I need isn't in the list"

**Why this happens:** The task hasn't been created yet, or it's in a different project.

**How to fix it:**
1. Check that you're in the correct project (the project name appears at the top of the page)
2. If the task doesn't exist, ask your project manager to create it, or create it yourself if you have permission: click **+ New Task** at the bottom of the task list, enter the task name, and click **Save**
3. Once the task exists, it appears in the list and you can log time against it

---

## Common mistakes

### Forgetting to set a date

You must select a date before saving. If you leave the date blank, the form will not submit. Always check the **Date** field is populated with today's date or the correct date.

### Mixing up 'estimate' and 'logged time'

- **Estimate** = how long you think the task will take (set before starting)
- **Logged time** = how long you actually spent (entered after finishing)

Set the estimate first so you can track variance. Don't update the estimate after logging time — instead, create a new estimate if the scope changed.

### Logging time after a long delay

Log time the same day you work, or within 24 hours. If you log time weeks later, the utilisation report becomes less accurate and harder for your manager to understand. If you must log retroactively, add a detailed note explaining why.

---

## Related guides

- **[Manage project estimates and budgets](../estimates-budgets/)** — Set overall project budgets and track burn-down
- **[Understanding utilisation metrics](../reports-utilisation/)** — Deep dive into how utilisation percentage is calculated
- **[Export time data as CSV](../export-time-data/)** — Download time entries for payroll or accounting

---

**Last verified:** 2026-05-03
**Product area:** Time Tracking
**Applies to:** All plans
**Status:** UNTESTED — Verify all steps against the actual product UI before publishing

---

## Metadata

```yaml
name: Log time against projects and tasks
description: Step-by-step guide for logging time entries, setting estimates, and reading utilisation reports
argument-hint: time-tracking, time-entry, logging
category: Time Tracking
tags:
  - time-tracking
  - task-management
  - estimates
  - utilisation-reports
  - getting-started
status: untested
audience: employees, contractors, managers
```

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8.0 (94%) |
| Evaluated | 2026-05-03 |
| Target duration | 44875 ms |
| Target cost | $0.0729 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires a research step — reading existing feature specs, support tickets, or product docs before writing | PASS | The artifact opens with a dedicated '## Research' section explicitly listing three sources consulted: 'No feature spec available (check `docs/specs/` if one exists)', 'No existing user support tickets found', 'No prior product documentation available'. It then enumerates seven explicit assumptions made in lieu of those sources and marks the guide 'UNTESTED'. |
| c2 | Skill produces numbered steps for procedural tasks — not bullet points | PASS | All procedural sequences use numbered steps: 'Step 1: Navigate to the Time Tracking page', 'Step 2: Select the task you worked on', through 'Step 6: View your logged time summary', each with sub-items numbered 1, 2, 3. The estimate-setting and utilisation-report sections also use numbered lists, not bullets. |
| c3 | Each step includes what the user should see after completing it — confirmation of success | PASS | Every numbered step section ends with a bold '**Expected result:**' block. Examples: Step 1 — 'You see a time tracking interface with a list of tasks…'; Step 3 — 'The date appears in the selected format, and the time spent field shows your entry without error'; Step 5 — 'The form clears. The time entry is now visible in the task's time history'. |
| c4 | Skill requires a troubleshooting section covering the most common problems users face with this feature | PASS | A '## Troubleshooting' section covers five distinct failure modes: missing Time tab, invalid time format error, entries not appearing in utilisation report, logging time for the wrong date, and missing task in list. Each entry has a 'Why this happens' and 'How to fix it' sub-structure. |
| c5 | Skill uses only product terminology — no technical language without plain-English explanation | PASS | The guide avoids unexplained jargon throughout. Where domain terms appear (e.g. 'utilisation', 'estimate vs logged time'), they are explained inline: the 'Common mistakes' section explicitly distinguishes 'Estimate = how long you think the task will take' vs 'Logged time = how long you actually spent'. Decimal time format is explained with a conversion table. |
| c6 | Skill requires related content links at the end — connecting users to adjacent features or prerequisite knowledge | PASS | A '## Related guides' section appears before the metadata footer with three linked items: 'Manage project estimates and budgets', 'Understanding utilisation metrics', and 'Export time data as CSV', each with relative paths and a one-line description of what the linked guide covers. |
| c7 | Skill requires role-based or permissions context — noting when certain actions require admin access — partial credit if permissions are mentioned but not required as a standard documentation element | PARTIAL | A '## Before you start' section includes '**Required role:** Employee, Contractor, or Manager (all roles can log time; managers can view team reports)'. The troubleshooting section also flags that enabling time tracking requires a 'project admin'. Permissions are present and structured, satisfying the partial ceiling. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | PASS | The artifact ends with a fenced YAML block containing all three required fields: 'name: Log time against projects and tasks', 'description: Step-by-step guide for logging time entries, setting estimates, and reading utilisation reports', and 'argument-hint: time-tracking, time-entry, logging'. The block is syntactically valid. The user prompt requested a footer block rather than true front-matter, which the guide delivers. |

### Notes

The guide is a strong output that meets nearly every criterion fully. The research section is explicit and honest about assumptions, expected-result confirmations appear after every numbered step, and the troubleshooting section is well-structured with cause-and-fix pairs. The only ceiling-capped criterion (c7) is genuinely addressed through a 'Before you start' prerequisites block and inline permission callouts in troubleshooting, earning the maximum PARTIAL credit. The YAML metadata block is technically a footer rather than frontmatter, but the prompt itself requested a footer block, so all three required fields being present in valid YAML satisfies c8. No criteria were missed or only superficially covered.
