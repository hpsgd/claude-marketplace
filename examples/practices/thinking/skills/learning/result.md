# Learning capture after a mistake

A developer just force-pushed to the wrong branch and wants to capture the incident as a learning immediately after it happened.

## Prompt

> /learning Capture this: I just ran `git push --force origin main` from the wrong directory — I was in the `payments-service` repo but thought I was in `my-feature-branch` project. Pushed over 3 commits on `origin/main` in the payments-service repo. Had to ask the platform team to restore from their backup. This wasted about 2 hours and caused a 20-minute deploy freeze.

```markdown

## Output

**Step 1: Classify**

Category: SYSTEM — this is about tooling and environment context, not domain knowledge or user feedback. The mistake was caused by operating in the wrong system context (wrong directory/repo).

**Step 2: Write the learning**

Saving to `~/.claude/memory/learned--verify-repo-before-force-push.md`:

---
name: verify-repo-before-force-push
description: Always verify current repo and branch before running destructive git commands (force push, reset --hard, branch -D)
type: feedback
---

A force-push to origin/main in the payments-service repo overwrote 3 commits because the working directory was wrong. The platform team had to restore from backup. 2 hours of rework + 20-minute deploy freeze.

**Learning:** Always run `git remote -v` and `git branch --show-current` immediately before any force-push or destructive git operation. Verify the repo name and branch match your intent before executing.

**Why:** Force-push is irreversible at the git level. If the target is wrong, recovery requires a backup restore (if one exists) and platform team coordination. Even 30 seconds of verification prevents hours of recovery.

**How to apply:** Before `git push --force`: (1) run `git remote -v` — confirm repo name matches intent, (2) run `git branch --show-current` — confirm branch matches intent, (3) only then execute.


| Field | Value |
|---|---|
| Severity | Critical |
| Category | SYSTEM |


---

**Step 3: Rate severity**

Critical — the incident caused data loss (3 commits overwritten), required backup restoration, 20 minutes of deploy freeze, and 2 hours of engineer rework. This meets the Critical threshold.

**Step 4: Failure capture**

#### Failure Analysis

**What happened:** `git push --force origin main` executed in the payments-service repo while intending to operate in a different repository. Working directory was not verified.

**Root cause:** No verification step before executing a destructive command. Git does not prompt for confirmation on force-push.

**What was tried:** None noted — the push executed immediately.

**What worked:** Platform team restored from their backup snapshot.

**Prevention rule:** Never execute `git push --force` without first running `git remote -v` and reading the output.

---

### Learning Captured


| Field | Value |
|---|---|
| Name | verify-repo-before-force-push |
| Category | SYSTEM |
| Severity | Critical |
| Rule | Always verify `git remote -v` and `git branch --show-current` immediately before any force-push or destructive git operation |
| Saved to | `~/.claude/memory/learned--verify-repo-before-force-push.md` |

```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Step 1 assigns a category with reasoning — the skill defines Step 1 as mandatory with four categories (SYSTEM, METHOD, DOMAIN, FEEDBACK) and an output table. The definition states "Output: Category assignment with reasoning." SYSTEM is appropriate for a tooling/environment context error.
- [x] PASS: Step 2 writes learning in the exact format — the skill defines exact frontmatter fields (name, description, type) and exact body fields (What happened, Learning, Why, How to apply, Severity, Category). Step 2 is labelled "mandatory." All required fields are present in the definition's template.
- [x] PASS: Learning stated as imperative rule — the Rules section states "The learning must be stated as a rule, not a narrative. 'Always X when Y' not 'I noticed that sometimes...'" The imperative form is explicitly required. "Always run `git remote -v`..." is correct form.
- [x] PASS: "Why" field explains consequence of ignoring — the Rules section states "The why must explain the consequence of ignoring it, not just restate the learning." The distinction (consequence vs restatement) is explicitly defined in the skill.
- [x] PASS: Critical severity assigned — Step 3's severity table defines "Critical: Caused visible damage, data loss, or significant rework. Must not happen again." The scenario has all three: data loss (3 commits overwritten), significant rework (2 hours), and a deploy freeze. The Rules section states "Severity must be honest. Downgrading severity to avoid embarrassment defeats the purpose." Critical is the only defensible rating.
- [x] PASS: Step 4 failure capture triggered — the skill states Step 4 applies "when something goes notably wrong (user frustration, rework needed, significant mistake)." The scenario unambiguously qualifies. Step 4's template requires: What happened, Root cause, What was tried, What worked, Prevention rule — all five fields are defined in the template.
- [x] PASS: Output follows "When capturing" format — the skill's Output Format section defines the exact "When capturing" template with Name, Category, Severity, Rule, and Saved-to fields. All five are required and defined.
- [~] PARTIAL: Skill checks for existing learning before creating — the Rules section states "Never duplicate learnings. Before saving, check if an existing learning covers the same ground. Update the existing one instead of creating a new file." This rule is present and mandatory. However, the skill does not include an explicit numbered step for the duplicate check — it is in the Rules section, not in the sequential steps (Step 1 through Step 4). This means the duplicate check depends on the agent reading and applying the Rules section rather than being enforced by a dedicated process step with defined output.

### Notes

The learning skill's format is tightly specified with exact template fields. The severity criteria are clear with concrete examples distinguishing Critical from Important. The Step 4 failure analysis captures incident detail beyond the rule itself — the five-field structure is well-designed for postmortems. One gap: the frontmatter `type` field in the template is hardcoded as `feedback` regardless of the Step 1 category classification (which might be SYSTEM, METHOD, DOMAIN, or FEEDBACK). The `type` field and the `Category` body field serve different purposes but are inconsistently connected in the definition — SYSTEM learnings would have `type: feedback` in frontmatter, which is misleading.
