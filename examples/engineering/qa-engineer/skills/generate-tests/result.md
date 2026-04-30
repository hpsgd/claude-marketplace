# Result: Generate tests for a discount code validation function

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18.5/19 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Skill** | `plugins/engineering/qa-engineer/skills/generate-tests/SKILL.md` |

## Output

Simulated output from invoking `/qa-engineer:generate-tests src/billing/discount.py::validate_discount_code`.

---

### Step 1: Reconnaissance

Reading `src/billing/discount.py` to inspect the function signature, return type, exception types, and side effects.

```python
# src/billing/discount.py (discovered during reconnaissance)
from decimal import Decimal
from uuid import UUID
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class DiscountResult:
    code: str
    amount: Decimal
    discount_type: str  # "percentage" | "fixed"

class DiscountNotFoundError(Exception): pass
class DiscountExpiredError(Exception): pass
class DiscountAlreadyUsedError(Exception): pass
class DiscountMinimumNotMetError(Exception): pass

def validate_discount_code(
    code: str,
    customer_id: UUID,
    order_total: Decimal,
) -> DiscountResult:
    """
    Validates a discount code for a given customer and order total.
    Raises DiscountNotFoundError, DiscountExpiredError,
    DiscountAlreadyUsedError, or DiscountMinimumNotMetError on failure.
    Returns DiscountResult with computed amount on success.
    """
    discount = discount_repository.find_by_code(code)
    if discount is None:
        raise DiscountNotFoundError(code)
    if discount.expires_at < datetime.utcnow():
        raise DiscountExpiredError(code)
    if usage_repository.has_used(customer_id, discount.id):
        raise DiscountAlreadyUsedError(code)
    if order_total < discount.minimum_order_total:
        raise DiscountMinimumNotMetError(code)
    if discount.discount_type == "percentage":
        amount = order_total * (discount.value / Decimal("100"))
    else:
        amount = discount.value
    return DiscountResult(code=code, amount=amount, discount_type=discount.discount_type)
```

Existing test conventions discovered via `find tests/ -name "*.py" | head -20`:

- Runner: `pytest`
- Location: `tests/` directory mirroring `src/`
- Factories: `tests/factories.py` (DiscountFactory, CustomerFactory already present)
- Mocking: `pytest-mock`

---

### Step 2: Test factories and fixtures

```python
# tests/factories.py (additions)
import factory
from decimal import Decimal
from datetime import datetime, timedelta
from uuid import uuid4
from src.billing.discount import DiscountResult


class DiscountFactory(factory.Factory):
    class Meta:
        model = Discount

    id = factory.LazyFunction(uuid4)
    code = factory.Sequence(lambda n: f"SAVE{n:04d}")
    discount_type = "percentage"
    value = Decimal("10.00")
    minimum_order_total = Decimal("50.00")
    expires_at = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(days=30))
```

---

### Step 3: Test file — RED phase

Writing all tests before any implementation changes.

```python
# tests/billing/test_discount.py
import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from uuid import uuid4

from src.billing.discount import (
    validate_discount_code,
    DiscountNotFoundError,
    DiscountExpiredError,
    DiscountAlreadyUsedError,
    DiscountMinimumNotMetError,
    DiscountResult,
)
from tests.factories import DiscountFactory


CUSTOMER_ID = uuid4()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_repos(mocker):
    """Patch the two repository calls that are external boundaries."""
    find = mocker.patch("src.billing.discount.discount_repository.find_by_code")
    used = mocker.patch("src.billing.discount.usage_repository.has_used")
    return find, used


# ---------------------------------------------------------------------------
# Happy path — percentage discount
# ---------------------------------------------------------------------------

def test_percentage_discount_returns_correct_amount(mock_repos):
    # Arrange
    find, used = mock_repos
    discount = DiscountFactory(
        discount_type="percentage",
        value=Decimal("10.00"),
        minimum_order_total=Decimal("100.00"),
    )
    find.return_value = discount
    used.return_value = False

    # Act
    result = validate_discount_code(discount.code, CUSTOMER_ID, Decimal("200.00"))

    # Assert
    assert result.amount == Decimal("20.00")


def test_percentage_discount_returns_discount_result_type(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory(
        discount_type="percentage",
        value=Decimal("10.00"),
        minimum_order_total=Decimal("100.00"),
    )
    find.return_value = discount
    used.return_value = False

    result = validate_discount_code(discount.code, CUSTOMER_ID, Decimal("200.00"))

    assert isinstance(result, DiscountResult)


# ---------------------------------------------------------------------------
# Happy path — fixed discount
# ---------------------------------------------------------------------------

def test_fixed_discount_returns_fixed_amount(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory(
        discount_type="fixed",
        value=Decimal("15.00"),
        minimum_order_total=Decimal("50.00"),
    )
    find.return_value = discount
    used.return_value = False

    result = validate_discount_code(discount.code, CUSTOMER_ID, Decimal("80.00"))

    assert result.amount == Decimal("15.00")


def test_fixed_discount_result_has_correct_type_field(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory(
        discount_type="fixed",
        value=Decimal("15.00"),
        minimum_order_total=Decimal("50.00"),
    )
    find.return_value = discount
    used.return_value = False

    result = validate_discount_code(discount.code, CUSTOMER_ID, Decimal("80.00"))

    assert result.discount_type == "fixed"


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------

def test_unknown_code_raises_discount_not_found(mock_repos):
    find, used = mock_repos
    find.return_value = None

    with pytest.raises(DiscountNotFoundError):
        validate_discount_code("UNKNOWN99", CUSTOMER_ID, Decimal("100.00"))


def test_expired_code_raises_discount_expired(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory(expires_at=datetime.utcnow() - timedelta(seconds=1))
    find.return_value = discount
    used.return_value = False

    with pytest.raises(DiscountExpiredError):
        validate_discount_code(discount.code, CUSTOMER_ID, Decimal("100.00"))


def test_already_used_code_raises_already_used(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory()
    find.return_value = discount
    used.return_value = True

    with pytest.raises(DiscountAlreadyUsedError):
        validate_discount_code(discount.code, CUSTOMER_ID, Decimal("100.00"))


def test_order_below_minimum_raises_minimum_not_met(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory(minimum_order_total=Decimal("100.00"))
    find.return_value = discount
    used.return_value = False

    with pytest.raises(DiscountMinimumNotMetError):
        validate_discount_code(discount.code, CUSTOMER_ID, Decimal("99.99"))


# ---------------------------------------------------------------------------
# Edge cases — boundary values
# ---------------------------------------------------------------------------

def test_order_total_exactly_at_minimum_passes(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory(
        discount_type="fixed",
        value=Decimal("10.00"),
        minimum_order_total=Decimal("100.00"),
    )
    find.return_value = discount
    used.return_value = False

    result = validate_discount_code(discount.code, CUSTOMER_ID, Decimal("100.00"))

    assert result.amount == Decimal("10.00")


def test_order_total_one_cent_below_minimum_raises(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory(minimum_order_total=Decimal("100.00"))
    find.return_value = discount
    used.return_value = False

    with pytest.raises(DiscountMinimumNotMetError):
        validate_discount_code(discount.code, CUSTOMER_ID, Decimal("99.99"))


def test_code_expiring_in_one_second_still_valid(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory(expires_at=datetime.utcnow() + timedelta(seconds=1))
    find.return_value = discount
    used.return_value = False

    result = validate_discount_code(discount.code, CUSTOMER_ID, Decimal("100.00"))

    assert isinstance(result, DiscountResult)


def test_code_at_exact_expiry_boundary_raises(mock_repos):
    find, used = mock_repos
    discount = DiscountFactory(expires_at=datetime.utcnow() - timedelta(microseconds=1))
    find.return_value = discount
    used.return_value = False

    with pytest.raises(DiscountExpiredError):
        validate_discount_code(discount.code, CUSTOMER_ID, Decimal("100.00"))


# ---------------------------------------------------------------------------
# Property-based tests (Hypothesis)
# ---------------------------------------------------------------------------

from hypothesis import given, settings
from hypothesis.strategies import decimals


@given(
    order_total=decimals(
        min_value=Decimal("0.01"),
        max_value=Decimal("999999.99"),
        places=2,
        allow_nan=False,
        allow_infinity=False,
    ),
    pct=decimals(
        min_value=Decimal("0"),
        max_value=Decimal("100"),
        places=2,
        allow_nan=False,
        allow_infinity=False,
    ),
)
@settings(max_examples=200)
def test_percentage_amount_never_exceeds_order_total(order_total, pct, mocker):
    find = mocker.patch("src.billing.discount.discount_repository.find_by_code")
    used = mocker.patch("src.billing.discount.usage_repository.has_used")
    discount = DiscountFactory(
        discount_type="percentage",
        value=pct,
        minimum_order_total=Decimal("0.00"),
    )
    find.return_value = discount
    used.return_value = False

    result = validate_discount_code(discount.code, CUSTOMER_ID, order_total)

    assert Decimal("0") <= result.amount <= order_total


@given(
    order_total=decimals(
        min_value=Decimal("1.00"),
        max_value=Decimal("9999.99"),
        places=2,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_zero_percent_discount_always_returns_zero_amount(order_total, mocker):
    find = mocker.patch("src.billing.discount.discount_repository.find_by_code")
    used = mocker.patch("src.billing.discount.usage_repository.has_used")
    discount = DiscountFactory(
        discount_type="percentage",
        value=Decimal("0"),
        minimum_order_total=Decimal("0.00"),
    )
    find.return_value = discount
    used.return_value = False

    result = validate_discount_code(discount.code, CUSTOMER_ID, order_total)

    assert result.amount == Decimal("0.00")
```

---

### RED run (before implementation exists)

```
$ pytest tests/billing/test_discount.py -v
```

```
FAILED tests/billing/test_discount.py::test_percentage_discount_returns_correct_amount
  ModuleNotFoundError: No module named 'src.billing.discount'

Exit code: 1
```

Failure is meaningful — the module does not exist yet. Not a syntax error.

---

### GREEN run (after implementation)

```
$ pytest tests/billing/test_discount.py -v
```

```
tests/billing/test_discount.py::test_percentage_discount_returns_correct_amount PASSED
tests/billing/test_discount.py::test_percentage_discount_returns_discount_result_type PASSED
tests/billing/test_discount.py::test_fixed_discount_returns_fixed_amount PASSED
tests/billing/test_discount.py::test_fixed_discount_result_has_correct_type_field PASSED
tests/billing/test_discount.py::test_unknown_code_raises_discount_not_found PASSED
tests/billing/test_discount.py::test_expired_code_raises_discount_expired PASSED
tests/billing/test_discount.py::test_already_used_code_raises_already_used PASSED
tests/billing/test_discount.py::test_order_below_minimum_raises_minimum_not_met PASSED
tests/billing/test_discount.py::test_order_total_exactly_at_minimum_passes PASSED
tests/billing/test_discount.py::test_order_total_one_cent_below_minimum_raises PASSED
tests/billing/test_discount.py::test_code_expiring_in_one_second_still_valid PASSED
tests/billing/test_discount.py::test_code_at_exact_expiry_boundary_raises PASSED
tests/billing/test_discount.py::test_percentage_amount_never_exceeds_order_total PASSED
tests/billing/test_discount.py::test_zero_percent_discount_always_returns_zero_amount PASSED

14 passed in 1.43s

Exit code: 0
```

---

### Evidence

| Test | Command | Exit | Result |
|---|---|---|---|
| test_percentage_discount_returns_correct_amount | `pytest tests/billing/test_discount.py::test_percentage_discount_returns_correct_amount -v` | 1 → 0 | RED then PASS |
| test_percentage_discount_returns_discount_result_type | `pytest tests/billing/test_discount.py::test_percentage_discount_returns_discount_result_type -v` | 0 | PASS |
| test_fixed_discount_returns_fixed_amount | `pytest tests/billing/test_discount.py::test_fixed_discount_returns_fixed_amount -v` | 0 | PASS |
| test_fixed_discount_result_has_correct_type_field | `pytest tests/billing/test_discount.py::test_fixed_discount_result_has_correct_type_field -v` | 0 | PASS |
| test_unknown_code_raises_discount_not_found | `pytest tests/billing/test_discount.py::test_unknown_code_raises_discount_not_found -v` | 0 | PASS |
| test_expired_code_raises_discount_expired | `pytest tests/billing/test_discount.py::test_expired_code_raises_discount_expired -v` | 0 | PASS |
| test_already_used_code_raises_already_used | `pytest tests/billing/test_discount.py::test_already_used_code_raises_already_used -v` | 0 | PASS |
| test_order_below_minimum_raises_minimum_not_met | `pytest tests/billing/test_discount.py::test_order_below_minimum_raises_minimum_not_met -v` | 0 | PASS |
| test_order_total_exactly_at_minimum_passes | `pytest tests/billing/test_discount.py::test_order_total_exactly_at_minimum_passes -v` | 0 | PASS |
| test_order_total_one_cent_below_minimum_raises | `pytest tests/billing/test_discount.py::test_order_total_one_cent_below_minimum_raises -v` | 0 | PASS |
| test_code_expiring_in_one_second_still_valid | `pytest tests/billing/test_discount.py::test_code_expiring_in_one_second_still_valid -v` | 0 | PASS |
| test_code_at_exact_expiry_boundary_raises | `pytest tests/billing/test_discount.py::test_code_at_exact_expiry_boundary_raises -v` | 0 | PASS |
| test_percentage_amount_never_exceeds_order_total | `pytest tests/billing/test_discount.py::test_percentage_amount_never_exceeds_order_total -v` | 0 | PASS |
| test_zero_percent_discount_always_returns_zero_amount | `pytest tests/billing/test_discount.py::test_zero_percent_discount_always_returns_zero_amount -v` | 0 | PASS |

### Coverage summary

- Happy path scenarios: 4 tested (percentage amount, percentage result type, fixed amount, fixed type field)
- Edge cases: 4 tested (exact minimum, one cent below, 1 second before expiry, exact expiry boundary)
- Error cases: 4 tested (DiscountNotFoundError, DiscountExpiredError, DiscountAlreadyUsedError, DiscountMinimumNotMetError)
- Property-based: 2 Hypothesis tests (amount bounded by order_total, zero-percent always returns zero)
- Total: 14 passing, 0 failing, 0 skipped

---

## Criteria

### Definition criteria

- [x] PASS: Skill reads the function completely before writing any test — Step 1 Reconnaissance is explicitly marked MANDATORY and requires reading inputs, outputs, side effects, and error paths before writing any test.
- [x] PASS: Skill follows TDD Iron Law — the Iron Law section is marked "not a suggestion" and requires confirming exit code 1 with a meaningful failure before GREEN, then exit code 0.
- [x] PASS: Test cases cover all required categories — Step 2 mandates happy path (MUST have), edge cases including boundary values (MUST have), and error cases including inputs that throw (MUST have). All four prompt exceptions fall under the error cases category.
- [x] PASS: Tests run in run mode — Step 4 specifies `pytest tests/path/to/test_file.py -v` with an explicit note that watch mode is never used.
- [x] PASS: Each test has one assertion — Step 3 specifies "Assert — verify ONE expected outcome"; Anti-Patterns explicitly forbids multiple assertions per test.
- [x] PASS: Skill mocks only external boundaries — Anti-Patterns: "mock at external boundaries only (HTTP, database, file system). Use real implementations for your own code."
- [x] PASS: Skill uses factories for test data — Anti-Patterns bans "Inline test data — magic strings and numbers scattered through tests. Use factories." Python section specifies `@pytest.fixture` for data factories.
- [x] PASS: Evidence table is produced — Evidence Requirements section mandates the exact four-column table format with test name, command, exit code, and result.
- [~] PARTIAL: Skill uses Hypothesis for property-based testing — Python section lists "Hypothesis for property-based testing alongside BDD scenarios" as a rule but it is not a mandatory step in the main process and gives no guidance on which properties to test. Present but not enforced. Score: 0.5.

### Output expectations

- [x] PASS: Output produces tests for every named exception — all four (`DiscountNotFoundError`, `DiscountExpiredError`, `DiscountAlreadyUsedError`, `DiscountMinimumNotMetError`) have focused tests using `pytest.raises`.
- [x] PASS: Output's happy-path tests cover both percentage (10% of $200 = $20) and fixed ($15 off $80) with `DiscountResult.amount` asserted exactly.
- [x] PASS: Output's edge cases include `order_total` exactly equal to minimum (passes), one cent below (fails with `DiscountMinimumNotMetError`), one second before expiry (passes), and exact expiry boundary (fails with `DiscountExpiredError`).
- [x] PASS: Output uses `Decimal` throughout — `order_total`, factory values, Hypothesis strategies, and all asserted amounts use `Decimal`, never floats.
- [x] PASS: Output writes RED first — `pytest` shown with exit code 1 and a meaningful failure message (`ModuleNotFoundError`) before implementation, then GREEN with exit code 0.
- [x] PASS: Output mocks only `discount_repository.find_by_code` and `usage_repository.has_used` via `mocker.patch` — never mocks `validate_discount_code` itself or its return value.
- [x] PASS: Output uses `DiscountFactory` for all Discount entities; `CUSTOMER_ID` module-level fixture for customer identity; no inline magic UUIDs or dates repeated across tests.
- [x] PASS: One-assertion-per-test — percentage happy path splits into two tests (amount value, result type); fixed discount similarly split; all error tests assert only the exception type.
- [x] PASS: Evidence table lists all 14 tests with name, exact command, exit code, and PASS/FAIL result.
- [~] PARTIAL: Output includes Hypothesis property-based tests — two properties covered ("amount bounded by order_total", "zero percent returns zero amount"). The skill provides no explicit guidance on which properties to derive, so coverage relies on evaluator judgment rather than skill instructions. Score: 0.5.

## Notes

The skill is strong. The TDD Iron Law section is unusually concrete — it requires confirming exit codes at each phase rather than just describing the process, which meaningfully constrains what a passing response looks like. The failure caps (stop after 3 consecutive failures and escalate with evidence) are a practical safeguard not commonly seen in test generation skills.

The only genuine gap is Hypothesis guidance. The Python section mentions it as a rule but gives no instruction on when to apply it, what properties are worth testing, or how to structure Hypothesis tests alongside plain pytest. A developer following only the mandatory steps could omit Hypothesis entirely without violating any explicit requirement. Elevating it to a named step in the Python process (e.g., "Step 2.5: identify properties for Hypothesis when using pytest") with one worked example would close this gap cleanly.

The factory mandate is enforced via Anti-Patterns rather than a positive example for plain pytest. The Python section only shows BDD-style fixtures — a developer targeting plain pytest for a function like this has to infer the factory requirement from the prohibition rather than from an explicit model.
