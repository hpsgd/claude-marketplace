# Test: Write feature spec for notification preferences

Scenario: Developer invokes the write-feature-spec skill to produce a BDD feature spec for a notification preferences system — users can enable or disable each notification channel (email, SMS, push) per event type.

## Prompt

Write a feature spec for notification preferences. Users should be able to enable or disable each notification channel (email, SMS, push) for each event type (new comment, task assigned, mention). Changes take effect immediately. An admin can also toggle channels for a user.

## Criteria

- [ ] PASS: Skill performs reconnaissance first — checks for existing `.feature` files and step definitions before writing anything
- [ ] PASS: Feature file uses business language exclusively — no technical terms like HTTP status codes, table names, or SQL in Given/When/Then
- [ ] PASS: Feature includes at minimum: one happy path scenario, one edge case scenario, and one error/permission scenario
- [ ] PASS: Each Given/When/Then is a single statement — no conjunctive steps combining two actions in one When
- [ ] PASS: Step definitions use `target_fixture` to pass data between steps — no global mutable state
- [ ] PASS: Skill produces or specifies factory functions for domain entities (e.g. `UserFactory`, `PreferenceFactory`)
- [ ] PARTIAL: Skill includes a Scenario Outline for parameterised cases (e.g. testing all three channels with the same logic)
- [ ] PASS: Output delivers all five artefacts: feature file, step definitions, shared steps in conftest.py if applicable, optional property-based companion, and evidence of tests passing
