# Acceptance Criteria: [Story Title]

| Field | Value |
|---|---|
| **Story reference** | [e.g. PROJ-1234] |
| **Author** | [Name] |
| **Reviewed by** | Product: [Name], Dev: [Name], QA: [Name] |
| **3 Amigos date** | [YYYY-MM-DD] |

## Story

> As a **[type of user]**,
> I want **[action or capability]**,
> so that **[benefit or value]**.

## Rules

1. [Business rule that governs this story — e.g. "Users must be authenticated to access this feature"]
2. [Second rule — e.g. "Discount cannot exceed 50% of the original price"]
3. [Third rule — e.g. "Email notification is sent within 60 seconds of the event"]

## Examples

### Rule 1: [Rule name or short description]

**Scenario: [Happy path]**
- **Given** [precondition — system state before the action]
- **When** [action the user takes]
- **Then** [expected outcome — observable result]

**Scenario: [Alternate path]**
- **Given** [different precondition]
- **When** [same or different action]
- **Then** [different expected outcome]

### Rule 2: [Rule name or short description]

**Scenario: [Happy path]**
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

### Rule 3: [Rule name or short description]

**Scenario: [Happy path]**
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

## Edge Cases

| Condition | Expected Behaviour |
|---|---|
| [Empty state — e.g. no items in list] | [What the user should see or experience] |
| [Boundary — e.g. maximum allowed value] | [What happens at the boundary] |
| [Boundary + 1 — e.g. exceeding maximum] | [Validation error or rejection behaviour] |
| [Concurrent action — e.g. two users editing same record] | [Conflict resolution behaviour] |
| [Error condition — e.g. network failure mid-operation] | [Error message, retry behaviour, data integrity] |
| [Invalid input — e.g. special characters, SQL injection] | [Input rejected with clear validation message] |

## Non-Functional Criteria

| Category | Criterion |
|---|---|
| **Performance** | [e.g. Page loads in < 2 seconds on 3G, API responds in < 200ms p95] |
| **Accessibility** | [e.g. WCAG 2.1 AA compliant, keyboard navigable, screen reader tested] |
| **Security** | [e.g. Input validated server-side, authorisation checked, no PII in logs] |

## Out of Scope

- [Functionality explicitly NOT included in this story — helps prevent scope creep]
- [Related feature that will be handled in a separate story]

## Open Questions

| # | Question | Raised By | Status | Resolution |
|---|---|---|---|---|
| 1 | [Question flagged during 3 amigos that needs resolution before implementation] | [Name] | [Open / Resolved] | [Answer once resolved] |

## Test Level Assignment

| Criterion | Test Level | Rationale |
|---|---|---|
| [Rule 1 — happy path] | [Unit] | [Pure business logic, no dependencies] |
| [Rule 1 — alternate path] | [Unit] | [Validation logic] |
| [Rule 2 — integration with external service] | [Integration] | [Requires API contract verification] |
| [Edge case — concurrent access] | [Integration] | [Requires database interaction] |
| [Full user journey through all rules] | [E2E] | [Cross-component, critical user flow] |
| [Non-functional — performance] | [Performance] | [Requires load testing under realistic conditions] |
