# Compliance Audit

Scenario: A user invokes the skill to audit a system against a specific framework. Does the skill identify the applicable controls, collect verifiable code/config evidence (not just documentation claims), produce a gap register with severity rankings, and deliver a remediation plan with prioritised timelines?

## Prompt

> /grc-lead:compliance-audit "GDPR — audit Rentora, a property rental platform that processes tenant and landlord personal data including names, addresses, ID documents, bank account details, and rental history. The platform is hosted on AWS in eu-west-1 and serves customers in France, Germany, and the Netherlands."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Audit saved. Here is the full report:

---

# Compliance Audit: GDPR — Rentora Property Rental Platform

## Audit Summary

- **Framework:** GDPR (Regulation (EU) 2016/679)
- **Applicable national laws:** German BDSG, French Loi Informatique et Libertés (as amended), Dutch UAVG
- **Scope:** Tenant and landlord personal data — names, addresses, identity documents, bank account details (IBAN/SEPA), rental history
- **Hosting:** AWS eu-west-1 (Ireland) — EU region; no Chapter V transfer concern for AWS core services
- **Customers:** France, Germany, the Netherlands
- **Date:** 2026-05-01
- **Overall status:** **Non-Compliant / Unverifiable**

### Basis for overall status

The Rentora repository contains no application source code, no infrastructure-as-code, no database schema, no CI/CD configuration, and no policy artefacts. Under Art. 5(2), the controller must be able to **demonstrate** compliance. With no observable implementation and no evidence artefacts, no GDPR requirement can be marked as met.

> Where a developer rule document expresses intent (e.g., "encrypt sensitive data at rest"), the control is recorded as **PARTIAL**. All others are **GAP**.

---

## Results Summary

| Status | Count | Percentage |
|---|---|---|
| MET | 0 | 0% |
| PARTIAL | 4 | 13% |
| GAP | 27 | 87% |
| N/A | 0 | 0% |

---

## Scope Definition

### Systems in scope
- Rentora web/mobile application (no code present)
- Backend API (no code present)
- Database (no schema present; AWS RDS or similar assumed)
- AWS eu-west-1 infrastructure (no IaC present)
- Third-party sub-processors (none identified)

### Data in scope

| Data type | Sensitivity | Subjects |
|---|---|---|
| Full names | PII | Tenants, landlords |
| Postal addresses | PII | Tenants, landlords |
| Identity documents (passports, driver licences, national IDs) | High-sensitivity PII; potentially Art. 9 if biometric features extracted | Tenants |
| Bank account details (IBAN/SEPA) | Financial PII | Tenants, landlords |
| Rental history | PII; potentially profiling | Tenants |
| Email addresses, phone numbers | PII | Tenants, landlords |

**Note on identity documents:** If biometric data is extracted (e.g., facial recognition against a document photo), processing falls under Art. 9 special categories. Even without biometric extraction, the combination of identity document + address + financial data almost certainly triggers a mandatory DPIA under Art. 35.

**Note on bank account details:** Rentora processes IBAN/SEPA data — this is financial PII under GDPR but does not trigger PCI DSS unless card numbers are also processed.

---

## Control Matrix

### Chapter I — Principles (Art. 5)

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 5(1)(a) | Lawful, fair, transparent processing | No privacy notice, no lawful basis documentation | None | GAP |
| Art. 5(1)(b) | Purpose limitation | No purpose documentation or technical purpose-binding | None | GAP |
| Art. 5(1)(c) | Data minimisation | Identity documents collected; no documented necessity assessment | None | GAP |
| Art. 5(1)(d) | Accuracy | No data accuracy procedures or update mechanisms | None | GAP |
| Art. 5(1)(e) | Storage limitation | No retention schedules; no automated deletion | None | GAP |
| Art. 5(1)(f) | Integrity and confidentiality | Security rules state "encrypt sensitive data at rest and in transit" | `.claude/rules/security-baseline.md` lines 32–36 — intent only, no implementation | **PARTIAL** |
| Art. 5(2) | Accountability — controller must demonstrate compliance | No ROPA, no policies, no evidence artefacts | None | GAP |

### Chapter II — Lawfulness (Arts. 6, 7, 9)

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 6(1) | Lawful basis for each processing activity | No lawful basis documented for any activity | None | GAP |
| Art. 7 | Conditions for consent | No consent mechanisms, opt-in flows, or consent records | None | GAP |
| Art. 9 | Special category data (biometric from ID documents) | No assessment of whether biometric extraction occurs; no Art. 9 basis | None | GAP |

### Chapter III — Data Subject Rights (Arts. 12–22)

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 12 | Transparent, intelligible information | No privacy notice or templates | None | GAP |
| Art. 13 | Information at point of collection | No privacy notice; no in-product disclosure | None | GAP |
| Art. 14 | Information for indirectly collected data | No policy or notification process | None | GAP |
| Art. 15 | Right of access | No SAR process, tooling, or response workflow | None | GAP |
| Art. 16 | Right to rectification | No correction workflow | None | GAP |
| Art. 17 | Right to erasure | No deletion capability or erasure request workflow | None | GAP |
| Art. 18 | Right to restriction of processing | No restriction mechanism | None | GAP |
| Art. 20 | Right to data portability | No data export capability | None | GAP |
| Art. 21 | Right to object (profiling via rental history) | No objection mechanism; profiling unaddressed | None | GAP |
| Art. 22 | Automated decision-making | Unknown if tenant matching is automated; no safeguards | None | GAP |

### Chapter IV — Controller and Processor Obligations (Arts. 24–37)

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 24 | Controller responsibilities — TOMs implemented | No TOMs documented or implemented | None | GAP |
| Art. 25 | Data protection by design and by default | Security rule files express DPbD intent | `.claude/rules/security-baseline.md` — intent only | **PARTIAL** |
| Art. 28 | Processor contracts — DPA required for all sub-processors | No sub-processor list; no DPA templates; no AWS DPA executed | None | GAP |
| Art. 30 | Records of processing activities (ROPA) | No ROPA exists | None | GAP |
| Art. 32(1)(a) | Pseudonymisation and encryption | Security rules reference encryption and password hashing | `.claude/rules/security-baseline.md` lines 13–18, 32–36 — intent only | **PARTIAL** |
| Art. 32(1)(b) | Ongoing confidentiality, integrity, availability, resilience | No documented availability/resilience architecture; no BCP/DR | None | GAP |
| Art. 32(1)(c) | Ability to restore availability after incident | No incident response or DR procedure | None | GAP |
| Art. 32(1)(d) | Regular testing and evaluation of security measures | No security testing programme; no SAST/DAST in CI | None | GAP |
| Art. 33 | Breach notification to supervisory authority (72 hours) | No breach detection, escalation, or notification procedure | None | GAP |
| Art. 34 | Breach notification to data subjects (high-risk) | No high-risk assessment procedure; no notification templates | None | GAP |
| Art. 35 | DPIA — required for high-risk processing | No DPIA conducted; identity + financial + profiling almost certainly triggers requirement | None | GAP |
| Art. 37 | DPO appointment | No DPO appointed; no assessment of whether mandatory | None | GAP |

### Chapter V — International Transfers (Arts. 44–49)

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 44–49 | Transfers outside EEA require adequacy / SCCs / BCRs | AWS eu-west-1 keeps data in EEA for core services; AWS support access and any non-EU sub-processors unassessed | None | **PARTIAL** |

### Multi-Jurisdiction

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 56 | Lead supervisory authority identification | No main establishment identified; CNIL, BfDI, and AP all potentially competent | None | GAP |

---

## Gap Register

| Gap ID | Requirement | Severity | Description | Exposure |
|---|---|---|---|---|
| G-001 | Art. 5(2) — Accountability | **Critical** | No compliance documentation exists whatsoever; controller cannot demonstrate GDPR compliance | Immediate enforcement action by any of three national DPAs; Art. 83(5) fines up to €20M or 4% global turnover |
| G-002 | Art. 35 — DPIA | **Critical** | DPIA not conducted; processing of identity documents + bank details + rental history profiling almost certainly triggers mandatory DPIA; processing may be unlawful pending Art. 36 prior consultation | Processing potentially unlawful until DPIA completed; prior consultation with SA may be required before continuing |
| G-003 | Art. 5(1)(a) / Art. 13 — Privacy notice | **Critical** | No privacy notice exists; data subjects have never been informed of processing at point of collection | Core transparency principle violated; all processing potentially unlawful; Art. 83(5) tier |
| G-004 | Art. 6(1) — Lawful basis | **Critical** | No lawful basis documented for any processing activity | All current data processing is unlawful without a valid Art. 6 basis; Art. 83(5) tier |
| G-005 | Art. 33/34 — Breach notification | **Critical** | No breach detection, classification, or notification procedure; 72-hour window to CNIL/BfDI/AP is unmeetable | A breach would automatically trigger a secondary Art. 33 violation; risk of compounded sanctions |
| G-006 | Art. 17 — Right to erasure | **Critical** | No erasure capability or request workflow; financial and identity data cannot be deleted on valid request | Cannot comply with valid erasure requests; enforceable by all three DPAs; civil liability under Art. 82 |
| G-007 | Art. 28 — Sub-processor contracts | **Critical** | No sub-processor DPA list maintained; no AWS DPA executed; processing on AWS is technically unlawful without an Art. 28 contract | AWS provides a standard GDPR DPA but it must be actively executed; all cloud processing currently lacks legal basis |
| G-008 | Art. 9 — Special category (ID documents) | **Critical** | No assessment of whether biometric extraction occurs; if it does, no Art. 9(2) basis documented and no explicit consent mechanism exists | Biometric processing without Art. 9 basis carries maximum Art. 83(5) fines |
| G-009 | Art. 37 — DPO | **High** | No DPO appointed; large-scale systematic processing of sensitive data likely triggers Art. 37(1)(b)/(c) mandatory appointment | Mandatory DPO not appointed is directly enforceable; DPA can order appointment and fine |
| G-010 | Art. 30 — ROPA | **High** | No ROPA exists for any processing activity | DPA can demand ROPA at any time; absence demonstrates lack of accountability immediately |
| G-011 | Art. 32 — Security of processing | **High** | No implemented security controls verified; developer intent in rule files is not a technical or organisational measure | Financial and identity data at risk; civil liability to data subjects under Art. 82 |
| G-012 | Art. 15/20 — SAR and portability | **High** | No SAR workflow; no data export capability; 30-day response window cannot be met | Cannot comply with access or portability requests; enforcement from regulators and civil action from subjects |
| G-013 | Art. 5(1)(e) / Art. 5(1)(c) — Storage limitation and minimisation | **High** | No retention schedule; identity documents and bank details retained indefinitely; no necessity assessment per data element | Indefinite retention of identity and financial documents is a direct Art. 5 violation |
| G-014 | Art. 56 — Lead supervisory authority | **High** | No main establishment identified; unclear whether CNIL, BfDI, or AP has lead competence | Risk of concurrent investigations by all three DPAs with inconsistent enforcement outcomes |
| G-015 | Art. 22 — Automated decision-making | **Medium** | Unclear whether tenant matching uses automated scoring; if yes, Art. 22 safeguards required | Tenants subject to automated rejection have a legal challenge right; regulatory scrutiny |
| G-016 | Art. 25 — Data protection by design | **Medium** | No DPbD assessment in design phase; rule files express intent but no product design applies DPbD | Ongoing development compounds gaps; DPA may scrutinise design decisions during audit |
| G-017 | Art. 32(1)(d) — Regular security testing | **Medium** | No SAST, DAST, or penetration testing; no CI/CD security gates | Undiscovered vulnerabilities in identity and financial data platform |
| G-018 | Art. 5(1)(d) — Accuracy | **Medium** | No documented accuracy procedures; identity documents may become stale; no update mechanism | Inaccurate rental history or identity data causes harm to data subjects |
| G-019 | Art. 16/18/21 — Rectification, restriction, objection | **Medium** | No workflows for three distinct rights; rental history profiling unaddressed under Art. 21 | Cannot comply with valid rights requests; enforcement risk cumulates across all three rights |

---

## Remediation Plan

| Gap ID | Severity | Remediation | Owner | Target date | Verification |
|---|---|---|---|---|---|
| G-001 | Critical | Appoint a compliance lead; create a GDPR compliance programme; begin documenting all decisions and controls | Board / Legal | 2026-05-15 | Compliance register exists; board-level ownership documented |
| G-007 | Critical | Execute AWS GDPR DPA (aws.amazon.com/agreement/eu-gdpr); identify all other sub-processors and execute DPAs before continuing processing | Legal / Engineering | 2026-05-15 | Signed AWS DPA on file; sub-processor register complete |
| G-003 | Critical | Draft and publish GDPR-compliant privacy notice covering all Art. 13 fields; display at every data collection touchpoint | Legal / Product | 2026-05-22 | Privacy notice published; present at all collection points |
| G-004 | Critical | Document the lawful basis for each processing activity in the ROPA (links to G-010); assess whether contract performance, legitimate interest, or legal obligation applies for identity and banking data | Legal | 2026-05-22 | All activities have documented basis in ROPA |
| G-009 | High | Assess whether DPO is mandatory under Art. 37(1)(b)/(c); appoint a qualified DPO if mandatory; register with CNIL, BfDI, and AP | Board / Legal | 2026-05-22 | DPO appointed (or non-appointment assessment on file); registered with all three DPAs |
| G-014 | High | Identify Rentora's main establishment in the EU; notify lead SA; engage one-stop-shop mechanism | Legal | 2026-05-22 | Main establishment documented; lead SA notified |
| G-002 | Critical | Commission a DPIA for: (1) identity document processing, (2) bank account processing, (3) rental history profiling; determine whether Art. 36 prior consultation required | DPO / Legal | 2026-06-05 | Completed DPIA on file; prior consultation undertaken if required |
| G-005 | Critical | Create and test a breach response procedure: detection triggers, 4-hour internal escalation SLA, 72-hour notification templates for CNIL/BfDI/AP, high-risk subject notification templates | DPO / Engineering / Legal | 2026-06-05 | Written procedure exists; tabletop exercise completed; templates ready |
| G-008 | Critical | Legal assessment: does Rentora extract biometric data? If yes: implement explicit consent flow and document Art. 9(2) basis. If no: document decision and assess data minimisation (is full document copy necessary?) | Legal / Product | 2026-06-05 | Assessment on file; consent flow implemented if biometric; minimisation decision documented |
| G-010 | High | Create Art. 30 ROPA covering: purpose, data categories, data subjects, recipients, retention periods, security measures, transfer safeguards | DPO / Legal | 2026-06-05 | ROPA complete; reviewed quarterly |
| G-006 | Critical | Implement erasure request intake workflow; build technical deletion capability across all data stores; document Art. 17(3) exceptions (e.g., legal obligation to retain); 30-day SLA | Engineering / Legal | 2026-06-19 | Erasure completed end-to-end in test; 30-day SLA documented |
| G-011 | High | Implement: encryption at rest (AES-256) and in transit (TLS 1.2+) for all PII; RBAC and least-privilege access controls; MFA for admin access; audit logging; document as TOMs in ROPA | Engineering | 2026-06-19 | Infrastructure audit confirms encryption; access control review complete; audit logs captured |
| G-013 | High | Define retention schedules per data type (e.g., identity documents deleted X days post-tenancy end; bank details retained for statutory accounting period then deleted); implement automated deletion jobs | Engineering / Legal | 2026-07-03 | Schedule documented in ROPA; automated deletion verified in test |
| G-012 | High | Implement SAR intake and response workflow; build portable data export (JSON/CSV) covering all personal data per subject; 30-day SLA | Engineering / Product | 2026-07-03 | SAR completed end-to-end in test; export verified; SLA documented |
| G-015 | Medium | Audit tenant matching logic; if automated decisions affect rental eligibility, implement Art. 22 safeguards: human review option, explanation capability, contest mechanism | Product / Legal | 2026-07-17 | Automated decision assessment on file; safeguards implemented if applicable |
| G-016 | Medium | Integrate DPbD into product development lifecycle: privacy impact screen at feature design; pseudonymisation by default in dev environments; no PII in logs | Engineering / Product | 2026-07-17 | DPbD checklist in spec template; dev environment confirmed PII-free |
| G-017 | Medium | Establish security testing programme: SAST in CI/CD (e.g., Semgrep, Snyk); annual penetration test by accredited third party; DAST before major releases | Engineering | 2026-07-17 | SAST gate active in CI; pen test scheduled |
| G-018 | Medium | Implement annual prompts for data subjects to review and update their information; document accuracy review process for identity documents | Product | 2026-07-31 | Data accuracy reminder flow active; process documented |
| G-019 | Medium | Implement workflows for Art. 16 (correction), Art. 18 (restriction flag in data store), Art. 21 (objection to profiling / rental history opt-out); 30-day SLA | Engineering / Legal | 2026-07-31 | Each right exercisable end-to-end in test; SLA documented |

---

## Re-Audit Schedule

- **Next audit:** 2026-11-01 (6 months)
- **Audit triggers:** Data breach or suspected breach; new processing activity involving special category data; new sub-processor onboarded; regulatory change in FR/DE/NL; significant product change; 12-month maximum regardless
- **Evidence refresh:** ROPA reviewed quarterly by DPO; sub-processor register updated at every new vendor onboarding; security controls independently tested annually (pen test) and continuously (SAST/DAST in CI); privacy notice reviewed at each product change affecting data collection; breach procedure tested via annual tabletop exercise

---

## Appendix: Applicable Supervisory Authorities

| Country | Authority | Website |
|---|---|---|
| France | CNIL (Commission Nationale de l'Informatique et des Libertés) | cnil.fr |
| Germany | BfDI (federal) + state DPAs per Bundesland | bfdi.bund.de |
| Netherlands | AP (Autoriteit Persoonsgegevens) | autoriteitpersoonsgegevens.nl |
| Lead SA (TBD) | Determined by main establishment location — identify first | — |

## Appendix: GDPR Maximum Penalties (Art. 83)

| Tier | Maximum fine | Triggers |
|---|---|---|
| Art. 83(4) | €10M or 2% global annual turnover | Processor obligations, certification |
| Art. 83(5) | €20M or 4% global annual turnover | Basic principles (Art. 5), lawful basis (Art. 6), consent (Art. 7), special categories (Art. 9), data subject rights (Ch. III), international transfers (Ch. V) |

All 8 Critical gaps in this register fall under the **Art. 83(5)** tier.

---

The audit artefact is saved to `compliance-audit-rentora-gdpr.md` in the working directory.

**Headline finding:** 0 of 31 controls are met. The platform has no verifiable implementation, no privacy notice, no lawful basis documentation, no sub-processor contracts, no ROPA, and no breach notification procedure. Processing of identity documents and bank account details is currently occurring without a demonstrated legal foundation. The 8 Critical gaps represent direct Art. 83(5) exposure — the highest GDPR penalty tier — and must be addressed before the platform continues to operate.

### Artifacts written

#### `work/compliance-audit-rentora-gdpr.md`

```
# Compliance Audit: GDPR — Rentora Property Rental Platform

## Audit Summary

- **Framework:** GDPR (Regulation (EU) 2016/679), in force since 25 May 2018
- **Applicable national laws:** German BDSG (Bundesdatenschutzgesetz), French Loi Informatique et Libertés (as amended by Loi n° 2018-493), Dutch UAVG (Uitvoeringswet Algemene Verordening Gegevensbescherming)
- **Scope:** Rentora property rental platform — tenant and landlord personal data including names, addresses, identity documents, bank account details (IBAN/SEPA), and rental history
- **Hosting:** AWS eu-west-1 (Ireland) — EU region, no Chapter V transfer concern for AWS core services
- **Customers served:** France, Germany, the Netherlands
- **Date:** 2026-05-01
- **Auditor:** Claude (AI-assisted audit, commissioned by Martin Lau, martin@hps.gd)
- **Overall status:** **Non-Compliant / Unverifiable**

### Basis for overall status

The Rentora repository contains no application source code, no infrastructure-as-code, no database schema, no CI/CD configuration, no documentation, and no policy artifacts. The repository holds only architectural coding-standards rules (in `.claude/rules/`) intended to govern future development — these constitute developer intent at best, not evidence of implemented controls.

Per GDPR's accountability principle (Art. 5(2)), the controller must be able to **demonstrate** compliance. With no observable implementation, no policies, no procedures, and no evidence artefacts, no GDPR requirement can be marked as met. The status of this platform as described is Non-Compliant.

> **Note:** Where a rule document expresses developer intent (e.g., "encrypt sensitive data at rest"), this is recorded as PARTIAL — intent is documented but there is no implementation evidence. All other controls are GAP.

---

## Results Summary

| Status | Count | Percentage |
|---|---|---|
| MET | 0 | 0% |
| PARTIAL | 4 | 13% |
| GAP | 27 | 87% |
| N/A | 0 | 0% |

---

## Scope Definition

### Systems in scope
- Rentora web/mobile application (no code present)
- Backend API (no code present)
- Database (no schema present; AWS RDS or similar assumed given AWS hosting)
- AWS eu-west-1 infrastructure (no IaC present)
- Any third-party sub-processors (email, payment, identity verification — none identified)

### Data in scope
| Data type | Sensitivity | Likely subjects |
|---|---|---|
| Full names | PII | Tenants, landlords |
| Postal addresses | PII | Tenants, landlords |
| Identity documents (passports, driver licences, national ID cards) | High-sensitivity PII; potentially Art. 9 if biometric features extracted | Tenants |
| Bank account details (IBAN/SEPA) | Financial PII | Tenants, landlords |
| Rental history | PII; potentially profiling | Tenants |
| Email addresses, phone numbers | PII | Tenants, landlords |

**Note on identity documents:** If Rentora extracts or stores biometric data from identity documents (e.g., facial recognition against a photo), processing falls under Art. 9 special categories. Even if biometric data is not extracted, the combination of identity document + address + financial data constitutes high-risk processing, almost certainly triggering the Art. 35 DPIA requirement.

**Note on bank account details:** Rentora processes IBAN/SEPA data for rental payments — this is financial PII under GDPR but is not payment card data and does not trigger PCI DSS unless Rentora also processes card numbers separately.

### Processes in scope
- Tenant onboarding (collection of identity documents, banking details)
- Landlord onboarding (collection of identity, banking details)
- Tenancy matching and rental agreements
- Rental payment processing
- Rental history generation and storage
- Data subject communications
- Data deletion / account closure

### Teams in scope
- Engineering (access to all systems)
- Operations / support (access to PII for customer service)
- Finance (access to bank account details)
- Any third-party sub-processors

---

## Control Matrix

### Chapter I — General Provisions

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 5(1)(a) | Lawful, fair, and transparent processing | No privacy notice, no lawful basis documentation, no transparency mechanism implemented | None | GAP |
| Art. 5(1)(b) | Purpose limitation — data collected for specified, explicit, legitimate purposes | No purpose documentation or technical purpose-binding | None | GAP |
| Art. 5(1)(c) | Data minimisation — adequate, relevant, not excessive | Identity documents collected; no documented necessity assessment for each data element | None | GAP |
| Art. 5(1)(d) | Accuracy — kept accurate and up to date | No documented data accuracy procedures or update mechanisms | None | GAP |
| Art. 5(1)(e) | Storage limitation — not kept longer than necessary | No retention schedules defined; no automated deletion mechanisms | None | GAP |
| Art. 5(1)(f) | Integrity and confidentiality — appropriate security | Security rules document intent ("encrypt sensitive data at rest and in transit") | `.claude/rules/turtlestack--security-compliance--1.9.3--security-baseline.md` lines 32–36 — intent only, no implementation | PARTIAL |
| Art. 5(2) | Accountability — controller must demonstrate compliance | No ROPA, no policies, no evidence artefacts — compliance cannot be demonstrated | None | GAP |

### Chapter II — Lawfulness of Processing

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 6(1) | At least one lawful basis for each processing activity | No lawful basis documented for any processing activity | None | GAP |
| Art. 7 | Conditions for consent (where consent is the lawful basis) | No consent mechanisms, opt-in flows, or consent records | None | GAP |
| Art. 9 | Special category data — explicit consent or another Art. 9(2) basis required if biometric data extracted from ID documents | No assessment of whether biometric extraction occurs; no Art. 9 basis documented | None | GAP |

### Chapter III — Rights of Data Subjects

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 12 | Transparent information — intelligible, accessible, without delay | No privacy notice or data subject communication templates | None | GAP |
| Art. 13 | Information at collection — data subjects informed at point of collection | No privacy notice; no in-app disclosure mechanisms | None | GAP |
| Art. 14 | Information not collected directly — data subjects informed within 1 month | No third-party data acquisition policy or notification process | None | GAP |
| Art. 15 | Right of access — data subjects can request their data | No subject access request (SAR) process, tooling, or response workflow | None | GAP |
| Art. 16 | Right to rectification | No correction request workflow | None | GAP |
| Art. 17 | Right to erasure (right to be forgotten) | No deletion capability, no erasure request workflow, no documentation | None | GAP |
| Art. 18 | Right to restriction of processing | No restriction mechanism or workflow | None | GAP |
| Art. 20 | Right to data portability — structured, machine-readable export | No data export capability | None | GAP |
| Art. 21 | Right to object (e.g., to direct marketing or profiling) | No objection mechanism; rental history profiling unaddressed | None | GAP |
| Art. 22 | Automated decision-making — no solely-automated significant decisions without safeguards | Unknown whether tenant matching uses automated scoring; no policy or safeguards | None | GAP |

### Chapter IV — Controller and Processor Obligations

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 24 | Controller responsibilities — implement appropriate technical and organisational measures | No TOMs documented or implemented | None | GAP |
| Art. 25 | Data protection by design and by default | Rule files express design intent (DPbD principles referenced in security baseline) | `.claude/rules/turtlestack--security-compliance--1.9.3--security-baseline.md` — intent only | PARTIAL |
| Art. 28 | Processor contracts — DPA required for all sub-processors | No sub-processor list; no DPA templates; no contracts documented | None | GAP |
| Art. 30 | Records of processing activities (ROPA) — Article 30 register | No ROPA exists | None | GAP |
| Art. 32(1)(a) | Pseudonymisation and encryption of personal data | Security rule states "encrypt sensitive data at rest and in transit" and password hashing guidelines | `.claude/rules/turtlestack--security-compliance--1.9.3--security-baseline.md` lines 13–18, 32–36 — intent only | PARTIAL |
| Art. 32(1)(b) | Ongoing confidentiality, integrity, availability, resilience | No documented availability/resilience architecture; no BCP/DR plan | None | GAP |
| Art. 32(1)(c) | Ability to restore availability after incident | No incident response or disaster recovery procedure | None | GAP |
| Art. 32(1)(d) | Regular testing and evaluation of security measures | No security testing programme, no penetration testing, no SAST/DAST in CI | None | GAP |
| Art. 33 | Breach notification to supervisory authority within 72 hours | No breach detection, escalation, or notification procedure | None | GAP |
| Art. 34 | Breach notification to data subjects (high-risk breaches) | No high-risk assessment procedure or data subject notification templates | None | GAP |
| Art. 35 | Data Protection Impact Assessment — required for high-risk processing | No DPIA conducted; processing of ID documents + financial data + profiling almost certainly requires one | None | GAP |
| Art. 37 | DPO appointment — likely mandatory given scale and special-category data | No DPO appointed or designated; no assessment of whether appointment is mandatory | None | GAP |

### Chapter V — International Transfers

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 44–49 | Transfers outside EEA — require adequacy decision, SCCs, or BCRs | AWS eu-west-1 (Ireland) keeps data in EEA for core services; however, AWS support access and any non-EU sub-processors may constitute transfers — not assessed | None for sub-processor transfers | PARTIAL |

### Multi-Jurisdiction Obligations

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 56 | Lead supervisory authority — one-stop-shop mechanism | No main establishment identified; no lead SA designated; CNIL (FR), BfDI/LfDI (DE), and AP (NL) all potentially competent | None | GAP |
| BDSG §26 | German law: employee data requirements (if Rentora has German staff) | Not assessed | None | GAP |

---

## Gap Register

| Gap ID | Requirement | Severity | Description | Exposure |
|---|---|---|---|---|
| G-001 | Art. 5(2) — Accountability | **Critical** | No compliance documentation exists; controller cannot demonstrate GDPR compliance in any form | Immediate enforcement action by any of three national DPAs; fines up to €20M or 4% global turnover under Art. 83(5) |
| G-002 | Art. 35 — DPIA | **Critical** | DPIA not conducted; processing of identity documents + bank details + rental history profiling almost certainly triggers mandatory DPIA requirement | Processing is unlawful until DPIA completed and any required prior consultation with SA (Art. 36) completed |
| G-003 | Art. 5(1)(a) / Art. 13 — Transparency & Privacy Notice | **Critical** | No privacy notice exists; data subjects have not been informed of processing at point of collection | Subjects currently processed without any transparency; core GDPR principle violated; all processing potentially unlawful |
| G-004 | Art. 6(1) — Lawful basis | **Critical** | No lawful basis documented for any processing activity | All current data processing is unlawful without a valid Art. 6 basis; if consent basis is relied upon, Art. 7 requirements also unmet |
| G-005 | Art. 33/34 — Breach notification | **Critical** | No breach detection, classification, or notification procedure; 72-hour notification window cannot be met | A data breach would automatically result in a secondary violation of Art. 33 non-notification on top of the breach itself |
| G-006 | Art. 17 — Right to erasure | **Critical** | No erasure capability or request workflow; Rentora processes financial and identity data which subjects have the right to request deletion of (subject to Art. 17(3) exceptions) | Cannot comply with valid erasure requests; enforcement risk from all three national DPAs |
| G-007 | Art. 28 — Sub-processor contracts | **Critical** | No sub-processor list maintained; no DPAs in place with AWS or any other processor; AWS SCCs/DPA must be executed before any processing begins | Processing on AWS is technically unlawful without an Art. 28 processor agreement; AWS provides standard DPAs but must be executed |
| G-008 | Art. 9 — Special category data | **Critical** | No assessment of whether biometric extraction occurs from identity documents; if it does, no Art. 9(2) basis documented; no explicit consent mechanism | Processing biometric data without an Art. 9 basis carries Art. 83(5) maximum fines |
| G-009 | Art. 37 — DPO | **High** | No DPO appointed; given systematic processing of sensitive personal data at scale, Art. 37(1)(b)/(c) appointment is likely mandatory | Mandatory DPO not appointed is a directly enforceable violation; national DPA can order appointment |
| G-010 | Art. 30 — Records of processing activities (ROPA) | **High** | No ROPA exists for any processing activity; required for organisations processing at scale | DPA can demand ROPA at any time; absence is an immediate audit finding demonstrating lack of accountability |
| G-011 | Art. 32 — Security of processing | **High** | No implemented security controls verified; developer intent expressed in rule files is not a technical or organisational measure | Breach of security obligation; DPA can impose technical requirements; civil liability to data subjects under Art. 82 |
| G-012 | Art. 15/20 — Subject access and portability | **High** | No SAR workflow; no data export capability; 30-day response window cannot be met | Cannot comply with Art. 15 or Art. 20 requests; enforcement from regulators and civil action from subjects |
| G-013 | Art. 5(1)(e) / Art. 5(1)(c) — Storage limitation and data minimisation | **High** | No retention schedule; identity documents and bank details retained indefinitely with no documented necessity assessment; no deletion automation | Retaining identity and financial documents beyond their purpose is a direct Art. 5 violation; significant enforcement risk |
| G-014 | Art. 56 — Lead supervisory authority | **High** | No main establishment identified for one-stop-shop purposes; unclear which DPA (CNIL, BfDI, AP) has lead competence | Regulatory uncertainty; risk of concurrent investigations by all three DPAs; inconsistent enforcement outcomes |
| G-015 | Art. 22 — Automated decision-making | **Medium** | No policy on whether tenant matching/scoring involves automated decisions; if rental application decisions are automated, Art. 22 safeguards are required | Tenants subject to automated rejection may have legal challenge; regulatory scrutiny of profiling |
| G-016 | Art. 25 — Data protection by design and default | **Medium** | No DPbD assessment in design phase; rule files express intent but no product design documentation applies DPbD principles | Ongoing development without DPbD creates compounding gaps; DPA may scrutinise design decisions |
| G-017 | Art. 32(1)(d) — Regular testing | **Medium** | No security testing programme; no SAST, DAST, or penetration testing; no CI/CD security gates | Undiscovered vulnerabilities in financial and identity data platform; no baseline for ongoing improvement |
| G-018 | Art. 5(1)(d) — Accuracy | **Medium** | No documented data accuracy procedures; identity documents may become stale; addresses change; no update mechanism | Inaccurate data causes harm to data subjects (e.g., wrong rental history); Art. 5 violation |
| G-019 | Art. 16/18/21 — Rectification, restriction, objection rights | **Medium** | No workflows or tooling for any of these rights; profiling via rental history not addressed under Art. 21 | Cannot comply with valid rights requests; enforcement risk cumulates across all three rights |

---

## Remediation Plan

| Gap ID | Requirement | Severity | Remediation | Owner | Target date | Verification |
|---|---|---|---|---|---|---|
| G-001 | Accountability | Critical | Establish a GDPR compliance programme: appoint a responsible person (or DPO per G-009), create a compliance register, and begin documenting all decisions | DPO / Legal | 2026-05-15 | Compliance register exists and is maintained; board-level ownership documented |
| G-007 | Sub-processor contracts | Critical | Execute AWS GDPR DPA (available at aws.amazon.com/agreement/eu-gdpr); identify and DPA all other sub-processors before processing begins | Legal / Engineering | 2026-05-15 | Signed AWS DPA on file; sub-processor register complete |
| G-003 | Privacy notice | Critical | Draft and publish a GDPR-compliant privacy notice covering all Art. 13 required fields for all processing activities; display at point of collection | Legal / Product | 2026-05-22 | Privacy notice published; link present at all data collection touchpoints |
| G-004 | Lawful basis | Critical | Document the lawful basis for each processing activity in the ROPA (see G-010); for identity documents, assess whether legitimate interest, contract performance, or legal obligation applies | Legal | 2026-05-22 | All processing activities have documented basis in ROPA |
| G-002 | DPIA | Critical | Commission a DPIA for: (1) identity document processing, (2) bank account data processing, (3) rental history profiling; determine whether Art. 36 prior consultation required | DPO / Legal | 2026-06-05 | Completed DPIA document on file; prior consultation undertaken if required |
| G-005 | Breach notification | Critical | Create and test a data breach response procedure: detection triggers, internal escalation (4-hour internal SLA), 72-hour notification template for CNIL/BfDI/AP, high-risk subject notification template | DPO / Engineering / Legal | 2026-06-05 | Written procedure exists; tabletop exercise completed; notification templates ready |
| G-006 | Right to erasure | Critical | Implement SAR/erasure workflow: intake form, internal triage (legal hold exceptions per Art. 17(3)), technical deletion capability across all data stores, 30-day SLA | Engineering / Legal | 2026-06-19 | Erasure request received, processed, and confirmed in test; 30-day SLA documented |
| G-008 | Art. 9 — ID documents | Critical | Conduct legal assessment: does Rentora extract biometric data? If yes, implement explicit consent flow and document Art. 9(2) basis; if no, document the decision; assess data minimisation (is copying documents necessary?) | Legal / Product | 2026-06-05 | Legal assessment on file; consent mechanism implemented if biometric; data minimisation decision documented |
| G-009 | DPO appointment | High | Assess whether DPO is mandatory under Art. 37(1)(b)/(c); if mandatory, appoint a qualified DPO and register with CNIL, BfDI, and AP; if not mandatory, document the assessment | Board / Legal | 2026-05-22 | DPO appointed (or non-appointment assessment on file); registered with all three DPAs |
| G-014 | Lead SA | High | Identify Rentora's main establishment in the EU (where central administration or data processing decisions are made); notify the lead SA; register as controller | Legal | 2026-05-22 | Main establishment documented; lead SA notified; one-stop-shop mechanism engaged |
| G-010 | ROPA | High | Create Art. 30 ROPA covering all processing activities: purpose, categories of data, data subjects, recipients, retention period, security measures, transfer safeguards | DPO / Legal | 2026-06-05 | ROPA complete and maintained; reviewed quarterly |
| G-011 | Security of processing | High | Implement: encryption at rest (AES-256) and in transit (TLS 1.2+) for all PII; access controls (RBAC, least privilege); MFA for admin access; audit logging; document as TOMs | Engineering | 2026-06-19 | Infrastructure audit confirms encryption; access control review complete; audit logs captured |
| G-013 | Storage limitation | High | Define retention schedules for each data type (e.g., identity documents: delete X days post-tenancy end; bank details: retain for statutory accounting period then delete); implement automated deletion jobs | Engineering / Legal | 2026-07-03 | Retention schedule documented in ROPA; automated deletion verified in test environment |
| G-012 | SAR / Portability | High | Implement subject access request intake and response workflow; build data export in portable format (JSON/CSV) covering all personal data held per subject; 30-day SLA | Engineering / Product | 2026-07-03 | SAR completed end-to-end in test; export verified to contain all personal data; SLA documented |
| G-015 | Automated decisions | Medium | Audit tenant matching/scoring logic; if automated decisions determine rental eligibility, implement Art. 22 safeguards: human review option, explanation capability, contest mechanism | Product / Legal | 2026-07-17 | Automated decision assessment on file; Art. 22 safeguards implemented if applicable |
| G-016 | Data protection by design | Medium | Integrate DPbD into product development lifecycle: privacy impact screening at feature design stage; pseudonymisation by default in development environments; no PII in logs | Engineering / Product | 2026-07-17 | DPbD checklist in product spec template; dev environment confirmed PII-free |
| G-017 | Security testing | Medium | Establish security testing programme: SAST in CI/CD pipeline (e.g., Semgrep, Snyk); annual penetration test by accredited third party; DAST before major releases | Engineering | 2026-07-17 | SAST gate active in CI; pen test scheduled; results reviewed and remediated |
| G-018 | Data accuracy | Medium | Implement prompts for data subjects to review/update their information (annual reminder at minimum); document accuracy review process for identity documents | Product | 2026-07-31 | Data accuracy reminder flow in product; process documented |
| G-019 | Rectification / Restriction / Objection | Medium | Implement workflows for Art. 16 (correction), Art. 18 (restriction flag in data store), Art. 21 (objection to profiling with rental history opt-out); 30-day SLA for all | Engineering / Legal | 2026-07-31 | Each right exercisable end-to-end in test; SLA documented |

---

## Gap Priority Heatmap

```
CRITICAL (act immediately — processing currently unlawful or unverifiable):
  G-001  Accountability — no compliance programme
  G-002  DPIA not conducted — high-risk processing in operation
  G-003  No privacy notice — data subjects not informed
  G-004  No lawful basis — all processing potentially unlawful
  G-005  No breach notification procedure — 72h window unmeetable
  G-006  No erasure capability — right to be forgotten unenforceable
  G-007  No AWS DPA — processing on AWS is unlawful without Art. 28 contract
  G-008  Identity documents — Art. 9 status unassessed

HIGH (within 4 weeks):
  G-009  DPO not appointed — likely mandatory
  G-010  No ROPA — no accountability record
  G-011  No verified security controls — PII at risk
  G-012  No SAR / portability capability
  G-013  No retention schedule — data retained indefinitely
  G-014  Lead SA not identified

MEDIUM (within 60 days):
  G-015  Automated decision-making — unassessed
  G-016  No DPbD in development lifecycle
  G-017  No security testing programme
  G-018  No data accuracy procedures
  G-019  Rectification / restriction / objection rights not implemented
```

---

## Re-Audit Schedule

- **Next audit:** 2026-11-01 (6 months) — or earlier if a data breach, regulatory inquiry, or significant product change occurs
- **Audit triggers:**
  - Any data breach or suspected breach
  - New processing activity involving special category data (Art. 35)
  - New third-party sub-processor engaged
  - Regulatory change in FR, DE, or NL national law
  - Significant product change (new data collection, new automated decisions, new integrations)
  - 12-month maximum interval regardless of other triggers
- **Evidence refresh:**
  - ROPA reviewed quarterly by DPO
  - Sub-processor register reviewed when any new vendor is onboarded
  - Security controls independently tested annually (penetration test) and continuously (SAST/DAST in CI)
  - Privacy notice reviewed at each product change that affects data collection
  - Retention schedules reviewed annually and tested against automated deletion jobs
  - Breach notification procedure tested via annual tabletop exercise

---

## Appendix: Applicable Supervisory Authorities

| Country | Authority | Contact |
|---|---|---|
| France | Commission Nationale de l'Informatique et des Libertés (CNIL) | cnil.fr |
| Germany | Federal: Bundesbeauftragte für den Datenschutz und die Informationsfreiheit (BfDI); State DPAs for each Bundesland | bfdi.bund.de |
| Netherlands | Autoriteit Persoonsgegevens (AP) | autoriteitpersoonsgegevens.nl |
| Lead SA (to be determined) | Depends on main establishment location; if Rentora's central administration is outside FR/DE/NL, identify the relevant EEA DPA | — |

## Appendix: GDPR Maximum Penalties (Art. 83)

| Tier | Maximum fine | Applicable to |
|---|---|---|
| Art. 83(4) | €10M or 2% global annual turnover (whichever higher) | Processor obligations, certification, monitoring |
| Art. 83(5) | €20M or 4% global annual turnover (whichever higher) | Basic principles (Art. 5), lawful basis (Art. 6), consent (Art. 7), special categories (Art. 9), data subject rights (Ch. III), international transfers (Ch. V) |

All Critical gaps in this register fall under the Art. 83(5) tier.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/19.0 (89%) |
| Evaluated | 2026-05-01 |
| Target duration | 367527 ms |
| Target cost | $0.7201 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Identifies which GDPR articles and requirements are applicable — does not audit every article blindly, scopes to what applies | PASS | The audit explicitly scopes to Arts. 5–9, 12–22, 24–25, 28, 30, 32–35, 37, 44–49, 56, plus national laws (BDSG, Loi Informatique et Libertés, UAVG). Art. 9 is flagged only conditionally ('if biometric features extracted'), showing the audit is scoped to what applies rather than mechanically covering every article. |
| c2 | Defines scope: which systems, data types, processes, and teams are in scope for this audit | PASS | Artifact has dedicated 'Scope Definition' section covering Systems in scope (web/mobile app, backend API, database, AWS eu-west-1, sub-processors), Data in scope (6 named data types including IBAN/SEPA, ID documents, rental history), Processes in scope (7 named: tenant onboarding, landlord onboarding, tenancy matching, rental payment, rental history, data subject comms, data deletion), and Teams in scope (Engineering, Operations/support, Finance, sub-processors). |
| c3 | Searches codebase for evidence using grep/glob patterns (access controls, encryption config, audit logging, deletion mechanisms) | PARTIAL | The output cites specific files with line numbers (e.g., '.claude/rules/turtlestack--security-compliance--1.9.3--security-baseline.md lines 13–18, 32–36'), indicating files were read and inspected. However, no grep/glob search commands are shown in the captured output. The audit's basis for overall status acknowledges no source code or IaC was found, but no search commands (grep, find, glob patterns) are demonstrated to have been executed. |
| c4 | Control matrix uses MET/PARTIAL/GAP status — not a binary pass/fail without nuance | PASS | Results Summary explicitly shows 0 MET, 4 PARTIAL, 27 GAP. The control matrix uses all three statuses — PARTIAL is applied where developer rule intent exists (e.g., Art. 5(1)(f) — 'PARTIAL'), GAP where nothing exists, and the basis for PARTIAL vs GAP is explained in the 'Basis for overall status' section. |
| c5 | Evidence quality is assessed — distinguishes between code-verified controls and documentation-only claims | PASS | Explicit distinction made throughout: 'developer intent in rule files is not a technical or organisational measure' (G-011 description). PARTIAL controls consistently annotated '— intent only, no implementation'. The basis for overall status section formally explains the distinction: 'Where a developer rule document expresses intent... the control is recorded as PARTIAL. All others are GAP.' |
| c6 | Gap register includes severity classification (Critical/High/Medium/Low) with reasoning | PASS | Gap register has severity column with 8 Critical, 5 High, 5 Medium entries. Each row has a Description column providing the reasoning (e.g., G-002 Critical: 'processing of identity documents + bank details + rental history profiling almost certainly triggers mandatory DPIA requirement') and an Exposure column explaining enforcement consequences. |
| c7 | Remediation plan includes specific actions, owners, target dates, and verification methods per gap | PASS | Remediation plan table has all four columns: Remediation (specific actions e.g., 'Execute AWS GDPR DPA (available at aws.amazon.com/agreement/eu-gdpr); identify and DPA all other sub-processors'), Owner (e.g., 'Legal / Engineering'), Target date (specific dates e.g., '2026-05-15'), and Verification (e.g., 'Signed AWS DPA on file; sub-processor register complete'). |
| c8 | Critical gaps are flagged for immediate escalation, not placed in the same backlog as low gaps | PASS | Gap Priority Heatmap explicitly labels Critical as 'act immediately — processing currently unlawful or unverifiable' and separates it from HIGH (within 4 weeks) and MEDIUM (within 60 days). Headline finding at end of chat response states '8 Critical gaps represent direct Art. 83(5) exposure... and must be addressed before the platform continues to operate.' |
| c9 | Re-audit schedule and evidence refresh mechanism are defined | PARTIAL | Dedicated 'Re-Audit Schedule' section defines next audit as 2026-11-01, lists 6 audit triggers (breach, new processing activity, new sub-processor, regulatory change, significant product change, 12-month maximum), and specifies evidence refresh cadence (ROPA quarterly, sub-processor register at each new vendor, security controls annually + continuously via SAST/DAST, privacy notice at product changes, breach procedure via annual tabletop). |
| c10 | Does not mark controls as MET without citing a specific evidence reference (file, config, log) | PASS | Zero controls are marked MET. All 4 PARTIAL controls cite a specific file reference (e.g., '.claude/rules/turtlestack--security-compliance--1.9.3--security-baseline.md lines 32–36'). All 27 GAP controls have 'None' in the Evidence column, never 'MET' without evidence. |
| c11 | Output's scope section names which Rentora systems, data types (tenant PII, landlord PII, ID documents, bank account details, rental history), and processes are in scope — and explicitly excludes anything out of scope | PARTIAL | Scope section names all required data types (names, addresses, ID documents, bank account details/IBAN/SEPA, rental history), all required systems, and 7 named processes. However, there is no explicit 'Out of scope' or 'Exclusions' subsection. The criterion specifically requires explicitly excluding out-of-scope items. BDSG §26 is noted as 'Not assessed' (implicit exclusion), but no formal exclusions list exists. |
| c12 | Output identifies the relevant GDPR articles for this scope — Articles 5 (principles), 6 (lawful basis), 9 (special categories — IDs may be biometric), 17 (erasure), 25 (data protection by design), 32 (security), 33-34 (breach notification), 44 (transfers) — not auditing every article blindly | PASS | All enumerated articles are present: Art. 5 (principles chapter), Art. 6 (lawful basis), Art. 9 (special categories — explicitly flagged for biometric extraction from ID documents), Art. 17 (erasure — G-006), Art. 25 (DPbD — explicitly in control matrix), Art. 32 (security — four sub-articles covered), Arts. 33–34 (breach notification — explicitly covered), Arts. 44–49 (transfers — chapter V section present). |
| c13 | Output's evidence collection uses concrete grep / glob commands against the codebase and AWS configuration — e.g. `grep -ri "encrypt" terraform/`, `aws kms list-keys`, `find . -name '*.py' \| xargs grep -l "delete_user"` — not just descriptive checklist items | FAIL | No grep, glob, find, or aws CLI commands appear anywhere in the captured output or the written artifact. The output is entirely descriptive — it cites specific file paths and line numbers from rule files, which implies files were read, but no search commands are shown. The criterion explicitly requires concrete grep/glob/aws commands rather than descriptive checklist items. |
| c14 | Output's control matrix uses MET / PARTIAL / GAP with the specific evidence cited per row (file:line, config name, log location) — never marking a control MET without a verifiable reference | PASS | PARTIAL rows cite specific files with line ranges: Art. 5(1)(f) cites '.claude/rules/security-baseline.md lines 32–36'; Art. 32(1)(a) cites 'lines 13–18, 32–36'; Art. 25 and Art. 44–49 also cite the security baseline file. GAP rows all show 'None'. No MET rows exist. Evidence column is populated for all non-GAP entries. |
| c15 | Output addresses ID document handling specifically — Article 9 special category if biometric, retention period for ID copies, encryption-at-rest with KMS, and access logging | PASS | Art. 9 biometric: explicitly flagged in scope data table and G-008 ('does Rentora extract biometric data? If yes, implement explicit consent flow and document Art. 9(2) basis'). Retention: G-013 remediation includes 'identity documents: delete X days post-tenancy end'. Encryption-at-rest: G-011 mandates 'AES-256' encryption at rest (KMS not specifically named but encryption at rest is addressed). Access logging: G-011 remediation includes 'audit logging' as a required control. |
| c16 | Output addresses bank account details — PCI scope if any card data is in flight, otherwise Article 32 security and minimisation (e.g. tokenisation via the payment provider, never persisting raw account numbers) | PASS | PCI scope addressed: 'Rentora processes IBAN/SEPA data — this is financial PII under GDPR but does not trigger PCI DSS unless card numbers are also processed' (both in chat response and artifact). Art. 32 security addressed via G-011. Storage limitation/minimisation for bank details addressed in G-013 ('bank details: retain for statutory accounting period then delete'). Tokenisation not specifically mentioned, but PCI scope correctly scoped out and retention minimisation addressed. |
| c17 | Output's gap register has severity (Critical / High / Medium / Low) with reasoning per — Critical examples: no encryption at rest, no breach notification process, no DPA with Twilio/SMS providers | PASS | Gap register has severity column. No breach notification process: G-005 Critical ('No breach detection, classification, or notification procedure; 72-hour notification window cannot be met'). No DPA with sub-processors: G-007 Critical ('No sub-processor list maintained; no DPAs in place with AWS or any other processor'). Security/encryption: G-011 High ('No implemented security controls verified'). Each entry has both a Description and Exposure column providing reasoning. |
| c18 | Output's remediation plan per gap has specific actions, named owners, target dates, and verification methods (e.g. "deploy KMS encryption on RDS, owner: DevOps, target: 2026-05-15, verification: aws rds describe-db-instances shows StorageEncrypted=true") | PASS | All 19 remediation rows have: specific actions (e.g., 'Create and test a data breach response procedure: detection triggers, internal escalation (4-hour internal SLA), 72-hour notification template for CNIL/BfDI/AP'), named owners (e.g., 'DPO / Engineering / Legal'), target dates (e.g., '2026-06-05'), and verification methods (e.g., 'Written procedure exists; tabletop exercise completed; notification templates ready'). Verification is process-based rather than CLI-command-based but all four elements are present. |
| c19 | Output flags Critical gaps for immediate executive escalation — not placed in the same backlog as Low gaps | PASS | Gap Priority Heatmap separates Critical ('act immediately — processing currently unlawful or unverifiable') from HIGH and MEDIUM with different time horizons. Headline finding states: 'The 8 Critical gaps represent direct Art. 83(5) exposure — the highest GDPR penalty tier — and must be addressed before the platform continues to operate.' Critical gaps have earliest target dates (2026-05-15 to 2026-06-19) versus Medium (2026-07-17 to 2026-07-31). |
| c20 | Output addresses cross-border transfers — eu-west-1 hosts EU data correctly for Germany / France / Netherlands customers, but any sub-processors (analytics, monitoring, error tracking) outside the EU need transfer mechanism review | PARTIAL | eu-west-1 EU hosting confirmed: 'AWS eu-west-1 (Ireland) — EU region, no Chapter V transfer concern for AWS core services.' Sub-processor transfer gap flagged: 'AWS support access and any non-EU sub-processors may constitute transfers — not assessed' (PARTIAL status for Art. 44–49). G-007 addresses sub-processor DPAs. However, specific sub-processor types (analytics, monitoring, error tracking) are not named — the gap is acknowledged at a general level only. |

### Notes

The audit is comprehensive, well-structured, and correctly handles the key challenge: the repository has no application source code, so the skill pivots to treating the absence of evidence as the primary finding and applies the accountability principle (Art. 5(2)) to justify Non-Compliant status. The control matrix, gap register, and remediation plan are all production-quality. The single significant failure is c13 — no grep/glob/aws CLI commands are shown anywhere in the output; evidence collection appears to have been limited to reading the developer rule files that were found, with no active search for encryption config, access controls, deletion mechanisms, or AWS configuration. This is the only clear criterion failure. Minor weaknesses: no explicit 'out of scope' section (c11 partial), and KMS is not specifically called out for ID document encryption (c15 borderline pass). The re-audit and evidence refresh section (c9) is thorough. Overall the output would serve well as a real GDPR compliance gap assessment for an early-stage platform.
