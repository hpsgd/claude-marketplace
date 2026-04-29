# Test: health-check full project setup audit

Scenario: A developer joins a new project and wants to understand the current state of the Claude Code setup — what rules are installed, which plugins are active, and whether the memory system is healthy.

## Prompt

/health-check

(Running in a project that has: 5 marketplace rules installed in ~/.claude/rules/, 3 learned rules in .claude/rules/, a CLAUDE.md at the project root, 2 wisdom frames in .claude/memory/ last updated 45 days ago, 12 learning files with 2 marked Critical and unresolved, and no project-level settings.json.)

## Criteria

- [ ] PASS: Skill checks both global (`~/.claude/rules/`) and project-level (`.claude/rules/`) rule locations using actual tool calls, not assumptions
- [ ] PASS: Report distinguishes marketplace rules from learned rules with counts for each
- [ ] PASS: Stale wisdom frames (last updated 45 days ago, exceeding the 30-day stable threshold) are flagged as stale — not reported as stable
- [ ] PASS: Unresolved Critical learnings are explicitly flagged as a finding, not just counted
- [ ] PASS: Each section reports what IS found, not what should be — recommendations go in a separate section
- [ ] PASS: Missing project-level settings.json is reported as "none found" — section is not skipped
- [ ] PASS: Report uses the defined output format with a summary header then per-section details
- [ ] PARTIAL: Recommendations section produces specific actions (e.g., "update wisdom-development frame" or "resolve 2 Critical learnings") rather than generic suggestions

## Output expectations

- [ ] PASS: Output reports the 5 marketplace rules in `~/.claude/rules/` and the 3 learned rules in `.claude/rules/` separately with their counts — not a single combined "8 rules" total
- [ ] PASS: Output uses real tool calls (Glob / ls) to enumerate the rule files and lists each by name — not asserting counts without evidence
- [ ] PASS: Output flags the 2 wisdom frames as STALE (45 days since last update, exceeding the 30-day threshold) — not just listed as "present"
- [ ] PASS: Output flags the 2 unresolved Critical learnings explicitly as a finding requiring resolution — with their names, not just a count of "2 unresolved"
- [ ] PASS: Output reports the 12 learning files with the breakdown by severity (e.g. "12 total: 2 Critical unresolved, X Important, Y Minor")
- [ ] PASS: Output reports CLAUDE.md as PRESENT (project root) and project-level `settings.json` as ABSENT — neither section skipped
- [ ] PASS: Output's findings are descriptive (what IS), separated from recommendations (what to do) — not mixed in the same paragraph
- [ ] PASS: Output's recommendations are specific actions tied to findings — e.g. "Update `wisdom-development.md` (45 days stale)", "Resolve the 2 Critical learnings: <name1>, <name2>", "Consider creating `.claude/settings.json` if project-specific overrides are needed" — not "consider reviewing"
- [ ] PASS: Output's summary header gives an at-a-glance project state (e.g. "Setup HEALTHY with 2 stale items requiring attention") before the per-section detail
- [ ] PARTIAL: Output flags whether the thinking plugin (the rule installer) is enabled — without it, marketplace rules in `~/.claude/rules/` may not be reaching the project, which is a common silent failure
