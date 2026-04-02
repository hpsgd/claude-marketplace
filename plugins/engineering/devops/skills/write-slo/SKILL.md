---
name: write-slo
description: "Define Service Level Objectives (SLOs) for a service -- SLIs, SLO targets, error budgets, and alerting policy. Produces a structured SLO document based on Google SRE practices. Use when a service enters production or when formalising reliability targets."
argument-hint: "[service name or endpoint to define SLOs for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write SLO Definition

Define Service Level Objectives for $ARGUMENTS. SLOs express reliability targets from the user's perspective — not uptime dashboards, not infrastructure metrics, but "does the service work for the people who depend on it?"

Reference: [Google SRE Book](https://sre.google/sre-book/table-of-contents/) chapters 4-5.

## Step 1: Identify the service and its users (mandatory)

```markdown
### Service profile

| Element | Detail |
|---|---|
| **Service name** | [name] |
| **What it does** | [one sentence — what value it provides] |
| **Users** | [who depends on it — end users, internal services, both] |
| **User-facing endpoints** | [API endpoints, web pages, async jobs that users care about] |
| **What "down" means to users** | [specific — "can't log in", "payments fail", "dashboard shows stale data"] |
| **Dependencies** | [upstream services this depends on — their failures affect your SLOs] |
| **Current reliability** | [what do you know today — uptime %, error rate, latency p50/p99] |
```

**Rules for service identification:**
- Define "down" from the user's perspective, not the infrastructure's. A database failover that takes 30 seconds is invisible to users if requests are retried — that's not downtime. A 200ms latency spike that causes timeouts in a calling service IS downtime for that service's users
- List dependencies explicitly — your SLOs cannot be better than your worst dependency's SLO

**Output:** Service profile table.

## Step 2: Define SLIs (mandatory)

Define the Service Level Indicators — what you measure:

```markdown
### Service Level Indicators

| SLI name | Category | What it measures | Good event definition | Bad event definition | Measurement method |
|---|---|---|---|---|---|
| **Availability** | Availability | Can users reach the service? | Request returns non-5xx response | Request returns 5xx or times out | Server-side logs / load balancer metrics |
| **Latency** | Latency | Is the service fast enough? | Request completes in < [X]ms | Request takes >= [X]ms | Server-side histogram at p50, p95, p99 |
| **Correctness** | Quality | Does the service return right answers? | Response matches expected output | Response is incorrect or incomplete | End-to-end probes / data validation |
| **Freshness** | Quality | Is the data up to date? | Data updated within [X] minutes | Data older than [X] minutes | Timestamp comparison |
```

**Rules for SLIs:**
- SLIs must be measurable from the user's perspective. Server CPU utilisation is not an SLI — it's an implementation detail. "Requests served successfully" is an SLI
- Define good events, not bad events. An SLI is the ratio of good events to total events
- Not every service needs every SLI category. An async batch job needs freshness and correctness but not latency. A real-time API needs availability and latency
- Measurement method must already exist or be buildable. An SLI you can't measure is an aspiration, not an indicator

**Output:** SLI table with good/bad event definitions and measurement methods.

## Step 3: Set SLO targets (mandatory)

```markdown
### Service Level Objectives

| SLI | SLO target | Measurement window | Error budget | Error budget in time |
|---|---|---|---|---|
| Availability | [e.g. 99.9%] | [rolling 30 days] | [0.1% = 43.2 min/month] | [X min of downtime/month] |
| Latency (p99) | [e.g. 99% of requests < 200ms] | [rolling 30 days] | [1% can exceed 200ms] | [~432 min of slow requests/month] |
| Correctness | [e.g. 99.99%] | [rolling 30 days] | [0.01%] | [~4.3 min of incorrect results/month] |

### Error budget reference

| SLO | Downtime per year | Downtime per month | Downtime per week |
|---|---|---|---|
| 99% | 3.65 days | 7.3 hours | 1.68 hours |
| 99.5% | 1.83 days | 3.65 hours | 50.4 min |
| 99.9% | 8.77 hours | 43.8 min | 10.1 min |
| 99.95% | 4.38 hours | 21.9 min | 5.04 min |
| 99.99% | 52.6 min | 4.38 min | 1.01 min |
| 99.999% | 5.26 min | 26.3 sec | 6.05 sec |
```

**Rules for SLO targets:**
- Start conservative. 99.9% is harder than it sounds — that's 43 minutes of downtime per month. If you've never measured, start at 99.5% and tighten after you have data
- SLOs must be achievable. Setting 99.99% when your current reliability is 99.5% is aspirational fiction. Set the target above current performance but within reach
- Use rolling windows, not calendar months. A 30-day rolling window avoids the "we blew the budget on day 1 so the rest of the month doesn't matter" problem
- SLOs should be stricter than SLAs. If your SLA promises 99.9%, your SLO should be 99.95% — the gap gives you time to fix things before breaching the SLA

**Output:** SLO targets table with error budgets calculated.

## Step 4: Define error budget policy (mandatory)

```markdown
### Error budget policy

**Error budget owner:** [name/role — single person accountable]

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
- Dependency failures (upstream service outage) counted in the error budget but flagged separately in review
```

**Rules for error budget policy:**
- Error budgets are for spending, not hoarding. If you never spend your error budget, your SLO is too loose — tighten it
- The feature freeze when budget is exhausted is the teeth of the policy. Without consequences, SLOs are just dashboards
- Every error budget policy needs an owner — a specific person who is accountable, not a team

**Output:** Error budget policy with thresholds and actions.

## Step 5: Configure alerting (mandatory)

```markdown
### Alerting policy

#### Fast burn alerts (page — immediate response required)
| Alert | Condition | Window | Action |
|---|---|---|---|
| **Availability critical** | Error rate > [X]x budget burn rate | 5 min over 1 hour | Page on-call, begin incident response |
| **Latency critical** | p99 latency > [X]ms | 5 min over 1 hour | Page on-call, investigate |

#### Slow burn alerts (ticket — investigate within business hours)
| Alert | Condition | Window | Action |
|---|---|---|---|
| **Availability degraded** | Error rate > [X]x budget burn rate | 6 hours over 3 days | Create ticket, investigate during business hours |
| **Latency degraded** | p99 latency > [X]ms | 6 hours over 3 days | Create ticket, review capacity |
| **Budget warning** | Error budget < 50% remaining | Rolling 30 days | Notify engineering lead |
| **Budget critical** | Error budget < 25% remaining | Rolling 30 days | Trigger error budget policy escalation |

#### Burn rate calculation
- **Fast burn:** consuming 30-day budget in 1 hour = 720x burn rate
- **Slow burn:** consuming 30-day budget in 3 days = 10x burn rate
- Alert when actual burn rate exceeds threshold for the specified window
```

**Rules for alerting:**
- Alert on burn rate, not on raw thresholds. A brief spike that consumes 0.01% of the error budget should not page anyone. A sustained degradation that will exhaust the budget in 2 hours should
- Fast burn = page (someone wakes up). Slow burn = ticket (someone investigates tomorrow). Get this wrong and you get alert fatigue or missed incidents
- Every alert must have a defined action. An alert that fires with no playbook is just noise

**Output:** Alerting table with burn rate thresholds and actions.

## Step 6: Define review cadence (mandatory)

```markdown
### SLO review cadence

| Review | Frequency | Attendees | Agenda |
|---|---|---|---|
| **Error budget check** | Weekly | SLO owner, on-call engineer | Budget remaining, burn rate trend, upcoming risks |
| **SLO review** | Monthly | SLO owner, engineering lead, product owner | SLO appropriateness, budget policy compliance, incidents |
| **SLO recalibration** | Quarterly | Engineering lead, product owner, stakeholders | Tighten/relax targets based on data, user feedback, business needs |

### Criteria for tightening SLOs
- Error budget consistently unspent (> 80% remaining at end of window for 3+ months)
- Users complaining about reliability despite SLO being met (SLO too loose)
- Dependency SLOs have tightened

### Criteria for relaxing SLOs
- Error budget consistently exhausted despite reasonable engineering investment
- SLO is tighter than user expectations (over-engineering reliability)
- Cost of meeting current SLO is disproportionate to business value
```

**Output:** Review cadence table with tightening/relaxing criteria.

## Rules

- **SLOs should be set from the user's perspective, not the infrastructure's.** CPU utilisation and disk space are not SLOs. "Requests served successfully within 200ms" is an SLO.
- **Start conservative.** 99.9% is harder than it sounds — that's 8.7 hours of downtime per year. If you've never measured, start at 99.5% and earn your way to 99.9%.
- **Error budgets are for spending, not hoarding.** If you never consume error budget, you're either over-investing in reliability or your SLO is too loose. Tighten it.
- **Every SLO needs an owner.** A single person accountable for the error budget. Not a team, not a Slack channel — a person.
- **SLOs are not SLAs.** SLAs are contractual with financial consequences. SLOs are internal targets. Your SLO should be stricter than your SLA.
- **Alert on burn rate, not raw error counts.** A spike that consumes 0.01% of budget is not worth a page. A sustained burn that will exhaust the budget in hours is.

## Output Format

```markdown
# SLO Definition: [service name]

## Service Profile
[From Step 1]

## Service Level Indicators
[SLI table from Step 2]

## Service Level Objectives
[SLO targets and error budgets from Step 3]

## Error Budget Policy
[Policy with thresholds from Step 4]

## Alerting
[Alert configuration from Step 5]

## Review Cadence
[Review schedule from Step 6]

---
Service: [name]
SLO owner: [person]
Review cadence: Weekly budget check, monthly review, quarterly recalibration
Last updated: [date]
```

## Related Skills

- `/devops:incident-response` — incidents consume error budget. Every incident post-mortem should reference how much error budget was consumed and whether the budget policy was triggered.
- `/performance-engineer:capacity-plan` — capacity directly affects availability SLOs. Under-provisioned services will burn through error budget during traffic spikes.
