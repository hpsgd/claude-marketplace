# Test: Load test plan for a search API endpoint

Scenario: Developer invokes the load-test-plan skill to design load tests for `/api/search` — a full-text search endpoint over a Postgres database with 5 million records, currently serving 50 requests/second at peak.

## Prompt

Design a load test plan for `GET /api/search?q=&page=&size=`. Current production load: ~50 rps peak. The database has ~5 million records. Average response time is 180ms. We want to verify the endpoint handles 3x current load (150 rps) gracefully and find the breaking point. We also suspect there might be a memory leak under sustained load. Tool preference: k6.

Implementation requirements:

- **Production-like data volume statement**: explicit section stating the test database MUST contain ~5 million records (production-like volume), NOT an empty test DB. Cite a seed-data approach (snapshot from prod scrubbed, or `pgbench` data generator with row count).
- **Think time** in the k6 script: include `sleep(randomBetween(1, 3))` between iterations to simulate real user pacing — not zero think time.
- **k6 script skeleton** with BOTH:
  - `check()` calls for response validation (status 200, body has `results` array, `response_time < 500ms`).
  - `thresholds` config for automated pass/fail (e.g. `http_req_duration: ['p(95)<800']`, `http_req_failed: ['rate<0.01']`, `http_reqs: ['count>9000']`).
- **Test scenarios (4 phases, sequenced)**:
  1. **Baseline** — 50 rps for 5 min (matches current production load).
  2. **3× target verification** — 150 rps for 30 min (verifies the goal).
  3. **Breaking point** — ramp from 150 rps to 1000 rps over 20 min, identify where p99 crosses 2× baseline OR error rate >1%.
  4. **Memory leak detection** — sustained 100 rps for 4 hours, monitor RSS / heap on the API process every 30s, flag if monotonic increase.
- **Realistic query parameter distribution**: `q` should rotate through ~100 representative search terms (popular + long-tail), not the same string every iteration. `page` should follow Zipf distribution favouring page 1.
- **Pre-flight infrastructure check**: state required environment — k6 binary version, target environment URL, monitoring dashboard for RSS/CPU during run.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

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
