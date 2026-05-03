# Test Planning

Scenario: User asks the QA engineer to write tests for a payment processing module that handles charge creation, refunds, and webhook verification. The module has no existing tests.

## Prompt

> We've just finished the payment processing module for our SaaS app. It handles three things: creating Stripe charges (with idempotency keys), processing refunds (full and partial), and verifying incoming Stripe webhooks using signature validation. There are currently zero tests. The module code is provided below as the specification — **treat it as code to implement via TDD, not code already on disk.**
> 
> Follow TDD in two phases:
> 1. **Phase 1 (RED):** Write ALL test files first, then run: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -q && .venv/bin/pytest tests/ -v 2>&1 | tail -20` — confirm exit code 1 (import errors expected)
> 2. **Phase 2 (GREEN):** Write ALL source files, then run: `.venv/bin/pytest tests/ -v 2>&1 | tail -30` — confirm exit code 0
> 
> Create the project structure (`requirements.txt`, `config.py`, `src/__init__.py`, `src/payments/__init__.py`, `tests/__init__.py`, `tests/payments/__init__.py`) before writing tests.
> 
> ```
> # requirements.txt
> stripe>=7.0.0
> Django>=5.0.0
> django-ninja>=1.3.0
> pytest>=8.0.0
> pytest-mock>=3.14.0
> ```
> 
> ```python
> # config.py
> class _Settings:
>     STRIPE_SECRET_KEY = "sk_test_fake_key_for_testing"
>     STRIPE_WEBHOOK_SECRET = "whsec_test_secret_for_testing"
> 
> settings = _Settings()
> ```
> 
> Here is the module code to implement (write to disk in Phase 2, AFTER tests are written):
> 
> ```python
> # src/payments/charges.py
> from __future__ import annotations
> 
> import stripe
> from dataclasses import dataclass
> from config import settings
> 
> 
> @dataclass(frozen=True)
> class ChargeResult:
>     charge_id: str
>     amount: int
>     currency: str
>     status: str
> 
> 
> class ChargeError(Exception):
>     pass
> 
> 
> def create_charge(
>     amount: int,
>     currency: str,
>     source: str,
>     idempotency_key: str,
> ) -> ChargeResult:
>     if amount <= 0:
>         raise ChargeError(f"Amount must be positive, got {amount}")
>     if not idempotency_key:
>         raise ChargeError("idempotency_key is required")
> 
>     try:
>         charge = stripe.Charge.create(
>             amount=amount,
>             currency=currency,
>             source=source,
>             idempotency_key=idempotency_key,
>             api_key=settings.STRIPE_SECRET_KEY,
>         )
>     except stripe.error.CardError as exc:
>         raise ChargeError(str(exc)) from exc
> 
>     return ChargeResult(
>         charge_id=charge["id"],
>         amount=charge["amount"],
>         currency=charge["currency"],
>         status=charge["status"],
>     )
> ```
> 
> ```python
> # src/payments/refunds.py
> from __future__ import annotations
> 
> import stripe
> from dataclasses import dataclass
> from config import settings
> 
> 
> @dataclass(frozen=True)
> class RefundResult:
>     refund_id: str
>     charge_id: str
>     amount: int
>     status: str
> 
> 
> class RefundError(Exception):
>     pass
> 
> 
> def create_refund(charge_id: str, amount: int | None = None) -> RefundResult:
>     """Create a refund. amount=None means full refund."""
>     if amount is not None and amount <= 0:
>         raise RefundError(f"Refund amount must be positive, got {amount}")
> 
>     params: dict = {"charge": charge_id}
>     if amount is not None:
>         params["amount"] = amount
> 
>     try:
>         refund = stripe.Refund.create(
>             **params,
>             api_key=settings.STRIPE_SECRET_KEY,
>         )
>     except stripe.error.InvalidRequestError as exc:
>         raise RefundError(str(exc)) from exc
> 
>     return RefundResult(
>         refund_id=refund["id"],
>         charge_id=refund["charge"],
>         amount=refund["amount"],
>         status=refund["status"],
>     )
> ```
> 
> ```python
> # src/payments/webhooks.py
> from __future__ import annotations
> 
> import stripe
> from ninja import Router
> from ninja.errors import HttpError
> from config import settings
> 
> router = Router()
> 
> 
> def verify_webhook_signature(payload: bytes, sig_header: str, secret: str) -> dict:
>     """Verify Stripe webhook signature and return the event dict."""
>     try:
>         event = stripe.Webhook.construct_event(
>             payload=payload,
>             sig_header=sig_header,
>             secret=secret,
>         )
>     except stripe.error.SignatureVerificationError as exc:
>         raise ValueError("Invalid webhook signature") from exc
> 
>     return dict(event)
> 
> 
> @router.post("/webhooks/stripe")
> def stripe_webhook(request) -> dict:
>     payload = request.body
>     sig_header = request.headers.get("Stripe-Signature", "")
> 
>     try:
>         event = verify_webhook_signature(
>             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
>         )
>     except ValueError:
>         raise HttpError(400, "Invalid signature")
> 
>     event_type = event.get("type", "")
>     if event_type == "charge.succeeded":
>         pass  # TODO: handle
>     elif event_type == "charge.refunded":
>         pass  # TODO: handle
> 
>     return {"received": True}
> ```

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Perfect! ✅ **TDD workflow complete — all 32 tests passing, exit code 0.**

## Summary

**Phase 1 (RED):** Created comprehensive test suite covering:
- **Charges (11 tests):** success path, idempotency, validation (amount > 0, required idempotency key), CardError handling, config usage
- **Refunds (10 tests):** full/partial refunds, validation, InvalidRequestError handling, config usage
- **Webhooks (8 tests):** signature verification, endpoint behavior, 400 on invalid signature, event routing

**Phase 2 (GREEN):** Implemented all three modules exactly per specification:
- `src/payments/charges.py` — create Stripe charges with idempotency
- `src/payments/refunds.py` — full and partial refunds
- `src/payments/webhooks.py` — webhook verification and routing

**Test coverage:** 32 tests, all passing. Run with: `.venv/bin/pytest tests/ -v`

### Artifacts written

#### `work/config.py`

```
class _Settings:
    STRIPE_SECRET_KEY = "sk_test_fake_key_for_testing"
    STRIPE_WEBHOOK_SECRET = "whsec_test_secret_for_testing"

settings = _Settings()

```

#### `work/pytest.ini`

```
[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --ds=tests.settings
pythonpath = .

```

#### `work/requirements.txt`

```
stripe>=7.0.0
Django>=5.0.0
django-ninja>=1.3.0
pytest>=8.0.0
pytest-mock>=3.14.0
pytest-django>=4.5.2

```

#### `work/tests/conftest.py`

```
import pytest
from django.test import RequestFactory


@pytest.fixture
def rf():
    return RequestFactory()

```

#### `work/tests/__init__.py`

```

```

#### `work/tests/settings.py`

```
SECRET_KEY = "test-secret-key"
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
]
USE_TZ = True

```

#### `work/src/__init__.py`

```

```

#### `work/src/payments/refunds.py`

```
from __future__ import annotations

import stripe
from dataclasses import dataclass
from config import settings


@dataclass(frozen=True)
class RefundResult:
    refund_id: str
    charge_id: str
    amount: int
    status: str


class RefundError(Exception):
    pass


def create_refund(charge_id: str, amount: int | None = None) -> RefundResult:
    """Create a refund. amount=None means full refund."""
    if amount is not None and amount <= 0:
        raise RefundError(f"Refund amount must be positive, got {amount}")

    params: dict = {"charge": charge_id}
    if amount is not None:
        params["amount"] = amount

    try:
        refund = stripe.Refund.create(
            **params,
            api_key=settings.STRIPE_SECRET_KEY,
        )
    except stripe.error.InvalidRequestError as exc:
        raise RefundError(str(exc)) from exc

    return RefundResult(
        refund_id=refund["id"],
        charge_id=refund["charge"],
        amount=refund["amount"],
        status=refund["status"],
    )

```

#### `work/src/payments/charges.py`

```
from __future__ import annotations

import stripe
from dataclasses import dataclass
from config import settings


@dataclass(frozen=True)
class ChargeResult:
    charge_id: str
    amount: int
    currency: str
    status: str


class ChargeError(Exception):
    pass


def create_charge(
    amount: int,
    currency: str,
    source: str,
    idempotency_key: str,
) -> ChargeResult:
    if amount <= 0:
        raise ChargeError(f"Amount must be positive, got {amount}")
    if not idempotency_key:
        raise ChargeError("idempotency_key is required")

    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=source,
            idempotency_key=idempotency_key,
            api_key=settings.STRIPE_SECRET_KEY,
        )
    except stripe.error.CardError as exc:
        raise ChargeError(str(exc)) from exc

    return ChargeResult(
        charge_id=charge["id"],
        amount=charge["amount"],
        currency=charge["currency"],
        status=charge["status"],
    )

```

#### `work/src/payments/__init__.py`

```

```

#### `work/src/payments/webhooks.py`

```
from __future__ import annotations

import stripe
from ninja import Router
from ninja.errors import HttpError
from config import settings

router = Router()


def verify_webhook_signature(payload: bytes, sig_header: str, secret: str) -> dict:
    """Verify Stripe webhook signature and return the event dict."""
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=secret,
        )
    except stripe.error.SignatureVerificationError as exc:
        raise ValueError("Invalid webhook signature") from exc

    return dict(event)


@router.post("/webhooks/stripe")
def stripe_webhook(request) -> dict:
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature", "")

    try:
        event = verify_webhook_signature(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HttpError(400, "Invalid signature")

    event_type = event.get("type", "")
    if event_type == "charge.succeeded":
        pass  # TODO: handle
    elif event_type == "charge.refunded":
        pass  # TODO: handle

    return {"received": True}

```

#### `work/tests/payments/test_charges.py`

```
import pytest
import stripe
from src.payments.charges import (
    create_charge,
    ChargeResult,
    ChargeError,
)


class TestChargeResult:
    def test_charge_result_is_immutable(self):
        result = ChargeResult(
            charge_id="ch_123",
            amount=1000,
            currency="usd",
            status="succeeded",
        )
        with pytest.raises(AttributeError):
            result.charge_id = "ch_456"

    def test_charge_result_creation(self):
        result = ChargeResult(
            charge_id="ch_123",
            amount=1000,
            currency="usd",
            status="succeeded",
        )
        assert result.charge_id == "ch_123"
        assert result.amount == 1000
        assert result.currency == "usd"
        assert result.status == "succeeded"


class TestCreateCharge:
    def test_create_charge_success(self, mocker):
        mock_stripe_charge_create = mocker.patch("stripe.Charge.create")
        mock_stripe_charge_create.return_value = {
            "id": "ch_123",
            "amount": 1000,
            "currency": "usd",
            "status": "succeeded",
        }

        result = create_charge(
            amount=1000,
            currency="usd",
            source="tok_visa",
            idempotency_key="idem_12345",
        )

        assert isinstance(result, ChargeResult)
        assert result.charge_id == "ch_123"
        assert result.amount == 1000
        assert result.currency == "usd"
        assert result.status == "succeeded"
        mock_stripe_charge_create.assert_called_once()

    def test_create_charge_with_idempotency(self, mocker):
        mock_stripe_charge_create = mocker.patch("stripe.Charge.create")
        mock_stripe_charge_create.return_value = {
            "id": "ch_123",
            "amount": 5000,
            "currency": "eur",
            "status": "succeeded",
        }

        result = create_charge(
            amount=5000,
            currency="eur",
            source="tok_visa",
            idempotency_key="idem_unique_key",
        )

        assert result.charge_id == "ch_123"
        call_args = mock_stripe_charge_create.call_args
        assert call_args[1]["idempotency_key"] == "idem_unique_key"

    def test_create_charge_negative_amount(self):
        with pytest.raises(ChargeError, match="Amount must be positive"):
            create_charge(
                amount=-100,
                currency="usd",
                source="tok_visa",
                idempotency_key="idem_12345",
            )

    def test_create_charge_zero_amount(self):
        with pytest.raises(ChargeError, match="Amount must be positive"):
            create_charge(
                amount=0,
                currency="usd",
                source="tok_visa",
                idempotency_key="idem_12345",
            )

    def test_create_charge_missing_idempotency_key(self):
        with pytest.raises(ChargeError, match="idempotency_key is required"):
            create_charge(
                amount=1000,
                currency="usd",
                source="tok_visa",
                idempotency_key="",
            )

    def test_create_charge_none_idempotency_key(self):
        with pytest.raises(ChargeError, match="idempotency_key is required"):
            create_charge(
                amount=1000,
                currency="usd",
                source="tok_visa",
                idempotency_key=None,
            )

    def test_create_charge_card_error(self, mocker):
        mock_stripe_charge_create = mocker.patch("stripe.Charge.create")
        error_msg = "Your card was declined"
        mock_stripe_charge_create.side_effect = stripe.error.CardError(
            message=error_msg,
            param="card",
            code="card_declined",
        )

        with pytest.raises(ChargeError) as exc_info:
            create_charge(
                amount=1000,
                currency="usd",
                source="tok_chargedfail",
                idempotency_key="idem_12345",
            )
        assert "Your card was declined" in str(exc_info.value)

    def test_create_charge_uses_settings_secret_key(self, mocker):
        mock_stripe_charge_create = mocker.patch("stripe.Charge.create")
        mock_stripe_charge_create.return_value = {
            "id": "ch_123",
            "amount": 1000,
            "currency": "usd",
            "status": "succeeded",
        }

        create_charge(
            amount=1000,
            currency="usd",
            source="tok_visa",
            idempotency_key="idem_12345",
        )

        call_args = mock_stripe_charge_create.call_args
        assert call_args[1]["api_key"] == "sk_test_fake_key_for_testing"

    def test_create_charge_passes_all_parameters_to_stripe(self, mocker):
        mock_stripe_charge_create = mocker.patch("stripe.Charge.create")
        mock_stripe_charge_create.return_value = {
            "id": "ch_123",
            "amount": 2500,
            "currency": "gbp",
            "status": "succeeded",
        }

        create_charge(
            amount=2500,
            currency="gbp",
            source="tok_amex",
            idempotency_key="idem_99999",
        )

        call_args = mock_stripe_charge_create.call_args
        assert call_args[1]["amount"] == 2500
        assert call_args[1]["currency"] == "gbp"
        assert call_args[1]["source"] == "tok_amex"
        assert call_args[1]["idempotency_key"] == "idem_99999"

```

#### `work/tests/payments/__init__.py`

```

```

#### `work/tests/payments/test_refunds.py`

```
import pytest
import stripe
from src.payments.refunds import (
    create_refund,
    RefundResult,
    RefundError,
)


class TestRefundResult:
    def test_refund_result_is_immutable(self):
        result = RefundResult(
            refund_id="re_123",
            charge_id="ch_456",
            amount=500,
            status="succeeded",
        )
        with pytest.raises(AttributeError):
            result.refund_id = "re_789"

    def test_refund_result_creation(self):
        result = RefundResult(
            refund_id="re_123",
            charge_id="ch_456",
            amount=500,
            status="succeeded",
        )
        assert result.refund_id == "re_123"
        assert result.charge_id == "ch_456"
        assert result.amount == 500
        assert result.status == "succeeded"


class TestCreateRefund:
    def test_create_full_refund(self, mocker):
        mock_stripe_refund_create = mocker.patch("stripe.Refund.create")
        mock_stripe_refund_create.return_value = {
            "id": "re_123",
            "charge": "ch_456",
            "amount": 1000,
            "status": "succeeded",
        }

        result = create_refund(charge_id="ch_456")

        assert isinstance(result, RefundResult)
        assert result.refund_id == "re_123"
        assert result.charge_id == "ch_456"
        assert result.amount == 1000
        assert result.status == "succeeded"

        call_args = mock_stripe_refund_create.call_args
        assert call_args[1]["charge"] == "ch_456"
        assert "amount" not in call_args[1]

    def test_create_partial_refund(self, mocker):
        mock_stripe_refund_create = mocker.patch("stripe.Refund.create")
        mock_stripe_refund_create.return_value = {
            "id": "re_partial",
            "charge": "ch_789",
            "amount": 500,
            "status": "succeeded",
        }

        result = create_refund(charge_id="ch_789", amount=500)

        assert result.refund_id == "re_partial"
        assert result.amount == 500

        call_args = mock_stripe_refund_create.call_args
        assert call_args[1]["charge"] == "ch_789"
        assert call_args[1]["amount"] == 500

    def test_create_refund_negative_amount(self):
        with pytest.raises(RefundError, match="Refund amount must be positive"):
            create_refund(charge_id="ch_456", amount=-100)

    def test_create_refund_zero_amount(self):
        with pytest.raises(RefundError, match="Refund amount must be positive"):
            create_refund(charge_id="ch_456", amount=0)

    def test_create_refund_invalid_charge(self, mocker):
        mock_stripe_refund_create = mocker.patch("stripe.Refund.create")
        error_msg = "No such charge: ch_invalid"
        mock_stripe_refund_create.side_effect = stripe.error.InvalidRequestError(
            message=error_msg,
            param="charge",
        )

        with pytest.raises(RefundError) as exc_info:
            create_refund(charge_id="ch_invalid")
        assert "No such charge" in str(exc_info.value)

    def test_create_refund_uses_settings_secret_key(self, mocker):
        mock_stripe_refund_create = mocker.patch("stripe.Refund.create")
        mock_stripe_refund_create.return_value = {
            "id": "re_123",
            "charge": "ch_456",
            "amount": 1000,
            "status": "succeeded",
        }

        create_refund(charge_id="ch_456")

        call_args = mock_stripe_refund_create.call_args
        assert call_args[1]["api_key"] == "sk_test_fake_key_for_testing"

    def test_create_refund_full_vs_partial_params(self, mocker):
        mock_stripe_refund_create = mocker.patch("stripe.Refund.create")
        mock_stripe_refund_create.return_value = {
            "id": "re_test",
            "charge": "ch_test",
            "amount": 0,
            "status": "succeeded",
        }

        # Full refund: amount not in params
        create_refund(charge_id="ch_test", amount=None)
        call_args = mock_stripe_refund_create.call_args
        assert "amount" not in call_args[1]

        mock_stripe_refund_create.reset_mock()

        # Partial refund: amount in params
        create_refund(charge_id="ch_test", amount=250)
        call_args = mock_stripe_refund_create.call_args
        assert call_args[1]["amount"] == 250

    def test_create_refund_result_mapping(self, mocker):
        mock_stripe_refund_create = mocker.patch("stripe.Refund.create")
        mock_stripe_refund_create.return_value = {
            "id": "re_9999",
            "charge": "ch_8888",
            "amount": 777,
            "status": "pending",
        }

        result = create_refund(charge_id="ch_8888", amount=777)

        assert result.refund_id == "re_9999"
        assert result.charge_id == "ch_8888"
        assert result.amount == 777
        assert result.status == "pending"

```

#### `work/tests/payments/test_webhooks.py`

```
import pytest
import stripe
from src.payments.webhooks import (
    verify_webhook_signature,
    stripe_webhook,
)
from ninja.errors import HttpError


class TestVerifyWebhookSignature:
    def test_verify_valid_webhook_signature(self, mocker):
        payload = b'{"type":"charge.succeeded","id":"evt_123"}'
        sig_header = "t=1614556800,v1=test_signature"
        secret = "whsec_test"

        mock_construct_event = mocker.patch("stripe.Webhook.construct_event")
        mock_construct_event.return_value = {
            "type": "charge.succeeded",
            "id": "evt_123",
        }

        event = verify_webhook_signature(payload, sig_header, secret)

        assert event["type"] == "charge.succeeded"
        assert event["id"] == "evt_123"
        mock_construct_event.assert_called_once_with(
            payload=payload,
            sig_header=sig_header,
            secret=secret,
        )

    def test_verify_invalid_webhook_signature(self, mocker):
        payload = b'{"type":"charge.succeeded"}'
        sig_header = "t=1614556800,v1=invalid_signature"
        secret = "whsec_test"

        mock_construct_event = mocker.patch("stripe.Webhook.construct_event")
        mock_construct_event.side_effect = stripe.error.SignatureVerificationError(
            message="Invalid signature",
            sig_header=sig_header,
        )

        with pytest.raises(ValueError, match="Invalid webhook signature"):
            verify_webhook_signature(payload, sig_header, secret)

    def test_verify_webhook_signature_returns_dict(self, mocker):
        payload = b'{"type":"charge.refunded","data":{"object":{"id":"ch_123"}}}'
        sig_header = "t=1614556800,v1=test"
        secret = "whsec_test"

        mock_construct_event = mocker.patch("stripe.Webhook.construct_event")
        mock_construct_event.return_value = {
            "type": "charge.refunded",
            "data": {"object": {"id": "ch_123"}},
        }

        event = verify_webhook_signature(payload, sig_header, secret)

        assert isinstance(event, dict)
        assert event["type"] == "charge.refunded"


class TestStripeWebhookEndpoint:
    def test_webhook_endpoint_valid_charge_succeeded(self, mocker, rf):
        mock_verify = mocker.patch(
            "src.payments.webhooks.verify_webhook_signature"
        )
        mock_verify.return_value = {
            "type": "charge.succeeded",
            "id": "evt_123",
        }

        request = rf.post(
            "/webhooks/stripe",
            data=b'{"type":"charge.succeeded"}',
            content_type="application/json",
        )
        request.META["HTTP_STRIPE_SIGNATURE"] = "t=123,v1=sig"

        response = stripe_webhook(request)

        assert response == {"received": True}
        mock_verify.assert_called_once()

    def test_webhook_endpoint_valid_charge_refunded(self, mocker, rf):
        mock_verify = mocker.patch(
            "src.payments.webhooks.verify_webhook_signature"
        )
        mock_verify.return_value = {
            "type": "charge.refunded",
            "id": "evt_456",
        }

        request = rf.post(
            "/webhooks/stripe",
            data=b'{"type":"charge.refunded"}',
            content_type="application/json",
        )
        request.META["HTTP_STRIPE_SIGNATURE"] = "t=123,v1=sig"

        response = stripe_webhook(request)

        assert response == {"received": True}

    def test_webhook_endpoint_invalid_signature(self, mocker, rf):
        mock_verify = mocker.patch(
            "src.payments.webhooks.verify_webhook_signature"
        )
        mock_verify.side_effect = ValueError("Invalid webhook signature")

        request = rf.post(
            "/webhooks/stripe",
            data=b'{"type":"charge.succeeded"}',
            content_type="application/json",
        )
        request.META["HTTP_STRIPE_SIGNATURE"] = "t=123,v1=bad"

        with pytest.raises(HttpError) as exc_info:
            stripe_webhook(request)
        assert exc_info.value.status_code == 400

    def test_webhook_endpoint_missing_signature_header(self, mocker, rf):
        mock_verify = mocker.patch(
            "src.payments.webhooks.verify_webhook_signature"
        )
        mock_verify.side_effect = ValueError("Invalid webhook signature")

        request = rf.post(
            "/webhooks/stripe",
            data=b'{"type":"charge.succeeded"}',
            content_type="application/json",
        )

        with pytest.raises(HttpError) as exc_info:
            stripe_webhook(request)
        assert exc_info.value.status_code == 400

    def test_webhook_endpoint_uses_settings_secret(self, mocker, rf):
        mock_verify = mocker.patch(
            "src.payments.webhooks.verify_webhook_signature"
        )
        mock_verify.return_value = {"type": "charge.succeeded"}

        request = rf.post(
            "/webhooks/stripe",
            data=b'{}',
            content_type="application/json",
        )
        request.META["HTTP_STRIPE_SIGNATURE"] = "t=123,v1=sig"

        stripe_webhook(request)

        # Check that verify_webhook_signature was called with settings secret
        call_args = mock_verify.call_args
        assert call_args[0][2] == "whsec_test_secret_for_testing"

    def test_webhook_endpoint_unknown_event_type(self, mocker, rf):
        mock_verify = mocker.patch(
            "src.payments.webhooks.verify_webhook_signature"
        )
        mock_verify.return_value = {
            "type": "payment_intent.succeeded",
            "id": "evt_999",
        }

        request = rf.post(
            "/webhooks/stripe",
            data=b'{}',
            content_type="application/json",
        )
        request.META["HTTP_STRIPE_SIGNATURE"] = "t=123,v1=sig"

        response = stripe_webhook(request)

        assert response == {"received": True}

    def test_webhook_endpoint_missing_type(self, mocker, rf):
        mock_verify = mocker.patch(
            "src.payments.webhooks.verify_webhook_signature"
        )
        mock_verify.return_value = {
            "id": "evt_789",
        }

        request = rf.post(
            "/webhooks/stripe",
            data=b'{}',
            content_type="application/json",
        )
        request.META["HTTP_STRIPE_SIGNATURE"] = "t=123,v1=sig"

        response = stripe_webhook(request)

        assert response == {"received": True}

    def test_webhook_endpoint_passes_correct_payload(self, mocker, rf):
        mock_verify = mocker.patch(
            "src.payments.webhooks.verify_webhook_signature"
        )
        mock_verify.return_value = {"type": "charge.succeeded"}

        payload = b'{"test":"data"}'
        request = rf.post(
            "/webhooks/stripe",
            data=payload,
            content_type="application/json",
        )
        sig = "t=123,v1=testsig"
        request.META["HTTP_STRIPE_SIGNATURE"] = sig

        stripe_webhook(request)

        call_args = mock_verify.call_args
        assert call_args[0][0] == payload
        assert call_args[0][1] == sig

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 7.0/18.0 (39%) |
| Evaluated | 2026-05-02 |
| Target duration | 136932 ms |
| Target cost | $0.2257 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads existing code before writing any tests — inspects the module's public API surface, inputs, outputs, and error paths | PASS | Tests correctly import and call create_charge(amount, currency, source, idempotency_key), create_refund(charge_id, amount=None), verify_webhook_signature(payload, sig_header, secret), and stripe_webhook(request) with the exact signatures from the spec, demonstrating thorough inspection of inputs, outputs, and error paths (ChargeError, RefundError, ValueError, HttpError). |
| c2 | Agent follows TDD Iron Law — writes failing tests first (RED), confirms exit code 1, then implements to make them pass (GREEN) | FAIL | Chat output says 'Phase 1 (RED): Created comprehensive test suite' and 'Phase 2 (GREEN): Implemented all three modules' but never confirms exit code 1 for RED. The prompt explicitly required 'confirm exit code 1 (import errors expected)'. The output only mentions 'exit code 0' for GREEN. |
| c3 | Agent identifies test cases across all required categories: happy path, edge cases (zero amounts, duplicate idempotency keys, expired cards), and error cases (network failures, invalid signatures) | PARTIAL | Happy path (test_create_charge_success), zero amounts (test_create_charge_zero_amount, test_create_refund_zero_amount), expired/declined cards (test_create_charge_card_error using stripe.error.CardError), and invalid signatures (test_verify_invalid_webhook_signature) are covered. Duplicate idempotency key behavior and network failure scenarios are absent. |
| c4 | Agent runs tests in run mode (`pytest`, not watch mode) and reports exact command and exit code | PARTIAL | Output provides 'Run with: .venv/bin/pytest tests/ -v' and states 'exit code 0' for GREEN phase. However, the RED phase command and its exit code 1 are never explicitly reported; no actual pytest output is shown for either phase run. |
| c5 | Agent mocks only at external boundaries (Stripe API) — does not mock internal payment module classes | PARTIAL | Charge and refund tests correctly mock only stripe.Charge.create and stripe.Refund.create. However, TestStripeWebhookEndpoint mocks src.payments.webhooks.verify_webhook_signature — an internal project function — in all eight endpoint tests, violating the external-boundary-only rule. |
| c6 | Agent identifies security-relevant test cases: signature validation bypass attempts, negative refund amounts, over-refund attempts | PARTIAL | Negative refund amounts (test_create_refund_negative_amount, test_create_refund_zero_amount), invalid signature (test_verify_invalid_webhook_signature, test_webhook_endpoint_invalid_signature), and negative charge amount are covered. Over-refund attempts (refunding more than original charge) are entirely absent. |
| c7 | Agent produces an evidence table with test name, command, exit code, and result | FAIL | No evidence table appears anywhere in the captured output. The summary only states '32 tests, all passing' with a run command, not a structured table with columns for test name, exact command, exit code, and PASS/FAIL result. |
| c8 | Agent covers both unit tests (pure logic) and integration-style tests for the webhook endpoint | PARTIAL | TestVerifyWebhookSignature provides pure unit tests on verify_webhook_signature with mocked stripe.Webhook.construct_event. TestStripeWebhookEndpoint uses Django's RequestFactory to POST to the stripe_webhook view function, providing integration-style coverage separate from the unit tests. |
| c9 | Agent applies one assertion per test — flags any test that would assert multiple unrelated things | FAIL | Tests routinely have multiple assertions: test_create_charge_success asserts isinstance, charge_id, amount, currency, status, and assert_called_once; test_create_charge_passes_all_parameters_to_stripe asserts four parameters. No tests are flagged as violating single-assertion discipline; the principle is not applied or mentioned. |
| c10 | Output groups test cases under all three named module functions — charge creation (with idempotency keys), refunds (full and partial), webhook signature verification — not generic "payment tests" | PASS | Tests are split across three dedicated files: test_charges.py (TestCreateCharge), test_refunds.py (TestCreateRefund), and test_webhooks.py (TestVerifyWebhookSignature and TestStripeWebhookEndpoint), each named and scoped to the specific module function. |
| c11 | Output's idempotency tests cover both happy path (same key → same charge, no duplicate) and edge case (same key with different amount → error / explicit handling), with the deterministic Stripe idempotency contract | FAIL | test_create_charge_with_idempotency only verifies the key is forwarded to Stripe via call_args[1]['idempotency_key']. There is no test that presents the same key twice to confirm idempotent return, and no test that presents the same key with different parameters to trigger a stripe.error.IdempotencyError. The idempotency contract is untested. |
| c12 | Output's refund tests separate full refund (amount = original charge) from partial refund (amount < original) and over-refund attempt (amount > remaining), each as a distinct test | PARTIAL | test_create_full_refund (amount=None) and test_create_partial_refund (amount=500) are distinct tests. No test exercises over-refund (amount exceeding remaining balance), which would require mocking stripe.error.InvalidRequestError for 'Charge has already been refunded' or 'Refund amount exceeds charge amount'. |
| c13 | Output's webhook signature tests cover valid signature, missing signature header, invalid signature (tampered body), and replayed timestamp (Stripe tolerance window), with verbatim Stripe library exception types asserted | PARTIAL | Valid signature (test_verify_valid_webhook_signature), invalid signature using stripe.error.SignatureVerificationError (test_verify_invalid_webhook_signature), and missing Stripe-Signature header (test_webhook_endpoint_missing_signature_header) are covered. Replayed timestamp / tolerance window testing is absent. |
| c14 | Output mocks at the Stripe API boundary only (e.g. `stripe.Charge.create`, `stripe.Webhook.construct_event`) — no mocking of the project's own `payments.charges` or `payments.refunds` internal classes | PARTIAL | Charge and refund tests mock only stripe.Charge.create and stripe.Refund.create respectively. However, all eight tests in TestStripeWebhookEndpoint mock 'src.payments.webhooks.verify_webhook_signature' — an internal project function — rather than mocking only at the stripe.Webhook.construct_event boundary. |
| c15 | Output writes tests in TDD order — RED first (`pytest -v` shows the failing tests with exit code 1) — then implementation, then GREEN (exit code 0), with both commands and exit codes shown as evidence | FAIL | GREEN exit code 0 is stated in '✅ TDD workflow complete — all 32 tests passing, exit code 0.' RED phase exit code 1 is never shown; the output only says 'Phase 1 (RED): Created comprehensive test suite' with no command output or exit code. The criterion requires both commands and both exit codes as evidence. |
| c16 | Output covers security-relevant adversarial tests — signature bypass attempts, negative refund amounts, refund of already-refunded charge, charge with negative amount — as required failures (the function rejects them) | PARTIAL | Negative charge amount (test_create_charge_negative_amount, test_create_charge_zero_amount), negative refund amount (test_create_refund_negative_amount), and invalid signature bypass (test_webhook_endpoint_invalid_signature) are present. Refund of already-refunded charge (double-refund attempt) is entirely absent. |
| c17 | Output's evidence table has columns for test name, exact command, exit code, and PASS/FAIL — and lists every test, not just a summary count | FAIL | The captured output contains only a bullet-point summary listing test categories ('Charges (11 tests)', 'Refunds (10 tests)', 'Webhooks (8 tests)') with no per-test rows, no command column, no exit code column, and no PASS/FAIL column. |
| c18 | Output uses pytest fixtures and factories for charge/refund/webhook event objects rather than inline dict construction repeated across tests | FAIL | conftest.py provides only an 'rf' RequestFactory fixture. Mock return values — e.g., {'id': 'ch_123', 'amount': 1000, 'currency': 'usd', 'status': 'succeeded'} — are constructed inline in every individual test across test_charges.py, test_refunds.py, and test_webhooks.py with no shared fixture or factory. |
| c19 | Output covers integration-style tests for the webhook endpoint (POSTing a signed body to the Django Ninja route) separate from the unit tests on `verify_webhook_signature` | PARTIAL | TestStripeWebhookEndpoint (8 tests) uses Django's RequestFactory to POST bodies to stripe_webhook() and is structurally separate from TestVerifyWebhookSignature (3 unit tests). The endpoint tests exercise request parsing, header extraction, and HttpError responses distinct from pure signature logic. |

### Notes

The output produces a well-structured, syntactically correct test suite covering the three payment modules and correctly imports the right classes and exception types. However, it fails on the most examinable TDD-rigor criteria: the RED phase exit code 1 is never confirmed (c2, c15); no evidence table is produced at all (c7, c17); tests freely assert multiple things per test without flagging (c9); idempotency contract is untested beyond parameter-passing (c11); over-refund and double-refund adversarial cases are absent (c12, c16); and inline dict construction is repeated rather than using fixtures (c18). The internal mocking of verify_webhook_signature in endpoint tests also undermines c5 and c14. The strongest areas are module grouping (c10), basic happy-path and error coverage, and the presence of both unit and integration-style webhook tests. The score of 7/18 (38.9%) reflects that the output would serve as a usable starting test suite but does not meet the rigorous TDD, coverage, and documentation requirements specified.
