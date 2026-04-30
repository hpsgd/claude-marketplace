# Result: Profile the report generation endpoint

**Verdict:** PARTIAL
**Score:** 15.5/19 criteria met (82%)
**Evaluated:** 2026-04-30

---

## Output

The following is a simulated output from invoking `/performance-engineer:performance-profile` against the scenario in `test.md`.

---

# Performance Profile: POST /api/reports/generate

## Baseline

| Metric | Value | Target | Status |
|---|---|---|---|
| p50 response | 420ms | < 200ms | FAIL |
| p95 response | 3,200ms | < 500ms | FAIL |
| p99 response | 8,000ms | < 1,000ms | FAIL |
| Throughput | [measure under load] | [establish target] | TBD |
| Error rate | [measure under load] | < 0.1% | TBD |

**Conditions recorded:** Up to 20 configured datasources per request. Multi-datasource feature introduced ~3 weeks ago. Measurements taken from production APM. Data volume and concurrent user count must be confirmed and locked for reproducible re-measurement.

---

## Timing Breakdown

Before recommending anything, instrument the endpoint to produce a waterfall breakdown. The following targets are the investigation frame — actual values need to be measured with query logging enabled and a profiler attached.

| Component | Estimated time (ms) | % of p99 | Notes |
|---|---|---|---|
| Network | ~10ms | ~0.1% | Negligible for an internal endpoint |
| Server processing | [measure] | [%] | Application logic, loop over datasources |
| Database queries | [measure] | [%] | **Suspect — N+1 if each datasource triggers individual query** |
| External datasource API calls | [measure] | [%] | **Suspect — sequential calls to up to 20 connectors** |
| Calculation / aggregation | [measure] | [%] | Report computation across fetched data |
| Serialisation | [measure] | [%] | JSON encoding of report output |

**Stack confirmation required:** Before attaching a profiler, confirm the server runtime:

- Node.js → use `clinic.js` or `0x` for flame graphs
- Python → use `py-spy` or `scalene`
- .NET → use `dotnet-trace` or `dotTrace`

*The stack is not specified in the prompt. Please confirm before proceeding with profiler-specific steps.*

---

## N+1 Query Investigation

The multi-datasource feature (added 3 weeks ago) is the prime suspect for the p99 regression. Enable query logging and count queries for a single request with 20 datasources.

**Expected query count:**

| Scenario | Query count | What it means |
|---|---|---|
| No N+1 | 1–3 | Single query batching all datasource IDs |
| N+1 present | 20–40+ | One query per datasource, one per result set |

```bash
# Check for ORM patterns that cause N+1
grep -rn "\.find\|\.get\|\.query\|\.select\|\.where\|\.include\|\.join" --include="*.ts" --include="*.py" --include="*.cs"

# Check for missing eager loading / batch fetch
grep -rn "lazy\|LazyLoad\|defer\|select_related\|prefetch_related" --include="*.ts" --include="*.py" --include="*.cs"
```

Run `EXPLAIN ANALYZE` on any queries identified as hot paths. Sequential scans on a datasources table or report data table at scale confirm the missing-index variant.

---

## External Call Analysis

Each datasource connector is likely contacted via an external API call. If calls are sequential, with 20 datasources and each connector averaging 300ms, total external call time reaches 6,000ms — which accounts for most of the p99 budget.

| Check | Finding | Action |
|---|---|---|
| **Sequential vs parallel?** | Inspect code loop over datasource connectors | If sequential: HIGH — parallelise with `Promise.all` / `Task.WhenAll` / `asyncio.gather` |
| **Timeouts configured?** | Each connector call must have an explicit timeout | Set 5–10s per call (or fail fast) |
| **Circuit breaker?** | If one connector fails, does it cascade? | Implement circuit breaker to isolate connector failures |
| **Caching?** | Is datasource config or connector metadata fetched per request? | Cache stable connector config with appropriate TTL |

**Sequential calls to 20 independent services is flagged as a HIGH-impact finding.** These calls carry no ordering dependency and can be fully parallelised.

---

## Resource Analysis

Apply USE and RED methods to rule out infrastructure bottlenecks independent of the code issues above.

**USE Method** (per Brendan Gregg) — for every resource (CPU, memory, DB connection pool, network):

- **Utilisation:** Is the resource > 70% busy during the p99 requests?
- **Saturation:** Is there a queue forming (connection pool wait times, thread pool backlog)?
- **Errors:** Are there error logs at resource boundaries (DB connection timeouts, connector rejections)?

**RED Method** (per Tom Wilkie) — for the report generation service itself:

- **Rate:** Requests/sec at baseline load
- **Errors:** Failed report generations per second (distinct from slow ones)
- **Duration:** Latency distribution — p50/p95/p99 already captured; confirm the shape (bimodal with/without 20 datasources?)

---

## Bottlenecks Identified

| # | Component | Problem | Impact | Effort | Priority |
|---|---|---|---|---|---|
| 1 | Database queries | N+1 — 20 individual DB queries per request (one per datasource) | ~3,000ms estimated saving at p99 | Medium — add batch fetch / eager loading | HIGH |
| 2 | External API calls | 20 sequential connector calls where calls are independent | ~5,000ms+ saving at p99 (parallelism reduces to max single-connector latency) | Medium — wrap in `Promise.all` / `Task.WhenAll` / `asyncio.gather` | HIGH |
| 3 | Missing stack profiler | Stack unknown — CPU-bound computation bottleneck unconfirmable without profiler | Unknown until measured | Low — attach profiler and review flame graph | MEDIUM |

---

## Recommendations (ordered by priority)

**Fix one thing at a time. Measure after each. Do not combine changes.**

1. **Database — fix N+1 queries.** Identify the loop over datasources that triggers individual DB calls. Replace with a batch fetch (IN clause or JOIN). Expected improvement: reduction from 20+ queries to 1–3 queries. Based on 20x query reduction, expect DB time to fall from an estimated 3s to ~150–200ms. Re-measure p99 with identical load before proceeding.

2. **External calls — parallelise connector calls.** After confirming and measuring the N+1 fix, inspect the loop over datasource connectors. If calls are sequential today, replace with `Promise.all` / `Task.WhenAll` / `asyncio.gather`. Expected improvement: external call time collapses from (20 × avg connector latency) to (max single connector latency). With avg 300ms connectors, this saves ~5,700ms at p99. Re-measure before proceeding to recommendation 3.

3. **Computation — attach profiler and review flame graph.** After addressing DB and external calls, re-profile to confirm whether calculation or serialisation accounts for any remaining tail latency. If the p99 is still above target after recommendations 1 and 2, this step identifies the residual bottleneck.

---

## Next Steps

- [ ] Confirm server stack (Node.js / Python / .NET) — required to select profiler
- [ ] Enable query logging and count DB queries for a single request with 20 datasources
- [ ] Review the diff for the multi-datasource feature added 3 weeks ago — this change is the prime regression suspect
- [ ] Implement recommendation #1 (N+1 fix)
- [ ] Re-measure p50/p95/p99 under identical load after #1
- [ ] Implement recommendation #2 (parallelise external calls) only after #1 is measured
- [ ] Re-measure p50/p95/p99 under identical load after #2

---

## Evaluation

### Criteria (definition against rubric)

- [x] PASS: Skill establishes a baseline with exact measurements before recommending anything — met. Step 1 mandates p50, p95, p99, throughput, error rate, and resource utilisation, with explicit rules requiring exact conditions to be recorded.
- [x] PASS: Skill breaks down end-to-end timing across components — met. Step 2 waterfall table covers network, server processing, database queries, external API calls, serialisation, rendering.
- [x] PASS: Skill systematically checks for N+1 queries — met. Step 3 explicitly requires query count per request (< 10 threshold), provides grep commands for ORM patterns, and instructs `EXPLAIN ANALYZE`.
- [x] PASS: Skill checks whether external API calls are parallel or sequential — met. Step 4 "Parallel calls?" row flags sequential calls to independent services and names the fix (`Promise.all`, `Task.WhenAll`, `asyncio.gather`).
- [x] PASS: Skill applies the one-change-at-a-time rule — met. Step 9 states "One optimisation at a time — measure after each change" and Anti-Patterns reinforces it.
- [x] PASS: Skill recommends a profiling tool appropriate to the server stack — met. Step 5 lists tools per stack (Node.js, Python, .NET).
- [x] PASS: Every recommendation specifies expected improvement with before/after measurement — met. Output format mandates "Expected improvement: [ms saved, % reduction]" per recommendation; Step 9 requires measuring the same metric with the same load.
- [~] PARTIAL: Skill references USE Method or RED Method — partially met per rubric type. Step 6 explicitly covers both USE and RED with descriptions and links. Full in substance; scored 0.5 per PARTIAL rubric type.
- [x] PASS: Output includes baseline table, timing breakdown, bottlenecks table with impact/effort/priority, and ordered recommendations — met. Output Format section contains all four required sections; bottlenecks table includes Impact, Effort, Priority columns.

**Criteria subtotal: 8.5/9**

### Output expectations (simulated output against rubric)

- [x] PASS: Output baseline table reproduces exact prompt metrics (p50=420ms, p95=3.2s, p99=8s) and records conditions — met. Baseline table uses exact values from prompt; conditions note records datasource count and feature timing.
- [x] PASS: Output timing breakdown decomposes request into named segments — met. Waterfall table covers server processing, database queries, external datasource API calls, calculation, serialisation.
- [x] PASS: Output investigation explicitly counts queries per request to confirm or refute the N+1 hypothesis — met. Query count table contrasts "1–3 queries" (no N+1) vs "20–40+ queries" (N+1 present) for 20 datasources.
- [x] PASS: Output checks whether external datasource API calls are sequential or parallel and flags sequential calls as HIGH-impact — met. External Call Analysis table flags this HIGH and quantifies the impact (20 × 300ms = 6,000ms).
- [x] PASS: Output applies one-change-at-a-time rule and orders recommendations sequentially — met. Recommendations section explicitly states "Fix one thing at a time. Measure after each. Do not combine changes."
- [ ] FAIL: Output names a profiling tool appropriate to the inferred stack and asks for stack confirmation if not stated — not fully met. The skill lists tools per stack in Step 5 but does not instruct the agent to ask for stack confirmation when the stack is unspecified. The simulated output adds a stack-confirmation prompt as best-practice interpretation, but the skill definition does not drive this behaviour.
- [x] PASS: Output ties each recommendation to a quantified expected improvement with a before/after measurement plan — met. Each recommendation includes estimated ms saving with reasoning (e.g. "20x query reduction → DB time falls from ~3s to ~150–200ms") and explicit re-measure step.
- [x] PASS: Output bottlenecks table includes impact, effort, and priority columns — met.
- [ ] FAIL: Output explicitly addresses the multi-datasource feature added 3 weeks ago as prime suspect, recommending a code/diff review — not met by the skill definition. The skill has no step instructing the agent to treat recent feature additions as regression suspects or to recommend a git diff review. The simulated output adds this as contextual interpretation, but the skill itself would not reliably produce it.
- [~] PARTIAL: Output references USE or RED method — partially met per rubric type. Scored 0.5.

**Output expectations subtotal: 7/10**

---

## Notes

The skill covers the core profiling workflow well. Two structural gaps affect the output expectations score:

1. **No stack-confirmation prompt.** When the stack is unknown (as in this scenario), the skill enumerates all profilers without asking which applies. A conditional — "if the stack is not specified, ask before recommending tools" — would close this gap cleanly.

2. **No recency-aware investigation step.** The scenario flags a feature added 3 weeks ago as a prime regression suspect. The skill has no instruction to treat recent changes as an investigation starting point or to recommend reviewing the relevant diff. This is a high-value pattern for real performance regressions that generic profiling frameworks consistently miss.

The USE/RED PARTIAL scores reflect the rubric type (both criteria are marked PARTIAL in `test.md`), not a substantive gap — Step 6 covers both methods thoroughly with descriptions, links, and application context.
