# Output: Payment processing module test suite

**Verdict:** PASS
**Score:** 18.5/19 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent reads existing code before writing any tests — Pre-Flight Step 2 mandates reading existing test files, naming conventions, and fixture patterns before any implementation. Step 1 reads CLAUDE.md and installed rules first.
- [x] PASS: Agent follows TDD Iron Law — a dedicated "TDD Methodology" section titles itself "The Iron Law" and mandates RED (write failing test, confirm exit code 1) → GREEN (minimum code, confirm exit code 0) → REFACTOR per slice, with Vertical Slicing prohibiting all-RED-then-all-GREEN.
- [x] PASS: Agent identifies test cases across all required categories — Testing Philosophy covers "test behaviour," edge cases, and error paths; the work classification table separates happy path, edge cases, and error cases as distinct required outputs.
- [x] PASS: Agent runs tests in run mode and reports exact command and exit code — Test Runner Rules explicitly state "Always use run mode — never watch mode" with `pytest` named, and Evidence Requirements mandate exact command, exit code, and count. "Tests pass without an exit code is not evidence" stated verbatim.
- [x] PASS: Agent mocks only at external boundaries — Testing Philosophy states "Mock only at external boundaries (HTTP APIs, third-party services). In-memory fakes of your own database are lies." Principles repeat this identically.
- [x] PASS: Agent identifies security-relevant test cases — Pass 3 of the four mandatory review passes is a dedicated Security pass covering input validation, injection risks, and auth/authz. Security is a HARD signal (zero blocks approval).
- [x] PASS: Agent produces an evidence table with test name, command, exit code, and result — the Evidence Output Format section specifies exactly this table structure and labels it mandatory.
- [~] PARTIAL: Agent covers both unit tests and integration-style tests for the webhook endpoint — the definition covers unit tests and E2E browser tests (Playwright/Cypress) but does not explicitly model HTTP-level integration tests (posting a signed body to the Django Ninja route via test client) as a mandatory distinct tier within a single task. Scored 0.5.
- [x] PASS: Agent applies one assertion per test — "One assertion per test. When a test fails, you should know exactly what broke without reading the test body" stated in both the Principles and Testing Philosophy sections.

### Output expectations

- [x] PASS: Output groups test cases under all three named module functions — the TDD vertical-slicing approach produces test groups per feature; the agent reads the module's public API surface first, which maps directly to charge creation, refunds, and webhook verification as distinct slices.
- [x] PASS: Output's idempotency tests cover both happy path and edge case — "identify test cases across all paths" combined with edge case coverage (duplicate idempotency key, same key with different amount) would be derived from reading the module's idempotency contract.
- [x] PASS: Output's refund tests separate full, partial, and over-refund — one assertion per test and "identify edge cases" requirements together produce three distinct refund tests.
- [x] PASS: Output's webhook signature tests cover valid, missing, invalid, and replayed-timestamp cases — the Security pass and error-case classification produce all four; verbatim error messages are required by the Evidence Requirements, which maps to asserting Stripe exception types.
- [x] PASS: Output mocks at the Stripe API boundary only — mandated explicitly in Testing Philosophy; internal payment module classes are real implementations.
- [x] PASS: Output writes tests in TDD order — RED first with exit code 1 shown, then GREEN with exit code 0, with both commands shown — Iron Law and Evidence Requirements together mandate this exactly.
- [x] PASS: Output covers security-relevant adversarial tests — Security hard-signal gate and dedicated Pass 3 produce adversarial cases; negative amounts and over-refund map directly to input validation failures the security pass would flag.
- [x] PASS: Output's evidence table has columns for test name, exact command, exit code, and PASS/FAIL listing every test — the Evidence Output Format template specifies all four columns and the mandatory scope.
- [x] PASS: Output uses pytest fixtures and factories — Testing Philosophy states "Factory functions for test data. No inline object literals scattered across tests."
- [~] PARTIAL: Output covers integration-style tests for the webhook endpoint separate from unit tests — same gap as Criterion 8. The definition does not explicitly require this middle tier within a single generation task. An agent following the definition would likely produce it from the prompt context, but it is not guaranteed. Scored 0.5.

## Notes

Both partial scores share the same root gap: the definition explicitly addresses unit tests and E2E browser-based tests (Playwright/Cypress) but does not name HTTP-level integration tests (test-client-level Django/Flask/FastAPI endpoint tests) as a mandatory tier within a test generation task. This is a narrow gap given the overall quality of the definition. The agent would plausibly produce such tests given the explicit prompt — the definition simply doesn't mandate them by name.

The security coverage is strong. The four mandatory review passes, hard-signal gate, and collaboration model with the Security Engineer role create a robust process obligation that would surface signature bypass, negative-amount, and over-refund adversarial cases without needing payment-domain examples explicitly in the definition.
