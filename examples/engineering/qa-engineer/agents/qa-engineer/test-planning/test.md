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
