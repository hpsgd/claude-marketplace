# Output: evaluate-technology skill structure

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires evaluation criteria and weights to be defined BEFORE research begins — met. Step 1 states "Assign weights BEFORE research to prevent post-hoc rationalisation" verbatim, positioned as a rule before any research instructions.

- [x] PASS: Skill provides a default criteria set including maturity, community, team familiarity, maintenance burden, lock-in risk, cost, and integration — met. Step 1 table lists all eight defaults: maturity/stability, community/ecosystem, team familiarity, performance, maintenance burden, lock-in risk, cost, integration.

- [x] PASS: Skill mandates a research brief per option with specific fields including current version, license, notable adopters, maturity signals, community signals, known limitations — met. Step 2 template names each as a distinct heading or field: version + release date, license type, notable adopters (3-5), maturity signals section, community signals section, and known limitations section.

- [x] PASS: Skill requires a weighted scoring matrix with raw and weighted scores per criterion, and a one-sentence justification for every score — met. Step 3 provides the matrix template with Raw (1-5) and Weighted columns, and states "Every score must have a one-sentence justification — no bare numbers."

- [x] PASS: Skill requires an explicit trade-off table and a risk register with trigger signals and mitigations — met. Step 4 provides both templates: a two-column trade-off table and a risk register with Trigger signal and Mitigation columns, both as mandatory outputs.

- [x] PASS: Skill's recommendation section requires stating what is sacrificed and reconsideration triggers — met. Step 5 template includes "What we sacrifice: [Explicit trade-off acknowledgement]" and "Reconsideration triggers: [Conditions that would change this recommendation]" as named required fields.

- [x] PASS: Skill lists anti-patterns including conclusion-first evaluation, popularity as proxy, and binary scoring — met. All three named explicitly in the Anti-Patterns section: "Conclusion-first evaluation", "Popularity as proxy", "Binary scoring."

- [x] PASS: Skill handles the case where neither option is clearly better — met in full. Step 5 states: "If neither option is clearly better, say so — recommend a time-boxed spike or prototype instead of a forced choice." Direct and unconditional.

### Output expectations

- [x] PASS: Output is structured as a review of the skill (verdict per requirement) rather than running an example evaluation — met. This result reviews the skill definition criterion by criterion without simulating an example evaluation.

- [x] PASS: Output verifies that criteria and weights are required BEFORE research, citing the "post-hoc rationalisation" anti-pattern guard — met. The phrase "post-hoc rationalisation" appears verbatim in Step 1 as the stated reason for the pre-research weight requirement.

- [x] PASS: Output confirms the default criteria set includes all eight defaults (maturity, community, team familiarity, performance, maintenance burden, lock-in risk, cost, integration) — met. All eight are present in Step 1 table. Performance is present as the fourth row alongside the seven named in the criterion.

- [x] PASS: Output verifies the research brief schema names specific required fields — met. Step 2 template calls out: version + release date, license, notable adopters, maturity signals, community signals, and known limitations as distinct labelled fields — not a generic "research the option" instruction.

- [x] PASS: Output confirms scoring uses a 1-5 scale with one-sentence justification per score and a weighted total, and that binary scoring is rejected as an anti-pattern — met. Step 3 specifies 1-5 scale and one-sentence justification. Binary scoring is called out by name in Anti-Patterns.

- [x] PASS: Output verifies the recommendation must include reconsideration triggers and explicit acknowledgement of what is sacrificed — met. Both "What we sacrifice" and "Reconsideration triggers" are named template fields in Step 5, not optional guidance.

- [x] PASS: Output confirms the skill includes a fall-through option (time-boxed spike) when neither option is clearly better — met. Step 5 gives an unconditional instruction to recommend a spike rather than force a choice.

- [x] PASS: Output verifies the anti-patterns list calls out conclusion-first evaluation, popularity-as-proxy, and binary scoring by name — met. All three appear verbatim in the Anti-Patterns section.

- [~] PARTIAL: Output identifies genuine gaps in the skill — partially met. Two genuine gaps exist:

  1. **Single-option fitness check has no adapted process.** The skill description (frontmatter) says it covers "assessing fitness of a single option," but all five process steps assume a multi-option comparison. There is no adapted path for evaluating one technology in isolation — no instruction on how to handle the scoring matrix or trade-off table when there is nothing to compare against.

  2. **Licence compatibility is not evaluated, only captured.** Step 2 records the licence type (MIT, Apache 2.0, etc.) in the research brief, but no criterion or scoring step asks whether that licence is compatible with the project's own licence or commercial use constraints. This is a distinct concern from cost and lock-in risk — a permissively licensed library can still be incompatible with a proprietary product depending on copyleft terms.

  The test also flags exit-cost / reversibility as a potential gap beyond lock-in risk. That is a fair observation but weaker — lock-in risk does partially cover migration cost.

## Notes

The skill is solid. The sequential process with explicit anti-pattern guards is well above the baseline for technology evaluation frameworks. Positioning the "post-hoc rationalisation" warning inside Step 1 — before the researcher has touched any documentation — is the right design choice.

One minor structural issue: the Output Format section at the end lists "Re-evaluate on [date or trigger condition]" as a follow-up item, but no process step instructs the evaluator to determine this date or condition. An evaluator following the five steps would reach the output template without having been prompted to decide when to revisit. Low severity, but worth noting.

The Step 3 fallback — "if you lack data for a criterion, score it 3 (neutral) and flag it as 'unverified'" — is practical but creates a weak point. A gap in evidence scores the same as a neutral result, which could understate risk. A stronger approach would require the evaluator to make at least one attempt to fill the gap before defaulting.
