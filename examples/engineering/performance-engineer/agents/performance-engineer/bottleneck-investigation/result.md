# Bottleneck Investigation

Scenario: User reports that API response times have degraded significantly under load, with P99 climbing from 200ms to 2s, and asks the performance engineer to investigate.

## Prompt

> Our API is getting slow under load. Two weeks ago P99 was around 200ms. Now it's hitting 2 seconds. P50 is still okay at about 180ms — it's the tail latency that's the problem. We're seeing this mostly on `GET /api/reports/{id}` and `POST /api/exports`. Traffic has grown about 30% in the past two weeks but that shouldn't explain a 10x P99 increase. We deploy multiple times a day so it's hard to pinpoint which change caused it. Can you investigate?
> 
> Do not ask for clarification — proceed using the information provided. State your assumptions where relevant.
> 
> A few specifics for the response (output in this exact section order):
> 
> 1. **Baseline section (FIRST, before any fixes)** — explicit table:
>    ```
>    | Metric            | 2 weeks ago | Now    | Delta  |
>    |-------------------|-------------|--------|--------|
>    | P50 latency       | ~180ms      | ~180ms | flat   |
>    | P95 latency       | (estimate)  | (estimate) | (delta) |
>    | P99 latency       | 200ms       | 2000ms | 10×    |
>    | Throughput (req/s)| baseline    | +30%   | +30%   |
>    | Error rate        | (record)    | (record) | (delta) |
>    ```
>    State the disproportionality explicitly: "10× P99 jump on 30% traffic growth is non-linear — suggests resource contention crossing a threshold, NOT linear scaling."
> 2. **Outside-in latency breakdown (BEFORE diving into DB)** — break the request flow into stages: client → load balancer → ingress → application layer → database → external calls → response. Estimate or measure time spent at each stage. Only narrow into the database AFTER you've identified database time as the likely contributor.
> 3. **Stack confirmation** — explicitly note "Assumed Python/Django stack based on common patterns; CONFIRM stack before recommending application profiler. If Python: `py-spy top --pid <pid>`. If Node: `clinic doctor`. If .NET: `dotnet-trace collect`. If JVM: `async-profiler`." Name the stack-appropriate profiler.
> 4. **Two-endpoint analysis** — `GET /api/reports/{id}` (read, sync) vs `POST /api/exports` (write, likely async). Different bottleneck profiles: reports → query/cache, exports → queue depth + lock contention + background-job worker capacity. Address each separately.
> 5. **Deploy bisection (multiple-times-a-day strategy)** — `git log --since="2 weeks ago" --pretty=format:"%h %ai %s"` to enumerate. Use deploy timestamps to bisect: identify the day when P99 crossed a threshold from APM, then bisect commits within that day.
> 6. **One-change-at-a-time discipline** — explicit subsection. Every recommended fix MUST be followed by a re-measurement step at the same load with the same metric BEFORE the next change. State the protocol: "warm-up 60s, sample 10min at fixed RPS, compare P99 with statistical significance (≥30 runs preferred for tight CI)."
> 7. **Decision Checkpoint before infrastructure scaling**: a STOP-and-decide block before any recommendation to add nodes, increase pool size, or upsize the DB. Frame: "Scaling will mask the underlying bottleneck and increase cost ~$X/month. Proceed only if root cause is confirmed and not addressable at the application layer."
> 8. **Findings table** with columns `Component | Impact (HIGH/MEDIUM/LOW) | Hypothesis | Evidence | Recommended Fix | Re-measure Plan`.
> 9. **Before/after measurement requirement** stated explicitly for every fix — same load, same metric, same protocol. No fix is "done" without before/after evidence.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll structure this as a systematic performance investigation. Key assumptions stated upfront: I'm assuming a standard web stack (Python/Django, Node, .NET, or JVM) with access to APM metrics and deployment logs. I'll lay out the full diagnostic methodology before we execute.

---

## 1. Baseline Section

| Metric | 2 weeks ago | Now | Delta | Assessment |
|---|---|---|---|---|
| P50 latency | ~180ms | ~180ms | flat | ✓ Normal |
| P95 latency | ~400-500ms (est.) | ~1000-1200ms (est.) | ~2-3× | Elevated |
| P99 latency | 200ms | 2000ms | **10×** | **Critical** |
| Throughput (req/s) | baseline | +30% | +30% | Linear growth |
| Error rate | (need measurement) | (need measurement) | ? | Need data |

**Disproportionality Analysis:**
A 10× P99 jump on 30% traffic growth is **non-linear and indicates resource contention crossing a threshold, not linear scaling**. Possible signatures:
- Query queue depth exceeded connection pool size
- Lock contention on a hot row/table
- Garbage collection pauses (JVM) or memory pressure (Python)
- Cascading timeouts to a dependency (payment service, external API)
- DNS or network timeout cascade

P50 remaining flat is a **strong signal the median user is unaffected** — only the tail (slowest 1%) is hitting walls. This narrows the suspect list to resource limits, not algorithmic complexity.

---

## 2. Outside-In Latency Breakdown

**Before drilling into the database, we need to map the request flow:**

```
Client → Load Balancer (LB) → Ingress/WAF → App Layer → DB → External APIs → Response
  [LB time]  [routing, SSL]     [filter]    [app+queue]  [query]  [API call]
```

**Measurement plan — instrument each stage:**

| Stage | Measurement Method | Typical Culprit |
|---|---|---|
| **Client → LB** | Check APM "request start" timestamp vs client-side timing | Network latency (usually rules out tail) |
| **LB → Ingress** | LB logs (ingress_time - request_time) | SSL renegotiation, WAF rules |
| **Ingress → App Handler** | Framework middleware timing (first log entry) | Rate limiting, auth delays |
| **App Layer (request processing)** | Instrumented span in your APM (before DB call) | Deserialization, business logic, cache miss |
| **DB Query** | APM database span timing | **Most likely culprit for GET /api/reports/{id}** |
| **External APIs** | APM span for outbound HTTP/gRPC calls | Timeouts cascading (e.g., payment API slow → app waits → queue builds) |
| **Response serialization** | Time between query return and response sent | JSON encoding, large result sets |

**Action now:** Pull your APM data (DataDog, New Relic, CloudWatch) for the two endpoints and **show me the breakdown**. If you don't have per-stage instrumentation, that's the first gap to fill.

---

## 3. Stack Confirmation & Profiler Selection

**I'm assuming one of these — confirm which:**

| Stack | Profiler Command | What It Captures |
|---|---|---|
| **Python/Django** | `py-spy top --pid <pid>` or `python -m cProfile` | CPU time per function; GC pauses |
| **Node.js** | `clinic doctor` (clinic.js) or `node --prof` | Event loop blocking, GC, V8 timeline |
| **.NET (C#)** | `dotnet-trace collect --process-id <pid>` | CPU samples, GC events, lock contention |
| **JVM (Java/Kotlin)** | `async-profiler` or `jcmd <pid> JFR.start` | CPU flame graphs, allocation, GC pause times |

**State your stack and I'll tailor the profiling strategy.**

---

## 4. Two-Endpoint Analysis

These endpoints have different bottleneck profiles — analyze separately:

### **GET /api/reports/{id}** (read, synchronous)
**Likely bottleneck chain:**
1. Query cache miss → database query
2. Report generation (if computed on-read) → CPU/memory spike
3. Large result set serialization → network time

**Hypothesis:** 
- N+1 query on the reports table (added a join two weeks ago?)
- Missing index on the `id` column or a new filter predicate
- Caching layer eviction (cache key changed, TTL too short, or cache size exceeded)

**To diagnose:**
- Run `EXPLAIN ANALYZE SELECT * FROM reports WHERE id = ?` in production (read replica if available)
- Check APM for "database time as % of total request time" — if >80%, it's the query

---

### **POST /api/exports** (write, likely async)
**Likely bottleneck chain:**
1. Acquire lock / check uniqueness (row-level lock contention)
2. Insert into queue / job table
3. Return immediately (fast) OR wait for background job to start (slow)

**Hypothesis:**
- Exports queue is backed up — background workers slower than incoming requests
- Lock contention on a shared counter (e.g., export_sequence_id)
- Background job worker pool undersized (e.g., 2 workers for 1000+ queued jobs)

**To diagnose:**
- Check job queue depth: `SELECT COUNT(*) FROM export_jobs WHERE status = 'pending'`
- Check worker count and job processing time: `SELECT AVG(ended_at - started_at) FROM export_jobs WHERE status = 'completed' AND started_at > NOW() - INTERVAL '1 hour'`
- If queue depth is growing, workers can't keep up

---

## 5. Deploy Bisection Strategy (Multiple-Times-Per-Day)

**List all commits in the window:**

```bash
git log --since="2 weeks ago" --pretty=format:"%h %ai %s" | head -30
```

**Cross-reference with deployment timestamps:**
- Query your deployment logs / GitHub Actions / CD pipeline for deploy times
- Query your APM for P99 metrics at each deploy timestamp
- **Identify the day P99 crossed from ~200ms to >500ms** (the inflection point)
- Narrow to commits deployed that day: `git log --since="2026-04-19" --until="2026-04-20" --pretty=format:"%h %s"`

**Bisect the narrowed set:**
If 8 commits were deployed on the day of the inflection, test the median commit:
```bash
git bisect start
git bisect bad <commit-at-end-of-day>
git bisect good <commit-before-day>
# Test intermediate commits under load
```

**Once you identify the culprit commit, share it** — the diff will tell us what changed.

---

## 6. One-Change-At-A-Time Discipline

**Protocol (non-negotiable):**

Each fix follows this sequence:

1. **Baseline measurement** (current state, P99 latency)
   - Warm-up: 60s at target RPS
   - Sample: 10 minutes at fixed RPS (same RPS as when P99 spiked, e.g., 30% above baseline)
   - Collect ≥30 samples of P99 (independent runs preferred)
   - Record: mean P99, 95% CI, error rate

2. **Apply ONE fix** (single commit, reviewable diff)

3. **Re-measure** (same load, same duration)
   - Record: mean P99, 95% CI, error rate
   - Statistical test: Welch's t-test or Mann-Whitney U to confirm significance (p < 0.05)

4. **Decision:**
   - If P99 improved ≥20% AND error rate stable → commit, monitor, proceed to next fix
   - If P99 flat or worse → revert, investigate why fix didn't work

5. **Move to next fix** — do NOT stack multiple changes

**Example fix cycle:**
```
Baseline P99: 2000ms (95% CI: 1950–2050ms) — 42 samples over 10 min
→ Fix: add index on reports(id) 
→ Re-measure P99: 1400ms (95% CI: 1350–1450ms) — 40 samples over 10 min
→ Improvement: 30% ✓ Significant (p < 0.001) → commit
→ Move to next fix
```

---

## 7. Decision Checkpoint: Before Any Infrastructure Scaling

**STOP HERE if you're considering:**
- Adding database replicas
- Increasing connection pool size
- Upscaling the database (larger instance)
- Adding app servers

**Frame:**
```
Scaling costs ~$X/month (estimate: $500–2000 depending on your cloud).
Scaling masks the underlying bottleneck and makes it harder to diagnose later.
Proceed ONLY if:
  ✓ Root cause is confirmed (e.g., "database is CPU-bound" or "queue is unbounded")
  ✓ AND the issue is NOT addressable at the application layer (bad query, missing index, etc.)
  ✓ AND scaling is the least-cost fix
```

**Example:** If the culprit is an N+1 query, scaling the DB is expensive and temporary. Fixing the query is cheap and permanent. Get the application fix first.

---

## 8. Findings Table Template

Once you run diagnostics, populate this:

| Component | Impact (HIGH/MED/LOW) | Hypothesis | Evidence | Recommended Fix | Re-measure Plan |
|---|---|---|---|---|---|
| Database query (`reports`) | HIGH | Missing index or N+1 join | APM: DB time 90% of request; EXPLAIN ANALYZE shows seq scan | Add index on `reports(id)` and remove join | Baseline P99 on GET /api/reports; re-measure post-fix |
| Export queue | HIGH | Unbounded job queue; workers backlogged | Queue depth: 5000+; avg job time: 45s | Scale background workers from 2 to 8; add queue monitoring | Measure P99 on POST /api/exports under same load |
| ... | ... | ... | ... | ... | ... |

---

## 9. Before/After Measurement Requirement

**No fix is "done" without proof.**

For every recommended change:

```
BEFORE (current state):
  P99: 2000ms
  P95: 1200ms
  Error rate: 0.2%
  Test: 10 min at 130 req/s, N=40 samples

CHANGE: [Describe what was modified]

AFTER (post-fix):
  P99: 1400ms  ← 30% improvement
  P95: 900ms   ← Tail improved proportionally
  Error rate: 0.2% ← No regressions
  Test: same protocol, same load
  Statistical significance: p < 0.001 (Welch's t-test)
  Conclusion: FIX ACCEPTED / REVERT
```

**State this for every change before moving forward.**

---

## Next Steps

To proceed, I need:

1. **Stack confirmation** — Python/Django, Node, .NET, or JVM?
2. **APM tool in use** — DataDog, New Relic, CloudWatch, Honeycomb?
3. **Deployment log access** — Can you provide commit hashes + deploy timestamps for the past two weeks?
4. **Current APM data** — P99 breakdown by stage (app time, DB time, queue time, external API time) for the two endpoints?
5. **Load test setup** — Do you have a tool (k6, Locust, JMeter) to reproduce load at 130+ req/s?

Once I have these, I'll run the bisection and profiling sequence methodically.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.5/18.5 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 38222 ms |
| Target cost | $0.0955 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent establishes a baseline measurement before recommending any fixes — records the exact current metrics (P50, P95, P99, throughput, error rate) | PASS | Section 1 'Baseline Section' is the first section and contains a full table with P50, P95 (estimated), P99, Throughput (req/s), and Error rate rows — all recorded before any fix is proposed. |
| c2 | Agent follows the outside-in bottleneck identification: end-to-end timing breakdown before diving into database or code | PASS | Section 2 'Outside-In Latency Breakdown' explicitly states 'Before drilling into the database, we need to map the request flow' and presents a stage table: Client → LB → Ingress/WAF → App Layer → DB → External APIs → Response with measurement methods per stage. Database work only appears later in Section 4. |
| c3 | Agent checks for database-level issues: N+1 queries, missing indexes, full table scans, and lock contention | PASS | Section 4 explicitly lists 'N+1 query on the reports table', 'Missing index on the id column', and 'Lock contention on a shared counter (e.g., export_sequence_id)'. The findings table row references 'EXPLAIN ANALYZE shows seq scan' for full table scans. EXPLAIN ANALYZE query is also provided. |
| c4 | Agent applies the one-change-at-a-time rule — does not recommend changing multiple things simultaneously | PASS | Section 6 'One-Change-At-A-Time Discipline' states: 'Apply ONE fix (single commit, reviewable diff)' and 'Move to next fix — do NOT stack multiple changes'. The protocol mandates measure → fix → re-measure → decide before proceeding. |
| c5 | Agent recommends profiling tools appropriate to the likely stack before proposing optimisations | PASS | Section 3 'Stack Confirmation & Profiler Selection' appears before code-level recommendations and lists: Python/Django → `py-spy top --pid <pid>`, Node.js → `clinic doctor`, .NET → `dotnet-trace collect --process-id <pid>`, JVM → `async-profiler`. |
| c6 | Agent raises a decision checkpoint before recommending infrastructure scaling changes (cost and architecture implications) | PASS | Section 7 'Decision Checkpoint: Before Any Infrastructure Scaling' is a dedicated STOP block stating 'Scaling costs ~$X/month (estimate: $500–2000 depending on your cloud). Scaling masks the underlying bottleneck and makes it harder to diagnose later.' with explicit proceed-only conditions. |
| c7 | Agent notes that P50 vs P99 divergence is a tail latency signal — suggests investigating resource contention and connection pool exhaustion under concurrency rather than average-case code paths | PASS | Section 1 states 'P50 remaining flat is a strong signal the median user is unaffected — only the tail (slowest 1%) is hitting walls. This narrows the suspect list to resource limits, not algorithmic complexity.' Candidate causes listed include 'Query queue depth exceeded connection pool size', 'Lock contention on a hot row/table', 'Garbage collection pauses'. |
| c8 | Agent produces a prioritised findings table with impact (HIGH/MEDIUM/LOW), component, and recommended fix | PARTIAL | Section 8 provides a findings table template with all required columns (Component, Impact HIGH/MED/LOW, Hypothesis, Evidence, Recommended Fix, Re-measure Plan) and two populated example rows both rated HIGH. However, it is explicitly a template saying 'Once you run diagnostics, populate this' — not a fully populated table with the full range of actual findings. |
| c9 | Agent specifies that every optimisation must have a before/after measurement using the same load and same metric | PASS | Section 9 'Before/After Measurement Requirement' explicitly states 'No fix is done without proof' and provides a structured template with BEFORE and AFTER blocks including load specification, P99/P95/error rate, sample count, and statistical test requirement. |
| c10 | Output's baseline section reproduces the exact metrics from the prompt — P50 ~180ms (still healthy), P99 was 200ms two weeks ago, P99 now 2s, 30% traffic growth — and notes the 10x P99 jump is disproportionate to traffic | PASS | Section 1 table shows P50 ~180ms flat, P99 200ms → 2000ms (10×), Throughput +30%. Text explicitly states: 'A 10× P99 jump on 30% traffic growth is non-linear and indicates resource contention crossing a threshold, not linear scaling.' |
| c11 | Output explicitly identifies the P50-stable / P99-degraded pattern as a tail-latency / contention signal rather than an across-the-board slowdown, and lists candidate causes (connection pool exhaustion, lock contention, GC pauses, cold cache, queueing under load) | PASS | Section 1 disproportionality analysis lists: 'Query queue depth exceeded connection pool size', 'Lock contention on a hot row/table', 'Garbage collection pauses (JVM) or memory pressure (Python)', 'Cascading timeouts to a dependency'. P50 stable / P99 degraded framing is explicit. |
| c12 | Output's investigation plan addresses the two named endpoints (`GET /api/reports/{id}` and `POST /api/exports`) specifically — looking at their distinct workloads (read vs write, sync vs async) | PASS | Section 4 'Two-Endpoint Analysis' has dedicated subsections for 'GET /api/reports/{id} (read, synchronous)' with query/cache bottleneck chain, and 'POST /api/exports (write, likely async)' with queue depth/lock contention/worker capacity chain. Each has separate hypotheses and diagnostic queries. |
| c13 | Output proposes correlating the regression with the deployment history — using deploy timestamps to bisect the change set, since 'we deploy multiple times a day' makes single-commit blame infeasible | PASS | Section 5 'Deploy Bisection Strategy (Multiple-Times-Per-Day)' provides `git log --since='2 weeks ago' --pretty=format:'%h %ai %s'`, instructs cross-referencing with APM P99 at each deploy timestamp to find the inflection day, then narrowing to commits deployed that day, then `git bisect`. |
| c14 | Output's database checks include N+1 detection, missing indexes, full table scans, and lock contention, with named tools or queries (`pg_stat_statements`, `EXPLAIN ANALYZE`, `pg_locks`) where applicable | PASS | Section 4 names `EXPLAIN ANALYZE SELECT * FROM reports WHERE id = ?`. The findings table references 'EXPLAIN ANALYZE shows seq scan' (full table scan). N+1 queries, missing indexes, and lock contention are all explicitly named as hypotheses. pg_stat_statements and pg_locks are not named, but the 'where applicable' qualifier is met by EXPLAIN ANALYZE coverage. |
| c15 | Output applies the one-change-at-a-time discipline — any recommended fix is followed by a re-measurement step before the next change, not a batch of optimisations | PASS | Section 6 protocol: 'Baseline measurement → Apply ONE fix → Re-measure → Decision → Move to next fix.' The example fix cycle illustrates this: index added, re-measured, p < 0.001 significance confirmed, then proceed. Explicit 'do NOT stack multiple changes'. |
| c16 | Output names a profiling tool appropriate to the inferred stack (e.g. py-spy, async-profiler, dotnet-trace, Node clinic) before proposing code-level changes — and asks for stack confirmation if not stated | PASS | Section 3 lists all four stacks with commands before any code-level proposals: py-spy (Python), clinic doctor (Node), dotnet-trace (.NET), async-profiler (JVM). Ends with 'State your stack and I'll tailor the profiling strategy.' |
| c17 | Output stops and asks before recommending infrastructure scaling (more nodes, larger pool, bigger DB), framing the cost/architecture implications | PASS | Section 7 is a STOP block listing scaling candidates (DB replicas, connection pool, DB upscale, app servers) with '$500–2000/month' cost estimate and 'Scaling masks the underlying bottleneck.' Proceed conditions require confirmed root cause not addressable at app layer. |
| c18 | Output's findings table is prioritised by likely impact (HIGH/MEDIUM/LOW) with component and recommended fix per row, not a flat unranked list | PASS | Section 8 findings table has Impact (HIGH/MED/LOW) column with populated rows showing 'HIGH' for database query (reports) and 'HIGH' for Export queue. Table includes Component, Hypothesis, Evidence, Recommended Fix, and Re-measure Plan columns. Structure is correct with impact-level prioritisation. |
| c19 | Output requires before/after measurement at the same load and same metric for every change, with the measurement protocol stated (warm-up, sample size, statistical significance) | PASS | Section 9 template specifies: same-load protocol ('Test: 10 min at 130 req/s, N=40 samples'), statistical significance ('p < 0.001, Welch's t-test'), conclusion gate. Section 6 adds 'warm-up 60s, sample 10min at fixed RPS, collect ≥30 samples' and Welch's t-test or Mann-Whitney U with p < 0.05 threshold. |

### Notes

The output is exceptionally thorough and matches the required section order precisely. Every mandatory section is present and substantive: the baseline table reproduces exact prompt metrics, the outside-in breakdown precedes any DB-specific work, stack confirmation with profiler commands is explicit, both endpoints are analyzed with distinct bottleneck profiles, deploy bisection strategy is concrete, one-change-at-a-time protocol is rigorous with warm-up/sample/significance details, the scaling checkpoint includes cost framing, and before/after requirements are stated with statistical rigor. The only ceiling-limited score is c8 (findings table), correctly capped at PARTIAL because the table is a template with two illustrative rows rather than a populated prioritised list of actual findings — the test author anticipated this limitation. The output does not name pg_stat_statements or pg_locks specifically, but covers the underlying concepts and names EXPLAIN ANALYZE, which satisfies the 'where applicable' qualifier in c14.
