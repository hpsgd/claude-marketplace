# Result: Write runbook

**Verdict:** PARTIAL
**Score:** 15/18 criteria met (83.3%)
**Evaluated:** 2026-04-29

## Results

### Criteria (structural)

- [x] PASS: First-timer at 2am — the skill's core principle is stated explicitly: "This runbook will be used by someone who has never done this procedure before, at 2am, while stressed. Every decision must serve that reader. No assumed knowledge. No missing steps. No ambiguity."
- [x] PASS: Every command includes expected output — the step template has a mandatory `**Expected output:**` field, and the rules state "Every step needs expected output. The operator must be able to confirm what they see matches what they should see."
- [x] PASS: Rollback for every destructive action — the Rollback section is mandatory, the rules require `⚠ WARNING:` prefixes on destructive steps, and the quality checklist explicitly checks "Rollback exists."
- [x] PASS: Escalation table with named roles and contact methods — the Escalation section template requires columns for Condition, Escalate to, Contact, and Expected response time, with a rule requiring PagerDuty service name, Slack channel, or vendor support case URL.
- [x] PASS: Verification step at end — the Verification section is mandatory, requiring a checklist with "exact command to run and the expected result" for every check.
- [x] PASS: Research step before writing — Step 1 requires searching the codebase for scripts, deployment configs, and infrastructure definitions before writing begins.
- [x] PASS: Severity/impact header — the Overview table now includes a mandatory **Business impact** field ("what breaks for users if this is not done; expected RTO/RPO if applicable") alongside the existing Risk level field.
- [x] PASS: Valid YAML frontmatter — frontmatter present with `name: write-runbook`, `description`, and `argument-hint: "[service, procedure, or incident type]"`.

### Output expectations (behavioural)

- [x] PASS: Output is specifically for promoting a read replica to primary — the skill's research-first Step 1 requires searching the codebase for deployment configs and infrastructure definitions, so $ARGUMENTS ("database failover procedure — promoting the read replica to primary") would drive stack-specific content (PostgreSQL or named provider with exact commands).
- [x] PASS: First section answers "is this the right runbook?" with health check, 60-second wait, and retry rule — the mandatory Pre-check section explicitly requires an exact health-check command, a 60-second wait + re-run rule for transient conditions, confirmation the trigger is not planned maintenance, and explicit stop conditions. This would appear in the output.
- [x] PASS: Commands are exact and copy-pasteable with $VAR syntax — the skill explicitly requires this pattern: `export SERVICE_NAME=my-service  # Replace with the actual service name from: kubectl get services`, and the quality checklist checks "Copy-paste test."
- [~] PARTIAL: Promotion step shows success indicators (writes accepted, replication lag N/A, verification queries) — the skill requires expected output per step and a verification checklist covering service health, logs, metrics, and user actions. General verification is required; database-failover-specific checks (replication lag = N/A, write acceptance queries) are not mandated.
- [x] PASS: Rollback covers original primary recovering with split-brain prevention and "do not promote both" warning — the Rollback section now explicitly requires an `⚠ WARNING: do not [activate / promote / write to] both` directive, ordered steps to demote/fence/quarantine the previously-active system, and instructions for re-introducing the recovered system as a follower after re-syncing.
- [~] PARTIAL: Escalation table has named contacts (PagerDuty service `database-oncall`, vendor support URL) — the skill requires concrete identifiers (PagerDuty service name, Slack channel, or vendor support case URL) and prohibits "the on-call team." The specific service name `database-oncall` is not mandated; the level of specificity required is present but the exact identifiers are left to the runbook author.
- [x] PASS: Escalation conditions are specific with data-loss thresholds — the escalation table template includes a "Data loss suspected (e.g. replication lag > [N] minutes at failover time)" row, and the rules require "specific and measurable" conditions with "numeric thresholds, time windows, or explicit signals." "If problems" or "escalate as needed" is explicitly prohibited.
- [~] PARTIAL: Verification confirms full health including application reads and writes — the Verification section template requires service health, logs, metrics, dependent services, and user actions. Confirming replication is re-established to a new replica (so the system is not running solo after failover) is not a required checklist item.
- [x] PASS: Research evidence shown in the output — the Appendix section now explicitly requires "References: source files, ADRs, vendor documentation, and infrastructure definitions consulted while writing this runbook — with paths or URLs," with the note that "this shows the runbook is grounded in the actual system, not invented procedure."
- [~] PARTIAL: Severity/impact header notes business impact (write outage, expected RTO) — the Business impact field is now a required Overview field with guidance to state what breaks for users and expected RTO/RPO. The specific framing "primary unavailable = full write outage; expected RTO 5-15 min" is illustrative rather than mandated; the field would likely contain this information for a database failover runbook given the $ARGUMENTS.

## Notes

The SKILL.md revision addresses four of the five gaps from the previous run. Pre-check is now a mandatory section with the exact 60-second retry rule. Split-brain/re-introduction is explicitly required in Rollback. Escalation thresholds are now mandated to be specific and measurable with numeric triggers. Research evidence is now required to appear in the Appendix with paths or URLs. Business impact is now a required Overview field.

The four remaining PARTIALs are narrow: database-specific verification checks (replication lag, write acceptance queries), the exact PagerDuty service name (`database-oncall`) vs. the required level of contact specificity, the "running solo" replica restoration check in verification, and the exact framing of the impact statement. None of these are structural gaps in the skill; they are specificity differences between what the skill mandates and what the test criteria expect for the database failover scenario.
