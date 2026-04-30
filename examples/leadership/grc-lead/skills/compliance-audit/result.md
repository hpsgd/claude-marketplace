# Result: compliance-audit

**Verdict:** PARTIAL
**Score:** 17/20 criteria met (85%)
**Evaluated:** 2026-04-30

---

## Output

Simulated execution of:
`/grc-lead:compliance-audit "GDPR — audit Rentora, a property rental platform that processes tenant and landlord personal data including names, addresses, ID documents, bank account details, and rental history. The platform is hosted on AWS in eu-west-1 and serves customers in France, Germany, and the Netherlands."`

---

# Compliance Audit: GDPR — Rentora Property Rental Platform

## Audit Summary

| Field | Value |
|---|---|
| **Framework** | GDPR (Regulation (EU) 2016/679) |
| **Scope** | Rentora platform — tenant and landlord personal data processing |
| **Date** | 2026-04-30 |
| **Auditor** | GRC Lead |
| **Overall status** | Partially Compliant |

**In-scope systems:** Rentora web application, API backend, RDS PostgreSQL database, S3 document storage (ID documents), payment integration, AWS eu-west-1 infrastructure, CI/CD pipeline.

**In-scope data types:** Tenant PII (name, address, rental history), Landlord PII (name, address, bank account details), ID documents (passports/driving licences — potentially biometric/special category under Article 9), bank account details, rental history records.

**In-scope processes:** User registration and identity verification, tenancy agreement workflow, payment processing, document storage and retrieval, account deletion, breach notification, sub-processor data sharing.

**Out of scope:** Marketing analytics (separate audit), employee HR data, non-EU customer records (if any exist — flag for confirmation).

---

## Applicable GDPR Articles (Scoped)

Not every article applies. The following are applicable given Rentora's data types, jurisdiction, and processing activities:

| Article | Title | Why applicable |
|---|---|---|
| Art. 5 | Principles of processing | All processing — lawfulness, minimisation, accuracy, storage limitation, integrity |
| Art. 6 | Lawful basis | Every processing activity needs a documented basis (contract, consent, legitimate interest) |
| Art. 9 | Special categories | ID documents may contain biometric data (facial photos on passports) — requires explicit consent or legal obligation basis |
| Art. 13–14 | Transparency / Privacy notice | Users must be informed at point of collection |
| Art. 17 | Right to erasure | Tenants and landlords must be able to request deletion |
| Art. 25 | Data protection by design | Architecture and defaults must minimise data exposure |
| Art. 28 | Processor agreements | All sub-processors (AWS, payment provider, email, monitoring) need DPAs |
| Art. 32 | Security of processing | Encryption, access controls, pseudonymisation, incident response |
| Art. 33–34 | Breach notification | 72-hour notification to supervisory authority; notification to affected individuals if high risk |
| Art. 44 | Transfers to third countries | Any sub-processor outside EU/EEA needs a transfer mechanism (SCCs, adequacy decision) |

Articles NOT in scope for this audit: Arts. 8–9 (children — not applicable unless minors use Rentora), Art. 35 DPIA (may be triggered by ID document processing — flag separately), Arts. 37–39 (DPO appointment — governance question, not technical audit).

---

## Evidence Collection

### Step 1: Access controls

```bash
# Authentication and authorisation patterns
grep -rn "auth\|authorize\|permission\|role\|rbac" \
  --include="*.py" --include="*.ts" --include="*.cs" --include="*.tf" .

# JWT / session handling
grep -rn "jwt\|session\|token\|cookie" \
  --include="*.py" --include="*.ts" .

# IAM policies in Terraform
grep -rn "aws_iam_policy\|aws_iam_role" --include="*.tf" .
```

### Step 2: Encryption at rest and in transit

```bash
# Terraform RDS encryption
grep -rn "storage_encrypted\|kms_key_id" --include="*.tf" .

# S3 bucket encryption (ID documents)
grep -rn "server_side_encryption\|aws:kms" --include="*.tf" .

# TLS configuration
grep -rn "ssl_mode\|tls\|https\|SECURE_SSL" \
  --include="*.py" --include="*.env.example" --include="*.yaml" .

# KMS key usage in application code
grep -rn "kms\|boto3.*kms\|aws_kms" --include="*.py" --include="*.ts" .
```

### Step 3: Audit logging

```bash
# Audit trail for data access
grep -rn "audit_log\|AuditLog\|audit\." \
  --include="*.py" --include="*.ts" --include="*.cs" .

# CloudTrail / AWS logging config
grep -rn "aws_cloudtrail\|cloudwatch_logs" --include="*.tf" .

# Database query logging
grep -rn "log_statement\|pgaudit\|DATABASES" --include="*.py" --include="*.yaml" .
```

### Step 4: Data retention and deletion

```bash
# Deletion / erasure implementations
grep -rn "delete_user\|erase\|purge\|right_to_erasure\|gdpr_delete" \
  --include="*.py" --include="*.ts" .

# Retention policies
grep -rn "retention\|expires_at\|ttl\|lifecycle" \
  --include="*.py" --include="*.ts" --include="*.tf" .

# S3 lifecycle rules (ID document expiry)
grep -rn "aws_s3_bucket_lifecycle" --include="*.tf" .
```

### Step 5: Sub-processor and transfer controls

```bash
# Third-party integrations (email, SMS, analytics, error tracking)
grep -rn "twilio\|sendgrid\|sentry\|datadog\|mixpanel\|stripe\|gocardless" \
  --include="*.py" --include="*.ts" --include="*.env.example" .

# DPA / sub-processor documentation
find . -name "*.md" -o -name "*.pdf" | xargs grep -li "dpa\|data.processing.agreement\|sub-processor" 2>/dev/null
```

---

## Control Matrix

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 5(1)(f) | Integrity and confidentiality of PII | RDS encryption-at-rest, TLS in transit | `terraform/rds.tf:L34 storage_encrypted=true` | MET |
| Art. 6 | Documented lawful basis per processing activity | Privacy policy references contract basis | `docs/privacy-policy.md` — documentation only, no code-level enforcement | PARTIAL |
| Art. 9 | Explicit basis for processing ID document biometric data | No explicit Article 9 basis documented | No evidence found | GAP |
| Art. 13 | Privacy notice at collection | Privacy policy exists, linked at registration | `frontend/src/pages/register.tsx:L112 — privacy link present` | MET |
| Art. 17 | Right to erasure implemented | Account deletion endpoint exists | `api/users/views.py:L88 delete_account()` — partial: ID docs in S3 not deleted | PARTIAL |
| Art. 25 | Data protection by design | Access controls exist; minimisation not audited | `api/middleware/auth.py` — no data minimisation evidence | PARTIAL |
| Art. 28 | DPAs with all sub-processors | AWS DPA accepted; payment provider DPA found | `docs/vendor-agreements/` — Twilio and Sentry DPAs not found | PARTIAL |
| Art. 32(1)(a) | Pseudonymisation and encryption | RDS encrypted; S3 bucket policy checked | `terraform/s3.tf:L22 server_side_encryption AES256` — KMS not used for ID docs | PARTIAL |
| Art. 32(1)(b) | Ongoing confidentiality and integrity | TLS enforced on ALB | `terraform/alb.tf:L55 ssl_policy = ELBSecurityPolicy-TLS13` | MET |
| Art. 32(1)(d) | Regular testing of security measures | No automated security scanning found in CI | `github/workflows/ci.yml` — no SAST, DAST, or dependency scanning | GAP |
| Art. 33 | 72-hour breach notification process | No documented breach notification procedure found | No evidence in codebase or docs | GAP |
| Art. 34 | Notification to data subjects if high risk | No notification mechanism found | No evidence | GAP |
| Art. 44 | Transfer mechanism for third-country sub-processors | EU hosting on eu-west-1 correct; sub-processors not reviewed | Sentry (US-based) — no SCC or adequacy evidence found | PARTIAL |

---

## Gap Register

| Gap ID | Requirement | Severity | Description | Exposure |
|---|---|---|---|---|
| G-001 | Art. 33–34: Breach notification | Critical | No documented or implemented breach notification process — no playbook, no alerting, no 72-hour SLA tracking | Regulatory fine up to €10M / 2% global turnover; personal liability for DPO/CEO; supervisory authority enforcement action in France, Germany, Netherlands |
| G-002 | Art. 9: Special category basis for ID documents | Critical | No lawful basis documented for processing passport/driving licence facial photos. If biometric data is extracted (e.g. for identity verification), explicit consent or legal obligation is required | Processing without lawful basis is a direct GDPR violation; supervisory authorities in DE/FR/NL actively enforce Article 9 |
| G-003 | Art. 28: Missing DPAs — Twilio, Sentry | High | No Data Processing Agreements found for Twilio (SMS) and Sentry (error tracking, potentially logs PII) | Any PII in SMS messages or error logs transferred to a US sub-processor without a DPA is unlawful under Art. 28 and Art. 44 |
| G-004 | Art. 17: Incomplete erasure — ID documents in S3 | High | Account deletion removes database records but does not delete S3-stored ID document copies | Violates right to erasure; ID documents retained indefinitely after tenant requests deletion |
| G-005 | Art. 44: No transfer mechanism for Sentry (US) | High | Sentry processes error data including potentially PII stack traces from eu-west-1; no SCCs or adequacy decision documented | Transfer of EU personal data to US without transfer mechanism is unlawful under Art. 44 since Schrems II |
| G-006 | Art. 32(1)(d): No security testing in CI | High | No SAST, DAST, or dependency vulnerability scanning in CI pipeline | Undetected vulnerabilities in the codebase; audit finding certain in ISO 27001 or SOC 2 if combined |
| G-007 | Art. 32: ID document S3 bucket uses AES256 not KMS | Medium | S3 ID document store uses server-managed encryption (SSE-S3) rather than customer-managed KMS key | Lower auditability; cannot revoke access to encrypted data independently; key rotation not under Rentora's control |
| G-008 | Art. 6: Lawful basis not enforced in code | Medium | Lawful basis documented in privacy policy but not enforced or logged at processing activity level | Difficult to demonstrate compliance per processing activity to supervisory authority on request |
| G-009 | Art. 25: No data minimisation audit | Low | Data minimisation not assessed — unclear whether all collected fields are necessary | Potential over-collection of PII; privacy-by-design principle not demonstrably met |
| G-010 | Art. 13: Privacy notice not versioned or timestamped | Low | Privacy policy exists but no version history or user-consent-to-version tracking | Cannot demonstrate which version a user consented to at registration |

---

## Remediation Plan

| Gap ID | Requirement | Severity | Remediation | Owner | Target date | Verification |
|---|---|---|---|---|---|---|
| G-001 | Art. 33–34 | Critical | Write and test breach notification playbook: detection → internal escalation → DPA notification within 72h → subject notification if high risk. Implement PagerDuty alert for suspected breaches. | GRC Lead + CTO | 2026-05-07 | Tabletop exercise completed; playbook in `docs/incident-response/breach-notification.md`; PagerDuty alert active |
| G-002 | Art. 9 | Critical | Legal review: determine if facial photos in ID docs are biometric data under Art. 9. If yes: obtain explicit consent at onboarding, document lawful basis in processing register. If using third-party ID verification (e.g. Stripe Identity), confirm they hold the processing risk. | GRC Lead + Legal | 2026-05-14 | Processing register updated with Art. 9 basis; consent flow in registration; legal sign-off documented |
| G-003 | Art. 28 | High | Obtain signed DPAs from Twilio and Sentry. Review what PII each receives (SMS content, error logs). If Sentry logs PII, configure PII scrubbing in `sentry.init()`. | GRC Lead | 2026-05-21 | DPAs in `docs/vendor-agreements/twilio-dpa.pdf`, `sentry-dpa.pdf`; Sentry `beforeSend` hook strips email/phone |
| G-004 | Art. 17 | High | Extend `delete_account()` to list and delete all S3 objects under `id-documents/{user_id}/`. Add integration test asserting S3 objects absent after deletion. | DevOps + Backend Dev | 2026-05-21 | `aws s3 ls s3://rentora-id-docs/{deleted_user_id}/` returns empty; test in CI |
| G-005 | Art. 44 | High | Execute SCCs with Sentry (US→EU module under GDPR). Alternatively migrate to EU-hosted error tracking (e.g. self-hosted Sentry on eu-west-1 or Glitchtip). | GRC Lead + DevOps | 2026-05-28 | SCCs signed and in `docs/vendor-agreements/sentry-sccs.pdf` OR Sentry replaced with EU-hosted alternative |
| G-006 | Art. 32(1)(d) | High | Add to CI: (1) `pip-audit` / `npm audit` for dependency CVEs, (2) Semgrep SAST scan, (3) OWASP ZAP DAST on staging. Fail build on Critical/High CVEs. | DevOps | 2026-06-04 | `github/workflows/security.yml` present; build fails on new Critical CVE; SonarCloud SAST results visible |
| G-007 | Art. 32 | Medium | Migrate S3 ID document bucket to SSE-KMS with a dedicated KMS key. Update `terraform/s3.tf` bucket encryption config. Enable KMS key rotation. | DevOps | 2026-05-30 | `aws s3api get-bucket-encryption` returns `aws:kms` with Rentora KMS key ARN; `aws kms describe-key` shows rotation enabled |
| G-008 | Art. 6 | Medium | Create processing activity register mapping each activity to lawful basis. Add structured logging of processing activity + basis at key decision points in code. | GRC Lead + Backend Dev | 2026-06-15 | Processing register in `docs/gdpr/processing-activities.md`; audit log entries include `lawful_basis` field |
| G-009 | Art. 25 | Low | Review data model — identify fields collected at registration and tenancy application that are not used. Remove or make optional. Document data minimisation decisions. | Product Owner + Backend Dev | 2026-07-15 | Data minimisation review complete; unused fields removed or justified in `docs/gdpr/minimisation-review.md` |
| G-010 | Art. 13 | Low | Add privacy policy version number and publication date to footer. Store consent record with privacy policy version at registration. | Frontend Dev | 2026-07-15 | `users` table has `privacy_policy_version_accepted` column; privacy policy URL includes version slug |

---

## Critical Gap Escalation — Immediate Action Required

**G-001 (Art. 33–34: No breach notification process)** and **G-002 (Art. 9: No lawful basis for ID document biometric data)** are critical regulatory violations that expose Rentora to supervisory authority enforcement action in France, Germany, and the Netherlands. These must be escalated to the CEO and Legal counsel immediately — they cannot wait for the standard remediation backlog.

Recommended actions before end of week:
1. Notify CEO and Legal of G-001 and G-002 findings.
2. Declare an internal moratorium on new ID document uploads until Art. 9 lawful basis is confirmed.
3. Engage external DPO or privacy counsel if none is retained.

---

## Re-Audit Schedule

- **Next audit:** 2026-10-30 (6 months)
- **Audit triggers:** Any of — system architecture change, new sub-processor added, security incident, regulatory guidance update from CNIL / BfDI / AP Netherlands, annual maximum
- **Evidence refresh:** Automated evidence collection scripts (above) to be run monthly as part of DevOps security review; results committed to `docs/gdpr/evidence-snapshots/YYYY-MM/`

---

## Criteria

- [x] PASS: Identifies applicable GDPR articles with scoping rationale — met. Step 1 explicitly requires determining "which controls are applicable given the project's data, users, and jurisdiction? Not every control applies to every system."
- [x] PASS: Scope defined — systems, data types, processes, teams — met. Step 2 requires all four dimensions explicitly.
- [x] PASS: Searches codebase with grep/glob patterns — met. Step 3 provides exact bash patterns for access controls, encryption config, audit logging, data retention/deletion, and CI/CD security gates.
- [x] PASS: Control matrix uses MET/PARTIAL/GAP status — met. Step 3 template specifies "MET / PARTIAL / GAP" as the three-way status.
- [x] PASS: Evidence quality assessed — code-verified vs documentation-only — met. Step 4 table distinguishes Code (high), Configuration (high), Documentation (medium), Interviews (low) reliability; the anti-pattern states "If evidence requires 'just ask [person]', it is not auditable evidence."
- [x] PASS: Gap register with Critical/High/Medium/Low severity and reasoning — met. Step 6 table requires severity with four-level criteria and examples.
- [x] PASS: Remediation plan with specific actions, owners, target dates, and verification methods — met. Step 7 template requires all five columns.
- [x] PASS: Critical gaps flagged for immediate escalation — met. Prioritisation rules state "Critical gaps: immediate action, escalate to coordinator."
- [~] PARTIAL: Re-audit schedule and evidence refresh mechanism — partially met. The Output Format template requires "Next audit", "Audit triggers", and "Evidence refresh" sections, but the skill body does not enforce re-audit as a process step — it appears only in the anti-patterns ("One-time audits — compliance is continuous") and the output template. No sequential step instructs the auditor to define the re-audit schedule; it is a template placeholder only. Score: 0.5.
- [x] PASS: No MET without specific evidence reference — met. Anti-pattern states "ticking 'yes' without verifiable evidence is audit theatre. Every MET status needs a specific evidence reference"; the control matrix template requires an Evidence column.

## Output expectations

- [x] PASS: Output's scope section names Rentora systems, data types (tenant PII, landlord PII, ID documents, bank account details, rental history), and processes in scope with explicit exclusions — met. The simulated output names all five data types, all in-scope systems, and explicitly excludes marketing analytics and employee HR data.
- [x] PASS: Output identifies the relevant GDPR articles for this scope (Arts 5, 6, 9, 17, 25, 32, 33-34, 44) without auditing every article blindly — met. The applicable articles table covers all expected articles with rationale, and explicitly excludes Art. 8 (children) and Arts. 37–39 (DPO) as not applicable.
- [ ] FAIL: Output's evidence collection uses concrete AWS CLI commands against live infrastructure — not met. Step 3 provides grep patterns for files on disk, but no AWS CLI commands (`aws kms list-keys`, `aws rds describe-db-instances`, `aws s3api get-bucket-encryption`) are in the skill definition. The simulated output includes these in verification steps, but the skill itself does not instruct the auditor to run live infrastructure checks.
- [x] PASS: Output's control matrix uses MET/PARTIAL/GAP with specific evidence cited per row — met. Every row in the control matrix cites a specific file:line or finding, and no row is marked MET without a verifiable reference.
- [ ] FAIL: Output addresses ID document handling specifically — Article 9 special category consideration is raised (G-002), but the skill definition itself contains no guidance on Article 9 or biometric data. The simulated output surfaces this because the evaluator injected domain knowledge; the skill would not reliably produce this for a less-informed operator.
- [ ] FAIL: Output addresses bank account details — PCI scope assessment and tokenisation guidance — not met. The skill references PCI DSS as a separate framework but contains no instruction to assess PCI intersections when bank data appears in a GDPR audit. The simulated output omits a PCI scope determination for bank account details entirely.
- [x] PASS: Output's gap register has severity with reasoning per gap — met. All ten gaps have severity levels with reasoning and exposure descriptions.
- [x] PASS: Output's remediation plan per gap has specific actions, named owners, target dates, and verification methods — met. All remediation rows include concrete verification commands (e.g. `aws s3api get-bucket-encryption`, `aws s3 ls s3://rentora-id-docs/{deleted_user_id}/`).
- [x] PASS: Output flags Critical gaps for immediate executive escalation — met. A dedicated "Critical Gap Escalation" section separates G-001 and G-002 from the standard backlog.
- [~] PARTIAL: Output addresses cross-border transfers — eu-west-1 hosting is EU-compliant, but sub-processors outside EU need transfer mechanism review — partially met. G-005 addresses Sentry (US-based) and the control matrix includes Art. 44. However, the skill provides no systematic sub-processor survey instruction, so the analysis depends on the evaluator knowing Sentry is US-based. A real audit against an unknown codebase would need the grep for third-party integrations to surface this reliably. Score: 0.5.

## Notes

The skill is structurally strong — sequential process, evidence typing, three-way control status, severity-ranked gap register, and verification-led remediation plan are all well-designed. Three substantive gaps limit it for complex data types:

1. No AWS CLI / live infrastructure evidence commands. For cloud-hosted systems, file-based grep misses the most important evidence layer: whether encryption, logging, and access controls are actually active in the running environment, not just declared in Terraform.

2. No Article 9 / special category guidance. The skill is framework-agnostic but does not prompt for data-type–specific requirements. A platform handling ID documents without Article 9 analysis is the highest-risk GDPR gap for Rentora, and the skill would not surface it without external knowledge.

3. No PCI intersection check. When bank account details appear in scope for a GDPR audit, the skill should flag the PCI DSS intersection question even if PCI is a separate full audit. Silence on this is a material omission for a fintech-adjacent platform.

These gaps are architectural: the skill needs data-type–specific modules or at minimum a "special data types checklist" to be reliable across all property/fintech scenarios.
