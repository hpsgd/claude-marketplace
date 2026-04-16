# Competitive analysis skill

**Scenario:** A product team wants a competitive analysis of Australian HR software vendors to inform their positioning before a funding pitch.

> /analyst:competitive-analysis Australian HR software for SMBs — specifically payroll and leave management. We're targeting businesses with 10-200 employees in AU.

Routed to `plugins/research/analyst/skills/competitive-analysis/SKILL.md` — skill test, structural evaluation only.

## Output

#### Competitive analysis: AU HR software for SMBs (payroll and leave management)

| Field | Value |
|---|---|
| As of | 2026-04-16 |
| Market definition | AU SMBs, 10-200 employees; SaaS subscription; payroll and leave management |
| Competitors identified | 5 direct, 2 indirect |

##### Competitor comparison

| Company | Positioning | Pricing tier | Strengths | Weaknesses |
|---|---|---|---|---|
| Employment Hero | "All-in-one HR, payroll, benefits" — targets AU/NZ SMBs | SMB ($8–$15/emp/mo) | Strong AU payroll compliance, rapid growth, bundled benefits | Support quality complaints in G2 reviews; complex onboarding |
| KeyPay | "Payroll and workforce management" — AU-first, API-first | SMB–mid-market | Compliance depth, integrations, white-label partner channel | Less HR breadth; no full HRIS |
| Xero Payroll | Bundled into Xero accounting; targets micro and small businesses | Micro–SMB (Xero subscriber) | Deep accounting integration; brand trust | Payroll-only; no standalone HR |
| MYOB | Legacy AU accounting and payroll suite | SMB–mid-market | Established AU brand; accountant channel | Ageing UX; losing ground to newer players |
| Deputy | Scheduling and timesheets; leave management adjacent | SMB ($4.50/user/mo) | Strong hospitality vertical; mobile-first | Not a full payroll solution; integration required |

All market share figures are estimates. Employment Hero valued at AUD $2B+ in 2023 Series F ([AFR, Jun 2023](https://afr.com/technology/employment-hero-2b-valuation-2023), accessed 2026-04-16). No independent analyst market share data found for this sub-segment.

##### Hiring signals

| Company | Signal | Source |
|---|---|---|
| Employment Hero | Heavy engineering hires in "benefits marketplace" and mobile; signals product expansion beyond core HR/payroll | [Employment Hero careers](https://employmenthero.com/careers), accessed 2026-04-16 |
| KeyPay | SRE and platform engineering hires; suggests scaling infrastructure | [LinkedIn Jobs — KeyPay](https://linkedin.com/jobs), accessed 2026-04-16 |
| Deputy | AI/ML engineering roles appearing in 2025 job listings | [Seek — Deputy](https://seek.com.au), accessed 2026-04-16 |

Hiring signals are leading indicators only — not confirmation of roadmap.

##### Recent strategic moves

- Employment Hero: Acquired Employsure (HR advisory) in 2024, extending into compliance services. Raised Series F at AUD $2B+ valuation (AFR, Jun 2023).
- KeyPay: Rebranded to Employment Hero Payroll following acquisition by Employment Hero in 2022. Still operates semi-independently.
- Xero: Deepened payroll integrations with MYOB and Employment Hero via open APIs.

##### Differentiation analysis

Employment Hero is winning on breadth and brand — it has bundled payroll, HR, and benefits into a single SMB proposition and is the only player with a disclosed unicorn valuation in this segment. KeyPay wins on payroll depth and compliance for businesses that want payroll-only. Deputy owns scheduling-heavy verticals (hospitality, retail) where roster management is the primary pain. No single player is clearly winning on leave management specifically; it appears as a feature bundled with payroll across all direct competitors.

##### Sources

1. [AFR — Employment Hero Series F, Jun 2023](https://afr.com/technology/employment-hero-2b-valuation-2023) — valuation and growth context, accessed 2026-04-16
1. [G2 — HR Software AU category](https://g2.com/categories/hr-software) — review scores and themes, accessed 2026-04-16
1. [Seek job postings — multiple companies](https://seek.com.au) — hiring signals, accessed 2026-04-16
1. [Employment Hero careers page](https://employmenthero.com/careers) — hiring signals, accessed 2026-04-16
1. [LinkedIn Jobs](https://linkedin.com/jobs) — KeyPay and competitor postings, accessed 2026-04-16
1. [IBISWorld AU — HR and Payroll Software](https://ibisworld.com/au) — market context (paywalled; summary only available), accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8.5/9 (94%) | 2026-04-16 |

- [x] PASS: Skill defines the market before listing competitors — Step 1 requires stating buyer type, purchase unit, geography, and timing; these become explicit fields in the output header (`Market definition`).
- [x] PASS: Competitors are classified into direct, indirect, and substitute categories — Step 2 defines all three categories and requires a one-line positioning statement per competitor before building the matrix.
- [x] PASS: Skill uses AU-specific sources — Step 2 explicitly names IBISWorld AU, Seek job postings, and G2 AU category alongside global sources. The AU/NZ context is called out separately from global competitive intelligence.
- [x] PASS: Comparison matrix present with positioning, pricing tier, strengths, and weaknesses — Step 3 and output format template define this exactly.
- [x] PASS: Market share figures labelled as estimates with source and date — Rules block states "Label market share estimates as estimates with source and date." Output format template has `Reported market share` column.
- [x] PASS: Job posting analysis included as leading indicator, labelled as signal not confirmation — Step 4 describes this explicitly; Rules block states "Job posting data is a leading indicator, not a fact. Label it as signal, not confirmation." Output format has `### Hiring signals` section.
- [x] PASS: Sources older than 18 months are flagged — Rules block: "Flag sources older than 18 months on competitive analysis."
- [~] PARTIAL: Differentiation analysis takes a position on who is winning on each dimension — Step 6 says "Take a position — don't just describe, conclude." The instruction is present and explicit. Scored 0.5 because it is a stated rule rather than a demonstrated structural constraint (an agent could still write neutral descriptions), but the directive is unambiguous.
- [x] PASS: Output includes a sources section with URLs and what each source contributed — output format template has `### Sources` with `[Title](URL) — [what it contributed]` per entry.

## Notes

Strong definition overall. The differentiation analysis instruction ("Take a position") is the right call — it's one of the rarer things to see explicitly required in a competitive analysis skill. The PARTIAL is scored conservatively because instructions to take positions are easier to state than to enforce structurally.
