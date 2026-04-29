# Result: cross-domain dispatch

**Verdict:** PARTIAL
**Score:** 18.5/20 criteria met (92.5%)
**Evaluated:** 2026-04-29

## Section breakdown

- Criteria: 8.5/9 scoreable (1 SKIP excluded)
- Output expectations: 10/11 scoreable

## Results

### Criteria

- [x] PASS: Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else — met. "Pre-Flight (MANDATORY)" Steps 1–3 explicitly direct reading CLAUDE.md, `.claude/rules/`, marketplace.json, and settings.json before any other action.
- [x] PASS: Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly) — met. The "Capability constraint" paragraph states: "you cannot write files or dispatch other agents... You analyse the situation and produce a structured dispatch plan listing which agents to invoke, in what order, with what context."
- [x] PASS: Decomposes work across both CPO team and CTO team — met. "Decompose Across Teams" lists both teams with named workstreams (product, design, content, GTM, support for CPO; architecture, QA Lead, development, QA Engineer, DevOps, security, data for CTO).
- [x] PASS: Identifies dependencies between workstreams — specifically that architecture and product must precede development — met. The dependency table in §3 shows Architecture depends on Product requirements and blocks Development; Product requirements also block QA Lead acceptance criteria.
- [x] PASS: Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts — met. Step 1 of the sequencing section names "Product + Architecture + QA Lead (3 amigos — define WHAT, HOW, and HOW TO VERIFY)". The definition also states "Development does not start until acceptance tests exist."
- [x] PASS: Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO — met. "Non-negotiable" states this directly. "What You Don't Do" lists "Make product decisions — that's the CPO" and "Make technical decisions — that's the CTO."
- [x] PASS: Checks Definition of Ready criteria before marking work as ready to start — met. The DoR section lists nine criteria with an explicit gate: "If any item is missing, the work is not ready. Send it back to the appropriate lead."
- [~] PARTIAL: Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope) — partially met. Security is listed as a CTO workstream ("Security: Threat model, security review checkpoints") and the security engineer appears throughout the RATSI table. The definition does not direct the coordinator to call out auth and roles as a specifically heightened risk surface. It would surface security, but not necessarily flag it as a priority concern for this category of feature.
- [-] SKIP: Escalates to the human on a CPO vs CTO conflict — skipped. The scenario describes no conflict between CPO and CTO.

### Output expectations

- [x] PASS: Output uses fully-qualified `plugin:agent` invocation format (e.g., `cpo:cpo`, `cto:cto`, `architect:architect`) rather than bare names — met. The definition devotes an "Agent invocation format" section to this requirement, including a warning that the short form "will fail with an error," and provides a full copy-paste reference table.
- [x] PASS: Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan — met. §"Understand the Human's Intent" lists five questions to answer first: desired outcome, appetite, priority, deadline type (hard vs soft), and commercial signals. The "before end of quarter" framing in the prompt would directly trigger the deadline and commercial signal questions.
- [x] PASS: Output explicitly identifies a critical path and gives a minimum timeline range rather than a single point estimate — met. §"Estimate Effort and Identify Critical Path" requires a named critical path with an explicit illustrative example including a range: "Critical path: Product requirements → Architecture → Development → QA execution → Release. Minimum 6–8 weeks."
- [x] PASS: Output frames work for leads at the right level rather than instructing specialists directly — met. §"Delegate to Leads" gives the instruction: "tell the CPO 'we need a PRD for X', not 'write user stories for Y' (that's the CPO's job to break down further)."
- [x] PASS: Output sequences QA twice — QA Lead in planning and QA Engineer writing acceptance tests before development — met. The sequencing section calls out "QA involved TWICE" and places QA Lead in Step 1 and QA Engineer in Step 3, explicitly before development starts.
- [x] PASS: Output names specific edge cases or anti-requirements relevant to roles/permissions — met. §"Definition of Ready" requires "Edge cases identified — empty state, error state, boundary conditions documented" and "Anti-requirements stated — what we're deliberately NOT doing." Following these instructions for a roles and invitations feature would surface examples like last-admin removal, role downgrade behaviour, and invite expiry as mandatory DoR items.
- [x] PASS: Output flags data-engineering and analytics work rather than treating it as implicit — met. The CTO workstream decomposition explicitly includes "Data: Event tracking, analytics, dashboards." The RATSI "Data & Analytics" table assigns event tracking plan ownership to the data engineer with product owner as a supporting input on what to track.
- [~] PARTIAL: Output flags agents referenced in the plan that exist in the marketplace but may not be enabled, with the `"<plugin>@hpsgd": true` enablement hint — partially met. Pre-Flight Step 3 and the "Flag inactive agents in dispatch plans" section describe this exact pattern with the correct hint format. Whether it fires depends on runtime state from settings.json — the mechanism is fully defined, execution depends on what the coordinator finds when it reads the file.
- [~] PARTIAL: Output distinguishes Definition of Ready from Definition of Done as separate checkpoints in the plan — partially met. Both sections exist and are clearly distinct (DoR = gate before development; DoD = gate before shipping), with "What Done does NOT include" further separating launch from done. The PARTIAL reflects that the definition does not explicitly direct the coordinator to surface both as named gates in the dispatch plan structure — it describes the criteria but the sequencing section does not label where each gate falls.
- [~] PARTIAL: Output surfaces likely CPO/CTO trade-offs to watch for without picking a side — partially met. §"Common conflicts" enumerates scope-vs-deadline, build-vs-buy, and security-vs-timeline — all directly relevant (invitations/email is a build-vs-buy candidate; roles/auth surfaces security-vs-timeline). The definition describes these patterns. The PARTIAL reflects that conflict resolution is framed reactively (when leads disagree) rather than as proactive flagging at plan time before disagreements materialise.
- [x] PASS: Output names a release/launch coordination step distinct from "done" — met. §"What 'Done' does NOT include" carves out production deployment, GTM/launch activities, and customer communication as separate from done. The sequencing section has a dedicated Step 5 (content, GTM, support preparation) and Step 6 (launch) following QA execution, with the Release Manager owning go/no-go per the RATSI.

## Notes

The definition scores 92.5% and the PARTIAL verdict is tight — one more half-point on security specificity or trade-off proactivity would bring it to PASS. The security PARTIAL reflects a structural gap: the definition lists security as a workstream but does not contain a heuristic to flag auth/roles/multi-tenancy as elevated-risk patterns warranting an early threat model rather than a later one.

The conflict resolution instructions are reactive by design (Coordinator steps in when CPO and CTO disagree), but for a plan this complex, anticipating likely trade-offs at dispatch time would be more valuable than knowing how to handle them after they surface. This is the most actionable improvement the definition could make.

The RATSI matrix is thorough and the QA Lead vs QA Engineer distinction is one of the clearest role boundary definitions in the codebase. The duplicate "Step 5" numbering in the sequencing and DoR sections is a cosmetic error that does not affect behaviour.
