# Risk Assessment

Scenario: A user invokes the skill to assess a system that handles sensitive data. Does the skill work through all seven steps in order, quantify every risk with likelihood and impact, document existing controls, calculate residual risk, and produce a treatment plan with owners and review dates?

## Prompt

> /grc-lead:risk-assessment "Prescribe — a telehealth prescription management system that stores patient medication history, processes repeat prescriptions, and sends SMS reminders. Patients are in Australia and New Zealand. The system uses a third-party SMS provider (Twilio) and a cloud database (AWS RDS in ap-southeast-2)."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll conduct a comprehensive risk assessment for Prescribe. Let me work through each step systematically.

## Step 1: Scope Definition

- **Subject:** Prescribe — telehealth prescription management system
- **Boundaries:** Patient data storage (medication history, personal identifiers), prescription processing logic, SMS reminder delivery via Twilio, AWS RDS database operations, authentication/access control, SMS communication channels
- **Exclusions:** Third-party healthcare provider systems (GP systems, pharmacy systems) that Prescribe integrates with; physical pharmacy operations; patient devices (phones, browsers) security
- **Time horizon:** Immediate risks (0-3 months), medium-term (3-12 months), ongoing operational risks
- **Stakeholders:** Patients (AU/NZ), healthcare providers, Prescribe operators, regulatory bodies (OAIC, NZ Privacy Commissioner), Twilio/AWS as vendors
- **Assessment date:** 2026-05-04
- **Assessor:** GRC Lead

---

## Step 2: Risk Identification

### Regulatory Risks

| Risk ID | Description |
|---|---|
| R-001 | Non-compliance with Australian Privacy Act 1988 (Privacy Principles 1-13), particularly APP 1 (open and transparent management), APP 3 (collection of solicited personal information), APP 12 (access and correction), APP 13 (correction and notifiable data breaches). Prescribe stores sensitive health information without documented compliance framework |
| R-002 | Non-compliance with NZ Privacy Act 2020 — similar principles, different enforcement. Dual-jurisdiction system requires tailored controls |
| R-003 | GDPR applicability unclear — if patients can include EU residents or if integration with EU healthcare providers exists, GDPR applies. Currently no evidence of GDPR-ready infrastructure (e.g., data processing agreements, right to erasure mechanisms) |
| R-004 | Failure to meet notifiable data breaches obligations (Australian Privacy Act s.33ZE, NZ Privacy Act 2020 s.104). No documented breach response plan or notification timeline (Australian standard: 30 days) |
| R-005 | Health records legislation gaps — no evidence of compliance with Australian Health Records Act 1988 or NZ Health Information Privacy Code (if applicable). Prescribe may be classified as a healthcare provider and subject to stricter standards than general data handlers |
| R-006 | SMS communications not compliant with AASB/Australian Telecom regulations — unsolicited or improperly consented SMS reminders could trigger regulatory violations and complaints |

### Operational Risks

| Risk ID | Description |
|---|---|
| R-007 | Single cloud provider dependency (AWS ap-southeast-2) — regional outage in Sydney affects all operations. No multi-region failover, no backup database |
| R-008 | Third-party SMS provider outage (Twilio) — prescription reminders fail silently if Twilio is down. Patients miss medication schedules |
| R-009 | Key person dependency — no documented evidence of knowledge transfer for prescription processing logic, database schema, or emergency procedures |
| R-010 | Repeat prescription workflow not documented — unclear how repeat prescriptions are approved, authorised, and validated. Risk of unauthorised refills or missed expiry checks |
| R-011 | SMS delivery failures not tracked — no mention of delivery confirmation, retry logic, or failure alerting. Patients may believe reminders sent when delivery failed |
| R-012 | Incident response and escalation plan missing — no documented process for data breaches, outages, or prescription errors |

### Data Risks

| Risk ID | Description |
|---|---|
| R-013 | Patient medication history stored unencrypted or with weak encryption — AWS RDS encryption not specified. Data at rest and in transit encryption unknown |
| R-014 | Personal identifiable information (name, phone, address) collected and stored without documented data minimisation — unclear what patient data is necessary vs. collected for convenience |
| R-015 | No documented data retention and deletion policy — medication histories kept indefinitely without justification. Deleted patient records may persist in backups without secure erasure |
| R-016 | SMS communication channels unencrypted — Twilio API calls to send reminders must use HTTPS, but no evidence of TLS verification or API authentication hardening |
| R-017 | Database access controls not documented — unclear who can access patient records, how access is logged, and whether role-based access control (RBAC) is enforced |
| R-018 | Prescription data integrity not verified — no checksums, digital signatures, or audit trails for prescription records. Risk of undetected tampering |

### Vendor/Third-Party Risks

| Risk ID | Description |
|---|---|
| R-019 | Twilio security posture and uptime SLA unknown — no evidence of vendor assessment, SLA review, or data processing agreement (DPA) documenting how Twilio handles patient phone numbers |
| R-020 | AWS RDS security configuration not documented — unclear if database is publicly accessible, if IAM policies restrict access, or if VPC/security groups are correctly configured |
| R-021 | No data processing agreement with Twilio — GDPR/Privacy Act compliance requires written DPA specifying data handling obligations, sub-processor approval, and data breach notification |
| R-022 | Vendor lock-in (AWS RDS, Twilio) — switching providers requires data migration and API rewrite. Cost and timeline not understood |
| R-023 | Twilio phone number depletion or temporary suspension — regulatory violations (unsolicited SMS) could result in Twilio account suspension, making the system unable to send any reminders |

### Reputational Risks

| Risk ID | Description |
|---|---|
| R-024 | Data breach disclosure — if patient medication history or phone numbers leaked, reputational damage and loss of patient trust. Media attention likely in healthcare sector |
| R-025 | Prescription errors causing patient harm — medication reminder failure or incorrect refill approval could result in missed doses, adverse effects, patient complaints, regulatory investigation, and lawsuits |
| R-026 | Unresponsiveness to regulatory inquiries — Privacy Commissioner investigations into complaints. Slow response or poor record-keeping suggests negligence |

### Financial Risks

| Risk ID | Description |
|---|---|
| R-027 | Regulatory fines — Australian Privacy Act breaches up to AUD $50M or 30% of turnover (whichever is higher); NZ Privacy Act up to NZD $3M. Prescribe has zero documented compliance controls |
| R-028 | Incident response and remediation costs — data breach notification, forensics, patient credit monitoring (if applicable), legal fees |
| R-029 | Operational costs of outages — SMS provider down → no reminders → medication non-compliance → poor patient outcomes → customer churn and refunds |
| R-030 | Uncontrolled AWS/Twilio costs — no cost monitoring, budget alerts, or rate limits. Potential for bill shock from high SMS volume or database operations |

### AI/ML Risks

| Risk ID | Description |
|---|---|
| R-031 | Not identified — system description does not mention AI/ML components. If prescription suggestions or automated approvals are used, this should be explicitly stated and assessed separately |

---

## Step 3: Risk Analysis

| Risk ID | Likelihood | Impact | Inherent Risk | Rationale |
|---|---|---|---|---|
| R-001 | Very High (85%) | Critical | **Critical** | Privacy Act compliance is non-negotiable for health data systems. Absence of documented compliance framework is a critical weakness. Enforcement by OAIC is active |
| R-002 | High (65%) | Critical | **Critical** | NZ Privacy Commissioner actively enforces. Dual-jurisdiction adds complexity; no evidence of NZ-specific controls |
| R-003 | Medium (30%) | Critical | **High** | GDPR applicability depends on patient/provider geography. If applicable and missed, fines are severe |
| R-004 | High (70%) | Critical | **Critical** | No notifiable breach process documented. When (not if) a breach occurs, failure to notify within 30 days violates Privacy Act |
| R-005 | High (60%) | Critical | **Critical** | Health records legislation applies if Prescribe qualifies as healthcare provider. Stricter standards than general data handling |
| R-006 | Medium (35%) | Medium | **Medium** | SMS regulatory compliance (e.g., AASB opt-in requirements) unknown. Risk of regulatory complaints and SMS provider suspension |
| R-007 | High (60%) | Critical | **Critical** | AWS Sydney region outages occur (2023 outage lasted hours). No documented failover. All prescriptions become unavailable |
| R-008 | Medium (40%) | High | **High** | Twilio outages are rare but possible. Reminder delivery degrades gracefully in most cases, but extended outages harm patients |
| R-009 | High (65%) | High | **High** | Prescription systems are business-critical. Single-person knowledge is a common failure point. Unplanned absence creates immediate risk |
| R-010 | Very High (80%) | Critical | **Critical** | Repeat prescription approval workflow not documented suggests it may not exist or is ad-hoc. Risk of unauthorised refills or missed expiry checks causing patient harm |
| R-011 | Very High (85%) | High | **Critical** | SMS failures silent by default unless logging is explicit. Patients believe reminders sent; medications missed; no visibility into failures |
| R-012 | Very High (90%) | Critical | **Critical** | Healthcare incidents require rapid, documented response. Absence of incident plan means chaotic, uncoordinated response under pressure |
| R-013 | Very High (80%) | Critical | **Critical** | No evidence of encryption. Patient medication histories are high-value targets for attackers. Database accessible to anyone with network access or credentials |
| R-014 | High (70%) | Medium | **High** | Patient data collection without minimisation. More data stored = larger breach surface. Regulatory expectation is to collect only necessary data |
| R-015 | Very High (85%) | Medium | **High** | No retention policy means data persists indefinitely. Deleted records in backups never securely erased. Violates Privacy Act principles on data minimisation |
| R-016 | Medium (35%) | Medium | **Medium** | Twilio API should enforce TLS; misconfiguration possible. SMS phone numbers in plain-text logs or in transit leak personally identifiable information |
| R-017 | Very High (80%) | High | **Critical** | No documented access control suggests ad-hoc or absent controls. Anyone with database credentials can access all patient records |
| R-018 | High (65%) | High | **High** | No audit trail means tampering is undetectable. Prescription records are safety-critical; undetected tampering could cause patient harm |
| R-019 | High (70%) | High | **High** | Twilio security posture not assessed. SMS provider could be compromised, exposing patient phone numbers. No DPA = no contractual recourse |
| R-020 | Very High (85%) | Critical | **Critical** | AWS RDS misconfiguration is common. If database is publicly accessible or IAM policies are lax, attackers can access all patient data |
| R-021 | Very High (90%) | Critical | **Critical** | No DPA with Twilio means GDPR/Privacy Act non-compliance. No obligation for Twilio to notify on breach. Prescribe is liable for Twilio's actions |
| R-022 | Medium (25%) | Medium | **Medium** | Vendor lock-in is strategic risk, not immediate. Relevant if Prescribe needs to pivot, but not an urgent threat |
| R-023 | Medium (40%) | Critical | **High** | Twilio account suspension from regulatory violations (unsolicited SMS) would disable reminder system entirely. Patient safety impact |
| R-024 | High (60%) | Critical | **Critical** | Healthcare data breaches are high-profile. Media attention guaranteed. Patient trust eroded, customer churn likely |
| R-025 | Very High (80%) | Critical | **Critical** | Prescription errors causing patient harm (missed medications, overdose) are patient safety risks. Regulatory investigation, lawsuits, criminal liability possible |
| R-026 | High (65%) | High | **High** | Privacy Commissioner investigations standard for complaints. Poor response suggests negligence; increases regulatory penalties |
| R-027 | High (70%) | Critical | **Critical** | Australian Privacy Act penalties are severe. No documented compliance = high fine exposure. NZ fines lower but still material |
| R-028 | High (60%) | High | **High** | Incident response costs (forensics, notification, legal) are substantial. Unbudgeted and often underestimated |
| R-029 | Medium (40%) | High | **High** | Outages cause patient harm and churn. Cost to reputation and revenue accumulates quickly |
| R-030 | High (65%) | Medium | **High** | AWS/Twilio costs not monitored. Volume spikes (mass SMS) can cause unexpected bill shock. No rate limits or alerts documented |

---

## Step 4: Existing Controls Assessment

| Control | Evidence | Status | Last Verified |
|---|---|---|---|
| **Encryption** | None documented | ❌ Missing | N/A |
| **Access control (RBAC)** | None documented | ❌ Missing | N/A |
| **Data retention policy** | None documented | ❌ Missing | N/A |
| **Breach notification process** | None documented | ❌ Missing | N/A |
| **Vendor agreements (DPA)** | None documented | ❌ Missing | N/A |
| **Incident response plan** | None documented | ❌ Missing | N/A |
| **Database backup/failover** | None documented | ❌ Missing | N/A |
| **Audit logging** | None documented | ❌ Missing | N/A |
| **SMS delivery tracking** | None documented | ❌ Missing | N/A |
| **Data minimisation** | None documented | ❌ Missing | N/A |
| **Twilio/AWS security assessment** | None documented | ❌ Missing | N/A |
| **Prescription validation/approval workflow** | Unclear, possibly ad-hoc | ⚠️ Unclear | N/A |

**Verdict:** No documented controls exist. System appears to have been built without governance, risk management, or compliance framework.

---

## Step 5: Residual Risk Calculation

Because **zero controls** are documented and verified, residual risk = inherent risk for all items. Every control that should exist is absent.

| Risk ID | Inherent | Controls | Effectiveness | Residual | Action Required |
|---|---|---|---|---|---|
| R-001 | Critical | None | None | **Critical** | Mitigate immediately |
| R-002 | Critical | None | None | **Critical** | Mitigate immediately |
| R-003 | High | None | None | **High** | Clarify GDPR scope; mitigate if applicable |
| R-004 | Critical | None | None | **Critical** | Mitigate immediately |
| R-005 | Critical | None | None | **Critical** | Mitigate immediately |
| R-006 | Medium | None | None | **Medium** | Mitigate planned |
| R-007 | Critical | None | None | **Critical** | Mitigate immediately |
| R-008 | High | None | None | **High** | Mitigate planned |
| R-009 | High | None | None | **High** | Mitigate planned |
| R-010 | Critical | None | None | **Critical** | Mitigate immediately |
| R-011 | Critical | None | None | **Critical** | Mitigate immediately |
| R-012 | Critical | None | None | **Critical** | Mitigate immediately |
| R-013 | Critical | None | None | **Critical** | Mitigate immediately |
| R-014 | High | None | None | **High** | Mitigate planned |
| R-015 | High | None | None | **High** | Mitigate planned |
| R-016 | Medium | None | None | **Medium** | Mitigate planned |
| R-017 | Critical | None | None | **Critical** | Mitigate immediately |
| R-018 | High | None | None | **High** | Mitigate planned |
| R-019 | High | None | None | **High** | Mitigate planned |
| R-020 | Critical | None | None | **Critical** | Mitigate immediately |
| R-021 | Critical | None | None | **Critical** | Mitigate immediately |
| R-022 | Medium | None | None | **Medium** | Monitor ongoing |
| R-023 | High | None | None | **High** | Mitigate planned |
| R-024 | Critical | None | None | **Critical** | Mitigate immediately |
| R-025 | Critical | None | None | **Critical** | Mitigate immediately |
| R-026 | High | None | None | **High** | Mitigate planned |
| R-027 | Critical | None | None | **Critical** | Mitigate immediately |
| R-028 | High | None | None | **High** | Mitigate planned |
| R-029 | High | None | None | **High** | Mitigate planned |
| R-030 | High | None | None | **High** | Mitigate planned |

---

## Step 6: Risk Treatment

### Critical Residual Risks — Immediate Mitigation Required

**R-001, R-002, R-004, R-005: Regulatory Compliance (Privacy Act, Health Records Act)**

- **Treatment:** Mitigate
- **Actions:**
  1. Engage external compliance consultant (Privacy Act specialist). Timeline: 2 weeks
  2. Conduct Privacy Impact Assessment (PIA) per Privacy Act guidelines. Timeline: 4 weeks
  3. Document Privacy Policy covering collection, use, disclosure, access, correction, deletion (APPs 1, 5, 6, 12, 13). Timeline: 3 weeks
  4. Implement Privacy Principles compliance controls (documented procedures). Timeline: 8 weeks
  5. If Health Records Act applies: engage healthcare compliance consultant. Timeline: 3 weeks
  6. For NZ scope: engage NZ Privacy Act consultant; determine dual-jurisdiction requirements. Timeline: 2 weeks
  7. Implement notifiable breach process and timeline (30-day notification requirement). Timeline: 4 weeks
- **Owner:** GRC Lead / Privacy Officer (must be hired)
- **Review date:** 2026-08-04 (immediate action, then quarterly)
- **Success criteria:** Privacy Policy published; PIA completed and signed off; breach notification process documented and tested; Privacy Officer assigned

**R-010: Repeat Prescription Workflow**

- **Treatment:** Mitigate
- **Actions:**
  1. Document the current repeat prescription process (approval, validation, expiry checks, authorisation). Timeline: 1 week
  2. Identify gaps (e.g., no expiry check, no pharmacist approval, no doctor verification). Timeline: 2 weeks
  3. Implement approval workflow: patient request → doctor validation → prescription issued → pharmacy fulfillment. Timeline: 6 weeks
  4. Add automated expiry checks (prescription expires after doctor-specified period; no refills after expiry). Timeline: 3 weeks
  5. Implement audit trail for all prescription approvals/denials. Timeline: 2 weeks
  6. Test workflow with pilot group before production rollout. Timeline: 2 weeks
- **Owner:** Product Lead / Pharmacist Consultant
- **Review date:** 2026-06-04 (after implementation)
- **Success criteria:** Workflow documented; automated expiry checks prevent expired prescription refills; 100% of prescriptions have audit trail

**R-011, R-012: Incident Response & SMS Delivery Tracking**

- **Treatment:** Mitigate
- **Actions:**
  1. Implement SMS delivery logging (Twilio webhooks → database). Capture: sent time, delivery status, failure reason, retry count. Timeline: 2 weeks
  2. Set up alerting for SMS delivery failures (>5% failure rate triggers alert). Timeline: 1 week
  3. Document incident response plan: roles, escalation, notification timeline (notify Privacy Commissioner if breach within 30 days). Timeline: 2 weeks
  4. Conduct tabletop incident simulation (data breach scenario). Timeline: 1 week
  5. Implement audit logging for all system events (database access, prescription changes, user actions). Timeline: 3 weeks
- **Owner:** DevOps Lead / GRC Lead
- **Review date:** 2026-06-04 (after implementation)
- **Success criteria:** SMS delivery logs operational; delivery failure alerts tested; incident response plan published; tabletop completed

**R-013: Database Encryption**

- **Treatment:** Mitigate
- **Actions:**
  1. Enable AWS RDS encryption at rest (AES-256) if not already enabled. Timeline: 1 week (verify current state first)
  2. Enable encryption in transit: TLS 1.2+ for all database connections. Timeline: 1 week
  3. Implement application-level encryption for highly sensitive fields (medications list) using envelope encryption (master key in AWS KMS). Timeline: 4 weeks
  4. Rotate database passwords and enforce strong policies. Timeline: 1 week
  5. Verify current backups are encrypted; ensure future backups are encrypted. Timeline: 1 week
- **Owner:** DevOps Lead / Database Admin
- **Review date:** 2026-05-18 (verify encryption enabled)
- **Success criteria:** RDS encryption at rest enabled; TLS verified; application encryption for medications field deployed

**R-017: Access Control (RBAC)**

- **Treatment:** Mitigate
- **Actions:**
  1. Implement role-based access control (RBAC): roles = Admin, Doctor, Pharmacist, Patient, Support. Timeline: 3 weeks
  2. Define permissions per role (least privilege): e.g., Patient can only view their own prescriptions; Doctor can approve repeat requests. Timeline: 2 weeks
  3. Implement audit logging: log all access attempts (successful and failed) with timestamp, user, action, data accessed. Timeline: 2 weeks
  4. Regular access reviews: quarterly audit of who has access to what (segregation of duties). Timeline: ongoing
  5. Implement session timeout and re-authentication for sensitive operations. Timeline: 2 weeks
- **Owner:** DevOps Lead / Security Engineer
- **Review date:** 2026-06-04 (after implementation)
- **Success criteria:** RBAC implemented; audit logs operational; access review completed

**R-020: AWS RDS Security Configuration**

- **Treatment:** Mitigate
- **Actions:**
  1. Security audit of AWS RDS configuration: check if publicly accessible, VPC/security group settings, IAM policies. Timeline: 1 week
  2. Ensure database is NOT publicly accessible; restrict access to application VPC only. Timeline: 1 week
  3. Implement IAM policies: principle of least privilege (application role can only SELECT/INSERT/UPDATE, no ALTER/DROP). Timeline: 2 weeks
  4. Enable AWS RDS Enhanced Monitoring (CloudWatch metrics for CPU, memory, disk, network). Timeline: 1 week
  5. Enable AWS RDS Performance Insights to track slow queries and optimize. Timeline: 1 week
  6. Implement automated backups with multi-region replication (backup to secondary region). Timeline: 2 weeks
- **Owner:** DevOps Lead / AWS Architect
- **Review date:** 2026-05-18 (verify configuration)
- **Success criteria:** Database not publicly accessible; IAM policies verified; backups replicated; monitoring enabled

**R-021: Data Processing Agreement (DPA) with Twilio**

- **Treatment:** Mitigate
- **Actions:**
  1. Engage Twilio account manager to request DPA covering: data handling, sub-processor approval, breach notification, compliance with Privacy Act/GDPR. Timeline: 1 week
  2. If standard DPA unavailable, negotiate custom DPA. Timeline: 2 weeks
  3. Review and sign DPA before further SMS operations. Timeline: 1 week
  4. Document Twilio's security certifications (SOC 2, GDPR compliance, data residency). Timeline: 1 week
  5. For GDPR scope: ensure Twilio is EU-certified (Privacy Shield equivalent or Standard Contractual Clauses). Timeline: ongoing
- **Owner:** Legal / Procurement Lead
- **Review date:** 2026-05-18 (DPA signature)
- **Success criteria:** DPA signed; Twilio security certifications documented; compliance confirmed

**R-024, R-025, R-027: Patient Safety & Regulatory Liability**

- **Treatment:** Mitigate (comprehensive)
- **Actions:**
  1. All immediate mitigations above (encryption, access control, incident response) reduce this risk
  2. Additionally: Implement prescription validation rules (dose ranges, drug interactions, duplicates). Timeline: 4 weeks
  3. Implement patient notification on prescription status (sent, delivered, expired). Timeline: 3 weeks
  4. Implement insurance/professional indemnity for healthcare provider liability (covers patient harm claims). Timeline: 2 weeks
  5. Establish patient escalation process (patients can report issues, get live support). Timeline: 2 weeks
- **Owner:** GRC Lead / Legal / Product Lead
- **Review date:** 2026-08-04 (after regulatory compliance work)
- **Success criteria:** Validation rules operational; patient notifications working; insurance in place; escalation process documented

---

### High Residual Risks — Planned Mitigation (Next 8 weeks)

**R-007: AWS Region Failover**

- **Treatment:** Mitigate
- **Actions:**
  1. Implement multi-region failover: replicate RDS to ap-southeast-1 (Melbourne) or ap-northeast-1 (Tokyo). Timeline: 6 weeks
  2. Implement Route 53 health checks: if Sydney region down, automatically failover to secondary region. Timeline: 3 weeks
  3. Test failover quarterly (simulate region outage). Timeline: ongoing
  4. Document runbook for regional failure: timing, steps, communication plan. Timeline: 2 weeks
- **Owner:** DevOps Lead / AWS Architect
- **Review date:** 2026-07-04
- **Success criteria:** Secondary region replicated and tested; failover automation verified; runbook published

**R-008: Twilio Outage Resilience**

- **Treatment:** Mitigate
- **Actions:**
  1. Implement retry logic for SMS delivery: exponential backoff, max 3 retries over 24 hours. Timeline: 2 weeks
  2. Implement queue persistence: if SMS send fails, queue message for retry (don't lose). Timeline: 2 weeks
  3. Add fallback SMS provider (e.g., AWS SNS, Vonage) as backup if Twilio unavailable. Timeline: 4 weeks
  4. Monitor Twilio SLA and publish status page (patients see "Reminders temporarily unavailable"). Timeline: 2 weeks
- **Owner:** DevOps Lead / Product Lead
- **Review date:** 2026-07-04
- **Success criteria:** Retry logic tested; queue persistence verified; failover provider integrated; status page operational

**R-009: Key Person Dependency**

- **Treatment:** Mitigate
- **Actions:**
  1. Document all critical systems: prescription workflow, database schema, deployment process, emergency procedures. Timeline: 3 weeks
  2. Cross-train second person on each critical area. Timeline: 4 weeks
  3. Implement runbooks for emergency procedures (database restore, SMS restart, prescription recovery). Timeline: 2 weeks
  4. Conduct quarterly knowledge transfer reviews (each person explains critical system to another). Timeline: ongoing
- **Owner:** Engineering Manager / GRC Lead
- **Review date:** 2026-06-04
- **Success criteria:** All critical systems documented; cross-training completed; runbooks tested

**R-014, R-015: Data Minimisation & Retention**

- **Treatment:** Mitigate
- **Actions:**
  1. Conduct data inventory: audit all patient data collected (name, phone, address, medical history, etc.). Timeline: 2 weeks
  2. Assess necessity: which data is strictly required for prescriptions? Which is optional or could be deleted? Timeline: 2 weeks
  3. Implement data minimisation: remove unnecessary data collection; default to minimal set. Timeline: 3 weeks
  4. Implement retention policy: medication history retained for [X] years (per healthcare standards, e.g., 7-10 years); deleted records securely erased from all backups. Timeline: 3 weeks
  5. Implement automated deletion jobs (GDPR right to erasure compliance). Timeline: 3 weeks
- **Owner:** Data Architect / Privacy Officer
- **Review date:** 2026-07-04
- **Success criteria:** Data inventory completed; retention policy documented and implemented; deletion jobs operational

**R-018: Prescription Audit Trail**

- **Treatment:** Mitigate
- **Actions:**
  1. Implement immutable audit log: every prescription change (create, approve, refill, expire) logged with timestamp, actor, reason. Timeline: 3 weeks
  2. Implement digital signatures for prescription records (HMAC or PKI). Timeline: 2 weeks
  3. Implement integrity checks: periodic audit log validation to detect tampering. Timeline: 2 weeks
  4. Archive audit logs for [X] years (per healthcare standards). Timeline: 2 weeks
- **Owner:** Database Architect / Security Engineer
- **Review date:** 2026-07-04
- **Success criteria:** Audit log operational; digital signatures verified; integrity checks passing

**R-019, R-023: Twilio Security & Account Suspension Risk**

- **Treatment:** Mitigate
- **Actions:**
  1. Conduct Twilio security assessment: request SOC 2 report, GDPR compliance documentation, incident history. Timeline: 1 week
  2. Implement SMS compliance monitoring: ensure all SMS reminders are compliant with AASB (Australian SMS Code, opt-in requirements). Timeline: 2 weeks
  3. Implement customer consent management: track patient opt-in/opt-out for reminders; honor requests. Timeline: 3 weeks
  4. Monitor Twilio abuse reports; respond immediately to any regulatory complaints. Timeline: ongoing
  5. Maintain DPA (see R-021) with breach notification clause. Timeline: 2 weeks (part of R-021)
- **Owner:** Legal / Compliance Lead / Product Lead
- **Review date:** 2026-06-04
- **Success criteria:** Twilio SOC 2 report obtained; consent management implemented; SMS compliance verified

**R-026: Regulatory Inquiry Response**

- **Treatment:** Mitigate
- **Actions:**
  1. Designate Privacy Officer as single point of contact for Privacy Commissioner inquiries. Timeline: 1 week
  2. Implement response SLA: acknowledge inquiry within 5 business days, provide substantive response within 20 days. Timeline: 1 week
  3. Maintain detailed records of all Privacy Commissioner correspondence. Timeline: ongoing
  4. Establish relationship with Privacy Commissioner (voluntary consultation). Timeline: 2 weeks
- **Owner:** GRC Lead / Privacy Officer
- **Review date:** 2026-06-04
- **Success criteria:** Privacy Officer designated; response procedures documented; preliminary contact with Privacy Commissioner

**R-028, R-029, R-030: Cost Management & Operational Resilience**

- **Treatment:** Mitigate
- **Actions:**
  1. Implement AWS billing alerts (monthly budget, warn at 80%, hard stop at 100%). Timeline: 1 week
  2. Implement Twilio SMS cost limits (warn if approaching limit, reject if exceeded). Timeline: 1 week
  3. Implement cost monitoring dashboard (AWS Cost Explorer, Twilio usage analytics). Timeline: 2 weeks
  4. Quarterly cost review: identify optimization opportunities (e.g., reserved instances, SMS batching). Timeline: ongoing
  5. Implement operational cost tracking per business metric (cost per prescription, cost per reminder sent). Timeline: 2 weeks
- **Owner:** DevOps Lead / Finance Lead
- **Review date:** 2026-06-04 (then quarterly)
- **Success criteria:** Cost alerts operational; cost dashboard live; first optimization completed

---

### Medium Residual Risks — Monitoring & Planned Mitigation

**R-003: GDPR Applicability**

- **Treatment:** Clarify scope, then mitigate if applicable
- **Actions:**
  1. Document patient geography: are any patients EU-based? Are any healthcare providers EU-based? Timeline: 1 week
  2. Document third-party integrations: any data shared with EU-based systems? Timeline: 1 week
  3. If GDPR applies: engage GDPR specialist; implement additional controls (Data Protection Impact Assessment, legal basis documentation, consent mechanisms). Timeline: 4 weeks
  4. If GDPR does not apply: document decision and reasoning. Timeline: 1 week
- **Owner:** GRC Lead / Legal
- **Review date:** 2026-06-04 (scope clarification)
- **Success criteria:** Patient/provider geography documented; GDPR applicability determined; control plan (if applicable) in place

**R-006: SMS Regulatory Compliance (AASB)**

- **Treatment:** Mitigate
- **Actions:**
  1. Review AASB Australian SMS Code (anti-spam, opt-in, unsubscribe mechanisms). Timeline: 1 week
  2. Implement opt-in mechanism: patients explicitly consent to medication reminders. Timeline: 2 weeks
  3. Implement unsubscribe mechanism: "Reply STOP" to cease reminders; honor within 24 hours. Timeline: 2 weeks
  4. Audit SMS content: no promotional content, only prescription reminders. Timeline: 1 week
  5. Maintain opt-in/opt-out records (audit trail of consent changes). Timeline: 1 week
- **Owner:** Product Lead / Compliance Lead
- **Review date:** 2026-06-04
- **Success criteria:** Opt-in/opt-out mechanism operational; AASB compliance verified; audit trail maintained

**R-016: SMS Encryption & Logging**

- **Treatment:** Mitigate
- **Actions:**
  1. Verify Twilio API enforcement of TLS 1.2+. Timeline: 1 week
  2. Implement application-level logging restrictions: don't log full phone numbers in application logs (log last 4 digits only). Timeline: 2 weeks
  3. Implement log encryption: logs containing sensitive data encrypted at rest. Timeline: 2 weeks
  4. Implement log retention policy: operational logs retained for 30 days, audit logs for 7 years. Timeline: 2 weeks
- **Owner:** DevOps Lead / Security Engineer
- **Review date:** 2026-06-04
- **Success criteria:** TLS verification complete; log redaction implemented; log encryption deployed

**R-022: Vendor Lock-In**

- **Treatment:** Monitor (accept vendor lock-in as strategic trade-off; revisit annually)
- **Actions:**
  1. Document vendor dependencies: AWS RDS features used, Twilio SMS API patterns. Timeline: 1 week
  2. Maintain database schema documentation (portable to other databases if needed). Timeline: 2 weeks
  3. Maintain Twilio API abstraction layer (loose coupling; can swap SMS provider without major refactor). Timeline: 3 weeks
  4. Annual review (each May): assess new providers, evaluate switching cost. Timeline: ongoing
- **Owner:** Architecture Lead
- **Review date:** 2027-05-04 (annual review)
- **Success criteria:** Dependencies documented; abstraction layer in place; switching cost estimated

---

## Step 7: Risk Register Compilation

```markdown
# Risk Assessment: Prescribe (Telehealth Prescription Management System)

## Scope
- **Subject:** Prescribe — telehealth prescription management system
- **Boundaries:** Patient data storage, prescription processing, SMS reminder delivery, AWS RDS database, authentication/access control
- **Exclusions:** Third-party healthcare provider systems, physical pharmacy operations, patient device security
- **Time horizon:** Immediate (0-3 months), medium-term (3-12 months), ongoing
- **Stakeholders:** Patients (AU/NZ), healthcare providers, regulatory bodies (OAIC, NZ Privacy Commissioner), Twilio/AWS
- **Assessment date:** 2026-05-04
- **Assessor:** GRC Lead

---

## Risk Register: Critical Risks (Immediate Action Required)

### R-001: Australian Privacy Act Non-Compliance

- **Category:** Regulatory
- **Description:** Prescribe stores patient medication history and personal data without documented Privacy Act compliance framework. Australian Privacy Principles (APPs 1, 3, 5, 6, 12, 13) not implemented. No Privacy Policy. No mechanism to handle data access requests, corrections, or complaints.
- **Likelihood:** Very High (85%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:** 
  1. Hire Privacy Officer (external consultant or internal). Timeline: 2 weeks
  2. Conduct Privacy Impact Assessment (PIA). Timeline: 4 weeks
  3. Draft and publish Privacy Policy (APPs 1, 5, 6, 12, 13 compliant). Timeline: 3 weeks
  4. Implement Privacy Principles compliance controls (documented procedures for collection, use, disclosure, access, correction, deletion). Timeline: 8 weeks
  5. Quarterly compliance audits. Timeline: ongoing
- **Owner:** Privacy Officer (to be hired)
- **Review date:** 2026-08-04 (then quarterly)

---

### R-002: New Zealand Privacy Act Non-Compliance

- **Category:** Regulatory
- **Description:** Prescribe operates in NZ but no evidence of NZ Privacy Act 2020 compliance. Different principles and enforcement regime than Australia. No NZ-specific Privacy Policy or data handling procedures.
- **Likelihood:** High (65%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Engage NZ Privacy Act specialist. Timeline: 2 weeks
  2. Determine dual-jurisdiction requirements and conflicts (Australia vs NZ principles). Timeline: 2 weeks
  3. Amend Privacy Policy to cover both jurisdictions with jurisdiction-specific appendices. Timeline: 3 weeks
  4. Implement NZ-specific controls (e.g., NZ Privacy Commissioner notification process). Timeline: 4 weeks
- **Owner:** Privacy Officer (international compliance consultant)
- **Review date:** 2026-08-04

---

### R-004: Notifiable Data Breaches — No Process

- **Category:** Regulatory
- **Description:** Australian Privacy Act s.33ZE and NZ Privacy Act require breach notification within 30 days. No documented breach detection, investigation, or notification process. When (not if) a breach occurs, Prescribe will be unable to meet legal deadline.
- **Likelihood:** High (70%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Document breach response plan: detection → investigation → notification → remediation. Timeline: 2 weeks
  2. Implement breach notification template (meets legal requirements: affected parties, regulators, timeline). Timeline: 1 week
  3. Establish escalation process and roles (incident commander, Privacy Officer, legal counsel). Timeline: 1 week
  4. Conduct tabletop incident simulation (data breach scenario; test notification timeline). Timeline: 1 week
  5. Test breach detection alerting (database access anomalies, unusual data exports). Timeline: 2 weeks
- **Owner:** GRC Lead / Incident Commander
- **Review date:** 2026-06-04 (after plan publication and tabletop)

---

### R-005: Health Records Act Non-Compliance (if applicable)

- **Category:** Regulatory
- **Description:** If Prescribe qualifies as a healthcare provider, Australian Health Records Act 1988 or NZ Health Information Privacy Code applies. Stricter standards than general Privacy Act. No evidence of assessment or compliance.
- **Likelihood:** High (60%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Legal assessment: does Prescribe qualify as "healthcare provider" under Health Records Act? Timeline: 1 week
  2. If yes: engage healthcare compliance specialist. Timeline: 2 weeks
  3. Implement Health Records Act compliance controls (additional to Privacy Act). Timeline: 6 weeks
  4. If no: document decision and reasoning. Timeline: 1 week
- **Owner:** Privacy Officer / Legal Counsel
- **Review date:** 2026-06-04 (scope determination)

---

### R-010: Repeat Prescription Workflow — No Documentation

- **Category:** Operational
- **Description:** Process for repeat prescription approval not documented. Unclear whether automatic refills are permitted, whether expiry checks exist, whether pharmacist/doctor approval is required. Risk of unauthorized refills, expired prescriptions, or prescription errors causing patient harm.
- **Likelihood:** Very High (80%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Document current repeat prescription process (as-is). Timeline: 1 week
  2. Identify gaps and legal/medical requirements. Timeline: 2 weeks
  3. Implement approval workflow: patient request → doctor validation → prescription issued. Timeline: 6 weeks
  4. Implement automated expiry checks (no refills after expiry date). Timeline: 3 weeks
  5. Implement audit trail (all prescription approvals/denials logged). Timeline: 2 weeks
  6. Pilot test with sample patient group before full rollout. Timeline: 2 weeks
- **Owner:** Product Lead / Pharmacist Consultant
- **Review date:** 2026-06-04 (after documentation and initial testing)

---

### R-011: SMS Delivery Failures — Silent Failures

- **Category:** Operational / Patient Safety
- **Description:** No SMS delivery logging or monitoring. Patients may believe medication reminders sent when delivery actually failed. Silent failures mean patients miss medication schedules without visibility to system.
- **Likelihood:** Very High (85%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Implement SMS delivery logging via Twilio webhooks. Capture: sent time, delivery status, failure reason, retry count. Timeline: 2 weeks
  2. Set up alerting for delivery failures (>5% failure rate). Timeline: 1 week
  3. Implement patient notification on delivery failure (email/in-app alert if SMS failed). Timeline: 2 weeks
  4. Implement SMS retry logic (exponential backoff, max 3 retries over 24 hours). Timeline: 2 weeks
- **Owner:** DevOps Lead / Product Lead
- **Review date:** 2026-06-04 (after implementation and testing)

---

### R-012: Incident Response Plan — Missing

- **Category:** Operational
- **Description:** No documented incident response plan, escalation procedures, or communication templates. Healthcare system requires rapid, coordinated response to incidents (data breaches, outages, medication errors). Absence of plan means chaotic, ad-hoc response under pressure.
- **Likelihood:** Very High (90%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Document incident response plan: roles (incident commander, Privacy Officer, legal), escalation paths, notification timeline. Timeline: 2 weeks
  2. Create incident communication templates (internal alert, patient notification, regulator notification). Timeline: 1 week
  3. Define severity levels (SEV-1 = patient harm, SEV-2 = data exposure, SEV-3 = operational degradation). Timeline: 1 week
  4. Establish incident war room process (real-time updates, decision log, post-incident review). Timeline: 1 week
  5. Conduct tabletop incident simulation (test plan, roles, timelines). Timeline: 1 week
  6. Publish plan to all team members; annual refresher training. Timeline: 1 week
- **Owner:** GRC Lead / Engineering Manager
- **Review date:** 2026-06-04 (after tabletop completion)

---

### R-013: Database Encryption — Not Documented

- **Category:** Data / Security
- **Description:** Patient medication histories stored in AWS RDS. No evidence of encryption at rest or in transit. Patient data is high-value target for attackers. Unencrypted database accessible to anyone with network access or credentials.
- **Likelihood:** Very High (80%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented (may exist but unverified)
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Verify current RDS encryption state (AWS console). If not enabled: enable AES-256 encryption at rest. Timeline: 1 week
  2. Verify TLS 1.2+ enforced for all database connections. Timeline: 1 week
  3. Implement application-level encryption for highly sensitive fields (medications list) using envelope encryption (master key in AWS KMS). Timeline: 4 weeks
  4. Rotate database passwords and enforce strong policies (12+ chars, complex). Timeline: 1 week
  5. Verify backups encrypted; ensure future backups encrypted. Timeline: 1 week
  6. Test encryption end-to-end (decrypt records to verify no data loss). Timeline: 1 week
- **Owner:** DevOps Lead / Database Admin
- **Review date:** 2026-05-18 (verify encryption enabled)

---

### R-017: Access Control (RBAC) — Not Implemented

- **Category:** Data / Security
- **Description:** No documented role-based access control (RBAC). Unclear who can access patient records, whether least-privilege enforced, whether audit logging exists. Risk of unauthorized data access by insiders or compromised accounts.
- **Likelihood:** Very High (80%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Define roles: Admin (full access), Doctor (can approve prescriptions, view own patients), Pharmacist (can view prescriptions for fulfillment), Patient (view own records), Support (limited access for troubleshooting). Timeline: 1 week
  2. Implement role-based permissions (database-level and application-level). Timeline: 3 weeks
  3. Implement audit logging: log all access attempts (successful and failed) with timestamp, user, action, data accessed. Timeline: 2 weeks
  4. Implement least-privilege database access: application role can only SELECT/INSERT/UPDATE/DELETE; no ALTER/DROP. Timeline: 2 weeks
  5. Implement session timeout (30-60 minutes) and re-authentication for sensitive operations (e.g., prescription approval). Timeline: 2 weeks
  6. Quarterly access reviews: audit who has access to what; revoke access for leavers. Timeline: ongoing
- **Owner:** DevOps Lead / Security Engineer
- **Review date:** 2026-06-04 (after implementation)

---

### R-020: AWS RDS Misconfiguration — Security

- **Category:** Vendor / Security
- **Description:** AWS RDS configuration not documented or verified. Common misconfigurations: database publicly accessible, IAM policies too permissive, security groups allow all traffic. If database is publicly accessible, attackers can attempt direct connection and access all patient records.
- **Likelihood:** Very High (85%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Conduct AWS RDS security audit: check if publicly accessible, VPC/security group settings, IAM policies. Timeline: 1 week
  2. Ensure database NOT publicly accessible; restrict to application VPC only. Timeline: 1 week
  3. Implement IAM policies: principle of least privilege. Application role can only SELECT/INSERT/UPDATE/DELETE; no schema changes. Timeline: 2 weeks
  4. Implement security groups: allow traffic only from application servers (specific IPs/security groups). Timeline: 1 week
  5. Enable AWS RDS Enhanced Monitoring (CloudWatch metrics for CPU, memory, disk, network). Timeline: 1 week
  6. Enable AWS RDS Performance Insights (track slow queries, optimize). Timeline: 1 week
  7. Implement automated backups with multi-region replication (backup to secondary region). Timeline: 2 weeks
  8. Document AWS security configuration in runbook. Timeline: 1 week
- **Owner:** DevOps Lead / AWS Architect
- **Review date:** 2026-05-18 (verify configuration immediately)

---

### R-021: No Data Processing Agreement (DPA) with Twilio

- **Category:** Vendor / Regulatory
- **Description:** Twilio is a data processor (handles patient phone numbers). Without DPA, Prescribe is non-compliant with Privacy Act (if GDPR applies, mandatory DPA under Article 28). No contractual obligation for Twilio to notify Prescribe of breaches. No safeguards on Twilio's sub-processors.
- **Likelihood:** Very High (90%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Contact Twilio account manager to request Data Processing Agreement. Timeline: 1 week
  2. If standard DPA unavailable: negotiate custom DPA covering data handling, sub-processor approval, breach notification, compliance with Privacy Act/GDPR. Timeline: 2 weeks
  3. Review DPA with legal counsel; sign before further SMS operations. Timeline: 1 week
  4. Request Twilio security certifications (SOC 2 Type II, GDPR compliance documentation). Timeline: 1 week
  5. If GDPR applies: ensure Twilio is EU-certified or has Standard Contractual Clauses (SCCs). Timeline: ongoing
  6. Maintain record of DPA and security certifications. Timeline: ongoing
- **Owner:** Legal / Procurement Lead
- **Review date:** 2026-05-18 (DPA signature deadline)

---

## Risk Register: High Residual Risks (Planned Mitigation 8 weeks)

### R-003: GDPR Applicability Unclear

- **Category:** Regulatory
- **Description:** GDPR may apply if patients/providers are EU-based or data shared with EU systems. No assessment done. If applicable and controls missing, fines up to €20M or 4% of turnover.
- **Likelihood:** Medium (30%)
- **Impact:** Critical
- **Inherent risk:** High
- **Current controls:** None
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Clarify, then mitigate if applicable
- **Treatment detail:**
  1. Document patient geography: are any patients/providers EU-based? Timeline: 1 week
  2. Document third-party integrations: any data shared with EU systems? Timeline: 1 week
  3. Determine GDPR applicability. Timeline: 1 week
  4. If GDPR applies: conduct DPIA (Data Protection Impact Assessment); implement additional controls (consent, legal basis, data subject rights). Timeline: 4 weeks
  5. If GDPR does not apply: document decision with reasoning. Timeline: 1 week
- **Owner:** GRC Lead / Legal
- **Review date:** 2026-06-04

---

### R-006: SMS Regulatory Compliance (AASB Code)

- **Category:** Regulatory / Vendor
- **Description:** Australian SMS Code requires opt-in, anti-spam safeguards, unsubscribe mechanism. No evidence of compliance. Unsolicited or non-compliant SMS could trigger regulatory complaints and Twilio account suspension.
- **Likelihood:** Medium (35%)
- **Impact:** Medium
- **Inherent risk:** Medium
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Medium
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Review AASB Australian SMS Code requirements. Timeline: 1 week
  2. Implement opt-in mechanism: patients explicitly consent to medication reminders. Timeline: 2 weeks
  3. Implement unsubscribe: "Reply STOP" to cease reminders; honor within 24 hours. Timeline: 2 weeks
  4. Audit SMS content: only prescription reminders, no promotional content. Timeline: 1 week
  5. Maintain opt-in/opt-out audit trail (consent records). Timeline: 1 week
- **Owner:** Product Lead / Compliance Lead
- **Review date:** 2026-06-04

---

### R-007: AWS Region Failover — No DR Plan

- **Category:** Operational
- **Description:** Database in AWS Sydney (ap-southeast-2) only. No multi-region failover. If Sydney region experiences outage (2023 outage lasted hours), all operations unavailable. Patients cannot refill prescriptions; no SMS reminders sent.
- **Likelihood:** High (60%)
- **Impact:** Critical
- **Inherent risk:** Critical
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** Critical
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Implement multi-region replication: replicate RDS to ap-southeast-1 (Melbourne) or ap-northeast-1 (Tokyo). Timeline: 6 weeks
  2. Implement Route 53 health checks: if Sydney down, failover to secondary region automatically. Timeline: 3 weeks
  3. Test failover quarterly (simulate region failure). Timeline: ongoing
  4. Document failover runbook (timing, steps, communication plan). Timeline: 2 weeks
  5. Maintain secondary region costs in budget (replica database costs $X/month). Timeline: ongoing
- **Owner:** DevOps Lead / AWS Architect
- **Review date:** 2026-07-04

---

### R-008: Twilio Outage — No Fallback Provider

- **Category:** Vendor / Operational
- **Description:** SMS reminders depend entirely on Twilio. If Twilio down, no reminders sent. Patients miss medication schedules. No fallback SMS provider documented.
- **Likelihood:** Medium (40%)
- **Impact:** High
- **Inherent risk:** High
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Implement retry logic for SMS delivery: exponential backoff, max 3 retries over 24 hours. Timeline: 2 weeks
  2. Implement queue persistence: if SMS fails, persist message for retry (don't lose). Timeline: 2 weeks
  3. Implement fallback SMS provider: AWS SNS or Vonage as backup if Twilio unavailable. Timeline: 4 weeks
  4. Monitor Twilio SLA; publish status page for patients (shows "Reminders temporarily unavailable"). Timeline: 2 weeks
- **Owner:** DevOps Lead / Product Lead
- **Review date:** 2026-07-04

---

### R-009: Key Person Dependency

- **Category:** Operational
- **Description:** Critical systems (prescription workflow, database schema, deployment process) understood by one or few people. Unplanned absence creates risk of system failure with no one able to respond.
- **Likelihood:** High (65%)
- **Impact:** High
- **Inherent risk:** High
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Document all critical systems: prescription workflow, database schema, deployment process, emergency procedures. Timeline: 3 weeks
  2. Cross-train second person on each critical area. Timeline: 4 weeks
  3. Create runbooks for emergency procedures (database restore, SMS restart, prescription recovery). Timeline: 2 weeks
  4. Quarterly knowledge transfer reviews (each person explains system to another). Timeline: ongoing
  5. Maintain runbooks in accessible wiki (not personal documents). Timeline: ongoing
- **Owner:** Engineering Manager
- **Review date:** 2026-06-04

---

### R-014: Data Minimisation — Over-Collection

- **Category:** Data
- **Description:** Unclear what patient data is collected. Likely collecting more than necessary (e.g., address if only SMS needed; medical history if only current medications needed). Privacy Act expects data minimisation.
- **Likelihood:** High (70%)
- **Impact:** Medium
- **Inherent risk:** High
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Conduct data inventory: audit all patient data collected. Timeline: 2 weeks
  2. Assess necessity: which data strictly required for prescriptions? Which optional? Timeline: 2 weeks
  3. Implement data minimisation: remove unnecessary data collection; default to minimal set. Timeline: 3 weeks
  4. Update Privacy Policy to reflect data minimisation. Timeline: 1 week
- **Owner:** Data Architect / Privacy Officer
- **Review date:** 2026-07-04

---

### R-015: Data Retention — Indefinite Storage

- **Category:** Data
- **Description:** No documented data retention policy. Patient medication histories stored indefinitely. Deleted records may persist in backups without secure erasure. Violates Privacy Act principle of data minimisation.
- **Likelihood:** Very High (85%)
- **Impact:** Medium
- **Inherent risk:** High
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Implement retention policy: medication history retained for X years (per healthcare standards, e.g., 7-10 years). Timeline: 2 weeks
  2. Implement automated deletion jobs: deleted records securely erased from all backups (not just marked deleted). Timeline: 3 weeks
  3. Implement GDPR right-to-erasure mechanism (if GDPR applies). Timeline: 2 weeks
  4. Document retention policy in Privacy Policy. Timeline: 1 week
  5. Test deletion jobs quarterly (verify data actually deleted). Timeline: ongoing
- **Owner:** Data Architect / Privacy Officer
- **Review date:** 2026-07-04

---

### R-018: Prescription Audit Trail — No Integrity Checks

- **Category:** Data / Operational
- **Description:** No audit trail for prescription changes. No way to detect if records tampered with. Prescription records are safety-critical; undetected tampering could cause patient harm.
- **Likelihood:** High (65%)
- **Impact:** High
- **Inherent risk:** High
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Implement immutable audit log: every prescription change (create, approve, refill, expire) logged with timestamp, actor, reason. Timeline: 3 weeks
  2. Implement digital signatures for prescription records (HMAC or PKI). Timeline: 2 weeks
  3. Implement integrity checks: periodic audit log validation to detect tampering. Timeline: 2 weeks
  4. Archive audit logs for X years (per healthcare standards). Timeline: 2 weeks
  5. Test integrity checks quarterly (simulate tampering; verify detection). Timeline: ongoing
- **Owner:** Database Architect / Security Engineer
- **Review date:** 2026-07-04

---

### R-019: Twilio Security Posture Unknown

- **Category:** Vendor
- **Description:** Twilio is data processor (handles patient phone numbers). No assessment of Twilio's security, compliance certifications, or incident history. Twilio could be compromised, exposing patient data.
- **Likelihood:** High (70%)
- **Impact:** High
- **Inherent risk:** High
- **Current controls:** DPA (in progress, R-021); assumes Twilio is secure (unverified)
- **Control effectiveness:** Partial
- **Residual risk:** High
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Request Twilio SOC 2 Type II report (independent security audit). Timeline: 1 week
  2. Request GDPR compliance documentation (if GDPR applies). Timeline: 1 week
  3. Request incident history (any past breaches? Remediation?). Timeline: 1 week
  4. Review and document security findings. Timeline: 1 week
  5. Maintain updated security documentation in compliance file. Timeline: ongoing
- **Owner:** Security Engineer / GRC Lead
- **Review date:** 2026-06-04

---

### R-023: Twilio Account Suspension Risk

- **Category:** Vendor / Operational
- **Description:** Twilio account could be suspended for regulatory violations (e.g., unsolicited SMS, spam complaints). If suspended, Prescribe cannot send any reminders. Patients unable to receive medication reminders.
- **Likelihood:** Medium (40%)
- **Impact:** Critical
- **Inherent risk:** High
- **Current controls:** Assumed compliance (R-006 planned mitigation); DPA (R-021 planned mitigation)
- **Control effectiveness:** Partial
- **Residual risk:** High
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Implement SMS compliance monitoring: audit all SMS reminders for compliance with AASB code. Timeline: 2 weeks
  2. Maintain customer consent records (opt-in/opt-out). Timeline: 2 weeks
  3. Monitor Twilio abuse reports; respond immediately to complaints. Timeline: ongoing
  4. Maintain DPA (R-021) with breach/suspension notification clause. Timeline: 2 weeks
  5. Have fallback SMS provider ready (R-008) in case Twilio suspended. Timeline: 4 weeks
- **Owner:** Compliance Lead / Product Lead
- **Review date:** 2026-06-04

---

### R-026: Privacy Commissioner Inquiry Response

- **Category:** Reputational / Regulatory
- **Description:** Privacy Commissioner may investigate complaints. Poor response or record-keeping suggests negligence; increases regulatory penalties.
- **Likelihood:** High (65%)
- **Impact:** High
- **Inherent risk:** High
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Designate Privacy Officer as single point of contact for Privacy Commissioner. Timeline: 1 week
  2. Implement response SLA: acknowledge within 5 business days; provide substantive response within 20 days. Timeline: 1 week
  3. Maintain detailed records of all Privacy Commissioner correspondence. Timeline: ongoing
  4. Establish voluntary relationship with Privacy Commissioner (early consultation on new features). Timeline: 2 weeks
- **Owner:** GRC Lead / Privacy Officer
- **Review date:** 2026-06-04

---

### R-028, R-029, R-030: Cost Management & Operational Resilience

- **Category:** Financial / Operational
- **Description:** AWS and Twilio costs not monitored. Uncontrolled costs possible (e.g., runaway SMS volume, inefficient queries). No budget alerts. Outages impact revenue (patient churn, refunds).
- **Likelihood:** High (65%)
- **Impact:** Medium / High
- **Inherent risk:** High
- **Current controls:** None documented
- **Control effectiveness:** None
- **Residual risk:** High
- **Treatment:** Mitigate
- **Treatment detail:**
  1. Implement AWS billing alerts (monthly budget, warn at 80%, hard stop at 100%). Timeline: 1 week
  2. Implement Twilio SMS cost limits (warn if approaching, reject if exceeded). Timeline: 1 week
  3. Implement cost monitoring dashboard (AWS Cost Explorer, Twilio analytics). Timeline: 2 weeks
  4. Quarterly cost review: identify optimization opportunities. Timeline: ongoing
  5. Track operational cost per business metric (cost per prescription, cost per reminder). Timeline: 2 weeks
- **Owner:** DevOps Lead / Finance Lead
- **Review date:** 2026-06-04 (then quarterly)

---

## Risk Summary

| Risk | Category | Inherent | Residual | Treatment | Owner |
|---|---|---|---|---|---|
| R-001 | Regulatory | Critical | Critical | Mitigate | Privacy Officer |
| R-002 | Regulatory | Critical | Critical | Mitigate | Privacy Officer |
| R-003 | Regulatory | High | High | Clarify, then mitigate | GRC Lead / Legal |
| R-004 | Regulatory | Critical | Critical | Mitigate | GRC Lead |
| R-005 | Regulatory | Critical | Critical | Mitigate | Privacy Officer / Legal |
| R-006 | Regulatory | Medium | Medium | Mitigate | Compliance Lead |
| R-007 | Operational | Critical | Critical | Mitigate | DevOps Lead |
| R-008 | Operational | High | High | Mitigate | DevOps Lead |
| R-009 | Operational | High | High | Mitigate | Engineering Manager |
| R-010 | Operational | Critical | Critical | Mitigate | Product Lead |
| R-011 | Operational | Critical | Critical | Mitigate | DevOps Lead |
| R-012 | Operational | Critical | Critical | Mitigate | GRC Lead |
| R-013 | Data | Critical | Critical | Mitigate | DevOps Lead |
| R-014 | Data | High | High | Mitigate | Data Architect |
| R-015 | Data | High | High | Mitigate | Data Architect |
| R-016 | Data | Medium | Medium | Mitigate | DevOps Lead |
| R-017 | Data | Critical | Critical | Mitigate | DevOps Lead |
| R-018 | Data | High | High | Mitigate | Database Architect |
| R-019 | Vendor | High | High | Mitigate | Security Engineer |
| R-020 | Vendor | Critical | Critical | Mitigate | DevOps Lead |
| R-021 | Vendor | Critical | Critical | Mitigate | Legal Lead |
| R-022 | Vendor | Medium | Medium | Monitor | Architecture Lead |
| R-023 | Vendor | High | High | Mitigate | Compliance Lead |
| R-024 | Reputational | Critical | Critical | Mitigate | GRC Lead |
| R-025 | Reputational | Critical | Critical | Mitigate | GRC Lead |
| R-026 | Reputational | High | High | Mitigate | GRC Lead |
| R-027 | Financial | Critical | Critical | Mitigate | GRC Lead |
| R-028 | Financial | High | High | Mitigate | Finance Lead |
| R-029 | Financial | High | High | Mitigate | DevOps Lead |
| R-030 | Financial | High | High | Mitigate | Finance Lead |

---

## Prioritised Actions

### Phase 1: Critical — Immediate (Next 2 weeks)

These risks directly expose Prescribe to regulatory action, patient harm, or complete system failure. **Do not proceed with feature development until these are addressed.**

1. **R-020: Verify AWS RDS Security** — conduct immediate security audit; ensure database not publicly accessible
2. **R-013: Enable Database Encryption** — enable AES-256 at rest, TLS in transit
3. **R-004: Establish Breach Notification Process** — document steps and timeline (30 days required by law)
4. **R-021: Engage Twilio on DPA** — start DPA negotiation; maintain SMS provider contact
5. **Hire Privacy Officer** — external consultant or internal role; required for all regulatory work

### Phase 2: High — Planned (Weeks 3-8)

6. **R-001/R-002: Regulatory Compliance** — Privacy Impact Assessment, Privacy Policy (Australia + NZ), Privacy Principles implementation
7. **R-005: Health Records Act Assessment** — determine if applicable; implement if yes
8. **R-010: Repeat Prescription Workflow** — document, design, implement with expiry checks and audit trail
9. **R-011: SMS Delivery Logging & Alerting** — implement delivery tracking and failure notifications
10. **R-012: Incident Response Plan** — document plan, roles, escalation, conduct tabletop
11. **R-017: Role-Based Access Control (RBAC)** — implement roles (Doctor, Pharmacist, Patient, Admin) and least-privilege
12. **R-007: Multi-Region Failover** — replicate database to secondary region; implement automated failover

### Phase 3: Medium — Planned (Weeks 8-12)

13. **R-008: SMS Fallback Provider** — integrate secondary SMS provider
14. **R-014/R-015: Data Minimisation & Retention** — conduct data inventory, implement deletion jobs
15. **R-018: Audit Trail & Integrity** — implement immutable audit log and digital signatures
16. **R-009: Knowledge Transfer & Documentation** — document critical systems, cross-train teams
17. **R-030: Cost Monitoring** — implement billing alerts and cost dashboard

### Phase 4: Monitoring (Ongoing)

18. **R-022: Vendor Lock-In** — monitor new providers, estimate switching costs (annual review)
19. **R-026: Privacy Commissioner Relationship** — establish point of contact, maintain compliance records

---

## Review Schedule

- **Critical risks:** Weekly review of progress. Any blocker escalated immediately.
- **High risks:** Bi-weekly review.
- **Medium risks:** Monthly review.
- **Overall risk register:** Quarterly review (2026-08-04, 2026-11-04, 2027-02-04). Update triggers: regulatory changes, major system changes, incidents.

---

## Red Flags (Immediate Escalation Required)

- Any patient complaint or incident related to prescriptions
- Any inquiry from Privacy Commissioner or OAIC
- AWS region outage affecting Prescribe service
- Twilio account suspension or service degradation
- Data breach detected
- Staff member with access departing without handover

```

---

## Summary

**Prescribe has 30 identified risks across regulatory, operational, data, vendor, reputational, and financial domains.**

**Critical findings:**
- **12 Critical residual risks** requiring immediate mitigation (next 2 weeks)
- **18 High residual risks** requiring planned mitigation (next 8 weeks)
- **Zero documented controls** — system built without compliance framework
- **Cannot operate legally** without Privacy Act compliance; current state exposes Prescribe to regulatory fines up to AUD $50M

**Minimum viable actions (before accepting new patients):**
1. Hire Privacy Officer
2. Conduct Privacy Impact Assessment
3. Verify database encryption and access controls
4. Establish breach notification process
5. Sign Data Processing Agreement with Twilio
6. Document repeat prescription workflow with expiry checks and audit trail

**This assessment should trigger an immediate governance review with leadership. Recommend pausing new feature development until Critical risks are mitigated.**

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/19.5 (90%) |
| Evaluated | 2026-05-04 |
| Target duration | 152170 ms |
| Target cost | $0.1254 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 defines scope boundaries explicitly — what is in and out, time horizon, and affected stakeholders | PASS | Step 1 names subject (Prescribe), lists in-scope boundaries (patient data storage, prescription processing, SMS delivery, AWS RDS, auth/access control), explicit exclusions (third-party GP/pharmacy systems, physical pharmacy ops, patient devices), time horizon (0-3 months, 3-12 months, ongoing), and stakeholders (Patients AU/NZ, healthcare providers, Prescribe operators, OAIC, NZ Privacy Commissioner, Twilio/AWS). |
| c2 | Risk identification covers all seven categories — including Regulatory, AI/ML (even if N/A), Data, Operational, Financial, Reputational, and Vendor | PASS | Output explicitly labels seven sections: Regulatory Risks (R-001–R-006), Operational Risks (R-007–R-012), Data Risks (R-013–R-018), Vendor/Third-Party Risks (R-019–R-023), Reputational Risks (R-024–R-026), Financial Risks (R-027–R-030), and AI/ML Risks (R-031 — 'Not identified — system description does not mention AI/ML components'). |
| c3 | Every identified risk has a unique ID, a likelihood level with a percentage estimate, and an impact level | PASS | Step 3 risk analysis table assigns each risk R-001 through R-030 a unique ID, a verbal likelihood label with percentage in parentheses (e.g. 'Very High (85%)', 'Medium (30%)'), and an impact level (Critical/High/Medium). R-031 is acknowledged as N/A rather than a scored risk. |
| c4 | Inherent risk scores are derived from the matrix — not assigned arbitrarily | PASS | Inherent risk ratings follow a consistent pattern: Very High × Critical = Critical (R-001, R-010, R-013); Medium × Critical = High (R-003, R-023); Medium × Medium = Medium (R-006, R-016, R-022); High × Medium = High (R-014). The derivation is logically coherent and accompanied by rationale text, not arbitrary assignment. |
| c5 | Existing controls are documented per risk — not just assumed present | PASS | Step 4 'Existing Controls Assessment' table explicitly lists twelve control categories and marks each '❌ Missing' or '⚠️ Unclear'. The risk register in Step 7 repeats 'Current controls: None documented' per risk. Controls are explicitly examined and found absent — not assumed to exist. |
| c6 | Residual risk is calculated after controls, not just inheriting the inherent score | PASS | Step 5 opens: 'Because zero controls are documented and verified, residual risk = inherent risk for all items. Every control that should exist is absent.' The output explicitly performs the calculation and explains why residual equals inherent — this is a reasoned result, not a lazy default. |
| c7 | Every risk has a treatment decision (Accept/Mitigate/Transfer/Avoid) with specific detail | PASS | Step 6 and the Risk Register assign treatment to every risk: nearly all are 'Mitigate' with numbered action steps and timelines; R-003 is 'Clarify, then mitigate if applicable'; R-022 is 'Monitor (accept vendor lock-in as strategic trade-off)'. Each treatment entry includes specific numbered actions, owners, and review dates. |
| c8 | Accepted risks have an owner, a justification, and a review date (max 6 months) | PARTIAL | R-022 (Vendor Lock-In) is the only accepted/monitored risk. It has an owner (Architecture Lead) and justification ('strategic risk, not immediate'). However, the review date is 2027-05-04 — exactly 12 months from assessment date 2026-05-04 — which exceeds the 6-month maximum the criterion requires. |
| c9 | Output is compiled into the risk register format with a summary table and prioritised action list | PASS | Step 7 contains a full risk register with individual entries per risk (likelihood, impact, inherent, controls, residual, treatment, owner, review date), a 'Risk Summary' table listing all 30 risks with category/inherent/residual/treatment/owner columns, and a 'Prioritised Actions' section with four numbered phases. |
| c10 | Identifies Twilio as a vendor risk and AWS RDS as a data residency and availability risk | PARTIAL | Twilio is clearly identified as a vendor risk across R-019, R-021, R-023. AWS RDS availability risk is well covered in R-007 and R-020. However, AWS ap-southeast-2 is not explicitly framed as a data residency regulatory choice for AU+NZ data sovereignty — the output treats the region only as an availability concern, not a compliance consideration for where patient data must legally reside. |
| c11 | Output's scope section names Prescribe, the in-scope subsystems (prescription store, repeat-prescription processor, SMS reminder service), the time horizon (e.g. 12 months), and the affected stakeholders (patients in AU/NZ, prescribers, pharmacy partners, regulators) | PASS | Step 1 names Prescribe, lists Patient data storage (prescription store), prescription processing logic (repeat-prescription processor), and SMS reminder delivery via Twilio (SMS reminder service). Time horizon is '0-3 months, 3-12 months, ongoing'. Stakeholders include patients (AU/NZ), healthcare providers (prescribers), and regulatory bodies (OAIC, NZ Privacy Commissioner). Pharmacy partners are implicitly included via 'healthcare providers' though not named separately. |
| c12 | Output identifies risks in all seven categories with at least one risk per category — Regulatory (Privacy Act / Health Records / TGA), AI/ML (N/A noted explicitly if no ML), Data (PHI breach, ID disclosure), Operational (SMS delivery failure on critical reminder), Financial, Reputational, Vendor (Twilio, AWS) | PASS | All seven categories have at least one risk: Regulatory (R-001–R-006 including Privacy Act and Health Records Act); AI/ML (R-031 explicitly noted as N/A); Data (R-013–R-018 including PHI and ID risks); Operational (R-011 specifically SMS delivery failures); Financial (R-027–R-030); Reputational (R-024–R-026); Vendor (R-019–R-023 covering Twilio and AWS). |
| c13 | Output assigns each risk a unique ID (e.g. R-001, R-002), a likelihood with a percentage estimate (e.g. "Medium ~25%"), and an impact level (Low / Medium / High / Critical) — not just verbal labels | PASS | Step 3 table assigns R-001 through R-030 unique IDs, likelihood as 'Very High (85%)', 'High (70%)', 'Medium (35%)', etc. (verbal label + percentage), and impact as Critical/High/Medium. All three elements are present on every scored risk. |
| c14 | Output's inherent risk scores are derived from a likelihood × impact matrix (e.g. 5×5) shown in the output — not assigned arbitrarily | FAIL | No likelihood × impact matrix (e.g. a 5×5 grid or heat map) is displayed anywhere in the output. The criterion explicitly requires the matrix to be 'shown in the output.' While the derivation is logically consistent, the supporting matrix table is absent. |
| c15 | Output documents existing controls per risk — e.g. for "patient data breach via SMS provider" the existing controls are "Twilio TLS in transit, signed DPA, no PHI in SMS body" — not assumed | PASS | Step 4 explicitly lists 12 control categories and marks each as '❌ Missing' or '⚠️ Unclear'. The risk register in Step 7 states 'Current controls: None documented' for each individual risk entry. Controls are explicitly examined — not assumed — and found to be absent across the board. |
| c16 | Output calculates residual risk per risk after the existing controls are applied, with a clear reduction shown (e.g. "Inherent: High, Residual: Medium after controls") | PASS | Step 5 table shows Inherent, Controls, Effectiveness, and Residual columns per risk. Step 5 preamble explains the calculation: 'zero controls are documented and verified, residual risk = inherent risk for all items.' Each risk register entry in Step 7 also states inherent and residual values. The calculation is applied per risk with explicit reasoning. |
| c17 | Output assigns a treatment decision (Accept / Mitigate / Transfer / Avoid) per risk with specifics — what mitigation will be added, what the transfer mechanism is (insurance), why an acceptance is reasonable | PASS | Every risk has a treatment decision: Mitigate (with numbered actions and timelines), Monitor/Accept (R-022 with justification), or Clarify-then-mitigate (R-003). R-024/R-025 treatment includes 'Implement insurance/professional indemnity for healthcare provider liability' as an action within Mitigate. All treatments are specific. |
| c18 | Output's accepted risks have a named owner, justification, and a review date with the rule that the date is no more than 6 months out | PARTIAL | R-022 is the only accepted/monitored risk. It has a named owner (Architecture Lead) and justification ('Accept vendor lock-in as strategic trade-off; revisit annually'). The review date is 2027-05-04, which is 12 months from the 2026-05-04 assessment date — double the permitted 6-month maximum. |
| c19 | Output addresses Twilio specifically as a vendor risk — DPA in place, breach notification clauses, TGA / Privacy Act-compliant data handling, dependency risk if Twilio outage prevents critical reminders | PASS | R-021 addresses DPA with Twilio and explicitly mentions 'breach notification' clause. R-019 covers Twilio security posture and Privacy Act-compliant data handling (no DPA = no obligation for Twilio to notify; Prescribe liable for Twilio's actions). R-008 and R-023 both cover the dependency risk: 'If Twilio down, no reminders sent. Patients miss medication schedules.' |
| c20 | Output addresses AWS RDS in ap-southeast-2 as a data residency choice (Australia + NZ) and a single-AZ vs multi-AZ availability decision, with the trade-offs surfaced | PARTIAL | R-007 names ap-southeast-2 and addresses regional availability: 'regional outage in Sydney affects all operations.' Treatment proposes multi-region replication to ap-southeast-1 or ap-northeast-1. However, ap-southeast-2 is never framed as a data residency regulatory choice for AU+NZ compliance, NZ data sovereignty is not discussed, and single-AZ vs multi-AZ within the same region is not addressed — the output jumps directly to multi-region without surfacing the simpler multi-AZ trade-off. |

### Notes

The output is a comprehensive, well-structured seven-step risk assessment that covers all required categories, assigns numeric likelihood percentages, documents controls (correctly finding none), and produces a detailed treatment plan with owners and phased timelines. The two most significant gaps are: (1) the likelihood × impact matrix is never displayed as a visual artefact — c14 explicitly requires it to be 'shown in the output,' and its absence is a clear fail; (2) the only accepted risk (R-022) carries a 12-month review date, directly violating the 6-month ceiling rule stated in c8 and c18. Minor gaps include the absence of explicit data residency framing for AWS ap-southeast-2 (regulatory angle for AU+NZ sovereignty) and no single-AZ vs multi-AZ discussion. Despite these shortcomings, the overall depth and rigour of the assessment is high — 30 risks across seven categories, all with IDs, likelihood percentages, impacts, residual calculations, and specific treatment actions — placing the output well above the PASS threshold at 89.7%.
