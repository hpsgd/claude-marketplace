# Test: decompose-initiative

Scenario: A user invokes the skill with a reasonably complex initiative. Does the skill produce a correctly structured decomposition with initiative context, relevant workstreams (not all of them), a dependency map, a phased execution sequence with gates, and a summary table with estimates?

## Prompt

/coordinator:decompose-initiative "Notification Centre — a new in-app notification system for Taskwave that lets users receive, manage, and act on real-time alerts for task assignments, deadline reminders, and @mentions. Estimated scope: medium. Timeline appetite: 6 weeks."

## Criteria

- [ ] PASS: Completes Step 1 (initiative context table) — including user problem, target user, success criteria, appetite, and constraints
- [ ] PASS: Assesses workstream relevance for both CPO and CTO teams — does not include all workstreams blindly, excludes irrelevant ones with reasoning
- [ ] PASS: Includes a dependency map showing what blocks what — specifically that design and architecture depend on product requirements
- [ ] PASS: Produces a phased execution sequence with named gates between phases (not just "move on when ready")
- [ ] PASS: Identifies the critical path and parallel opportunities explicitly
- [ ] PASS: Produces a summary table with owner roles, dependencies, key deliverables, phase, and effort estimates as ranges
- [ ] PASS: Effort estimates are ranges, not point estimates (e.g. "1–2 weeks" not "1 week")
- [ ] PARTIAL: Includes follow-up actions pointing to related skills (define-okrs, write-spec)
- [ ] PASS: Does not include GTM, support prep, or formal UX research if the scenario doesn't warrant it — avoids padding the decomposition
