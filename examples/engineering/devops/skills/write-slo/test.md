# Test: write-slo skill structure

Scenario: Checking that the write-slo skill produces a complete SLO document grounded in Google SRE practices — measurable SLIs, calculated error budgets, a policy with teeth (feature freeze), and burn-rate-based alerting.

## Prompt

Review the write-slo skill definition and verify it produces SLO definitions that reflect user experience rather than infrastructure uptime, with actionable error budget policies.

## Criteria

- [ ] PASS: Skill requires a service profile identifying what "down" means from the user's perspective — not from the infrastructure's perspective
- [ ] PASS: Skill defines SLIs as good-event/bad-event ratios with a measurement method — and explicitly prohibits infrastructure metrics (CPU, disk) as SLIs
- [ ] PASS: Skill requires SLO targets to be set with rolling windows (not calendar months) and provides an error budget reference table
- [ ] PASS: Skill includes a rule that SLOs must be achievable — warns against setting 99.99% when current reliability is 99.5%
- [ ] PASS: Skill defines an error budget policy with four threshold states (healthy, depleting, critical, exhausted) and specific actions at each state including a feature freeze
- [ ] PASS: Skill requires alerting on burn rate rather than raw error counts — defines fast burn (page) and slow burn (ticket) tiers
- [ ] PASS: Skill requires every SLO to have a named owner — not a team, a specific person
- [ ] PARTIAL: Skill defines review cadence with criteria for tightening or relaxing SLO targets based on observed data

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample SLO document
- [ ] PASS: Output confirms the user-perspective definition of "down" — what the user experiences, not what infrastructure metric is red
- [ ] PASS: Output verifies SLI definition as good-events / valid-events ratio with measurement method, and the explicit prohibition on infrastructure metrics (CPU, disk, memory) as SLIs
- [ ] PASS: Output confirms rolling-window SLO targets (e.g. 28-day rolling) instead of calendar months, and that an error budget reference table exists (e.g. 99.9% = ~43 min/month)
- [ ] PASS: Output verifies the achievability rule and warns against setting 99.99% when current measured reliability is 99.5%
- [ ] PASS: Output confirms the four-state error budget policy (healthy / depleting / critical / exhausted) with specific actions per state, including a feature freeze at exhaustion
- [ ] PASS: Output confirms burn-rate alerting with two tiers — fast burn (paging) and slow burn (ticket) — not raw error-count alerts
- [ ] PASS: Output verifies the named-owner-not-team rule — every SLO has a single accountable person, not a generic team mailing list
- [ ] PASS: Output confirms a review cadence with criteria for tightening or relaxing targets based on observed data, and grounds the framework in Google SRE practices
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no rule on SLI cardinality budgeting, no documented dependency between layered service SLOs, or no template for an SLO retro after policy actions fire
