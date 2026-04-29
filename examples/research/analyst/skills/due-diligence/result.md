# Result: due-diligence skill

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16/18 criteria met (88.9%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill states the scope explicitly at the top — Step 1 requires confirming the decision type (commercial partnership / investment / acquisition) before researching; scope is the first field in the output template.
- [x] PASS: Business fundamentals section includes a source and date for every revenue or funding figure — Step 2: "Each figure needs a source and date." Rules block repeats: "Every revenue figure needs a source and date."
- [x] PASS: Product signals section covers review score trend over time — Step 3 explicitly requires "score trend over 6+ months (not just current score)."
- [x] PASS: Team section notes current key executive tenures and notable recent departures — Step 4 requires both "Current key executives — tenures, any recent departures" and "Notable departures in last 12 months."
- [x] PASS: Signal summary table is present and precedes the verdict — Step 7 defines the signal taxonomy; Rules block states "The signal summary must precede the verdict." Output template enforces ordering.
- [x] PASS: Output clearly states this is public-data diligence only and routes legal/financial/technical diligence elsewhere — intro paragraph, Rules block, and output template footer all require the disclaimer explicitly.
- [~] PARTIAL: When two or more red signals are present, skill routes to appropriate follow-on skills — Step 7 "Red flag escalation" table maps red signal types to `/investigator:public-records`, `/investigator:corporate-ownership`, `/investigator:entity-footprint`, and `/analyst:competitive-analysis`. Mechanism is defined. Scored 0.5 because the test scenario (Culture Amp, stable company) doesn't trigger it, so routing can't be observed in practice.
- [x] PASS: Revenue and valuation are not conflated — Rules block: "Revenue ≠ valuation. Distinguish them — the confusion causes real decisions to go wrong." Enforced in both rules and Step 2 guidance for private companies.

**Criteria subtotal: 7.5/8**

### Output expectations

- [ ] FAIL: Output addresses Culture Amp specifically with entity confirmation (ABN, registered office) at the top — the skill's output format template starts with company name, date, scope, and data type. No ABN or registered office field is defined anywhere in the skill. Step 1 ("Establish scope") doesn't include entity verification. A well-formed output from this definition would not include ABN or registered office confirmation.
- [x] PASS: Scope statement explicitly limits to commercial-partnership diligence and names what's NOT covered — the output template footer states "Legal, financial, and technical diligence requires direct access to private information." The intro paragraph says the same. The three non-covered areas (legal, financial, technical) are named.
- [x] PASS: Every revenue/funding figure sourced with URL and date — Step 2 requires source and date for each figure; private-company label requirement is explicit.
- [x] PASS: Product signals trace review-score trend over time — Step 3 explicitly requires trend over 6+ months; review velocity and negative theme tracking are required elements.
- [x] PASS: Team section names current executives with tenure and notable departures in last 12 months — Step 4 structure and the output template's Team section both require this.
- [x] PASS: Signal summary table precedes the verdict with named signals — Step 7 defines the six-signal taxonomy; output template shows the table before the verdict section. Verdict is one sentence following the table.
- [x] PASS: Verdict follows from the signal table — Rules block and Step 7 structure enforce this; the verdict is a single sentence summarising the 1-2 factors from the signal table.
- [x] PASS: Output explicitly states public-data-only diligence and that partnership decision requires legal, financial, and technical diligence — hardcoded into output template as the final line of the verdict section.
- [x] PASS: Output distinguishes revenue from valuation — Rules block enforces this; Step 2 explicitly labels private-company revenue estimates separately from funding/valuation.
- [~] PARTIAL: Output addresses AU SaaS partnership specifics (SOCI Act, Privacy Act 1988 data-sharing) — SKILL.md includes ASIC Connect as an AU-specific regulatory search source in Step 6, and the scope definition for commercial partnership covers reputational risk. However, the skill contains no instruction to address SOCI Act applicability, Privacy Act 1988 customer-data-sharing obligations, or data-residency considerations for AU-AU partnerships. The AU context is partially acknowledged through ASIC sourcing, but the specific AU data-law obligations for customer-data sharing are not in scope.

**Output expectations subtotal: 8.5/10**

## Notes

The top gap is entity verification: the skill has no step for confirming ABN, ASIC registration, or registered office. For AU commercial partnerships this is a meaningful omission — the wrong entity could be the counterparty. A preflight entity confirmation step (ASIC Connect lookup to confirm legal name, ABN, and current registration status) would be a natural addition to Step 1.

The AU data-law gap is real but narrower: the skill correctly routes to ASIC Connect for regulatory findings, but doesn't prompt the analyst to check whether customer-data sharing under the Privacy Act 1988 requires a Data Processing Agreement or whether SOCI Act applies to the partner's sector. For an AU-AU SaaS integration this is a relevant risk that the skill currently leaves to the analyst's judgment rather than surfacing as a required check.

The red-flag routing mechanism (Step 7 escalation table) is the strongest structural feature of the skill — it prevents the analyst from stopping at a surface verdict when compounding signals are present.
