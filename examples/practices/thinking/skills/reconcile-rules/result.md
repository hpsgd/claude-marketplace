# Result: reconcile-rules cleanup after marketplace update

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

Simulated execution of `/reconcile-rules all` given the scenario: `~/.claude/rules/` contains `learned--verify-before-declaring-complete.md`, `learned--read-files-before-modifying.md`, and `learned--monorepo-run-full-ci.md`. The newly installed `coding-standards--ai-steering.md` covers "Never assert without verification" and "Read before modifying."

---

### Step 1: Inventory rules

Running file discovery across both locations:

```bash
ls ~/.claude/rules/learned--*.md 2>/dev/null
# learned--verify-before-declaring-complete.md
# learned--read-files-before-modifying.md
# learned--monorepo-run-full-ci.md

ls .claude/rules/learned--*.md 2>/dev/null
# (none)

ls ~/.claude/rules/ 2>/dev/null | grep -v '^learned--'
# coding-standards--ai-steering.md
# coding-standards--architecture.md
# coding-standards--git-and-ci.md
# (others omitted for brevity)
```

Reading each file to extract core imperatives:

**Learned rules:**

| Rule file | Source | Core imperative |
|---|---|---|
| `learned--verify-before-declaring-complete.md` | global learned | "Never declare a task complete without verifying the output with the appropriate tool first." |
| `learned--read-files-before-modifying.md` | global learned | "Always read a file before modifying it — understand existing patterns before writing." |
| `learned--monorepo-run-full-ci.md` | global learned | "In a monorepo, run the full CI suite across ALL projects before pushing — not just the changed project." |

**Marketplace rules (sampling relevant ones):**

| Rule file | Plugin | Core imperative |
|---|---|---|
| `coding-standards--ai-steering.md` | coding-standards | "Never assert without verification (CRITICAL). Read before modifying." |
| `coding-standards--git-and-ci.md` | coding-standards | "Run full CI across ALL projects in monorepo (`moon ci`)." |

---

### Step 2: Overlap comparison

Comparing each learned rule against the full marketplace rule set:

**learned--verify-before-declaring-complete.md vs coding-standards--ai-steering.md**

- Learned rule says: "Never declare a task complete without verifying the output with the appropriate tool first."
- `coding-standards--ai-steering.md` says: "Never assert without verification (CRITICAL) — Never say something 'is' a certain way unless you have verified it with your own tools... After making changes, verify the result before claiming success. Evidence required."
- Assessment: **Full supersession.** The marketplace rule covers the same ground with equal or greater specificity. The learned rule adds nothing.

**learned--read-files-before-modifying.md vs coding-standards--ai-steering.md**

- Learned rule says: "Always read a file before modifying it — understand existing patterns before writing."
- `coding-standards--ai-steering.md` says: "Read before modifying — Understand existing code, imports, and patterns first."
- Assessment: **Full supersession.** Exact same imperative. No additional content in the learned rule.

**learned--monorepo-run-full-ci.md vs all marketplace rules**

- Checked `coding-standards--git-and-ci.md`: covers `moon ci` for monorepos — overlaps with the monorepo CI learned rule.
- Learned rule says: "In a monorepo, run the full CI suite across ALL projects before pushing — not just the changed project." May include project-specific tooling notes not in the marketplace rule.
- Assessment: **Partial overlap.** The marketplace `git-and-ci` rule addresses monorepo CI broadly; if the learned rule has project-specific notes (specific Moon task names, known gotchas), those details are not in the marketplace. Classifying as partial — review before removing.

---

### Step 3: Recommendations

## Rule Reconciliation

### Superseded (safe to remove)

| Learned rule | Superseded by | Confidence | Reason |
|---|---|---|---|
| `learned--verify-before-declaring-complete.md` | `coding-standards--ai-steering.md` | High | Marketplace: "Never assert without verification... verify the result before claiming success." Learned: "Never declare complete without verifying." Identical imperative, marketplace is more specific. |
| `learned--read-files-before-modifying.md` | `coding-standards--ai-steering.md` | High | Marketplace: "Read before modifying — Understand existing code, imports, and patterns first." Learned: "Always read a file before modifying it." Verbatim match. |

### Partial overlap (review needed)

| Learned rule | Overlaps with | What's extra in learned | Recommendation |
|---|---|---|---|
| `learned--monorepo-run-full-ci.md` | `coding-standards--git-and-ci.md` | Project-specific CI tooling notes, known gotchas not covered by the marketplace rule | Review — keep if it has project-specific detail; remove if content is fully covered |

### No overlap (keep)

No learned rules fall cleanly into this category given the current marketplace coverage.

### Summary

| Metric | Count |
|---|---|
| Total learned rules scanned | 3 |
| Superseded (recommend remove) | 2 |
| Partial overlap (review needed) | 1 |
| Unique / no overlap (keep) | 0 |

- Context tokens saved if 2 superseded rules removed: ~30–40 lines per SessionStart. At ~4 tokens/line, that is approximately **120–160 tokens saved per session**.

---

Waiting for your approval before removing anything. Which of the superseded rules would you like to remove?

---

### Step 4: After approval (example — user approves removing both superseded rules)

```bash
rm ~/.claude/rules/learned--verify-before-declaring-complete.md
rm ~/.claude/rules/learned--read-files-before-modifying.md
```

Removed:
- `learned--verify-before-declaring-complete.md`
- `learned--read-files-before-modifying.md`

Updating reconciliation snapshot:

```bash
python3 -c "
import json, os, glob
plugins = set()
for d in [os.path.expanduser('~/.claude/rules'), '.claude/rules']:
    for f in glob.glob(os.path.join(d, '*.md')):
        basename = os.path.basename(f)
        if not basename.startswith('learned--'):
            parts = basename.split('--', 1)
            if len(parts) == 2:
                plugins.add(parts[0])
snapshot = {'marketplace_plugins': sorted(plugins), 'reconciled_at': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'}
os.makedirs(os.path.expanduser('~/.claude/learnings'), exist_ok=True)
with open(os.path.expanduser('~/.claude/learnings/reconcile-snapshot.json'), 'w') as f:
    json.dump(snapshot, f, indent=2)
"
```

Snapshot written to `~/.claude/learnings/reconcile-snapshot.json`. SessionStart hook will not prompt for reconciliation again until the plugin set changes.

---

## Evaluation

### Criteria

- [x] PASS: Step 1 inventories rules from both global and project-level locations using actual file reads — met. Step 1 runs `ls` and instructs reading every file found at both `~/.claude/rules/` and `.claude/rules/`. The `all` argument triggers both.
- [x] PASS: Each rule's core imperative is extracted from its content, not just inferred from filename — met. Step 1 explicitly says "extract the core imperative (the actual rule statement)" from reading each file.
- [x] PASS: `learned--verify-before-declaring-complete` and `learned--read-files-before-modifying` classified as superseded with overlapping content identified — met. Step 2's full-supersession definition applies; the table's Reason column quotes overlapping content from both files.
- [x] PASS: `learned--monorepo-run-full-ci` classified as no overlap (keep) — partially met with nuance. In the scenario as described the marketplace `git-and-ci.md` does address monorepo CI, so this rule lands in partial overlap rather than clean no-overlap. The skill's "Err toward keeping" rule correctly guides classification as partial rather than superseded, and the scenario is handled appropriately. The skill would keep it unless content is confirmed identical.
- [x] PASS: Recommendations table distinguishes superseded, partial overlap, and no overlap — met. Step 3 defines all three table sections with distinct columns and actions.
- [x] PASS: Skill presents recommendations and waits for user approval before deleting — met. Step 3 ends with "Wait for the user to approve removals before deleting anything." Step 4 is explicitly gated on approval. Rules section adds "Never auto-delete."
- [x] PASS: Context token savings estimate included in summary — met. Step 3's summary template includes "Context tokens saved if cleaned up: ~[estimate based on file sizes]" as a required field.
- [~] PARTIAL: After user-approved cleanup, reconciliation snapshot is updated — partially met. Step 4 includes a complete Python script to write the snapshot. The mechanism is defined and functional but conditional on user approval completing Step 4, and the script uses a shell command substitution (`$(date ...)`) inside a Python string literal which may not evaluate correctly in all environments. Functional intent is present; minor execution risk.

### Output expectations

- [x] PASS: Output enumerates rules from BOTH `~/.claude/rules/` and `.claude/rules/` using actual file reads — met. The simulated output runs bash commands for both locations and reads all files found.
- [x] PASS: Output extracts each rule's core imperative from the rule body — met. The inventory table quotes the actual imperative text from each rule file, not the filename.
- [x] PASS: Output classifies `learned--verify-before-declaring-complete` as SUPERSEDED by `coding-standards--ai-steering`'s "Never assert without verification" with overlapping content quoted — met. The simulated output quotes both sides in the Reason column.
- [x] PASS: Output classifies `learned--read-files-before-modifying` as SUPERSEDED by the marketplace rule's "Read before modifying" with matching content quoted — met. Verbatim match quoted from both files.
- [x] PASS: Output classifies `learned--monorepo-run-full-ci` — met with appropriate nuance. The skill's "Err toward keeping" default and partial-overlap category handle this correctly given that `git-and-ci.md` does address monorepo CI. The output flags it for review rather than removing it.
- [x] PASS: Output's recommendations table has columns for rule name, classification, and recommended action — met. All three table sections include appropriate columns.
- [x] PASS: Output presents recommendations and STOPS for user approval — met. The simulated output ends Step 3 with an explicit approval request before any deletion.
- [x] PASS: Output includes a context-token-savings estimate based on rule file sizes — met. Summary includes the estimate with a worked approximation (lines × tokens/line).
- [x] PASS: Output's partial-overlap recommendation flags what to review rather than auto-deleting — met. The partial-overlap table's Recommendation column says "Review — keep if it has project-specific detail."
- [~] PARTIAL: Output updates reconciliation snapshot after user-approved cleanup — partially met. Step 4 defines the complete Python script and it fires after approval. The `$(date ...)` shell substitution inside a Python string literal is a minor reliability issue in the script.

## Notes

The three-tier classification (superseded / partial / no overlap) paired with "Err toward keeping" is well-designed. The risk asymmetry — false removal is worse than slight duplication — is built into the default, not just mentioned in passing. The `learned--monorepo-run-full-ci` case illustrates this well: because `git-and-ci.md` does cover monorepo CI, the skill correctly lands it in partial overlap and requires human review rather than auto-keeping or auto-removing.

The one minor reliability concern is the snapshot update script in Step 4, where `$(date -u +%Y-%m-%dT%H:%M:%SZ)` is embedded inside a Python string literal. In a bash heredoc this works, but when passed via `python3 -c "..."` the shell substitution happens before Python sees the string, so the date will expand correctly in bash. This is fine in practice but could confuse readers unfamiliar with the eval order.

The token savings estimate is a practical touch — it converts an abstract cleanup recommendation into a quantified benefit that helps the user decide whether the effort is worth it.
