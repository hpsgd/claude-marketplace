# Output: Groom backlog

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines a structured multi-step process — met: 6 explicit ordered steps with "Follow every step below in order. Do not skip steps." stated at the top
- [x] PASS: Skill requires RICE scoring — met: Step 4 covers Reach, Impact, Confidence, Effort with formula `RICE = (Reach x Impact x Confidence) / Effort` and scoring guides for each factor
- [x] PASS: Skill defines a classification system with at least Ready, Needs Refinement, and Blocked — met: all three present in Step 2, plus a fourth state (Stale)
- [x] PASS: Skill requires dependency mapping — met: Step 5 is a dedicated dependency-mapping step with a named format and cycle-detection requirement
- [x] PASS: Skill specifies what "Ready" means — met: Step 2 lists five explicit, conjunctive criteria; all five must be true
- [x] PASS: Skill requires output as a structured table — met: Output Format section specifies four markdown tables with explicit column headers
- [x] PASS: Skill addresses items that lack sufficient data to score — met: Step 4 "When an item cannot be scored" gives a 4-point explicit procedure: mark `data needed`, name the specific missing input, recommend a data-collection action with effort estimate, and create it as a backlog item
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met: all three present in lines 2-4

### Output expectations

- [x] PASS: Output works through all 24 backlog items — met by design: Step 1 collects every item and Steps 2-6 process all of them; no top-N shortcut exists
- [x] PASS: Output classifies items by type with type-appropriate prioritisation — met: Step 1 tags each item as Bug / Tech Debt / Feature and Step 6 applies explicit type-aware rules (bugs with revenue impact compete with features on RICE; tech debt gets its own track at 15-25% capacity)
- [x] PASS: Output's RICE scoring shows all four columns numerically — met: Output Format table has separate Reach, Impact, Confidence, Effort, and RICE columns; the example row shows actual values in each column
- [x] PASS: Output flags items with insufficient data naming the specific missing input — met: Step 4 requires naming "the specific missing input" per unscoreable item, with examples ("need usage analytics for export feature", "need sales-team interview to confirm enterprise demand")
- [x] PASS: Output's "Ready" definition is concrete — met: Step 2 Ready criteria require acceptance criteria, one-sprint size, identified dependencies, stated "why," and no open questions
- [x] PASS: Output's dependency map identifies blocking relationships by name — met: Step 5 produces a named dependency map showing which items depend on which others, with cycle-detection requirement
- [x] PASS: Output's sprint candidates are based on RICE ranking + capacity + dependencies — met: Step 6 "Schedule Next" orders by RICE, and Step 5 dependency mapping informs sequencing; no blind "top 5 by RICE" shortcut
- [x] PASS: Output's data-gap recommendations are actionable with effort estimates — met: Step 4 explicitly requires "Recommend the data-collection action with an effort estimate" and shows examples like "instrument the export endpoint (S, ~2 days)"
- [x] PASS: Output produces a structured table with Item | Type | State | RICE | Dependencies | Reasoning — met: Output Format table is `Item | Type | State | Reach | Impact | Confidence | Effort | RICE | Dependencies | Reasoning`
- [~] PARTIAL: Output addresses stale items >6 months old with archive/reconfirm distinction — partially met: the Stale category exists and "Recommended for Closure" section produces per-item rationales; the threshold is 30+ days inactivity (stricter than 6 months), but there is no specific guidance on archiving vs. reconfirming items that are very long-stale (>6 months), and the output table template does not distinguish these

## Notes

The SKILL.md edit has substantially closed the gaps from the previous run. The three additions that changed the verdict: Type tagging in Step 1 with type-aware prioritisation logic, the explicit "When an item cannot be scored" procedure in Step 4 with named-input and effort-estimate requirements, and the expanded Output Format table with separate RICE component columns and a Reasoning column.

The only remaining gap is the stale-item handling. The 30-day threshold catches everything the 6-month criterion covers, but the skill does not distinguish between "stale for 2 months" and "stale for 18 months" — both get the same Recommended for Closure treatment. A note about reconfirming very long-stale items (e.g., stakeholder sign-off required before closing items older than 6 months) would address this fully.
