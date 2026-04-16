# Test: retrospective session analysis with corrections

Scenario: At the start of a new session, the retrospective skill analyses the previous session's transcript where the assistant made two approach reversals and received one explicit correction about file location assumptions.

## Prompt

/retrospective latest

(Session transcript contains: assistant declared a migration complete before running the verification step; user corrected "you haven't actually checked if the migration ran, please verify"; assistant then wrote a local rule file to the wrong path assuming project-level when user clarified it should be global; session ends with user saying "good work on the API refactor though, that was clean".)

## Criteria

- [ ] PASS: Step 1 locates the correct transcript file by computing the directory hash from the working path — does not assume a fixed location
- [ ] PASS: Step 2 runs the analysis script and presents metrics including turns, corrections, reversals, and correction rate
- [ ] PASS: The premature completion declaration is extracted as a correction event and classified as high severity
- [ ] PASS: The wrong-path assumption (project vs global rule location) is extracted as a correction event with scope classification
- [ ] PASS: The API refactor success is captured as a non-obvious positive learning worth reinforcing
- [ ] PASS: Path 1 (local learned rule) is written for every high-severity correction before any upstream PR is considered
- [ ] PASS: Learned rule files use the correct naming convention (`learned--{kebab-case-topic}.md`) and correct scope (global vs project)
- [ ] PARTIAL: Step 3 classifies pending signals from the signals queue and adds regex patterns for any correction phrases the existing patterns missed
