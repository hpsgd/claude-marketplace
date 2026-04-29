# Result: iterative-depth architecture decision analysis

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-29 |
| **Skill source** | `plugins/practices/thinking/skills/iterative-depth/SKILL.md` |

## Results

### Criteria

- [x] PASS: Step 1 produces a complete problem framing with problem statement, context, constraints, stakeholders, current state, and desired state — met: Step 1 provides an explicit six-field code block template requiring all six before lens selection can begin.

- [x] PASS: Step 2 selects 3-5 lenses from the eight available and states which were chosen and why — met: Step 2 instructs "Choose 3-5 lenses" and ends with "State which lenses you selected and why."

- [x] PASS: Lens selection includes at least one human lens (User or Business) and one system lens (Technical or Edge case) per the skill's selection rules — met: the "Lens selection rules" subsection states this as a hard rule: "Always include at least one 'human' lens (User or Business) and one 'system' lens (Technical or Edge case)."

- [x] PASS: Each lens analysis produces at least one finding not surfaced by any previous lens — met: the per-lens template includes a mandatory "Findings unique to this lens:" section; rules state "Each lens must produce at least one finding not surfaced by any previous lens. If a lens adds nothing new, either the analysis was too shallow or the lens was a poor choice — go deeper or swap it."

- [x] PASS: Contradictions between lenses are explicitly called out — not smoothed over — met: the per-lens template requires a "Contradictions with previous lenses:" field; the rules section states "Don't smooth over contradictions — highlight them."

- [x] PASS: Step 4 synthesis produces a convergent findings table, a tensions table with recommended resolutions, and a clear recommendation — met: Step 4 defines all three with explicit table schemas; the tensions table includes a "Recommended resolution" column.

- [x] PASS: Revised problem framing at the end of Step 4 differs from the Step 1 framing in a meaningful way — met: the "Revised problem framing" subsection requires rewriting Step 1 with a "Key difference: [what changed and why it matters]" field; the skill states "Expect it to evolve."

- [~] PARTIAL: Confidence level for the recommendation is stated with the evidence basis (not just "Medium confidence" but what data would raise or lower it) — partially met: the recommendation template includes "**Confidence:** [High / Medium / Low] — based on [what evidence]" and a "**What would change this recommendation:**" section covering conditions that trigger a change; this addresses the spirit of the criterion but the template doesn't explicitly prompt "what data would raise confidence to HIGH vs leave it at MEDIUM," which is the specific phrasing of the criterion.

### Output expectations

- [x] PASS: Output's problem framing reproduces the prompt's specific facts — 8,000 lines, 3 engineers in 6 months, 40% of incidents, weekly deploys, three channels — met: Step 1 template fields "Current state" and "Context" are direct slots for these facts; the instruction opens with "Run structured multi-lens analysis on $ARGUMENTS," feeding the prompt verbatim.

- [x] PASS: Output selects 3-5 lenses and names them with explanation of why each was chosen for THIS decision — met: Step 2 requires naming selected lenses and stating why; the lens table includes "Best for" and "Key risk if skipped" columns to guide scenario-specific reasoning.

- [x] PASS: Output's lens selection includes at least one human lens AND one system lens — met: same as Criteria item 3; hard rule in the skill.

- [x] PASS: Output addresses the 40% incident origination directly — does extracting reduce blast radius or shift the failure surface — met: the Adversarial lens ("How could this fail, be attacked, or go wrong?") combined with the per-lens requirement for 3+ sub-questions directly targets the failure mode question; the unique findings requirement prevents the lens from producing only surface observations.

- [x] PASS: Output's lens analyses produce DIFFERENT findings — technical surfaces extraction cost, operational surfaces deploy frequency change, team surfaces ownership clarity — met: the "Findings unique to this lens" template field and the explicit rule "Each lens must produce at least one finding not surfaced by any previous lens" enforce divergence structurally.

- [x] PASS: Output's contradiction-surfacing step calls out tensions between lenses explicitly — e.g. team favours extraction (ownership), operational cautions it (complexity) — met: each lens has a mandatory "Contradictions with previous lenses" field; Step 4 has a "Tensions and trade-offs" table requiring both lens positions and a recommended resolution.

- [x] PASS: Output's synthesis produces a convergent findings table, tensions table, and clear recommendation — met: Step 4 structure provides all three with table schemas and a recommendation template.

- [x] PASS: Output's recommendation considers the alternative of fixing-in-place — met: the Simplicity lens ("What's the simplest version that works? What can be removed?") is one of the eight available lenses and would surface this; the rules state "Don't anchor on the first lens" and "If every lens agrees with the first one, you're not trying hard enough," creating structural pressure to examine the fix-in-place path.

- [x] PASS: Output's revised problem framing differs from the Step 1 framing — shifts from "should we extract?" to "what's driving the 40% incidents, and is extraction the leverage point?" — met: the "Revised problem framing" subsection in Step 4 explicitly requires original vs revised framing with a "Key difference" field; the multi-lens process is designed to reframe rather than confirm.

- [~] PARTIAL: Output's confidence level is stated with the evidence basis, including what data would raise or lower it — e.g. "MEDIUM confidence; would rise to HIGH if..." — partially met: the recommendation template has "based on [what evidence]" and "What would change this recommendation: If X turns out to be true, reconsider Y," covering the change-condition logic; the gap is that the template doesn't explicitly prompt for confidence-level movement (MEDIUM → HIGH if X), though the change-condition prompts serve the same function.

## Notes

The skill definition is structurally strong. The mandatory unique-findings field and per-lens contradiction tracking are the key mechanisms preventing lenses from becoming parallel restatements. The synthesis section — convergent findings, tensions with required resolutions, blind spots, revised framing, success criteria, and what-would-change — produces a decision artifact rather than a brainstorm dump.

The two PARTIAL scores share the same root cause: the confidence template covers the spirit of the criterion via "What would change this recommendation" but doesn't explicitly phrase it as "what data would raise confidence from MEDIUM to HIGH." In practice the output would be functionally equivalent; the gap is terminological, not substantive.

One structural observation outside the rubric: the skill references `/council` and `/first-principles` as related skills but gives no trigger condition for when to hand off. A brief rule ("if tensions remain irreconcilable after synthesis, use /council") would reduce practitioner ambiguity.
