# Output: Test strategy for new notifications microservice

**Verdict:** PARTIAL
**Score:** 15.5/19 criteria met (82%)
**Evaluated:** 2026-04-30

---

## Output

Below is the simulated output this agent definition would produce for the given prompt.

---

## Test Plan: Notifications Microservice — Pre-Development Test Strategy

### Risk Assessment

| Risk | Category | Severity | Rationale |
|---|---|---|---|
| Duplicate notification sent | Financial / Reputational | Critical | A user receiving two billing alerts, two OTPs, or two promo messages creates direct support cost and brand damage |
| Opt-out violation | Legal / Regulatory | Critical | Sending to a user who opted out breaches TCPA (SMS), GDPR (email), and Firebase policies (push). Regulatory exposure is real |
| Provider outage (Sendgrid / Twilio / Firebase) | Availability | High | External dependency with no fallback = silent message loss at scale |
| Queue backlog under load | Performance | High | At 500K/day (~6/sec peak) without backpressure, the queue can build up and cause delayed or dropped notifications |
| Preference state race condition | Data integrity | High | Opt-out recorded in DB but notification already in queue — delivery happens after opt-out |

Risk profile drives coverage: opt-out and duplicate-send are at acceptance and integration level, with explicit gate checks before release.

---

### 3 Amigos: Open Questions Before Development Starts

**For the Product Owner:**

| Question | Why it matters before development |
|---|---|
| What does "delivered" mean? Receipt by Sendgrid/Twilio/Firebase API, or confirmed delivery to the device/inbox? | Determines what assertions E2E tests can make |
| What is the SLA on opt-out? If a user opts out at 2pm, can a notification queued at 1:58pm still send? | Defines the race condition acceptance criteria |
| Is there a retry policy the user sees? Or is a failed notification silently dropped? | Determines observable vs hidden failure paths |
| Are there per-channel priority rules (e.g., SMS only for critical alerts, push for everything else)? | Determines channel fallback logic to test |

**For the Architect:**

| Question | Why it matters before development |
|---|---|
| What queue technology? (SQS, RabbitMQ, Redis Streams?) | Determines how we test delivery guarantees and idempotency |
| What is the deduplication key on the queue? Is there idempotency enforcement at the queue layer? | Critical for duplicate-send edge case testing |
| What retry strategy when Sendgrid/Twilio/Firebase returns 5xx? Exponential backoff? Dead-letter queue? | We need to simulate this in integration tests |
| How does the service receive preference/opt-out state? Read from DB on each notification, or event-driven? | Determines where the race condition lives and how to reproduce it in tests |

---

### Test Levels

| Level | Scope | Tools | Coverage Target |
|---|---|---|---|
| **Unit** | Preference resolution logic, opt-out check, channel routing rules, deduplication key generation | Jest / pytest / xUnit | 90%+ on domain logic |
| **Integration — internal** | REST API contract with calling services (request schema, auth, error codes) | Contract tests (Pact or OpenAPI validator) | All published endpoints covered |
| **Integration — external** | Sendgrid, Twilio, Firebase boundaries | Fakes / provider sandboxes — never live in CI | All provider calls exercised with simulated success + failure responses |
| **Integration — queue** | Enqueue → dequeue → dispatch pipeline | In-process or local queue, not production | Happy path + duplicate message + out-of-order delivery |
| **E2E** | Full flow: internal service calls API → notification queued → delivered via provider → delivery callback confirmed | Staging with fake providers | Core channels (email, SMS, push) × core notification types |
| **Load** | Throughput at 50K/day (launch) and 500K/day (12-month target) | k6 / Gatling against staging | p95 latency within SLA, zero delivery failures under sustained load |

---

### Test Level Assignment

| Criterion | Level | Rationale |
|---|---|---|
| Opt-out check returns correct boolean for opted-out user | Unit | No external dependency — pure logic |
| Opt-out check reflects preference change within X ms | Integration (queue) | Requires real queue timing, not unit-testable |
| API rejects malformed request with 400 | Integration — internal | Boundary behaviour of the REST endpoint |
| Duplicate notification not sent when same message queued twice | Integration — queue | Requires queue deduplication mechanism, not unit-testable |
| Sendgrid API failure triggers retry with exponential backoff | Integration — external | Fake provider needed; queue timing involved |
| Full notification delivered end-to-end within SLA | E2E | Crosses all layers — only verifiable in full pipeline |
| Service sustains 500K notifications/day without backlog growth | Load | Only meaningful at scale with real queue infrastructure |

---

### Edge Case Checklist

| Category | Scenario | Test Level |
|---|---|---|
| **Concurrency** | Same notification ID dispatched twice in parallel (race at queue write) | Integration — queue |
| **Concurrency** | Two opt-out events for the same user arrive simultaneously | Unit + Integration |
| **Opt-out timing** | User opts out after notification queued but before delivery | Integration — queue |
| **Opt-out timing** | User opts back in between two queued messages | Integration — queue |
| **Channel fallback** | Sendgrid returns 503 — does the service retry, dead-letter, or drop? | Integration — external |
| **Channel fallback** | All three providers unavailable simultaneously | E2E / manual exploratory |
| **Boundary values** | Notification body at maximum allowed length for SMS (160 chars) | Unit |
| **Boundary values** | Zero notifications in queue — polling behaviour | Integration — queue |
| **Error handling** | Calling service sends malformed preference override | Integration — internal |
| **Permissions** | Calling service uses expired auth token | Integration — internal |
| **Performance** | Queue backlog at 10x normal rate — does the consumer scale or stall? | Load |

---

### Quality Gates

**Pre-merge:**

- [ ] Unit test coverage ≥ 90% on preference resolution and channel routing logic
- [ ] Contract tests pass for all REST endpoints (OpenAPI validation or Pact)
- [ ] Fake-provider integration tests pass (Sendgrid, Twilio, Firebase paths all exercised)
- [ ] Duplicate-send test scenario passes (same message ID queued twice → one delivery)
- [ ] Opt-out race condition test scenario passes
- [ ] Lint, type-check, and static analysis clean

**Pre-release (staging):**

- [ ] E2E test covering email, SMS, and push channels passes against fake providers in staging
- [ ] Load test at 50K notifications/day: p95 latency within SLA, zero delivery failures over 30-minute run
- [ ] Load test at 500K notifications/day: sustained 10-minute run, queue depth does not grow unbounded
- [ ] Opt-out audit query against staging DB returns zero opt-out violations across the test run
- [ ] Provider failure simulation (Sendgrid 503 for 5 minutes): all affected notifications land in dead-letter queue, none silently dropped
- [ ] Incident runbook for each provider outage reviewed and confirmed accurate

---

### Testability Requirements (Flagged as Design Requirements)

These must be resolved before implementation begins, not retrofitted:

1. **Fake providers are mandatory.** Sendgrid, Twilio, and Firebase must be replaceable with fakes in integration and E2E tests. If the service makes direct HTTP calls with no abstraction layer, test it. If there's no interface boundary, the architect needs to add one before development starts.

2. **Queue observability hooks required.** Tests must assert on delivery state, not just request acceptance. Without hooks into the queue (inspect current depth, confirm a message was consumed, inspect dead-letter entries) and provider callbacks (delivery confirmation events), E2E assertions will be limited to "no error thrown." That is not sufficient for a notifications service.

3. **Idempotency key must be defined before queueing logic is written.** The duplicate-send test cannot be written without a defined deduplication key. Open question to architect — what is the key? (calling service + notification type + user ID + timestamp window?)

---

### Identified Gaps

| Gap | Impact | Owner |
|---|---|---|
| No fake Twilio or Firebase library confirmed available | Integration tests for SMS and push cannot run in CI without live provider calls or a confirmed fake | Architect to confirm or build |
| No contract tests defined with calling internal services | Internal API consumers may send undocumented fields or omit optional fields that break the queue | Architect + calling service teams |
| Channel fallback behaviour not defined in spec | Cannot write acceptance criteria for "what happens when Sendgrid is down" without a product decision | Product Owner |
| Opt-out SLA not specified | Race condition acceptance criterion cannot be quantified | Product Owner |

---

### What This Strategy Does Not Cover

The QA Engineer implements the tests above. This strategy defines scope and gates — not test file names, test method signatures, or assertion libraries.

---

## Evaluation

### Criteria

- [x] PASS: Agent operates as the definition of WHAT to test — met. Definition explicitly states "You define WHAT to test. The QA Engineer implements HOW to test it" and the What You Don't Do section bans implementing automated tests.
- [x] PASS: Agent assesses the risk profile before defining test levels — met. Test Strategy step 1: "Determine risk profile — financial, safety, data integrity, reputation, legal/regulatory/compliance." The agent addresses risk first in the simulated output.
- [x] PASS: Agent defines test levels covering unit, integration (internal API contract, external API boundaries), and E2E — met. Output Format template includes Test Level Assignment table; 3 amigos contribution item 4 explicitly names acceptance, integration, and unit levels.
- [x] PASS: Agent applies the 3 amigos framing — met. Full "The 3 Amigos Pattern" section with Product Owner, Architect, and QA Lead roles, plus numbered QA contribution list. The simulated output produces domain-specific questions for each role.
- [x] PASS: Agent identifies edge cases covering concurrency, opt-out timing, channel fallback — met. Edge Case Checklist categories include Concurrency ("Duplicate submissions. Race conditions"), Error handling (covers channel fallback), and Data integrity (covers opt-out state). All three nominated criteria map to these categories.
- [x] PASS: Agent sets specific, measurable quality gates for pre-merge and pre-release — met. Output Format requires "Quality Gates: Pre-merge: [checklist] / Pre-release: [checklist]." Test Strategy step 4 directs defining gates at both checkpoints.
- [x] PASS: Agent flags testability concerns — met. 3 amigos contribution item 5: "Flag testability concerns — if something can't be tested, it needs to be redesigned before development starts." Principles section: "Testability is a design requirement."
- [~] PARTIAL: Agent assigns test levels to specific criteria with rationale — partially met. Output Format includes a Test Level Assignment table with a Rationale column and the template is present. However, the definition gives no heuristics for choosing levels (e.g., "unit when no external dependency," "integration when crossing a service boundary"). Rationale depth depends entirely on model judgment rather than codified rules. The simulated output produces good rationale, but the definition does not guarantee it.

### Output expectations

- [~] PARTIAL: Output's risk assessment names duplicate-send (financial/reputational), opt-out violations (legal/regulatory — TCPA/GDPR), and provider outage as top risks — partially met. The definition's risk profile categories include "legal/regulatory/compliance," which enables naming TCPA/GDPR. The agent can infer these domain-specific risks from the prompt, and the simulated output names them. The definition does not pre-wire notifications-domain risks by name, so the output depends on model inference from the prompt — plausible but not guaranteed.
- [x] PASS: Output's test levels table covers unit (logic, preference resolution), integration (internal REST API contract + external Sendgrid/Twilio/Firebase boundaries), and E2E — met. The definition's test levels structure and 3 amigos methodology support a full levels table, and the simulated output produces one covering all tiers with tools and coverage targets.
- [x] PASS: Output identifies integration test pattern — fakes/contract tests at provider boundaries, never live calls in CI — met. Testability concern instruction combined with edge case handling on external API failure would produce the fake/contract test pattern. Simulated output explicitly names this as a design requirement.
- [x] PASS: Output's edge case checklist covers concurrency, opt-out timing, and channel fallback — met. All three map directly to Edge Case Checklist categories. Simulated output produces specific scenarios for each.
- [x] PASS: Output applies the 3 amigos lens with named specific questions for PO and architect — met. The 3 Amigos Pattern provides explicit question frames per role, and the simulated output produces domain-specific questions derived from these frames.
- [x] PASS: Output sets specific quality gates pre-merge and pre-release — met. Output Format separates both checkpoints. Test Strategy step 4 directs measurable gates at each. Simulated output includes quantified targets (90% coverage, 30-minute load run, opt-out audit query).
- [x] PASS: Output addresses scaling from 50K to 500K notifications/day — met. Test Strategy step 6: "Cover stated growth or scale targets — if the prompt names launch volume and a future target, the strategy must validate the trajectory, not just the launch state." Simulated output includes load tests at both volumes.
- [x] PASS: Output stays at strategy level, no implementation test code or method names — met. The definition is unambiguous on this boundary, and the simulated output contains no test method signatures or assertion library usage.
- [x] PASS: Output identifies at least one specific gap — met. Test Strategy step 5 directs "Identify what can't be automated." Decision Checkpoints include "Signing off on a feature without edge case coverage — document the gap." Simulated output produces four named gaps with owners.
- [~] PARTIAL: Output addresses observability requirements as a testability concern — partially met. The definition covers testability concerns as a design requirement and the Testability section flags them. However, "observability" (asserting delivery state vs. request acceptance, queue hooks, provider callbacks) is not named as a distinct testability category in the definition. The simulated output surfaces it (item 2 in Testability Requirements), inferred from prompt context. The definition does not reliably guide the model toward this — it depends on the model recognising the queue/callback pattern as a testability concern from the scenario description.

## Notes

The two remaining PARTIAL criteria share the same root cause: the definition is structurally complete but lacks domain-specific heuristics for two judgment calls — test level rationale rules and observability as a named testability sub-category. Both gaps would require additions to the agent definition to close reliably, not just prompt-level inference.

The simulated output performs well on both: the test level rationale table is specific and defensible, and the testability section names the queue observability requirement explicitly. But "the model can infer this from a good prompt" is not the same as "the definition directs the model toward this." The PARTIAL verdict reflects the definition's reliability ceiling, not the output quality ceiling.

Score: 15.5/19 (82%) — PARTIAL.
