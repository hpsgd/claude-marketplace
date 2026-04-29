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

## Output expectations

- [ ] PASS: Output identifies BOTH correction events from the transcript — premature completion declaration AND wrong-path rule write — with verbatim or near-verbatim user quotes as evidence
- [ ] PASS: Output classifies the premature completion declaration as HIGH severity — verifying-before-declaring-done failures are repeated cause of customer-visible mistakes
- [ ] PASS: Output classifies the wrong-path assumption with explicit scope analysis — the assistant assumed project-level when global was correct, so the resulting learned rule must be scoped correctly (likely a global rule)
- [ ] PASS: Output captures the API refactor success as a positive learning — the user's explicit "good work" is non-obvious and worth reinforcing
- [ ] PASS: Output writes Path 1 (local learned rule) for both high-severity corrections BEFORE any upstream PR proposal — the dual-path rule requires immediate local rules
- [ ] PASS: Output's learned-rule files use the convention `learned--<kebab-case-topic>.md` — e.g. `learned--verify-before-declaring-complete.md` and `learned--check-rule-scope-before-writing.md`
- [ ] PASS: Output places each learned rule in the correct scope — global rules in `~/.claude/rules/`, project rules in `.claude/rules/` — and the wrong-path-correction rule itself is global because it applies across projects
- [ ] PASS: Output presents transcript metrics — turns, corrections, reversals, correction rate — with actual counts derived from the transcript, not estimates
- [ ] PASS: Output's transcript file lookup uses the directory hash (working-path → hash) to locate the correct file in `~/.claude/projects/` — not assuming a fixed path
- [ ] PARTIAL: Output classifies any pending signals from the signals queue and proposes regex patterns for correction phrases the existing patterns missed — strengthening future automated detection
