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
