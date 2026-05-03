# Learning

Scenario: A developer just force-pushed to the wrong branch and wants to capture the incident as a learning immediately after it happened.

## Prompt

> /learning Capture this: I just ran `git push --force origin main` from the wrong directory — I was in the `payments-service` repo but thought I was in `my-feature-branch` project. Pushed over 3 commits on `origin/main` in the payments-service repo. Had to ask the platform team to restore from their backup. This wasted about 2 hours and caused a 20-minute deploy freeze.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Learning Captured

**Name:** git-force-push-wrong-directory
**Category:** SYSTEM
**Severity:** Critical
**Rule:** Before any `git push --force` (or `reset --hard`, `branch -D`), run `pwd` → `git remote -v` → `git log --oneline -5` and verify all three match expectations. Do not proceed if there is any doubt about which repo you are in.
**Saved to:** `memory/system_git_force_push_wrong_directory.md`

### Failure Analysis summary

| Field | Detail |
|---|---|
| Root cause | No working-directory pre-flight check before a destructive command |
| Recovery | Platform team backup restore |
| Cost | 2h lost, 20-min deploy freeze, 3 commits overwritten on production `main` |
| Prevention rule | Treat `git push --force` like `rm -rf` — always verify context first |

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 10.5/17.0 (62%) |
| Evaluated | 2026-05-01 |
| Target duration | 40156 ms |
| Target cost | $0.0945 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 assigns a category (SYSTEM, METHOD, DOMAIN, or FEEDBACK) with reasoning | PARTIAL | Output shows '**Category:** SYSTEM' but provides zero reasoning for why SYSTEM was chosen over METHOD or DOMAIN. |
| c2 | Step 2 writes the learning in the exact format — frontmatter with name/description/type, plus What happened, Learning (imperative), Why, How to apply, Severity, and Category | FAIL | The captured output is a chat summary (Name, Category, Severity, Rule, Saved to). No frontmatter structure is shown, no description/type fields, no dedicated 'What happened', 'Why', or 'How to apply' sections appear anywhere in the output. |
| c3 | The learning is stated as an imperative rule ("Always X" or "Never Y"), not as a narrative | PASS | Rule field states: 'Before any `git push --force` (or `reset --hard`, `branch -D`), run `pwd` → `git remote -v` → `git log --oneline -5` and verify all three match expectations. Do not proceed if there is any doubt…' — imperative form. |
| c4 | The "Why" field explains the consequence of ignoring the rule — not just a restatement | PARTIAL | No dedicated 'Why' field appears. Consequences are implied by the failure analysis Cost row: '2h lost, 20-min deploy freeze, 3 commits overwritten on production `main`' — present but not in a structured Why field. |
| c5 | Step 3 assigns Critical severity given the data loss and rework described — downgrading to Important would violate the skill's own severity rules | PASS | '**Severity:** Critical' is explicitly stated in the output. |
| c6 | Step 4 failure capture is triggered (something went notably wrong) and produces a failure analysis with root cause, what was tried, what worked, and a prevention rule | PASS | Failure Analysis summary table includes Root cause ('No working-directory pre-flight check before a destructive command'), Recovery ('Platform team backup restore' covers both what was tried and what worked), Cost, and Prevention rule ('Treat `git push --force` like `rm -rf` — always verify context first'). |
| c7 | Output follows the "When capturing" format template with name, category, severity, rule, and saved-to path | PASS | All five elements present: **Name:** git-force-push-wrong-directory, **Category:** SYSTEM, **Severity:** Critical, **Rule:** (full imperative text), **Saved to:** `memory/system_git_force_push_wrong_directory.md`. |
| c8 | Skill checks for an existing learning on the same topic before creating a new file, to avoid duplicates | FAIL | No mention anywhere in the captured output of checking for existing learnings on git push --force or directory verification before creating the file. |
| c9 | Output classifies this incident as a SYSTEM learning (force-push without verifying the directory is a tool/environment behaviour, not a methodology gap) — with reasoning, not just a label | PARTIAL | '**Category:** SYSTEM' label is present, but no reasoning is given for why this is SYSTEM rather than METHOD (e.g., no explanation that it's a tool/environment behaviour, not a process gap). |
| c10 | Output's "What happened" reproduces the specific details — `git push --force origin main` from wrong directory, payments-service vs my-feature-branch, 3 commits overwritten, restored from platform team backup — verbatim or near-verbatim from the prompt | PARTIAL | Cost row mentions '3 commits overwritten on production `main`' and Recovery mentions 'Platform team backup restore', but the output omits `git push --force origin main` verbatim, the payments-service vs my-feature-branch distinction, and has no dedicated 'What happened' section. |
| c11 | Output's learning is stated as an imperative rule — e.g. "Always run `git remote -v` and `git status` before any `git push --force`" or "Never run `git push --force` without verifying the current working directory and remote first" — not narrative prose | PASS | Rule field: 'Before any `git push --force` (or `reset --hard`, `branch -D`), run `pwd` → `git remote -v` → `git log --oneline -5` and verify all three match expectations.' Imperative, not narrative. |
| c12 | Output's "Why" explains the consequence of ignoring the rule — data loss, requires upstream backup restore, downstream deploy freeze, hours of rework — not a restatement of "you might push to wrong branch" | PARTIAL | Cost row: '2h lost, 20-min deploy freeze, 3 commits overwritten on production `main`' — real consequences are present. But there is no dedicated 'Why' section; consequences are buried in the failure analysis table. |
| c13 | Output's "How to apply" gives a concrete trigger pattern — "before any `git push --force` command, mentally tick: am I in the right repo? am I on the right branch? am I overwriting commits I shouldn't?" — with optional shell helper or alias suggestion | PARTIAL | Rule field provides concrete steps (`pwd` → `git remote -v` → `git log --oneline -5`) and a trigger ('Before any `git push --force`'), but there is no dedicated 'How to apply' section and no shell helper or alias suggestion. |
| c14 | Output assigns CRITICAL severity given data loss + 2 hours rework + 20-minute deploy freeze impact — explicitly NOT downgraded to Important | PASS | '**Severity:** Critical' is explicitly stated. |
| c15 | Output's failure capture (Step 4) is triggered — produces a failure analysis with root cause (no verification of pwd/remote before destructive command), what was tried (asking platform team for backup), what worked (backup restore), and a prevention rule | PASS | Root cause: 'No working-directory pre-flight check before a destructive command' ✓; Recovery (what tried/worked): 'Platform team backup restore' ✓; Prevention rule: 'Treat `git push --force` like `rm -rf` — always verify context first' ✓. |
| c16 | Output is saved to a file path matching the convention — `~/.claude/learnings/<name>.md` or `.claude/learnings/<name>.md` — and the path is reported in the output | FAIL | Reported path is '`memory/system_git_force_push_wrong_directory.md`' which uses `memory/` prefix, not the expected `~/.claude/learnings/` or `.claude/learnings/` convention. |
| c17 | Output's frontmatter includes the required fields — name, description, type, severity, category — with the type matching the SYSTEM/METHOD/DOMAIN/FEEDBACK classification chosen | FAIL | No frontmatter is shown anywhere in the captured output. The output is a chat summary, not file content. The 'description' and 'type' fields are entirely absent. |
| c18 | Output checks `~/.claude/learnings/` and `.claude/learnings/` for existing learnings on `git push --force` or directory verification before creating a new file, to avoid duplicates | FAIL | No mention of any duplicate check or file listing in the captured output. The output goes directly to the 'Learning Captured' result with no deduplication step described. |

### Notes

The skill produced a concise, readable chat summary that gets the high-level format right (name, category, severity, rule, saved-to, failure analysis) and correctly assigns Critical severity and SYSTEM category. However, the captured output is only a summary — none of the structured file format (frontmatter, What happened, Why, How to apply sections) is demonstrated, the saved path uses `memory/` rather than the required `.claude/learnings/` convention, no reasoning is given for the SYSTEM classification, no deduplication check is evidenced, and incident-specific details (payments-service vs my-feature-branch, exact command verbatim) are missing from the failure narrative. The imperative rule and failure analysis are the strongest parts of the output.
