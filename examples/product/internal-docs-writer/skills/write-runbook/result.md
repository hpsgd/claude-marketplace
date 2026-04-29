# Result: Write runbook

**Verdict:** FAIL
**Score:** 11.5/18 criteria met (63.9%)
**Evaluated:** 2026-04-29

## Results

### Criteria (structural)

- [x] PASS: First-timer at 2am — the skill's core principle is stated explicitly: "This runbook will be used by someone who has never done this procedure before, at 2am, while stressed. Every decision must serve that reader. No assumed knowledge. No missing steps. No ambiguity."
- [x] PASS: Every command includes expected output — the step template has a mandatory `**Expected output:**` field, and the rules state "Every step needs expected output. The operator must be able to confirm what they see matches what they should see."
- [x] PASS: Rollback for every destructive action — the Rollback section is mandatory, the rules require `⚠ WARNING:` prefixes on destructive steps, and the quality checklist explicitly checks "Rollback exists."
- [x] PASS: Escalation table with named roles and contact methods — the Escalation section template requires columns for Condition, Escalate to, Contact, and Expected response time, with a rule to include primary and backup contacts.
- [x] PASS: Verification step at end — the Verification section is mandatory, requiring a checklist with "exact command to run and the expected result" for every check.
- [x] PASS: Research step before writing — Step 1 requires searching the codebase for scripts, deployment configs, and infrastructure definitions before writing begins.
- [~] PARTIAL: Severity/impact header — the Overview table requires a "Risk level" field (Low/Medium/High/Critical) but not a "Business impact" field. Risk classification is present; quantitative impact context (RTO, write outage scope) is not required as a header field.
- [x] PASS: Valid YAML frontmatter — frontmatter present with `name: write-runbook`, `description`, and `argument-hint: "[service, procedure, or incident type]"`.

### Output expectations (behavioural)

- [x] PASS: Output is specifically for promoting a read replica to primary — the skill's research-first Step 1 requires searching the codebase for deployment configs and infrastructure definitions, so $ARGUMENTS ("database failover procedure — promoting the read replica to primary") would drive stack-specific content (PostgreSQL or named provider with exact commands).
- [ ] FAIL: First section answers "is this the right runbook?" with health check, 60-second wait, and retry rule — the Overview requires "When to use" (trigger conditions) but the skill does not require a pre-procedure confirmation gate with a specific health check command, a 60-second wait, or a retry-before-failover rule. This would not appear in the output.
- [x] PASS: Commands are exact and copy-pasteable with $VAR syntax — the skill explicitly requires this pattern: `export SERVICE_NAME=my-service  # Replace with the actual service name from: kubectl get services`, and the quality checklist checks "Copy-paste test."
- [~] PARTIAL: Promotion step shows success indicators (writes accepted, replication lag N/A, verification queries) — the skill requires expected output per step and a verification checklist. The template mentions "Service is responding" and "Users can perform core action" but does not mandate checking replication lag = N/A or write acceptance specifically. General verification is required; these specific database-failover checks are not.
- [ ] FAIL: Rollback covers original primary recovering with split-brain prevention and "do not promote both" warning — the Rollback section template covers "When to rollback", "Rollback window", and "Data implications" but does not mandate the specific re-introduction-as-replica procedure or an explicit anti-split-brain warning.
- [~] PARTIAL: Escalation table has named contacts (PagerDuty service `database-oncall`, vendor support URL) — the skill requires real contacts with contact methods and backup contacts. It does not mandate PagerDuty service-level names or vendor support case URLs specifically. Named roles and contact methods are required; the level of specificity (PagerDuty service ID, RDS support URL) is not.
- [ ] FAIL: Escalation conditions are specific with data-loss thresholds (e.g. replication lag >5 minutes triggers DBA escalation before accepting writes) — the skill's escalation template has a Condition column but does not mandate threshold-specific conditions. A well-formed output from this skill could say "data loss suspected" without the quantified replication-lag trigger.
- [~] PARTIAL: Verification confirms full health including replication to a new replica and monitoring — the Verification section template requires checklist items with commands and expected results, and covers service health, logs, metrics, and user actions. Confirming replication is set up to a new replica (so system isn't running solo) is not a required checklist item.
- [ ] FAIL: Research evidence shown in the output — the skill requires research in Step 1 but the runbook output template does not require citing source files, ADRs, or cloud provider documentation. Research informs the commands but evidence of it appearing in the final runbook is not required.
- [~] PARTIAL: Severity/impact header notes business impact (write outage, expected RTO) — same as Criteria criterion 7. Risk level is a required Overview field; "primary unavailable = full write outage; expected RTO 5-15 min" style context is not mandated.

## Notes

The skill is structurally strong on all 8 structural criteria — the 2am principle, copy-pasteable commands, mandatory rollback and verification, research-first, and valid frontmatter are all genuinely present. The gap is in the Output expectations section, which tests whether the skill would produce runbook content meeting a higher specificity bar for a database failover scenario.

Four outright failures: the "is this the right runbook?" pre-check gate, the split-brain/re-introduction rollback, the quantified escalation thresholds, and research evidence visible in the output. These are legitimate gaps — a runbook produced by this skill would be well-structured but would not automatically include a 60-second retry-before-failover rule, an explicit "do not promote both" warning, a replication-lag data-loss threshold in the escalation table, or citations showing which configs and ADRs were consulted.
