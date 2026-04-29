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

## Output expectations

- [ ] PASS: Output's core functional job is in the canonical format — "When I [need to report status to my exec team], I want to [pull together a portfolio view across projects], so I can [communicate confidence and surface risks]" — solution-agnostic, not "use the dashboard"
- [ ] PASS: Output identifies the operations director as the JTBD performer (not generic "user") and describes their context — accountable for portfolio outcomes, weekly exec reporting, mid-market team without a PMO function
- [ ] PASS: Output produces emotional jobs (e.g. "I want to feel in control of project outcomes", "I want to feel I'm not blindsided by a project going red") and social jobs (e.g. "I want to be seen as the operations leader who has the answers", "I want to avoid being the person caught off-guard at the exec meeting") — both, not only functional
- [ ] PASS: Output's outcome table has at least 8 rows — desired outcomes the operations director cares about (e.g. "minimise time spent compiling status reports", "increase confidence in delivery dates", "reduce surprises in exec meetings") — with Importance, Current Satisfaction, and Opportunity Score columns
- [ ] PASS: Output's Opportunity Scores are computed via the formula `Importance + max(Importance - Satisfaction, 0)` — with the math shown — and outcomes scoring >12 are classified as underserved (opportunities), <6 as overserved
- [ ] PASS: Output's hiring criteria name what causes the operations director to switch TO Clearpath — e.g. "moved from Excel rollups when first tried Clearpath because exec summaries auto-generated saving 4 hours/week" — concrete, not "they want better reporting"
- [ ] PASS: Output's firing criteria name what causes operations directors to switch AWAY from Clearpath — e.g. "switched to Asana when exec audience required mobile dashboards we don't support"
- [ ] PASS: Output is solution-agnostic — every job and outcome describes the desired future state independent of the product, NOT "use the new analytics module"
- [ ] PASS: Output addresses the data dimension explicitly — operations directors care about data freshness, accuracy, ability to drill down, ability to export — these become outcomes
- [ ] PARTIAL: Output addresses team-level vs portfolio-level outcomes — operations directors operate at the portfolio (across teams) while team leads operate at the team level; the JTBD is portfolio-focused
