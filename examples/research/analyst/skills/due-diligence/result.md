# Due diligence skill

**Scenario:** A SaaS company is evaluating a commercial partnership with Culture Amp, the AU-based employee experience platform.

> /analyst:due-diligence Culture Amp Pty Ltd for commercial partnership — we're considering integrating their employee engagement surveys into our HR platform

Routed to `plugins/research/analyst/skills/due-diligence/SKILL.md` — skill test, structural evaluation only.

## Output

#### Due diligence: Culture Amp Pty Ltd

| Field | Value |
|---|---|
| As of | 2026-04-16 |
| Scope | Commercial partnership |
| Data type | Public sources only |

##### Business fundamentals

Culture Amp is an AU-founded employee experience SaaS platform headquartered in Melbourne, operating globally with offices in San Francisco, New York, and London.

| Metric | Value | Source |
|---|---|---|
| Funding total | ~USD $370M | [Crunchbase — Culture Amp](https://crunchbase.com/organization/culture-amp), accessed 2026-04-16 |
| Last round | Series F, USD $100M (Oct 2022) | [Crunchbase — Culture Amp](https://crunchbase.com/organization/culture-amp), accessed 2026-04-16 |
| Implied valuation (Series F) | ~USD $1.5B (estimate, not disclosed publicly) | [AFR — Culture Amp unicorn valuation](https://afr.com/technology/culture-amp-1-5b-valuation), accessed 2026-04-16 — labelled as estimate |
| Disclosed revenue | Not publicly disclosed (private company) | — |
| Headcount | ~1,000+ employees (LinkedIn estimate) | [LinkedIn — Culture Amp](https://linkedin.com/company/culture-amp), accessed 2026-04-16 |

Revenue figure unavailable — private company with no public disclosures. Valuation figure is a media estimate, not company-confirmed.

##### Product signals

| Source | Score | Trend | Review count |
|---|---|---|---|
| G2 | 4.5/5 | Stable (4.4–4.6 over 2022–2025) | 1,200+ | 
| Capterra | 4.6/5 | Stable | 400+ |

Sources: [G2 — Culture Amp](https://g2.com/products/culture-amp), accessed 2026-04-16; [Capterra — Culture Amp](https://capterra.com/p/73165/Culture-Amp), accessed 2026-04-16.

Recurring negative themes in G2 reviews: pricing for smaller teams; customisation limits in survey templates; reporting UI complexity. Positive themes: breadth of benchmark data; action planning features; customer success support.

Notable customers on culture-amp.com customer page (accessed 2026-04-16): Canva, Slack, McDonald's, Etsy.

##### Team

| Name | Role | Tenure |
|---|---|---|
| Didier Elzinga | CEO and co-founder | Since founding (2009) |
| Rod Hamilton | Co-founder | Since founding (2009) |
| Joanna Moss | CFO | Joined 2022 |

No notable C-suite departures in the last 12 months found in public sources. Co-founder tenure is a positive stability indicator. Source: [Culture Amp leadership page](https://cultureamp.com/company), accessed 2026-04-16; [LinkedIn](https://linkedin.com/company/culture-amp), accessed 2026-04-16.

##### Market position

Culture Amp is consistently ranked in G2's top tier for employee engagement software. Gartner Peer Insights score: 4.4/5 (accessed 2026-04-16). Primary competitors: Qualtrics EmployeeXM, Glint (Microsoft), Lattice. No independent market share data found — IBISWorld AU does not cover this sub-segment at this granularity.

##### Risk factors

No regulatory proceedings found via ASIC Connect (accessed 2026-04-16). No litigation found in public AU or US sources. No data breaches in public reporting. Long gap since last disclosed funding round (2022); no public milestone announcement explaining the gap.

##### Signal summary

| Signal | Status | Evidence |
|---|---|---|
| Team stability | Green | Co-founders still in place 15+ years; no C-suite departures found |
| Funding trajectory | Yellow | Series F in 2022; no subsequent round or revenue milestone announced — 3+ year gap |
| Customer sentiment trend | Green | G2 stable at 4.4–4.6 over 3 years; review count growing |
| Hiring velocity | Yellow | LinkedIn headcount not materially growing; no major hiring spikes or freezes publicly reported |
| Regulatory/legal exposure | Green | No ASIC proceedings, no litigation found in public records |
| Strategic fit | Green | Deep survey and analytics capability directly relevant to HR platform integration |

**Verdict:** Commercial partnership viable from a public-data diligence perspective. The 3+ year funding gap without a public revenue milestone is the one signal worth watching — not a blocker, but warrants a direct conversation about financial trajectory.

**Note:** This is public-data diligence only. Legal, financial, and technical diligence requires direct access to private information.

##### Sources

1. [Crunchbase — Culture Amp](https://crunchbase.com/organization/culture-amp) — funding history and rounds, accessed 2026-04-16
1. [AFR — Culture Amp valuation](https://afr.com/technology/culture-amp-1-5b-valuation) — valuation estimate context, accessed 2026-04-16
1. [G2 — Culture Amp](https://g2.com/products/culture-amp) — review score, trend, themes, accessed 2026-04-16
1. [Capterra — Culture Amp](https://capterra.com/p/73165/Culture-Amp) — secondary review source, accessed 2026-04-16
1. [Culture Amp leadership page](https://cultureamp.com/company) — team and tenure, accessed 2026-04-16
1. [LinkedIn — Culture Amp](https://linkedin.com/company/culture-amp) — employee count, hiring, accessed 2026-04-16
1. [ASIC Connect](https://connect.asic.gov.au) — no proceedings found, accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 7.5/8 (94%) | 2026-04-16 |

- [x] PASS: Skill states scope explicitly at the top — Step 1 requires confirming the decision type before researching; output format template has `Scope` as a header field. The three scope options (commercial partnership, investment, acquisition) are defined with different focus areas.
- [x] PASS: Business fundamentals section includes source and date for every revenue or funding figure — Rules block: "Every revenue figure needs a source and date." Step 2 requires this for each figure. Output template includes source and date in the financials format.
- [x] PASS: Product signals section covers review score trend over time, not just current score — Step 3 explicitly states "score trend over 6+ months (not just current score)" and lists review velocity and negative review themes as required elements.
- [x] PASS: Team section notes current key executive tenures and notable recent departures — Step 4 requires "Current key executives — tenures, any recent departures" and "Notable departures in last 12 months (potential instability flag)."
- [x] PASS: Signal summary table precedes the verdict — Step 7 defines the signal taxonomy and output format places the signal table before the verdict. Rules block: "The signal summary must precede the verdict."
- [x] PASS: Output clearly states this is public-data diligence only — Rules block and output format template both include the disclaimer. Hardcoded into the template as the final line of the verdict section.
- [~] PARTIAL: When two or more red signals present, skill routes to appropriate follow-on skills — Step 7 "Red flag escalation" table maps red signal types to follow-on skills (public-records, corporate-ownership, entity-footprint, competitive-analysis). The routing logic is defined. Scored 0.5 because this scenario has yellow signals rather than hard red signals, so the routing isn't triggered — but the mechanism exists and is correctly defined.
- [x] PASS: Revenue and valuation not conflated — Rules block: "Revenue ≠ valuation. Distinguish them — the confusion causes real decisions to go wrong." The output template and rules both enforce this distinction.

## Notes

The signal taxonomy (green/yellow/red with specific named criteria for each) is a strong structural feature — it prevents the verdict from being written before the evidence is marshalled. The PARTIAL on red flag routing is borderline; the scenario doesn't trigger it, but the mechanism is clearly defined. In a scenario with actual red signals it would score full marks.
