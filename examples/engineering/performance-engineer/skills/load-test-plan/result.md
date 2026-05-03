# Load Test Plan

Scenario: Developer invokes the load-test-plan skill to design load tests for `/api/search` — a full-text search endpoint over a Postgres database with 5 million records, currently serving 50 requests/second at peak.

## Prompt

> Design a load test plan for `GET /api/search?q=&page=&size=`. Current production load: ~50 rps peak. The database has ~5 million records. Average response time is 180ms. We want to verify the endpoint handles 3x current load (150 rps) gracefully and find the breaking point. We also suspect there might be a memory leak under sustained load. Tool preference: k6.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll design a comprehensive load test plan following the process. Let me work through each step.

## Load Test Plan: Search API (`GET /api/search`)

### Step 1: Target Identification

**What we're testing:**
- Endpoint: `GET /api/search?q=<query>&page=<num>&size=<count>`
- Current production load: ~50 rps peak
- Database: ~5 million records
- Current avg response time: 180ms
- Primary goal: Handle 150 rps gracefully + detect memory leaks under sustained load

**Assumptions documented:**
- Search queries are I/O bound (hitting database)
- Database is a primary bottleneck (not external APIs)
- Query latency scales with result set size and database load
- No caching layer or minimal caching

---

### Step 2: Scenario Design

| Scenario | Purpose | VUs | Duration | Load pattern | Key findings |
|---|---|---|---|---|---|
| **Baseline** | Establish normal perf | 50 VUs | 5 min | Constant 50 rps | Confirm p95 < 500ms, error rate < 0.1% |
| **Stress** | Find breaking point | 0→150 VUs | 18 min | Linear ramp over 15 min | Where errors spike, latency degrades |
| **Endurance** | Detect memory leak | 100 VUs | 90 min | Constant 2x load (100 rps) | Memory trend stable, no degradation over time |
| **Spike** | Test recovery | 250 VUs spike | 10 min | Sudden 5x jump, then return | How long to recover to baseline latency |

**VU calculation:**
- 50 rps baseline with 180ms avg response time = ~9 concurrent users (rps × duration)
- Using 50 VUs gives safety margin for think time and realistic pacing

---

### Step 3: Realistic Data

**Search query set:** Vary by:
1. **Query complexity:** Mix of single-term and multi-term queries (80% simple, 20% complex)
2. **Result cardinality:** 
   - Hot queries (few results, e.g., rare terms): 20%
   - Medium queries (hundreds of results): 60%
   - Cold queries (thousands of results): 20%
3. **Pagination:** 
   - Page 1-5: 80% (most users don't go deep)
   - Page 6+: 20% (power users)
4. **Size parameter:** Mix 10, 25, 50 records per page

**Data setup:**
- Use anonymized production data or generate realistic search corpus (5M documents)
- Index must match production (same sharding, partitions, indexes)
- Pre-warm indexes before baseline starts

---

### Step 4: k6 Script

```javascript
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';
import { SharedArray } from 'k6/data';

// Realistic search queries with cardinality metadata
const queries = new SharedArray('queries', () => [
  { q: 'javascript', page: 1, size: 25 },
  { q: 'react hooks', page: 1, size: 25 },
  { q: 'database optimization', page: 1, size: 10 },
  { q: 'kubernetes', page: 2, size: 25 },
  { q: 'async await', page: 1, size: 25 },
  { q: 'machine learning', page: 1, size: 50 },
  { q: 'redis cache', page: 1, size: 25 },
  { q: 'test fixtures', page: 3, size: 10 },
  { q: 'memory profiling', page: 1, size: 25 },
  { q: 'ci cd pipeline', page: 1, size: 25 },
  // Add 90+ more realistic queries for your domain
]);

// Custom metrics for deep analysis
const searchLatency = new Trend('search_latency');
const memoryTrend = new Trend('memory_usage');
const errorsByType = new Counter('errors_by_type');

export const options = {
  scenarios: {
    baseline: {
      executor: 'constant-vus',
      vus: 50,
      duration: '5m',
      tags: { test_type: 'baseline' },
    },
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },    // ramp to baseline
        { duration: '10m', target: 150 },  // linear ramp to 3x
        { duration: '3m', target: 250 },   // push to 5x briefly to find hard limit
        { duration: '3m', target: 0 },     // ramp down gracefully
      ],
      startTime: '5m30s',
      tags: { test_type: 'stress' },
    },
    endurance: {
      executor: 'constant-vus',
      vus: 100,
      duration: '90m',
      startTime: '30m',
      tags: { test_type: 'endurance' },
    },
    spike: {
      executor: 'ramping-vus',
      startVUs: 50,
      stages: [
        { duration: '1m', target: 50 },    // baseline
        { duration: '30s', target: 250 },  // sudden 5x spike
        { duration: '5m', target: 250 },   // sustain spike
        { duration: '2m', target: 50 },    // recover to baseline
        { duration: '1m', target: 0 },     // ramp down
      ],
      startTime: '122m',
      tags: { test_type: 'spike' },
    },
  },
  thresholds: {
    // Baseline thresholds (most strict)
    'http_req_duration{test_type:baseline}': [
      'p(50)<200',      // p50 < 200ms
      'p(95)<500',      // p95 < 500ms
      'p(99)<1000',     // p99 < 1s
    ],
    'http_req_failed{test_type:baseline}': ['rate<0.001'], // < 0.1% errors
    
    // Stress thresholds (relaxed, we expect degradation)
    'http_req_duration{test_type:stress}': ['p(95)<2000'], // allow 2s at 5x load
    'http_req_failed{test_type:stress}': ['rate<0.05'],    // < 5% errors acceptable
    
    // Endurance: stability matters more than absolute latency
    'http_req_failed{test_type:endurance}': ['rate<0.001'],
    
    // Spike: recovery is key
    'http_req_failed{test_type:spike}': ['rate<0.01'],     // < 1% errors post-recovery
  },
  ext: {
    loadimpact: {
      // Optional: k6 Cloud integration for comparison
      name: 'Search API Load Test',
      tags: { service: 'api-search', version: 'v1' },
    },
  },
};

export default function () {
  const query = queries[Math.floor(Math.random() * queries.length)];
  const url = `http://localhost:8080/api/search?q=${encodeURIComponent(query.q)}&page=${query.page}&size=${query.size}`;

  const res = http.get(url, {
    headers: { 'User-Agent': 'k6-load-test' },
    tags: { endpoint: 'search' },
  });

  // Record latency
  searchLatency.add(res.timings.duration, { test_type: __ENV.TEST_TYPE || 'baseline' });

  // Check response validity
  const success = check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'body not empty': (r) => r.body && JSON.parse(r.body).results?.length > 0,
    'response has required fields': (r) => {
      const body = JSON.parse(r.body);
      return body.results && body.totalCount !== undefined;
    },
  });

  if (!success) {
    errorsByType.add(1, { status: res.status, scenario: __ENV.TEST_TYPE });
  }

  // Simulate realistic think time (users pause between searches)
  sleep(Math.random() * 2 + 0.5); // 0.5–2.5 seconds
}
```

---

### Step 5: Success Criteria

| Metric | Baseline Target | Stress Target | Endurance Target | Spike Target |
|---|---|---|---|---|
| **p50 latency** | < 200ms | < 800ms | < 200ms | < 500ms (post-recovery) |
| **p95 latency** | < 500ms | < 1500ms | < 500ms (stable) | < 500ms (post-recovery) |
| **p99 latency** | < 1000ms | < 3000ms | < 1000ms (stable) | < 1000ms |
| **Error rate** | < 0.1% | < 5% | < 0.1% | < 1% (post-recovery) |
| **Throughput at 150 rps** | — | ≥ 145 rps (98% success) | — | — |
| **Memory leak** | — | — | Δ memory < 5% over 90 min | — |
| **Recovery time** | — | — | — | < 2 minutes to baseline |

**Failure = any threshold breach. Action: Profile bottleneck (DB, app, network) and retest.**

---

### Step 6: Environment Requirements

**Isolation:**
- Dedicated database instance (not shared staging)
- Dedicated application instance
- No other load on the host
- Network: direct LAN connection or isolated VPC (no shared Internet gateway)

**Sizing:**
- Same hardware profile as production (CPU cores, RAM, network)
- If production is a cluster, test against equivalent (1 node for 1-node prod, 3-node cluster for 3-node prod)

**Monitoring setup (collect at 1-minute intervals):**
- **Host:** CPU %, memory %, disk I/O
- **Database:** active connections, queries/sec, avg query latency, index scans
- **Application:** heap usage, GC pauses, thread pool saturation
- **Network:** bandwidth, packet loss

**Pre-flight checklist:**
- [ ] Database indices match production
- [ ] Query cache warmed (or explicitly cold, documented)
- [ ] No other workloads running
- [ ] Monitoring agents active
- [ ] Baseline metrics normal
- [ ] k6 script validated with 1 VU

---

### Step 7: Execution Plan

| Test | When | Monitor | Owner | Metrics captured | Post-test action |
|---|---|---|---|---|---|
| **Baseline** | Day 1, morning | Dashboard live | [Name] | Latency percentiles, errors, CPU/memory baseline | Confirm p95 < 500ms; if failed, debug before stress |
| **Stress** | Day 1, after baseline | Dashboard + alerts | [Name] | Breaking point (rps where p95 > 2s or errors spike), CPU/memory peak | Document failure threshold; profile if < 150 rps |
| **Endurance** | Day 2, off-peak | Hourly snapshot of memory, DB conn count | [Name] | Memory Δ, latency stability, error rate | Plot memory over time; if upward trend, investigate leaks |
| **Spike** | Day 2, after endurance | Real-time dashboard | [Name] | Time to exceed p95, recovery duration, max latency | Confirm recovery < 2 min |

**Results storage:**
```bash
# Run all tests and export metrics
k6 run plan.js \
  --out json=results.json \
  --summary-export=summary.json
```

Store in repo: `/load-tests/results/2026-04-30/`

---

### Anti-Patterns to Avoid

❌ Testing with empty database (no results)  
❌ Zero think time (will show unrealistic peak)  
❌ Same query repeated (caches skew results)  
❌ Running on dev machine (different hardware)  
❌ No baseline (cannot detect regression)  
❌ No monitoring (CPU peaking but latency looks okay = premature conclusion)  

---

### Next Steps

1. **Prepare:** Set up isolated environment, populate with 5M test records, warm database.
2. **Validate:** Run baseline with 1 VU, then 5 VUs to smoke-test the script.
3. **Execute:** Run full plan (Day 1 baseline + stress, Day 2 endurance + spike).
4. **Analyze:** Compare to thresholds; if any fail, profile (CPU? DB? network?) and iterate.
5. **Document:** Commit results and learnings to repo.

**Related next skills:**
- `/performance-engineer:performance-profile` — if stress test reveals bottleneck, profile to find root cause
- `/performance-engineer:capacity-plan` — if 150 rps is achievable, use these results to validate capacity model

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.5/19.0 (97%) |
| Evaluated | 2026-04-30 |
| Target duration | 38707 ms |
| Target cost | $0.0410 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill designs all four test types: baseline, stress, endurance, and spike — with distinct VU counts, durations, and load patterns for each | PASS | Scenarios table shows Baseline (50 VUs, 5 min, constant), Stress (0→150 VUs, 18 min, linear ramp), Endurance (100 VUs, 90 min, constant), Spike (250 VUs spike, 10 min, sudden jump). All four have distinct VU counts, durations, and load patterns. |
| c2 | Skill specifies using production-like data volume (5 million records) — not an empty test database | PASS | Data setup section states 'generate realistic search corpus (5M documents)' and 'Index must match production'. Anti-patterns section explicitly lists '❌ Testing with empty database (no results)'. |
| c3 | Skill includes think time in the k6 script — not zero think time between requests | PASS | k6 script includes `sleep(Math.random() * 2 + 0.5); // 0.5–2.5 seconds` at the end of the default function, with comment 'Simulate realistic think time (users pause between searches)'. |
| c4 | Success criteria (p50, p95, p99 thresholds and error rate) are defined BEFORE running the tests | PASS | Step 5: Success Criteria table defines p50, p95, p99 latency and error rate targets for all four scenario types before the execution plan (Step 7). k6 thresholds block also encodes these as automated pass/fail. |
| c5 | Endurance test duration is at least 1 hour to detect the suspected memory leak | PASS | Endurance scenario is defined with `duration: '90m'` in both the scenarios table ('90 min') and the k6 script options, exceeding the 1-hour minimum. |
| c6 | k6 script skeleton includes both `check()` for response validation and `thresholds` for automated pass/fail | PASS | k6 script contains a `check(res, {...})` block validating status 200, response time, body not empty, and required fields. The `options` object contains a `thresholds` block with p50/p95/p99 and error rate thresholds per scenario tag. |
| c7 | Skill specifies an isolated environment requirement — shared staging produces unreliable results | PASS | Step 6: Environment Requirements states 'Dedicated database instance (not shared staging)', 'Dedicated application instance', 'No other load on the host', and 'Network: direct LAN connection or isolated VPC (no shared Internet gateway)'. |
| c8 | Skill addresses the realistic request mix — search queries should vary (not repeat the same query, which would be cached) | PARTIAL | Realistic Data section defines query distribution by complexity (80/20 simple/complex), result cardinality (hot/medium/cold), pagination depth, and size mix. k6 script uses SharedArray of 10 sample queries with random selection. Anti-patterns includes '❌ Same query repeated (caches skew results)'. However, only 10 sample queries are provided with a comment to 'Add 90+ more', which is incomplete for a truly robust distribution. |
| c9 | Output includes scenarios table, thresholds table, environment requirements, and execution plan with monitoring owner | PASS | Scenarios table in Step 2, Success Criteria thresholds table in Step 5, Environment Requirements section in Step 6, and Execution Plan table in Step 7 which includes an 'Owner' column with '[Name]' placeholder and 'Monitor' column per test. |
| c10 | Output's scenarios table includes all four test types — baseline (~50 rps), stress (150 rps and beyond to find the breaking point), endurance (sustained, ≥1 hour for the suspected memory leak), spike — with distinct VU counts, durations, and ramp profiles per type | PASS | Step 2 table: Baseline (50 VUs, 5 min, constant 50 rps), Stress (0→150 VUs, 18 min, linear ramp), Endurance (100 VUs, 90 min, constant 2x load), Spike (250 VUs spike, 10 min, sudden 5x jump then return). Each has distinct VU count, duration, and load pattern. |
| c11 | Output's stress test ramps past 150 rps to find the actual breaking point (e.g. step up by 25 rps at intervals until error rate or latency thresholds are exceeded), not just confirming 150 rps works | PASS | Stress scenario in k6 script ramps to 150 VUs then continues to 250 VUs ('push to 5x briefly to find hard limit'). Scenarios table notes 'Where errors spike, latency degrades' as key finding. The plan explicitly goes beyond 150 rps to 250 VUs to find the breaking point. |
| c12 | Output specifies the database must contain ~5 million records (production-like volume) for the search endpoint to behave realistically, and that an empty test database is unacceptable | PASS | Data setup: 'Use anonymized production data or generate realistic search corpus (5M documents)'. Anti-patterns: '❌ Testing with empty database (no results)'. Both positive requirement and negative constraint are explicit. |
| c13 | Output's k6 script uses non-zero think time between iterations and varies the search query (`q`) across a realistic distribution rather than repeating the same query (which Postgres would cache and inflate results) | PASS | Script uses `sleep(Math.random() * 2 + 0.5)` for think time and `queries[Math.floor(Math.random() * queries.length)]` to randomly select from a SharedArray of varied queries covering different terms, pages, and sizes. |
| c14 | Output's success criteria are defined BEFORE running tests — explicit p50, p95, p99 latency thresholds and an error rate ceiling — and are encoded in k6 `thresholds` for automated pass/fail | PASS | Step 5 success criteria table defines p50/p95/p99 and error rate for all scenarios. k6 options.thresholds encodes these as `'http_req_duration{test_type:baseline}': ['p(50)<200', 'p(95)<500', 'p(99)<1000']` and `'http_req_failed{test_type:baseline}': ['rate<0.001']`. |
| c15 | Output's k6 script skeleton uses both `check()` (per-response correctness validation) and `thresholds` (aggregate pass/fail), shown as code, not just described | PASS | Full k6 code block shown. `check(res, {'status is 200': ..., 'response time < 500ms': ..., 'body not empty': ..., 'response has required fields': ...})` for per-response validation. `thresholds` block in options for automated aggregate pass/fail. Both are shown as actual code. |
| c16 | Output requires an isolated environment with no other workloads — production or shared staging produces noisy results — and names what 'isolated' means concretely (dedicated DB, no other consumers) | PASS | Step 6 specifies: 'Dedicated database instance (not shared staging)', 'Dedicated application instance', 'No other load on the host', 'Network: direct LAN connection or isolated VPC (no shared Internet gateway)'. Concrete definitions of isolation provided. |
| c17 | Output's endurance test runs at least 1 hour, with memory and connection-count monitoring at fixed intervals, so a leak can be detected as a monotonic upward trend | PASS | Endurance test is 90 min. Monitoring section specifies 'collect at 1-minute intervals' for 'memory %' and 'Database: active connections'. Execution plan states 'Hourly snapshot of memory, DB conn count' for endurance. Success criteria tracks 'Δ memory < 5% over 90 min'. |
| c18 | Output's execution plan names the monitoring owner and the metrics they track during each test (DB connection count, server memory, GC pauses, error logs) | PASS | Step 7 execution plan table has 'Owner' column ('[Name]' placeholder), 'Monitor' column (e.g., 'Dashboard live', 'Dashboard + alerts', 'Hourly snapshot of memory, DB conn count'), and 'Metrics captured' column specifying latency percentiles, errors, CPU/memory baseline, breaking point rps, memory Δ, latency stability per test type. |

### Notes

The captured output is exceptionally comprehensive, addressing all 18 criteria with specific evidence. The only criterion not at full PASS was c8 (realistic request mix, capped at PARTIAL by the test), where the output provides a solid distribution strategy and 10 sample queries with a note to add 90+ more — meeting the spirit but not providing a complete realistic corpus. All other criteria are fully met: four distinct test types with proper VUs/durations/ramp profiles, 5M record requirement with empty-DB anti-pattern explicitly called out, non-zero think time with random query selection, pre-defined p50/p95/p99 thresholds encoded in k6 thresholds block, 90-minute endurance test with interval monitoring, isolated environment concretely defined, and execution plan with owner and metrics columns.
