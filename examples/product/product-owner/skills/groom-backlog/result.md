# Output: Groom backlog

**Verdict:** FAIL
**Score:** 11.5/17 criteria met (68%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines a structured multi-step process — met: 6 explicit ordered steps with "Do not skip steps" stated at the top
- [x] PASS: Skill requires RICE scoring — met: Step 4 covers Reach, Impact, Confidence, Effort with formula `(R × I × C) / E` and scoring guides for each factor
- [x] PASS: Skill defines a classification system with at least Ready, Needs Refinement, and Blocked — met: all three are present in Step 2, plus a fourth state (Stale)
- [x] PASS: Skill requires dependency mapping — met: Step 5 is a dedicated dependency mapping step with a named format and cycle-detection requirement
- [x] PASS: Skill specifies what "Ready" means — met: Step 2 lists five explicit, conjunctive criteria for Ready; items must satisfy all five
- [x] PASS: Skill requires output as a structured table or list — met: Output Format section specifies markdown tables with explicit column headers
- [~] PARTIAL: Skill addresses items that lack sufficient data to score — partially met: Confidence scoring includes 50% = "gut feel, untested hypothesis, no data" and Reach says "state the assumption explicitly." Data gaps are acknowledged in scoring guidance, but no specific procedure exists for items that are entirely unscoreable (e.g., flag and skip vs. force a 50% confidence)
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met: all three present in lines 2-4

### Output expectations

- [x] PASS: Output works through all 24 backlog items — met by design: skill collects every item in Step 1 and processes all of them through Steps 2-6; no top-N shortcut exists
- [ ] FAIL: Output classifies items by type (bugs vs. tech debt vs. features) with type-appropriate prioritisation — not met: the skill classifies by readiness state only; no item-type classification logic, no separate tech-debt track, no guidance on how bugs with revenue impact compete with features
- [ ] FAIL: Output's RICE scoring shows all four columns numerically — not met: the Output Format table has a single "RICE" column, not four separate columns for Reach, Impact, Confidence, and Effort; the formula is defined but the output schema does not expose the components per item
- [ ] FAIL: Output flags items with insufficient data — naming the specific missing data per item — not met: skill uses a 50% confidence tier for low-data items but does not instruct the agent to produce a per-item "data needed" flag naming what is missing
- [x] PASS: Output's "Ready" definition is concrete — met: Step 2 Ready criteria require acceptance criteria, one-sprint size, identified dependencies, a stated "why," and no open questions
- [x] PASS: Output's dependency map identifies blocking relationships by name — met: Step 5 produces a named dependency map showing which items depend on which others, with cycle flagging
- [x] PASS: Output's sprint candidates are based on RICE ranking + capacity + dependencies — met: Step 6 "Schedule Next" orders by RICE and Step 5 dependency mapping informs sequencing; no blind "top 5 by RICE" shortcut
- [ ] FAIL: Output's data-gap recommendations are actionable with effort estimates — not met: skill does not instruct the agent to produce actionable data-collection recommendations with effort estimates; data gaps surface only as a confidence-tier signal
- [ ] FAIL: Output produces a table with Item | Type | State | RICE | Dependencies | Reasoning columns — not met: the Output Format table uses Priority | Item | RICE | Size | Dependencies | Notes; no Type column, no State column in the schedule table, no Reasoning column
- [~] PARTIAL: Output addresses stale items >6 months old — partially met: skill defines a Stale category and produces a "Recommended for Closure" list, but the threshold is 30+ days inactivity, not 6 months; no mandatory archive/reconfirm distinction for long-stale items

## Notes

The skill is structurally solid on process and RICE mechanics. The main gaps are on the output side: no item-type axis (bugs vs. features vs. tech debt), no four-column RICE breakdown in the output table, no per-item data-gap flagging with named missing inputs, no actionable data-collection recommendations, and an output table schema that differs from what the test expects. The Stale threshold (30 days) is also weaker than the test's 6-month archive boundary.
