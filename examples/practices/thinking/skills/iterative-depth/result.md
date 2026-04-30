# Result: iterative-depth architecture decision analysis

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Skill source** | `plugins/practices/thinking/skills/iterative-depth/SKILL.md` |

## Output

The following is a simulated invocation of `/iterative-depth Should we extract the notification subsystem from our Rails monolith into a separate service? It currently handles email, push, and SMS. It has 8,000 lines, 3 engineers have touched it in the past 6 months, and it's the source of 40% of our production incidents. We deploy the whole monolith weekly.`

---

## Step 1 — Frame the problem

```
Problem: Decide whether to extract the notification subsystem (email, push, SMS) from a
         Rails monolith into a separate service, or address its instability in place.

Context: The notification subsystem is the single largest contributor to production
         incidents (40%). Weekly monolith deploys mean a bad notification change can
         take down unrelated features, and vice versa. Three engineers have touched it
         in 6 months — high enough bus factor to retain context but concentrated enough
         to create ownership ambiguity.

Constraints:
  - Monolith deploy cycle is weekly, which gates all teams equally
  - Extraction adds operational complexity the team doesn't currently carry
  - Unknown: whether the 40% incident rate is caused by notification logic itself or
    by integration points between notifications and the rest of the monolith
  - Budget and timeline not specified

Stakeholders:
  - End users: affected by failed notifications (missed OTPs, delivery failures)
  - Engineering team: absorbs incident response load and any extraction effort
  - Product: deploys blocked when notification bugs require a rollback
  - Operations: would own an additional service if extraction proceeds

Current state:
  - Monolith containing an 8,000-line notification subsystem (email, push, SMS)
  - Weekly full-monolith deploys
  - 40% of production incidents trace here
  - Three engineers with recent context

Desired state:
  - Notification incidents are isolated and don't block other features
  - Notification defect rate falls significantly
  - Team has clear ownership and deploy autonomy for this domain
```

---

## Step 2 — Select lenses

**Selected lenses: Technical, Operational, Team, Business, Simplicity**

| Lens | Why chosen |
|---|---|
| **Technical** | Extraction is a technical decision: API contracts, data ownership, service communication, migration path. Can't skip it. |
| **Operational** | The 40% incident figure is an operational problem. Extraction changes blast radius and failure surface. The lens surfaces whether extraction solves or moves the problem. |
| **Team** | Only 3 engineers have touched this in 6 months. Extraction changes their working model significantly — ownership, on-call, deploy autonomy. This is a team-health decision as much as a technical one. |
| **Business** | 40% of incidents has a cost: SLA risk, engineer time on-call, product velocity blocked. The extraction investment needs to be weighed against the in-place fix alternative. |
| **Simplicity** | The "extract it" instinct is a common response to a messy module. Simplicity lens asks whether extraction is the simplest lever or whether the same outcome is achievable without it. |

Lens selection rules satisfied: Business + Team = human lenses; Technical + Operational = system lenses.

---

## Step 3 — Analyse through each lens

### Lens 1: Technical

**Focus question:** What does extraction actually cost, what do you get, and what hard problems does it create?

**Analysis:**

*Sub-question 1: What is the extraction effort?*
An 8,000-line subsystem handling three channels likely has: shared ActiveRecord models (users, preferences, subscriptions), direct database access, shared background job infrastructure (Sidekiq), and inline calls from other parts of the monolith. Extraction requires identifying and severing all of these. Conservative estimate: 6-10 engineer-weeks to extract cleanly, plus time for a parallel-run validation period. The monolith will need an HTTP/async client where direct calls used to be.

*Sub-question 2: What communication mechanism would replace direct calls?*
Options: synchronous HTTP (simplest, adds latency and network failure risk), async messaging (RabbitMQ/Kafka — reliable, adds infra and ops complexity), or a shared event bus already in the stack (if one exists). The choice changes the operational profile entirely. Async messaging is the right pattern for notifications (fire-and-forget acceptable for most cases) but requires the team to learn it if they don't already have it.

*Sub-question 3: What happens to shared data?*
Notification preferences and delivery logs are likely in the monolith's database. Extraction forces a data ownership decision: does the notification service get its own database, or does it continue querying the monolith's DB? A separate database is architecturally correct but doubles the extraction effort. Shared database access defeats the purpose of extraction.

**Findings unique to this lens:**
1. Extraction cost is probably 2-3x higher than it appears: the surface area of a notification subsystem in a Rails monolith (shared models, background jobs, preferences, delivery logs) is wide, and most of it is invisible until you start cutting.
2. Communication mechanism choice is a hidden decision inside the extraction decision. Choosing synchronous HTTP converts a local function call failure into a network call failure, potentially making incident rate worse before it gets better.
3. The monolith codebase retains callers after extraction — those callers need to be updated to the new interface, which is a second migration workstream running in parallel with building the new service.

**Contradictions with previous lenses:**
- No previous lenses yet — this is the first.

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Underestimating extraction scope | High | High | Spike: spend 2 days mapping all callers and shared models before committing |
| Sync HTTP replacing direct calls degrades reliability | Med | High | Use async messaging from day one; accept the learning curve |
| Shared DB access as a shortcut | Med | High | Hard rule: new service gets its own DB or it's not a real extraction |

**Open questions:**
- Does the team currently operate any async messaging infrastructure?
- How many call sites in the monolith reference notification functionality directly?

---

### Lens 2: Operational

**Focus question:** Does extraction reduce the blast radius of notification incidents, or does it change the failure surface in ways that make things harder?

**Analysis:**

*Sub-question 1: What is the current failure mode?*
In a monolith, a notification bug (memory leak in email rendering, Sidekiq queue backup, third-party API timeout) can exhaust shared resources — database connection pool, Sidekiq workers, memory — and affect unrelated features. The 40% incident rate likely includes both pure notification failures and collateral failures caused by resource contention.

*Sub-question 2: What is the failure mode post-extraction?*
A separate service means notification failures stay in their blast radius — they don't exhaust the monolith's connection pool. However, the inter-service communication layer becomes the new failure surface. A notification service that goes down means the monolith callers need circuit breakers and graceful degradation ("send notification failed, but the user's action still completed"). Without this, extraction moves the failure from "notification brings down the app" to "notification timeout brings down the app via a different path."

*Sub-question 3: What does deploy frequency look like post-extraction?*
With an independent service, the notification team can deploy independently — daily if they want. This is a significant operational win, but it also means the notification service must maintain its own deployment pipeline, monitoring, alerting, and on-call rotation.

**Findings unique to this lens:**
1. The 40% incident figure needs decomposition before extraction is justified. If 30 of those 40 points are resource-contention spillover (notification queue backs up and takes the connection pool), extraction eliminates them. If they're pure notification logic bugs, extraction doesn't reduce the incident rate — it just changes who gets paged.
2. Circuit-breaker and graceful-degradation patterns on the calling side of the monolith are mandatory, not optional. Without them, extraction adds a new class of distributed systems failures on top of the existing notification bugs.
3. Deploy independence is a double-edged win: faster iteration for notifications, but also the operational burden of running and monitoring an additional service — currently not priced into the decision.

**Contradictions with previous lenses:**
- Technical lens focused on extraction cost (effort, migration). Operational lens reveals that even a successful extraction doesn't reduce the incident rate unless the root causes are resource-contention — not a conclusion reachable from the technical lens alone.

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Extraction proceeds without root-cause analysis of the 40% | High | High | 2-week incident review before committing to extraction vs fix-in-place |
| Callers in monolith lack circuit breakers post-extraction | High | Med | Add circuit-breaker wrappers as part of extraction, not after |
| Monitoring gap during transition | Med | Med | Parallel-run period with both paths active and instrumented |

**Open questions:**
- What does the incident breakdown look like — resource contention vs logic bugs vs third-party failures?
- Does the team have experience running and monitoring a separate service?

---

### Lens 3: Team

**Focus question:** How does extraction change the working reality for the three engineers who own this area?

**Analysis:**

*Sub-question 1: What does ownership look like today?*
Three engineers have touched the code in 6 months — but in a monolith with no formal ownership model, "touched" may mean different things: one may be the domain expert, one may have fixed a bug, one may have added a field. Effective ownership is probably narrower. Extraction forces an explicit ownership decision: who is on-call for the notification service, who reviews its PRs, who sets its roadmap.

*Sub-question 2: Is the team's operational maturity ready for a separate service?*
Running a separate service means: a dedicated deploy pipeline, separate monitoring dashboards, a separate on-call schedule, SLO ownership, and incident runbooks specific to the service. If the team currently operates only a monolith, they're taking on all of this simultaneously while also extracting. That's a significant capability uplift, not just a code migration.

*Sub-question 3: Does the team want this?*
This sounds like a process question but it's a risk question. Engineers who feel a service was imposed on them rather than chosen will under-invest in its reliability practices. The 40% incident rate is already a morale signal — engineers in this area are absorbing a lot of pain. Extraction could feel like relief (autonomy) or punishment (more to own).

**Findings unique to this lens:**
1. Ownership clarity is a valid benefit of extraction entirely independent of the technical architecture arguments. Even if the service were technically identical to the subsystem, having a named owner and independent deploy would reduce cognitive switching cost.
2. The team's operational maturity may be the binding constraint — not the technical extraction complexity. A poorly operated separate service will produce more incidents than the current monolith, not fewer.
3. The three engineers' career context matters: if they're junior-to-mid, adding service ownership may be growth-accelerating. If they're already stretched, it may be the last straw.

**Contradictions with previous lenses:**
- Technical lens says extraction takes 2-3x more effort than expected. Team lens adds: the effort isn't just code — it's capability building. The team needs to learn distributed systems operations, not just write the code. This multiplies the Technical lens estimate further.
- Operational lens says deploy independence is a win. Team lens says it's only a win if the team has the maturity to use it safely. If they don't, it's a liability.

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Team capability gap for service operations | Med | High | Pair with an experienced SRE during initial rollout; invest in runbooks before go-live |
| No clear ownership post-extraction | Med | Med | Name the service owner before starting — not after |
| Team morale deteriorates if extraction feels imposed | Med | Med | Include the engineers in the decision; their ground-level knowledge of the 40% is irreplaceable |

**Open questions:**
- What's the seniority and operational experience of the three engineers?
- Do they want this?
- Does the organisation have SRE support for new service rollouts?

---

### Lens 4: Business

**Focus question:** What is the cost of inaction vs the cost of extraction, and is there a cheaper path to the same outcome?

**Analysis:**

*Sub-question 1: What is the current cost of 40% incident origination?*
If the team has, say, 8 incidents per month (a plausible number for a production service with known instability), 3.2 of them trace to notifications. Each incident involves engineer time (detection, diagnosis, fix, post-mortem): conservatively 4 engineer-hours per incident. That's ~13 engineer-hours/month burned on notification incidents. At a fully-loaded engineer cost of ~$150/hour, that's roughly $2,000/month in direct incident cost, not counting product downtime and customer impact.

*Sub-question 2: What does extraction cost vs fix-in-place?*
Extraction at 6-10 engineer-weeks = 240-400 engineer-hours = $36,000-$60,000. Fix-in-place (targeted refactoring, better test coverage, dependency cleanup, queue isolation) might take 3-5 weeks = $18,000-$30,000. If fix-in-place reduces the incident rate by even 50%, payback period is 18-30 months. If extraction eliminates resource-contention incidents entirely, the payback period may be shorter — but only if the root-cause analysis supports that conclusion.

*Sub-question 3: What is the strategic value of independent deploys?*
Beyond incident reduction, deploy independence allows the notification team to ship improvements faster — new channel support, deliverability improvements, customer preference features. If notifications are on the product roadmap as a growth driver, the deploy independence has a value beyond incident reduction. If notifications are pure infrastructure ("make sure emails go out"), the strategic premium is lower.

**Findings unique to this lens:**
1. The business case for extraction depends entirely on the root-cause breakdown of the 40% that no other lens surfaced. Without that data, the investment decision is a coin flip dressed up as an architectural debate.
2. Fix-in-place is meaningfully cheaper and deserves formal consideration in the decision record. The pattern of "rewrite/extract to fix bugs" often repeats the same mistakes in a new location; disciplined in-place refactoring can achieve the same defect reduction at half the cost.
3. Deploy independence has a strategic value multiplier if notifications are a product growth area — that multiplier should be explicitly estimated, not assumed.

**Contradictions with previous lenses:**
- Technical and Team lenses both make extraction sound necessary. Business lens says it's conditional — if fix-in-place achieves the same reliability outcome at lower cost, extraction doesn't pass a business case unless the strategic value of independent deploys is quantified.

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Decision made without root-cause data | High | High | Mandatory 2-week incident analysis before commit |
| Fix-in-place ignored as an option | High | Med | Explicitly include it in the decision document as Option B |
| Strategic value of deploy independence assumed, not quantified | Med | Med | Product team to confirm roadmap priority of notification features |

**Open questions:**
- What is the current incident cost in engineer-hours per month?
- What is the notification feature roadmap — infrastructure only, or growth driver?

---

### Lens 5: Simplicity

**Focus question:** What is the simplest path to fixing the reliability problem, and is extraction that path?

**Analysis:**

*Sub-question 1: What specifically is causing the 40%?*
If the root causes are: (a) poor test coverage of edge cases, (b) third-party API flakiness (email/SMS provider timeouts), (c) Sidekiq queue misconfiguration, or (d) a handful of known bugs that have never been fixed — then none of these require extraction. A targeted fix campaign over 3-4 weeks with a dedicated engineer could address all four without changing the architecture.

*Sub-question 2: Is the complexity of the module genuinely requiring extraction, or is it a maintenance problem?*
8,000 lines for a tri-channel notification subsystem is not small, but it's also not unusually large for the scope. The question is whether the code is 8,000 lines because the domain is complex, or because it's accumulated cruft. If it's cruft, a refactoring pass within the monolith is simpler than extraction and achieves the readability goals.

*Sub-question 3: What is the simplest version of extraction that still delivers the core benefit?*
If extraction proceeds, the simplest version might not be a full microservice. A "mailbox" pattern — where the monolith writes notification jobs to a shared queue and a lightweight worker consumes them — achieves blast-radius isolation without the full overhead of a service with its own database, API, and deployment pipeline. This captures most of the operational benefit at roughly half the extraction cost.

**Findings unique to this lens:**
1. A targeted fix campaign for the known root causes of the 40% may be available for less than half the cost of extraction, and should be formally documented as Option B before the team commits.
2. The 8,000-line size is not inherently a signal for extraction — it's a signal for a refactoring review. These are different interventions with different costs and outcomes.
3. If extraction is chosen, a lightweight consumer pattern (queue-based worker rather than full service) delivers most of the blast-radius benefit without the full operational overhead of a separate service.

**Contradictions with previous lenses:**
- Business lens quantified extraction cost vs fix-in-place at a high level. Simplicity lens adds a third option the Business lens didn't surface: partial extraction (queue-based consumer) that sits between "do nothing" and "full microservice" on the cost/benefit curve.
- Technical lens assumed full-service extraction as the frame. Simplicity lens challenges the frame itself.

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Partial extraction creates a worse hybrid — the worst of both worlds | Med | Med | Define clear boundaries upfront; partial extraction must have a completion path |
| Fix-in-place underinvested and same bugs recur | Med | Med | Fix-in-place option requires a structured refactor plan, not ad-hoc fixes |

**Open questions:**
- Have the root causes of the 40% incidents been formally documented?
- Is there appetite for a partial extraction (queue-based) as a stepping stone?

---

## Step 4 — Synthesise

### Convergent findings

| Finding | Supported by lenses | Confidence | Implication |
|---|---|---|---|
| The 40% incident figure needs root-cause decomposition before the decision | Operational, Business, Simplicity | High | A 2-week incident analysis is a prerequisite for this decision, not a nice-to-have |
| Fix-in-place is a valid option and must be formally considered | Business, Simplicity | High | The decision document must compare at least three options: extract fully, fix-in-place, partial extraction |
| Circuit breakers and graceful degradation are mandatory if extraction proceeds | Technical, Operational | High | They are not a post-launch addition — they must be part of the extraction design |
| Team operational maturity is a binding constraint on extraction success | Team, Operational | Medium | If the team lacks distributed systems ops experience, extraction is high-risk regardless of technical soundness |
| Deploy independence is a real benefit, but conditional on team readiness | Operational, Team, Business | Medium | The benefit is real but not unconditional — it requires investment in tooling and capability |

### Tensions and trade-offs

| Tension | Technical + Team says | Operational + Business says | Recommended resolution | Rationale |
|---|---|---|---|---|
| Extraction effort vs reliability benefit | Extraction is expensive and complex | The reliability benefit is conditional on root-cause type | Do the incident root-cause analysis first. If contention spillover is ≥50% of incidents, proceed with extraction. If not, fix-in-place first. | Making a $50k investment without this data is unjustifiable. |
| Full microservice vs partial extraction | Full extraction is architecturally clean | Partial extraction (queue consumer) achieves most of the blast-radius benefit at half the cost | Start with partial extraction as a staging point | Keeps options open; delivers measurable reliability improvement faster; lower capability requirement on team. |
| Autonomy benefit vs operational burden | Team ownership is a benefit | New operational burden may exceed the benefit for an under-experienced team | Only proceed with full extraction if an SRE or senior engineer is available for the rollout period | The autonomy benefit evaporates if the team is underwater with new operational tasks. |

### Blind spots filled

| Blind spot | Revealed by | Would have caused | Prevention |
|---|---|---|---|
| Root-cause decomposition of the 40% | Operational | Investment in extraction that doesn't reduce incident rate | Incident review as standard pre-requisite for reliability-motivated architectural changes |
| Partial extraction as a middle option | Simplicity | Binary framing (extract or don't) that misses the lower-cost path | Always apply Simplicity lens to architectural decisions; challenge the frame before accepting it |
| Team operational maturity as a binding constraint | Team | A technically correct extraction that produces more incidents due to operational gaps | Include team capability assessment in any architectural decision with operational consequences |

### Revised problem framing

```
Original framing: Should we extract the notification subsystem into a separate service?

Revised framing: We have a notification subsystem responsible for 40% of production incidents.
                 Before committing to extraction, we need to know whether those incidents are caused
                 by resource-contention spillover (which extraction solves) or by notification logic
                 bugs (which extraction moves but doesn't fix). That root-cause data determines
                 which of three options is appropriate: full extraction, targeted fix-in-place, or
                 partial extraction via a queue-based consumer pattern. The decision also depends on
                 whether the team has the operational maturity to run an independent service and
                 whether notifications are a product growth area (which changes the strategic value
                 of deploy independence).

Key difference: The original framing treated extraction as the question. The revised framing treats
                the 40% incident rate as the question — extraction is one of three possible answers,
                conditional on data we don't yet have.
```

### Refined success criteria

| Criterion | Source lens | Metric | Threshold |
|---|---|---|---|
| Incident rate from notification origin | Operational, Business | Incidents/month traceable to notifications | ≤50% reduction within 3 months of intervention |
| Monolith blast radius from notification failures | Operational | Incidents where notification failure cascades to unrelated features | Zero within 1 month of intervention |
| Deploy independence (if extraction proceeds) | Team, Business | Time from code-complete to notification deploy | ≤1 day (vs current weekly monolith cycle) |
| Team operational load | Team | Mean time to detect/resolve notification incidents | ≤50% of current MTTR |
| Extraction cost vs estimate | Technical, Business | Actual engineer-weeks vs estimate | Within 20% of estimate |

### Recommendation

```
Recommendation: Do not commit to full extraction yet. Spend 2 weeks on an incident root-cause analysis.
                Based on that data, choose from three options in order of preference:

                Option A (if ≥50% of incidents are resource-contention spillover):
                  Proceed with partial extraction — queue-based consumer pattern that isolates
                  notifications from the monolith's resource pool. Full microservice can follow once
                  the team builds operational experience with the simpler pattern.

                Option B (if <50% of incidents are resource-contention, majority are logic bugs):
                  Fix-in-place with a structured 3-4 week refactoring campaign targeting root causes.
                  Reassess extraction after 3 months of incident data.

                Option C (if notifications are a confirmed product growth area with roadmap investment):
                  Full extraction is justified regardless of the root-cause split, because deploy
                  independence has strategic value. Proceed only with SRE/senior support during rollout.

Confidence: MEDIUM — based on the problem statement data (40% incidents, 8,000 lines, 3 engineers,
            weekly deploys). Would rise to HIGH if: (a) incident root-cause analysis confirms
            contention spillover as the dominant cause, and (b) the team has operated at least one
            independent service before. Would remain LOW if the incident analysis shows the 40% is
            predominantly logic bugs with no contention component — in that case extraction is not the
            right lever.

Key risks:
  1. Decision made without root-cause data → mitigate by treating the 2-week analysis as mandatory,
     not optional
  2. Partial extraction starts but is never completed → mitigate by defining completion criteria
     before starting and committing to a timeline
  3. Team operational capability gap → mitigate by securing SRE support before committing to any
     extraction path

Next steps:
  1. Assign one engineer to a 2-week structured incident review — classify each notification incident
     by root cause (contention spillover, logic bug, third-party failure, other)
  2. Have the product team confirm whether notifications are on the growth roadmap or infrastructure-only
  3. Based on (1) and (2), bring a formal decision to the team with all three options documented,
     cost-estimated, and mapped to the root-cause data

What would change this recommendation:
  - If root-cause analysis shows ≥70% of incidents are contention spillover → move directly to
    partial extraction without further debate
  - If the product roadmap shows notifications as a growth area in the next 6 months → full extraction
    is justified; the strategic value changes the math
  - If the team already has experience operating a separate service → operational risk concern is
    significantly reduced; upgrade partial extraction recommendation to full extraction
  - If incident rate drops materially after a targeted fix campaign → defer extraction indefinitely
    and revisit only if a new architectural reason emerges
```

---

## Evaluation

### Criteria

- [x] PASS: Step 1 produces a complete problem framing with problem statement, context, constraints, stakeholders, current state, and desired state — met: the SKILL.md defines an explicit six-field code block template; all six fields are required before lens selection begins.

- [x] PASS: Step 2 selects 3-5 lenses from the eight available and states which were chosen and why — met: the skill instructs "Choose 3-5 lenses" and ends Step 2 with "State which lenses you selected and why." The simulated output selects 5 lenses with per-lens justification tied to this specific scenario.

- [x] PASS: Lens selection includes at least one human lens (User or Business) and one system lens (Technical or Edge case) per the skill's selection rules — met: the "Lens selection rules" subsection makes this a hard rule; Business + Team satisfy the human requirement, Technical + Operational satisfy the system requirement.

- [x] PASS: Each lens analysis produces at least one finding not surfaced by any previous lens — met: the per-lens template has a mandatory "Findings unique to this lens:" section; the rules state "Each lens must produce at least one finding not surfaced by any previous lens. If a lens adds nothing new, either the analysis was too shallow or the lens was a poor choice — go deeper or swap it." The simulated output produces distinct findings per lens.

- [x] PASS: Contradictions between lenses are explicitly called out — not smoothed over — met: the per-lens template requires a "Contradictions with previous lenses:" field; the rules state "Don't smooth over contradictions — highlight them." The simulated output surfaces explicit contradictions at each lens step.

- [x] PASS: Step 4 synthesis produces a convergent findings table, a tensions table with recommended resolutions, and a clear recommendation — met: Step 4 in the SKILL.md defines all three with explicit table schemas; each tensions row requires a "Recommended resolution" and "Rationale."

- [x] PASS: Revised problem framing at the end of Step 4 differs from the Step 1 framing in a meaningful way — met: the "Revised problem framing" subsection requires both original and revised framing plus a "Key difference" field; the simulated output shifts from "should we extract?" to "what is driving the 40% and which of three options is appropriate."

- [~] PARTIAL: Confidence level for the recommendation is stated with the evidence basis — partially met: the recommendation template includes "**Confidence:** [High / Medium / Low] — based on [what evidence]" and a "**What would change this recommendation:**" section. The simulated output states "MEDIUM — based on..." and explicitly names conditions that would raise it to HIGH or leave it LOW. The gap: the template prompt says "based on [what evidence]" but doesn't explicitly model the MEDIUM → HIGH transition as a named pattern; the "What would change this recommendation" section fills this functionally.

### Output expectations

- [x] PASS: Output's problem framing reproduces the prompt's specific facts — 8,000 lines, 3 engineers in 6 months, 40% of incidents, weekly deploys, three channels — met: all five specific facts appear in the Step 1 framing and are referenced in lens analyses.

- [x] PASS: Output selects 3-5 lenses and names them with explanation of why each was chosen for THIS decision — met: five lenses named with scenario-specific justification in a table.

- [x] PASS: Output's lens selection includes at least one human lens AND one system lens — met: Business + Team (human), Technical + Operational (system).

- [x] PASS: Output addresses the 40% incident origination directly — does extracting reduce blast radius or shift the failure surface — met: Operational lens Sub-question 2 directly addresses this; the synthesis convergent findings table includes it as a high-confidence finding.

- [x] PASS: Output's lens analyses produce DIFFERENT findings — met: Technical surfaces extraction cost and communication mechanism risk; Operational surfaces root-cause decomposition requirement and circuit-breaker need; Team surfaces operational maturity as binding constraint; Business surfaces fix-in-place cost comparison; Simplicity surfaces partial extraction as a third option.

- [x] PASS: Output's contradiction-surfacing step calls out tensions between lenses explicitly — met: each lens has a "Contradictions with previous lenses" section with named references to prior lenses; the Tensions table in synthesis documents three explicit tensions with recommended resolutions.

- [x] PASS: Output's synthesis produces a convergent findings table, tensions table, and clear recommendation — met: all three present with populated tables and a structured recommendation.

- [x] PASS: Output's recommendation considers the alternative of fixing-in-place — met: fix-in-place is documented as Option B in the recommendation with explicit conditions for when it is preferred; the Business and Simplicity lenses both surface it independently.

- [x] PASS: Output's revised problem framing differs from the Step 1 framing — met: the revised framing reframes from "should we extract?" to "which of three options is appropriate given root-cause data we don't yet have," with a "Key difference" field stating what changed.

- [~] PARTIAL: Output's confidence level is stated with the evidence basis, including what data would raise or lower it — partially met: confidence is stated as MEDIUM with the evidence basis named, and the "What would change this recommendation" section provides conditions for raising to HIGH; the gap is that the template doesn't prompt the confidence-level movement pattern by name, though the output covers it functionally.

## Notes

The skill definition is structurally strong. The mandatory unique-findings field and per-lens contradiction tracking are the key mechanisms preventing lenses from becoming parallel restatements of the same point. The synthesis section — convergent findings, tensions with required resolutions, blind spots, revised framing, success criteria, and what-would-change — produces a decision artifact rather than a brainstorm dump.

Both PARTIAL scores share the same root cause: the confidence template covers the spirit of the criterion via "What would change this recommendation" but doesn't explicitly frame it as "what data would raise confidence from MEDIUM to HIGH." In practice, a well-applied execution produces functionally equivalent output — as demonstrated in the simulated output above.

One structural note outside the rubric: the skill references `/council` and `/first-principles` as related skills but gives no trigger condition for when to hand off. A sentence like "if tensions remain unresolvable after the Tensions table, use `/council`" would remove the ambiguity.
