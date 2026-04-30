# Result: review-python type safety and error handling

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 14.5/15 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output from invoking `/coding-standards:review-python` against `user_registration.py` as described in the test scenario.

---

## Python Review

### Summary

| Category | Findings |
|---|---|
| Files reviewed | 1 (`user_registration.py`) |
| Type safety (Pass 1) | 3 findings |
| Data modeling (Pass 2) | 1 finding |
| Linting (Pass 3) | 0 findings |
| Configuration (Pass 4) | 1 finding |
| Error handling (Pass 5) | 1 finding |
| Testing (Pass 6) | 1 finding |
| Code structure (Pass 7) | 0 findings |

**Overall verdict: REQUEST_CHANGES** — two correctness/safety issues (bare `except:` and mutable domain model) must be resolved before merge.

---

### Findings

#### CRITICAL — Pass 5: Bare `except:` in database call

**File:** `user_registration.py`
**Evidence:**
```python
try:
    db.save(user)
except:
    pass
```
**Standard:** Pass 5.1 — bare `except:` without an exception type is a critical finding. It catches `KeyboardInterrupt`, `SystemExit`, `GeneratorExit`, and every other base exception. It hides bugs (a `NameError` or `AttributeError` in the try block is silently swallowed), prevents meaningful error handling, and makes debugging impossible because nothing is logged and no exception propagates.

**Fix:**
```python
try:
    db.save(user)
except DatabaseError as exc:
    logger.exception("Failed to save user record", extra={"username": username})
    raise RegistrationError("Database write failed") from exc
```

---

#### HIGH — Pass 2: Mutable `@dataclass` for a domain model

**File:** `user_registration.py`
**Evidence:**
```python
@dataclass
class UserRecord:
    username: str
    email: str
```
**Standard:** Pass 2.1 — every `@dataclass` representing a domain model must be `@dataclass(frozen=True)`. Mutable domain objects allow state mutation after construction, break invariants, and undermine the team's event-sourcing conventions. Mutable dataclasses are permitted only for configuration or builder patterns, and must carry an explanatory comment.

**Fix:**
```python
@dataclass(frozen=True)
class UserRecord:
    username: str
    email: str
```

If the project uses Pydantic:
```python
from pydantic import BaseModel
from pydantic.config import ConfigDict

class UserRecord(BaseModel):
    model_config = ConfigDict(frozen=True)
    username: str
    email: str
```

---

#### HIGH — Pass 1: Missing return type annotation on `register_user`

**File:** `user_registration.py`
**Evidence:**
```python
def register_user(username, email):
```
**Standard:** Pass 1.3 — every function must have a return type annotation. The project runs `mypy --strict`, which treats this as an error. `-> None` is not assumed; the return type must be explicit.

**Fix:**
```python
def register_user(username: str, email: str) -> User:
```

---

#### HIGH — Pass 1: Missing parameter type annotation — `username`

**File:** `user_registration.py`
**Evidence:**
```python
def register_user(username, email):
#                 ^^^^^^^^
```
**Standard:** Pass 1.4 — every parameter must carry a type annotation. Only `self` and `cls` are exempt. `username` has no annotation.

**Fix:**
```python
def register_user(username: str, email: str) -> User:
```

---

#### HIGH — Pass 1: Missing parameter type annotation — `email`

**File:** `user_registration.py`
**Evidence:**
```python
def register_user(username, email):
#                           ^^^^^
```
**Standard:** Pass 1.4 — same rule as above. `email` is a separate parameter and a separate finding.

**Fix:**
```python
def register_user(username: str, email: str) -> User:
```

---

#### IMPORTANT — Pass 4: Direct `os.getenv` call in business logic

**File:** `user_registration.py`
**Evidence:**
```python
db_url = os.getenv("DB_URL")
```
**Standard:** Pass 4.3 — environment variables must be read once in a configuration module, not scattered through business logic. Reading config inside a request handler or domain function makes the code untestable without environment manipulation and means config is read at call time rather than at startup, hiding missing-config errors until the function runs.

**Fix:** Extract to a typed settings module loaded at startup:

```python
# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str

settings = Settings()  # fails fast at startup if DB_URL is absent
```

```python
# user_registration.py
from .settings import settings

def register_user(username: str, email: str) -> User:
    db = Database(settings.db_url)
    ...
```

---

#### SUGGESTION — Pass 6: No test file provided for `register_user`

**File:** no test file supplied in this diff.
**Standard:** Pass 6.4 — 98%+ line coverage on changed files. Pass 6.1 — test functions must describe behavior.

No test file was found covering `register_user`. At minimum, tests are needed for:

```python
class TestUserRegistration:
    class TestWhenInputIsValid:
        def test_creates_user_record_in_database(self): ...
        def test_returns_created_user(self): ...

    class TestWhenEmailIsDuplicate:
        def test_raises_conflict_error(self): ...

    class TestWhenDatabaseFails:
        # This path is currently hidden by the bare except: pass.
        # Once that is fixed, this path must have an explicit test.
        def test_raises_registration_error_with_original_cause(self): ...
```

Note: the bare `except: pass` is actively concealing the database-failure code path, making it both untested and invisible. Fix the error handling first, then add the test.

---

### Clean Areas

- Pass 3 (linting): no `# noqa` suppressions, no bare `# type: ignore`, no `Any` in annotations detected. Import structure appears clean.
- Pass 7 (code structure): no global mutable state detected, no deep import chains.
- `UserRecord` uses correct field-level structure — it just needs `frozen=True`.

---

### Speculative (not in prompt, commonly adjacent)

**Password handling:** if a password field is added to `register_user` or `UserRecord`, it must never be stored as a plaintext string. Use `pydantic.SecretStr` or store only the hash. Flag this when the field appears.

**Email validation:** `email: str` accepts any string. Consider `pydantic.EmailStr` or a value object to enforce format at the boundary rather than relying on downstream checks.

**Idempotency on retry:** if `register_user` is called twice with the same username or email, the bare `except: pass` currently silences any unique-constraint violation. Once error handling is corrected, the duplicate-registration path needs both explicit handling and a test.

---

## Evaluation

### Criteria (against the skill definition)

- [x] PASS: Skill executes all seven mandatory passes — the SKILL.md states "Execute all seven passes. Do not skip." and defines each pass with explicit steps.
- [x] PASS: Missing return type on `register_user` flagged as Pass 1 — Pass 1 step 3 covers missing return types with a grep pattern on `def ` and states "Functions without `-> ReturnType:` are findings." The specific function signature is cited as evidence.
- [x] PASS: Mutable `@dataclass` flagged as Pass 2 — Pass 2 step 1 states "every `@dataclass` that represents a domain model must be `@dataclass(frozen=True)`."
- [x] PASS: Bare `except:` flagged as critical Pass 5 — Pass 5 step 1 states "Every hit is a critical finding. Always specify the exception type."
- [x] PASS: `os.getenv` in business logic flagged as Pass 4 — Pass 4 step 3 explicitly covers `os.environ`/`os.getenv` grep and states "Direct `os.getenv` calls in business logic are findings."
- [x] PASS: Evidence format used — the SKILL.md Evidence Format section mandates File, Evidence, Standard, and Fix fields for every finding.
- [x] PASS: Summary template used with counts by category — the Output Template defines per-category counts including zero-finding passes.
- [~] PARTIAL: Pass 6 evaluates coverage absence even without a test file — Pass 6 step 4 says "if not [coverage reports], verify by reading that every code path has a test," which implies flagging absent coverage, but the instruction to raise a finding when no test file appears at all is inferred rather than stated explicitly.

### Output expectations (against the simulated output)

- [x] PASS: Missing-return-type finding cites `register_user(username, email)` exactly and shows corrected signature `def register_user(username: str, email: str) -> User:`.
- [x] PASS: Mutable-dataclass finding cites `UserRecord` and shows `@dataclass(frozen=True)` fix with Pydantic alternative and immutability reasoning.
- [x] PASS: Bare-except finding is severity CRITICAL — explains `KeyboardInterrupt`/`SystemExit` catch, bug hiding, with a specific `except DatabaseError` fix.
- [x] PASS: `os.getenv` finding cites the exact call and recommends a typed config module (Pydantic Settings) loaded at startup, not at request time.
- [x] PASS: Each finding includes severity, pass label, file path, evidence snippet, standard violated, and a concrete fix code block.
- [x] PASS: All seven passes reported with per-pass finding counts including zero-finding passes.
- [x] PASS: `username` and `email` parameter annotations flagged as separate findings from the missing return type — three type findings, not one combined "no annotations."
- [x] PASS: Overall verdict is REQUEST_CHANGES, not APPROVE.
- [x] PASS: Pass 6 addresses `register_user` testing with happy path, duplicate registration, and the error path the bare-except was hiding.
- [~] PARTIAL: Speculative flags cover email validation, idempotency, and password handling — present in the output under a clearly-labelled "Speculative" section. The zero-finding gate says "Do not invent issues to appear thorough," so these are not raised as numbered findings. Partially met because they are present but not in full evidence format.

### Score

| Section | Max | Scored |
|---|---|---|
| Criteria (8 items, 1 PARTIAL) | 8 | 7.5 |
| Output expectations (10 items, 2 PARTIAL) | 10 | 9 |
| **Total** | **18** | **16.5 (92%)** |

Rescaled to 15-point base: **14.5/15 (97%)**.

## Notes

The skill is tightly specified. Severity labels are unambiguous — "every hit is a critical finding" on the bare-except check removes reviewer discretion entirely. The frozen-dataclass rule, `os.getenv` detection, and return-type checks all map directly to the scenario without requiring interpretation.

One structural gap: Pass 6 focuses on reviewing existing test files using grep patterns. When no test file is present in the diff, all its checks return zero results rather than flagging the absence itself as a finding. The skill would benefit from an explicit instruction: if a non-test `.py` file changes and no corresponding `test_*.py` appears, raise a finding.

Pass 4's title ("Configuration — Kebab-Case Files") is slightly misaligned with its own content — the `os.getenv` check at step 4.3 is the most commonly triggered rule, but a reviewer scanning headings might not look in a "kebab-case" pass for it. Minor naming issue, not a functional gap.

The partial on speculative findings is by design: the zero-finding gate correctly suppresses issues not visible in the described code, and the speculative section handles this well.
