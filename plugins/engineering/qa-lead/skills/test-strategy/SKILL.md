---
name: test-strategy
description: "Define a test strategy for a feature, service, or system. Determines what to test, at what level, with what tools, and what quality gates to enforce."
argument-hint: "[feature, service, or system to define test strategy for]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

# Test Strategy

Define a comprehensive test strategy for $ARGUMENTS.

## Step 1: Understand What's Being Tested

Before writing a single test plan:

1. **What does it do?** Describe the feature/service in one paragraph
2. **What are the critical user flows?** The paths that, if broken, mean the product is broken
3. **What are the failure modes?** What does a bug look like to users?
4. **What external dependencies exist?** APIs, databases, third-party services, time
5. **What's the risk profile?** Financial, safety, data integrity, reputation, convenience

## Step 2: Define Test Levels

### The Testing Pyramid

```
     /  E2E   \      Few, slow, expensive — critical flows only
    /----------\
   / Integration \   Moderate — component boundaries, API contracts
  /--------------\
 /    Unit Tests   \  Many, fast, cheap — logic, pure functions
/------------------\
```

Default allocation: 70% unit, 20% integration, 10% E2E. Adjust based on risk.

| Level | What it tests | Tools | Coverage target |
|---|---|---|---|
| **Unit** | Functions, business logic, transformations | Vitest / xUnit / pytest | 80%+ changed code |
| **Integration** | Boundaries, database, API endpoints, handlers | Alba+Testcontainers / Supertest | Critical paths |
| **E2E** | Complete user flows through UI | Playwright / Cypress | Top 5-10 flows |
| **Contract** | API compatibility producer↔consumer | Pact / OpenAPI validation | All public APIs |
| **Performance** | Latency p50/p95/p99, throughput | k6 / Locust | SLA benchmarks |
| **Security** | OWASP, auth/authz, input validation | SAST / security-review skill | Public-facing code |

Not every feature needs all levels. A utility function needs unit tests. A payment flow needs all six.

## Step 3: Stack-Specific Patterns

### TypeScript / Vitest
- `vi.hoisted()` + `vi.mock()` for module-level mocks
- `vi.stubGlobal()` for DOM APIs, clean up in `afterEach`
- No jsdom — tests run in Node
- Always run mode: `CI=true npx vitest run`
- Coverage: `@vitest/coverage-v8` with lcov

### .NET / xUnit
- BDD naming: `WhenDoingSomething`
- NSubstitute mocks, Shouldly assertions
- Integration: Alba + Testcontainers PostgreSQL (real database)
- Every endpoint: unit test + integration test
- Remove background services in test fixtures

### Python / pytest-bdd
- BDD specs > Property-based (Hypothesis) > Unit
- Features use business language, step defs hide infrastructure
- 98%+ line coverage, 80%+ mutation kill rate

## Step 4: Quality Gates

### Pre-Merge (MUST pass)
- [ ] All unit tests pass (exit 0)
- [ ] Integration tests pass
- [ ] Coverage above threshold on changed files
- [ ] No new lint/type-check errors
- [ ] No new security vulnerabilities
- [ ] No lint suppressions without justification

### Pre-Release (MUST pass)
- [ ] E2E tests pass on staging
- [ ] Performance benchmarks met
- [ ] Security review for auth/data changes
- [ ] Accessibility audit for UI changes
- [ ] Documentation updated for behaviour changes

## Step 5: Identify Gaps

1. **Untested paths** — coverage reports showing uncovered branches
2. **Missing edge cases** — empty, null, maximum, concurrent, network failure
3. **Over-tested code** — tests that add cost but not confidence
4. **Flaky tests** — fix or delete immediately
5. **Missing levels** — common gap: lots of unit tests, zero integration tests

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Testing implementation, not behaviour | Test what the system DOES |
| Mocking everything | Real implementations; mock only external boundaries |
| Happy path only | Test error cases, edge cases, boundaries |
| `sleep()` in tests | Proper async waiting or mocked time |
| Flaky tests tolerated | Fix immediately or delete |

## Output Format

```
## Test Strategy: [name]

### Risk Assessment
- Risk profile: [financial/data/reputation/convenience]
- Critical flows: [list]
- Failure modes: [list]

### Test Levels
| Level | Scope | Tools | Coverage | Est. Tests |
|---|---|---|---|---|

### Quality Gates
[Pre-merge + pre-release checklists]

### Gaps
[Currently untested areas]

### Recommendations
[Prioritised improvements]
```

## Related Skills

- `/qa-engineer:generate-tests` — generate individual tests based on this strategy. Define strategy first, then generate tests.
- `/qa-engineer:write-bug-report` — for documenting defects found during test execution.

Use the test strategy template (`templates/test-strategy.md`) for consistent output structure.
