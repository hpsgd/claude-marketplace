# Test: Write bug report for double-charge on retry

Scenario: Developer invokes the write-bug-report skill after discovering that retrying a failed payment creates a duplicate charge. The issue was found in production and a support ticket has been raised.

## Prompt

Write a bug report for this issue: When a payment attempt fails (e.g. card declined) and the user retries using the same form, a duplicate charge is created. We've had 3 confirmed cases in production. The payment goes through on the second attempt, but customers are charged twice. We're on commit `a4f92bc`, running Python 3.12, Django 4.2. The charge creation is in `src/billing/charges.py::create_charge()`.

## Criteria

- [ ] PASS: Skill mandates systematic investigation before writing the report — Phase 1 (evidence gathering), Phase 2 (pattern analysis), Phase 3 (root cause tracing), Phase 4 (coverage gap analysis)
- [ ] PASS: Skill assigns Critical severity — data loss/financial impact criteria are met (customers charged twice)
- [ ] PASS: Reproduction steps pass the "stranger test" — each step is one action with exact inputs and preconditions stated
- [ ] PASS: Error messages are copied verbatim — skill does not paraphrase or summarise error output
- [ ] PASS: Report distinguishes root cause (underlying defect) from proximate cause (immediate trigger) and contributing factor
- [ ] PASS: Coverage gap section asks: should a test have caught this? Identifies the missing test (idempotency check on retry)
- [ ] PASS: Report includes environment details: OS, Python version, commit SHA, and any relevant config
- [ ] PASS: Severity modifier is applied correctly — financial impact upgrades severity, not downgrades it
- [ ] PARTIAL: Report includes a suggested fix only if root cause is identified with confidence — not speculative
