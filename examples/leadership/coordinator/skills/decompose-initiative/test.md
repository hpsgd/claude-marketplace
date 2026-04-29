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

## Output expectations

- [ ] PASS: Output's initiative context table reproduces the prompt facts — Notification Centre, Taskwave, in-app notifications for task assignments / deadlines / @mentions, medium scope, 6-week appetite — not abstracted into generic placeholders
- [ ] PASS: Output's workstreams include the relevant ones — UX (notification surface design), architect (real-time delivery mechanism), backend developer (event sources for assignments, deadlines, mentions), frontend developer (notification centre UI), QA — and EXCLUDE GTM, support training, formal user research as out-of-scope for an internal feature this size
- [ ] PASS: Output's dependency map shows architect and UX work feeds developer implementation, and that backend event-source work for each notification type must be in place before the frontend can subscribe to them
- [ ] PASS: Output's phased execution sequence has named gates between phases — e.g. "Discovery complete → Design gate", "Design complete → Implementation gate", "Implementation complete → QA gate" — not just sequential phases without checkpoints
- [ ] PASS: Output identifies the critical path explicitly — likely real-time delivery mechanism design (e.g. WebSockets vs polling) blocking everything that depends on it — and names parallel opportunities (e.g. UI mockups can proceed while delivery mechanism is being chosen)
- [ ] PASS: Output's summary table has columns for owner role, dependencies, key deliverables, phase, AND effort estimate — and the effort estimates are ranges (e.g. "1-2 weeks") not single points
- [ ] PASS: Output's effort estimates fit within the 6-week appetite — total time on the critical path should be ≤6 weeks, with the timeline reasoning shown
- [ ] PASS: Output includes follow-up actions pointing to related skills — at minimum `/coordinator:write-spec` to spec the work and `/coordinator:define-okrs` if there's an outcome metric to track (e.g. notification engagement rate)
- [ ] PARTIAL: Output addresses the user-actionable nature of the notifications — task assignments and deadline reminders can drive workflow actions, so the design must cover both passive (read) and active (act) interactions
