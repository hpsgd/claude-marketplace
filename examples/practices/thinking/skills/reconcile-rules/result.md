# Output: reconcile-rules cleanup after marketplace update

**Verdict:** PASS
**Score:** 17/17 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Step 1 inventories rules from both global and project-level locations using actual file reads — met. Step 1 defines bash commands for both `~/.claude/rules/learned--*.md` and `.claude/rules/learned--*.md` and instructs "Read every rule file — both learned and marketplace." The `all` argument triggers both locations.
- [x] PASS: Each rule's core imperative is extracted from its content, not just inferred from the filename — met. Step 1 instructs extracting "the core imperative (the actual rule statement)" from each file read, not the filename.
- [x] PASS: `learned--verify-before-declaring-complete` and `learned--read-files-before-modifying` classified as superseded — met. Step 2 defines full supersession with concrete examples, and the comparison logic produces this outcome for rules fully covered by `coding-standards--ai-steering.md`. The table format includes a "Reason" column for quoting the overlapping content.
- [x] PASS: `learned--monorepo-run-full-ci` classified as no overlap (keep) — met. Step 2 defines "No overlap: The learned rule covers something the marketplace doesn't address at all. Keep it." The scenario confirms no marketplace rule covers general monorepo CI.
- [x] PASS: Recommendations table distinguishes superseded, partial overlap, and no overlap — met. Step 3 defines all three sections with distinct table formats and actions (Remove / Review / Keep).
- [x] PASS: Skill presents recommendations and waits for user approval before deleting — met. Step 3 ends "Wait for the user to approve removals before deleting anything." Step 4 is gated on user approval. The Rules section adds "Never auto-delete. This skill recommends. The user decides."
- [x] PASS: Context token savings estimate included in summary — met. Step 3 summary template includes "Context tokens saved if cleaned up: ~[estimate based on file sizes]" as a required field. The Rules section gives a concrete calculation example.
- [~] PARTIAL: After user-approved cleanup, reconciliation snapshot is updated — partially met. Step 4 includes a complete Python script to write `~/.claude/learnings/reconcile-snapshot.json`. The mechanism is defined and functional but is conditional on user approval completing Step 4.

### Output expectations

- [x] PASS: Output enumerates rules from BOTH `~/.claude/rules/` and `.claude/rules/` using actual file reads — met. Step 1 bash commands cover both locations and Step 1 instructs reading every rule file found.
- [x] PASS: Output extracts each rule's core imperative from the rule body — met. Step 1 explicitly says to read each file and extract "the core imperative (the actual rule statement)."
- [x] PASS: Output classifies `learned--verify-before-declaring-complete` as SUPERSEDED by `coding-standards--ai-steering`'s "Never assert without verification" — met. Step 2's full supersession definition and comparison logic produces this; the table includes a Reason column for quoting matching content from both files.
- [x] PASS: Output classifies `learned--read-files-before-modifying` as SUPERSEDED by the marketplace rule's "Read before modifying" — met. Same comparison logic applies.
- [x] PASS: Output classifies `learned--monorepo-run-full-ci` as KEEP — met. The no-overlap category handles this explicitly; the skill's "Err toward keeping" rule reinforces it when uncertain.
- [x] PASS: Output's recommendations table has columns for rule name, classification, and recommended action — met. Step 3 defines table schemas for each category with appropriate columns.
- [x] PASS: Output presents recommendations and STOPS for user approval — met. Three separate enforcement points: end of Step 3, Step 4 header, and the Rules section's "Never auto-delete" statement.
- [x] PASS: Output includes a context-token-savings estimate based on rule file sizes — met. Summary template includes the estimate; the Rules section demonstrates the calculation approach with a worked example.
- [x] PASS: Output's partial-overlap recommendation flags what to review rather than auto-deleting — met. The partial-overlap table includes a "What's extra in learned" column and a Recommendation column; the "Err toward keeping" rule ensures the default is keep, not remove.
- [~] PARTIAL: Output updates the reconciliation snapshot after user-approved cleanup — partially met. Step 4 defines a complete Python script to write the snapshot. Correctly gated on user approval rather than auto-executing; the mechanism is present and functional.

## Notes

The three-tier classification system (superseded / partial / no overlap) with an explicit "Err toward keeping" default is well-calibrated — the risk asymmetry (false removal is worse than slight duplication) is acknowledged and built into the default. The token savings estimate converts an abstract cleanup recommendation into a quantified cost, which aids user approval decisions. The snapshot update in Step 4 closes the lifecycle loop: cleanup resets the SessionStart trigger so reconcile doesn't surface again until the plugin set changes. The skill scores cleanly across all criteria; the two PARTIAL ratings reflect the correctly conditional nature of post-approval steps, not gaps in the definition.
