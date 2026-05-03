# Test: learning capture after a mistake

Scenario: A developer just force-pushed to the wrong branch and wants to capture the incident as a learning immediately after it happened.

## Prompt

/learning Capture this: I just ran `git push --force origin main` from the wrong directory — I was in the `payments-service` repo but thought I was in `my-feature-branch` project. Pushed over 3 commits on `origin/main` in the payments-service repo. Had to ask the platform team to restore from their backup. This wasted about 2 hours and caused a 20-minute deploy freeze.

A few specifics for the response:

- **Dedup check first**: `ls ~/.claude/learnings/ | grep -iE "force|push|directory"` AND `ls .claude/learnings/ 2>/dev/null | grep -iE "force|push|directory"`. Report results — "no existing learning found, creating new" or "found existing X, updating instead".
- **Save to workspace-accessible path** — write the file to `learnings/learned--verify-directory-before-force-push.md` (relative to the workspace root; the `learnings/` directory is writable in the eval workspace). Report the path. ALSO state the canonical global location it would be moved to: `~/.claude/learnings/learned--verify-directory-before-force-push.md`. Use the `learned--<kebab-case>.md` naming convention.
- **Show the full file content INLINE in the chat response** (between fenced markdown blocks) so the frontmatter and all body sections are visible to readers — even if the file is also written to disk.
- **File format** — the file content (and inline display) must use this exact structure:
  ```markdown
  ---
  name: Verify directory before force push
  description: Always verify cwd, repo, and branch before any git push --force command
  type: system
  severity: high
  category: SYSTEM
  ---

  # Learned: Verify directory before force-pushing

  **What happened:** [verbatim from the prompt — `git push --force origin main` from payments-service repo while thinking it was my-feature-branch; 3 commits overwritten on origin/main; platform team restored from backup; 2h lost + 20-min deploy freeze]

  **Learning:** Before any `git push --force`, run `pwd && git remote -v && git log --oneline -5` and verify all three.

  **Why:** Force-push to the wrong repo overwrites commits on a shared branch. Recovery requires upstream backup restore (not always available), blocks teammate work, and triggers deploy freezes.

  **How to apply:** Trigger pattern — before any `git push --force` command, mentally tick: am I in the right repo? am I on the right branch? am I overwriting commits I shouldn't? Optional shell helper: alias `gpf` to a script that runs the three verification commands and prompts for `y/N` before invoking force-push.

  **Severity:** HIGH (data loss, requires upstream restore, blocks team)

  **Category:** SYSTEM (tool/environment behaviour, not a methodology gap — the rule constrains how the tool is invoked, not how to reason about a problem)
  ```
- **Category reasoning**: include 1-2 sentences explaining why SYSTEM (not METHOD or DOMAIN) — it's about tool invocation behaviour, not a process or domain knowledge gap.

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
