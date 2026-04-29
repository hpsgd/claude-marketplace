# Test: evaluate-technology skill structure

Scenario: Checking that the evaluate-technology skill enforces an honest, evidence-based evaluation process — criteria defined before research, weighted scoring with justifications, and a clear recommendation with reconsideration triggers.

## Prompt

Review the evaluate-technology skill definition and verify it produces a structured, bias-resistant technology comparison.

## Criteria

- [ ] PASS: Skill requires evaluation criteria and weights to be defined BEFORE research begins — explicitly to prevent post-hoc rationalisation
- [ ] PASS: Skill provides a default criteria set including maturity, community, team familiarity, maintenance burden, lock-in risk, cost, and integration
- [ ] PASS: Skill mandates a research brief per option with specific fields: current version, license, notable adopters, maturity signals, community signals, known limitations
- [ ] PASS: Skill requires a weighted scoring matrix with raw and weighted scores per criterion, and a one-sentence justification for every score
- [ ] PASS: Skill requires an explicit trade-off table and a risk register with trigger signals and mitigations
- [ ] PASS: Skill's recommendation section requires stating what is sacrificed by the chosen option and what conditions would trigger reconsideration
- [ ] PASS: Skill lists anti-patterns including conclusion-first evaluation, popularity as proxy, and binary scoring
- [ ] PARTIAL: Skill handles the case where neither option is clearly better — recommends a time-boxed spike rather than forcing a choice

## Output expectations

- [ ] PASS: Output is structured as a review of the skill (verdict per requirement) rather than running an example evaluation
- [ ] PASS: Output verifies that criteria and weights are required BEFORE research, citing the explicit "post-hoc rationalisation" anti-pattern guard
- [ ] PASS: Output confirms the default criteria set includes all eight defaults (maturity, community, team familiarity, performance, maintenance burden, lock-in risk, cost, integration)
- [ ] PASS: Output verifies the research brief schema names specific required fields (current version, license, notable adopters, maturity/community signals, known limitations) — not just "research the option"
- [ ] PASS: Output confirms scoring uses a 1-5 scale with one-sentence justification per score and a weighted total — and that the skill rejects binary scoring as an anti-pattern
- [ ] PASS: Output verifies the recommendation must include reconsideration triggers and explicit acknowledgement of what is sacrificed — not just naming a winner
- [ ] PASS: Output confirms the skill includes a fall-through option (time-boxed spike) when neither option is clearly better, instead of forcing a recommendation
- [ ] PASS: Output verifies the anti-patterns list calls out conclusion-first evaluation, popularity-as-proxy, and binary scoring by name
- [ ] PARTIAL: Output identifies any genuine gaps in the skill — e.g. no guidance on how to evaluate when only one option is being assessed (fitness check), missing licence-compatibility consideration, or no exit-cost / reversibility metric beyond lock-in risk
