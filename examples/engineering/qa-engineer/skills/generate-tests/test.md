# Test: Generate tests for a discount code validation function

Scenario: Developer invokes the generate-tests skill targeting a `validate_discount_code` function in Python. The function checks if a code is valid, not expired, not already used by this customer, and applies a percentage or fixed discount.

## Prompt

Generate tests for `src/billing/discount.py::validate_discount_code`. The function signature is `validate_discount_code(code: str, customer_id: UUID, order_total: Decimal) -> DiscountResult`. It should: return a DiscountResult with amount when valid, raise `DiscountNotFoundError` for unknown codes, raise `DiscountExpiredError` for expired codes, raise `DiscountAlreadyUsedError` if this customer already used this code, and raise `DiscountMinimumNotMetError` if the order total is below the discount's minimum.

Implementation requirements:

- **Reconnaissance section** at top — show `find . -path "*billing*" -name "*.py"` and `Read src/billing/discount.py` results before writing tests.
- **Single-assertion-per-test discipline**: each `def test_*` asserts ONE behaviour. If you need to assert "function returns DiscountResult AND amount is correct AND it was called once", that's THREE separate tests.
- **Factories for test data** in `conftest.py`:
  ```python
  @pytest.fixture
  def discount_factory():
      def _make(code="WELCOME10", percent=10, expires=datetime(2030, 1, 1), minimum=Decimal("0")):
          return Discount(code=code, percent=percent, expires_at=expires, minimum_order=minimum)
      return _make
  @pytest.fixture
  def customer_id(): return UUID("00000000-0000-0000-0000-000000000001")
  ```
  No inline `UUID("...")` or `Decimal(...)` repeated across tests — use the fixtures.
- **Tests required (≥10)**: happy path, unknown code, expired code, already used code, minimum not met, plus boundary tests (amount = minimum exactly, expires_at = now exactly, percent at boundaries).
- **Evidence table** with columns `Test name | Command | Exit code | Result (PASS/FAIL)` listing EVERY test individually (not class/run level summary). Show actual `pytest -v src/billing/test_discount.py` output with each test name.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Skill reads the function completely before writing any test — inspects actual inputs, outputs, error types, and side effects
- [ ] PASS: Skill follows TDD Iron Law — writes RED test first, confirms exit code 1 with meaningful failure, then GREEN
- [ ] PASS: Test cases cover all required categories: happy path (valid percentage discount, valid fixed discount), edge cases (minimum order exactly met, code expiring at midnight), and all four error cases
- [ ] PASS: Tests run in run mode (`pytest tests/billing/test_discount.py -v`) — not watch mode
- [ ] PASS: Each test has one assertion — not multiple unrelated assertions in a single test function
- [ ] PASS: Skill mocks only external boundaries (e.g. database call to fetch the discount code) — not the function under test itself
- [ ] PASS: Skill uses factories for test data (discount objects, customer IDs) — no inline magic strings
- [ ] PASS: Evidence table is produced with test name, exact command, exit code, and PASS/FAIL result
- [ ] PARTIAL: Skill uses Hypothesis for property-based testing of the discount amount calculation

## Output expectations

- [ ] PASS: Output produces tests for every named exception in the prompt — `DiscountNotFoundError`, `DiscountExpiredError`, `DiscountAlreadyUsedError`, `DiscountMinimumNotMetError` — each with a focused test that asserts the specific exception type via `pytest.raises`
- [ ] PASS: Output's happy-path tests cover both percentage discount (e.g. 10% off $200 = $20 amount) and fixed discount (e.g. $15 off any qualifying order) — two distinct tests with the resulting `DiscountResult.amount` asserted exactly
- [ ] PASS: Output's edge cases include order_total exactly equal to the minimum (passes) and one cent below the minimum (fails with `DiscountMinimumNotMetError`), and an expiry test at the boundary (one second before expiry passes, at expiry fails)
- [ ] PASS: Output's tests use `Decimal` for `order_total` and amount values — never floats — matching the function's `Decimal` parameter type
- [ ] PASS: Output writes RED first — `pytest tests/billing/test_discount.py -v` shown with exit code 1 and a meaningful failure message before implementation, then GREEN with exit code 0
- [ ] PASS: Output mocks only the database lookup boundary (e.g. `discount_repository.find_by_code`) — never mocks `validate_discount_code` itself or its return value
- [ ] PASS: Output uses factories or fixtures for Discount, Customer, and DiscountUsage entities — no repeated inline construction with magic UUIDs and dates
- [ ] PASS: Output's tests follow one-assertion-per-test — a test that checks both "no exception raised" AND "amount equals X" should split into two if those are unrelated assertions, or use a single combined assertion on `DiscountResult` equality
- [ ] PASS: Output's evidence table lists every test with name, exact command, exit code, and PASS/FAIL result
- [ ] PARTIAL: Output includes Hypothesis property-based tests for the discount amount calculation — properties like "amount is always between 0 and order_total", "percentage discount of 0% returns amount = 0"
