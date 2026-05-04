# Define Okrs

Scenario: A user invokes the skill to define OKRs for a product team for a quarter. Does the skill enforce the OKR rules — qualitative objectives, quantified key results with baselines, 70% ambition target, mix of leading/lagging indicators, and a guardrail metric?

## Prompt

> /coordinator:define-okrs "Onboarding team at Stackform, Q3 2026. Context: last quarter we shipped a new onboarding wizard but activation (users who complete setup and send their first API request) is still only 38%. We want to fix this. Parent objective: grow the number of paying customers by 30% this year."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've drafted the OKRs for your Onboarding team in Q3 2026. Here's what shaped the structure:

**Two objectives, tightly focused:**

1. **Activation (the growth lever)** — moves from 38% to 55%. Three KRs measure the full path: the headline metric, speed of the flow, and whether activated users are actually getting value (7-day retention).

2. **Support friction (the health metric)** — ensures you're not just pushing volume through, but actually reducing friction. Self-serve completion rate + resolution speed + NPS tells you whether the experience is genuinely better.

**Key decisions:**

- **Activation target of 55%** — that's a 45% improvement over current state, ambitious enough to require real work but not so high it becomes absurd.
- **Time-to-activation under 12 minutes** — this is a leading indicator. If you're removing friction, users should reach their first API call faster.
- **7-day retention at 70%** — this is your guardrail that the activation isn't just a one-time event; users are actually getting value and coming back.
- **Measurement is explicit** — each KR specifies the tool, the query, frequency, and owner so there's no ambiguity in Q4 when you score.

**Three metrics need baselines by week 1** (time-to-activation, self-serve completion, NPS). You have the activation baseline already (38%), but the others require you to instrument tracking if it's not already there.

Does this align with where the team wants to go? Any adjustments before this goes into your docs?

### Artifacts written

#### `work/docs/okrs-onboarding-q3-2026.md`

```
# OKRs: Onboarding Team at Stackform — Q3 2026

**Context:** In Q2 2026, the Onboarding team shipped a redesigned onboarding wizard intended to improve the activation funnel. However, the activation rate (users who complete setup and send their first API request) remains low at 38%. This quarter we are focused on understanding and eliminating the barriers preventing users from reaching confident API proficiency, directly supporting the company's goal to grow paying customers by 30% this year.

**Parent objective:** Grow the number of paying customers by 30% this year (Company OKR)

---

## Objective 1: Help new developers reach confident API proficiency in their first hour

**Why this objective:** Activation is a leading indicator of conversion to paid customers. Users who successfully complete setup and send their first API request are significantly more likely to become paying customers. At 38%, our activation rate is below industry benchmarks (typically 50-70%). Improving this is the team's highest-impact lever for supporting company growth.

**Key Initiatives (inputs, not measured):**
- Redesign the first API request experience to be more discoverable and rewarding
- Add contextual help and "show me how" guidance at key friction points
- Create quick-start templates and example requests (curl, Python, JS) ready to copy-paste
- Optimize the setup flow for clarity and reduce required fields
- Implement progress indicators so users understand how close they are to activation

| KR | Metric | Baseline | Target | Measurement | Type |
|----|--------|----------|--------|-------------|------|
| KR1.1 | Activation rate (% of new users who complete setup AND send at least one successful API request within 14 days) | 38% (Q2 2026, Mixpanel) | 55% | Mixpanel: weekly cohort of new signups; measure completion of `onboarding_completed` + `api_request_successful` events within 14 days. Daily refresh, weekly report to team. Owner: Analytics | Lagging |
| KR1.2 | Median time from signup to first successful API request (for activated users) | Establish baseline by 2026-07-11 | <12 minutes | Session replay/event stream analysis (Amplitude or internal event logs): measure time from `account_created` to `api_request_successful`. Weekly rolling average. Owner: Product + Analytics | Leading |
| KR1.3 | 7-day retention among activated users (% of users who send at least one API request in a week and repeat in the following 7 days) | Establish baseline by 2026-07-11 | 70% | Mixpanel cohort retention: for users with `api_request_successful` event in week N, measure % with at least one `api_request_successful` in week N+1. Weekly calculation. Owner: Analytics | Leading |

---

## Objective 2: Make onboarding so intuitive that users rarely need support to get started

**Why this objective:** Friction in the setup flow manifests as both incomplete activations and support tickets. By reducing the need for support during onboarding, we both improve activation (users complete the flow) and reduce operational burden. This is a health metric that ensures we're not just increasing volume but improving the underlying user experience.

**Key Initiatives (inputs, not measured):**
- Add contextual error messages that guide users toward solutions, not just report problems
- Create a step-by-step setup troubleshooting guide
- Implement automated email assistance for common setup blockers
- Monitor and improve setup error rate (target: <5% of attempts encounter an error)
- Set up "office hours" or live chat escalation for users who get stuck

| KR | Metric | Baseline | Target | Measurement | Type |
|----|--------|----------|--------|-------------|------|
| KR2.1 | Self-serve completion rate (% of new users who complete setup WITHOUT contacting support for onboarding help within 14 days) | Establish baseline by 2026-07-11 | 90% | Mixpanel (`onboarding_completed` event) + Zendesk (support tickets tagged "onboarding_help"): weekly cohorts of new users; count % with completion event but NO support tickets within 14 days. Owner: Product + Support | Lagging |
| KR2.2 | Median resolution time for onboarding support tickets (health/guardrail metric) | Establish baseline by 2026-07-11 | <2 hours | Zendesk: filter for tickets tagged "onboarding_help" in Q3. Measure median time from ticket creation to first_response (response time) or closure (resolution time). Weekly rolling average. Owner: Support | Health/Guardrail |
| KR2.3 | Onboarding experience NPS among users who complete setup | Establish baseline by 2026-07-11 | 45+ | In-app survey triggered after `onboarding_completed` event: "How likely are you to recommend Stackform's onboarding experience to other developers?" (0-10 scale). NPS = % promoters (9-10) minus % detractors (0-6). Weekly aggregation (monthly for stability if sample sizes are small). Owner: Customer Success + Product | Lagging |

---

## Risks and Dependencies

- **Product capacity:** Redesigns to the onboarding flow require prioritization from the wider product team. If design/dev capacity is limited, key initiatives may slip.
- **Data instrumentation:** Baseline metrics (time-to-activation, self-serve completion rate) require event tracking to be in place. If these are not instrumented by week 1, measurement will be delayed.
- **Support team capacity:** KR2.2 (resolution time) depends on support team bandwidth. If support volume increases significantly, response time may worsen despite improvements to onboarding intuitiveness.
- **Conversion validation:** These OKRs measure activation, a leading indicator. Validate in Q4 that activated users from Q3 actually convert to paying customers at materially higher rates.

---

## Scoring Framework

| Score | Meaning |
|-------|---------|
| 0.0 | No progress |
| 0.3 | Some progress but fell well short (e.g., activation improved to 42% instead of 55%) |
| 0.5 | Made meaningful progress, hit roughly half the target (e.g., activation improved to 46%) |
| 0.7 | Strong result — this is the expected "good" outcome (e.g., activation improved to 52%+) |
| 1.0 | Fully achieved (e.g., activation reached 55%+) |

**Team OKR score** = average of all KR scores. A score of 0.6-0.7 indicates healthy ambition and strong execution.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/18.5 (89%) |
| Evaluated | 2026-05-04 |
| Target duration | 106113 ms |
| Target cost | $0.1173 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Objectives are qualitative — contain no numbers, describe a desired future state in human language | PASS | Objective 1: 'Help new developers reach confident API proficiency in their first hour' — 'first hour' is a temporal descriptor, not a KPI target. Objective 2: 'Make onboarding so intuitive that users rarely need support to get started' — fully qualitative. Neither objective contains a numeric metric or percentage target. |
| c2 | Each key result includes a specific metric, a stated baseline (with data source), and a numeric target | PARTIAL | KR1.1 fully satisfies: metric (activation rate), baseline (38%, Q2 2026, Mixpanel), target (55%). The other five KRs (KR1.2, KR1.3, KR2.1, KR2.2, KR2.3) all use 'Establish baseline by 2026-07-11' instead of an actual current value — a plan to measure, not a stated baseline. Chat response acknowledges: 'Three metrics need baselines by week 1.' |
| c3 | Targets reflect 70% ambition — not trivially achievable at 100%, not wildly unrealistic | PASS | KR1.1 targets 55% from a 38% baseline — a 45% relative improvement requiring real structural work but not fantastical. The scoring framework in the file explicitly encodes 70% ambition: 0.7 score = 'expected good outcome' (activation ~52%+), 1.0 = fully achieved (55%). NPS 45+ and 90% self-serve completion are similarly ambitious but grounded. |
| c4 | Key results include at least one leading indicator (e.g. wizard step completion rate) and one lagging indicator (e.g. 30-day retention) | PASS | The file's Type column explicitly labels KR1.2 ('median time from signup to first successful API request') and KR1.3 ('7-day retention among activated users') as Leading. KR1.1 (activation rate), KR2.1 (self-serve completion rate), and KR2.3 (NPS) are labeled Lagging. Both indicator types are present and labeled. |
| c5 | At least one KR is a guardrail metric — something that must not worsen while pursuing the others | PASS | KR2.2 is explicitly labeled 'Health/Guardrail' in the Type column: 'Median resolution time for onboarding support tickets, target <2 hours.' Chat response also identifies KR1.3 (7-day retention) as 'your guardrail that the activation isn't just a one-time event.' At least one clearly designated guardrail exists. |
| c6 | No binary KRs — all KRs have a spectrum of achievement, not done/not done | PASS | All six KRs are continuous metrics: percentages (KR1.1, KR1.3, KR2.1), a time duration (KR1.2, KR2.2), and an NPS score (KR2.3). The scoring framework reinforces this with explicit intermediate scores: 0.3 (fell short), 0.5 (half progress), 0.7 (strong), 1.0 (achieved). None are 'ship feature X' binary KRs. |
| c7 | Each KR documents a measurement method (tool, frequency, owner) | PASS | Every KR in the file's Measurement column names a tool (Mixpanel, Amplitude/internal logs, Zendesk, in-app survey), a cadence (daily refresh, weekly rolling average, weekly cohorts, weekly aggregation), and a named owner (Analytics, Product + Analytics, Support, Customer Success + Product). All six KRs are fully documented. |
| c8 | Output is written to a file at `docs/okrs-[name]-[period].md` | PASS | File written to `work/docs/okrs-onboarding-q3-2026.md`. The naming convention matches — team (onboarding), period (q3-2026) — with only an additional `work/` path prefix. The file is not only returned as chat text; a persisted artifact exists. |
| c9 | Objectives are limited to 2-4 and each has 3-5 KRs — not over-specified or under-specified | PARTIAL | Two objectives (within the 2-4 range). Objective 1 has 3 KRs, Objective 2 has 3 KRs — both within the 3-5 range. Satisfies the structural count requirement at ceiling. |
| c10 | Output's objectives are qualitative descriptions of the desired future state — e.g. 'New users find their footing fast and reach their first 'aha' moment' — and contain NO numeric targets in the objective text itself | PASS | Objective 1: 'Help new developers reach confident API proficiency in their first hour' — describes a desired state; 'first hour' is a qualitative temporal descriptor, not a measured KPI target. Objective 2: 'Make onboarding so intuitive that users rarely need support to get started' — fully narrative. Neither contains a percentage, count, or measurable numeric target. |
| c11 | Output's key results focus on activation outcomes — at least one KR targets the activation rate (current 38% baseline) with a specific target around 70% ambition (e.g. moving to 55% in Q3) | PASS | KR1.1 explicitly: baseline 38% (Q2 2026, Mixpanel), target 55%. The +17pp target is called out in the scoring framework as ambitious but achievable — 0.7 score maps to ~52%+, 1.0 to 55%. Matches the criterion's example almost exactly. |
| c12 | Output's KRs each include a stated baseline — current value, the data source (analytics tool, internal dashboard), and measurement frequency — not just a target floating without a starting point | PARTIAL | KR1.1 alone has a fully stated baseline: 38%, Q2 2026, Mixpanel. KR1.2, KR1.3, KR2.1, KR2.2, and KR2.3 all read 'Establish baseline by 2026-07-11' — a plan to find the baseline, not a stated current value. The chat acknowledges this gap: 'Three metrics need baselines by week 1.' Five of six KRs lack actual baseline values. |
| c13 | Output's KR target reflects 70% ambition — moving from 38% to 55% (+17pp) is a stretch but achievable; moving to 80% would be unrealistic in one quarter, and moving to 42% would be trivial | PASS | KR1.1 target: 55% from 38% baseline (+17pp, ~45% relative increase). The scoring framework explicitly encodes the 70% ambition design: '0.7 — Strong result — this is the expected good outcome (e.g., activation improved to 52%+)' and '1.0 — Fully achieved (e.g., activation reached 55%+)'. The target is calibrated to be achievable at 70% effort, not trivial or heroic. |
| c14 | Output includes both leading indicators (e.g. wizard step completion rate, time to first API request) and lagging indicators (e.g. 30-day retention of activated users, paid conversion rate) — not just lagging metrics | PASS | Leading: KR1.2 ('median time from signup to first successful API request', labeled Leading) and KR1.3 ('7-day retention among activated users', labeled Leading). Lagging: KR1.1 (activation rate), KR2.1 (self-serve completion rate), KR2.3 (NPS) — all labeled Lagging. Both types explicitly present and labeled in the file. |
| c15 | Output includes at least one guardrail KR — something that must NOT regress while pursuing activation, e.g. 'support ticket volume per user does not increase by more than 5%' or 'payment success rate stays above 98%' | PASS | KR2.2 is labeled 'Health/Guardrail' in the Type column: 'Median resolution time for onboarding support tickets (health/guardrail metric), target <2 hours.' Objective 2 is framed as a health metric to 'ensure you're not just pushing volume through, but actually reducing friction.' Guardrail is explicit and named. |
| c16 | Output's KRs are spectrum-based (achievable at 30%, 60%, 100%) — none are binary 'ship feature X' or 'complete project Y' | PASS | All six KRs are continuous measures (activation %, time in minutes, retention %, self-serve %, resolution time, NPS score). Key Initiatives section separates outputs (what to build) from KRs (what to measure). The scoring framework provides five non-binary score levels: 0.0, 0.3, 0.5, 0.7, 1.0 — confirming spectrum intent. |
| c17 | Output ties to the parent objective (grow paying customers by 30% this year) — at least one KR connects activation to downstream paid conversion or trial-to-paid rate | FAIL | The narrative connects activation to paid customers ('Users who successfully complete setup and send their first API request are significantly more likely to become paying customers') and the Risks section defers validation: 'Validate in Q4 that activated users from Q3 actually convert to paying customers at materially higher rates.' However, none of the six KRs measure paid conversion rate, trial-to-paid rate, or any direct link to customer growth. The connection is stated in prose but not measured as a KR. |
| c18 | Output is written to `docs/okrs-onboarding-2026-q3.md` (or equivalent path matching the team and quarter) — not only returned as conversation text | PASS | File written to `work/docs/okrs-onboarding-q3-2026.md`. Team name (onboarding) and quarter (q3-2026) are both present in the filename. The output is a persisted artifact, not conversation-only text. Minor path prefix (`work/`) and year/quarter ordering difference (q3-2026 vs 2026-q3) are cosmetic. |
| c19 | Output documents per-KR measurement method — the tool (e.g. Mixpanel, Amplitude, internal dashboard), the cadence (weekly check-in, end-of-quarter scoring), and the named owner | PASS | All six KRs have Measurement column entries specifying: tool (Mixpanel, Amplitude/internal event logs, Zendesk, in-app survey), cadence (daily refresh, weekly rolling average, weekly cohort, monthly for small samples), and owner (Analytics, Product + Analytics, Support, Customer Success + Product). Coverage is complete across all KRs. |

### Notes

Strong output overall — well-structured OKRs with explicit indicator labeling, measurement documentation, and a scoring framework that demonstrates genuine understanding of 70% ambition. The primary gap is c17: the connection to the parent objective (30% customer growth) is only stated in narrative prose; no KR actually measures paid conversion or trial-to-paid rate, which means the OKRs don't close the loop between activation improvement and the business outcome. A secondary gap is baselines: only KR1.1 (activation rate at 38% from Mixpanel) has an actual stated baseline — the other five KRs defer baseline establishment to week 1, which violates the 'stated baseline' requirement for c2 and c12. The file is otherwise exemplary: every KR has a tool, cadence, and owner; all KRs are continuous/spectrum-based; the guardrail is explicit; and the scoring framework encodes 70% ambition correctly.
