---
name: market-sizing
description: "Estimate the size of a market using top-down and bottom-up methods with explicit methodology. Use when you need a defensible TAM/SAM/SOM figure for a business plan, pitch, or investment decision."
argument-hint: "[market to size, with geography and buyer type if known]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Produce a market sizing estimate for $ARGUMENTS with explicit methodology.

## Step 1: Define the market

A market size without a definition is a number without meaning. Establish:

- **Buyer:** who is paying? (individual, SMB, enterprise, government department)
- **Purchase unit:** what are they buying? (subscription, one-time, services engagement)
- **Geography:** global, country-level, or regional?
- **Time horizon:** current year, or a projected year?

State these assumptions explicitly. Different assumptions produce wildly different numbers — the definition IS the methodology.

## Step 2: Top-down estimate

Find analyst estimates from credible sources:

- [Gartner](https://www.gartner.com) — technology markets
- [IDC](https://www.idc.com) — technology markets
- [Grand View Research](https://www.grandviewresearch.com) — broad industry coverage
- [IBISWorld](https://www.ibisworld.com) — AU industry reports specifically (`ibisworld.com/au`)
- [ABS](https://www.abs.gov.au) — AU macro/industry data
- [Stats NZ](https://www.stats.govt.nz) — NZ industry data

For each estimate: note the specific report title, year published, and the exact figure cited. Never round-trip a sourced figure without the original citation.

If no analyst report exists for this specific market, note it and proceed to bottom-up.

## Step 3: Bottom-up estimate

Build independently from first principles:

1. **Estimate addressable customer count** — how many potential buyers exist? (Use industry association data, government statistics, LinkedIn company size filters as proxies)
2. **Estimate average annual spend** — what does a typical buyer spend? (Use public pricing, customer testimonials, analyst benchmarks)
3. **Apply realistic penetration** — what share could be captured at maturity? (Comparable market penetration rates from analogous markets)

Show the calculation explicitly: `N customers × $X avg spend × Y% penetration = $Z`

## Step 4: Reconcile

Do the top-down and bottom-up figures agree within 2x?

- **Yes:** report both, note the alignment as confidence signal
- **No:** explain the variance. Common reasons: different market definitions, different geographies, different buyer segmentation. Don't average them — resolve the discrepancy

## Step 5: Growth rate

Find CAGR from:

- Analyst report projections (preferred)
- Public company revenue growth rates in the space (proxy — available from earnings reports)
- VC/PE investment velocity as a leading signal

Note the source and the period it covers.

## Rules

- A market size without methodology is a guess wearing a number's clothes. Always show the working.
- Label all estimates as estimates. Never present a number as fact unless it comes from a primary regulatory or government source.
- Top-down and bottom-up must both be attempted. If one genuinely can't be done, explain why.
- Don't average unreconciled top-down and bottom-up figures. Diagnose the gap instead.
- Distinguish TAM (total addressable), SAM (serviceable addressable), and SOM (serviceable obtainable) if the question calls for it. If not asked, default to TAM and state what's included.

## Output format

```markdown
## Market sizing: [Market name]

**As of:** [date]
**Market definition:** [buyer, purchase unit, geography, time horizon]

### Size estimates

| Method | Estimate | Source | Methodology |
|---|---|---|---|
| Top-down | $Xbn | [Analyst report, year] | [Brief description] |
| Bottom-up | $Xbn | Own calculation | [N customers × $X spend × Y% penetration] |

### Reconciliation

[Do the figures align? If not, why not?]

### Growth rate

[CAGR estimate with source and period]

### Confidence: [High / Medium / Low]

[Reasoning — do multiple sources agree? How recent is the data? How well-defined is the market?]

### Sources

1. [Title](URL) — [what it contributed]
```
