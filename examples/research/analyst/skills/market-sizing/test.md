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
