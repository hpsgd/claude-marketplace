# Result: expansion plan for a healthy account

| Field | Value |
|---|---|
| **Verdict** | FAIL |
| **Score** | 9.5/17 criteria met (56%) |
| **Evaluated** | 2026-04-29 |
| **Skill source** | `plugins/product/customer-success/skills/expansion-plan/SKILL.md` |

## Results

### Criteria section

- [x] PASS: Health prerequisite check passes and expansion planning proceeds — Step 1 is a mandatory gate with an explicit >= 70 threshold and four sub-conditions. Score 85, no churn signals, goals achieved (40% time savings), three QBRs of engagement all clear the gate.
- [x] PASS: Expansion is framed as customer enablement, not a sales motion — Step 4 is a dedicated "Frame as Enablement" section with a BAD/GOOD contrast table. Anti-Patterns explicitly prohibit "Sales framing."
- [x] PASS: The specific signal (customer asking about API tier) is used as the expansion anchor — Step 2 signal table maps "Requesting higher-tier features" to Upsell; rules require organic, customer-driven signals; the skill directs using the signal as the entry point in Step 6 Step 3.
- [ ] FAIL: Revenue impact is estimated with assumptions stated — Step 3 asks for an Estimated expansion ARR figure and a Confidence level, but does not instruct the agent to show the underlying pricing assumption, seat count, or adoption-scenario math. The template outputs a single dollar figure, not a worked calculation with stated assumptions.
- [x] PASS: A timeline with milestones is produced — Step 6 is a five-row Action/Owner/Date execution table; Step 5 Timing Strategy adds milestone triggers. Anti-Patterns prohibit vague framing.
- [~] PARTIAL: Risk factors for the expansion are identified — Adoption risk appears in Anti-Patterns and is tracked in Step 7 success criteria, but there is no dedicated risk section or output field. Risk is embedded rather than surfaced as a named deliverable.
- [x] PASS: The plan references the customer's demonstrated value as proof of readiness — Step 6 Step 1 explicitly instructs a value summary of customer achievements; Step 4 enablement framing connects expansion to already-realised outcomes.

### Output expectations section

- [x] PASS: Output's health prerequisite check passes explicitly — Step 1 requires checking all four conditions; Meridian's data satisfies each. The output template's Health Check section has an explicit "Clear to expand: Yes/No" field.
- [x] PASS: Output uses customer's specific request (API integration tier) as expansion anchor — Step 2 signal rules require organic, customer-driven signals; the inquiry maps directly to "Requesting higher-tier features." The skill anchors on that signal via the Approach/Trigger field.
- [ ] FAIL: Output's revenue impact estimate is shown with assumptions and math — Step 3 collects an ARR estimate and confidence level, but the skill does not instruct the agent to show per-seat pricing, seat count, or adoption-scenario math. The worked calculation this criterion requires is not directed.
- [x] PASS: Output's enablement-not-sales framing is visible — Step 4 framing table, Anti-Patterns, and the "Framing" field in the output template collectively ensure the recommendation discusses what API integration unlocks, not revenue growth.
- [ ] FAIL: Output's timeline has milestones of the required granularity — the Execution Plan table structure (Step/Action/Owner/Date) exists, but the skill does not instruct week-level granularity or require technical scoping, trial, and production rollout stages as discrete milestones. Generic structure only.
- [ ] FAIL: Output references the 40% time-savings as the "ready for more" signal — Step 6 Step 1 says prepare a value summary, but the skill does not explicitly instruct the agent to connect QBR-proven value to the expansion ask as the readiness signal. Implied at best.
- [ ] FAIL: Output identifies adoption risks specific to the API tier — the Anti-Patterns block warns generically about "expanding without adoption," but the skill does not instruct diagnosis of whether the customer has engineering capacity to consume the tier, or gate the upsell on confirming technical readiness.
- [ ] FAIL: Output addresses renewal context — the skill has no instruction to situate expansion ahead of the renewal cycle or discuss how it sets up the renewal conversation. This dimension is entirely absent from the process and output template.
- [ ] FAIL: Output names the AE / CSM owner explicitly — the Execution Plan table has an "Owner" column but the skill only supplies role labels ("CSM," "CSM + Sales"), not a named individual. The criterion requires naming the specific responsible CSM.
- [~] PARTIAL: Output addresses cross-sell beyond the API tier — Step 2 includes "New use cases emerging" as a cross-sell signal and the Expansion Signals table would capture it, but the skill does not instruct the agent to flag downstream cross-sell opportunities as future-gated expansion. Weak partial match.

## Notes

The skill's structural process is sound: the mandatory health gate, signal identification, enablement framing, and execution plan are all present. Criteria that test for structural soundness mostly pass.

The failures cluster in output depth. The skill does not require the agent to show revenue math with assumptions, produce week-granularity milestones, name the responsible CSM, connect QBR value explicitly to the expansion readiness narrative, assess technical readiness for the specific tier, or address renewal context. These are gaps in the prompt instructions, not missing process steps.

The output format template is also sparse — it provides column headers but gives no guidance on required detail per field, leaving the agent free to produce a thin plan that technically populates the template without satisfying the richer output expectations. The prior evaluation (2026-04-24) scored this PASS at 93% against the Criteria-only rubric, which was accurate for that narrower set. The full rubric including Output expectations reveals the depth gaps.
