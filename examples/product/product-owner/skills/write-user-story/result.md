# Output: Write user story

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/18 criteria met (94%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill requires Gherkin format (Given/When/Then) for acceptance criteria — met. Step 3 mandates Gherkin exclusively with explicit rules and a worked example prohibiting other formats.
- [x] PASS: Skill requires at least one edge case or error scenario, not just the happy path — met. Step 3 rule 5 states "Include the negative case. For every happy-path scenario, write the corresponding error scenario." Step 5 adds a mandatory edge case table with Gherkin scenarios covering error handling, permissions, concurrency, and empty state.
- [x] PASS: Skill includes the ISC splitting test — met. Step 4 is dedicated to Independent, Small, and Complete with definitions and verification questions for each.
- [x] PASS: Skill requires the standard "As a [role], I want [action], so that [outcome]" story format — met. Step 2 specifies the exact three-clause format with a code template and anti-patterns for each clause.
- [x] PASS: Skill prohibits solution-specifying stories — met. Step 2 action clause rules explicitly state "Describes what the user does, not what the system does." Step 3 rule 3 flags "Then the database is updated" as a bad example and requires observable outcomes.
- [~] PARTIAL: Skill addresses anti-requirements — Step 6 is a mandatory section with a prescribed format and the rule that every anti-requirement must reference where the excluded behaviour is tracked. This exceeds the partial bar but the criterion type caps scoring at 0.5.
- [x] PASS: Skill specifies that stories must have a single, clear acceptance condition — met. Step 2 applies the "and test" to the action clause. Step 3 rule 1 requires one scenario per behaviour and says "if a scenario has multiple When steps, split it."
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met. All three required fields present, plus user-invocable and allowed-tools.

### Output expectations

- [x] PASS: Step 1 bans "As a user" and requires specific role + context. A faithful output would produce a concrete role such as "analyst reviewing dashboard data" or "operations manager using the reporting dashboard."
- [x] PASS: Step 3 mandates Gherkin with at least happy path + error per rule 5, plus edge case scenarios from Step 5. At least 3 scenarios would result from following the skill faithfully.
- [x] PASS: Step 3 rules and example cover the main flow. The output format template shows a happy-path scenario structure; a faithful output would cover "Given I'm viewing a dashboard with data, When I export, Then a file downloads."
- [x] PASS: Step 5 edge case table includes Empty state and Scale (0/1/1000 items). These map directly to empty dashboard export and large dataset handling.
- [x] PASS: Step 5 includes Permissions ("What happens if the user lacks permission?") and Error handling ("network failure? Timeout? Server error?"). The skill explicitly drives error scenario coverage.
- [x] PASS: Step 3 rule 3 states "Then describes observable outcomes" and gives the counter-example "Then the database is updated is not observable to the user." The skill enforces verifiable criteria.
- [x] PASS: Step 4 (ISC test) applies per scenario; Step 7 validates the whole story. A faithful output would pass ISC as the skill requires applying each check explicitly.
- [x] PASS: Step 2 rules prohibit implementation-specifying action and value clauses. Step 3 rule 3 prohibits non-observable Then steps. Combined, the skill prevents implementation-specific acceptance criteria.
- [x] PASS: Step 3 rule 4 requires concrete values. Step 5 edge case table (Scale, Empty state) drives the agent to specify what data appears in the export. A faithful output would address CSV content scope.
- [~] PARTIAL: Step 6 requires anti-requirements but uses generic placeholders ("bulk operations", "admin workflow") rather than prompting scope-specific exclusions. Whether the output names CSV-specific anti-requirements (no Excel, no scheduled exports) depends on agent inference, not explicit instruction. Partial credit only.

## Notes

The skill is well-structured and substantive across all seven steps. The seven-step flow gives concrete rules at each stage rather than vague guidance, which reliably constrains model output. The ISC test applies at the scenario level (not just the story level), which is more rigorous than most story-writing approaches.

The PARTIAL on the anti-requirements output criterion reflects a genuine gap: Step 6's template examples are generic domain stubs. Adding a prompt like "List format, scheduling, and integration exclusions specific to the feature" would close it.

Story sizing guidance in Step 7 (half-day too small, one week too large) and the Related Skills cross-links to `groom-backlog` and `write-prd` are useful additions beyond the rubric scope.
