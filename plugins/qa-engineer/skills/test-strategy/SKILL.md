---
name: test-strategy
description: Define a test strategy for a feature, service, or system. Determines what to test, at what level, and what quality gates to enforce.
argument-hint: "[feature, service, or system to define test strategy for]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Define a test strategy for $ARGUMENTS.

## Process

### 1. Understand what's being tested

- What is the feature/service? What does it do?
- What are the critical user flows?
- What are the failure modes? (What would a bug look like to users?)
- What external dependencies exist? (APIs, databases, third-party services)

### 2. Define test levels

For each level, determine what to test and what tools to use:

| Level | What it tests | Tools | Coverage target |
|---|---|---|---|
| **Unit** | Individual functions, business logic | Vitest / xUnit / pytest | 80%+ on new code |
| **Integration** | Component boundaries, API contracts | Alba+Testcontainers / Supertest | Critical paths |
| **E2E** | Complete user flows | Playwright / Cypress | Top 5-10 flows |
| **Contract** | API compatibility | Pact / OpenAPI validation | All public APIs |
| **Performance** | Latency, throughput, resource usage | k6 / Locust | SLA benchmarks |

Not every feature needs all levels. Recommend the appropriate depth.

### 3. Define quality gates

What must pass before merge:
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Coverage above threshold on changed files
- [ ] No new security vulnerabilities (dependency scan)
- [ ] Linting and formatting clean

What must pass before release:
- [ ] E2E tests pass on staging
- [ ] Performance benchmarks met
- [ ] Accessibility audit passed
- [ ] Security review completed (if applicable)

### 4. Identify testing gaps

- What's currently untested that should be?
- What's over-tested (tests that add cost but not confidence)?
- What's flaky and needs fixing?

## Output

Present as a test strategy document:
1. Scope and objectives
2. Test levels with specific recommendations
3. Quality gates (merge and release)
4. Gaps and recommendations
5. Tools and infrastructure needed
