---
name: generate-tests
description: Generate test cases and test code for a function, component, endpoint, or feature.
argument-hint: "[file, function, or component to test]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Generate tests for $ARGUMENTS.

## TDD Iron Law

**No production code without a failing test first.** This is not a suggestion. This is the process:

1. **RED:** Write a test that fails. Run it. Confirm exit code 1. Confirm the failure message is meaningful (not a syntax error or import error)
2. **GREEN:** Write the minimum code to make the test pass. Run it. Confirm exit code 0
3. **REFACTOR:** Clean up. Run tests again. Confirm still exit code 0

### Vertical Slicing (MANDATORY)

RED-GREEN per feature slice, not all RED then all GREEN:
- CORRECT: test1 -> impl1, test2 -> impl2, test3 -> impl3
- WRONG: test1, test2, test3 ... impl1, impl2, impl3

Each slice must be a complete behaviour. Never leave more than one test failing at a time.

### Failure Caps

- **GREEN phase:** If the same test fails 3 consecutive times after code changes, STOP. The test or the approach is wrong. Do not attempt a 4th fix. Step back, re-read the test, re-read the requirement, check assumptions. Escalate with the 3 failure messages as evidence
- **Build/lint loop:** If the same linter or type-checker error recurs after 3 fix attempts (same error code, same file), STOP. Report the error and the 3 attempts

## Process

### Step 1: Reconnaissance (MANDATORY before writing any test)

1. Read the code under test completely — inputs, outputs, side effects, error paths, edge cases
2. Identify the public API surface — what can callers invoke?
3. Find existing tests in the project to match conventions:
   - Test runner (Vitest, Jest, xUnit, pytest, pytest-bdd)
   - File location pattern (co-located vs separate `tests/` directory)
   - Naming conventions (describe/it, test classes, BDD scenarios)
   - Assertion library (expect, Shouldly, assert, pytest assertions)
   - Mock strategy (vi.mock, NSubstitute, unittest.mock, pytest fixtures)
   - Factory patterns for test data

### Step 2: Test Case Identification

For every function/component/endpoint, identify these categories:

**Happy path (MUST have):**
- Primary use case with valid inputs producing expected output
- Multiple valid input variations if the function branches on input type

**Edge cases (MUST have):**
- Empty inputs (null, undefined, empty string, empty array, zero)
- Boundary values (min, max, off-by-one, first, last)
- Single-element collections
- Unicode and special characters where strings are accepted

**Error cases (MUST have):**
- Invalid inputs that should throw or return errors
- Missing required fields
- Type mismatches (if dynamically typed)
- Network/IO failures (for async operations)
- Timeout and cancellation scenarios

**State transitions (if applicable):**
- Before/after side effects
- Idempotency — calling twice produces the same result
- Concurrent access (if relevant)

### Step 3: Write Tests

Follow this structure for every test:

```
Arrange — set up preconditions and inputs
Act     — invoke the behaviour under test (ONE action)
Assert  — verify ONE expected outcome
```

### Step 4: Run and Verify

Run tests using the correct runner in **run mode** (never watch mode):

```bash
# TypeScript/Vitest
CI=true npx vitest run path/to/file.test.ts

# TypeScript/Jest
CI=true npx jest path/to/file.test.ts

# .NET/xUnit
dotnet test --filter "FullyQualifiedName~ClassName"

# Python/pytest
pytest tests/path/to/test_file.py -v
```

After every test run, verify no orphaned processes:
```bash
pgrep -f "vitest|jest" || echo "Clean"
```

## Stack-Specific Patterns

### TypeScript / Vitest

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Hoist mocks BEFORE imports
const mockDependency = vi.hoisted(() => ({
  doThing: vi.fn(),
}));

vi.mock('./dependency', () => ({ dependency: mockDependency }));

describe('MyFunction', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('returns null when user is not found', async () => {
    // Arrange
    mockDependency.doThing.mockResolvedValue(null);

    // Act
    const result = await myFunction('nonexistent-id');

    // Assert
    expect(result).toBeNull();
  });
});
```

Rules:
- `vi.hoisted()` + `vi.mock()` for module mocks — never inline factory without hoisting
- No `jsdom` environment — test logic, not DOM
- Co-located test files: `my-function.test.ts` next to `my-function.ts`
- Use `vi.fn()` for function mocks, `vi.spyOn()` for partial mocks
- `beforeEach(() => vi.clearAllMocks())` to prevent state leakage

### .NET / xUnit

```csharp
public class WhenCreatingANewSource
{
    [Fact]
    public async Task it_returns_the_created_source()
    {
        // Arrange
        var command = SourceFactory.CreateCommand();
        var handler = new CreateSourceHandler(
            Substitute.For<IDocumentSession>());

        // Act
        var result = handler.Handle(command);

        // Assert
        result.ShouldNotBeNull();
        result.Name.ShouldBe(command.Name);
    }
}
```

Rules:
- BDD-style class naming: `WhenDoingSomething`, `GivenSomeState`
- NSubstitute for mocks (`Substitute.For<T>()`)
- Shouldly for assertions (`ShouldBe`, `ShouldNotBeNull`, `ShouldThrow`)
- Alba for HTTP integration tests (full pipeline, real routing)
- Factory classes for test data (e.g., `SourceFactory.Create()`)
- Separate unit test project from integration test project

### Python / pytest-bdd

```python
# tests/features/user_login.feature
Feature: User login
  Scenario: Successful login with valid credentials
    Given a registered user with email "test@example.com"
    When the user logs in with correct password
    Then the response contains a valid access token

# tests/step_defs/test_user_login.py
from pytest_bdd import given, when, then, scenarios

scenarios('../features/user_login.feature')

@given('a registered user with email "test@example.com"')
def registered_user(db_session):
    return UserFactory.create(email="test@example.com")

@when('the user logs in with correct password')
def login(client, registered_user):
    return client.post('/login', json={...})

@then('the response contains a valid access token')
def verify_token(login):
    assert login.status_code == 200
    assert 'access_token' in login.json()
```

Rules:
- Gherkin features for behaviour specs, step definitions for implementation
- Business language in `.feature` files — no infrastructure details
- Reuse step definitions across features via `conftest.py`
- Hypothesis for property-based testing alongside BDD scenarios
- `@pytest.fixture` for test data factories and shared setup

## Anti-Patterns (NEVER do these)

- **Multiple assertions per test** — when it fails, you don't know which behaviour broke
- **Testing implementation details** — verifying mock call counts, internal state, private methods
- **Shared mutable state** — tests that depend on execution order or modify shared objects
- **Inline test data** — magic strings and numbers scattered through tests. Use factories
- **Mocking what you own** — mock at external boundaries only (HTTP, database, file system). Use real implementations for your own code
- **Sleep in tests** — use polling with timeout, fake timers, or async await. `sleep(1000)` is a race condition
- **Testing the framework** — don't test that React renders or that Express routes. Test your logic
- **Snapshot overuse** — snapshots are for catching unintended changes, not for replacing real assertions
- **Ignoring flaky tests** — a flaky test is a bug. Fix it or delete it. Never skip and forget

## Evidence Requirements

Every test generation output MUST include:

```
### Evidence

| Test | Command | Exit | Result |
|---|---|---|---|
| [test name] | [exact command] | [0/1] | [PASS/FAIL: message] |

### Coverage Summary

- Happy path scenarios: [count] tested
- Edge cases: [count] tested
- Error cases: [count] tested
- Total tests: [count] passing, [count] failing, [count] skipped
```

**"Tests pass" without an exit code is not evidence.** Every claim requires the exact command and its exit code.

## Output

Deliver:
1. Test file(s) following project conventions
2. Any required test fixtures or factories
3. Evidence table with commands and exit codes
4. List of any test cases intentionally deferred (with justification)

## Related Skills

- `/qa-engineer:write-bug-report` — when tests reveal defects, write a structured bug report.
- `/qa-lead:test-strategy` — for defining the overall test strategy before generating individual tests.
