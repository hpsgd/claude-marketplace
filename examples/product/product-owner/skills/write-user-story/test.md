# Test: Write user story

Scenario: Testing whether the write-user-story skill definition produces stories in Gherkin format with proper acceptance criteria and ISC splitting guidance.

## Prompt


/product-owner:write-user-story for allowing users to export their data as a CSV file from the reporting dashboard.

## Criteria


- [ ] PASS: Skill requires Gherkin format (Given/When/Then) for acceptance criteria — not free-form bullet points
- [ ] PASS: Skill requires at least one edge case or error scenario in the acceptance criteria, not just the happy path
- [ ] PASS: Skill includes the ISC splitting test — Independent, Small, Complete — to verify stories are appropriately sized
- [ ] PASS: Skill requires the standard "As a [role], I want [action], so that [outcome]" story format
- [ ] PASS: Skill prohibits solution-specifying stories — acceptance criteria must describe behaviour, not implementation
- [ ] PARTIAL: Skill addresses anti-requirements (things the story explicitly should NOT do) — partial credit if mentioned but not required as a mandatory section
- [ ] PASS: Skill specifies that stories must have a single, clear acceptance condition — not "and/or" compound criteria
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
