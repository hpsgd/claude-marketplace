---
name: write-battle-card
description: "Write a competitive battle card — a one-page sales reference for a specific competitor. Produces a concise card with win/lose analysis, objection handling, and proof points. Use when sales needs a quick reference for competitive deals."
argument-hint: "[competitor name or product to create battle card for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a competitive battle card for $ARGUMENTS.

A battle card is a one-page reference a salesperson can use during a live call. It must be scannable in under 30 seconds, evidence-based, and honest about where we lose.

## Step 1 — Research the competitor

Before writing anything, gather current intelligence:

1. **Check existing analysis.** Search the codebase and docs for prior `/gtm:competitive-analysis` output on this competitor. Do not duplicate work.
2. **Competitor profile.** What do they do? Who do they sell to? What is their pricing model?
3. **Recent changes.** New features, pricing changes, acquisitions, leadership changes — anything that affects competitive positioning.
4. **Win/loss data.** Search for deal retrospectives, CRM notes, or customer feedback that mentions this competitor.

**Rule:** Every claim on the battle card must have a source. If you cannot verify it, mark it as "Unverified — needs confirmation" rather than stating it as fact.

## Step 2 — Identify win/lose dynamics

Analyse head-to-head dynamics across dimensions that matter to buyers:

| Dimension | We win | They win | It's a wash |
|---|---|---|---|
| [Core capability 1] | [specific evidence] | [specific evidence] | [specific evidence] |
| [Core capability 2] | [specific evidence] | [specific evidence] | [specific evidence] |
| Pricing | [specific evidence] | [specific evidence] | [specific evidence] |
| Ease of use | [specific evidence] | [specific evidence] | [specific evidence] |
| Support | [specific evidence] | [specific evidence] | [specific evidence] |
| Integration | [specific evidence] | [specific evidence] | [specific evidence] |

**Rules for win/lose analysis:**
- **Be specific.** "Better UX" is not a win. "Onboarding takes 5 minutes vs. their 2-hour setup" is a win.
- **Include where we lose.** A battle card that claims we win everywhere is not credible. Sales will lose trust in the card and stop using it.
- **Quantify where possible.** Numbers beat adjectives. "3x faster" beats "much faster."
- **Focus on what buyers care about.** Winning on a dimension buyers ignore is not winning.

## Step 3 — Build objection handling

For every common objection a prospect raises about choosing us over this competitor, provide a structured response:

```
### Objection: "[What the prospect says]"

**Why they say it:** [Root cause — is it a real concern, a misconception, or competitor FUD?]

**Response:** [What the salesperson should say — conversational, not scripted]

**Proof point:** [Specific evidence — customer quote, benchmark, case study, documentation link]
```

Build at least 4 objection-response pairs. Prioritise by frequency — the objections sales hears most go first.

**Rules for objection handling:**
- **Never dismiss the objection.** Acknowledge it, then redirect.
- **Proof points are mandatory.** A response without evidence is opinion. Prospects can smell it.
- **If the objection is valid, say so.** "That's a fair point — here's how our customers work around it" is stronger than denying reality.

## Step 4 — Create landmine questions

Landmine questions are questions the salesperson asks the prospect that expose competitor weaknesses without directly attacking the competitor.

### Questions to ask (expose their weaknesses)

| Question | Why it works | Expected answer if using competitor |
|---|---|---|
| "[Question that probes a known weakness]" | [What this reveals] | [What they'll likely say, and how to follow up] |
| "[Question about a capability we're strong in]" | [What this reveals] | [What they'll likely say, and how to follow up] |
| "[Question about total cost of ownership]" | [What this reveals] | [What they'll likely say, and how to follow up] |

### Questions to avoid (expose our weaknesses)

| Question | Why it's dangerous | If it comes up anyway |
|---|---|---|
| "[Question that probes our known weakness]" | [What this reveals about us] | [How to handle it honestly] |
| "[Question about a capability they're strong in]" | [What this reveals about us] | [How to redirect the conversation] |

**Rule:** Never coach salespeople to lie or mislead. Landmine questions should reveal genuine differences, not trick the prospect.

## Step 5 — Assemble the battle card

Compile the final battle card using this template:

```markdown
# Battle Card: [Our Product] vs. [Competitor]

**Last updated:** [date]
**Confidence level:** [High / Medium / Low — based on data freshness and completeness]

## TL;DR
[2-3 sentences: when we win, when we lose, and the single most important thing to remember]

## Quick Comparison
| Dimension | Us | Them | Verdict |
|---|---|---|---|
| [dimension] | [specific] | [specific] | [Win / Lose / Tie] |

## Where We Win
1. [Strongest advantage — with proof point]
2. [Second advantage — with proof point]
3. [Third advantage — with proof point]

## Where We Lose (be honest)
1. [Their advantage — with mitigation strategy]
2. [Their advantage — with mitigation strategy]

## Objection Handling
| Objection | Response | Proof |
|---|---|---|
| "[objection]" | [response] | [evidence] |

## Landmine Questions
- "[Question to ask]" — reveals [what]
- "[Question to ask]" — reveals [what]
- "[Question to ask]" — reveals [what]

## Questions to Avoid
- "[Dangerous question]" — if it comes up: [how to handle]

## Key Proof Points
- **Customer quote:** "[quote]" — [customer name/type]
- **Benchmark:** [metric comparison with source]
- **Case study:** [summary with link]

## Competitive Intel Sources
- [Source 1 — date last checked]
- [Source 2 — date last checked]
```

## Rules

- **Evidence-based only.** Every claim needs a source. No unsourced assertions on a document salespeople will use in front of prospects.
- **Update quarterly at minimum.** A stale battle card is worse than no battle card — it gives salespeople false confidence. Include the "last updated" date prominently.
- **Be honest about weaknesses.** Sales reps will discover our weaknesses in live calls. If the battle card doesn't prepare them, they'll be caught flat-footed and lose the deal anyway.
- **Concise enough for a sales call.** If a rep can't scan the card and find what they need in 30 seconds, the card is too long. Prefer tables and bullets over paragraphs.
- **One competitor per card.** Do not combine multiple competitors into a single card. Each card is a focused reference for a specific competitive deal.
- **Proof points must be current.** A case study from 2 years ago or a benchmark on a deprecated version hurts credibility.

## Related Skills

- `/gtm:competitive-analysis` — feeds into this skill. Run a competitive analysis first to generate the research that battle cards distil into a sales-ready format.
- `/gtm:positioning` — provides the positioning context that shapes how we frame our advantages on the battle card.
