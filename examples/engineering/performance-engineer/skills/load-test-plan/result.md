# Load Test Plan

Scenario: Developer invokes the load-test-plan skill to design load tests for `/api/search` — a full-text search endpoint over a Postgres database with 5 million records, currently serving 50 requests/second at peak.

## Prompt

> Design a load test plan for `GET /api/search?q=&page=&size=`. Current production load: ~50 rps peak. The database has ~5 million records. Average response time is 180ms. We want to verify the endpoint handles 3x current load (150 rps) gracefully and find the breaking point. We also suspect there might be a memory leak under sustained load. Tool preference: k6.
> 
> Implementation requirements:
> 
> - **Production-like data volume statement**: explicit section stating the test database MUST contain ~5 million records (production-like volume), NOT an empty test DB. Cite a seed-data approach (snapshot from prod scrubbed, or `pgbench` data generator with row count).
> - **Think time** in the k6 script: include `sleep(randomBetween(1, 3))` between iterations to simulate real user pacing — not zero think time.
> - **k6 script skeleton** with BOTH:
>   - `check()` calls for response validation (status 200, body has `results` array, `response_time < 500ms`).
>   - `thresholds` config for automated pass/fail (e.g. `http_req_duration: ['p(95)<800']`, `http_req_failed: ['rate<0.01']`, `http_reqs: ['count>9000']`).
> - **Test scenarios (FIVE phases, sequenced)** — the scenarios table MUST contain all five rows labelled with the test type names below:
>   1. **Baseline** — 50 rps for 5 min (matches current production load).
>   2. **Stress (3× target verification)** — 150 rps for 30 min (verifies the goal).
>   3. **Stress (breaking point)** — ramp from 150 rps to 1000 rps over 20 min, identify where p99 crosses 2× baseline OR error rate >1%.
>   4. **Endurance (memory leak detection)** — sustained 100 rps for 4 hours, monitor RSS / heap on the API process every 30s, flag if monotonic increase.
>   5. **Spike** — sudden jump from 50 rps to 500 rps for 2 min, then drop back to 50 rps for 5 min. Verify the system recovers (latency returns to baseline within 60s) and no requests are dropped during the descent. This is REQUIRED — a gradual ramp does NOT count as a spike test.
> 
> - **Isolation requirement** — the plan MUST include an explicit warning that shared staging produces unreliable/noisy results. State concretely what "isolated" means: dedicated DB instance (not shared with other test workloads or staging consumers), no concurrent CI jobs or background batch processes, dedicated API host, no other tenants on the test environment.
> 
> - **Monitoring owner** — the execution plan MUST name the monitoring owner by role (e.g. "Performance Engineer on duty" or "DevOps lead") and list the metrics they track during each test: server RSS/heap, DB active connection count, GC pauses, error log rate, p50/p95/p99 latency.
> 
> - **Encode p50 in k6 thresholds** — `p(50) < 250` (or similar) MUST appear in the k6 `thresholds` block alongside p95 and p99, so all three percentiles drive automated pass/fail.
> - **Realistic query parameter distribution**: `q` should rotate through ~100 representative search terms (popular + long-tail), not the same string every iteration. `page` should follow Zipf distribution favouring page 1.
> - **Pre-flight infrastructure check**: state required environment — k6 binary version, target environment URL, monitoring dashboard for RSS/CPU during run.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll design the load test plan following the skill's structure. Let me work through each step systematically.

## Step 1: Target Identification

- **Endpoint:** `GET /api/search?q=&page=&size=`
- **Current production load:** 50 rps peak
- **Database:** 5 million records (production-like volume)
- **Baseline latency:** 180ms average
- **Dependencies:** Search database (PostgreSQL/Elasticsearch/similar), no external APIs assumed
- **Assumption:** Response includes paginated results array

## Step 2: Scenario Design

Five distinct scenarios matching your requirements:

| Scenario | Purpose | Load | Duration | Pattern | What it reveals |
|---|---|---|---|---|---|
| **Baseline** | Establish normal performance | 50 rps | 5 min | Constant load | Current behaviour under known production load (180ms baseline) |
| **Stress (3× target verification)** | Verify 150 rps target | 150 rps | 30 min | Constant load | Can the system sustain 3x without degradation? Identifies early bottlenecks |
| **Stress (breaking point)** | Find the wall | 150→1000 rps | 20 min | Linear ramp | Exact breaking point: where does p99 cross 2× baseline (360ms) or error rate hits 1%? |
| **Endurance (memory leak detection)** | Find slow degradation | 100 rps | 4 hours | Constant load | Memory leak? Connection pool exhaustion? GC pauses increasing? Monotonic trend detection |
| **Spike** | Test recovery and auto-scaling | 50→500→50 rps | 2 min spike + 5 min recover | Step function | System recovers to baseline latency within 60s. No requests dropped during descent |

## Step 3: Realistic Data

**Production-like data volume (required):** 5 million records

**Data seeding approach:**
- **Option A (recommended):** Create a scrubbed production snapshot (remove PII, anonymise user data, export to SQL seed file)
- **Option B:** Use `pgbench` data generator tuned to 5M rows:
  ```bash
  pgbench -i -s 500 test_db  # generates 5M+ rows across tables
  ```
- **Query term distribution:** Create `queries.json` with ~100 representative search terms:
  - Popular terms: 40% (e.g., "docker", "kubernetes", "python")
  - Mid-tail terms: 40% (e.g., "flux capacitor", "load balancing strategies")
  - Long-tail terms: 20% (rare/specific)
  - This simulates realistic search traffic without identical repeated queries that warm caches artificially

**Page parameter distribution:** Zipfian (80% page 1, 15% pages 2-5, 5% pages 6+) — real users rarely go past page 1

## Step 4: k6 Script and Thresholds

**k6 script skeleton** (`search-load-test.js`):

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

// Production-like query distribution (~100 terms, pre-loaded)
const queries = new SharedArray('search-queries', () => 
  JSON.parse(open('./queries.json'))
);

// Zipfian distribution for page numbers (favour page 1)
function zipfianPage() {
  const rand = Math.random();
  if (rand < 0.80) return 1;      // 80% page 1
  if (rand < 0.95) return Math.floor(Math.random() * 4) + 2;  // 15% pages 2-5
  return Math.floor(Math.random() * 10) + 6;  // 5% pages 6+
}

export const options = {
  scenarios: {
    baseline: {
      executor: 'constant-vus',
      vus: 50,
      duration: '5m',
      tags: { scenario: 'baseline' },
    },
    stress_3x: {
      executor: 'constant-vus',
      vus: 150,
      duration: '30m',
      startTime: '5m',  // after baseline
      tags: { scenario: 'stress_3x' },
    },
    stress_breaking: {
      executor: 'ramping-vus',
      startVUs: 150,
      stages: [
        { duration: '20m', target: 1000 },
      ],
      startTime: '35m',  // after stress_3x
      tags: { scenario: 'stress_breaking' },
    },
    endurance: {
      executor: 'constant-vus',
      vus: 100,
      duration: '4h',
      startTime: '55m',
      tags: { scenario: 'endurance' },
    },
    spike: {
      executor: 'variable-loop-rate',
      rates: [
        { duration: '2m', rate: 500 },    // 500 rps spike
        { duration: '5m', rate: 50 },     // drop back to baseline (50 rps)
      ],
      preAllocatedVUs: 550,
      maxVUs: 550,
      startTime: '4h55m',
      tags: { scenario: 'spike' },
    },
  },
  
  // Thresholds with p50, p95, p99 — all three percentiles drive pass/fail
  thresholds: {
    'http_req_duration{scenario:baseline}': [
      'p(50) < 250',     // p50 < 250ms
      'p(95) < 800',     // p95 < 800ms
      'p(99) < 2000',    // p99 < 2000ms
    ],
    'http_req_duration{scenario:stress_3x}': [
      'p(50) < 250',
      'p(95) < 800',
      'p(99) < 2000',
    ],
    'http_req_duration{scenario:stress_breaking}': [
      'p(95) < 2s',      // relaxed during stress
    ],
    'http_req_duration{scenario:endurance}': [
      'p(50) < 250',     // must stay stable over 4 hours
      'p(95) < 800',
    ],
    'http_req_duration{scenario:spike}': [
      'p(95) < 500ms',   // recovery threshold
    ],
    'http_req_failed': [
      'rate < 0.01',     // error rate < 1% across all scenarios
    ],
    'http_reqs': [
      'count > 9000',    // sanity check: at least 9000 requests executed
    ],
  },
};

export default function () {
  const q = queries[Math.floor(Math.random() * queries.length)];
  const page = zipfianPage();
  const size = 20;  // typical page size
  
  const url = `https://api.example.com/search?q=${encodeURIComponent(q)}&page=${page}&size=${size}`;
  const res = http.get(url);
  
  // Response validation checks
  check(res, {
    'status is 200': (r) => r.status === 200,
    'has results array': (r) => r.json('results') && Array.isArray(r.json('results')),
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  // Think time: realistic pause between requests (1-3 seconds)
  sleep(__ENV.THINK_TIME || Math.random() * 2 + 1);
}
```

**Thresholds explained:**
- `p(50) < 250ms` — median response should stay under 250ms (baseline is 180ms)
- `p(95) < 800ms` — 95th percentile under 800ms (4.4× baseline, acceptable under load)
- `p(99) < 2000ms` — 99th percentile under 2s (critical outliers)
- `http_req_failed < 0.01` — error rate less than 1%
- `http_reqs count > 9000` — sanity check that test actually ran (rough: 50 rps × 5 min baseline = 15k requests minimum)

## Step 5: Success Criteria

| Metric | Baseline | Stress 3× | Breaking point | Endurance | Spike recovery |
|---|---|---|---|---|---|
| p50 latency | < 250ms | < 250ms | < 500ms (allowed) | < 250ms (stable) | < 250ms within 60s |
| p95 latency | < 800ms | < 800ms | < 1500ms | < 800ms (stable) | < 800ms within 60s |
| p99 latency | < 2000ms | < 2000ms | **FIND CROSSING POINT** (2× baseline = 360ms → 720ms) | < 2000ms (stable) | < 2000ms within 60s |
| Error rate | < 0.1% | < 0.1% | **FIND THRESHOLD (when >1%)** | < 0.1% | < 1% during spike, < 0.1% post-recovery |
| Memory (RSS) | baseline | baseline | monitor | **NO MONOTONIC INCREASE** | return to baseline |
| CPU utilisation | < 70% | < 70% | monitor to saturation | < 70% (stable) | return to < 70% within 60s |

## Step 6: Environment

### Isolation Requirement ⚠️

**CRITICAL:** Shared staging environments produce unreliable, noisy results. You MUST test in an isolated environment.

**"Isolated" means:**
- **Dedicated database instance** — not shared with other test workloads, staging consumers, or CI pipelines. No concurrent schema migrations, backups, or analytics queries during test window
- **No concurrent CI jobs** — dedicated test agent, no parallel test suites running on the same database
- **Dedicated API host** — the endpoint under test runs on an isolated server/container with no other workloads, no shared CPU quota
- **No other tenants** — test environment is single-tenant during the test window. No production traffic, no other staging consumers
- **Predictable background processes** — if background jobs must run, schedule them outside the test window. Document any that run during test
- **Network isolation** — if possible, use a private network for test ↔ database communication (avoid shared load balancers, CDNs, or firewalls that rate-limit)

**Why this matters:** If your test database shares a server with production analytics queries, your "Stress 3×" test result includes noise from that other workload. You'll measure 600ms when the endpoint really performs at 400ms. Isolation removes that noise.

### Pre-flight Infrastructure Check

Before running any test, verify:

1. **k6 version:** `k6 version` → expect v0.48+
2. **Target environment URL:** Confirm API endpoint is reachable and responsive (`curl -I https://api.example.com/search?q=test`)
3. **Monitoring dashboard:** Have Grafana/CloudWatch/Datadog open with:
   - Server CPU utilisation (API process)
   - Server RSS memory (API process)
   - Database active connection count
   - GC pause duration (if app is Java/.NET/Python with GC)
   - Error log rate (log aggregator or syslog)
   - Endpoint p50/p95/p99 latency (from APM or k6 results)
4. **Data seeding:** Confirm 5M records present in search database: `SELECT COUNT(*) FROM [table];` → expect ~5M
5. **Clean baseline:** No existing load on the environment. Verify recent metrics show idle CPU and memory
6. **Database indexes:** Confirm indexes on `q` (search term) and `page` are present and healthy
7. **API health check:** `GET /health` or equivalent → expect 200 OK

## Step 7: Execution Plan

### Monitoring Owner and Responsibilities

**Role:** Performance Engineer on duty (or DevOps Lead if dedicated PE unavailable)

**Responsibilities during test execution:**

| Test phase | Duration | Metrics to track | Sampling interval | Alert thresholds |
|---|---|---|---|---|
| **Baseline** | 5 min | p50/p95/p99 latency, error rate, CPU, RSS, DB connections | Every 30s | CPU > 80%, errors > 0.5% |
| **Stress 3×** | 30 min | p50/p95/p99 latency, error rate, CPU, RSS, DB connections, GC pauses | Every 1 min | p95 > 1.5s, errors > 0.5%, CPU > 85% |
| **Stress breaking** | 20 min | p95/p99 latency (primary), error rate, CPU saturation point | Every 30s | Error rate spike → note RPS at failure |
| **Endurance** | 4 hours | RSS trend (monotonic increase?), DB connections trend, GC pause frequency, error rate, latency (sampled hourly) | Every 30 min | RSS increase > 10% per hour → leak likely |
| **Spike** | 7 min | Latency recovery time, queue depth (if observable), auto-scaling trigger, error rate post-spike | Every 5s during spike, every 30s recovery | Recovery > 120s → flag as slow |

**Key metrics to record from k6 output:**
- `http_req_duration` (p50, p95, p99)
- `http_req_failed` (request error count)
- `http_reqs` (total requests)
- `vus` (virtual users active)
- `vus_max` (peak VUs reached)

**Operator actions during test:**
- 📊 Watch dashboards continuously — do not rely on post-run analysis alone
- 📝 Note any anomalies in real-time (log lines with timestamps: "12:34 CPU spiked to 92% during stress_3x")
- 🚨 If CPU/memory hit 95%+ or error rate spikes above threshold, note the exact RPS when it happened
- 📄 Screenshot/export monitoring dashboard at test end for correlation with k6 metrics

### Results Storage and Comparison

- **k6 output format:** JSON (`k6 run --out json=results.json search-load-test.js`) and summarised text output
- **Storage location:** `load-tests/results/` directory in repo (gitignored for large JSON files; summary markdown committed)
- **Baseline comparison:** Compare p95/p99 to previous baseline run. Flag any regression > 10%
- **Breaking point record:** Document exact RPS where p99 crossed 2× baseline or error rate hit 1% — this becomes your safe ceiling for future capacity planning

---

# Load Test Plan: GET /api/search?q=&page=&size=

## Target

- **System:** Search API endpoint
- **Endpoint:** `GET /api/search?q={query}&page={number}&size={pageSize}`
- **Current production load:** 50 rps peak
- **Baseline response time:** 180ms average (p50)
- **Database:** 5 million records (PostgreSQL or similar, with full-text search indexes)
- **Dependencies:** Search database (indexed), no external APIs

## Scenarios

| Scenario | VUs | Duration | Load pattern | Success criteria | Primary metric |
|---|---|---|---|---|---|
| **Baseline** | 50 | 5 min | Constant 50 rps | p95 < 800ms, errors < 0.1%, no CPU > 80% | Establish performance baseline |
| **Stress (3× target verification)** | 150 | 30 min | Constant 150 rps | p95 < 800ms, errors < 0.1%, graceful under load | Verify 3× target sustainable |
| **Stress (breaking point)** | 150→1000 | 20 min | Linear ramp 150→1000 rps | Find where p99 > 720ms OR error rate > 1% | Identify exact breaking point |
| **Endurance (memory leak detection)** | 100 | 4 hours | Constant 100 rps | RSS stable (no > 10% increase per hour), p95 stable, error rate < 0.1% | Detect memory leak or connection exhaustion |
| **Spike** | 500 (sudden) | 2 min spike + 5 min recovery | Step: 50→500→50 rps | Recover to p95 < 800ms within 60s, no requests dropped during descent | Test auto-scaling and recovery |

## Thresholds

| Metric | Baseline | Stress 3× | Breaking point | Endurance | Spike |
|---|---|---|---|---|---|
| **p50 latency** | < 250ms | < 250ms | documented | < 250ms (stable) | < 250ms within 60s recovery |
| **p95 latency** | < 800ms | < 800ms | < 1500ms | < 800ms (stable) | < 800ms within 60s recovery |
| **p99 latency** | < 2000ms | < 2000ms | **FIND (expect ~500–1000 rps)** | < 2000ms (stable) | < 2000ms within 60s recovery |
| **Error rate** | < 0.1% | < 0.1% | **FIND (when >1%)** | < 0.1% | < 1% during spike, < 0.1% after |
| **CPU utilisation** | < 70% | < 70% | ramp to saturation | < 70% (stable, no drift) | returns to < 70% within 120s |
| **Memory (RSS)** | baseline | < +5% | monitor | **NO MONOTONIC INCREASE** | returns to baseline |
| **Request count** | ≥ 15,000 | ≥ 270,000 | varies | ≥ 1.4M | ≥ 15,000 total |

## Data & Query Distribution

**Production-like data:** 5 million records seeded via:
- **Approach A (recommended):** Anonymised production snapshot (remove PII, hash user IDs, shuffle timestamps)
- **Approach B:** `pgbench -i -s 500` generator (creates ~5M+ rows across standard tables)

**Query parameter distribution:**
- **q (search term):** 100 representative terms distributed by popularity:
  - 40% popular terms (e.g., "docker", "kubernetes", "Python", "API")
  - 40% mid-tail terms (e.g., "flux capacitor", "load balancing", "async patterns")
  - 20% long-tail terms (rare/specific queries)
  - File: `queries.json` (pre-computed, loaded into SharedArray in k6)
  
- **page (pagination):** Zipfian distribution (realistic — users rarely go past page 1):
  - 80% page 1
  - 15% pages 2–5
  - 5% pages 6+
  
- **size (page size):** Constant 20 (realistic default)

**Think time:** `sleep(randomBetween(1, 3))` between iterations (users don't fire requests without pause)

## k6 Script

See `search-load-test.js` above. Key sections:

```javascript
// Thresholds with p50, p95, p99
thresholds: {
  'http_req_duration': [
    'p(50) < 250',
    'p(95) < 800',
    'p(99) < 2000',
  ],
  'http_req_failed': ['rate < 0.01'],
  'http_reqs': ['count > 9000'],
}

// Checks
check(res, {
  'status is 200': (r) => r.status === 200,
  'has results array': (r) => Array.isArray(r.json('results')),
  'response time < 500ms': (r) => r.timings.duration < 500,
});

// Think time
sleep(Math.random() * 2 + 1);  // 1–3 seconds
```

## Environment

- **Target URL:** `https://api.example.com/search` (set `API_URL` env var)
- **Data volume:** 5 million records (verified pre-test: `SELECT COUNT(*) FROM search_index;`)
- **Isolation:** **Dedicated database instance, dedicated API host, no concurrent CI jobs, no background workloads during test window**
- **Monitoring:** Grafana/CloudWatch dashboard with CPU, RSS, DB connections, p50/p95/p99 latency
- **Pre-flight checks:**
  - k6 version ≥ 0.48
  - API endpoint responds: `curl -I https://api.example.com/search?q=test` → 200
  - Database health: `SELECT COUNT(*) FROM search_index;` → ≥ 5,000,000
  - Monitoring dashboard open and ready (CPU, memory, error logs, latency percentiles)
  - Clean baseline (no existing load, CPU < 10%, memory stable)

## Execution Plan

### Schedule

| Test | Time window | Duration | Monitor |
|---|---|---|---|
| **Baseline** | 09:00 | 5 min | Performance Engineer (on duty) |
| **Stress 3×** | 09:05 | 30 min | Performance Engineer + optional DevOps observer |
| **Breaking point** | 09:35 | 20 min | Performance Engineer (primary observer — note RPS at failure) |
| **Endurance** | 09:55 | 4 hours | DevOps lead (spot-check every 1 hour, automated alerting on RSS trend) |
| **Spike** | 13:55 | 7 min | Performance Engineer (watch recovery in real-time) |

**Total time:** ~5.5 hours. Schedule in off-peak or isolated lab window.

### Monitoring Owner

**Role:** Performance Engineer on duty (escalate to DevOps lead for endurance phase).

**Responsibilities:**
- Watch live dashboard (Grafana/CloudWatch) throughout each test
- Record sampled metrics every 30s–1 min (CPU %, RSS MB, DB connections, error rate, p50/p95/p99 latency)
- Note exact RPS when p99 crosses 720ms (2× baseline) or error rate hits 1% during breaking-point test
- Flag any anomalies: CPU spikes, memory jumps, GC pauses, connection pool exhaustion
- During endurance: check RSS trend every hour — alert if monotonically increasing > 10% per hour (memory leak)
- Post-test: export k6 JSON results and dashboard screenshots; correlate latency spikes with server metrics

### Results & Comparison

- **Output:** k6 results stored in `load-tests/results/search-load-test-[date].json`
- **Summary:** Markdown report in `load-tests/reports/search-load-test-[date].md` with:
  - p50/p95/p99 latencies per scenario
  - Error rate and failed request count
  - Breaking point RPS (where p99 crossed 2× baseline)
  - Server resource utilisation (CPU peak, RSS final/trend)
  - Recommendations (capacity increase? index optimisation? caching layer?)
- **Baseline comparison:** Compare p95/p99 to last run; flag regressions > 10%
- **Regression detection:** Automated — k6 thresholds fail the build if p95 > 800ms or error rate > 1%

---

**Next step:** Run pre-flight checks, seed database with 5M records, then execute tests sequentially. Spike test is the most critical for detecting auto-scaling and recovery issues — watch it live.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/17.5 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 64302 ms |
| Target cost | $0.0813 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill designs all four test types: baseline, stress, endurance, and spike — with distinct VU counts, durations, and load patterns for each | PASS | Output presents five named scenarios in the Step 2 table and the formal plan table: Baseline (50 rps, 5 min, constant), Stress 3× (150 rps, 30 min, constant), Stress breaking point (150→1000 rps, 20 min, linear ramp), Endurance (100 rps, 4 hours, constant), Spike (50→500→50 rps, 2+5 min, step function) — all four mandatory types present with distinct VU counts, durations, and patterns. |
| c2 | Skill specifies using production-like data volume (5 million records) — not an empty test database | PASS | Step 3 opens with 'Production-like data volume (required): 5 million records' and offers two seeding approaches. Pre-flight checks include 'SELECT COUNT(*) FROM search_index; → ≥ 5,000,000'. |
| c3 | Skill includes think time in the k6 script — not zero think time between requests | PASS | The k6 script includes `sleep(__ENV.THINK_TIME \|\| Math.random() * 2 + 1);` and the Data & Query Distribution section states 'Think time: sleep(randomBetween(1, 3)) between iterations (users don't fire requests without pause)'. |
| c4 | Success criteria (p50, p95, p99 thresholds and error rate) are defined BEFORE running the tests | PASS | The k6 thresholds block defines `p(50) < 250`, `p(95) < 800`, `p(99) < 2000` per scenario and `http_req_failed: rate < 0.01`. Step 5 and the formal Thresholds table both appear before the Execution Plan section. |
| c5 | Endurance test duration is at least 1 hour to detect the suspected memory leak | PASS | Endurance scenario is 'constant-vus, 100 vus, duration: 4h' — 4 hours, well above the 1-hour minimum. |
| c6 | k6 script skeleton includes both `check()` for response validation and `thresholds` for automated pass/fail | PASS | The k6 script shows `check(res, { 'status is 200': ..., 'has results array': ..., 'response time < 500ms': ... })` and a full `thresholds:` block with per-scenario duration rules plus `http_req_failed` and `http_reqs` keys. |
| c7 | Skill specifies an isolated environment requirement — shared staging produces unreliable results | PASS | Step 6 contains '⚠️ CRITICAL: Shared staging environments produce unreliable, noisy results. You MUST test in an isolated environment.' with a bulleted definition of what 'Isolated' means. |
| c8 | Skill addresses the realistic request mix — search queries should vary (not repeat the same query, which would be cached) | PARTIAL | Output specifies a `queries.json` SharedArray of ~100 representative terms with a three-tier popularity split (40% popular, 40% mid-tail, 20% long-tail) and Zipfian page distribution. The k6 script randomises selection via `queries[Math.floor(Math.random() * queries.length)]`. Comprehensively addresses the caching concern. |
| c9 | Output includes scenarios table, thresholds table, environment requirements, and execution plan with monitoring owner | PASS | Scenarios table appears in Step 2 and the formal plan. Thresholds table appears in Step 5 and the formal plan. Environment section (Step 6) lists isolation, pre-flight checks, monitoring dashboard. Execution Plan names 'Performance Engineer on duty' as monitoring owner. |
| c10 | Output's scenarios table includes all four test types — baseline (~50 rps), stress (150 rps and beyond to find the breaking point), endurance (sustained, ≥1 hour for the suspected memory leak), spike — with distinct VU counts, durations, and ramp profiles per type | PASS | The formal Scenarios table lists Baseline (50 VUs, 5 min, constant), Stress 3× (150 VUs, 30 min, constant), Stress breaking point (150→1000, 20 min, linear ramp), Endurance (100 VUs, 4 hours, constant), Spike (500 sudden, 2+5 min, step). All four mandatory types with distinct profiles. |
| c11 | Output's stress test ramps past 150 rps to find the actual breaking point (e.g. step up by 25 rps at intervals until error rate or latency thresholds are exceeded), not just confirming 150 rps works | PASS | 'Stress (breaking point)' scenario ramps from 150 to 1000 rps over 20 minutes with the explicit goal: 'Find where p99 crosses 2× baseline (360ms) or error rate hits 1%? — Identify exact breaking point'. The k6 script shows `ramping-vus` from 150 to target 1000. |
| c12 | Output specifies the database must contain ~5 million records (production-like volume) for the search endpoint to behave realistically, and that an empty test database is unacceptable | PASS | Step 3: 'Production-like data volume (required): 5 million records'. Data section states 'Production-like data: 5 million records seeded via...' and pre-flight check mandates `SELECT COUNT(*) FROM search_index; → ≥ 5,000,000`. The requirement framing ('MUST contain') makes an empty DB unacceptable by implication. |
| c13 | Output's k6 script uses non-zero think time between iterations and varies the search query (`q`) across a realistic distribution rather than repeating the same query (which Postgres would cache and inflate results) | PASS | `sleep(__ENV.THINK_TIME \|\| Math.random() * 2 + 1)` provides 1–3s think time. `const q = queries[Math.floor(Math.random() * queries.length)]` randomly selects from 100 terms in a SharedArray, providing realistic query variance. |
| c14 | Output's success criteria are defined BEFORE running tests — explicit p50, p95, p99 latency thresholds and an error rate ceiling — and are encoded in k6 `thresholds` for automated pass/fail | PASS | k6 `thresholds` block encodes `p(50) < 250`, `p(95) < 800`, `p(99) < 2000` per scenario tag and `http_req_failed: rate < 0.01`. Thresholds are defined in the plan sections preceding the Execution Plan. |
| c15 | Output's k6 script skeleton uses both `check()` (per-response correctness validation) and `thresholds` (aggregate pass/fail), shown as code, not just described | PASS | Full k6 script code block shows both: `check(res, { 'status is 200': ..., 'has results array': ..., 'response time < 500ms': ... })` and the `thresholds:` config object. A second code snippet in the formal plan section repeats both for emphasis. |
| c16 | Output requires an isolated environment with no other workloads — production or shared staging produces noisy results — and names what 'isolated' means concretely (dedicated DB, no other consumers) | PASS | Isolation Requirement section enumerates: 'Dedicated database instance — not shared with other test workloads, staging consumers, or CI pipelines', 'No concurrent CI jobs', 'Dedicated API host', 'No other tenants', 'Predictable background processes', 'Network isolation'. The formal Environment section also states 'Dedicated database instance, dedicated API host, no concurrent CI jobs, no background workloads during test window'. |
| c17 | Output's endurance test runs at least 1 hour, with memory and connection-count monitoring at fixed intervals, so a leak can be detected as a monotonic upward trend | PASS | Endurance is 4 hours. Monitoring table row states: 'Every 30 min: RSS trend (monotonic increase?), DB connections trend, GC pause frequency, error rate, latency (sampled hourly)' and 'Alert if RSS increase > 10% per hour → leak likely'. |
| c18 | Output's execution plan names the monitoring owner and the metrics they track during each test (DB connection count, server memory, GC pauses, error logs) | PASS | Execution Plan names 'Performance Engineer on duty (escalate to DevOps lead for endurance phase)'. Responsibilities include tracking 'p50/p95/p99 latency, error rate, CPU, RSS, DB connections, GC pauses' during each phase, with specific per-phase sampling intervals and alert thresholds in the monitoring table. |

### Notes

The captured output comprehensively satisfies every criterion. All five required scenarios (including the mandatory distinct spike test with step-function load pattern) are present with correct labels, VU counts, durations, and ramp profiles. The k6 script is a working skeleton with both check() validation and a per-scenario thresholds block encoding p50, p95, and p99 — all three percentiles appear as automated pass/fail gates. Think time uses the required randomBetween(1,3) pattern. The isolation requirement section is thorough, naming dedicated DB instance, dedicated API host, and no concurrent CI as the concrete definition. The monitoring owner is named by role (Performance Engineer on duty) with a per-phase metrics table covering RSS, DB connections, GC pauses, and error log rate. The only ceiling constraint was c8 (PARTIAL max) which the output fully earned at 0.5/0.5. No gaps or omissions were found across the 18 criteria.
