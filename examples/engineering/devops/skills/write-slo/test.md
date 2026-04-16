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
