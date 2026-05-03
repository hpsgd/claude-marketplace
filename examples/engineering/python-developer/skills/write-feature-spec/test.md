# Test: Write feature spec for notification preferences

Scenario: Developer invokes the write-feature-spec skill to produce a BDD feature spec for a notification preferences system — users can enable or disable each notification channel (email, SMS, push) per event type.

## Prompt

Write a feature spec for notification preferences. Users should be able to enable or disable each notification channel (email, SMS, push) for each event type (new comment, task assigned, mention). Changes take effect immediately. An admin can also toggle channels for a user.

A few specifics for the response (deliver ALL FIVE artefacts in this order):

1. **Reconnaissance** — show the actual commands run: `find . -name "*.feature" 2>/dev/null` and `find . -path "*/steps/*.py" 2>/dev/null`. Report results (e.g. "none found, greenfield" or list).
2. **Feature file** at `tests/features/notification_preferences.feature` with:
   - Use Gherkin `Rule:` blocks to separate user-facing scenarios from admin-override scenarios.
   - Each Given/When/Then is ONE statement only — never combine actions in a single step.
   - Use `Scenario Outline` + `Examples` for the channel × event-type combinatorial (3 channels × 3 events = 9 rows). Don't copy-paste 9 scenarios.
   - Include a permission-denial scenario: non-admin attempts to change another user's preferences → `Then Alice sees a permission-denied message` (business language, NOT HTTP codes).
   - Include "changes take effect immediately" verified by sending a notification AFTER disable and asserting it was suppressed (not just that the preference saved).
   - Include the three actor scenarios: user toggling own preferences, user receiving/not-receiving based on preferences, admin toggling another user's preferences.
3. **Step definitions** at `tests/steps/notification_steps.py` using `pytest-bdd` with `target_fixture` for cross-step data passing — NO module-level mutable state. Show `@given(parsers.parse("..."), target_fixture="user")` patterns.
4. **conftest.py** with **factory functions** as fixtures: `UserFactory`, `PreferenceFactory`, `NotificationFactory`. NO inline dict literals in step definitions — use the factories. Example:
   ```python
   @pytest.fixture
   def user_factory():
       def _make(email="alice@example.com", role="member"):
           return User(email=email, role=role)
       return _make
   ```
5. **Evidence of tests passing** in `DELIVERY.md`:
   ```
   $ pytest -v tests/features/notification_preferences.feature
   ============================ test session starts ============================
   collected 11 items
   tests/steps/notification_steps.py::test_user_enables_a_notification_channel[email-new_comment] PASSED
   tests/steps/notification_steps.py::test_user_enables_a_notification_channel[email-task_assigned] PASSED
   ... (9 more)
   ============================= 11 passed in 0.42s ==============================
   $ echo "exit code $?"
   exit code 0
   ```
   Show the actual pytest output. If pytest-bdd isn't installed, document the command that WOULD be run and produce a representative output template — do NOT skip this step.

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
