# Test: API latency regression investigation

Scenario: User reports that API response times have degraded significantly under load, with P99 climbing from 200ms to 2s, and asks the performance engineer to investigate.

## Prompt

Our API is getting slow under load. Two weeks ago P99 was around 200ms. Now it's hitting 2 seconds. P50 is still okay at about 180ms — it's the tail latency that's the problem. We're seeing this mostly on `GET /api/reports/{id}` and `POST /api/exports`. Traffic has grown about 30% in the past two weeks but that shouldn't explain a 10x P99 increase. We deploy multiple times a day so it's hard to pinpoint which change caused it. Can you investigate?

## Criteria

- [ ] PASS: Agent establishes a baseline measurement before recommending any fixes — records the exact current metrics (P50, P95, P99, throughput, error rate)
- [ ] PASS: Agent follows the outside-in bottleneck identification: end-to-end timing breakdown before diving into database or code
- [ ] PASS: Agent checks for database-level issues: N+1 queries, missing indexes, full table scans, and lock contention
- [ ] PASS: Agent applies the one-change-at-a-time rule — does not recommend changing multiple things simultaneously
- [ ] PASS: Agent recommends profiling tools appropriate to the likely stack before proposing optimisations
- [ ] PASS: Agent raises a decision checkpoint before recommending infrastructure scaling changes (cost and architecture implications)
- [ ] PASS: Agent notes that P50 vs P99 divergence is a tail latency signal — suggests investigating resource contention and connection pool exhaustion under concurrency rather than average-case code paths
- [ ] PARTIAL: Agent produces a prioritised findings table with impact (HIGH/MEDIUM/LOW), component, and recommended fix
- [ ] PASS: Agent specifies that every optimisation must have a before/after measurement using the same load and same metric
