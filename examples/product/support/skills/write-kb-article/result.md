# Output: Write KB article (support)

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14/18 criteria met (77.8%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria (structural — skill definition)

- [x] PASS: Skill requires the article title to be a question the user would search — met: the Title section explicitly mandates "the question the user would type into a search bar" using "their vocabulary, not internal terminology," with good/bad examples
- [x] PASS: Skill requires a short answer at the top that resolves the issue without requiring the user to read the full article — met: Short Answer section requires "1-2 sentences that directly answer the question" that "must be self-contained — a user who reads only this sentence should get the core answer"
- [x] PASS: Skill produces step-by-step instructions where applicable — not prose explanations — met: Step-by-step instructions section mandates numbered steps with prescribed format (action verb, exact UI element names, expected result) and explicitly prohibits prose summaries
- [x] PASS: Skill requires a troubleshooting section covering variations of the problem — met: Troubleshooting section mandates Problem/Cause/Solution triples and explicitly requires coverage of environment variations (browser, mobile vs desktop, older version)
- [x] PASS: Skill is written to deflect repeat support tickets — met: Step 1 requires reading full ticket threads, quality rules include Testable check, and Related Skills section explicitly states "KB articles reduce ticket volume"
- [~] PARTIAL: Skill requires the article to be tested against original ticket language — partially met: user vocabulary over jargon is required throughout and Step 1 requires reading full ticket threads, but there is no explicit instruction to validate that title and summary match how users phrase the problem in tickets
- [x] PASS: Skill requires related articles or next steps at the end — met: Related articles section mandates 3-5 articles grouped into Next steps, Related topics, and Background categories
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — met: frontmatter contains all three required fields

### Output expectations (behavioural — would the skill produce the right article?)

- [x] PASS: Output's title is phrased as a user-search question — the skill's Title section with good/bad examples would produce "Why do my exports fail for large datasets?" rather than "Export Limitations"; the prompt provides ticket language that maps directly to this
- [x] PASS: Output's first paragraph tells the user the fix in 1-3 sentences — the Short Answer section's rules ("1-2 sentences", "must be self-contained") would produce the direct fix without requiring the full article to be read
- [x] PASS: Output's step-by-step instructions are numbered with concrete actions — the prescribed step format (action verb + UI element + expected result) would produce numbered steps; the prompt's answer ("use date range filtering to export in smaller batches") maps to concrete numbered actions
- [x] PASS: Output's troubleshooting section covers variations — the Troubleshooting section's requirement to cover errors, user mistakes, and environment differences would produce entries for "still fails with date filtering", "file is empty", and similar; the format enforces Problem/Cause/Solution triples
- [x] PASS: Output is written to deflect support contact — the quality rules (Testable, Error-path covered) and maintenance helpfulness tracking ("track article views vs. support tickets") establish this; the skill would produce a contact-support fallback with required detail
- [ ] FAIL: Output uses ticket language for the title and summary — the skill requires user vocabulary generally but has no mechanism to validate against actual ticket phrasing; an agent following this skill could produce "Large Dataset Export Limitations" and pass the skill's own checks
- [ ] FAIL: Output addresses the WHY briefly after the WHAT — the skill has no instruction to explain the underlying constraint (e.g. timeout duration); step format focuses on actions and expected results, not system behaviour explanation
- [x] PASS: Output's related-articles links cover adjacent topics — the Related articles section's Next steps / Related topics / Background grouping would produce adjacent topics like scheduled exports and API access; the skill prompts coverage of related features
- [ ] FAIL: Output addresses the at-scale customer — the skill has no instruction to escalate or point power users to API access or a support upgrade path; nothing in the step format or quality rules covers the "workaround vs. real solution" distinction
- [~] PARTIAL: Output uses screenshots or visual references — the skill specifies precise UI element names and navigation paths ("Go to **Settings** > **Team** > **Permissions**") but has no instruction to include screenshots or visual callouts; the step format would produce text-only steps

## Notes

The skill is strong on structure and prescription. The step format is unusually specific — action verb, exact UI element, expected result — which closes the gap between "write something" and "write something testable." The maintenance section (90-day freshness, views vs. ticket tracking) is genuinely useful and goes beyond the rubric.

The three output failures share a pattern: the skill tells agents how to format articles but not how to reason about user needs beyond basic vocabulary. It has no instruction to explain system constraints (WHY exports time out), no escalation path for users who can't work around the limitation, and no validation loop against ticket language. These are the gaps between a well-formatted article and one that actually reduces repeat contacts.
