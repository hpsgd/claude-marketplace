# Production incident coordination

**Scenario:** A production outage in the payments service requires the CTO to coordinate incident response across multiple teams. Tests whether the CTO follows incident protocol (mitigate first, investigate second) and delegates correctly rather than debugging directly.

> Production is down. The payments service is returning 500 errors for all transactions. Grafana shows it started 20 minutes ago. The last deployment was 45 minutes ago by the dotnet team — a handler change for order processing. Customer support is getting flooded. What do we do?

Routed to the CTO, which owns incident response and must follow the detect/assess/mitigate/delegate sequence rather than attempting to debug code directly.

## Output

**CTO incident response — payments service outage**

**Detect + Assess**

Impact: all payment transactions returning 500 errors. Started 20 minutes ago. Last deployment 45 minutes ago — dotnet team, handler change for order processing. Correlation is strong. All customers attempting payments are affected.

**Immediate action: mitigation first**

Rollback the deployment before investigating. The deployment is the most likely cause and rollback is faster than diagnosing the handler change.

**Dispatch plan**

Immediate — DevOps:
- Objective: roll back the dotnet order processing handler deployment to the previous stable version
- Scope: rollback only — do not attempt to fix forward
- Evidence required: confirmation of rollback completion, Grafana dashboard showing error rate returning to baseline, deployment log showing the rollback commit

Concurrent — Dotnet-developer:
- Objective: diagnose the handler change to identify what caused the 500 errors
- Scope: read the diff of the handler change, review error traces, do not push any fixes until rollback is confirmed successful
- Evidence required: the specific line or change causing the failures, error traces from the 20-minute window, Grafana dashboard link capturing the incident timeline

Escalate now — Coordinator:
- Objective: route customer communication to the CPO's support team
- Context: payments service has been down for 20+ minutes, all transactions affected, customer support is already receiving volume
- The coordinator routes this to CPO's support team — they own customer-facing messaging

**Post-incident**

After service is restored: root cause analysis with the dotnet team, post-mortem document covering timeline, impact, and prevention. ADR if the handler change reveals a systemic pattern that needs a design decision.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 7.5/8 (94%) | 2026-04-16 |

- [x] PASS: CTO follows incident response protocol — the definition has a dedicated "Incident Response" section (Section 6) with explicit ordered steps; "1. Detect + Assess — what's the impact? Who's affected? Is data at risk?" is the required first step before any other action
- [x] PASS: First action is mitigation, not investigation — the definition states "2. Mitigate — fastest path to reduce impact (rollback, feature flag, scale). Do this BEFORE root-causing." Rollback is listed as the first mitigation option; the BEFORE instruction is unambiguous
- [x] PASS: CTO delegates to devops for rollback and developer for diagnosis — Step 3 of incident response: "Delegate investigation — assign the devops and relevant developer to diagnose"; the team table maps devops to `incident-response` skill
- [x] PASS: CTO escalates to coordinator for customer communication — Step 4 of incident response: "Communicate — escalate to the coordinator if customer communication is needed. The CPO's support team handles customer-facing messaging"; the escalation path is explicit
- [~] PARTIAL: Delegation includes specific evidence requirements — the Delegation Protocol requires "Specify evidence requirements — what proof you need (test results, verification commands, screenshots)" as a general rule; the incident response section does not enumerate specific evidence types (deployment logs, error traces, Grafana links) for incident delegations specifically. The general protocol supports the behaviour but doesn't mandate these specifics in the incident context. Score: 0.5
- [~] PARTIAL: CTO identifies blast radius and estimates customer impact — Step 1 asks "what's the impact? Who's affected? Is data at risk?" which covers blast radius assessment; it does not require quantifying or estimating customer impact beyond identifying who is affected. Score: 0.5 (PARTIAL ceiling)
- [x] PASS: Post-incident actions mentioned — Step 6 of incident response: "Post-incident review — ensure an ADR or post-mortem is written"; explicit requirement
- [x] PASS: CTO does not debug code directly — "What You Don't Do" includes "Implement features directly — delegate to the appropriate developer"; the incident response section delegates investigation rather than having the CTO investigate personally; the principle "Verify before asserting" combined with the delegation model makes direct debugging inconsistent with the definition

## Notes

The incident response section is one of the more explicit and well-structured parts of the CTO definition. The minor gap is that evidence requirements for incident delegations aren't enumerated in the incident section itself — a reader needs to cross-reference the general Delegation Protocol. Adding incident-specific evidence requirements (logs, traces, dashboards) to Section 6 would make it self-contained and remove the cross-referencing dependency.
