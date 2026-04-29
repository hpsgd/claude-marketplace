# Output: Feedback synthesis

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14.5/18 criteria met (81%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill themes feedback using user language — met. Step 3 Rule 1 explicitly mandates theme names come from user language with contrasting examples ("Can't find the export button" not "Export discoverability deficit").
- [x] PASS: Skill applies a quantified impact scoring formula — met. Step 6 defines Impact = Severity × Frequency × Segment weight with exact numeric scales for all three variables.
- [x] PASS: Skill tracks trends — met. Step 4 requires trend direction (increasing, stable, or decreasing) per theme, with explicit handling for undated feedback ("trend unknown").
- [x] PASS: Skill produces prioritised recommendations linked to themes — met. Step 7 requires each recommendation to name the theme with count and trend, state a specific action, cite evidence, and estimate reach.
- [x] PASS: Skill requires an ingest step before categorising — met. Step 1 requires reading every piece of feedback and counting total data points before proceeding to categorisation.
- [x] PASS: Skill distinguishes between customer segments when quantifying impact — met. Step 4 requires segment concentration per theme; Step 6 applies 1.5× weight for Enterprise/paid vs 1.0× for Free/Unknown.
- [x] PARTIAL: Skill identifies feedback that indicates churn risk — fully met, exceeding the partial threshold. Step 5 Pattern Detection includes an explicit "Silent churn signal" pattern (Complaints + no feature requests from same users) with the interpretation "These users have stopped asking and may leave." This is a named, required detection step, not just negative sentiment tracking.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met. Frontmatter on lines 1–7 contains all three required fields.

### Output expectations

- [x] PASS: Output processes both data sources — Step 1 instructs ingesting all feedback from $ARGUMENTS across all sources; the Step 7 summary table requires listing sources with counts. Cross-source pattern detection is enabled by Step 2 recording source per data point and Step 5 scanning across the full dataset.
- [ ] FAIL: Output's themes are named in user language — the skill mandates this in Step 3 Rule 1 and would produce user-language theme names. However, this criterion tests the output itself given the prompt's two specific data sources (tickets + NPS). The skill provides no worked example of what a synthesised theme name looks like for this kind of input; it only gives generic guidance. The criterion is behavioural and can only be assessed against actual output — not verifiable from the definition alone.
- [x] PASS: Output's impact scoring formula is shown explicitly per theme — Step 6 defines the formula with named numeric scales, and Step 7 includes an "Impact score" column in the theme table. The skill would produce explicit numeric scores per theme, not qualitative labels.
- [ ] FAIL: Output identifies trends per theme with the math — Step 4 requires trend direction (increasing/stable/decreasing) and the theme table in Step 7 includes a Trend column. However, the skill gives no instruction to show the underlying arithmetic (e.g. "23 last quarter, 87 this quarter — 3.8x increase"). It states the direction only, not the period-over-period counts that derive it.
- [x] PASS: Output segments the impact — Step 4 requires segment concentration per theme and Step 6 names the segment weight applied (Enterprise/paid 1.5×, Free 1.0×). The theme table includes a Segment column. The skill would produce named segment weights per theme.
- [x] PASS: Output's recommendations are linked to themes — Step 7 mandates each recommendation names its theme with count and trend, states a specific action, cites evidence quotes, and estimates reach. This is a structural requirement, not a guideline.
- [~] PARTIAL: Output's churn-risk flagging identifies explicit churn signals — Step 5 flags "Silent churn signal" (Complaints + no feature requests) and Step 2 categorises "I'm considering switching" as a Complaint. Repeat tickets from the same account and NPS detractors are not explicitly surfaced as churn signals in their own right. Partially met.
- [x] PASS: Output's prioritisation recommends 3-5 specific actions — Step 7 "Top 3 recommendations" section requires specific actions with theme, evidence, reach, and rationale. The format is well-specified and would produce concrete actions, not vague suggestions.
- [ ] FAIL: Output addresses theme novelty — the skill has no instruction to flag themes that are new this quarter vs. themes that have appeared in prior periods. Trend direction covers increasing/stable/decreasing for known themes but there is no "new signal" flag for themes with no prior-period history.
- [~] PARTIAL: Output identifies positive feedback themes — Step 2 includes a Praise category and Step 5 includes a "Praise cluster" pattern. However, the skill's recommendations section ("Top 3 recommendations") and scoring formula (Severity × Frequency × Segment weight) both skew toward problems. Positive themes appear in the theme table and pattern detection, but the skill does not explicitly instruct surfacing "what to protect and amplify" as a distinct output section. Partially met.

## Notes

The skill is strong on structural elements: ingest-before-categorise, quantified scoring, segment weighting, and the pattern detection table are all well-specified. The three output expectation gaps are worth noting:

**Trend math not required.** The skill asks for trend direction but not the underlying period-over-period calculation. An output could say "increasing" without showing "23 last quarter → 87 this quarter." The output expectation requires the math; the skill doesn't mandate it.

**No new-theme flagging.** The "new signal" flag is a meaningful early-warning feature that requires comparing this period's theme list against a prior baseline. The skill has no concept of prior-period comparison beyond trend direction on existing themes.

**Positive themes underweighted in output structure.** Praise and praise clusters appear in the framework but the output format does not include a dedicated section for what's working well. Teams using this skill for product decisions need the positive signal to know what to protect, not just what to fix.

One minor robustness gap noted previously: no fallback for missing segment data. If segment information is absent from input, the 1.5× enterprise weight cannot be applied and the skill gives no guidance for handling the unknown-segment case beyond assigning 1.0×.
