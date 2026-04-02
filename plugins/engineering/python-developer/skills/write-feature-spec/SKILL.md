---
name: write-feature-spec
description: Write a BDD feature specification in Gherkin with step definitions.
argument-hint: "[feature or behaviour to specify]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.py"
  - "**/*.feature"
---

Write a BDD feature spec for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Reconnaissance

Before writing any Gherkin:

1. **Read existing features** — match conventions:
   ```bash
   find . -name "*.feature" | head -20
   find . -name "test_*.py" -path "*/step_defs/*" | head -20
   ```

2. **Check existing step definitions** — reuse where possible:
   ```bash
   grep -rn "@given\|@when\|@then" --include="*.py" | head -30
   ```

3. **Identify the domain language** — what terms do product/business use? Use those, not technical terms

### Step 2: Feature File Structure

Every feature file follows this structure:

```gherkin
# tests/features/<feature-name>.feature

Feature: <Feature name in business language>
  As a <role>
  I want <capability>
  So that <business value>

  Background:
    Given <common precondition shared by all scenarios>

  Scenario: <Happy path — most common success case>
    Given <specific precondition in business language>
    When <user action in business language>
    Then <expected outcome in business language>

  Scenario: <Edge case — boundary or unusual input>
    Given <precondition>
    When <action with edge-case input>
    Then <expected outcome>

  Scenario: <Error case — invalid input or failed precondition>
    Given <precondition>
    When <action that should fail>
    Then <expected error behaviour>

  Scenario Outline: <Parameterised scenario for multiple inputs>
    Given <precondition with <parameter>>
    When <action with <input>>
    Then <outcome with <expected>>

    Examples:
      | parameter | input | expected |
      | value1    | x     | y        |
      | value2    | a     | b        |
```

### Step 3: Gherkin Writing Rules (MANDATORY)

**Language rules:**
- Features use **business language exclusively** — no technical terms, no implementation details
- BAD: `Given the user table has a row with id=5 and status='active'`
- GOOD: `Given an active user named "Alice"`
- BAD: `When a POST request is sent to /api/login with body {"email": "..."}`
- GOOD: `When Alice logs in with her email and password`
- BAD: `Then the response status code is 200`
- GOOD: `Then Alice sees her dashboard`

**Structure rules:**
- Each `Given`/`When`/`Then` is ONE statement. Use `And` for additional conditions
- `Given` establishes state — not action. It describes what IS, not what happened
- `When` is ONE user action or system event. Never multiple actions in one `When`
- `Then` verifies ONE outcome. Multiple assertions use `And`
- `Background` for preconditions shared by ALL scenarios in the file — not just some
- Scenario names describe the BEHAVIOUR, not the test: `"Successful login"` not `"Test login endpoint"`

**Scenario completeness:**
Every feature MUST include at minimum:
1. **Happy path** — the primary success case
2. **At least one edge case** — boundary input, empty collection, maximum length
3. **At least one error case** — invalid input, missing precondition, unauthorised access
4. **Scenario Outline** — if the same logic applies to multiple inputs, use parameterised scenarios

**Anti-patterns in Gherkin:**
- **Incidental details** — `Given a user with email "test@example.com" and password "Pass123!" and role "admin" and created_at "2024-01-01"` — only include details that matter for this scenario
- **Imperative style** — step-by-step UI instructions instead of declarative behaviour
- **Conjunctive steps** — `When the user logs in and navigates to settings and changes their name` — that's three steps
- **Tautological Then** — `Then the user is created` after `When the user is created` — test the EFFECT, not the action

### Step 4: Step Definitions

```python
# tests/step_defs/test_<feature>.py

from pytest_bdd import given, when, then, scenarios, parsers
import pytest

# Link to feature file
scenarios('../features/<feature>.feature')


# GIVEN — establish state using fixtures
@given('an active user named "<name>"', target_fixture='user')
def active_user(name, db_session):
    """Create an active user in the test database."""
    return UserFactory.create(name=name, status='active')


@given('the user has <count> pending notifications', target_fixture='notifications')
def pending_notifications(user, count, db_session):
    """Create pending notifications for the user."""
    return NotificationFactory.create_batch(int(count), user=user, status='pending')


# WHEN — perform the action, capture the result
@when('the user marks all notifications as read', target_fixture='result')
def mark_all_read(user, notification_service):
    """Call the service to mark all notifications as read."""
    return notification_service.mark_all_read(user.id)


# THEN — assert the outcome
@then('all notifications are marked as read')
def all_notifications_read(notifications, db_session):
    """Verify all notifications are now read."""
    for notification in notifications:
        db_session.refresh(notification)
        assert notification.status == 'read'


@then('the unread count is <expected>')
def unread_count(user, expected, notification_service):
    """Verify the unread notification count."""
    count = notification_service.get_unread_count(user.id)
    assert count == int(expected)
```

**Step definition rules:**
- `target_fixture` to pass data between steps — not global variables or module-level state
- Step definitions contain INFRASTRUCTURE code — database operations, API calls, service invocations
- Business logic stays in the feature file; infrastructure details stay in step definitions
- One step definition file per feature file: `test_<feature>.py` maps to `<feature>.feature`
- Keep step definitions short — delegate to factories and service functions

### Step 5: Step Definition Reuse

Reusable steps go in `conftest.py`:

```python
# tests/step_defs/conftest.py

from pytest_bdd import given, parsers
import pytest

# Shared fixtures
@pytest.fixture
def db_session(app):
    """Provide a database session for the test."""
    session = app.db.create_session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def notification_service(db_session):
    """Provide the notification service."""
    return NotificationService(db_session)

# Shared steps — reusable across feature files
@given('an active user named "<name>"', target_fixture='user')
def active_user(name, db_session):
    return UserFactory.create(name=name, status='active')

@given('an admin user named "<name>"', target_fixture='admin')
def admin_user(name, db_session):
    return UserFactory.create(name=name, role='admin')
```

**Reuse rules:**
- Steps used in 2+ feature files MUST be moved to `conftest.py`
- Steps used in only one feature file stay in `test_<feature>.py`
- Shared steps should be generic enough to reuse without modification
- Use `parsers.parse` for typed parameters: `@given(parsers.parse('a user with {count:d} items'))` for integer parsing
- Never duplicate step definitions — pytest-bdd raises errors for ambiguous step matches

### Step 6: Factory Functions

```python
# tests/factories.py

import factory
from myapp.models import User, Notification


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid4)
    name = factory.Faker('name')
    email = factory.Faker('email')
    status = 'active'
    role = 'user'
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))


class NotificationFactory(factory.Factory):
    class Meta:
        model = Notification

    id = factory.LazyFunction(uuid4)
    user = factory.SubFactory(UserFactory)
    message = factory.Faker('sentence')
    status = 'pending'
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))
```

**Factory rules:**
- Every domain entity has a factory — no inline object construction in tests
- Factories have sensible defaults — tests only override what's relevant to the scenario
- Use `factory.SubFactory` for relationships
- Use `factory.LazyFunction` for dynamic defaults (UUIDs, timestamps)
- `create_batch(n)` for generating multiple instances

### Step 7: Property-Based Companion Tests

For logic-heavy features, add Hypothesis property-based tests alongside BDD scenarios:

```python
# tests/test_<feature>_properties.py

from hypothesis import given, strategies as st
from hypothesis import settings

@given(
    amount=st.decimals(min_value=0.01, max_value=10000, places=2),
    currency=st.sampled_from(['USD', 'EUR', 'GBP']),
)
@settings(max_examples=200)
def test_conversion_roundtrip_preserves_value(amount, currency):
    """Converting to USD and back should preserve the original amount."""
    usd = convert(amount, currency, 'USD')
    back = convert(usd, 'USD', currency)
    assert abs(back - amount) < Decimal('0.01')


@given(items=st.lists(st.builds(OrderItem, quantity=st.integers(1, 100), price=st.decimals(0.01, 1000, places=2))))
def test_order_total_equals_sum_of_line_items(items):
    """Order total should always equal the sum of item quantity * price."""
    order = Order(items=items)
    expected = sum(item.quantity * item.price for item in items)
    assert order.total == expected
```

**Property-based rules:**
- BDD tests verify specific scenarios; property-based tests verify invariants
- Use for: mathematical properties, roundtrip conversions, invariants (total = sum of parts)
- `max_examples=200` is a good default — enough to find edge cases, fast enough for CI
- Strategies should generate realistic values — not `st.integers()` for prices

## Running Tests

```bash
# Run all BDD tests
pytest tests/ -v --tb=short

# Run a specific feature
pytest tests/step_defs/test_notifications.py -v

# Run with coverage
pytest tests/ --cov=myapp --cov-report=term-missing
```

## Anti-Patterns (NEVER do these)

- **Technical language in features** — `Given a row in the users table` is infrastructure, not behaviour
- **Multiple actions in When** — `When the user logs in and creates a post` is two scenarios
- **Testing the framework** — don't test that Flask routes or SQLAlchemy ORM works. Test your business logic
- **Global mutable state** — tests that depend on execution order or modify shared state
- **Missing error scenarios** — only testing happy paths. Every feature has at least one error case
- **Copy-paste step definitions** — if two features need the same step, move it to `conftest.py`
- **Scenario as unit test** — BDD scenarios test behaviour at the service/feature level, not individual functions

## Output

Deliver:
1. Feature file (`tests/features/<feature>.feature`) with happy path, edge case, and error scenarios
2. Step definitions (`tests/step_defs/test_<feature>.py`) with factories and fixtures
3. Shared steps moved to `conftest.py` if reusable
4. Property-based companion test if applicable
5. Evidence that tests pass (command + exit code)

## Related Skills

- `/python-developer:write-schema` — when the feature involves configuration or data contracts, write the schema after the feature spec defines the behaviour.
