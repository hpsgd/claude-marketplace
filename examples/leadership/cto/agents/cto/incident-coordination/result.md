# Incident Coordination

Scenario: A production outage in the payments service requires the CTO to coordinate incident response across multiple teams. Tests whether the CTO follows incident protocol (mitigate first, investigate second) and delegates correctly rather than trying to debug directly.

## Prompt

> Production is down. The payments service is returning 500 errors for all transactions. Grafana shows it started 20 minutes ago. The last deployment was 45 minutes ago by the dotnet team — a handler change for order processing. Customer support is getting flooded. What do we do?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Immediate priority: rollback first, investigate second.**

1. **Rollback now** — the deployment 45 min ago is the prime suspect. Don't wait for root cause. Revert the dotnet handler change and redeploy. Recovery time beats diagnosis time when customers are affected.

2. **Declare incident** — get the dotnet team lead and an on-call engineer in a war room (Slack/call) immediately. Assign one person to communicate with customer support so they stop guessing.

3. **While rollback deploys** — pull logs from the payments service for the last 20 minutes. Look for the first 500, the stack trace, and what request triggered it. The handler change likely introduced a null ref, unhandled exception, or a schema mismatch on the order payload.

4. **Verify recovery** — after rollback, confirm Grafana error rate drops and run a test transaction before declaring resolved.

5. **Hold the post-mortem** — once stable, the dotnet team reviews what the handler change broke and why it wasn't caught in staging. Don't skip this step.

**Don't** try to hotfix forward while production is burning. Rollback buys you time to fix it properly.

What does your rollback process look like — do you have a one-click revert or does it need a manual redeployment?

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 9.5/17.0 (56%) |
| Evaluated | 2026-05-01 |
| Target duration | 12268 ms |
| Target cost | $0.0412 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO follows incident response protocol — detect/assess before root-causing | PASS | Opening line: 'Immediate priority: rollback first, investigate second.' Log investigation is step 3, only while rollback deploys. |
| c2 | First action is mitigation (rollback the deployment), not investigation | PASS | Step 1 is explicitly 'Rollback now — the deployment 45 min ago is the prime suspect. Don't wait for root cause. Revert the dotnet handler change and redeploy.' |
| c3 | CTO delegates to devops for the rollback and the relevant developer for diagnosis | PARTIAL | Step 2 says 'get the dotnet team lead and an on-call engineer in a war room' and step 5 mentions 'dotnet team reviews.' DevOps is never explicitly named as owning the rollback; the rollback is framed as a command ('Rollback now') with no named assignee. |
| c4 | CTO escalates to coordinator for customer communication (support team is under CPO) | PARTIAL | Step 2: 'Assign one person to communicate with customer support so they stop guessing.' Someone is assigned, but the CPO, coordinator, or escalation path is never mentioned. |
| c5 | Delegation includes specific evidence requirements — deployment logs, error traces, Grafana dashboard links | PARTIAL | Step 3 asks for 'logs from the payments service for the last 20 minutes,' 'the first 500, the stack trace, and what request triggered it.' Grafana dashboard links are never mentioned. |
| c6 | CTO identifies the blast radius (all payment transactions) and estimates customer impact | PARTIAL | Output references 'when customers are affected' and the original framing of 'all transactions' is accepted, but no explicit quantification of revenue impact, volume, or severity level is provided. |
| c7 | Post-incident actions are mentioned — root cause analysis, ADR or post-mortem | PASS | Step 5: 'Hold the post-mortem — once stable, the dotnet team reviews what the handler change broke and why it wasn't caught in staging. Don't skip this step.' |
| c8 | CTO does not attempt to debug the code directly — delegates to the specialist | PASS | No code is read or debugged. The CTO directs investigation to 'the dotnet team' and does not attempt to trace through the handler logic. |
| c9 | Output's first action is mitigation — initiating rollback of the deployment from 45 minutes ago — not investigation, not log diving, not asking for more data | PASS | Step 1 is 'Rollback now — the deployment 45 min ago is the prime suspect.' No data gathering precedes this. |
| c10 | Output correlates the deploy timestamp (45 min ago) with the error onset (20 min ago) explicitly — the 25-minute lag suggests the bad code rolled out and slowly poisoned in-flight requests / cache state, supporting the rollback decision | FAIL | The output identifies the deployment as 'prime suspect' but never explicitly correlates the two timestamps or reasons about the 25-minute lag between deploy and error onset. |
| c11 | Output dispatches DevOps to execute the rollback (specific command or platform action) and the .NET developer who shipped the order-processing handler change to begin diagnosis in parallel — not sequential | PARTIAL | Step 3 implies parallelism ('While rollback deploys — pull logs'), and the dotnet team lead is summoned. But DevOps is never named as the rollback executor, and no explicit parallel dispatch of two separate actors is stated. |
| c12 | Output escalates customer communication to the coordinator (or directly to the support team via CPO) — the CTO does not draft customer comms, but ensures someone is doing it | PARTIAL | Step 2: 'Assign one person to communicate with customer support.' The CTO does not draft comms. However, no CPO or coordinator is named, and the escalation chain is absent. |
| c13 | Output specifies the evidence required from the diagnosing developer — deployment logs / artefact diff, error traces from APM, Grafana dashboard time-range link spanning before/after deploy, and the specific exception stack — so the post-rollback analysis is concrete | PARTIAL | Step 3 requests 'logs,' 'the first 500, the stack trace, and what request triggered it.' No deployment artefact diff, no APM mention, no Grafana time-range link. |
| c14 | Output quantifies blast radius — 'all payment transactions failing' means revenue impact per minute, customer-side checkout failures, and likely refund / retry obligations — to set incident severity (probably P0/SEV-1) | FAIL | No severity level (P0/SEV-1), no revenue impact per minute, no quantification of checkout failures or retry/refund obligations. Customer impact is acknowledged only as 'customers are affected' and 'support is flooded.' |
| c15 | Output names the post-incident actions — blameless post-mortem with timeline, root cause analysis, ADR or learnings doc capturing what the deployment process missed (no canary, no health-check gate, no feature flag), and an action item to add the gate | PARTIAL | Step 5 mentions a post-mortem and reviewing why the issue wasn't caught in staging. No mention of blameless format, timeline, ADR/learnings doc, or specific deployment process improvements (canary, health-check gate, feature flag). |
| c16 | Output does NOT attempt to read code or hypothesise root cause directly — delegates to the developer who owns the change, while owning the coordination and communication | PARTIAL | Step 3: 'The handler change likely introduced a null ref, unhandled exception, or a schema mismatch on the order payload.' This is direct root-cause hypothesizing. No code is read, but the CTO does not stay in coordination-only mode. |
| c17 | Output establishes a timeline for the rollback (e.g. 'rollback executed within 5 min, errors should clear within 10 min, declare resolution after error rate returns to baseline for 5 min') | FAIL | No timeline or time-bound targets are given at any point in the output. Step 4 says 'verify recovery after rollback' but provides no time expectations. |
| c18 | Output addresses incident communication cadence — internal Slack channel, status page update for customers, support team brief — with timing per channel | FAIL | Step 2 says 'Assign one person to communicate with customer support.' No Slack channels, no status page, no timing per channel, no communication cadence whatsoever. |

### Notes

The output is a competent triage response that correctly prioritizes rollback over investigation and avoids code-debugging, but it falls short on depth across nearly every coordination and evidence criterion. Critical gaps: no explicit correlation of the deploy/error timestamps (c10), no blast-radius quantification or severity level (c14), no rollback timeline (c17), no communication cadence beyond 'assign someone' (c18), and no specific mention of deployment process improvements in the post-mortem (c15). DevOps and the CPO escalation chain are never named. The hypothesis about 'null ref / schema mismatch' is a minor breach of the delegation-only posture. The response reads like a strong engineering manager's instinct but lacks the structured, role-aware rigor expected of a CTO incident commander.
