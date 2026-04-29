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

## Output expectations

- [ ] PASS: Output's claim inventory enumerates well over 10 atomic claims from the 4-week plan — including stated claims (Postgres set up Week 1, dual-writes Week 1, parity validated Week 2), implied claims (latency budget on dual-writes acceptable, no MySQL-specific stored proc behaviour breaks under translation, schema migration is reversible), and required claims (rollback path during cutover, pg replication keeping up with 2TB history)
- [ ] PASS: Output's steelman step strengthens the plan before attacking — adds a Week 0 staging dry-run, names the dual-write coordinator pattern (transactional outbox vs sync), specifies parity validation as percentage thresholds rather than vague "validate" — fixing trivial weaknesses before the real attack
- [ ] PASS: Output attacks the stored procedure rewrite specifically — 12 procs in 1 week is the team's stated risk, and the red-team flags it: are these procs in transactional hot paths, do they have edge-case behaviour that's hard to test, what's the test coverage on the existing procs
- [ ] PASS: Output attacks the dual-write latency assumption — at 2TB and 95 tables, every write becomes 2 writes; the latency budget on the synchronous-vs-async dual-write decision is interrogated, with the failure mode (Postgres latency dragging primary write performance) named
- [ ] PASS: Output attacks the parity validation — what does "data parity" mean concretely (row counts? hash-of-sorted-rows? checksum per partition?), what's the tolerance, what triggers a rollback if parity fails
- [ ] PASS: Output attacks the cutover step — Week 3 reads switch is the riskiest single moment; what happens if Postgres has a stale row from a missed dual-write, what's the rollback mechanism mid-week, what's the read-traffic ramp (canary % vs all-at-once)
- [ ] PASS: Output's findings are classified into critical weaknesses (could fail the migration), significant risks (likely to bite but recoverable), and unverified assumptions (need data before committing) — three separate tables
- [ ] PASS: Output's verdict uses one of the four ratings (Robust / Conditionally sound / Fragile / Fatally flawed) — given 4-week zero-downtime is aggressive for 2TB + 12 procs, "Conditionally sound" or "Fragile" is the honest verdict
- [ ] PASS: Output's verdict does NOT soften — if the plan is genuinely fragile (e.g. Week 4 decommission with no fallback if a problem surfaces post-cutover), the verdict says so and does not hedge with "should be fine in most cases"
- [ ] PASS: Output's weaknesses each include a direction for fixing — extend timeline, add canary cutover, add a staging full-rehearsal, hire a Postgres DBA, etc. — not just "this is risky"
