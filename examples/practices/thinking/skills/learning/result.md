# Output: learning capture after a mistake

**Verdict:** PARTIAL
**Score:** 13.5/16 criteria met (84%)
**Evaluated:** 2026-04-30

## Simulated output

Given the prompt `/learning Capture this: I just ran 'git push --force origin main' from the wrong directory...`, a model executing this skill would produce the following.

---

**Step 1 — Classify**

Category: **SYSTEM**

Reasoning: The failure was triggered by environmental context — being in the wrong working directory — not by a flawed methodology or missing domain knowledge. The model had no contextual signal to distinguish `payments-service` from `my-feature-branch`. Infrastructure/tooling/environment failures map to SYSTEM. The category is assigned before writing.

---

**Step 2 — Write the learning**

```markdown
---
name: verify-repo-before-force-push
description: Always verify the current directory, remote, and branch before running git push --force — failure causes data loss and requires upstream backup restore
type: feedback
---

Developer ran `git push --force origin main` while working in the `payments-service` repository, believing they were in the `my-feature-branch` project. This overwrote 3 commits on `origin/main` in `payments-service`. Recovery required the platform team to restore from backup, caused a 20-minute deploy freeze, and consumed approximately 2 hours of engineering time.

**Learning:** Never run `git push --force` without first confirming the current working directory (`pwd`), the active remote (`git remote -v`), and the current branch (`git branch --show-current`).

**Why:** A force-push to the wrong remote permanently overwrites history. Recovery depends entirely on whether the hosting platform holds a recent backup. If no backup exists, commits are gone. Even with a backup, the restore causes a deploy freeze and wastes hours of engineering time across multiple people.

**How to apply:** Before any `git push --force` command, run this three-step check: (1) `pwd` — am I in the right repo? (2) `git remote -v` — is the remote pointing where I expect? (3) `git branch --show-current` — am I on the right branch? Consider adding a shell alias that enforces the check: `alias gpf='echo "Remote: $(git remote -v | head -1)" && echo "Branch: $(git branch --show-current)" && echo "Dir: $(pwd)" && read -p "Force push? [y/N] " c && [[ $c == y ]] && git push --force'`

**Severity:** Critical
**Category:** SYSTEM
```

---

**Step 3 — Severity**

**Critical.** The skill's severity table uses "Force-pushed to main and lost 3 commits" as the canonical Critical example. This incident matches exactly: 3 commits overwritten, backup restore required, deploy freeze, 2 hours of rework. No downgrade is warranted.

---

**Step 4 — Failure analysis**

```markdown
### Failure Analysis

**What happened:** `git push --force origin main` executed from `payments-service` repository while the developer believed they were in a different project, overwriting 3 commits on the live main branch.

**Root cause:** No verification of current working directory, remote, or branch before issuing a destructive git command. The shell prompt or terminal tab did not clearly distinguish between the two projects.

**What was tried:** Asked the platform team to restore the branch from backup.

**What worked:** Platform team restored `origin/main` from their backup copy, recovering the 3 lost commits.

**Prevention rule:** Never run `git push --force` without first running `pwd`, `git remote -v`, and `git branch --show-current`. If any of the three does not match expectation, abort.
```

---

**Capture summary**

```markdown
## Learning Captured

**Name:** verify-repo-before-force-push
**Category:** SYSTEM
**Severity:** Critical
**Rule:** Never run `git push --force` without first confirming pwd, remote, and branch — wrong-directory force-pushes cause irreversible data loss requiring upstream backup restore
**Saved to:** ~/.claude/learnings/verify-repo-before-force-push.md
```

---

## Results

### Criteria (against the skill definition)

- [x] PASS: Step 1 assigns a category with reasoning — the skill mandates Step 1 category assignment with reasoning as its mandatory first output; SYSTEM with reasoning is present
- [x] PASS: Step 2 writes the learning in the exact format — the skill's Step 2 template specifies frontmatter (name, description, type) plus What happened, Learning, Why, How to apply, Severity, Category fields; all are present
- [x] PASS: The learning is stated as an imperative rule — the skill's Rules section explicitly requires "Always X when Y" form, not narrative; the definition drives this directly
- [x] PASS: The "Why" field explains the consequence of ignoring the rule — the skill's rules state "The 'why' must explain the consequence of ignoring it, not just restate the learning"; the definition enforces this
- [x] PASS: Step 3 assigns Critical severity — the severity table uses "Force-pushed to main and lost 3 commits" as the canonical Critical example, matching this scenario exactly
- [x] PASS: Step 4 failure capture is triggered — the scenario describes data loss, rework, and a platform team restore; Step 4 defines the five-field failure analysis format as required output when something goes notably wrong
- [x] PASS: Output follows the "When capturing" format — the skill's Output Format section defines the exact template with Name, Category, Severity, Rule, and Saved-to fields
- [~] PARTIAL: Skill checks for existing learning before creating — the Rules section states "Never duplicate learnings. Before saving, check if an existing learning covers the same ground." The obligation is present but there is no procedural step, no tool call sequence, and no path list; the check depends entirely on the model's discretion with no mechanical enforcement

### Output expectations (against the simulated output)

- [x] PASS: Output classifies as SYSTEM with reasoning — force-push from wrong directory is a tooling/environment context failure; the skill's SYSTEM definition ("Infrastructure, tooling, configuration, environment") maps directly; reasoning accompanies the label
- [x] PASS: "What happened" reproduces specific details — the command (`git push --force origin main`), wrong directory (payments-service vs my-feature-branch), 3 commits overwritten, platform team backup restore are all present verbatim
- [x] PASS: Learning stated as an imperative rule — "Never run `git push --force` without first confirming..." satisfies the imperative form requirement
- [x] PASS: "Why" explains the consequence — data loss, dependency on backup existence, deploy freeze, and hours of rework are all present; it does not merely restate the rule
- [~] PARTIAL: "How to apply" gives a concrete trigger pattern with shell helper — the simulated output does include a three-step trigger check and a shell alias; however, the skill definition provides no example that would reliably drive this level of specificity; a model executing the skill without the test's expectations in view might produce a vaguer pattern. Scored 0.5 — the content is present in simulation but the definition does not guarantee it
- [x] PASS: CRITICAL severity assigned — the canonical example in the severity table matches; explicit reasoning given; no downgrade
- [x] PASS: Failure capture triggered with required fields — root cause (no verification before destructive command), what was tried (platform team backup), what worked (restore), and prevention rule are all present
- [x] PASS: Saved to a path matching the convention — `~/.claude/learnings/verify-repo-before-force-push.md` reported in the capture summary
- [x] PASS: Frontmatter includes required fields — name, description, type present in frontmatter; severity and category in body; type field reflects classification (though hardcoded as `feedback` in the template — see Notes)
- [~] PARTIAL: Output checks both learnings paths before creating — the "Never duplicate" rule exists in the Rules section; the skill provides no procedural mechanism (no Glob/Grep step, no path enumeration, no ordering before Step 2) to make the check happen reliably

## Notes

The skill is structurally strong for the core capture flow. The severity table's use of a force-push scenario as its Critical canonical example is a precise design choice — it eliminates ambiguity for exactly this class of incident.

Two gaps that recur across both halves of the rubric:

1. **Duplicate check has no mechanism.** The "Never duplicate learnings" rule in the Rules section is a stated obligation with no execution path. There is no Glob or Grep step before Step 2, no path list to search, no ordering constraint. A model following the skill definition will sometimes remember to check and sometimes will not. The fix is a mandatory pre-Step-2 check: "Glob `~/.claude/learnings/*.md` and `.claude/learnings/*.md`; grep for keywords from `$ARGUMENTS`; if a match is found, update rather than create."

2. **"How to apply" has no template example.** The field is defined as "specific enough that future-you can act on it without remembering the context" but there is no example in the skill that suggests a shell helper or alias as a valid output. The simulated output includes one, but that is the evaluator providing what the definition should have driven. A model executing the skill is likely to produce a vaguer pattern.

One structural inconsistency outside the rubric: the Step 2 frontmatter hardcodes `type: feedback` regardless of the Step 1 classification. A SYSTEM learning carries `type: feedback` in its frontmatter while the body says `Category: SYSTEM`. The template should either use a dynamic placeholder (`type: [SYSTEM/METHOD/DOMAIN/FEEDBACK]`) or rename the frontmatter field to avoid the mismatch silently.
