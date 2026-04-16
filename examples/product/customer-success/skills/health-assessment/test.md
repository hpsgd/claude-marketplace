# Test: Health assessment

Scenario: Testing whether the health-assessment skill scores all 5 dimensions with correct weights, produces a composite health score, and recommends specific interventions rather than generic advice.

## Prompt


/customer-success:health-assessment for our top 15 enterprise accounts ahead of our quarterly CS team review — we need to know which accounts need immediate attention.

## Criteria


- [ ] PASS: Skill scores all 5 dimensions: Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%)
- [ ] PASS: Skill calculates a composite health score using the correct weighted formula — not an unweighted average
- [ ] PASS: Skill classifies accounts into health categories (e.g. Green/Yellow/Red or equivalent) with defined thresholds
- [ ] PASS: Skill requires identifying data sources for each dimension before scoring — not scoring from memory
- [ ] PASS: Skill identifies specific risk signals per account — not just a score, but what is driving it
- [ ] PASS: Skill produces recommended interventions for at-risk accounts — specific actions, not "schedule a check-in"
- [ ] PARTIAL: Skill produces a portfolio summary view — partial credit if individual accounts are assessed but no aggregated portfolio view is required
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
