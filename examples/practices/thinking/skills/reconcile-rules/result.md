# Reconcile rules cleanup after marketplace update

A developer runs reconcile-rules after a new version of the coding-standards plugin was installed, which now covers ground previously handled by two local learned rules.

## Prompt

> /reconcile-rules all
>
> (Setup: ~/.claude/rules/ contains `learned--verify-before-declaring-complete.md` and `learned--read-files-before-modifying.md`. The newly installed coding-standards plugin has added `coding-standards--ai-steering.md` which includes "Never assert without verification" and "Read before modifying" as explicit rules. A third learned rule `learned--monorepo-run-full-ci.md` covers something the marketplace does not address.)

```markdown

## Output

**Step 1: Inventory rules**

```bash
ls ~/.claude/rules/learned--*.md 2>/dev/null
```
Found:
- `~/.claude/rules/learned--verify-before-declaring-complete.md`
- `~/.claude/rules/learned--read-files-before-modifying.md`
- `~/.claude/rules/learned--monorepo-run-full-ci.md`

```bash
ls .claude/rules/learned--*.md 2>/dev/null
```
Not found (no project-level learned rules)

Marketplace rules (non-learned):
```bash
ls ~/.claude/rules/ | grep -v '^learned--'
```
Found:
- `coding-standards--ai-steering.md`
- `coding-standards--git-and-ci.md`
- `writing-style--tone-and-voice.md`

Reading all rule files (extracting core imperatives from content)...

`learned--verify-before-declaring-complete.md`:
Core imperative: "Never say a task is done without verifiable evidence."

`learned--read-files-before-modifying.md`:
Core imperative: "Always read a file's full content before editing it."

`learned--monorepo-run-full-ci.md`:
Core imperative: "In monorepos, always run full CI across ALL projects before pushing."

`coding-standards--ai-steering.md`:
Extracted imperatives include:
- "Never assert without verification" (overlaps verify-before-declaring-complete)
- "Read before modifying" (overlaps read-files-before-modifying)

`coding-standards--git-and-ci.md`:
Key content: "In Moon monorepos: moon ci checks web apps, packages, AND services"

---

**Step 2: Compare for overlap**

`learned--verify-before-declaring-complete` vs `coding-standards--ai-steering.md`:
- Learned: "Never say done without verifiable evidence"
- Marketplace: "Never assert without verification. Never say something 'is' a certain way unless verified"
- Verdict: Full supersession — marketplace covers same ground

`learned--read-files-before-modifying` vs `coding-standards--ai-steering.md`:
- Learned: "Always read full content before editing"
- Marketplace: "Read before modifying. Understand existing code, imports, and patterns first"
- Verdict: Full supersession — marketplace covers same ground

`learned--monorepo-run-full-ci` vs all marketplace rules:
- `coding-standards--git-and-ci.md` mentions "In Moon monorepos: moon ci" — tool-specific
- Learned rule is more general (all monorepos, all CI systems)
- Verdict: Partial overlap — marketplace covers Moon specifically; learned rule is broader

---

### Rule Reconciliation

#### Superseded (safe to remove)

| Learned rule | Superseded by | Confidence | Reason |
|---|---|---|---|
| `learned--verify-before-declaring-complete.md` | `coding-standards--ai-steering.md` | High | "Never assert without verification" covers same imperative |
| `learned--read-files-before-modifying.md` | `coding-standards--ai-steering.md` | High | "Read before modifying" covers same imperative |

#### Partial overlap (review needed)

| Learned rule | Overlaps with | What's extra in learned | Recommendation |
|---|---|---|---|
| `learned--monorepo-run-full-ci.md` | `coding-standards--git-and-ci.md` | General monorepo CI principle (not Moon-specific) | Keep — marketplace only covers Moon monorepos |

#### No overlap (keep)

None — all three learned rules have some marketplace coverage.

#### Summary
- Total learned rules: 3
- Superseded (remove): 2
- Partial overlap (review): 1
- Unique (keep): 0
- Context tokens saved if cleaned up: ~28 lines × 4 tokens/line ≈ ~112 tokens per session

---

Waiting for user approval before removing anything.

Which rules would you like to remove?
- [ ] `learned--verify-before-declaring-complete.md`
- [ ] `learned--read-files-before-modifying.md`
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Step 1 inventories rules from both locations using actual file reads — the skill's Step 1 defines bash commands for both `~/.claude/rules/learned--*.md` and `.claude/rules/learned--*.md` and states "Read every rule file — both learned and marketplace. For each, extract: the description from frontmatter, the core imperative." The `$ARGUMENTS` value of `all` triggers checking both global and project locations. The inventory is built from explicit file reads via bash, not from assumptions.
- [x] PASS: Core imperative extracted from content, not filename — the skill's Step 1 states "For each, extract: the description from frontmatter, the core imperative (the actual rule statement), the evidence/source." The simulation shows the extracted content from each file body, not just the filename. The imperatives quoted are plausible outputs of reading those files.
- [x] PASS: Both learned rules classified as superseded with overlapping content identified — the skill's Step 2 defines "Full supersession: The marketplace rule covers the same ground as the learned rule." Both `verify-before-declaring-complete` and `read-files-before-modifying` are marked High confidence with the specific overlapping text from the marketplace rule quoted alongside the learned rule text.
- [x] PASS: `monorepo-run-full-ci` classified appropriately as partial overlap / keep — the skill's Step 2 defines "Partial overlap: The marketplace rule covers part of the learned rule, but the learned rule has additional specifics not in the marketplace." The comparison correctly identifies that `coding-standards--git-and-ci.md` covers Moon monorepos specifically while the learned rule is tool-agnostic. Classification as partial overlap with recommendation to keep is correct per the skill's Rules section: "Err toward keeping. If you're unsure... classify as 'partial overlap' not 'superseded.'"
- [x] PASS: Recommendations table distinguishes all three categories — the skill's Step 3 output template defines exactly three table sections: "Superseded (safe to remove)", "Partial overlap (review needed)", "No overlap (keep)." All three sections appear in the output with the skill's defined column structure.
- [x] PASS: Skill presents recommendations and waits for approval before deleting — the skill's Step 3 ends with "Wait for the user to approve removals before deleting anything." Step 4 states "Do NOT remove rules the user hasn't explicitly approved." The Rules section states "Never auto-delete." The output ends with a waiting state showing candidate checkboxes.
- [x] PASS: Context token savings estimate included — the skill's Step 3 summary template defines "Context tokens saved if cleaned up: ~[estimate based on file sizes]." The estimate is a required field in the summary block. The simulation calculates ~112 tokens based on file line counts.
- [~] PARTIAL: Reconciliation snapshot updated after cleanup — the skill's Step 4 defines a Python script to write `~/.claude/learnings/reconcile-snapshot.json` after cleanup occurs. This step is defined in the skill and includes the full script. Partial because the snapshot update is conditional on user approval and actual file deletion — it only runs after Step 4's cleanup is executed, which requires both user approval and the agent proceeding through Step 4. The skill includes the mechanism but cannot enforce it without the preceding approvals completing. The criterion asks whether the snapshot update is defined and would run, which it is, but only conditionally.

### Notes

The reconcile-rules skill has a clean three-classification system with a clear ordering (superseded → partial → keep). The "err toward keeping" rule in the Rules section is a sensible conservative default that prevents false removals. The token savings estimate adds a concrete value signal to what would otherwise be an abstract cleanup recommendation. The partial-overlap classification for `monorepo-run-full-ci` is the most interesting case — the skill correctly handles the scenario where a learned rule is partially but not fully subsumed, with the general principle surviving alongside the tool-specific marketplace rule.
