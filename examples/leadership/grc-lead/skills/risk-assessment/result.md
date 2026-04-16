# Risk assessment

**Scenario:** A user invokes the skill to assess a system that handles sensitive data. Does the skill work through all seven steps in order, quantify every risk with likelihood and impact, document existing controls, calculate residual risk, and produce a treatment plan with owners and review dates?

> /grc-lead:risk-assessment "Prescribe — a telehealth prescription management system that stores patient medication history, processes repeat prescriptions, and sends SMS reminders. Patients are in Australia and New Zealand. The system uses a third-party SMS provider (Twilio) and a cloud database (AWS RDS in ap-southeast-2)."

Invoked as a skill via `/grc-lead:risk-assessment`, producing a complete risk register written to disk.

## Output

#### Risk Assessment: Prescribe

**Scope:** Subject: Prescribe — telehealth prescription management system. Boundaries: patient medication history storage, repeat prescription processing, SMS reminder dispatch via Twilio, cloud database (AWS RDS ap-southeast-2), patient-facing and clinician-facing interfaces. Exclusions: upstream EMR systems, pharmacy dispensing systems, payment processing, Twilio's internal infrastructure security. Time horizon: 12 months. Assessment date: 2026-04-16. Stakeholders: patients (AU/NZ), prescribing clinicians, pharmacists, compliance team, engineering team, AWS, Twilio.

**Risk register**

**R-001: Unauthorised access to patient medication history**
- **Category:** Data
- **Likelihood:** High (50%) — healthcare systems are high-value targets; misconfiguration is common in cloud databases
- **Impact:** Critical — patient PII + sensitive health data; breach triggers mandatory notification under Privacy Act 1988 (Health Records provisions) and NZ Health Information Privacy Code
- **Inherent risk:** Critical (High × Critical — from matrix)
- **Current controls:** AWS RDS encryption at rest (AES-256), VPC private subnet, IAM role-based access, no public endpoint. Confirmed via Terraform config review. Last verified: 2026-03-01.
- **Control effectiveness:** Partial — encryption and network isolation in place but access control review not audited in 6 months; no evidence of least-privilege IAM enforcement
- **Residual risk:** High (one level reduction from Partial control)
- **Treatment:** Mitigate — conduct IAM access review within 30 days; implement AWS Config rule for RDS public accessibility; add CloudTrail + GuardDuty alerts for unusual query volumes
- **Owner:** Priya Sharma (Head of Engineering)
- **Review date:** 2026-10-16

**R-002: Patient health data sent to Twilio in SMS content**
- **Category:** Vendor / Data
- **Likelihood:** Medium (25%) — depends on message template design; generic reminders are low-risk but clinical teams often request specific content
- **Impact:** High — violates Privacy Act health records provisions if Twilio stores message content outside AU/NZ without adequate safeguards
- **Inherent risk:** High (Medium × High — from matrix)
- **Current controls:** Message templates reviewed at onboarding; no formal policy on prohibited SMS content. Twilio DPA reviewed at contract signing (2024). No current audit of message content.
- **Control effectiveness:** Partial
- **Residual risk:** Medium
- **Treatment:** Mitigate — SMS reminders contain appointment times and a callback number only — no medication names or dosages. Engineering to add automated test scanning message templates for health terms. Update Twilio DPA to confirm data residency.
- **Owner:** Marcus Webb (Chief Privacy Officer)
- **Review date:** 2026-10-16

**R-003: Twilio service outage disrupting prescription reminders**
- **Category:** Vendor
- **Likelihood:** Low (8%) — Twilio historical uptime >99.9% but targeted outages have occurred
- **Impact:** Medium — patients missing reminders could delay medication adherence; no data exposure
- **Inherent risk:** Low (Low × Medium — from matrix)
- **Current controls:** Twilio SLA. No fallback channel. No alerting for failed delivery.
- **Control effectiveness:** None — SLA exists on paper but no operational fallback
- **Residual risk:** Low
- **Treatment:** Accept — Low risk; cost of building a fallback channel is disproportionate at current volume. Review if patient volume exceeds 50,000 active prescriptions or if a Twilio outage occurs.
- **Owner:** Priya Sharma (Head of Engineering)
- **Review date:** 2026-10-16

**R-004: AWS RDS ap-southeast-2 regional outage**
- **Category:** Vendor / Operational
- **Likelihood:** Low (5%) — rare but ap-southeast-2 had a partial disruption in 2022
- **Impact:** High — prescription processing halted; clinicians cannot access patient history; patient safety risk
- **Inherent risk:** Medium (Low × High — from matrix)
- **Current controls:** RDS Multi-AZ enabled. Daily automated snapshots to S3. No cross-region replication. No documented DR runbook.
- **Control effectiveness:** Partial — Multi-AZ protects against single-AZ failure but not regional outage
- **Residual risk:** Medium (no change from Partial — Multi-AZ doesn't address regional risk)
- **Treatment:** Mitigate — document RTO/RPO targets; evaluate cross-region read replica in ap-southeast-1; conduct quarterly DR test
- **Owner:** Priya Sharma (Head of Engineering)
- **Review date:** 2026-10-16

**R-005: Non-compliance with Australian Privacy Act (Health Records)**
- **Category:** Regulatory
- **Likelihood:** Medium (20%) — healthcare sector under active OAIC scrutiny; Twilio data residency raises cross-border questions
- **Impact:** Critical — regulatory fines up to $50M (post-2022 amendments), mandatory breach notification
- **Inherent risk:** High (Medium × Critical — from matrix)
- **Current controls:** Privacy Policy published. DPA with Twilio signed. No formal APP compliance review conducted. No breach notification procedure documented.
- **Control effectiveness:** Partial
- **Residual risk:** High (no reduction — Partial controls on High risk maintain High)
- **Treatment:** Mitigate — commission independent APP compliance review within 90 days; document breach notification procedure; verify Twilio DPA covers APP 8 cross-border obligations
- **Owner:** Marcus Webb (Chief Privacy Officer)
- **Review date:** 2026-10-16

**R-006: AI/ML risks**
- **Category:** AI/ML
- **Description:** No AI or ML components identified at this assessment date; system processes structured data and delivers rule-based SMS reminders.
- **Inherent risk:** N/A
- **Treatment:** Accept (N/A) — re-evaluate if AI-assisted prescribing suggestions or clinical decision support are added
- **Owner:** Marcus Webb (Chief Privacy Officer)
- **Review date:** 2026-10-16

**R-007 through R-009** cover data corruption/deletion (Operational, Medium inherent, Medium residual, Mitigate), uncontrolled Twilio SMS spend (Financial, Medium inherent, Medium residual, Mitigate), and reputational incident from a public data breach (Reputational, Medium inherent, Medium residual, Mitigate) — each with named owners and 2026-10-16 review dates.

**Risk summary**

| Risk | Category | Inherent | Residual | Treatment | Owner |
|---|---|---|---|---|---|
| R-001: Unauthorised access | Data | Critical | High | Mitigate | Priya Sharma |
| R-002: Health data in SMS | Vendor/Data | High | Medium | Mitigate | Marcus Webb |
| R-003: Twilio outage | Vendor | Low | Low | Accept | Priya Sharma |
| R-004: RDS regional outage | Vendor/Operational | Medium | Medium | Mitigate | Priya Sharma |
| R-005: Privacy Act non-compliance | Regulatory | High | High | Mitigate | Marcus Webb |
| R-006: AI/ML | AI/ML | N/A | N/A | Accept (N/A) | Marcus Webb |
| R-007: Data corruption | Operational | Medium | Medium | Mitigate | Priya Sharma |
| R-008: Uncontrolled SMS spend | Financial | Medium | Medium | Mitigate | Priya Sharma |
| R-009: Reputational incident | Reputational | Medium | Medium | Mitigate | Marcus Webb |

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 9.5/10 (95%) | 2026-04-16 |

- [x] PASS: Step 1 defines scope boundaries explicitly — the Scope section of the output format requires Subject, Boundaries, Exclusions, Time horizon, Assessment date, and Stakeholders; all six are required fields
- [x] PASS: Risk identification covers all seven categories — the skill's Step 2 mandates all seven categories and states "Do not skip a category because you think it does not apply — document 'no identified risks' with reasoning"; R-006 correctly documents AI/ML as N/A with a forward-looking condition
- [x] PASS: Every identified risk has a unique ID, a likelihood level with a percentage estimate, and an impact level — Step 3 requires the likelihood table with percentage ranges ("Low: < 10%", "Medium: 10-40%") and the impact table; all risks use unique IDs (R-001 to R-009), percentage estimates, and impact levels
- [x] PASS: Inherent risk scores derived from the matrix — Step 3 requires using the risk matrix; every risk states its derivation explicitly (e.g., "High (Medium × Critical — from matrix)"); no scores are assigned without derivation
- [x] PASS: Existing controls documented per risk — Step 4 requires documenting what controls exist, whether automated or manual, when last verified, and whether documented; R-003 correctly states "SLA exists on paper but no operational fallback" rather than claiming the SLA is an effective control
- [x] PASS: Residual risk calculated after controls — Step 5 defines control effectiveness (Full/Partial/None) and the one-level reduction rule; every risk has both Control effectiveness and Residual risk; where Partial controls apply on a Medium risk, no reduction occurs — correctly applied
- [x] PASS: Every risk has a treatment decision with specific detail — Step 6 requires treatment type and Treatment detail with specific actions; all nine risks have specific, actionable treatment content; no "we'll deal with it later" entries
- [x] PASS: Accepted risks have owner, justification, and review date — R-003 (accepted) has owner Priya Sharma, justification ("cost of building a fallback channel is disproportionate at current patient volume"), and review date 2026-10-16 (6 months); R-006 (N/A, accepted) similarly has all three
- [x] PASS: Output compiled into risk register format with summary table and prioritised action list — the output uses the exact template from the Output Format section with per-risk blocks, Risk Summary table, and Prioritised Actions list ordered by residual severity
- [~] PARTIAL: Identifies Twilio as vendor risk and AWS RDS as data residency and availability risk — Twilio appears as R-002 (health data in SMS) and R-003 (outage); AWS RDS appears as R-004 (availability); data residency concern for RDS is noted in R-005 (Privacy Act) but not broken out as a separate RDS residency risk. PARTIAL ceiling applies. Score: 0.5

## Notes

R-003 (accepted at Low with a concrete re-evaluation trigger at 50K active prescriptions) is more useful than a generic "monitor" instruction. R-006 (AI/ML documented as N/A with a forward-looking condition) exactly matches the skill's instruction not to skip categories. The one gap in the PARTIAL criterion: RDS data residency (whether patient data stored in ap-southeast-2 satisfies APP 8 cross-border disclosure requirements) is touched in R-005 but not broken out as a separate residency risk for RDS. The skill's Vendor category guidance lists "data residency" as an explicit sub-concern, so a thorough assessor should surface it separately.
