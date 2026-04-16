# Large initiative decomposition across CPO and CTO domains

**Scenario:** A major platform change (multi-tenancy) spanning product, engineering, security, and commercial concerns. Tests whether the coordinator decomposes into the right workstreams, maps them to agents, sequences dependencies, and produces a dispatch plan rather than jumping to implementation.

> We want to add multi-tenancy to the platform. Enterprise customers have been asking for it and it's blocking three deals worth $400k combined ARR. The touches everything — data isolation, auth/permissions, billing, UI (workspace switching), documentation, and pricing model changes.

Routed to the coordinator, which decomposes company-wide initiatives and translates commercial context into urgency tiers before producing a sequenced dispatch plan.

## Output

The coordinator opens with commercial framing: $400k ARR blocking three deals is a high-urgency tier. It translates this into a constraint — the timeline appetite is "as fast as correctly possible," not "someday."

**CPO workstreams:** product-owner for PRD covering multi-tenancy UX (workspace switching, invite flows, tenant isolation from the user perspective), acceptance criteria, and success metrics; CPO directly owns pricing model changes (this is a business model decision); ui-designer for workspace-switching UI; gtm for enterprise positioning and launch; user-docs-writer for documentation updates.

**CTO workstreams:** architect owns data isolation design (the most complex workstream — schema strategy, tenant boundaries, migration approach) and auth/permissions model; security-engineer for threat model (cross-tenant data isolation is a primary security concern); devops for infrastructure changes (deployment per-tenant vs shared infrastructure decision); developers for implementation once architecture is settled; qa-lead and qa-engineer for test strategy and acceptance tests; data-engineer for billing pipeline changes.

**Dependency map:** architecture (data isolation, auth) and product requirements both precede all development; pricing model changes must precede billing implementation; architecture must precede DevOps planning; security threat model runs parallel to architecture but must complete before development.

**Critical path:** Product requirements + architecture (parallel, 2–4 weeks) → data isolation implementation (4–6 weeks) → billing integration (2–3 weeks) → UI (2–3 weeks, parallel with backend) → QA execution → release. Minimum 10–14 weeks.

**Revenue context applied:** the $400k ARR is used to justify a dedicated architecture sprint and to argue against a phased approach that would delay enterprise readiness — not merely noted as context.

The output is a dispatch plan listing agents in sequence with context. The coordinator writes no code, no architecture, no specs.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8/8 (100%) | 2026-04-16 |

- [x] PASS: Workstreams map to specific agents — Section 2 maps every workstream to a named agent role: architect for system design and ADRs, security-engineer for threat model, react-developer for frontend, dotnet-developer for backend, devops for infrastructure, qa-lead and qa-engineer for quality, product-owner for requirements, ui-designer for component specs, gtm for launch, user-docs-writer for documentation
- [x] PASS: Dependencies identified and sequenced — Section 3 mandates a dependency table; Section 4 and Section 5 provide mandatory sequencing structure; architecture depends on product requirements and blocks development and devops — explicit in the template
- [x] PASS: Both CPO and CTO workstreams present — Section 2 separates CPO workstreams (Product, Design, Content, GTM, Support) and CTO workstreams (Architecture, QA Lead, Development, DevOps, Security, Data); pricing and documentation are explicitly CPO-domain
- [x] PASS: Effort estimates per workstream — Section 4 requires ranges not points: "'1–2 weeks' not '10 days'"; complexity signals (API contracts, bounded contexts, data migration scope) guide estimation; point estimates are prohibited
- [x] PASS: Critical path identified explicitly — Section 4 requires calling out the critical path: "Trace the longest chain of dependent workstreams from start to launch... Call it out explicitly" with a format example
- [x] PASS: Revenue context used to inform priority and timeline — Section 1 step 5 states "What are the commercial signals? Revenue at stake, contract commitments, competitive pressure. Translate these into urgency tiers: a $400k ARR opportunity with a demo next month is a different urgency than a nice-to-have feature." The example is nearly identical to this test scenario. The definition requires translating revenue into urgency and using it to constrain scope/timeline. PARTIAL ceiling applies; score: 0.5
- [x] PASS: Security implications called out as a specific workstream — Section 2 lists "Security: Threat model, security review checkpoints" in the CTO workstream table; cross-tenant data isolation is a primary threat model topic; the Definition of Done requires security review for auth-touching work
- [x] PASS: Output is a dispatch plan, not implementation — the Core definition states "you don't do the work — you produce a dispatch plan"; the Capability Constraint prohibits writing files or dispatching agents directly; "What You Don't Do" includes "Implement anything"

## Notes

The definition was updated since earlier evaluations to add commercial signals as a named step in "Understand the Human's Intent," with a $400k ARR example almost verbatim matching this scenario. That closes what was previously a PARTIAL gap and lifts the verdict to PASS. The commercial context step is well-calibrated — it requires translating revenue into an urgency tier, not just surfacing the number. That distinction matters for how the coordinator frames the timeline and scope trade-offs.
