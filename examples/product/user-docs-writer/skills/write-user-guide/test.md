# Test: Write user guide

Scenario: Testing whether the write-user-guide skill requires a research step, numbered steps with expected results, and a troubleshooting section for the feature.

## Prompt


/user-docs-writer:write-user-guide for our time tracking feature — users can log time against projects and tasks, set estimates, and view utilisation reports.

A few specifics for the response:

- Begin with a short **Research** subsection listing what you would consult before writing — feature spec, existing support tickets, prior product docs. State the assumptions you're making in lieu of those (e.g. "no spec available; assuming standard time-entry model"). Don't start cold.
- Include a footer YAML-style metadata block (or markdown table) listing: `name:`, `description:`, `argument-hint:`, `category:`, `tags:` so the article can be ingested by a docs system.

## Criteria


- [ ] PASS: Skill requires a research step — reading existing feature specs, support tickets, or product docs before writing
- [ ] PASS: Skill produces numbered steps for procedural tasks — not bullet points
- [ ] PASS: Each step includes what the user should see after completing it — confirmation of success
- [ ] PASS: Skill requires a troubleshooting section covering the most common problems users face with this feature
- [ ] PASS: Skill uses only product terminology — no technical language without plain-English explanation
- [ ] PASS: Skill requires related content links at the end — connecting users to adjacent features or prerequisite knowledge
- [ ] PARTIAL: Skill requires role-based or permissions context — noting when certain actions require admin access — partial credit if permissions are mentioned but not required as a standard documentation element
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
