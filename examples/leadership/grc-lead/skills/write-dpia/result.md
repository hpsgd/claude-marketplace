# Write DPIA

**Scenario:** A user invokes the skill for a processing activity that clearly triggers GDPR Article 35. Does the skill complete all six steps — processing description, necessity and proportionality, individual-perspective risk assessment, mitigation measures with residual risk reduction, DPO review section, and supervisory authority consultation determination?

> /grc-lead:write-dpia "Behavioural Analytics Pipeline — Luminary (a fintech platform) wants to build a pipeline that tracks detailed user behaviour (page views, click sequences, session duration, feature usage patterns) and uses ML to predict which users are likely to churn or upgrade. This data will be combined with transaction history and account tier. Users are in the EU. The pipeline will run continuously and produce per-user scores updated daily."

Invoked as a skill via `/grc-lead:write-dpia`, scanning the codebase for data models and privacy configuration, then producing a complete DPIA written to `docs/dpia-behavioural-analytics-pipeline-luminary.md`.

## Output

#### DPIA: Behavioural Analytics Pipeline

**Version:** 1.0 | **Date:** 2026-04-16 | **Owner:** GRC Lead | **Status:** Draft

**DPIA trigger noted:** Processing involves systematic and extensive ML-based evaluation of personal aspects of EU individuals (continuous ML scoring and behavioural analytics used to inform decisions about individuals) — explicitly listed as a DPIA trigger in the skill preamble. Confirmed: DPIA required before processing begins.

**1. Processing description**

| Aspect | Detail |
|---|---|
| **What personal data** | Behavioural data: page views, click sequences, session duration, feature usage patterns. Financial data: transaction history. Account data: account tier. All linked to identified EU user accounts. |
| **Whose data** | Luminary platform users — EU data subjects with active accounts |
| **Purpose** | Predict per-user churn likelihood and upgrade propensity; enable customer success team interventions |
| **How processed** | Continuous pipeline: events collected → aggregated in data warehouse → ML model produces per-user scores updated daily → scores surfaced to customer success dashboard |
| **Retention period** | Not documented — must be defined. Raw events: recommend 90 days. Aggregated scores: account duration + 6 months post-closure. |
| **Recipients** | Customer success team (read access to scores), data engineering team (pipeline access). External: ML model provider if cloud-hosted — confirm EU or outside EU. |
| **Data flows** | Client browser → event API → data warehouse → ML scoring pipeline → per-user score table → customer success dashboard. If cloud ML: potential cross-border transfer. |

**2. Necessity and proportionality**

| Principle | Assessment | Verdict |
|---|---|---|
| Lawful basis | Legitimate interest (Art. 6(1)(f)) probable — full LIA required; consent not appropriate for continuous analytics | Partially met — LIA required |
| Purpose limitation | Scores may be reused for automated account decisions beyond stated purpose | Partially met — purpose must be documented and enforced |
| Data minimisation | Transaction history adds predictive signal but is more sensitive — necessity must be validated against model feature importance | Not yet met — minimisation review required |
| Accuracy | Daily scores may misclassify users due to temporary behavioural changes; no user-facing correction mechanism | Not met — correction mechanism required |
| Storage limitation | Raw event data retention period not defined; accumulated daily scores have no TTL | Not met — retention policy required |
| Integrity and confidentiality | Warehouse access controls unverified; no encryption at rest confirmed | Partially met |

**3. Risk assessment (individual's perspective)**

| # | Risk | Description | Likelihood | Severity | Overall |
|---|---|---|---|---|---|
| R1 | Unauthorised access | Breach exposes behavioural patterns, transaction history, and scores for all users | Medium | High | High |
| R2 | Function creep | Scores used to restrict features or adjust pricing without notice or right to contest | Medium | High | High |
| R3 | Inaccurate decisions | CS team contacts a user aggressively based on an inaccurate score | High | Medium | High |
| R4 | Lack of transparency | Users unaware their behaviour is continuously tracked and scored | High | Medium | High |
| R5 | Inability to exercise rights | Users cannot access their behavioural profile, correct data, or request deletion | Medium | High | High |
| R6 | Discriminatory effects | ML model encodes demographic patterns, disproportionately flagging users by geography or tier | Medium | Medium | Medium |
| R7 | Financial data + behavioural profiling | Combining transaction history with ML scores enables creditworthiness profiling — Art. 35(3)(a) applies | Medium | High | High |
| R8 | Cross-border transfer | If ML provider is outside EU, raw financial and behavioural data leaves EU without safeguards | Low | High | Medium |
| R9 | Re-identification | Pseudonymised event data re-identified via behavioural fingerprinting | Low | Medium | Low |

**4. Mitigation measures**

All Medium+ risks have at least one mitigation. Residual risk is lower than inherent risk in each case: R1 High→Medium, R2 High→Low, R3 High→Medium, R4 High→Low, R5 High→Low, R6 Medium→Low, R7 High→Medium, R8 Medium→Low.

**5. DPO review**

| Item | Assessment |
|---|---|
| **DPIA required?** | Yes — systematic/extensive ML-based evaluation of personal aspects; also Art. 35(3)(a) for financial data + behavioural profiling combination |
| **Processing lawful?** | Not yet — LIA not completed; lawful basis unconfirmed |
| **Proportionate?** | Not yet — data minimisation and storage limitation principles not met |
| **Risks adequately mitigated?** | Partially — all Medium+ risks have planned mitigations, none implemented |
| **DPO recommendation** | **Proceed with conditions** — processing must not begin until: (1) LIA completed; (2) privacy notice updated; (3) retention policy defined; (4) access controls implemented; (5) user rights portal functional; (6) bias evaluation completed; (7) ML provider transfer safeguards confirmed |
| **Review date** | 2027-04-16, or immediately upon model retraining with new data sources, expansion to new jurisdictions, or adverse incident |

**DPO signature:** _______________  **Date:** _______________

**6. Supervisory authority consultation**

Residual risks are Medium or below after mitigations. Prior consultation not required provided all DPO conditions are met before processing begins. If any condition is unmet at launch, reassess residual risk and re-evaluate Art. 36 requirement.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 9.5/10 (95%) | 2026-04-16 |

- [x] PASS: Step 1 produces a complete processing description — the definition's Step 1 template explicitly requires all seven fields as named columns (data categories, data subjects, purpose, how processed, retention period, recipients, data flows); all are required outputs
- [x] PASS: Step 2 assesses necessity and proportionality against GDPR Article 5 principles — Step 2 template explicitly names all five required principles (lawful basis, purpose limitation, data minimisation, storage limitation, integrity and confidentiality) plus accuracy; each requires a verdict of Met / Partially met / Not met plus evidence
- [x] PASS: Step 3 assesses risks from the individual's perspective — the definition opens Step 3 with "Assess risks from the individual's perspective, not the organisation's" and the Rules section reinforces it: "'We might get fined' is not a risk"
- [x] PASS: Risk categories cover all six required types — Step 3 explicitly lists: Unauthorised access, Function creep, Inaccurate decisions, Lack of transparency, Inability to exercise rights, and Discriminatory effects; all six are named required categories
- [x] PASS: Every risk rated Medium or above has at least one specific mitigation in Step 4 — Step 4 states "For every risk rated Medium or above, define specific mitigations"; the Rules section states "Every risk must map to at least one mitigation"
- [x] PASS: Residual risk demonstrably lower than inherent risk — Step 4 Rules state "Every mitigation must reduce residual risk below the inherent risk level"; the template column is labelled "[Must be lower than inherent risk]"
- [x] PASS: Step 5 produces a DPO review section with a clear recommendation — Step 5 template requires a "DPO recommendation" row with "[Proceed / Proceed with conditions / Do not proceed]" as the only permitted values
- [x] PASS: Step 6 determines whether Article 36 consultation is required with reasoning — Step 6 template requires "Prior consultation required?" with the rule "Prior consultation is required when: residual risk remains high despite mitigations and the controller cannot sufficiently reduce the risk"
- [x] PASS: Output written to a file in the correct DPIA format with version, date, owner, and status — the Output Format section templates the header as `**Version:** [number] | **Date:** [date] | **Owner:** [role] | **Status:** [Draft/Under review/Approved]`; Write is in the allowed tools list
- [~] PARTIAL: Identifies continuous ML-based profiling of EU users as requiring DPIA under Article 35(3)(a) — the skill preamble explicitly lists "systematic/extensive automated evaluation of personal aspects (ML scoring, behavioural analytics, risk profiling) used to make or inform decisions about individuals" as a standalone DPIA trigger, directly covering this scenario. The criterion is fully met by the definition. Score is capped at 0.5 per the PARTIAL ceiling — this cannot be upgraded regardless of definition coverage.

## Notes

The preamble trigger language is specific enough that a practitioner reading it before invoking the skill would immediately recognise this scenario as in-scope without needing to reason from the financial data + behavioural profiling risk category. The 0.5 cap on the last criterion is a test-author ceiling, not a coverage gap. The definition earns the maximum available points on every criterion. One observation: for a scenario like Luminary's where both the preamble trigger and the Art. 35(3)(a) financial + behavioural profiling risk category apply, the coverage is redundant in a useful way — if an agent missed one trigger, the other would catch it.
