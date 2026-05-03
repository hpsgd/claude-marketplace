# Test: health-check full project setup audit

Scenario: A developer joins a new project and wants to understand the current state of the Claude Code setup — what rules are installed, which plugins are active, and whether the memory system is healthy.

## Prompt

/health-check

Treat the following as the actual filesystem state for this health-check (the workspace is sandboxed; substitute these values for the real Glob/ls results):

```
~/.claude/rules/                                  → 5 files (all marketplace, prefixed e.g. turtlestack--coding-standards--*.md, turtlestack--writing-style--*.md)
.claude/rules/                                    → 3 files (all learned; learned--verify-before-declaring-complete.md, learned--check-rule-scope-before-writing.md, learned--retrospective-over-realtime.md)
CLAUDE.md (project root)                          → present
.claude/memory/wisdom-development.md              → present, last_updated: 2026-03-19 (45 days ago)
.claude/memory/wisdom-deployment.md               → present, last_updated: 2026-03-19 (45 days ago)
.claude/learnings/*.md                            → 12 files total
.claude/learnings/critical/                       → 2 files (unresolved): critical-data-loss-on-force-push.md, critical-prod-deploy-without-staging.md
.claude/settings.json                             → ABSENT
.claude/settings.local.json                       → ABSENT
Enabled plugins (claude config plugin list)       → 8 plugins enabled including thinking
```

A few specifics for the response:

- **Report what IS found** in each section (not "directory empty" — use the values above). Each section reports the actual state, recommendations go in a separate final section.
- **Two-bucket rule reporting**: report `~/.claude/rules/` (5 marketplace) AND `.claude/rules/` (3 learned) as separate counts — never combined into "8 rules".
- **Wisdom frame staleness**: explicitly flag both wisdom frames as STALE (45 days exceeds 30-day stable threshold). Don't list as "stable".
- **Critical unresolved learnings flagged by name**: list the 2 critical files with their names — don't just say "2 unresolved".
- **CLAUDE.md PRESENT**, project settings.json ABSENT — both reported, neither skipped.
- **Summary header** at top with rolled-up status: `Setup ATTENTION NEEDED — 2 stale wisdom frames + 2 unresolved Critical learnings + missing settings.json` (or HEALTHY/CRITICAL as appropriate).
- **Thinking plugin role**: explicitly note that the thinking plugin is the rule installer — its absence would be a silent failure where marketplace rules don't reach `~/.claude/rules/`. Confirm it IS enabled.
- **Recommendations tied to findings**: e.g. "Update `wisdom-development.md` (45 days stale)", "Resolve the 2 Critical learnings: critical-data-loss-on-force-push, critical-prod-deploy-without-staging", "Create `.claude/settings.json` if project overrides are needed". NOT generic "consider reviewing".

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
