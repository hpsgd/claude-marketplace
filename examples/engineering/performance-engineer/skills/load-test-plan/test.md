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
