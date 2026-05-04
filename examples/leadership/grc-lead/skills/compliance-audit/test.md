# Test: compliance-audit

Scenario: A user invokes the skill to audit a system against a specific framework. Does the skill identify the applicable controls, collect verifiable code/config evidence (not just documentation claims), produce a gap register with severity rankings, and deliver a remediation plan with prioritised timelines?

## Prompt

/grc-lead:compliance-audit "GDPR — audit Rentora, a property rental platform that processes tenant and landlord personal data including names, addresses, ID documents, bank account details, and rental history. The platform is hosted on AWS in eu-west-1 and serves customers in France, Germany, and the Netherlands."

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

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

## Output expectations

- [ ] PASS: Output's scope section names which Rentora systems, data types (tenant PII, landlord PII, ID documents, bank account details, rental history), and processes are in scope — and explicitly excludes anything out of scope
- [ ] PASS: Output identifies the relevant GDPR articles for this scope — Articles 5 (principles), 6 (lawful basis), 9 (special categories — IDs may be biometric), 17 (erasure), 25 (data protection by design), 32 (security), 33-34 (breach notification), 44 (transfers) — not auditing every article blindly
- [ ] PASS: Output's evidence collection uses concrete grep / glob commands against the codebase and AWS configuration — e.g. `grep -ri "encrypt" terraform/`, `aws kms list-keys`, `find . -name '*.py' | xargs grep -l "delete_user"` — not just descriptive checklist items
- [ ] PASS: Output's control matrix uses MET / PARTIAL / GAP with the specific evidence cited per row (file:line, config name, log location) — never marking a control MET without a verifiable reference
- [ ] PASS: Output addresses ID document handling specifically — Article 9 special category if biometric, retention period for ID copies, encryption-at-rest with KMS, and access logging
- [ ] PASS: Output addresses bank account details — PCI scope if any card data is in flight, otherwise Article 32 security and minimisation (e.g. tokenisation via the payment provider, never persisting raw account numbers)
- [ ] PASS: Output's gap register has severity (Critical / High / Medium / Low) with reasoning per — Critical examples: no encryption at rest, no breach notification process, no DPA with Twilio/SMS providers
- [ ] PASS: Output's remediation plan per gap has specific actions, named owners, target dates, and verification methods (e.g. "deploy KMS encryption on RDS, owner: DevOps, target: 2026-05-15, verification: aws rds describe-db-instances shows StorageEncrypted=true")
- [ ] PASS: Output flags Critical gaps for immediate executive escalation — not placed in the same backlog as Low gaps
- [ ] PARTIAL: Output addresses cross-border transfers — eu-west-1 hosts EU data correctly for Germany / France / Netherlands customers, but any sub-processors (analytics, monitoring, error tracking) outside the EU need transfer mechanism review
