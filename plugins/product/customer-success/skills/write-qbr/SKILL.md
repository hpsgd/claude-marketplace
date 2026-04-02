---
name: write-qbr
description: "Prepare a Quarterly Business Review for a customer account. Produces a structured QBR document with value delivered, usage highlights, and strategic recommendations. Use before quarterly customer meetings."
argument-hint: "[customer name or account to prepare QBR for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Prepare a Quarterly Business Review for $ARGUMENTS.

A QBR is a strategic conversation, not a product demo. It must lead with value delivered, acknowledge challenges honestly, and propose specific next steps. The document should be ready for presentation to the customer's executive sponsor.

## Step 1 — Gather account data

Collect all relevant data before writing anything:

1. **Health score.** Pull the latest health assessment (or run `/customer-success:health-assessment` if none exists). Record the composite score and dimension breakdown.
2. **Usage metrics.** DAU/MAU, feature adoption rates, usage trends over the quarter. Identify features used heavily and features not adopted.
3. **Support history.** Tickets opened this quarter — volume, severity, resolution time, recurring themes. Note any P1/P2 incidents.
4. **Goals from last QBR.** What did we commit to? What did the customer commit to? Track each goal to completion status.
5. **Commercial context.** Contract renewal date, current tier, billing status, any pricing discussions.
6. **Relationship signals.** NPS/CSAT scores, meeting attendance, executive sponsor engagement, champion status.

**Rule:** If data is unavailable for a dimension, state the gap explicitly. Do not fabricate metrics. "Usage data unavailable — analytics integration pending" is honest; an invented number is a trust-destroying liability.

## Step 2 — Analyse value delivered

Translate raw metrics into business outcomes the customer cares about:

### ROI and goal tracking

| Goal (from last QBR) | Target | Actual | Status | Evidence |
|---|---|---|---|---|
| [Goal 1] | [metric target] | [metric actual] | [Met / Partial / Missed] | [specific data] |
| [Goal 2] | [metric target] | [metric actual] | [Met / Partial / Missed] | [specific data] |

### Usage highlights

| Metric | Last quarter | This quarter | Change | Interpretation |
|---|---|---|---|---|
| [Key metric 1] | [value] | [value] | [+/- %] | [what this means for the customer] |
| [Key metric 2] | [value] | [value] | [+/- %] | [what this means for the customer] |

### Value narrative

Write 2-3 paragraphs summarising the value story in business language, not product language. "Your team resolved 40% more support tickets this quarter using the automation workflows" not "Automation workflow usage increased 40%."

**Rules for value analysis:**
- **Quantify everything.** "Your team saved approximately 120 hours this quarter" not "Your team saved a lot of time."
- **Tie metrics to their goals, not ours.** Frame usage in terms of customer outcomes, not product engagement.
- **Acknowledge missed goals honestly.** If we did not deliver on a commitment, say so with a remediation plan.

## Step 3 — Identify risks and recommendations

### Risks

| Risk | Severity | Evidence | Recommended action |
|---|---|---|---|
| [Underutilised feature] | Medium | [adoption rate, usage data] | [Training session, workflow review] |
| [Support pattern] | [severity] | [ticket trends] | [root cause fix, process change] |
| [Relationship gap] | [severity] | [engagement signals] | [executive outreach, sponsor identification] |
| [Renewal concern] | [severity] | [commercial signals] | [value reinforcement, pricing discussion] |

### Expansion opportunities

Identify specific expansion signals — but only recommend expansion for healthy accounts.

| Opportunity | Signal | Estimated value | Timing |
|---|---|---|---|
| [Upsell / cross-sell opportunity] | [what triggered this — usage pattern, team growth, feature request] | [ARR impact] | [this quarter / next quarter] |

### Strategic recommendations

Provide 3-5 specific recommendations for the next quarter. Each must be:
- **Specific** — "Run a 2-hour training session on reporting features for the analytics team" not "Increase adoption"
- **Tied to evidence** — linked to a metric, risk, or opportunity identified above
- **Owned** — who is responsible (us or the customer)
- **Time-bound** — when it should happen

## Step 4 — Prepare the QBR document

Assemble the final QBR using this template:

```markdown
# Quarterly Business Review: [Customer Name]

**Quarter:** [Q1/Q2/Q3/Q4 YYYY]
**Prepared by:** [CSM name]
**Date:** [date]
**Next QBR:** [scheduled date]

## Executive Summary
[3-5 sentences: health status, key wins, key challenges, top recommendation]

## Value Delivered This Quarter

### Goals Scorecard
| Goal | Target | Actual | Status |
|---|---|---|---|
| [goal] | [target] | [actual] | [Met / Partial / Missed] |

### Key Wins
1. [Win with quantified impact]
2. [Win with quantified impact]
3. [Win with quantified impact]

### Usage Trends
| Metric | Last quarter | This quarter | Change |
|---|---|---|---|
| [metric] | [value] | [value] | [delta] |

## Challenges and Lessons Learned
| Challenge | Impact | What we did | Current status |
|---|---|---|---|
| [issue] | [business impact] | [response] | [resolved / in progress / monitoring] |

## Health Overview
- **Composite score:** [0-100] ([Healthy / Neutral / At Risk / Critical])
- **Trend:** [improving / stable / declining]
- **Key signals:** [top 2-3 health signals]

## Recommendations for Next Quarter

### Goals
| Goal | Metric | Target | Owner | Timeline |
|---|---|---|---|---|
| [specific goal] | [how measured] | [number] | [us / customer] | [by when] |

### Expansion Opportunities
| Opportunity | Business case | Next step |
|---|---|---|
| [opportunity] | [why it makes sense for them] | [specific action] |

## Appendix
- Detailed usage data
- Support ticket summary
- Feature adoption breakdown
```

## Rules

- **Quantify everything.** A QBR without numbers is a conversation without substance. Every claim about value needs a metric.
- **Lead with value, not product updates.** The customer does not care about your release notes. They care about what those releases did for them. Product updates go in the appendix, not the executive summary.
- **Be honest about challenges.** Hiding problems from the customer destroys trust. Acknowledging them with a remediation plan builds it. If there was a P1 incident, address it directly.
- **Recommendations must be specific.** "Improve adoption" is not a recommendation. "Schedule a 90-minute training session for the 12-person analytics team on the reporting module by end of next month" is a recommendation.
- **Do not propose expansion to unhealthy accounts.** If the customer is At Risk or Critical, the QBR should focus on stabilisation, not upselling. Expansion conversations with struggling customers accelerate churn.
- **Track commitments both ways.** A QBR captures what we will do and what the customer will do. Both sides need accountability.

## Related Skills

- `/customer-success:health-assessment` — feeds the health score and dimension breakdown into the QBR. Run a health assessment before preparing the QBR.
- `/customer-success:expansion-plan` — when the QBR reveals expansion opportunities in a healthy account, use this skill to build a detailed expansion plan.
