# Test: Write user guide

Scenario: Testing whether the write-user-guide skill requires a research step, numbered steps with expected results, and a troubleshooting section for the feature.

## Prompt


/user-docs-writer:write-user-guide for our time tracking feature — users can log time against projects and tasks, set estimates, and view utilisation reports.

## Criteria


- [ ] PASS: Skill requires a research step — reading existing feature specs, support tickets, or product docs before writing
- [ ] PASS: Skill produces numbered steps for procedural tasks — not bullet points
- [ ] PASS: Each step includes what the user should see after completing it — confirmation of success
- [ ] PASS: Skill requires a troubleshooting section covering the most common problems users face with this feature
- [ ] PASS: Skill uses only product terminology — no technical language without plain-English explanation
- [ ] PASS: Skill requires related content links at the end — connecting users to adjacent features or prerequisite knowledge
- [ ] PARTIAL: Skill requires role-based or permissions context — noting when certain actions require admin access — partial credit if permissions are mentioned but not required as a standard documentation element
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output covers the three named time-tracking capabilities — log time against projects/tasks, set estimates, view utilisation reports — each as a distinct task section with its own steps
- [ ] PASS: Output's "log time" section walks through both flows users will actually do — log time as you work (timer-based or "start tracking now"), AND log retrospectively (enter time after the fact for yesterday's work)
- [ ] PASS: Output's "set estimates" section explains the WHY first — estimates feed into utilisation reports and over/under tracking — and how to set them on projects vs tasks (and what happens if both have estimates)
- [ ] PASS: Output's "utilisation reports" section explains how to read the report — what utilisation % means, what 80% utilisation indicates, how billable vs non-billable hours are categorised
- [ ] PASS: Output's steps are numbered with explicit expected results — "Step 3: Click Log Time. The time entry form appears showing today's date. Step 4: Enter the duration. The form shows the running total for this task" — not just "log your time"
- [ ] PASS: Output's troubleshooting covers common problems — timer was running but didn't save (browser closed, network), edit/delete a logged entry, time entry dispute (manager-locked entries), reporting period boundaries (entries that span months)
- [ ] PASS: Output uses product terminology consistently — "log time" / "time entry" / "estimate" / "utilisation report" — without jargon; any internal-only terms (e.g. "TES" for time-entry-service) are excluded
- [ ] PASS: Output addresses role / permissions explicitly — who can edit other users' time entries (admins / project leads), who can see utilisation reports (managers, not all team members), and what individual users can see
- [ ] PASS: Output's related-content links cover adjacent features — exporting timesheets to payroll, integrating with billable invoicing, blocking time entries after submission deadline
- [ ] PARTIAL: Output addresses mobile time entry if the product supports it — quickly logging on the go is a common time-tracking use case
