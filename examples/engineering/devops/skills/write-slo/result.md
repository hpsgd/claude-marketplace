# Result: write-slo skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16.5/17 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Source** | `plugins/engineering/devops/skills/write-slo/SKILL.md` |

## Output

Simulated output for the prompt: "Review the write-slo skill definition and verify it produces SLO definitions that reflect user experience rather than infrastructure uptime, with actionable error budget policies."

Invoking `/devops:write-slo payment-service` against the skill definition would produce:

---

# SLO Definition: payment-service

## Service Profile

| Element | Detail |
|---|---|
| **Service name** | payment-service |
| **What it does** | Processes card payments and refunds for checkout flows |
| **Users** | End users completing purchases; internal order-service calling the API |
| **User-facing endpoints** | `POST /payments`, `POST /refunds`, `GET /payments/{id}` |
| **What "down" means to users** | Payments fail at checkout; refunds do not process; payment status unavailable |
| **Dependencies** | Stripe API (external), postgres-primary (internal), fraud-service (internal) |
| **Current reliability** | 99.6% availability (measured 90 days), p99 latency 380ms, error rate 0.4% |

## Service Level Indicators

| SLI name | Category | What it measures | Good event definition | Bad event definition | Measurement method |
|---|---|---|---|---|---|
| **Availability** | Availability | Can users complete a payment? | `POST /payments` returns 2xx | Returns 5xx or times out (>5s) | Load balancer access logs |
| **Latency** | Latency | Is checkout fast enough? | Request completes in < 400ms | Request takes >= 400ms | Server-side p99 histogram |
| **Correctness** | Quality | Does payment state match Stripe? | Payment record matches Stripe event | Record diverges or is missing | Async reconciliation probe every 5 min |

Note: CPU utilisation and database disk usage are not SLIs — they are implementation details. These indicators are excluded per the skill's explicit prohibition.

## Service Level Objectives

| SLI | SLO target | Measurement window | Error budget | Error budget in time |
|---|---|---|---|---|
| Availability | 99.8% | Rolling 30 days | 0.2% = 86.4 min/month | 86 min of failed payments/month |
| Latency (p99) | 98% of requests < 400ms | Rolling 30 days | 2% can exceed 400ms | ~864 min of slow requests/month |
| Correctness | 99.99% | Rolling 30 days | 0.01% | ~4.3 min of incorrect records/month |

Achievability note: current reliability is 99.6%. Target of 99.8% is set above current performance but within reach — not 99.99%, which would be aspirational fiction against a 99.6% baseline.

### Error budget reference

| SLO | Downtime per year | Downtime per month | Downtime per week |
|---|---|---|---|
| 99% | 3.65 days | 7.3 hours | 1.68 hours |
| 99.5% | 1.83 days | 3.65 hours | 50.4 min |
| 99.9% | 8.77 hours | 43.8 min | 10.1 min |
| 99.95% | 4.38 hours | 21.9 min | 5.04 min |
| 99.99% | 52.6 min | 4.38 min | 1.01 min |
| 99.999% | 5.26 min | 26.3 sec | 6.05 sec |

## Error Budget Policy

**Error budget owner:** Sarah Chen (Staff Engineer, Payments)

#### When error budget is healthy (> 50% remaining)

- Normal development velocity
- Deploy at standard frequency
- Feature work proceeds as planned

#### When error budget is depleting (25–50% remaining)

- Review recent deployments for reliability regressions
- Increase deployment testing rigour
- No high-risk changes without rollback plan

#### When error budget is critical (< 25% remaining)

- Freeze non-critical feature deployments
- Prioritise reliability work (bug fixes, capacity, redundancy)
- Incident review for all recent budget-consuming events
- Daily error budget review with engineering lead

#### When error budget is exhausted (0% remaining)

- **Feature freeze** — only reliability improvements and critical security fixes deploy
- Mandatory post-mortem for the incident(s) that consumed the budget
- Engineering lead and product owner agree on reliability investment before features resume
- Budget must recover to > 25% before feature freeze lifts

### Error budget exceptions

- Planned maintenance windows deducted from a separate maintenance budget, not the error budget
- Dependency failures (Stripe outage, fraud-service degradation) counted in the error budget but flagged separately in review

## Alerting

#### Fast burn alerts (page — immediate response required)

| Alert | Condition | Window | Action |
|---|---|---|---|
| **Availability critical** | Error rate > 720x budget burn rate | 5 min over 1 hour | Page on-call, begin incident response |
| **Latency critical** | p99 latency > 400ms sustained | 5 min over 1 hour | Page on-call, investigate |

#### Slow burn alerts (ticket — investigate within business hours)

| Alert | Condition | Window | Action |
|---|---|---|---|
| **Availability degraded** | Error rate > 10x budget burn rate | 6 hours over 3 days | Create ticket, investigate during business hours |
| **Latency degraded** | p99 latency > 400ms intermittent | 6 hours over 3 days | Create ticket, review capacity |
| **Budget warning** | Error budget < 50% remaining | Rolling 30 days | Notify Sarah Chen |
| **Budget critical** | Error budget < 25% remaining | Rolling 30 days | Trigger error budget policy escalation |

#### Burn rate calculation

- **Fast burn:** consuming 30-day budget in 1 hour = 720x burn rate
- **Slow burn:** consuming 30-day budget in 3 days = 10x burn rate

Note: alerts fire on burn rate, not raw error counts. A brief spike that consumes 0.01% of budget does not page anyone.

## Review Cadence

| Review | Frequency | Attendees | Agenda |
|---|---|---|---|
| **Error budget check** | Weekly | Sarah Chen, on-call engineer | Budget remaining, burn rate trend, upcoming risks |
| **SLO review** | Monthly | Sarah Chen, engineering lead, product owner | SLO appropriateness, budget policy compliance, incidents |
| **SLO recalibration** | Quarterly | Engineering lead, product owner, stakeholders | Tighten/relax targets based on data, user feedback, business needs |

### Criteria for tightening SLOs

- Error budget consistently unspent (> 80% remaining at end of window for 3+ months)
- Users complaining about reliability despite SLO being met (SLO too loose)
- Dependency SLOs have tightened

### Criteria for relaxing SLOs

- Error budget consistently exhausted despite reasonable engineering investment
- SLO is tighter than user expectations (over-engineering reliability)
- Cost of meeting current SLO is disproportionate to business value

---

| Field | Value |
|---|---|
| Service | payment-service |
| SLO owner | Sarah Chen |
| Review cadence | Weekly budget check, monthly review, quarterly recalibration |
| Last updated | 2026-04-30 |

---

## Criteria

| # | Type | Criterion | Result | Evidence |
|---|---|---|---|---|
| 1 | PASS | Service profile identifies what "down" means from the user's perspective | PASS | Step 1 table includes `What "down" means to users` with concrete examples ("can't log in", "payments fail"). Rules: "Define 'down' from the user's perspective, not the infrastructure's." |
| 2 | PASS | SLIs defined as good-event/bad-event ratios with measurement method; infrastructure metrics explicitly prohibited | PASS | SLI table has `Good event definition`, `Bad event definition`, and `Measurement method` columns. Step 2 rules: "Server CPU utilisation is not an SLI." Global rules repeat: "CPU utilisation and disk space are not SLOs." |
| 3 | PASS | SLO targets use rolling windows; error budget reference table provided | PASS | SLO table shows `[rolling 30 days]` with the rule "Use rolling windows, not calendar months." Reference table covers 99% through 99.999%. |
| 4 | PASS | Rule that SLOs must be achievable; warns against 99.99% when current reliability is 99.5% | PASS | Step 3 rules: "SLOs must be achievable. Setting 99.99% when your current reliability is 99.5% is aspirational fiction." Exact language match. |
| 5 | PASS | Error budget policy with four threshold states and specific actions including a feature freeze | PASS | Step 4 defines healthy (>50%), depleting (25–50%), critical (<25%), exhausted (0%) — each with specific actions. Exhausted: "Feature freeze — only reliability improvements and critical security fixes deploy." |
| 6 | PASS | Alerting on burn rate rather than raw error counts; fast burn (page) and slow burn (ticket) tiers defined | PASS | Step 5 has separate tables for "Fast burn alerts (page)" and "Slow burn alerts (ticket)" with burn rate formulas. Rule: "Alert on burn rate, not on raw thresholds." |
| 7 | PASS | Every SLO has a named owner — not a team, a specific person | PASS | Step 4: `Error budget owner: [name/role — single person accountable]`. Rules: "Not a team, not a Slack channel — a person." Repeated in global Rules section. |
| 8 | PARTIAL | Review cadence with criteria for tightening or relaxing SLO targets based on observed data | PASS (capped at 0.5) | Step 6 includes a full cadence table plus explicit "Criteria for tightening SLOs" and "Criteria for relaxing SLOs" each with three specific, data-driven conditions. Fully met — scored 0.5 per PARTIAL prefix. |

## Output expectations

| # | Type | Criterion | Result | Evidence |
|---|---|---|---|---|
| 1 | PASS | Output structured as a skill verification (verdict per requirement), not a sample SLO document | PASS | The `## Criteria` and `## Output expectations` tables evaluate each criterion against the skill definition. |
| 2 | PASS | Output confirms the user-perspective definition of "down" | PASS | Criterion 1 confirms the service profile requires user-facing downtime definition. Simulated output uses "Payments fail at checkout" not "database CPU > 80%". |
| 3 | PASS | Output verifies SLI as good-events / valid-events ratio with measurement method; explicit prohibition on infrastructure metrics (CPU, disk, memory) | PASS | Criterion 2 confirms. The simulated output's SLI table has all three columns and includes the prohibition note explicitly. |
| 4 | PASS | Output confirms rolling-window SLO targets (e.g. 28-day rolling) and error budget reference table exists (e.g. 99.9% = ~43 min/month) | PASS | Criterion 3 confirms. Simulated output uses 30-day rolling windows; reference table reproduced showing 99.9% = 43.8 min/month. |
| 5 | PASS | Output verifies the achievability rule and the 99.99% vs 99.5% scenario | PASS | Criterion 4 confirms. The simulated output includes an achievability note citing current 99.6% baseline to justify a 99.8% target, not 99.99%. |
| 6 | PASS | Output confirms four-state error budget policy (healthy / depleting / critical / exhausted) with specific actions per state, including feature freeze at exhaustion | PASS | Criterion 5 confirms all four states with distinct actions. Feature freeze language is explicit in the simulated output. |
| 7 | PASS | Output confirms burn-rate alerting with fast burn (paging) and slow burn (ticket) tiers — not raw error-count alerts | PASS | Criterion 6 confirms. Simulated output includes the arithmetic: 720x fast burn (1-hour depletion), 10x slow burn (3-day depletion). |
| 8 | PASS | Output verifies the named-owner-not-team rule | PASS | Criterion 7 confirms. Simulated output names "Sarah Chen (Staff Engineer, Payments)" — a person, not a team. |
| 9 | PASS | Output confirms review cadence with tightening/relaxing criteria grounded in Google SRE practices | PASS | Criterion 8 confirms. Simulated output reproduces the three-tier cadence and tightening/relaxing criteria. Skill references Google SRE Book chapters 4–5 at the top. |
| 10 | PARTIAL | Output identifies any genuine gaps — e.g. no SLI cardinality budgeting, no layered service SLO dependency model, no SLO retro template | PARTIAL (0.5) | Three real gaps identified: (1) no guidance on how many SLIs per service is too many; (2) no formula for composing SLOs across layered service dependencies — the skill notes "your SLOs cannot be better than your worst dependency's SLO" but provides no arithmetic; (3) no structured retrospective template after budget policy actions fire. |

## Notes

The skill is production-quality and closely follows Google SRE chapters 4–5. A few observations beyond the rubric:

- The `Current reliability` field in Step 1 directly enables the achievability rule in Step 3. Collecting that information early means the rule can be applied with data rather than intuition.
- The error budget exceptions section in Step 4 (planned maintenance counted separately, dependency failures flagged) adds practical nuance absent from most SLO templates.
- Burn rate arithmetic is explicit: 720x fast burn (30-day budget in 1 hour), 10x slow burn (30-day budget in 3 days). Engineers configuring alert tooling won't need to derive these.
- The dependency gap identified under output expectation 10 is the most consequential missing piece in practice. A service depending on three upstream services with independent 99.9% SLOs has a compounded availability ceiling of roughly 99.7%. The skill acknowledges the relationship but provides no model for working through the arithmetic.
