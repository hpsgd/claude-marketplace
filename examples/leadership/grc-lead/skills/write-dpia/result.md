# Write Dpia

Scenario: A user invokes the skill for a processing activity that clearly triggers GDPR Article 35. Does the skill complete all six steps — processing description, necessity and proportionality, individual-perspective risk assessment, mitigation measures with residual risk reduction, DPO review section, and supervisory authority consultation determination?

## Prompt

> /grc-lead:write-dpia "Behavioural Analytics Pipeline — Luminary (a fintech platform) wants to build a pipeline that tracks detailed user behaviour (page views, click sequences, session duration, feature usage patterns) and uses ML to predict which users are likely to churn or upgrade. This data will be combined with transaction history and account tier. Users are in the EU. The pipeline will run continuously and produce per-user scores updated daily."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The DPIA has been written to `dpia-behavioural-analytics-pipeline.md`. Here's a summary of what it contains and the key findings:

---

## DPIA: Behavioural Analytics Pipeline — Summary

**Status: Draft — cannot proceed without satisfying 11 pre-conditions**

### Key findings

**Three Art. 35 triggers apply** — DPIA is mandatory: systematic automated profiling (Art. 35(3)(a)), large-scale financial data, and innovative ML use.

**Lawful basis is not yet established.** Legitimate interests requires a completed LIA; transaction data repurposing requires an Art. 6(4) compatibility assessment. Neither has been done. Processing cannot begin until both are resolved.

**11 risks identified across 4 Very High / 5 High / 1 Medium inherent ratings:**

| # | Risk | Inherent | Residual |
|---|---|---|---|
| R1 | Unauthorised access to combined financial + behavioural data | Very High | Medium |
| R4 | Function creep — scores used beyond stated purpose | Very High | Medium |
| R10 | Transaction data repurposed beyond contract performance | Very High | Medium* |
| R11 | **Art. 9 special category inference** (health, religion, sexual orientation revealed by merchant category codes) | High | Medium* |
| R2, R3, R5, R6, R8, R9 | Inaccurate decisions, discrimination, lack of transparency, rights, cross-border transfers, excessive collection | High → Medium | Low–Medium |

*Conditional on legal counsel assessments.

**The Art. 9 finding is significant:** transaction descriptions like pharmacy spend, clinic payments, or donations can indirectly reveal health, religious, or sexual orientation data under CJEU case law. Legitimate interests is not available as a lawful basis for Art. 9 data — explicit consent may be required. A merchant-category exclusion list (M14) and proxy-leakage test in the model bias audit are required mitigations.

**DPO recommendation: Proceed with conditions.** Prior supervisory authority consultation is not currently required, but becomes mandatory if the Art. 6(4) or Art. 9 legal assessments cannot establish a valid lawful basis, or if the bias audit finds unmitigatable discriminatory effects.

### Artifacts written

#### `work/dpia-behavioural-analytics-pipeline.md`

```
# DPIA: Behavioural Analytics Pipeline

**Version:** 1.0  |  **Date:** 2026-05-01  |  **Owner:** Data Protection Officer  |  **Status:** Draft

---

## 1. Processing Description

### Overview

Luminary, an EU-regulated fintech platform, proposes to build a continuous behavioural analytics pipeline that tracks detailed user interactions, combines them with financial transaction history and account tier data, and feeds this combined dataset into ML models to generate daily per-user churn and upgrade propensity scores.

### Processing Description Table

| Aspect | Detail |
|---|---|
| **What personal data** | **Behavioural:** page views (URL, timestamp, referrer), click sequences (element, coordinates, order), session duration, feature usage patterns (which product features accessed, frequency, recency). **Financial:** transaction history (amount, merchant category, frequency, direction), account tier (basic/premium/enterprise). **Inferred:** ML-derived churn score (0–1), upgrade propensity score (0–1), behavioural segment label. **Technical identifiers:** user ID, device fingerprint, browser/OS metadata, IP address (at collection), session ID. |
| **Whose data** | Registered users of Luminary's fintech platform located in the EU. These are consumers and/or SME operators interacting with financial services. |
| **Purpose** | (1) Predict which users are at risk of churning so Luminary can trigger retention interventions. (2) Predict which users are likely to upgrade their account tier so Luminary can target upsell communications. Both purposes are commercial and serve Luminary's business interests. |
| **How processed** | Client-side instrumentation collects behavioural events in real time. Events are streamed into an ingestion pipeline, stored in a data warehouse, joined with transaction history and account tier from the core banking/product database, and fed into ML models. Models run in batch and produce per-user scores updated daily. Scores are written to a scoring database and consumed by downstream systems (CRM, push notification engine, account management tooling). Processing is continuous; no human review of individual scores before they are acted upon. |
| **Retention period** | Not defined at this stage — **gap requiring resolution before processing begins**. Behavioural events likely retained indefinitely unless policy is set. Scores may accumulate across model runs. Recommendation: raw events 90 days; aggregated features 12 months; scores 30 days rolling. |
| **Recipients** | Internal: Data Engineering (pipeline operation), ML/Data Science (model training and evaluation), Product (feature usage analytics), Growth/Marketing (retention and upsell campaigns), Customer Success (at-risk user interventions). External: Cloud infrastructure provider (processor); analytics/ML tooling vendors (sub-processors — not yet enumerated). |
| **Data flows** | User browser/app → event collector (client-side SDK) → streaming ingestion (e.g., Kafka/Kinesis) → raw event store (data warehouse) → feature engineering (join with transaction DB + account tier) → ML model inference → scoring database → downstream consumers (CRM, notification engine, account management). Cross-border transfers: not specified — **gap requiring resolution** if cloud infrastructure or sub-processors operate outside the EU/EEA. |

### Data Flow Summary

```
[User device]
    │  behavioural events (real-time)
    ▼
[Event Collector / Client-side SDK]
    │
    ▼
[Streaming Ingestion Pipeline]
    │
    ▼
[Raw Event Store (Data Warehouse)]  ◄── [Transaction DB + Account Tier]
    │
    ▼
[Feature Engineering Layer]
    │  combined dataset: behaviour + financial + tier
    ▼
[ML Model Batch Inference]  (runs daily)
    │
    ▼
[Scoring Database]  (per-user scores, updated daily)
    │
    ├──► [CRM / Retention Campaign Engine]
    ├──► [Push / Email Notification Engine]
    └──► [Account Management / CS Tooling]
```

---

## 2. Necessity and Proportionality

### Art. 35 Triggers Present

This processing triggers mandatory DPIA under **multiple** GDPR Art. 35 criteria:

1. **Art. 35(3)(a)** — systematic and extensive evaluation of personal aspects of natural persons based on automated processing, including profiling, and on which decisions are made that produce legal or similarly significant effects. ML-derived churn and upgrade scores feed directly into business decisions (retention interventions, upsell targeting) about individual users.
2. **WP29 Guidelines on DPIAs** — large-scale processing of financial data combined with behavioural profiling.
3. **WP29 criterion: profiling** — systematic profiling of individuals to predict future behaviour.
4. **WP29 criterion: innovative use of technology** — ML-based inference on combined behavioural and financial datasets.

### Necessity and Proportionality Assessment

| Principle | Assessment | Verdict | Evidence / Gaps |
|---|---|---|---|
| **Lawful basis (Art. 6)** | Legitimate interests (Art. 6(1)(f)) is the most likely candidate. Contract performance (Art. 6(1)(b)) cannot cover ML-based churn scoring — this goes beyond delivering the contracted service. Consent (Art. 6(1)(a)) would be operationally viable but not yet implemented. A Legitimate Interests Assessment (LIA) has not been conducted. | **Not yet met** | LIA required. Users have a reasonable expectation their transaction data is used to deliver financial services, not to build behavioural profiles for commercial gain. The balance test may not favour Luminary without strong safeguards. |
| **Purpose limitation (Art. 5(1)(b))** | Stated purposes are churn prediction and upgrade propensity. However, scores are accessible to Growth/Marketing, Product, and Customer Success — creating multiple use paths. Transaction history collected for service delivery is being repurposed for commercial profiling. | **Partially met** | Downstream access controls must limit scores to the stated use cases. Repurposing transaction data requires explicit compatibility assessment under Art. 6(4). |
| **Data minimisation (Art. 5(1)(c))** | Click sequences, mouse coordinates, and detailed page-level behavioural data likely exceed what is necessary for churn/upgrade prediction. Session-level aggregates (sessions per week, features used Y/N, last active date) may be sufficient. Individual click sequences and element-level coordinates are particularly difficult to justify. | **Not met** | A data minimisation review is required before pipeline design is finalised. Raw click-coordinate data must not be collected unless necessity is demonstrated. |
| **Accuracy (Art. 5(1)(d))** | ML models produce probabilistic scores that may be inaccurate for individual users. No mechanism described for users to challenge or correct their score. Models trained on historical data may reflect past behaviour that no longer applies (e.g., a user who was inactive due to a personal event). | **Not met** | Model accuracy metrics must be defined and monitored. A rights mechanism allowing users to query and challenge their score must be implemented. |
| **Storage limitation (Art. 5(1)(e))** | No retention periods have been defined for raw events, features, or scores. Indefinite retention of detailed behavioural data is not lawful. | **Not met** | Retention policy must be defined, documented, and enforced with automated deletion before processing begins. |
| **Integrity and confidentiality (Art. 5(1)(f))** | Not yet specified. The combination of financial and detailed behavioural data creates a high-value target. Security architecture has not been described. | **Not yet assessed** | Security architecture must be reviewed. Encryption at rest and in transit, access controls, and audit logging are baseline requirements. |
| **Transparency (Art. 13/14)** | Users in the EU are entitled to be informed about profiling at the point of data collection. It is not confirmed that Luminary's privacy notice covers ML-based behavioural profiling or the right to object under Art. 21(2). | **Not met** | Privacy notice must be updated to describe this processing before launch. |

**Overall proportionality verdict: Partially met — significant gaps must be remediated before processing begins.**

---

## 3. Risk Assessment

### Risk Table

| # | Risk | Description | Likelihood | Severity | Overall Risk |
|---|---|---|---|---|---|
| R1 | Unauthorised access to combined financial and behavioural data | A breach of the data warehouse or scoring database exposes per-user transaction history combined with detailed click-level behavioural profiles. The combination creates a richer identity and financial picture than either dataset alone, enabling identity theft, financial fraud, and social engineering. | High | High | **Very High** |
| R2 | Inaccurate ML scores driving harmful decisions | A user's churn score is elevated due to a data quality issue (e.g., bot traffic misattributed, inactive period miscoded) or model bias. The user receives restricted service, is deprioritised for support, or is targeted with pressure communications without grounds. The user has no visibility or recourse. | High | Medium | **High** |
| R3 | Discriminatory effects from behavioural + financial profiling | ML models trained on historical behaviour may encode protected characteristics as proxies. Users with certain spending patterns, feature usage habits, or session cadences correlated with age, disability, or ethnic background may be systematically scored lower for upgrade propensity, resulting in differential treatment. This is not hypothetical — financial services ML has a documented history of proxy discrimination. | Medium | High | **High** |
| R4 | Function creep — scores used beyond stated purposes | Churn and upgrade scores, once available in the CRM and notification engine, are likely to be used for purposes not stated at collection: credit risk assessment, account restrictions, fee structure changes, third-party commercial partnerships. No access controls or purpose-binding mechanisms are described. | High | High | **Very High** |
| R5 | Lack of transparency — users unaware of profiling | Users do not know their behaviour is being tracked at click/element level, that it is combined with their financial history, or that ML scores influence how they are treated by Luminary. This violates Art. 13/14 and undermines informed consent or objection. | High | Medium | **High** |
| R6 | Inability to exercise data subject rights | Users cannot currently access their score, understand its basis, challenge its accuracy, or request deletion of the underlying data. This blocks Art. 15 (access), Art. 16 (rectification), Art. 17 (erasure), and Art. 22 (automated decision-making) rights. | High | Medium | **High** |
| R7 | Re-identification from pseudonymised behavioural data | Detailed click sequences and session patterns may function as a behavioural fingerprint that re-identifies users even after pseudonymisation. Combined with device metadata, this creates a persistent identity signal. | Medium | Medium | **Medium** |
| R8 | Cross-border data transfer without adequate safeguards | If the data warehouse, ML infrastructure, or any sub-processor (analytics SaaS, model training platform) operates outside the EU/EEA, financial and behavioural data may be transferred without appropriate safeguards (SCCs, adequacy decision). | Medium | High | **High** |
| R9 | Excessive collection — click-level granularity disproportionate | Raw click sequences and element-level coordinates are collected but churn/upgrade prediction likely requires only session-level aggregates. Storing granular interaction data creates unnecessary risk surface with no proportionate benefit. | High | Medium | **High** |
| R10 | Financial data repurposed beyond service delivery | Transaction history collected under Art. 6(1)(b) (contract performance) is being repurposed for ML-based commercial profiling. Without a compatibility assessment and additional lawful basis, this constitutes purpose limitation violation — an inherent legal risk to Luminary and a rights violation for users. | High | High | **Very High** |
| R11 | Indirect revelation of Art. 9 special category data via transaction patterns | Transaction descriptors and merchant category codes can indirectly reveal special category data under Art. 9: spending at fertility clinics, HIV treatment centres, or pharmacies → health data; donations to religious institutions → religious belief; payments to political organisations → political opinion; payments to LGBTQ+ services → sexual orientation. Under CJEU case law (C-184/20 *OT v Vyriausioji tarnybinės etikos komisija*), data that indirectly reveals a special category is treated as Art. 9 data. ML features built on transaction history can encode these signals as model inputs, requiring Art. 9(2) explicit consent or another Art. 9 basis — which legitimate interests does not satisfy. | Medium | High | **High** |

---

## 4. Mitigation Measures

### Mitigation Table

| # | Measure | Risk(s) Addressed | Implementation Status | Residual Risk |
|---|---|---|---|---|
| M1 | **Conduct and document a Legitimate Interests Assessment (LIA)** before processing begins. The LIA must test whether Luminary's commercial interest in churn/upgrade prediction overrides users' reasonable expectations. If the LIA fails, switch to explicit opt-in consent (layered consent at onboarding, per-purpose, with easy withdrawal). | R10, R5 | Planned — must precede launch | R10: High → **Medium** (if LIA passes with documented mitigations); R5: High → **Medium** |
| M2 | **Data minimisation: replace raw click-event collection with pre-aggregated session-level features.** Collect: sessions per week, distinct features used (boolean per feature), last active date, session duration buckets (not raw seconds). Do not collect: element coordinates, click sequences, raw page URLs (collect page category instead). Validate feature necessity against model performance before each pipeline iteration. | R9, R1, R7 | Planned — pipeline design phase | R9: High → **Low**; R1: Very High → **High**; R7: Medium → **Low** |
| M3 | **Encrypt data at rest (AES-256) and in transit (TLS 1.3)** across all pipeline stages: event ingestion, data warehouse, feature store, scoring database. Apply column-level encryption to financial data fields. | R1 | Planned | R1: Very High → **High** (encryption alone does not eliminate insider threat or API exposure) |
| M4 | **Implement role-based access controls (RBAC) with need-to-know enforcement.** Raw behavioural events: Data Engineering only. Combined feature datasets: ML/Data Science only. Scores: defined downstream consumers only (CRM system account, not humans directly). Enforce via database permissions and API gateway authorisation. Log all access. | R1, R4 | Planned | R1: → **Medium**; R4: Very High → **Medium** |
| M5 | **Define and enforce retention periods with automated deletion.** Raw events: 90-day rolling delete. Aggregated features: 12-month rolling delete. Daily scores: 30-day rolling delete with model training snapshots archived separately under Data Science data governance. Implement automated deletion jobs with alerting on failure. | R9, R1 | Planned | R9: → **Low**; lifecycle risk component of R1 reduced |
| M6 | **Update privacy notice before launch** to describe: (a) behavioural tracking at session/feature level; (b) combination with transaction history; (c) ML-based profiling for churn and upgrade prediction; (d) categories of decisions influenced by scores; (e) right to object to profiling under Art. 21(2); (f) right to request human review of any decision significantly affecting the user. | R5, R6 | Planned | R5: High → **Low**; R6: High → **Medium** |
| M7 | **Implement a data subject rights portal** supporting: Art. 15 access (user can download their score and the features used to generate it — not the raw model weights); Art. 16 rectification (flag data quality issues for review); Art. 17 erasure (delete behavioural data and recalculate score without it); Art. 21 objection to profiling (opt-out removes user from ML pipeline, retains service access). Process SARs within 30 days. | R6, R2 | Planned | R6: High → **Low**; R2: High → **Medium** |
| M8 | **Conduct pre-launch model bias audit** across protected characteristics (age bracket, account tier as proxy for income, geography). Define fairness metrics (equalised odds, demographic parity) and set acceptable thresholds. Repeat audit after each major model retraining. Document findings and corrective actions. | R3 | Planned | R3: High → **Medium** |
| M9 | **Implement human-in-the-loop review for significant decisions, with Art. 22(3) safeguards.** Any action with material impact on a user (account restriction, fee change, blocking access to a product feature) must not be triggered solely by an ML score. Define a score threshold above which a human reviewer must approve before action is taken. Provide users the Art. 22(3) rights: to express their point of view, to obtain human intervention, and to contest the decision. For retention/upsell communications, automated action is acceptable provided the user can easily opt out. | R2, R3 | Planned | R2: High → **Low**; R3: → **Low** for significant decisions |
| M10 | **Enumerate all third-party sub-processors** (cloud provider, data warehouse vendor, ML platform, CRM, notification engine). Confirm EU/EEA data residency or execute Standard Contractual Clauses (SCCs) with Transfer Impact Assessments (TIAs) for any transfers to third countries. Document in Records of Processing Activities (RoPA). | R8 | Planned | R8: High → **Medium** (SCCs do not eliminate third-country surveillance risk — TIA required) |
| M11 | **Conduct Art. 6(4) compatibility assessment** for repurposing transaction history. Document: link between original purpose (contract performance) and new purpose (ML profiling); context of collection; nature of data (financial); possible consequences; and safeguards applied. If incompatibility is found, separate lawful basis must be established. | R10 | Planned | R10: Very High → **Medium** (if compatible with safeguards); Very High → **Not mitigatable** (if incompatible — processing must stop) |
| M12 | **Establish purpose-binding controls** for the scoring database. Implement a data contract or API schema that enforces permitted use cases (retention interventions, upgrade offers). Log queries against stated purpose. Quarterly review of downstream consumption patterns against declared purposes. | R4 | Planned | R4: Very High → **Medium** |
| M13 | **Establish an anomaly detection and breach response procedure** specific to the pipeline. Define detection for: unusual query volumes against the scoring DB, bulk exports of combined datasets, ML feature store access outside normal hours. Integrate with SIEM. Test incident response plan (including 72-hour Art. 33 notification SLA) before launch. | R1 | Planned | R1 breach response component: → **Medium** |
| M14 | **Define and enforce an Art. 9 feature exclusion list for the ML pipeline.** Before feature engineering, apply a blocklist to merchant category codes (MCCs) and payee descriptors associated with Art. 9-sensitive categories: health/medical providers, pharmacies, reproductive health services, religious organisations, political parties, LGBTQ+ establishments. These transaction records must be excluded from ML features. The bias audit (M8) must include a proxy-leakage check — testing whether retained features correlate with excluded Art. 9-associated categories at model input or output level. If proxy leakage is detected, the correlated feature must be dropped. Legal counsel must assess whether remaining features indirectly reveal Art. 9 data and, if so, whether explicit consent (Art. 9(2)(a)) is required as a separate lawful basis before ML training proceeds. | R11 | Planned | R11: High → **Medium** (feature exclusion and proxy audit reduce direct risk; residual reflects irreducible inference risk in complex ML models) |

### Residual Risk Summary

| Risk | Inherent Risk | Residual Risk | Mitigations Applied |
|---|---|---|---|
| R1 Unauthorised access | Very High | **Medium** | M2, M3, M4, M5, M13 |
| R2 Inaccurate decisions | High | **Low** | M7, M8, M9 |
| R3 Discriminatory effects | High | **Medium** | M8, M9 |
| R4 Function creep | Very High | **Medium** | M4, M12 |
| R5 Lack of transparency | High | **Low** | M6 |
| R6 Rights inability | High | **Low** | M6, M7 |
| R7 Re-identification | Medium | **Low** | M2 |
| R8 Cross-border transfer | High | **Medium** | M10 |
| R9 Excessive collection | High | **Low** | M2, M5 |
| R10 Financial data repurposing | Very High | **Medium** (conditional on M11 compatibility finding) | M1, M11 |
| R11 Art. 9 special category inference | High | **Medium** | M14 |

**Note:** R3, R4, R8, R10, and R11 retain residual risk at Medium. R10 is conditional — if the Art. 6(4) compatibility assessment (M11) finds the repurposing incompatible, residual risk cannot be mitigated and processing must not commence until a separate lawful basis is established. R11 retains irreducible inference risk; the feature exclusion list (M14) reduces but cannot eliminate it — legal counsel must assess whether explicit Art. 9(2)(a) consent is required as an additional lawful basis.

---

## 5. DPO Review

### DPO Review Table

| Item | Assessment |
|---|---|
| **DPIA required?** | **Yes.** Three Art. 35 triggers apply: (1) Art. 35(3)(a) — systematic, extensive automated evaluation of personal aspects used to make or inform decisions about individuals; (2) large-scale processing of financial data (WP29 guidelines); (3) behavioural profiling combined with financial data (WP29 high-risk criteria). DPIA is mandatory and must be completed before processing begins. |
| **Processing lawful?** | **Not yet.** Lawful basis under Art. 6 has not been confirmed. Legitimate interests requires a completed LIA (M1) that has not yet been conducted. The repurposing of transaction data requires an Art. 6(4) compatibility assessment (M11). Processing cannot begin until both are complete and documented. |
| **Proportionate?** | **Not yet.** Data minimisation (R9), storage limitation (R9/R5), transparency (R5), accuracy/rights (R2/R6), and purpose limitation (R4/R10) principles are currently not met. All mitigations in Section 4 must be implemented before proportionality can be confirmed. |
| **Risks adequately mitigated?** | **With conditions.** After full implementation of M1–M14, no residual risks are rated High or Very High. However: (a) M11 (compatibility assessment) is a gate — if it finds incompatibility, R10 blocks the entire pipeline; (b) M8 (bias audit) must confirm acceptable fairness metrics and pass proxy-leakage check for Art. 9-associated features before launch; (c) M14 requires legal counsel assessment of whether Art. 9(2)(a) explicit consent is needed; (d) R3, R8, and R11 retain Medium residual risk, which is acceptable provided M8, M9, M10, and M14 are fully implemented and monitored. |
| **DPO recommendation** | **Proceed with conditions.** The processing is commercially legitimate and technically feasible under GDPR, but several pre-conditions must be satisfied before any data collection begins. |
| **Conditions before processing begins** | 1. Complete LIA and confirm Art. 6(1)(f) lawful basis, OR implement layered opt-in consent mechanism (M1). 2. Complete Art. 6(4) compatibility assessment for transaction data repurposing (M11). 3. Implement Art. 9 feature exclusion list and have legal counsel assess whether explicit Art. 9(2)(a) consent is required (M14). 4. Implement data minimisation: replace raw click collection with session-level aggregates (M2). 5. Define and document retention periods; implement automated deletion (M5). 6. Update privacy notice to cover this processing (M6). 7. Implement data subject rights portal including Art. 22(3) rights (express view, contest decision) (M7). 8. Enumerate all sub-processors and confirm EU residency or execute SCCs + TIAs (M10). 9. Implement RBAC and audit logging (M4). 10. Conduct pre-launch model bias audit including proxy-leakage check with documented acceptable thresholds (M8). 11. Define and implement human-in-the-loop controls for significant decisions with Art. 22(3) safeguards (M9). |
| **Post-launch obligations** | Quarterly purpose-binding review (M12). Repeat bias audit after each major model retraining (M8). Annual DPIA review (or earlier if processing changes materially). |
| **Review date** | **2027-05-01** (12 months from issue). Earlier review required if: ML model architecture changes materially; new data sources are added to the pipeline; new downstream use cases for scores are introduced; a security incident occurs involving pipeline data. |

**DPO signature:** _______________  **Date:** _______________

---

## 6. Supervisory Authority Consultation

### Consultation Assessment

| Question | Answer |
|---|---|
| **Any residual risks rated High or Very High after mitigation?** | No — provided all mitigations M1–M13 are fully implemented. R3, R4, R8, and R10 retain Medium residual risk; none exceed that level after mitigation. |
| **Conditional gate remaining?** | Yes — R10 (financial data repurposing) is conditionally Medium. If the Art. 6(4) compatibility assessment concludes the repurposing is incompatible, and no alternative lawful basis can be established, residual risk becomes Very High and is not mitigatable. At that point, prior consultation is required and the processing component using transaction data must be suspended. |
| **Can residual risk be further reduced?** | For R3 (discriminatory effects), the Medium residual risk reflects the inherent limitations of ML fairness techniques. Human review gates (M9) are the primary remaining control. Further reduction would require restricting the model to non-sensitive feature sets, which may be evaluated in a future pipeline iteration. For R8 (cross-border transfers), SCCs + TIA represent the maximum available mitigation short of full EU-only infrastructure. |
| **Prior consultation required (Art. 36)?** | **No — conditional.** Prior consultation is not required at this stage, provided all conditions in Section 5 are satisfied before processing begins and the Art. 6(4) compatibility assessment (M11) confirms compatibility. **Consultation becomes mandatory if:** (a) the Art. 6(4) assessment finds incompatibility and no alternative lawful basis is available; (b) the bias audit (M8) identifies discriminatory effects that cannot be remediated to acceptable thresholds; or (c) legal counsel determines that Art. 9 special category data is present in the ML feature set (R11) and no Art. 9(2) lawful basis can be established. |
| **Relevant supervisory authority** | Users are in the EU — the lead supervisory authority depends on Luminary's EU establishment. If Luminary's main EU establishment is in Ireland: **Data Protection Commission (DPC)**. If France: **CNIL**. If Germany: **BfDI / relevant Landesbehörde**. If Luminary has no EU establishment, the authority of the EU member state in which the users are based has jurisdiction (Art. 55). The DPO must confirm the lead authority before finalising this DPIA. |
| **Consultation timeline** | If consultation is triggered: notify the supervisory authority before processing begins. The authority has 8 weeks to respond (extendable by 6 weeks for complex cases — Art. 36(2)). Processing must not commence during the consultation period. |

**Consultation determination: Prior consultation not currently required. Mandatory if Art. 6(4) gate fails or bias audit identifies unmitigatable discriminatory effects.**

---

## Appendices

### Appendix A: Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA COLLECTION                              │
│                                                                     │
│  [User Browser / Mobile App]                                        │
│       │ click events, page views, session data (real-time)         │
│       │ SDK collects: element ID, timestamp, session ID, user ID   │
│       ▼                                                             │
│  [Event Collector / Client-side Instrumentation]                    │
│       │ strips IP after geo-lookup; pseudonymises with user ID     │
└───────┼─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     INGESTION & STORAGE                             │
│                                                                     │
│  [Streaming Pipeline]  ──────────────────────────────────────────  │
│       │                         [Transaction DB]  [Account DB]     │
│       ▼                               │                │           │
│  [Raw Event Store]  ◄─────────────────┘────────────────┘           │
│  (data warehouse, 90-day retention)                                 │
│  Encrypted at rest; Data Engineering access only                   │
└───────┼─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   FEATURE ENGINEERING                               │
│                                                                     │
│  [Feature Store]                                                    │
│  Aggregates: sessions/week, features used, last active,            │
│  transaction frequency/category, account tier                      │
│  No raw click sequences or coordinates (post-M2)                   │
│  ML/Data Science access only; 12-month retention                   │
└───────┼─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ML INFERENCE (daily batch)                       │
│                                                                     │
│  [Churn Model]  →  churn_score (0–1)                               │
│  [Upgrade Model]  →  upgrade_score (0–1)                           │
│  Bias audit controls applied; scores pseudonymised by user ID      │
└───────┼─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SCORING DATABASE                                 │
│  30-day rolling retention                                           │
│  RBAC: read access scoped per downstream consumer                  │
│  Purpose-binding controls; query audit log                         │
└───────┬─────────────────┬──────────────────┬────────────────────────┘
        │                 │                  │
        ▼                 ▼                  ▼
  [CRM / Retention]  [Notification     [Account Mgmt /
  campaign engine]    Engine]           CS Tooling]
  (with human gate    (opt-out          (human review
   for significant     available)        required for
   decisions)                           material actions)
```

### Appendix B: Legal Basis Analysis

**Art. 6(1)(f) — Legitimate Interests**

*Luminary's interest:* Reducing churn and optimising upsell conversion are legitimate commercial interests for a fintech platform. Retention interventions may also benefit users by surfacing relevant features.

*Necessity test:* The processing must be necessary for this interest — i.e., it cannot be achieved through less intrusive means. Session-level aggregates (post-M2) are more likely to pass this test than raw click-level data.

*Balancing test:* Users of a fintech platform have a heightened expectation of data protection given the financial nature of the service. Combining behavioural tracking with transaction history is not a reasonable expectation from service delivery. The processing must demonstrate it does not override these expectations. Safeguards (transparency, opt-out, data minimisation) are necessary to tip the balance in Luminary's favour.

*LIA must document:* the three-part test above; evidence that less intrusive alternatives were considered and rejected; the safeguards applied.

**Art. 6(4) — Compatibility Assessment for Transaction Data**

Transaction history was collected under Art. 6(1)(b) (performance of contract — delivering financial services). Repurposing it for ML-based commercial profiling requires:

1. *Link between purposes:* Service delivery → commercial profiling. Link is indirect; users would not expect this.
2. *Context of collection:* Financial services context — high sensitivity, high user expectation of data protection.
3. *Nature of data:* Financial data — not a special category under Art. 9, but among the most sensitive personal data in practice.
4. *Consequences:* Decisions about how users are treated commercially. Risk of discrimination, financial exclusion, unequal service.
5. *Safeguards:* Encryption, RBAC, retention limits, bias audit, human review.

*Preliminary assessment:* Compatibility is not straightforward given the financial services context and the mismatch between user expectations at collection and the new purpose. The LIA and compatibility assessment must be conducted by qualified legal counsel and documented before processing begins.

**Art. 9 — Special Category Inference**

Although financial transaction data is not itself a special category under Art. 9 GDPR, transaction descriptors and merchant category codes can *indirectly reveal* special category data. Spending at medical clinics, pharmacies, or reproductive health providers may reveal health status. Donations to religious organisations or political parties reveal religious belief or political opinion. Payments to LGBTQ+ establishments may reveal sexual orientation. Under *OT v Vyriausioji tarnybinės etikos komisija* (CJEU, C-184/20), data that indirectly discloses a special category is treated as Art. 9 data. Legitimate interests is not an available lawful basis for Art. 9 data processing; explicit consent (Art. 9(2)(a)) or another enumerated Art. 9(2) basis is required. Legal counsel must assess whether the ML feature set, after applying the M14 exclusion list, continues to involve indirect Art. 9 revelation, and must confirm the appropriate Art. 9 lawful basis before processing begins.

### Appendix C: Third-Party Processor and Sub-Processor Register

*To be completed before launch. At minimum, the following must be enumerated, with DPA status confirmed:*

| Processor | Role | Data accessed | EU/EEA residency | SCC executed? |
|---|---|---|---|---|
| Cloud Infrastructure Provider (TBD) | Compute, storage for data warehouse and pipeline | All pipeline data | TBD | TBD |
| Data Warehouse Vendor (TBD) | Storage and query for raw events and features | Behavioural + financial features | TBD | TBD |
| ML Platform / Training Infrastructure (TBD) | Model training and inference | Feature datasets | TBD | TBD |
| CRM Platform (TBD) | Downstream consumption of scores for campaigns | User ID + churn/upgrade scores | TBD | TBD |
| Notification Engine (TBD) | Email/push delivery triggered by scores | User ID + contact details + score-derived trigger | TBD | TBD |

*All entries marked TBD must be resolved before launch. Executing SCCs and Transfer Impact Assessments for non-EU processors is a launch prerequisite (M10).*

---

*This DPIA was prepared in accordance with GDPR Article 35 and the WP29/EDPB Guidelines on Data Protection Impact Assessments (wp248rev.01). It should be reviewed by qualified legal counsel before being relied upon for processing decisions.*

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.5/19.5 (95%) |
| Evaluated | 2026-05-01 |
| Target duration | 347422 ms |
| Target cost | $0.8347 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 produces a complete processing description — data categories, data subjects, purpose, how processed, retention period, recipients, and data flow | PASS | Section 1 Processing Description Table covers: data categories (Behavioural, Financial, Inferred, Technical identifiers), data subjects ('Registered users of Luminary's fintech platform located in the EU'), purpose ('churn prediction, upgrade propensity'), how processed (SDK → streaming → warehouse → ML → scoring DB), retention period (flagged as gap with recommendations: raw 90d, features 12m, scores 30d), recipients (internal: Data Engineering, ML/DS, Product, Growth/Marketing, Customer Success; external: cloud infra, analytics/ML vendors), and an ASCII data flow diagram. |
| c2 | Step 2 assesses necessity and proportionality against GDPR Article 5 principles — lawful basis, purpose limitation, data minimisation, storage limitation, and security | PASS | Section 2 Necessity and Proportionality Assessment table rows cover: Lawful basis (Art.6 – 'Not yet met', LIA required), Purpose limitation ('Partially met'), Data minimisation ('Not met' – click sequences flagged as excess), Storage limitation ('Not met' – no retention periods defined), Accuracy ('Not met'), Integrity and confidentiality ('Not yet assessed'), and Transparency ('Not met'). Each row has an assessment, verdict, and evidence/gaps column. |
| c3 | Step 3 assesses risks from the individual's perspective — not the organisation's perspective | PASS | Risk descriptions focus on what happens to the user: R1 'enabling identity theft, financial fraud, and social engineering'; R2 'The user has no visibility or recourse'; R3 'users with certain spending patterns…may be systematically scored lower'; R5 'Users do not know their behaviour is being tracked'; R6 'Users cannot currently access their score…blocks Art. 15/16/17/22 rights'. Organisational liability framing is absent from risk descriptions. |
| c4 | Risk categories cover: unauthorised access, function creep, inaccurate decisions, lack of transparency, inability to exercise rights, and discriminatory effects | PASS | R1 = unauthorised access; R4 = function creep ('scores used beyond stated purposes'); R2 = inaccurate decisions; R5 = lack of transparency; R6 = inability to exercise rights ('blocks Art. 15/16/17/22 rights'); R3 = discriminatory effects ('may encode protected characteristics as proxies'). All six required categories are present. |
| c5 | Every risk rated Medium or above has at least one specific mitigation defined in Step 4 | PASS | Residual Risk Summary table cross-references each risk to mitigations: R1→M2,M3,M4,M5,M13; R2→M7,M8,M9; R3→M8,M9; R4→M4,M12; R5→M6; R6→M6,M7; R7→M2; R8→M10; R9→M2,M5; R10→M1,M11; R11→M14. R7 is Medium and has M2 assigned. All 11 risks (Medium+) have at least one specific mitigation. |
| c6 | Residual risk after mitigation is demonstrably lower than inherent risk for each mitigated risk | PASS | Residual Risk Summary table in Section 4 explicitly maps inherent→residual for all 11 risks: R1 Very High→Medium, R2 High→Low, R3 High→Medium, R4 Very High→Medium, R5 High→Low, R6 High→Low, R7 Medium→Low, R8 High→Medium, R9 High→Low, R10 Very High→Medium, R11 High→Medium. Every residual is strictly lower than its inherent rating. |
| c7 | Step 5 produces a DPO review section with a clear recommendation (Proceed / Proceed with conditions / Do not proceed) | PASS | Section 5 DPO Review states 'DPO recommendation: Proceed with conditions' and enumerates 11 specific pre-conditions before processing can begin (LIA, Art. 6(4) compatibility assessment, Art. 9 feature exclusion, data minimisation, retention policy, privacy notice update, rights portal, sub-processor enumeration, RBAC, bias audit, human-in-the-loop controls). |
| c8 | Step 6 determines whether Article 36 supervisory authority consultation is required with reasoning | PASS | Section 6 Consultation Assessment explicitly states 'Prior consultation not currently required' with the reasoning that no residual risks are High or Very High after full mitigation implementation. It also specifies three conditions that would make consultation mandatory: (a) Art. 6(4) compatibility fails, (b) bias audit finds unmitigatable discriminatory effects, (c) Art. 9(2) basis cannot be established. The relevant supervisory authorities (DPC, CNIL, BfDI) are identified. |
| c9 | Output is written to a file in the correct DPIA format with version, date, owner, and status | PASS | File `work/dpia-behavioural-analytics-pipeline.md` header: 'Version: 1.0 \| Date: 2026-05-01 \| Owner: Data Protection Officer \| Status: Draft'. All four required metadata fields present. |
| c10 | Identifies that continuous ML-based profiling of EU users likely requires a DPIA under Article 35(3)(a) (large-scale profiling) | PARTIAL | Section 2 explicitly cites 'Art. 35(3)(a) — systematic and extensive evaluation of personal aspects of natural persons based on automated processing, including profiling' as a trigger. Also identifies WP29 criteria for large-scale financial data processing and profiling. The DPO Review confirms 'Three Art. 35 triggers apply' with (a) as the first. Ceiling is PARTIAL per test definition. |
| c11 | Output's processing description names the data categories (page views, click sequences, session duration, feature usage, transaction history, account tier), the data subjects (EU users), the purpose (churn / upgrade prediction), the processing means (continuous pipeline + ML model), retention period, recipients (internal CS / sales teams), and includes a data flow diagram | PASS | Section 1 Processing Description Table lists: 'page views (URL, timestamp, referrer), click sequences (element, coordinates, order), session duration, feature usage patterns', 'transaction history', 'account tier'; data subjects 'EU users'; purpose 'churn/upgrade prediction'; processing means 'client-side instrumentation…streaming pipeline…ML models…batch…daily'; retention noted as gap with recommended periods; recipients include Customer Success (CS tooling listed as downstream). ASCII data flow diagram included in both Section 1 and Appendix A. |
| c12 | Output's necessity and proportionality assessment evaluates each Article 5 principle — lawful basis (likely legitimate interest with LIA), purpose limitation (analytics only, not third-party sale), data minimisation (do all signals contribute?), storage limitation (retention proportionate to model training cycle), accuracy, security | PASS | Section 2 table rows: Lawful basis (Art.6(1)(f) legitimate interests with LIA required); Purpose limitation (downstream access creates multiple use paths); Data minimisation (click sequences and coordinates flagged as beyond necessity); Storage limitation ('No retention periods have been defined' — Not met); Accuracy (ML probabilistic scores, no rectification mechanism — Not met); Integrity and confidentiality (security architecture not yet specified — Not yet assessed). All six Article 5 principles assessed with verdicts. |
| c13 | Output's risk assessment is from the individual's perspective — what could happen to a user — not from Luminary's perspective | PASS | Risk descriptions consistently focus on user harm: R2 'The user receives restricted service, is deprioritised for support…The user has no visibility or recourse'; R3 'users…may be systematically scored lower for upgrade propensity, resulting in differential treatment'; R5 'Users do not know their behaviour is being tracked at click/element level'; R11 reveals 'health data; religious belief; political opinion; sexual orientation' about individual users. No risks are framed as Luminary's legal/reputational liability. |
| c14 | Output's risk categories cover unauthorised access, function creep (the score being repurposed for credit decisions or marketing), inaccurate decisions (false-positive churn predictions affecting service tier), lack of transparency (users unaware of scoring), inability to exercise rights (deletion, access), and discriminatory effects (proxy bias from behavioural signals correlating with protected characteristics) | PASS | R1=unauthorised access; R4 function creep explicitly names 'credit risk assessment, account restrictions, fee structure changes, third-party commercial partnerships'; R2 inaccurate decisions — 'data quality issue or model bias…user receives restricted service'; R5 transparency — 'Users do not know'; R6 rights inability — 'blocks Art. 15/16/17/22'; R3 discriminatory effects — 'may encode protected characteristics as proxies…correlated with age, disability, or ethnic background'. All six categories with the specific sub-types requested are covered. |
| c15 | Output's mitigations target each Medium+ risk with at least one specific control — e.g. for function creep: documented purpose limitation in privacy notice, technical access controls preventing the score from feeding marketing systems | PASS | M4 implements RBAC ('Scores: defined downstream consumers only (CRM system account, not humans directly)') and M12 implements 'a data contract or API schema that enforces permitted use cases…Log queries against stated purpose. Quarterly review of downstream consumption patterns' — exactly the combination of technical controls and documented purpose limitation required for function creep. All 11 Medium+ risks have specific, named controls in the mitigation table. |
| c16 | Output's residual risk is demonstrably lower than inherent risk per mitigated risk, with a likelihood × impact recalculation shown after controls | PARTIAL | The Residual Risk Summary table clearly shows inherent→residual for all 11 risks (e.g., R1 Very High→Medium, R2 High→Low). However, the output does not show a post-mitigation likelihood × impact recalculation. Section 3 breaks down inherent risk as Likelihood × Severity, but the residual summary only shows the final rating, not the post-control likelihood and impact components separately. Risk reduction is demonstrated; the L×I recalculation after controls is absent. |
| c17 | Output's DPO review section produces a clear recommendation — Proceed / Proceed with conditions (specifying the conditions) / Do not proceed — not a vague 'this is risky' | PASS | Section 5 states 'DPO recommendation: Proceed with conditions' and immediately lists 11 numbered specific conditions (e.g., '1. Complete LIA…2. Complete Art. 6(4) compatibility assessment…3. Implement Art. 9 feature exclusion list…'). The recommendation is unambiguous and the conditions are concrete, not vague. |
| c18 | Output's Article 36 determination is explicit — supervisory authority consultation IS or IS NOT required, with reasoning tied to whether residual risk remains High | PASS | Section 6 states 'Prior consultation not currently required' with the explicit reasoning 'No — provided all mitigations M1–M13 are fully implemented. R3, R4, R8, and R10 retain Medium residual risk; none exceed that level after mitigation.' Mandatory triggers are tied specifically to residual risk remaining High (Art. 6(4) gate failure, unmitigatable bias audit findings, Art. 9 basis failure). |
| c19 | Output is written to a file with version, date, owner (DPO), and status — not only returned in conversation | PASS | The ARTIFACTS WRITTEN section confirms file `work/dpia-behavioural-analytics-pipeline.md` was written to disk. Header reads: 'Version: 1.0 \| Date: 2026-05-01 \| Owner: Data Protection Officer \| Status: Draft'. Chat response also confirms 'The DPIA has been written to dpia-behavioural-analytics-pipeline.md'. |
| c20 | Output explicitly states this processing triggers Article 35(3)(a) (systematic and extensive evaluation based on automated processing including profiling, on which decisions producing legal/significant effects are based) and likely (b) (large-scale processing of personal data) | PARTIAL | Art. 35(3)(a) is explicitly cited verbatim in Section 2: 'Art. 35(3)(a) — systematic and extensive evaluation of personal aspects of natural persons based on automated processing, including profiling, and on which decisions are made that produce legal or similarly significant effects.' Art. 35(3)(b) is not explicitly cited by article number — instead the document references 'WP29 Guidelines on DPIAs — large-scale processing of financial data combined with behavioural profiling' as a separate trigger. The criterion requires explicit citation of both (a) and (b); only (a) is explicitly named. |

### Notes

This is an exceptionally thorough DPIA output. It covers all six required steps with depth and specificity: a complete processing description with ASCII data flow diagrams, a systematic Article 5 proportionality table with explicit verdicts, an individual-perspective risk assessment with 11 named risks, 14 specific mitigation measures each cross-referenced to risk IDs with residual ratings, a clear 'Proceed with conditions' DPO recommendation with 11 enumerated pre-conditions, and an explicit Article 36 determination with conditional triggers. The two partial scores reflect: (1) c16 — residual risk reduction is clearly shown but without a formal post-mitigation likelihood × impact breakdown (only final ratings); (2) c20 — Art. 35(3)(a) is explicitly cited verbatim but Art. 35(3)(b) is referenced only through WP29 guidelines language without the article number. A notable strength is the Art. 9 inference finding (R11/M14) identifying CJEU case law C-184/20 and the merchant-category exclusion list requirement — this goes beyond what most DPIA templates address. The Art. 6(4) compatibility assessment gate for transaction data repurposing (R10/M11) is also correctly identified as a potential processing blocker.
