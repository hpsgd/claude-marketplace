# Test: Write integration guide

Scenario: Testing whether the write-integration-guide skill requires numbered steps with expected output, a complete runnable example, and a troubleshooting section.

## Prompt


/developer-docs-writer:write-integration-guide for connecting Clearpath to Salesforce — syncing deal status from Salesforce opportunities to Clearpath projects automatically.

## Criteria


- [ ] PASS: Skill requires numbered steps — not bullet points — so developers can follow sequentially and know exactly where they are
- [ ] PASS: Each step includes the expected output or visible result after completion, not just the action
- [ ] PASS: Skill requires a complete runnable end-to-end example that exercises the full integration
- [ ] PASS: Skill requires a troubleshooting section covering common failure modes with specific fixes
- [ ] PASS: Skill requires a prerequisites section before the integration steps begin
- [ ] PASS: Skill requires a research step — understanding both systems before writing the guide
- [ ] PARTIAL: Skill covers how to verify the integration is working correctly — partial credit if verification is embedded in steps but not a dedicated section
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
