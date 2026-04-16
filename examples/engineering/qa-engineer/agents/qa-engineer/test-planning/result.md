# Payment processing module test suite

User asks the QA engineer to write tests for a payment processing module that handles charge creation, refunds, and webhook verification. The module has no existing tests.

## Prompt

> We've just finished the payment processing module for our SaaS app. It handles three things: creating Stripe charges (with idempotency keys), processing refunds (full and partial), and verifying incoming Stripe webhooks using signature validation. There are currently zero tests. The module is in `src/payments/` and uses our Django Ninja API. Can you write a comprehensive test suite for it? We use pytest.

## Output

**Simulated agent response for this prompt:**

Pre-flight: reads CLAUDE.md and existing test files for conventions (test runner: pytest, file location, assertion style). Then reads `src/payments/` completely — inspects `charges.py`, `refunds.py`, `webhooks.py` public API surface, inputs, outputs, error paths, and exception types before writing any tests.

TDD Iron Law: writes RED tests first. `pytest tests/payments/ -v` → exit code 1. Confirms failure message is meaningful. Then implements minimum code. GREEN → exit code 0.

Test cases identified:
- Happy path: successful charge creation, full refund, partial refund, valid webhook
- Edge cases: zero amount charge (should raise), duplicate idempotency key (idempotent behaviour), expired card response
- Error cases: Stripe network failure (mock `stripe.Charge.create`), invalid webhook signature
- Idempotency: calling `create_charge` twice with same key returns same result

Run mode: `pytest tests/payments/ -v` — not `pytest --watch`. Reports exact command and exit code.

Mocking: only `stripe.Charge.create`, `stripe.Refund.create`, `stripe.Webhook.construct_event` at the library boundary. Not mocking internal `PaymentService` classes.

Evidence table: test name | command | exit code | PASS/FAIL.

Unit tests: pure logic (refund amount validation). Integration-style: webhook endpoint via Django test client.

One assertion per test: each test has a single `assert` or `pytest.raises` block.

Note: the agent does not have an explicit instruction to identify security-specific test cases (signature bypass, negative amounts, over-refund) during test generation. It would identify error cases and boundary values per Step 2, which would likely surface these, but there is no dedicated security test step in the generate-tests skill.

## Evaluation

- [x] PASS: Agent reads existing code before writing tests — qa-engineer agent Pre-Flight Step 2 and generate-tests SKILL.md Step 1 (Reconnaissance) both mandate reading the code under test completely before writing any test.
- [x] PASS: Agent follows TDD Iron Law — qa-engineer agent definition has a full "TDD Methodology" section with the Iron Law; generate-tests SKILL.md opens with the Iron Law as a non-negotiable.
- [x] PASS: Agent identifies test cases across all required categories — generate-tests SKILL.md Step 2 mandates happy path, edge cases (empty, boundary, single-element), and error cases (invalid inputs, network/IO failures, timeouts) as MUST-have categories.
- [x] PASS: Agent runs tests in run mode with exact command and exit code — generate-tests SKILL.md Step 4 specifies `pytest tests/path/to/test_file.py -v` in run mode; the Evidence Requirements section mandates exact command and exit code.
- [x] PASS: Agent mocks only at external boundaries — generate-tests SKILL.md Anti-Patterns explicitly prohibits "Mocking what you own — mock at external boundaries only (HTTP, database, file system)"; qa-engineer agent Principles states "Mock only at external boundaries."
- [~] PARTIAL: Agent identifies security-relevant test cases — generate-tests SKILL.md Step 2 covers error cases and state transitions (including idempotency), which would surface duplicate-key and refund-boundary cases. But there is no explicit instruction to identify security-specific test cases (bypass attempts, negative amounts). The criterion is partially met through the error/edge case framework, not through a dedicated security step.
- [x] PASS: Agent produces evidence table — generate-tests SKILL.md Evidence Requirements section mandates an Evidence table with test name, command, exit code, and PASS/FAIL result. The format is specified explicitly.
- [~] PARTIAL: Agent covers both unit and integration-style tests — the generate-tests SKILL.md covers test categories (happy/edge/error) and mentions Playwright/Cypress for E2E in the qa-engineer context, but does not explicitly require a split between unit tests and integration-style endpoint tests as a structured requirement. The qa-engineer agent mentions both unit test coverage and E2E acceptance testing, but as separate work types, not as a mandatory pairing within a single test generation task. Maximum score is 0.5 per criterion ceiling.
- [x] PASS: Agent applies one assertion per test — generate-tests SKILL.md Step 3 mandates "Assert — verify ONE expected outcome" per test; Anti-Patterns explicitly lists "Multiple assertions per test" as never do.


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/9 criteria met (83%) |
| Evaluated | 2026-04-16 |


## Notes

The existing evaluation scored this 8.5/9 (94%) by marking criterion 6 (security test cases) as PASS. The definition does not contain a specific step or instruction for security test identification during test generation — it surfaces security via the error/edge case categories, not a dedicated mechanism. Downgraded to PARTIAL. The score remains above the 80% PASS threshold.
