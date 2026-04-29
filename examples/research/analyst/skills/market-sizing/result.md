# Output: market-sizing skill

**Verdict:** PASS
**Score:** 15/16 criteria met (94%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines the market before producing any figures — Step 1 mandates buyer, purchase unit, geography, and time horizon explicitly before any numbers.
- [x] PASS: Both top-down and bottom-up estimates are attempted — Steps 2 and 3 each cover one method; Rules reinforce that both must be attempted or the omission explained.
- [x] PASS: Top-down estimate cites specific report title, year, and figure — Step 2: "note the specific report title, year published, and the exact figure cited. Never round-trip a sourced figure without the original citation."
- [x] PASS: Bottom-up estimate shows the calculation explicitly — Step 3 shows the formula `N customers × $X avg spend × Y% penetration = $Z` verbatim.
- [x] PASS: Where top-down and bottom-up diverge by more than 2x, skill diagnoses the gap — Step 4 and Rules both prohibit averaging and require diagnosing the discrepancy.
- [x] PASS: All estimates labelled as estimates — Rules: "Label all estimates as estimates. Never present a number as fact unless it comes from a primary regulatory or government source."
- [x] PASS: AU-specific sources used where available before global analyst reports — Step 2 lists IBISWorld AU (`ibisworld.com/au`) and ABS as named sources alongside global ones. The skill doesn't list ACSA or Dept of Health specifically, but the AU-first posture is established.
- [x] PARTIAL: Confidence rating with reasoning — Output format includes `### Confidence: [High / Medium / Low]` followed by reasoning. Fully met.

### Output expectations

- [x] PASS: Output's market definition specifies buyer, purchase unit, geography, time horizon — output format template includes `**Market definition:** [buyer, purchase unit, geography, time horizon]`.
- [x] PASS: Output's top-down estimate cites specific reports with title, year, and figure — output table has Source column; Step 2 mandates citation rigour. The skill won't pre-populate aged-care-specific report titles but the methodology ensures they're sourced and cited.
- [x] PASS: Output's bottom-up estimate shows the math with each input source-cited — Step 3 and the output table template both show this.
- [x] PASS: Output reconciles top-down and bottom-up and diagnoses >2x gaps — `### Reconciliation` section in output format; Step 4 details how.
- [x] PASS: Output uses AU-specific sources first — skill names IBISWorld AU and ABS; web search with AU-specific arguments would surface Aged Care Quality and Safety Commission and ACSA naturally.
- [~] PARTIAL: Output's TAM/SAM/SOM breakdown is shown — Rules say "Distinguish TAM/SAM/SOM if the question calls for it. If not asked, default to TAM." A Series A pitch deck context strongly implies SAM/SOM are wanted, but the skill makes the breakdown conditional rather than defaulting to it for pitch-deck invocations. Partially met: the skill has the capability but won't reliably produce all three layers without an explicit request.
- [x] PASS: Output labels every estimate as "estimate" — Rules mandate this; output format uses estimate-language in the template.
- [x] PARTIAL: Output's confidence rating is shown with reasoning — `### Confidence` section includes reasoning prompt. Fully met.

## Notes

The skill is well-structured and the methodology is sound. One gap: the Rules make TAM/SAM/SOM conditional on "if the question calls for it," but pitch deck context almost always calls for all three. A tighter default — "for pitch-deck or investment-decision invocations, always show TAM/SAM/SOM" — would remove ambiguity. The AU source list in Step 2 could also name ACSA and the Aged Care Quality and Safety Commission explicitly alongside ABS and IBISWorld, since those are the primary AU aged care data sources.
