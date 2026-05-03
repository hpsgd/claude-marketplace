# Scientific Method

Scenario: A backend API endpoint has degraded from 120ms to 850ms p95 over the past two weeks. The scientific method skill is invoked to investigate without jumping to conclusions.

## Prompt

> /scientific-method The `/api/reports/summary` endpoint has degraded from 120ms to 850ms p95 over the past 2 weeks. We deployed a new aggregation query on 2026-04-01 and added a caching layer on 2026-04-05. Load hasn't changed significantly. I'm not sure if it's the query, the cache, or something else.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Investigation: `/api/reports/summary` p95 latency degradation

---

### Goal

**Goal:** Identify the root cause of p95 latency degradation and restore performance.
**Current state:** 850ms p95
**Target state:** ≤150ms p95 (within 25% of original 120ms baseline)
**How to measure:** p95 latency on `/api/reports/summary` over a 1-hour window under representative load, before/after each change.

---

### Observations

| # | Observation | Source | Surprising? |
|---|---|---|---|
| O1 | p95 rose from 120ms → 850ms (~7× increase) | APM/metrics | No — something broke |
| O2 | New aggregation query deployed 2026-04-01 | Deploy log | No |
| O3 | Caching layer added 2026-04-05 | Deploy log | No |
| O4 | Load has not changed significantly | Traffic metrics | No |
| O5 | Degradation observed "over past 2 weeks" — not a cliff-edge spike | Framing | **Yes** — gradual degradation despite point-in-time deploys suggests either a slow-growing data problem or cache behaviour that worsens over time |
| O6 | We don't know if p95 jumped immediately on 2026-04-01, on 2026-04-05, or drifted across both | APM history | **Yes — this is the critical missing data** |

**What has been tried:** Nothing yet.
**What measurements exist:** APM p95 timeseries, deploy timestamps.
**What's missing:** Latency breakdown by phase (query time vs cache lookup vs serialisation); cache hit/miss rate over time; EXPLAIN ANALYZE on the new aggregation query; p95 at each deploy boundary.

---

### Hypotheses

| # | Hypothesis | If true, expect to see | If false, expect to see | Likelihood |
|---|---|---|---|---|
| H1 | The new aggregation query is slow and performs a full table scan or expensive join — the 850ms is pure DB time | Latency jumped on 2026-04-01; DB query time ~700ms+; EXPLAIN shows seq scan or missing index | Latency was fine until 2026-04-05; DB query time < 50ms | **High** |
| H2 | The caching layer has a high miss rate or is actively making things worse (e.g. stampede, serialisation overhead, or cache invalidation on every write) | Latency jumped on 2026-04-05; cache hit rate low or zero; cache overhead visible in trace | Latency was bad before 2026-04-05; cache hit rate healthy | **High** |
| H3 | Data volume under the aggregation query has grown since 2026-04-01 — the query was acceptable at deploy but degrades as table grows | Latency drifts upward steadily post 2026-04-01; EXPLAIN shows row count increasing; query plan unchanged but row estimates higher | Latency was bad from day one of deploy; row counts stable | **Medium** |
| H4 | The cache TTL is too long, causing stale locks or contention when the cache entry expires and multiple requests regenerate simultaneously (thundering herd) | Latency spikes are periodic rather than uniform; spikes correlate with cache TTL interval | Latency is uniformly high at all times | Low |
| H5 | An unrelated background job or index rebuild introduced around the same time is consuming DB resources | Latency degrades during specific time windows; DB CPU/IO elevated during those windows | Latency is evenly distributed across all hours | Low |

---

### Experiment (Start here — Step 4)

**Testing hypothesis:** H1 and H2 simultaneously via read-only observation (no code change).

The first experiment is **observational** — check the APM timeseries to locate the exact inflection point, then get a query trace.

**Variable:** Nothing changes — this is measurement only.
**Control:** Production system as-is.

**Measurement steps (in order):**

1. Pull p95 latency timeseries with 1-hour granularity from 2026-03-28 to 2026-05-01.
   - **Expected if H1:** Cliff at 2026-04-01, flat since.
   - **Expected if H2:** Cliff at 2026-04-05, or gradual post-2026-04-05 worsening.
   - **Expected if H3:** Gradual slope upward from 2026-04-01.

2. Run `EXPLAIN (ANALYZE, BUFFERS)` on the new aggregation query against production (read replica if available).
   - **Expected if H1:** Sequential scan, high actual row count, >500ms execution time.
   - **Expected if H1 false:** Index scan, low row count, <50ms.

3. Pull cache hit/miss ratio for the `/api/reports/summary` cache key since 2026-04-05.
   - **Expected if H2:** Hit rate < 50%, or hit rate high but latency still high (serialisation).
   - **Expected if H2 false:** Hit rate >80%, and cache path latency is low.

**Time budget:** 30 minutes to gather this data. If the inflection point is ambiguous after step 1, that IS the result — it tells you the degradation is gradual (H3).

---

### Results

_(Run the measurements above and fill this in.)_

**What happened:** —
**Expected outcome matched:** —
**Quantitative result:** —
**Unexpected observations:** —

---

### Analysis

_(Complete after results.)_

**Decision tree based on findings:**

- Cliff on 2026-04-01 + slow EXPLAIN → **H1 confirmed** → Add index, rewrite aggregation to avoid full scan.
- Cliff on 2026-04-05 + low cache hit rate → **H2 confirmed** → Fix cache key, TTL, or invalidation logic.
- Gradual slope from 2026-04-01 + growing row count → **H3 confirmed** → Partition the aggregation or add a pre-aggregation materialized view.
- Cliff on 2026-04-05 + high cache hit rate + still slow → Cache path itself is slow → Profile serialisation and cache client overhead.

---

### Next Action

**Run Step 5 now.** The three measurements above are non-destructive, take <30 minutes, and will falsify at least two of the top three hypotheses in one pass. Do not change code until the inflection point is located — changing the query AND the cache simultaneously would make results uninterpretable.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.0 (97%) |
| Evaluated | 2026-05-01 |
| Target duration | 36410 ms |
| Target cost | $0.0690 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 defines a measurable goal with current state (850ms), target state (back to 120ms), and how success is measured | PASS | Goal section explicitly states: 'Current state: 850ms p95', 'Target state: ≤150ms p95 (within 25% of original 120ms baseline)', 'How to measure: p95 latency on `/api/reports/summary` over a 1-hour window under representative load, before/after each change.' |
| c2 | Step 2 observes and records current facts before forming hypotheses — includes what data exists, what's been tried, and what's missing | PASS | Observations table with O1–O6 (facts recorded before hypotheses), explicit 'What has been tried: Nothing yet', 'What measurements exist: APM p95 timeseries, deploy timestamps', and 'What's missing: Latency breakdown by phase... cache hit/miss rate... EXPLAIN ANALYZE... p95 at each deploy boundary.' |
| c3 | Step 3 generates a minimum of 3 distinct, falsifiable hypotheses — not just the one the user already suspects | PASS | Five distinct hypotheses H1–H5 generated: slow aggregation query (H1), caching layer issues (H2), data volume growth (H3), thundering herd/TTL (H4), background job contention (H5). Well beyond the minimum of 3. |
| c4 | Each hypothesis includes 'if true, expect to see' and 'if false, expect to see' columns — the falsification criteria | PASS | Hypothesis table explicitly includes 'If true, expect to see' and 'If false, expect to see' columns populated for all five hypotheses, e.g. H1 true: 'Latency jumped on 2026-04-01; DB query time ~700ms+; EXPLAIN shows seq scan or missing index'; H1 false: 'Latency was fine until 2026-04-05; DB query time < 50ms'. |
| c5 | Step 4 experiment targets the highest-likelihood hypothesis with a single variable change and a pre-stated expected outcome | PASS | Experiment section states 'Variable: Nothing changes — this is measurement only' (observational, no variable changed), targets H1 and H2 (both marked High likelihood), and each measurement step includes pre-stated expected outcomes per hypothesis. |
| c6 | The skill enforces the rule that only one variable changes per experiment — does not propose changing both the query and the cache simultaneously | PASS | Next Action section explicitly states: 'Do not change code until the inflection point is located — changing the query AND the cache simultaneously would make results uninterpretable.' |
| c7 | Steps 5 and 6 are structured to record actual results vs predicted, and return a hypothesis verdict (confirmed/refuted/inconclusive) | PASS | Results section provides template fields: 'What happened', 'Expected outcome matched', 'Quantitative result', 'Unexpected observations'. Analysis section provides decision tree with verdict routing: 'H1 confirmed → Add index, rewrite aggregation', 'H2 confirmed → Fix cache key', etc. |
| c8 | Step 7 determines next action based on the verdict — goal met leads to documentation, refuted hypothesis leads back to Step 4 with the next hypothesis | PARTIAL | Analysis decision tree maps measurement findings to corrective actions (add index, fix cache, partition, profile serialisation). However, no explicit 'if goal is met → document' branch, and the 'refuted → return to Step 4 with next hypothesis with the same rigor' feedback loop is implied rather than stated explicitly. |
| c9 | Output's measurable goal is concrete — 'restore p95 to 120ms or below' — not 'make it faster' — with how-measured (the same APM metric, same time window, same load conditions) | PASS | Goal states '≤150ms p95 (within 25% of original 120ms baseline)' measured via 'p95 latency on `/api/reports/summary` over a 1-hour window under representative load, before/after each change' — specific metric, time window, and load condition all specified. |
| c10 | Output's observations include specific facts — current p95 850ms, previous p95 120ms, 2 deploys (aggregation query 2026-04-01, cache layer 2026-04-05), load unchanged — and notes what's missing (e.g. p99, error rate, cache hit rate, query plan) | PASS | O1 records '120ms → 850ms', O2 records '2026-04-01 aggregation query', O3 records '2026-04-05 caching layer', O4 records 'Load has not changed'. What's missing lists 'cache hit/miss rate over time; EXPLAIN ANALYZE on the new aggregation query; p95 at each deploy boundary'. (p99/error rate not called out explicitly but the listed gaps satisfy the criterion's 'e.g.' phrasing.) |
| c11 | Output generates at least 3 distinct hypotheses — at minimum: H1 the new aggregation query is the cause (table scan, missing index, expensive join), H2 the caching layer is the cause (cache misses thrashing, network hop added, serialisation overhead), H3 something else (background job contention, DB statistics stale, replica lag if reads went to a replica) | PASS | H1 covers aggregation query/seq scan/missing index. H2 covers cache miss rate/stampede/serialisation overhead. H3 covers data volume growth (a distinct 'something else'). H4 covers thundering herd. H5 covers background job contention — all three required categories represented with extras. |
| c12 | Output's hypotheses each include 'if true, expect to see' / 'if false, expect to see' columns — e.g. for H1 true: query alone in EXPLAIN ANALYZE shows >700ms; for H2 true: bypass cache returns to 120ms-ish | PASS | H1 true: 'DB query time ~700ms+; EXPLAIN shows seq scan or missing index'. H2 true: 'Latency jumped on 2026-04-05; cache hit rate low or zero'. Explicit 'if false' columns also populated for all hypotheses. |
| c13 | Output's experiment design changes ONE variable — does not propose to revert both deploys simultaneously, even though that would 'fix' the symptom | PASS | 'Variable: Nothing changes — this is measurement only' and 'Do not change code until the inflection point is located — changing the query AND the cache simultaneously would make results uninterpretable.' No simultaneous revert proposed. |
| c14 | Output prioritises the highest-likelihood hypothesis first — likely H1 (the aggregation query is the more invasive change) — with reasoning grounded in the timing (degradation started ~2 weeks ago aligns with 2026-04-01) | PASS | H1 is listed first and rated 'High' likelihood. Measurement step 2 (EXPLAIN ANALYZE on the aggregation query) is ordered before step 3 (cache hit rate). H1's 'if true' criteria references 'Latency jumped on 2026-04-01' grounding it in timing. |
| c15 | Output's experiment has a pre-stated expected outcome — 'if H1 confirmed, EXPLAIN ANALYZE on the new query shows >700ms; otherwise the query is not the bottleneck and we move to H2' | PASS | Each measurement step has inline 'Expected if H1:', 'Expected if H2:', 'Expected if H3:' predictions. Step 2: 'Expected if H1: Sequential scan, high actual row count, >500ms execution time. Expected if H1 false: Index scan, low row count, <50ms.' |
| c16 | Output's record-results step structures actual vs predicted — a table with predicted outcome, actual measurement, verdict (CONFIRMED / REFUTED / INCONCLUSIVE) | PASS | Results section template contains 'What happened', 'Expected outcome matched' (actual vs predicted), and 'Quantitative result'. Analysis decision tree then maps findings to hypothesis outcomes ('H1 confirmed', 'H2 confirmed'). The 'Expected outcome matched' field functions as the verdict gate. |
| c17 | Output's verdict drives the next action explicitly — confirmed → fix the query (add index, rewrite, materialise), refuted → next hypothesis with the same rigour, inconclusive → instrument better and redo | PASS | Analysis decision tree: 'Cliff on 2026-04-01 + slow EXPLAIN → H1 confirmed → Add index, rewrite aggregation'; 'Cliff on 2026-04-05 + low cache hit rate → H2 confirmed → Fix cache key, TTL, or invalidation logic'; 'Gradual slope → H3 confirmed → Partition or materialized view'. Each verdict routes to a specific corrective action. |
| c18 | Output addresses the rollback option — if the issue is the aggregation query AND a fix isn't immediate, reverting that deploy is a temporary mitigation while the proper fix is developed | FAIL | The output does not mention rollback anywhere. The Analysis section for H1 confirmed goes directly to 'Add index, rewrite aggregation to avoid full scan' without noting that reverting the 2026-04-01 aggregation query deploy is a valid temporary mitigation if the fix is not immediate. |

### Notes

The captured output is an exceptionally thorough scientific-method investigation. It correctly structures all major phases: measurable goal with APM-backed target, rich observation table calling out critical missing data (the inflection point timing), five falsifiable hypotheses with both 'if true/false' columns, an observational experiment that explicitly refuses to change multiple variables simultaneously, pre-stated expected outcomes per measurement step, and a verdict-driven decision tree. The only meaningful gap is c18 — rollback as a temporary mitigation is never mentioned; the H1-confirmed path goes straight to 'fix the query' without acknowledging that reverting the 2026-04-01 deploy is an immediate option while the proper solution is developed. The c8 partial deduction is minor: the feedback loop back to Step 4 on refutation and the 'goal met → document' branch are implied but not explicitly stated. Overall a very high-quality output.
