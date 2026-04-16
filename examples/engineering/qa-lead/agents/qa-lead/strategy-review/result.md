# Test strategy for new notifications microservice

User asks the QA lead to define a test strategy for a new microservice that sends email, SMS, and push notifications. The service will be called by multiple other services via an internal API.

## Prompt

> We're building a new notifications microservice. It receives requests from other internal services (via a REST API), queues them, and delivers via Sendgrid (email), Twilio (SMS), and Firebase (push). There's a preference/opt-out system per user per channel. The service needs to handle ~50,000 notifications/day at launch, growing to ~500,000 within 12 months. Can you define the test strategy before we start development?

The qa-lead agent reads CLAUDE.md and checks `.claude/rules/` before starting. It classifies this as a test strategy definition task and invokes the `/test-strategy` skill.

## Output

**Step 1 — Risk profile (assessed before any test levels):**

Reputational risk: sending duplicate notifications to a user damages trust and may violate user expectations (unsubscribes, spam complaints). Legal/compliance risk: ignoring opt-outs for SMS/email may violate CAN-SPAM, GDPR, or TCPA depending on jurisdiction. Financial risk: each provider call costs money — at 500K/day, runaway duplicates could generate significant unexpected API charges. Volume risk: the 10x growth target within 12 months means performance assumptions baked in at launch will need to be revisited.

**3 amigos questions (before development starts):**

To the Product Owner: What is the retry behaviour when a provider is unavailable? Is there an SLA per channel? What counts as a "delivered" notification for reporting purposes?

To the Architect: How is deduplication implemented — database-level idempotency key, queue deduplication, or application-level lock? Is the queue implementation testable in isolation with an in-memory fake?

Testability concern: Sendgrid, Twilio, and Firebase cannot be called live in integration tests. The architecture must expose provider interfaces that can be replaced with test fakes. If the provider clients are not injectable, this blocks integration testing — redesign required before development starts.

**Test levels:**

| Level | Scope | Tools | Coverage | Est. Tests |
|---|---|---|---|---|
| Unit | Preference lookup logic, deduplication logic, opt-out enforcement, message formatting | Vitest / xUnit | 80%+ changed code | ~30 |
| Integration | Internal REST API contract (schema validation), external provider boundaries via fakes (Sendgrid/Twilio/Firebase) — NOT live calls, database opt-out state | Supertest + Testcontainers | Critical paths | ~20 |
| E2E | Full flow: request received → queued → delivered; opt-out honoured end-to-end | Limited to top 3 critical flows | Top 3 flows | ~6 |
| Performance | 50K/day load baseline; 500K/day growth target | k6 | SLA benchmarks | N/A |

**Edge cases:**

Concurrency: two services POST the same notification simultaneously within milliseconds — race condition on queue deduplication. Opt-out timing: opt-out received while notification is already in-flight (in queue, not yet sent) — should the send be aborted or is the message already committed? Channel fallback: Firebase unavailable — is there a fallback to email, or does the notification fail silently?

**Quality gates:**

Pre-merge: all unit tests pass (exit 0), integration tests pass, 80%+ branch coverage on changed files, no new type errors, external provider clients replaced with fakes (no live API calls).

Pre-release: E2E critical paths pass on staging, load test at 50K/day request rate meets latency SLA, opt-out integration verified end-to-end.

**Test level assignment:**

| Criterion | Level | Rationale |
|---|---|---|
| Opt-out enforcement logic | Unit | Pure function, no dependencies |
| Duplicate deduplication | Integration | Requires database state |
| Internal API contract | Integration | Requires HTTP boundary |
| Full notification flow | E2E | Critical user-visible path |
| 500K/day capacity | Performance | Requires load testing tool |

**Gap:** No load testing specification exists for the 500K/day growth target. Performance baseline must be established now so the 12-month regression can be detected. This is the primary gap.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Agent defines WHAT to test, does not write implementation test code — qa-lead.md states "You don't implement tests — that's the QA Engineer" and "What You Don't Do: Implement automated tests." The boundary is explicit. The agent delegates test code to the QA Engineer.
- [x] PASS: Agent assesses risk profile before defining test levels — qa-lead.md Step 3 classify work: "Test strategy definition: Assess risk profile → set coverage targets → choose test levels." The test-strategy SKILL.md Step 1 makes risk profile the mandatory first step.
- [x] PASS: Agent defines unit, integration (API contract + external boundaries), and E2E test levels — test-strategy SKILL.md Step 2 defines all levels with the testing pyramid; the integration level explicitly includes "Boundaries, database, API endpoints, handlers" and Step 3 specifies that external providers must be faked (not called live in integration tests).
- [x] PASS: Agent applies 3 amigos framing — qa-lead.md has a dedicated "3 Amigos Pattern" section with the QA Lead's specific contribution list, including item 5: "Flag testability concerns — if something can't be tested, it needs to be redesigned before development starts."
- [x] PASS: Agent identifies the three specified edge cases — qa-lead.md Edge Case Checklist includes "Concurrency: Two users editing the same record. Duplicate submissions. Race conditions" (covers duplicate send race condition), "Error handling: Network failure, timeout, invalid input" (covers channel fallback), and the timing edge case falls under boundary conditions + permissions category.
- [x] PASS: Agent sets specific measurable quality gates — test-strategy SKILL.md Step 4 provides pre-merge and pre-release checklists with specific pass/fail criteria. The qa-lead agent Output Format requires "Quality Gates: Pre-merge: [checklist] / Pre-release: [checklist]."
- [x] PASS: Agent flags testability concern about external providers — qa-lead.md 3 amigos contribution item 5: "Flag testability concerns — if something can't be tested, it needs to be redesigned before development starts." The fakeability of Sendgrid/Twilio/Firebase is a direct testability design requirement that must be raised before development.
- [~] PARTIAL: Agent assigns test levels with rationale — test-strategy SKILL.md Step 2 includes the test levels table with "what it tests" per level. The qa-lead agent Output Format includes "Test Level Assignment: Criterion / Level / Rationale" columns. The definition supports this output but does not enforce a minimum rationale depth per criterion.
- [x] PASS: Output includes Risk Assessment, Test Levels table, Quality Gates, and identified gap — test-strategy SKILL.md output format explicitly requires all four sections: Risk Assessment, Test Levels table (with scope/tools/coverage/est. tests), Quality Gates (pre-merge + pre-release), and Gaps.

### Notes

The testability concern criterion (7) is unusually well-supported: qa-lead.md has it as an explicit numbered item in the 3 amigos contribution list, not just implied by general principles. The performance gap (500K/day growth target not specified in testing) is the correct identified gap for this scenario — a load testing specification at launch is a genuine omission given the stated 10x growth target within 12 months.
