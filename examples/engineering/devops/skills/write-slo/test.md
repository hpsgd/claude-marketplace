# Test: write-slo skill produces a complete SLO document

Scenario: The DevOps engineer invokes the write-slo skill for a live API that currently has no formal reliability targets. The output should be a complete, Google SRE-grounded SLO document with measurable SLIs, a realistic SLO target, a four-state error budget policy, burn-rate alerting, and a review cadence.

## Prompt

/devops:write-slo for the Payments API — it processes Stripe charges and refunds for a B2B SaaS platform. Key facts: current error rate 0.08% over the last 30 days (measured at the load balancer); current p99 latency 340ms; on-call is currently paged on raw HTTP 5xx count spikes which produces 2–3 false alarms per week; the service has no formal SLO yet. "Down" for users means the payment button returns an error or the charge never appears in their billing dashboard.

## Criteria

- [ ] PASS: Service profile identifies what "down" means from the user's perspective — payment fails or times out for the customer making a purchase — not an infrastructure metric like server CPU or memory
- [ ] PASS: SLIs are defined as good-event/bad-event ratios with a measurement method — and infrastructure metrics (CPU, disk) are explicitly excluded
- [ ] PASS: SLO target is set with a rolling window (not calendar months) and includes an error budget reference table (e.g. 99.9% = ~43 min/month)
- [ ] PASS: SLO target is achievable given current reliability — does not aspirationally set 99.99% when the current measured error rate puts reliability at ~99.92%
- [ ] PASS: Error budget policy defines four threshold states (healthy, depleting, critical, exhausted) with specific actions at each, including a feature freeze at exhausted
- [ ] PASS: Alerting is configured on burn rate rather than raw error counts — fast burn tier (page) and slow burn tier (ticket) are both defined
- [ ] PASS: Every SLO has a named owner — a specific person or role, not a team name or Slack channel
- [ ] PARTIAL: Review cadence defines criteria for tightening or relaxing the SLO target based on observed data

## Output expectations

- [ ] PASS: Output's service profile table includes a "What 'down' means to users" row describing a customer-facing symptom (e.g. payment fails, charge does not appear in billing dashboard) — not an infrastructure state
- [ ] PASS: Output's SLI section defines availability as a ratio of good events to total events (e.g. non-5xx responses / total requests) with a named measurement method — and explicitly does not use CPU, disk, or memory as SLIs
- [ ] PASS: Output's SLO target uses a rolling window (28-day or 30-day) and includes an error budget reference table showing downtime allowance per year/month/week for common percentages
- [ ] PASS: Output's chosen SLO target is consistent with the current ~99.92% reliability (0.08% error rate) — a 99.9% target is appropriate; 99.99% would be flagged as aspirational fiction
- [ ] PASS: Output's error budget policy has all four states — healthy (>50% remaining), depleting (25–50%), critical (<25%), exhausted (0%) — with distinct named actions at each level, including a feature freeze at exhaustion
- [ ] PASS: Output's alerting section has a fast burn tier (paging condition, short window) and a slow burn tier (ticket condition, longer window) — not a single raw error-count threshold
- [ ] PASS: Output names a specific person or role (e.g. "Platform lead", "Sarah Chen") as SLO owner — not a team, a channel, or a mailing list
- [ ] PASS: Output includes a review cadence table with at least weekly budget check, monthly review, and quarterly recalibration — with explicit criteria for when to tighten or relax the target
- [ ] PARTIAL: Output flags the current raw-error-count on-call setup as an anti-pattern and notes it will be replaced by the burn-rate alerting defined in the document
