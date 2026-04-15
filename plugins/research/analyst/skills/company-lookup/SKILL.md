---
name: company-lookup
description: "Research a company from public sources: overview, products, team, financials, recent news, and strategic direction. Use for due diligence prep, competitive context, or general company research. Covers AU/NZ sources (ASIC, ABN, NZ Companies Office)."
argument-hint: "[company name]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Produce a structured company snapshot for $ARGUMENTS from publicly available sources.

## Step 1: Identify source types

Before searching, determine which source types apply:

- **Public company (ASX/NZX/NYSE/NASDAQ):** annual reports, exchange filings
- **AU company:** ASIC Connect (`connect.asic.gov.au`) for company extract, director history, financials; ABN Lookup (`abn.business.gov.au`) for ABN/ACN cross-reference
- **NZ company:** NZ Companies Office (`companies.govt.nz`) for director history, shareholding, annual returns
- **US public company:** SEC EDGAR for 10-K/10-Q filings
- **UK company:** Companies House for filings and structure
- **Private company:** Crunchbase, LinkedIn, press

If the company's jurisdiction or listing status is unclear, run a quick name search on ASIC Connect and Crunchbase first to establish it.

## Step 2: Research overview and products

Search for: company name + "about", company website, LinkedIn company page.

Capture:

- What the company does and its business model
- Core products/services with pricing if public
- Target customer and market segment
- Founding year, HQ, and approximate size (employee count or revenue band)

## Step 3: Research team

Search company website "team" or "leadership" page, LinkedIn.

Capture founding team backgrounds and current key executives (name, role, tenure where visible).

Note notable hires or departures in the last 12 months.

## Step 4: Research financials

For public companies: pull latest annual report or filing for revenue, growth rate, and key metrics.

For private companies: check Crunchbase for funding rounds (amount, date, investors, valuation if disclosed). Note when data was last confirmed.

Never present a revenue figure without its source and date. Label estimates as estimates.

## Step 5: Research recent news

Search: `[company name] site:news.google.com` or Google News for last 6 months.

Prioritise: funding rounds, product launches, leadership changes, regulatory actions, acquisitions, layoffs.

## Step 6: Assess strategic direction

Signals for where the company is heading:

- Current job postings (company careers page + LinkedIn Jobs + Seek for AU/NZ) — engineering hires in a new area, senior leadership hires in a new function
- Recent press releases and executive statements
- Product launches and roadmap announcements
- Investor day or analyst day materials (public companies)

## Rules

- Never present a revenue estimate for a private company without stating the source and explicitly labelling it as an estimate.
- Cross-reference at least two independent sources for any fact listed in the output.
- If the company has no meaningful public web presence, flag before proceeding — may be too early-stage for useful intelligence.
- Revenue ≠ valuation. Distinguish these clearly when both appear.
- Recency matters on competitive data. Flag any source older than 18 months.

## Output format

```markdown
## Company: [Name]

**As of:** [date]
**Sources:** [count] public sources

### Overview

[2-3 sentence summary]

| Attribute | Detail |
|---|---|
| Founded | — |
| HQ | — |
| Size | — |
| Business model | — |
| Revenue model | — |

### Products/services

[Structured summary with pricing where public]

### Team

[Key executives — name, role, tenure — sourced from company site or LinkedIn]

### Financials

[Revenue or funding data — each figure with source and date]

### Recent news

[Bulleted list, dated, most recent first]

### Strategic direction

[Key themes from job postings, announcements, executive statements]

### Sources

1. [Title](URL) — [what it contributed]
```
