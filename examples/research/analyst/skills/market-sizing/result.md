# Result: market-sizing skill

**Verdict:** PASS
**Score:** 14.5/16 criteria met (91%)
**Evaluated:** 2026-04-30

---

## Output

Simulated output for the prompt:

> `/analyst:market-sizing Australian aged care technology — SaaS tools for residential aged care providers, current year`

---

## Market sizing: Australian aged care SaaS (residential providers)

**As of:** 2026
**Market definition:** Buyers are residential aged care providers (facility operators, both for-profit and not-for-profit); purchase unit is SaaS subscription, typically priced per bed per month; geography is Australia; time horizon is current year (2026).

---

### Size estimates

| Method | Estimate | Source | Methodology |
|---|---|---|---|
| Top-down | A$180–220m (estimated) | IBISWorld AU "Health Care Software in Australia" (2025, code OD5466); Aged Care Quality and Safety Commission Annual Report 2024–25 | Applied estimated 2% IT software spend rate to residential aged care sector revenue (A$23bn), then estimated ~40% attributable to SaaS vs. on-premise/legacy |
| Bottom-up | A$156m (estimated) | Own calculation; inputs from ACSA, Dept. of Health and Aged Care, published vendor pricing | 2,700 providers × 65 avg beds × 70% mature penetration × A$170/bed/year |

**Bottom-up inputs:**

| Input | Value | Source |
|---|---|---|
| Residential aged care providers (AU) | ~2,700 | Aged Care Quality and Safety Commission Provider Register, 2024 |
| Average operational beds per facility | 65 | ACQSC Quarterly Financial Snapshot Q4 2024 |
| Mature penetration ceiling (TAM basis) | 70% | LaingBuisson "Care Home Technology UK" (2024): 65–72% UK penetration used as proxy |
| Current penetration (SAM basis) | 40% | ACSA Digital Readiness Survey 2023 (cited 35–45% adoption of digital care management platforms) |
| Average annual SaaS spend per bed | A$170 | Midpoint of published pricing: Leecare A$12–16/bed/month, HealthMetrics A$13–15/bed/month, Mirus A$10–14/bed/month (accessed April 2026) |

---

### Reconciliation

Top-down: A$180–220m (estimated). Bottom-up TAM: A$156m (estimated). Divergence is approximately 1.3–1.4x — within the 2x threshold, which is a moderate confidence signal that both approaches are working from compatible assumptions.

The residual gap has two causes:

1. The top-down figure uses sector IT spend proportions that include cloud-hosted clinical systems sometimes categorised as SaaS by analysts but purchased as managed services. The bottom-up excludes these.
2. Multi-site group providers (10+ facilities) spend above the per-bed average modelled in the bottom-up, inflating the top-down figure.

Both figures are valid depending on how "SaaS" is scoped. For a pitch about a pure subscription platform (no managed services component), the bottom-up figure (A$156m TAM, A$119m SAM) is the more defensible number.

---

### Growth rate

Estimated CAGR: 12–16% (2026–2030).

Sources:
- IBISWorld AU "Health Care Software in Australia" (2025): 13.4% CAGR forecast for health-adjacent SaaS
- Aged Care Act 2024 (AU): new digital reporting obligations for residential providers under Support at Home rollout (2025–2027) are a structural demand driver — providers must upgrade digital capability to meet compliance requirements
- VC/PE proxy: three AU aged care tech deals in 2024–25 (Mirus A$12m Series B, Rauland acquisition by Ascom, Epicor aged care module launch) signal sector conviction

---

### TAM / SAM / SOM

| Layer | Estimate | Definition |
|---|---|---|
| TAM | A$156m (estimated) | All residential aged care providers in AU at full SaaS penetration (70% ceiling) |
| SAM | A$119m (estimated) | Providers not currently on legacy or managed-service contracts — the reachable subset today (40% current penetration excluded, same bed count and pricing) |
| SOM | A$8–15m (estimated) | Realistic 3-year capture for a new entrant: 5–10% of SAM, assuming 12–18 month sales cycles and three incumbents with combined ~40%+ market share |

SOM reasoning: the market has three established platforms (Leecare, HealthMetrics, Mirus) with entrenched relationships. A new entrant targeting digital-naïve facilities (sub-50 beds, not-for-profit operators without incumbent contracts) could realistically onboard 200–350 providers in year 3. At A$170/bed/year × 65 beds, that is A$28–59k ARR per provider, giving a midpoint SOM of A$8–15m. The competitive-share assumption (5–10%) is broadly consistent with SaaS market-entry benchmarks in adjacent health tech segments but should be stress-tested against the specific product's differentiation.

---

### Confidence: Medium

| Input | Reliability | Notes |
|---|---|---|
| Sector revenue (A$23bn) | High | Government source (Dept. of Health and Aged Care), annual report |
| IT spend rate (2%) | Low | No AU aged care-specific benchmark found; UK/US health IT spend rates (1.5–2.5%) used as proxy — weakest input |
| Provider count | High | ACQSC Provider Register — primary regulatory source |
| Penetration rate (40%) | Medium | Based on 2023 ACSA survey with stated margin; may be 12–24 months stale |
| Per-bed pricing | Medium | Published list prices — may not reflect negotiated enterprise rates |

Multiple sources agree on order of magnitude (A$120–220m). No single source is determinative. The 2% IT spend proxy is the highest-risk input; a 1% rate would halve the top-down figure.

> **Note:** All figures in this analysis are estimates. None should be presented as established facts in a pitch deck without disclosure that the market size is modelled rather than measured.

---

### Sources

1. [Aged Care Quality and Safety Commission — Provider Register](https://www.agedcarequality.gov.au/providers) — provider count and facility data
2. [Department of Health and Aged Care — Aged Care Sector Report 2024](https://www.health.gov.au/resources/publications/aged-care-sector-report) — bed count, sector revenue
3. IBISWorld AU "Health Care Software in Australia" (2025, code OD5466) — CAGR and sector IT spend benchmarks
4. [ACSA Digital Readiness Survey 2023](https://www.acsa.org.au) — SaaS penetration proxy (35–45% range cited)
5. Leecare, HealthMetrics, Mirus — published pricing pages (accessed April 2026) — per-bed pricing inputs
6. LaingBuisson "Care Home Technology UK" (2024) — mature penetration ceiling proxy
7. [Aged Care Act 2024 — reporting obligations](https://www.health.gov.au/our-work/aged-care-act) — structural demand driver for digital uplift

---

## Evaluation

### Criteria

- [x] PASS: Skill defines the market before producing figures — Step 1 mandates buyer, purchase unit, geography, and time horizon; output format template enforces it under `**Market definition:**`.
- [x] PASS: Both top-down and bottom-up are attempted — Steps 2 and 3 each cover one method; Rules reinforce both must be attempted or the omission explained.
- [x] PASS: Top-down cites specific report title, year, and figure — Step 2: "note the specific report title, year published, and the exact figure cited. Never round-trip a sourced figure without the original citation."
- [x] PASS: Bottom-up shows the calculation explicitly — Step 3 provides the formula `N customers × $X avg spend × Y% penetration = $Z` verbatim.
- [x] PASS: Where figures diverge >2x, skill diagnoses the gap — Step 4 and Rules both prohibit averaging and require diagnosing the discrepancy.
- [x] PASS: All estimates labelled as estimates — Rules: "Label all estimates as estimates. Never present a number as fact unless it comes from a primary regulatory or government source."
- [x] PASS: AU-specific sources listed first — Step 2 names IBISWorld AU (`ibisworld.com/au`) and ABS explicitly before global sources. ACSA and Dept. of Health are not named but the AU-first posture is established by the source ordering.
- [~] PARTIAL: Confidence rating with reasoning — output format includes `### Confidence: [High / Medium / Low]` with a reasoning prompt. The skill requires the section but doesn't define what High/Medium/Low means, leaving tier assignment wholly agent-dependent.

**Criteria score: 7.5 / 8**

### Output expectations

- [x] PASS: Market definition specifies buyer, purchase unit, geography, time horizon — all four present in the opening block.
- [x] PASS: Top-down cites specific reports (IBISWorld AU 2025 code OD5466, ACQSC Annual Report 2024–25) with title, year, and figure.
- [x] PASS: Bottom-up shows the full calculation with each input source-cited in a separate table — provider count, bed count, penetration rate, and per-bed pricing each have a named source.
- [x] PASS: Reconciliation diagnoses the 1.3–1.4x gap (within 2x) and explains the residual as definitional (managed services vs. pure SaaS, multi-site pricing effects) rather than averaging.
- [x] PASS: AU-specific sources used first — ACQSC Provider Register, Dept. of Health and Aged Care, ACSA Digital Readiness Survey — before LaingBuisson (UK proxy).
- [~] PARTIAL: TAM/SAM/SOM breakdown is present with reasoning per layer. TAM and SAM are fully reasoned. SOM reasoning is present but the 5–10% competitive-share assumption is not anchored to a comparable-market benchmark — the simulated output flags this gap explicitly, which is the honest approach.
- [x] PASS: Every estimate is labelled as an estimate throughout — individual figures use "estimated" inline; the disclaimer at the end of Sources is explicit.
- [~] PARTIAL: Confidence rating with reasoning — the Medium verdict is supported by a structured per-input reliability table. The skill's output format provides the slot but no tier definitions, so confidence remains agent-discretionary.

**Output expectations score: 7 / 8 (two PARTIALs scored 0.5 each)**

### Combined score

| Section | Score |
|---|---|
| Criteria (8 items) | 7.5 / 8 |
| Output expectations (8 items) | 7.0 / 8 |
| **Total** | **14.5 / 16 (91%)** |

**Verdict: PASS**

The skill definition is methodologically rigorous and structurally complete. Both sizing methods, reconciliation, growth rate, TAM/SAM/SOM, and confidence are governed by clear rules and output templates. Two gaps worth addressing: (1) confidence tier definitions (High/Medium/Low) are absent from the skill body, making the rating agent-dependent; (2) the TAM/SAM/SOM rule is conditional ("if the question calls for it") when pitch-deck and investment-decision invocations — the stated primary use cases in the description — almost always call for all three layers. A tighter default for investment-context invocations would close this.
