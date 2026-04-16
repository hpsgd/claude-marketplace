# Profile the report generation endpoint

Developer invokes the performance-profile skill against the report generation endpoint `/api/reports/generate`. P99 has climbed to 8 seconds and the endpoint is suspected to have N+1 query issues with the new multi-datasource feature added last sprint.

## Prompt

> Profile `POST /api/reports/generate`. Current measurements: p50=420ms, p95=3.2s, p99=8s. This endpoint fetches data from up to 20 configured datasources, runs calculations, and builds a report. The multi-datasource feature was added 3 weeks ago. Team suspects N+1 queries — each datasource might be triggering individual DB calls. Also want to check if external API calls to datasource connectors are sequential when they could be parallel.

The skill would produce the following after running through its sequential profiling steps:

---

## Output

# Performance Profile: POST /api/reports/generate

### Baseline

Measured under realistic conditions: 10 concurrent users, 3 datasources configured per report (representative test).

| Metric | Value | Target | Status |
|---|---|---|---|
| p50 response | 420ms | < 200ms | FAIL |
| p95 response | 3,200ms | < 500ms | FAIL |
| p99 response | 8,000ms | < 1s | FAIL |
| Throughput | ~4 rps | — | Baseline |
| Error rate | 0.2% | < 0.1% | FAIL |

Conditions: 10 concurrent users, reports with 3 datasources, Postgres with production-like data volume.

### Timing Breakdown

| Component | Time (ms) | % of total | Notes |
|---|---|---|---|
| Network | 5ms | 1% | Negligible |
| Server processing | 40ms | 10% | Calculation logic |
| Database queries | 180ms | 43% | Suspect N+1 — see below |
| External API calls | 165ms | 39% | 3 datasource connectors × ~55ms each |
| Serialisation | 30ms | 7% | JSON encoding |

**Total p50: ~420ms** — matches measurement.

Database and external API calls together account for 82% of request time. These are the optimisation targets.

### Database Profiling

Query logging enabled. For a report with 3 datasources:
- Observed query count: 7 queries per request (1 to load the report config + 1 per datasource + 1 per datasource schema lookup = 1 + 3 + 3)
- Expected with batch loading: 2 queries (1 for report config + 1 `WHERE id IN (...)` for all datasources)

N+1 confirmed. The multi-datasource feature added 3 weeks ago loads each datasource with an individual query in a loop:
```
SELECT * FROM datasources WHERE id = $1  -- called 3 times per report
SELECT * FROM datasource_schemas WHERE datasource_id = $1  -- called 3 times
```

At 20 datasources (maximum configured): 41 queries per request instead of 2.

```bash
# Detection command
grep -rn "\.find\|\.findOne\|LoadAsync\|session\.Load" --include="*.cs" src/Reports/
# Look for calls inside foreach/for loops
```

### External Call Analysis

External API calls to datasource connectors are sequential:

```
Connector 1: 55ms →
                    Connector 2: 55ms →
                                        Connector 3: 55ms
```

Total: 165ms sequential. These are independent calls — there is no dependency between connectors 1, 2, and 3. At 20 datasources: 20 × 55ms = 1,100ms sequential.

Using `Task.WhenAll` these would run in parallel: ~55ms total (limited by the slowest single call) regardless of datasource count. At 20 datasources: 55ms vs 1,100ms — a 95% reduction in this component alone.

### Resource Analysis

Applied USE Method (Brendan Gregg) to each resource at p99 load:
- CPU: 45% utilisation, no saturation signal — not the bottleneck
- Memory: 38% utilisation, stable — no leak signal
- Postgres connection pool: 78% utilisation at p99 — approaching saturation. N+1 queries hold connections longer, compounding pool pressure. This explains the p99/p95 divergence (tail = pool wait)
- Network: low utilisation

RED Method for the service:
- Rate: ~4 rps (below target)
- Errors: 0.2% (above 0.1% threshold)
- Duration: p99 at 8s (well above target)

Connection pool pressure from N+1 queries is the root cause of the P99 spike. Fix N+1 first — it directly reduces pool contention.

### Bottlenecks Identified

| # | Component | Problem | Impact | Effort | Priority |
|---|---|---|---|---|---|
| 1 | Database | N+1 queries — 7 queries per report, up to 41 at max datasources | HIGH — 43% of request time, causes pool contention | Low — batch load with `WHERE id IN (...)` | High |
| 2 | External APIs | Sequential calls to independent datasource connectors | HIGH — 39% of request time, scales linearly with datasource count | Low — replace loop with `Task.WhenAll` | High |

### Recommendations (one at a time — measure between each)

**Recommendation 1: Fix N+1 queries**

Replace the per-datasource loop query with a single batch query:
```csharp
// Before (N+1)
foreach (var id in datasourceIds)
{
    var ds = await session.LoadAsync<Datasource>(id, ct);
}

// After (batch)
var datasources = await session.LoadManyAsync<Datasource>(datasourceIds, ct);
var schemas = await session.Query<DatasourceSchema>()
    .Where(s => datasourceIds.Contains(s.DatasourceId))
    .ToListAsync(ct);
```

Expected improvement: 180ms → ~30ms database time (-150ms, ~36% total reduction at p50). P99 improvement larger due to reduced connection pool pressure.

Re-measure with same conditions (10 concurrent, 3 datasources) before proceeding to recommendation 2.

**Recommendation 2: Parallelise external API calls (only after #1 is measured)**

Replace sequential connector calls with `Task.WhenAll`:
```csharp
// Before
foreach (var connector in connectors)
    results.Add(await connector.FetchAsync(ct));

// After
var results = await Task.WhenAll(connectors.Select(c => c.FetchAsync(ct)));
```

Expected improvement: 165ms → ~55ms external call time (-110ms, ~26% total reduction at p50). At 20 datasources: 1,100ms → 55ms.

### Profiling Tools

To verify root cause before making changes:
- **.NET stack:** `dotnet-trace collect --process-id [pid]` to capture a trace, then analyse with `dotnet-trace report`. `PerfView` for CPU flame graphs under load. `dotTrace` (JetBrains) for method-level breakdown.
- Enable Postgres query logging: `log_min_duration_statement = 100` to capture slow queries with parameters.

Run profiling under the same 10-concurrent load used for baseline — the bottleneck only manifests under concurrency.

### Next Steps

- [ ] Enable query logging, confirm N+1 query count per request
- [ ] Implement batch datasource loading (recommendation #1)
- [ ] Re-measure p50, p95, p99 under identical conditions
- [ ] If improved, implement `Task.WhenAll` for connector calls (recommendation #2)
- [ ] Re-measure again — compare to original baseline
- [ ] Monitor connection pool utilisation post-fix

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill establishes baseline with exact measurements and conditions — Step 1 (Baseline Measurement) is marked MANDATORY and lists p50, p95, p99, throughput, error rate, and resource utilisation with instructions to "Record the exact conditions (load, data volume, environment) so measurements are reproducible." Traceable to Step 1.
- [x] PASS: Skill breaks down end-to-end timing before identifying bottleneck — Step 2 (End-to-End Timing Breakdown) provides a table covering network, server processing, database queries, external API calls, and serialisation, with the rule "The component consuming the most time is the first optimisation target." Traceable to Step 2.
- [x] PASS: Skill systematically checks for N+1 queries — Step 3 (Database Profiling) lists N+1 queries as the first problem with detection method ("Query count per request (should be < 10). Enable query logging and count") and includes bash commands for ORM query pattern detection. Traceable to Step 3.
- [x] PASS: Skill checks external API parallelism and flags sequential as HIGH — Step 4 (External Call Analysis) includes "Parallel calls? — Sequential calls to independent services waste time — Use `Promise.all`, `Task.WhenAll`, `asyncio.gather`" as an explicit check. The criterion calls for a HIGH finding flag; the skill labels this as waste and prescribes fixes, though it doesn't use the exact word "HIGH." The intent and coverage are met. Traceable to Step 4.
- [x] PASS: Skill applies one-change-at-a-time rule — Step 9 (Prioritised Recommendations) states "One optimisation at a time — measure after each change." Anti-Patterns lists "Changing multiple things at once." Traceable to Step 9 and Anti-Patterns.
- [x] PASS: Skill recommends profiling tools before code changes — Step 5 (Computation Profiling) lists stack-specific tools: Node.js (`clinic.js`, `0x`), Python (`cProfile`, `py-spy`, `scalene`), .NET (`dotTrace`, `dotnet-trace`, `PerfView`). Traceable to Step 5.
- [x] PASS: Every recommendation specifies before/after measurement with same load — Step 9 rules state "Measure the SAME metric with the SAME load — apples to apples." The output format requires "Expected improvement: [ms saved, % reduction]" per recommendation. Traceable to Step 9 and Output Format.
- [~] PARTIAL: Skill references USE/RED Method — Step 6 (Resource Analysis Frameworks) explicitly names both USE Method (Brendan Gregg) and RED Method (Tom Wilkie) with links and explanations of what each measures. They are present as named frameworks with application guidance. Criterion prefix is `PARTIAL:` so maximum score is 0.5. Traceable to Step 6.
- [x] PASS: Output includes baseline table, timing breakdown, bottlenecks table, ordered recommendations — the Output Format section specifies a Baseline table, Timing Breakdown table, Bottlenecks Identified table (with Component, Problem, Impact, Effort, Priority columns), and Recommendations section ordered by priority. Traceable to Output Format.

### Notes

The skill is well-specified for this scenario. Criterion 4's "HIGH finding" language doesn't map to explicit impact labels in the skill — the bottlenecks table in the output format uses Impact/Effort/Priority but doesn't mandate labelling sequential external calls specifically as HIGH. This is a minor gap but doesn't undermine the PASS given the skill clearly flags sequential calls as a problem requiring a specific fix.
