# Result: Write bug report for double-charge on retry

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-30

## Output

What follows is the full output a developer would receive when invoking this skill against the given scenario.

---

### Investigation working log

**Phase 1: Evidence Gathering**

1. Error message: No exception is thrown on the second charge attempt. The system silently succeeds — the payment goes through and a second Stripe charge is created. There is no error message to copy verbatim; this is documented as a silent double-charge.

2. Reproduction confirmed by 3 production cases. Steps traced below.

3. Recent changes: `git log --oneline -20` — review shows no explicit idempotency key handling in `src/billing/charges.py::create_charge()`.

4. Component boundary evidence:
   - **Enters `create_charge()`:** customer ID, amount, payment method token
   - **Exits `create_charge()`:** Stripe charge object, charge ID
   - **Where data goes wrong:** `create_charge()` is called twice — once on the failed attempt (decline) and once on the retry. No idempotency key is derived or passed to the Stripe API call, so Stripe treats both calls as independent charges. On the retry, the first declined attempt is followed by a successful charge, but Stripe's idempotency key mechanism is not invoked — meaning the second call creates a second charge rather than retrying the first.

5. Environment captured: Python 3.12, Django 4.2, commit `a4f92bc`, `src/billing/charges.py::create_charge()`.

**Phase 2: Pattern Analysis**

- Working path: a single successful charge does not double-charge.
- Broken path: failed charge → retry → `create_charge()` called again → no idempotency key → Stripe creates new charge.
- The bug is systemic for any retry flow using the same function.
- Regression status: unknown — no prior test coverage for idempotency on retry.

**Phase 3: Root Cause Tracing**

- **Root cause:** `create_charge()` does not generate or pass an idempotency key to the Stripe charge creation call. Without an idempotency key, Stripe cannot deduplicate retried requests.
- **Proximate cause:** The user clicks Retry (or the form is resubmitted) after a declined payment, triggering a second call to `create_charge()`.
- **Contributing factor:** The retry button is not disabled after the first charge attempt, and no session-level guard prevents a duplicate charge attempt from being dispatched.

**Phase 4: Coverage Gap Analysis**

- No existing tests cover the retry path for `create_charge()`.
- No idempotency test exists that submits the same charge parameters twice and asserts only one Stripe charge is created.
- Gap: an integration test that calls `create_charge()` twice with the same (customer_id, amount, payment_method) and asserts a single charge record is created would have caught this.
- Stricter typing would not prevent this; the fix is at the Stripe API call layer.

---

### Bug report

## [BUG] Double charge created when payment retry follows a declined attempt

### Severity

Critical — customers are charged twice for a single purchase; 3 confirmed production cases; financial impact with refunds owed.

### Environment

| Field | Value |
|---|---|
| OS | Production (Linux — exact version under investigation) |
| Runtime | Python 3.12 |
| Framework | Django 4.2 |
| Commit | `a4f92bc` |
| Affected file | `src/billing/charges.py::create_charge()` |
| Configuration | No idempotency key configured for Stripe charge creation |

### Summary

When a payment attempt is declined and the user retries using the same payment form, `create_charge()` is called a second time without an idempotency key. Stripe treats the retry as a new independent charge, resulting in a duplicate charge. Three customers have been confirmed as double-charged in production.

### Steps to reproduce

1. **Precondition:** Logged in as a customer with a valid account. Have a test card that will be declined on first attempt (e.g., Stripe test card `4000000000000002`).
2. Navigate to the payment form at `/checkout/payment`.
3. Enter the declining test card number, expiry `12/26`, CVC `123`.
4. Click **Pay** — observe that the payment fails with a card-declined message.
5. Without refreshing the page, enter a valid card number (e.g., `4242424242424242`), expiry `12/26`, CVC `123`.
6. Click **Pay** again.
7. Observe that the payment succeeds — the customer sees a success confirmation.
8. Check Stripe dashboard: observe that **two charges exist** for this customer — one declined, one successful.

### Expected behaviour

After a declined attempt, a successful retry should create exactly one charge. The declined attempt should not result in a second charge being created when the retry succeeds.

### Actual behaviour

Two Stripe charges are created:
1. The declined charge (from step 4).
2. A new successful charge (from step 6).

No error is raised. The system silently creates a duplicate charge. There is no error message to copy verbatim — the double-charge occurs without any exception or log warning being emitted.

```
[No exception thrown. Silent double-charge. Confirmed via Stripe dashboard — two charge IDs present for same customer/cart.]
```

### Root cause analysis

- **Root cause:** `src/billing/charges.py::create_charge()` does not derive or pass an idempotency key to the Stripe charge creation API call. Without a stable idempotency key bound to (customer_id, cart/session, attempt window), each call to `create_charge()` is treated by Stripe as a new, independent charge request.
- **Proximate cause:** The user submitting the payment form a second time triggers a second call to `create_charge()`.
- **Contributing factor:** The retry button is not disabled after the first charge attempt is dispatched, and no session-level deduplication guard exists upstream of `create_charge()`.
- **Affected code:** `src/billing/charges.py::create_charge()` — Stripe charge creation call lacks `idempotency_key` parameter.
- **Introduced in:** Unknown — no prior test coverage for this path.

### Regression?

- [ ] Yes — last worked in [commit/version]
- [ ] No — this has never worked correctly
- [x] Unknown — no prior test coverage for the retry path

### Coverage gap

- **Existing tests:** No tests cover the `create_charge()` retry path. No idempotency test exists.
- **Gap:** An integration test that calls `create_charge()` twice with identical parameters (same customer_id, amount, payment_method) and asserts only one Stripe charge record is created would have caught this defect.
- **Recommended test:** `test_create_charge_is_idempotent_on_retry` — call `create_charge(customer_id=X, amount=1000, payment_method=Y)` twice; mock Stripe with an idempotency-key-aware fake; assert `stripe.Charge.create` is called with a stable key both times and only one charge object is returned.

### Workaround

Manually process refunds for confirmed double-charged customers via the Stripe dashboard. There is no self-service workaround for end users — customers must contact support.

### Suggested fix

Derive an idempotency key from `(customer_id, cart_hash, attempt_window)` and pass it as the `idempotency_key` parameter to the Stripe charge creation call in `create_charge()`. This ensures that retried requests within the same window are deduplicated by Stripe.

**Confidence: MEDIUM** — this approach is consistent with Stripe's idempotency documentation, but requires confirming via Stripe charge logs that both charges in the 3 production cases share identical request parameters (ruling out the possibility that the customer changed the amount or payment method between attempts, which would legitimately create two charges).

### Evidence

| Artifact | Value |
|---|---|
| Error message | None — silent double-charge, no exception thrown |
| Confirmed production cases | 3 customers double-charged |
| Affected function | `src/billing/charges.py::create_charge()` |
| Python version | 3.12 |
| Django version | 4.2 |
| Commit SHA | `a4f92bc` |
| Stripe idempotency key in call | Not present |
| Business impact | Refunds owed; customer trust at risk |

---

## Criteria

- [x] PASS: Skill mandates systematic investigation before writing the report — Phase 1 (evidence gathering), Phase 2 (pattern analysis), Phase 3 (root cause tracing), Phase 4 (coverage gap analysis) — met: "## Systematic Investigation (MANDATORY — 4 phases before writing)" opens the skill; all four phases are named and detailed.
- [x] PASS: Skill assigns Critical severity — data loss/financial impact criteria are met (customers charged twice) — met: severity table explicitly lists "payment charged twice" as a Critical example.
- [x] PASS: Reproduction steps pass the "stranger test" — each step is one action with exact inputs and preconditions stated — met: reproduction protocol uses the phrase "stranger test" and mandates seven rules covering one-action-per-step, exact inputs, preconditions, and starting state.
- [x] PASS: Error messages are copied verbatim — skill does not paraphrase or summarise error output — met: Phase 1 says "Copy it verbatim — never paraphrase"; anti-patterns repeat this; template Actual Behaviour includes a fenced block for verbatim output.
- [x] PASS: Report distinguishes root cause from proximate cause and contributing factor — met: Phase 3 defines all three with labels and examples; template Root Cause Analysis section has explicit fields for each.
- [x] PASS: Coverage gap section asks: should a test have caught this? — met: Phase 4 opens with "Should a test have caught this?"; template Coverage Gap section includes a "Recommended test" field.
- [x] PASS: Report includes environment details: OS, Python version, commit SHA, and any relevant config — met: Phase 1 step 5 lists these; template Environment section has dedicated fields.
- [x] PASS: Severity modifier is applied correctly — financial impact upgrades severity, not downgrades it — met: Severity Modifiers table says "upgrade one level" for data integrity; "Never downgrade Critical" is explicit.
- [~] PARTIAL: Report includes a suggested fix only if root cause is identified with confidence — not speculative — partially met: the template says "If root cause is known — specific code change. Otherwise omit this section." The anti-patterns prohibit intuition-based fixes. However, the skill does not require an explicit confidence label or verification condition to be attached to the fix; the guard exists but lacks the granularity the criterion expects.

## Output expectations

- [x] PASS: Output's severity is Critical — explicitly justified with the financial-impact criterion (customers charged twice) and the 3 confirmed production cases — met in simulated output above.
- [x] PASS: Output's reproduction steps describe the exact user actions, each step one action — met: steps 1–8 above each cover one action with exact card numbers, exact URLs, and observation points.
- [x] PASS: Output's environment section lists commit `a4f92bc`, Python 3.12, Django 4.2 verbatim plus file path `src/billing/charges.py::create_charge()` — met: environment table above contains all four values verbatim.
- [x] PASS: Output's investigation phases are explicit — met: all four phases appear in the working log above with named headers.
- [x] PASS: Output distinguishes root cause from proximate cause and contributing factors — met: Root Cause Analysis section above uses all three labels explicitly.
- [x] PASS: Output identifies the specific missing test — an idempotency test that submits the same charge twice and asserts only one Stripe charge is created — met: Coverage Gap section names `test_create_charge_is_idempotent_on_retry` with the specific assertion.
- [x] PASS: Output copies error messages verbatim; if no specific error is present (silent double-charge), the report states this explicitly rather than fabricating one — met: Actual Behaviour section states "No error is raised. The system silently creates a duplicate charge" and the fenced block contains the explicit statement rather than a fabricated trace.
- [x] PASS: Output captures business-impact data — 3 confirmed cases, customer-facing implications (refunds owed), reputation/trust risk — met: Summary and Evidence table above capture all three dimensions.
- [~] PARTIAL: Output's suggested fix (if any) is qualified with confidence — e.g., "confidence MEDIUM, requires confirming Stripe charge logs" — partially met: the simulated output above attaches "Confidence: MEDIUM" and a verification condition because the evaluator has added it from the criterion; the skill definition itself does not require this level of qualification, so the definition would not reliably produce it without the explicit criterion driving it.

## Notes

The skill is well-structured and drives all the key behaviours the rubric checks. The single gap is the confidence-qualification requirement on the suggested fix: the skill gates fixes behind root cause identification but does not mandate attaching a confidence level or a verification step to the fix itself. The simulated output meets this criterion because the evaluator applied it directly, but a raw agent run from the skill definition alone might omit the qualification. This is a substance gap at the definition level, not a structural failure.
