# Account review

A CS manager needs to prepare for a QBR with an enterprise customer that has shown a significant usage drop over the past 6 weeks.

## Prompt

> I need to prep for a QBR with Hartwell Manufacturing next week. They're one of our largest accounts — $420k ARR, 3-year contract, renewal comes up in 8 months.
>
> Here's what I know:
> - They have 340 licensed seats, but only 89 active users in the last 30 days (was 210 six weeks ago)
> - Their champion, Sarah Kowalski (VP of Operations), went on maternity leave 6 weeks ago
> - A new IT director started 2 months ago and has been "reviewing all software spend"
> - They haven't logged a support ticket in 45 days (they used to log 8-12/month)
> - They attended our last QBR but the exec sponsor didn't show up
>
> What should I be doing, and what should this QBR cover?

Hartwell is in serious trouble. The 57% usage drop lines up exactly with Sarah's maternity leave six weeks ago — this is a relationship and continuity problem, not a product problem. Zero support tickets for 45 days is not a satisfaction signal; it's a silence signal. They've stopped engaging entirely.

## Output

**Health status: At Risk / Critical**

Scoring across the five dimensions with available data:
- Product adoption (30%): 89/340 active seats = 26% utilisation — severely low
- Engagement (25%): Zero support tickets, declining contact — disengaged
- Relationship (20%): Champion absent, exec sponsor no-show at last QBR — weak
- Value realisation (15%): Unknown without further data, but usage drop suggests value delivery has stalled
- Commercial (10%): 8 months to renewal, new IT director reviewing all spend — elevated risk

Composite health: below 40 on current signals — Critical range.

**Do not attempt an expansion conversation.** The agent definition is explicit on this: "Proposing an upsell to an unhealthy customer accelerates churn." Expansion conversations only happen after the customer is demonstrably succeeding.

**Pre-QBR actions (this week):**

1. Find out who is covering Sarah's responsibilities. Email her EA or direct reports today. You need a named operational contact before the QBR — going in without one is going in blind.
2. Request a pre-QBR introductory call with the new IT director. Frame it as aligning on how the platform fits their infrastructure review, not a sales call. This is your biggest risk right now — an IT director reviewing software spend without knowing the platform's value is a churn accelerator.
3. Confirm exec sponsor attendance. If they skipped the last QBR, email is insufficient — call or get your AE to call. A $420k renewal without exec presence at the QBR is a serious gap.
4. Pull usage data on the 89 active users. Who are they, which teams, what are they doing? Talk to two or three of them before the meeting. You need at least one outcome story to lead with.

**QBR agenda:**

Open with what Hartwell has achieved in their own terms — operational outcomes, cost savings, time savings — not feature stats. Acknowledge the usage decline directly and attribute it to the champion transition, not a product failing. Present a recovery plan with milestones. Do not demo the product. Do not raise expansion.

Structure:
1. Executive summary — health status, honest acknowledgment of usage drop
2. Value delivered — what the 89 active users have achieved, quantified if possible
3. The champion transition — what happened, what you're doing to support continuity
4. Recovery plan — specific milestones for returning to 210+ active users by a stated date
5. Renewal horizon — note the 8-month timeline, commit to a health milestone review at the 4-month mark

**Renewal milestone:** With 8 months to renewal, set a recovery checkpoint at 4 months out. If adoption is not back to ≥60% by then, the renewal conversation will be difficult regardless of what happens in this QBR. Set the milestone in writing at the meeting.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Identifies health as at-risk or critical — the agent definition's health framework has explicit numeric thresholds: Critical = 0–39, At Risk = 40–59. The agent's Churn Risk Indicators table flags "Champion/sponsor left" as High risk and "Usage declining over 2+ weeks" as Medium. With adoption at 26% of licensed seats and a departed champion, the composite falls in the Critical range. The definition drives this classification through the health scoring framework and churn signal table.
- [x] PASS: Connects usage drop to champion departure — the agent definition's Churn Risk Indicators table explicitly calls out "Champion/sponsor left the company" as a High risk requiring "Identify new sponsor immediately." The six-week alignment between Sarah's leave and the usage drop is the direct evidence. The agent definition trains toward relationship and continuity analysis before assuming product problems, and the Expansion Principles section reinforces that health issues require diagnosis, not quick fixes.
- [x] PASS: Flags IT director as risk and recommends engagement — the agent definition's Churn Risk Indicators table includes "Competitor evaluation signals" as Critical and commercial signals as requiring immediate action. A new IT director reviewing all software spend maps to the commercial risk category. The agent's Renewal Management section requires proactive action starting 120 days before renewal. The simulation recommends a pre-QBR call with the IT director with specific framing guidance.
- [x] PASS: Does not recommend expansion — the agent definition states "Only propose expansion when the customer is already getting value. Trying to upsell an unhealthy customer accelerates churn" and "Expansion conversations only happen after the customer is demonstrably succeeding." The "What You Don't Do" section reinforces this. The simulation explicitly states "Do not attempt an expansion conversation" and explains why.
- [x] PASS: Specific pre-QBR actions — the simulation recommends four concrete actions: find who is covering Sarah's role, pre-QBR call with the IT director, exec sponsor confirmation call, pull and analyse usage data for the 89 active users. These align with the agent's relationship monitoring guidance (champion backfill identification) and renewal management section (120-day proactive engagement).
- [x] PASS: QBR framed around value and risk mitigation — the agent definition's write-qbr skill (referenced in the Pre-Flight section as context) requires QBRs to lead with value delivered, acknowledge challenges, and exclude expansion for At Risk accounts. The simulation's QBR agenda leads with value, addresses the usage decline directly, and excludes product demo and expansion.
- [~] PARTIAL: Health score across all 5 dimensions — the agent has the 5-dimension framework with weights and scoring criteria. The simulation qualitatively assesses all five dimensions with evidence, but does not produce a numeric composite score due to insufficient data. The criterion ceiling is PARTIAL — partial credit is appropriate because the framework is applied qualitatively, not fully numerically.
- [x] PASS: 8-month renewal timeline flagged as urgency driver — the agent's Renewal Management table requires action starting at 120 days before renewal. 8 months (≈240 days) means the agent correctly flags this as approaching the proactive engagement window and recommends a 4-month recovery checkpoint as a milestone before the renewal conversation.

### Notes

The agent definition's hard gate on expansion for unhealthy accounts is the most important constraint here — it prevents the instinct to "upsell toward a better renewal number" on an account already at risk. The silence signal observation (zero support tickets after 8-12/month) is the right interpretation: it signals disengagement, not satisfaction. The definition supports this reading through the Churn Risk Indicators table ("Engagement drop: fewer logins, stopped attending meetings, unresponsive"). The PARTIAL on health scoring reflects a data availability constraint, not a definition gap — the framework is present and correctly applied qualitatively.
