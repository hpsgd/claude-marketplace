# Test: Payment processing module test suite

Scenario: User asks the QA engineer to write tests for a payment processing module that handles charge creation, refunds, and webhook verification. The module has no existing tests.

## Prompt

We've just finished the payment processing module for our SaaS app. It handles three things: creating Stripe charges (with idempotency keys), processing refunds (full and partial), and verifying incoming Stripe webhooks using signature validation. There are currently zero tests. The module is in `src/payments/` and uses our Django Ninja API. Can you write a comprehensive test suite for it? We use pytest.

## Criteria

- [ ] PASS: Agent reads existing code before writing any tests — inspects the module's public API surface, inputs, outputs, and error paths
- [ ] PASS: Agent follows TDD Iron Law — writes failing tests first (RED), confirms exit code 1, then implements to make them pass (GREEN)
- [ ] PASS: Agent identifies test cases across all required categories: happy path, edge cases (zero amounts, duplicate idempotency keys, expired cards), and error cases (network failures, invalid signatures)
- [ ] PASS: Agent runs tests in run mode (`pytest`, not watch mode) and reports exact command and exit code
- [ ] PASS: Agent mocks only at external boundaries (Stripe API) — does not mock internal payment module classes
- [ ] PASS: Agent identifies security-relevant test cases: signature validation bypass attempts, negative refund amounts, over-refund attempts
- [ ] PASS: Agent produces an evidence table with test name, command, exit code, and result
- [ ] PARTIAL: Agent covers both unit tests (pure logic) and integration-style tests for the webhook endpoint
- [ ] PASS: Agent applies one assertion per test — flags any test that would assert multiple unrelated things

## Output expectations

- [ ] PASS: Output groups test cases under all three named module functions — charge creation (with idempotency keys), refunds (full and partial), webhook signature verification — not generic "payment tests"
- [ ] PASS: Output's idempotency tests cover both happy path (same key → same charge, no duplicate) and edge case (same key with different amount → error / explicit handling), with the deterministic Stripe idempotency contract
- [ ] PASS: Output's refund tests separate full refund (amount = original charge) from partial refund (amount < original) and over-refund attempt (amount > remaining), each as a distinct test
- [ ] PASS: Output's webhook signature tests cover valid signature, missing signature header, invalid signature (tampered body), and replayed timestamp (Stripe tolerance window), with verbatim Stripe library exception types asserted
- [ ] PASS: Output mocks at the Stripe API boundary only (e.g. `stripe.Charge.create`, `stripe.Webhook.construct_event`) — no mocking of the project's own `payments.charges` or `payments.refunds` internal classes
- [ ] PASS: Output writes tests in TDD order — RED first (`pytest -v` shows the failing tests with exit code 1) — then implementation, then GREEN (exit code 0), with both commands and exit codes shown as evidence
- [ ] PASS: Output covers security-relevant adversarial tests — signature bypass attempts, negative refund amounts, refund of already-refunded charge, charge with negative amount — as required failures (the function rejects them)
- [ ] PASS: Output's evidence table has columns for test name, exact command, exit code, and PASS/FAIL — and lists every test, not just a summary count
- [ ] PASS: Output uses pytest fixtures and factories for charge/refund/webhook event objects rather than inline dict construction repeated across tests
- [ ] PARTIAL: Output covers integration-style tests for the webhook endpoint (POSTing a signed body to the Django Ninja route) separate from the unit tests on `verify_webhook_signature`
