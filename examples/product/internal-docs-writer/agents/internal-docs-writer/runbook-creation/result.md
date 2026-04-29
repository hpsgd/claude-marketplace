# Output: Runbook creation

**Verdict:** PARTIAL
**Score:** 14/18 criteria met (78%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Written for a first-timer at 2am — met. The definition states "Every runbook is written for someone handling it at 2am for the first time" as a non-negotiable in the Core section, and restates it verbatim in the Principles section. The runbook rules require copy-pasteable commands and expected output per step. This is a structural constraint, not aspirational language.

- [x] PASS: Includes a decision tree or clear branching logic for different failure modes — met. The Troubleshooting section ("common issues and their fixes") combined with the numbered Steps structure and the 2am principle would drive the agent to produce per-mode routing logic for the four failure modes named in the prompt. The definition does not use the phrase "decision tree" but the combination of per-mode troubleshooting and explicit work classification before writing means branching logic would be produced. Inferred from principles rather than named as a template section.

- [x] PASS: Every diagnostic step includes the exact command or query to run — met. The runbook rules are unambiguous: "Every command is copy-pasteable. No placeholders without explanation." The Verification Protocol also includes "Run every command — in a clean environment if possible." The definition structurally prohibits "check the logs" as a step.

- [x] PASS: Includes a rollback or safe revert step for any action that could make the situation worse — met. The runbook structure has an explicit Rollback section, and the rules add: "Rollback for every destructive step. If step 3 can break things, there's a rollback before step 4." Structural, not optional.

- [x] PASS: Specifies an escalation path with roles and contact method — met. "Escalation — who to contact if the runbook doesn't resolve it" is a required section in the runbook structure. The framing ("who to contact") would produce role-and-contact-method content rather than a vague "escalate if needed."

- [x] PASS: Documents how to verify the incident is resolved — met. "Verification — how to confirm the procedure succeeded" is a mandatory runbook section. Given the prompt context (Datadog monitoring, specific alert thresholds of 95% success rate and 2% error rate), the agent would produce metric-and-threshold verification steps.

- [~] PARTIAL: Covers all four failure modes — 0.5. The agent reads and uses prompt context. All four failure modes (API timeouts, card declines, idempotency conflicts, webhook failures) are named in the prompt and the agent would address all four via the Troubleshooting and Steps sections. The definition does not independently enforce exhaustive failure mode coverage — coverage depends on what the user provides.

- [x] PASS: Includes severity classification or impact assessment — met. The runbook Overview section requires "when to use this runbook, what it accomplishes," and the definition emphasises honesty about sharp edges and writing for an audience under pressure who need to act. Given the explicit $3,400/minute business impact in the prompt, the agent would surface this in the Overview as urgency context. The runbook template has no explicit "severity" section, but the Overview requirement and audience-first principles are strong enough to drive impact quantification.

### Output expectations

- [x] PASS: Output's runbook header states the alert trigger conditions verbatim — met. The Overview section requires "when to use this runbook, what it accomplishes." With trigger conditions explicitly supplied in the prompt (payment success rate < 95% over 5 min, Stripe API error rate > 2%), and the definition's 2am framing demanding immediate actionability, the agent would reproduce these conditions in the header. The $3,400/minute figure would appear as the business impact.

- [x] PASS: Output's decision tree branches on the first observable signal — met. The Troubleshooting section plus the 2am-first-timer constraint would drive the agent to route on the first observable signal. With four distinct failure modes supplied in the prompt, a branching entry point is the natural output of the per-mode troubleshooting structure.

- [x] PASS: Output's diagnostic commands are exact and copy-pasteable — met. "Every command is copy-pasteable. No placeholders without explanation." is a hard rule. The agent would produce specific commands against the stack named in the prompt (Node.js, PostgreSQL, Redis/Bull, Datadog) rather than generic descriptions.

- [x] PASS: Output's commands each show the expected output/threshold — met. "Every step has a verification. After running this, you should see: [expected output]" is an explicit runbook rule. The agent would show thresholds (e.g. healthy vs failure counts) alongside every diagnostic command.

- [x] PASS: Output handles each of the four failure modes with branch-specific diagnostics — met. All four modes are named in the prompt. The agent reads the prompt context and the Troubleshooting section would yield branch-specific steps for each. The specific remediation paths described in the criterion (fail-over to retry queue, Redis key commands, Bull queue depth) are consistent with what the agent would produce given the stack context.

- [x] PASS: Output's rollback steps are explicit for any destructive action — met. "Rollback for every destructive step" is a hard rule in the definition. The Rollback section is mandatory structure. The agent would produce explicit undo commands rather than "reverse the action."

- [ ] FAIL: Output's escalation table names roles AND contacts with specific contact details — not met. The definition's Escalation section requires only "who to contact if the runbook doesn't resolve it." Without knowing the organisation's actual contact details (Stripe enterprise email, PagerDuty service names, on-call backup contacts), the agent would produce a role-level escalation path but not specific contact information like "enterprise@stripe.com" or "PagerDuty service payments-backup." The definition provides no mechanism to supply or require specific contact details.

- [ ] FAIL: Output's escalation thresholds are defined — not met. The definition specifies who to escalate to but says nothing about when — no time-based triggers, no "if no resolution after X minutes" rule. The escalation section requirement is structural ("who to contact") with no time-threshold component. The agent would not reliably produce "if no resolution after 30 min, page the engineering manager" without a definition-level rule requiring it.

- [ ] FAIL: Output's verification step shows what success looks like with the specific Datadog query — partial met, scoring as FAIL. The Verification section is mandatory and the prompt supplies Datadog as the monitoring tool and specific thresholds. The agent would produce a verification step referencing those thresholds. However, the definition does not require a specific Datadog query syntax (e.g. `payment.errors{service:payment-api} | sum:1m`), and the agent has no access to the organisation's actual Datadog metric names. A threshold-based description is likely; a runnable Datadog query is not reliably produced.

- [x] PASS: Output is written for a first-timer at 2am — met. This is stated three times in the definition (Core non-negotiables, Runbook rules, Principles) and drives every structural choice. Single-action steps, no assumed knowledge, and explicit paths are required by the definition's constraints.

## Notes

The Criteria section (original 8 items) scores 7.5/8 — the definition is strong on runbook structure fundamentals.

The Output expectations section (10 items) scores 6.5/10 — three specific gaps emerge:

1. **Escalation contacts.** The definition drives "who to escalate to" but cannot supply organisation-specific contact details it doesn't have access to. Specific contact details (email addresses, PagerDuty service names) require either a template slot in the definition or a pre-flight step that reads contact information from a team file.

2. **Escalation thresholds.** No time-based or condition-based escalation trigger is defined anywhere in the runbook structure or rules. Adding "Escalation triggers — conditions (time elapsed, scope, Stripe status page incident) that require waking someone up" to the Escalation section definition would fix this.

3. **Monitoring query specificity.** The definition correctly drives verification steps, but cannot produce runnable Datadog queries without knowing the organisation's metric naming conventions. A pre-flight step reading a monitoring reference file, or a definition rule requiring the agent to ask for metric names before writing verification steps, would close this gap.

The Decision Checkpoints table correctly flags untested runbooks — for an agent without access to a Stripe sandbox, the produced runbook would be marked [UNTESTED]. Honest, but worth noting for practical output quality.
