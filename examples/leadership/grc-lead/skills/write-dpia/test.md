# Test: write-dpia

Scenario: A user invokes the skill for a processing activity that clearly triggers GDPR Article 35. Does the skill complete all six steps — processing description, necessity and proportionality, individual-perspective risk assessment, mitigation measures with residual risk reduction, DPO review section, and supervisory authority consultation determination?

## Prompt

/grc-lead:write-dpia "Behavioural Analytics Pipeline — Luminary (a fintech platform) wants to build a pipeline that tracks detailed user behaviour (page views, click sequences, session duration, feature usage patterns) and uses ML to predict which users are likely to churn or upgrade. This data will be combined with transaction history and account tier. Users are in the EU. The pipeline will run continuously and produce per-user scores updated daily."

## Criteria

- [ ] PASS: Step 1 produces a complete processing description — data categories, data subjects, purpose, how processed, retention period, recipients, and data flow
- [ ] PASS: Step 2 assesses necessity and proportionality against GDPR Article 5 principles — lawful basis, purpose limitation, data minimisation, storage limitation, and security
- [ ] PASS: Step 3 assesses risks from the individual's perspective — not the organisation's perspective
- [ ] PASS: Risk categories cover: unauthorised access, function creep, inaccurate decisions, lack of transparency, inability to exercise rights, and discriminatory effects
- [ ] PASS: Every risk rated Medium or above has at least one specific mitigation defined in Step 4
- [ ] PASS: Residual risk after mitigation is demonstrably lower than inherent risk for each mitigated risk
- [ ] PASS: Step 5 produces a DPO review section with a clear recommendation (Proceed / Proceed with conditions / Do not proceed)
- [ ] PASS: Step 6 determines whether Article 36 supervisory authority consultation is required with reasoning
- [ ] PASS: Output is written to a file in the correct DPIA format with version, date, owner, and status
- [ ] PARTIAL: Identifies that continuous ML-based profiling of EU users likely requires a DPIA under Article 35(3)(a) (large-scale profiling)
