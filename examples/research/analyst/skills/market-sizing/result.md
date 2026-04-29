# Result: market-sizing skill

**Verdict:** PARTIAL
**Score:** 13/18 criteria met (72%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines the market before producing any figures — Step 1 requires buyer, purchase unit, geography, and time horizon to be stated explicitly. The output format template includes a `Market definition` field. The instruction that "the definition IS the methodology" is structurally enforced.
- [x] PASS: Both top-down and bottom-up estimates are attempted — Step 3 and Rules block: "Top-down and bottom-up must both be attempted. If one genuinely can't be done, explain why." Output format has both rows in the size estimates table.
- [x] PASS: Top-down estimate cites a specific report title, year, and figure — Step 2 requires "specific report title, year published, and exact figure cited" for each analyst estimate. Rule: "Never round-trip a sourced figure without the original citation."
- [x] PASS: Bottom-up estimate shows the calculation explicitly — Step 3 requires showing the calculation as `N customers × $X avg spend × Y% penetration = $Z`. This is hardcoded in the skill instructions.
- [x] PASS: Where top-down and bottom-up figures diverge by more than 2x, skill diagnoses the gap rather than averaging — Step 4: "Don't average them — resolve the discrepancy." Output format has a `### Reconciliation` section. The 2x threshold is explicit.
- [x] PASS: All estimates are labelled as estimates — Rules block: "Label all estimates as estimates. Never present a number as fact unless it comes from a primary regulatory or government source."
- [x] PASS: AU-specific sources are used where available before defaulting to global analyst reports — Step 2 lists IBISWorld AU, ABS, Stats NZ as the first-tier sources. Rule: "For AU/NZ topics, use AU/NZ sources first." Global sources are a fallback.
- [~] PARTIAL: Confidence rating is provided with reasoning — output format has `### Confidence: [High / Medium / Low]` with a reasoning sub-section. The instruction to reason the confidence is present. Scored 0.5 because the skill doesn't define specific criteria for each confidence level — the rating is qualitative and agent-discretionary.

### Output expectations

- [~] PARTIAL: Output's market definition specifies buyer, purchase unit, geography, time horizon, and segment scope (excludes home care, retirement living) — Step 1 covers buyer, purchase unit, geography, and time horizon explicitly. Segment scope exclusions (home care, retirement living) are not instructed anywhere in the skill, so this would be agent-discretionary. Scored 0.5.
- [x] PASS: Output's top-down estimate cites specific AU reports with title, year, and figure — Step 2 lists IBISWorld AU, ABS, government data as first-tier sources and requires title, year, and exact figure for every estimate. Structurally enforced.
- [~] PARTIAL: Output's bottom-up estimate shows the math with ~700-900 providers per Royal Commission data — Step 3 requires showing the calculation with N × $X × Y% and citing each input's source. However, the skill does not mention the Royal Commission as a data source for provider counts, nor does it direct the agent to that specific figure. The math structure is required; the Royal Commission citation is not. Scored 0.5.
- [x] PASS: Output reconciles top-down and bottom-up — Step 4 requires diagnosing the gap if figures diverge by >2x rather than averaging. This is explicit.
- [x] PASS: Output uses AU-specific sources first — Step 2 names IBISWorld AU, ABS, Stats NZ as primary sources before global alternatives. ACQSC and ACSA are consistent with this.
- [ ] FAIL: Output addresses the post-Royal-Commission context (AN-ACC funding model, mandatory care minutes, technology subsidies) — not mentioned anywhere in the skill definition. No instruction to address sector-specific demand drivers.
- [~] PARTIAL: Output's TAM / SAM / SOM breakdown is shown — Rules say "distinguish TAM, SAM, and SOM if the question calls for it." For a pitch deck context this applies, but the skill leaves it conditional and does not instruct the agent to apply this automatically when pitch context is detected. Scored 0.5.
- [x] PASS: Output labels every estimate as "estimate" — Rules block: "Label all estimates as estimates." This is a hard rule, not a suggestion.
- [~] PARTIAL: Output's confidence rating per estimate is shown with reasoning — the skill has `### Confidence: [High / Medium / Low]` with a reasoning sub-section, but it is a single overall confidence rating. The test expects per-estimate confidence (TAM HIGH, penetration MEDIUM, spend per bed LOW). The skill does not instruct per-variable confidence ratings. Scored 0.5.
- [ ] FAIL: Output addresses the pitch context — whether the AU market is large enough to justify Series A alone, and whether NZ / international expansion should feature in the deck — not mentioned in the skill at all. The skill has no awareness of downstream use context.

## Notes

The Criteria section scores well (7.5/8). The Output expectations section reveals the gap: the skill is a solid general-purpose market sizing tool, but the scenario is a pitch deck for a specific regulated sector. Three things are missing structurally.

First, the skill has no sector-specific hooks. For a regulated market like Australian aged care, the Royal Commission, AN-ACC funding model, mandatory care minutes, and technology subsidy schemes are material demand-side factors. The skill would produce a competent estimate but miss the context that makes the number defensible to an informed Series A investor.

Second, TAM/SAM/SOM is conditional ("if the question calls for it") rather than automatically triggered by pitch context. A pitch deck always needs all three layers. The skill should either always produce TAM/SAM/SOM or detect pitch context and apply it.

Third, the skill has no concept of downstream use. It produces a number but doesn't flag whether the number is large enough for the stated purpose, or suggest scope expansion if it isn't. For pitch deck work, that omission is material.

The confidence scoring gap (single overall vs. per-variable) is a refinement issue, not a structural failure.
