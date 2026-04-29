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

## Output expectations

- [ ] PASS: Output assesses all 15 accounts — not a sample, not a "top movers" subset — with a row per account in the resulting table
- [ ] PASS: Output scores each account on all 5 dimensions — Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%) — and shows the per-dimension score per account
- [ ] PASS: Output computes the composite score using the WEIGHTED formula: Adoption*0.30 + Engagement*0.25 + Relationship*0.20 + Value*0.15 + Commercial*0.10 — not a simple average; the math is verifiable from the per-dimension scores
- [ ] PASS: Output classifies each account as Green / Yellow / Red (or equivalent ternary) with stated thresholds — e.g. ">=80 Green, 60-79 Yellow, <60 Red" — not just "looks healthy"
- [ ] PASS: Output names the data source per dimension before scoring — adoption from product analytics, engagement from in-app event tracking, relationship from CRM contact frequency, value from QBR notes, commercial from billing/contract data — not scoring from CSM memory
- [ ] PASS: Output identifies specific risk signals per at-risk account — not just "Score 55, Red" but "Adoption dropped 30% in last 60 days, no exec sponsor identified, support tickets ticked up to 12/month from 3"
- [ ] PASS: Output's recommended interventions per at-risk account are specific actions tied to the failing dimension — e.g. "Adoption red: schedule training session with team lead by Friday; Relationship red: identify backup champion within IT" — not "schedule a check-in"
- [ ] PASS: Output's portfolio summary view aggregates the 15 accounts — e.g. "3 Red, 4 Yellow, 8 Green; total ARR at risk: $X" — so the CS leadership team can prioritise meeting time
- [ ] PASS: Output prioritises the at-risk accounts for the upcoming review — listing Red accounts first with renewal dates, ARR, and the specific intervention required
- [ ] PARTIAL: Output flags trends across the portfolio — e.g. "adoption is the weakest dimension across the at-risk accounts, suggesting a systemic onboarding gap" — not just per-account observations
