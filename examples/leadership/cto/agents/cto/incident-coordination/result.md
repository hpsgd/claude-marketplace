# Result: Production incident coordination

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 14.5/16 criteria met (91%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: CTO follows incident response protocol — detect/assess before root-causing — met. Section 6 "Incident Response" explicitly lists "Detect + Assess" as step 1 before any mitigation or investigation.
- [x] PASS: First action is mitigation (rollback the deployment), not investigation — met. Step 2 states "Mitigate — fastest path to reduce impact (rollback, feature flag, scale). Do this BEFORE root-causing." Unambiguous.
- [x] PASS: CTO delegates to devops for the rollback and the relevant developer for diagnosis — met. Step 3: "Delegate investigation — assign the devops and relevant developer to diagnose"; the team table maps devops to incident response and dotnet-developer to .NET backend.
- [x] PASS: CTO escalates to coordinator for customer communication — met. Step 4: "Communicate — escalate to the coordinator if customer communication is needed. The CPO's support team handles customer-facing messaging." Escalation Protocol reinforces this: "Incidents requiring customer communication (coordinator routes to CPO's support team)."
- [~] PARTIAL: Delegation includes specific evidence requirements — partially met. The Delegation Protocol mandates "Specify evidence requirements — what proof you need" as a general rule. The Incident Response section does not enumerate the specific artifacts (deployment logs, error traces, Grafana dashboard links, exception stack) for incident delegations specifically. General protocol covers the behaviour but the incident section is not self-contained. Score: 0.5.
- [~] PARTIAL: CTO identifies blast radius (all payment transactions) and estimates customer impact — partially met. Step 1 asks "what's the impact? Who's affected? Is data at risk?" which covers blast-radius assessment but does not prescribe quantifying revenue impact per minute or estimating refund/retry obligations. The principle is present; the depth is not specified. Score: 0.5.
- [x] PASS: Post-incident actions are mentioned — met. Step 5 "Root cause + prevent" and Step 6 "Post-incident review — ensure an ADR or post-mortem is written" are both explicit.
- [x] PASS: CTO does not attempt to debug code directly — met. "What You Don't Do" includes "Implement features directly — delegate to the appropriate developer"; the incident response protocol delegates investigation to devops and the developer; direct debugging is inconsistent with the delegation model.

### Output expectations

- [x] PASS: Output's first action is mitigation — met. The protocol mandates mitigation before root-causing; a well-formed response following Section 6 would lead with rollback, not log-diving or information gathering.
- [x] PASS: Output correlates deploy timestamp with error onset explicitly — met. "Detect + Assess — what's the impact? Who's affected?" combined with "Verify before asserting" means the agent would surface the 45-min/20-min gap as evidence supporting the rollback decision rather than skipping to action.
- [x] PASS: Output dispatches DevOps and .NET developer in parallel — met. "Cross-Domain Coordination" step 2 "Sequence — identify dependencies"; rollback and diagnosis are independent tasks; the dispatch plan format produces parallel dispatches when there are no blocking dependencies.
- [x] PASS: Output escalates customer comms to coordinator or CPO — met. Escalation Protocol explicitly names "Incidents requiring customer communication" as a coordinator trigger.
- [x] PASS: Output specifies evidence required from the diagnosing developer — met. Delegation Protocol mandates "Specify evidence requirements" as a named step for all delegations; deployment logs, error traces, and Grafana links are the natural artifacts that support post-rollback analysis.
- [x] PASS: Output quantifies blast radius — met. Detect + Assess asks "what's the impact? Who's affected?" which covers blast-radius assessment and severity classification; all-transactions-down would be characterised as P0/SEV-1.
- [x] PASS: Output names post-incident actions — met. "Post-incident review — ensure an ADR or post-mortem is written" is explicit; "Root cause + prevent" covers the RCA and process gap identification (no canary, no health-check gate).
- [x] PASS: Output does NOT attempt to read code or hypothesise root cause — met. "What You Don't Do" prohibits direct implementation; the capability constraint confirms the agent produces dispatch plans, not code analysis; incident protocol delegates investigation.
- [x] PASS: Output establishes a rollback timeline — met. Delegation Protocol requires "Set acceptance criteria — how you'll know it's done", which for a rollback naturally includes time bounds; "Verify before asserting" implies tracking error rate returning to baseline.
- [~] PARTIAL: Output addresses incident communication cadence — partially met. The definition covers escalation to the coordinator for comms and the CPO's support team handling customer-facing messaging. Channel routing is covered. Timing intervals (e.g., Slack channel every 15 min, status page on declaration) are not prescribed — those belong in a runbook, not an agent definition, but they are missing against the criterion as stated. Score: 0.5.

## Notes

The incident response section is one of the most explicit parts of the CTO definition and maps well onto the test criteria. The three partial marks share the same root: the agent prescribes the right behaviours at a structural level but does not descend to operational specifics — revenue-per-minute blast radius, named evidence artifacts in the incident section, per-channel communication cadence. These gaps are arguably appropriate for an agent definition (runbooks carry operational detail), but they are real gaps against the rubric. The definition would produce a strong, well-structured incident response for this scenario.
