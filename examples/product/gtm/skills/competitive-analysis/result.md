# Output: Competitive analysis

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16/18 criteria met (88.9%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill defines the competitive set using all 5 types — Step 1 contains an explicit five-row table defining Direct, Indirect, Substitute, Potential, and Customer inertia, each with a definition and example. The instruction "you must consider all five" is explicit. Minimum thresholds (3 direct, 2 non-obvious) are stated as requirements.
- [x] PASS: Skill requires a research step for each competitor — Step 2 mandates use of WebSearch and WebFetch per competitor. The competitor profile template is a required format, not a suggestion. The rule "If information is unavailable, state 'Unknown — could not verify' rather than guessing" prohibits writing from assumptions.
- [x] PASS: Skill produces a comparison table covering key dimensions — Step 3 "Build the comparison table" is a mandatory step with an explicit template. Rules require "specific values, not ratings" and "include dimensions where you lose." A table is required; prose substitution is not permitted.
- [x] PASS: Skill produces a differentiation analysis — Step 4 mandates a head-to-head template per competitor covering Where we win / Where we lose / Where it's a wash / Their likely counter-positioning / Best counter-argument. This structure requires qualitative differentiation reasoning, not a feature checklist.
- [x] PASS: Skill identifies strategic opportunities based on competitive gaps — Step 5 mandates four outputs: Underserved segments table, Feature gaps table, Positioning white space analysis, and Competitive threats table. Each requires identifying where competitors are weak or where the market is underserved.
- [~] PARTIAL: Skill distinguishes between parity features and differentiators — Step 4's "Where it's a wash" captures functional parity, and the comparison table rules distinguish "has feature" from "does feature well." However, the skill never explicitly frames features as table stakes (must-haves that don't win deals) vs. differentiators (reasons to choose). The distinction exists implicitly but is not enforced as a named strategic lens. Partially met.
- [x] PASS: Skill produces output that informs positioning decisions — Step 6 requires Recommended Actions with timeline and expected impact tied to specific findings. The Related Skills section explicitly states the analysis feeds into `/gtm:positioning`. The output format is structured for strategic use, not raw intelligence.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — frontmatter contains `name: competitive-analysis`, `description: Research and analyse competitors — strengths, weaknesses, positioning, and differentiation opportunities.`, and `argument-hint: "[competitor name, or 'landscape' for the full competitive set]"`. All three required fields are present.

### Output expectations

- [x] PASS: Output's competitive set covers all 5 types — the skill's Step 1 framework maps directly to the scenario. Direct (Asana, Monday.com, ClickUp), indirect (Jira, Trello), substitute (spreadsheets + email), potential (AI-native PM tools), customer inertia (status quo) would all be produced. The minimum-thresholds requirement ensures at least 1-2 examples per type.
- [~] PARTIAL: Output's research notes per competitor cite sources — Step 2 rules say "Evidence over opinion. Cite user reviews, G2/Capterra ratings, public complaints, documented limitations" and "Pricing must be current. State the date you checked." This pushes toward sourcing, but the skill does not require the named-source-per-stat format the criterion asks for (e.g., "Asana 2024 ARR ~$650M (10-K)"). Generic evidence is required; attributed citations are encouraged but not mandated.
- [x] PASS: Output's comparison table has structured dimensions — Step 3 template explicitly includes pricing (entry and at scale), integration depth, setup time, and differentiator rows. Rules require "specific values, not ratings" and one column per competitor. The template structure matches the criterion.
- [x] PASS: Output's differentiation analysis names concrete specifics — Step 4 rules state "Specific over generic. 'Better performance' is worthless. 'Dashboard loads in 200ms vs. their 3-second average (verified by independent benchmark)' is a weapon." The skill enforces specificity through rules and template examples.
- [x] PASS: Output's strategic opportunities are tied to specific competitive gaps — Step 5 tables require "why underserved" per segment and "which competitors could fill it" per gap. The Positioning white space section explicitly asks where no competitor owns a position. Outputs would be tied to specific findings, not generic market-size assertions.
- [ ] FAIL: Output distinguishes table-stakes features from differentiators with 3 of each named — the skill's Step 4 "Where it's a wash" captures parity areas, but nowhere does the skill require explicitly labelling features as table stakes (absent = lose deal) vs. differentiators (present = win deal). The criterion requires at least 3 of each named; the skill doesn't produce this framing.
- [x] PASS: Output's analysis informs the mid-market repositioning decision — Step 5 includes Underserved segments and Positioning white space; Step 6 requires Recommended Actions with specific findings. The output structure would conclude which segments are defensible, which competitors threaten, and what positioning shifts to make.
- [x] PASS: Output addresses status-quo / do-nothing as a competitor — Step 1 defines "Customer inertia" as a required type. Step 3 rules require including "manual process / spreadsheet" as a table column. The skill explicitly treats doing nothing as a competitor class.
- [~] PARTIAL: Output identifies the buying centre's likely competitive consideration — Step 2's competitor profile includes a "Buyer persona" field per competitor, but the skill does not require synthesising across competitors to identify which alternatives the buying centre (operations directors / PMOs) actually evaluates as in-house standards. The per-competitor profile captures decision-maker titles; the cross-competitor "consideration set as seen by the buyer" lens is absent.
- [~] PARTIAL: Output addresses pricing power — Step 2 and Step 3 both include detailed pricing sections (model, entry price, enterprise tiers, free tier). The comparison table has "Pricing (entry)" and "Pricing (at scale)" rows. However, the skill does not require positioning a specific add-on (e.g., analytics at $15/seat) relative to competitors' included tiers. Pricing data would be collected; the competitive pricing-power framing is not mandated.

## Notes

The skill is structurally strong. The five-type competitive framework, the "include non-obvious competitors" rule, and the "Include dimensions where you lose" table rule all show deliberate bias against self-serving analysis. The explicit DRAFT labelling requirement is appropriate for web-sourced intelligence.

The main gap across both criteria and output expectations is the table-stakes / differentiator distinction. The skill captures parity in Step 4's "Where it's a wash" but never frames features as either "table stakes (absence loses deals)" or "differentiators (presence wins deals)." A single addition to Step 4 — a two-column list of table-stakes vs. differentiators per competitor pairing — would close this without adding significant complexity.

The output-expectations sourcing criterion is ambitious. Requiring ARR figures with 10-K citations assumes the skill runs against publicly traded competitors with investor filings. The skill's "Evidence over opinion" rule is the right intent; the criterion sets a higher bar than the skill enforces.

The buying-centre consideration gap is a real one. The skill profiles each competitor independently but never asks "which of these does the buyer actually compare us against on evaluation day?" That synthesis step — distinct from individual competitor profiling — is missing and would add genuine strategic value to the output.
