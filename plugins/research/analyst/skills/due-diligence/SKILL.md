---
name: due-diligence
description: "Assess a company from public sources for a specific decision: partnership, investment consideration, or acquisition. Produces a structured signal summary with green/red indicators. Public data only."
argument-hint: "[company name] for [partnership | investment | acquisition]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Produce a public-data due diligence report on $ARGUMENTS.

This skill covers public-data diligence only. Legal, financial, and technical diligence requires direct access to private information — flag this clearly in the output.

## Step 1: Establish scope

Before researching, confirm what decision this diligence is for:

- **Commercial partnership** — focus on product-market fit, team stability, and reputational risk
- **Investment consideration** — focus on growth trajectory, unit economics signals, and competitive moat
- **Acquisition consideration** — full picture: fundamentals + product + team + market position + risk

The scope determines how deep to go on each section. Misclassified scope produces an incomplete report.

## Step 2: Business fundamentals

For public companies: pull latest annual report/filing for revenue, growth rate, gross margin, key operational metrics.

For private companies: Crunchbase for funding history; press for disclosed revenue milestones; LinkedIn for headcount growth as a proxy.

Each figure needs a source and date. Label revenue estimates for private companies explicitly.

## Step 3: Product signals

Customer sentiment from public reviews:

- [G2](https://www.g2.com) — review count, score, score trend, category rank
- [Capterra](https://www.capterra.com) — secondary review source
- App Store / Google Play — mobile products

Look for: score trend over 6+ months (not just current score), review velocity (growing or stalling), themes in negative reviews (support, reliability, missing features).

Also note: notable customer wins mentioned in press, reference customers on their website, case studies.

## Step 4: Team

From company website, LinkedIn, and press:

- Founding team backgrounds (relevant domain experience, prior exits)
- Current key executives — tenures, any recent departures
- Notable hires in last 12 months (signal of growth direction)
- Notable departures in last 12 months (potential instability flag)

Note: executive churn without a clear succession announcement is a red signal.

## Step 5: Market position

- Analyst market share estimates (cite report and year)
- Growth rate vs market growth rate (is the company growing faster or slower than the market?)
- Any identifiable competitive moat (network effects, switching costs, data advantage, regulatory barriers)
- Customer concentration signals (are case studies all from one segment?)

## Step 6: Risk factors

- Regulatory exposure: active proceedings, compliance actions — search ASIC Connect (AU), Companies House (UK), SEC EDGAR (US)
- Litigation: court filings, press coverage of legal disputes
- Reputational: negative press, data breach history, executive controversy
- Financial red flags: down rounds, flat rounds, long gaps between funding with no milestone announced
- Operational red flags: hiring freeze with no explanation, mass layoffs, major customer losses

## Step 7: Signal summary

Classify every major finding against the signal taxonomy before writing the verdict.

**Green signals:**

- Consecutive funding rounds with increasing round size
- Core founding team still in place after 3+ years
- Review score stable or improving, review count growing
- Customer logos include recognisable names in target segment
- Hiring volume growing, seniority of hires increasing
- Press coverage is product-led (shipping) not just funding-led (raising)

**Red signals:**

- Sudden C-suite departure without succession announcement
- Down round or flat round after strong growth
- Review score declining over 6+ months
- Regulatory proceedings or litigation in public records
- Layoff announcements without a clear restructuring narrative
- Hiring freeze with no public explanation
- Long gap between funding rounds, no revenue milestone announced
- Heavy reliance on a single customer segment

## Red flag escalation

When the signal summary contains two or more red signals, don't stop at the verdict. Route deeper:

| Red signal type | Follow-on |
|---|---|
| Regulatory or litigation findings | `/investigator:public-records` for the full court and regulatory record |
| Complex or opaque ownership | `/investigator:corporate-ownership` to map the full structure |
| Reputational concern or data breach history | `/investigator:entity-footprint` for digital footprint and press timeline |
| Customer concentration or market position concern | `/analyst:competitive-analysis` to understand alternatives |

One red signal warrants noting. Two or more warrants investigation.

## Rules

- State the scope explicitly at the top. Diligence for a partnership is narrower than for an acquisition.
- Every revenue figure needs a source and date.
- Revenue ≠ valuation. Distinguish them — the confusion causes real decisions to go wrong.
- The signal summary must precede the verdict. Don't write conclusions without showing the signals.
- Flag clearly that this is public-data diligence only. Private diligence (financials, legal, technical) requires direct access.

## Output format

```markdown
## Due diligence: [Company name]

**As of:** [date]
**Scope:** [partnership | investment consideration | acquisition consideration]
**Data type:** Public sources only

### Business fundamentals

[Revenue, growth rate, funding history — each figure with source and date]

### Product signals

[Customer review summary — score, trend, review count, key themes]

### Team

[Founding team backgrounds, key executive tenures, notable hires and departures]

### Market position

[Share estimate, growth vs market, moat assessment]

### Risk factors

[Regulatory, litigation, reputational, financial, operational flags]

### Signal summary

| Signal | Status | Evidence |
|---|---|---|
| Team stability | 🟢 / 🟡 / 🔴 | [evidence] |
| Funding trajectory | 🟢 / 🟡 / 🔴 | [evidence] |
| Customer sentiment trend | 🟢 / 🟡 / 🔴 | [evidence] |
| Hiring velocity | 🟢 / 🟡 / 🔴 | [evidence] |
| Regulatory/legal exposure | 🟢 / 🟡 / 🔴 | [evidence] |
| Strategic fit | 🟢 / 🟡 / 🔴 | [evidence] |

**Verdict:** [one sentence — the 1-2 factors that most influence it]

**Note:** This is public-data diligence only. Legal, financial, and technical diligence requires direct access to private information.

### Sources

1. [Title](URL) — [what it contributed]
```
