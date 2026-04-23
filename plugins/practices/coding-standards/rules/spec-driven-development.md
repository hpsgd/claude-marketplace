---
description: Spec-driven development principles — specs before code, acceptance criteria before implementation
---

# Spec-Driven Development

## Principle

Write specs before code. Define acceptance criteria before implementation. The spec is the contract between product (what), engineering (how), and QA (verify). Never start implementation without a written spec that stakeholders have reviewed.

## The flow

Follow this order strictly:

1. **Product Owner** writes the spec — user stories with acceptance criteria in Given/When/Then ([BDD](https://cucumber.io/docs/bdd/))
2. **Architect** adds API contracts (OpenAPI) and data model to the spec
3. **QA Lead** reviews acceptance criteria for completeness and edge cases
4. **QA Engineer** writes acceptance tests from the spec (tests must fail initially)
5. **Developer** implements until all acceptance tests pass
6. **Doc writers** document the implemented behaviour from the spec

Never reverse this order. Code that exists before a spec is prototyping, not delivery.

## What counts as a spec

A spec must include:

- User stories with Gherkin acceptance criteria (Given/When/Then)
- API contract (OpenAPI / GraphQL schema) for any new or changed endpoints
- Data model changes (new tables, columns, constraints)
- Edge cases and error scenarios — not just the happy path
- Non-functional requirements (latency, throughput, availability) when relevant

Use [Example Mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/) to discover rules, examples, and questions before writing Gherkin. See also [Specification by Example](https://gojko.net/books/specification-by-example/) by Gojko Adzic.

## When to skip

A full spec is not required for:

- Trivial changes estimated under 1 hour
- Pure refactoring with no behaviour change (existing tests are the spec)
- Documentation-only changes
- Dependency updates with no API changes

Even when skipping, state the reason in the PR description.

## Anti-patterns

- **"I'll write the spec after"** — the spec becomes documentation, not a contract. It no longer drives design decisions.
- **"The code IS the spec"** — code is the implementation. It tells you what happens, not what should happen or why.
- **"We don't have time for specs"** — you don't have time for the rework, miscommunication, and missed edge cases that follow from skipping specs.
- **"The spec is in Slack/the meeting notes"** — if it's not in the repo alongside the code, it doesn't exist.
