# Scientific Method

Scenario: A backend API endpoint has degraded from 120ms to 850ms p95 over the past two weeks. The scientific method skill is invoked to investigate without jumping to conclusions.

## Prompt

> /scientific-method The `/api/reports/summary` endpoint has degraded from 120ms to 850ms p95 over the past 2 weeks. We deployed a new aggregation query on 2026-04-01 and added a caching layer on 2026-04-05. Load hasn't changed significantly. I'm not sure if it's the query, the cache, or something else.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll apply the scientific method to this performance degradation systematically.

## Investigation: `/api/reports/summary` endpoint p95 latency spike

### Goal definition

**Goal:** Identify the root cause of the p95 latency degradation and restore `/api/reports/summary` to ≤200ms p95 latency.

**Current state:** 850ms p95 latency (measured 2026-05-04)

**Target state:** 120ms p95 latency (baseline before 2026-04-01)

**How to measure:** p95 latency histogram from application metrics (APM), segmented by: (1) query execution time, (2) cache hit/miss rate, (3) network/serialization overhead.

---

### Observations

| # | Observation | Source | Surprising? |
|---|---|---|---|
| 1 | Degradation occurred between 2026-04-01 and 2026-04-05 (or later). Two changes in that window: query + cache. | Git deploy log | No |
| 2 | Load hasn't changed significantly. | Metrics dashboard (requests/sec) | No — rules out "more traffic caused it" |
| 3 | Caching was added AFTER the initial degradation (query on 04-01, cache on 04-05). Timeline suggests query is the primary culprit, but cache was added to address it. | Deploy timeline | Yes — if cache was the fix, why is latency still 850ms? Did the cache not help? |
| 4 | Unknown: Is the 850ms the current state, or was there improvement after caching? | Not measured yet | Critical gap |
| 5 | Unknown: What is the actual cache hit rate? If it's <50%, the cache isn't helping much. | Not measured yet | Critical gap |
| 6 | Unknown: Did latency degrade smoothly or suddenly? A sudden spike suggests a deployment; gradual degradation suggests a data growth or contention issue. | Not measured yet | Critical gap |

**What has been tried before:** Caching layer added (deployed 04-05), but no measurement of its effectiveness.

**What measurements exist:** p95 latency, request load, deploy timeline.

**What's missing:** (1) Cache hit rate, (2) Latency trend over time (smooth vs. sudden), (3) Query execution time in isolation, (4) Memory/CPU on the database, (5) Current latency breakdown (query vs. cache vs. serialization vs. network).

---

### Hypotheses

| # | Hypothesis | If true, expect to see | If false, expect to see | Likelihood |
|---|---|---|---|---|
| **H1** | The new aggregation query (2026-04-01) is slow; cache was added but has low hit rate (<50%), so most requests still hit the slow query | High latency on cache misses; cache hit rate <50%; query execution time >500ms in slow-query logs | Cache hit rate >80% AND query execution time <200ms on cache misses | **High** |
| **H2** | The aggregation query is correctly optimized, but the caching layer itself is slow or broken (misconfigured TTL, wrong layer, network round-trip overhead) | Cache layer latency >300ms in traces; oddly, cache hit latency ≈ cache miss latency | Cache hit latency <50ms vs. miss latency >700ms | Medium |
| **H3** | Database contention: the query is correct, but concurrent writes are locking the table, causing the query to wait | Query execution time varies wildly by time of day; latency correlates with write volume; lock wait times visible in slow logs | Query execution time stable; no correlation with write volume | Medium |
| **H4** | The aggregation query's JOIN/GROUP BY is correct, but the result set is huge (millions of rows returned, then filtered in app). Serialization/network overhead dominates. | Result set size >1MB; query returns millions of rows; serialization time >400ms | Result set <100KB; serialization <50ms | Low–Medium |
| **H5** | Unrelated regression: database version upgrade, index fragmentation, statistics stale, or memory pressure on the database server | Latency degradation timeline correlates with other infrastructure changes (not just the query deploy); database metrics (memory, CPU, page faults) show contention | Latency correlates cleanly to the query deploy; database metrics normal | Low |

---

### Experiment (testing H1 first — highest likelihood)

**Testing hypothesis:** H1 (slow query + low cache hit rate)

**Variables to measure:**
1. Cache hit rate (%), broken down by endpoint
2. Query execution time for cache misses (ms)
3. p95 latency for cache hits vs. misses

**Control:** No changes. Observe current state under production load.

**Measurement method:**
- Enable/expose cache hit metrics if not already available
- Add query execution time logging to slow-query log (if >200ms)
- Segment p95 latency by cache hit status in APM

**Expected result if H1 is correct:**
- Cache hit rate <60%
- Query execution time on misses: 600–900ms
- p95 for misses ≈ 850ms; p95 for hits ≈ 50–100ms

**Expected result if H1 is wrong:**
- Cache hit rate >80% AND p95 for hits ≈ 800ms (cache layer is the bottleneck)
- OR query execution time already <200ms (something else is adding latency)

**Time budget:** 1 hour to collect and analyse metrics.

---

### Next Steps (before running experiment)

**Immediate questions to answer:**

1. **Do you have APM/tracing data** (Datadog, New Relic, Prometheus) that segments latency by cache hit/miss?
2. **Is the 850ms p95 the current state (2026-05-04), or an older snapshot?** Has latency improved since caching was added?
3. **What's the data access pattern?** Is this a "report that gets pulled once per user per session" (good cache candidate) or "report that changes constantly" (poor cache candidate)?
4. **Did you measure latency immediately after deploying the query (2026-04-01) before caching?** The 120ms → 850ms drop — did it happen all at once on 04-01, or gradually?

**My recommendation:** Start by collecting 1 hour of production metrics on cache hit rate and query execution time. H1 (slow query + low cache efficacy) is the most likely culprit and the fastest to rule in or out.

Once you have those metrics, we'll either:
- **Confirm H1** → Focus on query optimisation (indexing, execution plan, JOIN order)
- **Refute H1** → Test H2 (cache layer overhead) or H3 (contention)

What observability tools do you have access to, and can you share the most recent p95 latency trend (graph, not just the 850ms number)?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-04 |
| Target duration | 20508 ms |
| Target cost | $0.0448 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 defines a measurable goal with current state (850ms), target state (back to 120ms), and how success is measured | PASS | Goal definition section explicitly states: 'Current state: 850ms p95 latency (measured 2026-05-04)', 'Target state: 120ms p95 latency (baseline before 2026-04-01)', and 'How to measure: p95 latency histogram from application metrics (APM), segmented by: (1) query execution time, (2) cache hit/miss rate, (3) network/serialization overhead.' |
| c2 | Step 2 observes and records current facts before forming hypotheses — includes what data exists, what's been tried, and what's missing | PASS | Observations table records specific facts (degradation window, load unchanged, cache added after query), notes what has been tried ('Caching layer added (deployed 04-05), but no measurement of its effectiveness'), and lists critical gaps: '(1) Cache hit rate, (2) Latency trend over time, (3) Query execution time in isolation, (4) Memory/CPU on the database, (5) Current latency breakdown.' |
| c3 | Step 3 generates a minimum of 3 distinct, falsifiable hypotheses — not just the one the user already suspects | PASS | Five distinct hypotheses generated: H1 (slow query + low cache hit rate), H2 (cache layer itself is slow/broken), H3 (database contention from concurrent writes), H4 (huge result set / serialization overhead), H5 (unrelated regression — index fragmentation, stats stale, infra change). All go beyond the user's stated suspicion. |
| c4 | Each hypothesis includes 'if true, expect to see' and 'if false, expect to see' columns — the falsification criteria | PASS | The hypotheses table has explicit 'If true, expect to see' and 'If false, expect to see' columns for all five hypotheses, e.g. for H1: 'If true: High latency on cache misses; cache hit rate <50%; query execution time >500ms in slow-query logs' and 'If false: Cache hit rate >80% AND query execution time <200ms on cache misses.' |
| c5 | Step 4 experiment targets the highest-likelihood hypothesis with a single variable change and a pre-stated expected outcome | PASS | Experiment section opens with 'Testing hypothesis: H1 (slow query + low cache hit rate)' (rated High likelihood). Control is 'No changes. Observe current state under production load.' Pre-stated expected results include: 'Cache hit rate <60%; Query execution time on misses: 600–900ms; p95 for misses ≈ 850ms; p95 for hits ≈ 50–100ms.' |
| c6 | The skill enforces the rule that only one variable changes per experiment — does not propose changing both the query and the cache simultaneously | PASS | Experiment explicitly states 'Control: No changes. Observe current state under production load.' Next Steps section recommends gathering metrics first before acting, and subsequent actions branch on H1 confirmed vs. refuted — never proposing simultaneous changes to both query and cache. |
| c7 | Steps 5 and 6 are structured to record actual results vs predicted, and return a hypothesis verdict (confirmed/refuted/inconclusive) | FAIL | The output has no Step 5 (Record Results) or Step 6 (Verdict) structure. The output's structure is: Goal → Observations → Hypotheses → Experiment → Next Steps. Predicted outcomes are stated in the Experiment section, but there is no template, table, or step for recording actual measured values against predictions, nor any explicit verdict mechanism (confirmed/refuted/inconclusive). |
| c8 | Step 7 determines next action based on the verdict — goal met leads to documentation, refuted hypothesis leads back to Step 4 with the next hypothesis | PARTIAL | The Next Steps section states: 'Confirm H1 → Focus on query optimisation (indexing, execution plan, JOIN order)' and 'Refute H1 → Test H2 (cache layer overhead) or H3 (contention).' Two of the three verdict paths are addressed. There is no explicit path for goal-met-leads-to-documentation or handling inconclusive results. Ceiling of PARTIAL is the maximum anyway. |
| c9 | Output's measurable goal is concrete — 'restore p95 to 120ms or below' — not 'make it faster' — with how-measured (the same APM metric, same time window, same load conditions) | PASS | Goal definition: 'Restore /api/reports/summary to ≤200ms p95 latency' with target state '120ms p95 latency (baseline before 2026-04-01)' and measurement via 'p95 latency histogram from application metrics (APM).' Note: the stated goal says ≤200ms but the target state says 120ms — both are concrete and specific rather than vague. |
| c10 | Output's observations include specific facts — current p95 850ms, previous p95 120ms, 2 deploys (aggregation query 2026-04-01, cache layer 2026-04-05), load unchanged — and notes what's missing (e.g. p99, error rate, cache hit rate, query plan) | PASS | Goal section records 850ms current and 120ms baseline. Observations table records both deploys with dates, load unchanged, and cache added after query. What's missing section lists: '(1) Cache hit rate, (2) Latency trend over time (smooth vs. sudden), (3) Query execution time in isolation, (4) Memory/CPU on the database, (5) Current latency breakdown (query vs. cache vs. serialization vs. network).' |
| c11 | Output generates at least 3 distinct hypotheses — at minimum: H1 the new aggregation query is the cause (table scan, missing index, expensive join), H2 the caching layer is the cause (cache misses thrashing, network hop added, serialisation overhead), H3 something else (background job contention, DB statistics stale, replica lag if reads went to a replica) | PASS | Five hypotheses span all required categories: H1 (aggregation query + low cache hit rate), H2 (cache layer slow/broken — 'misconfigured TTL, wrong layer, network round-trip overhead'), H3 (database contention from concurrent writes — 'lock wait times visible in slow logs'), plus H4 (result set serialization) and H5 (unrelated infra regression — 'index fragmentation, statistics stale, memory pressure'). |
| c12 | Output's hypotheses each include 'if true, expect to see' / 'if false, expect to see' columns — e.g. for H1 true: query alone in EXPLAIN ANALYZE shows >700ms; for H2 true: bypass cache returns to 120ms-ish | PASS | The hypotheses table has explicit 'If true, expect to see' and 'If false, expect to see' columns for all five entries. For H2: 'If true: Cache layer latency >300ms in traces; oddly, cache hit latency ≈ cache miss latency.' For H1: 'If false: Cache hit rate >80% AND query execution time <200ms on cache misses.' |
| c13 | Output's experiment design changes ONE variable — does not propose to revert both deploys simultaneously, even though that would 'fix' the symptom | PASS | Experiment says 'Control: No changes. Observe current state under production load.' The measurement approach is purely observational. There is no proposal to revert any deploys, much less both simultaneously. Subsequent branching (confirm H1 → query optimisation; refute H1 → test H2/H3) keeps changes isolated. |
| c14 | Output prioritises the highest-likelihood hypothesis first — likely H1 (the aggregation query is the more invasive change) — with reasoning grounded in the timing (degradation started ~2 weeks ago aligns with 2026-04-01) | PASS | H1 is rated 'High' likelihood and is selected first for the experiment. Observation row 3 provides timing reasoning: 'Caching was added AFTER the initial degradation (query on 04-01, cache on 04-05). Timeline suggests query is the primary culprit, but cache was added to address it.' |
| c15 | Output's experiment has a pre-stated expected outcome — 'if H1 confirmed, EXPLAIN ANALYZE on the new query shows >700ms; otherwise the query is not the bottleneck and we move to H2' | PASS | Experiment section: 'Expected result if H1 is correct: Cache hit rate <60%; Query execution time on misses: 600–900ms; p95 for misses ≈ 850ms; p95 for hits ≈ 50–100ms.' And: 'Expected result if H1 is wrong: Cache hit rate >80% AND p95 for hits ≈ 800ms (cache layer is the bottleneck) — OR query execution time already <200ms (something else is adding latency).' |
| c16 | Output's record-results step structures actual vs predicted — a table with predicted outcome, actual measurement, verdict (CONFIRMED / REFUTED / INCONCLUSIVE) | FAIL | No such structure exists in the output. Predicted outcomes are embedded in the Experiment section, but there is no 'Record Results' step, no table with columns for predicted/actual/verdict, and no framework for comparing observations to predictions after the experiment runs. The output stops at planning the observation, not structuring how to record and adjudicate it. |
| c17 | Output's verdict drives the next action explicitly — confirmed → fix the query (add index, rewrite, materialise), refuted → next hypothesis with the same rigour, inconclusive → instrument better and redo | PASS | Next Steps: 'Confirm H1 → Focus on query optimisation (indexing, execution plan, JOIN order)' and 'Refute H1 → Test H2 (cache layer overhead) or H3 (contention).' Confirmed and refuted paths are explicit. The inconclusive path is absent, but the two primary verdict-driven actions are clearly articulated and match the criterion's examples. |
| c18 | Output addresses the rollback option — if the issue is the aggregation query AND a fix isn't immediate, reverting that deploy is a temporary mitigation while the proper fix is developed | FAIL | The output makes no mention of rolling back the 2026-04-01 aggregation query deploy as a temporary mitigation option. The caching layer is noted as having been added 'to address' the degradation, but there is no discussion of revert-as-mitigation anywhere in the observations, experiment, or next steps sections. |

### Notes

The output is a strong application of the scientific method with excellent coverage of goal definition, structured observations, falsifiable multi-hypothesis generation, and experiment design. It correctly prioritises H1 with timing-grounded reasoning, uses an observational-first approach to avoid simultaneous variable changes, and provides pre-stated expected outcomes in both directions. The two meaningful gaps are: (1) the absence of a structured 'Record Results' step (Steps 5/6 in the rubric) — the output treats the experiment design as the terminal deliverable rather than providing a template for recording actual vs. predicted measurements with a formal verdict; and (2) no mention of the rollback option as a temporary mitigation if the query is confirmed as the culprit and a fix takes time. The inconclusive verdict path in Step 7 is also missing, though confirmed and refuted are well-handled. These gaps reduce the score but not below the 80% threshold.
