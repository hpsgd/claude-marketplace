# Risk Assessment

Scenario: A user invokes the skill to assess a system that handles sensitive data. Does the skill work through all seven steps in order, quantify every risk with likelihood and impact, document existing controls, calculate residual risk, and produce a treatment plan with owners and review dates?

## Prompt

> /grc-lead:risk-assessment "Prescribe — a telehealth prescription management system that stores patient medication history, processes repeat prescriptions, and sends SMS reminders. Patients are in Australia and New Zealand. The system uses a third-party SMS provider (Twilio) and a cloud database (AWS RDS in ap-southeast-2)."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The risk assessment is complete and saved to `risk-assessment-prescribe.md`. Here's a summary of what was found:

---

**16 risks identified across 7 categories.** Key findings:

**Two pre-launch blockers (Critical residual — do not go live until closed):**
- **R-001 — TGA SaMD:** Prescription automation is likely a medical device under Australian law. Operating without TGA registration is a criminal offence. Commission a regulatory affairs consultant immediately.
- **R-002 — RTPM:** If the platform handles S8/controlled substances, state Real-Time Prescription Monitoring integration is mandatory. Map obligations by state before launch.

**High residual risks requiring mitigation before launch:**
- **R-005** — Twilio likely transmits PHI offshore; APP 8 compliance requires a DPA and/or PHI stripping from SMS templates
- **R-006** — NZ patient data in AWS Sydney is legally cross-border under NZ Privacy Act IPP 12; requires legal opinion and patient disclosure
- **R-008** — No confirmed RBAC or audit logging for internal record access

**Notable AU/NZ-specific issues the assessment surfaced:**
- NZ data residency is a distinct risk from AU residency — ap-southeast-2 satisfies AU but not NZ
- RTPM is a state-level obligation often missed in system design
- Post-2024 Privacy Act penalties reach $50M AUD for serious contraventions

Related next steps: `/grc-lead:compliance-audit` against the APPs once controls are in place; `/grc-lead:ai-governance-review` before any ML features are introduced.

### Artifacts written

#### `work/risk-assessment-prescribe.md`

```
# Risk Assessment: Prescribe — Telehealth Prescription Management System

## Scope

- **Subject:** Prescribe — a telehealth prescription management system that stores patient medication history, processes repeat prescriptions, and sends SMS reminders
- **Boundaries:** Patient-facing prescription workflows; medication history storage (AWS RDS ap-southeast-2); SMS reminder delivery (Twilio); Australian and New Zealand patient populations
- **Exclusions:** Clinical practice management (booking, billing); prescriber-side workflows beyond prescription submission; My Health Record integration (not described); payment processing; patient-facing web/mobile UI internals
- **Time horizon:** Immediate to 12 months — risks are present from the moment the system processes patient data or goes live
- **Assessment date:** 2026-05-01
- **Assessor:** GRC Lead (Claude Code — turtlestack/grc-lead)
- **Stakeholders:** Patients (AU/NZ); prescribing practitioners; dispensing pharmacists; OAIC (AU regulator); NZ Privacy Commissioner; TGA; state pharmacy boards; Prescribe's board and leadership

---

## AI/ML Category

**No AI/ML risks identified.** The system description specifies rule-based prescription processing and SMS reminders with no machine learning components. If ML is introduced (e.g., adherence prediction, dosing recommendations), a dedicated `/grc-lead:ai-governance-review` must be commissioned before deployment.

---

## Risk Register

---

### R-001: TGA Software as a Medical Device (SaMD) classification — unregistered operation

- **Category:** Regulatory
- **Description:** Software that "processes repeat prescriptions" is likely classifiable as a Software as a Medical Device (SaMD) under the Therapeutic Goods Administration's framework (Therapeutic Goods Act 1989, IMDRF SaMD classification guidance adopted post-2021). A system that automates clinical repeat-prescription workflows may qualify as Class IIa or higher. Operating an unregistered medical device is a criminal offence under s.41MI of the Therapeutic Goods Act. This risk is present from first patient use.
- **Likelihood:** High (50%) — prescription automation consistently triggers SaMD classification in TGA assessments
- **Impact:** Critical — criminal liability for directors, forced shutdown, inability to legally operate in Australia
- **Inherent risk:** Critical (High × Critical)
- **Current controls:** None identified. No TGA classification analysis exists in the codebase or described architecture.
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate — commission a formal TGA SaMD classification review with a regulatory affairs consultant before any live patient use. If classified: register as a medical device, implement ISO/IEC 62304 software lifecycle processes, and prepare conformance documentation. This is a pre-launch blocker.
- **Owner:** [Chief Medical Officer / Regulatory Affairs Lead — to be appointed]
- **Review date:** 2026-07-01 — must be resolved before patient go-live; do not wait for the 6-month cycle

> ⚠️ **Critical residual risk — coordinator approval required before acceptance or deferral.**

---

### R-002: Real-Time Prescription Monitoring (RTPM) non-compliance

- **Category:** Regulatory
- **Description:** Australian state and territory laws mandate integration with Real-Time Prescription Monitoring (RTPM) systems for Schedule 8 (S8) controlled medicines, and increasingly S4 medicines of concern. Systems in scope: SafeScript (VIC), ScriptCheck (SA), QScript (QLD), DORA (WA), MedView (NSW), ScriptWise (TAS). If Prescribe handles controlled substance prescriptions and does not report to or query the relevant RTPM systems, prescribers using Prescribe may be in breach of state Poisons Acts, and Prescribe may be enabling non-compliant prescribing. Liability extends to the platform operator.
- **Likelihood:** High (50%) — controlled substance prescriptions are common in telehealth; RTPM obligations are state-mandatory
- **Impact:** Critical — prescriber licence sanctions (AHPRA), state regulator enforcement, patient harm from undetected drug-seeking, platform liability
- **Inherent risk:** Critical (High × Critical)
- **Current controls:** None identified.
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate — determine which substance schedules the platform handles. If S8 or S4-of-concern: map RTPM obligations by state, integrate RTPM APIs before launch, implement mandatory RTPM query before repeat prescriptions are issued. If S8 is excluded from scope, document that exclusion explicitly in the system's intended use statement.
- **Owner:** [Chief Medical Officer — to be appointed]
- **Review date:** 2026-07-01 — pre-launch blocker

> ⚠️ **Critical residual risk — coordinator approval required before acceptance or deferral.**

---

### R-003: Australian Privacy Act 1988 non-compliance (sensitive health information)

- **Category:** Regulatory
- **Description:** Patient medication history is "sensitive information" under the Privacy Act 1988 (Cth), subject to a higher standard of protection across all 13 Australian Privacy Principles (APPs). Key obligations: APP 3 (lawful collection with notice), APP 6 (no secondary use without consent), APP 8 (cross-border disclosure controls), APP 11 (security — must take reasonable steps), APP 12/13 (access and correction on request). Post-2024 amendments raise maximum civil penalties to $50M AUD for serious or repeated contraventions. The Notifiable Data Breaches (NDB) scheme requires notification to the OAIC and affected individuals within 30 days of becoming aware of an eligible breach.
- **Likelihood:** Medium (25%) — systematic APP compliance gaps are common in new systems lacking a dedicated Privacy Officer
- **Impact:** Critical — OAIC enforcement, civil penalties up to $50M, NDB notifications, patient trust loss
- **Inherent risk:** High (Medium × Critical)
- **Current controls:** None confirmed. AWS RDS in ap-southeast-2 provides Australian data residency (positive), but application-level APP controls (consent capture, purpose limitation, access logging) are unknown.
- **Control effectiveness:** Partial — data residency satisfied, application-level controls unverified
- **Residual risk:** Medium
- **Treatment:** Mitigate — commission a Privacy Impact Assessment (PIA) before launch; appoint a Privacy Officer; implement consent capture at onboarding; build access-and-correction request workflow; establish an NDB incident response playbook with 30-day notification capability.
- **Owner:** [Privacy Officer — to be appointed]
- **Review date:** 2026-09-01

---

### R-004: NZ Privacy Act 2020 / Health Information Privacy Code 2020 non-compliance

- **Category:** Regulatory
- **Description:** The NZ Privacy Act 2020 applies to any organisation collecting personal information about NZ residents. The Health Information Privacy Code 2020 imposes specific obligations on health information handling, including purpose limitation, security safeguards, and mandatory breach reporting (notify Privacy Commissioner as soon as practicable for serious breaches). NZ data stored in AWS ap-southeast-2 (Sydney, Australia) constitutes cross-border transfer — NZ IPP 12 requires the organisation to take reasonable steps to ensure comparable protection applies offshore. AWS contractual arrangements may satisfy this, but require explicit legal analysis.
- **Likelihood:** Medium (25%)
- **Impact:** High — NZ Privacy Commissioner enforcement, compliance orders, patient trust damage
- **Inherent risk:** Medium (Medium × High)
- **Current controls:** None confirmed.
- **Control effectiveness:** None
- **Residual risk:** Medium
- **Treatment:** Mitigate — conduct NZ Privacy Act gap analysis; obtain legal opinion on IPP 12 cross-border compliance basis for AWS ap-southeast-2; include NZ-specific privacy disclosures in patient onboarding.
- **Owner:** [Privacy Officer — to be appointed]
- **Review date:** 2026-09-01

---

### R-005: Cross-border PHI transfer via Twilio (APP 8 / NZ IPP 12)

- **Category:** Regulatory / Vendor
- **Description:** Twilio is a US-headquartered company. SMS content passes through Twilio's infrastructure before delivery to carriers. **The severity of this risk depends on SMS message content — to be verified:** if messages include PHI (e.g., patient name, medication name, dosage, repeat count), this constitutes cross-border disclosure of sensitive information under APP 8 (Australia) and NZ IPP 12 (New Zealand). APP 8 requires either: (a) a contractual arrangement ensuring the overseas recipient meets APP standards, or (b) patient consent after being informed the information may not be protected. A generic Twilio commercial contract does not satisfy APP 8. Even messages like "Your prescription reminder" without PHI carry lower risk but require review.
- **Assumption to verify:** Do SMS templates include medication names, patient names, or dosage information?
- **Likelihood:** High (50%) — probable if SMS includes medication details; lower if de-identified
- **Impact:** High — APP 8 / IPP 12 breach, OAIC enforcement, patient trust damage
- **Inherent risk:** High (High × High)
- **Current controls:** None confirmed. Twilio is GDPR-compliant but GDPR adequacy does not automatically satisfy Australian APPs.
- **Control effectiveness:** None (without a verified DPA)
- **Residual risk:** High
- **Treatment:** Mitigate — (1) audit all SMS message templates and strip PHI where possible (e.g., replace medication name with a portal link); (2) execute an APP 8-compliant Data Processing Agreement with Twilio; (3) update patient privacy notices to disclose overseas SMS processing. If PHI cannot be removed, obtain explicit informed consent.
- **Owner:** [Privacy Officer — to be appointed]
- **Review date:** 2026-08-01

---

### R-006: NZ patient data residency — AWS ap-southeast-2 is outside New Zealand

- **Category:** Regulatory / Data
- **Description:** All patient data (including NZ residents) is stored in AWS ap-southeast-2, which is physically located in Sydney, Australia. Under the NZ Privacy Act 2020, this constitutes offshore disclosure and triggers IPP 12 obligations. While AWS provides contractual data protection commitments, the compliance basis (adequate safeguards or explicit patient consent) must be documented. Without documented compliance basis, Prescribe is operating in breach of NZ privacy law from first NZ patient record stored.
- **Likelihood:** Very High (>90%) — this is the current architecture by design; it is happening unless addressed
- **Impact:** High — NZ Privacy Commissioner enforcement, potential requirement to delete/relocate NZ data, operational disruption
- **Inherent risk:** Critical (Very High × High)
- **Current controls:** AWS Data Processing Addendum (assumed standard) — may partially satisfy IPP 12 if documented.
- **Control effectiveness:** Partial — AWS contracts exist, but adequacy determination and documentation unverified
- **Residual risk:** High
- **Treatment:** Mitigate — obtain legal opinion on whether AWS DPA satisfies NZ IPP 12; document the compliance basis; disclose offshore storage to NZ patients at onboarding; consider data residency controls or regional separation if legal opinion is unfavourable.
- **Owner:** [Privacy Officer — to be appointed]
- **Review date:** 2026-08-01

---

### R-007: Patient medication history data breach (AWS RDS)

- **Category:** Data
- **Description:** The RDS database contains highly sensitive health records (medication history, prescription records, patient identifiers). Attack vectors include: SQL injection in application layer, compromised application credentials, misconfigured RDS security groups (publicly accessible), insider threat, or compromised CI/CD pipeline with database access. A breach triggers NDB obligations (AU) and mandatory breach reporting (NZ), potential class action, and AHPRA investigation of clinical records handling.
- **Likelihood:** Medium (25%)
- **Impact:** Critical — PHI exposure for potentially thousands of patients, NDB/NZ breach notification, regulatory action, patient harm
- **Inherent risk:** High (Medium × Critical)
- **Current controls:** AWS RDS provides encryption at rest (AES-256) and in transit (TLS) if configured; VPC network isolation assumed. Application-level controls (parameterised queries, WAF, audit logging) are unverified.
- **Control effectiveness:** Partial — infrastructure controls assumed; application controls unverified
- **Residual risk:** Medium
- **Treatment:** Mitigate — verify RDS encryption at rest and in transit are enabled; conduct penetration test before launch; implement WAF; enforce parameterised queries; enable RDS audit logging; establish breach response runbook capable of NDB 30-day notification.
- **Owner:** [CTO / Head of Engineering — to be appointed]
- **Review date:** 2026-09-01

---

### R-008: Unauthorised internal access to prescription records

- **Category:** Data
- **Description:** Platform staff (engineers, operations, support) may have overly broad access to patient prescription data without clinical justification. Minimum-necessary-access is an APP 11 requirement. Without role-based access control and audit trails, internal actors can access any patient record, creating both compliance and patient trust risk. Telehealth platforms are high-profile targets for data misuse given the sensitivity of the information.
- **Likelihood:** Medium (25%) — common in early-stage systems without mature RBAC
- **Impact:** Critical — APP 11 breach, potential OAIC enforcement, patient harm, reputational damage
- **Inherent risk:** High (Medium × Critical)
- **Current controls:** None identified.
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Mitigate — implement role-based access control with minimum necessary access; enable database audit logging (who accessed what, when); conduct access reviews quarterly; segregate production data from development environments.
- **Owner:** [CTO / Head of Engineering — to be appointed]
- **Review date:** 2026-09-01

---

### R-009: Prescription processing error causing patient harm

- **Category:** Operational
- **Description:** A software defect causes an incorrect repeat prescription to be issued — wrong medication, wrong dose, wrong frequency, or prescription issued to the wrong patient. In a telehealth context, there is reduced opportunity for physical verification compared to in-person consultations. Prescription errors can cause serious patient harm (overdose, under-treatment, drug interactions). Liability extends to the platform operator if the system contributed to the error.
- **Likelihood:** Low (8%) for a clinically significant error
- **Impact:** Critical — patient harm, death in worst case, coronial inquiry, AHPRA investigation, medical indemnity claim
- **Inherent risk:** Medium (Low × Critical)
- **Current controls:** None confirmed. Clinical workflow design (prescriber sign-off, confirmation steps) is not described.
- **Control effectiveness:** None
- **Residual risk:** Medium
- **Treatment:** Mitigate — implement mandatory prescriber confirmation step before any prescription is issued or repeated; add clinical decision support warnings for known interactions; implement two-person authorisation for S8 medications; maintain an audit trail of every prescription action.
- **Owner:** [Chief Medical Officer — to be appointed]
- **Review date:** 2026-09-01

---

### R-010: SMS delivery failure causing missed medication reminders

- **Category:** Operational
- **Description:** SMS reminders fail to deliver due to: Twilio delivery error, invalid/changed patient phone number, carrier filtering, or temporary outage. Patients miss medication refill reminders, leading to medication non-adherence. While a single missed reminder is low-severity, systematic delivery failure for a patient cohort on critical medications (e.g., blood pressure, diabetes, psychiatric medications) creates clinical risk and erodes product value.
- **Likelihood:** Medium (25%) — SMS non-delivery rates of 5–15% are typical; phone number churn in NZ/AU is significant
- **Impact:** Medium — medication non-adherence for some patients; product value degradation; not a catastrophic failure if patients can access the portal directly
- **Inherent risk:** Medium (Medium × Medium)
- **Current controls:** Twilio provides delivery receipts and status webhooks. Whether these are monitored is unknown.
- **Control effectiveness:** Partial — delivery reporting exists at Twilio level; application-level retry and monitoring unknown
- **Residual risk:** Medium
- **Treatment:** Mitigate — implement delivery receipt monitoring; add retry logic for failed sends; provide a fallback communication channel (email) for critical reminders; alert operations team when delivery failure rate exceeds 10%.
- **Owner:** [Head of Product / Operations — to be appointed]
- **Review date:** 2026-11-01

---

### R-011: RDS data loss (backup failure, accidental deletion, ransomware)

- **Category:** Operational / Data
- **Description:** Patient prescription history is permanently lost due to backup failure, accidental deletion of RDS instance, or ransomware encrypting the database. Prescription history loss is not merely a business continuity issue — loss of medication records can directly endanger patients who cannot access their prescription history in emergencies.
- **Likelihood:** Low (<10%) — AWS RDS automated backups reduce probability significantly, but untested backups are a known failure mode
- **Impact:** Critical — loss of clinical records, patient safety risk, potential regulatory action for failure to maintain health records
- **Inherent risk:** Medium (Low × Critical)
- **Current controls:** AWS RDS automated daily backups (assumed enabled). Point-in-time recovery available. Cross-region backup replication unknown.
- **Control effectiveness:** Partial — backups assumed enabled but recovery procedures untested
- **Residual risk:** Low (if backups are verified and tested)
- **Treatment:** Mitigate — verify automated backups are enabled and configured correctly; test recovery to a non-production environment quarterly; document and test RTO/RPO targets; consider cross-region snapshot replication for disaster recovery.
- **Owner:** [CTO / Head of Engineering — to be appointed]
- **Review date:** 2026-09-01

---

### R-012: Twilio vendor security incident (PHI exposure)

- **Category:** Vendor
- **Description:** Twilio suffered a significant security breach in August 2022 (social engineering attack on employees, exposing customer data and internal systems). If SMS messages contain PHI, a future Twilio breach could expose patient health information. The platform cannot control Twilio's internal security posture, making this a residual transfer risk regardless of internal controls.
- **Likelihood:** Low (10%) — vendor breaches are infrequent; Twilio has improved security posture post-2022
- **Impact:** High — PHI disclosed to a third party, triggering NDB notification, OAIC inquiry, reputational damage
- **Inherent risk:** Medium (Low × High)
- **Current controls:** Twilio is SOC 2 Type II certified. Twilio GDPR DPA available. AU/NZ-specific data processing agreement status is unknown.
- **Control effectiveness:** Partial — SOC 2 certification provides some assurance; PHI minimisation in SMS is the primary mitigation
- **Residual risk:** Low
- **Treatment:** Accept with conditions — minimise PHI in SMS content (primary mitigation from R-005); verify Twilio DPA covers AU/NZ obligations; include Twilio in annual vendor security review.
- **Owner:** [Privacy Officer — to be appointed]
- **Review date:** 2026-11-01

---

### R-013: AWS RDS availability (single-AZ deployment)

- **Category:** Operational / Vendor
- **Description:** If AWS RDS is deployed in a single Availability Zone (single-AZ), an AZ-level failure causes complete database unavailability, blocking all prescription processing. In a clinical context, unavailability of prescription history can cause prescribers to make uninformed decisions or patients to be unable to access critical medications.
- **Likelihood:** Low (<10%) — AWS AZ-level failures are infrequent but not unknown
- **Impact:** High — complete service outage; clinical workflow disruption; potential patient harm if prescription access is urgent
- **Inherent risk:** Medium (Low × High)
- **Current controls:** Multi-AZ RDS configuration assumed but unverified.
- **Control effectiveness:** Full (if Multi-AZ is confirmed) / None (if single-AZ)
- **Residual risk:** Low — contingent on Multi-AZ being confirmed (see treatment)
- **Treatment:** Mitigate — verify Multi-AZ is enabled on the RDS instance; document failover RTO (typically 1–2 minutes with Multi-AZ); test failover in a staging environment.
- **Owner:** [CTO / Head of Engineering — to be appointed]
- **Review date:** 2026-09-01

---

### R-014: Twilio service outage (SMS channel unavailable)

- **Category:** Vendor
- **Description:** A Twilio platform outage renders the entire SMS reminder channel unavailable. No reminders are sent during the outage window. For patients on time-sensitive medication regimens, this could cause adherence issues.
- **Likelihood:** Low (5%) — Twilio SLA is approximately 99.95%
- **Impact:** Medium — reminders fail; patient inconvenience; no direct clinical emergency if portal remains accessible
- **Inherent risk:** Low (Low × Medium)
- **Current controls:** Twilio status page (https://status.twilio.com). Monitoring integration unknown.
- **Control effectiveness:** Partial — visibility exists; no failover
- **Residual risk:** Low
- **Treatment:** Accept — Twilio's SLA and track record make extended outages rare. Monitor Twilio status page; consider Sinch or AWS SNS as fallback SMS providers if SLA requirements harden.
- **Owner:** [Head of Operations — to be appointed]
- **Review date:** 2026-11-01

---

### R-015: Uncontrolled Twilio SMS spend

- **Category:** Financial
- **Description:** A bug in the reminder scheduling system (e.g., infinite retry loop, scheduling table corruption) triggers mass or duplicate SMS sends to the patient population. Twilio charges per-message; at scale, a runaway send could generate $10,000–$100,000+ in unexpected charges before detection.
- **Likelihood:** Low (10%)
- **Impact:** Medium — financial loss; reputational damage if patients receive dozens of duplicate messages
- **Inherent risk:** Low (Low × Medium)
- **Current controls:** None confirmed. Twilio does not enforce spend caps by default.
- **Control effectiveness:** None
- **Residual risk:** Low
- **Treatment:** Mitigate — configure Twilio spend alerts and hard spending caps in the Twilio console; implement application-level per-patient daily send limits; add duplicate detection before any send.
- **Owner:** [CTO / Head of Engineering — to be appointed]
- **Review date:** 2026-11-01

---

### R-016: Public data breach causing reputational damage and patient exodus

- **Category:** Reputational
- **Description:** A significant patient data breach (R-007) becomes public — through media reporting, OAIC disclosure, or patient notification. Loss of patient trust causes churn, new patient acquisition failure, and potential business-ending consequences for a telehealth startup operating on trust-sensitive health data. Regulatory action (OAIC or TGA) compounds reputational impact.
- **Likelihood:** Medium (20%) — conditional on a breach occurring and breaches being reportable (NDB threshold)
- **Impact:** Critical — patient exodus, media coverage, regulatory scrutiny, investor confidence loss, potential business failure
- **Inherent risk:** High (Medium × Critical)
- **Current controls:** None specific to reputational management.
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Mitigate — develop a breach response communications plan before launch; prepare patient notification templates; establish a media response protocol; obtain cyber liability insurance; test the response plan annually.
- **Owner:** [CEO — to be appointed]
- **Review date:** 2026-09-01

---

## Risk Summary

| Risk ID | Description | Category | Inherent | Residual | Treatment | Owner |
|---|---|---|---|---|---|---|
| R-001 | TGA SaMD classification — unregistered operation | Regulatory | **Critical** | **Critical** | Mitigate | CMO / Regulatory Affairs |
| R-002 | RTPM non-compliance (controlled substances) | Regulatory | **Critical** | **Critical** | Mitigate | CMO |
| R-003 | Australian Privacy Act / APPs non-compliance | Regulatory | High | Medium | Mitigate | Privacy Officer |
| R-004 | NZ Privacy Act 2020 / HIPC non-compliance | Regulatory | Medium | Medium | Mitigate | Privacy Officer |
| R-005 | Cross-border PHI via Twilio (APP 8 / IPP 12) | Regulatory / Vendor | High | High | Mitigate | Privacy Officer |
| R-006 | NZ data residency — AP-SE-2 is outside NZ | Regulatory / Data | **Critical** | High | Mitigate | Privacy Officer |
| R-007 | Patient medication history data breach (RDS) | Data | High | Medium | Mitigate | CTO |
| R-008 | Unauthorised internal access to records | Data | High | High | Mitigate | CTO |
| R-009 | Prescription processing error / patient harm | Operational | Medium | Medium | Mitigate | CMO |
| R-010 | SMS delivery failure / missed reminders | Operational | Medium | Medium | Mitigate | Head of Product |
| R-011 | RDS data loss (backup failure / ransomware) | Operational / Data | Medium | Low | Mitigate | CTO |
| R-012 | Twilio vendor security breach | Vendor | Medium | Low | Accept | Privacy Officer |
| R-013 | AWS RDS AZ availability (single-AZ risk) | Operational / Vendor | Medium | Low | Mitigate | CTO |
| R-014 | Twilio service outage | Vendor | Low | Low | Accept | Head of Operations |
| R-015 | Uncontrolled Twilio SMS spend | Financial | Low | Low | Mitigate | CTO |
| R-016 | Public breach — reputational damage | Reputational | High | High | Mitigate | CEO |

---

## Prioritised Actions

### Immediate — Pre-Launch Blockers (Critical residual risk)

1. **R-001 — TGA SaMD Review:** Commission a TGA regulatory affairs consultant to classify Prescribe under the SaMD framework. If the system is SaMD, registration and ISO/IEC 62304 compliance are required before any patient use. This is a criminal liability risk. **Target: before patient go-live.**

2. **R-002 — RTPM Integration:** Determine which medication schedules (S4, S8) the platform handles. If S8 or S4-of-concern medications are in scope, integrate with state RTPM systems before launch. If not, document the exclusion explicitly. **Target: before patient go-live.**

### High Priority — Complete Before 3 Months

3. **R-005 — Twilio PHI audit:** Review all SMS templates. Strip PHI where possible; execute APP 8-compliant DPA with Twilio; update patient privacy notices. If PHI cannot be removed, obtain explicit informed consent from patients.

4. **R-006 — NZ data residency legal opinion:** Obtain legal advice on NZ IPP 12 compliance basis for AWS ap-southeast-2; disclose offshore storage to NZ patients; document the compliance position.

5. **R-008 — Internal access controls:** Implement role-based access control; enable RDS audit logging; segregate production data from development environments.

6. **R-016 — Breach response plan:** Develop patient notification templates, media response protocol, and internal incident escalation runbook. Obtain cyber liability insurance. Test annually.

### Planned Mitigation — Complete Before Launch

7. **R-003 — Privacy Impact Assessment:** Commission PIA; appoint Privacy Officer; implement consent capture, access/correction workflow, and NDB incident response playbook.

8. **R-004 — NZ Privacy Act gap analysis:** Conduct gap assessment against Health Information Privacy Code 2020; add NZ-specific privacy disclosures.

9. **R-007 — Data security hardening:** Verify RDS encryption at rest and in transit; conduct pre-launch penetration test; implement WAF; enforce parameterised queries.

10. **R-009 — Clinical safety workflow:** Implement prescriber confirmation step; add clinical decision support warnings; implement audit trail for all prescription actions.

11. **R-011 — Backup verification:** Test RDS backup recovery to a non-production environment; document RTO/RPO; consider cross-region snapshot replication.

12. **R-013 — Multi-AZ verification:** Confirm Multi-AZ is enabled on the RDS instance; document and test failover.

### Monitor and Review (Low–Medium residual)

13. **R-010** — Implement delivery receipt monitoring and retry logic; alert on delivery failure > 10%.
14. **R-012** — Annual vendor review of Twilio security posture; verify DPA annually.
15. **R-014** — Subscribe to Twilio status page; evaluate fallback SMS provider at 12-month review.
16. **R-015** — Configure Twilio spend alerts and per-patient daily send limits before launch.

---

## Review Schedule

- **Next review:** 2026-11-01 (6 months)
- **Review triggers (any of these require immediate reassessment):**
  - Any notifiable data breach or security incident
  - Addition of AI/ML features (triggers `/grc-lead:ai-governance-review`)
  - Expansion to additional countries or patient populations
  - Integration with My Health Record, Medicare, or RTPM systems
  - Change in medication schedules handled (e.g., adding S8 substances)
  - New regulatory guidance from TGA, OAIC, or NZ Privacy Commissioner
  - Change of SMS provider or cloud hosting architecture
  - 6-month calendar maximum (2026-11-01)

---

## Related Assessments

- `/grc-lead:compliance-audit` — run against the Australian Privacy Act APPs and NZ Privacy Act 2020 once controls are implemented (R-003, R-004)
- `/grc-lead:ai-governance-review` — required before any ML features are introduced
- TGA SaMD classification review — external regulatory affairs engagement (R-001)

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 19.0/19.5 (97%) |
| Evaluated | 2026-05-01 |
| Target duration | 397880 ms |
| Target cost | $1.0468 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 defines scope boundaries explicitly — what is in and out, time horizon, and affected stakeholders | PASS | Scope section lists in-scope ('Patient-facing prescription workflows; medication history storage; SMS reminder delivery; AU and NZ patient populations'), explicit exclusions ('Clinical practice management; prescriber-side workflows beyond prescription submission; My Health Record; payment processing; patient-facing web/mobile UI internals'), time horizon ('Immediate to 12 months'), and stakeholders ('Patients (AU/NZ); prescribing practitioners; dispensing pharmacists; OAIC; NZ Privacy Commissioner; TGA; state pharmacy boards; Prescribe's board and leadership'). |
| c2 | Risk identification covers all seven categories — including Regulatory, AI/ML (even if N/A), Data, Operational, Financial, Reputational, and Vendor | PASS | Regulatory: R-001 to R-006. AI/ML: explicit 'No AI/ML risks identified' section. Data: R-006, R-007, R-008. Operational: R-009, R-010, R-011, R-013. Financial: R-015. Reputational: R-016. Vendor: R-012 (Twilio breach), R-014 (Twilio outage). All seven categories present. |
| c3 | Every identified risk has a unique ID, a likelihood level with a percentage estimate, and an impact level | PASS | All 16 risks (R-001 through R-016) carry unique IDs, percentage-qualified likelihoods (e.g. R-001: 'High (50%)', R-009: 'Low (8%)', R-006: 'Very High (>90%)', R-014: 'Low (5%)'), and explicit impact levels (Low / Medium / High / Critical). |
| c4 | Inherent risk scores are derived from the matrix — not assigned arbitrarily | PASS | Every inherent risk entry shows the derivation in parenthetical notation, e.g. R-003: 'High (Medium × Critical)', R-006: 'Critical (Very High × High)', R-009: 'Medium (Low × Critical)'. Scores are consistent across all 16 risks — the same likelihood-impact combinations always produce the same outcome. |
| c5 | Existing controls are documented per risk — not just assumed present | PASS | Each risk carries a 'Current controls' field that distinguishes confirmed, assumed, and absent controls. E.g. R-007: 'AWS RDS provides encryption at rest (AES-256) and in transit (TLS) if configured; VPC network isolation assumed. Application-level controls (parameterised queries, WAF, audit logging) are unverified.' R-001 and R-002 both state 'None identified.' Control effectiveness ratings follow. |
| c6 | Residual risk is calculated after controls, not just inheriting the inherent score | PASS | Multiple risks show residual reduction: R-003 Inherent High → Residual Medium; R-006 Inherent Critical → Residual High; R-007 Inherent High → Residual Medium; R-011 Inherent Medium → Residual Low; R-012 Inherent Medium → Residual Low. Where no controls exist, residual equals inherent (R-001, R-002 both remain Critical), which is correct reasoning. |
| c7 | Every risk has a treatment decision (Accept/Mitigate/Transfer/Avoid) with specific detail | PASS | All 16 risks have labelled treatments. Mitigate risks include step-by-step actions (e.g. R-005: '(1) audit all SMS message templates and strip PHI where possible; (2) execute an APP 8-compliant DPA with Twilio; (3) update patient privacy notices'). Accept treatments (R-012, R-014) include rationale. No Transfer or Avoid decisions used — the option is visible but treatments are all Mitigate or Accept. |
| c8 | Accepted risks have an owner, a justification, and a review date (max 6 months) | PASS | R-012: Owner '[Privacy Officer — to be appointed]', justification 'Twilio has improved security posture post-2022; vendor breaches are infrequent', review date '2026-11-01' (6 months from assessment date 2026-05-01). R-014: Owner '[Head of Operations — to be appointed]', justification 'Twilio's SLA and track record make extended outages rare', review date '2026-11-01'. Both within the 6-month cap. |
| c9 | Output is compiled into the risk register format with a summary table and prioritised action list | PASS | Artifact contains a 'Risk Register' section with full per-risk entries, a 'Risk Summary' table (Risk ID, Description, Category, Inherent, Residual, Treatment, Owner columns across 16 rows), and a 'Prioritised Actions' section with four tiers: Immediate Pre-Launch Blockers, High Priority (3 months), Planned Mitigation (before launch), and Monitor and Review. |
| c10 | Identifies Twilio as a vendor risk and AWS RDS as a data residency and availability risk | PARTIAL | Twilio addressed as vendor risk in R-012 (security breach) and R-014 (outage). AWS RDS addressed as data residency risk in R-003 and R-006 (NZ residency gap), and as availability risk in R-013 (single-AZ). All four dimensions covered. Ceiling is PARTIAL by test design. |
| c11 | Output's scope section names Prescribe, the in-scope subsystems (prescription store, repeat-prescription processor, SMS reminder service), the time horizon (e.g. 12 months), and the affected stakeholders (patients in AU/NZ, prescribers, pharmacy partners, regulators) | PASS | Scope names 'Prescribe', lists 'medication history storage (AWS RDS ap-southeast-2)' (prescription store), 'Patient-facing prescription workflows' (repeat-prescription processor, implicit), 'SMS reminder delivery (Twilio)' (SMS reminder service), time horizon 'Immediate to 12 months', and stakeholders including 'Patients (AU/NZ); prescribing practitioners; dispensing pharmacists; OAIC; NZ Privacy Commissioner; TGA'. Pharmacy partners represented as 'dispensing pharmacists'. |
| c12 | Output identifies risks in all seven categories with at least one risk per category — Regulatory (Privacy Act / Health Records / TGA), AI/ML (N/A noted explicitly if no ML), Data (PHI breach, ID disclosure), Operational (SMS delivery failure on critical reminder), Financial, Reputational, Vendor (Twilio, AWS) | PASS | All seven present: Regulatory — R-001 (TGA), R-003 (AU Privacy Act), R-004 (NZ Privacy Act). AI/ML — 'No AI/ML risks identified' section with explicit note. Data — R-007 (PHI breach via RDS), R-008 (internal access). Operational — R-010 (SMS delivery failure on reminders). Financial — R-015 (runaway Twilio spend). Reputational — R-016 (public breach). Vendor — R-012 (Twilio), R-013 (AWS RDS). |
| c13 | Output assigns each risk a unique ID (e.g. R-001, R-002), a likelihood with a percentage estimate (e.g. "Medium ~25%"), and an impact level (Low / Medium / High / Critical) — not just verbal labels | PASS | All 16 risks use R-001 through R-016 format, percentage-qualified likelihoods ('High (50%)', 'Medium (25%)', 'Low (8%)', 'Very High (>90%)', 'Low (5%)'), and one of four impact levels (Medium, High, Critical). Numeric percentages are present throughout, not just verbal labels. |
| c14 | Output's inherent risk scores are derived from a likelihood × impact matrix (e.g. 5×5) shown in the output — not assigned arbitrarily | PARTIAL | Derivation notation is shown inline for every risk (e.g. 'High (Medium × Critical)', 'Critical (High × Critical)') confirming non-arbitrary assignment and consistent application of the matrix. However, no standalone matrix table (e.g. a 5×5 grid of likelihood vs impact cells) is explicitly shown in the artifact. The derivation is visible but the matrix itself is not rendered. |
| c15 | Output documents existing controls per risk — e.g. for "patient data breach via SMS provider" the existing controls are "Twilio TLS in transit, signed DPA, no PHI in SMS body" — not assumed | PASS | R-005 (Twilio PHI): 'None confirmed. Twilio is GDPR-compliant but GDPR adequacy does not automatically satisfy Australian APPs.' R-012 (Twilio breach): 'Twilio is SOC 2 Type II certified. Twilio GDPR DPA available. AU/NZ-specific data processing agreement status is unknown.' Controls are documented with explicit uncertainty markers ('assumed', 'unverified', 'unknown') rather than treated as given. |
| c16 | Output calculates residual risk per risk after the existing controls are applied, with a clear reduction shown (e.g. "Inherent: High, Residual: Medium after controls") | PASS | Every risk entry shows both Inherent risk and Residual risk fields. Reductions are visible: R-003 High → Medium, R-006 Critical → High, R-007 High → Medium, R-011 Medium → Low, R-012 Medium → Low. The summary table also shows both columns side-by-side for all 16 risks. |
| c17 | Output assigns a treatment decision (Accept / Mitigate / Transfer / Avoid) per risk with specifics — what mitigation will be added, what the transfer mechanism is (insurance), why an acceptance is reasonable | PASS | All 16 risks have labelled treatments with action specifics. R-016 Mitigate includes 'obtain cyber liability insurance' (transfer mechanism). R-012 Accept: 'Twilio has improved security posture post-2022' (justification). R-014 Accept: 'Twilio's SLA and track record make extended outages rare' (justification). Mitigate decisions list numbered or bulleted concrete steps. |
| c18 | Output's accepted risks have a named owner, justification, and a review date with the rule that the date is no more than 6 months out | PASS | R-012: owner '[Privacy Officer — to be appointed]', justification 'vendor breaches are infrequent; Twilio has improved security posture post-2022', review date '2026-11-01'. R-014: owner '[Head of Operations — to be appointed]', justification 'Twilio's SLA and track record make extended outages rare', review date '2026-11-01'. Assessment date is 2026-05-01; both review dates are exactly 6 months, meeting the cap. |
| c19 | Output addresses Twilio specifically as a vendor risk — DPA in place, breach notification clauses, TGA / Privacy Act-compliant data handling, dependency risk if Twilio outage prevents critical reminders | PASS | R-005 addresses APP 8 / Privacy Act-compliant handling via Twilio and DPA requirement. R-012 references 'Twilio GDPR DPA available' and 'AU/NZ-specific data processing agreement status unknown', and 2022 breach history. R-010 addresses delivery failure dependency risk for missed medication reminders. R-014 addresses outage dependency. All four dimensions covered. |
| c20 | Output addresses AWS RDS in ap-southeast-2 as a data residency choice (Australia + NZ) and a single-AZ vs multi-AZ availability decision, with the trade-offs surfaced | PASS | Data residency: R-003 notes 'AWS RDS in ap-southeast-2 provides Australian data residency (positive)'; R-006 explicitly flags 'AWS ap-southeast-2, which is physically located in Sydney, Australia... constitutes offshore disclosure' for NZ patients under IPP 12. Single-AZ vs Multi-AZ: R-013 'If AWS RDS is deployed in a single Availability Zone (single-AZ), an AZ-level failure causes complete database unavailability' with trade-offs and mitigation. |

### Notes

An exceptionally thorough risk assessment. All 16 risks span all seven required categories, each carrying unique IDs, percentage-qualified likelihoods, explicit impact levels, documented controls with uncertainty markers, residual calculations, and treatment decisions. AU/NZ regulatory nuance is notably strong — TGA SaMD, state-level RTPM systems, APP 8 cross-border obligations, NZ IPP 12 data residency, and post-2024 penalty scales are all accurately surfaced. The only meaningful gap is c14: no standalone likelihood×impact matrix table is rendered in the artifact; derivation is visible only through inline parenthetical notation (e.g. 'High × Critical'). Everything else meets or exceeds the rubric. The output's prioritised action list correctly escalates TGA SaMD and RTPM to pre-launch blockers, and accepted risks (R-012, R-014) have owners, justifications, and review dates exactly at the 6-month ceiling.
