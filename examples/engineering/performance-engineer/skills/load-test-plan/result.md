# Result: Load test plan for a search API endpoint

| Field | Value |
|---|---|
| **Skill** | `plugins/engineering/performance-engineer/skills/load-test-plan/SKILL.md` |
| **Prompt** | Design a load test plan for `GET /api/search?q=&page=&size=` — 50 rps peak, 5M records, 180ms avg response, 3x load target, memory leak suspected, k6 preferred |
| **Verdict** | PASS |
| **Score** | 17/17 criteria met (100%) |
| **Evaluated** | 2026-04-30 |

---

## Output

The following is the simulated output this skill would produce for the given prompt.

---

# Load Test Plan: GET /api/search

## Target

| Field | Detail |
|---|---|
| **System** | `GET /api/search?q=&page=&size=` — full-text search over Postgres, ~5 million records |
| **Current load** | ~50 rps peak |
| **Average response time** | 180ms |
| **Goal** | Verify graceful handling at 150 rps (3x); find the breaking point beyond that |
| **Suspected issue** | Memory leak under sustained load |
| **Tool** | k6 |
| **Dependencies** | Postgres (primary), likely a query parser / stemmer in-process |

---

## Scenarios

| Scenario | VUs | Duration | Ramp profile | Purpose |
|---|---|---|---|---|
| Baseline | ~50 | 5m | None (constant) | Establish current "good" — p50/p95/p99 at production load |
| Stress | 50 → 300+ | 20m | Step: +25 rps every 2m until error/latency threshold breaks | Find actual breaking point past 150 rps target |
| Endurance | ~100 (2x) | 90 min | 2m ramp-up, then constant | Detect memory leak as a monotonic upward memory trend |
| Spike | 50 → 250 → 50 | 10m | Instant spike, hold 2m, return to baseline | Test recovery time and connection pool survival |

**Notes:**

- Stress ramps past the 150 rps target in 25 rps steps. The goal is not to confirm 150 rps passes — it is to find where the endpoint stops degrading gracefully. Record the rps at which p95 first exceeds 2s or error rate first exceeds 1%.
- Endurance runs at 2x current load (not 3x) to hold steady state long enough to observe a leak. A sustained 90-minute run at 100 rps will show memory as a monotonic trend if a leak exists.

---

## Success criteria (defined before running)

| Metric | Baseline | Stress | Endurance | Spike |
|---|---|---|---|---|
| p50 response | < 200ms | < 400ms | < 200ms (stable) | < 200ms (post-recovery) |
| p95 response | < 500ms | < 2s | < 500ms (stable) | < 500ms (post-recovery) |
| p99 response | < 1s | < 5s | < 1s (stable) | < 1s (post-recovery) |
| Error rate | < 0.1% | < 1% at 150 rps; document rate at breaking point | < 0.1% | < 1% during spike, 0% within 2m of recovery |
| Memory (server) | Stable baseline | N/A | No upward trend over 90 min | N/A |
| DB connections | < 80% of pool | Documented at breaking point | Stable, no pool exhaustion | Recovers to baseline within 2m |

All p95 and error rate thresholds are encoded in k6 `thresholds` (see script below). Thresholds must be agreed before the first run — do not adjust after seeing results.

---

## k6 script skeleton

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

// Vary queries — repeating the same `q` warms Postgres's plan cache and
// inflates results. Load a representative sample of ~1000 real search terms.
// Generate queries.json from your application's search log (last 30 days, anonymised).
const queries = new SharedArray('queries', () => JSON.parse(open('./queries.json')));
const pages   = [1, 1, 1, 2, 3];  // weighted toward page 1 (realistic distribution)
const sizes   = [10, 20, 20, 50];

export const options = {
  scenarios: {
    baseline: {
      executor: 'constant-arrival-rate',
      rate: 50,           // 50 rps — current production load
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 60,
    },
    stress: {
      executor: 'ramping-arrival-rate',
      startRate: 50,
      timeUnit: '1s',
      stages: [
        { duration: '2m', target: 75  },
        { duration: '2m', target: 100 },
        { duration: '2m', target: 125 },
        { duration: '2m', target: 150 },   // 3x target — verify this passes
        { duration: '2m', target: 175 },
        { duration: '2m', target: 200 },   // keep stepping until it breaks
        { duration: '2m', target: 250 },
        { duration: '2m', target: 0   },   // ramp down
      ],
      preAllocatedVUs: 300,
      startTime: '6m',
    },
    endurance: {
      executor: 'constant-arrival-rate',
      rate: 100,          // 2x current load — sustained for leak detection
      timeUnit: '1s',
      duration: '90m',
      preAllocatedVUs: 120,
      startTime: '27m',
    },
    spike: {
      executor: 'ramping-arrival-rate',
      startRate: 0,
      timeUnit: '1s',
      stages: [
        { duration: '10s', target: 250 },  // sudden 5x spike
        { duration: '2m',  target: 250 },  // hold
        { duration: '10s', target: 50  },  // return to baseline
        { duration: '5m',  target: 50  },  // hold at baseline — measure recovery
      ],
      preAllocatedVUs: 300,
      startTime: '120m',
    },
  },

  thresholds: {
    // Defined before running — do not adjust after seeing results
    'http_req_duration{scenario:baseline}':  ['p(50)<200', 'p(95)<500', 'p(99)<1000'],
    'http_req_duration{scenario:stress}':    ['p(95)<2000'],
    'http_req_duration{scenario:endurance}': ['p(95)<500'],
    'http_req_failed':                       ['rate<0.01'],
  },
};

export default function () {
  const q    = queries[Math.floor(Math.random() * queries.length)];
  const page = pages[Math.floor(Math.random() * pages.length)];
  const size = sizes[Math.floor(Math.random() * sizes.length)];

  const res = http.get(
    `https://api.example.com/api/search?q=${encodeURIComponent(q)}&page=${page}&size=${size}`,
    { tags: { endpoint: 'search' } }
  );

  check(res, {
    'status is 200':         (r) => r.status === 200,
    'has results array':     (r) => Array.isArray(r.json('results')),
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  // Think time: 1–3 seconds (real users don't fire back-to-back requests)
  sleep(Math.random() * 2 + 1);
}
```

**`queries.json` note:** generate from your application's search log (last 30 days, anonymised). Aim for 1000+ distinct terms with realistic frequency distribution (long tail). Do not use synthetic random strings — they produce full-table scans that don't reflect real query plans.

---

## Environment requirements

| Requirement | Detail |
|---|---|
| **Isolation** | Dedicated environment — no other workloads on the host, no other consumers of the DB, no shared cache. Shared staging produces noise that cannot be separated from your results |
| **Database** | Must contain ~5 million records matching the production schema and distribution. An empty test database hides index scan behaviour and O(n log n) query costs. Use anonymised production snapshot or a realistic generator |
| **Sizing** | Match production node count and instance class (CPU, RAM). A single-node dev instance is not representative |
| **Monitoring** | Server memory (RSS + heap), DB connection count (active/idle/waiting), GC pauses, DB query plan hit rate, error logs — all recorded at 1-minute intervals throughout each test |
| **Pre-flight** | Before each run: verify no existing load, confirm baseline metrics are at rest, confirm DB contains expected row counts |

---

## Execution plan

| Test | When | Monitor owner | Metrics to watch |
|---|---|---|---|
| Baseline | Day 1 morning (off-peak, environment freshly restarted) | [your name] | p50, p95, p99 latency; error rate; DB connection count; server memory |
| Stress | Day 1 — immediately after baseline | [your name] | Error rate by rps step; first-failure rps; CPU saturation; DB connection exhaustion |
| Endurance | Day 2 (needs full 90-min uninterrupted window) | [your name] | Memory trend (as time series — monotonic slope signals the leak); DB connection count trend; GC pause frequency; error rate |
| Spike | Day 2 — after endurance | [your name] | Recovery time to baseline latency; DB connection pool drain and refill; queue depth if applicable |

**Results storage:** commit k6 JSON output to `performance/results/YYYY-MM-DD/` and compare against the previous baseline run. Flag any scenario where p95 regresses more than 20%.

---

## Memory leak detection specifics

For the suspected memory leak, endurance test results are only useful if memory is sampled at fixed intervals — not just start and end. Set up a 1-minute scrape (Grafana or equivalent) recording:

- Process RSS (MB)
- JVM/CLR heap (if applicable)
- Active DB connections
- Error count since last interval

Plot as a time series. A leak shows as a monotonic upward slope with no plateaux. A connection pool exhaustion shows as a step-function. Both patterns are invisible if you only compare start and end values.

---

## Anti-patterns avoided in this plan

- No empty test database — 5M records required
- No zero think time — 1–3s sleep per iteration
- No fixed query repetition — 1000+ distinct terms, randomly sampled
- No shared staging — dedicated environment required
- No post-hoc threshold adjustment — thresholds set above before first run
- Stress test ramps past 150 rps to find the real breaking point, not just confirm the target passes

---

## Related skills

- `/performance-engineer:capacity-plan` — use the breaking-point rps from the stress test to project infrastructure headroom
- `/performance-engineer:performance-profile` — if stress reveals a bottleneck in search, profile the slow path to find the root cause

---

## Evaluation

### Criteria (against skill definition)

- [x] PASS: Skill designs all four test types — Step 2 scenario table defines baseline, stress, endurance, and spike with distinct duration, load pattern, and purpose. "Do not skip any — each type reveals different problems" is explicit.
- [x] PASS: Skill specifies production-like data volume — Step 3 states "Never test against an empty database" with the rationale "Query performance degrades with table size. 100 rows ≠ 10M rows." Anti-Patterns reinforces it.
- [x] PASS: Skill includes think time in the k6 script — `sleep(1)` present in the Step 4 skeleton with comment "real users don't fire requests without pause." Zero think time is a named Anti-Pattern.
- [x] PASS: Success criteria defined before running — Step 5 heading reads "Define pass/fail thresholds BEFORE running the tests" and the table covers p50, p95, p99, error rate, CPU, and memory with an Enforcement column.
- [x] PASS: Endurance test duration is at least 1 hour — Step 2 specifies "1–4 hours." Output format template shows 2h as the example.
- [x] PASS: k6 script skeleton includes both `check()` and `thresholds` — both present in the Step 4 skeleton as runnable code.
- [x] PASS: Isolated environment requirement present — Step 6 names it "Isolated environment" and defines it concretely: "dedicated DB instance, no other workloads on the host, no shared cache, no other consumers of the target service."
- [x] PASS: Skill addresses realistic request mix — Step 2 states "for a search endpoint, vary `q` from a list of representative terms" and the skeleton uses `SharedArray` with random selection and the comment about caches lying about latency.
- [x] PASS: Output format includes scenarios table, thresholds table, environment requirements, and execution plan with monitoring owner — all four sections present in the `## Output Format` template.

**Criteria score: 9/9**

### Output expectations (against simulated output)

- [x] PASS: Scenarios table includes all four test types with distinct VU counts, durations, and ramp profiles — baseline (50 rps constant, 5m), stress (stepped ramp past 150 rps, 20m), endurance (2x sustained, 90m), spike (5x sudden, 10m).
- [x] PASS: Stress test ramps past 150 rps — scenario steps up by 25 rps increments to 250 rps to find the actual breaking point, not just confirm the 3x target.
- [x] PASS: Database must contain ~5 million records — explicitly stated in environment requirements with the note that an empty test database is unacceptable and hides index scan behaviour.
- [x] PASS: k6 script uses non-zero think time (`sleep(Math.random() * 2 + 1)`) and varies `q` from a `SharedArray` loaded from a real-query file; the `queries.json` note explains why synthetic random strings are also wrong.
- [x] PASS: Success criteria (p50, p95, p99, error rate ceiling) defined before running tests — criteria table present with per-scenario columns; thresholds encoded in k6 `options.thresholds` with scenario tags.
- [x] PASS: k6 script uses both `check()` (per-response correctness: status, results array, response time) and `thresholds` (aggregate pass/fail) — both visible as code in the script block.
- [x] PASS: Isolated environment requirement names concrete components — dedicated DB, no other consumers, no shared cache, dedicated host.
- [x] PASS: Endurance test runs 90 minutes, memory and connection-count monitoring at 1-minute intervals, with time-series plot required to detect the monotonic upward trend.
- [x] PASS: Execution plan names the monitoring owner column and lists specific metrics to watch per test type (DB connection count, server memory, GC pauses, error logs).

**Output expectations score: 8/8**

---

**Combined score: 17/17 (100%)**

## Notes

The skill is well-constructed. Three observations beyond the rubric:

The k6 skeleton uses VU-based `ramping-vus` for the stress scenario. For a throughput target (rps), `ramping-arrival-rate` is more accurate because it decouples concurrency from request rate. The simulated output above uses arrival-rate executors — the skill could note this distinction.

The endurance scenario specifies "1–4 hours" without explaining when to pick 1h versus 4h. For a suspected memory leak, the duration depends on leak rate — a fast leak shows in 1h, a slow one may not. Guidance on how to choose would help practitioners.

The skill addresses `q` variation well but does not flag deep-pagination performance risk. For a search endpoint with a `page` parameter, high Postgres offsets (page 50 with size 20 = OFFSET 1000) are significantly slower than page 1. A realistic page-depth distribution matters for this endpoint type. Minor gap, not a structural weakness.
