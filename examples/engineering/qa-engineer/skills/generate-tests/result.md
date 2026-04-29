# Output: Generate tests for a discount code validation function

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 18/19 criteria met (94.7%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill reads the function completely before writing any test — Step 1 (Reconnaissance) is explicitly marked MANDATORY before writing any test; requires reading inputs, outputs, side effects, and error paths.
- [x] PASS: Skill follows TDD Iron Law — the skill opens with the Iron Law section specifying RED → confirm exit code 1 with meaningful failure message → GREEN → confirm exit code 0. Marked "not a suggestion."
- [x] PASS: Test cases cover all required categories — Step 2 mandates happy path (MUST have) with multiple valid input variations, edge cases including boundary values (MUST have), and error cases including inputs that throw (MUST have). All four error types fall under the error cases category.
- [x] PASS: Tests run in run mode — Step 4 specifies `pytest tests/path/to/test_file.py -v` as the run command, with an explicit note that watch mode is never used.
- [x] PASS: Each test has one assertion — Step 3 mandates "Assert — verify ONE expected outcome"; Anti-Patterns lists "Multiple assertions per test" as never-do.
- [x] PASS: Skill mocks only external boundaries — Anti-Patterns: "Mocking what you own — mock at external boundaries only (HTTP, database, file system). Use real implementations for your own code."
- [x] PASS: Skill uses factories for test data — Python/pytest-bdd section specifies `@pytest.fixture` for test data factories and shared setup; Anti-Patterns: "Inline test data — magic strings and numbers scattered through tests. Use factories."
- [x] PASS: Evidence table is produced with test name, exact command, exit code, and PASS/FAIL result — Evidence Requirements section mandates exactly this table format with all four columns specified.
- [~] PARTIAL: Skill uses Hypothesis for property-based testing — Python/pytest-bdd section references "Hypothesis for property-based testing alongside BDD scenarios" as a rule, but it is not a mandatory step in the main process. Present but not enforced. Score: 0.5.

### Output expectations

- [x] PASS: Output produces tests for every named exception — Error cases are MUST have in Step 2, and Reconnaissance mandates reading all error paths. All four exceptions (`DiscountNotFoundError`, `DiscountExpiredError`, `DiscountAlreadyUsedError`, `DiscountMinimumNotMetError`) are covered by the mandatory error cases category with `pytest.raises` implied by the stack-specific patterns.
- [x] PASS: Output's happy-path tests cover both percentage and fixed discount — Step 2 mandates "Multiple valid input variations if the function branches on input type." The function branches on discount type, so both must appear.
- [x] PASS: Output's edge cases include exact minimum boundary and expiry boundary — Step 2 mandates "Boundary values (min, max, off-by-one, first, last)" as MUST have for edge cases. Both boundary conditions are captured.
- [x] PASS: Output uses `Decimal` for `order_total` and amount values — Reconnaissance (Step 1) requires reading actual inputs and outputs. The function signature uses `Decimal`; tests derived from it must match the type.
- [x] PASS: Output writes RED first — TDD Iron Law is mandatory and requires showing `pytest` with exit code 1 before implementation, then exit code 0.
- [x] PASS: Output mocks only the database lookup boundary — Anti-Patterns explicitly states "mock at external boundaries only (HTTP, database, file system)" and "never mock what you own."
- [x] PASS: Output uses factories or fixtures for Discount, Customer, and DiscountUsage entities — Anti-Patterns bans inline test data with magic strings; Python rules specify `@pytest.fixture` for factories.
- [x] PASS: Output's tests follow one-assertion-per-test — Anti-Patterns bans "Multiple assertions per test" with a clear rationale.
- [x] PASS: Output's evidence table lists every test with name, exact command, exit code, and PASS/FAIL result — Evidence Requirements section mandates this exact four-column format.
- [~] PARTIAL: Output includes Hypothesis property-based tests — Hypothesis is referenced in the Python/pytest-bdd rules but sits outside the mandatory process. An agent following only the mandatory steps may omit it. Score: 0.5.

## Notes

Both PARTIAL criteria point to the same gap: Hypothesis is present in the skill but positioned as a stack-specific rule rather than a mandatory step. An agent following the process strictly could skip it without violating any mandatory marker. Elevating Hypothesis to a numbered step in the Python process section (e.g., Step 2.5 for property-based tests when using pytest) would close this gap. All other criteria are covered by explicit, named mandatory sections or unambiguous anti-patterns.
