---
name: competitive-analysis
description: "Map the competitive landscape for a market or product space: identify competitors, compare on key dimensions, and surface strategic moves. Includes job posting analysis as a leading indicator of product direction."
argument-hint: "[market, product, or company to analyse]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Produce a competitive analysis for $ARGUMENTS.

## Step 1: Define the market

Before identifying competitors, define what you're actually comparing:

- What problem is being solved?
- Who is the buyer? (individual, SMB, enterprise, government)
- What is the purchase unit? (subscription, licence, one-time, services)
- What geography? (global, US, AU/NZ, other)

If these aren't clear from $ARGUMENTS, make your assumptions explicit in the output.

## Step 2: Identify competitors

Three categories:

- **Direct** — same solution, same customer, competing for the same purchase decision
- **Indirect** — different solution, same underlying problem
- **Substitutes** — alternative approaches the buyer might choose instead (including doing nothing or building in-house)

Sources: G2 category pages, Capterra category pages, "alternatives to [product]" searches, industry analyst quadrant reports, LinkedIn "companies also viewed."

For AU/NZ markets: IBISWorld AU reports, Seek job postings pattern, local industry press.

List each competitor with a one-line positioning statement before building the matrix.

## Step 3: Build comparison matrix

For each identified competitor, research:

| Attribute | What to look for |
|---|---|
| Positioning | Their own words — tagline, homepage hero, ICP |
| Pricing tier | Free/freemium/SMB/mid-market/enterprise — exact pricing if public |
| Strengths | G2/Capterra review themes, analyst commentary, customer win stories |
| Weaknesses | Negative review themes, gaps in feature set, company risk factors |
| Reported market share | Analyst estimates where available — label clearly as estimates |

## Step 4: Job postings as roadmap signal

Search each competitor's careers page and LinkedIn Jobs. Engineering hires in a new area signal product direction before any announcement.

Patterns to look for:

- New language or platform skills appearing in bulk (ML, mobile, specific cloud)
- Senior leadership hires in a new function (first Head of Enterprise Sales = moving upmarket)
- Spikes in hiring volume (growth mode) or absence of hiring (freeze or pivot)

For AU/NZ companies: check Seek (`seek.com.au` / `seek.co.nz`) alongside LinkedIn for a fuller picture of hiring activity.

Cross-reference with their public announcements — divergence between what they say and what they're hiring for is the more useful signal.

## Step 5: Recent strategic moves

For each competitor, note the last 12 months:

- Acquisitions and partnerships
- Pricing changes or packaging shifts
- Major product launches or deprecations
- Fundraising rounds or M&A activity
- Leadership changes

## Step 6: Differentiation analysis

Synthesise: who is winning on what dimension, and why? One paragraph per meaningful differentiation axis. Take a position — don't just describe, conclude.

## Rules

- Define the market before mapping competitors. A comparison without scope is noise.
- Label market share estimates as estimates with source and date.
- Flag sources older than 18 months on competitive analysis — a competitor can ship a lot in that time.
- Don't produce a matrix so wide it can't be read. Cap at 6 attributes if there are more than 4 competitors.
- Job posting data is a leading indicator, not a fact. Label it as signal, not confirmation.

## Output format

```markdown
## Competitive analysis: [Space]

**As of:** [date]
**Market definition:** [buyer, purchase unit, geography]
**Competitors identified:** [count] direct, [count] indirect

### Competitor comparison

| Company | Positioning | Pricing tier | Strengths | Weaknesses |
|---|---|---|---|---|

### Hiring signals

| Company | Signal | Source |
|---|---|---|

### Recent strategic moves

[Bulleted list by company, dated]

### Differentiation analysis

[Who is winning on what dimension, with evidence — one paragraph per axis]

### Sources

1. [Title](URL) — [what it contributed]
```
