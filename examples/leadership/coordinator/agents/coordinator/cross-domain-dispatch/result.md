# Cross-domain dispatch

**Scenario:** A user brings a multi-domain feature launch requiring product, design, engineering, and launch work. Does the coordinator decompose it correctly and produce a structured dispatch plan without making unilateral decisions?

> We need to ship a new "Team Workspaces" feature for Flowbase before the end of the quarter. It lets multiple users collaborate inside a shared workspace — they can invite members, assign roles (admin/editor/viewer), and work on the same projects together. We need the whole thing: specs, designs, backend, frontend, tests, deployment, and launch content. Can you coordinate this?

Routed to the coordinator, which decomposes cross-team initiatives into structured dispatch plans and produces sequenced delegation rather than executing directly.

## Output

The coordinator opens with pre-flight: reads CLAUDE.md and .claude/CLAUDE.md, reads `.claude-plugin/marketplace.json` to check which agents are enabled, identifies installed leads (CPO, CTO), reviews any existing roadmap artefacts, and checks for active workstreams that might affect capacity.

It then produces a structured dispatch plan:

**CPO workstreams:** product-owner for PRD and user stories (roles, permissions model, invite flow, workspace switching UX); ui-designer for component specs and accessibility requirements; gtm for launch plan and positioning. Support prep flagged as relevant (role-based onboarding, invite emails).

**CTO workstreams:** architect for system design (multi-user data model, role-based access control, workspace isolation, API contracts) and ADR; security-engineer for threat model (auth, roles, access control — explicitly in scope); qa-lead for acceptance criteria and test strategy (3 amigos); dotnet-developer and react-developer for backend/frontend implementation; devops for infrastructure and deployment pipeline; qa-engineer for acceptance tests (must precede development per 3 amigos pattern).

**Dependencies:** architecture and product requirements precede all development; QA Lead participates in 3 amigos before development starts; security threat model runs parallel to design, must complete before implementation begins.

**Definition of Ready gate:** the coordinator calls out that development cannot start until the DoR checklist is cleared — problem validated, user stories written, QA Lead reviewed acceptance criteria, design complete, architecture agreed, ADR written, dependencies identified.

The plan does not include decisions on data model choices, technology stack, pricing, or feature scope — those are routed to CTO and CPO respectively.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8/8 (100%) | 2026-04-16 |

- [x] PASS: Performs pre-flight checks — the Pre-Flight section is MANDATORY and requires reading CLAUDE.md, `.claude/CLAUDE.md`, marketplace.json, and settings.json before any decomposition; checking installed leads and reviewing active workstreams is explicitly required
- [x] PASS: Produces a structured dispatch plan — the Core definition states "you produce a dispatch plan that the main conversation executes"; the Capability Constraint section prohibits direct execution: "You cannot write files or dispatch other agents"
- [x] PASS: Decomposes across both CPO and CTO teams — Section 2 explicitly lists CPO workstreams (Product, Design, Content, GTM, Support) and CTO workstreams (Architecture, QA Lead, Development, QA Engineer, DevOps, Security, Data); both teams are required for any cross-team initiative
- [x] PASS: Dependencies identified — architecture and product precede development — Section 3 mandates a dependency table showing Architecture depends on Product requirements and blocks Development and DevOps; QA Lead depends on Product requirements and blocks Development
- [x] PASS: 3-amigos sequencing applied — Section 5 specifies "Product + Architecture + QA Lead (3 amigos)" as step 1, and explicitly states "Development does not start until acceptance tests exist"
- [x] PASS: No unilateral product or technical decisions — the Non-negotiable principle states "You never make unilateral decisions that belong to the CPO or CTO"; "What You Don't Do" lists "Make product decisions" and "Make technical decisions" explicitly
- [x] PASS: Definition of Ready checked before marking work ready — Section 5 (Definition of Ready) provides a nine-item checklist with the explicit rule "If any item is missing, the work is not ready. Send it back to the appropriate lead for completion"
- [x] PASS: Security workstream identified as relevant — the CTO team workstream list explicitly includes "Security: Threat model, security review checkpoints"; the RATSI matrix shows security-engineer owns threat models; Team Workspaces involves roles, member invitations, and access control — all auth-adjacent; the Definition of Done requires security review for auth-touching changes
- [-] SKIP: CPO vs CTO conflict escalation — no conflict simulated in this scenario

## Notes

The coordinator definition handles this cleanly. The RATSI matrix is the most useful element for the security criterion — it makes security-engineer ownership of threat models unambiguous without requiring inference. One structural note: the definition has two sections labelled "Step 5" (Sequence the Work and Definition of Ready). The numbering error doesn't affect behaviour but could confuse someone reading linearly. Pre-Flight Step 3 (flagging inactive agents in dispatch plans) is a practical addition not tested by this rubric — it's worth having.
