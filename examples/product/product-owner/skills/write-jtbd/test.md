# Test: Write JTBD

Scenario: Testing whether the write-jtbd skill definition requires functional, emotional, and social job statements, an outcome table with opportunity scoring, and hiring/firing criteria.

## Prompt


/product-owner:write-jtbd for the reporting and analytics area of our project management tool, focusing on how operations directors use our data.

## Criteria


- [ ] PASS: Skill requires a core functional job statement in the canonical format: "When I [situation], I want to [motivation], so I can [outcome]"
- [ ] PASS: Skill requires emotional jobs (how the performer wants to feel) AND social jobs (how they want to be perceived) — not just functional jobs
- [ ] PASS: Skill requires an outcome table with Importance, Current Satisfaction, and Opportunity Score columns
- [ ] PASS: Skill defines the Opportunity Score formula: Importance + max(Importance - Satisfaction, 0), with thresholds for underserved (>12) and overserved (<6)
- [ ] PASS: Skill requires hiring and firing criteria — what causes someone to switch TO and AWAY from the product
- [ ] PASS: Skill prohibits solution-specific job statements — "I want to use the dashboard" is explicitly called out as wrong
- [ ] PARTIAL: Skill requires at least 8 outcome statements for the core job — partial credit if outcomes are required but minimum count is not specified
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
