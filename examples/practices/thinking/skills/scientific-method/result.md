# Result: scientific-method performance investigation

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16.5 / 18 criteria met (91.7%) |
| **Evaluated** | 2026-04-29 |
| **Skill source** | `plugins/practices/thinking/skills/scientific-method/SKILL.md` |

## Results

### Criteria

- [x] PASS: Step 1 defines a measurable goal with current state, target state, and how success is measured — met: template has `**Current state:**`, `**Target state:**`, `**How to measure:**` fields; rules explicitly require "a number or a binary pass/fail condition"
- [x] PASS: Step 2 observes and records current facts before forming hypotheses — met: observation table precedes hypotheses; template includes `**What has been tried before:**`, `**What measurements exist:**`, `**What's missing:**`; rules frame observation as a pre-hypothesis step
- [x] PASS: Step 3 generates a minimum of 3 distinct, falsifiable hypotheses — met: template shows H1–H3 rows; rules state "Minimum 3 hypotheses. If you can only think of one, you don't understand the problem yet"; falsifiability is required
- [x] PASS: Each hypothesis includes "if true, expect to see" and "if false, expect to see" columns — met: hypothesis table has explicit `If true, expect to see` and `If false, expect to see` columns; rules call the "if false" column "the most important"
- [x] PASS: Step 4 experiment targets the highest-likelihood hypothesis with a single variable change and a pre-stated expected outcome — met: step 4 opens "For the highest-likelihood hypothesis"; template includes `**Variable (what changes):**`, `**Expected result if hypothesis is correct:**`, `**Expected result if hypothesis is wrong:**`
- [x] PASS: The skill enforces the rule that only one variable changes per experiment — met: step 4 rules state "Change ONE variable at a time. Changing multiple things makes results uninterpretable"; repeated in global Rules section and Quick Diagnosis Mode
- [x] PASS: Steps 5 and 6 are structured to record actual results vs predicted, and return a hypothesis verdict — met: step 5 has `**Expected outcome matched:** Yes / No / Partially`; step 6 has `**Hypothesis H[N] status:** Confirmed / Refuted / Inconclusive` and `**Distance from goal:**`
- [~] PARTIAL: Step 7 determines next action based on the verdict — partially met (fully met, capped at 0.5): step 7 maps all verdict branches explicitly — goal met → document; hypothesis refuted → return to Step 4; hypothesis confirmed but goal not met → return to Step 3; stuck → /first-principles. Both branches named in the criterion are present and correctly routed.

### Output expectations

- [x] PASS: Output's measurable goal is concrete — met: skill's own example in Step 1 rules reads "Reduce p95 latency from 800ms to under 200ms on the /api/search endpoint"; template enforces `**How to measure:**` field
- [x] PASS: Output's observations include specific facts and notes what's missing — met: observation table structure captures sourced observations; `**What's missing:**` field is explicit in the template
- [x] PASS: Output generates at least 3 distinct hypotheses — met: minimum-3 rule forces consideration beyond the two suspects the user named; "alternative explanation" and "another possibility" prompts in the template push for diverse hypotheses
- [x] PASS: Output's hypotheses each include "if true, expect to see" / "if false, expect to see" columns — met: these are explicit columns in the hypothesis table template
- [x] PASS: Output's experiment design changes ONE variable — met: single-variable rule is stated, enforced by template structure, and repeated in Quick Diagnosis Mode
- [x] PASS: Output prioritises the highest-likelihood hypothesis first — met: rules state "Rank by likelihood but test the most likely first, not the most interesting"; step 4 opens "For the highest-likelihood hypothesis"
- [x] PASS: Output's experiment has a pre-stated expected outcome — met: template requires `**Expected result if hypothesis is correct:**` and `**Expected result if hypothesis is wrong:**` to be filled before the experiment runs
- [x] PASS: Output's record-results step structures actual vs predicted — met: step 5 template captures `**What happened:**`, `**Expected outcome matched:**`, `**Quantitative result:**`; step 6 provides the verdict field
- [x] PASS: Output's verdict drives the next action explicitly — met: step 7 maps confirmed / refuted / inconclusive to explicit next actions with routing back to step 4 or step 3 as appropriate
- [ ] PARTIAL: Output addresses the rollback option — not met: the skill contains no mention of rollback, revert, or temporary mitigation. When the root cause is identified but a fix isn't immediate, the skill routes straight to "fix and document" with no intermediate path. The rollback-as-mitigation pattern is absent.

## Notes

The skill handles the two-deployment scenario well structurally. The single-variable rule prevents a common mistake: if both the query and cache layer are reverted or changed simultaneously, there's no way to attribute the result to either one. The minimum-3-hypotheses rule does the most important work here — the user named two suspects, and the rule forces at least one alternative.

The one real gap against the output expectations is the rollback path. When a confirmed hypothesis has no quick fix, reverting the causative deploy is a legitimate temporary mitigation that reduces customer impact while the proper solution is developed. The skill's Step 7 goes from "confirmed" directly to "fix and document" with no acknowledgment that the fix might take time. For a production latency regression, this is a meaningful omission.

The `**Time budget:**` field in step 4 has no guidance on reasonable defaults for latency investigations. Minor — the template prompts for a value but leaves the investigator without a reference point.
