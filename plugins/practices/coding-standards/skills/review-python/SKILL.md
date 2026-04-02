---
name: review-python
description: Review Python code against team conventions. Auto-invoked when reviewing .py files.
allowed-tools: Read, Grep, Glob, Bash
paths:
  - "**/*.py"
---

Review Python code against team standards covering type safety, data modeling, testing, linting, configuration, and code structure. Every check has a concrete grep pattern. Every finding requires evidence.

## Mandatory Process

Execute all seven passes. Do not skip.

### Pass 1: Type Safety — mypy Strict

The project runs `mypy --strict`. Code must pass without exceptions.

1. **`Any` usage** — grep for explicit `Any` in type annotations:
   ```bash
   grep -rn '\bAny\b' --include='*.py' [changed files]
   ```
   Every hit is a finding unless it meets one of these conditions:
   - Wrapping a third-party library with no type stubs (must have `# type: ignore[import]` with comment)
   - Callback protocols where the signature is genuinely unknown (rare)

   The fix: define a `Protocol`, use `object`, use a generic `TypeVar`, or create a specific type.

2. **`# type: ignore` audit** — grep for all type ignore comments:
   ```bash
   grep -rn '# type: ignore' --include='*.py' [changed files]
   ```
   Each must specify the error code: `# type: ignore[attr-defined]` not bare `# type: ignore`. Each must have a justification comment on the same or preceding line.

3. **Missing return types** — every function must have a return type annotation. Read each function definition in changed files and verify:
   ```bash
   grep -rn 'def ' --include='*.py' [changed files]
   ```
   Functions without `-> ReturnType:` are findings. This includes `__init__` (should be `-> None`).

4. **Missing parameter types** — every parameter must have a type annotation. Only exception: `self` and `cls`.

5. **`cast()` usage** — grep for `cast(`:
   ```bash
   grep -rn 'cast(' --include='*.py' [changed files]
   ```
   Each is a finding unless the alternative is worse (wrapping a poorly-typed library). Prefer type narrowing with `isinstance`, `TypeGuard`, or `assert`.

6. **String annotations** — use `from __future__ import annotations` at the top of every file, or use modern syntax. Quoted forward references (`"ClassName"`) are acceptable only in files without the future import.

### Pass 2: Data Modeling — Frozen Dataclasses

Domain models use frozen dataclasses. Not mutable classes. Not dicts. Not NamedTuples (unless there is a specific reason).

1. **Dataclass detection** — find all dataclasses in changed files:
   ```bash
   grep -rn '@dataclass' --include='*.py' [changed files]
   ```
   Every `@dataclass` that represents a domain model must be `@dataclass(frozen=True)`. Mutable dataclasses are acceptable only for configuration or builder patterns — and must have a comment explaining why.

2. **Dict-as-model** — grep for `dict[str,` or `Dict[str,` in function signatures. If a function passes around a dict that represents a structured entity, it should be a frozen dataclass instead:
   ```bash
   grep -rn 'dict\[str\|Dict\[str' --include='*.py' [changed files]
   ```

3. **Pydantic models** — if the project uses Pydantic, models should use `model_config = ConfigDict(frozen=True)` for domain objects. Mutable Pydantic models at API boundaries (request/response) are acceptable.

4. **`__post_init__` validation** — frozen dataclasses should use `__post_init__` for validation, not external validator functions. Keep the validation with the data.

### Pass 3: Linting — Ruff Clean

The project uses Ruff. Code must be clean.

1. **No lint suppressions without discussion** — grep for `# noqa`:
   ```bash
   grep -rn '# noqa' --include='*.py' [changed files]
   ```
   Every `# noqa` must:
   - Specify the rule code: `# noqa: E501` not bare `# noqa`
   - Have a justification comment
   - Be discussed in the PR if it is new

2. **Import sorting** — Ruff handles import sorting (isort-compatible). Verify imports follow the convention:
   - Standard library
   - Third-party
   - Local/project
   Each group separated by a blank line.

3. **Line length** — default 88 characters (Black-compatible). Lines over this limit without a `# noqa: E501` are findings. Long strings should use implicit concatenation or parenthesized line breaks.

4. **f-string vs format** — prefer f-strings. `str.format()` and `%` formatting are findings unless required for lazy logging (`logger.info("msg %s", var)` is acceptable for performance).

### Pass 4: Configuration — Kebab-Case Files

1. **Config file naming** — all configuration files (YAML, TOML, JSON, INI) must use kebab-case:
   - **Right**: `app-config.yaml`, `database-settings.toml`
   - **Wrong**: `appConfig.yaml`, `app_config.yaml`, `AppConfig.yaml`

   ```bash
   find . -name '*.yaml' -o -name '*.toml' -o -name '*.json' -o -name '*.ini' | grep -v node_modules | grep -v __pycache__
   ```
   Check each config file name against the convention.

2. **Explicit references** — all references to external resources (file paths, URLs, environment variables, config keys) must use the explicit `{path: ...}` form, not implicit string concatenation:
   - **Right**: `config.get(path="database.connection_string")`
   - **Wrong**: `config["database"]["connection_string"]`

   This applies to the project's specific reference system. Check the codebase for the convention and verify new code follows it.

3. **Environment variable access** — grep for `os.environ` and `os.getenv`:
   ```bash
   grep -rn 'os\.environ\|os\.getenv' --include='*.py' [changed files]
   ```
   Environment variables should be read once in a configuration module, not scattered throughout the code. Direct `os.getenv` calls in business logic are findings.

### Pass 5: Error Handling

1. **Bare except** — grep for `except:` without an exception type:
   ```bash
   grep -rn 'except:' --include='*.py' [changed files]
   ```
   Every hit is a critical finding. Always specify the exception type.

2. **`except Exception: pass`** — grep for pass in except blocks:
   ```bash
   grep -rn 'except.*:' -A1 --include='*.py' [changed files] | grep 'pass'
   ```
   Swallowed exceptions are critical findings. At minimum, log the exception.

3. **Broad except** — `except Exception` at a level where specific exceptions should be caught. Acceptable only at the top-level entry point (CLI main, web request handler).

4. **Exception chaining** — when catching and re-raising, use `raise NewError() from original`:
   ```bash
   grep -rn 'raise.*Error\|raise.*Exception' --include='*.py' [changed files]
   ```
   Re-raises without `from` lose the traceback context.

5. **Custom exceptions** — new exceptions should inherit from a project base exception, not directly from `Exception` or `ValueError`. Check the project for an exception hierarchy.

### Pass 6: Testing — BDD Hierarchy

Tests follow a BDD-style hierarchy: describe the context, then the behavior.

1. **Test naming** — test functions must describe behavior, not implementation:
   - **Right**: `test_when_user_has_no_email_registration_fails`
   - **Wrong**: `test_register`, `test_1`, `test_email_validation`

   ```bash
   grep -rn 'def test_' --include='*.py' [changed test files]
   ```
   Read each test name. It should tell you what scenario is being tested without reading the body.

2. **Test hierarchy** — use `class` grouping for related tests:
   ```python
   class TestUserRegistration:
       class TestWhenEmailIsValid:
           def test_creates_user_in_database(self): ...
           def test_sends_welcome_email(self): ...
       class TestWhenEmailIsDuplicate:
           def test_returns_conflict_error(self): ...
   ```
   Flat test files with 50 `test_` functions are findings — group by scenario.

3. **Testing preference** — the hierarchy of test types, from most to least preferred:
   - BDD-style integration tests (test real behavior through the system)
   - Property-based tests (hypothesis) for pure functions with complex inputs
   - Unit tests for isolated pure logic
   - Mock-heavy tests (last resort, only when external systems cannot be faked)

4. **Coverage targets**:
   - Line coverage: 98%+ on changed files
   - Mutation testing kill rate: 80%+ (if mutation testing is configured)
   If coverage reports are available, check them. If not, verify by reading that every code path has a test.

5. **No test logic** — tests must not contain `if`, `for`, `while`, or `try/except`. A test that branches is testing multiple things.

### Pass 7: Code Structure

1. **Module organization** — each module should have a clear responsibility. A module with 500+ lines needs review.

2. **Import depth** — imports from more than 3 levels deep (`from a.b.c.d.e import X`) suggest the module structure is too deep or the import should go through a public API.

3. **Circular imports** — if you see `TYPE_CHECKING` imports that seem to work around circular dependencies, trace the cycle and flag it.

4. **Global state** — module-level mutable state (lists, dicts, sets defined at module scope that get modified) is a finding:
   ```bash
   grep -rn '^[a-z_].*= \[\]\|^[a-z_].*= {}\|^[a-z_].*= set()' --include='*.py' [changed files]
   ```

## Evidence Format

```
### [SEVERITY] [Pass]: [Short description]

**File:** `path/to/file.py:42`
**Evidence:** [grep output or code]
**Standard:** [which rule is violated]
**Fix:** [concrete code change]
```

## Output Template

```
## Python Review

### Summary
- Files reviewed: N
- Type safety: X findings
- Data modeling: X findings
- Linting: X findings
- Configuration: X findings
- Error handling: X findings
- Testing: X findings
- Code structure: X findings

### Findings
[grouped by severity: critical, important, suggestion]

### Clean Areas
[what was done well]
```

## Zero-Finding Gate

If everything passes: "No findings. Python review complete — all changed files comply with team standards." Do not invent issues to appear thorough.
