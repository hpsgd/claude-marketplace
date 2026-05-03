# Strategy Review

Scenario: User asks the QA lead to define a test strategy for a new microservice that sends email, SMS, and push notifications. The service will be called by multiple other services via an internal API.

## Prompt

> We're building a new notifications microservice. It receives requests from other internal services (via a REST API), queues them, and delivers via Sendgrid (email), Twilio (SMS), and Firebase (push). There's a preference/opt-out system per user per channel. The service needs to handle ~50,000 notifications/day at launch, growing to ~500,000 within 12 months. Can you define the test strategy before we start development?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the test strategy framework for your notifications microservice. This is a HIGH-risk system (user data integrity, opt-out compliance, financial cost exposure via Twilio/Sendgrid), so we'll shift the testing pyramid significantly toward integration and E2E.

## Test Strategy: Notifications Microservice

### Risk Assessment

**Risk profile:** Data integrity (wrong user, opt-outs), Financial (API overage), Compliance (preference enforcement), Reliability (lost/duplicate notifications)

**Critical flows:**
1. Request → validation → queue → delivery (happy path)
2. User opts out → preference lookup → skipped delivery
3. Delivery failure → retry with backoff → DLQ on max retries
4. Request deduplication → single delivery despite duplicate requests

**Failure modes (risk level):**
- Notification sent to opted-out user **(HIGH - compliance violation)**
- Duplicate delivery **(HIGH - reputation, user frustration)**
- Lost notification (not persisted/delivered) **(HIGH - business impact)**
- Notification sent to wrong user **(CRITICAL - data integrity)**
- Queue message loss on restart **(HIGH - reliability)**
- Unbounded API calls to Twilio/Sendgrid **(HIGH - financial)**
- Queue backlog / cascading timeout **(MEDIUM - operational)**
- Invalid request causes service crash **(MEDIUM - stability)**
- Preference cache out of sync **(MEDIUM - data consistency)**
- Third-party outage blocks all delivery **(MEDIUM - resilience)**

### Test Levels

| Level | Scope | Tools | Target | Est. Tests |
|---|---|---|---|---|
| **Unit** | Preference resolution, deduplication, retry logic, validation, rate limiting | Vitest + Sinon | 80%+ changed code | 120–150 |
| **Integration** | API endpoints, queue ops, DB preference lookup, channel handlers, DLQ logic | Supertest + testcontainers | All critical paths | 40–60 |
| **E2E** | End-to-end delivery (test Sendgrid/Twilio/Firebase accounts), opt-out enforcement | Playwright / bash + logs | Top 5 flows | 8–12 |
| **Contract** | Sendgrid/Twilio/Firebase API compatibility, internal service contract | Pact / OpenAPI validation | All public endpoints | 20–30 |
| **Performance** | Latency p50/p95/p99, throughput, queue drain rate, 50K→500K sustained load | k6 / Artillery | p99 < 200ms API, 1K+ msgs/s queue | 5–8 scenarios |
| **Security** | Input validation (XSS, injection), auth to internal APIs, rate limiting, audit logging | SAST + manual review | Public-facing endpoints | 15–20 |

**Pyramid allocation:** 55% unit / 25% integration / 10% E2E / 5% contract + 5% performance/security. This shifts unit→integration because external API mocking is fragile; real queue/DB in integration tests catches more bugs than unit mocks do.

---

### Quality Gates

**Pre-Merge (MUST pass):**
- [ ] 80%+ line coverage on changed code; 90%+ on `preferences/`, `delivery/`, `dedup/` modules
- [ ] All unit tests pass (exit 0)
- [ ] All integration tests pass (real Postgres + Redis in testcontainers)
- [ ] No new lint/type errors
- [ ] No OWASP issues found by SAST
- [ ] No `// TODO` or suppressed lint rules without justification

**Pre-Release (MUST pass):**
- [ ] E2E test suite passes on staging (against test Sendgrid/Twilio/Firebase accounts)
- [ ] Load test: sustained 50K/day for 30 min, p99 latency < 200ms
- [ ] Spike test: 500K/day for 5 min, queue recovery within 2 min
- [ ] Zero duplicate deliveries in 50K synthetic test messages
- [ ] Zero notifications sent to opted-out users in 50K synthetic test messages
- [ ] Zero lost notifications (all queued messages delivered or DLQ'd)
- [ ] Preference cache invalidation working (opt-out takes effect < 2 min)
- [ ] Audit trail complete: all deliveries logged with user ID, timestamp, channel, status, retry count
- [ ] Security review passed (auth, rate limiting, input validation)

---

### Test Gaps (Currently Untested — Flag for Implementation)

1. **Graceful degradation** — one channel down (Sendgrid offline), others still deliver
2. **Circuit breaker** — after N consecutive Twilio failures, pause SMS for 5 min, alert
3. **Deduplication under load** — 1000 duplicate requests/sec → single delivery
4. **Preference cache invalidation** — user opts out → next request respects it (not > 2 min stale)
5. **Queue persistence across restarts** — service crashes, restarts, all queued messages delivered
6. **Cascading timeout** — if Sendgrid takes > 30s, does API request hang or timeout properly?
7. **Invalid external API responses** — Sendgrid returns malformed JSON → handled gracefully
8. **Rate limit backoff** — Twilio returns 429 → exponential backoff, not hammering API
9. **Concurrent requests to same user** — dedup logic holds under 100+ concurrent requests
10. **Dead letter queue growth** — unbounded DLQ doesn't exhaust disk (implement retention/archival)

---

### Recommendations (Prioritized)

**P0 — Before first commit:**
1. Add contract tests for Sendgrid/Twilio/Firebase (catches API changes early)
2. Implement deduplication tests under load (concurrency is your biggest risk at 500K/day)
3. Add opt-out enforcement test: user opts out, next 10 requests respect it (cache freshness)
4. Performance baseline: establish p99 target (< 200ms) before optimization is hard

**P1 — Before staging:**
1. Add graceful degradation test (one channel down, others proceed)
2. Queue persistence test (restart the service, verify no message loss)
3. Preference cache invalidation test (opt-out takes effect within 2 min)
4. Rate limiting test (detect Twilio 429, backoff correctly)

**P2 — Ongoing:**
1. Mutation testing on `preferences/` and `dedup/` modules (identify weak tests)
2. Chaos engineering: random latency/errors from external APIs, measure recovery
3. Monthly load test scaling toward 500K/day target

---

## Next Step

Once you approve this strategy, we can:
1. **Define acceptance criteria** for a spike (queue + dedup + API endpoint)
2. **Generate specific tests** from this strategy using `/qa-engineer:generate-tests`
3. **Bootstrap the test structure** (folder layout, fixtures, test helpers)

Does this align with your risk tolerance? Any failure modes I've missed or test levels you'd prioritize differently?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/18.0 (89%) |
| Evaluated | 2026-04-30 |
| Target duration | 40923 ms |
| Target cost | $0.0679 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent operates as the definition of WHAT to test — does not write implementation test code (that is the QA Engineer's job) | PASS | The entire output defines strategy, risk levels, quality gates, and gaps. No actual test code, test method names, or implementation specifics appear anywhere. |
| c2 | Agent assesses the risk profile before defining test levels — identifies financial/reputational risk (sending duplicate notifications, ignoring opt-outs) | PASS | Risk Assessment section leads the output. It explicitly lists 'Duplicate delivery (HIGH - reputation, user frustration)', 'Notification sent to opted-out user (HIGH - compliance violation)', and 'Unbounded API calls to Twilio/Sendgrid (HIGH - financial)'. |
| c3 | Agent defines test levels covering unit, integration (internal API contract, external API boundaries), and E2E | PASS | Test Levels table has distinct rows for Unit, Integration (API endpoints, queue ops, DB preference lookup, channel handlers), E2E (end-to-end delivery via test accounts), and Contract (Sendgrid/Twilio/Firebase API compatibility, internal service contract via Pact/OpenAPI). |
| c4 | Agent applies the 3 amigos framing — identifies questions the product owner and architect must answer before development starts | FAIL | No 3 amigos framing appears anywhere in the output. There are no explicit questions directed at the product owner (e.g., 'what does delivery confirmation mean?', 'what is the SLA on opt-out?') or at the architect (e.g., 'which queue technology?', 'retry strategy?'). The 'Next Step' section invites approval but does not surface blocking questions. |
| c5 | Agent identifies edge cases in the edge case checklist: concurrency (duplicate send race condition), opt-out timing, channel fallback when one provider is down | PASS | Test Gaps section names: 'Deduplication under load — 1000 duplicate requests/sec → single delivery' (concurrency), 'Preference cache invalidation — user opts out → next request respects it (not > 2 min stale)' (opt-out timing), and 'Graceful degradation — one channel down (Sendgrid offline), others still deliver' (channel fallback). |
| c6 | Agent sets specific, measurable quality gates for pre-merge and pre-release | PASS | Quality Gates section has two distinct checklists: Pre-Merge (80%+ line coverage, 90%+ on critical modules, all unit/integration tests pass, no OWASP issues) and Pre-Release (sustained 50K/day load test, p99 < 200ms, zero duplicates in 50K synthetic messages, opt-out audit, preference cache invalidation < 2 min). |
| c7 | Agent flags testability concerns — e.g. external providers must be fakeable in integration tests, not called live | PASS | Contract test row uses 'Pact / OpenAPI validation' for Sendgrid/Twilio/Firebase compatibility. E2E specifies 'test Sendgrid/Twilio/Firebase accounts' (not production). The pyramid rationale states 'external API mocking is fragile' driving toward contract tests rather than live calls in CI. Pattern is present even if not labeled 'testability requirement.' |
| c8 | Agent assigns test levels to specific criteria with rationale (unit vs integration vs E2E reasoning) | PARTIAL | The pyramid allocation line gives a rationale: '55% unit / 25% integration / 10% E2E... This shifts unit→integration because external API mocking is fragile; real queue/DB in integration tests catches more bugs than unit mocks do.' However, the rationale is brief and not mapped criterion-by-criterion to specific risks or test cases. |
| c9 | Output includes Risk Assessment, Test Levels table, Quality Gates, and at minimum one identified gap | PASS | All four sections are present: 'Risk Assessment', 'Test Levels' table, 'Quality Gates' (Pre-Merge and Pre-Release), and 'Test Gaps (Currently Untested)' with 10 enumerated gaps. |
| c10 | Output's risk assessment names duplicate-send (financial/reputational), opt-out violations (legal/regulatory — TCPA / GDPR / spam laws), and provider outage as the top risks for a notifications service — not generic 'data quality' | PASS | Risk Assessment names: 'Duplicate delivery (HIGH - reputation, user frustration)', 'Notification sent to opted-out user (HIGH - compliance violation)', and 'Third-party outage blocks all delivery (MEDIUM - resilience)'. Specific, not generic. Specific regulation names (TCPA/GDPR) absent but compliance framing is clear. |
| c11 | Output's test levels table covers unit (logic, preference resolution), integration (internal REST API contract + external Sendgrid/Twilio/Firebase boundaries), and E2E (full request → queue → delivery → callback), with tools/coverage targets per level | PASS | Unit row: 'Preference resolution, deduplication, retry logic, validation, rate limiting / Vitest + Sinon / 80%+ changed code'. Integration row: 'API endpoints, queue ops, DB preference lookup, channel handlers, DLQ logic / Supertest + testcontainers / All critical paths'. E2E row: 'End-to-end delivery (test accounts), opt-out enforcement / Playwright / Top 5 flows'. |
| c12 | Output identifies the integration test pattern — fakes/contract tests at the Sendgrid/Twilio/Firebase boundaries, never live calls in CI — and names this as a testability requirement | PASS | Contract test row explicitly covers 'Sendgrid/Twilio/Firebase API compatibility' using Pact/OpenAPI validation. E2E uses 'test Sendgrid/Twilio/Firebase accounts' (test tier, not prod). P0 recommendation: 'Add contract tests for Sendgrid/Twilio/Firebase (catches API changes early)'. The pattern is identified and named as a P0 priority. |
| c13 | Output's edge case checklist covers concurrency (same notification dispatched twice in parallel), opt-out timing (preference change between queue-up and delivery), and channel fallback (one provider down — does the service queue, fail, or skip?) | PASS | Test Gaps section: 'Deduplication under load — 1000 duplicate requests/sec → single delivery' and 'Concurrent requests to same user — dedup logic holds under 100+ concurrent requests' (concurrency); 'Preference cache invalidation — user opts out → next request respects it (not > 2 min stale)' (opt-out timing); 'Graceful degradation — one channel down (Sendgrid offline), others still deliver' (channel fallback). |
| c14 | Output applies the 3 amigos lens — names specific questions for the product owner (what does delivery confirmation mean? what's the SLA on opt-out?) and architect (queue technology, retry strategy) | FAIL | No 3 amigos lens is applied. The output contains no questions directed to the product owner about confirmation semantics or opt-out SLAs, and no questions directed to the architect about queue technology choices or retry strategy. The closing 'Does this align with your risk tolerance?' is a general approval prompt, not structured 3-amigos questioning. |
| c15 | Output sets specific quality gates pre-merge (coverage threshold, contract tests pass, lint/type clean) and pre-release (load test at 50K/day, opt-out audit query returns zero violations, provider failure simulation) | PASS | Pre-Merge gates: '80%+ line coverage', 'No new lint/type errors', 'No OWASP issues found by SAST'. Pre-Release gates: 'Load test: sustained 50K/day for 30 min, p99 < 200ms', 'Zero notifications sent to opted-out users in 50K synthetic test messages'. Provider failure simulation is in P2 recommendations (chaos engineering) but not a named pre-release gate. |
| c16 | Output addresses scaling from 50K to 500K notifications/day in the test strategy — load tests must validate the 10x growth path, not just the launch volume | PASS | Pre-Release gate: 'Spike test: 500K/day for 5 min, queue recovery within 2 min'. P2 recommendation: 'Monthly load test scaling toward 500K/day target'. Both launch volume and 10x growth path are explicitly covered. |
| c17 | Output stays at strategy level — does NOT include implementation test code or specific test method names, leaving that to the QA Engineer | PASS | The entire output is composed of risk tables, quality gate checklists, tool names, and scenario descriptions. There are no code blocks, no test function signatures, no `describe`/`it` blocks or equivalent — consistent with a QA lead strategy document rather than implementation. |
| c18 | Output identifies at least one specific gap — e.g. no fake Twilio/Sendgrid available yet, no preference-change-during-flight test scenario in scope, or no contract tests with the calling internal services | PASS | 'Test Gaps (Currently Untested — Flag for Implementation)' section lists 10 specific gaps including 'Graceful degradation', 'Deduplication under load', 'Preference cache invalidation', 'Queue persistence across restarts', 'Rate limit backoff', and others. |
| c19 | Output addresses observability requirements as a testability concern — tests need to assert delivery state, not just request acceptance, which requires hooks into the queue and provider callbacks | PARTIAL | Pre-Release gate: 'Audit trail complete: all deliveries logged with user ID, timestamp, channel, status, retry count'. Quality gate: 'Zero lost notifications (all queued messages delivered or DLQ'd)'. These imply delivery-state assertion rather than request-acceptance. However, the output does not explicitly frame this as a testability concern requiring queue/callback hooks as an architectural prerequisite. |

### Notes

The output is a strong, well-structured test strategy that covers risk assessment, test levels, quality gates, and gaps comprehensively. The two meaningful failures are both on the 3 amigos framing (c4/c14): the output never surfaces specific blocking questions for the product owner (delivery confirmation semantics, opt-out SLA) or architect (queue technology, retry contract). These are distinct criteria but the same underlying gap. Provider failure simulation appears in P2 recommendations but not in the pre-release quality gates, which is a minor omission against c15 but not enough to drop the score. The observability concern (c19) is partially addressed through audit trail requirements but not named as an architectural testability prerequisite. Overall the strategy is practical, specific, and correctly calibrated for a high-risk notification service.
