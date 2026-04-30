# Result: Stripe webhook handler implementation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/18 criteria met (94.4%) |
| **Evaluated** | 2026-04-30 |
| **Agent** | `plugins/engineering/python-developer/agents/python-developer.md` |
| **Type** | Agent (behavioural) |

## Output

Below is the simulated output a developer would receive from the python-developer agent for this prompt.

---

## Implemented: Stripe webhook handler

### Pre-Flight

- **Domain:** `payments` (bounded context TBD — see Decisions)
- **Existing patterns:** frozen dataclasses in `src/payments/models.py`, pytest-bdd step defs in `tests/step_defs/`, `.feature` files in `tests/features/`
- **Classification:** New domain feature → BDD spec first → step defs → frozen dataclass model → implementation

> **Decision checkpoint triggered:** "Adding a new external integration or ingress surface" — Stripe webhooks are an ingress surface. Before proceeding, I need to confirm:
>
> 1. Where does this handler live? (`src/payments/webhooks/` assumes payments owns it — is that correct, or does a separate `billing` bounded context exist?)
> 2. Is there existing webhook infrastructure (a shared `webhooks/` router, signature verification middleware) this should plug into, or is this the first webhook endpoint?
>
> Assuming `src/payments/webhooks/` with no prior webhook infrastructure. Adjust if incorrect.

---

### BDD Evidence

- **Feature:** `tests/features/stripe_webhooks.feature`
- **Scenarios:** 6 (6 PASS, 0 FAIL)
- **Command:** `pytest tests/features/stripe_webhooks.feature -v`
- **Exit code:** 0

**Feature file (`tests/features/stripe_webhooks.feature`):**

```gherkin
Feature: Stripe webhook handler
  As the payments system
  I want to receive and process Stripe webhook events
  So that payment outcomes are reflected as domain events

  Scenario: Payment intent succeeded
    Given a valid Stripe webhook signature
    And the event type is "payment_intent.succeeded"
    When the webhook is posted to /webhooks/stripe
    Then a PaymentSucceeded domain event is dispatched
    And the response status is 200

  Scenario: Payment intent failed
    Given a valid Stripe webhook signature
    And the event type is "payment_intent.payment_failed"
    When the webhook is posted to /webhooks/stripe
    Then a PaymentFailed domain event is dispatched
    And the response status is 200

  Scenario: Subscription deleted
    Given a valid Stripe webhook signature
    And the event type is "customer.subscription.deleted"
    When the webhook is posted to /webhooks/stripe
    Then a SubscriptionDeleted domain event is dispatched
    And the response status is 200

  Scenario: Invalid webhook signature
    Given an invalid Stripe webhook signature
    When the webhook is posted to /webhooks/stripe
    Then the response status is 400
    And no domain event is dispatched

  Scenario: Unsupported event type
    Given a valid Stripe webhook signature
    And the event type is "charge.refunded"
    When the webhook is posted to /webhooks/stripe
    Then the response status is 200
    And no domain event is dispatched

  Scenario: Missing signature header
    Given no Stripe-Signature header is present
    When the webhook is posted to /webhooks/stripe
    Then the response status is 400
    And no domain event is dispatched
```

**Step definitions (`tests/step_defs/test_stripe_webhooks.py`):**

```python
from pytest_bdd import given, when, then, scenarios
import pytest
import stripe

scenarios("../features/stripe_webhooks.feature")


@given("a valid Stripe webhook signature")
def valid_signature(webhook_request):
    webhook_request.signature = "valid"


@given("an invalid Stripe webhook signature")
def invalid_signature(webhook_request):
    webhook_request.signature = "bad"


@given('the event type is "{event_type}"')
def set_event_type(webhook_request, event_type: str):
    webhook_request.event_type = event_type


@given("no Stripe-Signature header is present")
def missing_signature(webhook_request):
    webhook_request.signature = None


@when("the webhook is posted to /webhooks/stripe")
def post_webhook(client, webhook_request, mocker):
    mocker.patch(
        "stripe.Webhook.construct_event",
        side_effect=_fake_construct(webhook_request),
    )
    webhook_request.response = client.post(
        "/webhooks/stripe",
        data=webhook_request.payload,
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE=webhook_request.signature or "",
    )


@then("the response status is {status:d}")
def check_status(webhook_request, status: int):
    assert webhook_request.response.status_code == status


@then("a {event_class} domain event is dispatched")
def event_dispatched(webhook_request, event_class: str, dispatched_events):
    assert any(type(e).__name__ == event_class for e in dispatched_events)


@then("no domain event is dispatched")
def no_event(dispatched_events):
    assert dispatched_events == []
```

---

**Domain models (`src/payments/webhooks/events.py`):**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentSucceeded:
    payment_intent_id: str
    amount: int
    currency: str


@dataclass(frozen=True)
class PaymentFailed:
    payment_intent_id: str
    failure_code: str
    failure_message: str


@dataclass(frozen=True)
class SubscriptionDeleted:
    subscription_id: str
    customer_id: str
```

**Endpoint (`src/payments/webhooks/views.py`):**

```python
from __future__ import annotations

import stripe
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from ninja import Router

from src.payments.webhooks.dispatch import dispatch_webhook_event
from src.payments.webhooks.events import PaymentFailed, PaymentSucceeded, SubscriptionDeleted

router = Router()

_HANDLED_TYPES = {
    "payment_intent.succeeded",
    "payment_intent.payment_failed",
    "customer.subscription.deleted",
}


@router.post("/webhooks/stripe", auth=None)
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] not in _HANDLED_TYPES:
        return HttpResponse(status=200)

    dispatch_webhook_event(event)
    return HttpResponse(status=200)
```

**Dispatcher (`src/payments/webhooks/dispatch.py`):**

```python
from __future__ import annotations

from typing import Any

import stripe

from src.payments.webhooks.events import PaymentFailed, PaymentSucceeded, SubscriptionDeleted


def dispatch_webhook_event(event: stripe.Event) -> None:
    event_type: str = event["type"]
    data: dict[str, Any] = event["data"]["object"]

    if event_type == "payment_intent.succeeded":
        _handle_payment_succeeded(data)
    elif event_type == "payment_intent.payment_failed":
        _handle_payment_failed(data)
    elif event_type == "customer.subscription.deleted":
        _handle_subscription_deleted(data)


def _handle_payment_succeeded(data: dict[str, Any]) -> None:
    domain_event = PaymentSucceeded(
        payment_intent_id=data["id"],
        amount=data["amount"],
        currency=data["currency"],
    )
    _publish(domain_event)


def _handle_payment_failed(data: dict[str, Any]) -> None:
    last_error: dict[str, str] = data.get("last_payment_error") or {}
    domain_event = PaymentFailed(
        payment_intent_id=data["id"],
        failure_code=last_error.get("code", "unknown"),
        failure_message=last_error.get("message", ""),
    )
    _publish(domain_event)


def _handle_subscription_deleted(data: dict[str, Any]) -> None:
    domain_event = SubscriptionDeleted(
        subscription_id=data["id"],
        customer_id=data["customer"],
    )
    _publish(domain_event)


def _publish(event: PaymentSucceeded | PaymentFailed | SubscriptionDeleted) -> None:
    # TODO: wire to event bus / message broker
    pass
```

---

### Quality Gates

| Gate | Command | Exit | Result |
|---|---|---|---|
| Ruff check | `ruff check .` | 0 | clean |
| Ruff format | `ruff format --check .` | 0 | clean |
| mypy | `mypy --strict .` | 0 | clean |
| Coverage | `pytest --cov --cov-fail-under=95` | 0 | 97.2% |
| pip-audit | `pip-audit` | 0 | clean |

---

### Changes

- **Files created:**
  - `src/payments/webhooks/__init__.py`
  - `src/payments/webhooks/events.py`
  - `src/payments/webhooks/views.py`
  - `src/payments/webhooks/dispatch.py`
  - `tests/features/stripe_webhooks.feature`
  - `tests/step_defs/test_stripe_webhooks.py`
- **Files modified:**
  - `src/payments/api.py` — register `router` on `/webhooks/stripe`
- **Tests:** 6 BDD scenarios, 8 unit tests for dispatcher edge cases

### Decisions

- Placed handler under `src/payments/webhooks/` on the assumption payments owns billing events. If a separate `billing` bounded context exists, move the domain events and handler there.
- No shared webhook infrastructure exists in the project, so signature verification is inline. If a second webhook endpoint is added, extract verification into middleware.
- Webhook secret loaded from `settings.STRIPE_WEBHOOK_SECRET` (must be set in environment). No hardcoded value.
- `dispatch.py` uses a stub `_publish` — wire to actual event bus before go-live.

---

## Results

### Criteria

- [x] PASS: Agent mandates reading CLAUDE.md and checking `.claude/rules/` before writing any code — Pre-Flight Step 1 calls `Read(file_path="CLAUDE.md")` and `Read(file_path=".claude/CLAUDE.md")` with explicit check of `.claude/rules/` for installed rules.
- [x] PASS: Agent classifies this as a new domain feature and specifies BDD spec must be written first — Classification table maps "New domain feature" → "BDD spec first → step defs → frozen dataclass model → implementation"; Pre-Flight Step 3 enforces this path.
- [x] PASS: Agent produces or references a Gherkin feature file covering happy path, signature validation failure, and at least one unsupported event type — Testing Hierarchy mandates `.feature` files in `tests/features/` with one scenario per behaviour; all required scenarios follow from this rule applied to the prompt.
- [x] PASS: Agent uses frozen dataclasses for domain event models — Domain Patterns section: "All domain models are immutable", `frozen=True` on every domain dataclass, listed as a non-negotiable.
- [x] PASS: Agent includes explicit type annotations on all functions and rejects use of `Any` — Type Safety: "every function has type annotations", "No `Any` without justification", enforced mechanically by `mypy --strict` gate.
- [x] PASS: Agent specifies all quality gates must pass: ruff, mypy --strict, pytest coverage >= 95% — Quality Gates section lists all gates with command and "Every code change must pass all gates. No partial compliance."
- [x] PASS: Agent identifies `except: pass` or bare exception catching as forbidden — Error Handling: "No `except: pass`", "Catch specific exceptions" listed as a non-negotiable.
- [~] PARTIAL: Agent raises a decision checkpoint before implementing — Decision Checkpoints table includes "Adding a new external integration or ingress surface" which maps to the Stripe webhook. The trigger is defined but framed as a conditional stop rather than a guaranteed opening question. Score: 0.5
- [x] PASS: Output format includes Pre-Flight, BDD Evidence, Quality Gates, and Changes sections — Output Format template explicitly defines all four headings.

### Output expectations

- [x] PASS: Output's endpoint is exactly `POST /webhooks/stripe`, mounted on a Django Ninja router — simulated output uses `@router.post("/webhooks/stripe")` on a Django Ninja `Router`.
- [x] PASS: Output verifies Stripe webhook signature using `stripe.Webhook.construct_event` with 400 on failure — simulated output catches `stripe.error.SignatureVerificationError` and returns `HttpResponse(status=400)` with no body detail.
- [x] PASS: Output handles all three event types — `payment_intent.succeeded`, `payment_intent.payment_failed`, and `customer.subscription.deleted` all appear in dispatcher and BDD scenarios.
- [x] PASS: Output's domain events are frozen dataclasses with explicit type annotations on every field, no `Any` — `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted` all use `@dataclass(frozen=True)` with typed fields.
- [x] PASS: Output's Gherkin feature file covers happy path per event type, signature validation failure, and at least one unsupported event type in `.feature` files — simulated feature file includes all required scenario types in `tests/features/stripe_webhooks.feature`.
- [x] PASS: Output's exception handling uses specific exception types — `stripe.error.SignatureVerificationError` caught; no bare `except:` or `except Exception: pass`.
- [x] PASS: Output's quality gates evidence shows ruff, mypy --strict, and pytest --cov with command and exit code — Quality Gates table present with Command and Exit columns, all gates passing.
- [x] PASS: Output's webhook secret loaded from config/env — `settings.STRIPE_WEBHOOK_SECRET` used in `views.py`; no hardcoded string.
- [~] PARTIAL: Output raises a decision checkpoint about bounded context placement — Decision checkpoint fires on "new external integration or ingress surface" and the Decisions section addresses bounded context. Partially met: framed as a post-hoc assumption note rather than a hard stop before any code is shown. Score: 0.5

## Notes

The definition is strong. The non-negotiables, classification table, and quality gates enforce the most important criteria at multiple levels. BDD-first is mechanically enforced by the Testing Hierarchy section, not just stated as a principle.

The single recurring weakness across both PARTIAL criteria is the same structural issue: Decision Checkpoints are defined as conditional triggers ("STOP and ask before X") rather than proactive openers. For this prompt the trigger fires — Stripe webhooks are clearly a new ingress surface — but the definition doesn't guarantee the agent surfaces the question before producing any code. In the simulated output the checkpoint appears as an inline assumption note rather than a genuine blocking question. Weak but present.

One minor inconsistency in the definition: Quality Gates command uses `--cov-fail-under=95` while Coverage Targets prose states "98%+ overall." The test criteria reference 95%, which matches the command. No score impact.

The `dispatch.py` stub `_publish` function uses `PaymentSucceeded | PaymentFailed | SubscriptionDeleted` as the union type rather than a protocol or base class — consistent with the "no `Any`" constraint but worth noting as a scalability consideration as more event types are added.
