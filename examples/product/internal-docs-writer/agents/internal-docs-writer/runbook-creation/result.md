# Output: Runbook creation

**Verdict:** PARTIAL
**Score:** 16/18 criteria met (89%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Written for a first-timer at 2am — met. The definition states "Every runbook is written for someone handling it at 2am for the first time" as a non-negotiable in the Core section, and restates it verbatim in the Principles section. The runbook rules require copy-pasteable commands and expected output per step. Structural, not aspirational.

- [x] PASS: Includes a decision tree or clear branching logic for different failure modes — met. The Troubleshooting section combined with the numbered Steps structure and the 2am-first-timer principle would drive per-mode routing logic for the four failure modes named in the prompt. The definition does not use the phrase "decision tree" but the per-mode troubleshooting structure and explicit work classification before writing means branching logic would be produced.

- [x] PASS: Every diagnostic step includes the exact command or query to run — met. "Every command is copy-pasteable. No placeholders without explanation." is a hard rule. The definition structurally prohibits "check the logs" as a step.

- [x] PASS: Includes a rollback or safe revert step for any action that could make the situation worse — met. The runbook structure has an explicit Rollback section, and the rules add "Rollback for every destructive step. If step 3 can break things, there's a rollback before step 4." Structural, not optional.

- [x] PASS: Specifies an escalation path with roles and contact method — met. "Escalation — who to contact if the runbook doesn't resolve it" is a required section. The framing would produce role-and-contact-method content rather than a vague "escalate if needed."

- [x] PASS: Documents how to verify the incident is resolved — met. "Verification — how to confirm the procedure succeeded" is a mandatory section. Given the prompt's Datadog monitoring context and specific alert thresholds, the agent would produce metric-and-threshold verification steps.

- [~] PARTIAL: Covers all four failure modes — 0.5. The agent reads and uses prompt context. All four failure modes (API timeouts, card declines, idempotency conflicts, webhook failures) are named in the prompt and the agent would address all four via the Troubleshooting and Steps sections. Coverage depends on what the user provides, not on an explicit exhaustive-coverage rule in the definition.

- [x] PASS: Includes severity classification or impact assessment — met. The runbook Overview section requires "when to use this runbook, what it accomplishes." Given the explicit $3,400/minute business impact in the prompt and the 2am-audience framing, the agent would surface this as urgency context in the Overview.

### Output expectations

- [x] PASS: Output's runbook header states the alert trigger conditions verbatim — met. The Overview section requires "when to use this runbook, what it accomplishes." With trigger conditions explicitly supplied in the prompt (payment success rate < 95% over 5 min, Stripe API error rate > 2%) and the $3,400/minute figure, the 2am framing demands these appear in the header.

- [x] PASS: Output's decision tree branches on the first observable signal — met. The Troubleshooting section plus the 2am-first-timer constraint would drive the agent to route on the first observable signal. With four distinct failure modes in the prompt, a branching entry point is the natural output of the per-mode troubleshooting structure.

- [x] PASS: Output's diagnostic commands are exact and copy-pasteable — met. "Every command is copy-pasteable. No placeholders without explanation." is a hard rule. The agent would produce specific commands against the named stack (Node.js, PostgreSQL, Redis/Bull, Datadog).

- [x] PASS: Output's commands each show the expected output/threshold — met. "Every step has a verification. After running this, you should see: [expected output]" is an explicit runbook rule.

- [x] PASS: Output handles each of the four failure modes with branch-specific diagnostics — met. All four modes are named in the prompt. The Troubleshooting section would yield branch-specific steps for each, and the specific remediation paths in the criterion (retry queue fail-over, Redis key commands, Bull queue depth) are consistent with what the agent would produce given the stack context.

- [x] PASS: Output's rollback steps are explicit for any destructive action — met. "Rollback for every destructive step" is a hard rule. The Rollback section is mandatory structure. The agent would produce explicit undo commands.

- [x] PASS: Output's escalation thresholds are defined — met. The Escalation section now explicitly requires "the triggers that fire escalation (time elapsed without resolution, scope expansion, vendor status page incident, severity threshold)." The agent would produce time-based and condition-based triggers rather than a vague escalation note. This addresses the previous gap.

- [ ] FAIL: Output's escalation table names specific contact details — not met. The definition drives "who to contact" and now drives escalation triggers, but cannot supply organisation-specific contact details it doesn't know: no Stripe enterprise email, no PagerDuty service name, no on-call backup contacts. The agent would produce a role-level escalation path but not runnable contact information. No definition-level mechanism supplies or requires specific contact details.

- [x] PASS: Output's verification step shows what success looks like with a Datadog query — met. The Verification section now requires "the exact monitoring query or metric reference (same copy-pasteable standard as diagnostic commands) and the threshold that proves recovery." With Datadog named as the monitoring tool and specific thresholds supplied in the prompt, the agent would produce a copy-pasteable Datadog query and a "success looks like" threshold statement. This addresses the previous gap.

- [x] PASS: Output is written for a first-timer at 2am — met. Stated three times in the definition (Core, Runbook rules, Principles) and drives every structural choice. Single-action steps, no assumed knowledge, explicit paths throughout.

## Notes

The definition was updated between evaluations. Two gaps from the prior pass are now closed:

1. **Escalation thresholds** — the Escalation section now requires triggers (time elapsed, vendor status page, severity threshold), so the agent would produce "if no resolution after 30 min, escalate" logic rather than open-ended escalation guidance.

2. **Verification query** — the Verification section now explicitly requires the exact monitoring query in the same copy-pasteable standard as diagnostic commands. Given Datadog is named and thresholds are supplied in the prompt, the agent would produce a runnable query.

The one remaining FAIL is structural: specific contact details (PagerDuty service names, Stripe escalation email, on-call contacts) can only come from an organisation-supplied source the agent doesn't have access to. A pre-flight step that reads from a contacts file, or a definition rule that prompts the user to supply contact details before writing, would close this gap.

The PARTIAL on failure mode coverage (criterion 27) reflects that exhaustive coverage is prompt-driven, not enforced by the definition. If the prompt had omitted one failure mode the agent would miss it.
