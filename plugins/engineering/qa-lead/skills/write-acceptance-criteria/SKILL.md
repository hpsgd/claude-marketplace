---
name: write-acceptance-criteria
description: "Write acceptance criteria for a user story using Example Mapping and Given/When/Then format. The primary output of the 3 amigos session (product + dev + QA). Use when a story needs testable criteria before development starts."
argument-hint: "[user story or feature to write acceptance criteria for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write acceptance criteria for $ARGUMENTS.

Acceptance criteria define the boundary of "done" for a story. They must be testable, unambiguous, and written in business language. Every criterion is a contract between product, development, and QA.

## Step 1 — Understand the story

Before writing criteria, decompose the story:

1. **User type.** Who is the actor? Be specific — "admin user with billing permissions" not "user."
2. **Goal.** What are they trying to accomplish? State the outcome, not the mechanism.
3. **Value.** Why does this matter? What business outcome does it enable?
4. **Context.** What preconditions, permissions, or system states are relevant?
5. **Scope boundaries.** What is explicitly out of scope? Document this now to prevent scope creep during development.

Search the codebase for related features, existing test files, and prior acceptance criteria to understand patterns and avoid contradictions.

## Step 2 — Identify business rules

Business rules are the constraints that govern the story's behaviour. Each rule becomes a group of scenarios.

Use Example Mapping to structure the discovery:

| Colour | Represents | Examples |
|---|---|---|
| **Yellow** | The story | "As a billing admin, I want to apply a discount code" |
| **Blue** | Business rules | "Discount codes can only be used once per account" |
| **Green** | Examples per rule | "Given a valid code, When applied, Then the discount is reflected in the total" |
| **Red** | Questions / unknowns | "What happens if the code expired 1 minute ago mid-checkout?" |

List every business rule before writing scenarios. Common sources of rules:
- Permissions and authorisation ("who can do this?")
- Validation constraints ("what inputs are valid?")
- State transitions ("what must be true before and after?")
- Concurrency ("what if two users do this simultaneously?")
- Time and scheduling ("are there deadlines, delays, or time zones?")
- Limits and thresholds ("are there caps, quotas, or rate limits?")

**Rule:** If you discover a red card (unanswered question), flag it explicitly. Do not invent an answer. Unresolved questions block development.

## Step 3 — Write examples per rule (Given/When/Then)

For each business rule, write concrete scenarios using Gherkin syntax:

```gherkin
Rule: [Business rule in plain language]

  Scenario: [Happy path — the expected behaviour]
    Given [precondition — system state, user state, data state]
    And [additional precondition if needed]
    When [action the user takes]
    And [additional action if needed]
    Then [observable outcome]
    And [additional outcome if needed]

  Scenario: [Error case — what happens when something goes wrong]
    Given [precondition]
    When [action that triggers the error]
    Then [error behaviour — what the user sees, what the system does]

  Scenario: [Edge case — boundary conditions]
    Given [precondition at the boundary]
    When [action]
    Then [expected behaviour at the boundary]
```

### Scenario coverage per rule

Every business rule must have at minimum:

| Scenario type | Purpose | Required |
|---|---|---|
| **Happy path** | The expected, successful flow | Yes — always |
| **Validation error** | Invalid input is rejected correctly | Yes — if the rule involves input |
| **Permission denied** | Unauthorised user is blocked correctly | Yes — if the rule involves permissions |
| **Edge case** | Boundary values, empty states, maximums | Yes — always |
| **Concurrency** | Simultaneous actions handled correctly | If applicable |

**Rules for writing scenarios:**
- **One behaviour per scenario.** A scenario that tests two things is two scenarios. If you need multiple `Then` clauses testing different behaviours, split the scenario.
- **Business language, not technical language.** "Then the user sees an error message" not "Then the API returns 422." The technical implementation is the developer's concern.
- **Given sets up state, When triggers action, Then observes outcome.** Do not put assertions in Given. Do not put setup in Then.
- **Concrete examples over abstract rules.** "Given the discount code 'SAVE20' has been used by account 'Acme Corp'" not "Given a used discount code." Concrete examples are unambiguous.
- **Every rule needs at least 2 examples.** One example is a demo. Two examples define a pattern. If you can't write two examples, the rule is not clear enough.

## Step 4 — Define non-functional criteria

Functional criteria say what the system does. Non-functional criteria say how well it does it.

| Category | Criterion | Threshold | How to test |
|---|---|---|---|
| **Performance** | Page load / API response time | < 2s page / < 500ms API at p95 | k6 load test, integration timing |
| **Accessibility** | Keyboard + screen reader | Full flow without mouse, elements announced | Playwright keyboard + axe-core |
| **Security** | Auth enforced, input sanitised | 403 for unauthorised, no XSS | Role-based integration tests, security suite |
| **Resilience** | Graceful degradation | Error state when dependency is down | Integration test with dependency unavailable |

Include only the categories relevant to this story.

## Step 5 — Assign test levels

Each criterion must be mapped to a test level so QA and development know where it gets verified:

| Criterion | Test level | Rationale |
|---|---|---|
| [Business rule scenario 1] | Unit | Pure logic, no dependencies |
| [Business rule scenario 2] | Integration | Involves database/API boundary |
| [Permission check scenario] | Integration | Requires auth middleware |
| [Happy path end-to-end] | E2E | Critical user flow |
| [Performance criterion] | Performance | Requires load testing tool |
| [Accessibility criterion] | Manual + automated | axe-core catches 30-50%, rest needs manual review |

**Rules for test level assignment:**
- **Default to the lowest sufficient level.** Unit over integration over E2E. Lower levels run faster and fail more precisely.
- **E2E only for critical user flows.** If the scenario can be verified at integration level, it should be.
- **Security criteria need dedicated tests.** Do not rely on happy-path tests to catch authorisation bypasses.

## Step 6 — Review completeness

Run these final checks before declaring the criteria complete:

### INVEST check

| Property | Check | Status |
|---|---|---|
| **Independent** | Can this story be delivered without other stories in progress? | [Yes / No — dependency] |
| **Negotiable** | Are the criteria flexible on implementation while fixed on outcome? | [Yes / No — over-specified] |
| **Valuable** | Does completing this deliver user or business value? | [Yes / No — missing value] |
| **Estimable** | Can the team estimate effort from these criteria? | [Yes / No — unclear] |
| **Small** | Can this be completed in a single sprint? | [Yes / No — split suggestion] |
| **Testable** | Can every criterion be verified pass/fail? | [Yes / No — vague criterion] |

### Edge case audit

Verify you have covered: empty/null input, maximum/minimum values, special characters, concurrent access, network failure, permission boundaries, and time zone variations (if applicable).

### Out of scope

Explicitly list what this story does NOT cover to prevent scope creep.

## Output Format

```markdown
# Acceptance Criteria: [Story title]

**Story:** As a [user type], I want to [goal], so that [value]
**Scope:** [what's in] | **Out of scope:** [what's out]

## Business Rules and Scenarios

### Rule 1: [Business rule]

**Scenario: [Happy path]**
- Given [precondition]
- When [action]
- Then [outcome]

**Scenario: [Error case]**
- Given [precondition]
- When [action]
- Then [outcome]

**Scenario: [Edge case]**
- Given [precondition]
- When [action]
- Then [outcome]

### Rule 2: [Business rule]
[scenarios...]

## Non-Functional Criteria
| Category | Criterion | Threshold |
|---|---|---|
| [category] | [criterion] | [threshold] |

## Test Level Mapping
| Criterion | Level | Notes |
|---|---|---|
| [criterion] | [unit/integration/e2e] | [rationale] |

## Open Questions
| Question | Impact | Owner |
|---|---|---|
| [unresolved question] | [blocks/informs what] | [who resolves] |
```

## Rules

- **One scenario per behaviour, not per test.** A scenario describes a single behaviour. Multiple test cases may verify it, but the acceptance criterion is the behaviour, not the test.
- **Business language, not technical language.** Acceptance criteria are a contract with product, not a test script for QA. Write in the language of the user and the domain.
- **Every rule needs at least 2 examples.** A rule with one example is ambiguous. The second example clarifies intent, and the edge case validates boundaries.
- **Edge cases are mandatory, not optional.** Empty inputs, boundary values, concurrent access, and error states are where bugs live. If your acceptance criteria only cover the happy path, you have a spec for a demo, not a spec for production software.
- **Unresolved questions block development.** A red card (open question) must be resolved before the story enters a sprint. Flag them loudly.
- **Non-functional criteria are acceptance criteria too.** "It works" is not sufficient. "It works within 500ms for 95% of requests" is an acceptance criterion.

## Related Skills

- `/qa-lead:test-strategy` — provides the overall test strategy context (tools, levels, coverage targets) that acceptance criteria map into.
- `/qa-engineer:generate-tests` — consumes acceptance criteria to generate executable test code. Write the criteria first, then generate the tests.
- `/product-owner:write-user-story` — produces the user stories that acceptance criteria are written for. The story defines what; the criteria define done.
