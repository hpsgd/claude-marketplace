# Result: Large initiative decomposition across CPO and CTO domains

**Verdict:** PASS
**Score:** 17/18 criteria met (94%)
**Evaluated:** 2026-04-29

## Criteria

- [x] PASS: Coordinator decomposes into workstreams that map to specific agents — met. "Decompose Across Teams" maps every workstream to a named agent role; the RATSI matrix provides unambiguous ownership for each activity type. Architect, security-engineer, product-owner, CPO, gtm, user-docs-writer are all in the agent list.
- [x] PASS: Dependencies between workstreams identified and sequenced — met. Section 3 mandates a dependency table with explicit "depends on / blocks" structure; Section 5 (Sequence the Work) requires architecture and product requirements to precede development.
- [x] PASS: Both CPO and CTO workstreams present — met. The decomposition framework explicitly separates CPO workstreams (Product, Design, Content, GTM, Support) from CTO workstreams (Architecture, Development, QA, DevOps, Security, Data); pricing and documentation are CPO-domain.
- [x] PASS: Effort estimates or sizing signals per workstream — met. Section 4 requires ranges not points ("'1–2 weeks' not '10 days'"); point estimates are prohibited; complexity signals guide estimation.
- [x] PASS: Critical path identified — met. Section 4 requires calling out the critical path explicitly with the format "Critical path: [chain]. Minimum [N] weeks."
- [~] PARTIAL: Revenue context ($400k ARR) used to inform priority and timeline, not just mentioned — partially met. Section 1 Step 5 instructs translating commercial signals into urgency tiers with the exact scenario type ("a $400k ARR opportunity... is a different urgency than a nice-to-have feature"). The instruction exists but does not go as far as connecting the dollar value to a specific target quarter or delivery date — that level of specificity is not mandated.
- [x] PASS: Security implications called out as a specific workstream or constraint — met. "Security: Threat model, security review checkpoints" is listed under CTO workstreams; the security-engineer is in the RATSI as Responsible for threat models.
- [x] PASS: Output is a dispatch plan, not implementation — met. Core definition: "you don't do the work — you produce a dispatch plan." Capability Constraint prohibits writing files. "What You Don't Do" includes "Implement anything."

## Output expectations

- [x] PASS: Workstreams cover data isolation, auth/permissions, billing, UI workspace switching, documentation, pricing model — met. The decomposition framework and RATSI matrix address all six areas; architect covers data isolation and auth, CPO covers pricing/billing, product-owner covers workspace switching, user-docs-writer covers documentation, GTM covers commercial changes.
- [x] PASS: Dependency map shows data isolation before implementation, pricing before billing, auth feeding UI — met. Section 3 dependency table structure and Section 5 sequencing pattern require exactly this kind of typed dependency chain; the definition's 3-amigos and "architecture precedes development" rules enforce the ordering.
- [x] PASS: Critical path named with what blocks what — met. Section 4 mandates explicit critical path identification with the chain and minimum weeks stated; the definition's example format ("Critical path: Product requirements → Architecture → Development → QA execution → Release") demonstrates the expected output shape.
- [~] PARTIAL: $400k ARR used to inform a target delivery date or quarter — partially met. Section 1 Step 5 requires translating revenue context into urgency tiers, but the definition does not mandate connecting the dollar amount to a specific delivery date or quarter — it could satisfy the instruction by classifying it as "high urgency" without naming a timeline, which is weaker than the criterion requires.
- [x] PASS: Multi-tenancy security as distinct workstream covering tenant isolation, blast-radius, and encryption options — met. Security threat model is a required CTO workstream; the security-engineer is responsible for threat models and CVSS scoring; the architecture section requires ADRs for significant technical decisions, which would include tenant isolation and encryption at rest.
- [x] PASS: Effort estimates per workstream as ranges, not single-point — met. Section 4 is unambiguous: "'1–2 weeks' not '10 days'." Point estimates are explicitly prohibited.
- [x] PASS: Dispatch plan names agent/role per workstream, deliverable, and entry/exit criteria — does NOT contain code or specs — met. The Core definition, Capability Constraint, and "What You Don't Do" collectively enforce this. Agent invocation reference provides the qualified format for every agent.
- [x] PASS: Covers both CPO (pricing, packaging, GTM, customer comms) and CTO (data, auth, infra) workstreams — met. Both domains are explicitly required in the decomposition framework; CPO workstreams list includes GTM and Content; RATSI maps customer-success and support as informed parties for launches.
- [x] PASS: Addresses migration of existing single-tenant customers as a workstream — met. The definition requires identifying "Dependencies: external APIs, data migrations, infrastructure changes" in the Definition of Ready; data migrations and migration of existing data structures are required elements before work can start.
- [x] PASS: Identifies parallel opportunities — UX research while data isolation designed, docs alongside implementation — met. Section 5 Sequence the Work explicitly calls out parallel tracks (Design and Security threat model run in parallel in step 2; step 3 allows QA test writing and developer unit tests to run concurrently; step 5 shows Content and GTM preparation running parallel to QA execution).

## Notes

The agent definition is thorough and covers all criteria well. The one consistent gap across both sections is the specificity of how revenue context maps to delivery dates — the definition instructs urgency-tier translation but stops short of mandating a named quarter or milestone date. That's a minor structural gap rather than a missing concept. The RATSI matrix and decomposition framework together give the coordinator enough structure to produce a well-formed dispatch plan for a multi-tenancy initiative of this complexity.
