# Result: define-okrs

**Verdict:** PASS
**Score:** 18/18.5 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Objectives are qualitative — met. Step 2 Rule 1 states "Numbers go in Key Results, never in Objectives"; bad/good examples reinforce this; the Objective Validation checklist requires "Qualitative — no numbers in the objective."
- [x] PASS: Each KR includes metric, baseline with data source, and numeric target — met. Step 3 Rule 1 shows the labelled template; Rule 2 states "Baselines are mandatory. A target without a baseline is a guess, not a goal" and requires the data source to be stated; the Key Result Validation checklist enforces this.
- [x] PASS: Targets reflect 70% ambition — met. Step 3 Rule 4 states "Targets should be ambitious enough that achieving 70% represents a strong result. 100% means you set the bar too low"; the Key Result Validation checklist requires "Target follows the 70% rule."
- [x] PASS: Leading and lagging indicators present — met. Step 3 requires both: "A good OKR set has at least one leading KR... and at least one lagging KR"; the Key Result Validation checklist requires a mix; the Output Format template has a Type column.
- [x] PASS: At least one guardrail metric — met. The Set-Level Validation checklist requires "At least one KR is a guardrail metric (something that should NOT get worse while you pursue the others)"; the Output Format template shows a Type: Guardrail KR.
- [x] PASS: No binary KRs — met. Step 3 Rule 5 states "No binary KRs. 'Launch feature X' is binary — convert to: 'Feature X adopted by 30% of eligible users within 4 weeks of launch'"; the Key Result Validation checklist requires "Not binary — has a spectrum of achievement."
- [x] PASS: Each KR documents a measurement method — met. Step 3 Rule 6 requires all four sub-elements: tool/data source, query/report, responsible person, measurement frequency; the Key Result Validation checklist enforces all four.
- [x] PASS: Output written to a file — met. The Output Format section states "Write the output to a file: `docs/okrs-[team-or-initiative]-[period].md`"; the naming convention is explicit; Write is in the allowed tools list.
- [~] PARTIAL: Objectives limited to 2-4, each with 3-5 KRs — partially met. Step 2 Rule 5 states "Limited to 2-4 objectives per team per quarter"; Step 3 states "Each objective gets 3-5 Key Results"; both are named rules enforced in the Set-Level Validation checklist. The floor (minimum 3 KRs) and ceiling (maximum 4 objectives, 5 KRs) are both present but enforcement is checklist-based, not automatic. Score 0.5.

### Output expectations

- [x] PASS: Output's objectives are qualitative descriptions of the desired future state with no numeric targets — met. Step 2 Rule 1 and its bad/good examples directly enforce this. The skill would produce objectives like "Make new users productive on day one," not "Increase activation from 38% to 55%."
- [x] PASS: Output's KRs focus on activation outcomes with a specific target reflecting 70% ambition from the 38% baseline — met. The skill requires all KRs to state the baseline with source, apply the 70% rule, and measure outcomes not outputs. Given the 38% baseline stated in the prompt, the skill would produce a KR targeting approximately 55% activation — a stretch but not absurd.
- [x] PASS: Output's KRs each include a stated baseline with current value, data source, and measurement frequency — met. Step 3 Rule 2 is explicit: "state it with the data source: 'Current: 14 min (measured via Mixpanel, Q4 average)'"; Rule 6 requires tool, query, frequency, and owner for every KR.
- [x] PASS: Output's KR target reflects 70% ambition — moving from 38% to ~55% is stretch but achievable; moving to 80% or to 42% would both fail the 70% rule — met. The skill's Rule 4 and the Key Result Validation checklist enforce this range explicitly, and the scoring framework (0.7 = strong result) reinforces it.
- [x] PASS: Output includes both leading indicators (wizard step completion, time to first API request) and lagging indicators (30-day retention, paid conversion) — met. Step 3's Leading vs. Lagging Indicators section gives exactly these examples as illustrations; the Output Format template includes a Type column; the Key Result Validation checklist requires the mix.
- [x] PASS: Output includes at least one guardrail KR — met. Set-Level Validation checklist requires it; the output template shows a Guardrail-typed KR in the example table. The skill would produce something like "support tickets tagged 'onboarding' per 100 signups must not increase."
- [x] PASS: Output's KRs are spectrum-based, not binary — met. Step 3 Rule 5 prohibits binary KRs and gives the conversion pattern; the Key Result Validation checklist enforces "Not binary — has a spectrum of achievement."
- [x] PASS: Output ties to the parent objective (grow paying customers 30% this year) — met. Step 1 Rule 3 states "Every team OKR should visibly connect to a company or department objective"; the Output Format includes a "Parent objective" field; the prompt includes the parent objective explicitly.
- [x] PASS: Output is written to `docs/okrs-onboarding-2026-q3.md` (or equivalent) — met. The Output Format section specifies the exact naming pattern `docs/okrs-[team-or-initiative]-[period].md`; Write is in the allowed tools list; the prompt supplies the team name and quarter.
- [x] PASS: Output documents per-KR measurement method with tool, cadence, and named owner — met. Step 3 Rule 6 requires all four elements (tool, query, responsible person, frequency); the output template's Measurement column holds these; the Key Result Validation checklist enforces it.

## Notes

The skill is thorough and well-structured across all criteria. All OKR mechanics are enforced at three levels: named rules with bad/good examples, a per-KR validation checklist, and a set-level validation checklist. The guardrail metric check correctly sits in Set-Level Validation — a guardrail is a property of the whole set, not a single objective. The PARTIAL on the 2-4 objective / 3-5 KR count criterion reflects that the skill enforces it through a checklist the model runs, not through a structural constraint that prevents over-specification — the rubric ceiling applies, not a genuine gap in coverage.
