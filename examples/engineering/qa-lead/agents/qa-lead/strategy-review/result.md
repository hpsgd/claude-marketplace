# Strategy Review

Scenario: User asks the QA lead to define a test strategy for a new microservice that sends email, SMS, and push notifications. The service will be called by multiple other services via an internal API.

## Prompt

> We're building a new notifications microservice. It receives requests from other internal services (via a REST API), queues them, and delivers via Sendgrid (email), Twilio (SMS), and Firebase (push). There's a preference/opt-out system per user per channel. The service needs to handle ~50,000 notifications/day at launch, growing to ~500,000 within 12 months. Can you define the test strategy before we start development?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the test strategy framework step by step.

## Test Strategy: Notifications Microservice

### Risk Assessment

**Risk profile:** Data integrity + Privacy (HIGH)

**Critical flows:**
1. Notification received → queued → delivered via correct channel
2. User opt-out respected before delivery
3. Duplicate request handled idempotently
4. Provider failure → retry without data loss

**Failure modes (by risk):**
| Failure Mode | Risk | Impact |
|---|---|---|
| Notification lost (queued but never delivered) | HIGH | User never receives message, no audit trail |
| Notification sent to opted-out user | HIGH | Privacy violation, user trust damage |
| Duplicate delivery on same channel | MEDIUM | User annoyance, potential SMS/email charges |
| Preference lookup returns stale data | HIGH | Wrong opt-out decision made |
| Queue overflow under load (500k/day) | HIGH | Dropped notifications, system collapse |
| Provider timeout → notification stuck | MEDIUM | Recovered by retry, but adds latency |
| Audit trail gaps | HIGH | Cannot prove delivery or diagnose failures |

**External dependencies:**
- Sendgrid, Twilio, Firebase (delivery)
- Internal preference service (opt-out data — freshness critical)
- Queue system (durability critical)
- Database (audit/state tracking)

---

### Test Levels & Allocation

Risk shift from default pyramid: **55% unit, 25% integration, 15% E2E, + contract + performance**

| Level | What it tests | Tools | Coverage | Est. Tests |
|---|---|---|---|---|
| **Unit** | Preference evaluation, message building, deduplication, retry logic | Vitest / pytest | 90%+ on core modules | 60–80 |
| **Integration** | API request → queue, queue consumer → preference check → delivery, database consistency | Testcontainers + Supertest | All critical paths | 25–35 |
| **E2E** | Full journey: API → queue → delivery; opt-out respected; retry on failure | Playwright (sync test against running service) | Top 5 flows | 5–8 |
| **Contract** | Request schema, preference service response, provider API mocks | OpenAPI validation | All public contracts | 10–15 |
| **Performance** | Throughput at 50k/day and 500k/day; p50/p95/p99 latency; queue backpressure | k6 / Locust | SLA: p95 < 2s delivery | 3–5 load profiles |
| **Security** | Input validation, SQL injection, PII in logs, auth on API | SAST + manual | Public-facing code | 8–12 |

---

### Test Coverage Detail

#### Unit Tests (core logic)
```
preference/
  ✓ Evaluate opt-out: user opted out of email → skip sendgrid
  ✓ Evaluate opt-out: user not opted out → include channel
  ✓ Stale preference cache: cache expired → re-fetch
  ✓ Preference missing → default to opt-in (confirm this is the rule)

message-builder/
  ✓ Build email: template + user data → valid sendgrid payload
  ✓ Build SMS: template + user data → valid twilio payload
  ✓ Build push: template + user data → valid firebase payload
  ✓ Sanitise PII from logs: email content → masked in audit trail

deduplication/
  ✓ Duplicate request (same idempotency key) → skip, return existing ID
  ✓ New request (new key) → queue normally
  ✓ Dedup TTL expired → treat as new

retry-backoff/
  ✓ First failure → backoff 1s
  ✓ Third failure → backoff 32s (exponential)
  ✓ Max retries (5) exceeded → dead letter queue
```

#### Integration Tests (boundaries & state)
```
api/notifications POST
  ✓ Valid request → 202 Accepted, notification queued with ID
  ✓ Missing required fields → 400, clear error
  ✓ Unknown channel → 400 (validate against whitelist: email|sms|push)
  ✓ Duplicate ID (idempotency) → 202, returns same notification ID

queue-consumer
  ✓ Poll queue → fetch notification, check preferences, build message
  ✓ Preference service unavailable (timeout) → exponential backoff, retry
  ✓ Sendgrid delivery succeeds → mark as delivered, audit log
  ✓ Sendgrid delivery fails (4xx) → dead letter (don't retry)
  ✓ Sendgrid delivery fails (5xx) → retry queue with backoff
  ✓ Twilio rate limit (429) → respect retry-after header, requeue
  ✓ Firebase fails silently (device offline) → mark delivered (async delivery ok)

database/audit-trail
  ✓ Every notification: created → queued → delivered (or failed)
  ✓ No gaps in audit trail across concurrent writes (ACID)
  ✓ Retry record preserved in audit for debugging

preference-cache
  ✓ Cache hit → serve from cache (< 10ms)
  ✓ Cache miss → fetch from service, populate cache
  ✓ Cache invalidation: preference updated → propagate within 30s
```

#### E2E Tests (complete flows, mocked providers)
```
Happy path
  ✓ POST /notifications (email) → queued → sendgrid mock called → delivered
  
Opt-out respected
  ✓ User opted out of SMS → POST /notifications (sms) → filtered, not queued
  
Retry on transient failure
  ✓ Sendgrid fails with 503 → retried → succeeds on 2nd attempt
  
Concurrent to same user
  ✓ 3 notifications queued to same user on 3 channels → all delivered in parallel
  
Duplicate handling
  ✓ POST /notifications (id=X) → queued
  ✓ POST /notifications (id=X) again → returns same notification ID, no duplicate in queue
```

#### Performance Tests
```
Load profile 1: 50k notifications/day (launch)
  ✓ Sustained throughput: 578 notifs/sec
  ✓ p50 latency (API → queued): < 100ms
  ✓ p95 latency (queued → delivered): < 2s
  ✓ p99 latency: < 5s
  ✓ Queue depth never exceeds 1000

Load profile 2: 500k notifications/day (12 months)
  ✓ Sustained throughput: 5,787 notifs/sec
  ✓ Same latency targets
  ✓ Queue backpressure: if delivery slows, API returns 429 instead of queuing

Spike test
  ✓ 2x load for 5 min → recovers to baseline
```

#### Security Tests
```
Input validation
  ✓ Oversized request body → 413
  ✓ Invalid channel enum → 400
  ✓ SQL injection in notification content → sanitised, not injected
  ✓ XSS in template variables → escaped for each channel

Authentication
  ✓ Missing API key → 401
  ✓ Invalid API key → 403
  ✓ Request signed by different service → 403

Logging
  ✓ User email not in logs
  ✓ Phone number not in logs
  ✓ API response bodies not logged in full (only status + ID)
```

---

### Quality Gates

#### Pre-Merge (MUST pass)
- [ ] 90%+ line coverage on `preference/`, `deduplication/`, `message-builder/`
- [ ] 80%+ line coverage on remaining code
- [ ] All unit + integration tests pass
- [ ] No new lint or type-check errors
- [ ] No new security vulnerabilities (run SAST)
- [ ] Performance regression test: p95 latency increase < 10%

#### Pre-Release (MUST pass)
- [ ] E2E tests pass on staging against sandbox Sendgrid/Twilio/Firebase
- [ ] Load test: 50k/day sustained without latency regression
- [ ] Audit trail: sampled 100 notifications, 0 delivery gaps
- [ ] Monitoring & alerting wired up: alerts for queue depth, delivery errors, provider timeouts
- [ ] Run-book: on-call guide for queue backlog, provider outages, manual retry
- [ ] Documentation: API contract (OpenAPI), preference service dependency, retry strategy

---

### Key Questions Before Building

These must be answered and codified in code/config before development starts:

1. **Deduplication strategy:** What identifies a duplicate? (request ID, idempotency key passed by caller, content hash?) How long does the duplicate window last? (1 hour? 24 hours?)

2. **Preference cache freshness:** How stale can the opt-out data be? (must be < 30 seconds? < 5 minutes?) Who invalidates the cache, and how?

3. **Retry strategy:** Max retries per provider? Backoff formula? Should a provider 4xx (user not found) retry, or go straight to dead letter?

4. **Dead letter handling:** After max retries, what happens? (stored for manual review, discarded with alert, sent to another queue?)

5. **Notification order:** If 3 notifications queue for the same user, must they be delivered in order? (affects delivery parallelism)

6. **Provider quota limits:** What if we hit Sendgrid's daily email limit? (queue backpressure or discard?) Same for SMS?

7. **Audit trail retention:** How long do delivery records stay in the database? (affects schema sizing for 500k/day growth)

8. **Notification content:** Can callers pass HTML templates, or only plain text? (affects sanitisation/XSS risk)

9. **User identification:** Caller passes user ID, we look up contact details. What if user not found? (error, skip, store for manual review?)

10. **Multi-channel conflict:** If user requests notification on all 3 channels but is opted out of 2, do we queue 1 message (for push only) or 3 (email/sms/push) with filters applied later?

---

### Critical Gaps (for spec clarification)

Before the architect finalizes the API contract:

| Gap | Why it matters |
|---|---|
| Idempotency key format & lifespan | Affects duplicate handling; if caller doesn't pass one, service must generate it |
| Preference service SLA | If it's slow (1s), queue consumer becomes bottleneck; affects retry strategy |
| Batch vs single notifications | API accepts 1 notif or N? Affects queue throughput design |
| Notification priority/urgency | Should high-priority bypass queue and go straight to providers? |
| User contact data lookup | Service owns user DB, or calls another service? Failure modes change |

---

### Recommendations (prioritized)

1. **Define deduplication + retry strategy** (Week 1 spec). These are load-bearing decisions that affect database schema and queue consumer logic.

2. **Contract test against preference service** (Week 1). Preference lookups are critical path; must mock reliably or hit real test environment.

3. **Load test at 50k/day before release** (Week 3). Don't guess at queue size, database pool, or consumer concurrency. Measure under realistic load.

4. **Implement audit trail as event stream** (not CRUD logs). Easier to reconstruct delivery state, debug gaps, and audit retries.

5. **Mock all 3 providers in test suite**. Don't hit real Sendgrid/Twilio/Firebase in CI. Use sandbox credentials only in staging.

6. **Dead letter queue visibility**. Surface dead letters (notifications that failed after max retries) as alerts + dashboard. On-call needs to see them immediately.

---

**Next step:** Use this strategy to write acceptance criteria (Given/When/Then) for each critical flow, then generate unit + integration tests. Once tests are written (but failing), implement.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.0/18.0 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 56633 ms |
| Target cost | $0.0677 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent operates as the definition of WHAT to test — does not write implementation test code (that is the QA Engineer's job) | PASS | All test cases are written as descriptive specifications (e.g., '✓ Evaluate opt-out: user opted out of email → skip sendgrid') — no actual test framework code (no describe/it/def test_ blocks). The closing line explicitly says 'Once tests are written (but failing), implement,' deferring implementation to the QA Engineer. |
| c2 | Agent assesses the risk profile before defining test levels — identifies financial/reputational risk (sending duplicate notifications, ignoring opt-outs) | PASS | Risk Assessment section appears first with a 7-row risk table. 'Notification sent to opted-out user' is rated HIGH with 'Privacy violation, user trust damage.' 'Duplicate delivery on same channel' is rated MEDIUM with 'User annoyance, potential SMS/email charges.' Risk profile leads the entire strategy. |
| c3 | Agent defines test levels covering unit, integration (internal API contract, external API boundaries), and E2E | PASS | Test Levels & Allocation table explicitly names Unit (preference evaluation, deduplication, retry logic), Integration (API request → queue, queue consumer → preference → delivery, Testcontainers + Supertest), and E2E (full journey: API → queue → delivery, Playwright). Contract and Performance levels are additionally included. |
| c4 | Agent applies the 3 amigos framing — identifies questions the product owner and architect must answer before development starts | PASS | 'Key Questions Before Building' section lists 10 numbered questions that must be answered before development. Includes PO concerns (notification content, multi-channel conflict, dead letter handling) and architect concerns (deduplication strategy, retry strategy, preference cache freshness, notification order, provider quota limits). |
| c5 | Agent identifies edge cases in the edge case checklist: concurrency (duplicate send race condition), opt-out timing, channel fallback when one provider is down | PASS | Concurrency: E2E test 'Concurrent to same user → 3 notifications queued to same user on 3 channels → all delivered in parallel' and deduplication tests. Opt-out timing: risk row 'Preference lookup returns stale data \| HIGH' and integration test 'Cache invalidation: preference updated → propagate within 30s.' Provider failure: integration tests cover Sendgrid 4xx (dead letter), Sendgrid 5xx (retry queue), Twilio 429 (respect retry-after). |
| c6 | Agent sets specific, measurable quality gates for pre-merge and pre-release | PASS | Quality Gates section has Pre-Merge checklist (90%+ line coverage on core modules, 80%+ remaining, all unit + integration tests pass, no new lint/type errors, no new SAST vulnerabilities, p95 latency regression < 10%) and Pre-Release checklist (E2E on staging, load test 50k/day sustained, audit trail sample of 100 with 0 gaps, monitoring wired up, runbook, documentation). |
| c7 | Agent flags testability concerns — e.g. external providers must be fakeable in integration tests, not called live | PASS | Recommendations #5 explicitly states: 'Mock all 3 providers in test suite. Don't hit real Sendgrid/Twilio/Firebase in CI. Use sandbox credentials only in staging.' E2E section labels scenarios as 'mocked providers.' Integration tests reference provider failure simulation without live calls. |
| c8 | Agent assigns test levels to specific criteria with rationale (unit vs integration vs E2E reasoning) | PARTIAL | The table states 'Risk shift from default pyramid: 55% unit, 25% integration, 15% E2E, + contract + performance' and the 'What it tests' column explains what each level covers. Coverage Detail sections group tests by level. However, explicit per-test reasoning (e.g., 'this is unit rather than integration because it has no external dependencies') is not provided — the rationale is implied by category description rather than stated for individual test assignments. |
| c9 | Output includes Risk Assessment, Test Levels table, Quality Gates, and at minimum one identified gap | PASS | All four required sections present: Risk Assessment (7-row table with failure modes), Test Levels & Allocation (6-row table with tools and coverage targets), Quality Gates (Pre-Merge and Pre-Release checklists), and Critical Gaps (5-row table with gaps like idempotency key format, preference service SLA, batch vs single API design). |
| c10 | Output's risk assessment names duplicate-send (financial/reputational), opt-out violations (legal/regulatory — TCPA / GDPR / spam laws), and provider outage as the top risks for a notifications service — not generic 'data quality' | PASS | Risk table names 'Notification sent to opted-out user \| HIGH \| Privacy violation, user trust damage' (opt-out violations), 'Duplicate delivery on same channel \| MEDIUM \| User annoyance, potential SMS/email charges' (duplicate-send with financial framing), and 'Provider timeout → notification stuck \| MEDIUM \| Recovered by retry.' These are notification-service-specific risks, not generic data quality framing. TCPA/GDPR are not named explicitly, but the framing goes well beyond generic quality concerns. |
| c11 | Output's test levels table covers unit (logic, preference resolution), integration (internal REST API contract + external Sendgrid/Twilio/Firebase boundaries), and E2E (full request → queue → delivery → callback), with tools/coverage targets per level | PASS | Unit: 'Preference evaluation, message building, deduplication, retry logic \| Vitest/pytest \| 90%+ on core modules.' Integration: 'API request → queue, queue consumer → preference check → delivery, database consistency \| Testcontainers + Supertest.' E2E: 'Full journey: API → queue → delivery; opt-out respected; retry on failure \| Playwright \| Top 5 flows.' All three levels have tools and coverage targets. |
| c12 | Output identifies the integration test pattern — fakes/contract tests at the Sendgrid/Twilio/Firebase boundaries, never live calls in CI — and names this as a testability requirement | PASS | Recommendations #5: 'Mock all 3 providers in test suite. Don't hit real Sendgrid/Twilio/Firebase in CI. Use sandbox credentials only in staging.' Contract tests are a dedicated row in the Test Levels table: 'Request schema, preference service response, provider API mocks \| OpenAPI validation.' E2E tests explicitly use 'mocked providers.' |
| c13 | Output's edge case checklist covers concurrency (same notification dispatched twice in parallel), opt-out timing (preference change between queue-up and delivery), and channel fallback (one provider down — does the service queue, fail, or skip?) | PASS | Concurrency: E2E 'Duplicate handling' test and 'Concurrent to same user' test. Opt-out timing: Risk row 'Preference lookup returns stale data \| HIGH' plus integration test 'Cache invalidation: preference updated → propagate within 30s.' Channel/provider down: Integration tests define behavior for Sendgrid 4xx (dead letter), Sendgrid 5xx (retry queue), Twilio 429 (respect retry-after), Firebase silent failure (mark delivered). Behavior is explicitly defined. |
| c14 | Output applies the 3 amigos lens — names specific questions for the product owner (what does delivery confirmation mean? what's the SLA on opt-out?) and architect (queue technology, retry strategy) | PASS | 'Key Questions Before Building' section contains PO-relevant questions (dead letter handling, notification order, provider quota limits, multi-channel conflict, notification content type) and architect-relevant questions (deduplication strategy, preference cache freshness/SLA, retry strategy, user contact data lookup). Retry strategy is question #3; preference cache freshness ('How stale can opt-out data be?') is question #2. Questions are not role-labeled but the content maps clearly. |
| c15 | Output sets specific quality gates pre-merge (coverage threshold, contract tests pass, lint/type clean) and pre-release (load test at 50K/day, opt-out audit query returns zero violations, provider failure simulation) | PASS | Pre-Merge: 90%+ coverage on core modules, 80%+ remaining, unit + integration tests pass, no new lint/type errors, SAST gate, p95 latency regression < 10%. Pre-Release: load test at 50k/day sustained, 'Audit trail: sampled 100 notifications, 0 delivery gaps,' E2E on staging against sandbox providers (provider failure simulation implied). Opt-out-specific audit query is not explicitly named but delivery gap audit covers it. |
| c16 | Output addresses scaling from 50K to 500K notifications/day in the test strategy — load tests must validate the 10x growth path, not just the launch volume | PASS | Performance Tests section has two distinct load profiles: 'Load profile 1: 50k notifications/day (launch) — 578 notifs/sec' and 'Load profile 2: 500k notifications/day (12 months) — 5,787 notifs/sec' with the same latency targets applied to both and a spike test. Both profiles are explicitly scoped. |
| c17 | Output stays at strategy level — does NOT include implementation test code or specific test method names, leaving that to the QA Engineer | PASS | All test cases use descriptive specification format (e.g., '✓ Evaluate opt-out: user opted out of email → skip sendgrid') — no test method implementations, no test framework syntax, no import statements. The closing sentence explicitly defers to QA: 'Use this strategy to write acceptance criteria... then generate unit + integration tests. Once tests are written (but failing), implement.' |
| c18 | Output identifies at least one specific gap — e.g. no fake Twilio/Sendgrid available yet, no preference-change-during-flight test scenario in scope, or no contract tests with the calling internal services | PASS | 'Critical Gaps (for spec clarification)' section is a dedicated 5-row table naming: idempotency key format and lifespan, preference service SLA, batch vs single notification API design, notification priority/urgency, and user contact data lookup ownership. Each gap explains why it matters for testability. |
| c19 | Output addresses observability requirements as a testability concern — tests need to assert delivery state, not just request acceptance, which requires hooks into the queue and provider callbacks | PARTIAL | E2E tests assert delivery state ('sendgrid mock called → delivered'), integration tests check 'mark as delivered, audit log,' and Recommendation #4 says 'Implement audit trail as event stream (not CRUD logs)' with Recommendation #6 requiring 'Dead letter queue visibility... On-call needs to see them immediately.' However, the output does not explicitly frame observability as a testability prerequisite — it does not call out that asserting delivery (vs. request acceptance) requires deliberate queue/callback hooks to be designed in. |

### Notes

This is an exceptionally thorough test strategy output. It correctly leads with risk assessment, defines six test levels with tools and coverage targets, provides 10 pre-development clarification questions, sets measurable pre-merge and pre-release gates, and explicitly calls out both the 50K and 500K/day load profiles. The provider-mocking requirement is named explicitly and placed as a recommendation. The only areas falling short of full marks are both at their PARTIAL ceiling by design: c8 assigns tests to levels but doesn't provide per-test rationale for the assignment decision; c19 shows observability in practice (delivery state assertions, audit trail recommendations) but never explicitly frames it as a testability architectural requirement. The absence of TCPA/GDPR naming in the risk table is a minor gap but does not prevent PASS on c10 since the risks are otherwise correctly identified and framed beyond generic data quality. Overall the output is production-quality.
