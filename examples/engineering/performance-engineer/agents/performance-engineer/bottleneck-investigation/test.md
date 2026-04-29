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

## Output expectations

- [ ] PASS: Output's baseline section reproduces the exact metrics from the prompt — P50 ~180ms (still healthy), P99 was 200ms two weeks ago, P99 now 2s, 30% traffic growth — and notes the 10x P99 jump is disproportionate to traffic
- [ ] PASS: Output explicitly identifies the P50-stable / P99-degraded pattern as a tail-latency / contention signal rather than an across-the-board slowdown, and lists candidate causes (connection pool exhaustion, lock contention, GC pauses, cold cache, queueing under load)
- [ ] PASS: Output's investigation plan addresses the two named endpoints (`GET /api/reports/{id}` and `POST /api/exports`) specifically — looking at their distinct workloads (read vs write, sync vs async)
- [ ] PASS: Output proposes correlating the regression with the deployment history — using deploy timestamps to bisect the change set, since "we deploy multiple times a day" makes single-commit blame infeasible
- [ ] PASS: Output's database checks include N+1 detection, missing indexes, full table scans, and lock contention, with named tools or queries (`pg_stat_statements`, `EXPLAIN ANALYZE`, `pg_locks`) where applicable
- [ ] PASS: Output applies the one-change-at-a-time discipline — any recommended fix is followed by a re-measurement step before the next change, not a batch of optimisations
- [ ] PASS: Output names a profiling tool appropriate to the inferred stack (e.g. py-spy, async-profiler, dotnet-trace, Node clinic) before proposing code-level changes — and asks for stack confirmation if not stated
- [ ] PASS: Output stops and asks before recommending infrastructure scaling (more nodes, larger pool, bigger DB), framing the cost/architecture implications
- [ ] PASS: Output's findings table is prioritised by likely impact (HIGH/MEDIUM/LOW) with component and recommended fix per row, not a flat unranked list
- [ ] PASS: Output requires before/after measurement at the same load and same metric for every change, with the measurement protocol stated (warm-up, sample size, statistical significance)
