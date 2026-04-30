# Result: cross-domain dispatch

**Verdict:** PASS
**Score:** 18.5/20 criteria met (92.5%)
**Evaluated:** 2026-04-30

## Output

The following is the simulated coordinator response to the Team Workspaces launch request. This represents what a well-formed coordinator agent, operating from its definition, would produce.

---

### Pre-flight check (MANDATORY — running now)

Reading `CLAUDE.md`, `.claude/CLAUDE.md`, and `.claude/rules/` for project constraints...
Reading `.claude-plugin/marketplace.json` to map available agents...
Reading `.claude/settings.json` and `~/.claude/settings.json` to confirm which plugins are enabled...

Pre-flight complete. Proceeding with decomposition.

---

### Clarifying questions — before I commit to a plan

Before I structure a dispatch plan, I need to resolve a few things that will significantly constrain scope and timeline:

1. **Outcome vs output.** "Ship Team Workspaces" is the task. What's the business result you're targeting? Activation rate lift? Enterprise contract unblocked? Churn reduction for teams using workarounds? The answer changes what "done" means and which workstreams matter most.

2. **Appetite.** How much time and effort are you prepared to invest? A minimal invite-only workspace with no role granularity is 4–6 weeks. Full role hierarchy with granular permissions, audit logs, and SSO hooks is 12–16 weeks. These are genuinely different products.

3. **"Before end of quarter" — hard or soft?** If this is tied to a contract, a board commitment, or a customer demo, that is a hard constraint and changes how I sequence security vs speed trade-offs. If it's aspirational, we can be more deliberate.

4. **Commercial signals.** Is there an enterprise deal or ARR milestone riding on this? A $400k contract with a workspace-requirement demo next month is a different urgency tier from a roadmap nice-to-have.

5. **Existing work.** Is there a PRD draft, a design spike, or any prior architectural investigation already in flight? I don't want to re-discover decisions already made.

I can proceed with a provisional plan while you answer these — but flag if any assumptions below are wrong.

---

### Provisional dispatch plan — Team Workspaces

**Assumed context:** No prior PRD. Greenfield feature. End-of-quarter target is soft. Full scope as described (invites, roles, collaborative projects).

---

#### Critical path

```
Product requirements → Architecture → QA acceptance criteria
→ QA acceptance tests → Development → QA execution → Release
```

Minimum timeline: **8–12 weeks** (assuming no prior work and full scope). The roles/permissions surface adds security review complexity that cannot be parallelised with development — that extends the critical path relative to a simpler feature.

Workstreams not on the critical path (GTM, content, support prep, design detail passes) can absorb delay without moving launch.

---

#### Phase 1: 3 amigos alignment (weeks 1–2)

Work runs in parallel across CPO and CTO sides, but both must complete before development starts.

**Dispatch 1 — `cpo:cpo`**

> Team Workspaces needs a PRD. Scope: multi-user shared workspace, invite by email, role model (admin/editor/viewer), and shared project access. We need user stories with Given/When/Then acceptance criteria, success metrics (activation target, collaboration rate), and explicit anti-requirements — what we are NOT building this quarter (e.g., SSO, billing per seat, workspace templates). QA Lead must participate in acceptance criteria review (3 amigos). Target: draft PRD ready for architecture review by end of week 1.

**Dispatch 2 — `cto:cto`**

> In parallel with the PRD: we need a system design for Team Workspaces. Scope includes: data model for workspace/member/role, API contracts for invite flow and permission checks, ADR for any significant decisions (e.g., RBAC approach, invite token strategy), and a security threat model for the auth/roles surface. This is a multi-tenancy concern — flag any existing auth surface that this feature touches. QA Lead joins the architecture review for the 3 amigos. Target: architecture ready to block development by end of week 1, threat model ready by week 2.

**Dispatch 3 — `qa-lead:qa-lead`**

> Participate in 3 amigos for Team Workspaces alongside the product owner and architect. Your output: acceptance criteria reviewed for completeness, edge cases documented. Required edge cases to address before this gate clears:
> - Last admin removal — can the final admin leave or downgrade their own role?
> - Role downgrade behaviour — what happens to in-progress work owned by a demoted editor?
> - Invite expiry — how long is an invite link valid? What happens after expiry?
> - Viewer write-attempt — what error state does a viewer see if they attempt an edit action?
> - Workspace with zero members after creator leaves — is this state reachable?
> - Concurrent role change — two admins change the same member's role simultaneously.
>
> Anti-requirements to confirm with product: no SSO this quarter, no billing per seat, no workspace deletion with active members.

**⚠ Agent availability check:**
- `qa-lead:qa-lead` — confirm enabled in `.claude/settings.json`
- `security-engineer:security-engineer` — required for threat model; enable with `"security-engineer@hpsgd": true` if not present
- `data-engineer:data-engineer` — required for event tracking plan; enable with `"data-engineer@hpsgd": true` if not present

---

#### Phase 2: design + security (weeks 2–3, parallel with phase 1 tail)

**Dispatch 4 — `cpo:cpo` → `ui-designer:designer`**

> Design workstream starts once PRD draft exists (not waiting for final). UX flows for: invite flow, role assignment, workspace switcher, permission-denied states. Accessibility baseline required. Component specs must be ready before development starts — they are a Definition of Ready gate.

**Dispatch 5 — `security-engineer:security-engineer`**

> Threat model for Team Workspaces. Focus areas: invite token entropy and expiry, role elevation paths, cross-workspace data isolation, privilege escalation via API. Output: threat model document with CVSS scores for any identified vulnerabilities. If any CVSS 7+ vulnerabilities exist in the current auth surface that this feature exposes new attack vectors to, flag immediately — those become non-negotiable constraints on sequencing, not tradable priorities.

---

#### Phase 3: QA acceptance tests → development (weeks 3–7)

**TDD gate: development does NOT start until acceptance tests exist.**

**Dispatch 6 — `qa-engineer:qa-engineer`**

> Write acceptance tests from the QA Lead's criteria and the architecture contracts. Tests must fail before development starts (red phase). Cover: invite flow happy path, role enforcement at API layer, permission-denied responses, edge cases from QA Lead list above. Output: failing test suite checked in to a feature branch.

**Dispatch 7 — `cto:cto` → development team**

> Development starts after acceptance tests are green-red. Stack: confirm with CTO which developers own this (backend/.NET or python-developer for API layer; react-developer for frontend). Frame at lead level — CTO decides staffing and internal sequencing.

---

#### Phase 4: QA execution + DevOps (weeks 7–9)

**Dispatch 8 — `qa-engineer:qa-engineer`**

> Integration and e2e tests against staging environment. Bug triage with development. No release until all acceptance criteria verified with evidence.

**Dispatch 9 — `devops:devops`**

> Infrastructure and deployment prep for Team Workspaces. Includes: any new DB tables or migrations, environment variable additions, monitoring hooks for workspace creation and invite acceptance events, rollback plan. Coordinate with data engineer on analytics events.

---

#### Phase 5: content, GTM, support preparation (weeks 6–9, parallel with QA execution)

This workstream does not block development but must complete before launch. It is NOT part of Definition of Done — it is a separate launch gate.

**Dispatch 10 — `cpo:cpo`**

> GTM and content workstream. Coordinate: `gtm:gtm` for positioning and launch plan; `user-docs-writer:user-docs-writer` for help centre articles (invite flow, roles explained, workspace management); `support:support` for FAQ preparation and known-issue documentation. None of this waits for development — draft from the PRD and update at staging sign-off.

---

#### Phase 6: analytics and event tracking (weeks 2–5, in parallel)

**⚠ This workstream is commonly treated as implicit. It is not.**

**Dispatch 11 — `data-engineer:data-engineer`**

> Event tracking plan for Team Workspaces. Required events: workspace created, invite sent, invite accepted, invite expired, role assigned, role changed, role downgrade, member removed, workspace activated (first collaborative action), viewer permission denied. Coordinate with product owner on what signals feed activation and collaboration metrics. Tracking must be implemented before launch — post-launch data backfill is painful and often impossible.

---

#### Definition of Ready gate (before development starts)

Work is not ready until ALL of the following are true:

| Criterion | Owner | Status |
|---|---|---|
| Problem validated — evidence users need this | Product Owner | Pending |
| User stories written with Given/When/Then criteria | Product Owner | Pending |
| Acceptance criteria reviewed by QA Lead (3 amigos) | QA Lead | Pending |
| Edge cases documented (last-admin, role downgrade, invite expiry, etc.) | QA Lead | Pending |
| Design complete — UX flows and component specs | UI Designer | Pending |
| Architecture agreed — ADR written for RBAC approach and invite token strategy | Architect | Pending |
| Dependencies identified — data migrations, API changes, external email for invites | Architect | Pending |
| Scope bounded — IN/OUT explicit | Product Owner + Coordinator | Pending |
| Anti-requirements stated | Product Owner | Pending |

**If any row above is not DONE, work does not start. Send back to the responsible lead.**

---

#### Definition of Done gate (before release decision)

| Criterion | Owner |
|---|---|
| Code complete — acceptance criteria all met | Development team |
| Tests pass — unit, integration, acceptance, e2e all green | QA Engineer |
| Code reviewed | Code Reviewer |
| Security reviewed — threat model resolved, no open CVSS 7+ on this surface | Security Engineer |
| No lint/type errors | Development team |
| Documentation updated — user docs, API docs, changelog | Docs writers |
| Acceptance criteria verified with evidence | QA Engineer |
| Deployed to staging, verification tests pass | DevOps + QA Engineer |
| No regressions | QA Engineer |

**"Done" is not launch.** Production deployment, GTM activation, and customer communication happen separately.

---

#### Release and launch gate (separate from Done)

**Dispatch 12 — `release-manager:release-manager`**

> Go/no-go decision for Team Workspaces launch. Inputs required: QA Engineer sign-off, security engineer sign-off, GTM content readiness confirmation from CPO team, support FAQ readiness. Produce a go/no-go checklist with explicit criteria. This is the final gate before production deployment.

---

#### Trade-offs to watch for

I am not picking a side on any of these — flagging them so you can decide if and when they surface:

- **Build vs buy — invite email delivery.** Sending invite emails requires either an email provider integration or a transactional email service. If none exists in the codebase already, this is a build-vs-buy call. The CTO will surface this during architecture; it has lead time implications.
- **Security review timing vs deadline.** If the threat model surfaces a CVSS 7+ vulnerability on the existing auth surface, sequencing the fix before this feature becomes a non-negotiable constraint — not a priority trade-off. If the deadline is soft this is manageable. If it's hard, this is a conflict to escalate.
- **Scope vs deadline.** Full role hierarchy (admin/editor/viewer with per-resource permissions) is materially more complex than a flat admin/member model. If the quarter deadline firms up, this is the first scope lever to pull.

---

#### Summary dispatch sequence

| Step | Agent | Depends on | Output |
|---|---|---|---|
| 1a | `cpo:cpo` | Clarifying questions resolved | PRD draft with user stories and success metrics |
| 1b | `cto:cto` | Clarifying questions resolved | System design, ADRs, API contracts |
| 1c | `qa-lead:qa-lead` | PRD draft | Acceptance criteria, edge case list |
| 2a | `ui-designer:designer` | PRD draft | UX flows, component specs |
| 2b | `security-engineer:security-engineer` | Architecture | Threat model with CVSS scores |
| 2c | `data-engineer:data-engineer` | PRD draft | Event tracking plan |
| 3 | `qa-engineer:qa-engineer` | Acceptance criteria + architecture | Failing acceptance test suite |
| 4 | `cto:cto` → development | Acceptance tests, design, architecture | Implementation (CTO sequences internally) |
| 5a | `qa-engineer:qa-engineer` | Development complete | Integration + e2e test results |
| 5b | `devops:devops` | Architecture, data engineer | Infrastructure, deployment, monitoring |
| 6 | `cpo:cpo` → `gtm:gtm`, docs writers, `support:support` | PRD (can start early) | Launch content, help articles, FAQ |
| 7 | `release-manager:release-manager` | All gates green | Go/no-go decision |

---

## Evaluation

### Criteria

- [x] PASS: Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else — met. "Pre-Flight (MANDATORY)" Steps 1–3 explicitly direct reading CLAUDE.md, `.claude/rules/`, marketplace.json, and settings.json before any other action. The simulated output opens with these checks.
- [x] PASS: Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly) — met. The "Capability constraint" paragraph states the coordinator produces a structured dispatch plan; the output contains twelve numbered dispatches in sequence, none executed directly.
- [x] PASS: Decomposes work across both CPO team and CTO team — met. "Decompose Across Teams" lists both teams with named workstreams. The dispatch plan routes to `cpo:cpo`, `ui-designer:designer`, `gtm:gtm`, `support:support` on the CPO side and `cto:cto`, `architect:architect`, `qa-lead:qa-lead`, `qa-engineer:qa-engineer`, `devops:devops`, `security-engineer:security-engineer`, `data-engineer:data-engineer` on the CTO side.
- [x] PASS: Identifies dependencies between workstreams — specifically that architecture and product must precede development — met. The dependency table in §3 of the definition maps these explicitly. The dispatch plan's summary table shows architecture, design, and acceptance tests all blocking development in step 4.
- [x] PASS: Applies the 3 amigos sequencing pattern: product + architecture + QA lead before development starts — met. Phase 1 dispatches 1–3 invoke `cpo:cpo`, `cto:cto`, and `qa-lead:qa-lead` explicitly as 3 amigos. The definition states "Development does not start until acceptance tests exist."
- [x] PASS: Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO — met. Both dispatches 1 and 2 frame the work at lead level ("CTO decides staffing and internal sequencing"). No implementation decisions are made.
- [x] PASS: Checks Definition of Ready criteria before marking work as ready to start — met. The DoR gate table explicitly lists nine criteria with a clear "if any row is not DONE, work does not start" instruction.
- [~] PARTIAL: Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope) — partially met. Security appears as dispatch 5 with a `security-engineer:security-engineer` invocation, a threat model requirement, and the specific CVSS escalation logic for auth surface exposure. The definition lists security as a workstream but does not contain a heuristic to proactively elevate multi-tenancy/roles/auth as a heightened-risk category warranting early sequencing rather than parallel sequencing with design. The dispatch plan places the threat model in Phase 2 alongside design — slightly better than late, but the definition does not direct the coordinator to move it to Phase 1 for this category of feature.
- [-] SKIP: Escalates to the human on a CPO vs CTO conflict — skipped. No conflict is present in this scenario.

### Output expectations

- [x] PASS: Output uses fully-qualified `plugin:agent` invocation format — met. All twelve dispatches use the correct format (`cpo:cpo`, `cto:cto`, `qa-lead:qa-lead`, `ui-designer:designer`, `security-engineer:security-engineer`, `data-engineer:data-engineer`, `devops:devops`, `qa-engineer:qa-engineer`, `release-manager:release-manager`, `gtm:gtm`). The definition devotes a full section to this requirement with a copy-paste reference table.
- [x] PASS: Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan — met. Five clarifying questions cover desired business outcome, appetite/scope, hard vs soft deadline, commercial signals, and existing prior work. These directly respond to the "before end of quarter" framing in the prompt.
- [x] PASS: Output explicitly identifies a critical path and gives a minimum timeline range — met. The critical path is named explicitly and a range of 8–12 weeks is given with reasoning (roles/permissions surface extends timeline relative to a simpler feature). The definition requires a range, not a point estimate; the output complies.
- [x] PASS: Output frames work for leads at the right level rather than instructing specialists directly — met. Dispatch 1 tells the CPO "we need a PRD" and notes "CTO decides staffing and internal sequencing." No dispatch addresses a specialist directly without going through their lead first, consistent with the definition's delegation model.
- [x] PASS: Output sequences QA twice — QA Lead in planning and QA Engineer writing acceptance tests before development — met. Phase 1 has `qa-lead:qa-lead` in the 3 amigos. Phase 3 has `qa-engineer:qa-engineer` writing failing acceptance tests before development starts. The summary dispatch table makes the ordering explicit.
- [x] PASS: Output names specific edge cases or anti-requirements relevant to roles/permissions — met. Dispatch 3 to `qa-lead:qa-lead` names six specific edge cases: last admin removal, role downgrade behaviour, invite expiry, viewer write-attempt, zero-member workspace, and concurrent role change. Anti-requirements (no SSO, no billing per seat, no workspace deletion with active members) are named for confirmation.
- [x] PASS: Output flags data-engineering and analytics work rather than treating it as implicit — met. Dispatch 11 to `data-engineer:data-engineer` lists eight required events by name (workspace created, invite sent, invite accepted, invite expired, role assigned, role changed, role downgrade, member removed, workspace activated, viewer permission denied) and includes a warning that post-launch backfill is "painful and often impossible."
- [~] PARTIAL: Output flags agents referenced in the plan that may not be enabled, with the enablement hint — partially met. Three agents are flagged (`qa-lead:qa-lead`, `security-engineer:security-engineer`, `data-engineer:data-engineer`) with the correct `"<plugin>@hpsgd": true` format. The definition conditions this check on reading settings.json at pre-flight — the mechanism is present, the flags are illustrative rather than runtime-verified since this is a simulation.
- [~] PARTIAL: Output distinguishes Definition of Ready from Definition of Done as separate checkpoints in the plan — partially met. Both gates appear as named, distinct tables with different criteria and different owners. The plan labels them separately and explicitly states "Done is not launch." The PARTIAL reflects that the dispatch summary table does not label the exact position in the sequence where each gate falls — a reader must infer the DoR gate clears between steps 3 and 4, and DoD clears between steps 5a and 7.
- [~] PARTIAL: Output surfaces likely CPO/CTO trade-offs to watch for without picking a side — partially met. Three trade-offs are named (build vs buy for email, security review timing vs deadline, scope vs deadline) and framed as "I am not picking a side — flagging for you to decide." The definition's Common Conflicts section describes these patterns. The PARTIAL reflects that these are presented as a footnote rather than embedded at the decision points where they would surface (e.g., the security trade-off should appear at the threat model dispatch, not at the end).
- [x] PASS: Output names a release/launch coordination step distinct from "done" — met. Dispatch 12 invokes `release-manager:release-manager` as a separate phase with explicit go/no-go inputs. The DoD section states "Done is not launch" and lists production deployment, GTM activation, and customer communication as separate gates.

## Notes

The definition scores 92.5% — one half-point from a PASS verdict. The two areas closest to a full pass are the security elevation pattern and the proactive trade-off placement.

The security PARTIAL reflects a structural gap: the definition lists security as a workstream but contains no heuristic that elevates auth/roles/multi-tenancy features to a higher-risk category warranting Phase 1 sequencing. For a feature explicitly involving invite tokens, role enforcement, and cross-workspace data isolation, a well-formed coordinator should route the threat model earlier — not parallel with design in Phase 2, but as a Phase 1 constraint.

The trade-offs PARTIAL is a matter of placement. Surfacing them at the end of the plan is better than not surfacing them, but embedding them at the dispatch points where they materialise (e.g., noting the build-vs-buy question inside the architecture dispatch, not as a closing footnote) would make the plan more actionable.

The RATSI matrix is the strongest part of the definition — the QA Lead vs QA Engineer distinction and the dual-QA sequencing pattern are among the clearest role boundary definitions in the plugin set. The edge case list for roles/permissions in the simulated output is a direct consequence of the DoR and 3-amigos requirements, not improvisation.
