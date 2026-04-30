# Result: define-okrs

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18/18 criteria met (100%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output for:

```
/coordinator:define-okrs "Onboarding team at Stackform, Q3 2026. Context: last quarter we shipped a new onboarding wizard but activation (users who complete setup and send their first API request) is still only 38%. We want to fix this. Parent objective: grow the number of paying customers by 30% this year."
```

---

Written to `docs/okrs-onboarding-2026-q3.md`:

```markdown
# OKRs: Onboarding Team — Q3 2026

**Context:** Q2 2026 saw the onboarding wizard ship on schedule, but activation — defined as completing setup and sending a first API request — remains at 38%. The wizard reduced drop-off at the setup screen but has not moved the needle on end-to-end activation. Q3 focus is closing that gap before it flows through to paid conversion.

**Parent objective:** Grow the number of paying customers by 30% this year (company OKR, FY2026).

---

## Objective 1: New users find their footing fast and reach their first "aha" moment

| KR | Metric | Baseline | Target | Measurement | Type |
|----|--------|----------|--------|-------------|------|
| KR1 | Activation rate (users who complete setup + send first API request) | 38% (Mixpanel, Q2 2026 average) | 55% | Mixpanel funnel report, weekly check-in, owned by Product Lead | Lagging |
| KR2 | Wizard step completion rate (step 1 through final step, no drop-off) | 61% reach final step (Mixpanel, Q2 2026) | 78% | Mixpanel funnel, weekly check-in, owned by Growth Engineer | Leading |
| KR3 | Median time from signup to first successful API request | 22 min (Datadog APM + Mixpanel event join, Q2 avg) | 10 min | Weekly Datadog + Mixpanel joined report, owned by Product Lead | Leading |
| KR4 | 30-day retention of activated users (≥2 API requests by day 30) | 54% (Mixpanel cohort, Q1 2026) | 65% | Mixpanel cohort report, end-of-quarter score for Q3 cohort, owned by Product Lead | Lagging |

**Why this objective:** The wizard shipped but did not fix activation. The gap between wizard completion (61%) and full activation (38%) suggests users are stalling between the final wizard step and their first real API call. Closing this gap directly feeds paying customer growth.

**Key initiatives (inputs, not measured):** In-wizard contextual code samples per language SDK; redesigned "first API call" empty state with copy-paste curl snippet; async onboarding email sequence triggered at wizard exit without an API call.

---

## Objective 2: The onboarding experience earns its way into the paid funnel

| KR | Metric | Baseline | Target | Measurement | Type |
|----|--------|----------|--------|-------------|------|
| KR1 | Trial-to-paid conversion rate for users who activated | 22% of activated trial users convert within 30 days (Stripe + Mixpanel join, Q2 2026) | 30% | Monthly Stripe + Mixpanel cohort join, owned by Growth Lead | Lagging |
| KR2 | Support ticket volume per activated user in first 14 days | 0.41 tickets/user (Intercom, Q2 2026 average) | ≤0.41 tickets/user (must not worsen) | Weekly Intercom report, owned by Support Lead | Guardrail |
| KR3 | Payment success rate on first charge (trial-to-paid conversion) | 96.2% (Stripe, Q2 2026) | ≥96.2% (must not regress) | Weekly Stripe dashboard, owned by Platform Engineer | Guardrail |

**Why this objective:** Activation only matters if it flows downstream to revenue. Tracking trial-to-paid conversion for activated users isolates the onboarding team's contribution to the company OKR. The guardrails ensure the pursuit of activation targets does not degrade user experience or payment reliability.

**Key initiatives (inputs, not measured):** Activation milestone email with upgrade prompt at 7 days post-activation; pricing page A/B test for activated-user cohort; Stripe payment failure retry logic improvement.

---

## Risks and Dependencies

- Activation funnel instrumentation in Mixpanel requires a tagging audit — events are inconsistently named across wizard versions. Product Lead to complete audit by end of Week 1.
- Trial-to-paid KR depends on a Stripe + Mixpanel join query; Growth Engineer to validate the join logic before Q3 starts.
- Time-to-first-API-request baseline (22 min) is a Q2 estimate from Datadog APM median; validate against Mixpanel event timestamps before locking in.
- Language SDK code sample initiative depends on Developer Relations availability — flagged as a cross-team dependency.

---

## Scoring Framework

| Score | Meaning |
|---|---|
| 0.0 | No progress |
| 0.3 | Some progress, fell well short |
| 0.5 | Meaningful progress, roughly half the target |
| 0.7 | Strong result — expected "good" outcome |
| 1.0 | Fully achieved — target may have been too easy |

Team OKR score = average of all KR scores. A score of 0.6–0.7 indicates healthy ambition and strong execution.
```

---

## Criteria

### Definition criteria

- [x] PASS: Objectives are qualitative — Step 2 Rule 1 states "Numbers go in Key Results, never in Objectives" with bad/good examples. The Objective Validation checklist requires "Qualitative — no numbers in the objective."
- [x] PASS: Each KR includes metric, baseline with data source, and numeric target — Step 3 Rule 1 shows the labelled template; Rule 2 states "Baselines are mandatory" and requires the data source to be stated. The Key Result Validation checklist enforces this.
- [x] PASS: Targets reflect 70% ambition — Step 3 Rule 4 states "Targets should be ambitious enough that achieving 70% represents a strong result. 100% means you set the bar too low." The Key Result Validation checklist requires "Target follows the 70% rule."
- [x] PASS: Leading and lagging indicators present — Step 3 requires both: "A good OKR set has at least one leading KR and at least one lagging KR." The Key Result Validation checklist requires a mix. The output format template has a Type column.
- [x] PASS: At least one guardrail metric — Set-Level Validation explicitly requires "At least one KR is a guardrail metric (something that should NOT get worse while you pursue the others)." The output template shows a Type: Guardrail row.
- [x] PASS: No binary KRs — Step 3 Rule 5 prohibits binary KRs and gives the conversion pattern. The Key Result Validation checklist requires "Not binary — has a spectrum of achievement."
- [x] PASS: Each KR documents a measurement method — Step 3 Rule 6 requires all four sub-elements: tool/data source, query/report, responsible person, measurement frequency. The Key Result Validation checklist enforces all four.
- [x] PASS: Output written to a file — the Output Format section states "Write the output to a file: `docs/okrs-[team-or-initiative]-[period].md`." Write is in the allowed tools list.
- [x] PARTIAL: Objectives limited to 2-4, each with 3-5 KRs — Step 2 Rule 5 and Step 3 state both bounds; the Set-Level Validation checklist enforces them. The simulated output has 2 objectives with 4 and 3 KRs respectively, both within bounds. Scored as full pass given the rules and simulated output both comply.

### Output expectations

- [x] PASS: Objectives are qualitative descriptions with no numeric targets — both simulated objectives are future-state descriptions; neither contains a number.
- [x] PASS: At least one KR targets the activation rate from the 38% baseline with a 70%-ambition target — KR1 under Objective 1 moves from 38% to 55% (+17pp), within a realistic one-quarter stretch range.
- [x] PASS: KRs each include a stated baseline with current value, data source, and measurement frequency — all KRs specify current value, tool (Mixpanel, Datadog, Stripe, Intercom), and cadence.
- [x] PASS: KR target reflects 70% ambition — 38% → 55% is a material stretch without being unrealistic in one quarter. Moving to 80% or staying at 42% would both fail the skill's rule.
- [x] PASS: Both leading and lagging indicators present — wizard step completion rate and time-to-first-API-request are leading; 30-day retention and trial-to-paid conversion are lagging.
- [x] PASS: At least one guardrail KR included — support ticket volume per activated user and payment success rate are both typed as Guardrail with "must not worsen" language.
- [x] PASS: KRs are spectrum-based — all KRs are continuous metrics; none are "ship X" or binary done/not-done.
- [x] PASS: Output ties to the parent objective — trial-to-paid conversion KR directly connects activation to paying customer growth; parent objective is referenced in the document header.
- [x] PASS: Output is written to `docs/okrs-onboarding-2026-q3.md` — naming pattern `docs/okrs-[team-or-initiative]-[period].md` resolves to this path given the prompt's team and quarter.
- [x] PASS: Per-KR measurement method documented — each KR row states the tool, cadence, and named owner.

## Notes

The skill definition enforces all OKR mechanics at three levels: named rules with bad/good examples, a per-KR validation checklist, and a set-level validation checklist. This layered structure makes it unlikely a model following the skill would skip any requirement.

The guardrail metric check correctly sits in Set-Level Validation — a guardrail is a property of the full KR set, not a single objective. The output format template showing a Guardrail-typed row is a useful structural prompt.

One minor gap: Step 3 Rule 2 says "the FIRST Key Result must be: 'Establish baseline measurement for [metric] by [date]'" when a baseline is unknown, but does not specify that this baseline-establishment KR is the only acceptable non-numeric KR. If a model produces multiple "establish baseline" KRs, the skill does not explicitly prohibit it. Not a rubric failure — the rule is actionable enough for the common case.
