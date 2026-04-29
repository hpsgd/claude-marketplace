# Test: Stripe webhook handler implementation

Scenario: User asks the Python developer to implement a webhook handler for Stripe payment events in an existing Django Ninja API. The project uses event sourcing with frozen dataclasses and strict typing.

## Prompt

We need to handle Stripe webhooks in our Django Ninja API. The endpoint should be at `POST /webhooks/stripe` and handle these event types: `payment_intent.succeeded`, `payment_intent.payment_failed`, and `customer.subscription.deleted`. Each event should be validated with the Stripe webhook secret and then dispatched as a domain event. The project uses pytest-bdd for testing and mypy strict mode. Can you implement this?

## Criteria

- [ ] PASS: Agent mandates reading CLAUDE.md and checking `.claude/rules/` before writing any code
- [ ] PASS: Agent classifies this as a new domain feature and specifies BDD spec must be written first
- [ ] PASS: Agent produces or references a Gherkin feature file covering happy path, signature validation failure, and at least one unsupported event type
- [ ] PASS: Agent uses frozen dataclasses for domain event models (e.g. `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted`)
- [ ] PASS: Agent includes explicit type annotations on all functions and rejects use of `Any`
- [ ] PASS: Agent specifies all quality gates must pass: ruff, mypy --strict, pytest coverage >= 95%
- [ ] PASS: Agent identifies `except: pass` or bare exception catching as forbidden and handles Stripe signature errors with a specific exception type
- [ ] PARTIAL: Agent raises a decision checkpoint before implementing (e.g. asks about bounded context placement or existing webhook infrastructure)
- [ ] PASS: Output format includes Pre-Flight, BDD Evidence, Quality Gates, and Changes sections

## Output expectations

- [ ] PASS: Output's endpoint is exactly `POST /webhooks/stripe`, mounted on a Django Ninja router, accepts the raw request body (not Django's parsed JSON) so signature verification can use the raw bytes
- [ ] PASS: Output verifies the Stripe webhook signature using `stripe.Webhook.construct_event` (or equivalent) with the configured webhook secret, and returns 400 with no body details on signature failure
- [ ] PASS: Output handles all three event types from the prompt — `payment_intent.succeeded`, `payment_intent.payment_failed`, `customer.subscription.deleted` — and returns 200 (acknowledgement) for unsupported event types rather than 4xx, so Stripe doesn't retry forever
- [ ] PASS: Output's domain events (e.g. `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted`) are frozen dataclasses with explicit type annotations on every field — no `Any`
- [ ] PASS: Output's Gherkin feature file covers happy path per event type, signature validation failure, and at least one unsupported event type — and the BDD specs are in `.feature` files, not just docstrings
- [ ] PASS: Output's exception handling uses specific exception types (e.g. `stripe.error.SignatureVerificationError`) — never bare `except:` or `except Exception: pass`
- [ ] PASS: Output's quality gates evidence shows `ruff check` clean, `mypy --strict` clean, and `pytest --cov` with coverage at or above 95% — with command and exit code shown
- [ ] PASS: Output's webhook secret is loaded from configuration / env (e.g. `settings.STRIPE_WEBHOOK_SECRET`), never hardcoded, and the test fixtures use a separate test secret
- [ ] PASS: Output handles webhook idempotency — Stripe can retry the same event, so the handler must be safe to invoke twice with the same `event.id` (deduplication by event ID, or idempotent domain event publishing)
- [ ] PARTIAL: Output raises a decision checkpoint about bounded context placement (where the webhook handler lives, which domain owns the events) before just dropping it into a generic `webhooks/` module
