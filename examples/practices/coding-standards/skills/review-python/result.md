# Review Python

Scenario: A developer submits Python code for review with several type safety violations: a function missing a return type annotation, bare `except:` clauses, and a mutable dataclass used for a domain model.

## Prompt

> First, write this file to disk at `user_registration.py`:
> 
> ```python
> from __future__ import annotations
> 
> import os
> from dataclasses import dataclass
> 
> 
> @dataclass
> class UserRecord:
>     username: str
>     email: str
>     created_at: str
> 
> 
> def register_user(username, email):
>     db_url = os.getenv("DB_URL")
>     try:
>         conn = connect(db_url)
>         existing = conn.query("SELECT id FROM users WHERE email = %s", email)
>         if existing:
>             return None
>         user = UserRecord(
>             username=username,
>             email=email,
>             created_at=now(),
>         )
>         conn.insert(user)
>         return user
>     except:
>         return None
> ```
> 
> Then run:
> 
> /coding-standards:review-python user_registration.py

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Python Review

### Summary
- File reviewed: 1
- Type safety: 4 findings
- Data modeling: 1 finding
- Linting: 0 findings
- Configuration: 1 finding
- Error handling: 2 findings (critical)
- Testing: Not applicable (no tests in file)
- Code structure: 0 findings

---

### Findings

#### CRITICAL

**[CRITICAL] Error Handling Pass 5: Bare except swallows exceptions**

**File:** `user_registration.py:28`
**Evidence:**
```python
28	    except:
29	        return None
```
**Standard:** Bare `except:` is prohibited. Always specify exception type(s).
**Fix:** 
```python
except (DatabaseError, ConnectionError) as e:
    logger.error("user registration failed", exc_info=True)
    return None
```

---

#### IMPORTANT

**[IMPORTANT] Type Safety Pass 1: Missing parameter type annotations**

**File:** `user_registration.py:14`
**Evidence:**
```python
14	def register_user(username, email):
```
**Standard:** mypy strict — every parameter must have a type annotation. Only `self` and `cls` are exceptions.
**Fix:**
```python
def register_user(username: str, email: str) -> UserRecord | None:
```

**[IMPORTANT] Type Safety Pass 1: Missing return type annotation**

**File:** `user_registration.py:14`
**Evidence:**
```python
14	def register_user(username, email):
```
**Standard:** mypy strict — every function must have a return type. This function returns `UserRecord` or `None`.
**Fix:** See above — return type should be `UserRecord | None`.

**[IMPORTANT] Data Modeling Pass 2: Dataclass not frozen**

**File:** `user_registration.py:7`
**Evidence:**
```python
7	@dataclass
8	class UserRecord:
9	    username: str
10	    email: str
11	    created_at: str
```
**Standard:** Domain models (structured data representing entities) must use `@dataclass(frozen=True)` for immutability.
**Fix:**
```python
@dataclass(frozen=True)
class UserRecord:
    username: str
    email: str
    created_at: str
```

**[IMPORTANT] Configuration Pass 4: Environment variable in business logic**

**File:** `user_registration.py:15`
**Evidence:**
```python
15	    db_url = os.getenv("DB_URL")
```
**Standard:** Environment variables should be read once in a configuration module, not scattered throughout business logic. This couples the function to environment details.
**Fix:** Extract to a config module:
```python
# config.py
import os

db_url: str = os.getenv("DB_URL") or "postgres://localhost/mydb"

# user_registration.py
from config import db_url

def register_user(username: str, email: str) -> UserRecord | None:
    try:
        conn = connect(db_url)
        # ...
```

**[IMPORTANT] Type Safety Pass 1: Undefined names will fail mypy**

**File:** `user_registration.py:17, 24`
**Evidence:**
```python
17	        conn = connect(db_url)
24	            created_at=now(),
```
**Standard:** Functions `connect()` and `now()` are not imported or defined. mypy strict will error on these.
**Fix:** Import from the appropriate modules:
```python
from database import connect
from datetime import datetime

created_at=datetime.now().isoformat(),
```

---

### Verdict

**REQUEST_CHANGES**

The code has critical issues that violate team standards:

1. **Bare except** swallows all exceptions without logging — impossible to debug failures
2. **Missing type annotations** prevent mypy strict from passing
3. **Undefined functions** will cause immediate runtime errors
4. **Dataclass not frozen** allows mutation of domain data
5. **Config leakage** couples business logic to environment variables

All five issues must be resolved before this code is production-ready.

### Artifacts written

#### `work/user_registration.py`

```
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class UserRecord:
    username: str
    email: str
    created_at: str


def register_user(username, email):
    db_url = os.getenv("DB_URL")
    try:
        conn = connect(db_url)
        existing = conn.query("SELECT id FROM users WHERE email = %s", email)
        if existing:
            return None
        user = UserRecord(
            username=username,
            email=email,
            created_at=now(),
        )
        conn.insert(user)
        return user
    except:
        return None

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-04 |
| Target duration | 28405 ms |
| Target cost | $0.0721 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all seven mandatory passes — none skipped | PASS | Summary lists all seven categories: type safety, data modeling, linting, configuration, error handling, testing, code structure — each with a finding count or status. |
| c2 | Missing return type annotation on `register_user` is flagged as a Pass 1 finding with the specific function signature as evidence | PASS | Finding '[IMPORTANT] Type Safety Pass 1: Missing return type annotation' cites `user_registration.py:14` with evidence `def register_user(username, email):`. |
| c3 | Mutable `@dataclass` (missing `frozen=True`) is flagged as a Pass 2 finding for a domain model class | PASS | Finding '[IMPORTANT] Data Modeling Pass 2: Dataclass not frozen' cites `user_registration.py:7` and shows the `@dataclass` without frozen=True. |
| c4 | Bare `except:` without an exception type is flagged as a critical Pass 5 finding | PASS | Finding '[CRITICAL] Error Handling Pass 5: Bare except swallows exceptions' at `user_registration.py:28`. |
| c5 | Direct `os.getenv` call in business logic is flagged as a Pass 4 configuration finding | PASS | Finding '[IMPORTANT] Configuration Pass 4: Environment variable in business logic' cites `user_registration.py:15` with evidence `db_url = os.getenv("DB_URL")`. |
| c6 | Each finding includes the evidence format — file, evidence, standard, and concrete fix | PASS | Every finding (bare except, missing annotations, frozen dataclass, config, undefined names) contains a File: path, an Evidence: code block, a Standard: sentence, and a Fix: code block. |
| c7 | Output uses the summary template with counts by category | PASS | Summary section shows 'Type safety: 4 findings', 'Data modeling: 1 finding', 'Linting: 0 findings', 'Configuration: 1 finding', 'Error handling: 2 findings', 'Testing: Not applicable', 'Code structure: 0 findings'. |
| c8 | Pass 6 (testing) evaluates whether the changed file has corresponding test coverage, even if no test file was provided in the prompt | PARTIAL | Testing pass is acknowledged in the summary ('Testing: Not applicable (no tests in file)'), but no evaluation of coverage gaps or specific test recommendations is provided. Ceiling capped at PARTIAL. |
| c9 | Output's missing-return-type finding cites `register_user(username, email)` exactly and shows the corrected signature with explicit type annotations (e.g. `def register_user(username: str, email: str) -> User:`) | PASS | Fix shown as `def register_user(username: str, email: str) -> UserRecord \| None:` under the missing return type finding at line 14. |
| c10 | Output's mutable-dataclass finding cites `UserRecord` and shows the fix `@dataclass(frozen=True)` (or `model_config = ConfigDict(frozen=True)` if the project uses Pydantic) with the reasoning that domain models must be immutable | PASS | Finding cites `UserRecord` at line 7 and states 'Domain models (structured data representing entities) must use `@dataclass(frozen=True)` for immutability.' Fix shows `@dataclass(frozen=True)`. |
| c11 | Output's bare-except finding is severity HIGH/critical — explains that bare `except:` catches `KeyboardInterrupt` and `SystemExit`, hides bugs, and prevents proper error handling — with the fix specifying a specific exception type (e.g. `except DatabaseError:`) | PARTIAL | Finding is marked [CRITICAL] and heading says 'Bare except swallows exceptions'. Fix specifies `except (DatabaseError, ConnectionError) as e:` with logging. However, the output never explicitly states that bare `except:` intercepts `KeyboardInterrupt` and `SystemExit` — the specific technical reason required by the criterion is absent. |
| c12 | Output's `os.getenv` finding cites the exact call and recommends moving the config read to a typed config module (Pydantic Settings or equivalent) loaded at startup, not at request time inside business logic | PASS | Finding cites `db_url = os.getenv("DB_URL")` at line 15. Fix proposes a `config.py` module with `db_url: str = os.getenv("DB_URL") or ...` imported into the business logic — module-level load (startup) rather than inline. The type annotation qualifies as 'equivalent' typed config per the criterion. |
| c13 | Output's findings each include severity, pass label (Pass 1, 2, 4, 5), file path, evidence snippet, the standard violated, and a concrete fix code block — not just a list of issues | PASS | Each finding includes severity prefix ([CRITICAL]/[IMPORTANT]), pass label in heading (e.g. 'Pass 5'), File: path, Evidence: code block, Standard: text, and Fix: code block. |
| c14 | Output runs all seven mandatory passes and reports per-pass finding counts in the summary, including passes with zero findings | PASS | Summary reports all 7 categories with explicit counts including 'Linting: 0 findings' and 'Code structure: 0 findings' for zero-finding passes. |
| c15 | Output's missing-type-annotation findings on `username` and `email` parameters are flagged separately from the missing return type — three findings, not one combined | PARTIAL | The output separates the return type into its own finding ('[IMPORTANT] Missing return type annotation') but groups `username` and `email` parameters into a single combined finding ('[IMPORTANT] Missing parameter type annotations'). That produces 2 type-annotation findings, not 3 as the criterion requires. |
| c16 | Output's overall verdict reflects the severity — bare `except:` plus mutable domain model are correctness/safety issues, so REQUEST_CHANGES (not APPROVE) | PASS | Verdict section explicitly states 'REQUEST_CHANGES' and lists bare except and unfrozen dataclass among the five issues requiring resolution before production. |
| c17 | Output addresses Pass 6 (testing) by noting whether `register_user` has corresponding tests and recommending tests for at least the happy path, duplicate registration, and the error path that the bare-except is hiding | FAIL | Testing pass is dismissed with 'Not applicable (no tests in file)' — no recommendation to add tests for the happy path, duplicate-email path, or the error path hidden by the bare except. The criterion requires specific test recommendations, none were provided. |
| c18 | Output flags any other issues — e.g. password handling if implied (not in prompt but commonly adjacent), email validation, idempotency on registration retry — even if speculative | FAIL | The only additional finding beyond the main criteria is undefined names (`connect()` and `now()`). No speculative issues such as missing password field/hashing, email format validation, or idempotency on retry are raised. Ceiling was PARTIAL but output provides no evidence for this. |

### Notes

The review is well-structured and hits the main required findings (bare except, missing annotations, frozen dataclass, config leakage) with proper severity labels, pass numbers, evidence blocks, and fix code. Strengths: all seven passes are enumerated in the summary, the verdict is correct (REQUEST_CHANGES), and most findings are richly formatted. Weaknesses: the bare-except explanation omits the specific technical reason (KeyboardInterrupt/SystemExit interception) the criterion checks for; parameter annotations are grouped into a single finding rather than individually (producing 2 type findings, not 3); the testing pass is entirely dismissed as 'not applicable' instead of recommending concrete test cases for the happy path, duplicate registration, and error paths; and no speculative quality observations (email validation, password handling, idempotency) are offered. These gaps bring the score to ~85%, just clearing the PASS threshold.
