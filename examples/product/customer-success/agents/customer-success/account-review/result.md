# Account Review

Scenario: A CS manager needs to prepare for a QBR with an enterprise customer that has shown a significant usage drop over the past 6 weeks.

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

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's the full picture.

---

## The situation in plain terms

This account is in active decline. The 58% usage drop and the support silence happening simultaneously with Sarah's leave is not a coincidence — her team lost their internal owner and no one filled the gap. The new IT Director is a wildcard who has no relationship with you and every incentive to cut spend. You have 8 months to turn this around before a very uncomfortable renewal conversation.

---

## Before the QBR (this week — non-negotiable)

**1. Meet the IT Director now, not at the QBR.**
Book a 30-min intro call before next week. Find out their evaluation criteria, their timeline, and whether they have concerns already. Walking into the QBR as strangers is a mistake you can't undo.

**2. Find out who's covering Sarah's responsibilities.**
Her absence almost certainly caused the usage drop. Identify who her team reports to in her absence and get that person into the QBR as the interim champion.

**3. Confirm exec sponsor attendance — escalate if needed.**
They no-showed last time. With a spend review underway, you need leadership in the room. If your outreach hasn't worked, ask your VP/CRO to do a peer-to-peer ask.

**4. Call 2-3 users directly.**
Zero tickets in 45 days means something — you don't know what yet. Are they disengaged, routing issues to the IT Director, or genuinely fine? A 10-minute call gives you the answer. Don't go into the QBR without it.

**5. Pull team-level usage data.**
You need to know *which teams* went dark, not just the aggregate number. That tells you whether this is a Sarah problem (isolated) or a product problem (systemic).

---

## What the QBR itself should cover

The full document is at `hartwell-qbr-2026-q2.md`. The structure:

- **Open with honesty, not slides.** Acknowledge the usage drop directly before showing any data. It disarms defensiveness and signals that you're a partner, not a vendor.
- **Show the numbers plainly** — including the uncomfortable one: at 26% utilisation, they're paying ~$4,720/active user/year. The IT Director will find that. Find it first.
- **Focus on recovery, not expansion.** No upsell conversation in this meeting. Raising it with an At Risk account accelerates churn.
- **Leave with named owners on every commitment** — both yours and theirs. The two most important asks: name an interim champion within 2 weeks, and give you access to the team leads who went dark.

The key number to hit by end of Q3 is 175 active users (50% of seats). That's a defensible renewal story. 89 is not.

### Artifacts written

#### `work/hartwell-qbr-2026-q2.md`

```
# Quarterly Business Review: Hartwell Manufacturing

**Quarter:** Q2 2026  
**Prepared by:** [CSM Name]  
**Date:** 2026-05-01  
**QBR Date:** Week of 2026-05-05  
**Next QBR:** Q3 2026 (August)  
**Renewal:** January 2027 (8 months)

---

## Pre-QBR Action Plan (This Week)

These must happen **before** you walk into that room. The QBR itself cannot fix a relationship problem you haven't started addressing.

### 1. Get in front of the IT Director before the QBR (Priority: Critical)

Do not let the QBR be the first time you meet them. Book a 30-minute introductory call this week — frame it as "I want to make sure you have context on how your team uses [product] before we meet next week." Your goal: understand their evaluation criteria, surface any concerns they already have, and give them a reason to see you as a partner rather than a line item. If they're already skeptical, find out now.

**What to learn on that call:**
- What does success look like to them for software at this spend level?
- What's their timeline for the spend review?
- Are they aware of the QBR next week, and will they attend?

### 2. Identify who is covering Sarah Kowalski's responsibilities

Sarah's absence coincides exactly with the usage drop. This is almost certainly not a coincidence — her team lost their internal champion and no one filled that gap. Find out:
- Who is acting in her role, or who her team reports to while she's out?
- Did they hand off any active workflows or onboarding to a colleague?
- Can you get that person into the QBR?

Contact Sarah directly if appropriate — a short, warm message acknowledging her leave and letting her know you're supporting the team in her absence can preserve the relationship and give you an internal reference.

### 3. Confirm exec sponsor attendance — escalate if needed

The exec sponsor no-showed last QBR. With a renewal 8 months out and a spend review underway, this QBR needs executive coverage. If your standard outreach hasn't worked, escalate internally — ask your VP/CRO to reach out peer-to-peer. The message: "We want to make sure this review is worth your time and addresses what matters most at the leadership level."

### 4. Investigate the support silence

Zero tickets in 45 days after 8-12/month is not a health signal — it's a missing signal. Possibilities:
- Users stopped using the product (consistent with the usage drop)
- They're routing issues through the new IT Director instead of your support channel
- Sarah was the one filing tickets on behalf of the team

Before the QBR, call or email 2-3 users directly and ask how things are going. Don't make it a survey — make it a conversation. You need to know if there's a specific frustration that's gone unreported.

### 5. Pull the actual usage breakdown before you walk in

You know 89 of 340 seats are active. Before the QBR you need to know:
- Which teams/departments are those 89 users from?
- Which features are they using?
- Who were the 121 users who dropped off — what teams were they in?

This tells you whether the problem is isolated (Sarah's team stopped, others are fine) or systemic (the whole org is drifting). The answer changes your strategy significantly.

---

## QBR Document

### Executive Summary

Hartwell Manufacturing is currently **At Risk**. Active usage has dropped 58% over the past six weeks — from 210 to 89 users — coinciding with the departure of your primary champion, Sarah Kowalski, on maternity leave. Support activity has also stopped entirely, which combined with the usage decline suggests disengagement rather than self-sufficiency. With a renewal in 8 months and an IT Director currently reviewing software spend, the next 60 days are critical for stabilising this account.

This QBR will focus on three things: an honest accounting of where things stand, understanding what Hartwell needs to get value from the remaining licensed seats, and agreeing on a concrete recovery plan with clear ownership on both sides.

---

### Value Delivered — What We Know

> **Data gap:** Without goal commitments from the last QBR and without feature-level usage data pulled before this meeting, specific ROI quantification is not possible here. Fill this section from your analytics before the QBR. Do not fabricate numbers.

**Goals Scorecard** *(fill from last QBR commitments)*

| Goal | Target | Actual | Status | Notes |
|---|---|---|---|---|
| [Goal from last QBR] | [target metric] | [actual metric] | [Met / Partial / Missed] | |
| [Goal from last QBR] | [target metric] | [actual metric] | [Met / Partial / Missed] | |

**Usage Trends**

| Metric | 6 weeks ago | Today | Change |
|---|---|---|---|
| Active users (30-day) | 210 | 89 | **−58%** |
| Licensed seats utilised | 62% | 26% | **−36 pts** |
| Support tickets/month | 8–12 | 0 | **−100%** |
| [Feature adoption — pull from analytics] | | | |

**What the numbers mean:** At 26% seat utilisation on a $420k contract, Hartwell is paying approximately **$4,720 per active user per year**. An IT Director doing a spend review will find this number. You need to find it first and have a plan for it.

---

### Challenges and Honest Assessment

| Challenge | Business Impact | What Happened | Current Status |
|---|---|---|---|
| Champion on maternity leave | Loss of internal advocacy, team lost day-to-day owner | Sarah Kowalski, VP Operations, started leave 6 weeks ago | No interim champion identified |
| 58% usage drop | 121 users inactive; contract value-per-user has tripled | Coincides with Sarah's departure; root cause unconfirmed | Under investigation |
| New IT Director reviewing spend | Renewal at risk if they can't see ROI | Started 2 months ago, no relationship established | Pre-QBR intro call being scheduled |
| Support silence | Unreported issues may be compounding disengagement | Tickets dropped from 8-12/month to zero | Root cause unknown — needs direct outreach |
| Exec sponsor not present at last QBR | Reduced executive buy-in | [Reason, if known] | Escalating to confirm attendance this QBR |

---

### Health Overview

- **Composite score:** Critical / At Risk  
- **Trend:** Declining — rapid deterioration over past 6 weeks  
- **Key signals:**
  - Usage collapse (58% drop, 6 weeks)
  - Champion absence with no succession
  - Executive disengagement (sponsor no-show)
  - Support silence (ambiguous — needs investigation)

---

### Recommendations for Next Quarter

These are recovery-focused. Do not raise expansion in this meeting.

**Goals for Q3 2026**

| Goal | How Measured | Target | Owner | By When |
|---|---|---|---|---|
| Restore active user base | 30-day active users | 175 users (50% of licensed seats) | Joint — we provide enablement, they identify a champion | End of July |
| Identify and onboard interim champion | Named internal owner confirmed | 1 person committed, onboarded | Hartwell (we facilitate) | Within 2 weeks of QBR |
| Conduct team re-onboarding sessions | Sessions run, attendance tracked | [N] sessions covering the [X] teams that dropped off | Us | Within 30 days of QBR |
| Establish regular cadence with IT Director | Monthly check-in on calendar | First meeting completed | Us | Within 2 weeks of QBR |
| Clarify support channel usage | Tickets resuming or alternative channel confirmed | Agreed escalation path documented | Joint | Within 2 weeks of QBR |

**Specific actions we're committing to:**

1. **Usage audit delivered within 1 week.** We will send a team-by-team breakdown showing which users are active, which dropped off, and what features the active group is using. This gives the interim champion and IT Director a clear picture.

2. **Dedicated re-onboarding sessions.** Once we identify which teams went dark, we'll schedule 90-minute working sessions — not webinars — focused on specific workflows relevant to those teams. Target: within 30 days.

3. **Monthly check-ins for the next 3 months.** Standard QBR cadence is quarterly, but given the current situation we'll move to monthly touchpoints until usage is restored.

4. **Executive alignment call.** We'll ask our VP to join a call with Hartwell's exec sponsor before the next QBR to ensure leadership alignment on the renewal and the recovery plan.

**What we're asking from Hartwell:**

1. **Name an interim champion within 2 weeks.** This person doesn't need to replace Sarah — they just need to be the internal point of contact who can attend our monthly calls and help us reach the right people internally.

2. **Provide access to team leads in the departments that dropped off.** We need 30 minutes with each team lead to understand what changed. We'll set up those calls.

3. **Include IT Director in the monthly check-ins.** This protects the renewal conversation — if they're informed, they're not surprised.

---

### Opening the Conversation in the Room

Lead with this, not a slide deck:

> "Before we get into the data, I want to acknowledge something directly. Usage has dropped significantly over the past six weeks, and we haven't heard from your team on support in over a month. I don't think that means everything is fine — I think it means we lost momentum when Sarah went on leave, and we should have caught that sooner. This QBR is about understanding what happened, and agreeing on a concrete plan to get back on track."

Then go into the data. This posture — honest, not defensive, action-oriented — is what earns you the renewal conversation.

---

### Things Not to Do in This QBR

- **Don't lead with a product roadmap.** They don't need features, they need users back on the features they already have.
- **Don't mention expansion or upsell.** This account is not healthy enough for that conversation. Raising it now will damage trust.
- **Don't be surprised by the IT Director's questions.** If you haven't met them before the QBR, that's a problem (see pre-QBR actions). Walk in having already built that relationship.
- **Don't let the meeting end without named owners on every commitment.** Verbal agreements at QBRs evaporate. Every action needs a who and a when, written in the meeting.

---

### Appendix: Data to Pull Before the QBR

- [ ] Team-by-team active user breakdown (who dropped off, when)
- [ ] Feature adoption rates for active vs. lapsed users
- [ ] Support ticket history with resolution times and themes
- [ ] Goal commitments from last QBR
- [ ] NPS/CSAT scores if collected
- [ ] Contract details: exact renewal date, current tier, any past pricing discussions

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-01 |
| Target duration | 132267 ms |
| Target cost | $0.2037 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Identifies the health status as red or at-risk based on the signals — 57% usage drop, champion absence, new IT director reviewing spend, exec sponsor no-show | PASS | Artifact explicitly states 'Hartwell Manufacturing is currently **At Risk**' and 'Composite score: Critical / At Risk'. Chat opens with 'This account is in active decline.' All four signals are enumerated in the Challenges table. |
| c2 | Connects the usage drop to the champion's maternity leave (6 weeks aligns exactly) rather than treating it as a product problem | PASS | Chat: 'The 58% usage drop and the support silence happening simultaneously with Sarah's leave is not a coincidence — her team lost their internal owner.' Artifact: 'Sarah's absence coincides exactly with the usage drop. This is almost certainly not a coincidence.' |
| c3 | Flags the new IT director as a risk and recommends a strategy to identify and engage this stakeholder before the QBR | PASS | Chat action #1: 'Meet the IT Director now, not at the QBR. Book a 30-min intro call before next week.' Artifact has a dedicated section 'Get in front of the IT Director before the QBR (Priority: Critical)' with specific talking points for the call. |
| c4 | Does NOT recommend an expansion conversation — this account is unhealthy and expansion would be inappropriate per the CS agent's constraints | PASS | Chat: 'Focus on recovery, not expansion. No upsell conversation in this meeting.' Artifact: 'These are recovery-focused. Do not raise expansion in this meeting.' and under 'Things Not to Do': 'Don't mention expansion or upsell.' |
| c5 | Recommends specific pre-QBR actions: re-engaging day-to-day users, identifying who has backfilled Sarah's role, getting an exec sponsor confirmed before the meeting | PASS | Chat lists: (1) 'Call 2-3 users directly', (2) 'Find out who's covering Sarah's responsibilities', (3) 'Confirm exec sponsor attendance — escalate if needed'. All three actions also appear in the artifact's Pre-QBR Action Plan. |
| c6 | Frames the QBR agenda around value realised and risk mitigation — not a product demo or upsell | PASS | Artifact QBR structure covers 'Value Delivered — What We Know', 'Challenges and Honest Assessment', 'Recommendations for Next Quarter' (all recovery-focused). 'Things Not to Do' explicitly bans product roadmap and upsell discussions. |
| c7 | Recommends a health score review across all 5 dimensions — partial credit if health is assessed qualitatively but not scored across adoption/engagement/relationship/value/commercial dimensions | PARTIAL | Artifact's 'Health Overview' section gives a composite score ('Critical / At Risk') and lists key signals, but does not score across the five named dimensions individually. The Challenges table implicitly covers adoption (usage drop), engagement (support silence), and relationship (champion, IT director, exec sponsor) but commercial and value realisation are not distinctly scored. |
| c8 | Identifies the 8-month renewal timeline as creating urgency and recommends a recovery milestone before the renewal conversation | PASS | Chat: 'The key number to hit by end of Q3 is 175 active users (50% of seats). That's a defensible renewal story. 89 is not.' Artifact goal table: 'Restore active user base \| 175 users (50% of licensed seats) \| End of July' with renewal explicitly noted as 'January 2027 (8 months)'. |
| c9 | Output classifies Hartwell as RED / at-risk — explicitly naming all four signals (57% MAU drop 210→89, champion on leave, new IT director reviewing spend, exec sponsor no-show) as compounding evidence, not just one | PASS | Artifact executive summary explicitly states 'At Risk' and lists: '58% over the past six weeks — from 210 to 89 users', 'departure of your primary champion, Sarah Kowalski', 'IT Director currently reviewing software spend', and 'Exec sponsor not present at last QBR' in the Challenges table. |
| c10 | Output computes the actual usage drop numerically — "MAU dropped from 210 to 89, a 58% reduction" or similar — and connects the timing to the champion's 6-week leave (the drop and the leave align almost exactly) | PASS | Artifact usage table: 'Active users (30-day) \| 210 \| 89 \| **−58%**'. Artifact: 'Active usage has dropped 58% over the past six weeks — from 210 to 89 users — coinciding with the departure of your primary champion, Sarah Kowalski, on maternity leave.' |
| c11 | Output explicitly does NOT propose expansion or upsell — recognising the account is unhealthy, with the constraint that expansion only follows healthy accounts | PASS | Chat: 'No upsell conversation in this meeting. Raising it with an At Risk account accelerates churn.' Artifact: 'Do not raise expansion in this meeting' and 'Don't mention expansion or upsell. This account is not healthy enough for that conversation. Raising it now will damage trust.' |
| c12 | Output names the new IT director as a critical risk and proposes a specific pre-QBR action — identifying the IT director by name, requesting a 1:1 introduction before the QBR, demonstrating value to that stakeholder | PASS | The IT director is unnamed in the prompt (no name given), so naming them is not possible. The output does mark this 'Priority: Critical', proposes a '30-minute introductory call this week', and specifies demonstrating value by understanding 'their evaluation criteria, their timeline' — meeting all achievable elements of this criterion. |
| c13 | Output proposes finding Sarah Kowalski's interim coverage — who's running operations in her absence, and getting that person engaged as a temporary champion | PASS | Chat: 'Find out who's covering Sarah's responsibilities' and 'Get that person into the QBR as the interim champion.' Artifact: 'Identify who is covering Sarah Kowalski's responsibilities' section asks 'Who is acting in her role?' and 'Can you get that person into the QBR?' Artifact goal: 'Identify and onboard interim champion'. |
| c14 | Output's pre-QBR action list is concrete with timing — e.g. "this week: identify IT director and request 1:1; week before QBR: confirm exec sponsor attendance; day before: send pre-read with usage analysis" | PASS | Chat labels the entire pre-QBR section 'this week — non-negotiable'. Artifact header: 'These must happen **before** you walk into that room.' Actions include booking IT director call 'this week', confirming exec sponsor, calling users before QBR. The 'e.g.' in the criterion indicates example timing structure, not a rigid requirement. |
| c15 | Output's QBR agenda is structured around value realised + risk mitigation — NOT product demos or new features — with sections like "Value to date" (from the previous 16-month period), "What changed in the last 6 weeks", "Path to renewal in 8 months" | PASS | Artifact QBR sections: 'Value Delivered — What We Know' (includes goals scorecard), 'Challenges and Honest Assessment' (covers what changed in last 6 weeks), 'Recommendations for Next Quarter' (recovery path with renewal as explicit anchor). No product demo or roadmap section present. |
| c16 | Output addresses the 8-month renewal as creating urgency — proposing a 90-day recovery milestone (e.g. "MAU restored to ~150 by end of Q2") so the renewal conversation in month 8 can happen from a position of strength | PASS | Chat: 'The key number to hit by end of Q3 is 175 active users... That's a defensible renewal story.' Artifact goal: '175 users (50% of licensed seats) \| End of July' — QBR is May 2026, End of July is ~90 days. Renewal January 2027 explicitly noted as the horizon. |
| c17 | Output addresses the dropped support tickets (8-12/month → 0 in 45 days) as a SILENT-departure signal, not "they figured it out" — explaining that customers stop logging tickets when they stop using the product | PASS | Artifact: 'Zero tickets in 45 days after 8-12/month is not a health signal — it's a missing signal.' First listed possibility: 'Users stopped using the product (consistent with the usage drop).' Chat: 'Zero tickets in 45 days means something... Are they disengaged...?' |
| c18 | Output performs a qualitative health assessment across the 5 dimensions (adoption, engagement, relationship, value realisation, commercial) — partial credit if assessed without explicit scoring | PARTIAL | Dimensions covered qualitatively but not labeled: adoption (58% usage drop), engagement (support silence), relationship (champion absent, IT director new, exec sponsor no-show), commercial (spend review, 8-month renewal). Value realisation is implied via the $4,720/active-user calculation. No explicit 5-dimension framework used. |

### Notes

The output is exceptionally strong across all criteria. The chat response and the written artifact (hartwell-qbr-2026-q2.md) together cover every required element: at-risk classification with all four compounding signals, explicit numerical computation of the 58% usage drop tied to Sarah's 6-week absence, a pre-QBR action plan framed as 'this week — non-negotiable', firm prohibition on expansion/upsell, a 90-day recovery milestone (175 users by end of July), and treatment of support silence as a departure signal rather than self-sufficiency. The only gaps are: the health dimensions (c7, c18) aren't broken into the canonical five-dimension framework — the assessment is holistic rather than structured across adoption/engagement/relationship/value/commercial explicitly. Both criteria with PARTIAL ceilings receive PARTIAL credit, and no PASS-ceiling criteria were missed.
