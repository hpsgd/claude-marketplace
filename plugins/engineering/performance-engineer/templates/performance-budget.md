# Performance Budget: [Service / Application Name]

| Field | Value |
|---|---|
| **Author** | [Name] |
| **Baseline date** | [YYYY-MM-DD] |
| **Review cadence** | [e.g. Monthly, quarterly] |
| **Status** | Draft / Active / Under Review |

## API Performance Budget

| Endpoint / Operation | p50 Target | p95 Target | p99 Target | Error Rate Target | Throughput Target |
|---|---|---|---|---|---|
| [e.g. GET /api/users] | [e.g. 50ms] | [e.g. 200ms] | [e.g. 500ms] | [e.g. < 0.1%] | [e.g. 1000 req/s] |
| [e.g. POST /api/orders] | [e.g. 100ms] | [e.g. 400ms] | [e.g. 1000ms] | [e.g. < 0.05%] | [e.g. 500 req/s] |
| [e.g. Background job: invoice generation] | [e.g. 2s] | [e.g. 5s] | [e.g. 10s] | [e.g. < 0.01%] | [e.g. 100/min] |

## Frontend Performance Budget

Based on [Google Core Web Vitals](https://web.dev/vitals/).

| Metric | Target | Threshold (Action Required) |
|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 200ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | > 0.25 |
| **Bundle size** (JS, compressed) | [e.g. < 200 KB] | [e.g. > 300 KB] |
| **Page weight** (total transfer) | [e.g. < 1 MB] | [e.g. > 2 MB] |
| **Time to Interactive** | [e.g. < 3.5s] | [e.g. > 5.0s] |
| **First Contentful Paint** | [e.g. < 1.8s] | [e.g. > 3.0s] |

## Infrastructure Budget

| Resource | Ceiling | Alert Threshold | Measurement Window |
|---|---|---|---|
| **CPU utilisation** | [e.g. 70% sustained] | [e.g. 60% for 5 min] | [e.g. 5-minute rolling average] |
| **Memory utilisation** | [e.g. 80%] | [e.g. 70%] | [e.g. 5-minute rolling average] |
| **Connection pool utilisation** | [e.g. 75%] | [e.g. 60%] | [e.g. 1-minute rolling average] |
| **Disk I/O** | [e.g. 80% throughput capacity] | [e.g. 65%] | [e.g. 5-minute rolling average] |
| **Network bandwidth** | [e.g. 70% of provisioned] | [e.g. 55%] | [e.g. 5-minute rolling average] |

## Enforcement Mechanisms

| Metric | Enforcement | Tool | Threshold |
|---|---|---|---|
| Bundle size | CI gate — fails build | [e.g. bundlesize, size-limit] | [e.g. > 200 KB compressed] |
| Core Web Vitals | Alert + dashboard | [e.g. Lighthouse CI, SpeedCurve] | [e.g. LCP > 2.5s on 3 consecutive runs] |
| API latency (p95) | Alert | [e.g. Datadog, Grafana] | [e.g. > 200ms for 5 min] |
| Error rate | Alert + page | [e.g. PagerDuty, Opsgenie] | [e.g. > 0.5% for 2 min] |
| Infrastructure utilisation | Alert | [e.g. CloudWatch, Prometheus] | [e.g. CPU > 70% for 10 min] |

## Baseline Values

Measured on [YYYY-MM-DD] against [environment — e.g. production, staging].

| Metric | Current Value | Target | Gap |
|---|---|---|---|
| [e.g. LCP] | [e.g. 3.1s] | [e.g. < 2.5s] | [e.g. -0.6s needed] |
| [e.g. GET /api/users p95] | [e.g. 180ms] | [e.g. < 200ms] | [e.g. Within budget] |
| [e.g. Bundle size] | [e.g. 245 KB] | [e.g. < 200 KB] | [e.g. -45 KB needed] |

## Exception Process

| Step | Detail |
|---|---|
| **Request** | [Open an issue/PR with justification, expected duration, and plan to return within budget] |
| **Approval** | [Who approves — e.g. tech lead + performance engineer] |
| **Duration** | [Maximum exception duration — e.g. 30 days, 1 sprint] |
| **Tracking** | [How the exception is tracked — e.g. label on issue, entry in this document] |
| **Expiry** | [What happens when the exception expires — budget must be met or exception renewed with new justification] |

## Review Schedule

| Field | Value |
|---|---|
| **Review cadence** | [e.g. Monthly] |
| **Reviewers** | [e.g. Performance engineer, tech lead, SRE] |
| **Criteria for tightening** | [e.g. Baseline consistently 20%+ below target for 3 consecutive reviews] |
| **Criteria for relaxing** | [e.g. Business requirement change, architecture migration in progress] |
| **Next review date** | [YYYY-MM-DD] |
