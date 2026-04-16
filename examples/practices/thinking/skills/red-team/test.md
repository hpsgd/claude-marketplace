# Test: red-team migration plan attack

Scenario: An engineering team has decided to migrate their MySQL database to PostgreSQL over a 4-week window with zero downtime. They want the plan stress-tested before they start.

## Prompt

/red-team Our plan: migrate from MySQL to PostgreSQL in 4 weeks with zero downtime. Week 1 — set up Postgres and run dual-writes. Week 2 — validate data parity. Week 3 — cut reads over to Postgres. Week 4 — cut writes and decommission MySQL. We have 2TB of data, 95 tables, 12 stored procedures. Main risk we've identified is the stored procedure rewrite.

## Criteria

- [ ] PASS: Step 1 decomposes the plan into a claim inventory with stated, implied, and required claims — a 4-week plan should yield well above 10 atomic claims
- [ ] PASS: Step 2 steelmans the plan by building its strongest version before attacking — fixes obvious weaknesses before the attack
- [ ] PASS: Step 3 attacks each claim with the required structure — disproof test, failure conditions, weakest link, unverified assumption, strongest opposition
- [ ] PASS: Findings are classified by severity — critical weaknesses, significant risks, and unverified assumptions in separate tables
- [ ] PASS: Implied and required claims receive specific attack — not just the stated claims (e.g., the implicit assumption that dual-write adds acceptable latency is attacked)
- [ ] PASS: Step 4 delivers a verdict using one of the four ratings (Robust/Conditionally sound/Fragile/Fatally flawed) with reasoning
- [ ] PASS: Every weakness in the verdict section comes with a direction for fixing it
- [ ] PARTIAL: Verdict does not soften if the plan is genuinely fragile — the skill's own rule is "never soften the verdict"
