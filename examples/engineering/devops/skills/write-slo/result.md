# Write slo skill structure

Checking that the write-slo skill produces a complete SLO document grounded in Google SRE practices — measurable SLIs, calculated error budgets, a policy with teeth (feature freeze), and burn-rate-based alerting.

## Prompt

> Review the write-slo skill definition and verify it produces SLO definitions that reflect user experience rather than infrastructure uptime, with actionable error budget policies.

Given the prompt "define SLOs for a payment processing API", the skill would produce a six-section document: service profile (including "what 'down' means to users"), SLI table (availability, latency, correctness — each with good/bad event definitions and measurement method), SLO targets with rolling 30-day windows and error budgets calculated, error budget policy with all four threshold states, alerting table with fast burn (page) and slow burn (ticket) tiers, and review cadence with quarterly recalibration criteria.

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill requires service profile identifying "down" from user perspective — Step 1 service profile template includes "What 'down' means to users" as a required row. Rules: "Define 'down' from the user's perspective, not the infrastructure's. A database failover that takes 30 seconds is invisible to users if requests are retried — that's not downtime. A 200ms latency spike that causes timeouts in a calling service IS downtime for that service's users."

- [x] PASS: Skill defines SLIs as good/bad event ratios and prohibits infrastructure metrics — Step 2 SLI table has "Good event definition" and "Bad event definition" columns alongside "Measurement method". Rules: "Server CPU utilisation is not an SLI — it's an implementation detail. 'Requests served successfully' is an SLI."

- [x] PASS: Skill requires rolling windows and provides error budget reference table — Step 3 SLO template uses "rolling 30 days" as the measurement window. Rules: "Use rolling windows, not calendar months." Error budget reference table is provided with six rows (99% through 99.999%) showing downtime per year, month, and week.

- [x] PASS: Skill includes achievable SLO rule — Step 3 rules: "SLOs must be achievable. Setting 99.99% when your current reliability is 99.5% is aspirational fiction. Set the target above current performance but within reach." The exact numbers from the criterion appear verbatim.

- [x] PASS: Skill defines error budget policy with all four states and feature freeze — Step 4 defines: healthy (> 50%), depleting (25–50%), critical (< 25%), exhausted (0% remaining). The exhausted state specifies: "Feature freeze — only reliability improvements and critical security fixes deploy."

- [x] PASS: Skill requires burn rate alerting with fast/slow tiers — Step 5 defines "Fast burn alerts (page — immediate response required)" and "Slow burn alerts (ticket — investigate within business hours)". Rules: "Alert on burn rate, not on raw thresholds. A brief spike that consumes 0.01% of the error budget should not page anyone."

- [x] PASS: Skill requires named owner, not a team — Rules section: "Every SLO needs an owner. A single person accountable for the error budget. Not a team, not a Slack channel — a person." Step 4 template shows "Error budget owner: [name/role — single person accountable]."

- [~] PARTIAL: Skill defines review cadence with tightening/relaxing criteria — Step 6 provides a review cadence table (weekly, monthly, quarterly) and explicit "Criteria for tightening SLOs" and "Criteria for relaxing SLOs" subsections with specific observable conditions. The content fully satisfies the criterion, but PARTIAL-prefixed criteria are capped at 0.5 regardless.

## Notes

The tightening/relaxing criteria in Step 6 are specific and data-driven: tighten when "Error budget consistently unspent (> 80% remaining at end of window for 3+ months)" or "Users complaining about reliability despite SLO being met." Relax when "Error budget consistently exhausted despite reasonable engineering investment." These are real decision signals, not placeholders. The PARTIAL score reflects the criterion prefix constraint, not a gap in the definition.
