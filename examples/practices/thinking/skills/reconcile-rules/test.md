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
