# Test: Test strategy for new notifications microservice

Scenario: User asks the QA lead to define a test strategy for a new microservice that sends email, SMS, and push notifications. The service will be called by multiple other services via an internal API.

## Prompt

We're building a new notifications microservice. It receives requests from other internal services (via a REST API), queues them, and delivers via Sendgrid (email), Twilio (SMS), and Firebase (push). There's a preference/opt-out system per user per channel. The service needs to handle ~50,000 notifications/day at launch, growing to ~500,000 within 12 months. Can you define the test strategy before we start development?

## Criteria

- [ ] PASS: Agent operates as the definition of WHAT to test — does not write implementation test code (that is the QA Engineer's job)
- [ ] PASS: Agent assesses the risk profile before defining test levels — identifies financial/reputational risk (sending duplicate notifications, ignoring opt-outs)
- [ ] PASS: Agent defines test levels covering unit, integration (internal API contract, external API boundaries), and E2E
- [ ] PASS: Agent applies the 3 amigos framing — identifies questions the product owner and architect must answer before development starts
- [ ] PASS: Agent identifies edge cases in the edge case checklist: concurrency (duplicate send race condition), opt-out timing, channel fallback when one provider is down
- [ ] PASS: Agent sets specific, measurable quality gates for pre-merge and pre-release
- [ ] PASS: Agent flags testability concerns — e.g. external providers must be fakeable in integration tests, not called live
- [ ] PARTIAL: Agent assigns test levels to specific criteria with rationale (unit vs integration vs E2E reasoning)
- [ ] PASS: Output includes Risk Assessment, Test Levels table, Quality Gates, and at minimum one identified gap
