# SLO Definition — {{service_name}}

| Field        | Value            |
|--------------|------------------|
| Service      | {{service_name}} |
| Owner        | {{team}}         |
| Last reviewed| {{date}}         |
| Status       | Draft / Active / Under Review |

## Service Level Indicators (SLIs)

| # | Indicator | Measurement | Good event definition | Data source |
|---|-----------|-------------|----------------------|-------------|
| 1 | Availability | Proportion of successful requests (non-5xx) | HTTP status < 500 | {{e.g. load balancer logs}} |
| 2 | Latency (p50) | Median response time | < {{threshold}} ms | {{APM / metrics}} |
| 3 | Latency (p99) | 99th percentile response time | < {{threshold}} ms | {{APM / metrics}} |
| 4 | Correctness | Proportion of responses with correct payload | Matches contract / golden test | {{e.g. synthetic monitor}} |
| 5 | {{custom SLI}} | {{measurement}} | {{good threshold}} | {{source}} |

## Service Level Objectives (SLOs)

| SLI | Target | Window | Error budget | Budget (absolute) |
|-----|--------|--------|-------------|-------------------|
| Availability | {{99.9 %}} | {{30 days rolling}} | {{0.1 %}} | {{~43 min/month}} |
| Latency p50 | {{95 % of requests < X ms}} | {{30 days rolling}} | {{5 %}} | — |
| Latency p99 | {{99 % of requests < Y ms}} | {{30 days rolling}} | {{1 %}} | — |
| Correctness | {{99.99 %}} | {{30 days rolling}} | {{0.01 %}} | — |

## Alerting — burn-rate alerts

| Alert | Burn rate | Window (long) | Window (short) | Severity | Channel |
|-------|----------|---------------|----------------|----------|---------|
| Page  | {{14.4x}} | {{1 h}}      | {{5 min}}      | Critical | {{PagerDuty}} |
| Page  | {{6x}}   | {{6 h}}       | {{30 min}}     | High     | {{PagerDuty}} |
| Ticket| {{3x}}   | {{1 d}}       | {{2 h}}        | Medium   | {{Slack + ticket}} |
| Ticket| {{1x}}   | {{3 d}}       | {{6 h}}        | Low      | {{Slack}} |

> Burn-rate methodology follows the Google SRE multi-window approach.

## Review cadence

| Activity | Frequency | Participants |
|----------|-----------|-------------|
| SLO review | {{monthly}} | {{SRE + service owner}} |
| Error budget review | {{weekly}} | {{on-call lead}} |
| SLO target revision | {{quarterly}} | {{eng leadership + SRE}} |

## Error budget policy

When the error budget for any SLO is **exhausted** within the window:

1. **Freeze** — no non-critical deployments until budget recovers.
2. **Prioritise** — team allocates {{e.g. 50 %}} of sprint capacity to reliability work.
3. **Post-mortem** — conduct incident review for any single event that consumed >{{25 %}} of the budget.
4. **Escalate** — if budget is exhausted two consecutive windows, escalate to {{eng leadership}}.

When the error budget is **healthy** (>{{50 %}} remaining):

- Feature work proceeds at normal velocity.
- Team may run controlled experiments (canary, chaos testing).

## Appendix — dashboard links

| Dashboard | URL |
|-----------|-----|
| SLO overview | {{url}} |
| Error budget burn-down | {{url}} |
| Alerting config | {{url}} |
