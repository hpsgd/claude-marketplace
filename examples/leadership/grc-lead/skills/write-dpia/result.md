# Write Dpia

Scenario: A user invokes the skill for a processing activity that clearly triggers GDPR Article 35. Does the skill complete all six steps — processing description, necessity and proportionality, individual-perspective risk assessment, mitigation measures with residual risk reduction, DPO review section, and supervisory authority consultation determination?

## Prompt

> /grc-lead:write-dpia "Behavioural Analytics Pipeline — Luminary (a fintech platform) wants to build a pipeline that tracks detailed user behaviour (page views, click sequences, session duration, feature usage patterns) and uses ML to predict which users are likely to churn or upgrade. This data will be combined with transaction history and account tier. Users are in the EU. The pipeline will run continuously and produce per-user scores updated daily."
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've completed the DPIA for Luminary's Behavioural Analytics Pipeline. The document is saved and ready for review. Here are the critical findings:

## DPIA Status: **HIGH RISK — Conditional Approval**

### Why This Is High-Risk

The combination of **financial data + ML-driven behavioural profiling** triggers GDPR Article 35(3) mandatory DPIA on two grounds:

1. **Automated decision-making (Art. 35(3)(a)):** ML churn/upgrade scores inform marketing campaigns and offer eligibility — this has meaningful impact on user treatment.
2. **Systematic monitoring (Art. 35(3)(b)):** Fine-grained behavioural tracking (page views, click sequences, session timing) of EU users constitutes systematic observation.

### Very High Risks Identified

| Risk | Impact |
|---|---|
| **R1: Data breach** | Financial + behavioural data exposed → identity theft, account takeover, fraud |
| **R3: Discriminatory effects** | ML model + financial data enables automated creditworthiness profiling. Scores correlated with protected characteristics (age, location, inferred disability) can produce discriminatory outcomes: e.g., low-income users deprioritised from upsell, certain demographics excluded from premium features |
| **R6: Function creep** | Churn scores initially used for marketing; later repurposed for loan decisioning, credit assessment, collection priority without user awareness |

### Current Status: **NOT LAWFUL IN PRESENT FORM**

The processing currently violates:
- **Transparency:** Users unaware of granular tracking or ML scoring
- **Purpose limitation:** No enforcement preventing score misuse for credit decisions
- **Data minimisation:** Over-collects granular behavioural data (likely includes non-predictive fields)
- **Rights:** No mechanism for users to access/explain/correct their scores

### 7 Pre-Launch Conditions (BLOCKING)

Processing cannot begin until:

1. **Lawful basis documented** — Legitimate Interest Assessment or explicit consent (Legal/DPO, due May 15)
2. **Data minimisation audit** — remove non-essential behavioural fields (Data Science, due May 15)
3. **Transparency update** — revised Privacy Policy + in-product disclosure live (Product/Legal, due May 15)
4. **Subject Access process** — users can request score + explanation within 30 days (Product/DPO, due May 20)
5. **Encryption verified** — security audit confirms AES-256 at rest, TLS in transit, key management (Security, due May 20)
6. **Fairness audit (pre-launch)** — model tested for disparate impact across demographics before deployment (ML Eng, due May 15)
7. **Access logging live** — all data access logged + TTL deletion controls tested (DevOps, due May 20)

### 16 Mitigation Measures (All Feasible)

After implementation, residual risk drops from **Very High → Low/Medium**, including:
- Encryption + audit logging (R1)
- Monthly bias audits + fairness testing (R3)
- API-level access control + function creep contracts (R6)
- Data minimisation + anonymisation (R4, R7)
- Model explainability (SHAP/LIME) for user explanations (R5)

### Supervisory Authority Consultation

**Recommended: Submit Article 36 consultation** to relevant DPA (e.g., ICO, CNIL, BfDI depending on Luminary's Member State) 4 weeks before launch. This is not mandatory (risk is mitigable) but best practice for fintech + profiling + high DPA scrutiny in this sector. DPA has 8 weeks to respond.

### Critical Dependencies for Launch

- Data minimisation must happen **before** fairness audit (fewer fields = lower bias risk)
- Fairness audit must be **pre-launch**, not post-launch (gap: between launch + first audit is high-risk)
- SAR process requires explainability (M3 + M5 paired)
- Function creep prevention requires contractual + technical controls (M8 + M15 paired)

---

**Bottom line:** Luminary can proceed with this processing **if all pre-launch conditions are met by May 20, 2026**, and DPA approval received (if consulting). The risks are substantial but mitigable. The blocking issue is lack of transparency and user controls — fix those and the legal/ethical case improves materially.

### Artifacts written

#### `work/DPIA-behavioural-analytics.md`

```
# DPIA: Behavioural Analytics Pipeline — Luminary

**Version:** 1.0  |  **Date:** 2026-05-04  |  **Owner:** Data Protection Officer (Luminary)  |  **Status:** Draft for DPO Review

---

## 1. Processing Description

### Overview
Luminary intends to deploy a continuous behavioural analytics pipeline that collects, processes, and scores user interactions within the fintech platform to predict customer churn and upgrade likelihood. The pipeline combines granular user behaviour data with transaction history and account tier information, producing daily per-user ML-driven risk/opportunity scores used to inform targeted retention and upsell campaigns.

### Processing Activity Table

| Aspect | Detail |
|---|---|
| **What personal data** | (1) Behavioural: page views, click sequences, session duration, feature usage patterns, navigation paths, time-on-page; (2) Financial: transaction history, account tier, payment methods, account balance, spending patterns; (3) Transactional metadata: user ID, email, account creation date, device fingerprint, IP address, geolocation |
| **Whose data** | Active and inactive customers of Luminary (fintech platform users, aged 18+, located in EU jurisdictions) |
| **Purpose** | Primary: predict customer churn and upgrade/upsell likelihood to inform targeted retention and monetisation campaigns. Secondary: improve product UX via behavioural insights, reduce churn-related revenue loss, optimise marketing spend. |
| **How processed** | (1) Collection: server-side event tracking (implicit, not requiring per-action consent), (2) Storage: anonymised behaviour events + PII-linked account records in data warehouse, (3) Enrichment: joined with transaction history and account tier, (4) Analysis: ML model training on historical cohorts to predict future behaviour, (5) Scoring: daily batch execution producing per-user churn/upgrade probability scores (0–100), (6) Application: scores exposed to marketing automation, retention campaign system, and product analytics dashboards |
| **Retention period** | Behavioural events: 24 months (online); 12 months (archived for analytics). Transaction data: 7 years (regulatory requirement). Per-user scores: updated daily, retained for 36 months for model drift analysis. Users: deletion on account closure + 12-month grace period. |
| **Recipients** | Internal: Product team (feature decisions), Marketing/Retention team (campaign targeting), Analytics team (model development), Finance (regulatory reporting). External: none at present; potential future ML/analytics processors require prior DPIA amendment. |
| **Data flows** | User interaction → event log → ETL pipeline → data warehouse (joined with transaction + account tier) → ML scoring model → scores table → API consumption by retention + marketing systems → targeting decisions. Cross-border: EU-only storage initially; future cloud processor evaluation required. |

### Data Flow Diagram

```
[EU User] 
    ↓ (page views, clicks, session data)
[Event Tracking Layer]
    ↓
[Data Warehouse — EU region]
    ├─ Behavioural events (24mo online, 12mo archive)
    ├─ Transaction history (PII-linked, 7yr retention)
    └─ Account tier metadata
    ↓
[ML Pipeline — Churn/Upgrade Model]
    ↓
[Scores Table] (updated daily)
    ↓
[APIs] → Marketing Automation, Retention Campaigns, Product Analytics
    ↓
[Targeting Decisions, Campaign Execution]
```

**Key flow assumption:** All data processed and stored within EU jurisdiction (no third-country transfers at present).

---

## 2. Necessity and Proportionality

### Principle-by-Principle Assessment

| Principle | Assessment | Evidence | Verdict |
|---|---|---|---|
| **Lawful basis (Art. 6)** | Legitimate interest (business: churn reduction, revenue optimisation) OR explicit opt-in consent. Basis not yet stated in product terms or privacy policy. Must be documented. | Need to review: (1) current Terms of Service for consent language, (2) Privacy Policy for fair processing notice, (3) any existing opt-out mechanism for analytics. | **Partially met** — must establish and document lawful basis before processing begins. Recommend: Legitimate interest assessment (LIA) for churn prediction OR explicit consent toggle in settings. |
| **Purpose limitation (Art. 5(1)(b))** | Stated purpose: churn/upgrade prediction for retention/upsell targeting. Risk: scores may be repurposed (loan decisioning, fraud scoring, credit assessment) without user knowledge. Prevention mechanism needed. | Must audit retention system + marketing automation for score consumption. Code review of API consumers. | **Partially met** — purpose is clear but requires enforcement mechanism. Recommend: API-level access control; audit logging of score consumption; contractual restrictions on internal use. |
| **Data minimisation (Art. 5(1)(c))** | Granular behavioural tracking (click sequences, feature usage) enables rich profiling but introduces scope creep risk. Question: Could aggregate/anonymised metrics achieve same goal? Example: "session duration >30min" instead of click-by-click timeline. | Requires data architect review: (1) which behavioural fields directly improve model accuracy, (2) which are "nice to have" but not essential, (3) can page views be aggregated vs granular. | **Not met** — current design assumes all data needed; likely over-collects. Recommend: ML model feature importance audit; remove non-predictive fields; compress granular sequences to summary stats. |
| **Accuracy (Art. 5(1)(d))** | ML predictions are inherently probabilistic; users have no mechanism to view/challenge their churn score or the reasons for it. Inaccurate scores → wrong targeting → users sent unwanted campaigns or excluded from beneficial offers. | Must establish: (1) user right to explanation of score + model inputs, (2) user ability to request score recalculation, (3) appeals process for harmful predictions. Currently absent. | **Not met** — users cannot access/contest their scores. Recommend: Implement subject access request (SAR) process disclosing score + top model features; allow users to request re-scoring if circumstances change; document model accuracy metrics (precision, recall, false positive rate). |
| **Storage limitation (Art. 5(1)(e))** | Retention periods stated (24mo behavioural, 7yr transaction, 36mo scores) but automated deletion mechanism not confirmed. Manual cleanup risks data lingering indefinitely. | Code review: (1) are DELETE/anonymisation jobs scheduled + logging successful completion?, (2) what is fallback if job fails?, (3) is there audit trail of deletions? | **Partially met** — retention periods defined but automation unclear. Recommend: Implement automated TTL-based deletion with failure alerts; audit log all data deletion events; confirm backup retention aligns with primary deletion. |
| **Integrity and confidentiality (Art. 5(1)(f)) + Art. 32** | Financial + behavioural data requires strong protections. Assumed: encryption in transit (TLS), at rest (AES-256), and access controls (role-based). But not verified. | Requires security assessment: (1) encryption implementation + key management, (2) database access controls (who can query raw data?), (3) API authentication (token handling, expiry), (4) audit logging (all data access logged?), (5) incident response plan. | **Partially met** — likely implemented but unverified. Recommend: Complete security audit per NIST SP 800-53 or equivalent; document encryption at rest + transit; confirm MFA for admin access; establish 30-day log retention for access events; execute incident response drill. |

### Summary Verdict

**Overall: Partially proportionate.** Processing is justified in purpose (churn reduction has legitimate interest) but overstretched in scope (data minimisation violated) and lacks individual protections (no accuracy/transparency/rights mechanisms). **Processing must not begin until:** (1) lawful basis established + documented, (2) data minimisation audit removes non-essential fields, (3) subject access + explanation mechanisms implemented, (4) security controls verified.

---

## 3. Risk Assessment

### Risk Table

| # | Risk | Description | Likelihood | Severity | Overall Risk |
|---|---|---|---|---|---|
| **R1** | **Unauthorised access to combined financial + behavioural data** | Breach of data warehouse, API, or backup systems exposes customer financial records + behavioural profiles. Attacker gains account balance, transaction history, spending patterns, feature usage (lifestyle inference). Enables identity theft, account takeover, fraud. | High | Very High | **Very High** |
| **R2** | **Inaccurate ML scoring leading to harmful targeting decisions** | Model trained on historical bias (e.g., overrepresents profitable customers, underrepresents lower-income users). Model drift post-deployment (patterns change but model not retrained). Inaccurate churn predictions result in: (a) loyal customers sent aggressive retention offers (signal of distrust), (b) at-risk customers ignored (revenue loss), (c) discriminatory targeting (e.g., higher-cost offers to certain demographics). | Medium | High | **High** |
| **R3** | **Discriminatory effects from financial + behavioural profiling (Art. 35(3)(a))** | ML model directly processes financial data (transaction history, account balance, payment methods) + behavioural signals (feature usage, time-to-purchase) to assign churn/upgrade scores. Combination enables automated creditworthiness/financial-risk profiling. If scores correlate with protected characteristics (age, geographic origin, inferred disability), model produces discriminatory outcomes: e.g., users of low transaction volume systematically ranked as high-churn and deprioritised from upsell campaigns; young users excluded from premium features; users in certain postal codes assigned lower upgrade likelihood. | Medium | Very High | **Very High** |
| **R4** | **Lack of transparency and informed consent** | Users unaware of detailed behavioural tracking (page views, click sequences, session data logged per interaction). No clear notice of ML scoring or use of scores to determine marketing/product decisions. No consent mechanism or opt-out for analytics (only account deletion). Users cannot predict how their behaviour affects treatment. | High | High | **High** |
| **R5** | **Inability to exercise rights (Art. 15, 16, 17, 21)** | Users cannot: (a) access their churn score + explain why model assigned it, (b) correct inaccurate financial/behavioural data (e.g., transaction incorrectly categorised), (c) delete their data without closing account (12-mo grace period may still retain scores for analysis), (d) object to marketing campaigns driven by scores. Creates rights vacuum. | High | Medium | **High** |
| **R6** | **Function creep — scores repurposed for high-risk decisions** | Churn/upgrade scores initially used for marketing targeting. Later internal use cases emerge: loan decisioning (score correlated with creditworthiness), fraud detection (score used as risk signal), internal credit assessment, collection priority (score used to determine payment schedule). Users consented/accepted scores for marketing; unaware of credit/underwriting use. Constitutes material purpose change requiring new DPIA. | Medium | Very High | **Very High** |
| **R7** | **Re-identification and cross-linking** | Behavioural events anonymised at source (hashed user ID). But when joined with transaction history + account tier (inherently identifiable), re-identification becomes trivial. Fintech context: account balance + specific transaction amounts form unique identifier. Adversary can link "anonymous" behaviour to real individual. Enables profiling without consent. | High | Medium | **High** |
| **R8** | **Model drift and degradation over time** | ML model trained on historical data. User behaviour changes (economic downturn, new competitor, product pivot). Model not retrained; predictions become inaccurate. Churn model drifts; retention campaigns target wrong cohorts; upgrade model over-predicts uplift. Silent failure — no flag that scores are stale. Results in wasted marketing spend + poor targeting. | Medium | Medium | **Medium** |
| **R9** | **Retention data compromise via backup/disaster recovery** | Backups of data warehouse stored in secondary region or external provider (assumption). Backup retention policies may exceed active data retention (e.g., backups kept 1yr, active data deleted after 24mo). Breach of backup copy exposes deleted user data. | Medium | High | **High** |
| **R10** | **Inadvertent profiling of special categories** | Behavioural data (feature usage, time-on-page, session patterns) may infer health status (e.g., frequent visits to savings/budgeting features = financial stress/mental health concern), religion (transaction with religious organisation), sexual orientation (premium feature usage patterns), disability (session duration, feature usage variations). Even if not intentional, model may learn and use these inferences. GDPR Art. 9 prohibits processing special categories without legal basis. | Medium | High | **High** |
| **R11** | **Cross-border data transfer risks (future)** | Currently EU-only storage assumed. But future scaling may move data to cloud processors (AWS, GCP, Azure with non-EU regions). Transfers to non-EU jurisdictions expose data to foreign government access (CLOUD Act, similar US laws). Standard contractual clauses insufficient post-Schrems II. Prior DPIA required before any transfer. | Low (currently) | High | **Medium** (escalates to High if transfer planned) |

### Risk Assessment Notes

- **Financial + Behavioural combination (R3, R6):** This combination is explicitly called out in GDPR guidance as triggering Article 35(3)(a) — automated decision-making with legal/significant effect. Churn/upgrade scoring, if used to deny/delay services or alter pricing/offers, constitutes automated decision-making. Risk is elevated.
- **Transparency/Rights (R4, R5):** Current product does not disclose fine-grained behavioural tracking or ML scoring. Users have no mechanism to contest scores or opt out without closing accounts. Gap is material.
- **Model explainability (R2, R3):** No indication that model is explainable (e.g., LIME, SHAP). Cannot debug discriminatory outputs or explain to users why they received a score. Risk mitigation requires explainability.

---

## 4. Mitigation Measures

### Mitigation Table

| # | Measure | Risk(s) addressed | Implementation status | Owner | Residual risk |
|---|---|---|---|---|---|
| **M1** | **Establish lawful basis (Legitimate Interest Assessment + Privacy Policy update)** | R4 (transparency), R5 (rights) | Planned (Pre-launch) | Legal + DPO | Low — users informed of basis; right to object enabled |
| **M2** | **Data minimisation audit: remove non-predictive behavioural fields** | R2 (accuracy overfitting), R4 (excessive data), R5 (subject access complexity) | Planned (Pre-launch) | Data Science + Architecture | Low — scope reduced; model interpretability improves |
| **M3** | **Implement ML model explainability (SHAP/LIME feature importance)** | R2 (inaccurate decisions), R3 (discriminatory effects), R5 (right to explanation) | Planned (Pre-launch) | ML Engineering | Medium — explainability implemented, but user-facing explanation UX not yet designed |
| **M4** | **Automated bias audit of model outputs (monthly)** | R3 (discriminatory effects) | Planned (First month post-launch) | Data Science + Analytics | Low — detects and flags drift; requires response plan for disparate impact |
| **M5** | **Implement Subject Access Request (SAR) process** | R5 (right to access, right to explanation) | Planned (Pre-launch) | Product + DPO | Low — SAR fulfillable within 30 days; includes score, top-3 model features, training cohort description |
| **M6** | **Encryption at rest (AES-256, managed keys) + in transit (TLS 1.3)** | R1 (unauthorised access), R9 (backup compromise) | Assumed implemented; requires verification | Security/DevOps | Medium — encryption strong but key management audit needed |
| **M7** | **Audit logging: all data access (read/write/delete) + API calls to scores** | R1 (breach detection), R5 (accountability), R6 (function creep detection) | Planned (Pre-launch) | Engineering/Security | Low — logs retained 12mo; enables forensics + compliance audits |
| **M8** | **API-level access control: restrict score consumption to approved systems only** | R5 (rights), R6 (function creep) | Planned (Pre-launch) | Architecture | Low — role-based access; score API requires authentication; usage monitored |
| **M9** | **Automated TTL-based data deletion (behavioural 24mo, scores 36mo)** | R5 (storage limitation), R9 (backup retention) | Planned (Pre-launch); requires verification | DevOps/Database | Low — automated; failure alerts configured |
| **M10** | **Privacy-by-Design: anonymise sensitive financial fields where possible** | R1 (breach impact), R3 (profiling), R10 (special categories inference) | Planned (Design phase) | Architecture | Medium — anonymisation may reduce model accuracy; trade-off analysis needed |
| **M11** | **User notification of ML scoring + opt-out mechanism for direct marketing** | R4 (transparency), R5 (right to object) | Planned (Privacy Policy + Settings UX) | Product + Marketing | Low — users can opt out of marketing campaigns; churn prediction happens server-side regardless (mitigation: limiting downstream use) |
| **M12** | **Model retraining schedule + drift monitoring** | R2 (inaccuracy), R8 (model drift) | Planned (Quarterly retraining, weekly drift checks) | ML Engineering | Low — automated alerts if drift detected; manual review required before retraining |
| **M13** | **Data Processing Agreement (DPA) with all processors; SCC for any non-EU transfers (if applicable)** | R11 (cross-border transfer), R1 (processor security) | Pre-launch | Legal/DPO | Low — DPA establishes processor obligations; SCC required if EU transfer planned |
| **M14** | **Incident response plan: data breach notification within 72h of discovery** | R1 (breach), R9 (backup compromise) | Planned (Q2 2026) | Security + Legal | Low — establishes notification timeline; testing via tabletop exercise recommended |
| **M15** | **Restrict churn/upgrade scores to marketing/retention use only; contractual prohibition on credit/underwriting use** | R6 (function creep) | Planned (Pre-launch via API + internal contracts) | Legal + Architecture | Low — enforced via API access control + documentation |
| **M16** | **Fairness testing before model deployment: audit for disparate impact across demographics** | R3 (discriminatory effects) | Planned (Pre-launch) | ML Engineering + Product | Medium — fairness metrics (equal opportunity ratio, calibration across groups) established; threshold for acceptable disparity defined by business + legal |

### Mitigation Summary

**Overall residual risk after mitigation: Medium→Low** (after all measures implemented)

- **Very High risks (R1, R3, R6):** Mitigated to Medium-Low via encryption (M6), bias audit (M4), fairness testing (M16), and function creep controls (M8, M15).
- **High risks (R2, R4, R5, R7, R9, R10):** Mitigated to Low via explainability (M3), transparency (M11), SAR process (M5), anonymisation (M10), and data deletion (M9).
- **Medium risks (R8, R11):** Mitigated to Low via retraining schedule (M12) and contractual safeguards (M13).

**Critical dependencies:**
- M2 (data minimisation) must be completed before M4 + M16 (bias audit). Fewer features = lower false positive risk.
- M5 (SAR process) requires M3 (explainability) to produce meaningful explanations.
- M11 (user opt-out) requires M1 (lawful basis established) and privacy policy update.

---

## 5. DPO Review

### DPO Assessment

| Item | Assessment |
|---|---|
| **DPIA required?** | **YES** — This processing is high-risk under GDPR Article 35(3) on multiple grounds: (a) Automated decision-making with legal/significant effect (Art. 35(3)(a)): ML-driven churn/upgrade scores inform marketing targeting, campaign frequency, and offer eligibility. Scores have meaningful impact on user experience and commercial treatment. (b) Systematic monitoring (Art. 35(3)(b)): granular behavioural tracking (page views, click sequences, session timing) constitutes systematic observation of user behaviour. (c) Large-scale processing of special categories (Art. 35(3)(b)): combined financial + behavioural data risks inadvertent profiling of protected characteristics (health, disability, financial vulnerability). (d) Core business activity (Art. 35(3)(c)): processing is central to user targeting and business model. DPIA is mandatory. |
| **Processing lawful?** | **CONDITIONAL** — Lawfulness depends on: (1) Lawful basis established (Art. 6): Recommend Legitimate Interest (retention/churn reduction has legitimate business purpose and is not overridden by user interests). Alternative: explicit opt-in consent (less restrictive on user choice, but requires clear notice). (2) Fairness (Art. 5(1)(a)): Must be transparent; currently NOT transparent. (3) Necessity (Art. 5(1)(c)): Data minimisation audit (M2) must confirm all fields necessary. **Verdict: NOT lawful in current form. Processing must not begin until lawful basis documented, fairness notice provided, and data minimisation audit completed.** |
| **Proportionate?** | **NO (currently).** Assessment: (1) Purpose is legitimate (churn reduction). (2) But means are excessive: data minimisation principle violated (over-collects granular behavioural data). (3) Individual protections absent: no transparency, no right to explanation, no opt-out for analytics (only account deletion). (4) Risks not adequately mitigated without M1–M6. **Verdict: Disproportionate in current form. Rebalance required.** |
| **Risks adequately mitigated?** | **CONDITIONAL** — After implementing M1–M16 (all measures planned for pre-launch), residual risks are Medium→Low. But: (1) Several measures are **Planned** not **Implemented** (M1, M2, M3, M5, M11, M12, M14, M15, M16). (2) M6 encryption is **Assumed** implemented; requires verification. (3) M4 bias audit is monthly post-launch, not pre-launch — high-risk period between launch and first audit. **Verdict: Risks will be adequately mitigated IF all Planned measures are completed before launch and Assumed measures are verified. Gap: M4 bias audit should move to pre-launch.** |
| **DPO recommendation** | **CONDITIONAL APPROVAL — Proceed if and only if:** 1. Lawful basis (Legitimate Interest Assessment or explicit consent) documented and approved by Legal before launch. 2. Data minimisation audit (M2) completed; non-essential fields removed from collection/storage. 3. Transparency notice (updated Privacy Policy + in-product disclosure) published and live before processing begins. 4. SAR process (M5) + subject right to explanation operational before launch. 5. Encryption at rest/transit (M6) verified by security audit. 6. Bias audit (M4) completed pre-launch for initial model (move from post-launch to pre-launch). 7. All access logging + retention controls (M7, M9) operational. **If any of 1–7 incomplete at launch date, processing must be postponed.** |
| **Conditions (if any)** | **(a) Pre-launch (blocking):** Conditions 1–7 above. (b) Post-launch (continuous):** Monthly fairness audits (M4) with results reviewed by DPO. Incident response drills (M14) executed quarterly. Model retraining assessment (M12) reviewed by DPO at each cycle. Bias audit findings above defined threshold trigger processing pause + remediation. (c) Ongoing:** Annual DPIA review (scheduled May 2027). New DPIA required if: model used for credit/underwriting decisions (R6), data transferred outside EU (R11), behavioural data scope expanded, special categories processed. (d) Stakeholder:** All conditions assigned to named owners with target completion dates (see table below). |
| **Review date** | **12 months: May 2027.** Triggers: (1) Annual statutory review. (2) Model retraining + significant accuracy/fairness changes. (3) Any material change to processing purpose, scope, or recipients. (4) Incident or audit finding affecting risk profile. Earlier review if: bias audit flags disparate impact, data breach occurs, user complaints escalate, regulatory inquiry received. |

### Pre-Launch Conditions Checklist

| Condition | Target date | Owner | Status |
|---|---|---|---|
| 1. Lawful basis documented (LIA or consent framework) | 2026-05-15 | Legal + DPO | Pending |
| 2. Data minimisation audit completed; non-essential fields identified for removal | 2026-05-15 | Data Science + Architecture | Pending |
| 3. Privacy Policy + in-product disclosure updated and live | 2026-05-15 | Product + Legal | Pending |
| 4. SAR process documented + operational (30-day SLA) | 2026-05-20 | Product + DPO | Pending |
| 5. Encryption at rest/transit verified via security audit | 2026-05-20 | Security + DevOps | Pending |
| 6. Model fairness audit (pre-launch) completed; disparate impact assessment passed | 2026-05-15 | ML Engineering | Pending |
| 7. Access logging + TTL deletion controls live and tested | 2026-05-20 | DevOps | Pending |

---

## 6. Supervisory Authority Consultation

### Consultation Determination

| Question | Answer |
|---|---|
| **What is the highest residual risk rating after mitigation?** | Medium→Low (after all measures implemented). Before implementation: Very High (R1, R3, R6). **Current state (unmitigated): Very High.** |
| **Can residual risk be reduced further?** | **Yes.** Primary levers: (a) Limit score use to marketing only; ban credit/underwriting use (eliminates R6 Very High). (b) Implement pre-launch fairness audit (eliminates R3 risk of launch with biased model). (c) Implement differential privacy on model training (reduces R1 re-identification risk). These are feasible and reduce residual from High→Low. |
| **After all feasible mitigations, is residual risk High or Very High?** | **NO.** After M1–M16 (all measures complete), residual risk is Low→Medium. Acceptable range for standard processing (no prior consultation required). |
| **Is processing subject to Art. 35(3)(a) automated decision-making?** | **YES.** Churn/upgrade scores inform marketing automation and offer eligibility decisions. Art. 35(3)(a) applies. Does this trigger mandatory prior consultation? Per [GDPR Recital 75](https://gdpr-info.eu/recitals/75/), mandatory consultation required only if "the controller is not able to mitigate the risk adequately." Luminary can mitigate (see conditions above). **Conclusion: Consultation not mandatory if all conditions met.** |
| **Is processing subject to Art. 35(3)(b) systematic monitoring?** | **YES.** Granular behavioural tracking of online user activity is systematic monitoring. Does this trigger mandatory prior consultation? Per ICO guidance, systematic monitoring is high-risk if processing reveals sensitive information or enables targeting/discrimination. Luminary's processing does carry this risk (R3, R4). **Conclusion: Consultation warranted as best practice, even if not strictly mandatory.** |
| **Prior consultation required?** | **RECOMMENDED (not mandatory if conditions met).** Rationale: (1) Art. 35(3)(a) and (3)(b) both apply. (2) Risk level prior to mitigation is Very High (R1, R3, R6). (3) Supervisory authorities (ICO, CNIL, etc.) have issued guidance on fintech + profiling risks; advance consultation builds confidence. (4) Cost: 3–4 weeks for DPA response; low burden given processing timeline. **Recommend: Submit Article 36 consultation request to primary DPA [e.g., ICO if UK-operated] or relevant Member State DPA 4 weeks before intended launch.** |
| **Which supervisory authority?** | Luminary's primary data protection authority based on: (1) Main establishment (where central processing decisions made), (2) User base (EU-wide, so multiple DPAs potentially). **Assumption: Luminary based in [EU Member State]; recommend consulting that state's DPA (e.g., Germany = BfDI, France = CNIL, UK = ICO).** Alternative: Submit to one DPA; cite Article 36(4) for DPA to consult others if processing affects residents of other states. |
| **Consultation timeline** | **Mandatory DPA response deadline: 8 weeks from submission (Art. 36(4)).** Recommended consultation timeline: (1) DPIA finalised + conditions list completed: Week 1 (May 4, 2026). (2) Legal review + consultation request drafted: Week 2 (May 11, 2026). (3) Submit Art. 36 request: Week 3 (May 18, 2026). (4) Await DPA response: Weeks 3–10 (May 18 – July 13, 2026). (5) Address DPA feedback (if any): Week 11–12 (July 13 – July 27, 2026). (6) Process launch: **Not before July 27, 2026** (after DPA response window closes). |

### Supervisory Authority Consultation Summary

**Recommendation: SUBMIT ARTICLE 36 CONSULTATION REQUEST** to the relevant supervisory authority before launch.

**Justification:**
- Processing involves high-risk automated decision-making (Art. 35(3)(a)) + systematic monitoring (Art. 35(3)(b)).
- Financial + behavioural data combination creates risk of discriminatory outcomes (protected grounds: age, disability, financial vulnerability).
- Fintech sector is under regulatory scrutiny (EBA guidelines on credit risk profiling; ECB fintech supervision).
- Early engagement with DPA reduces compliance risk and builds trust.

**Key point:** Consultation is not admission of wrongdoing; it is DPA engagement on a legitimate business activity. Most fintech firms consulting on similar processing receive approval with minor conditions.

**Deliverable for consultation request:**
- This DPIA (sections 1–5 complete)
- Data minimisation audit (M2 output)
- Fairness audit report (M16 output)
- Privacy Policy amendments
- Copies of mitigating measures (M1–M16 implementation evidence)

---

## Appendices

### Appendix A: Data Flow Diagram (Detailed)

```
┌──────────────────────────────────────────────────────────────────────┐
│ EU User Jurisdiction (GDPR applies)                                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [1. Event Generation]                                              │
│  ├─ Page view (URL, timestamp, user ID)                             │
│  ├─ Click event (element, target, session ID)                       │
│  ├─ Session duration (login → logout)                               │
│  ├─ Feature usage (API call log)                                    │
│  └─ Device metadata (IP, user agent, device ID)                     │
│       ↓ [Client-side tracking script or server-side logging]        │
│                                                                      │
│  [2. Event Pipeline — Real-time Collection]                         │
│  ├─ Events queued (Kafka/Pub-Sub)                                   │
│  ├─ Deduplicated & validated                                        │
│  └─ Batched to event store (24h retention online)                   │
│       ↓                                                              │
│                                                                      │
│  [3. Data Warehouse — EU Region (e.g., EU-West Frankfurt)]          │
│  ├─ Table: events (user_id, event_type, timestamp, properties)      │
│  ├─ Table: user_transactions (user_id, account_balance, txn_amount) │
│  ├─ Table: account_tier (user_id, tier, feature_access_level)       │
│  └─ Table: user_identity (user_id, email, name, onboarded_date)     │
│                                                                      │
│  [4. ETL Pipeline — Join & Enrich]                                  │
│  ├─ Join events + transactions on user_id                           │
│  ├─ Enrich with account_tier                                        │
│  ├─ Aggregate: session_count, avg_session_duration, feature_usage   │
│  └─ Create feature matrix (user_id, feature_1, ..., feature_N)      │
│       ↓                                                              │
│                                                                      │
│  [5. ML Pipeline — Churn & Upgrade Models]                          │
│  ├─ Historical training data (users active 12mo ago)                │
│  ├─ Labels: churn = user inactive >90d, upgrade = tier_change       │
│  ├─ Model: XGBoost / Neural Net predicting P(churn), P(upgrade)     │
│  ├─ Output: per-user churn_score (0–100), upgrade_score (0–100)    │
│  └─ Schedule: Daily batch execution (22:00 UTC)                     │
│       ↓                                                              │
│                                                                      │
│  [6. Scores Table — Per-User Predictions]                           │
│  ├─ Schema: (user_id, churn_score, upgrade_score, last_updated)     │
│  ├─ Retention: 36 months (for model drift analysis)                 │
│  └─ Access: API (read-only) for downstream systems                  │
│       ↓                                                              │
│                                                                      │
│  [7. API Consumers — Downstream Use]                                │
│  ├─ Marketing Automation System                                      │
│  │   ├─ Query: SELECT users WHERE churn_score > 70                  │
│  │   └─ Action: Send retention offer email                          │
│  ├─ Campaign Management System                                       │
│  │   ├─ Query: SELECT users WHERE upgrade_score > 60                │
│  │   └─ Action: Display premium feature upsell                      │
│  └─ Analytics Dashboard                                              │
│      └─ Aggregated metrics: avg churn_score by segment              │
│                                                                      │
│  [8. User Treatment — Marketing/Product Decisions]                  │
│  ├─ High churn_score → retention emails, win-back offers            │
│  ├─ High upgrade_score → premium feature recommendations            │
│  └─ Low scores → standard treatment                                 │
│                                                                      │
│  [9. Data Retention & Deletion]                                     │
│  ├─ Behavioural events: 24mo (TTL job runs daily)                   │
│  ├─ Scores: 36mo (for model analysis)                               │
│  ├─ User account closed → all data deleted + 12mo grace period      │
│  └─ Deletion audit log: immutable record of what was deleted        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Appendix B: Lawful Basis Analysis

#### Option 1: Legitimate Interest (Art. 6(1)(f))

**Controller's interest:** Reduce churn revenue loss, identify upsell opportunities, optimise marketing spend.

**Necessity test:** Is the processing necessary to achieve the interest? YES — predictive analytics require behavioural + transaction data to train models; aggregate data alone is insufficient.

**Proportionality test:** Is the interest overridden by user rights/expectations?
- Users expect some marketing targeting (legitimate).
- Users may NOT expect granular click-by-click tracking or ML scoring (not transparent).
- Financial data + behavioural profiling sensitive; users likely have high expectations of privacy.
- **Verdict: Proportionate IF transparency + user controls implemented (M1, M11).**

**Assessment:**
- Lawful basis: YES, if Legitimate Interest Assessment (LIA) completed and documented.
- Recommended actions: (a) Draft LIA document (public-facing summary); (b) Solicit internal stakeholder review (Privacy, Product, Legal); (c) Monitor user objections; (d) Publish in Privacy Policy with user right to object.

#### Option 2: Explicit Consent (Art. 7)

**Consent mechanism:** User opt-in checkbox at account onboarding or within Settings.

**Advantages:** Clearest legal basis; high bar for legitimacy; aligns with GDPR Article 4(11) freely given, specific, informed, unambiguous indication.

**Disadvantages:** Consent withdrawal = inability to process; users may refuse. Churn prediction still valuable without consent (can use aggregate data), but less precise.

**Assessment:**
- Feasible if implemented correctly (M1).
- Recommended: Implement consent + Legitimate Interest as fallback (i.e., if user withdraws consent, fall back to Legitimate Interest for basic marketing targeting, but disable ML scoring).

**Luminary's choice:** Recommend **Legitimate Interest + transparency + user right to object** as primary basis (lower friction), with optional **additional consent** for advanced ML features.

---

### Appendix C: Third-Party Processor List

| Processor | Function | Data categories | Location | Safeguards |
|---|---|---|---|---|
| (Internal: Data Science team) | ML model development, bias audit, retraining | Behavioural events, transaction data, training labels | EU | Access control, audit logging |
| (Internal: Marketing team) | Campaign targeting, offer decision | Scores only (not raw data) | EU | Read-only API access; usage logged |
| (Internal: Product team) | Feature analytics, UX insights | Aggregated metrics only | EU | Dashboard access; no raw data |
| (Cloud provider — to be selected) | Data warehouse hosting, compute | All data (encrypted) | EU-West region | DPA + SCC required before use |
| (Optional: External ML vendor) | Model training/tuning as-a-service | De-identified feature matrix | TBD | DPA + SCC + pseudo-anonymisation |

**Note:** No external processors active at launch. All processing in-house. Any future processor engagement requires prior DPIA amendment + DPA consultation (Art. 36).

---

## Sign-Off

### DPO Review & Approval

**Draft DPIA prepared by:** [Technical team / Product team]  
**Reviewed by:** [DPO name]  
**Date:** [DPO review date]

**DPO Sign-Off:**

I have reviewed this DPIA for the Behavioural Analytics Pipeline. My assessment:

- **DPIA required:** YES (Art. 35(3)(a) + (3)(b))
- **Processing lawful:** CONDITIONAL (subject to pre-launch conditions)
- **Risks adequately mitigated:** YES (after M1–M16 implementation)
- **Recommendation:** CONDITIONAL APPROVAL — Proceed if all pre-launch conditions completed by [target date: 2026-05-20]

**DPO Name:** [___________]  
**Signature:** [___________]  
**Date:** [___________]

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-04 | Initial DPIA draft; submitted for DPO review |
| | | |

---

**Document Status:** Draft for DPO Review  
**Next Action:** DPO review + feedback → Remediate pre-launch conditions → DPO approval → Submit Art. 36 consultation (if required) → Process launch (post-approval)


```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 19.0/19.5 (97%) |
| Evaluated | 2026-05-04 |
| Target duration | 134962 ms |
| Target cost | $0.1620 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 produces a complete processing description — data categories, data subjects, purpose, how processed, retention period, recipients, and data flow | PASS | Section 1 Processing Activity Table covers all elements: data categories (behavioural, financial, transactional metadata), data subjects ('Active and inactive customers of Luminary, aged 18+, located in EU jurisdictions'), purpose ('predict customer churn and upgrade/upsell likelihood'), how processed (6-step flow from collection through scoring to application), retention periods (24mo behavioural, 7yr transaction, 36mo scores), recipients (internal Product, Marketing, Analytics, Finance teams), and a text-art data flow diagram. |
| c2 | Step 2 assesses necessity and proportionality against GDPR Article 5 principles — lawful basis, purpose limitation, data minimisation, storage limitation, and security | PASS | Section 2 'Principle-by-Principle Assessment' table explicitly addresses six rows: Lawful basis (Art. 6), Purpose limitation (Art. 5(1)(b)), Data minimisation (Art. 5(1)(c)), Accuracy (Art. 5(1)(d)), Storage limitation (Art. 5(1)(e)), and Integrity/confidentiality (Art. 5(1)(f) + Art. 32), each with assessment, evidence gaps, and verdict. |
| c3 | Step 3 assesses risks from the individual's perspective — not the organisation's perspective | PASS | Risk descriptions are framed around harms to users: R1 ('Enables identity theft, account takeover, fraud'), R3 ('users of low transaction volume systematically ranked as high-churn and deprioritised from upsell campaigns; young users excluded from premium features'), R4 ('Users unaware of detailed behavioural tracking... Users cannot predict how their behaviour affects treatment'), R5 ('Users cannot: (a) access their churn score + explain why... (c) delete their data without closing account'). Organisational framing (revenue loss, wasted spend) appears only incidentally in R2/R8. |
| c4 | Risk categories cover: unauthorised access, function creep, inaccurate decisions, lack of transparency, inability to exercise rights, and discriminatory effects | PASS | R1='Unauthorised access to combined financial + behavioural data'; R6='Function creep — scores repurposed for high-risk decisions'; R2='Inaccurate ML scoring leading to harmful targeting decisions'; R4='Lack of transparency and informed consent'; R5='Inability to exercise rights (Art. 15, 16, 17, 21)'; R3='Discriminatory effects from financial + behavioural profiling'. All six categories are explicitly named and rated. |
| c5 | Every risk rated Medium or above has at least one specific mitigation defined in Step 4 | PASS | Section 4 Mitigation Table maps measures to risks for all 11 risks (R1–R11, rated Medium to Very High). E.g., R1 → M6 (AES-256 + TLS 1.3) + M7 (audit logging) + M14 (incident response); R3 → M4 (monthly bias audit) + M16 (fairness testing); R6 → M8 (API access control) + M15 (contractual prohibition on credit/underwriting use); R8 (Medium) → M12 (retraining schedule); R11 (Medium) → M13 (DPA + SCC). |
| c6 | Residual risk after mitigation is demonstrably lower than inherent risk for each mitigated risk | PASS | Mitigation Table has a 'Residual risk' column per measure showing reduced risk: e.g., R1 inherent Very High → M6 residual 'Medium — encryption strong but key management audit needed'; R6 inherent Very High → M15 residual 'Low — enforced via API access control + documentation'; R3 inherent Very High → M16 residual 'Medium — fairness metrics established'. Mitigation Summary explicitly states 'Very High risks (R1, R3, R6): Mitigated to Medium-Low'. |
| c7 | Step 5 produces a DPO review section with a clear recommendation (Proceed / Proceed with conditions / Do not proceed) | PASS | Section 5 DPO Assessment table includes a 'DPO recommendation' row with 'CONDITIONAL APPROVAL — Proceed if and only if:' followed by 7 numbered, owner-assigned blocking conditions. This is unambiguously 'Proceed with conditions', not a vague risk statement. |
| c8 | Step 6 determines whether Article 36 supervisory authority consultation is required with reasoning | PASS | Section 6 has a 'Prior consultation required?' row: 'RECOMMENDED (not mandatory if conditions met)' with four explicit reasons. The section also answers: 'After all feasible mitigations, is residual risk High or Very High? NO.' and concludes 'Consultation not mandatory if all conditions met' but recommends submitting an Art. 36 request. The Consultation Summary restates 'SUBMIT ARTICLE 36 CONSULTATION REQUEST' with a 10-week timeline. |
| c9 | Output is written to a file in the correct DPIA format with version, date, owner, and status | PASS | Artifact `work/DPIA-behavioural-analytics.md` header line: '**Version:** 1.0 \| **Date:** 2026-05-04 \| **Owner:** Data Protection Officer (Luminary) \| **Status:** Draft for DPO Review'. All four required fields present. |
| c10 | Identifies that continuous ML-based profiling of EU users likely requires a DPIA under Article 35(3)(a) (large-scale profiling) | PARTIAL | Section 5 DPO Assessment explicitly states: 'DPIA required? YES — This processing is high-risk under GDPR Article 35(3) on multiple grounds: (a) Automated decision-making with legal/significant effect (Art. 35(3)(a)): ML-driven churn/upgrade scores inform marketing targeting...' and Section 6 confirms 'Is processing subject to Art. 35(3)(a) automated decision-making? YES.' Ceiling is PARTIAL so maximum score is 0.5. |
| c11 | Output's processing description names the data categories (page views, click sequences, session duration, feature usage, transaction history, account tier), the data subjects (EU users), the purpose (churn / upgrade prediction), the processing means (continuous pipeline + ML model), retention period, recipients (internal CS / sales teams), and includes a data flow diagram | PASS | Section 1 Processing Activity Table lists all named categories: 'page views, click sequences, session duration, feature usage patterns, navigation paths, time-on-page' plus 'transaction history, account tier'. Data subjects: 'EU jurisdictions'. Purpose: 'predict customer churn and upgrade/upsell likelihood'. Processing means: 'ML model training on historical cohorts... daily batch execution producing per-user churn/upgrade probability scores'. Retention: multiple periods specified. Recipients: 'Marketing/Retention team (campaign targeting)' and others. Data flow diagram included in both Section 1 and Appendix A. |
| c12 | Output's necessity and proportionality assessment evaluates each Article 5 principle — lawful basis (likely legitimate interest with LIA), purpose limitation (analytics only, not third-party sale), data minimisation (do all signals contribute?), storage limitation (retention proportionate to model training cycle), accuracy, security | PASS | Section 2 table rows: Lawful basis ('Legitimate interest... Recommend: Legitimate interest assessment (LIA)'); Purpose limitation ('Analytics only; risk: scores may be repurposed... requires enforcement mechanism'); Data minimisation ('Could aggregate/anonymised metrics achieve same goal?... ML model feature importance audit; remove non-predictive fields'); Storage limitation ('Retention periods stated... automated deletion mechanism not confirmed'); Accuracy ('ML predictions are inherently probabilistic; users have no mechanism to view/challenge their churn score'); Integrity/confidentiality ('Financial + behavioural data requires strong protections... requires security assessment'). |
| c13 | Output's risk assessment is from the individual's perspective — what could happen to a user — not from Luminary's perspective | PASS | Risk descriptions consistently frame harm to users: R3 describes 'users of low transaction volume systematically ranked as high-churn and deprioritised'; R4 'Users unaware of detailed behavioural tracking... No consent mechanism or opt-out'; R5 'Users cannot: (a) access their churn score + explain why model assigned it, (b) correct inaccurate financial/behavioural data, (c) delete their data without closing account'; R6 'Users consented/accepted scores for marketing; unaware of credit/underwriting use'. Organisational losses mentioned in R2 and R8 are secondary. |
| c14 | Output's risk categories cover unauthorised access, function creep (the score being repurposed for credit decisions or marketing), inaccurate decisions (false-positive churn predictions affecting service tier), lack of transparency (users unaware of scoring), inability to exercise rights (deletion, access), and discriminatory effects (proxy bias from behavioural signals correlating with protected characteristics) | PASS | R1=unauthorised access; R6='scores repurposed for loan decisioning, fraud detection, internal credit assessment, collection priority'; R2='Inaccurate ML scoring... Model trained on historical bias... loyal customers sent aggressive retention offers'; R4='Users unaware of detailed behavioural tracking... No clear notice of ML scoring'; R5='Users cannot... access their churn score... delete their data'; R3='scores correlate with protected characteristics (age, geographic origin, inferred disability)... users of low transaction volume systematically ranked as high-churn'. All six categories matched with specificity. |
| c15 | Output's mitigations target each Medium+ risk with at least one specific control — e.g. for function creep: documented purpose limitation in privacy notice, technical access controls preventing the score from feeding marketing systems | PASS | For function creep (R6): M8 'API-level access control: restrict score consumption to approved systems only' and M15 'Restrict churn/upgrade scores to marketing/retention use only; contractual prohibition on credit/underwriting use'. For each Medium+ risk, the Mitigation Table maps specific named controls: e.g., R1→M6 (AES-256+TLS 1.3)+M7+M14; R3→M4 (monthly bias audit)+M16 (fairness testing with equal opportunity ratio metrics); R4→M1 (LIA/privacy policy update)+M11 (opt-out mechanism). |
| c16 | Output's residual risk is demonstrably lower than inherent risk per mitigated risk, with a likelihood × impact recalculation shown after controls | PARTIAL | The Mitigation Table has a 'Residual risk' column per mitigation measure (e.g., M6→'Medium', M15→'Low') and the Mitigation Summary states 'Very High risks (R1, R3, R6): Mitigated to Medium-Low'. Residual risk is demonstrably lower. However, there is no per-risk post-mitigation table re-running the same Likelihood × Severity × Overall structure used in the inherent risk table (Section 3). The output shows qualitative residual risk per measure but not an explicit likelihood × impact recalculation matrix after all controls applied to each risk. |
| c17 | Output's DPO review section produces a clear recommendation — Proceed / Proceed with conditions (specifying the conditions) / Do not proceed — not a vague 'this is risky' | PASS | Section 5 DPO recommendation row: 'CONDITIONAL APPROVAL — Proceed if and only if:' with 7 numbered and owner-assigned conditions, each with a target date (e.g., 'Lawful basis documented (LIA or consent framework): 2026-05-15, Legal + DPO, Pending'). A separate Pre-Launch Conditions Checklist table repeats all 7 conditions with dates and owners. This is specific and actionable, not vague. |
| c18 | Output's Article 36 determination is explicit — supervisory authority consultation IS or IS NOT required, with reasoning tied to whether residual risk remains High | PASS | Section 6 explicitly answers: 'After all feasible mitigations, is residual risk High or Very High? NO. After M1–M16 (all measures complete), residual risk is Low→Medium. Acceptable range for standard processing (no prior consultation required).' Reasoning directly tied to residual risk level. Determination: consultation 'RECOMMENDED (not mandatory if conditions met)' with justification that Art. 35(3)(a) and (b) both apply and fintech sector has regulatory scrutiny. Final recommendation: 'SUBMIT ARTICLE 36 CONSULTATION REQUEST'. |
| c19 | Output is written to a file with version, date, owner (DPO), and status — not only returned in conversation | PASS | Artifact `work/DPIA-behavioural-analytics.md` confirmed written to disk with header: 'Version: 1.0 \| Date: 2026-05-04 \| Owner: Data Protection Officer (Luminary) \| Status: Draft for DPO Review'. The file is separate from the chat response summary. |
| c20 | Output explicitly states this processing triggers Article 35(3)(a) (systematic and extensive evaluation based on automated processing including profiling, on which decisions producing legal/significant effects are based) and likely (b) (large-scale processing of personal data) | PASS | Section 5 DPO Assessment: '(a) Automated decision-making with legal/significant effect (Art. 35(3)(a)): ML-driven churn/upgrade scores inform marketing targeting, campaign frequency, and offer eligibility. Scores have meaningful impact on user experience and commercial treatment. (b) Systematic monitoring (Art. 35(3)(b)): granular behavioural tracking (page views, click sequences, session timing) constitutes systematic observation of user behaviour.' Section 6 confirms both: 'Is processing subject to Art. 35(3)(a) automated decision-making? YES.' and 'Is processing subject to Art. 35(3)(b) systematic monitoring? YES.' |

### Notes

The output is a comprehensive, well-structured DPIA covering all six required steps with detailed substance. The artifact is properly written to disk with all required metadata fields. Sections 1–5 are thorough: the processing description is exhaustive, the necessity and proportionality assessment addresses every Article 5 principle, risks are consistently framed from the individual's perspective with 11 named risk categories, 16 mitigation measures are mapped to specific risks, and the DPO section delivers a clear conditional approval with 7 blocking pre-launch conditions. Section 6 provides an explicit Art. 36 consultation recommendation with a 10-week timeline. The only gap is in c16: while residual risk is demonstrably lower for each mitigated risk (shown via the Residual risk column in the mitigation table), the output does not reproduce the inherent risk's Likelihood × Severity × Overall structure as a post-mitigation recalculation table for each risk — residual risk is expressed qualitatively per measure rather than as a matched matrix. The c10 PARTIAL ceiling is met at maximum since the output explicitly identifies Art. 35(3)(a) in the DPO section.
