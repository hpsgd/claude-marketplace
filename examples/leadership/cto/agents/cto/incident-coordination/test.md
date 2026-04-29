# Test: Production incident coordination

Scenario: A production outage in the payments service requires the CTO to coordinate incident response across multiple teams. Tests whether the CTO follows incident protocol (mitigate first, investigate second) and delegates correctly rather than trying to debug directly.

## Prompt

Production is down. The payments service is returning 500 errors for all transactions. Grafana shows it started 20 minutes ago. The last deployment was 45 minutes ago by the dotnet team — a handler change for order processing. Customer support is getting flooded. What do we do?

## Criteria

- [ ] PASS: CTO follows incident response protocol — detect/assess before root-causing
- [ ] PASS: First action is mitigation (rollback the deployment), not investigation
- [ ] PASS: CTO delegates to devops for the rollback and the relevant developer for diagnosis
- [ ] PASS: CTO escalates to coordinator for customer communication (support team is under CPO)
- [ ] PASS: Delegation includes specific evidence requirements — deployment logs, error traces, Grafana dashboard links
- [ ] PARTIAL: CTO identifies the blast radius (all payment transactions) and estimates customer impact
- [ ] PASS: Post-incident actions are mentioned — root cause analysis, ADR or post-mortem
- [ ] PASS: CTO does not attempt to debug the code directly — delegates to the specialist

## Output expectations

- [ ] PASS: Output's first action is mitigation — initiating rollback of the deployment from 45 minutes ago — not investigation, not log diving, not asking for more data
- [ ] PASS: Output correlates the deploy timestamp (45 min ago) with the error onset (20 min ago) explicitly — the 25-minute lag suggests the bad code rolled out and slowly poisoned in-flight requests / cache state, supporting the rollback decision
- [ ] PASS: Output dispatches DevOps to execute the rollback (specific command or platform action) and the .NET developer who shipped the order-processing handler change to begin diagnosis in parallel — not sequential
- [ ] PASS: Output escalates customer communication to the coordinator (or directly to the support team via CPO) — the CTO does not draft customer comms, but ensures someone is doing it
- [ ] PASS: Output specifies the evidence required from the diagnosing developer — deployment logs / artefact diff, error traces from APM, Grafana dashboard time-range link spanning before/after deploy, and the specific exception stack — so the post-rollback analysis is concrete
- [ ] PASS: Output quantifies blast radius — "all payment transactions failing" means revenue impact per minute, customer-side checkout failures, and likely refund / retry obligations — to set incident severity (probably P0/SEV-1)
- [ ] PASS: Output names the post-incident actions — blameless post-mortem with timeline, root cause analysis, ADR or learnings doc capturing what the deployment process missed (no canary, no health-check gate, no feature flag), and an action item to add the gate
- [ ] PASS: Output does NOT attempt to read code or hypothesise root cause directly — delegates to the developer who owns the change, while owning the coordination and communication
- [ ] PASS: Output establishes a timeline for the rollback (e.g. "rollback executed within 5 min, errors should clear within 10 min, declare resolution after error rate returns to baseline for 5 min")
- [ ] PARTIAL: Output addresses incident communication cadence — internal Slack channel, status page update for customers, support team brief — with timing per channel
