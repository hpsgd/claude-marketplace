# Test: market-sizing skill

Scenario: A startup founder needs a defensible TAM estimate for the Australian aged care technology market to include in a Series A pitch deck.

## Prompt

/analyst:market-sizing Australian aged care technology — SaaS tools for residential aged care providers, current year

## Criteria

- [ ] PASS: Skill defines the market before producing any figures — buyer type, purchase unit, geography (AU), and time horizon are all stated
- [ ] PASS: Both top-down and bottom-up estimates are attempted — if one genuinely can't be done, the reason is explained
- [ ] PASS: Top-down estimate cites a specific report title, year, and figure — not a generic reference to "analysts"
- [ ] PASS: Bottom-up estimate shows the calculation explicitly (N customers × $X avg spend × Y% penetration = $Z)
- [ ] PASS: Where top-down and bottom-up figures diverge by more than 2x, skill diagnoses the gap rather than averaging them
- [ ] PASS: All estimates are labelled as estimates — none presented as established facts
- [ ] PASS: AU-specific sources are used where available (ABS, IBISWorld AU, ACSA) before defaulting to global analyst reports
- [ ] PARTIAL: Confidence rating is provided with reasoning — not just asserted without evidence

## Output expectations

- [ ] PASS: Output's market definition specifies — buyer (residential aged care provider with X+ beds), purchase unit (per-bed per-month subscription typical), geography (Australia), time horizon (current year), and segment scope (excludes home care, retirement living)
- [ ] PASS: Output's top-down estimate cites specific reports — IBISWorld Australia "Aged Care SaaS" or sector adjacent, government data (Department of Health and Aged Care), Aged Care Industry Association reports — with title, year, and figure
- [ ] PASS: Output's bottom-up estimate shows the math — N residential aged care providers in AU (~700-900 per Royal Commission data) × average-bed count × % currently using SaaS × $X per-bed-per-month × 12 — with each input source-cited
- [ ] PASS: Output reconciles top-down and bottom-up — if they differ by >2x, the gap is diagnosed (different segment definitions, different penetration assumptions, one excludes hardware) rather than averaged
- [ ] PASS: Output uses AU-specific sources first — Aged Care Quality and Safety Commission, ABS Health Services data, ACSA (Aged & Community Services Australia), AFR / Australian sector press — before defaulting to global analyst reports
- [ ] PASS: Output addresses the post-Royal-Commission context — AN-ACC funding model, mandatory care minutes, technology subsidies — these directly affect aged care providers' SaaS purchasing capacity and behaviour
- [ ] PASS: Output's TAM / SAM / SOM breakdown is shown — TAM (all residential aged care SaaS), SAM (the addressable subset given product fit), SOM (realistic capture given competitive set and team) — with reasoning per layer
- [ ] PASS: Output labels EVERY estimate as "estimate" — not "the market is $X" but "estimated at $X based on Y inputs from Z sources"
- [ ] PASS: Output's confidence rating per estimate is shown with reasoning — "TAM HIGH confidence (regulatory data robust), penetration MEDIUM (industry estimates only), spend per bed LOW (vendor-claimed)"
- [ ] PARTIAL: Output addresses the pitch context — Series A investors expect a defensible TAM in the low-billions or compelling growth trajectory; if the AU market is too small to justify Series A alone, output flags whether expansion to NZ / international should be in the deck
