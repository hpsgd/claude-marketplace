---
name: competitive-analysis
description: Research and analyse competitors — strengths, weaknesses, positioning, and differentiation opportunities.
argument-hint: "[competitor name, or 'landscape' for the full competitive set]"
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep, WebSearch, WebFetch
---

Analyse $ARGUMENTS competitively using the mandatory process below.

## Step 1 — Define the competitive set

Before analysing individual competitors, map the full landscape. Competitors come in five types — you must consider all five:

| Type | Definition | Example |
|---|---|---|
| **Direct** | Same product category, same target customer | Competitor X that does what you do |
| **Indirect** | Different category, same problem solved | A general-purpose tool used for this specific job |
| **Substitute** | Fundamentally different approach to the same need | Manual processes, spreadsheets, hiring a person |
| **Potential** | Not competing today but could enter easily | Adjacent product with the right audience and distribution |
| **Customer inertia** | Doing nothing — the status quo | "We've always done it this way" |

List at least 3 direct competitors and at least 2 non-obvious competitors (indirect, substitute, or potential). If the user asked about a specific competitor, still briefly map the full landscape for context.

## Step 2 — Research each competitor

For each competitor, gather the following. Use `WebSearch` and `WebFetch` to find current information. If information is unavailable, state "Unknown — could not verify" rather than guessing.

### Competitor profile template

```
## [Competitor name]

### What they do
[One paragraph. What is the product? What problem does it solve? For whom?]

### Target customer
- Primary segment: [who they primarily serve]
- Company size: [startup / SMB / mid-market / enterprise]
- Industry focus: [horizontal or specific verticals]
- Buyer persona: [title/role of the decision maker]

### Product
- Core capabilities: [what the product actually does — be specific]
- Platform: [web, mobile, desktop, API, CLI]
- Integrations: [key integrations]
- Technical approach: [how they solve the problem — architecture, methodology]

### Pricing
- Model: [per seat / usage-based / flat rate / freemium / enterprise-only]
- Entry price: [lowest tier price if public]
- Enterprise: [custom pricing? what's included?]
- Free tier: [what's available for free?]

### Strengths (be honest)
1. [Specific strength with evidence]
2. [Specific strength with evidence]
3. [Specific strength with evidence]

### Weaknesses (be specific)
1. [Specific weakness with evidence — user reviews, known limitations, architectural constraints]
2. [Specific weakness with evidence]
3. [Specific weakness with evidence]

### Positioning
- How they describe themselves: "[their tagline or one-liner]"
- Market category they claim: [category]
- Key messaging themes: [what they emphasise in marketing]

### Traction signals
- Funding / revenue: [if known]
- Team size: [if known]
- Customer logos: [notable customers]
- Growth trajectory: [growing, stable, declining — based on available signals]
```

Rules for competitor research:
- **Strengths must be honest.** Dismissing competitors' strengths is dangerous. If they're winning deals, there's a reason.
- **Weaknesses must be specific.** "Bad UX" is not a weakness. "Requires a 45-minute setup wizard with 23 configuration fields before first use" is.
- **Pricing must be current.** State the date you checked. Pricing changes.
- **Evidence over opinion.** Cite user reviews, G2/Capterra ratings, public complaints, documented limitations — not your gut feeling.

## Step 3 — Build the comparison table

Create a feature-by-feature comparison. Choose dimensions that matter to buyers, not dimensions that make you look good.

```
| Dimension | Your product | Competitor A | Competitor B | Competitor C |
|---|---|---|---|---|
| [Core capability 1] | [specifics] | [specifics] | [specifics] | [specifics] |
| [Core capability 2] | [specifics] | [specifics] | [specifics] | [specifics] |
| Setup time | [specifics] | [specifics] | [specifics] | [specifics] |
| Pricing (entry) | [specifics] | [specifics] | [specifics] | [specifics] |
| Pricing (at scale) | [specifics] | [specifics] | [specifics] | [specifics] |
| Integration depth | [specifics] | [specifics] | [specifics] | [specifics] |
| [Differentiator 1] | [specifics] | [specifics] | [specifics] | [specifics] |
| [Differentiator 2] | [specifics] | [specifics] | [specifics] | [specifics] |
```

Rules for the comparison table:
- **Use specific values, not ratings.** "5-minute setup" not "Easy setup." "$49/mo for 10 users" not "Affordable."
- **Include dimensions where you lose.** A comparison table where you win every row is not credible and not useful.
- **Include non-obvious competitors** in the table — especially "manual process / spreadsheet" as a column, because that's what you're often really competing against.
- **Distinguish between "has feature" and "does feature well."** A checkbox comparison is misleading. Depth and quality matter.

## Step 4 — Analyse differentiation

For each competitor, answer:

### Head-to-head differentiation

```
#### vs. [Competitor name]

**Where we win:**
- [Specific advantage with evidence — e.g., "3x faster import because of streaming architecture vs. their batch processing"]

**Where we lose:**
- [Specific disadvantage with evidence — e.g., "They support 40+ integrations natively; we support 12"]

**Where it's a wash:**
- [Areas of parity]

**Their likely counter-positioning:**
- [What they would say about you — anticipate their sales objections]

**Best counter-argument:**
- [How to respond when a prospect says "but Competitor X does..."]
```

Rules for differentiation:
- **Specific over generic.** "Better performance" is worthless. "Dashboard loads in 200ms vs. their 3-second average (verified by independent benchmark)" is a weapon.
- **Sustainable over temporary.** Can they match this in 6 months? If yes, it's a feature gap, not differentiation. True differentiation comes from architecture, approach, or business model — things that are hard to copy.
- **Differentiation must matter to the buyer.** Being different in ways the customer doesn't care about is not differentiation.

## Step 5 — Identify strategic opportunities

Based on the full analysis, identify:

### Underserved segments

```
| Segment | Why underserved | How to win them | Confidence |
|---|---|---|---|
| [segment] | [what competitors miss] | [your approach] | High / Medium / Low |
```

### Feature gaps in the market

```
| Gap | Who needs it | Which competitors could fill it | Priority |
|---|---|---|---|
| [capability nobody does well] | [segment] | [competitors] | High / Medium / Low |
```

### Positioning white space

Where in the market is there room to position that no competitor owns? Consider:
- Price point gaps (is there a gap between free tools and enterprise pricing?)
- Audience gaps (is there a segment nobody targets?)
- Approach gaps (is everyone solving this the same way, and is there a better way?)

### Competitive threats

```
| Threat | Source | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| [what could happen] | [which competitor] | High / Medium / Low | High / Medium / Low | [what to do about it] |
```

## Step 6 — Output

Deliver the analysis in this order:

1. **Executive summary** (3-5 sentences) — the most important findings
2. **Competitive landscape map** — the full set of competitors by type
3. **Individual competitor profiles** — one per competitor using the template from Step 2
4. **Comparison table** — the feature comparison from Step 3
5. **Differentiation analysis** — head-to-head for each major competitor from Step 4
6. **Strategic opportunities** — from Step 5
7. **Recommended actions** — top 3 things to do based on this analysis, each with:
   - What to do
   - Why (tied to a specific finding)
   - Timeline (now / next quarter / long-term)
   - Expected impact

## Rules

- Never dismiss a competitor. If they exist and have customers, they're doing something right. Find out what.
- Analyse competitors as they are today, not as they were six months ago. Products change fast.
- Include non-obvious competitors. The spreadsheet your prospect uses today is a harder competitor than the startup that just raised a Series A.
- Differentiation must be specific and verifiable. If a salesperson can't use it in a call, it's too vague.
- Be honest about where you lose. The analysis is for internal strategy, not marketing copy. Lying to yourself is the most expensive kind of lying.
- Update this analysis quarterly. Competitive landscapes change. A 6-month-old competitive analysis is a liability, not an asset.
- When information is unavailable, say so. "Unknown" is better than a guess presented as fact.
