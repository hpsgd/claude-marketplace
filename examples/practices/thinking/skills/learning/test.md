# Test: learning capture after a mistake

Scenario: A developer just force-pushed to the wrong branch and wants to capture the incident as a learning immediately after it happened.

## Prompt

/learning Capture this: I just ran `git push --force origin main` from the wrong directory — I was in the `payments-service` repo but thought I was in `my-feature-branch` project. Pushed over 3 commits on `origin/main` in the payments-service repo. Had to ask the platform team to restore from their backup. This wasted about 2 hours and caused a 20-minute deploy freeze.

## Criteria

- [ ] PASS: Step 1 assigns a category (SYSTEM, METHOD, DOMAIN, or FEEDBACK) with reasoning
- [ ] PASS: Step 2 writes the learning in the exact format — frontmatter with name/description/type, plus What happened, Learning (imperative), Why, How to apply, Severity, and Category
- [ ] PASS: The learning is stated as an imperative rule ("Always X" or "Never Y"), not as a narrative
- [ ] PASS: The "Why" field explains the consequence of ignoring the rule — not just a restatement
- [ ] PASS: Step 3 assigns Critical severity given the data loss and rework described — downgrading to Important would violate the skill's own severity rules
- [ ] PASS: Step 4 failure capture is triggered (something went notably wrong) and produces a failure analysis with root cause, what was tried, what worked, and a prevention rule
- [ ] PASS: Output follows the "When capturing" format template with name, category, severity, rule, and saved-to path
- [ ] PARTIAL: Skill checks for an existing learning on the same topic before creating a new file, to avoid duplicates

## Output expectations

- [ ] PASS: Output classifies this incident as a SYSTEM learning (force-push without verifying the directory is a tool/environment behaviour, not a methodology gap) — with reasoning, not just a label
- [ ] PASS: Output's "What happened" reproduces the specific details — `git push --force origin main` from wrong directory, payments-service vs my-feature-branch, 3 commits overwritten, restored from platform team backup — verbatim or near-verbatim from the prompt
- [ ] PASS: Output's learning is stated as an imperative rule — e.g. "Always run `git remote -v` and `git status` before any `git push --force`" or "Never run `git push --force` without verifying the current working directory and remote first" — not narrative prose
- [ ] PASS: Output's "Why" explains the consequence of ignoring the rule — data loss, requires upstream backup restore, downstream deploy freeze, hours of rework — not a restatement of "you might push to wrong branch"
- [ ] PASS: Output's "How to apply" gives a concrete trigger pattern — "before any `git push --force` command, mentally tick: am I in the right repo? am I on the right branch? am I overwriting commits I shouldn't?" — with optional shell helper or alias suggestion
- [ ] PASS: Output assigns CRITICAL severity given data loss + 2 hours rework + 20-minute deploy freeze impact — explicitly NOT downgraded to Important
- [ ] PASS: Output's failure capture (Step 4) is triggered — produces a failure analysis with root cause (no verification of pwd/remote before destructive command), what was tried (asking platform team for backup), what worked (backup restore), and a prevention rule
- [ ] PASS: Output is saved to a file path matching the convention — `~/.claude/learnings/<name>.md` or `.claude/learnings/<name>.md` — and the path is reported in the output
- [ ] PASS: Output's frontmatter includes the required fields — name, description, type, severity, category — with the type matching the SYSTEM/METHOD/DOMAIN/FEEDBACK classification chosen
- [ ] PARTIAL: Output checks `~/.claude/learnings/` and `.claude/learnings/` for existing learnings on `git push --force` or directory verification before creating a new file, to avoid duplicates
