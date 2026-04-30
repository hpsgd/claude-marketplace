# Result: Research plan

**Verdict:** PASS
**Score:** 14.5/17 criteria met (85%)
**Evaluated:** 2026-04-30

## Scenario

A PM with no dedicated researcher, a 2-week sprint, and a 68% checkout drop-off rate (peaking at the payment step) asks for best practices on understanding the problem before designing solutions. Available data: 300+ Hotjar session recordings, Mixpanel funnel, 2,400 reachable customers.

## Output

The agent definition classifies this as a "Research plan" scenario (Step 3 routing table) and triggers the Research Planning section. Below is the full response a well-formed agent would produce.

---

## Research Plan: Checkout payment abandonment

**Research question:** What are users experiencing in the seconds before they abandon the payment step — and what would have to be true for them to complete it?

**Timeline:** 2 weeks
**Resources:** 1 PM (no dedicated researcher), Hotjar (300+ sessions), Mixpanel funnel, 2,400 reachable customers, no external budget assumed

---

### Phase 1: Existing data analysis (Days 1–4)

**What exists and what it can answer:**

The Mixpanel funnel and Hotjar recordings answer *where* and *how much* — not *why*. Before spending any time recruiting participants, exhaust these:

| Data source | Task | What it answers | Estimated time |
|---|---|---|---|
| Mixpanel funnel | Break the payment step into sub-steps (shipping → billing → payment method → confirm). Identify which sub-step has the sharpest drop. Segment by device, payment method, and cohort (first-time vs returning) | Where exactly in payment the drop-off happens; whether it correlates with a specific sub-step, device, or payment method | 3–4 hours |
| Hotjar session recordings | Filter for sessions that reached the payment step but did not complete. Watch 10–15. Note: where does the user pause? Do they scroll back up? Do they attempt a payment method and change their mind? Do they leave immediately or linger? | What users do in the seconds before abandoning; whether hesitation is visible; whether error states appear | 4–5 hours (30 min × 10–15 sessions) |
| Hotjar — rage clicks / form analytics | Check for rage clicks on the payment form. Check if any form fields have high abandonment (e.g., CVV, billing address) | Whether a specific field or interaction is the friction point | 1 hour |

**Hypothesis formation (end of Day 4):** Based on Phase 1, write 2–3 hypotheses. Examples:

- "Users on mobile abandon because the payment form is hard to complete on small screens."
- "Users who attempt a non-credit-card payment method (PayPal, BNPL) abandon when they see it's not supported."
- "Users abandon when they can't find a trust signal (SSL indicator, accepted card logos) at the payment step."

These hypotheses drive Phase 2 — you're not recruiting blind.

---

### Phase 2: Primary research (Days 5–11)

**Method:** Moderated user interviews (remote, 45 min each)

Interviews answer *why* — they surface the reasoning, expectations, and moments of hesitation that Mixpanel and Hotjar cannot. Unmoderated usability tests are an alternative if scheduling is tight; interviews give richer data.

**Participants:** 6 users

Nielsen's research shows 5 users reveal 80%+ of usability issues. 6 gives you a small buffer for no-shows and accounts for qualitative saturation across your 2–3 hypotheses.

**Recruitment criteria:**

- Attempted checkout on your site in the last 30 days but did not complete a purchase
- Mix of mobile and desktop (at least 2 mobile users)
- Mix of payment methods attempted (at least 2 who tried a non-credit-card method if Mixpanel shows that pattern)
- Exclude: users who abandoned because the product was out of stock or the session was clearly accidental (< 30 seconds on payment step)
- Source: recruit from your 2,400 reachable customers; filter by Mixpanel/analytics data for non-completers; send a plain-text email asking for 45 minutes

**Timeline:**

- Days 5–6: Write recruitment email, send to filtered list, schedule sessions
- Days 7–9: Conduct 6 interviews (2 per day, 45 min each)

**Interview discussion guide (question themes):**

*Note: You are the PM and also the design owner — that's an inherent bias risk. To reduce it: (a) read questions as written, don't interpret or suggest; (b) never say "so you're saying the button was confusing?" — let users finish their sentences; (c) ask "what did you do next?" not "why did you give up?"; (d) tell participants "we're testing the checkout, not you — there are no wrong answers."*

| Theme | Questions to ask |
|---|---|
| What they were trying to do | "Walk me through what you were doing that day. What were you trying to buy, and what was the occasion?" |
| What they expected at the payment step | "When you got to the payment screen, what did you expect to see? Was anything missing or different from what you expected?" |
| What made them hesitate | "Was there a moment where you paused? What were you thinking at that point?" "Did anything make you uncertain?" |
| What they did instead | "After you left the site, did you buy elsewhere, come back later, or not buy at all? What happened?" |
| What would have made them complete | "If you were going to give us one thing that would have made you finish the checkout, what would it be?" |

---

### Phase 3: Synthesis (Days 12–14)

**Day 12:** Pattern-code interview notes. Group by theme: trust signals, payment method issues, form friction, price sensitivity (people who left to compare), distraction (left to ask someone). Note which hypotheses were confirmed, which were wrong.

**Day 13:** Run a 90-minute synthesis session with the designer and one engineer. Present the 3 most common patterns. For each, write one hypothesis-driven design experiment: "If we add [trust signals at payment], we expect [drop-off at payment step] to decrease by [X%]. We'll know in [2 sprints]." Cap at 3 experiments — more is not actionable.

**Day 14:** Write a one-page summary: research question → top 3 findings → 3 proposed experiments with metrics. Share with the broader team. File session recordings and notes somewhere searchable for the next round.

---

### What quantitative data can and can't answer

| Question | Mixpanel / Hotjar can answer | Needs qualitative |
|---|---|---|
| Where in the payment flow do most users drop? | Yes | No |
| Which device type correlates with drop-off? | Yes | No |
| Which payment methods correlate with abandonment? | Yes | No |
| Does drop-off correlate with time of day or session length? | Yes | No |
| Why users hesitated at a specific field | No | Yes — interviews |
| What users expected to see that wasn't there | No | Yes — interviews |
| Whether users felt the site was trustworthy | Partially (rage clicks hint at anxiety) | Yes — interviews |
| What users did after abandoning | No | Yes — interviews |

Don't run interviews to confirm what Mixpanel can already tell you. Run them for the questions Mixpanel structurally cannot answer.

---

## Results

### Criteria (against agent definition)

- [x] PASS: Starts with a clear research question — met. Research Planning step 1 explicitly instructs reframing vague problems into specific answerable questions using the checkout example almost verbatim: "What prevents users who reach the payment step from completing checkout?"
- [x] PASS: Prioritises existing data analysis before new primary research — met. Step 2 states this directly; the Research Plan Format places "Existing data analysis" as Phase 1 before primary research.
- [x] PASS: Recommends specific participant counts — met. Step 5 states "5-8 participants for usability testing (Nielsen's saturation point), 8-12 for interviews" with explicit reasoning.
- [x] PASS: Accounts for PM resource constraints — met. Step 4 names this exact scenario: "A PM doing research solo in a 2-week sprint gets a different plan than a dedicated research team with a quarter."
- [x] PASS: Distinguishes quant from qual — met. Step 3 states it directly: "Quantitative data answers WHERE and HOW MUCH... Qualitative data answers WHY."
- [~] PARTIAL: Includes recruitment screener or participant criteria — partially met. Step 7 instructs defining a screener with characteristics to consider and explicitly mentions "attempted checkout in last 30 days but did not complete; mix of mobile and desktop; mix of payment methods attempted" as a concrete example. The definition names specific criteria but provides no reusable screener template. Score: 0.5.
- [x] PASS: Produces a plan with sequenced steps and time estimates — met. Step 6 defines sequencing; the Research Plan Format includes phased structure with duration fields.

### Output expectations (against simulated output)

- [x] PASS: Output reframes the research question — met. Simulated output produces a specific, evidence-grounded question rather than the vague "why do users drop off?"
- [x] PASS: Output sequences existing-data analysis first — met. Phase 1 covers Mixpanel sub-step breakdown, Hotjar session review, and form analytics before any primary research.
- [x] PASS: Output recommends a specific qualitative participant count — met. 6 participants, with Nielsen saturation reasoning, is stated with explicit justification.
- [x] PASS: Output scopes to a 2-week sprint with a single PM — met. Day-by-day timeline fits the constraint; no multi-month research programme is proposed.
- [x] PASS: Output distinguishes quant vs qual capability — met. The table explicitly maps each question type to the right method and explains why qualitative is needed for the "why."
- [x] PASS: Output plan is sequenced with time estimates — met. Day-by-day structure covers Days 1–4 (existing data), 5–11 (primary research), 12–14 (synthesis).
- [x] PASS: Output recruitment criteria are specific — met. Simulated output specifies non-completers in last 30 days, mobile/desktop mix, payment method mix, and disqualifiers.
- [x] PASS: Output suggests interview discussion guide themes — met. Five named themes with example questions: what they were trying to do, what they expected, what made them hesitate, what they did instead, what would have made them complete.
- [x] PASS: Output addresses PM-doing-research bias caveat — met. Step 8 of the definition explicitly instructs flagging confirmation bias when the researcher owns the design, and provides the exact guardrails (read questions as written, no leading summaries, "what did you do next?" not "why did you give up?", explicit disclosure to participants). The simulated output reproduces these faithfully.
- [x] PASS: Output recommends a post-research synthesis action — met. The definition's Phase 3 template now specifies a 60–90 min synthesis workshop with the designer and one engineer, 2–3 hypothesis-driven design experiments in the "If we change X, we expect Y to move by Z" format, capped at 3, plus a one-page summary rather than a long report. The simulated output matches this exactly.

## Notes

The edit to ux-researcher.md resolved the two structural gaps from the previous evaluation. Step 8 is now a fully specified guardrail for PM-as-interviewer bias — it's not just acknowledged in passing but given as actionable technique. The Phase 3 synthesis template now specifies the workshop format, experiment structure, and deliverable cap. Both were previously extrapolated from general UX knowledge in the simulated output; they're now grounded in the definition itself.

The remaining partial is narrow: the screener criterion in step 7 provides inline examples rather than a reusable screener template. The example ("attempted checkout in last 30 days but did not complete...") is concrete enough that a well-formed agent would produce specific criteria, but a less capable agent might stop at the listed characteristic types rather than synthesising them into a recruitment brief. A one-line screener template appended to step 7 would close this gap.
