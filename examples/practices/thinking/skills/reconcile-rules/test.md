# Test: reconcile-rules cleanup after marketplace update

Scenario: A developer runs reconcile-rules after a new version of the coding-standards plugin was installed, which now covers ground previously handled by two local learned rules.

## Prompt

/reconcile-rules all

(Setup: ~/.claude/rules/ contains `learned--verify-before-declaring-complete.md` and `learned--read-files-before-modifying.md`. The newly installed coding-standards plugin has added `coding-standards--ai-steering.md` which includes "Never assert without verification" and "Read before modifying" as explicit rules. A third learned rule `learned--monorepo-run-full-ci.md` covers something the marketplace does not address.)

## Criteria

- [ ] PASS: Step 1 inventories rules from both global and project-level locations using actual file reads — not assumptions about what's installed
- [ ] PASS: Each rule's core imperative is extracted from its content, not just inferred from the filename
- [ ] PASS: `learned--verify-before-declaring-complete` and `learned--read-files-before-modifying` are classified as superseded by the marketplace rule with the specific overlapping content identified
- [ ] PASS: `learned--monorepo-run-full-ci` is classified as no overlap (keep) because the marketplace does not address it
- [ ] PASS: Recommendations table distinguishes superseded (safe to remove), partial overlap (review needed), and no overlap (keep)
- [ ] PASS: Skill presents recommendations and waits for user approval before deleting anything — never auto-deletes
- [ ] PASS: Context token savings estimate is included in the summary
- [ ] PARTIAL: After user-approved cleanup, the reconciliation snapshot is updated so the SessionStart hook won't prompt again until plugins change

## Output expectations

- [ ] PASS: Output enumerates rules from BOTH `~/.claude/rules/` (global / marketplace) AND `.claude/rules/` (project / learned) using actual file reads — not assuming the listing
- [ ] PASS: Output extracts each rule's core imperative from the rule body (e.g. "Always verify before declaring complete" rather than guessing from the filename)
- [ ] PASS: Output classifies `learned--verify-before-declaring-complete` as SUPERSEDED by `coding-standards--ai-steering`'s "Never assert without verification" rule — with the specific overlapping content quoted from both files
- [ ] PASS: Output classifies `learned--read-files-before-modifying` as SUPERSEDED by the marketplace rule's "Read before modifying" — quoting the matching content
- [ ] PASS: Output classifies `learned--monorepo-run-full-ci` as KEEP (no marketplace coverage) — explicitly checking the marketplace rules and confirming nothing addresses monorepo CI
- [ ] PASS: Output's recommendations table has columns for rule name, classification (Superseded / Partial overlap / No overlap), and recommended action (Remove / Review / Keep)
- [ ] PASS: Output presents recommendations and STOPS for user approval — never auto-deletes any rule file, even when classification is unambiguous
- [ ] PASS: Output includes a context-token-savings estimate — e.g. "removing 2 superseded rules saves approximately X tokens per SessionStart" — based on the rule file sizes
- [ ] PASS: Output's partial-overlap (if any) recommendation flags what to review rather than auto-deleting — the user verifies before removal
- [ ] PARTIAL: Output updates the reconciliation snapshot file after user-approved cleanup so the next SessionStart's reconcile prompt is suppressed until the plugin set changes
