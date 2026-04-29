# Result: Technical decision

**Verdict:** PARTIAL
**Score:** 16.5/18.5 criteria met (89%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Performs pre-flight — met. The Pre-Flight (MANDATORY) section requires reading CLAUDE.md and .claude/CLAUDE.md, checking installed rules, reading marketplace.json, reviewing the technology stack, checking for existing ADRs, and identifying active technical debt. All steps are required by name.
- [x] PASS: Delegates the architecture decision to the architect agent, framing the decision with scope, constraints, and context — met. The definition classifies "System structure, bounded contexts, integration patterns → `system-design`" under architect delegation. The Delegation Protocol mandates five elements (objective, scope, context, acceptance criteria, evidence requirements).
- [x] PASS: Does not pick an option without analysis — met. The architecture decision path explicitly requires "produce a trade-off summary in your output: what options exist, what each sacrifices, and your initial assessment" before delegating. This is a mandatory step.
- [x] PASS: Applies "simple until proven otherwise" — met. The Principles section states "Simple until proven otherwise. Add complexity only when you have evidence it's needed." Team size and year-one scale are the correct evidence to cite.
- [x] PASS: Produces a dispatch plan rather than implementing directly — met. The Capability Constraint states the CTO "produce[s] a dispatch plan listing which engineering agents to invoke." "What You Don't Do" prohibits direct implementation.
- [x] PASS: Frames a clear escalation path if the decision involves significant vendor lock-in — met. The Decision Checkpoints table lists "Choosing a technology that creates significant vendor lock-in → escalate to coordinator" as a STOP trigger. The Escalation Protocol also names this explicitly.
- [~] PARTIAL: References the need for an ADR — partially met (rubric ceiling). The definition states "Every architecture decision must produce an ADR → include `write-adr` as a required deliverable in the acceptance criteria." This is explicit and unconditional. Scored 0.5 per PARTIAL ceiling.
- [x] PASS: Does not make product decisions — met. "What You Don't Do" lists "Decide what to build or for whom — that's the CPO's domain" explicitly.
- [-] SKIP: Escalates to coordinator — skipped. No budget or cross-domain conflict is present in this scenario.

### Output expectations

- [x] PASS: Recommends starting with the monolith — met. The definition's "simple until proven otherwise" principle applied to a 3-person team at 50-client scale unambiguously produces a monolith recommendation. The mandatory trade-off summary step would produce the reasoning about microservices overhead burning engineering capacity on plumbing.
- [x] PASS: Addresses the 50 → 500 client growth path — met. The trade-off summary requirement and the "simple until proven otherwise" principle together require evidence-based assessment; a 500-client year-three target is directly relevant scope the CTO would include as context for the architect. The dispatch to `system-design` would frame this as a constraint.
- [x] PASS: Dispatches to the architect via `architect:architect` with the `system-design` skill — met. The definition classifies this as "System structure, bounded contexts, integration patterns → `system-design`" and requires the fully-qualified `architect:architect` format. Scope, constraints, and deliverables are mandated by the Delegation Protocol.
- [x] PASS: Covers trade-offs honestly — met. The architecture decision path requires producing "a trade-off summary: what options exist, what each sacrifices, and your initial assessment." This mandates coverage of both monolith and microservices trade-offs. The definition does not enumerate them explicitly, but the step is mandatory and the format requires both sides.
- [x] PASS: Requires an ADR as the architect's deliverable — met. The definition states "Every architecture decision must produce an ADR → include `write-adr` as a required deliverable in the acceptance criteria." Year-3 reconsideration triggers and rejected alternatives are normal ADR content, though not explicitly named; the ADR requirement itself is explicit.
- [~] PARTIAL: Addresses document-management domain specifically — partially met. The definition requires domain-sliced architecture ("Organise by bounded context, not by technical layer") and the trade-off summary step would capture bounded context implications. However, the definition does not explicitly name document storage, search, and access control as the first extraction candidates or require the architect to model clean Django app boundaries for these. The principle supports this output but does not mandate it.
- [x] PASS: Stays in the technical domain — met. "What You Don't Do" explicitly prohibits deciding what to build, making go-to-market decisions, and writing user-facing copy. The definition holds a clean boundary between the CTO's "how" and the CPO's "what."
- [x] PASS: Produces a dispatch plan rather than implementation — met. The Capability Constraint is explicit: the CTO produces a dispatch plan; the main conversation executes the dispatches. "Implement features directly" is in "What You Don't Do."
- [x] PASS: Flags vendor lock-in considerations — met. The Decision Checkpoints table explicitly requires a STOP before "Choosing a technology that creates significant vendor lock-in." The definition would surface data store and infrastructure choices (Postgres, search infrastructure) as the lock-in vectors to flag.
- [~] PARTIAL: Addresses team-skill match — partially met. The definition does not explicitly require matching technology selection to team operational depth. The "simple until proven otherwise" principle and the trade-off summary step would likely surface this, but the definition does not mandate team-skill match as a named criterion. The output would plausibly include it, but it is not a structural guarantee.

## Notes

The prior result.md only scored the `## Criteria` section (9 items); this evaluation adds the `## Output expectations` section (10 items). The definition is strong on structural guarantees — pre-flight, trade-off summary, dispatch format, vendor lock-in, ADR requirement — but the output expectations for domain specificity (module boundary naming for document storage, search, access control) and team-skill match are not mandated by name. The definition would plausibly produce these outputs but does not structurally guarantee them. Overall the definition is well-formed for this scenario; the gaps are in specificity of architect dispatch framing rather than principle.
