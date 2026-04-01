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

## Feature file (`tests/features/<feature>.feature`)

```gherkin
Feature: <Feature name>
  As a <role>
  I want <action>
  So that <outcome>

  Scenario: <Happy path description>
    Given <precondition in business language>
    When <action in business language>
    Then <expected outcome in business language>

  Scenario: <Edge case description>
    Given <precondition>
    When <action>
    Then <expected outcome>
```

## Rules

- Features use **business language** — hide infrastructure in step definitions
- One scenario per behaviour
- Describe the *what*, not the *how*
- Given/When/Then — each is one statement. Use And for additional conditions
- Step definitions in `tests/step_defs/test_<feature>.py`
- Reuse existing step definitions where possible

## Step definitions

```python
from pytest_bdd import given, when, then, scenarios

scenarios('../features/<feature>.feature')

@given('<precondition>')
def given_precondition():
    # Infrastructure setup here
    pass

@when('<action>')
def when_action():
    pass

@then('<expected outcome>')
def then_outcome():
    pass
```
