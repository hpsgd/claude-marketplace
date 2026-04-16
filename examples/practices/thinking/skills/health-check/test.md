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
