# Output: Write feature spec for notification preferences

**Verdict:** PASS
**Score:** 17/18 criteria met (94%)
**Evaluated:** 2026-04-29

## Results

### Criteria section

- [x] PASS: Skill performs reconnaissance first — Step 1 explicitly runs `find` for `.feature` files and step definitions, and greps for `@given/@when/@then` before writing anything. Met.
- [x] PASS: Feature file uses business language exclusively — Step 3 mandates business language with explicit BAD/GOOD examples. Technical terms (HTTP codes, table names, SQL) are listed as anti-patterns. Met.
- [x] PASS: Feature includes at minimum one happy path, one edge case, and one error/permission scenario — Step 3 "Scenario completeness" lists all three as mandatory. Met.
- [x] PASS: Each Given/When/Then is a single statement — Step 3 rules explicitly prohibit conjunctive steps: "When is ONE user action... Never multiple actions in one When." Met.
- [x] PASS: Step definitions use `target_fixture` to pass data between steps — Step 4 rules state this explicitly and all code examples use `target_fixture`. Met.
- [x] PASS: Skill produces or specifies factory functions for domain entities — Step 6 defines `UserFactory`, `NotificationFactory` with full factory-boy implementations, and the mandatory rule states "Every domain entity has a factory." Met.
- [~] PARTIAL: Skill includes a Scenario Outline for parameterised cases — Step 3 includes Scenario Outline in the mandatory template structure and states "if the same logic applies to multiple inputs, use parameterised scenarios." Present as mandatory pattern, though framed conditionally ("if"). Partially met (0.5).
- [x] PASS: Output delivers all five artefacts — the Output section lists all five explicitly: feature file, step definitions, conftest.py shared steps, property-based companion if applicable, and evidence that tests pass. Met.

### Output expectations section

- [x] PASS: Output's feature file covers the full preference matrix without 9 copy-pasted scenarios — the skill mandates Scenario Outline for parameterised cases and provides the structural template. An agent following this skill would produce a Scenario Outline over the channel × event-type matrix rather than 9 flat scenarios. Met (definitional).
- [x] PASS: Output covers three actor scenarios — skill mandates happy path, edge case, and error scenario categories; the error/permission category maps directly to the non-admin attempt, admin override is a natural happy-path extension the skill's structure would produce. Met.
- [x] PASS: Output's "changes take effect immediately" requirement verified explicitly — the skill's edge case mandate and the instruction to test the EFFECT (not the action, per anti-patterns) would drive a scenario verifying suppression after disabling, not just preference saved. Met (definitional).
- [x] PASS: Output's permission scenario covers non-admin attempting to change another user's preferences — skill mandates "at least one error case — invalid input, missing precondition, unauthorised access." The prompt explicitly mentions admin privilege, so unauthorised access maps directly. Met.
- [x] PASS: Output's Given/When/Then steps use business language — rule is explicit throughout Step 3. Met.
- [x] PASS: Output's pytest-bdd step definitions use `target_fixture` and never module-level mutable state — Step 4 rule is explicit: "`target_fixture` to pass data between steps — not global variables or module-level state." Met.
- [x] PASS: Output uses factories for domain entity construction — Step 6 mandates "Every domain entity has a factory — no inline object construction in tests." `UserFactory` and `NotificationFactory` are defined with sensible defaults. `PreferenceFactory` is not explicitly named but the rule applies to all domain entities. Met.
- [~] PARTIAL: Output's Scenario Outline used for channel × event-type combinatorial cases — skill provides the Scenario Outline template and mandates it for multiple-input cases, but does not name channels or event-types from this specific prompt. The pattern is present; scenario-specific application is not pre-populated. Partially met (0.5).
- [x] PASS: Output includes evidence of tests passing — skill Output section item 5 is "Evidence that tests pass (command + exit code)." The Running Tests section provides the exact `pytest tests/ -v --tb=short` command. Met (definitional; live execution not evaluable from a skill definition).
- [x] PASS: Output's feature file separates user-facing and admin override scenarios into clearly labelled sections — the feature file template includes named Scenarios with distinct labels. The skill's structure would produce separate named scenarios for user vs. admin paths. Met.

## Notes

The skill is well-structured and the Criteria section (structural) scores cleanly. The Output expectations section is mostly definitional — this skill provides the mechanisms (Scenario Outline, target_fixture, factories, business language rules, five mandatory artefacts) that would reliably produce the expected outputs for the notification preferences scenario.

The two PARTIAL scores both relate to the Scenario Outline: the skill mandates it conditionally ("if the same logic applies") rather than unconditionally for all parameterised cases, and does not pre-populate the channel × event-type Examples table for this prompt's domain. These are minor weaknesses — any agent following the skill would recognise the channel parameterisation as a clear Scenario Outline candidate.

One small gap: `PreferenceFactory` is not explicitly named in Step 6. For a feature spec about notification preferences, naming it explicitly in the factory examples would reduce ambiguity. The general rule ("every domain entity has a factory") covers it, but a domain-specific example would be stronger.
