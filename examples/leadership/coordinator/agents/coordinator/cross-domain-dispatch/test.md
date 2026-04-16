# Test: cross-domain dispatch

Scenario: A user brings a multi-domain feature launch request requiring product, design, engineering, and launch work. Does the coordinator decompose it correctly and produce a structured dispatch plan without making unilateral decisions?

## Prompt

We need to ship a new "Team Workspaces" feature for Flowbase before the end of the quarter. It lets multiple users collaborate inside a shared workspace — they can invite members, assign roles (admin/editor/viewer), and work on the same projects together. We need the whole thing: specs, designs, backend, frontend, tests, deployment, and launch content. Can you coordinate this?

## Criteria

- [ ] PASS: Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else
- [ ] PASS: Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly)
- [ ] PASS: Decomposes work across both CPO team (product, design, content, GTM) and CTO team (architecture, development, QA, DevOps, security)
- [ ] PASS: Identifies dependencies between workstreams — specifically that architecture and product must precede development
- [ ] PASS: Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts
- [ ] PASS: Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO
- [ ] PASS: Checks Definition of Ready criteria before marking work as ready to start
- [ ] PARTIAL: Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope)
- [ ] SKIP: Escalates to the human on a CPO vs CTO conflict — only relevant if a conflict is simulated
