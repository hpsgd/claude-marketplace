---
description: General testing principles — applies across all languages and frameworks
paths:
  - "**/*.test.*"
  - "**/*.spec.*"
  - "**/tests/**"
  - "**/__tests__/**"
---

# Testing Conventions

## General principles
- New or modified code **must** have unit tests
- When changing a file with testable logic (pure functions, utilities, data transformations), add or update tests
- Test location: co-located alongside source (`*.test.ts` / `*.test.py`)
- Keep test coverage for changed files above 80%
- Extract pure functions for testability

## [Vitest](https://vitest.dev) (TypeScript)
- Import from `vitest`: `import { describe, expect, it, vi } from 'vitest'`
- Module mocking: `vi.hoisted()` + `vi.mock()` for module-level mocks
- Global stubs: `vi.stubGlobal()` for `fetch`, `document`, etc. Clean up with `vi.unstubAllGlobals()` in `afterEach`
- No jsdom: tests run in Node — mock DOM APIs via `vi.stubGlobal` when needed
- Coverage: `@vitest/coverage-v8` with lcov output (consumed by [SonarCloud](https://sonarcloud.io))

## Writing tests
- Each test should verify one behavior — keep tests focused
- Use descriptive test names that read as sentences: `it('returns null when user is not found')`
- Follow Arrange-Act-Assert (AAA) pattern
- Prefer real implementations over mocks — mock only external boundaries (network, filesystem, time)
- When mocking is necessary, prefer dependency injection over module mocking

## Assertions
- Use specific assertions: `toEqual` over `toBeTruthy`, `toHaveLength` over checking `.length`
- Assert on the most specific thing possible — don't just check that something is defined
- For error cases, assert on the error type and message, not just that an error was thrown

## Test data
- Use factory functions or builders for test data rather than inline object literals
- Keep test data minimal — only include fields relevant to the test
- Avoid shared mutable state between tests

## External dependencies
- Abstract external dependencies (HTTP, AI/LLM, email) behind interfaces
- Provide stub/fake implementations for tests
- Every new component accepting an external dependency must use constructor injection
