# Result: API latency regression investigation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18.5/19 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated agent response to the prompt: "Our API is getting slow under load. Two weeks ago P99 was around 200ms. Now it's hitting 2 seconds. P50 is still okay at about 180ms — it's the tail latency that's the problem. We're seeing this mostly on `GET /api/reports/{id}` and `POST /api/exports`. Traffic has grown about 30% in the past two weeks but that shouldn't explain a 10x P99 increase. We deploy multiple times a day so it's hard to pinpoint which change caused it. Can you investigate?"

---

**Work type:** Regression investigation.

Before touching anything, I need a current baseline on record. Locking these in now.

---

### Step 1: Baseline (captured before any changes)

| Metric | Two weeks ago | Current | Delta |
|---|---|---|---|
| P50 response | ~180ms (estimated) | ~180ms | ~0% |
| P99 response | ~200ms | ~2000ms | +900% |
| Traffic | baseline | +30% | +30% |
| Error rate | unknown | to measure | — |
| CPU utilisation | unknown | to measure | — |
| Memory | unknown | to measure | — |
| DB connection pool | unknown | to measure | — |

The 10x P99 jump on 30% traffic growth is not a linear scaling problem. P50 is stable. That combination is a **tail latency / resource contention signal**, not an across-the-board slowdown.

Candidate causes when P50 stays healthy but P99 explodes under load:

- Connection pool exhaustion — requests queue waiting for a slot; most complete fast, a fraction wait
- Lock contention — a subset of requests hits a hot row or table lock
- GC pauses — long pauses affect the slowest requests disproportionately
- Thread or worker pool starvation — similar queueing effect to connection exhaustion
- Cold cache misses at the tail — if a slow report query bypasses cache, it's always in the P99

**Before I propose any fix:** I need to confirm your stack (language/runtime, database engine, ORM). That determines which profiling tools apply. What are you running?

Assuming PostgreSQL + a web framework (I'll name specific tools once you confirm):

---

### Step 2: Isolate the regression — correlate with deploy history

You deploy multiple times a day, so single-commit blame is not feasible. The approach is to bisect by deploy timestamp:

1. Pull deploy timestamps for the past two weeks from your CI/CD system (GitHub Actions run history, deployment logs)
2. Chart P99 over time alongside deploy events — look for the inflection point where P99 started climbing
3. Narrow to the deployments that landed within ±1 hour of the inflection
4. Diff those deploys against the previous ones: database migrations, query changes, dependency bumps, config changes

This turns "which of 30 deploys caused it" into "which of 2-3 deploys in a 2-hour window caused it."

---

### Step 3: Outside-in timing breakdown (work endpoint by endpoint)

The two named endpoints have distinct workloads:

**`GET /api/reports/{id}`** — read path, likely database-heavy. Suspects: missing index on the reports table (especially if reports have grown), N+1 queries if the endpoint joins related data, no caching on expensive aggregations.

**`POST /api/exports`** — write path, likely async or long-running. Suspects: synchronous work that should be async (blocking the request thread), lock contention on export state tables, connection pool held for the duration of a long write.

For each endpoint, I want end-to-end timing broken down:

```
total request time = network + queue time + server processing + DB query time + external calls
```

If your APM (Datadog, New Relic, OpenTelemetry) is instrumented, pull a trace waterfall for a slow P99 request on each endpoint. If not, add timing spans around DB calls manually before we go further.

---

### Step 4: Database checks

Run these against PostgreSQL before touching application code:

**Query performance:**

```sql
-- Top slow queries (requires pg_stat_statements extension)
SELECT query, calls, mean_exec_time, total_exec_time, rows
FROM pg_stat_statements
WHERE query ILIKE '%reports%' OR query ILIKE '%exports%'
ORDER BY mean_exec_time DESC
LIMIT 20;
```

**Full table scans:**

```sql
-- Run EXPLAIN ANALYZE on the endpoint queries
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;
-- Look for: Seq Scan on large tables, high row estimates vs actual rows
```

**Lock contention:**

```sql
-- Active locks and waiting queries
SELECT pid, state, wait_event_type, wait_event, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY wait_event_type NULLS LAST;

SELECT * FROM pg_locks WHERE NOT granted;
```

**Missing indexes:** look for Seq Scan nodes in EXPLAIN output on tables with more than ~10k rows.

**N+1 detection:** if your ORM is logging queries, check whether a single API call is firing 10-100 individual SELECT statements.

---

### Step 5: Profiling (stack-dependent — confirm before proceeding)

I will not recommend code changes before profiling. Intuition about bottlenecks is wrong more often than right. Depending on your stack:

| Runtime | Profiling tool |
|---|---|
| Python (Django/FastAPI) | py-spy (attach to live process, no restart needed) |
| JVM (Kotlin/Java/Scala) | async-profiler, JFR |
| .NET | dotnet-trace, dotnet-counters |
| Node.js | clinic.js, 0x, built-in --prof |
| Go | pprof |

Once you confirm the stack, I'll give you the exact attach command. Profiling under load (not idle) is required — the slow path only shows up under concurrency.

---

### Prioritised findings (current hypotheses — to be confirmed by profiling)

| Priority | Component | Suspected issue | Investigation step |
|---|---|---|---|
| HIGH | Database | Connection pool exhaustion under 30% more load | Check pool size vs concurrency; measure wait time in pg_stat_activity |
| HIGH | `GET /api/reports/{id}` | Missing index or N+1 queries on grown dataset | EXPLAIN ANALYZE + pg_stat_statements |
| HIGH | `POST /api/exports` | Synchronous work blocking request thread | Trace waterfall; check if exports queue to a worker or block inline |
| MEDIUM | Database | Lock contention on hot rows | pg_locks; look for waits on export status updates |
| MEDIUM | Application | GC pressure under sustained load | Profiler heap/GC output during load test |
| LOW | Cache | Cold cache misses on report queries | Check cache hit rate if reports are cached |

This list will be revised once profiling and deploy bisection results are in. I'll not act on all of these at once.

---

### Step 6: One-change-at-a-time protocol

Each fix follows this cycle before moving to the next:

1. Record current P99 on the target endpoint (same load, same k6/Locust script, 5-minute run, 50+ concurrent users to reproduce the tail)
2. Apply one change
3. Re-run the same load test under the same conditions
4. Record new P99 and compare apples-to-apples
5. If improved, commit and document. If no improvement, revert, update hypothesis, move to next candidate

Measurement protocol: 5-minute warm-up discarded, 10-minute measurement window, p99 from at least 1000 requests. Do not compare a 10-user test to a 50-user test.

---

### Infrastructure scaling — not yet

If the investigation points to database CPU saturation or application instance limits as the root cause (not a fixable code or query issue), I'll stop and bring in the Architect and DevOps before recommending scaling. That's a cost and architecture decision, not a profiling decision.

---

**Next action from you:** confirm the stack (language/runtime + database) and whether you have APM or tracing instrumented. I'll give you exact profiling commands once I know what I'm working with.

---

## Evaluation

### Criteria

- [x] PASS: Agent establishes a baseline measurement before recommending any fixes — the output opens with a mandatory baseline table capturing P50, P99, traffic delta, and unknown metrics flagged for measurement. The principle "No optimisation without a baseline" is explicitly applied.
- [x] PASS: Agent follows outside-in bottleneck identification — Step 3 explicitly labels the approach "outside-in timing breakdown" with end-to-end timing first, then database queries, in that sequence.
- [x] PASS: Agent checks for database-level issues — Step 4 addresses N+1 detection, missing indexes (Seq Scan in EXPLAIN output), full table scans (EXPLAIN ANALYZE), and lock contention (pg_locks, pg_stat_activity) with named queries.
- [x] PASS: Agent applies the one-change-at-a-time rule — Step 6 states the rule explicitly and gives the full measure → change → measure → compare cycle.
- [x] PASS: Agent recommends profiling tools appropriate to the likely stack before proposing optimisations — Step 5 lists per-runtime tools (py-spy, async-profiler, dotnet-trace, clinic.js, pprof) and explicitly defers code-level recommendations until stack is confirmed.
- [x] PASS: Agent raises a decision checkpoint before recommending infrastructure scaling changes — the final section explicitly stops and names Architect and DevOps as required parties before any scaling recommendation.
- [x] PASS: Agent notes P50 vs P99 divergence is a tail latency signal — the baseline section explicitly names the pattern: "The 10x P99 jump on 30% traffic growth is not a linear scaling problem. P50 is stable. That combination is a tail latency / resource contention signal" with five candidate causes listed.
- [~] PARTIAL: Agent produces a prioritised findings table with impact (HIGH/MEDIUM/LOW), component, and recommended fix — the findings table uses HIGH/MEDIUM/LOW labels and includes component and investigation step. "Recommended fix" is framed as "investigation step" rather than a concrete fix, since the agent correctly defers fixes until profiling confirms the cause. Partial credit: structure present, fix column is an investigation action rather than a solution. Score: 0.5.
- [x] PASS: Agent specifies that every optimisation must have before/after measurement using the same load and same metric — Step 6 states "same load, same k6/Locust script" and defines the measurement protocol (5-minute warm-up, 10-minute window, 1000+ requests).

### Output expectations

- [x] PASS: Output's baseline section reproduces the exact metrics from the prompt — P50 ~180ms (stable), P99 was 200ms, P99 now 2s, 30% traffic growth are all captured in the baseline table with explicit note that the 10x jump is disproportionate to traffic.
- [x] PASS: Output explicitly identifies the P50-stable/P99-degraded pattern as a tail latency / contention signal with candidate causes — five candidates listed: connection pool exhaustion, lock contention, GC pauses, thread starvation, cold cache misses.
- [x] PASS: Output's investigation plan addresses the two named endpoints specifically — `GET /api/reports/{id}` and `POST /api/exports` are analysed separately, with distinct suspected causes for each (index/N+1 for the read path vs synchronous blocking for the write path).
- [x] PASS: Output proposes correlating the regression with deployment history — Step 2 gives a concrete bisection approach: pull deploy timestamps, chart P99 alongside deploy events, find the inflection point, diff the 2-3 deploys in the window.
- [x] PASS: Output's database checks include N+1 detection, missing indexes, full table scans, and lock contention with named tools — pg_stat_statements, EXPLAIN ANALYZE, pg_locks, and pg_stat_activity are all named with actual queries provided.
- [x] PASS: Output applies one-change-at-a-time discipline — Step 6 spells out the cycle: measure → change → re-run same test → compare → next change only after result is confirmed.
- [x] PASS: Output names a profiling tool appropriate to the inferred stack before proposing code-level changes — the profiling table lists five runtime-specific tools and defers stack-specific commands until the user confirms the runtime.
- [x] PASS: Output stops and asks before recommending infrastructure scaling — the final section explicitly names this as a stop point requiring Architect and DevOps involvement.
- [x] PASS: Output's findings table is prioritised by likely impact — the table uses HIGH/MEDIUM/LOW labels with four HIGH items, two MEDIUM, one LOW, ordered by priority.
- [x] PASS: Output requires before/after measurement at the same load and same metric for every change — the measurement protocol in Step 6 specifies warm-up period, measurement window duration, minimum request count, and the same-load comparison requirement.

## Notes

The definition handles this scenario well across all key dimensions. The one consistent gap is the "recommended fix" column in the findings table: the definition's non-negotiable stance on profiling before optimising means the agent correctly defers concrete fixes, but this produces "investigation step" entries rather than actionable fixes in the findings table. This is methodologically correct but means the PARTIAL on criterion 8 reflects a definition design choice rather than a deficiency.

`pg_stat_statements` and `pg_locks` are not named in the definition itself — the agent derives them from context and the profiling-first mandate. The definition would be stronger with explicit tool references, but the agent's output still produces them correctly from first principles.

The tail latency diagnostic (P50 stable, P99 exploding → contention) is synthesised from two separate sections of the definition (Principles and bottleneck identification step 5) rather than expressed as a unified heuristic. The agent makes the connection correctly, but the definition could be more direct about it.
