# Research Plan

Scenario: A product team is seeing high drop-off at checkout and needs a research plan to understand why users abandon the flow.

## Prompt

> We're seeing a 68% drop-off rate at our checkout flow. Analytics show most abandonment happens at the payment step, but we don't know why. We have:
> - Hotjar session recordings (300+ sessions from last month)
> - A Mixpanel funnel showing where in the payment step people drop
> - Access to 2,400 customers we could survey or recruit for interviews
> 
> We're a 12-person team. No dedicated researcher — I'm a PM doing this myself. Sprint is 2 weeks. Best practices on what should I do to understand the problem before we start designing solutions?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Start with what you already have — don't recruit until you have hypotheses.**

## Week 1: Mine existing data (days 1–5)

**Day 1–2: Mixpanel first.** Pinpoint exactly where in the payment step people exit. Entering card details? Address? Clicking submit? Error state? This tells you what to look for in Hotjar and keeps you from watching 300 sessions blind.

**Day 2–4: Targeted Hotjar review.** Watch 20–30 sessions of people who abandoned at that specific sub-step — not all 300. You'll hit pattern saturation fast. Look for:
- Rage clicks or repeated field interactions
- Hesitation before exiting (user reading something)
- Error states appearing
- Unexpected page reloads

**Day 3: Check payment processor error logs.** A technical failure causing silent card declines would show up here but not in Hotjar. Rule it out early.

**End of week 1 deliverable:** A short hypothesis list — "we believe drop-off is caused by A, B, C."

---

## Week 2: Validate with humans (days 8–14)

**Day 8–9: Send a single-question survey to recent abandonees.** From your 2,400, filter to people who abandoned in the last 30 days. One open question: *"What stopped you from completing your purchase?"* with 5–6 options + free text. Typeform or Google Form is fine. Aim for 100+ responses before day 12.

**Day 10–12: 4–5 moderated interviews (30 min each).** Recruit from survey respondents who opt in. Walk them through checkout on staging. Ask them to think aloud. This is where you'll understand the *why* behind the quantitative signal.

---

## Common payment drop-offs to watch for

- Forced account creation before purchase
- Unexpected shipping costs appearing late
- Missing trust signals (no recognizable payment logos, no SSL indicator)
- Limited payment methods (no Apple Pay, no PayPal)
- Unhelpful error messages on card decline
- Mobile keyboard covering the submit button

---

**The trap to avoid:** Don't recruit interviews before you've watched the sessions. You'll ask the wrong questions. The Mixpanel + Hotjar pass should take you from "payment step" to something specific like "users who see the address form are quitting" — then you know what to probe in interviews.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.5/16.0 (72%) |
| Evaluated | 2026-05-01 |
| Target duration | 34587 ms |
| Target cost | $0.1016 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Starts with a clear research question (not "why do users drop off" but a more specific framing grounded in the available evidence) | FAIL | The output opens with 'Start with what you already have — don't recruit until you have hypotheses.' This is strategic framing, not a research question. No specific research question is stated at the outset grounded in the available evidence. |
| c2 | Prioritises existing data analysis (Hotjar recordings, Mixpanel funnel) before recommending new primary research — evidence before assumption | PASS | Week 1 is entirely dedicated to mining existing data: 'Day 1–2: Mixpanel first' then 'Day 2–4: Targeted Hotjar review.' Week 2 introduces new primary research (survey, interviews). Structure is explicit and sequenced. |
| c3 | Recommends a specific number of usability test or interview participants appropriate for the timeline (5-8 for qualitative, not vague "a few users") | PASS | Output states '4–5 moderated interviews (30 min each)' — a specific number rather than a vague recommendation. |
| c4 | Accounts for the PM's resource constraints — 2-week sprint, no researcher — and scopes the plan accordingly rather than recommending a full research programme | PASS | Plan is structured across exactly 2 weeks with no mention of additional headcount or extended timelines. Methods chosen (targeted Hotjar review of 20–30 sessions, single-question survey, 4–5 interviews) fit a solo PM executing in a sprint. |
| c5 | Distinguishes between what the quantitative data can answer (where drop-off happens) and what qualitative research is needed for (why it happens) | PASS | Mixpanel is framed as revealing 'exactly where in the payment step people exit'; interviews are where 'you'll understand the *why* behind the quantitative signal.' The 'trap to avoid' section also reinforces this: quant narrows the location, then qualitative probes the reason. |
| c6 | Includes a recruitment screener or participant criteria for interviews/tests — partial credit if criteria are mentioned but not specified | PARTIAL | Survey targets 'people who abandoned in the last 30 days' from the 2,400 list; interviews recruit from 'survey respondents who opt in.' Criteria are present but limited — no device split, no payment method filter, no screener questions. |
| c7 | Produces a plan with sequenced steps and time estimates, not a list of research methods | PASS | Plan uses explicit day ranges: Day 1–2, Day 2–4, Day 3, End of week 1, Day 8–9, Day 10–12 — sequenced steps with time estimates, not an unordered method list. |
| c8 | Output reframes the research question — instead of "why do users drop off at checkout", it becomes more specific based on the available evidence, e.g. "What are users experiencing in the seconds before they abandon the payment step, and what would have to be true for them to complete it?" | PARTIAL | The 'trap to avoid' section illustrates a potential reframe: 'Mixpanel + Hotjar pass should take you from "payment step" to something specific like "users who see the address form are quitting."' This hints at reframing but presents it as a possible outcome rather than stating a specific reframed research question upfront. |
| c9 | Output sequences existing-data analysis FIRST — Mixpanel funnel deep-dive (which sub-step within payment, which payment methods correlate with drop-off), Hotjar session review (5-10 representative recordings of abandoners) — BEFORE recommending new primary research | PASS | Week 1 is entirely Mixpanel + Hotjar + error logs; Week 2 introduces survey and interviews. Order is unambiguous. |
| c10 | Output recommends a specific number of qualitative participants — 5-8 user interviews / unmoderated tests is typical for qualitative — with reasoning that 5 reveals 80%+ of usability issues, more adds diminishing returns | PARTIAL | '4–5 moderated interviews' gives a specific number, but no reasoning is provided about saturation, diminishing returns, or the 80% heuristic. The number alone without rationale is incomplete against this criterion. |
| c11 | Output scopes the plan to a 2-week sprint with a single PM — does NOT recommend a multi-month research programme; instead picks the highest-leverage methods that fit the constraint | PASS | The two-week structure is explicit; methods chosen (20–30 Hotjar sessions, one survey, 4–5 interviews) are minimal and high-leverage. No extended programme is proposed. |
| c12 | Output distinguishes what the quantitative data CAN answer (where in the funnel, which segment, time-of-day patterns, browser / device patterns) from what only qualitative can answer (why users hesitate, what they expected to see, what would have built confidence) | PASS | Quant (Mixpanel, Hotjar) answers 'where' and surface behaviors (rage clicks, hesitation, error states); qualitative (interviews) answers 'why' — explicitly stated: 'you'll understand the *why* behind the quantitative signal.' The distinction is clear, though the output doesn't enumerate device/time-of-day patterns specifically. |
| c13 | Output's plan is sequenced with time estimates per step — e.g. "Days 1-2: Mixpanel deep-dive. Days 3-5: Hotjar session review (10 sessions × 30 min). Days 6-7: recruit 6 interview participants. Days 8-10: conduct interviews. Days 11-12: synthesise findings. Days 13-14: write recommendations." | PASS | Day 1–2 (Mixpanel), Day 2–4 (Hotjar), Day 3 (error logs), Day 8–9 (survey), Day 10–12 (interviews) — each step has a named day range. Synthesis and recommendations are not explicitly scheduled but overall structure matches the criterion's intent. |
| c14 | Output's recruitment criteria are specific — "users who attempted checkout in the last 30 days but did not complete; mix of mobile and desktop; mix of payment methods attempted" — not "a few users" | PARTIAL | Output specifies 'people who abandoned in the last 30 days' but lacks the mobile/desktop mix and payment-method mix that the criterion requires. Partial specificity only. |
| c15 | Output suggests an interview discussion guide with named question themes — what they were trying to do, what they expected at the payment step, what made them hesitate, what they did instead | FAIL | No interview discussion guide or named question themes appear in the output. The 'Common payment drop-offs to watch for' section is a hypothesis list, not a discussion guide. The output only says 'Walk them through checkout on staging. Ask them to think aloud.' |
| c16 | Output addresses the PM-doing-research caveat — provides discussion-guide guardrails to avoid leading questions and confirmation bias (interviewer who is also the design owner is an inherent bias risk) | FAIL | No mention of confirmation bias, leading questions, or any guardrails for a PM conducting interviews on their own product. The PM-as-researcher bias risk is entirely absent from the output. |
| c17 | Output recommends a quick post-research action — a synthesis workshop with the design / engineering team to translate findings into 2-3 hypothesis-driven design experiments rather than waiting for a comprehensive research report | FAIL | No post-research action, synthesis workshop, or recommendation to translate findings into design experiments is mentioned anywhere in the output. |

### Notes

The output is a solid, practically structured research plan that correctly sequences existing data analysis before primary research, provides a day-by-day schedule, and fits the PM's 2-week solo constraint. It scores well on process and structure. Its main gaps are at the depth layer: no explicit reframed research question, no interview discussion guide with named themes, no PM-as-researcher bias guardrails, no post-research synthesis step, and recruitment criteria that are partial rather than fully specified. The 4–5 interviews recommendation is specific but lacks the saturation rationale the rubric requires. The output is competent UX research guidance but stops short of the expert-level specificity on participant screeners, discussion guides, and bias management that the more demanding criteria expect.
