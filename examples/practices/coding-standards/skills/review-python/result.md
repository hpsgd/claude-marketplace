# Review python type safety and error handling

A developer submits Python code for review with several type safety violations: a function missing a return type annotation, bare `except:` clauses, and a mutable dataclass used for a domain model.

## Prompt

> Review `user_registration.py`. The file has a `register_user` function that takes a `username` and `email` param with no type annotations and no return type. There's a `@dataclass` class called `UserRecord` that's not frozen. The error handling uses a bare `except:` clause around the database call, and there's an `os.getenv("DB_URL")` call directly inside the function body rather than through a config module.

```markdown

## Output

### Python Review

#### Summary
- Files reviewed: 1 (user_registration.py)
- Type safety: 2 findings (missing return type, missing parameter types)
- Data modeling: 1 finding
- Linting: 0 findings
- Configuration: 1 finding
- Error handling: 1 finding
- Testing: 1 finding (no corresponding test file found)
- Code structure: 0 findings

#### Findings

##### CRITICAL [Pass 5]: Bare except clause


| Field | Value |
|---|---|
| File | `user_registration.py` (database call block) |
| Evidence | `except:` with no exception type specified |
| Standard | Every hit is a critical finding. Always specify the exception type. |
| Fix | `except (DatabaseError, ConnectionError) as e:` — at minimum `except Exception as e:`. Bare `except:` also catches `SystemExit`, `KeyboardInterrupt`, and `GeneratorExit`. |


---

##### IMPORTANT [Pass 1]: Missing return type on `register_user`


| Field | Value |
|---|---|
| File | `user_registration.py` |
| Evidence | `def register_user(username, email):` — no `-> ReturnType:` annotation |
| Standard | Every function must have a return type annotation. Missing return types fail mypy --strict. |
| Fix | `def register_user(username: str, email: str) -> UserRecord:` |


---

##### IMPORTANT [Pass 1]: Missing parameter type annotations


| Field | Value |
|---|---|
| File | `user_registration.py` |
| Evidence | `def register_user(username, email):` — both parameters have no type annotations |
| Standard | Every parameter must have a type annotation. Only `self` and `cls` are exempt. |
| Fix | `def register_user(username: str, email: str) -> UserRecord:` |


---

##### IMPORTANT [Pass 2]: Mutable dataclass used as domain model


| Field | Value |
|---|---|
| File | `user_registration.py` |
| Evidence | `@dataclass` on `UserRecord` without `frozen=True` |
| Standard | Domain models use frozen dataclasses. Mutable dataclasses are acceptable only for configuration or builder patterns — and must have a comment explaining why. |
| Fix | `@dataclass(frozen=True)` |


---

##### IMPORTANT [Pass 4]: Direct os.getenv in business logic


| Field | Value |
|---|---|
| File | `user_registration.py` |
| Evidence | `os.getenv("DB_URL")` inside function body |
| Standard | Environment variables should be read once in a configuration module, not scattered throughout the code. Direct `os.getenv` calls in business logic are findings. |
| Fix | Move to a config module: `from config import db_settings; db_settings.url` |


---

##### SUGGESTION [Pass 6]: No corresponding test file found


| Field | Value |
|---|---|
| File | `user_registration.py` |
| Evidence | No `test_user_registration.py` found in the diff |
| Standard | Every new function needs at least one test covering the happy path and one covering an error case. |
| Fix | Create `tests/test_user_registration.py` with a happy-path test and a duplicate-user or database-error case. |


#### Clean Areas

No linting suppressions (`# noqa`) found. Code structure appears focused — single function with single responsibility.
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/7.5 (100%) |
| Evaluated | 2026-04-16 |


- [x] PASS: All seven mandatory passes executed — the definition states "Execute all seven passes. Do not skip." All seven passes have explicit grep commands; none are conditional
- [x] PASS: Missing return type flagged as Pass 1 finding — Pass 1 step 3 states "every function must have a return type annotation" and includes a grep for `def ` to verify; the `register_user` function matches directly
- [x] PASS: Mutable dataclass flagged as Pass 2 finding — Pass 2 step 1 states "Every `@dataclass` that represents a domain model must be `@dataclass(frozen=True)`. Mutable dataclasses are acceptable only for configuration or builder patterns — and must have a comment explaining why"
- [x] PASS: Bare `except:` flagged as critical Pass 5 finding — Pass 5 step 1 states "grep -rn 'except:' ... Every hit is a critical finding. Always specify the exception type." The severity is explicitly mandated as critical
- [x] PASS: Direct os.getenv flagged as Pass 4 finding — Pass 4 step 3 states "grep -rn 'os\.environ\|os\.getenv' ... Direct `os.getenv` calls in business logic are findings"
- [x] PASS: Evidence format followed — the Evidence Format section defines `File/Evidence/Standard/Fix` as mandatory fields; every finding in the simulated output follows this structure
- [x] PASS: Output uses the summary template — the Output Template section defines exactly the per-category count structure with Summary/Findings/Clean Areas sections
- [~] PARTIAL: Pass 6 evaluates coverage when no test file is provided — Pass 6 step 4 states "If coverage reports are available, check them. If not, verify by reading that every code path has a test." This implies checking even without a test file in the diff, but the definition doesn't explicitly say to flag the absence of a test file as a finding. The behaviour must be inferred from the spirit of the pass. Credit for the mandate existing; partial for the gap in explicit fallback instruction

### Notes

The seven-pass structure is tight. The bare-except critical severity is unambiguous — "every hit" leaves no discretion. The frozen dataclass rule is equally clear. Pass 4's environment variable rule is specific enough to catch the scenario exactly. The one gap is Pass 6's fallback: the definition says to verify coverage exists but doesn't spell out the finding format when no test file appears in the diff at all. An agent would reasonably flag this, but the instruction to do so is implicit rather than explicit.
