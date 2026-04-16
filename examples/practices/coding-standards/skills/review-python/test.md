# Test: review-python type safety and error handling

Scenario: A developer submits Python code for review with several type safety violations: a function missing a return type annotation, bare `except:` clauses, and a mutable dataclass used for a domain model.

## Prompt

Review `user_registration.py`. The file has a `register_user` function that takes a `username` and `email` param with no type annotations and no return type. There's a `@dataclass` class called `UserRecord` that's not frozen. The error handling uses a bare `except:` clause around the database call, and there's an `os.getenv("DB_URL")` call directly inside the function body rather than through a config module.

## Criteria

- [ ] PASS: Skill executes all seven mandatory passes — none skipped
- [ ] PASS: Missing return type annotation on `register_user` is flagged as a Pass 1 finding with the specific function signature as evidence
- [ ] PASS: Mutable `@dataclass` (missing `frozen=True`) is flagged as a Pass 2 finding for a domain model class
- [ ] PASS: Bare `except:` without an exception type is flagged as a critical Pass 5 finding
- [ ] PASS: Direct `os.getenv` call in business logic is flagged as a Pass 4 configuration finding
- [ ] PASS: Each finding includes the evidence format — file, evidence, standard, and concrete fix
- [ ] PASS: Output uses the summary template with counts by category
- [ ] PARTIAL: Pass 6 (testing) evaluates whether the changed file has corresponding test coverage, even if no test file was provided in the prompt
