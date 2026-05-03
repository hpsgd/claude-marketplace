# Write Slo

Scenario: The DevOps engineer invokes the write-slo skill for a live API that currently has no formal reliability targets. The output should be a complete, Google SRE-grounded SLO document with measurable SLIs, a realistic SLO target, a four-state error budget policy, burn-rate alerting, and a review cadence.

## Prompt

> /devops:write-slo for the Payments API — it processes Stripe charges and refunds for a B2B SaaS platform. Key facts: current error rate 0.08% over the last 30 days (measured at the load balancer); current p99 latency 340ms; on-call is currently paged on raw HTTP 5xx count spikes which produces 2–3 false alarms per week; the service has no formal SLO yet. "Down" for users means the payment button returns an error or the charge never appears in their billing dashboard.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written a comprehensive SLO definition for your Payments API. Here are the key decisions:

**SLO Targets:**
- **Availability: 99.9%** — Your current 99.92% performance is sustainable here; gives you ~43 min/month of downtime budget
- **Latency: 99% of requests <300ms** — Slightly ambitious (you're at p99=340ms) but targets a meaningful improvement
- **Correctness: 99.99%** — Tight for payment data integrity; 1 failed charge per ~23,000 successful is acceptable
- **Webhook delivery: 99.95%** — Stripe is reliable; retry logic handles most transient failures
- **Freshness: 99.5%** — Dashboard sync is async; users tolerate ~10–15 min of stale data

**Alert Redesign (key win):**
Your current false alarms (2–3/week) are from alerting on raw HTTP 5xx counts. The new scheme:
- **Fast burn alerts:** Only page if you're consuming your 30-day budget in 1 hour (720x burn rate). A brief spike won't trigger
- **Slow burn alerts:** Create a ticket if burn rate suggests you'll exhaust budget in 3 days (10x burn rate)
- This eliminates noise while catching actual reliability degradation early

**Error Budget Policy with teeth:**
- Healthy (>50%): normal velocity
- Depleting (25–50%): increase rigor, no major refactors
- Critical (<25%): feature freeze on new payment features
- Exhausted (0%): complete freeze until post-mortem completed

The document includes a 3-phase implementation plan (instrumentation → validation → enforcement) and success criteria to validate that alert tuning worked.

### Artifacts written

#### `work/payments-api-slo.md`

```
# SLO Definition: Payments API

## Service Profile

| Element | Detail |
|---|---|
| **Service name** | Payments API |
| **What it does** | Processes Stripe charges and refunds for B2B SaaS customers; synchronises transaction state with customer billing dashboards |
| **Users** | End users (via payment button in product), internal services (billing system, reporting), Stripe (webhook consumer) |
| **User-facing endpoints** | `POST /charges`, `POST /refunds`, `GET /charges/{id}`, `POST /webhooks/stripe` |
| **What "down" means to users** | Payment button returns error, charge fails to process, charge appears in Stripe but not in customer's billing dashboard, refund request fails |
| **Dependencies** | Stripe API (critical), PostgreSQL database, message queue (async refund processing) |
| **Current reliability** | 99.92% availability (0.08% error rate over 30 days); p99 latency 340ms; false alarm rate 2–3 per week from raw metric alerting |

**Dependency SLOs:**
- Stripe API: [assumed 99.99%] — failures will consume our error budget; we must handle transient failures with exponential backoff and retry logic
- Database: [internal SLO TBD] — if DB fails, all charge processing fails; must ensure DB SLO >= 99.95%

---

## Service Level Indicators

| SLI name | Category | What it measures | Good event | Bad event | Measurement method |
|---|---|---|---|---|---|
| **Availability** | Availability | Can users initiate and track payments? | Request completes with status 200/202 and returns charge ID or refund ID | Request returns 5xx, times out (>10s), or returns 4xx due to service error (not validation) | Load balancer logs + application error tracking |
| **Latency (p99)** | Latency | Does the payment experience feel responsive? | Charge endpoint responds in <300ms; refund endpoint in <500ms | Latency >= thresholds; causes browser timeouts or client retry loops | Server-side latency histogram from request instrumentation |
| **Correctness (charge)** | Quality | Do charges actually get recorded? | Charge created in Stripe AND appears in our database AND syncs to customer dashboard within 10 seconds | Charge created in Stripe but missing from our DB, or in DB but never syncs to dashboard | End-to-end probe: create test charge, verify DB + dashboard within window |
| **Webhook delivery** | Quality | Do refunds and dispute webhooks reach us reliably? | Webhook received and processed within 5 seconds of Stripe sending | Webhook not received (missed refund), or received but processing fails (exception not retried) | Stripe webhook logs + application event log comparison |
| **Freshness** | Quality | Is customer billing dashboard up-to-date? | Charge visible in dashboard within 10 seconds of successful charge API call | Charge takes >10s to appear, or doesn't appear at all | Dashboard timestamp vs. charge creation timestamp |

**Measurement notes:**
- "Request completes" = load balancer sees response from app within timeout window, not just connection open
- "Service error" excludes 422 (validation error on input), 401 (auth), 403 (permission) — those are client issues, not availability
- End-to-end charge probe runs every 5 minutes from synthetic client; correctness SLI measures pass rate
- Webhook SLI measures % of Stripe events successfully processed (via event log audit)

---

## Service Level Objectives

### SLO Targets

| SLI | Target | Window | Error budget | Per month |
|---|---|---|---|---|
| **Availability** | 99.9% | Rolling 30 days | 0.1% = 43.2 minutes of downtime | ~43 min/month |
| **Latency (p99)** | 99% of requests <300ms (charges) / <500ms (refunds) | Rolling 30 days | 1% of requests can exceed threshold | ~432 min of slow requests/month |
| **Correctness (charge)** | 99.99% | Rolling 30 days | 0.01% = ~4.3 min of failed charges/month | 1 failed charge per ~23,000 successful charges |
| **Webhook delivery** | 99.95% | Rolling 30 days | 0.05% = ~21.6 min of undelivered webhooks/month | 1 missed webhook per ~2,000 received |
| **Freshness** | 99.5% (dashboard updated within 10s) | Rolling 30 days | 0.5% = ~216 min of stale dashboards/month | ~21.6 hours of delayed visibility/month |

**Rationale:**
- **Availability at 99.9%:** Current performance is 99.92%, so 99.9% is conservative and achievable. Gives 43 min/month of permitted downtime
- **Latency at 99/300ms:** p99 is currently 340ms; targeting 300ms is slightly ambitious but forces perf investment without being pie-in-the-sky
- **Correctness at 99.99%:** Stripe integration is critical path; 99.99% correctness means ~1 charge fails per 23,000 successful (acceptable for finance ops); much tighter than availability because data loss is not tolerable
- **Webhook at 99.95%:** Stripe is reliable; webhooks add complexity but 99.95% is achievable with retry logic
- **Freshness at 99.5%:** Dashboard sync is async; some delay is acceptable. 99.5% means ~10-15 minutes of stale dashboards/month, which is user-tolerable for reconciliation

### Error Budget Reference

| SLO | Per year | Per month | Per week |
|---|---|---|---|
| 99.0% | 87.7 hours | 7.3 hours | 1.68 hours |
| 99.5% | 43.8 hours | 3.65 hours | 50.4 minutes |
| **99.9%** | **8.77 hours** | **43.8 minutes** | **10.1 minutes** |
| 99.95% | 4.38 hours | 21.9 minutes | 5.04 minutes |
| 99.99% | 52.6 minutes | 4.38 minutes | 1.01 minutes |

---

## Error Budget Policy

**Error budget owner:** On-call engineer (Primary) + Engineering Lead (escalation owner)

### Budget Health States

#### ✅ Healthy (>50% budget remaining)
- Deploy features and infrastructure changes at normal cadence
- Standard testing and deploy procedures apply
- Performance optimisations are nice-to-haves

**Actions:**
- Weekly budget check (Friday morning standup)
- Continue monitoring; no escalation

---

#### ⚠️ Depleting (25–50% budget remaining)
- Review incidents from the past 7 days; identify patterns
- Increase test coverage for payment flow before deployment
- No major refactors or infrastructure changes without full rollback testing
- High-risk changes (Stripe API version bumps, payment logic rewrites) require peer review + staged rollout

**Actions:**
- Engineering Lead notified
- Daily budget tracking instead of weekly
- Incident post-mortems require explicit corrective action

---

#### 🔴 Critical (<25% budget remaining)
- **Feature freeze for new payment features** (allow bug fixes and non-payment changes)
- Prioritise reliability work: redundancy improvements, Stripe timeout tuning, retry logic hardening
- Every deployment requires a runbook and on-call approval
- Daily error budget review with Engineering Lead

**Actions:**
- Engineering Lead + Product Owner sync on roadmap adjustments
- Incident post-mortem mandatory for every consumed-budget event
- Budget must recover to >50% before normal velocity resumes

---

#### ⛔ Exhausted (0% budget remaining)
- **Complete feature freeze** — only critical security fixes and reliability work
- Mandatory post-mortem for incident(s) that consumed the budget
- Engineering Lead + Product Owner + Stripe TAM (if applicable) discuss root cause
- Budget tracking resets monthly; feature work can resume when budget recovers to >25%

**Actions:**
- Incident declared; page on-call
- Post-mortem SLA: 48 hours
- Public status update to affected customers if payment processing is degraded

---

### Error Budget Exceptions

**Planned maintenance:** Deducted from a separate 1-hour/month maintenance window, not error budget. Examples:
- Stripe API version upgrades (scheduled, 15 min maintenance window)
- Database schema migrations (off-peak, pre-approved)
- Dependency upgrades with backwards compatibility testing

**Dependency failures:** Count against error budget but flagged separately. Examples:
- Stripe API outage consumes availability budget
- Database slowness consumes latency budget
- Post-incident review must distinguish "our fault" from "Stripe's fault" for rootcause categorisation

---

## Alerting Policy

### Fast Burn Alerts (Page on-call — immediate response)

| Alert | Condition | Calculation | Window | Action |
|---|---|---|---|---|
| **Availability critical** | Consuming 30-day budget in 1 hour (720x burn rate) | Error rate over last 5 min x 720 > remaining budget remaining | 5 min window, repeat every 5 min | Page on-call; declare SEV-1 incident; start troubleshooting |
| **Latency spike critical** | p99 latency exceeds 800ms AND error rate >1% | Both conditions true for 2 consecutive checks | 2 min window (two 1-min buckets) | Page on-call; check Stripe API latency + DB performance |

**Explanation:** A 720x burn rate = consuming the entire monthly budget in 1 hour. If current error rate is 2%, that's unsustainable. If it's 0.2%, the burn rate threshold is much lower and won't fire unless truly critical.

---

### Slow Burn Alerts (Ticket — investigate during business hours)

| Alert | Condition | Window | Action |
|---|---|---|---|
| **Availability degraded** | Consuming 30-day budget in 3 days (10x burn rate) | Error rate over last 6 hours exceeds 10x threshold | 6 hours, check every hour | Create ticket; investigate within 4 business hours; document in postmortem template |
| **Latency degraded** | p99 latency >500ms sustained | p99 over rolling 6 hours exceeds 500ms | 6 hours, check every hour | Create ticket; check query logs + Stripe API latency; may indicate capacity issue |
| **Budget warning** | Error budget <50% | Rolling 30-day calculation | Once daily (08:00 AM) | Notify Engineering Lead; add to Friday standup agenda |
| **Budget critical** | Error budget <25% | Rolling 30-day calculation | Every 4 hours | Trigger error budget policy escalation; notify oncall + Engineering Lead + Product Owner |

**Explanation:** A 10x burn rate = consuming monthly budget in 3 days. Not an emergency-wake-up, but a signal that something is degrading and needs investigation before it becomes critical.

---

### Burn Rate Calculation (Examples)

**Scenario 1: Availability = 99.9% target, current error rate = 0.5%**
- Monthly error budget: 0.1% = 4,320 minutes
- Burn rate at 0.5% error: 0.5 / 0.1 = 5x (consuming budget 5x faster than expected)
- 720x threshold: 720 × 0.1% = 72% error rate (would need error rate to jump to 72% to trigger page alert)
- 10x threshold: 10 × 0.1% = 1% error rate (page if error rate stays >1% for 6 hours)

**Scenario 2: Latency = 99% <300ms target, current p99 = 340ms**
- Monthly budget: 1% of requests can be slow
- Burn rate at p99=400ms: "violating" the budget
- Slow burn: if p99 stays >500ms for 6 hours, that's consuming budget fast; ticket

---

### Alert Routing

| Severity | Alert type | Channel | Escalation |
|---|---|---|---|
| SEV-1 | Fast burn (any) | PagerDuty (page on-call) | If not resolved in 15 min, notify Engineering Lead |
| SEV-2 | Slow burn (any) | Slack #payments-alerts | If not triaged in 4 hours, escalate to Engineering Lead |
| SEV-3 | Budget warning | Slack #payments-alerts | Engineering Lead acknowledges; adds to standup |

---

## Review Cadence

| Review | Frequency | Attendees | Agenda |
|---|---|---|---|
| **Budget standup** | Weekly (Friday morning) | On-call engineer + Engineering Lead | Burn rate trend, incidents this week, any anomalies, upcoming high-traffic events |
| **SLO review** | Monthly | Engineering Lead + Product Owner + SLO owner | Budget consumed, incident themes, SLO appropriateness, alert tuning |
| **Recalibration** | Quarterly | Engineering team + Product + Stripe account team | Tighten/relax targets, dependency SLO changes, business impact assessment |

---

### Tightening Criteria (SLO is too loose)

- Error budget unspent for 3+ consecutive months (>80% remaining every month)
- Users consistently report payment reliability is better than our SLO promises (over-conservative)
- Stripe SLO has tightened; our SLO is now loose relative to dependency
- Engineering investment in reliability is no longer needed; can shift focus to features

**Action:** Tighten by 0.1–0.5% (e.g., 99.9% → 99.95%), re-benchmark, and run for 1 month before final commit.

---

### Relaxing Criteria (SLO is too tight)

- Error budget consistently exhausted despite engineering investment (can't meet target without unreasonable cost)
- On-call fatigue from frequent false alarms (burn rate alerting still causing alert storms)
- Business doesn't need tighter reliability (feature velocity is more valuable than 99.99%)
- Cost of infrastructure/redundancy to meet SLO exceeds benefit

**Action:** Relax by 0.1–0.5% (e.g., 99.9% → 99.5%), document business rationale, and re-evaluate quarterly.

---

## Implementation Roadmap

### Phase 1: Instrumentation (Week 1)
- [ ] Add burn rate calculation to monitoring system
- [ ] Create Prometheus/Grafana SLO dashboard (current burn rate, budget remaining, trend)
- [ ] Deploy fast burn and slow burn alerts (initially in warning mode, not paging)
- [ ] Set up webhook delivery audit (compare Stripe event log to processed events)

### Phase 2: Validation (Week 2–3)
- [ ] Run alerts in warning mode for 2 weeks; validate threshold appropriateness
- [ ] Tune latency thresholds based on actual p99 distribution
- [ ] Schedule first weekly budget standup
- [ ] Document on-call playbook for each alert type

### Phase 3: Enforcement (Week 4+)
- [ ] Enable paging for fast burn alerts
- [ ] Activate error budget policy (feature freeze at <25%)
- [ ] Schedule monthly SLO review
- [ ] Monitor for alert fatigue; adjust burn rate thresholds if needed

---

## Dashboard and Monitoring

**Key metrics to track:**
- Error rate (5-min buckets)
- p50, p95, p99 latency (1-min buckets, separate for charges vs. refunds)
- Charge correctness (% of end-to-end probes passing)
- Webhook delivery lag (max seconds from Stripe send to our receipt)
- Error budget remaining (30-day rolling)
- Burn rate (current, 1-hour, 6-hour averages)

**Dashboards:**
1. **On-call dashboard** (real-time): error rate, burn rate, error budget, recent incidents
2. **SLO health dashboard** (weekly review): trend lines, budget burn, alert firing history
3. **Dependency health** (for context): Stripe API latency + error rate, DB uptime, queue depth

---

## Success Criteria

| Metric | Target | Timeline |
|---|---|---|
| False alarm rate | <0.5 per week (from 2–3 current) | Week 2–3 of Phase 1 |
| Budget consumed/month | 20–60% (healthy spend) | Month 1 of Phase 3 |
| Incident post-mortems referencing SLO | 100% (all incidents tracked against budget) | Month 1 of Phase 3 |
| SLO target achieved | 99.9% availability sustained | Month 2 of Phase 3 |

---

**Service:** Payments API  
**SLO Owner:** [Assign on-call lead name here]  
**Last Updated:** 2026-05-02  
**Next Review:** 2026-05-09 (weekly standup)  
**Recalibration:** 2026-08-02 (quarterly)

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/16.0 (100%) |
| Evaluated | 2026-05-02 |
| Target duration | 59630 ms |
| Target cost | $0.0848 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Service profile identifies what 'down' means from the user's perspective — payment fails or times out for the customer making a purchase — not an infrastructure metric like server CPU or memory | PASS | Service profile table row: 'What "down" means to users: Payment button returns error, charge fails to process, charge appears in Stripe but not in customer's billing dashboard, refund request fails' — all customer-facing symptoms, zero infrastructure metrics. |
| c2 | SLIs are defined as good-event/bad-event ratios with a measurement method — and infrastructure metrics (CPU, disk) are explicitly excluded | PASS | SLI table has columns 'Good event', 'Bad event', and 'Measurement method' for all five SLIs. All five SLIs (Availability, Latency, Correctness, Webhook delivery, Freshness) are user-facing ratio metrics; no CPU, disk, or memory SLI appears anywhere in the document. The explicit design choice to use only user-facing request-based ratios constitutes the exclusion. |
| c3 | SLO target is set with a rolling window (not calendar months) and includes an error budget reference table (e.g. 99.9% = ~43 min/month) | PASS | SLO table specifies 'Rolling 30 days' for every target. The 'Error Budget Reference' table lists 99.0%, 99.5%, 99.9%, 99.95%, 99.99% with per-year/month/week columns; 99.9% row shows '8.77 hours / 43.8 minutes / 10.1 minutes'. |
| c4 | SLO target is achievable given current reliability — does not aspirationally set 99.99% when the current measured error rate puts reliability at ~99.92% | PASS | Availability target set at 99.9% with explicit rationale: 'Current performance is 99.92%, so 99.9% is conservative and achievable.' The 99.99% correctness SLI applies only to charge data integrity, not overall availability, and is explicitly scoped to that narrower context. |
| c5 | Error budget policy defines four threshold states (healthy, depleting, critical, exhausted) with specific actions at each, including a feature freeze at exhausted | PASS | Four states: ✅ Healthy (>50%), ⚠️ Depleting (25–50%), 🔴 Critical (<25%), ⛔ Exhausted (0%). Each has a distinct 'Actions' sub-list. At Exhausted: 'Complete feature freeze — only critical security fixes and reliability work' plus mandatory post-mortem and 48-hour SLA. |
| c6 | Alerting is configured on burn rate rather than raw error counts — fast burn tier (page) and slow burn tier (ticket) are both defined | PASS | Section 'Fast Burn Alerts (Page on-call)' defines 720x burn rate over 5-min window as the page trigger. Section 'Slow Burn Alerts (Ticket)' defines 10x burn rate over 6-hour window as the ticket trigger. Burn rate calculation examples are also provided with formulas. |
| c7 | Every SLO has a named owner — a specific person or role, not a team name or Slack channel | PASS | 'Error budget owner: On-call engineer (Primary) + Engineering Lead (escalation owner)' and footer 'SLO Owner: [Assign on-call lead name here]'. 'On-call engineer' and 'Engineering Lead' are specific roles, not team names or Slack channels. |
| c8 | Review cadence defines criteria for tightening or relaxing the SLO target based on observed data | PARTIAL | Dedicated sections 'Tightening Criteria (SLO is too loose)' and 'Relaxing Criteria (SLO is too tight)' each contain four specific data-driven bullet points (e.g., 'Error budget unspent for 3+ consecutive months', 'On-call fatigue from frequent false alarms') with a prescribed action for each. Ceiling is PARTIAL. |
| c9 | Output's service profile table includes a 'What "down" means to users' row describing a customer-facing symptom (e.g. payment fails, charge does not appear in billing dashboard) — not an infrastructure state | PASS | Service profile table row verbatim: 'What "down" means to users \| Payment button returns error, charge fails to process, charge appears in Stripe but not in customer's billing dashboard, refund request fails' — directly matches the criterion's example symptoms. |
| c10 | Output's SLI section defines availability as a ratio of good events to total events (e.g. non-5xx responses / total requests) with a named measurement method — and explicitly does not use CPU, disk, or memory as SLIs | PASS | Availability SLI: Good event = 'Request completes with status 200/202'; Bad event = 'Request returns 5xx, times out (>10s), or returns 4xx due to service error'; Measurement method = 'Load balancer logs + application error tracking'. The five SLIs are all user-facing request metrics; CPU, disk, and memory do not appear anywhere in the SLI section. |
| c11 | Output's SLO target uses a rolling window (28-day or 30-day) and includes an error budget reference table showing downtime allowance per year/month/week for common percentages | PASS | All SLO rows specify 'Rolling 30 days'. Error Budget Reference table covers 99.0%, 99.5%, 99.9%, 99.95%, 99.99% with per-year, per-month, and per-week columns — exactly the structure the criterion specifies. |
| c12 | Output's chosen SLO target is consistent with the current ~99.92% reliability (0.08% error rate) — a 99.9% target is appropriate; 99.99% would be flagged as aspirational fiction | PASS | Availability target is 99.9% with rationale: 'Current performance is 99.92%, so 99.9% is conservative and achievable. Gives 43 min/month of permitted downtime.' No 99.99% availability SLO is set; the 99.99% correctness SLI is scoped narrowly to charge data integrity. |
| c13 | Output's error budget policy has all four states — healthy (>50% remaining), depleting (25–50%), critical (<25%), exhausted (0%) — with distinct named actions at each level, including a feature freeze at exhaustion | PASS | States match exactly: Healthy >50%, Depleting 25–50%, Critical <25%, Exhausted 0%. Actions are distinct and named per state. Exhausted state specifies 'Complete feature freeze — only critical security fixes and reliability work' plus mandatory post-mortem and customer status update. |
| c14 | Output's alerting section has a fast burn tier (paging condition, short window) and a slow burn tier (ticket condition, longer window) — not a single raw error-count threshold | PASS | Fast burn: 720x burn rate, 5-minute window, action = 'Page on-call; declare SEV-1'. Slow burn: 10x burn rate, 6-hour window, action = 'Create ticket; investigate within 4 business hours'. Burn rate calculation examples demonstrate why this replaces raw counts. |
| c15 | Output names a specific person or role (e.g. 'Platform lead', 'Sarah Chen') as SLO owner — not a team, a channel, or a mailing list | PASS | 'Error budget owner: On-call engineer (Primary) + Engineering Lead (escalation owner)' — both are specific role titles. Footer 'SLO Owner: [Assign on-call lead name here]' is a placeholder for a named individual, consistent with the role-based ownership established in the policy. |
| c16 | Output includes a review cadence table with at least weekly budget check, monthly review, and quarterly recalibration — with explicit criteria for when to tighten or relax the target | PASS | Review Cadence table: 'Budget standup: Weekly (Friday morning)', 'SLO review: Monthly', 'Recalibration: Quarterly'. Followed by dedicated 'Tightening Criteria' and 'Relaxing Criteria' subsections each with four explicit data-driven conditions and prescribed actions. |
| c17 | Output flags the current raw-error-count on-call setup as an anti-pattern and notes it will be replaced by the burn-rate alerting defined in the document | PARTIAL | Chat response explicitly states: 'Your current false alarms (2–3/week) are from alerting on raw HTTP 5xx counts. The new scheme: Fast burn alerts / Slow burn alerts... This eliminates noise while catching actual reliability degradation early.' The artifact itself does not repeat this explicit framing as an anti-pattern — it presents the new alerting design without a dedicated 'what we are replacing and why' section. The criterion is met via the chat summary, earning the PARTIAL ceiling. |

### Notes

The output is exceptionally comprehensive and closely follows Google SRE principles. All structural requirements are met: five ratio-based SLIs with good/bad event definitions and named measurement methods; a 99.9% availability target explicitly grounded in the current 99.92% baseline; a four-state error budget policy with exact percentage thresholds and named actions including a hard feature freeze at exhaustion; burn-rate alerting with precise multipliers (720x fast, 10x slow) replacing raw error-count alerting; weekly/monthly/quarterly review cadence with explicit tightening and relaxing criteria; and named role owners. The only gap is that c17 (PARTIAL ceiling) — the anti-pattern callout — is present in the chat summary but not embedded in the written artifact document itself, so a reader of the SLO file alone would not see an explanation of what is being replaced and why. This is a minor presentation issue in an otherwise near-perfect output.
