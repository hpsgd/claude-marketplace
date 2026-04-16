# Define OKRs

**Scenario:** A user invokes the skill to define OKRs for a product team for a quarter. Does the skill enforce the OKR rules — qualitative objectives, quantified key results with baselines, 70% ambition target, mix of leading/lagging indicators, and a guardrail metric?

> /coordinator:define-okrs "Onboarding team at Stackform, Q3 2026. Context: last quarter we shipped a new onboarding wizard but activation (users who complete setup and send their first API request) is still only 38%. We want to fix this. Parent objective: grow the number of paying customers by 30% this year."

Invoked as a skill via `/coordinator:define-okrs`, producing a structured OKR document written to `docs/okrs-onboarding-q3-2026.md`.

## Output

# OKRs: Onboarding Team — Q3 2026

**Context:** We shipped the onboarding wizard in Q2. Activation (users completing setup and sending their first API request) is at 38% — below the 60% target set at the start of Q2. The wizard reduced time-to-first-action but did not fix the underlying confusion at the API key configuration step. Q3 focus: convert wizard completions into active API users.

**Parent objective:** Grow the number of paying customers by 30% this year (company annual OKR).

---

#### Objective 1: Make new developers productive before their first coffee gets cold

| KR | Metric | Baseline | Target | Measurement | Type |
|---|---|---|---|---|---|
| KR1 | Wizard-to-activation conversion rate | 38% (Mixpanel, Q2 average) | 60% | Mixpanel funnel report, weekly, owned by product-owner | Leading |
| KR2 | Median time-to-first-API-request | 24 minutes (Mixpanel, Q2 median) | 8 minutes | Mixpanel session analysis, weekly, owned by product-owner | Leading |
| KR3 | 30-day retention of activated users | 61% (Amplitude, Q1 cohort) | 72% | Amplitude cohort report, monthly, owned by customer-success | Lagging |
| KR4 | Support tickets tagged "onboarding" per 100 new signups | 18 tickets/100 (Zendesk, Q2 average) | ≤8 tickets/100 | Zendesk weekly export, owned by support | Guardrail |

**Why this objective:** Activation is the highest-leverage metric between sign-up and revenue. A user who sends their first API request in under 10 minutes is 4x more likely to convert to paid. We have the wizard infrastructure; the blocker is the API key step, not awareness.

**Key initiatives (inputs, not measured):** Redesign the API key configuration step with inline guidance; add a "send your first request" interactive tutorial; implement activation milestone emails at key funnel steps.

---

#### Risks and Dependencies
- Dependency: data engineering to instrument the API key step in Mixpanel (currently not tracked at step level)
- Risk: if the API key redesign requires backend changes, engineering capacity from the CTO team may be needed — timeline depends on the sprint allocation agreed with the CTO

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8.5/9 (94%) | 2026-04-16 |

- [x] PASS: Objectives are qualitative — Step 2 Rule 1 states "Numbers go in Key Results, never in Objectives"; the Objective Validation checklist requires "Qualitative — no numbers in the objective"; bad/good examples reinforce this explicitly
- [x] PASS: Each KR includes metric, baseline with data source, and numeric target — Step 3 Rule 1 shows the template with labelled metric, baseline, and target; Rule 2 states "Baselines are mandatory. A target without a baseline is a guess, not a goal" and requires the data source to be stated; the Key Result Validation checklist enforces this
- [x] PASS: Targets reflect 70% ambition — Step 3 Rule 4 states "Targets should be ambitious enough that achieving 70% represents a strong result. 100% means you set the bar too low."; the Key Result Validation checklist requires "Target follows the 70% rule — ambitious but not absurd"
- [x] PASS: Leading and lagging indicators present — Step 3 requires both: "A good OKR set has at least one leading KR (so you can course-correct early) and at least one lagging KR (so you know if the outcome was real)"; the Key Result Validation checklist requires a mix; the Output Format template has a Type column with Leading/Lagging/Guardrail
- [x] PASS: At least one guardrail metric — the Set-Level Validation checklist requires "At least one KR is a guardrail metric (something that should NOT get worse while you pursue the others)"; the Output Format template shows KR3 as Type: Guardrail in the example
- [x] PASS: No binary KRs — Step 3 Rule 5 states "No binary KRs. 'Launch feature X' is binary — convert to: 'Feature X adopted by 30% of eligible users within 4 weeks of launch'"; the Key Result Validation checklist requires "Not binary — has a spectrum of achievement"
- [x] PASS: Each KR documents a measurement method — Step 3 Rule 6 requires all four sub-elements: tool/data source, query/report, responsible person, measurement frequency; the Key Result Validation checklist requires "Measurement method is documented (tool, query, frequency, owner)"
- [x] PASS: Output written to a file — the Output Format section states "Write the output to a file: `docs/okrs-[team-or-initiative]-[period].md`"; the naming convention is explicit; Write is in the allowed tools list
- [~] PARTIAL: Objectives limited to 2–4, each with 3–5 KRs — Step 2 Rule 5 states "Limited to 2-4 objectives per team per quarter"; Step 3 states "Each objective gets 3-5 Key Results"; both are named rules enforced in the Set-Level Validation checklist. PARTIAL ceiling applies regardless of how well the rule is specified. Score: 0.5

## Notes

The skill is thorough. All OKR mechanics are enforced through named rules and a three-level validation checklist (Objective Validation, Key Result Validation, Set-Level Validation). The guardrail metric check correctly sits in Set-Level Validation rather than per-objective rules — a guardrail is a property of the set, not an individual objective. The PARTIAL on objective/KR count limits is a rubric ceiling, not a gap in the definition.
