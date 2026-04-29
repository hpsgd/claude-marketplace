# Test: Load test plan for a search API endpoint

Scenario: Developer invokes the load-test-plan skill to design load tests for `/api/search` — a full-text search endpoint over a Postgres database with 5 million records, currently serving 50 requests/second at peak.

## Prompt

Design a load test plan for `GET /api/search?q=&page=&size=`. Current production load: ~50 rps peak. The database has ~5 million records. Average response time is 180ms. We want to verify the endpoint handles 3x current load (150 rps) gracefully and find the breaking point. We also suspect there might be a memory leak under sustained load. Tool preference: k6.

## Criteria

- [ ] PASS: Skill designs all four test types: baseline, stress, endurance, and spike — with distinct VU counts, durations, and load patterns for each
- [ ] PASS: Skill specifies using production-like data volume (5 million records) — not an empty test database
- [ ] PASS: Skill includes think time in the k6 script — not zero think time between requests
- [ ] PASS: Success criteria (p50, p95, p99 thresholds and error rate) are defined BEFORE running the tests
- [ ] PASS: Endurance test duration is at least 1 hour to detect the suspected memory leak
- [ ] PASS: k6 script skeleton includes both `check()` for response validation and `thresholds` for automated pass/fail
- [ ] PASS: Skill specifies an isolated environment requirement — shared staging produces unreliable results
- [ ] PARTIAL: Skill addresses the realistic request mix — search queries should vary (not repeat the same query, which would be cached)
- [ ] PASS: Output includes scenarios table, thresholds table, environment requirements, and execution plan with monitoring owner

## Output expectations

- [ ] PASS: Output's scenarios table includes all four test types — baseline (~50 rps), stress (150 rps and beyond to find the breaking point), endurance (sustained, ≥1 hour for the suspected memory leak), spike — with distinct VU counts, durations, and ramp profiles per type
- [ ] PASS: Output's stress test ramps past 150 rps to find the actual breaking point (e.g. step up by 25 rps at intervals until error rate or latency thresholds are exceeded), not just confirming 150 rps works
- [ ] PASS: Output specifies the database must contain ~5 million records (production-like volume) for the search endpoint to behave realistically, and that an empty test database is unacceptable
- [ ] PASS: Output's k6 script uses non-zero think time between iterations and varies the search query (`q`) across a realistic distribution rather than repeating the same query (which Postgres would cache and inflate results)
- [ ] PASS: Output's success criteria are defined BEFORE running tests — explicit p50, p95, p99 latency thresholds and an error rate ceiling — and are encoded in k6 `thresholds` for automated pass/fail
- [ ] PASS: Output's k6 script skeleton uses both `check()` (per-response correctness validation) and `thresholds` (aggregate pass/fail), shown as code, not just described
- [ ] PASS: Output requires an isolated environment with no other workloads — production or shared staging produces noisy results — and names what "isolated" means concretely (dedicated DB, no other consumers)
- [ ] PASS: Output's endurance test runs at least 1 hour, with memory and connection-count monitoring at fixed intervals, so a leak can be detected as a monotonic upward trend
- [ ] PASS: Output's execution plan names the monitoring owner and the metrics they track during each test (DB connection count, server memory, GC pauses, error logs)
- [ ] PARTIAL: Output addresses pagination distribution (`page` parameter) — high page numbers exercise different code paths and may have worse latency than page 1, so realistic pagination should be in the test mix
