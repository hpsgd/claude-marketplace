# Test: compliance-audit

Scenario: A user invokes the skill to audit a system against a specific framework. Does the skill identify the applicable controls, collect verifiable code/config evidence (not just documentation claims), produce a gap register with severity rankings, and deliver a remediation plan with prioritised timelines?

## Prompt

/grc-lead:compliance-audit "GDPR — audit Rentora, a property rental platform that processes tenant and landlord personal data including names, addresses, ID documents, bank account details, and rental history. The platform is hosted on AWS in eu-west-1 and serves customers in France, Germany, and the Netherlands."

## Criteria

- [ ] PASS: Identifies which GDPR articles and requirements are applicable — does not audit every article blindly, scopes to what applies
- [ ] PASS: Defines scope: which systems, data types, processes, and teams are in scope for this audit
- [ ] PASS: Searches codebase for evidence using grep/glob patterns (access controls, encryption config, audit logging, deletion mechanisms)
- [ ] PASS: Control matrix uses MET/PARTIAL/GAP status — not a binary pass/fail without nuance
- [ ] PASS: Evidence quality is assessed — distinguishes between code-verified controls and documentation-only claims
- [ ] PASS: Gap register includes severity classification (Critical/High/Medium/Low) with reasoning
- [ ] PASS: Remediation plan includes specific actions, owners, target dates, and verification methods per gap
- [ ] PASS: Critical gaps are flagged for immediate escalation, not placed in the same backlog as low gaps
- [ ] PARTIAL: Re-audit schedule and evidence refresh mechanism are defined
- [ ] PASS: Does not mark controls as MET without citing a specific evidence reference (file, config, log)
