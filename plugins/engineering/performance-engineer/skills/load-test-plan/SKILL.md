---
name: load-test-plan
description: Design a load test plan — define scenarios, configure realistic load patterns, script tests, and define success criteria.
argument-hint: "[system, endpoint, or flow to load test]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Design a load test plan for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Target Identification

Before writing any test scripts, understand what you are testing and what "normal" looks like.

1. **What system/endpoint/flow?** — specific URLs, API routes, or user workflows
2. **Current traffic patterns** — check APM, access logs, or analytics for: requests/second, concurrent users, peak hours, read/write ratio
3. **Data characteristics** — how large is the database? How many records in key tables? What is the average payload size?
4. **Dependencies** — what external services does this endpoint call? (databases, caches, third-party APIs, message queues)

If no traffic data exists, estimate from user count and expected usage patterns. Document the assumption.

### Step 2: Scenario Design

Design tests for each type. Do not skip any — each type reveals different problems.

| Test type | Purpose | Duration | Load pattern | What it reveals |
|---|---|---|---|---|
| **Baseline** | Establish normal performance | 5 minutes | Current production load | What "good" looks like — your comparison point |
| **Stress** | Find the breaking point | 15 minutes | Ramp from 1x to 10x current load | Where errors start, which component fails first |
| **Endurance** | Find slow leaks and degradation | 1–4 hours | Sustained 2x load | Memory leaks, connection pool exhaustion, log disk filling |
| **Spike** | Test auto-scaling and recovery | 10 minutes | Sudden 5x spike, then return to normal | Recovery time, auto-scaling behaviour, queue backlog clearance |

**For each scenario, define:**
- Virtual users (VUs): how many concurrent users
- Ramp-up: how quickly to reach target load
- Think time: realistic pause between user actions (not zero — real users think)
- Request mix: percentage of different operations (e.g., 80% reads, 15% writes, 5% deletes)
- Input variation: parameterise request inputs (search terms, IDs, page numbers) from a realistic distribution. Repeating the same input warms query/result caches and inflates results — for a search endpoint, vary `q` from a list of representative terms

### Step 3: Realistic Data

Test with production-like data. Empty databases lie about performance.

| Requirement | Why it matters |
|---|---|
| Production-like data volume | Query performance degrades with table size. 100 rows ≠ 10M rows |
| Realistic data distribution | Hotspots, popular items, skewed access patterns affect caching and indexing |
| Diverse user profiles | Different users have different data volumes (power users vs new users) |
| Representative payloads | Request and response sizes affect network, serialisation, and memory |

**Rules:**
- Never test against an empty database
- Use anonymised production data or realistic generators
- Document the data setup so tests are reproducible

### Step 4: Tool Selection and Scripting

**Preferred:** [k6](https://k6.io) — scriptable, CI-friendly, JavaScript-based, built-in metrics.
**Alternative:** [Locust](https://locust.io) — Python-native, distributed by default.

**k6 script skeleton:**

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

// Realistic input set — repeated identical inputs hit caches and lie about latency.
const queries = new SharedArray('queries', () => JSON.parse(open('./queries.json')));

export const options = {
  scenarios: {
    baseline: {
      executor: 'constant-vus',
      vus: 50,          // adjust to current production load
      duration: '5m',
    },
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },   // ramp to baseline
        { duration: '5m', target: 200 },   // ramp to 4x
        { duration: '5m', target: 500 },   // ramp to 10x
        { duration: '3m', target: 0 },     // ramp down
      ],
      startTime: '6m',  // start after baseline completes
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],   // p95 < 500ms
    http_req_failed: ['rate<0.01'],     // error rate < 1%
  },
};

export default function () {
  const q = queries[Math.floor(Math.random() * queries.length)];
  const res = http.get(`https://api.example.com/endpoint?q=${encodeURIComponent(q)}`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1); // think time — real users don't fire requests without pause
}
```

### Step 5: Success Criteria

Define pass/fail thresholds BEFORE running the tests:

| Metric | Target | Enforcement |
|---|---|---|
| p50 response time | < 200ms for API, < 1s for page load | k6 threshold |
| p95 response time | < 500ms for API, < 3s for page load | k6 threshold — build fails if exceeded |
| p99 response time | < 1s for API, < 5s for page load | k6 threshold |
| Throughput | Sustain 3x current load without degradation | Stress test verification |
| Error rate | < 0.1% under normal load, < 1% under stress | k6 threshold |
| CPU utilisation | < 70% at normal load | Monitoring during test |
| Memory utilisation | Stable (no upward trend during endurance test) | Monitoring during test |

### Step 6: Environment

| Requirement | Why |
|---|---|
| **Isolated environment** | Shared staging gives shared noise. Concretely: dedicated DB instance, no other workloads on the host, no shared cache, no other consumers of the target service |
| **Production-like sizing** | Testing on a single-node dev instance tells you nothing about production |
| **Monitoring active** | CPU, memory, disk I/O, network, database connections — all must be observable, and recorded at fixed intervals (e.g., every 5 minutes during endurance) so monotonic trends are visible, not just final values |
| **Pre-flight check** | Before running: verify environment is clean, no existing load, baseline metrics are normal |

### Step 7: Execution Plan

| Item | Detail |
|---|---|
| **When to run** | Off-peak for shared environments. Any time for isolated environments |
| **Who monitors** | Someone watches dashboards during the test — automated tests need human observation for unexpected patterns. Name the owner per test type |
| **Metrics per test** | Baseline: latency percentiles, error rate. Stress: error rate, first-failure threshold, CPU/memory saturation. Endurance: memory trend, DB connection count, GC pauses (sampled at fixed intervals). Spike: recovery time, queue depth, auto-scaling behaviour |
| **Results storage** | k6 Cloud, InfluxDB + Grafana, or JSON output committed to repo |
| **Comparison baseline** | Every run is compared to the previous baseline. Regressions are flagged automatically |

## Anti-Patterns (NEVER do these)

- **Testing against empty databases** — query performance is O(1) on 100 rows and O(n log n) on 10M rows. Empty databases lie
- **Zero think time** — real users pause between actions. Zero think time tests your server under unrealistic conditions
- **Testing only the happy path** — include error paths, auth failures, large payloads, and concurrent writes
- **Shared staging** — if other teams are using the same environment, your results include their noise
- **No baseline** — without a baseline, you cannot detect regression. Always run baseline first
- **One-time tests** — load tests should run in CI on every significant change to performance-critical paths

## Output Format

```markdown
# Load Test Plan: [target system/endpoint]

## Target
- **System:** [what is being tested]
- **Current load:** [requests/sec, concurrent users]
- **Data profile:** [database size, key table counts]
- **Dependencies:** [external services called]

## Scenarios
| Scenario | VUs | Duration | Ramp | Success criteria |
|---|---|---|---|---|
| Baseline | [n] | 5m | None | p95 < 500ms, errors < 0.1% |
| Stress | [n→10n] | 15m | Linear | Find breaking point, graceful degradation |
| Endurance | [2n] | 2h | None | No memory leak, stable latency |
| Spike | [5n sudden] | 10m | Step | Recovery < 2 minutes |

## Thresholds
| Metric | Baseline | Stress | Endurance | Spike |
|---|---|---|---|---|
| p95 response | < 500ms | < 2s | < 500ms (stable) | < 500ms (post-recovery) |
| Error rate | < 0.1% | < 5% | < 0.1% | < 1% (post-recovery) |
| CPU | < 70% | documented | < 70% (stable) | recovers to < 70% |

## Environment
- **Target:** [URL/endpoint]
- **Data:** [production-like, [n] records]
- **Monitoring:** [tools in use]
- **Isolation:** [dedicated/shared]

## Schedule
- **Date:** [when]
- **Monitor:** [who watches]
- **Results:** [where stored]
```

## Related Skills

- `/performance-engineer:capacity-plan` — use load test results to validate or update capacity plans.
- `/performance-engineer:performance-profile` — when load tests reveal bottlenecks, profile the specific endpoints to find root causes.
