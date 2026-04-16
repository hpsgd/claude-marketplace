# Load test plan for a search API endpoint

Developer invokes the load-test-plan skill to design load tests for `/api/search` — a full-text search endpoint over a Postgres database with 5 million records, currently serving 50 requests/second at peak.

## Prompt

> Design a load test plan for `GET /api/search?q=&page=&size=`. Current production load: ~50 rps peak. The database has ~5 million records. Average response time is 180ms. We want to verify the endpoint handles 3x current load (150 rps) gracefully and find the breaking point. We also suspect there might be a memory leak under sustained load. Tool preference: k6.

The skill would produce the following for this scenario:

---

## Output

# Load Test Plan: GET /api/search

### Target

- **System:** Full-text search endpoint over Postgres (5 million records)
- **Current load:** ~50 rps peak
- **Data profile:** 5 million records in search table, average response 180ms
- **Dependencies:** Postgres (primary), application server

### Scenarios

| Scenario | VUs | Duration | Ramp | Success criteria |
|---|---|---|---|---|
| Baseline | 50 | 5m | None | p95 < 500ms, errors < 0.1% |
| Stress | 50→500 | 15m | Linear ramp | Find breaking point, graceful degradation |
| Endurance | 100 (2x) | 2h | None | No memory leak, p95 stable (not trending up) |
| Spike | 250 sudden | 10m | Instant spike then back | Recovery < 2 minutes, errors < 1% post-recovery |

Endurance test is 2 hours — the suspected memory leak requires sustained load to manifest. A 10-minute endurance test would not reveal a slow leak.

### Thresholds

Define pass/fail BEFORE running the tests. These are the gates — if any threshold is breached, the build fails.

| Metric | Baseline | Stress | Endurance | Spike |
|---|---|---|---|---|
| p50 response | < 200ms | — | < 200ms (stable) | < 200ms (post-recovery) |
| p95 response | < 500ms | < 2s | < 500ms (no upward trend) | < 500ms (post-recovery) |
| p99 response | < 1s | documented | < 1s (no upward trend) | < 1s (post-recovery) |
| Error rate | < 0.1% | < 5% | < 0.1% | < 1% (post-recovery) |
| Memory (server) | stable | documented | no upward trend | recovers to baseline |

### k6 Script

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

// Vary queries to avoid cache warmup bias — same query every time = artificial cache hits
const searchTerms = [
  'quarterly report', 'invoice', 'contract renewal', 'project alpha',
  'onboarding', 'compliance audit', 'budget forecast', 'risk assessment',
  'customer feedback', 'product roadmap',
];

export const options = {
  scenarios: {
    baseline: {
      executor: 'constant-vus',
      vus: 50,
      duration: '5m',
    },
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },    // ramp to baseline
        { duration: '3m', target: 150 },   // ramp to 3x (target)
        { duration: '5m', target: 500 },   // ramp to 10x (find breaking point)
        { duration: '5m', target: 0 },     // ramp down
      ],
      startTime: '6m',
    },
    endurance: {
      executor: 'constant-vus',
      vus: 100,
      duration: '2h',
      startTime: '25m',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.001'],
  },
};

export default function () {
  const q = searchTerms[Math.floor(Math.random() * searchTerms.length)];
  const res = http.get(`https://api.example.com/api/search?q=${encodeURIComponent(q)}&page=1&size=25`);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'has items in body': (r) => JSON.parse(r.body).items !== undefined,
  });

  sleep(1); // think time — real users don't fire requests without pause
}
```

### Environment

- **Target:** Isolated staging environment, production-sized
- **Data:** 5 million records — use anonymised production dump or realistic data generator. Do not test against empty or small dataset — query performance is O(n log n) with table size
- **Monitoring:** Grafana dashboard for CPU, memory, Postgres connections, query times, and application metrics active during the test
- **Isolation:** Dedicated environment — no other teams or tests running concurrently. Shared staging invalidates results

### Schedule

- **Date:** Off-peak (after-hours or weekend)
- **Monitor:** One engineer watches Grafana dashboards throughout — automated thresholds catch pass/fail but human observation catches unexpected patterns (e.g., connection pool climbing, GC pauses)
- **Results:** k6 output to InfluxDB + Grafana, JSON summary committed to repo alongside script
- **Comparison:** Every run compared to previous baseline. Regressions flagged automatically via threshold breach

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill designs all four test types — Step 2 (Scenario Design) provides a table with Baseline, Stress, Endurance, and Spike, each with distinct duration, load pattern, and VU guidance. The instruction "Do not skip any — each type reveals different problems" is explicit. Traceable to Step 2.
- [x] PASS: Skill specifies production-like data volume — Step 3 (Realistic Data) states "Never test against an empty database" and "Production-like data volume — Query performance degrades with table size. 100 rows ≠ 10M rows." Traceable to Step 3.
- [x] PASS: Skill includes think time in k6 script — the k6 script skeleton in Step 4 includes `sleep(1); // think time — real users don't fire requests without pause`. Zero think time is listed in Anti-Patterns. Traceable to Step 4.
- [x] PASS: Success criteria defined before running tests — Step 5 (Success Criteria) is titled "Define pass/fail thresholds BEFORE running the tests" and includes p50, p95, p99, throughput, error rate, CPU, and memory targets. Traceable to Step 5.
- [x] PASS: Endurance test ≥1 hour — Step 2 specifies endurance duration as "1–4 hours". The minimum is 1 hour, meeting the criterion. Traceable to Step 2.
- [x] PASS: k6 script includes `check()` and `thresholds` — the k6 script skeleton in Step 4 shows both a `thresholds` block (`http_req_duration`, `http_req_failed`) and `check(res, {...})` with response validation. Traceable to Step 4.
- [x] PASS: Skill specifies isolated environment requirement — Step 6 (Environment) states "Isolated environment — Shared staging gives shared noise. Results are meaningless if other tests are running." Anti-Patterns lists "Shared staging". Traceable to Step 6 and Anti-Patterns.
- [~] PARTIAL: Skill addresses realistic request mix — Step 3 mentions "Realistic data distribution — Hotspots, popular items, skewed access patterns affect caching and indexing" and Step 2 specifies "Request mix: percentage of different operations." However, neither the script skeleton nor an explicit rule requires query parameterisation to avoid cache warming from repeated identical queries. This is implied by realistic patterns but not enforced. Criterion prefix is `PARTIAL:` so maximum score is 0.5. Traceable to Steps 2 and 3.
- [x] PASS: Output includes scenarios table, thresholds table, environment requirements, and execution plan with monitoring owner — the Output Format section specifies a Scenarios table, a Thresholds table, an Environment section, and a Schedule section that includes "Who monitors." Traceable to Output Format.

### Notes

The load-test-plan SKILL.md is thorough. The one genuine gap for a search endpoint test is the absence of explicit guidance on query parameterisation to prevent cache warmup bias — the skill covers realistic data and realistic patterns in general terms but a developer following it precisely might still use a fixed query string in the script. Worth adding a specific rule under Step 3 or 4.
