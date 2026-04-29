# Output: write-dpia

**Verdict:** PASS
**Score:** 19.5/20 criteria met (97.5%)
**Evaluated:** 2026-04-29

## Results

### Criteria section

- [x] PASS: Step 1 produces a complete processing description — data categories, data subjects, purpose, how processed, retention period, recipients, and data flow — met: the processing description table in Step 1 covers all seven aspects as explicit named columns; Appendix A in the output format is a data flow diagram
- [x] PASS: Step 2 assesses necessity and proportionality against GDPR Article 5 principles — lawful basis, purpose limitation, data minimisation, storage limitation, and security — met: the proportionality table covers all six Article 5 principles with verdict and evidence columns
- [x] PASS: Step 3 assesses risks from the individual's perspective — not the organisation's perspective — met: Step 3 opens with "Assess risks from the individual's perspective, not the organisation's" and the Rules section reinforces this with the "We might get fined is not a risk" example
- [x] PASS: Risk categories cover unauthorised access, function creep, inaccurate decisions, lack of transparency, inability to exercise rights, and discriminatory effects — met: all six are enumerated in the Step 3 risk categories list, plus the financial data + behavioural profiling combination which is directly relevant to this scenario
- [x] PASS: Every risk rated Medium or above has at least one specific mitigation defined in Step 4 — met: Step 4 states "For every risk rated Medium or above, define specific mitigations" and the Rules section states "Every risk must map to at least one mitigation"
- [x] PASS: Residual risk after mitigation is demonstrably lower than inherent risk for each mitigated risk — met: the mitigation table includes a residual risk column labelled "[Must be lower than inherent risk]" and the Rules section states "Every mitigation must reduce residual risk below the inherent risk level"
- [x] PASS: Step 5 produces a DPO review section with a clear recommendation (Proceed / Proceed with conditions / Do not proceed) — met: the DPO review table includes a "DPO recommendation" row with exactly those three options specified
- [x] PASS: Step 6 determines whether Article 36 supervisory authority consultation is required with reasoning — met: Step 6 has a dedicated table with "Prior consultation required?" and explicit rationale tied to residual risk level
- [x] PASS: Output is written to a file in the correct DPIA format with version, date, owner, and status — met: the output format header specifies Version, Date, Owner, and Status; Write is listed in allowed-tools
- [~] PARTIAL: Identifies that continuous ML-based profiling of EU users likely requires a DPIA under Article 35(3)(a) (large-scale profiling) — partially met: the skill preamble explicitly names ML scoring and behavioural analytics as Art. 35(3)(a) triggers; the DPO review table asks which Article 35 trigger applies, but the skill does not pre-flag 35(3)(b) large-scale processing as a separate trigger, and the pre-identification happens only in the preamble description rather than as a named check before Step 1

### Output expectations section

- [x] PASS: Output's processing description names the specific data categories from the scenario, data subjects, purpose, processing means, retention period, recipients, and includes a data flow diagram — met: Step 1 template requires all these fields and Appendix A is explicitly a data flow diagram
- [x] PASS: Output's necessity and proportionality assessment evaluates each Article 5 principle including lawful basis (legitimate interest with LIA), purpose limitation, data minimisation, storage limitation, accuracy, security — met: the six-row proportionality table covers all these with verdict and evidence columns
- [x] PASS: Output's risk assessment is from the individual's perspective — met: stated explicitly in Step 3 and Rules section, with a concrete example of what does and does not qualify as a risk
- [x] PASS: Output's risk categories cover unauthorised access, function creep, inaccurate decisions, lack of transparency, inability to exercise rights, and discriminatory effects — met: all are in the Step 3 risk categories list; the financial data + behavioural profiling category specifically addresses the Luminary scenario's combination of transaction history with ML scoring
- [x] PASS: Output's mitigations target each Medium+ risk with at least one specific control — met: Step 4 requires specific technical and organisational measures per risk with the mitigation categories providing concrete examples
- [~] PARTIAL: Output's residual risk is demonstrably lower than inherent risk per mitigated risk, with a likelihood × impact recalculation shown after controls — partially met: the residual risk column is required and labelled to be lower than inherent risk, and the likelihood × severity matrix is defined in Step 3, but Step 4 does not explicitly require the agent to show a recalculated likelihood × impact score for each risk after mitigations; the agent could populate residual risk ratings without showing the arithmetic
- [x] PASS: Output's DPO review section produces a clear recommendation with conditions specified — met: the DPO review template has "DPO recommendation" with the three permitted values and a "Conditions (if any)" row requiring specifics
- [x] PASS: Output's Article 36 determination is explicit — consultation IS or IS NOT required, with reasoning tied to whether residual risk remains High — met: Step 6 ties prior consultation explicitly to "residual risk remains high despite mitigations"
- [x] PASS: Output is written to a file with version, date, owner (DPO), and status — not only returned in conversation — met: the output format defines this file structure; Write is in allowed-tools
- [~] PARTIAL: Output explicitly states this processing triggers Article 35(3)(a) and likely (b) — partially met: the skill's preamble names 35(3)(a) automated evaluation explicitly and the DPO review table asks which trigger applies, but 35(3)(b) large-scale processing of special categories is not separately named as a trigger in the guidance, so the agent may not identify both subsections without additional prompting

## Notes

The skill is structurally sound and maps cleanly to ICO/EDPB DPIA methodology. Two gaps keep two criteria at partial. First, Step 4 does not require a visible likelihood × impact recalculation after mitigations — the residual risk column exists but agents could populate it without showing the arithmetic. Second, Article 35(3)(b) is absent from the trigger guidance; only 35(3)(a) and general large-scale language appear. For this specific Luminary scenario both 35(3)(a) and 35(3)(b) are likely triggered and the skill would catch 35(3)(a) but might miss 35(3)(b). The individual-perspective framing is enforced in two places which is good redundancy. The Rules section is the strongest part of the definition.
