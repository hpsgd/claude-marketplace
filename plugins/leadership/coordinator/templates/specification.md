# Specification: [Feature/Project Title]

| Field        | Value                          |
|--------------|--------------------------------|
| Version      | 0.1                            |
| Status       | Draft / Review / Approved      |
| Author       | [Name]                         |
| Reviewers    | [Product], [Architecture], [QA]|
| Last Updated | YYYY-MM-DD                     |

---

## Problem Statement

**What problem are we solving?**
[Describe the specific problem in concrete terms. Avoid solution language.]

**Who experiences this problem?**
[Identify the affected user segments and estimate how many users are impacted.]

**What evidence do we have?**
[Link to support tickets, analytics, user research, or business metrics that demonstrate the problem exists and its severity.]

---

## User Stories

| # | Story | RICE Score |
|---|-------|------------|
| 1 | As a [user type], I want [action], so that [benefit]. | R: _ I: _ C: _ E: _ = **_** |
| 2 | As a [user type], I want [action], so that [benefit]. | R: _ I: _ C: _ E: _ = **_** |

---

## Acceptance Criteria

### Story 1: [Story title]

- **Happy path:** Given [precondition], when [action], then [expected result].
- **Error case:** Given [precondition], when [invalid action], then [error handling].
- **Edge case:** Given [boundary condition], when [action], then [expected result].
- **Boundary:** Given [limit value], when [action], then [expected result].

### Story 2: [Story title]

[Repeat Given/When/Then for happy path, error cases, edge cases, and boundaries.]

---

## API Contract

| Method | Endpoint             | Description              |
|--------|----------------------|--------------------------|
| GET    | /api/v1/resource     | [What it returns]        |
| POST   | /api/v1/resource     | [What it creates]        |

**Request/response schemas:** Reference OpenAPI spec at `[path]`, or inline JSON schema here.

**Error codes:** 400 [validation], 401 [auth], 404 [not found], 409 [conflict], 500 [server].

---

## Data Model

| Entity       | Key Fields              | Relationships                | Constraints            |
|--------------|-------------------------|------------------------------|------------------------|
| [EntityName] | id, name, status, ...   | belongs_to [Other], has_many  | name NOT NULL, UNIQUE  |

**Migrations needed:**
- [ ] [Describe schema change and its reversibility.]

---

## Non-Functional Requirements

| Category       | Requirement                                              |
|----------------|----------------------------------------------------------|
| Performance    | [e.g., p95 latency < 200ms under 1000 RPS]              |
| Security       | [e.g., input sanitised, RBAC enforced, PII encrypted]    |
| Accessibility  | [e.g., WCAG 2.1 AA compliance]                          |
| Scalability    | [e.g., support 10x current load without architecture change] |

---

## Edge Cases & Boundary Conditions

| # | Scenario                                | Expected Behaviour                     |
|---|-----------------------------------------|----------------------------------------|
| 1 | [Empty input / zero-length collection]  | [What should happen]                   |
| 2 | [Maximum allowed value]                 | [What should happen]                   |
| 3 | [Concurrent modification]               | [What should happen]                   |
| 4 | [Network timeout mid-operation]         | [What should happen]                   |

---

## Out of Scope

- [Feature or behaviour explicitly excluded from this spec.]
- [Another excluded item with brief rationale.]

---

## Open Questions

| # | Question                                         | Owner   | Status |
|---|--------------------------------------------------|---------|--------|
| 1 | [Question needing clarification before dev starts]| [Name] | Open   |
| 2 | [Another question]                                | [Name] | Open   |

---

## Approval

| Role         | Name   | Date       | Approved |
|--------------|--------|------------|----------|
| Product      | [Name] | YYYY-MM-DD | [ ]      |
| Architecture | [Name] | YYYY-MM-DD | [ ]      |
| QA           | [Name] | YYYY-MM-DD | [ ]      |
