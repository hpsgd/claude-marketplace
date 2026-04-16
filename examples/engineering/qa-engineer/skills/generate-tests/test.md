# Test: Generate tests for a discount code validation function

Scenario: Developer invokes the generate-tests skill targeting a `validate_discount_code` function in Python. The function checks if a code is valid, not expired, not already used by this customer, and applies a percentage or fixed discount.

## Prompt

Generate tests for `src/billing/discount.py::validate_discount_code`. The function signature is `validate_discount_code(code: str, customer_id: UUID, order_total: Decimal) -> DiscountResult`. It should: return a DiscountResult with amount when valid, raise `DiscountNotFoundError` for unknown codes, raise `DiscountExpiredError` for expired codes, raise `DiscountAlreadyUsedError` if this customer already used this code, and raise `DiscountMinimumNotMetError` if the order total is below the discount's minimum.

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
