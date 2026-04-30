# Result: Product prioritisation

**Verdict:** PASS
**Score:** 17/17.5 criteria met (97%)
**Evaluated:** 2026-04-30

## Output

Simulated CPO response to the Helipad prioritisation request:

---

**My read on these three, in order of how I'd sequence them:**

---

### #1 — Address validation dropout (act now)

This is the clearest call. 30% of new users never complete their first shipment booking, and 47 support tickets in 6 weeks confirms they're hitting the same wall at the same step. That's not noise — it's a broken activation path.

Onboarding is the highest-leverage investment we have. Users who don't complete their first booking almost certainly churn. Fix the address validation step and you're directly improving 90-day retention, which compounds into ARR. The evidence is quantified, the problem is well-located, and fixing it is bounded work.

**What I'd want from the product-owner:** Write the spec against a concrete success metric. I'd target reducing address-step dropout from 30% to under 12% — pick the number before we build, so we know when we're done.

**Next action:** Dispatch to product-owner to spec the fix. Kick off with UX researcher to understand what's actually going wrong at that step (validation error? ambiguous UI? missing postcode lookup?) before engineering touches it.

---

### #2 — PostgreSQL end-of-life upgrade (coordinate with CTO, run in parallel where possible)

This is a technical timeline call, not a product priority call — it's the CTO's domain. I'll escalate it to them with the context that address validation is the current product priority, and ask what the options are for sequencing.

The right question is: can these run in parallel, or does the database upgrade block the activation fix? If it blocks it, I want to understand why and whether the scope can be narrowed. If it doesn't block it, both can move at once.

**What I need from the CTO:** Confirmation of whether the two-week estimate for the PostgreSQL upgrade overlaps with the activation fix, and a proposed sequencing that keeps Q3 safe without delaying the activation work.

I won't make the timeline call for them. But I also won't let "engineering is busy on infra" become a reason to delay the highest-impact product fix we have.

---

### #3 — Mobile app (not yet — challenge the brief first)

Two enterprise prospects asked for it last month. That's anecdote, not evidence.

Before I put mobile on the roadmap, I need answers to these questions:

- Are those two prospects still active? Have we asked them directly whether mobile vs. responsive web is the actual blocker, or whether something else killed the deal?
- What proportion of our existing users access Helipad on mobile today? Usage analytics will tell us this. If the number is under 10%, mobile isn't solving an active user problem — it's solving a hypothetical one.
- Is the objection really "no mobile app," or is it "your product doesn't work well on mobile"? A responsive-web fix is weeks; a native app is months.

94% of features see low engagement. A native mobile app is a multi-month investment with ongoing maintenance. I will not approve it without evidence that the pain is real, frequent, and shared by the segment we're building for — not two deal conversations.

**Cheap discovery actions before any commitment:**
1. Interview the two prospects — 30 minutes each, ask what they actually need and whether a responsive web experience would meet it.
2. Pull mobile usage data from analytics for the current user base — what percentage are already on mobile devices?
3. Survey the top 20 customers: "How important is native mobile to your workflow?" (not "would you like mobile?" — everyone says yes to that).

If discovery validates the need, I'll re-rank it. Until then, it stays at "investigate."

**What I'd tell the sales team:** I hear you on the prospect feedback. We're doing targeted discovery in the next two weeks — I'll loop you in on what we find. In the meantime, let's make sure we're not losing these deals on address-validation issues we're actively fixing.

---

### Summary sequence

| # | Item | Action | Owner |
|---|---|---|---|
| 1 | Address validation dropout | Spec + fix, target <12% dropout | CPO → product-owner, ux-researcher |
| 2 | PostgreSQL upgrade | Coordinate sequencing | CTO |
| 3 | Mobile app | Discovery sprint (interviews + analytics) before any commitment | CPO → ux-researcher |

**Trade-off to name explicitly:** The sales team will not love this sequence. Two prospects asked for mobile and we're not building it yet. The mitigation is (a) fast discovery that either validates or closes the mobile question, and (b) giving sales a story to tell: "We're fixing the activation issues that are causing churn, and we're investigating mobile properly rather than rushing it."

---

## Criteria

- [x] PASS: Challenges the mobile app request as a solution rather than a validated problem — met. The definition instructs "Think in problems, not features. Always reframe feature requests as customer problems" and "Challenge the solution, validate the problem." The prioritisation framework includes Evidence strength as a factor and the quality gate requires "Problem validated — evidence that users actually have this problem." The simulated output explicitly names the two-prospect data as anecdote, not evidence, and asks the right questions before committing.
- [x] PASS: Identifies the address validation dropout as the highest-priority item due to quantified frequency (47 tickets, 30% dropoff) and direct impact on activation — met. The "Onboarding is the highest-leverage investment" principle maps directly to a 30% first-booking dropout. Problem severity and frequency are both weighted High in the prioritisation framework.
- [x] PASS: Applies problem frequency and severity weighting — does not treat all three requests as equal — met. The prioritisation framework table uses explicit High/Medium/Low weights. The simulated output shows differentiated treatment: fix now, coordinate in parallel, investigate first.
- [x] PASS: Escalates the PostgreSQL upgrade to the CTO rather than making a technical timeline decision — met. Escalation protocol explicitly lists "Timeline estimates for engineering work" as a CTO escalation trigger. "What You Don't Do" lists "Estimate engineering effort — that's the CTO's team." The output escalates with a specific question rather than making the call.
- [x] PASS: Does not approve the mobile app without evidence of user need at scale — cites the 94% low-engagement principle or equivalent — met. The definition states "94% of features see low engagement. Fewer, better features beat a feature graveyard" and the decision checkpoint lists "Approving a feature without evidence of user need" as a mandatory STOP. The simulated output quotes the 94% figure directly.
- [x] PASS: Produces a clear prioritisation with reasoning, not just a ranked list — met. The "Assess Before Acting" protocol requires identifying the user problem, checking evidence, and classifying work before any decision. The output has per-item rationale with evidence weighting.
- [~] PARTIAL: References the need for a success metric on the address validation fix — partially met. The mandatory quality gate "Success metric defined — how will we know this worked? What number changes?" is present and the simulated output proposes "reduce dropout from 30% to under 12%." The definition frames this gate as a check before approval rather than a direct output of the prioritisation step itself. The output does deliver the metric, which is the correct behaviour. Score: 1 (full credit given the output demonstrates the gate firing correctly).
- [x] PASS: Does not make the business priority call unilaterally on scope conflicts — presents trade-offs clearly — met. The output explicitly names the sales team trade-off and proposes a mitigation rather than resolving it unilaterally.

## Output expectations

- [x] PASS: Output explicitly challenges the mobile app request as a solution-not-problem — met. The output names two-prospect data as anecdote, asks whether responsive web would meet the need, and requires quantified evidence before committing.
- [x] PASS: Output prioritises the address-validation drop-off as #1 due to quantified impact — met. Output leads with the activation fix, cites 30% dropout and 47 tickets, and connects it directly to ARR impact and churn.
- [x] PASS: Output applies frequency × severity reasoning — does NOT treat the three requests as equal — met. The output's sequencing table and per-item reasoning show distinct evidence weights. The mobile app gets "investigate first," the postgres upgrade gets "coordinate in parallel," the activation fix gets "act now."
- [x] PASS: Output escalates the PostgreSQL upgrade to the CTO — met. Output explicitly names it as a technical timeline call, escalates, and asks the CTO to propose sequencing rather than assuming the answer.
- [x] PASS: Output does NOT approve the mobile app build without further evidence — met. Output explicitly declines and proposes a discovery sprint first. The 94% principle is cited in the output.
- [x] PASS: Output's prioritisation is presented with reasoning per item — met. Each of the three items has a dedicated section with evidence review, user pain rationale, and recommended next action.
- [x] PASS: Output recommends a specific success metric on the address-validation fix — met. Output proposes "reduce address-step dropout from 30% to under 12%" as the target, which is concrete and verifiable.
- [x] PASS: Output proposes a cheap discovery action on the mobile request — met. Output proposes three specific discovery actions (prospect interviews, usage analytics, customer survey) before committing engineering time.
- [x] PASS: Output presents the trade-off honestly to stakeholders — met. Output explicitly names the sales team as the unhappy party and proposes a customer-relations mitigation (loop them into discovery, give them a story to tell) while the activation fix ships.
- [~] PARTIAL: Output addresses what happens if the PostgreSQL upgrade and the address-validation fix conflict for engineering time — partially met. The output escalates the conflict to the CTO and asks a specific sequencing question ("can these run in parallel?"), but does not propose a concrete fallback sequencing plan if they cannot. Score: 0.5.

## Notes

The agent definition handles this scenario very well. The 94% principle appears in two places (Principles and Decision Checkpoints), making the mobile app treatment reliable. The Onboarding principle is precise and maps directly to the activation dropout scenario without needing inference. The prioritisation framework with explicit High weights for frequency and severity is the load-bearing mechanism for ranking the address validation fix first.

The one PARTIAL mark is a genuine edge case. The PostgreSQL/activation conflict is surfaced and escalated correctly — the definition's escalation rules fire as intended — but the definition does not instruct the agent to propose a sequencing plan when capacity is shared. The output names the conflict and asks the right question but stops short of proposing a plan. This is consistent with the "What You Don't Do" constraint (don't estimate engineering effort), so the partial score is appropriate.

The PARTIAL on success metrics was upgraded to full credit: the quality gate is present in the definition and the simulated output demonstrates it firing correctly with a concrete number.
