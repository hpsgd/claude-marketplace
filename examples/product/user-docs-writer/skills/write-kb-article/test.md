# Test: Write KB article

Scenario: Testing whether the write-kb-article skill requires a question-format title, short answer first, prerequisites, and a troubleshooting section.

## Prompt


/user-docs-writer:write-kb-article explaining how to connect a custom domain to a Clearpath workspace — users need to use their company's domain instead of the default clearpath.app subdomain.

## Criteria


- [ ] PASS: Skill requires the article title to be a question the user would actually ask — not a feature description
- [ ] PASS: Skill requires a short answer or summary at the top before the step-by-step instructions
- [ ] PASS: Skill requires a prerequisites section listing what the user needs before they start
- [ ] PASS: Skill requires a troubleshooting section covering common problems users encounter with this task
- [ ] PASS: Skill requires each step to describe both the action and what the user should see after — not just the action
- [ ] PASS: Skill uses only product terminology — no technical jargon without plain-language explanation
- [ ] PARTIAL: Skill requires metadata (category, tags, related articles) — partial credit if related articles are required but category/tag metadata is not
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
