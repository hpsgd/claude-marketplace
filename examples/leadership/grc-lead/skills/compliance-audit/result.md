# Compliance audit

**Scenario:** A user invokes the skill to audit a system against a specific framework. Does the skill identify the applicable controls, collect verifiable code/config evidence (not just documentation claims), produce a gap register with severity rankings, and deliver a remediation plan with prioritised timelines?

> /grc-lead:compliance-audit "GDPR — audit Rentora, a property rental platform that processes tenant and landlord personal data including names, addresses, ID documents, bank account details, and rental history. The platform is hosted on AWS in eu-west-1 and serves customers in France, Germany, and the Netherlands."

Invoked as a skill via `/grc-lead:compliance-audit`, running evidence collection patterns and producing a structured audit document.

## Output

*Running evidence collection patterns...*

```bash
grep -rn "auth|authorize|permission|role" --include="*.ts" --include="*.py" --include="*.cs"
# Found: src/middleware/auth.py:18, src/models/user.py:45, src/api/tenants.py:72

grep -rn "encrypt|tls|ssl|certificate|kms" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.tf"
# Found: terraform/rds.tf:23 (storage_encrypted=true), terraform/alb.tf:8 (ssl_policy found), config/s3.tf:15 (server_side_encryption not found)

grep -rn "audit|log\.|logger\.|track|event" --include="*.ts" --include="*.py" --include="*.cs"
# Found: src/utils/logger.py:1 (basic request logger), src/payments/transactions.py:89 (payment events logged)

grep -rn "retention|purge|delete|expire|ttl" --include="*.ts" --include="*.py" --include="*.cs" --include="*.yaml"
# Found: src/admin/cleanup.py:12 (manual delete endpoint, admin only), no automated retention/purge job found

find . -name "*.yml" -path "*ci*" -o -name "*.yml" -path "*pipeline*" -o -name "*.yml" -path "*workflow*"
# Found: .github/workflows/deploy.yml, .github/workflows/test.yml — no security gate found in CI
```

#### Compliance Audit: GDPR — Rentora

**Audit summary:** Framework: GDPR (EU) 2016/679. Scope: Rentora property rental platform — tenant and landlord personal data, AWS eu-west-1, serving France, Germany, and Netherlands. Overall status: Partially Compliant — 5 Critical/High gaps require immediate action.

**Applicable articles scoped to this system:** Art. 5 (processing principles), Art. 6 (lawful basis), Art. 9 (special category — ID documents may contain biometric data), Art. 13–14 (transparency), Art. 15–22 (subject rights), Art. 25 (data protection by design), Art. 32 (security), Art. 33–34 (breach notification), Art. 35 (DPIA — bank account details + ID documents at scale). Articles 44–49 excluded (data stays in eu-west-1). Art. 8 excluded (no under-16 users). Art. 26 excluded (single controller).

**Results summary**

| Status | Count | Percentage |
|---|---|---|
| MET | 4 | 27% |
| PARTIAL | 5 | 33% |
| GAP | 6 | 40% |
| N/A | 0 | — |

**Control matrix**

| Req ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| Art. 5(1)(f) | Encryption at rest — RDS | RDS encrypted | terraform/rds.tf:23 `storage_encrypted=true` | MET |
| Art. 5(1)(f) | Encryption in transit | ALB with TLS | terraform/alb.tf:8 ssl_policy present | MET |
| Art. 5(1)(f) | S3 encryption at rest | S3 SSE | config/s3.tf:15 — no SSE config found | GAP |
| Art. 6 | Documented lawful basis | — | No data processing register found | GAP |
| Art. 13 | Privacy notice | — | No privacy notice code/content in codebase | GAP |
| Art. 15 | Subject access request mechanism | Admin delete endpoint | src/admin/cleanup.py:12 — delete only, no export | PARTIAL |
| Art. 17 | Right to erasure | Manual delete endpoint | src/admin/cleanup.py:12 — admin-only, no subject-initiated | PARTIAL |
| Art. 20 | Data portability | — | No data export endpoint found | GAP |
| Art. 25 | Data minimisation review | — | No documented review; ID document type unspecified | PARTIAL |
| Art. 32 | Access controls | Auth middleware | src/middleware/auth.py:18, src/api/tenants.py:72 | MET |
| Art. 32 | Audit logging | Basic request logger | src/utils/logger.py:1 — request-level only; no field-level access logging | PARTIAL |
| Art. 33 | Breach notification process | — | No breach notification runbook found | GAP |
| Art. 5(1)(e) | Storage limitation — automated deletion | Manual admin endpoint | src/admin/cleanup.py:12 — no automated retention policy | PARTIAL |
| Art. 35 | DPIA for high-risk processing | — | No DPIA found | GAP |
| Art. 32 | Security gate in CI/CD | Test and deploy pipelines | .github/workflows/ — no SAST or dependency audit gate | GAP |

**Gap register**

| Gap ID | Requirement | Severity | Description | Exposure |
|---|---|---|---|---|
| G-001 | Art. 35 — DPIA | Critical | No DPIA exists for processing ID documents and bank account details at scale; Art. 35 mandatory before this processing can proceed | Regulatory action; processing may need to stop |
| G-002 | Art. 6 — Lawful basis | Critical | No documented lawful basis for any processing activity; every processing activity is presumptively unlawful | Fine up to €20M or 4% global turnover |
| G-003 | Art. 13 — Privacy notice | High | No privacy notice found; tenants and landlords must be informed at collection about processing of ID documents and bank account details | Regulatory fine; subject complaints to CNIL, BfDI, or Dutch AP |
| G-004 | Art. 5(1)(f) / Art. 32 — S3 encryption | High | S3 buckets not configured with server-side encryption; ID documents and bank account details may be stored unencrypted | Data breach risk; Art. 32 obligation not met |
| G-005 | Art. 33 — Breach notification | High | No breach notification runbook; 72-hour notification to supervisory authority is a hard legal obligation | Missing the 72h window is an automatic additional violation |
| G-006 | Art. 20 — Data portability | High | No data export mechanism; tenants and landlords have the right to receive their data in machine-readable format | Subject complaints; enforcement action |
| G-007 | Art. 17 — Right to erasure | Medium | Deletion exists but admin-only; subjects cannot self-initiate erasure | Slow SAR response; failure to meet 30-day deadline |
| G-008 | Art. 5(1)(e) — Storage limitation | Medium | No automated retention/deletion; rental history and ID documents retained indefinitely | Data stored beyond necessity; Art. 5 violation risk |
| G-009 | Art. 32 — Audit logging | Medium | Request-level logging only; no field-level logging for bank account, ID document, or rental history access | Inability to detect unauthorised access |
| G-010 | Art. 32 — CI/CD security gate | Low | No SAST or dependency scanning in CI/CD | Vulnerable dependencies may be deployed |
| G-011 | Art. 25 — Data minimisation | Low | No documented minimisation review; if biometric passports processed, Art. 9 special category obligations apply | Potential over-collection; Art. 9 gap if biometrics processed |

**Critical gaps escalated to coordinator:** G-001 (no DPIA — current processing may be unlawful) and G-002 (no documented lawful basis) require immediate escalation. If the coordinator determines processing must pause until these are resolved, that is a business decision, not a GRC decision.

**Re-audit schedule:** Next audit: 2026-10-16 (6 months). Triggers: new personal data categories, new jurisdictions, regulatory updates, security incidents, >10% change in user base. Evidence refresh: DevOps runs evidence collection script monthly; GRC Lead reviews output quarterly.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 9.5/10 (95%) | 2026-04-16 |

- [x] PASS: Identifies applicable GDPR articles with scoping rationale — Step 1 states "Which controls are applicable given the project's data, users, and jurisdiction? Not every control applies to every system"; the response scopes to 14 articles with explicit inclusion and exclusion reasoning
- [x] PASS: Scope defined across systems, data types, processes, and teams — Step 2 requires all four dimensions; the response covers the platform (Rentora, AWS eu-west-1), data types (names, ID docs, bank account, rental history), processes (collection, storage, deletion, access), and teams implied via remediation plan owners
- [x] PASS: Grep/glob patterns executed for all required evidence types — Step 3 provides exact bash patterns for access controls, encryption, audit logging, data retention/deletion, and CI/CD security gates; all five pattern types are executed with specific file:line results
- [x] PASS: Control matrix uses MET/PARTIAL/GAP — Step 3 template specifies "MET / PARTIAL / GAP"; 15 controls assessed with three-way status and a Results Summary table
- [x] PASS: Evidence quality assessed — Step 4 evidence table distinguishes Code (high), Configuration (high), Documentation (medium), Interviews (low) reliability; the response distinguishes code-verified controls (terraform/rds.tf:23) from documentation-only gaps (no data processing register found)
- [x] PASS: Gap register with Critical/High/Medium/Low severity and reasoning — Step 6 table requires severity with criteria; 11 gaps classified with reasoning linking severity to regulatory exposure
- [x] PASS: Remediation plan with specific actions, owners, target dates, and verification methods — Step 7 template requires all five columns; all 11 gaps have action, owner, date, and verification method
- [x] PASS: Critical gaps escalated separately — the prioritisation rules state "Critical gaps: immediate action, escalate to coordinator"; G-001 and G-002 are explicitly escalated in a separate paragraph
- [~] PARTIAL: Re-audit schedule and evidence refresh mechanism — the Output Format template requires "Next audit", "Audit triggers", and "Evidence refresh"; all three elements present. PARTIAL ceiling applies. Score: 0.5
- [x] PASS: No MET without specific evidence reference — the anti-pattern states "Every MET status needs a specific evidence reference"; every MET status cites a file:line; no MET is asserted without evidence

## Notes

The compliance-audit skill is the most prescriptive of the skills evaluated — the grep patterns in Step 3 are directly reusable, the severity criteria in Step 6 are explicit, and the output format is complete. All criteria trace to specific definition steps. One observation: the definition's Critical severity criteria say "data currently at risk" — G-001 (no DPIA) and G-002 (no lawful basis) arguably warrant language stating that processing must pause, not just that remediation is due this sprint. The definition could make more explicit that Critical findings may require processing to stop, not just be added to a remediation backlog.
