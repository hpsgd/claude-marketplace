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

## Output expectations

- [ ] PASS: Output's severity is Critical — explicitly justified with the financial-impact criterion (customers charged twice) and the 3 confirmed production cases
- [ ] PASS: Output's reproduction steps describe the exact user actions: navigate to payment form, submit with a card that will be declined (or trigger decline), see error, click Retry/resubmit same form — each step is one action, not a compound instruction
- [ ] PASS: Output's environment section lists commit `a4f92bc`, Python 3.12, Django 4.2 — verbatim — plus the file path `src/billing/charges.py::create_charge()`
- [ ] PASS: Output's investigation phases are explicit: Phase 1 (gather evidence — error logs, charge IDs, customer reports), Phase 2 (pattern analysis — what do the 3 cases share?), Phase 3 (root cause tracing in `create_charge()`), Phase 4 (coverage gap — should an idempotency test have caught this?)
- [ ] PASS: Output distinguishes root cause (e.g. missing or non-deterministic idempotency key on charge creation) from proximate cause (the second click) and any contributing factor (e.g. retry button not disabled after first click)
- [ ] PASS: Output identifies the specific missing test — an idempotency test that submits the same charge twice with the same key and asserts only one Stripe charge is created — naming this as the coverage gap
- [ ] PASS: Output copies error messages and log lines verbatim where they exist; if no specific error is present (the system silently double-charges), the report states this explicitly rather than fabricating one
- [ ] PASS: Output captures business-impact data — 3 confirmed cases, customer-facing implications (refunds owed), reputation/trust risk — to justify the severity assignment
- [ ] PARTIAL: Output's suggested fix (if any) is qualified with confidence — e.g. "Suggested: derive idempotency key from (customer_id, cart_hash, attempt_window) — confidence MEDIUM, requires confirming Stripe charge logs show the same idempotency key on both attempts"
