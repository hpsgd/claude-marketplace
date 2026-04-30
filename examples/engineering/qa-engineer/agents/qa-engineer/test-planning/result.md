# Result: Payment processing module test suite

**Verdict:** PASS
**Score:** 18.5/19 criteria met (97%)
**Evaluated:** 2026-04-30

## Output

Given the prompt:

> We've just finished the payment processing module for our SaaS app. It handles three things: creating Stripe charges (with idempotency keys), processing refunds (full and partial), and verifying incoming Stripe webhooks using signature validation. There are currently zero tests. The module is in `src/payments/` and uses our Django Ninja API. Can you write a comprehensive test suite for it? We use pytest.

A well-formed agent following this definition would produce:

---

### Pre-flight

**Step 1 — conventions**

```bash
cat CLAUDE.md .claude/CLAUDE.md 2>/dev/null
ls .claude/rules/
```

No existing conventions file found. Proceeding with project defaults.

**Step 2 — existing patterns**

```bash
find src/payments -type f -name "*.py" | sort
find tests -type f -name "*.py" | sort 2>/dev/null || echo "No tests/ directory found"
```

Discovered:

```
src/payments/__init__.py
src/payments/charges.py
src/payments/refunds.py
src/payments/webhooks.py
src/payments/api.py
```

No existing tests. Reading module public API surface:

- `charges.py` — `create_charge(amount, currency, customer_id, idempotency_key)` → `stripe.Charge`
- `refunds.py` — `create_refund(charge_id, amount=None)` → `stripe.Refund`
- `webhooks.py` — `verify_webhook_signature(payload, sig_header, secret)` → `stripe.Event`
- `api.py` — Django Ninja router with `/charges`, `/refunds`, `/webhooks/stripe` endpoints

**Step 3 — classify**

| Type | Approach |
|---|---|
| Unit test coverage | Zero tests exist — write tests for all paths, then implement to pass |

Work is new test coverage with TDD. Vertical slicing per feature.

---

### Slice 1: Charge creation

**RED — write failing tests first**

`tests/payments/test_charges.py`:

```python
import pytest
from unittest.mock import patch, MagicMock
import stripe

from src.payments.charges import create_charge


@pytest.fixture
def stripe_charge_factory():
    def _make(charge_id="ch_test_001", amount=5000, currency="aud", status="succeeded"):
        charge = MagicMock(spec=stripe.Charge)
        charge.id = charge_id
        charge.amount = amount
        charge.currency = currency
        charge.status = status
        return charge
    return _make


@patch("src.payments.charges.stripe.Charge.create")
def test_create_charge_happy_path(mock_create, stripe_charge_factory):
    mock_create.return_value = stripe_charge_factory()
    result = create_charge(5000, "aud", "cus_123", idempotency_key="idem_001")
    assert result.status == "succeeded"


@patch("src.payments.charges.stripe.Charge.create")
def test_create_charge_same_idempotency_key_returns_same_charge(mock_create, stripe_charge_factory):
    charge = stripe_charge_factory(charge_id="ch_idempotent")
    mock_create.return_value = charge
    result1 = create_charge(5000, "aud", "cus_123", idempotency_key="idem_dup")
    result2 = create_charge(5000, "aud", "cus_123", idempotency_key="idem_dup")
    assert result1.id == result2.id


@patch("src.payments.charges.stripe.Charge.create")
def test_create_charge_duplicate_key_different_amount_raises(mock_create):
    mock_create.side_effect = stripe.error.IdempotencyError(
        "Keys for idempotent requests can only be used with the same parameters",
        idempotency_key="idem_conflict",
    )
    with pytest.raises(stripe.error.IdempotencyError):
        create_charge(9999, "aud", "cus_123", idempotency_key="idem_conflict")


@patch("src.payments.charges.stripe.Charge.create")
def test_create_charge_expired_card_raises(mock_create):
    mock_create.side_effect = stripe.error.CardError(
        "Your card has expired.", param="exp_month", code="expired_card"
    )
    with pytest.raises(stripe.error.CardError):
        create_charge(5000, "aud", "cus_expired", idempotency_key="idem_002")


@patch("src.payments.charges.stripe.Charge.create")
def test_create_charge_network_failure_raises(mock_create):
    mock_create.side_effect = stripe.error.APIConnectionError("Network error")
    with pytest.raises(stripe.error.APIConnectionError):
        create_charge(5000, "aud", "cus_123", idempotency_key="idem_003")


def test_create_charge_negative_amount_raises():
    with pytest.raises(ValueError, match="amount must be positive"):
        create_charge(-100, "aud", "cus_123", idempotency_key="idem_004")
```

**Run RED:**

```bash
pytest tests/payments/test_charges.py -v
```

```
FAILED tests/payments/test_charges.py::test_create_charge_happy_path - ImportError: cannot import name 'create_charge'
...
6 failed, 0 passed
```

Exit code: `1` — confirmed RED.

**GREEN — minimum implementation**

`src/payments/charges.py`:

```python
import stripe


def create_charge(amount: int, currency: str, customer_id: str, idempotency_key: str):
    if amount <= 0:
        raise ValueError("amount must be positive")
    return stripe.Charge.create(
        amount=amount,
        currency=currency,
        customer=customer_id,
        idempotency_key=idempotency_key,
    )
```

**Run GREEN:**

```bash
pytest tests/payments/test_charges.py -v
```

```
PASSED tests/payments/test_charges.py::test_create_charge_happy_path
PASSED tests/payments/test_charges.py::test_create_charge_same_idempotency_key_returns_same_charge
PASSED tests/payments/test_charges.py::test_create_charge_duplicate_key_different_amount_raises
PASSED tests/payments/test_charges.py::test_create_charge_expired_card_raises
PASSED tests/payments/test_charges.py::test_create_charge_network_failure_raises
PASSED tests/payments/test_charges.py::test_create_charge_negative_amount_raises
6 passed in 0.18s
```

Exit code: `0` — confirmed GREEN.

---

### Slice 2: Refunds

**RED**

`tests/payments/test_refunds.py`:

```python
import pytest
from unittest.mock import patch, MagicMock
import stripe

from src.payments.refunds import create_refund


@pytest.fixture
def stripe_refund_factory():
    def _make(refund_id="re_test_001", amount=5000, status="succeeded"):
        refund = MagicMock(spec=stripe.Refund)
        refund.id = refund_id
        refund.amount = amount
        refund.status = status
        return refund
    return _make


@patch("src.payments.refunds.stripe.Refund.create")
def test_full_refund_succeeds(mock_create, stripe_refund_factory):
    mock_create.return_value = stripe_refund_factory(amount=5000)
    result = create_refund("ch_test_001", amount=5000)
    assert result.status == "succeeded"


@patch("src.payments.refunds.stripe.Refund.create")
def test_partial_refund_succeeds(mock_create, stripe_refund_factory):
    mock_create.return_value = stripe_refund_factory(amount=2000)
    result = create_refund("ch_test_001", amount=2000)
    assert result.amount == 2000


@patch("src.payments.refunds.stripe.Refund.create")
def test_over_refund_raises(mock_create):
    mock_create.side_effect = stripe.error.InvalidRequestError(
        "Refund amount exceeds charge amount", param="amount"
    )
    with pytest.raises(stripe.error.InvalidRequestError):
        create_refund("ch_test_001", amount=99999)


def test_negative_refund_amount_raises():
    with pytest.raises(ValueError, match="amount must be positive"):
        create_refund("ch_test_001", amount=-500)


@patch("src.payments.refunds.stripe.Refund.create")
def test_refund_already_refunded_charge_raises(mock_create):
    mock_create.side_effect = stripe.error.InvalidRequestError(
        "Charge ch_already_refunded has already been refunded", param="charge"
    )
    with pytest.raises(stripe.error.InvalidRequestError):
        create_refund("ch_already_refunded", amount=5000)
```

**Run RED:**

```bash
pytest tests/payments/test_refunds.py -v
```

Exit code: `1` — confirmed RED.

**GREEN:**

```bash
pytest tests/payments/test_refunds.py -v
```

```
5 passed in 0.14s
```

Exit code: `0` — confirmed GREEN.

---

### Slice 3: Webhook signature verification

**RED**

`tests/payments/test_webhooks.py`:

```python
import pytest
from unittest.mock import patch, MagicMock
import stripe

from src.payments.webhooks import verify_webhook_signature


VALID_PAYLOAD = b'{"type":"charge.succeeded","data":{}}'
VALID_SIG = "t=1234567890,v1=abc123"
SECRET = "whsec_test_secret"


@pytest.fixture
def stripe_event_factory():
    def _make(event_type="charge.succeeded"):
        event = MagicMock(spec=stripe.Event)
        event.type = event_type
        return event
    return _make


@patch("src.payments.webhooks.stripe.Webhook.construct_event")
def test_valid_signature_returns_event(mock_construct, stripe_event_factory):
    mock_construct.return_value = stripe_event_factory()
    result = verify_webhook_signature(VALID_PAYLOAD, VALID_SIG, SECRET)
    assert result.type == "charge.succeeded"


@patch("src.payments.webhooks.stripe.Webhook.construct_event")
def test_missing_signature_header_raises(mock_construct):
    mock_construct.side_effect = stripe.error.SignatureVerificationError(
        "No signatures found matching the expected signature", sig_header=None
    )
    with pytest.raises(stripe.error.SignatureVerificationError):
        verify_webhook_signature(VALID_PAYLOAD, None, SECRET)


@patch("src.payments.webhooks.stripe.Webhook.construct_event")
def test_tampered_body_invalid_signature_raises(mock_construct):
    mock_construct.side_effect = stripe.error.SignatureVerificationError(
        "No signatures found matching the expected signature", sig_header=VALID_SIG
    )
    with pytest.raises(stripe.error.SignatureVerificationError):
        verify_webhook_signature(b'{"tampered":"true"}', VALID_SIG, SECRET)


@patch("src.payments.webhooks.stripe.Webhook.construct_event")
def test_replayed_timestamp_outside_tolerance_raises(mock_construct):
    # Stripe rejects timestamps older than 300s by default
    mock_construct.side_effect = stripe.error.SignatureVerificationError(
        "Timestamp outside the tolerance zone", sig_header="t=1000000000,v1=stale"
    )
    with pytest.raises(stripe.error.SignatureVerificationError):
        verify_webhook_signature(VALID_PAYLOAD, "t=1000000000,v1=stale", SECRET)


@patch("src.payments.webhooks.stripe.Webhook.construct_event")
def test_signature_bypass_attempt_raises(mock_construct):
    # Adversarial: attacker sends an empty sig header hoping to bypass validation
    mock_construct.side_effect = stripe.error.SignatureVerificationError(
        "No signatures found matching the expected signature", sig_header=""
    )
    with pytest.raises(stripe.error.SignatureVerificationError):
        verify_webhook_signature(VALID_PAYLOAD, "", SECRET)
```

**Run RED:**

```bash
pytest tests/payments/test_webhooks.py -v
```

Exit code: `1` — confirmed RED.

**Run GREEN:**

```bash
pytest tests/payments/test_webhooks.py -v
```

```
5 passed in 0.12s
```

Exit code: `0` — confirmed GREEN.

---

### Full suite run

```bash
pytest tests/payments/ -v
```

```
PASSED tests/payments/test_charges.py::test_create_charge_happy_path
PASSED tests/payments/test_charges.py::test_create_charge_same_idempotency_key_returns_same_charge
PASSED tests/payments/test_charges.py::test_create_charge_duplicate_key_different_amount_raises
PASSED tests/payments/test_charges.py::test_create_charge_expired_card_raises
PASSED tests/payments/test_charges.py::test_create_charge_network_failure_raises
PASSED tests/payments/test_charges.py::test_create_charge_negative_amount_raises
PASSED tests/payments/test_refunds.py::test_full_refund_succeeds
PASSED tests/payments/test_refunds.py::test_partial_refund_succeeds
PASSED tests/payments/test_refunds.py::test_over_refund_raises
PASSED tests/payments/test_refunds.py::test_negative_refund_amount_raises
PASSED tests/payments/test_refunds.py::test_refund_already_refunded_charge_raises
PASSED tests/payments/test_webhooks.py::test_valid_signature_returns_event
PASSED tests/payments/test_webhooks.py::test_missing_signature_header_raises
PASSED tests/payments/test_webhooks.py::test_tampered_body_invalid_signature_raises
PASSED tests/payments/test_webhooks.py::test_replayed_timestamp_outside_tolerance_raises
PASSED tests/payments/test_webhooks.py::test_signature_bypass_attempt_raises
16 passed in 0.41s
```

Exit code: `0`

---

### Evidence

| Test | Command | Exit | Result |
|---|---|---|---|
| test_create_charge_happy_path | `pytest tests/payments/test_charges.py::test_create_charge_happy_path -v` | 0 | PASS |
| test_create_charge_same_idempotency_key_returns_same_charge | `pytest tests/payments/test_charges.py::test_create_charge_same_idempotency_key_returns_same_charge -v` | 0 | PASS |
| test_create_charge_duplicate_key_different_amount_raises | `pytest tests/payments/test_charges.py::test_create_charge_duplicate_key_different_amount_raises -v` | 0 | PASS |
| test_create_charge_expired_card_raises | `pytest tests/payments/test_charges.py::test_create_charge_expired_card_raises -v` | 0 | PASS |
| test_create_charge_network_failure_raises | `pytest tests/payments/test_charges.py::test_create_charge_network_failure_raises -v` | 0 | PASS |
| test_create_charge_negative_amount_raises | `pytest tests/payments/test_charges.py::test_create_charge_negative_amount_raises -v` | 0 | PASS |
| test_full_refund_succeeds | `pytest tests/payments/test_refunds.py::test_full_refund_succeeds -v` | 0 | PASS |
| test_partial_refund_succeeds | `pytest tests/payments/test_refunds.py::test_partial_refund_succeeds -v` | 0 | PASS |
| test_over_refund_raises | `pytest tests/payments/test_refunds.py::test_over_refund_raises -v` | 0 | PASS |
| test_negative_refund_amount_raises | `pytest tests/payments/test_refunds.py::test_negative_refund_amount_raises -v` | 0 | PASS |
| test_refund_already_refunded_charge_raises | `pytest tests/payments/test_refunds.py::test_refund_already_refunded_charge_raises -v` | 0 | PASS |
| test_valid_signature_returns_event | `pytest tests/payments/test_webhooks.py::test_valid_signature_returns_event -v` | 0 | PASS |
| test_missing_signature_header_raises | `pytest tests/payments/test_webhooks.py::test_missing_signature_header_raises -v` | 0 | PASS |
| test_tampered_body_invalid_signature_raises | `pytest tests/payments/test_webhooks.py::test_tampered_body_invalid_signature_raises -v` | 0 | PASS |
| test_replayed_timestamp_outside_tolerance_raises | `pytest tests/payments/test_webhooks.py::test_replayed_timestamp_outside_tolerance_raises -v` | 0 | PASS |
| test_signature_bypass_attempt_raises | `pytest tests/payments/test_webhooks.py::test_signature_bypass_attempt_raises -v` | 0 | PASS |

### Quality Score

| Dimension | Score | Evidence |
|---|---|---|
| Security | 100 | Adversarial tests: signature bypass, negative amounts, over-refund, replayed timestamps — all asserted as required rejections |
| Correctness | 100 | All branches covered — happy path, edge cases, error paths per slice |
| Performance | 85 | No N+1 or loop concerns in test logic; fixtures reused via factory pattern |
| Maintainability | 90 | Fixture factories used throughout; one assertion per test; tests co-located under `tests/payments/` |
| Test Coverage | 90 | All public API functions covered; integration-level Django Ninja route tests not included (noted below) |
| **Confidence** | **90** | min(100, 100) capped by avg(85, 90, 90) − 10 = 88 → rounded to 90 |

---

### Note

The definition does not mandate HTTP-level integration tests (posting a signed payload to the `/webhooks/stripe` Django Ninja route via test client). Unit tests on `verify_webhook_signature` are present and complete. A route-level integration test would require reading `api.py` and adding a `django_test_client` fixture — this would be natural given the prompt but the definition doesn't guarantee it.

---

## Evaluation

### Criteria

- [x] PASS: Agent reads existing code before writing any tests — Pre-Flight Step 2 mandates reading existing test files, naming conventions, and fixture patterns before any implementation. Step 1 reads CLAUDE.md first.
- [x] PASS: Agent follows TDD Iron Law — a dedicated "TDD Methodology" section mandates RED (write failing test, confirm exit code 1) → GREEN (minimum code, confirm exit code 0) → REFACTOR per slice, with Vertical Slicing prohibiting all-RED-then-all-GREEN.
- [x] PASS: Agent identifies test cases across all required categories — Testing Philosophy covers "test behaviour," edge cases, and error paths; the work classification table separates happy path, edge cases, and error cases as distinct required outputs.
- [x] PASS: Agent runs tests in run mode and reports exact command and exit code — Test Runner Rules state "Always use run mode — never watch mode" with `pytest` named, and Evidence Requirements mandate exact command, exit code, and count. "Tests pass without an exit code is not evidence" stated verbatim.
- [x] PASS: Agent mocks only at external boundaries — Testing Philosophy states "Mock only at external boundaries (HTTP APIs, third-party services). In-memory fakes of your own database are lies." Principles repeat this identically.
- [x] PASS: Agent identifies security-relevant test cases — Pass 3 of four mandatory review passes is a dedicated Security pass covering input validation, injection risks, and auth/authz. Security is a HARD signal (zero blocks approval).
- [x] PASS: Agent produces an evidence table with test name, command, exit code, and result — the Evidence Output Format section specifies exactly this table structure and labels it mandatory.
- [~] PARTIAL: Agent covers both unit tests and integration-style tests for the webhook endpoint — the definition covers unit tests and E2E browser tests (Playwright/Cypress) but does not explicitly model HTTP-level integration tests (posting a signed body to the Django Ninja route via test client) as a mandatory distinct tier within a single task. Scored 0.5.
- [x] PASS: Agent applies one assertion per test — "One assertion per test. When a test fails, you should know exactly what broke without reading the test body" stated in both the Principles and Testing Philosophy sections.

### Output expectations

- [x] PASS: Output groups test cases under all three named module functions — vertical slicing per feature produces three discrete test files mapped to charge creation, refunds, and webhook verification.
- [x] PASS: Output's idempotency tests cover both happy path (same key → same charge) and edge case (same key with different amount → IdempotencyError), with the Stripe idempotency contract asserted.
- [x] PASS: Output's refund tests separate full refund, partial refund, and over-refund attempt as three distinct tests, each with one assertion.
- [x] PASS: Output's webhook signature tests cover valid signature, missing signature header, tampered body (invalid signature), and replayed timestamp, with verbatim `stripe.error.SignatureVerificationError` asserted.
- [x] PASS: Output mocks at the Stripe API boundary only (`stripe.Charge.create`, `stripe.Refund.create`, `stripe.Webhook.construct_event`) — no mocking of internal `payments.charges` or `payments.refunds` classes.
- [x] PASS: Output writes tests in TDD order — RED first (`pytest -v` shows failures with exit code 1) then GREEN (exit code 0), with both commands and exit codes shown as evidence.
- [x] PASS: Output covers security-relevant adversarial tests — signature bypass attempts, negative refund amounts, refund of already-refunded charge, and charge with negative amount all present as required rejections.
- [x] PASS: Output's evidence table has columns for test name, exact command, exit code, and PASS/FAIL, listing every test individually.
- [x] PASS: Output uses pytest fixtures and factories (`stripe_charge_factory`, `stripe_refund_factory`, `stripe_event_factory`) — no inline dict construction repeated across tests.
- [~] PARTIAL: Output covers integration-style tests for the webhook endpoint (POSTing a signed body to the Django Ninja route) separate from unit tests — not produced. The definition does not mandate this tier. Scored 0.5.

## Notes

Both partial scores share the same root gap: the definition explicitly addresses unit tests and E2E browser-based tests (Playwright/Cypress) but does not name HTTP-level integration tests as a mandatory tier within a test generation task. The agent would plausibly produce them given the explicit prompt — the definition does not guarantee it.

Security coverage is strong. The four mandatory review passes, hard-signal gate, and collaboration model with the Security Engineer role create a robust process obligation that surfaces signature bypass, negative-amount, and over-refund adversarial cases without needing payment-domain examples in the definition.

The fixture factory pattern is well-specified ("Factory functions for test data. No inline object literals scattered across tests") and produces clean, reusable test infrastructure without prompting.
