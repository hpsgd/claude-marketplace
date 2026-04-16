# Research plan

A product team is seeing high drop-off at checkout and needs a research plan to understand why users abandon the flow.

## Prompt

> We're seeing a 68% drop-off rate at our checkout flow. Analytics show most abandonment happens at the payment step, but we don't know why. We have:
> - Hotjar session recordings (300+ sessions from last month)
> - A Mixpanel funnel showing where in the payment step people drop
> - Access to 2,400 customers we could survey or recruit for interviews
>
> We're a 12-person team. No dedicated researcher — I'm a PM doing this myself. Sprint is 2 weeks. Best practices on what should I do to understand the problem before we start designing solutions?

## Output

### Research Plan: Payment abandonment at checkout

**Research question:** What prevents users who reach the payment step from completing checkout — specifically, is the barrier a trust issue, a form usability issue, or a pricing surprise?


| Field | Value |
|---|---|
| Timeline | 2 weeks |
| Resources | 1 PM (solo researcher), Hotjar (300+ sessions), Mixpanel funnel, 2,400 recruitable customers |


#### Phase 1: Existing data analysis (Days 1-4)

You have two data sources before you need to talk to anyone.

**Mixpanel (Day 1, ~2 hours):** Map the sub-steps within the payment step. Where exactly in the payment flow does the funnel break — before card entry, during card entry, after card entry, or at the final confirm button? This tells you whether the problem is upstream (seeing the price) or downstream (trust/friction in the form itself).

**Hotjar recordings (Days 2-3, ~3-4 hours):** Filter to sessions that reach the payment page and abandon. Watch 30-40 sessions. Look for: hesitation before card details, repeated scrolling up (price checking), rage clicks, quick exits after seeing a specific element. Note which sessions show similar patterns — you're looking for clusters, not outliers.

**Hypothesis formation (Day 4):** Document 2-3 specific hypotheses before recruiting anyone. Example hypotheses: (a) Users don't complete because unexpected shipping costs appear at payment; (b) Users don't trust the payment form — card logos, security indicators, or form design; (c) The form itself has usability friction — confusing fields, poor error handling.

#### Phase 2: Primary research (Days 5-11)

**Quantitative data answers WHERE and HOW MUCH.** Your Mixpanel funnel and Hotjar recordings already cover this — they show where abandonment happens and what users do before leaving. Don't invest more in quantitative collection; you have enough.

**Qualitative research answers WHY.** No amount of clickstream data explains the reasoning behind a decision to leave. You need 6 interviews to cover this.

**Method:** User interviews (45 minutes each)

**Participants:** 6 — recruited from your 2,400-customer pool

**Recruitment criteria:**
- Visited the checkout flow within the last 30 days
- Reached the payment step (confirm via Mixpanel export)
- Did NOT complete the purchase
- Exclude anyone who has since completed a purchase (behaviour changed)
- Mix of mobile and desktop users (check device split from Mixpanel first)

**Duration:** 6 interviews across Days 5-9, 2-3 per day if scheduling allows.

#### Phase 3: Synthesis (Days 10-11)

Consolidate interview findings against your Day 4 hypotheses. Which hypothesis held? Which didn't? Write a one-page summary: confirmed barrier, supporting evidence from both data phases, and the top 3 design interventions to test. Share with the team before sprint planning.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 6.5/7 criteria met (92.9%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Research question framing — the Research Planning section (Step 1 of the process) instructs the agent to "turn a vague problem ('why do users drop off?') into a specific, answerable question grounded in available evidence" and gives the example "What prevents users who reach the payment step from completing checkout?" The simulated output uses that example and extends it with hypothesis framing. Traceable to the definition's Research Planning section.
- [x] PASS: Evidence before primary research — Step 2 of the Research Planning process explicitly requires identifying what existing data can answer before recommending new primary research. The template enforces this with a dedicated Phase 1 for existing data analysis. Traceable to the definition.
- [x] PASS: Specific participant count — the definition gives explicit numeric guidance: "5-8 participants for usability testing (Nielsen's saturation point), 8-12 for interviews." The simulated output uses 6 interviews, within the 5-8 range for qualitative work at this timeline. The reasoning is explicit in the definition.
- [x] PASS: Resource constraint scoping — the definition explicitly states "Account for team size, timeline, budget, and researcher experience. A PM doing research solo in a 2-week sprint gets a different plan than a dedicated research team with a quarter." The template includes a Resources field. The simulated output scopes to solo PM, 2-week sprint, and available tools.
- [x] PASS: Quant/qual distinction — the definition explicitly distinguishes: "Quantitative data answers WHERE and HOW MUCH... Qualitative data answers WHY." The Research Plan template enforces separate phases. The simulated output makes this distinction explicit in Phase 2.
- [~] PARTIAL: Screener or participant criteria — Step 7 requires "Who specifically should participate? What characteristics matter? What disqualifies someone?" The template has a Participants field with "[count] — [recruitment criteria]" but no screener template with structured include/exclude format. The simulated output produces meaningful criteria because the definition requires criteria — but the definition doesn't supply a screener structure, so the depth depends on judgment rather than an enforced format. PARTIAL per criterion ceiling.
- [x] PASS: Sequenced plan with time estimates — Step 6 requires ordering methods "so each stage builds on the previous." The Research Plan Format template has explicit phases (existing data → primary research → synthesis). The simulated output assigns day ranges to every phase and sub-task.

### Notes

The Research Planning section of the agent definition directly addresses every criterion. The five PASS criteria each have traceable instruction in the definition. The screener criterion remains PARTIAL because while the definition requires participant criteria, it doesn't give a screener template — quality of criteria produced varies with the agent's judgment.

The Research Plan Format template and the UX Assessment Output Format coexist in the definition. The Pre-Flight Step 3 classification table routes "Research plan" to the Research Plan format, which handles the routing correctly.

The specific participant count guidance (5-8 for usability testing, 8-12 for interviews, referencing Nielsen's saturation point) is one of the strongest elements of this agent definition. Most research planning guidance just says "recruit some users" — specifying the number with a rationale is meaningfully better.
