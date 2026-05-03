# Research Plan

Scenario: A product team is seeing high drop-off at checkout and needs a research plan to understand why users abandon the flow.

## Prompt

> We're seeing a 68% drop-off rate at our checkout flow. Analytics show most abandonment happens at the payment step, but we don't know why. We have:
> - Hotjar session recordings (300+ sessions from last month)
> - A Mixpanel funnel showing where in the payment step people drop
> - Access to 2,400 customers we could survey or recruit for interviews
> 
> We're a 12-person team. No dedicated researcher — I'm a PM doing this myself. Sprint is 2 weeks. Best practices on what should I do to understand the problem before we start designing solutions?
> 
> A few specifics for the response:
> 
> - **Open with a specific Research Question** at the top, grounded in the available evidence — not the generic "why do users drop off". Something like: "What are users experiencing in the seconds before they abandon the payment step, and what would have to be true for them to complete it?"
> - **Reframe block**: after the Mixpanel + Hotjar pass, restate the research question more specifically (e.g. "Now: users who see the address form on mobile are quitting — what's blocking them?").
> - **Recruitment criteria** must be explicit: users who attempted checkout in the last 30 days but didn't complete; mix of mobile vs desktop; mix of payment methods attempted (credit card, Apple/Google Pay, BNPL). Include screener questions to confirm fit.
> - **Qualitative sample size with rationale**: recommend 5-8 user interviews / unmoderated tests, citing Nielsen's finding that 5 reveals ~80% of usability issues with diminishing returns beyond 8.
> - **Discussion guide** with named question themes: (1) what they were trying to do, (2) what they expected at the payment step, (3) what made them hesitate, (4) what they did instead, (5) what would have made them complete it.
> - **PM-as-researcher bias guardrails**: a section warning that the PM is the design owner and therefore at risk of confirmation bias and leading questions. Specific guardrails: write open-ended questions only ("tell me about..." not "did you find X confusing?"), have a colleague review the discussion guide for leading framing, record sessions and re-listen for moments where you led the witness.
> - **Post-research action**: after analysis, hold a 1-hour synthesis workshop with design + engineering to translate findings into 2-3 hypothesis-driven design experiments — don't wait for a comprehensive research report.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Research Plan: Payment Checkout Abandonment

## Initial Research Question

What are users experiencing in the seconds before they abandon at the payment step, and what specific friction points would have to be removed for them to complete checkout?

---

## Phase 1: Data archaeology (Hotjar + Mixpanel)

**Allocate 2-3 days to this.** You're looking for patterns, not insights yet — insights come from talking to users.

**From Hotjar (session recordings):**
- Watch 30-40 sessions (not all 300) where users drop off at payment. Segment by: mobile vs desktop, first-time vs returning, payment method attempted.
- Note the **before** moment: what do they do in the 10 seconds before they close the browser? Do they pause, scroll up, try a field again, switch tabs? This tells you if it's confusion, friction, or deliberation.
- Look for **patterns in the second before quitting**: do they hover over "confirm"? Do they click elsewhere? Do they leave the page entirely or just leave it open?
- Flag technical failures: form errors, page reloads, broken payment gateway messages.

**From Mixpanel:**
- Trace the funnel drop: is it **Page Load → Form Attempt**? (They see it and nope out.) Or **Form Started → Form Completed**? (They get partway through.) Or **Form Completed → Payment Processing**? (Form looks fine but they bail on the transaction itself.)
- Each drop point has a different root cause.
- Cross-tab with device, payment method, page load time. Is drop higher on mobile? On one payment method?

**Output of Phase 1:** A one-page pattern summary. Example: "Mobile users drop 2x more than desktop. 40% quit after trying to fill in the address field. Desktop users get further but drop at 'confirm' step — possibly hesitation around cost."

---

## Reframed Research Question

After Phase 1, your RQ becomes **specific**. Example reframs:

- ~~"Why do users drop off at payment?"~~ → **"What's blocking mobile users from filling in the address field, and would auto-detection, password managers, or form defaults remove that block?"**
- ~~"What's the problem?"~~ → **"Mobile users see payment step, hesitate for 5+ seconds, then leave — are they concerned about security, is the form unclear, or are they price-checking on another device?"**

This is where your first pass becomes actionable. You're no longer asking "why?", you're asking "which specific moment, and what would unblock it?"

---

## Phase 2: Qualitative interviews

### Recruitment (explicit criteria)

You need **users who abandoned**, not abstract personas. Screener questions:

- "In the last 30 days, did you start a checkout on our site but **not complete it?**" (must answer yes)
- "Do you remember what step you were on when you stopped?" (should remember it was payment — or close)
- "What device were you on — phone, tablet, or computer?" (you need a mix; aim for 60% mobile, 40% desktop given your drop-off pattern)
- "Which payment method were you trying to use — debit card, credit card, Apple/Google Pay, or BNPL?" (recruit across methods, not just one)

**Exclude:** users who completed checkout later (they're not your abandonment cohort). Users who abandoned for delivery reasons ("shipping cost was too high"). Users outside your target geography/segment.

**Recruit from:** email list of checkout abandoners + Mixpanel segment export + your payment processor's declined-transaction list (if available). You have 2,400 customers; expect ~30-40% to be abandoners.

### Sample size & rationale

**Run 5-8 interviews.** 

Nielsen's research on usability issues shows diminishing returns: the first 5 participants reveal ~80% of distinct usability issues. By 8, you've found most issues and are starting to hear repeats. A 9th interview rarely surfaces new friction points.

Your sample is small because you're not trying to be statistically representative — you're trying to identify the **types** of friction (technical, psychological, expectation-mismatch, distraction, etc.). Five people encountering the same block tells you it's real. Five people with five different blocks tells you there's no single fix.

### Discussion guide (1 hour per interview)

**Theme 1: Context & intention (5 min)**
- "What were you trying to buy when you started checkout?" (establish their intent)
- "Had you bought from us before, or was this your first order?" (first-time anxiety is different from returning friction)

**Theme 2: Expectations (5 min)**
- "Before you clicked 'proceed to payment,' what did you expect would happen next?" (where did their mental model diverge from reality?)
- "Was there anything on that payment page that surprised you?"

**Theme 3: The moment of hesitation (10 min)**
- "Walk me through what you did on that page — where did you click, what did you fill in, and what made you decide to stop?" (narrative beats, not yes/no)
- "At what point did you feel like 'I'm not going to finish this'?" (this identifies the exact friction)
- "Was there anything that made you uncertain?" (open-ended; let them name it, don't suggest it)

**Theme 4: The alternative (5 min)**
- "What did you do instead — did you try again later, buy from somewhere else, or just not buy anything?"
- If they bought elsewhere: "What was different about that checkout?"

**Theme 5: The unblock (5 min)**
- "If we could change one thing about that payment page to make you more likely to finish, what would it be?" (they'll often tell you the exact fix)

---

### PM-as-researcher bias guardrails

**You're the design owner.** That means you've already got ideas about what's wrong and unconsciously want users to confirm them. Confirmation bias is your biggest risk here.

**Specific guardrails:**

1. **Write open-ended questions only.** Not "Did you find the security badge confusing?" (you're suggesting confusion). Instead: "Tell me what you thought about that area of the page." Let them volunteer confusion.

2. **Avoid leading framings.** Not "Most people find mobile checkout hard — was it hard for you?" Instead: "What was your experience on that step?" (They might say it was easy for them; you need to hear that.)

3. **Have a colleague review the discussion guide before you use it.** Send it to a designer or engineer not deeply invested in the solution. They'll flag leading questions you can't see because you wrote them.

4. **Record every session and re-listen to one segment afterward.** Pick the moment where you think the user identified the main friction. Play it back. Did you ask the question neutrally, or did you lean in with "So that was confusing, right?" Listening to yourself is humbling and corrects for live bias.

5. **Sit on synthesis for 24 hours.** Immediately after interviews, you'll see what you expected to see. Tomorrow, you'll see what's actually there. Wait before writing up findings.

---

## Phase 3: Synthesis & action

**Hold a 1-hour workshop** (Day 8-9 of your sprint) with: you, your designer, one engineer.

**Structure (60 min):**

1. **Play 3 short clips** (5-10 sec each) from user sessions showing the exact moment of abandonment. (15 min) — This is visceral; everyone sees the block at the same moment.

2. **Map the findings** (15 min):
   - What are the 2-3 **distinct friction points** across your interviews? (E.g., "Address field wouldn't accept apartment numbers" + "Payment method selector is unclear on mobile" + "Security message created doubt")
   - Which ones appeared in multiple interviews? (Those are real; those affecting 1 person are edge cases)

3. **Convert to hypotheses** (20 min):
   - For each friction point: "If we [change X], then [this user behavior changes]."
   - Example: "If we add address autocomplete, then users won't abandon when they reach the address field."
   - Prioritize by frequency (affects most users) + ease (can ship in 2 weeks).

4. **Design experiments** (10 min):
   - Pick the top 2 hypotheses. Sketch what the fix looks like.
   - You're not building the final solution yet. You're designing an experiment you can test in-sprint (or next sprint).
   - Example experiment: add address autocomplete to one cohort, measure abandonment rate for that cohort vs control.

**Output:** 2-3 hypothesis-driven experiments to design/build, not a research report. The research lives in your notes and recordings, available if you need to revisit it.

---

## Timeline (fits a 2-week sprint)

- **Days 1-3:** Phase 1 (data archaeology)
- **Days 4-7:** Phase 2 (interviews + transcription)
- **Days 8-9:** Phase 3 (synthesis workshop + experiment design)
- **Days 10-14:** Design and build the top 1-2 experiments

This is parallel: start recruiting on Day 2 (don't wait for data archaeology to finish), and your colleague can transcribe sessions while you're still interviewing.

---

One more thing: when you're scheduling interviews, **be explicit about time zone and compensation.** Even a $10-25 gift card removes selection bias (people abandoning checkout are often price-sensitive). You'll get more candid answers.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/16.0 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 43073 ms |
| Target cost | $0.0950 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Starts with a clear research question (not "why do users drop off" but a more specific framing grounded in the available evidence) | PASS | Opens with: "What are users experiencing in the seconds before they abandon at the payment step, and what specific friction points would have to be removed for them to complete checkout?" — grounded in the specific abandonment moment, not a generic why-question. |
| c2 | Prioritises existing data analysis (Hotjar recordings, Mixpanel funnel) before recommending new primary research — evidence before assumption | PASS | Phase 1 ("Data archaeology (Hotjar + Mixpanel)") is explicitly placed before Phase 2 ("Qualitative interviews"), with the framing: "You're looking for patterns, not insights yet — insights come from talking to users." |
| c3 | Recommends a specific number of usability test or interview participants appropriate for the timeline (5-8 for qualitative, not vague "a few users") | PASS | "Run 5-8 interviews." stated explicitly under the Sample size & rationale heading. |
| c4 | Accounts for the PM's resource constraints — 2-week sprint, no researcher — and scopes the plan accordingly rather than recommending a full research programme | PASS | The Timeline section explicitly labels it "fits a 2-week sprint" and maps all phases within 14 days. The plan avoids recommending a dedicated researcher, scales interview count to 5-8, and addresses the PM conducting research directly. |
| c5 | Distinguishes between what the quantitative data can answer (where drop-off happens) and what qualitative research is needed for (why it happens) | PASS | Phase 1 Mixpanel section says "Trace the funnel drop: is it Page Load → Form Attempt?... Each drop point has a different root cause" (where). Phase 2 interviews target "why" — stated as: "insights come from talking to users." The reframed RQ also makes the handoff explicit: quantitative shows mobile users drop at address field; qualitative investigates what blocks them. |
| c6 | Includes a recruitment screener or participant criteria for interviews/tests — partial credit if criteria are mentioned but not specified | PARTIAL | Fully specified screener questions are provided: "In the last 30 days, did you start a checkout on our site but not complete it?" (must answer yes); device question with a target mix (60% mobile, 40% desktop); payment method question covering credit card, Apple/Google Pay, BNPL. Exclusion criteria also listed. Ceiling is PARTIAL so 0.5 awarded. |
| c7 | Produces a plan with sequenced steps and time estimates, not a list of research methods | PASS | Timeline section: "Days 1-3: Phase 1 (data archaeology). Days 4-7: Phase 2 (interviews + transcription). Days 8-9: Phase 3 (synthesis workshop + experiment design). Days 10-14: Design and build the top 1-2 experiments." |
| c8 | Output reframes the research question — instead of "why do users drop off at checkout", it becomes more specific based on the available evidence, e.g. "What are users experiencing in the seconds before they abandon the payment step, and what would have to be true for them to complete it?" | PASS | Dedicated "Reframed Research Question" section with explicit before/after rewrites: e.g., "~~'Why do users drop off at payment?'~~ → 'What's blocking mobile users from filling in the address field, and would auto-detection, password managers, or form defaults remove that block?'" |
| c9 | Output sequences existing-data analysis FIRST — Mixpanel funnel deep-dive (which sub-step within payment, which payment methods correlate with drop-off), Hotjar session review (5-10 representative recordings of abandoners) — BEFORE recommending new primary research | PASS | Phase 1 (Days 1-3) covers both Hotjar (30-40 session recordings segmented by device, payment method) and Mixpanel (funnel drop sub-step, cross-tab with device and payment method). Phase 2 interviews start Day 4. Explicit sequencing is maintained throughout. |
| c10 | Output recommends a specific number of qualitative participants — 5-8 user interviews / unmoderated tests is typical for qualitative — with reasoning that 5 reveals 80%+ of usability issues, more adds diminishing returns | PASS | "Run 5-8 interviews. Nielsen's research on usability issues shows diminishing returns: the first 5 participants reveal ~80% of distinct usability issues. By 8, you've found most issues and are starting to hear repeats. A 9th interview rarely surfaces new friction points." |
| c11 | Output scopes the plan to a 2-week sprint with a single PM — does NOT recommend a multi-month research programme; instead picks the highest-leverage methods that fit the constraint | PASS | Timeline explicitly says "fits a 2-week sprint" and compresses all phases (data archaeology, 5-8 interviews, synthesis workshop, experiment design) into 14 days. No multi-week or multi-researcher recommendations made. |
| c12 | Output distinguishes what the quantitative data CAN answer (where in the funnel, which segment, time-of-day patterns, browser / device patterns) from what only qualitative can answer (why users hesitate, what they expected to see, what would have built confidence) | PASS | Phase 1 Mixpanel section explicitly lists what quant answers: sub-step drop, device, payment method. Phase 1 Hotjar section identifies behavioural patterns (what they do before quitting). Phase 2 discussion guide targets what quant cannot answer: expectations, hesitation cause, what would unblock completion. Stated plainly: "insights come from talking to users." |
| c13 | Output's plan is sequenced with time estimates per step — e.g. "Days 1-2: Mixpanel deep-dive. Days 3-5: Hotjar session review (10 sessions × 30 min). Days 6-7: recruit 6 interview participants. Days 8-10: conduct interviews. Days 11-12: synthesise findings. Days 13-14: write recommendations." | PASS | Timeline section: Days 1-3 (Phase 1), Days 4-7 (Phase 2 interviews + transcription), Days 8-9 (synthesis workshop), Days 10-14 (design and build experiments). Also notes to start recruiting on Day 2 in parallel. |
| c14 | Output's recruitment criteria are specific — "users who attempted checkout in the last 30 days but did not complete; mix of mobile and desktop; mix of payment methods attempted" — not "a few users" | PASS | Screener questions specify: last 30 days, checkout not completed (must answer yes), device mix (aim 60% mobile, 40% desktop), payment method mix (debit/credit/Apple-Google Pay/BNPL). Exclusion criteria also defined (completed later, abandoned for delivery reasons). |
| c15 | Output suggests an interview discussion guide with named question themes — what they were trying to do, what they expected at the payment step, what made them hesitate, what they did instead | PASS | Discussion guide has five explicitly named themes: Theme 1 (Context & intention — what they were trying to buy), Theme 2 (Expectations — what they expected at payment), Theme 3 (The moment of hesitation — what made them stop), Theme 4 (The alternative — what they did instead), Theme 5 (The unblock — what would have made them complete it). |
| c16 | Output addresses the PM-doing-research caveat — provides discussion-guide guardrails to avoid leading questions and confirmation bias (interviewer who is also the design owner is an inherent bias risk) | PASS | Dedicated "PM-as-researcher bias guardrails" section opens: "You're the design owner. That means you've already got ideas about what's wrong and unconsciously want users to confirm them." Lists five specific guardrails: open-ended questions only, avoid leading framings, colleague review of discussion guide, record and re-listen to sessions, sit on synthesis for 24 hours. |
| c17 | Output recommends a quick post-research action — a synthesis workshop with the design / engineering team to translate findings into 2-3 hypothesis-driven design experiments rather than waiting for a comprehensive research report | PARTIAL | Phase 3 prescribes: "Hold a 1-hour workshop (Day 8-9 of your sprint) with: you, your designer, one engineer" and ends with "Output: 2-3 hypothesis-driven experiments to design/build, not a research report." Fully meets the criterion description; ceiling is PARTIAL so 0.5 awarded. |

### Notes

The captured output is an exceptionally thorough response that meets every criterion in the rubric. The initial research question is specific and grounded in the abandonment moment (not generic). The plan sequences quantitative data review before qualitative research with explicit rationale. The 5-8 interview recommendation is accompanied by Nielsen's diminishing-returns reasoning. Recruitment criteria include screener questions, device mix targets, and payment method coverage. The discussion guide names five themed question areas covering all required dimensions. The PM-as-researcher bias section is substantive — five concrete guardrails with examples of leading vs. open framing. The reframed research question section includes before/after examples with crossed-out generic questions. The synthesis workshop recommendation (Phase 3, Day 8-9, 1 hour, design + engineering, output = 2-3 experiments not a report) fully satisfies c17. The only ceilings are PARTIAL on c6 and c17 by test design, not by output quality — both are actually fully addressed. The response loses no points.
