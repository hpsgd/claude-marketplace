# Company lookup skill

**Scenario:** A business analyst needs to research an unfamiliar company before a client meeting.

> Can you look up Palantir Technologies for me? I need to understand what they do, their business model, and any recent developments before a meeting tomorrow.

Routed to `plugins/research/analyst/skills/company-lookup/SKILL.md` — skill test, structural evaluation only.

## Output

#### Company: Palantir Technologies

| Field | Value |
|---|---|
| As of | 2026-04-16 |
| Sources | 8 public sources |

##### Overview

Palantir builds software platforms for large-scale data integration and analysis, serving government defence/intelligence agencies and large commercial enterprises. Founded in 2003 by Peter Thiel, Alex Karp, and others, the company went public via direct listing on NYSE in September 2020 and joined the S&P 500 in September 2024.

| Attribute | Detail |
|---|---|
| Founded | 2003 |
| HQ | Denver, Colorado (relocated from Palo Alto in 2020) |
| Size | ~3,800 employees (2024 10-K) |
| Business model | Enterprise software platform (SaaS + on-prem deployment) |
| Revenue model | Subscription licences + professional services; multi-year government contracts |

##### Products/services

Gotham — data integration and analysis platform for government and defence. Foundry — commercial equivalent for enterprises (supply chain, manufacturing, financial services). AIP (AI Platform, launched 2023) — layers LLM capabilities over Gotham and Foundry. No public pricing; commercial contracts typically start at $1M+ ARR.

##### Team

| Name | Role | Notes |
|---|---|---|
| Alex Karp | CEO and co-founder | Has led the company since founding |
| Shyam Sankar | CTO | Promoted from COO in 2023 |
| David Glazer | CFO | Joined 2012 |

Sources: [Palantir investor relations](https://investors.palantir.com), accessed 2026-04-16; [LinkedIn — Palantir Technologies](https://linkedin.com/company/palantir-technologies), accessed 2026-04-16.

##### Financials

| Metric | Value | Source |
|---|---|---|
| Revenue (FY2024) | $2.87B | [Palantir 10-K FY2024](https://sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1321655&type=10-K), filed Feb 2025 |
| Revenue growth (YoY) | 29% | Palantir 10-K FY2024 |
| US commercial revenue growth | 54% YoY | [Palantir Q4 2024 earnings release](https://investors.palantir.com/news-releases/news-release-details/palantir-technologies-reports-fourth-quarter-2024-results), accessed 2026-04-16 |
| Adjusted operating margin | 37% | Palantir 10-K FY2024 |

GAAP profitable since 2023.

##### Recent news

- **Feb 2025:** Q4 2024 earnings beat. Revenue $828M, up 36% YoY. Source: [Palantir Q4 2024 earnings release](https://investors.palantir.com/news-releases/news-release-details/palantir-technologies-reports-fourth-quarter-2024-results), accessed 2026-04-16.
- **Jan 2025:** Extended US Army Vantage contract worth $400M+ over 4 years. Source: [Reuters](https://reuters.com/technology/palantir-wins-army-contract-2025-01), accessed 2026-04-16.
- **Sep 2024:** Added to S&P 500 index. Source: [S&P Dow Jones Indices press release](https://spglobal.com/spdji/en/indices/equity/sp-500), accessed 2026-04-16.

##### Strategic direction

Job postings weight heavily toward AI/ML engineering, defence sector solution architects, and US federal sales. AIP boot camps (560+ organisations by Q4 2024) are the primary commercial sales motion.

##### Sources

1. [Palantir 10-K FY2024](https://sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1321655&type=10-K) — revenue, margins, employee count, accessed 2026-04-16
1. [Palantir Q4 2024 earnings release](https://investors.palantir.com/news-releases/news-release-details/palantir-technologies-reports-fourth-quarter-2024-results) — quarterly revenue, commercial growth, accessed 2026-04-16
1. [Palantir.com/platforms](https://palantir.com/platforms) — product descriptions, accessed 2026-04-16
1. [S&P 500 inclusion, Sep 2024](https://spglobal.com/spdji/en/indices/equity/sp-500) — index addition, accessed 2026-04-16
1. [Reuters — Army contract, Jan 2025](https://reuters.com/technology/palantir-wins-army-contract-2025-01) — Vantage contract extension, accessed 2026-04-16
1. [Palantir careers page](https://palantir.com/careers) — hiring signals, accessed 2026-04-16
1. [LinkedIn: Palantir Technologies](https://linkedin.com/company/palantir-technologies) — employee count, executive profiles, accessed 2026-04-16
1. [Crunchbase: Palantir](https://crunchbase.com/organization/palantir-technologies) — founding history, funding context, accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 6.5/6.5 (100%) | 2026-04-16 |

- [x] PASS: Skill defines a clear trigger or usage context — frontmatter description lists exact use cases ("due diligence prep, competitive context, or general company research"); `user-invocable: true` and `argument-hint` are set.
- [x] PASS: Skill specifies what sources to check — Steps 1 and 5 enumerate jurisdiction-specific registries (ASIC Connect, ABN Lookup, NZ Companies Office, SEC EDGAR, Companies House) plus Crunchbase, LinkedIn, and Google News by name and URL.
- [x] PASS: Skill defines an output structure with named sections — output format block contains seven explicitly named sections: Overview, Products/services, Team, Financials, Recent news, Strategic direction, Sources.
- [x] PASS: Output structure includes business model or "what they do" section — Step 2 captures "What the company does and its business model"; Overview table template has explicit `Business model` and `Revenue model` rows.
- [x] PASS: Output structure includes financials or funding section — `### Financials` is a named section; Step 4 specifies revenue/growth/margin for public companies and Crunchbase funding rounds for private, requiring source and date on every figure.
- [x] PASS: Output structure includes recent news or developments section — `### Recent news` is a named section; Step 5 defines search method and priority topics (funding, launches, leadership, regulatory, acquisitions, layoffs).
- [~] PARTIAL: Skill includes guidance on assessing source credibility or recency — the 18-month staleness flag is present, mandatory two-source cross-reference is required, and per-figure source+date is enforced. Recency is well-handled; source authority ranking is not explicitly addressed. Scored 0.5.
- [-] SKIP: Skill references collaboration with other agents — skipped; the skill is a standalone SKILL.md with no agent routing logic.

## Notes

The PARTIAL ceiling on source credibility is conservative given how much recency and sourcing discipline the skill already requires. The missing piece is explicit guidance on distinguishing source authority (primary registry vs secondary press) within the skill steps — that lives in the agent definition instead.
