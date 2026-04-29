# Result: compliance-audit

**Verdict:** PARTIAL
**Score:** 17/20 criteria met (85%)
**Evaluated:** 2026-04-29

## Criteria

- [x] PASS: Identifies applicable GDPR articles with scoping rationale — met. Step 1 explicitly requires determining "which controls are applicable given the project's data, users, and jurisdiction? Not every control applies to every system."
- [x] PASS: Scope defined — systems, data types, processes, teams — met. Step 2 requires all four dimensions explicitly.
- [x] PASS: Searches codebase with grep/glob patterns — met. Step 3 provides exact bash patterns for access controls, encryption config, audit logging, data retention/deletion, and CI/CD security gates.
- [x] PASS: Control matrix uses MET/PARTIAL/GAP status — met. Step 3 template specifies "MET / PARTIAL / GAP" as the three-way status.
- [x] PASS: Evidence quality assessed — code-verified vs documentation-only — met. Step 4 table distinguishes Code (high), Configuration (high), Documentation (medium), Interviews (low) reliability; the anti-pattern states "If evidence requires 'just ask [person]', it is not auditable evidence."
- [x] PASS: Gap register with Critical/High/Medium/Low severity and reasoning — met. Step 6 table requires severity with four-level criteria and examples.
- [x] PASS: Remediation plan with specific actions, owners, target dates, and verification methods — met. Step 7 template requires all five columns.
- [x] PASS: Critical gaps flagged for immediate escalation — met. Prioritisation rules state "Critical gaps: immediate action, escalate to coordinator."
- [~] PARTIAL: Re-audit schedule and evidence refresh mechanism — partially met. The Output Format template requires "Next audit", "Audit triggers", and "Evidence refresh" sections, but the skill body does not enforce re-audit as a process step — it appears only in the anti-patterns ("One-time audits — compliance is continuous") and the output template. No step in the sequential process instructs the auditor to define the re-audit schedule; it is only a template placeholder. Score: 0.5.
- [x] PASS: No MET without specific evidence reference — met. Anti-pattern states "ticking 'yes' without verifiable evidence is audit theatre. Every MET status needs a specific evidence reference"; the control matrix template requires an Evidence column.

## Output expectations

- [x] PASS: Output's scope section names Rentora systems, data types (tenant PII, landlord PII, ID documents, bank account details, rental history), and processes in scope, with explicit exclusions — met. Step 2 requires systems, data types, processes, and teams explicitly; the Output Format audit summary requires scope to be stated.
- [x] PASS: Output identifies relevant GDPR articles for this scope (Arts 5, 6, 9, 17, 25, 32, 33-34, 44) without auditing every article blindly — met. Step 1 requires scoping to applicable controls and the framework table references Articles 5–49 as the range; the scoping instruction filters to what applies.
- [ ] FAIL: Output's evidence collection uses concrete grep/glob commands against the codebase and AWS configuration — not met for AWS-specific commands. Step 3 provides grep patterns for code and config files, but no AWS CLI commands (`aws kms list-keys`, `aws rds describe-db-instances`, etc.) are included. The skill's bash patterns do not address infrastructure-as-observed (live AWS state), only files on disk.
- [x] PASS: Output's control matrix uses MET/PARTIAL/GAP with specific evidence cited per row — met. The template requires "Evidence" column and the anti-pattern blocks marking controls MET without a verifiable reference.
- [ ] FAIL: Output addresses ID document handling specifically — Article 9 special category if biometric, retention, KMS encryption, access logging — not met. The skill definition contains no mention of special category data (Article 9), biometric considerations, or ID document–specific controls. A GDPR audit against a platform handling ID documents would need this, but the skill has no mechanism to surface it.
- [ ] FAIL: Output addresses bank account details — PCI scope assessment, tokenisation vs raw persistence, Article 32 — not met. The skill references PCI DSS as a framework in its own right but does not instruct the auditor to consider PCI implications when bank data is in scope within a GDPR audit. No guidance on tokenisation or raw account number persistence.
- [x] PASS: Output's gap register has severity (Critical/High/Medium/Low) with reasoning per gap — met. Step 6 severity table includes the criteria and examples such as "no encryption for PII at rest, no breach notification process."
- [x] PASS: Output's remediation plan per gap has specific actions, named owners, target dates, and verification methods — met. Step 7 template columns include Remediation, Owner, Target date, and Verification.
- [x] PASS: Output flags Critical gaps for immediate executive escalation — met. Prioritisation rules state Critical gaps require immediate action and escalation to coordinator.
- [~] PARTIAL: Output addresses cross-border transfers — eu-west-1 hosting is EU-compliant, but sub-processors outside EU need transfer mechanism review — partially met. The framework table references "Article 44 transfers" as in scope for GDPR, but the skill provides no specific guidance on sub-processor transfer analysis or the distinction between primary hosting location and third-party service providers. A well-formed output would likely note Article 44 but may not systematically surface sub-processor gaps. Score: 0.5.

## Notes

The skill is strong for structural compliance auditing — the sequential process, evidence typing, control matrix, and gap register are all well-designed. The main weaknesses are: (1) no AWS CLI or live infrastructure evidence commands, limiting the skill's ability to verify cloud-hosted systems beyond what is checked into files; (2) no data-type–specific guidance for special category data (Article 9) or financial data PCI intersections, which means domain-specific risks in a GDPR audit of a fintech-adjacent property platform would require the auditor to supply that knowledge independently. These are substantive gaps for a scenario like Rentora where both apply.
