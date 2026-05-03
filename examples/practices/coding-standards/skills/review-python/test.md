# Test: review-python type safety and error handling

Scenario: A developer submits Python code for review with several type safety violations: a function missing a return type annotation, bare `except:` clauses, and a mutable dataclass used for a domain model.

## Prompt

First, write this file to disk at `user_registration.py`:

```python
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

Then run:

/coding-standards:review-python user_registration.py

## Criteria

- [ ] PASS: Skill executes all seven mandatory passes — none skipped
- [ ] PASS: Missing return type annotation on `register_user` is flagged as a Pass 1 finding with the specific function signature as evidence
- [ ] PASS: Mutable `@dataclass` (missing `frozen=True`) is flagged as a Pass 2 finding for a domain model class
- [ ] PASS: Bare `except:` without an exception type is flagged as a critical Pass 5 finding
- [ ] PASS: Direct `os.getenv` call in business logic is flagged as a Pass 4 configuration finding
- [ ] PASS: Each finding includes the evidence format — file, evidence, standard, and concrete fix
- [ ] PASS: Output uses the summary template with counts by category
- [ ] PARTIAL: Pass 6 (testing) evaluates whether the changed file has corresponding test coverage, even if no test file was provided in the prompt

## Output expectations

- [ ] PASS: Output's missing-return-type finding cites `register_user(username, email)` exactly and shows the corrected signature with explicit type annotations (e.g. `def register_user(username: str, email: str) -> User:`)
- [ ] PASS: Output's mutable-dataclass finding cites `UserRecord` and shows the fix `@dataclass(frozen=True)` (or `model_config = ConfigDict(frozen=True)` if the project uses Pydantic) with the reasoning that domain models must be immutable
- [ ] PASS: Output's bare-except finding is severity HIGH/critical — explains that bare `except:` catches `KeyboardInterrupt` and `SystemExit`, hides bugs, and prevents proper error handling — with the fix specifying a specific exception type (e.g. `except DatabaseError:`)
- [ ] PASS: Output's `os.getenv` finding cites the exact call and recommends moving the config read to a typed config module (Pydantic Settings or equivalent) loaded at startup, not at request time inside business logic
- [ ] PASS: Output's findings each include severity, pass label (Pass 1, 2, 4, 5), file path, evidence snippet, the standard violated, and a concrete fix code block — not just a list of issues
- [ ] PASS: Output runs all seven mandatory passes and reports per-pass finding counts in the summary, including passes with zero findings
- [ ] PASS: Output's missing-type-annotation findings on `username` and `email` parameters are flagged separately from the missing return type — three findings, not one combined "no annotations"
- [ ] PASS: Output's overall verdict reflects the severity — bare `except:` plus mutable domain model are correctness/safety issues, so REQUEST_CHANGES (not APPROVE)
- [ ] PASS: Output addresses Pass 6 (testing) by noting whether `register_user` has corresponding tests and recommending tests for at least the happy path, duplicate registration, and the error path that the bare-except is hiding
- [ ] PARTIAL: Output flags any other issues — e.g. password handling if implied (not in prompt but commonly adjacent), email validation, idempotency on registration retry — even if speculative
