# Scientific method performance investigation

A backend API endpoint has degraded from 120ms to 850ms p95 over the past two weeks. The scientific method skill is invoked to investigate without jumping to conclusions.

## Prompt

> /scientific-method The `/api/reports/summary` endpoint has degraded from 120ms to 850ms p95 over the past 2 weeks. We deployed a new aggregation query on 2026-04-01 and added a caching layer on 2026-04-05. Load hasn't changed significantly. I'm not sure if it's the query, the cache, or something else.

```markdown

## Output

### Investigation: /api/reports/summary latency degradation

#### Goal


| Field | Value |
|---|---|
| Goal | Reduce p95 latency of `/api/reports/summary` to ≤150ms |
| Current state | 850ms p95 (as of today) |
| Target state | ≤150ms p95 (120ms was the baseline; 150ms allows for modest acceptable overhead) |
| How to measure | p95 latency over a 10-minute steady-state window under representative load, sampled from APM or from a load test against staging with production-equivalent data |


---

#### Observations

| # | Observation | Source | Surprising? |
|---|---|---|---|
| 1 | p95 latency is 850ms — 7x the 120ms baseline | APM / user report | No |
| 2 | New aggregation query deployed 2026-04-01 | Deploy log | No |
| 3 | Caching layer added 2026-04-05 | Deploy log | No |
| 4 | Load (requests/min) has not changed significantly | APM metrics | No |
| 5 | Degradation onset is unknown — did it spike on 04-01, 04-05, or gradually? | Unknown | Yes |
| 6 | No mitigation attempts have been made | User report | Yes — 850ms with no rollback attempted |

**What has been tried before:** Nothing.

**What measurements exist:** Deploy timestamps (04-01, 04-05), current p95 (850ms), baseline (120ms), presumably APM traces if the team has monitoring.

**What's missing:**
- p95 trend over time — the exact onset date is unknown
- Database query execution time for the aggregation query in production
- Cache hit rate and miss latency breakdown
- Request trace breakdown showing time in DB vs app vs network
- Query execution plan from `EXPLAIN ANALYZE`

---

#### Hypotheses

| # | Hypothesis | If true, expect to see | If false, expect to see | Likelihood |
|---|---|---|---|---|
| H1 | The aggregation query (04-01) runs a full table scan due to a missing index | Seq Scan in query plan; query duration ≈700ms+; latency trend spikes starting 04-01 | Index Scan in query plan; query duration <50ms | High |
| H2 | The caching layer (04-05) has low hit rate — cache misses route to an already-slow backend with added overhead | Hit rate <40%; miss latency ≈850ms; no improvement from the 04-05 deploy | Hit rate >80%; cache hit latency much lower than miss latency | Medium |
| H3 | Response serialisation is the bottleneck — the aggregation produces a large payload that is slow to marshal | Query finishes <100ms; serialisation/response takes 700ms+; response payload >500KB | Query duration dominates in trace; payload is small | Low |
| H4 | Connection pool contention — a background job or new query competes for DB connections | P95 much worse than p50; latency correlates with scheduled job timing; pool exhaustion visible in logs | P50 and P95 degrade proportionally; no schedule correlation | Low |

---

#### Experiment design

**Testing hypothesis:** H1 (aggregation query — full table scan)

**Variable (what changes):** Nothing in the application changes — this is a measurement experiment, not a code change.

**Control:** Caching layer stays on, load unchanged, no code changes.

**Measurement:**
1. Run `EXPLAIN ANALYZE` on the aggregation query against a production replica or staging with representative data
2. Check APM trace — what percentage of request time is spent in the database?
3. Check p95 trend from APM — does a spike appear starting 2026-04-01?

**Expected result if H1 is correct:** `EXPLAIN ANALYZE` shows `Seq Scan`; query cost is high; APM shows 80%+ of request time in DB; latency trend begins spiking from 04-01.

**Expected result if H1 is wrong:** `EXPLAIN ANALYZE` shows index usage; query finishes in <100ms; APM shows time spent outside the database; onset may be 04-05.

**Time budget:** 20 minutes to gather query plan and APM trace. If inconclusive, move to H2.

**Do not change both the query and the caching layer simultaneously — one variable per experiment. If H1 is confirmed by adding an index and latency improves but does not reach target, that is a separate experiment.**

---

#### Results

(To be filled after running the experiment)


| Field | Value |
|---|---|
| What happened | [factual description of outcome] |
| Expected outcome matched | Yes / No / Partially |
| Quantitative result | [p95 reading, query plan output, trace breakdown] |
| Unexpected observations | [anything not predicted] |


---

#### Analysis

(To be filled after results)


| Field | Value |
|---|---|
| Hypothesis H1 status | Confirmed / Refuted / Inconclusive |
| Distance from goal | [current p95 vs ≤150ms target] |
| What we learned | [new knowledge from this cycle] |
| What we still don't know | [remaining uncertainty] |


---

#### Next Action

- **H1 confirmed:** Add the missing index. Retest p95 in a 10-minute window. If ≤150ms → document what worked and why, and what would cause regression. Done.
- **H1 confirmed but goal not met:** Index added, query faster, but p95 still above target. Return to Step 3 with revised hypotheses — the problem is now partly understood but not solved.
- **H1 refuted:** Move to H2. Design a measurement experiment: measure cache hit rate and miss latency separately without changing either the query or the caching configuration.
- **H1 inconclusive:** Tighten the experiment — get a cleaner query plan from a replica with production-scale data. Do not re-interpret ambiguous results as confirmation.
- **Stuck:** Use `/first-principles` to challenge the framing. Could the degradation have started before 04-01? Could it be data volume growth independent of the deployment?
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Step 1 defines measurable goal with current state, target state, and measurement method — the skill's Step 1 template requires `Goal`, `Current state`, `Target state`, and `How to measure`, with the rule "Every goal must have a number or a binary pass/fail condition." The output provides all four fields with specific numbers (850ms current, ≤150ms target) and a concrete measurement method (p95 over 10-minute steady-state window).
- [x] PASS: Step 2 observes facts before forming hypotheses — the skill states "Gather data about the current state BEFORE forming hypotheses. Observation without hypothesis prevents confirmation bias." The observation table template requires Source and Surprising columns, plus fields for "What has been tried before," "What measurements exist," and "What's missing." All fields are populated before the Hypotheses section.
- [x] PASS: Step 3 generates minimum 3 distinct falsifiable hypotheses — the skill's Rules section states "Minimum 3 hypotheses. If you can only think of one, you don't understand the problem yet." The output produces 4 hypotheses (query full table scan, cache hit rate, serialisation, connection pool contention) covering causes beyond the two the user already named.
- [x] PASS: Each hypothesis includes both "if true" and "if false" columns — the skill's hypothesis table template explicitly defines "If true, expect to see" and "If false, expect to see" as required columns. All four hypotheses have specific, distinct predictions for both outcomes — the "if false" column specifies what would change the investigator's mind about each hypothesis.
- [x] PASS: Step 4 targets highest-likelihood hypothesis with single variable and pre-stated outcome — the skill mandates "For the highest-likelihood hypothesis, design the smallest test" and the template requires `Variable (what changes)`, `Expected result if hypothesis is correct`, and `Expected result if hypothesis is wrong`. H1 (rated High likelihood) is selected, the experiment changes nothing (measurement only), and expected outcomes are stated before any measurement runs.
- [x] PASS: One variable per experiment enforced — the skill's Rules section states "Change ONE variable at a time. Changing multiple things makes results uninterpretable." The experiment design explicitly notes "Do not change both the query and the caching layer simultaneously" and treats the two-deploy scenario as requiring separate measurement experiments.
- [x] PASS: Steps 5 and 6 structured to record actual vs predicted with hypothesis verdict — Step 5 template requires `Expected outcome matched: Yes / No / Partially` and `Unexpected observations`. Step 6 template requires `Hypothesis H[N] status: Confirmed / Refuted / Inconclusive` and `Distance from goal`. Both templates appear in the output ready for results.
- [~] PARTIAL: Step 7 determines next action based on verdict — the skill defines four iteration paths (Goal met → document; hypothesis confirmed but goal not met → revise approach; hypothesis refuted → next hypothesis; Stuck → first-principles). The output covers all four paths as a decision tree, correctly matching the skill's Step 7 structure. PARTIAL ceiling applies regardless.

### Notes

The minimum-3-hypotheses rule is doing important work here — the user already named two suspects (query, cache), and the rule forces exploration of alternatives (serialisation, connection pool). The "if false, expect to see" column is the most analytically valuable element in the template: it makes falsification criteria explicit before the experiment runs. The single-variable rule prevents a common mistake in debugging: changing two things simultaneously and not knowing which one fixed the problem. The Quick Diagnosis Mode section in the definition (for the 15-minute rule) is not invoked here, which is correct — this is a sustained investigation, not a quick debug cycle.
