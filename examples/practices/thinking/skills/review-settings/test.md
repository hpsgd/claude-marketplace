# Test: review-settings broad permission cleanup

Scenario: A developer's settings files have accumulated overly broad permissions from months of auto-approvals, including a bare `Bash` entry, several shell loop fragments, and duplicate plugin entries across scopes.

## Prompt

/review-settings

(Setup: `.claude/settings.json` contains `"allow": ["Bash", "Bash(done)", "Bash(do echo:*)", "Bash(git *)", "Read"]` and enables `coding-standards` plugin. `~/.claude/settings.json` also enables `coding-standards` and contains `"allow": ["Bash(git commit:*)", "Bash(npm run build)"]`.)

## Criteria

- [ ] PASS: Skill reads all three settings file locations in priority order before making any recommendations
- [ ] PASS: Bare `Bash` (no argument constraint) is flagged as high risk with explanation of what it allows in concrete terms
- [ ] PASS: `Bash(done)` and `Bash(do echo:*)` are flagged as fragment/junk rules from auto-approval with recommendation to remove
- [ ] PASS: `Read` with no path constraint is flagged as overly broad
- [ ] PASS: `Bash(git commit:*)` in global settings is flagged as a subset of `Bash(git *)` in project settings — one is redundant
- [ ] PASS: `coding-standards` plugin enabled at both global and project scope is flagged as cross-file redundancy
- [ ] PASS: Reconciled configuration is produced as a diff against the original — not a rewrite from scratch
- [ ] PARTIAL: AskUserQuestion is used to offer application options (apply all, per-file, selective, export-only) before any files are modified
