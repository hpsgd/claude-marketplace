# Result: risk-assessment

**Verdict:** PASS
**Score:** 19/20 criteria met (95%)
**Evaluated:** 2026-04-30

## Output

The following is a simulated output for the prompt:

> `/grc-lead:risk-assessment "Prescribe — a telehealth prescription management system that stores patient medication history, processes repeat prescriptions, and sends SMS reminders. Patients are in Australia and New Zealand. The system uses a third-party SMS provider (Twilio) and a cloud database (AWS RDS in ap-southeast-2)."`

---

# Risk Assessment: Prescribe

## Scope

| Field | Value |
|---|---|
| **Subject** | Prescribe — telehealth prescription management system |
| **Boundaries** | Prescription data store (AWS RDS ap-southeast-2), repeat-prescription processing engine, SMS reminder service (Twilio), patient-facing web/mobile interface, prescriber portal, pharmacy partner API integration |
| **Exclusions** | Clinical decision-making logic (out of scope for this assessment), downstream pharmacy dispensing systems, Twilio internal infrastructure |
| **Time horizon** | 12 months from assessment date |
| **Assessment date** | 2026-04-30 |
| **Assessor** | GRC Lead |
| **Stakeholders** | Patients (AU/NZ), prescribing clinicians, pharmacy partners, Prescribe engineering and ops teams, Australian Privacy Commissioner, NZ Privacy Commissioner, TGA (Therapeutic Goods Administration) |

---

## Risk Register

### R-001: Privacy Act (AU) and Health Information Privacy Code (NZ) non-compliance

- **Category:** Regulatory
- **Description:** Prescribe stores patient medication history (sensitive health information). Failure to comply with the Australian Privacy Act 1988 (APPs) — particularly APP 8 (cross-border disclosure) and APP 11 (security) — or the NZ Privacy Act 2020 / Health Information Privacy Code could result in regulatory investigation, mandatory breach notification, and civil penalties.
- **Likelihood:** Medium (~25%) — health data custodians are frequent targets of regulatory audits; obligations are complex across two jurisdictions.
- **Impact:** Critical — regulatory sanction, civil penalties, potential suspension of operations.
- **Inherent risk:** High (Medium likelihood × Critical impact → High from matrix)
- **Current controls:** Privacy policy published; DPA with Twilio referencing APP 8; AWS ap-southeast-2 (Australian region) satisfies data residency for most APPs; NZ-specific Health Information Privacy Code review not yet completed.
- **Control effectiveness:** Partial (NZ review gap leaves residual exposure)
- **Residual risk:** Medium
- **Treatment:** Mitigate
- **Treatment detail:** Commission NZ Health Information Privacy Code gap analysis within 60 days. Update privacy impact assessment to cover NZ-domiciled patients. Implement consent management that distinguishes AU vs NZ obligations.
- **Owner:** Head of Legal / Compliance
- **Review date:** 2026-10-30

---

### R-002: Patient data breach via third-party SMS provider (Twilio)

- **Category:** Vendor
- **Description:** Twilio processes outbound SMS reminders. If PHI is inadvertently included in SMS body text (e.g., medication name, dose), a Twilio security incident or misconfiguration could expose health information to unauthorised parties.
- **Likelihood:** Medium (~20%) — Twilio has a documented 2022 breach; SMS channel is inherently low-security.
- **Impact:** Critical — PHI exposure triggers mandatory breach notification under APP 11 / NZ Privacy Act; reputational damage; potential TGA attention if medication-related data disclosed.
- **Inherent risk:** High (Medium likelihood × Critical impact → High from matrix)
- **Current controls:** DPA with Twilio signed (references APP 8 cross-border disclosure); TLS in transit enforced on Twilio API calls; SMS bodies contain only appointment reminders ("Your prescription is ready for collection") with no medication names, doses, or patient identifiers beyond first name; breach notification clause in Twilio contract requires 72-hour notification.
- **Control effectiveness:** Partial (no PHI in SMS body reduces impact significantly; DPA covers compliance; however Twilio account compromise risk remains and no MFA on Twilio console confirmed)
- **Residual risk:** Medium
- **Treatment:** Mitigate
- **Treatment detail:** Enforce MFA on Twilio console access and rotate API keys quarterly. Conduct quarterly review of SMS template library to confirm no PHI drift. Evaluate fall-back SMS provider (e.g., MessageBird) to reduce single-vendor dependency for critical reminders.
- **Owner:** Head of Engineering
- **Review date:** 2026-07-30

---

### R-003: AWS RDS data residency and availability (ap-southeast-2)

- **Category:** Data
- **Description:** AWS RDS in ap-southeast-2 stores all patient medication history. Two sub-risks: (1) data residency — if RDS snapshots or replicas are moved outside AU/NZ, APP 8 cross-border disclosure obligations apply; (2) availability — single-AZ RDS deployment would mean a zonal failure causes Prescribe to be unable to process repeat prescriptions or confirm medication histories, which has patient safety implications.
- **Likelihood:** Low (~10%) for residency breach; Medium (~30%) for AZ-level availability event over 12 months.
- **Impact:** Critical for residency breach (regulatory); High for availability event (patient harm, business continuity).
- **Inherent risk:** Medium (residency, Low likelihood × Critical → Medium); High (availability, Medium × High → High from matrix)
- **Current controls:** RDS deployed in ap-southeast-2 (Sydney); automated backups enabled; no confirmed cross-region replication (residency risk is Low); current deployment is single-AZ (availability risk is unmitigated).
- **Control effectiveness:** Full for residency risk; None for AZ availability risk.
- **Residual risk:** Low (residency); High (availability)
- **Treatment:** Mitigate (availability); Accept (residency)
- **Treatment detail — availability:** Upgrade RDS to Multi-AZ deployment within 30 days. Target RTO < 2 minutes for automatic failover. Test failover in staging before production cutover.
- **Treatment detail — residency:** Accept current posture — data confirmed in ap-southeast-2, no cross-region replication. Review if disaster recovery requirements change.
- **Owner:** Head of Engineering (availability); Head of Legal / Compliance (residency acceptance)
- **Review date:** 2026-07-30 (availability); 2026-10-30 (residency)

---

### R-004: Repeat prescription fraud or unauthorised access

- **Category:** Operational
- **Description:** A malicious actor (including an authenticated-but-compromised clinician account) could generate fraudulent repeat prescriptions or access other patients' medication histories via the prescriber portal.
- **Likelihood:** Medium (~20%) — credential stuffing and account compromise are common in healthcare portals.
- **Impact:** High — regulatory breach, patient harm, criminal liability under TGA legislation.
- **Inherent risk:** Medium (Medium likelihood × High impact → Medium from matrix)
- **Current controls:** Prescriber authentication via username/password; session timeout after 15 minutes; audit log of prescription actions retained for 7 years; role-based access control separating patient records by prescriber.
- **Control effectiveness:** Partial (no MFA on prescriber accounts is the primary gap)
- **Residual risk:** Medium
- **Treatment:** Mitigate
- **Treatment detail:** Implement MFA for all prescriber accounts within 60 days. Add anomaly detection alert for bulk prescription generation (>10 scripts in <5 minutes) triggering account suspension and ops review.
- **Owner:** Head of Engineering
- **Review date:** 2026-07-30

---

### R-005: SMS reminder delivery failure for critical medications

- **Category:** Operational
- **Description:** If Twilio experiences an outage or the Prescribe SMS dispatch service fails, patients on critical medications (immunosuppressants, anticoagulants) may miss refill reminders, leading to treatment interruption.
- **Likelihood:** Low (~8%) — Twilio SLA is 99.95%; service failures in dispatch logic possible.
- **Impact:** High — patient harm, reputational damage, potential regulatory action if systemic.
- **Inherent risk:** Medium (Low likelihood × High impact → Medium from matrix)
- **Current controls:** Twilio 99.95% uptime SLA; delivery receipts logged; failed delivery retry logic (3 attempts, 10-minute intervals); no fall-back channel currently implemented.
- **Control effectiveness:** Partial (retry handles transient failures; extended Twilio outage has no mitigation)
- **Residual risk:** Medium
- **Treatment:** Mitigate
- **Treatment detail:** Implement a fall-back in-app push notification for patients with the Prescribe mobile app. For patients without the app, flag undelivered SMS at 24 hours for manual outreach by pharmacy partner. Document in runbook.
- **Owner:** Head of Product
- **Review date:** 2026-07-30

---

### R-006: Uncontrolled AWS spend / infrastructure cost overrun

- **Category:** Financial
- **Description:** RDS instance size and data transfer costs may exceed budget if prescription volume grows faster than projected, or if Multi-AZ upgrade (R-003 treatment) is not costed correctly.
- **Likelihood:** Medium (~30%) — growth assumptions may be optimistic; Multi-AZ doubles RDS instance cost.
- **Impact:** Medium — project budget overrun, potential scaling delay.
- **Inherent risk:** Medium (Medium × Medium → Medium from matrix)
- **Current controls:** AWS billing alerts set at 110% of monthly budget; monthly infrastructure cost review in engineering planning.
- **Control effectiveness:** Partial (alerts exist but no auto-scaling governance policy)
- **Residual risk:** Low
- **Treatment:** Accept
- **Treatment detail:** Billing alerts and monthly review are sufficient. Multi-AZ cost delta (~$400/month for current instance size) has been modelled and approved in Q2 budget.
- **Owner:** Head of Engineering
- **Review date:** 2026-10-30

---

### R-007: Reputational damage from public data incident

- **Category:** Reputational
- **Description:** A publicly disclosed data breach or adverse media event (e.g., patients' medication histories exposed) could damage patient trust, cause prescriber churn, and attract regulatory scrutiny simultaneously.
- **Likelihood:** Low (~10%) — depends on R-002 and R-003 materialising and being publicly disclosed.
- **Impact:** Critical — patient attrition, prescriber departures, media coverage, regulatory action.
- **Inherent risk:** Medium (Low × Critical → Medium from matrix)
- **Current controls:** Incident response plan exists; PR crisis communications protocol documented; breach notification obligations documented (72 hours to regulator under AU/NZ Privacy Acts).
- **Control effectiveness:** Partial (plan exists but has not been tabletop-tested in 18 months)
- **Residual risk:** Medium
- **Treatment:** Mitigate
- **Treatment detail:** Run a tabletop incident response exercise within 90 days. Update crisis comms template to reference both AU and NZ regulatory contacts. Assign dedicated media response contact.
- **Owner:** CEO
- **Review date:** 2026-10-30

---

### R-008: No AI/ML components — category assessed as N/A

- **Category:** AI/ML
- **Description:** Prescribe does not currently use AI/ML models for clinical recommendations, prescription generation, or patient triage. No prompt injection, hallucination, or model dependency risks apply.
- **Likelihood:** N/A
- **Impact:** N/A
- **Inherent risk:** N/A
- **Current controls:** N/A
- **Control effectiveness:** N/A
- **Residual risk:** N/A
- **Treatment:** Accept — no risks identified in this category. If AI-assisted prescribing features are added, run `/grc-lead:ai-governance-review` before deployment.
- **Owner:** Head of Engineering
- **Review date:** 2026-10-30 (trigger: any AI feature proposal)

---

## Risk Summary

| Risk | Category | Description | Inherent | Residual | Treatment | Owner |
|---|---|---|---|---|---|---|
| R-001 | Regulatory | Privacy Act (AU) / Health Information Privacy Code (NZ) | High | Medium | Mitigate | Head of Legal |
| R-002 | Vendor | Patient data breach via Twilio | High | Medium | Mitigate | Head of Engineering |
| R-003 | Data | AWS RDS residency and availability | High (availability) | High (availability) | Mitigate | Head of Engineering |
| R-004 | Operational | Prescription fraud / unauthorised access | Medium | Medium | Mitigate | Head of Engineering |
| R-005 | Operational | SMS delivery failure for critical medications | Medium | Medium | Mitigate | Head of Product |
| R-006 | Financial | AWS cost overrun | Medium | Low | Accept | Head of Engineering |
| R-007 | Reputational | Public data incident | Medium | Medium | Mitigate | CEO |
| R-008 | AI/ML | No AI/ML components | N/A | N/A | Accept (N/A) | Head of Engineering |

## Prioritised Actions

1. **Immediate (within 30 days):** Upgrade AWS RDS to Multi-AZ deployment (R-003) — residual risk currently High.
2. **Within 60 days:** Implement MFA for all prescriber accounts (R-004); enforce MFA on Twilio console and rotate API keys (R-002).
3. **Within 60 days:** Commission NZ Health Information Privacy Code gap analysis (R-001).
4. **Within 90 days:** Run tabletop incident response exercise (R-007); implement fall-back push notification for SMS failures (R-005).
5. **Monitoring:** Quarterly SMS template audit (R-002); monthly AWS cost review (R-006 — accepted, monitoring in place).

## Review Schedule

- **Next review:** 2026-07-30
- **Review triggers:** Any new feature deployment touching patient data; any Twilio or AWS incident; any regulatory inquiry; addition of AI/ML components; maximum 6-month interval regardless.

---

## Results

### Criteria

- [x] PASS: Step 1 defines scope boundaries explicitly — the skill mandates Subject, Boundaries, Exclusions, Time horizon, and Stakeholders as required scope fields. The output above populates all five with Prescribe-specific content.
- [x] PASS: Risk identification covers all seven categories — Step 2 mandates all seven and explicitly states "Do not skip a category because you think it does not apply — document 'no identified risks' with reasoning." R-008 demonstrates the N/A pattern for AI/ML.
- [x] PASS: Every identified risk has a unique ID, a likelihood level with a percentage estimate, and an impact level — Step 3 requires the likelihood table with percentage ranges; the output template notation `**Likelihood:** [level] ([percentage estimate])` enforces this. Every risk above has an R-NNN ID and a percentage.
- [x] PASS: Inherent risk scores are derived from the matrix — Step 3 provides the full 4×4 matrix and the output template notation "(from matrix)" enforces visible derivation. Each risk above cites the matrix cell used.
- [x] PASS: Existing controls are documented per risk — Step 4 requires documenting controls, whether automated or manual, and when last verified. The anti-pattern "Controls without verification" prohibits claiming unverified controls. Each risk above has a Current controls field with specific evidence.
- [x] PASS: Residual risk is calculated after controls — Step 5 defines control effectiveness (Full/Partial/None) and the reduction rule. Each risk above shows the effectiveness rating and the resulting residual score.
- [x] PASS: Every risk has a treatment decision with specific detail — Step 6 requires both a treatment type and specific action. The anti-pattern "'We'll deal with it later' is not a treatment" is explicit. All risks above have specific treatment detail.
- [x] PASS: Accepted risks have an owner, justification, and review date (max 6 months) — Step 6 acceptance rules require a named person (not a team), a maximum 6-month expiry, and documented reasoning. R-006 and R-008 demonstrate this; R-003 residency sub-risk is also accepted with owner and date within 6 months.
- [x] PASS: Output compiled into risk register format with summary table and prioritised action list — the Output Format section requires per-risk blocks, Risk Summary table, Prioritised Actions list, and Review Schedule. All four are present in the simulated output above.
- [~] PARTIAL: Identifies Twilio as vendor risk and AWS RDS as data residency and availability risk — Twilio is explicitly addressed in R-002 (Vendor category) with DPA, breach notification, and outage coverage. AWS RDS ap-southeast-2 is addressed in R-003 covering both data residency and availability. However, the skill's Vendor category guidance lists "data residency" as a sub-concern without mandating that RDS availability topology (single-AZ vs multi-AZ) be called out as a distinct dimension. A thorough assessment surfaces this (as shown), but the skill text does not require it explicitly.

### Output expectations

- [x] PASS: Scope section names Prescribe, in-scope subsystems, time horizon, and affected stakeholders — all present in the simulated output: prescription data store, repeat-prescription processing engine, SMS reminder service, prescriber portal, pharmacy partner API; 12-month horizon; patients in AU/NZ, prescribers, pharmacy partners, TGA, both Privacy Commissioners.
- [x] PASS: Output identifies risks in all seven categories with at least one risk per category — R-001 (Regulatory), R-002 (Vendor), R-003 (Data), R-004/R-005 (Operational), R-006 (Financial), R-007 (Reputational), R-008 (AI/ML with explicit N/A).
- [x] PASS: Each risk has a unique R-NNN ID, a likelihood with percentage, and an impact level — all eight risks above have these three fields populated.
- [x] PASS: Inherent risk scores derived from the 4×4 matrix shown in the skill — each risk above cites the matrix cell (e.g., "Medium likelihood × Critical impact → High from matrix").
- [x] PASS: Existing controls documented per risk with specificity — R-002 lists "DPA signed, TLS in transit, no PHI in SMS body, 72-hour breach notification clause" rather than generic claims.
- [x] PASS: Residual risk calculated per risk with a clear reduction shown — e.g., R-001: Inherent High → Residual Medium (Partial control effectiveness); R-003 availability: Inherent High → Residual High (None effectiveness — unmitigated until Multi-AZ).
- [x] PASS: Treatment decision per risk with specifics — each risk has both a treatment type and a concrete action (timeline, mechanism, owner).
- [x] PASS: Accepted risks have a named owner, justification, and review date within 6 months — R-006 (accepted, Head of Engineering, 2026-10-30, justified by budget approval); R-003 residency sub-risk (accepted, Head of Legal, 2026-10-30, justified by confirmed ap-southeast-2 deployment).
- [x] PASS: Twilio addressed as vendor risk with DPA, breach notification, TGA/Privacy Act compliance, and outage dependency — R-002 covers all four dimensions explicitly.
- [~] PARTIAL: AWS RDS in ap-southeast-2 addressed as data residency choice and single-AZ vs multi-AZ decision with trade-offs — R-003 surfaces both residency and availability as distinct sub-risks and calls out single-AZ as the unmitigated gap. However, the skill does not explicitly prompt for AZ topology analysis — this surfaces only because the scenario description mentions the cloud database and a thorough assessor would infer it. The skill guides toward "data residency" and "availability" at category level but does not require AZ topology as a specific check.

## Notes

The skill is structurally strong. All mandatory output fields are enforced via the template, matrix derivation is explicit, and the anti-patterns cover the most common failure modes — orphaned acceptances, unverified controls, missing residual risk. The N/A pattern for AI/ML (R-008) is well-handled: the skill requires documenting "no identified risks with reasoning" rather than silently skipping the category.

The one structural gap: the skill does not prompt for infrastructure topology decisions (single-AZ vs multi-AZ) under the Data or Vendor categories. For a telehealth system with patient safety implications, AZ availability is material. The scenario's description of "AWS RDS in ap-southeast-2" is sufficient for a skilled assessor to flag this, but the skill's category guidance does not require it explicitly. Worth adding "availability topology (single-AZ vs multi-AZ, RTO/RPO)" to the Vendor or Operational category guidance in SKILL.md.
