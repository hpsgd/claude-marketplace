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
