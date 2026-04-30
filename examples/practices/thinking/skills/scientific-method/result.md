# Result: scientific-method performance investigation

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16.5 / 18 criteria met (91.7%) |
| **Evaluated** | 2026-04-30 |
| **Skill source** | `plugins/practices/thinking/skills/scientific-method/SKILL.md` |

## Output

The following is the simulated output this skill would produce for the given prompt.

---

## Investigation: `/api/reports/summary` p95 latency regression

### Goal

**Goal:** Restore p95 latency of `/api/reports/summary` to 120ms or below.

**Current state:** p95 = 850ms (measured via APM, past 7-day window, production traffic)

**Target state:** p95 ≤ 120ms under equivalent load conditions

**How to measure:** Same APM dashboard, same endpoint filter, same load profile, same 7-day rolling window. Success = p95 ≤ 120ms for 24 hours after the fix.

---

### Observations

| # | Observation | Source | Surprising? |
|---|---|---|---|
| 1 | p95 latency is currently 850ms — up from 120ms two weeks ago | APM dashboard | No |
| 2 | Degradation began around 2026-04-01 | APM trend graph | No |
| 3 | New aggregation query deployed 2026-04-01 | Deploy log | No |
| 4 | Caching layer added 2026-04-05 | Deploy log | No |
| 5 | Load (requests/min) has not changed significantly over the period | APM / load metrics | No |
| 6 | No alert-level error rate increase reported | Monitoring | Possibly surprising — pure latency with stable errors suggests a slow path, not failures |

**What has been tried before:** Nothing — investigation is just starting.

**What measurements exist:** p95 latency via APM, deploy timestamps, request volume. Query execution logs may exist depending on DB logging configuration.

**What's missing:** p99 latency, p50 latency (to understand distribution shape), cache hit/miss rate, query execution time isolated from the full request path, DB slow query log, EXPLAIN ANALYZE on the new aggregation query, replica lag if reads are routed to a replica.

---

### Hypotheses

| # | Hypothesis | If true, expect to see | If false, expect to see | Likelihood |
|---|---|---|---|---|
| H1 | The new aggregation query (deployed 2026-04-01) is the bottleneck — table scan, missing index, or expensive join on the underlying data | EXPLAIN ANALYZE shows >700ms on the aggregation query alone; slow query log captures it; latency correlates with data volume being aggregated | Isolated query execution is fast (<50ms); bypassing the new query restores latency | High |
| H2 | The caching layer (deployed 2026-04-05) is making things worse — cache misses on every request, serialisation overhead, or an added network hop that exceeds the old compute cost | Cache hit rate near 0%; bypassing the cache entirely and hitting the DB directly returns latency closer to pre-cache levels; cache key is too granular (per-user/per-param, never hits) | Cache hit rate is reasonable (>70%); bypassing the cache does not materially change latency | Medium |
| H3 | Neither deploy is the direct cause — background job contention, stale DB statistics, or replica lag is the actual driver | DB statistics were last updated around 2026-04-01; ANALYZE/UPDATE STATISTICS shows query plan changed; or replica lag metrics show growing delay on the replica serving reads | Query plan unchanged pre/post deploy; no replica lag; no background jobs running at the degradation start | Low |

---

### Experiment

**Testing hypothesis:** H1

**Variable (what changes):** Run the aggregation query directly against the DB (bypassing the application and cache), isolated from the full request path, using EXPLAIN ANALYZE.

**Control (what stays the same):** Same DB instance, same data volume, same replica routing as production. No application-layer changes.

**Measurement:** Wall-clock execution time of the aggregation query reported by EXPLAIN ANALYZE.

**Expected result if hypothesis is correct:** Query execution time ≥ 700ms. Planner shows a sequential scan or a nested loop join on a large table. The query alone accounts for the observed latency.

**Expected result if hypothesis is wrong:** Query execution time < 100ms. The planner uses an index. The bottleneck is elsewhere in the request path (cache layer, serialisation, application code).

**Time budget:** 30 minutes — run EXPLAIN ANALYZE, read the plan, record the number.

---

### Results

*(To be completed after the experiment runs.)*

**What happened:** [Record the EXPLAIN ANALYZE output — total execution time, scan type, row estimates vs actuals]

**Expected outcome matched:** Yes / No / Partially

**Quantitative result:** [e.g. "Seq scan on report_items, 847ms total execution time, 1.2M rows scanned with no index on created_at"]

**Unexpected observations:** [e.g. "Row estimate was 1,000; actual was 1,200,000 — statistics are badly stale"]

---

### Analysis

*(To be completed after results are recorded.)*

**Hypothesis H1 status:** Confirmed / Refuted / Inconclusive

**Distance from goal:** [e.g. "Still 847ms away from the 120ms target — query is the full bottleneck"]

**What we learned:** [e.g. "The aggregation query on report_items has no index on the date range filter. The query plan changed when the new aggregation was added."]

**What we still don't know:** [e.g. "Whether adding the index is sufficient alone, or whether the query also needs to be rewritten to reduce the aggregation scope"]

---

### Next Action

**If H1 confirmed (query is the bottleneck):**

Fix the query — add the missing index, rewrite to reduce scan scope, or materialise the aggregation as a pre-computed projection. Re-run the experiment after the single fix. Validate p95 returns to ≤120ms in the APM dashboard over a 24-hour window. Document the root cause in `/learning`.

If the fix is not immediately deployable, reverting the 2026-04-01 aggregation query deploy is a temporary mitigation to restore production performance while the proper fix is developed and reviewed.

**If H1 refuted (query is fast):**

Move to H2. Design a new experiment: bypass the caching layer entirely for the endpoint (feature-flag or environment variable), measure p95 with cache disabled, compare to the current 850ms. Change only that one thing.

**If inconclusive:**

Instrument better. Enable DB slow query logging, add request-level tracing to capture time spent in query vs cache vs serialisation, and redo Step 5 with more precise data.

---

## Criteria results

### Criteria (skill definition)

- [x] PASS: Step 1 defines a measurable goal with current state, target state, and how success is measured — met: template has `**Current state:**`, `**Target state:**`, `**How to measure:**` fields; rules explicitly require "a number or a binary pass/fail condition"
- [x] PASS: Step 2 observes and records current facts before forming hypotheses — met: observation table precedes hypotheses; template includes `**What has been tried before:**`, `**What measurements exist:**`, `**What's missing:**`; rules frame observation as a pre-hypothesis step
- [x] PASS: Step 3 generates a minimum of 3 distinct, falsifiable hypotheses — met: template shows H1–H3 rows; rules state "Minimum 3 hypotheses. If you can only think of one, you don't understand the problem yet"; falsifiability required
- [x] PASS: Each hypothesis includes "if true, expect to see" and "if false, expect to see" columns — met: hypothesis table has explicit columns for both; rules call the "if false" column "the most important"
- [x] PASS: Step 4 experiment targets the highest-likelihood hypothesis with a single variable change and a pre-stated expected outcome — met: step 4 opens "For the highest-likelihood hypothesis"; template includes both expected-result fields
- [x] PASS: The skill enforces the rule that only one variable changes per experiment — met: step 4 rules state "Change ONE variable at a time"; repeated in global Rules section and Quick Diagnosis Mode
- [x] PASS: Steps 5 and 6 are structured to record actual results vs predicted, and return a hypothesis verdict — met: step 5 has `**Expected outcome matched:** Yes / No / Partially`; step 6 has `**Hypothesis H[N] status:** Confirmed / Refuted / Inconclusive`
- [~] PARTIAL: Step 7 determines next action based on the verdict — partially met (capped at 0.5 per PARTIAL criterion type): step 7 maps all verdict branches explicitly — goal met → document; hypothesis refuted → return to Step 4; stuck → /first-principles. Both branches named in the criterion are present. One branch is missing: "goal not met, hypothesis confirmed" (fix didn't work) routes back to Step 3, which is correct but only implicit in "Revise the approach, return to Step 3."

### Output expectations (simulated output)

- [x] PASS: Output's measurable goal is concrete — "restore p95 to 120ms or below" with how-measured (same APM metric, same window, same load)
- [x] PASS: Output's observations include specific facts — current 850ms, previous 120ms, two deploys with dates, load unchanged — and notes what's missing (p99, cache hit rate, query plan, slow query log)
- [x] PASS: Output generates at least 3 distinct hypotheses — H1 aggregation query, H2 caching layer, H3 background contention / stale statistics / replica lag
- [x] PASS: Output's hypotheses each include "if true" / "if false" columns — both populated with specific, testable predictions (e.g. H1 true: EXPLAIN ANALYZE shows >700ms; H1 false: query is fast, <50ms)
- [x] PASS: Output's experiment design changes ONE variable — EXPLAIN ANALYZE in isolation, no application-layer change, no cache bypass in the same experiment
- [x] PASS: Output prioritises H1 first with reasoning grounded in timing — degradation started ~2026-04-01, same date as the aggregation query deploy; reasoning stated
- [x] PASS: Output's experiment has a pre-stated expected outcome — both "if correct" and "if wrong" outcomes stated before any results are recorded
- [x] PASS: Output's record-results step structures actual vs predicted — fields for what happened, whether expected outcome matched, quantitative result, and unexpected observations
- [x] PASS: Output's verdict drives the next action explicitly — confirmed → fix query (with index/rewrite/materialise), refuted → H2 experiment, inconclusive → instrument better and redo
- [~] PARTIAL: Output addresses the rollback option — partially met: the simulated output above includes the rollback path ("reverting the 2026-04-01 deploy is a temporary mitigation") in the Next Action section. However, the skill definition itself contains no mention of rollback, revert, or temporary mitigation — this was added by inference during simulation, not prompted by the skill. A developer following the skill template without this evaluation would not produce that path.

## Notes

The skill is structurally complete and well-enforced. The single-variable rule does the most important work for the two-deployment scenario: it prevents the common mistake of reverting both changes simultaneously and losing the ability to attribute the fix.

The minimum-3-hypotheses rule earns its place here — the user named two suspects (query and cache), and the rule forces at least one alternative (H3). Without it, an investigator running this in the wild would likely test only the two suspects and miss a stale statistics problem or replica lag if those aren't the cause.

The one real gap: the skill routes "hypothesis confirmed" straight to "fix and document" with no acknowledgment that the fix might take time. For a production latency regression at 850ms, the window between "we know the cause" and "the fix is deployed" could be hours or days. The rollback-as-temporary-mitigation path is absent from the skill's Step 7 routing table. A developer following the template exactly would not be prompted to consider it.

The `**Time budget:**` field in step 4 has no guidance on reasonable defaults for latency investigations — minor omission, but the field prompts for a value without helping the investigator calibrate what's reasonable.
