---
name: capacity-plan
description: Create a capacity plan — analyse current load, project growth, calculate headroom, and recommend scaling actions.
argument-hint: "[system or service to plan capacity for]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Create a capacity plan for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Current Load Profile

Measure current traffic patterns. You cannot plan capacity without knowing current consumption.

| Metric | How to measure | What to capture |
|---|---|---|
| **Requests/sec** | APM, load balancer logs, application metrics | Average, peak, by endpoint |
| **Concurrent users** | Session count, WebSocket connections | Average, peak, by time of day |
| **Data volume** | Database size, storage metrics | Total size, growth rate per day/week |
| **Bandwidth** | Network metrics, CDN analytics | Inbound, outbound, by service |

**Capture patterns:**
- **Daily** — peak hours, quiet hours, ratio between them
- **Weekly** — weekday vs weekend patterns
- **Seasonal** — monthly trends, event-driven spikes (launches, campaigns, end-of-quarter)

### Step 2: Resource Utilisation Baseline

Measure resource consumption at current load. Target: **< 70% utilisation at normal load** — this leaves headroom for spikes.

| Resource | Current utilisation | Target | Headroom |
|---|---|---|---|
| **CPU** | [%] at normal, [%] at peak | < 70% normal, < 90% peak | [remaining %] |
| **Memory** | [GB] at normal, [GB] at peak | < 70% normal, < 85% peak | [remaining GB] |
| **Disk I/O** | [IOPS] at normal | < 60% provisioned IOPS | [remaining IOPS] |
| **Network** | [Mbps] at normal | < 50% bandwidth limit | [remaining Mbps] |
| **Connection pools** | [n] active / [n] max | < 70% pool size | [remaining connections] |
| **Storage** | [GB] used / [GB] provisioned | < 80% provisioned | [remaining GB, days until full] |

**Red flags:**
- Any resource > 70% at normal load — scaling is already overdue
- Any resource > 90% at peak — one anomalous spike away from failure
- Connection pool > 80% — pool exhaustion causes cascading failures

### Step 3: Growth Projection

| Growth model | When to use | How to calculate |
|---|---|---|
| **Linear** | Steady user acquisition, mature product | Current growth rate × time |
| **Exponential** | Viral growth, new market, post-launch | Compound growth rate, with a ceiling estimate |
| **Step function** | Sales-driven (enterprise customers), geographic expansion | Planned customer additions × per-customer load |
| **Seasonal** | E-commerce, education, tax/financial | Historical seasonal multiplier × base growth |

**Project forward:** 3 months, 6 months, 12 months. For each time horizon:
- Expected request volume
- Expected data volume
- Expected concurrent users
- Expected storage consumption

### Step 4: Breaking Point Identification

From stress test data (if available) or architectural analysis:

| Question | Answer |
|---|---|
| At what load does the system degrade? | [requests/sec or concurrent users] |
| What component fails first? | [database, application, cache, network, external API] |
| What is the failure mode? | [errors, latency spike, timeout, crash, data corruption] |
| How far is current peak from the breaking point? | [multiplier — e.g., "3.2x headroom"] |

If no stress test data exists, flag this as a critical gap. Capacity planning without knowing the breaking point is guesswork.

### Step 5: Headroom Calculation

Apply these models to translate between user-facing metrics and infrastructure capacity:

- **[Little's Law](https://en.wikipedia.org/wiki/Little%27s_law):** L = λ x W (concurrent users = arrival rate x average response time). Essential for translating between concurrent users and requests/second. If you expect 100 req/s and average response time is 200ms, you need capacity for 20 concurrent requests.
- **[Universal Scalability Law](https://www.perfdynamics.com/Manifesto/USLscalability.html)** (Neil Gunther): Real scaling is sub-linear due to contention (σ) and coherence (κ). Linear headroom calculations overestimate available capacity — doubling servers does not double throughput. Use USL to model realistic scaling curves and identify the point of diminishing returns.

```
Headroom = (Breaking point - Current peak) / Current peak

Time until scaling needed = Headroom / Growth rate
```

| Component | Current peak | Breaking point | Headroom | Time to scale (at projected growth) |
|---|---|---|---|---|
| [component] | [metric] | [metric] | [Nx] | [months] |

**Rules:**
- Minimum acceptable headroom: **2x** above current peak
- Plan to scale BEFORE headroom drops below 2x — scaling takes time
- The component with the LEAST headroom is the bottleneck — that is where to focus

### Step 6: Scaling Options

| Strategy | When to use | Lead time | Cost impact |
|---|---|---|---|
| **Vertical** (bigger instance) | Single bottleneck, simple architecture | Hours–days | Linear increase |
| **Horizontal** (more instances) | Stateless services, read-heavy workloads | Minutes (auto-scale) to days (manual) | Linear increase |
| **Caching** (CDN, Redis, application cache) | Read-heavy, cacheable content | Days–weeks | Reduces load on origin |
| **Read replicas** | Database read bottleneck | Days | Database cost increase |
| **Async processing** (queues, workers) | Write-heavy, batch operations | Weeks | Decouples peak from processing |
| **Architectural** (sharding, microservices, CQRS) | Fundamental scalability limit reached | Months | Significant engineering investment |

For each viable option:
- Estimated cost (monthly)
- Estimated capacity gain
- Implementation complexity
- Time to implement

### Step 7: Lead Time Assessment

| Scaling method | Lead time | Automation |
|---|---|---|
| Auto-scaling (cloud) | Minutes | Fully automated — configure scaling policies |
| Manual horizontal scaling | Hours–days | Requires provisioning and deployment |
| Vertical scaling | Hours (cloud) to weeks (on-prem) | Requires downtime for some configurations |
| Database scaling | Days–weeks | Requires migration planning, potential downtime |
| Architectural changes | Sprints–quarters | Requires design, implementation, migration |

**Critical rule:** Start scaling BEFORE you need it. If lead time is 2 weeks and you have 3 weeks of headroom, the decision must be made NOW.

### Step 8: Recommendation

Synthesise findings into a clear recommendation with decision timeline.

**Decision checkpoint:** Before recommending infrastructure scaling (new instances, upgraded tiers, additional replicas), stop and present the cost-vs-risk trade-off to the user. Scaling has cost and operational implications. Present: what happens if we don't scale (risk), what scaling costs (monthly/annual estimate), and when the decision needs to be made by (lead time). Do not assume approval — the user decides.

## Anti-Patterns (NEVER do these)

- **Linear extrapolation of non-linear growth** — viral growth is exponential. Seasonal business has peaks. Don't assume tomorrow looks like today
- **Planning for average, not peak** — systems fail at peak, not average. Capacity must handle peak with headroom
- **Ignoring seasonal patterns** — "we were fine last month" means nothing if next month is peak season
- **No cost analysis** — scaling has a cost. Recommendations without cost estimates are incomplete
- **Scaling before profiling** — if one query causes 80% of database load, adding replicas is treating the symptom. Profile first, scale second
- **Ignoring lead time** — "we'll scale when we need to" fails when scaling takes longer than the time to failure

## Output Format

```markdown
# Capacity Plan: [system/service]

## Current State
| Metric | Average | Peak | Trend |
|---|---|---|---|
| Requests/sec | [n] | [n] | [growing/stable/declining] |
| Concurrent users | [n] | [n] | [trend] |
| Data volume | [GB] | — | [growth rate/day] |

## Resource Utilisation
| Resource | Normal | Peak | Headroom | Status |
|---|---|---|---|---|
| CPU | [%] | [%] | [%] | OK / WARNING / CRITICAL |
| Memory | [GB] | [GB] | [GB] | OK / WARNING / CRITICAL |
| Storage | [GB] | — | [days until full] | OK / WARNING / CRITICAL |

## Growth Projections
| Horizon | Requests/sec | Users | Data volume |
|---|---|---|---|
| 3 months | [n] | [n] | [GB] |
| 6 months | [n] | [n] | [GB] |
| 12 months | [n] | [n] | [GB] |

## Bottleneck Analysis
| Component | Current peak | Breaking point | Headroom | Time to scale |
|---|---|---|---|---|
| [component] | [metric] | [metric] | [Nx] | [months] |

## Recommendations
| Priority | Action | Cost/month | Capacity gain | Lead time |
|---|---|---|---|---|
| 1 | [action] | [$] | [Nx] | [time] |

## Decision Timeline
- **Immediate:** [actions needed now]
- **30 days:** [decisions that must be made]
- **90 days:** [planned scaling activities]
```

## Related Skills

- `/performance-engineer:load-test-plan` — validate capacity assumptions with load tests. Plan capacity first, then design load tests to verify.
- `/performance-engineer:performance-profile` — profile specific bottlenecks identified during capacity planning.

Use the performance budget template (`templates/performance-budget.md`) for consistent output structure.
