# Result: Write KB article (support)

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

The following is a simulated KB article the skill would produce for the prompt:

> `/support:write-kb-article about why exports fail for large datasets — we get 8-12 tickets a week about this and the answer is always the same: use date range filtering to export in smaller batches.`

---

### Why do my exports fail when I try to download large datasets?

Exports time out when your dataset is too large to process within the system's 30-second limit. Use date-range filtering to split the export into smaller batches — each batch will download successfully.

*Why this happens:* The export engine streams your data through a single 30-second processing window. Datasets over approximately 50,000 rows (or those with many columns) can't fit in that window, so the export times out before completing.

---

**Prerequisites**

- You must have the **Viewer**, **Editor**, or **Admin** role on the dashboard you want to export.
- Available on all plans. API export for very large datasets requires a Pro or Enterprise plan.

---

**Step-by-step instructions**

1. **Open the dashboard you want to export.**
   Go to the **Dashboards** section from the left sidebar and click the dashboard name.

   Expected result: The dashboard loads with your data visible.

2. **Open the date range filter.**
   Click the **Date Range** button in the top-right corner of the dashboard.

   ![Screenshot: Date Range button in top-right of dashboard](TODO)

   Expected result: A date picker panel opens.

3. **Set a one-month date range.**
   Choose a start date and end date no more than 31 days apart. Use the **From** and **To** fields to enter dates manually, or click the calendar to select them.

   Expected result: The dashboard updates to show data for your selected range.

4. **Export the filtered data.**
   Click **Export** > **Download as CSV** in the top-right menu.

   Expected result: A file download begins immediately. If you see an error here, see the Troubleshooting section below.

5. **Repeat for the next date range.**
   Move your date range forward by one month and repeat steps 3–4 until you have exported all the data you need.

   Expected result: You have one CSV file per month, covering the full period you need.

---

**Troubleshooting**

**Problem:** Export still fails after applying date-range filtering.
**Cause:** The filtered dataset may still be too large — either the date range is too wide or the dashboard has a large number of columns.
**Solution:** Narrow the date range further (try two weeks instead of one month), or reduce the number of columns by hiding fields you don't need before exporting.

**Problem:** Export downloads but the file is empty.
**Cause:** The date range filter selected a period with no data, or a secondary filter (e.g. a segment or team filter) excluded all rows.
**Solution:** Check that there is data visible in the dashboard before exporting. Confirm no additional filters are active by clicking **Clear all filters** and re-applying only the date range.

**Problem:** Export file downloads but won't open in Excel.
**Cause:** The file is encoded in UTF-8, which Excel on Windows does not open automatically.
**Solution:** In Excel, use **Data** > **From Text/CSV** and select **UTF-8** encoding when prompted, rather than double-clicking the file.

**Problem:** Export button is greyed out or missing.
**Cause:** Your role does not have export permissions on this dashboard.
**Solution:** Ask an Admin or Owner to grant you at least Viewer export access, or ask them to run the export on your behalf.

---

**When this workaround isn't enough**

If you're exporting large datasets every week, splitting by date range manually is a band-aid. Two better paths:

- **Scheduled exports:** Set up a recurring export delivered to your inbox — available on Pro and Enterprise plans. See *Setting up scheduled exports* [To be created].
- **API access:** Use the export API to pull data programmatically without the 30-second timeout. See *Exporting data via the API* [To be created], or contact support about API access on your current plan.

---

**Related articles**

*Next steps*
- Scheduled exports for large reports [To be created]
- Exporting data via the API [To be created]

*Related topics*
- Filtering and sorting your dashboards [To be created]
- Combining and merging exported CSV files [To be created]

*Background*
- Understanding dashboard data refresh and lag [To be created]

---

**If this didn't help**

Contact support with the following details so we can investigate:
- The dashboard name and URL
- The date range you selected
- The exact error message you saw (or "no error, file just didn't download")
- Your browser and operating system

---

```
---
Last verified: 2026-04-30
Product area: Data Export
Applies to: All plans (API export: Pro and Enterprise)
Tags: export, CSV, large dataset, timeout, date range filter
---
```

**Maintenance**

- **Update trigger:** Review when the export feature changes in a product release.
- **Staleness check:** Flag for review if not verified within 90 days.
- **Helpfulness tracking:** Monitor article views vs. tickets on this topic. High views with continued ticket volume means the article needs a rewrite.
- **Retirement criteria:** Archive when the export system is replaced; redirect to the successor article.

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Skill requires the article title to be a question the user would search — the skill is explicit: "Write the title as the question the user would type into a search bar. Use their vocabulary, not internal terminology." Good/bad examples are provided.
- [x] PASS: Skill requires a short answer at the top that resolves the issue without requiring the user to read the full article — the "Short answer" section mandates "1-2 sentences that directly answer the question... a user who reads only this sentence should get the core answer."
- [x] PASS: Skill produces step-by-step instructions where applicable — the "Step-by-step instructions" section mandates numbered steps with a strict format: action verb, exact UI location, expected result.
- [x] PASS: Skill requires a troubleshooting section covering variations of the problem — the "Troubleshooting" section is mandatory and requires the most common error, user mistake, and environment differences.
- [x] PASS: Skill is written to deflect repeat support tickets — maintenance rules include "helpfulness tracking" (views vs. tickets), the quality checklist includes "Testable" and "Error-path covered", and the skill explicitly links back to ticket triage.
- [x] PASS (full): Skill requires the article to be tested against the original ticket language — Step 2 "Title" says: "If you have access to source tickets, validate the title and short answer against the actual phrasing customers use... Pull at least two ticket subject lines and confirm the title would be a plausible search query." Full credit awarded; criterion exceeds PARTIAL bar.
- [x] PASS: Skill requires related articles or next steps at the end — the "Related articles" section is mandatory and specifies grouping by Next steps, Related topics, and Background.
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter at lines 1–7 includes all three required fields.

### Output expectations

- [x] PASS: Output title is phrased as a user-search question — "Why do my exports fail when I try to download large datasets?" matches customer vocabulary, not internal terminology.
- [x] PASS: Output's first paragraph tells the user the fix in 1-3 sentences without requiring them to read further — "Use date-range filtering to split the export into smaller batches" is the core answer up front.
- [x] PASS: Step-by-step instructions are numbered with concrete actions — 5 numbered steps, each with an exact UI path and expected result.
- [x] PASS: Troubleshooting covers four variations — date filter still fails, empty file, file won't open, export button missing.
- [x] PASS: Article deflects support contact — ends with an explicit "if this didn't help, contact support with X/Y/Z details" section.
- [x] PASS: Output uses ticket language — "exports fail", "large datasets" phrasing rather than "export limitation documentation."
- [x] PASS: Output addresses the WHY — the 30-second timeout constraint is explained immediately after the short answer.
- [x] PASS: Related articles cover adjacent topics — scheduled exports, API access, filtering/sorting, combining CSVs, dashboard refresh.
- [x] PASS: Output addresses the at-scale customer — "When this workaround isn't enough" section explicitly calls out date-range splitting as a band-aid and points to scheduled exports and API access.
- [~] PARTIAL: Output uses screenshots or visual references — one screenshot placeholder is included for the Date Range button. Steps 1, 3, 4, and 5 omit placeholders despite involving non-obvious UI elements. Skill requires flagging all non-obvious elements; only partial coverage here.

## Notes

The skill definition is genuinely strong. Every output expectation maps directly to an explicit requirement, not implied behaviour. The "When the answer is a workaround" section is the standout feature — it forces the author to address the power-user case that most KB skill definitions leave out entirely.

The PARTIAL criterion on ticket-language matching is fully met: the skill goes beyond requiring plain language to mandate pulling two ticket subject lines and validating the title against them.

One gap worth flagging for improvement: the skill says to add screenshot placeholders for "non-obvious" UI elements but doesn't define non-obvious or require a systematic visual audit pass. In practice this leads to uneven placeholder coverage, as shown in the simulated output. A stronger version would require a post-draft pass: "for every step, ask whether a first-time user could locate the UI element from the description alone. If not, add a placeholder."
