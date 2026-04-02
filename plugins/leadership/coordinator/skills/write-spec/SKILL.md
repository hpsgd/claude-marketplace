---
name: write-spec
description: "Write a specification document — the contract between product (what), engineering (how), and QA (verify). Produces a structured spec with user stories, acceptance criteria, API contracts, and data model. Use after decompose-initiative to define what will be built before development starts."
argument-hint: "[feature or workstream to specify]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write Spec

Write a specification document for $ARGUMENTS. The spec is the contract between product (what), engineering (how), and QA (verify). Use `/coordinator:decompose-initiative` first to identify workstreams, then write a spec for each workstream before development starts.

## Step 1: Define the Problem

Before specifying a solution, establish what problem exists and for whom:

```markdown
### Problem Definition

| Question | Answer |
|---|---|
| **What problem are we solving?** | [Specific problem — not "improve the experience"] |
| **Who has this problem?** | [Specific user type — not "users"] |
| **How do we know it's a problem?** | [Evidence — support tickets, analytics, user research, business metric] |
| **What does success look like?** | [Measurable criteria — "reduce checkout abandonment from 40% to 25%"] |
| **What happens if we don't solve it?** | [Cost of inaction — quantified if possible] |
```

Scan the codebase for existing implementations related to this feature. Use `Glob` and `Grep` to find relevant code, tests, and documentation that inform the spec.

**Output:** Completed problem definition table with evidence.

## Step 2: Write User Stories

For each distinct user need, write a story in standard format with [RICE scoring](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/):

```markdown
### User Stories

| ID | Story | RICE Score | Priority |
|---|---|---|---|
| US-1 | As a [user type], I want [capability] so that [benefit] | R:_ I:_ C:_ E:_ = _ | P0/P1/P2 |
| US-2 | ... | ... | ... |
```

**RICE components:**
- **Reach** — how many users per quarter
- **Impact** — [3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal]
- **Confidence** — [100%=high, 80%=medium, 50%=low]
- **Effort** — person-weeks

Stories must be **independent, negotiable, valuable, estimable, small, and testable** (INVEST).

**Output:** Prioritised user story table with RICE scores.

## Step 3: Write Acceptance Criteria

For each user story, write acceptance criteria in Given/When/Then format covering happy path, error cases, and edge cases:

```markdown
### US-1: [Story title]

#### Happy path
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

#### Error cases
- **Given** [precondition]
- **When** [invalid action or failure condition]
- **Then** [error handling — message, rollback, retry]

#### Edge cases
- **Given** [boundary condition — empty, maximum, concurrent, timeout]
- **When** [action at boundary]
- **Then** [expected behaviour at boundary]
```

Every story must have at least: 1 happy path, 2 error cases, and 2 edge cases. If you cannot write acceptance criteria for a story, the story is too vague — rewrite it.

**Output:** Acceptance criteria for every user story.

## Step 4: Define API Contract

For each endpoint or interface the feature requires:

```markdown
### API Contract

#### [METHOD] /path/to/resource

**Purpose:** [What this endpoint does]

**Request:**
| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| field_name | string | Yes | max 255, regex pattern | [What it represents] |

**Response (200):**
```json
{
  "id": "uuid",
  "field": "value",
  "created_at": "ISO8601"
}
```

**Error responses:**
| Status | Code | When |
|---|---|---|
| 400 | VALIDATION_ERROR | [Specific trigger] |
| 404 | NOT_FOUND | [Specific trigger] |
| 409 | CONFLICT | [Specific trigger] |
| 422 | UNPROCESSABLE | [Specific trigger] |
```

If an [OpenAPI](https://www.openapis.org/) specification exists in the codebase, reference and extend it rather than duplicating.

**Output:** API contract for every endpoint with request/response schemas and error codes.

## Step 5: Define Data Model

Document entities, relationships, and constraints:

```markdown
### Data Model

#### [Entity Name]

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK, generated | Primary identifier |
| field_name | varchar(255) | NOT NULL, UNIQUE | [Purpose] |
| status | enum | CHECK(status IN ('active','archived')) | [State machine description] |
| created_at | timestamptz | NOT NULL, DEFAULT now() | Record creation time |

#### Relationships
- [Entity A] 1:N [Entity B] via `entity_a_id` FK
- [Entity C] M:N [Entity D] via `entity_c_d` join table

#### Indexes
| Index | Columns | Type | Rationale |
|---|---|---|---|
| idx_entity_status | status, created_at | btree | Filter active records by date |

#### Migration notes
- [Breaking changes, backfill requirements, rollback strategy]
```

Check existing models in the codebase with `Grep` to ensure consistency with established patterns.

**Output:** Data model with entities, relationships, constraints, indexes, and migration notes.

## Step 6: Define Non-Functional Requirements

```markdown
### Non-Functional Requirements

| Category | Requirement | Measurement | Target |
|---|---|---|---|
| **Performance** | API response time | p95 latency | < 200ms |
| **Performance** | Throughput | Requests/second | > 100 rps |
| **Scalability** | Concurrent users | Load test | [target] |
| **Security** | Authentication | [mechanism] | [standard] |
| **Security** | Authorisation | [model — RBAC, ABAC] | [policy] |
| **Accessibility** | WCAG compliance | Automated + manual audit | WCAG 2.1 AA |
| **Reliability** | Availability | Uptime monitoring | 99.9% |
| **Observability** | Logging/metrics | [tools] | [what to capture] |
```

**Output:** NFR table with measurable targets.

## Step 7: List Edge Cases and Boundary Conditions

Exhaustively enumerate edge cases — this is where bugs hide:

```markdown
### Edge Cases

| # | Category | Scenario | Expected Behaviour |
|---|---|---|---|
| E1 | Empty state | No data exists yet | [Behaviour — empty state UI, default values] |
| E2 | Maximum | Field at max length/value | [Behaviour — validation, truncation] |
| E3 | Concurrent | Two users edit same record | [Behaviour — optimistic locking, conflict resolution] |
| E4 | Network | Request timeout mid-operation | [Behaviour — retry, idempotency, partial state] |
| E5 | Permissions | User lacks required role | [Behaviour — 403, UI state] |
| E6 | Migration | Existing data with old schema | [Behaviour — backfill, defaults] |
```

**Output:** Edge case table — minimum 10 entries for any non-trivial feature.

## Step 8: Mark Open Questions and Out-of-Scope

```markdown
### Open Questions (BLOCKS development)

| # | Question | Owner | Deadline | Impact if unresolved |
|---|---|---|---|---|
| Q1 | [Unresolved decision] | [Who decides] | [Date] | [What is blocked] |

### Out of Scope

| Item | Reason | Future consideration? |
|---|---|---|
| [Excluded capability] | [Why excluded] | [Yes — v2 / No — never] |
```

Open questions **must** be resolved before development starts on the affected area.

**Output:** Open questions with owners and deadlines; explicit out-of-scope list.

## Step 9: Circulate for Three Amigos Review

Request sign-off from all three perspectives:

```markdown
### Three Amigos Review

| Role | Reviewer | Status | Comments |
|---|---|---|---|
| **Product** | [name/role] | [Pending/Approved/Changes requested] | [Feedback] |
| **Architecture** | [name/role] | [Pending/Approved/Changes requested] | [Feedback] |
| **QA** | [name/role] | [Pending/Approved/Changes requested] | [Feedback] |

**Review date:** [date]
**Spec status:** [Draft / In review / Approved / Superseded]
```

**Output:** Review tracker with sign-off status.

## Rules

- **Spec before code.** Never write the spec after implementation to document what was built. The spec defines what **will** be built. Writing specs after the fact is documentation, not specification.
- **Acceptance criteria are mandatory.** No user story exists without acceptance criteria. A story without criteria is a wish, not a requirement.
- **Open questions block development.** If a question is unresolved, the affected work cannot start. "We'll figure it out during development" is how rework happens.
- **The spec is a living document.** Requirements change — update the spec when they do. A stale spec is worse than no spec because it misleads.
- **Be specific or be wrong.** "Fast response times" is not a requirement. "p95 latency under 200ms for the search endpoint" is a requirement.
- **Don't spec what you don't need.** Not every feature needs a complex API contract or data model. If the feature is a copy change, the spec is short. Match detail to complexity.

## Output Format

```markdown
# Specification: [Feature Name]

**Version:** [number]  |  **Date:** [date]  |  **Status:** [Draft/In review/Approved]

## 1. Problem Definition
[From Step 1]

## 2. User Stories
[From Step 2 — prioritised with RICE scores]

## 3. Acceptance Criteria
[From Step 3 — per story, Given/When/Then]

## 4. API Contract
[From Step 4 — endpoints, schemas, errors]

## 5. Data Model
[From Step 5 — entities, relationships, migrations]

## 6. Non-Functional Requirements
[From Step 6 — measurable targets]

## 7. Edge Cases
[From Step 7 — exhaustive list]

## 8. Open Questions & Out of Scope
[From Step 8 — blockers and exclusions]

## 9. Review Status
[From Step 9 — three amigos sign-off]
```

## Related Skills

- `/coordinator:decompose-initiative` — produces workstreams that need specs. Decompose the initiative first, then write a spec for each workstream.
- `/qa-lead:test-strategy` — detailed test strategy for the feature. Write the spec first, then define how to test it.
- `/product-owner:write-user-story` — story format and refinement guidance. Use when stories need deeper elaboration.
