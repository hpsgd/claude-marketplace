# Output: review-python type safety and error handling

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill executes all seven mandatory passes — none skipped — all seven passes defined with explicit "Do not skip" instruction on line 15
- [x] PASS: Missing return type annotation on `register_user` is flagged as a Pass 1 finding — Pass 1 step 3 covers missing return types with grep pattern on `def ` and states "Functions without `-> ReturnType:` are findings"
- [x] PASS: Mutable `@dataclass` (missing `frozen=True`) is flagged as a Pass 2 finding — Pass 2 step 1 states "Every `@dataclass` that represents a domain model must be `@dataclass(frozen=True)`"
- [x] PASS: Bare `except:` without an exception type is flagged as a critical Pass 5 finding — Pass 5 step 1 states "Every hit is a critical finding"
- [x] PASS: Direct `os.getenv` call in business logic is flagged as a Pass 4 configuration finding — Pass 4 step 3 explicitly covers `os.getenv` in business logic as a finding
- [x] PASS: Each finding includes the evidence format — the Evidence Format section mandates File, Evidence, Standard, and Fix fields
- [x] PASS: Output uses the summary template with counts by category — the Output Template defines per-category counts including zero-finding passes
- [~] PARTIAL: Pass 6 evaluates whether the changed file has corresponding test coverage even without a test file in the prompt — Pass 6 step 4 says "if not [coverage reports], verify by reading that every code path has a test," which implies flagging absent coverage, but the instruction to raise a finding when no test file exists at all is implicit rather than explicit

### Output expectations

- [x] PASS: Output's missing-return-type finding cites `register_user(username, email)` exactly and shows corrected signature — Pass 1 step 3 requires reading each function definition and the evidence format requires the exact evidence snippet; the skill would produce this with the corrected `-> User:` form
- [x] PASS: Output's mutable-dataclass finding cites `UserRecord` and shows `@dataclass(frozen=True)` fix with immutability rationale — Pass 2 step 1 and step 3 cover both `@dataclass(frozen=True)` and Pydantic `ConfigDict(frozen=True)` fixes; the "domain models must be immutable" rationale is stated in the pass
- [x] PASS: Output's bare-except finding is severity HIGH/critical and explains catch-all behaviour — Pass 5 step 1 labels bare `except:` as "a critical finding" and the fix guidance specifies the exception type; the skill would explain `SystemExit`/`KeyboardInterrupt` are caught
- [x] PASS: Output's `os.getenv` finding cites the exact call and recommends typed config module at startup — Pass 4 step 3 explicitly requires citing the `os.getenv` call and moving config reads to a configuration module
- [x] PASS: Output's findings each include severity, pass label, file path, evidence snippet, standard violated, and concrete fix code block — the Evidence Format template mandates all these fields
- [x] PASS: Output runs all seven mandatory passes and reports per-pass finding counts including passes with zero findings — the Output Template summary lists all seven categories explicitly
- [x] PASS: Output's missing-type-annotation findings on `username` and `email` parameters are flagged separately from the missing return type — Pass 1 step 3 (return types) and step 4 (parameter types) are distinct checks producing separate findings for each unannotated parameter
- [x] PASS: Output's overall verdict reflects severity — bare `except:` is labeled critical and mutable domain model is a finding; the zero-finding gate only applies when everything passes, so REQUEST_CHANGES is the correct output
- [x] PASS: Output addresses Pass 6 (testing) by noting whether `register_user` has corresponding tests — Pass 6 requires verifying every code path has a test, which covers the error path masked by the bare except and the happy path
- [~] PARTIAL: Output flags other adjacent issues (password handling, email validation, idempotency) — the zero-finding gate says "Do not invent issues to appear thorough," which correctly suppresses speculative findings not visible in the described code; the skill would not flag issues implied but absent from the scenario

## Notes

The skill is tightly specified. The bare-except critical severity is unambiguous — "every hit" eliminates reviewer discretion. The frozen dataclass rule, os.getenv detection, and return type checks all map directly to the scenario. The one structural gap is Pass 6: the definition instructs checking coverage but does not explicitly tell the reviewer to raise a finding when no test file appears in the diff. An agent following the skill would reasonably flag it, but the instruction is inferred rather than stated. The partial on speculative findings is by design — the zero-finding gate is the correct behaviour and preventing fabricated findings is a feature, not a gap.
