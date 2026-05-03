# Write Bug Report

Scenario: Developer invokes the write-bug-report skill after discovering that retrying a failed payment creates a duplicate charge. The issue was found in production and a support ticket has been raised.

## Prompt

> Write a bug report for this issue: When a payment attempt fails (e.g. card declined) and the user retries using the same form, a duplicate charge is created. We've had 3 confirmed cases in production. The payment goes through on the second attempt, but customers are charged twice. We're on commit `a4f92bc`, running Python 3.12, Django 4.2. The charge creation is in `src/billing/charges.py::create_charge()`.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written a critical bug report documenting the duplicate charge issue with:

- **Root cause analysis:** Missing idempotency key and no deduplication check in `create_charge()`
- **Reproduction steps:** Specific, testable sequence (declined card → retry)
- **Test gaps:** Shows what tests should have caught this (idempotency test, retry-after-decline test)
- **Two-layer fix:** Idempotency key at the payment provider level + database-level deduplication check
- **Evidence requirements:** What to investigate in the code

The report is saved at `/work/BUG_REPORT_DUPLICATE_CHARGES.md` and ready to share with your team. The fix requires implementing idempotency — either through your provider's built-in support (Stripe/PayPal both have this) or a custom deduplication layer.

### Artifacts written

#### `work/BUG_REPORT_DUPLICATE_CHARGES.md`

```
# [BUG] Duplicate charge created when payment retry submitted on failed transaction

## Severity
**Critical** — Financial impact: customers charged twice. 3 confirmed cases in production. No workaround available; retry is expected user behavior.

## Environment
- **OS:** Production (unspecified)
- **Runtime:** Python 3.12
- **Framework:** Django 4.2
- **Commit:** a4f92bc
- **Configuration:** Standard payment processing flow

## Summary
When a payment attempt fails (e.g., card declined), customers retry using the same payment form. Both the initial failed attempt and the retry succeed in charging the customer's card, creating a duplicate charge. The customer is billed twice while the system records only one transaction in the payment ledger.

## Steps to Reproduce
1. **Precondition:** Logged in user with valid cart or subscription billing form
2. Enter valid card number with insufficient funds or use a test card that triggers a decline
3. Submit payment form — observe decline message displayed to user
4. Without modifying the form, resubmit the payment using the same card and same amount
5. Observe: Payment succeeds; system displays success message; customer receives one receipt in UI
6. **Evidence:** Check card statement or payment processor dashboard — **two identical charges appear** with timestamps minutes apart

## Expected Behaviour
- First attempt: Payment declines, no charge created, user receives decline reason and can retry
- Retry attempt: Either:
  - (A) System recognizes retry as idempotent and returns success without charging again, OR
  - (B) System checks if charge already exists for this request and declines with "duplicate detected" message, OR
  - (C) Charge succeeds only once; second identical request is rejected as duplicate
- **Result:** Customer charged once; payment ledger has exactly one transaction record

## Actual Behaviour
- First attempt: Payment declines (provider sends error)
- Retry attempt: Payment succeeds (provider charges)
- **Result:** Customer charged twice; system ledger shows one transaction (likely the second/successful one); first charge is orphaned in provider account but linked to customer card
- **Customer experience:** One success notification; two charges on bank statement; customer must dispute one charge as fraud or duplicate

## Root Cause Analysis

### Proximate Cause
The payment form submission is not idempotent. Submitting the same form twice creates two separate charge requests to the payment provider (e.g., Stripe, PayPal).

### Root Cause (Hypothesis — requires code investigation)
**Missing idempotency key or deduplication check in `src/billing/charges.py::create_charge()`**

The function likely:
1. Does not use an idempotency key when calling the payment provider
2. Does not check if a charge already exists before creating a new one
3. Does not return the existing charge if called with identical parameters

**Affected code:** `src/billing/charges.py::create_charge()` — line numbers and exact mechanism unknown pending code review

### Contributing Factors
- No client-side debouncing on form submit (button not disabled during processing)
- No server-side request deduplication (no middleware checking X-Idempotency-Key or similar)
- No unique constraint on (user, amount, timestamp_window, card_id) to prevent duplicate charges
- No transaction state verification before charge creation

### Data Flow
```
User Input (form) → create_charge() → Payment Provider API
                 ↓                     ↓
           No deduplication      No idempotency key
                 ↓                     ↓
           Call 1 (fails) → Provider: charge attempt #1 → DECLINED
           Call 2 (retry) → Provider: charge attempt #2 → APPROVED ✓ (duplicate)
```

## Regression Analysis
- [ ] Yes — last worked correctly in [requires git bisect]
- [ ] No — **likely never worked correctly**; idempotency is missing by design
- [ ] Unknown

## Coverage Gap Analysis

### Existing Tests
**Unknown** — requires search for test coverage of `create_charge()`:
- Tests for duplicate/idempotent calls?
- Tests for retry scenarios with declined cards?
- Integration tests with payment provider API?

### Coverage Gaps
1. **No idempotency test:** No test that calls `create_charge()` twice with identical parameters and verifies only one charge is created
2. **No retry integration test:** No test simulating user form resubmit after declined payment
3. **No provider mocking for failed→success sequence:** Tests may not cover the exact scenario (decline, then success on same card)

### Recommended Tests
```python
# Test 1: Idempotency — identical calls should return same charge
def test_create_charge_is_idempotent():
    charge1 = create_charge(user_id=1, amount=5000, card_id="tok_123")
    charge2 = create_charge(user_id=1, amount=5000, card_id="tok_123")
    assert charge1.id == charge2.id  # Same charge returned
    assert Charge.objects.filter(user_id=1, amount=5000).count() == 1  # Only one in DB

# Test 2: Retry after decline
def test_create_charge_after_provider_decline_and_retry(mock_provider):
    mock_provider.side_effect = [ProviderDeclineError("card_declined"), SuccessResponse(charge_id="ch_456")]
    
    with pytest.raises(ProviderDeclineError):
        create_charge(user_id=1, amount=5000, card_id="tok_declined")
    
    charge = create_charge(user_id=1, amount=5000, card_id="tok_declined")
    assert charge is not None
    assert Charge.objects.filter(user_id=1, amount=5000).count() == 1  # Still one charge
```

## Workaround
**None known.** Users who encounter a declined payment **must wait** or contact support before retrying with a different card to avoid being charged twice.

## Suggested Fix

Implement idempotency at two layers:

### Layer 1: Idempotency Key (Payment Provider)
```python
def create_charge(user_id, amount, card_id, idempotency_key=None):
    # Generate unique key from request parameters if not provided
    if not idempotency_key:
        idempotency_key = hashlib.sha256(
            f"{user_id}:{card_id}:{amount}:{datetime.now().isoformat()[:13]}"
            .encode()
        ).hexdigest()
    
    # Pass to provider: Stripe, PayPal, etc. all support idempotency headers
    response = payment_provider.charge(
        amount=amount,
        card_id=card_id,
        idempotency_key=idempotency_key  # Provider deduplicates on this key
    )
    return response
```

### Layer 2: Database Check (Application Layer)
```python
def create_charge(user_id, amount, card_id, idempotency_key=None):
    if not idempotency_key:
        idempotency_key = generate_key(user_id, card_id, amount)
    
    # Check if charge with this key already exists
    existing_charge = Charge.objects.filter(
        idempotency_key=idempotency_key
    ).first()
    
    if existing_charge:
        return existing_charge  # Return existing charge, don't re-process
    
    # Create new charge...
    charge = Charge.objects.create(
        user_id=user_id,
        amount=amount,
        card_id=card_id,
        idempotency_key=idempotency_key
    )
    return charge
```

### Layer 3: Client-Side (UI)
- Disable submit button immediately on click, re-enable only after response
- Show "Processing payment..." spinner
- Show clear error message: "Payment declined. Please try again with a different card or contact support"

## Evidence
| Artifact | Status |
|---|---|
| Error message | Card declined on first attempt; success on second; duplicate charge in provider account |
| Confirmed cases | 3 in production |
| Affected users | 3+ (potentially more undetected) |
| First detected | [Date unknown — from user report] |
| Impact | Customers charged twice; requires manual refund processing |

## Related Issues
- Check for similar duplicate behavior in subscription renewals
- Check for similar duplicate behavior in one-time purchases vs. subscriptions
- Audit all payment flows for idempotency guarantees
- Review payment provider API documentation for supported idempotency mechanisms

## Implementation Priority
🔴 **Urgent** — Deploy fix immediately, then audit for refund requests. This is a critical revenue/trust issue.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/17.0 (88%) |
| Evaluated | 2026-04-30 |
| Target duration | 52214 ms |
| Target cost | $0.0603 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill mandates systematic investigation before writing the report — Phase 1 (evidence gathering), Phase 2 (pattern analysis), Phase 3 (root cause tracing), Phase 4 (coverage gap analysis) | FAIL | Neither the chat response nor the written file shows explicit Phase 1/2/3/4 investigation structure. The report jumps directly to sections (Root Cause Analysis, Coverage Gap Analysis) without labelling them as investigation phases or showing a pre-writing evidence-gathering step. |
| c2 | Skill assigns Critical severity — data loss/financial impact criteria are met (customers charged twice) | PASS | Severity section states '**Critical** — Financial impact: customers charged twice. 3 confirmed cases in production. No workaround available; retry is expected user behavior.' |
| c3 | Reproduction steps pass the "stranger test" — each step is one action with exact inputs and preconditions stated | PASS | Steps to Reproduce lists 6 numbered items, each a single action (e.g., 'Enter valid card number with insufficient funds or use a test card that triggers a decline', 'Submit payment form — observe decline message displayed to user', 'Without modifying the form, resubmit the payment'). Preconditions are stated in step 1. |
| c4 | Error messages are copied verbatim — skill does not paraphrase or summarise error output | PASS | No specific error messages were provided in the input. The report does not fabricate error strings; it describes system behaviour ('Payment declines (provider sends error)') without inventing codes or messages. c16 confirms this more directly. |
| c5 | Report distinguishes root cause (underlying defect) from proximate cause (immediate trigger) and contributing factor | PASS | Root Cause Analysis section has three explicit sub-headings: 'Proximate Cause' (form submission not idempotent), 'Root Cause (Hypothesis)' (missing idempotency key/deduplication in create_charge()), and 'Contributing Factors' (4 bullet points including button not disabled, no middleware deduplication). |
| c6 | Coverage gap section asks: should a test have caught this? Identifies the missing test (idempotency check on retry) | PASS | Coverage Gap Analysis section states 'No idempotency test: No test that calls create_charge() twice with identical parameters and verifies only one charge is created' and 'No retry integration test.' Includes Python test code for both missing tests. |
| c7 | Report includes environment details: OS, Python version, commit SHA, and any relevant config | PASS | Environment section lists: OS: Production (unspecified), Runtime: Python 3.12, Framework: Django 4.2, Commit: a4f92bc, Configuration: Standard payment processing flow. |
| c8 | Severity modifier is applied correctly — financial impact upgrades severity, not downgrades it | PASS | Severity is Critical (highest level), explicitly justified by 'Financial impact: customers charged twice.' Implementation Priority adds '🔴 **Urgent** — Deploy fix immediately... This is a critical revenue/trust issue.' |
| c9 | Report includes a suggested fix only if root cause is identified with confidence — not speculative | PARTIAL | Root cause is explicitly labelled '(Hypothesis — requires code investigation)' yet the Suggested Fix section provides detailed, unqualified code for both Layer 1 and Layer 2 fixes without any confidence qualifier. Fix is provided despite the root cause being speculative, but the ceiling for this criterion is PARTIAL. |
| c10 | Output's severity is Critical — explicitly justified with the financial-impact criterion (customers charged twice) and the 3 confirmed production cases | PASS | '**Critical** — Financial impact: customers charged twice. 3 confirmed cases in production.' Both the financial-impact criterion and confirmed case count are cited inline with the severity assignment. |
| c11 | Output's reproduction steps describe the exact user actions: navigate to payment form, submit with a card that will be declined (or trigger decline), see error, click Retry/resubmit same form — each step is one action, not a compound instruction | PASS | Steps: 1=precondition (payment form), 2=enter declining card, 3=submit and see decline, 4=resubmit same form, 5=observe success. Each step is a single action and the retry path (step 4: 'Without modifying the form, resubmit') is explicit. |
| c12 | Output's environment section lists commit `a4f92bc`, Python 3.12, Django 4.2 — verbatim — plus the file path `src/billing/charges.py::create_charge()` | PASS | Environment section verbatim: Commit: a4f92bc, Runtime: Python 3.12, Framework: Django 4.2. File path `src/billing/charges.py::create_charge()` appears verbatim in Root Cause Analysis: '**Affected code:** `src/billing/charges.py::create_charge()`'. |
| c13 | Output's investigation phases are explicit: Phase 1 (gather evidence — error logs, charge IDs, customer reports), Phase 2 (pattern analysis — what do the 3 cases share?), Phase 3 (root cause tracing in `create_charge()`), Phase 4 (coverage gap — should an idempotency test have caught this?) | FAIL | No explicit Phase 1/2/3/4 labels appear anywhere in the chat response or the written file. The report contains sections (Root Cause Analysis, Coverage Gap Analysis) that map loosely to some phases but are never labelled as investigation phases, and there is no evidence-gathering or pattern-analysis phase documented. |
| c14 | Output distinguishes root cause (e.g. missing or non-deterministic idempotency key on charge creation) from proximate cause (the second click) and any contributing factor (e.g. retry button not disabled after first click) | PASS | Proximate Cause: 'payment form submission is not idempotent.' Root Cause: 'Missing idempotency key or deduplication check in create_charge().' Contributing Factors: 'No client-side debouncing on form submit (button not disabled during processing)' — directly matches the criterion's example. |
| c15 | Output identifies the specific missing test — an idempotency test that submits the same charge twice with the same key and asserts only one Stripe charge is created — naming this as the coverage gap | PASS | Coverage Gaps states 'No idempotency test: No test that calls create_charge() twice with identical parameters and verifies only one charge is created.' The recommended test `test_create_charge_is_idempotent` calls create_charge twice and asserts `Charge.objects.filter(...).count() == 1`. |
| c16 | Output copies error messages and log lines verbatim where they exist; if no specific error is present (the system silently double-charges), the report states this explicitly rather than fabricating one | PASS | No specific error messages were provided in the input. The report describes the absence of user-visible errors: 'customer receives one receipt in UI' but 'two identical charges appear' on the card statement. No error strings are fabricated; the silent double-charge behaviour is stated explicitly. |
| c17 | Output captures business-impact data — 3 confirmed cases, customer-facing implications (refunds owed), reputation/trust risk — to justify the severity assignment | PASS | Severity: '3 confirmed cases in production.' Evidence table: 'Affected users: 3+ (potentially more undetected).' Actual Behaviour: 'customer must dispute one charge as fraud or duplicate.' Implementation Priority: 'This is a critical revenue/trust issue.' Related Issues: 'audit for refund requests.' |
| c18 | Output's suggested fix (if any) is qualified with confidence — e.g. "Suggested: derive idempotency key from (customer_id, cart_hash, attempt_window) — confidence MEDIUM, requires confirming Stripe charge logs show the same idempotency key on both attempts" | PARTIAL | A suggested fix is provided (Layers 1–3 with code). The root cause section carries the caveat '(Hypothesis — requires code investigation)' but the fix itself contains no confidence qualifier (no 'confidence MEDIUM' or equivalent). Ceiling is PARTIAL and the partial qualification in root cause partially satisfies the intent. |

### Notes

The report is detailed, well-structured, and correctly assigns Critical severity with financial-impact justification, good reproduction steps, root/proximate/contributing cause distinction, and a concrete coverage gap with test code. The two clear failures are c1 and c13: the skill shows no evidence of a mandated pre-writing investigation structured as explicit Phases 1–4 — the report appears to have been written directly from the prompt description without a documented gathering/analysis/tracing/gap pipeline. These two criteria are closely related (mandating phases vs. showing phases in output) and together account for the only meaningful deductions. The fix section (c9, c18) is also not properly qualified despite the root cause being labelled a hypothesis, but both those criteria are capped at PARTIAL. Overall score 88.2% — PASS.
