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

# Churn Analysis: Hartwell Manufacturing

## Risk Summary
- **Churn probability:** HIGH
- **Risk score:** 16/18
- **ARR at risk:** $420,000
- **Time to action:** URGENT — this week before QBR

---

## Active Signals

| Signal | Severity | Evidence | Duration |
|---|---|---|---|
| **Usage collapse** | Critical | 58% decline (210 → 89 active users) | 6 weeks, ongoing |
| **Support radio silence** | Critical | Zero tickets in 45 days vs 8-12/month baseline | 45 days |
| **Champion departure** | High | Sarah Kowalski (VP Ops) on maternity leave | 6 weeks |
| **Relationship deterioration** | High | Exec sponsor no-show at last QBR | ~4 weeks |
| **Procurement scrutiny** | High | New IT director initiated software spend review | 2 months |
| **No replacement advocate** | High | Sarah's absence not covered; no identified champion | 6 weeks ongoing |

---

## Timeline

| Date | Event | Significance |
|---|---|---|
| Early March (2 months ago) | New IT director started, began software spend review | Procurement entered decision-making; budget pressure signal |
| Mid-March (6 weeks ago) | Sarah Kowalski went on maternity leave | **Inflection point: active users dropped from 210 → 89 days later** |
| Mid-March (6 weeks ago) | Last support ticket logged | Account went silent; disengagement or active evaluation |
| ~4 weeks ago | Last QBR; exec sponsor didn't attend | Executive priority dropped; disengagement confirmed |
| Now | QBR scheduled for next week | Window to intervene before renewal cycle decision-making hardens |

---

## Root Cause

**Primary: Relationship failure + Internal organizational change**

- **Relationship failure**: Sarah Kowalski was the driver and internal advocate. Her departure left a vacuum. The 58% usage drop six weeks ago correlates precisely with her maternity leave — the product isn't self-defending without a champion inside.
- **Internal organizational change**: New IT director's spend review shifted decision-making from operations (Sarah's lens: "does this work for us?") to procurement (IT director's lens: "what does this cost?"). This is a cost-cutting exercise, not a product evaluation.

**Contributing factors:**
- No coverage plan for Sarah's absence (product adoption depends on her advocacy, but there's no backup)
- Executive sponsor disengagement (didn't attend QBR) — signals low priority on their side
- No proactive engagement from your team during the transition (silent for 6 weeks)

**Addressable: YES — but only through direct relationship-building**

You cannot fix Sarah's maternity leave. You can rebuild the relationship with the new IT director and help him understand the true business value (outcomes, not just cost).

---

## Risk Scoring

| Factor | Score | Evidence |
|---|---|---|
| **Usage trend** | 3 | 58% decline, 6 weeks, ongoing → severe |
| **Engagement** | 3 | Zero support tickets, exec no-show, unresponsive → critical disengagement |
| **Sponsor status** | 3 | Champion absent, new IT director with cost-cutting mandate, no identified replacement → no advocate |
| **Value realisation** | 3 | Unknown if stated goals are being met; silence suggests either stopped using or stopped caring → risk |
| **Contract timeline** | 2 | 8 months to renewal → medium-term, but procurement will start positioning in 4–6 months |
| **Competitive activity** | 2 | Spend review signals evaluation mode; no named competitor yet, but spend reviews usually precede competitive RFPs |
| **TOTAL** | **16** | **HIGH RISK: Urgent intervention required** |

---

## What's Actually Happening

Read between the lines:

1. **Sarah was the product owner internally.** She drove adoption, attended your QBRs, filed support tickets. Without her, the organisation didn't know how to use the product.

2. **The new IT director doesn't understand the business value.** His mandate is "reduce software spend." He's seeing 340 licensed seats, 89 active users, and thinking "$420k for 26% utilisation = cut this first."

3. **Your team didn't fill the gap.** For 6 weeks, nobody from your company reached out to understand what happened. Silence = abandonment from the customer's perspective.

4. **The renewal is winnable, but not if you treat the QBR as a product demo.** The IT director needs to understand business outcomes, not feature tours.

---

## Intervention Plan

### BEFORE the QBR (this week — within 48 hours)

| Action | Owner | Timeline | Success criteria |
|---|---|---|---|
| **Call the new IT director (not Sarah)** | You | By Wednesday 2026-05-07 | He agrees to 30-min call before QBR. You learn: (1) what "software spend review" found, (2) who his primary stakeholder is, (3) what success looks like to him |
| **Understand what happened during Sarah's absence** | Account manager | By Wednesday | Reach Sarah's cover or a peer to learn: did usage drop because people didn't know how to use it, or did they leave intentionally? |
| **Map new decision-makers** | You | By Thursday | Identify: (1) who replaced Sarah in day-to-day operations, (2) who the CFO/budget holder is, (3) who the exec sponsor really is now |
| **Prepare a value-focused QBR agenda** | You | By Friday | The QBR is NOT a product demo. It's a business conversation: outcomes you've delivered, business metrics tied to your product, obstacles removing from their path. The IT director needs to see ROI, not features. |

### AT the QBR (next week)

**Attendees YOU should prepare for:**
- New IT director (the actual decision-maker now)
- Someone from operations (to bridge from Sarah's absence)
- Possibly the exec sponsor (only if you can get him to commit to attending)
- Sarah, if she's able to call in (but don't rely on it)

**The QBR agenda should be:**
1. **Business outcomes** — what did Hartwell achieve with your product in the last year? Quantify: cost saved, time reclaimed, revenue impact, risk reduced. (You'll need to dig into this — don't assume you know.)
2. **Why usage dropped** — ask directly and listen. "We noticed active users are at 89 vs 210 six weeks ago. Walk us through what changed." (It's probably: Sarah left, nobody knew how to use it, so they stopped.)
3. **Value the IT director can defend** — reframe from "software cost" to "operational capability." "This product saves your operations team 15 hours/week. At your loaded labor cost, that's $X annually." Give him a number he can put in his business case.
4. **Obstacles we can remove** — ask what's in their way. Maybe they need training, maybe the product isn't integrated with their stack, maybe the pricing model doesn't match their org structure now. Listen.
5. **Renewal planning** — make clear: "We want to support you through this transition. We're flexible on structure (price, seats, terms) as long as we're creating value together. What would make sense for you?"

**Do NOT:**
- Lead with discounts or price haggling (that signals the product isn't valuable, just expensive)
- Demo new features (they don't care right now; they care about value they're already paying for)
- Assume Sarah will be the advocate (she's on leave; plan without her)
- Pretend everything is fine (they know usage dropped; acknowledge it directly)

---

## Retention Economics

| Metric | Value | Context |
|---|---|---|
| **ARR at risk** | $420,000 | Full annual contract amount |
| **Replacement cost** | $2.1M–$2.9M | 5–7x cost to acquire equivalent revenue |
| **Intervention cost** | ~10 hours (your time) | Low |
| **ROI if retained** | 200–250x | Every hour spent now saves $40k–$50k in replacement cost |
| **Worst case (churn)** | $420k lost + 15–18 months to replace | Significant impact on quota + team credibility |

---

## Checkpoint

- **Review date:** May 14 (day after QBR)
- **Success indicators after QBR:**
  - IT director agrees to work together on transition plan
  - Usage stops declining (stabilises or shows early recovery)
  - Decision to renew made within 30 days (vs silence through summer)
  - New champion or co-champion identified (shared ownership between ops and IT)
- **Escalation trigger:**
  - IT director requests pricing reduction >20% or threatens to start RFP
  - Usage continues declining after QBR
  - Executive sponsor still won't engage after direct outreach

---

## What You Should Do RIGHT NOW

1. **Call the new IT director today.** Not the exec sponsor, not Sarah's cover. The decision-maker. Say something like: "Martin here — I wanted to check in before next week's QBR. Your team went through a software spend review recently. I'd like to understand what you found and make sure the QBR is valuable for you. Can we grab 30 minutes this week?"

   **Why:** You need to understand his lens before you walk into the room. If he's already decided to cut, you need to hear that and adjust. If he's open but confused about value, you can fix that.

2. **Do a quiet recon on Sarah's absence coverage.** Find out: Is someone covering her role? Who's running operations day-to-day? They're your new internal champion. Build the relationship now.

3. **Pull together the value story.** What has Hartwell actually achieved with your product? Find a measurable outcome (cost saved, efficiency gain, revenue impact, risk mitigated). You'll need this in the QBR.

4. **Prepare to be flexible on structure.** You might need to offer: different pricing model (per-user instead of per-seat), lower cost for the renewal, training investment, integration work, or different contract terms. Don't pre-decide what you can't move on — wait until you understand what matters to them.

The QBR next week is your intervention point. If you walk in without doing this prep, you'll be answering questions defensively instead of leading with value. And at this risk level, passive doesn't work.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-04 |
| Target duration | 57860 ms |
| Target cost | $0.0669 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Identifies the health status as red or at-risk based on the signals — 57% usage drop, champion absence, new IT director reviewing spend, exec sponsor no-show | PASS | Risk Summary table shows 'Churn probability: HIGH', 'Risk score: 16/18'. Active Signals table explicitly lists all four: '58% decline (210 → 89 active users)', 'Sarah Kowalski (VP Ops) on maternity leave', 'New IT director initiated software spend review', 'Exec sponsor no-show at last QBR'. |
| c2 | Connects the usage drop to the champion's maternity leave (6 weeks aligns exactly) rather than treating it as a product problem | PASS | Root Cause section: 'The 58% usage drop six weeks ago correlates precisely with her maternity leave — the product isn't self-defending without a champion inside.' Timeline also marks the inflection point: 'Mid-March (6 weeks ago) Sarah Kowalski went on maternity leave — Inflection point: active users dropped from 210 → 89 days later'. |
| c3 | Flags the new IT director as a risk and recommends a strategy to identify and engage this stakeholder before the QBR | PASS | Active Signals lists 'Procurement scrutiny: High'. Pre-QBR intervention: 'Call the new IT director (not Sarah) — By Wednesday 2026-05-07'. 'What You Should Do RIGHT NOW' opens with 'Call the new IT director today' and provides a specific call script. |
| c4 | Does NOT recommend an expansion conversation — this account is unhealthy and expansion would be inappropriate per the CS agent's constraints | PASS | No expansion or upsell recommendation anywhere in the output. QBR agenda explicitly says 'Do NOT: Lead with discounts or price haggling... Demo new features.' Retention economics focuses entirely on retaining existing $420k ARR, not growing it. |
| c5 | Recommends specific pre-QBR actions: re-engaging day-to-day users, identifying who has backfilled Sarah's role, getting an exec sponsor confirmed before the meeting | PASS | Intervention Plan table includes: 'Understand what happened during Sarah's absence — Reach Sarah's cover or a peer' and 'Map new decision-makers — Identify: (1) who replaced Sarah in day-to-day operations'. 'What You Should Do RIGHT NOW' item 2: 'Do a quiet recon on Sarah's absence coverage. Find out: Is someone covering her role? Who's running operations day-to-day?' |
| c6 | Frames the QBR agenda around value realised and risk mitigation — not a product demo or upsell | PASS | QBR agenda items: (1) Business outcomes, (2) Why usage dropped, (3) Value the IT director can defend, (4) Obstacles we can remove, (5) Renewal planning. Explicit 'Do NOT' list includes 'Demo new features'. Narrative: 'the QBR is NOT a product demo. It's a business conversation: outcomes you've delivered, business metrics tied to your product'. |
| c7 | Recommends a health score review across all 5 dimensions — partial credit if health is assessed qualitatively but not scored across adoption/engagement/relationship/value/commercial dimensions | PARTIAL | Risk Scoring table covers usage trend (≈adoption: 3), engagement (3), sponsor status (≈relationship: 3), value realisation (3), contract timeline (≈commercial: 2), competitive activity (2). Not labelled as the canonical 5-dimension framework (adoption/engagement/relationship/value/commercial) but functionally maps to all five. |
| c8 | Identifies the 8-month renewal timeline as creating urgency and recommends a recovery milestone before the renewal conversation | PASS | Risk Scoring: 'Contract timeline: 2 — 8 months to renewal → medium-term, but procurement will start positioning in 4–6 months'. Checkpoint section sets 'Review date: May 14 (day after QBR)' with success indicators. QBR agenda item 5 is 'Renewal planning' with explicit language about the path forward. |
| c9 | Output classifies Hartwell as RED / at-risk — explicitly naming all four signals (57% MAU drop 210→89, champion on leave, new IT director reviewing spend, exec sponsor no-show) as compounding evidence, not just one | PASS | Active Signals table enumerates all four explicitly: '58% decline (210 → 89 active users)', 'Sarah Kowalski (VP Ops) on maternity leave', 'New IT director initiated software spend review', 'Exec sponsor no-show at last QBR'. Risk Summary: 'Churn probability: HIGH', 'Risk score: 16/18'. |
| c10 | Output computes the actual usage drop numerically — 'MAU dropped from 210 to 89, a 58% reduction' or similar — and connects the timing to the champion's 6-week leave (the drop and the leave align almost exactly) | PASS | Active Signals: '58% decline (210 → 89 active users)'. Root Cause: 'The 58% usage drop six weeks ago correlates precisely with her maternity leave'. Timeline explicitly links both events to 'Mid-March (6 weeks ago)'. |
| c11 | Output explicitly does NOT propose expansion or upsell — recognising the account is unhealthy, with the constraint that expansion only follows healthy accounts | PASS | No upsell or expansion recommendation appears anywhere. Retention Economics section focuses entirely on retaining existing ARR. QBR agenda 'Do NOT' list excludes feature demos and price haggling. The entire framing is retention-oriented. |
| c12 | Output names the new IT director as a critical risk and proposes a specific pre-QBR action — identifying the IT director by name, requesting a 1:1 introduction before the QBR, demonstrating value to that stakeholder | PASS | Active Signals flags IT director as 'High' severity. Pre-QBR action: 'Call the new IT director (not Sarah) — By Wednesday 2026-05-07 — He agrees to 30-min call before QBR'. Call script provided. Value demonstration framing: 'reframe from software cost to operational capability… Give him a number he can put in his business case.' (No name given in input, so no name available to cite.) |
| c13 | Output proposes finding Sarah Kowalski's interim coverage — who's running operations in her absence, and getting that person engaged as a temporary champion | PASS | 'Understand what happened during Sarah's absence — Reach Sarah's cover or a peer' and 'Map new decision-makers — Identify: (1) who replaced Sarah in day-to-day operations'. 'What You Should Do RIGHT NOW' item 2: 'Who's running operations day-to-day? They're your new internal champion. Build the relationship now.' |
| c14 | Output's pre-QBR action list is concrete with timing — e.g. 'this week: identify IT director and request 1:1; week before QBR: confirm exec sponsor attendance; day before: send pre-read with usage analysis' | PASS | Intervention Plan table has specific dates: IT director call by Wednesday 2026-05-07, Sarah's absence coverage by Wednesday, decision-maker mapping by Thursday, QBR agenda prepared by Friday. Concrete owners and success criteria per action. |
| c15 | Output's QBR agenda is structured around value realised + risk mitigation — NOT product demos or new features — with sections like 'Value to date' (from the previous 16-month period), 'What changed in the last 6 weeks', 'Path to renewal in 8 months' | PASS | QBR agenda: (1) Business outcomes — quantified value, (2) Why usage dropped — directly maps to 'what changed in last 6 weeks', (3) Value the IT director can defend, (4) Obstacles we can remove, (5) Renewal planning — maps to 'path to renewal in 8 months'. Explicit 'Do NOT: Demo new features'. |
| c16 | Output addresses the 8-month renewal as creating urgency — proposing a 90-day recovery milestone (e.g. 'MAU restored to ~150 by end of Q2') so the renewal conversation in month 8 can happen from a position of strength | PARTIAL | Urgency is addressed ('procurement will start positioning in 4–6 months') and Checkpoint section sets a May 14 review date with success indicators including 'Usage stops declining (stabilises or shows early recovery)'. However, no specific numeric recovery milestone is proposed (e.g. 'MAU restored to ~150 by end of Q2'). The 30-day decision target is about closing renewal, not a recovery precondition. |
| c17 | Output addresses the dropped support tickets (8-12/month → 0 in 45 days) as a SILENT-departure signal, not 'they figured it out' — explaining that customers stop logging tickets when they stop using the product | PARTIAL | Active Signals labels it 'Support radio silence: Critical — Zero tickets in 45 days vs 8-12/month baseline'. Timeline: 'Account went silent; disengagement or active evaluation' — correctly treating it as disengagement, not self-sufficiency. However, the specific mechanism ('customers stop logging tickets when they stop using the product') is not explicitly stated; it's implied via the champion-absence narrative. |
| c18 | Output performs a qualitative health assessment across the 5 dimensions (adoption, engagement, relationship, value realisation, commercial) — partial credit if assessed without explicit scoring | PARTIAL | Risk Scoring table covers usage trend (adoption), engagement, sponsor status (relationship), value realisation, and contract timeline (commercial) with a 1–3 numeric scale. All five functional dimensions are present, though the framework is labelled as 'Risk Scoring' rather than the canonical 5-dimension health model. |

### Notes

The output is a thorough, well-structured churn intervention plan that hits nearly every criterion. It correctly classifies the account as high-risk, connects the usage drop precisely to the champion's maternity leave, flags the IT director as the emergent decision-maker, rules out expansion, and frames the QBR entirely around value and retention. The two PARTIAL scores on PASS-ceiling criteria reflect genuine gaps: c16 identifies urgency around the 8-month window but never proposes a specific numeric recovery milestone (e.g. 'restore MAU to ~150 by end of Q2') that would set up the renewal from strength; c17 correctly reads the ticket silence as disengagement but doesn't explicitly articulate the mechanism that customers who stop using a product stop filing tickets. Both gaps are minor omissions in an otherwise exceptional response. The two PARTIAL-ceiling criteria (c7, c18) are both awarded PARTIAL as the health assessment covers all five functional dimensions under a different label.
