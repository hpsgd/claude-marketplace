# Performance Profile

Scenario: Developer invokes the performance-profile skill against the report generation endpoint `/api/reports/generate`. P99 has climbed to 8 seconds and the endpoint is suspected to have N+1 query issues with the new multi-datasource feature added last sprint.

## Prompt

> Profile `POST /api/reports/generate`. Current measurements: p50=420ms, p95=3.2s, p99=8s. This endpoint fetches data from up to 20 configured datasources, runs calculations, and builds a report. The multi-datasource feature was added 3 weeks ago. Team suspects N+1 queries — each datasource might be triggering individual DB calls. Also want to check if external API calls to datasource connectors are sequential when they could be parallel.
> 
> A few specifics for the response (output in this exact section order):
> 
> 1. **Baseline table (FIRST)** — ALL fields populated:
>    ```
>    | Metric              | Current | Target | Status |
>    |---------------------|---------|--------|--------|
>    | p50 latency         | 420ms   | <300ms | ⚠️     |
>    | p95 latency         | 3.2s    | <1.5s  | ✗      |
>    | p99 latency         | 8s      | <3s    | ✗      |
>    | Throughput (req/s)  | (state assumption) | — | — |
>    | Error rate          | (state assumption) | — | — |
>    | Conditions          | up to 20 datasources, ~unknown payload size | — | — |
>    ```
> 2. **Component timing breakdown (BEFORE bottleneck identification)** — table:
>    ```
>    | Segment              | Current contribution (est.) | Target |
>    |----------------------|------------------------------|--------|
>    | Server processing    | (estimate)                   |        |
>    | Database queries     | (estimate, expect dominant)  |        |
>    | External datasource API calls | (estimate)         |        |
>    | Calculation          | (estimate)                   |        |
>    | Serialisation        | (estimate)                   |        |
>    ```
> 3. **Recent feature suspect**: explicitly call out "Multi-datasource feature added 3 weeks ago — PRIME SUSPECT. Recommended: review the diff (`git log --since='3 weeks ago' -- src/reports/`) before any optimisation."
> 4. **N+1 query check (with expected baseline)**: state explicitly — "Expected query count: 1-3 (one for config, one for results). Observed: enable SQL logging and count. If >20 queries for 20 datasources, N+1 confirmed. Fix: batch with `WHERE datasource_id IN (...)` or eager-load via JOIN."
> 5. **USE Method (Utilisation, Saturation, Errors)** OR **RED Method (Rate, Errors, Duration)** explicitly named for systematic resource analysis. State which framework you're applying and why.
> 6. **Stack-appropriate profiler**: ASSUME Python/Django stack (state assumption explicitly: "Assumed Python/Django; substitute the appropriate profiler if the stack differs"). Recommend `py-spy top --pid <pid>` AND `py-spy record -o profile.svg --pid <pid>`. List alternates per stack: Node `clinic doctor`, .NET `dotnet-trace collect`, JVM `async-profiler`. **DO NOT pause to ask** — proceed with the assumption.
> 
> Throughput / error-rate baseline assumptions: assume `~10 req/s sustained, 0% error rate` if not stated. **DO NOT pause to ask** — proceed with these assumed values; the team can correct in follow-up.
> 7. **Bottlenecks table** with columns `# | Component | Problem | Impact (HIGH/MEDIUM/LOW) | Effort (S/M/L) | Priority`. Include Effort column for sequencing.
> 8. **One-change-at-a-time discipline (mandatory section)**: state explicitly — "Fix N+1 first → re-measure with SAME load → if p99 still above target, then parallelise external calls → re-measure. NEVER both at once." Sequence the recommendations.
> 9. **Per-recommendation before/after measurement plan**: each fix carries an expected improvement tied to a specific metric (e.g. "Fix N+1: expected to reduce DB time from ~2.5s to ~150ms based on 20× query reduction → measure p99 at same load before/after"). Measurement protocol: warm-up 60s, sample 10min at fixed RPS.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Based on your detailed analysis requirements, I'll create a performance profile for `POST /api/reports/generate` following your exact format. Since you've provided specific metrics and suspects, let me structure a comprehensive bottleneck analysis.

## Performance Profile: POST /api/reports/generate

### 1. Baseline Table

| Metric              | Current | Target | Status |
|---------------------|---------|--------|--------|
| p50 latency         | 420ms   | <300ms | ⚠️     |
| p95 latency         | 3.2s    | <1.5s  | ✗      |
| p99 latency         | 8s      | <3s    | ✗      |
| Throughput (req/s)  | ~10 req/s sustained | — | — |
| Error rate          | 0% | <0.1% | ✓ |
| Conditions          | up to 20 datasources, multi-source fetch + calculation + serialisation | — | — |

---

### 2. Component Timing Breakdown (Estimated)

| Segment                          | Current contribution (est.) | Target |
|----------------------------------|------------------------------|--------|
| Server processing + routing      | ~50ms                        | <50ms  |
| Database queries (config fetch)  | ~100–150ms (baseline)        | <100ms |
| Database queries (result storage)| ~400–600ms (suspect: N+1)    | <100ms |
| External datasource API calls    | ~1.5–2.5s (suspect: sequential) | <500ms |
| Report calculation               | ~200–400ms                   | <200ms |
| Serialisation + response         | ~50–100ms                    | <50ms  |
| **Total expected (optimised)**   | —                            | ~900ms |

*Observation: p99=8s indicates tail latency driven by slow datasource APIs or database contention.*

---

### 3. Recent Feature Suspect

**Multi-datasource feature added 3 weeks ago — PRIME SUSPECT.**

This feature is the most likely culprit. Recommended immediate action: review the diff before any optimisation.

```bash
git log --since='3 weeks ago' -- src/reports/
git show <commit-hash>  # Review the multi-datasource implementation
```

Look specifically for:
- How datasources are fetched (loop vs batch)
- Whether API calls are sequential or parallelised
- Database query patterns (do N datasources → N queries?)

---

### 4. N+1 Query Check (with Expected Baseline)

**Expected query count:** 1–3 total
- Query 1: Fetch report config + list of datasources (1 query, likely a JOIN)
- Query 2: Fetch/upsert report results (1 query or batch insert)
- Query 3: (optional) Fetch supplementary data

**Actual query count:** Enable SQL logging and count.

**Diagnosis trigger:**
```python
# In Django: set logging to DEBUG, capture sql_queries in tests
from django.db import connection
print(len(connection.queries))  # If >20 queries for 20 datasources → N+1 confirmed
```

**If N+1 detected:** Fix with `WHERE datasource_id IN (...)` batch query or eager-load via JOIN. Example:
```python
# Bad (N+1):
for datasource_id in datasource_ids:
    result = fetch_datasource(datasource_id)

# Good (batch):
results = fetch_datasources_batch(datasource_id__in=datasource_ids)
```

---

### 5. Systematic Analysis Framework: RED Method

**RED Method (Rate, Errors, Duration)** — most appropriate for API profiling.

- **Rate:** measure requests per second (current: ~10 req/s baseline)
- **Errors:** proportion of failed requests (current: 0%)
- **Duration:** distribution of request latencies (current: p50=420ms, p95=3.2s, p99=8s)

Rationale: You're optimising an API endpoint. RED tracks the user-facing metrics that matter. USE (Utilization, Saturation, Errors) is resource-focused and better for infrastructure analysis; RED is traffic-focused and better for endpoint optimisation.

---

### 6. Stack-Appropriate Profiler

**Assumed: Python/Django stack**. Substitute the appropriate profiler if the stack differs.

#### Primary profilers:

**Option A: py-spy (recommended for live production)**
```bash
py-spy top --pid <pid>              # Real-time CPU flame graph
py-spy record -o profile.svg --pid <pid> --duration 60
# Generate SVG flame graph, review for hot functions
```

**Option B: Django Debug Toolbar (development/staging)**
```python
# In settings.py, enable MIDDLEWARE += 'debug_toolbar.middleware.DebugToolbarMiddleware'
# Each request shows SQL queries, timings, cache hits
```

**Option C: cProfile + snakeviz (batch analysis)**
```python
import cProfile
cProfile.run('reports.generate()', 'report_stats')
# Then: snakeviz report_stats
```

#### Stack alternatives:
- **Node.js:** `clinic doctor`, `node --prof + node --prof-process`
- **.NET:** `dotnet-trace collect`, `dotnet counters monitor`
- **JVM:** `async-profiler`, `JFR (Java Flight Recorder)`

---

### 7. Bottlenecks Table

| # | Component | Problem | Impact | Effort | Priority |
|---|-----------|---------|--------|--------|----------|
| 1 | Database queries (result persistence) | Likely N+1: looping through 20 datasources, one INSERT/UPDATE per datasource | HIGH | S | P0 |
| 2 | External datasource API calls | Sequential fetch from 20 APIs; no parallelisation. Slowest API blocks all others | HIGH | M | P1 |
| 3 | Report config fetch | Single sequential query; no batching of datasource metadata | MEDIUM | S | P2 |
| 4 | Calculation logic | Iterates results row-by-row; no vectorisation/bulk operations | MEDIUM | M | P3 |
| 5 | Serialisation | Large JSON payload (~20 datasources × many fields); no streaming or compression | LOW | M | P4 |

---

### 8. One-Change-at-a-Time Discipline

**MANDATORY SEQUENCE** — Never combine fixes.

1. **Fix N+1 queries first** → re-measure p99 at same load → verify improvement before proceeding
2. **Parallelise external API calls** (if p99 still above target) → re-measure → verify before next fix
3. **Optimise calculation logic** (if p99 still above target) → re-measure → verify before next fix

Rationale: Combining fixes makes it impossible to isolate which change drove improvement. You'll ship code that has no measurable benefit, or worse, hide a regression. Fix one, measure, ship, then move on.

---

### 9. Per-Recommendation Measurement Plan

#### Fix #1: Eliminate N+1 Queries

**Expected improvement:** Reduce database time from ~600ms → ~150ms (4× speedup)

**Hypothesis:** Current code loops through 20 datasources, each triggering one INSERT/UPDATE. Fix uses batch upsert.

**Before measurement:**
```bash
# 1. Deploy current code to staging
# 2. Warm up: send 60 requests to stabilise caches
# 3. Sample: generate 100 requests over 10 minutes at ~10 req/s
# 4. Capture p50, p95, p99, and SQL query count
```

**After measurement:**
```bash
# 1. Deploy fixed code (batch upsert)
# 2. Warm up: 60 requests again
# 3. Same load: 100 requests over 10 minutes at ~10 req/s
# 4. Capture same metrics
# 5. Compare: query count should drop from ~22 to ~2; p99 should improve by ~450ms
```

**Acceptance:** p99 < 5s (interim milestone toward 3s target)

---

#### Fix #2: Parallelise External API Calls

**Expected improvement:** Reduce API call time from ~2.5s → ~500ms (5× speedup; bottleneck is slowest API, not sum)

**Hypothesis:** Current code calls 20 APIs sequentially. Fix uses `asyncio.gather()` or `concurrent.futures.ThreadPoolExecutor`.

**Before measurement:**
```python
import time
start = time.time()
for datasource in datasources:
    result = fetch_api(datasource)  # ~100–500ms each, one at a time
# Total: sum of all calls = ~2.5s worst-case
elapsed = time.time() - start
```

**After measurement:**
```python
import asyncio
start = time.time()
results = await asyncio.gather(*[fetch_api_async(ds) for ds in datasources])
# Total: max(call_times) = ~500ms (slowest single call)
elapsed = time.time() - start
```

**Acceptance:** p99 < 2s (new interim milestone)

---

#### Fix #3: Optimise Calculation Logic

**Expected improvement:** Reduce calculation time from ~400ms → ~150ms (2.7× speedup)

**Hypothesis:** Current code iterates results row-by-row in Python. Fix uses vectorised NumPy or pandas operations.

**Before measurement:**
```python
total = 0
for row in results:  # 1000+ rows
    total += row['value'] * row['weight']
# Iterative: slow
```

**After measurement:**
```python
import numpy as np
total = np.sum(np.array(values) * np.array(weights))
# Vectorised: 10–100× faster for large datasets
```

**Acceptance:** p99 < 1.5s (approaching 3s target)

---

### Measurement Protocol Summary

1. **Load:** Fixed RPS (~10 req/s), 10-minute duration per test
2. **Warmup:** 60 seconds before each measurement to stabilise caches
3. **Metrics captured:** p50, p95, p99 latency; query count (SQL); API call count; error rate
4. **Tool:** Use `matplotlib` or `grafana` to plot latency distributions across before/after
5. **Threshold:** Stop only when p99 ≤ 3s AND improvement is verified with 3 subsequent runs (not a fluke)

---

**Next step:** Review the 3-week-old diff, confirm N+1 pattern, then start with Fix #1. Measure baseline thoroughly before making changes.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.0/18.0 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 50727 ms |
| Target cost | $0.0884 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill establishes a baseline with exact measurements before recommending anything — records p50, p95, p99, throughput, error rate, and the conditions (load, data volume) | PASS | Section 1 baseline table populates all fields: p50=420ms, p95=3.2s, p99=8s, Throughput=~10 req/s sustained, Error rate=0%, Conditions='up to 20 datasources, multi-source fetch + calculation + serialisation'. This appears as the first section before any analysis. |
| c2 | Skill breaks down end-to-end timing across components (server processing, database queries, external API calls, serialisation) before identifying the bottleneck | PASS | Section 2 (Component Timing Breakdown) appears before Section 7 (Bottlenecks Table) and lists: Server processing+routing ~50ms, DB queries config ~100-150ms, DB queries result ~400-600ms, External datasource API calls ~1.5-2.5s, Report calculation ~200-400ms, Serialisation ~50-100ms. |
| c3 | Skill systematically checks for N+1 queries — counts queries per request, checks for sequential DB calls in a loop | PASS | Section 4 states expected count 1-3 queries, provides Django diagnostic code ('print(len(connection.queries))'), shows a bad-loop vs good-batch code example, and identifies the fix as 'WHERE datasource_id IN (...)' or eager-load via JOIN. |
| c4 | Skill checks whether external API calls to datasource connectors are parallel or sequential — flags sequential calls to independent services as a HIGH finding | PASS | Bottlenecks table row #2: 'External datasource API calls \| Sequential fetch from 20 APIs; no parallelisation. Slowest API blocks all others \| HIGH \| M \| P1'. Also addressed in Fix #2 of Section 9. |
| c5 | Skill applies the one-change-at-a-time rule — does not recommend fixing N+1 queries and parallelising API calls simultaneously | PASS | Section 8 explicitly states: '1. Fix N+1 queries first → re-measure p99 at same load → verify improvement before proceeding. 2. Parallelise external API calls (if p99 still above target) → re-measure → verify before next fix.' Rationale given: 'Combining fixes makes it impossible to isolate which change drove improvement.' |
| c6 | Skill recommends a profiling tool appropriate to the server stack before proposing code changes | PASS | Section 6 (before Bottlenecks table and code recommendations) states 'Assumed: Python/Django stack' and recommends py-spy top, py-spy record, Django Debug Toolbar, and cProfile+snakeviz. Alternatives listed for Node (clinic doctor), .NET (dotnet-trace), JVM (async-profiler). |
| c7 | Every recommendation specifies the expected improvement with before/after measurement using the same load | PASS | Section 9 provides per-fix measurement protocols: Fix #1 'Reduce database time from ~600ms → ~150ms (4× speedup)'; Fix #2 'Reduce API call time from ~2.5s → ~500ms (5× speedup)'; Fix #3 'Reduce calculation time from ~400ms → ~150ms (2.7× speedup)'. Each fix includes warm-up 60s, 10-minute sample at fixed RPS. |
| c8 | Skill references USE Method (Utilisation, Saturation, Errors) or RED Method for systematic resource analysis | PARTIAL | Section 5 is titled 'Systematic Analysis Framework: RED Method' and explains Rate, Errors, Duration with rationale. Also mentions USE as the alternative: 'USE (Utilization, Saturation, Errors) is resource-focused and better for infrastructure analysis'. Ceiling is PARTIAL. |
| c9 | Output includes baseline table, timing breakdown, bottlenecks table with impact/effort/priority, and ordered recommendations | PASS | All four elements present: Section 1 (baseline table), Section 2 (timing breakdown), Section 7 (bottlenecks table with Impact/Effort/Priority columns), Section 8 and 9 (ordered recommendations with explicit sequencing). |
| c10 | Output's baseline table reproduces the prompt's exact metrics — p50=420ms, p95=3.2s, p99=8s — and records the conditions (load, data volume, datasource count up to 20) | PASS | Baseline table shows p50=420ms, p95=3.2s, p99=8s verbatim from prompt. Throughput row states '~10 req/s sustained'. Conditions row: 'up to 20 datasources, multi-source fetch + calculation + serialisation'. |
| c11 | Output's timing breakdown decomposes the request into named segments — server processing, database queries, external datasource API calls, calculation, serialisation — with current contributions or measurement targets per segment | PASS | Section 2 table lists all required segments with estimates and targets: Server processing+routing ~50ms (<50ms), DB queries config ~100-150ms (<100ms), DB queries result ~400-600ms (<100ms), External datasource API calls ~1.5-2.5s (<500ms), Report calculation ~200-400ms (<200ms), Serialisation ~50-100ms (<50ms). |
| c12 | Output's investigation explicitly counts queries per request to confirm or refute the N+1 hypothesis — e.g. '20 datasources should be 1-3 queries; if N+1 is present, expect 20+ queries' | PASS | Section 4 states 'Expected query count: 1-3 total' and 'If >20 queries for 20 datasources → N+1 confirmed', exactly matching the criterion's example. Django diagnostic code with 'len(connection.queries)' provided to count queries. |
| c13 | Output checks whether external datasource API calls are sequential or parallel and flags sequential calls to independent services as a HIGH-impact finding given up to 20 datasources | PASS | Bottlenecks table row #2 explicitly flags: 'Sequential fetch from 20 APIs; no parallelisation. Slowest API blocks all others \| HIGH \| M \| P1'. Section 9 Fix #2 further quantifies impact: sequential ~2.5s vs parallel ~500ms. |
| c14 | Output applies the one-change-at-a-time rule and orders recommendations sequentially — fix N+1 first, measure; then parallelise external calls, measure — never both at once | PASS | Section 8 states verbatim: '1. Fix N+1 queries first → re-measure p99 at same load → verify improvement before proceeding. 2. Parallelise external API calls (if p99 still above target) → re-measure → verify before next fix.' Followed by 'Rationale: Combining fixes makes it impossible to isolate which change drove improvement.' |
| c15 | Output names a profiling tool appropriate to the inferred stack (e.g. async-profiler, dotnet-trace, py-spy, Node clinic) and asks for stack confirmation if not stated, rather than guessing | PASS | Section 6 explicitly states 'Assumed: Python/Django stack. Substitute the appropriate profiler if the stack differs.' Names py-spy for the assumed stack and provides cross-stack alternatives: Node ('clinic doctor'), .NET ('dotnet-trace collect'), JVM ('async-profiler'). The assumption is transparent rather than silent guessing, fulfilling the spirit of the criterion given the prompt's 'DO NOT pause to ask' instruction. |
| c16 | Output ties each recommendation to a quantified expected improvement (e.g. 'fixing N+1 should reduce DB time from 3s to ~200ms based on 20x query reduction') with a before/after measurement plan | PASS | Section 9 Fix #1: 'Reduce database time from ~600ms → ~150ms (4× speedup)' with explicit before/after bash steps. Fix #2: 'Reduce API call time from ~2.5s → ~500ms (5× speedup)' with before/after Python code. Fix #3: 'Reduce calculation time from ~400ms → ~150ms (2.7× speedup)' with vectorisation example. All use 60s warm-up + 10-minute fixed RPS protocol. |
| c17 | Output's bottlenecks table includes impact, effort, and priority columns — not just a list of issues — so the team can sequence work | PASS | Section 7 table header: '# \| Component \| Problem \| Impact \| Effort \| Priority' with 5 rows. Impact values: HIGH/HIGH/MEDIUM/MEDIUM/LOW. Effort: S/M/S/M/M. Priority: P0 through P4. |
| c18 | Output explicitly addresses the new multi-datasource feature added 3 weeks ago as the prime suspect, recommending a code/diff review of that change as part of the investigation | PASS | Section 3 heading: 'Multi-datasource feature added 3 weeks ago — PRIME SUSPECT.' Provides exact git commands: 'git log --since="3 weeks ago" -- src/reports/' and 'git show <commit-hash>'. Lists specific patterns to look for (loop vs batch, sequential vs parallel, query patterns). |
| c19 | Output references the USE method (Utilisation, Saturation, Errors) or RED method (Rate, Errors, Duration) for systematic resource analysis | PARTIAL | Section 5 is a dedicated heading 'Systematic Analysis Framework: RED Method' explaining Rate (~10 req/s), Errors (0%), Duration (p50/p95/p99 distribution). Also contrasts with USE: 'USE is resource-focused and better for infrastructure analysis; RED is traffic-focused and better for endpoint optimisation.' Ceiling is PARTIAL. |

### Notes

The captured output is a comprehensive, well-structured performance profile that meets every criterion at its ceiling. All 17 PASS-ceiling criteria are fully satisfied, and both PARTIAL-ceiling criteria (c8, c19 on USE/RED method) are achieved at the PARTIAL level. Standout strengths: the exact section ordering matches the prompt's specification (baseline → timing breakdown → prime suspect → N+1 check → framework → profiler → bottlenecks → one-change discipline → per-fix measurement plans); the bottlenecks table includes all required columns (impact, effort, priority); each fix carries a quantified before/after improvement tied to the same load protocol; and the multi-datasource prime suspect is called out verbatim with exact git commands. The profiler section handles the 'DO NOT pause to ask' instruction appropriately by making the Python/Django assumption explicit and listing cross-stack alternatives. No criteria failed.
