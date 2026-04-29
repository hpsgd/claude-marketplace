# Result: Load test plan for a search API endpoint

**Verdict:** PASS
**Score:** 18 / 18 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill designs all four test types (baseline, stress, endurance, spike) with distinct VUs, durations, and load patterns — Step 2 provides a table with all four types, each with distinct duration, load pattern, and VU guidance. "Do not skip any" is explicit.

- [x] PASS: Skill specifies using production-like data volume (5 million records), not an empty test database — Step 3 states "Never test against an empty database" and "Query performance degrades with table size. 100 rows ≠ 10M rows." Anti-Patterns reinforces this.

- [x] PASS: Skill includes think time in the k6 script — the Step 4 skeleton includes `sleep(1); // think time — real users don't fire requests without pause`. Zero think time is an explicit Anti-Pattern.

- [x] PASS: Success criteria (p50, p95, p99 thresholds and error rate) are defined BEFORE running the tests — Step 5 is titled "Define pass/fail thresholds BEFORE running the tests" and provides a table covering p50, p95, p99, error rate, CPU, and memory.

- [x] PASS: Endurance test duration is at least 1 hour — Step 2 specifies 1–4 hours. The output format template shows 2h as the example.

- [x] PASS: k6 script skeleton includes both `check()` for response validation and `thresholds` for automated pass/fail — both present in the Step 4 skeleton.

- [x] PASS: Skill specifies isolated environment requirement — Step 6 states "Isolated environment — Shared staging gives shared noise." Anti-Patterns lists "Shared staging" as a named violation.

- [x] PASS: Skill addresses realistic request mix — search queries should vary to avoid cache hits — Step 2 explicitly states "for a search endpoint, vary `q` from a list of representative terms" and the k6 skeleton uses `SharedArray` with randomised query selection from `queries.json`. Both prose and script enforce this.

- [x] PASS: Output includes scenarios table, thresholds table, environment requirements, and execution plan with monitoring owner — the Output Format template explicitly defines all four sections including "Monitor: [who watches]."

### Output expectations

- [x] PASS: Scenarios table includes all four test types with distinct VUs, durations, and ramp profiles — the output format template and Step 2 scenario table both cover Baseline (~50 rps), Stress (ramps to 10x), Endurance (sustained 2x, ≥1h), and Spike (sudden 5x then return to baseline).

- [x] PASS: Stress test ramps past 150 rps to find the actual breaking point — the k6 skeleton stages go from 50 → 200 → 500 VUs, well past the 150 rps target. The scenario table describes "Ramp from 1x to 10x current load" with "Find breaking point" as the purpose.

- [x] PASS: Database must contain ~5 million records for realistic behaviour — Step 3 and Anti-Patterns both make explicit that an empty test database is unacceptable and that query performance degrades with table size.

- [x] PASS: k6 script uses non-zero think time AND varies the search query across a realistic distribution — `sleep(1)` is present for think time, and the skeleton uses `SharedArray` with `queries[Math.floor(Math.random() * queries.length)]` to draw from a realistic query set, with an explicit comment: "Realistic input set — repeated identical inputs hit caches and lie about latency."

- [x] PASS: Success criteria defined BEFORE running tests with explicit p50/p95/p99 and error rate in k6 thresholds — Step 5 covers all metrics pre-test, and the skeleton encodes them in the `thresholds` block.

- [x] PASS: k6 script uses both `check()` (per-response correctness) and `thresholds` (aggregate pass/fail), shown as code — both are present in the Step 4 skeleton as runnable JavaScript, not just described.

- [x] PASS: Output requires isolated environment and names concretely what "isolated" means — Step 6 states "Concretely: dedicated DB instance, no other workloads on the host, no shared cache, no other consumers of the target service." The infrastructure components are named explicitly.

- [x] PASS: Endurance test runs ≥1 hour with memory and connection-count monitoring at fixed intervals — duration is 1–4 hours, and Step 6 specifies metrics "recorded at fixed intervals (e.g., every 5 minutes during endurance) so monotonic trends are visible, not just final values."

- [x] PASS: Execution plan names the monitoring owner and the specific metrics tracked during each test — Step 7 has a "Who monitors" row instructing the owner to be named per test type, and a "Metrics per test" row with explicit per-test breakdowns: Baseline (latency percentiles, error rate), Stress (error rate, first-failure threshold, CPU/memory saturation), Endurance (memory trend, DB connection count, GC pauses sampled at fixed intervals), Spike (recovery time, queue depth, auto-scaling behaviour).

## Notes

The skill addresses all 18 criteria cleanly after recent edits. Three things changed materially from the previous evaluation:

The k6 skeleton now uses `SharedArray` with randomised query selection, closing the cache-hit gap that was the main weakness. The comment "Repeated identical inputs hit caches and lie about latency" makes the intent explicit. Step 2's prose also calls this out directly for search endpoints.

Step 6's "Concretely:" clause names the actual infrastructure components required for isolation — dedicated DB instance, no shared cache, no other consumers. The previous version identified the problem without specifying the setup.

Step 7's "Metrics per test" row gives human monitors a concrete per-scenario checklist rather than a generic "watch dashboards" instruction.

The one gap not covered anywhere is deep-pagination performance: for a search endpoint with a `page` parameter, high Postgres offsets can be significantly slower than page 1 due to offset execution cost. The skill mentions parameterising page numbers but does not flag this characteristic or suggest a realistic page-depth distribution. Minor gap for this endpoint type, not a structural weakness.
