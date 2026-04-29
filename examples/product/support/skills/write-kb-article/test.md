# Test: Write KB article (support)

Scenario: Testing whether the support plugin's write-kb-article skill produces articles that resolve tickets and reduce repeat contacts, with a question-format title and troubleshooting section.

## Prompt


/support:write-kb-article about why exports fail for large datasets — we get 8-12 tickets a week about this and the answer is always the same: use date range filtering to export in smaller batches.

## Criteria


- [ ] PASS: Skill requires the article title to be a question the user would search — not a feature description or internal category
- [ ] PASS: Skill requires a short answer at the top that resolves the issue without requiring the user to read the full article
- [ ] PASS: Skill produces step-by-step instructions where applicable — not prose explanations of what to do
- [ ] PASS: Skill requires a troubleshooting section covering variations of the problem (e.g. export still fails after date filtering)
- [ ] PASS: Skill is written to deflect repeat support tickets — the article should make it unnecessary to contact support for this issue
- [ ] PARTIAL: Skill requires the article to be tested against the original ticket language — the title and summary should match how users describe the problem, not how support describes the solution — partial credit if plain language is required but ticket-language matching is not
- [ ] PASS: Skill requires related articles or next steps at the end
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's title is phrased as a user-search question — e.g. "Why do my exports fail for large datasets?" or "How do I export more than 10,000 rows?" — not "Export Limitations" or "Bulk Data Export Documentation"
- [ ] PASS: Output's first paragraph (the short answer) tells the user the fix in 1-3 sentences — "Exports time out for datasets over X rows. Use date-range filtering to export in smaller batches" — without requiring them to read the full article
- [ ] PASS: Output's step-by-step instructions are numbered with concrete actions — "1. Open the dashboard you want to export. 2. Click the date range filter. 3. Set a 1-month range. 4. Click Export." — not prose
- [ ] PASS: Output's troubleshooting section covers variations — "Export still fails with date filtering" → check column count, "Export works but file is empty" → check filter selection, "Export downloads but won't open" → file format / encoding issue
- [ ] PASS: Output is written to deflect support contact — at the end the user has both the fix AND the why, so they don't need to email support; the article includes "if this didn't help, contact support with X / Y / Z details"
- [ ] PASS: Output uses ticket language for the title and summary — phrasing matches how customers describe the problem ("export failing", "can't download", "stuck on loading"), not how support describes the solution
- [ ] PASS: Output addresses the WHY briefly after the WHAT — "exports time out at 30 seconds; large datasets need to fit in this window" — so users understand the constraint rather than just following instructions blindly
- [ ] PASS: Output's related-articles links cover adjacent topics — "Filtering and sorting your dashboards", "Scheduled exports for large reports", "API access for very large datasets" — so the user has next-step paths
- [ ] PASS: Output addresses the at-scale customer — for someone with consistently large datasets, the date-range workaround is a band-aid; the article points to API access or a support upgrade path
- [ ] PARTIAL: Output uses screenshots or visual references where applicable — e.g. "the date filter is in the top-right of the dashboard" with a note that screenshots are part of the article (even if just placeholders)
