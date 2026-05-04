# Test: reconcile-rules cleanup after marketplace update

Scenario: A developer runs reconcile-rules after a new version of the coding-standards plugin was installed, which now covers ground previously handled by two local learned rules.

## Prompt

/reconcile-rules all

Treat the following as the actual filesystem state for this reconciliation (the workspace is sandboxed; substitute these values for the real ls / Read results). Do NOT pause to ask permission or check the real filesystem — these ARE the contents to reconcile:

```
~/.claude/rules/ (global, 2 learned rules):
  learned--verify-before-declaring-complete.md  → "Always verify state with tools before declaring a task complete. Never assert without checking."
  learned--read-files-before-modifying.md       → "Always Read a file before Edit. Editing without Read fails."

.claude/rules/ (project-local, 1 learned rule):
  learned--monorepo-run-full-ci.md              → "In monorepos run `moon ci` checking all projects, not just the changed one."

Marketplace rules just installed (via thinking plugin SessionStart hook):
  turtlestack--coding-standards--ai-steering.md → contains explicit rules "Never assert without verification" AND "Read before modifying" (PLUS other rules)
```

A few specifics for the response:

- **Output structure** — include sections in this order:
  1. **Inventory** — list all 5 files (2 global learned, 1 project learned, 1+ marketplace) with their core imperative quoted from content (not just file name).
  2. **Overlap analysis** — table with columns `Learned rule | Marketplace rule | Overlap classification | Recommended action`. Three classifications: SUPERSEDED (safe to remove), PARTIAL OVERLAP (review needed — narrower scope or different angle), NO OVERLAP (keep).
  3. **Per-rule classification**:
     - `learned--verify-before-declaring-complete` → SUPERSEDED by `coding-standards--ai-steering.md` ("Never assert without verification") → recommend remove.
     - `learned--read-files-before-modifying` → SUPERSEDED by `coding-standards--ai-steering.md` ("Read before modifying") → recommend remove.
     - `learned--monorepo-run-full-ci` → NO OVERLAP — marketplace doesn't address monorepo CI specifically → keep.
  4. **User-approval prompt** — present the recommendations and ask for approval before deleting (don't auto-delete).
  5. **Reconciliation snapshot update** — after approval, write the snapshot file (`~/.claude/learnings/reconciliation-snapshot.json` or workspace-local equivalent) so the SessionStart hook knows reconciliation is current.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

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
