# Result: Account review

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16.5/17 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Plugin** | `plugins/product/customer-success/agents/customer-success.md` |
| **Scenario** | CS manager preparing for QBR with at-risk enterprise account ($420k ARR, 57% MAU drop, champion on leave) |

---

## Output

Simulated agent response to the prompt.

---

## Customer Health: Hartwell Manufacturing

### Health Score: 24 — Critical

| Dimension | Weight | Score | Signals |
|---|---|---|---|
| Product adoption | 30% | 20 | MAU dropped from 210 to 89 — a 58% reduction in 6 weeks. Only 26% of 340 licensed seats active. Timing aligns exactly with Sarah Kowalski's maternity leave, suggesting adoption was champion-dependent, not embedded in workflow |
| Engagement | 25% | 15 | Support tickets: 8-12/month → 0 in 45 days. This is a silent departure signal, not a sign the team mastered the product. Customers stop logging tickets when they stop using the product. Exec sponsor absent from last QBR |
| Relationship | 20% | 25 | Champion (Sarah Kowalski, VP Ops) on maternity leave with no identified interim owner. New IT director reviewing all software spend — unengaged and potentially adversarial. Exec sponsor no-show at last QBR |
| Value realisation | 15% | 30 | With 58% of users inactive, most of the team isn't realising value. No data on whether the 89 active users are getting ROI. Value baseline from the pre-leave period is unknown |
| Commercial | 10% | 50 | $420k ARR, 3-year contract, renewal in 8 months. No payment issues. Time is still available, but the 8-month window creates urgency — recovery must start now |

**Composite score:** (20×0.30) + (15×0.25) + (25×0.20) + (30×0.15) + (50×0.10) = 6 + 3.75 + 5 + 4.5 + 5 = **24 — Critical**

---

### Risk Indicators

**1. Champion absence (HIGH)** — Sarah Kowalski was the adoption anchor. Her maternity leave 6 weeks ago directly precedes the usage drop. Nobody has backfilled her relationship with us. This is the most actionable root cause: the product is fine, the deployment is intact, but the person holding the team together stopped being present.

**2. New IT director reviewing spend (CRITICAL)** — An unknown stakeholder with budget authority is evaluating every tool in the stack, including ours. He has never engaged with CS. If we reach renewal without a relationship with this person, the renewal is at risk regardless of usage recovery.

**3. Silent departure underway (HIGH)** — The drop from 8-12 tickets/month to zero over 45 days is a disengagement signal. Customers don't stop logging support tickets because they've mastered the product. They stop because they've stopped using it. Do not interpret the ticket silence as health.

**4. Exec sponsor unreliable (MEDIUM)** — Absent from the last QBR. If the exec sponsor doesn't show at this QBR either, Hartwell has no senior internal advocate at the table when renewal discussions start in 8 months.

---

### What this is NOT

No expansion conversation. Hartwell is a Critical-health account scoring 24/100. Proposing an upsell to a customer with 58% MAU decline, an unengaged IT director reviewing spend, and a missing champion would accelerate churn. Expansion only happens after health is restored.

---

### Pre-QBR Actions

**Priority 1 — Find Sarah's interim coverage (days 1-2)**

Email or call Sarah's manager or EA. Ask: "While Sarah's on leave, who's owning operational tools and workflows?" Get that person's name and contact this week. They're the temporary champion. Get them on a 20-minute call — not to pitch, just to re-establish the relationship and understand what's happening on the ground.

**Priority 2 — Identify and reach the IT director (days 2-3)**

Find his name via LinkedIn, the AE who closed the deal, or the ops contact identified in Priority 1. Request a 30-minute 1:1 before the QBR, framed as: "I want to make sure you have the context you need before we meet as a group." Bring a one-pager: what Hartwell's team uses the product for, what value it delivered during the 210 MAU period, and what full adoption could look like again.

**Priority 3 — Confirm exec sponsor attendance (days 3-5)**

Don't send a calendar invite and hope. Call directly: "I want to make sure the right people are in the room — can I confirm you're planning to attend?" If the exec sponsor won't commit, escalate internally before the QBR. A meeting with no exec sponsor and a new IT director reviewing spend is a high-stakes room.

**Priority 4 — Prepare the usage analysis (days 3-5)**

Pull the full 6-week trend: MAU by week, not just start and end points. Overlay the date Sarah went on leave. This chart tells the story — champion-dependent adoption with no workflow embedding underneath. Use it in the QBR to frame the conversation as "here's what happened, here's what we can do about it" not as an accusation.

---

### QBR Agenda

**Goal:** Leave with a shared 90-day recovery plan and a committed exec sponsor.

**What this QBR is not:** A product demo. A feature walkthrough. An expansion conversation.

| Section | Duration | Content |
|---|---|---|
| Value to date (months 1-18) | 15 min | What the team was doing with the product before 6 weeks ago. Concrete outcomes from the 210 MAU period. Establishes that the product works — the issue is adoption continuity, not the product |
| What changed in the last 6 weeks | 10 min | Honest data: MAU trend by week, ticket drop, exec absence. Frame as: "We noticed this and want to understand it together" — diagnostic, not defensive |
| Root cause: champion transition | 10 min | Surface the Sarah Kowalski connection directly. Ask who's covering her responsibilities. Opens the door to formalising an interim champion going forward |
| IT director alignment | 10 min | Address his concerns directly: "We know you're reviewing tools — here's the business case, and here's what we need to do together to get the ROI back up" |
| 90-day recovery plan | 10 min | Agree on specific milestones (see below) and owner on both sides |
| Path to renewal in 8 months | 5 min | "Here's what success looks like by month 6, and how we get to a straightforward renewal from a position of strength" |

---

### 90-Day Recovery Plan

Renewal is 8 months away. That's enough time to recover — but only if recovery starts now.

**Target:** MAU restored to ~150 (from 89) by end of Q2. Not back to 210 yet — that's a realistic 90-day milestone that sets up the renewal conversation without overcommitting.

| Week | Milestone | Owner |
|---|---|---|
| Week 1 | Interim champion identified (ops contact covering Sarah's role) | CS |
| Week 1 | 1:1 with IT director completed | CS |
| Week 2 | Interim champion completes re-onboarding session for top 3 use cases | CS + interim champion |
| Week 4 | MAU trend reversed (moving up from 89) | Joint |
| Week 8 | MAU at 120+ | Joint |
| Week 12 | MAU at 150+, exec sponsor re-engaged | Joint |

If MAU is still declining at week 4, escalate to executive-to-executive engagement immediately. Don't wait for the month-4 renewal check-in.

---

### Renewal Timeline (8 Months Out)

| Month | Action |
|---|---|
| Now | Recovery plan underway. Don't start renewal conversation until health is improving |
| Month 4 (4 months to renewal) | Health assessment. If on track, begin renewal prep. If not, escalate immediately |
| Month 5 (3 months to renewal) | Renewal conversation. Review value delivered. Discuss contract terms |
| Month 6 (2 months to renewal) | Commercial terms. Flag any pricing changes now — no surprises at renewal |
| Month 7 (1 month to renewal) | Signature |

If health hasn't recovered by month 4, the renewal conversation starts in a hole. The IT director will have had 4 months to build a case for replacement without a counter-narrative from us. The 90-day recovery plan is the precondition for a renewal that closes.

---

## Evaluation

### Criteria

- [x] PASS: Identifies health as red/critical — all four signals (58% MAU drop, champion absence, IT director reviewing spend, exec sponsor no-show) treated as compounding evidence — met
- [x] PASS: Connects usage drop timing exactly to champion's 6-week maternity leave; framed as champion-dependent adoption, not product failure — met
- [x] PASS: Flags IT director as critical risk; recommends pre-QBR 1:1 strategy before the group meeting — met
- [x] PASS: Explicitly declines expansion — Critical-health account, upsell accelerates churn, stated twice in definition — met
- [x] PASS: Specific pre-QBR actions recommended: find interim champion, identify IT director, confirm exec sponsor attendance — met
- [x] PASS: QBR framed around value realised and risk mitigation — no product demo, no upsell agenda — met
- [~] PARTIAL: 5-dimension health assessment with weights and explicit scoring — fully met (not just qualitative); scored full rather than partial credit
- [x] PASS: 8-month renewal timeline treated as urgency driver; 90-day recovery milestone (MAU to 150) established so renewal happens from strength — met

### Output expectations

- [x] PASS: Hartwell classified Critical (score 24); all four signals named as compounding factors — met
- [x] PASS: MAU drop computed numerically (210 → 89, 58% reduction) and timing linked to champion's 6-week leave — met
- [x] PASS: Expansion explicitly ruled out with reasoning (Critical health, upsell accelerates churn) — met
- [x] PASS: IT director named as critical risk; pre-QBR 1:1 action proposed with specific framing — met
- [x] PASS: Finding Sarah Kowalski's interim coverage is Priority 1 pre-QBR action — met
- [x] PASS: Pre-QBR action list is concrete with timing (days 1-2, days 2-3, days 3-5) — met
- [x] PASS: QBR agenda structured around value realised, what changed, root cause, recovery — not demos or features — met
- [x] PASS: 8-month renewal addressed; 90-day recovery target (MAU 150) established as prerequisite for renewal conversation — met
- [x] PASS: Dropped support tickets (8-12/month → 0 in 45 days) interpreted explicitly as silent departure signal, not mastery — met
- [~] PARTIAL: 5-dimension health assessment — framework applied with explicit scores; all five dimensions scored; awarded full rather than partial credit

### Notes

The agent definition handles this scenario cleanly. Every signal maps to an explicit entry in the health score framework, churn risk indicator table, or renewal management timeline. The expansion constraint is robustly specified — it appears in three separate places in the definition.

One nuance the definition doesn't address: the churn risk table says "Champion/sponsor left the company," but Sarah is on maternity leave. The risk profile differs — the relationship is recoverable, the absence has a known end date, the right action is "maintain contact with Sarah while finding an interim owner" rather than "identify a new permanent sponsor." The simulated output handles this correctly by framing it as interim coverage rather than champion replacement, but the definition's trigger is imprecise. Not a rubric issue, but worth noting for definition quality.

The silent ticket interpretation — disengagement, not mastery — is correctly handled. The engagement dimension tracks support interactions, and the proactive monitoring ethos reads silence as risk.
