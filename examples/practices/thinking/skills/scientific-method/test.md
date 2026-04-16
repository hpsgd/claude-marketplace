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
