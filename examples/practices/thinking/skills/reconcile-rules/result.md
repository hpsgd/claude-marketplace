# Reconcile Rules

Scenario: A developer runs reconcile-rules after a new version of the coding-standards plugin was installed, which now covers ground previously handled by two local learned rules.

## Prompt

> /reconcile-rules all
> 
> (Setup: ~/.claude/rules/ contains `learned--verify-before-declaring-complete.md` and `learned--read-files-before-modifying.md`. The newly installed coding-standards plugin has added `coding-standards--ai-steering.md` which includes "Never assert without verification" and "Read before modifying" as explicit rules. A third learned rule `learned--monorepo-run-full-ci.md` covers something the marketplace does not address.)

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I have all the information needed to do the comparison. Let me present the reconciliation.

---

## Rule Reconciliation

**Scope:** 3 global learned rules vs 1 marketplace rule (`coding-standards--ai-steering.md`)

---

### Superseded (safe to remove)

| Learned rule | Superseded by | Confidence | Reason |
|---|---|---|---|
| `learned--verify-before-declaring-complete.md` | `coding-standards--ai-steering.md` § "Never assert without verification" | **High** | The marketplace section explicitly says "Before saying a test passes: run it / Before saying a file contains X: read it / Before saying a build succeeds: build it" — this is the same principle as the learned rule, stated more broadly. The learned rule's "declaring complete" scenario is a strict subset of "never assert without verification." |
| `learned--read-files-before-modifying.md` | `coding-standards--ai-steering.md` § "Read before modifying" | **High** | The marketplace section is titled "Read before modifying," covers the identical trigger (Edit, Write, shell redirect), and states the same imperative. The learned rule adds "in the same session" as a qualifier, but the marketplace rule is otherwise equivalent and loaded every session. |

### No overlap (keep)

| Learned rule | Covers |
|---|---|
| `learned--monorepo-run-full-ci.md` | Monorepo-specific CI scope: after a change to a shared package, run downstream consumer tests, not just the directly-modified package. No marketplace rule addresses this. |

---

### Summary

- Total learned rules: **3**
- Superseded (remove): **2**
- Partial overlap (review): **0**
- Unique (keep): **1**
- Context tokens saved if cleaned up: **~270 tokens/session** (~28 lines across the two files)

---

**Approve removal of these two files?**

```
$GLOBAL_RULES_DIR/learned--verify-before-declaring-complete.md
$GLOBAL_RULES_DIR/learned--read-files-before-modifying.md
```

Reply "yes" (or "yes, delete them") and I'll remove them and update the reconciliation snapshot. The `learned--monorepo-run-full-ci.md` will be kept as-is.

### Artifacts written

#### `rules/coding-standards--ai-steering.md`

```
---
name: AI Steering — coding-standards plugin
description: AI behavior standards installed by the coding-standards plugin
type: rule
---

## Never assert without verification

Do not make claims about code state, test results, or build outcomes without actually running the relevant check. Asserting something works without verifying it is a form of hallucination.

- Before saying a test passes: run it.
- Before saying a file contains X: read it.
- Before saying a build succeeds: build it.

## Read before modifying

Always read the current state of a file before editing it. Edits made without reading may overwrite existing content or miss context that changes what the correct edit is.

Applies to: all file modifications via Edit, Write, or any shell redirect.

## Type safety first

Prefer typed interfaces over `any`. All public function signatures must have explicit return types.

## Test coverage

New code requires tests. Bug fixes require a regression test.

```

#### `global-rules/learned--read-files-before-modifying.md`

```
---
name: Read files before modifying
description: Always read a file before editing it to avoid overwriting unknown content
type: feedback
---

Always read a file with the Read tool before editing it. Never assume you know what's in a file from context alone.

**Why:** Overwrote content that was already there because I assumed the file matched what I'd written earlier. User lost work.

**How to apply:** Any Edit or Write operation must be preceded by a Read of the target file in the same session. If you haven't read it, read it first.

```

#### `global-rules/learned--monorepo-run-full-ci.md`

```
---
name: Run full CI in monorepos
description: In monorepos, always run CI for all affected packages, not just the package you changed
type: feedback
---

When making changes in a monorepo, run the full CI suite (or at minimum the cross-package impact check) rather than only testing the package you directly modified.

**Why:** Changed a shared utility in packages/core. Only ran tests for packages/core — passed. packages/api consumed that utility and its tests failed in CI. Caught after merge.

**How to apply:** After any change to a shared package, identify downstream consumers and run their tests too. If a workspace-level CI command exists (e.g., `pnpm -r test`, `nx affected --target=test`), prefer it over per-package runs.

```

#### `global-rules/learned--verify-before-declaring-complete.md`

```
---
name: Verify before declaring complete
description: Always verify the actual state of the work before telling the user the task is done
type: feedback
---

Never declare a task complete without verifying the outcome. Run the relevant check (test, build, read the file, confirm the API response) before saying "done."

**Why:** Declared a fix complete without running the tests. The tests still failed. User had to point it out. Cost two extra turns and broke trust.

**How to apply:** Before any "done" / "complete" / "finished" message, verify: run the test, read the file, check the output.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/17.0 (82%) |
| Evaluated | 2026-05-01 |
| Target duration | 99016 ms |
| Target cost | $0.1935 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 inventories rules from both global and project-level locations using actual file reads — not assumptions about what's installed | PARTIAL | The output opens with 'I have all the information needed to do the comparison' and jumps directly to the reconciliation table. No explicit inventory step or file-read operations are shown. However, content quoted in the output (e.g. 'in the same session' qualifier from the learned rule; specific bullet points from the marketplace rule) matches the artifacts, implying reads occurred — but no explicit enumeration step is demonstrated. |
| c2 | Each rule's core imperative is extracted from its content, not just inferred from the filename | PASS | For the superseded rules, the output cites specific body content: 'Before saying a test passes: run it / Before saying a file contains X: read it' from the marketplace rule, and the 'in the same session' qualifier from the learned rule. For the monorepo rule, it extracts 'after a change to a shared package, run downstream consumer tests' — all from the rule bodies, not filenames. |
| c3 | `learned--verify-before-declaring-complete` and `learned--read-files-before-modifying` are classified as superseded by the marketplace rule with the specific overlapping content identified | PASS | Both appear in the 'Superseded (safe to remove)' table. For verify-before-declaring-complete: 'marketplace section explicitly says Before saying a test passes: run it / Before saying a file contains X: read it ... the learned rule's declaring complete scenario is a strict subset.' For read-files-before-modifying: 'covers the identical trigger (Edit, Write, shell redirect)' with the 'in the same session' qualifier noted. |
| c4 | `learned--monorepo-run-full-ci` is classified as no overlap (keep) because the marketplace does not address it | PASS | Output places `learned--monorepo-run-full-ci` in the 'No overlap (keep)' table with the explicit note: 'No marketplace rule addresses this.' |
| c5 | Recommendations table distinguishes superseded (safe to remove), partial overlap (review needed), and no overlap (keep) | PASS | Output has a 'Superseded (safe to remove)' section and a 'No overlap (keep)' section. The summary row shows 'Partial overlap (review): **0**', confirming the category exists in the framework even when empty. |
| c6 | Skill presents recommendations and waits for user approval before deleting anything — never auto-deletes | PASS | Output ends: 'Approve removal of these two files? ... Reply "yes" (or "yes, delete them") and I'll remove them.' No files were deleted; the skill explicitly pauses for confirmation. |
| c7 | Context token savings estimate is included in the summary | PASS | Summary table row: 'Context tokens saved if cleaned up: **~270 tokens/session** (~28 lines across the two files)' |
| c8 | After user-approved cleanup, the reconciliation snapshot is updated so the SessionStart hook won't prompt again until plugins change | PARTIAL | The approval prompt states 'I'll remove them and update the reconciliation snapshot' — the intent is stated but no snapshot file was created or updated in the captured artifacts (user approval hasn't been given yet). |
| c9 | Output enumerates rules from BOTH `~/.claude/rules/` (global / marketplace) AND `.claude/rules/` (project / learned) using actual file reads — not assuming the listing | PARTIAL | Output references '3 global learned rules vs 1 marketplace rule' but doesn't explicitly separate the two directory paths (~/.claude/rules/ vs .claude/rules/) or show a file listing from each. The artifacts have separate global-rules/ and rules/ directories, but the output doesn't enumerate them by path. |
| c10 | Output extracts each rule's core imperative from the rule body (e.g. "Always verify before declaring complete" rather than guessing from the filename) | PASS | Imperatives are drawn from body content: the marketplace rule's bullet list is cited verbatim; the learned rule's 'in the same session' qualifier (from the body) is called out; the monorepo rule's 'downstream consumer tests' framing comes from the body, not the filename. |
| c11 | Output classifies `learned--verify-before-declaring-complete` as SUPERSEDED by `coding-standards--ai-steering`'s "Never assert without verification" rule — with the specific overlapping content quoted from both files | PARTIAL | The marketplace rule content is quoted ('Before saying a test passes: run it / Before saying a file contains X: read it / Before saying a build succeeds: build it'). The learned rule is described by scenario ('declaring complete') rather than quoted from its body. Criterion requires quotes from both files; only one side is directly quoted. |
| c12 | Output classifies `learned--read-files-before-modifying` as SUPERSEDED by the marketplace rule's "Read before modifying" — quoting the matching content | PASS | Output cites the marketplace section title 'Read before modifying', its trigger scope '(Edit, Write, shell redirect)', and then the learned rule's differentiating qualifier 'in the same session' — specific textual references drawn from both file bodies. |
| c13 | Output classifies `learned--monorepo-run-full-ci` as KEEP (no marketplace coverage) — explicitly checking the marketplace rules and confirming nothing addresses monorepo CI | PARTIAL | Output asserts 'No marketplace rule addresses this' but does not demonstrate the check (no enumeration of marketplace rules was shown, no explicit comparison against each marketplace rule's scope). The conclusion is stated without showing the reasoning chain. |
| c14 | Output's recommendations table has columns for rule name, classification (Superseded / Partial overlap / No overlap), and recommended action (Remove / Review / Keep) | PARTIAL | The output uses two separate tables rather than one unified table with the required columns. The superseded table has: Learned rule \| Superseded by \| Confidence \| Reason. The no-overlap table has: Learned rule \| Covers. Neither has explicit 'classification' or 'recommended action' columns; those are implied by which table a rule appears in. |
| c15 | Output presents recommendations and STOPS for user approval — never auto-deletes any rule file, even when classification is unambiguous | PASS | Output ends with 'Approve removal of these two files? ... Reply "yes" (or "yes, delete them") and I'll remove them and update the reconciliation snapshot.' No deletion occurred. |
| c16 | Output includes a context-token-savings estimate — e.g. "removing 2 superseded rules saves approximately X tokens per SessionStart" — based on the rule file sizes | PASS | 'Context tokens saved if cleaned up: **~270 tokens/session** (~28 lines across the two files)' — present in the summary section. |
| c17 | Output's partial-overlap (if any) recommendation flags what to review rather than auto-deleting — the user verifies before removal | PASS | No partial-overlap cases exist in this scenario. The summary explicitly shows 'Partial overlap (review): **0**', confirming the framework accounts for the category without violating the criterion. The overall approval-gate pattern applies to all removals. |
| c18 | Output updates the reconciliation snapshot file after user-approved cleanup so the next SessionStart's reconcile prompt is suppressed until the plugin set changes | PARTIAL | The approval prompt says 'I'll remove them and update the reconciliation snapshot' — acknowledging the action, but no snapshot file appears in the artifacts and user approval has not been given. Maximum score is PARTIAL per the ceiling. |

### Notes

The skill produces a high-quality, well-structured reconciliation with accurate supersession analysis and correct keep/remove decisions. Its main weaknesses are procedural transparency: the output skips the explicit inventory/file-read step (jumping straight to conclusions), and doesn't unify the recommendation tables into the single-table format with explicit classification and recommended-action columns the criteria require. Content extraction from rule bodies is solid, and the approval gate before any deletion is correctly implemented. The reconciliation snapshot update is mentioned prospectively but not demonstrated. Token-savings estimate and the monorepo 'keep' decision are both correct. Overall the skill satisfies the core use-case competently.
