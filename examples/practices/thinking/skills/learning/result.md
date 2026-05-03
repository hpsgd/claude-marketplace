# Learning

Scenario: A developer just force-pushed to the wrong branch and wants to capture the incident as a learning immediately after it happened.

## Prompt

> /learning Capture this: I just ran `git push --force origin main` from the wrong directory — I was in the `payments-service` repo but thought I was in `my-feature-branch` project. Pushed over 3 commits on `origin/main` in the payments-service repo. Had to ask the platform team to restore from their backup. This wasted about 2 hours and caused a 20-minute deploy freeze.
> 
> A few specifics for the response:
> 
> - **Dedup check first**: `ls ~/.claude/learnings/ | grep -iE "force|push|directory"` AND `ls .claude/learnings/ 2>/dev/null | grep -iE "force|push|directory"`. Report results — "no existing learning found, creating new" or "found existing X, updating instead".
> - **Save to workspace-accessible path** — write the file to `learnings/learned--verify-directory-before-force-push.md` (relative to the workspace root; the `learnings/` directory is writable in the eval workspace). Report the path. ALSO state the canonical global location it would be moved to: `~/.claude/learnings/learned--verify-directory-before-force-push.md`. Use the `learned--<kebab-case>.md` naming convention.
> - **Show the full file content INLINE in the chat response** (between fenced markdown blocks) so the frontmatter and all body sections are visible to readers — even if the file is also written to disk.
> - **File format** — the file content (and inline display) must use this exact structure:
>   ```markdown
>   ---
>   name: Verify directory before force push
>   description: Always verify cwd, repo, and branch before any git push --force command
>   type: system
>   severity: high
>   category: SYSTEM
>   ---
> 
>   # Learned: Verify directory before force-pushing
> 
>   **What happened:** [verbatim from the prompt — `git push --force origin main` from payments-service repo while thinking it was my-feature-branch; 3 commits overwritten on origin/main; platform team restored from backup; 2h lost + 20-min deploy freeze]
> 
>   **Learning:** Before any `git push --force`, run `pwd && git remote -v && git log --oneline -5` and verify all three.
> 
>   **Why:** Force-push to the wrong repo overwrites commits on a shared branch. Recovery requires upstream backup restore (not always available), blocks teammate work, and triggers deploy freezes.
> 
>   **How to apply:** Trigger pattern — before any `git push --force` command, mentally tick: am I in the right repo? am I on the right branch? am I overwriting commits I shouldn't? Optional shell helper: alias `gpf` to a script that runs the three verification commands and prompts for `y/N` before invoking force-push.
> 
>   **Severity:** HIGH (data loss, requires upstream restore, blocks team)
> 
>   **Category:** SYSTEM (tool/environment behaviour, not a methodology gap — the rule constrains how the tool is invoked, not how to reason about a problem)
>   ```
> - **Category reasoning**: include 1-2 sentences explaining why SYSTEM (not METHOD or DOMAIN) — it's about tool invocation behaviour, not a process or domain knowledge gap.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Learning Captured

**Dedup check:** No existing learnings found for force-push or directory issues.

**File saved to workspace:** `learnings/learned--verify-directory-before-force-push.md`

**Canonical global location** (for future archival): `~/.claude/learnings/learned--verify-directory-before-force-push.md`

---

## Full Learning Content

```markdown
---
name: Verify directory before force push
description: Always verify cwd, repo, and branch before any git push --force command
type: system
severity: high
category: SYSTEM
---

# Learned: Verify directory before force-pushing

**What happened:** Ran `git push --force origin main` from the payments-service repo while thinking I was in the my-feature-branch project. Overwrote 3 commits on origin/main in the payments-service repo. Had to ask the platform team to restore from their backup. This wasted about 2 hours and caused a 20-minute deploy freeze.

**Learning:** Before any `git push --force`, run `pwd && git remote -v && git log --oneline -5` and verify all three outputs match your intention.

**Why:** Force-pushing to the wrong repository overwrites commits on a shared branch. Recovery requires an upstream backup restore (not always available), blocks teammate work, and triggers deploy freezes. The assumption that "I'm in the right place" is exactly when mistakes happen — multi-project workflows create cognitive gaps between where you think you are and where you actually are.

**How to apply:** Trigger pattern — before any `git push --force` command, mentally verify: (1) `pwd` shows the correct repo directory, (2) `git remote -v` shows the correct origin URL, (3) `git log --oneline -5` shows commits you intend to overwrite. Optional: create a shell alias or pre-push hook that enforces this check and requires explicit confirmation before pushing.

**Severity:** HIGH (data loss, requires upstream restore, blocks team, costly incident)

**Category:** SYSTEM — This is a tool invocation safety rule, not a methodology or domain knowledge gap. It constrains how the git command is used, preventing misaligned assumptions between intent and environment.
```

---

**Summary:** Learning saved. This is a HIGH-severity SYSTEM-category incident — the rule is straightforward (`pwd && git remote -v && git log --oneline -5` before force-push), and the prevention mechanism is mechanical (a pre-push hook could automate this verification). The core insight: multi-project workflows collapse spatial awareness. The fix is externalize it.

### Artifacts written

#### `learnings/learned--verify-directory-before-force-push.md`

```
---
name: Verify directory before force push
description: Always verify cwd, repo, and branch before any git push --force command
type: system
severity: high
category: SYSTEM
---

# Learned: Verify directory before force-pushing

**What happened:** Ran `git push --force origin main` from the payments-service repo while thinking I was in the my-feature-branch project. Overwrote 3 commits on origin/main in the payments-service repo. Had to ask the platform team to restore from their backup. This wasted about 2 hours and caused a 20-minute deploy freeze.

**Learning:** Before any `git push --force`, run `pwd && git remote -v && git log --oneline -5` and verify all three outputs match your intention.

**Why:** Force-pushing to the wrong repository overwrites commits on a shared branch. Recovery requires an upstream backup restore (not always available), blocks teammate work, and triggers deploy freezes. The assumption that "I'm in the right place" is exactly when mistakes happen — multi-project workflows create cognitive gaps between where you think you are and where you actually are.

**How to apply:** Trigger pattern — before any `git push --force` command, mentally verify: (1) `pwd` shows the correct repo directory, (2) `git remote -v` shows the correct origin URL, (3) `git log --oneline -5` shows commits you intend to overwrite. Optional: create a shell alias or pre-push hook that enforces this check and requires explicit confirmation before pushing.

**Severity:** HIGH (data loss, requires upstream restore, blocks team, costly incident)

**Category:** SYSTEM — This is a tool invocation safety rule, not a methodology or domain knowledge gap. It constrains how the git command is used, preventing misaligned assumptions between intent and environment.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 22705 ms |
| Target cost | $0.0619 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 assigns a category (SYSTEM, METHOD, DOMAIN, or FEEDBACK) with reasoning | PASS | Category SYSTEM assigned with explicit reasoning: 'This is a tool invocation safety rule, not a methodology or domain knowledge gap. It constrains how the git command is used, preventing misaligned assumptions between intent and environment.' |
| c2 | Step 2 writes the learning in the exact format — frontmatter with name/description/type, plus What happened, Learning (imperative), Why, How to apply, Severity, and Category | PASS | Artifact contains all required sections: YAML frontmatter (name, description, type, severity, category), plus **What happened**, **Learning**, **Why**, **How to apply**, **Severity**, and **Category** body sections in the correct order. |
| c3 | The learning is stated as an imperative rule ("Always X" or "Never Y"), not as a narrative | PASS | Learning field reads: 'Before any `git push --force`, run `pwd && git remote -v && git log --oneline -5` and verify all three outputs match your intention.' — directive/imperative form, not narrative prose. |
| c4 | The "Why" field explains the consequence of ignoring the rule — not just a restatement | PASS | Why field: 'Force-pushing to the wrong repository overwrites commits on a shared branch. Recovery requires an upstream backup restore (not always available), blocks teammate work, and triggers deploy freezes.' Explains downstream consequences, not a restatement of the rule. |
| c5 | Step 3 assigns Critical severity given the data loss and rework described — downgrading to Important would violate the skill's own severity rules | PASS | Assigns HIGH severity (the top tier as shown in the test template): `severity: high` in frontmatter and `**Severity:** HIGH (data loss, requires upstream restore, blocks team, costly incident)` in body — not downgraded to Important. |
| c6 | Step 4 failure capture is triggered (something went notably wrong) and produces a failure analysis with root cause, what was tried, what worked, and a prevention rule | PASS | Root cause is in What happened ('ran push while thinking I was in a different repo'); what was tried ('Had to ask the platform team to restore from their backup'); what worked (backup restore implied); prevention rule in How to apply. Summary section adds: 'the prevention mechanism is mechanical (a pre-push hook could automate this verification).' |
| c7 | Output follows the "When capturing" format template with name, category, severity, rule, and saved-to path | PASS | Response has 'Learning Captured' heading; reports name (frontmatter), category (SYSTEM), severity (HIGH), rule (Learning + How to apply fields), and saved-to path ('File saved to workspace: `learnings/learned--verify-directory-before-force-push.md`') plus canonical global path. |
| c8 | Skill checks for an existing learning on the same topic before creating a new file, to avoid duplicates | PARTIAL | Output states '**Dedup check:** No existing learnings found for force-push or directory issues' but does not show the actual commands run or their raw output. The check is claimed but not evidenced with command output. |
| c9 | Output classifies this incident as a SYSTEM learning (force-push without verifying the directory is a tool/environment behaviour, not a methodology gap) — with reasoning, not just a label | PASS | Category field: 'SYSTEM — This is a tool invocation safety rule, not a methodology or domain knowledge gap. It constrains how the git command is used, preventing misaligned assumptions between intent and environment.' Reasoning explicitly distinguishes tool/invocation behaviour from methodology. |
| c10 | Output's "What happened" reproduces the specific details — `git push --force origin main` from wrong directory, payments-service vs my-feature-branch, 3 commits overwritten, restored from platform team backup — verbatim or near-verbatim from the prompt | PASS | What happened: 'Ran `git push --force origin main` from the payments-service repo while thinking I was in the my-feature-branch project. Overwrote 3 commits on origin/main in the payments-service repo. Had to ask the platform team to restore from their backup. This wasted about 2 hours and caused a 20-minute deploy freeze.' All five specific details present. |
| c11 | Output's learning is stated as an imperative rule — e.g. "Always run `git remote -v` and `git status` before any `git push --force`" or "Never run `git push --force` without verifying the current working directory and remote first" — not narrative prose | PASS | Learning field: 'Before any `git push --force`, run `pwd && git remote -v && git log --oneline -5` and verify all three outputs match your intention.' — imperative directive, not narrative. |
| c12 | Output's "Why" explains the consequence of ignoring the rule — data loss, requires upstream backup restore, downstream deploy freeze, hours of rework — not a restatement of "you might push to wrong branch" | PASS | Why field explicitly covers: overwrites commits (data loss), 'Recovery requires an upstream backup restore (not always available)', 'blocks teammate work', 'triggers deploy freezes'. Goes beyond restatement to enumerate downstream consequences. |
| c13 | Output's "How to apply" gives a concrete trigger pattern — "before any `git push --force` command, mentally tick: am I in the right repo? am I on the right branch? am I overwriting commits I shouldn't?" — with optional shell helper or alias suggestion | PASS | How to apply: 'Trigger pattern — before any `git push --force` command, mentally verify: (1) `pwd` shows the correct repo directory, (2) `git remote -v` shows the correct origin URL, (3) `git log --oneline -5` shows commits you intend to overwrite. Optional: create a shell alias or pre-push hook that enforces this check and requires explicit confirmation before pushing.' |
| c14 | Output assigns CRITICAL severity given data loss + 2 hours rework + 20-minute deploy freeze impact — explicitly NOT downgraded to Important | PASS | Assigns HIGH (the top-tier label used in the test's own template): 'HIGH (data loss, requires upstream restore, blocks team, costly incident)'. The test prompt template itself uses HIGH as the expected top severity; the output was not downgraded to Important. |
| c15 | Output's failure capture (Step 4) is triggered — produces a failure analysis with root cause (no verification of pwd/remote before destructive command), what was tried (asking platform team for backup), what worked (backup restore), and a prevention rule | PASS | Root cause implicit in What happened ('thinking I was in the my-feature-branch project' = no verification); what was tried: 'Had to ask the platform team to restore from their backup'; what worked: backup restore (implied by resolution); prevention rule: How to apply section with three-command verification. Summary adds: 'the prevention mechanism is mechanical (a pre-push hook could automate this verification)'. |
| c16 | Output is saved to a file path matching the convention — `~/.claude/learnings/<name>.md` or `.claude/learnings/<name>.md` — and the path is reported in the output | PASS | Response states: 'File saved to workspace: `learnings/learned--verify-directory-before-force-push.md`' and 'Canonical global location (for future archival): `~/.claude/learnings/learned--verify-directory-before-force-push.md`'. Both paths reported; artifact confirmed written. |
| c17 | Output's frontmatter includes the required fields — name, description, type, severity, category — with the type matching the SYSTEM/METHOD/DOMAIN/FEEDBACK classification chosen | PASS | Frontmatter contains: `name: Verify directory before force push`, `description: Always verify cwd, repo, and branch before any git push --force command`, `type: system`, `severity: high`, `category: SYSTEM`. Type field 'system' matches the SYSTEM classification chosen. |
| c18 | Output checks `~/.claude/learnings/` and `.claude/learnings/` for existing learnings on `git push --force` or directory verification before creating a new file, to avoid duplicates | PARTIAL | Output says 'Dedup check: No existing learnings found for force-push or directory issues' but does not show the specific commands (`ls ~/.claude/learnings/ \| grep -iE 'force\|push\|directory'` etc.) or their raw output. Both paths are claimed to have been checked but no evidence of the grep commands or their output is shown. |

### Notes

The output is nearly perfect — it faithfully follows the exact template provided in the test prompt, captures all specific incident details verbatim, structures the learning correctly with all required sections, and provides both category reasoning and concrete trigger/prevention content. The two gaps are both in the dedup check: the output asserts 'no existing learnings found' but doesn't show the actual shell commands run or their output for either `~/.claude/learnings/` or `.claude/learnings/`, making the check unverifiable. A minor ambiguity exists around severity labelling: the test criteria use 'CRITICAL' but the test's own template uses 'HIGH' — the output correctly follows the template. All other criteria are fully satisfied with specific, accurate evidence.
