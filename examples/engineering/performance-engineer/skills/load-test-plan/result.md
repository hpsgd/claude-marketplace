# Result: Load test plan for a search API endpoint

**Verdict:** PARTIAL
**Score:** 14.5 / 18.5 criteria met (78%)
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

- [~] PARTIAL: Skill addresses realistic request mix — search queries should vary to avoid cache hits — Step 2 mentions "Request mix: percentage of different operations" and Step 3 covers "Realistic data distribution." These address structural variety but neither the prose nor the script skeleton explicitly instructs varying query string parameters to avoid Postgres query cache hits on repeated identical searches. Implied, not enforced. 0.5.

- [x] PASS: Output includes scenarios table, thresholds table, environment requirements, and execution plan with monitoring owner — the Output Format template explicitly defines all four sections including "Monitor: [who watches]."

### Output expectations

- [x] PASS: Scenarios table includes all four test types with distinct VUs, durations, and ramp profiles — the output format template and Step 2 scenario table both cover Baseline (~50 rps), Stress (ramps to 10x), Endurance (sustained 2x, ≥1h), and Spike (sudden 5x then return to baseline).

- [x] PASS: Stress test ramps past 150 rps to find the actual breaking point — the k6 skeleton stages go from 50 → 200 → 500 VUs, well past the 150 rps target. The scenario table describes "Ramp from 1x to 10x current load" with "Find breaking point" as the purpose.

- [x] PASS: Database must contain ~5 million records for realistic behaviour — Step 3 and Anti-Patterns both make explicit that an empty test database is unacceptable and that query performance degrades with table size.

- [~] PARTIAL: k6 script uses non-zero think time AND varies the search query across a realistic distribution — think time is present (`sleep(1)`). Query variation is not: the skeleton uses a static `http.get('https://api.example.com/endpoint')` with no parameterization. The skill's "Realistic data distribution" guidance implies this but does not enforce it in the script or explicitly name the cache-hit risk for repeated identical search terms. 0.5.

- [x] PASS: Success criteria defined BEFORE running tests with explicit p50/p95/p99 and error rate in k6 thresholds — Step 5 covers all metrics pre-test, and the skeleton encodes them in the `thresholds` block.

- [x] PASS: k6 script uses both `check()` (per-response correctness) and `thresholds` (aggregate pass/fail), shown as code — both are present in the Step 4 skeleton as runnable JavaScript, not just described.

- [~] PARTIAL: Output requires isolated environment and names concretely what "isolated" means — Step 6 and Anti-Patterns address shared staging, production-like sizing, and pre-flight baseline checks. However the skill does not spell out what "isolated" means in terms of infrastructure components (dedicated DB instance, no other workloads on the host, no shared caches). The guidance identifies the problem but not the concrete setup checklist. 0.5.

- [~] PARTIAL: Endurance test runs ≥1 hour with memory and connection-count monitoring at fixed intervals — the 1–4 hour duration is covered. Memory and DB connections are mentioned in Step 6 as observable metrics. Fixed-interval monitoring cadence is not specified; the skill says metrics "must be observable" but not "check every N minutes and record the trend." 0.5.

- [~] PARTIAL: Execution plan names the monitoring owner and the specific metrics tracked during each test — Step 7 includes a "Who monitors" row and references dashboards. The output format template has "Monitor: [who watches]." However the skill does not break down which metrics to track per test type (e.g., for endurance: memory trend and connection count; for stress: error rate and first-failure threshold). 0.5.

- [ ] PARTIAL: Output addresses pagination distribution (page parameter) — the skill does not mention pagination variation or that high page numbers exercise different code paths. Not addressed anywhere in the skill. 0.

## Notes

The skill is well-structured and covers the core load testing discipline reliably. Anti-Patterns does active work naming the most common mistakes as failures rather than leaving developers to infer them.

The main gap for a search-specific scenario is query string parameterization. The skill's skeleton shows a static URL, which for a full-text search endpoint would trigger repeated Postgres query cache hits and produce artificially low latency. A single note under Step 3 or Step 4 — "for search endpoints, parameterise `q` from a file of realistic search terms; repeated identical queries warm Postgres query cache and inflate results" — would close this.

The monitoring granularity gap (fixed-interval checks, per-test metric breakdown) is a real weakness for the memory leak use case specifically. Saying "memory must be observable" is not the same as "record memory every 5 minutes during endurance and plot as a time series." A monotonic upward trend requires interval data — a final snapshot is not enough.

Pagination distribution is absent entirely. High page numbers (deep pagination) in Postgres can be significantly slower than page 1 due to offset execution. For a realistic search endpoint test, the `page` parameter distribution matters.
