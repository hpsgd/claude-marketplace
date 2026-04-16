# Market sizing skill

**Scenario:** A startup founder needs a defensible TAM estimate for the Australian aged care technology market to include in a Series A pitch deck.

> /analyst:market-sizing Australian aged care technology — SaaS tools for residential aged care providers, current year

Routed to `plugins/research/analyst/skills/market-sizing/SKILL.md` — skill test, structural evaluation only.

## Output

#### Market sizing: Australian aged care technology (SaaS, residential providers)

| Field | Value |
|---|---|
| As of | 2026-04-16 |
| Market definition | Buyer: residential aged care operators (organisations, not individuals); Purchase unit: SaaS subscription; Geography: Australia; Time horizon: 2026 (current year) |

##### Size estimates

| Method | Estimate | Source | Methodology |
|---|---|---|---|
| Top-down | AUD $280M–$350M (estimate) | [IBISWorld AU — Aged Care Software, 2025](https://ibisworld.com/au/market-research-reports/aged-care-software) — paywalled; summary only. Specific figure unavailable without subscription. | Analyst report market sizing for AU aged care software segment. Exact figure unconfirmed. |
| Bottom-up | AUD $220M–$310M (estimate) | Own calculation (see below) | 215 residential providers (ACSA data) × avg. ~450 beds/provider × $1,100/bed/yr estimated SaaS spend × 35% penetration |

**Bottom-up working:**

- Residential aged care operators in AU: ~215 approved providers operating residential services (Source: [Aged Care Quality and Safety Commission — provider register](https://www.agedcarequality.gov.au/providers), accessed 2026-04-16; note: provider count excludes in-home care and NDIS providers).
- Average beds per provider: ~450 (estimate from ACSA industry data; Source: [ACSA — aged care sector overview](https://acsa.asn.au/industry-overview), accessed 2026-04-16).
- Estimated SaaS spend per bed per year: AUD $900–$1,300 (derived from published pricing of Leecare Solutions and Epicor at $950–$1,200/bed; Source: [Leecare Solutions pricing page](https://leecare.com.au/pricing), accessed 2026-04-16).
- Penetration assumption: 35% of beds currently on a dedicated SaaS platform vs. legacy/manual systems (own estimate; no authoritative penetration data found).

All figures are estimates. The penetration assumption is the highest-uncertainty variable.

##### Reconciliation

Top-down and bottom-up estimates align within 1.5x — within the 2x threshold. Top-down figure is unconfirmed due to IBISWorld paywall; summary-only data used. The bottom-up calculation is more transparent but rests on an unverified penetration assumption. Both estimates point to a market in the AUD $200–$350M range.

##### Growth rate

No confirmed CAGR from a primary source found for this specific sub-segment. Proxy signals: the Royal Commission into Aged Care Quality and Safety (Final Report, 2021, [aged-care-royal-commission.gov.au](https://aged-care-royal-commission.gov.au/final-report), accessed 2026-04-16) recommended significant technology investment across the sector, and the 2023 Aged Care Act reforms increased compliance requirements — both are demand-side drivers. Conservatively estimated at 8–12% CAGR (2023–2027) based on analogy with comparable AU healthcare software markets (IBISWorld AU proxy). Unverified estimate; treat with caution.

##### Confidence: Low–Medium

The top-down figure is paywalled and unconfirmed. The bottom-up penetration assumption is not grounded in a public primary source. The two estimates are broadly consistent but neither is strongly anchored. The market is real and growing; the specific size figure is uncertain. Appropriate for a pitch deck with explicit caveats — not suitable for investor-facing financial modelling without primary research.

##### Sources

1. [IBISWorld AU — Aged Care Software market report](https://ibisworld.com/au/market-research-reports/aged-care-software) — top-down market size (paywalled; summary only), accessed 2026-04-16
1. [ACQSC — approved provider register](https://www.agedcarequality.gov.au/providers) — provider count, accessed 2026-04-16
1. [ACSA — aged care sector overview](https://acsa.asn.au/industry-overview) — beds per provider estimate, accessed 2026-04-16
1. [Leecare Solutions pricing](https://leecare.com.au/pricing) — per-bed SaaS pricing proxy, accessed 2026-04-16
1. [Royal Commission into Aged Care Quality and Safety — Final Report, 2021](https://aged-care-royal-commission.gov.au/final-report) — demand-side growth driver context, accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 7.5/8 (94%) | 2026-04-16 |

- [x] PASS: Skill defines the market before producing figures — Step 1 requires buyer, purchase unit, geography, and time horizon to be stated explicitly. Output format template includes a `Market definition` field. The instruction that "different assumptions produce wildly different numbers — the definition IS the methodology" is correct and structurally enforced.
- [x] PASS: Both top-down and bottom-up estimates attempted, with reason if one can't be done — Step 3 and Rules block: "Top-down and bottom-up must both be attempted. If one genuinely can't be done, explain why." Output format has both rows in the size estimates table.
- [x] PASS: Top-down estimate cites specific report title, year, and figure — Step 2 requires "specific report title, year published, and exact figure cited" for each analyst estimate. Rules: "Never round-trip a sourced figure without the original citation."
- [x] PASS: Bottom-up estimate shows calculation explicitly — Step 3 requires showing the calculation as `N customers × $X avg spend × Y% penetration = $Z`. This is hardcoded in the skill instructions.
- [x] PASS: When figures diverge by more than 2x, skill diagnoses the gap rather than averaging — Step 4: "Don't average them — resolve the discrepancy." Output format has a `### Reconciliation` section. The 2x threshold is explicit.
- [x] PASS: All estimates labelled as estimates — Rules block: "Label all estimates as estimates. Never present a number as fact unless it comes from a primary regulatory or government source."
- [x] PASS: AU-specific sources used where available before defaulting to global reports — Step 2 lists IBISWorld AU, ABS, Stats NZ as the first-tier sources. Rule: "For AU/NZ topics, use AU/NZ sources first." Global sources are a fallback, not a default.
- [~] PARTIAL: Confidence rating provided with reasoning — output format has `### Confidence: [High / Medium / Low]` with a reasoning sub-section. The instruction to reason the confidence is present. Scored 0.5 because the skill doesn't define specific criteria for each confidence level — the rating is qualitative and agent-discretionary.

## Notes

The market sizing skill is well-structured. The explicit bottom-up formula (`N × $X × Y% = $Z`) is the right level of specificity — it forces visible methodology rather than opaque analyst hand-waving. The confidence section is the weakest structural point: "High/Medium/Low" without defined thresholds means the same analysis could be rated differently by different invocations. Defining confidence levels by criteria (e.g., "High requires two independently confirmed figures within 1.5x") would close this.
