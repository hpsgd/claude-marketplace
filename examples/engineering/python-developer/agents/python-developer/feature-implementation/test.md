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
