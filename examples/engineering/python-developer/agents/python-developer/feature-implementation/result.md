# Result: Stripe webhook handler implementation

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 15/19 criteria met (79%) |
| **Evaluated** | 2026-04-29 |
| **Agent** | `plugins/engineering/python-developer/agents/python-developer.md` |
| **Type** | Agent (behavioural) |

## Results

### Criteria

- [x] PASS: Agent mandates reading CLAUDE.md and checking `.claude/rules/` before writing any code — Pre-Flight Step 1 calls `Read(file_path="CLAUDE.md")` and `Read(file_path=".claude/CLAUDE.md")` plus an explicit check for installed rules in `.claude/rules/`.
- [x] PASS: Agent classifies this as a new domain feature and specifies BDD spec must be written first — Classification table maps "New domain feature" → "BDD spec first → step defs → frozen dataclass model → implementation". Principles and failure caps reinforce this.
- [x] PASS: Agent produces or references a Gherkin feature file covering happy path, signature validation failure, and at least one unsupported event type — Testing Hierarchy mandates "Every user-facing behaviour has a feature scenario" and "one scenario per behaviour." All required scenarios follow from the definition applied to this prompt.
- [x] PASS: Agent uses frozen dataclasses for domain event models — Domain Patterns: "All domain models are immutable", `frozen=True` enforced on every domain dataclass. Listed as a non-negotiable.
- [x] PASS: Agent includes explicit type annotations on all functions and rejects use of `Any` — Type Safety section: "every function has type annotations", "No `Any` without justification." Enforced mechanically by `mypy --strict` gate.
- [x] PASS: Agent specifies all quality gates must pass: ruff, mypy --strict, pytest coverage >= 95% — Quality Gates section lists all gates with "Every code change must pass all gates. No partial compliance."
- [x] PASS: Agent identifies `except: pass` or bare exception catching as forbidden and handles Stripe signature errors with a specific exception type — Error Handling: "No `except: pass`", "Catch specific exceptions", "Add context when re-raising". Listed as a non-negotiable.
- [~] PARTIAL: Agent raises a decision checkpoint before implementing — Decision Checkpoints table includes "Adding a new bounded context" which covers placement of the webhook handler. However, it does not explicitly list "new external integration" or "existing webhook infrastructure" as triggers, so the check for pre-existing webhook middleware would not be a formal stop. Score: 0.5
- [x] PASS: Output format includes Pre-Flight, BDD Evidence, Quality Gates, and Changes sections — Output Format template explicitly defines all four headings with correct names.

### Output expectations

- [ ] FAIL: Output's endpoint is exactly `POST /webhooks/stripe` on a Django Ninja router, accepting raw request body — The agent definition does not address raw body handling for webhook signature verification. Pre-Flight reads existing patterns, but if no existing webhook handler exists, the agent has no basis to know `HttpRequest` body must be read as raw bytes before Django parses it. This implementation detail is not derivable from the definition alone.
- [x] PASS: Output verifies Stripe webhook signature using `stripe.Webhook.construct_event` with 400 on failure — Error Handling section pattern maps directly: catch `stripe.error.SignatureVerificationError`, raise `HttpError(400, ...) from exc`. The definition produces this.
- [~] PARTIAL: Output handles all three event types and returns 200 for unsupported events — The agent would handle all three specified event types (BDD scenarios mandate this). Returning 200 rather than 4xx for unsupported events requires Stripe-specific domain knowledge (Stripe retries on 4xx/5xx) that the agent definition does not encode. The agent might return 200 by default or might return 400, depending on implementation choices. Score: 0.5
- [x] PASS: Output's domain events are frozen dataclasses with explicit type annotations on every field, no `Any` — Enforced by Domain Patterns (frozen=True, no `Any`) and mypy --strict gate.
- [x] PASS: Output's Gherkin feature file covers happy path, signature failure, and unsupported event type in `.feature` files — Testing Hierarchy mandates `.feature` files in `tests/features/` and step defs in `tests/step_defs/`. All required scenarios follow from the BDD-first mandate.
- [x] PASS: Output's exception handling uses specific exception types, never bare `except:` or `except Exception: pass` — Non-negotiable constraint; Error Handling section is explicit and enforced by the quality gates.
- [x] PASS: Output's quality gates evidence shows ruff, mypy --strict, and pytest --cov >= 95% with command and exit code — Output Format template includes a Quality Gates table with Command and Exit columns. The definition mandates this structure.
- [~] PARTIAL: Output's webhook secret is loaded from config/env, never hardcoded, and test fixtures use a separate test secret — The agent reads CLAUDE.md and `.claude/rules/` which includes the security baseline (no hardcoded secrets). However, the agent definition does not specifically address test fixture secrets vs production secrets as distinct requirements. The production secret would come from config; a separate test secret in fixtures is not guaranteed from the definition. Score: 0.5
- [ ] FAIL: Output handles webhook idempotency — The agent definition does not mention idempotency for webhook handlers. The event sourcing section covers idempotency guards on aggregate creation handlers, but this is not connected to the webhook ingress surface. An agent following this definition would not produce idempotency handling unless prompted.
- [x] PASS: PARTIAL criterion — Output raises a decision checkpoint about bounded context placement — Decision Checkpoints table includes "Adding a new bounded context" as a stop trigger. The agent asks about placement before proceeding.

## Notes

The definition is strong on typing, BDD discipline, and error handling. These are enforced at multiple levels (non-negotiables, classification table, principles, failure caps) making them hard to bypass accidentally.

Two output expectation gaps are genuine definition weaknesses rather than prompt-specific blind spots. Raw body handling for Stripe signature verification is an infrastructure detail the definition has no mechanism to surface — the Pre-Flight reads existing patterns, but if no webhook handler exists, the agent picks a body-handling approach without guidance. Idempotency is a design concern the definition skips entirely; the event sourcing section covers creation handlers but not ingress deduplication.

The 95% vs 98% coverage inconsistency from the prior evaluation remains. Quality Gates commands use `--cov-fail-under=95` but Coverage Targets prose states "98%+ overall." An agent following the definition would pass gates at 97% and consider the task complete.
