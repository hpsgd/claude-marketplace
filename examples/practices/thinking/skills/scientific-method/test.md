# Test: scientific-method performance investigation

Scenario: A backend API endpoint has degraded from 120ms to 850ms p95 over the past two weeks. The scientific method skill is invoked to investigate without jumping to conclusions.

## Prompt

/scientific-method The `/api/reports/summary` endpoint has degraded from 120ms to 850ms p95 over the past 2 weeks. We deployed a new aggregation query on 2026-04-01 and added a caching layer on 2026-04-05. Load hasn't changed significantly. I'm not sure if it's the query, the cache, or something else.

## Criteria

- [ ] PASS: Step 1 defines a measurable goal with current state (850ms), target state (back to 120ms), and how success is measured
- [ ] PASS: Step 2 observes and records current facts before forming hypotheses — includes what data exists, what's been tried, and what's missing
- [ ] PASS: Step 3 generates a minimum of 3 distinct, falsifiable hypotheses — not just the one the user already suspects
- [ ] PASS: Each hypothesis includes "if true, expect to see" and "if false, expect to see" columns — the falsification criteria
- [ ] PASS: Step 4 experiment targets the highest-likelihood hypothesis with a single variable change and a pre-stated expected outcome
- [ ] PASS: The skill enforces the rule that only one variable changes per experiment — does not propose changing both the query and the cache simultaneously
- [ ] PASS: Steps 5 and 6 are structured to record actual results vs predicted, and return a hypothesis verdict (confirmed/refuted/inconclusive)
- [ ] PARTIAL: Step 7 determines next action based on the verdict — goal met leads to documentation, refuted hypothesis leads back to Step 4 with the next hypothesis

## Output expectations

- [ ] PASS: Output's measurable goal is concrete — "restore p95 to 120ms or below" — not "make it faster" — with how-measured (the same APM metric, same time window, same load conditions)
- [ ] PASS: Output's observations include specific facts — current p95 850ms, previous p95 120ms, 2 deploys (aggregation query 2026-04-01, cache layer 2026-04-05), load unchanged — and notes what's missing (e.g. p99, error rate, cache hit rate, query plan)
- [ ] PASS: Output generates at least 3 distinct hypotheses — at minimum: H1 the new aggregation query is the cause (table scan, missing index, expensive join), H2 the caching layer is the cause (cache misses thrashing, network hop added, serialisation overhead), H3 something else (background job contention, DB statistics stale, replica lag if reads went to a replica)
- [ ] PASS: Output's hypotheses each include "if true, expect to see" / "if false, expect to see" columns — e.g. for H1 true: query alone in EXPLAIN ANALYZE shows >700ms; for H2 true: bypass cache returns to 120ms-ish
- [ ] PASS: Output's experiment design changes ONE variable — does not propose to revert both deploys simultaneously, even though that would "fix" the symptom
- [ ] PASS: Output prioritises the highest-likelihood hypothesis first — likely H1 (the aggregation query is the more invasive change) — with reasoning grounded in the timing (degradation started ~2 weeks ago aligns with 2026-04-01)
- [ ] PASS: Output's experiment has a pre-stated expected outcome — "if H1 confirmed, EXPLAIN ANALYZE on the new query shows >700ms; otherwise the query is not the bottleneck and we move to H2"
- [ ] PASS: Output's record-results step structures actual vs predicted — a table with predicted outcome, actual measurement, verdict (CONFIRMED / REFUTED / INCONCLUSIVE)
- [ ] PASS: Output's verdict drives the next action explicitly — confirmed → fix the query (add index, rewrite, materialise), refuted → next hypothesis with the same rigour, inconclusive → instrument better and redo
- [ ] PARTIAL: Output addresses the rollback option — if the issue is the aggregation query AND a fix isn't immediate, reverting that deploy is a temporary mitigation while the proper fix is developed
