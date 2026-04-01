---
name: generate-tests
description: Generate test cases and test code for a function, component, endpoint, or feature.
argument-hint: "[file, function, or component to test]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Generate tests for $ARGUMENTS.

## Process

1. Read the code to understand what it does — inputs, outputs, side effects, error cases
2. Identify test cases: happy path, edge cases, error cases, boundary conditions
3. Write tests at the appropriate level (unit, integration, or e2e)
4. Follow the project's testing conventions:
   - **TypeScript/Vitest**: co-located `.test.ts`, `vi.hoisted()` + `vi.mock()`, no jsdom
   - **.NET/xUnit**: BDD naming (`WhenDoingSomething`), NSubstitute, Shouldly, Alba for HTTP
   - **Python/pytest-bdd**: Gherkin features + step defs for behaviour, Hypothesis for properties

## Rules

- One assertion per test — each test verifies one behaviour
- Arrange-Act-Assert pattern
- Real implementations over mocks — mock only at external boundaries
- Test data via factory functions, not inline literals
- Each test independent — no shared mutable state
- Name describes the behaviour: `it('returns null when user is not found')`
