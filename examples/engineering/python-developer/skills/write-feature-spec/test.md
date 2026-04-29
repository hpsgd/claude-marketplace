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

## Output expectations

- [ ] PASS: Output's feature file covers the full preference matrix from the prompt — three channels (email, SMS, push) × three event types (new comment, task assigned, mention) — without hardcoding all 9 combinations as separate scenarios where a Scenario Outline would suffice
- [ ] PASS: Output covers the three actor scenarios — user toggling their own preferences, user receiving (or NOT receiving) notifications based on those preferences, admin toggling another user's preferences — at minimum one scenario each
- [ ] PASS: Output's "changes take effect immediately" requirement is verified explicitly — a scenario where a notification is suppressed right after the user disables a channel, not just that the preference was saved
- [ ] PASS: Output's permission scenario covers a non-admin attempting to change another user's preferences and being denied (403/error in business language)
- [ ] PASS: Output's Given/When/Then steps use business language — "Given Alice has email notifications enabled for new comments" — never HTTP status codes, table names, or SQL
- [ ] PASS: Output's pytest-bdd step definitions use `target_fixture` to pass data between steps and never rely on module-level mutable state for cross-step data
- [ ] PASS: Output uses factories (`UserFactory`, `PreferenceFactory`, `NotificationFactory`) for domain entity construction in step definitions — no inline magic strings or repeated dict literals
- [ ] PASS: Output's Scenario Outline (Examples table) is used for the channel × event-type combinatorial cases, demonstrating the parameterised pattern rather than 9 copy-pasted scenarios
- [ ] PASS: Output includes evidence of tests passing — exact `pytest -v --bdd` (or equivalent) command and exit code 0
- [ ] PARTIAL: Output's feature file structure separates the user-facing preferences scenarios from the admin override scenarios into clearly labelled rule blocks or feature sections
