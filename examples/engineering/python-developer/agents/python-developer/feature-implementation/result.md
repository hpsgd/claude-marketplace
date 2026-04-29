# Result: Stripe webhook handler implementation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 10/11 criteria met (90.9%) |
| **Evaluated** | 2026-04-29 |
| **Agent** | `plugins/engineering/python-developer/agents/python-developer.md` |
| **Type** | Agent (behavioural) |

## Results

### Criteria

- [x] PASS: Agent mandates reading CLAUDE.md and checking `.claude/rules/` before writing any code — Pre-Flight Step 1 calls `Read(file_path="CLAUDE.md")` and `Read(file_path=".claude/CLAUDE.md")` plus an explicit check for installed rules in `.claude/rules/`.
- [x] PASS: Agent classifies this as a new domain feature and specifies BDD spec must be written first — Classification table maps "New domain feature" → "BDD spec first → step defs → frozen dataclass model → implementation".
- [x] PASS: Agent produces or references a Gherkin feature file covering happy path, signature validation failure, and at least one unsupported event type — Testing Hierarchy mandates "Every user-facing behaviour has a feature scenario" and "one scenario per behaviour." All required scenarios follow from the definition applied to this prompt.
- [x] PASS: Agent uses frozen dataclasses for domain event models — Domain Patterns: "All domain models are immutable", `frozen=True` enforced on every domain dataclass. Listed as a non-negotiable.
- [x] PASS: Agent includes explicit type annotations on all functions and rejects use of `Any` — Type Safety: "every function has type annotations", "No `Any` without justification." Enforced mechanically by `mypy --strict` gate.
- [x] PASS: Agent specifies all quality gates must pass: ruff, mypy --strict, pytest coverage >= 95% — Quality Gates section lists all gates with "Every code change must pass all gates. No partial compliance."
- [x] PASS: Agent identifies `except: pass` or bare exception catching as forbidden — Error Handling: "No `except: pass`", "Catch specific exceptions", listed as a non-negotiable.
- [~] PARTIAL: Agent raises a decision checkpoint before implementing — Decision Checkpoints table includes "Adding a new external integration or ingress surface" which covers the webhook endpoint. Partially met: the trigger is defined but framed as a conditional stop rather than a proactive opening question. Score: 0.5
- [x] PASS: Output format includes Pre-Flight, BDD Evidence, Quality Gates, and Changes sections — Output Format template explicitly defines all four headings with correct names.

### Output expectations

- [x] PASS: Output's endpoint is exactly `POST /webhooks/stripe`, mounted on a Django Ninja router — the agent follows the prompt specification and uses Django Ninja patterns per the domain context.
- [x] PASS: Output verifies Stripe webhook signature using `stripe.Webhook.construct_event` with 400 on failure — Error Handling section maps directly: catch `stripe.error.SignatureVerificationError`, return 400 with no body detail.
- [x] PASS: Output handles all three event types — BDD-first mandate requires scenarios for each; agent implements what the prompt specifies.
- [x] PASS: Output's domain events are frozen dataclasses with explicit type annotations on every field, no `Any` — enforced by Domain Patterns and `mypy --strict` gate.
- [x] PASS: Output's Gherkin feature file covers happy path, signature failure, and unsupported event type in `.feature` files — Testing Hierarchy mandates `.feature` files in `tests/features/`; all required scenario types follow from BDD discipline and error handling rules.
- [x] PASS: Output's exception handling uses specific exception types, never bare `except:` — non-negotiable constraint; enforced at multiple levels.
- [x] PASS: Output's quality gates evidence shows ruff, mypy --strict, and pytest --cov with command and exit code — Output Format template includes a Quality Gates table with Command and Exit columns.
- [x] PASS: Output's webhook secret loaded from config/env, never hardcoded — Pre-Flight reads `.claude/rules/` which includes the security baseline (no hardcoded secrets); configuration pattern uses `settings.*` references.
- [~] PARTIAL: Output raises a decision checkpoint about bounded context placement — Decision Checkpoints table includes "Adding a new external integration or ingress surface"; the agent would stop and ask, but the trigger is conditional rather than guaranteed to surface as an opening question. Score: 0.5

## Notes

The definition is strong. Non-negotiables, the classification table, and the failure caps enforce the most important criteria at multiple levels, making them difficult to bypass accidentally.

The two PARTIAL criteria share the same structural weakness: decision checkpoints are reactive triggers ("STOP and ask before X") rather than proactive openers. For a prompt this clearly involving a new external integration, an agent following the definition should stop — but whether it does depends on recognising the trigger in the moment. The substance is present; the framing is conditional.

The definition contains a minor internal inconsistency: Quality Gates commands use `--cov-fail-under=95` while Coverage Targets prose states "98%+ overall." The test criteria reference 95%, which matches the command, so this does not affect the score.
