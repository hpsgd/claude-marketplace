# Iterative Depth

Scenario: A team is deciding whether to extract their monolith's notification subsystem into a separate microservice. The iterative-depth skill is used to examine the decision from multiple angles.

## Prompt

> /iterative-depth Should we extract the notification subsystem from our Rails monolith into a separate service? It currently handles email, push, and SMS. It has 8,000 lines, 3 engineers have touched it in the past 6 months, and it's the source of 40% of our production incidents. It handles email, push, and SMS. We deploy the whole monolith weekly.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll run a deep multi-lens analysis on this extraction decision. Let me work through it systematically.

## Step 1: Frame the problem

**Problem:** Should we extract the notification subsystem (email, push, SMS) from the Rails monolith into a separate service?

**Context:** 
- Notification subsystem is 8,000 lines, 3 engineers in past 6 months, 40% of production incidents
- Weekly deploy cycle for whole monolith
- High incident rate is painful for the team and reliability

**Constraints:** 
- Weekly deploy frequency (means slow feedback on changes)
- High incident response burden
- Limited team bandwidth

**Stakeholders:** 
- Engineering team (deployment, incident response, on-call burden)
- Product (feature velocity, reliability)
- Operations (monitoring, infrastructure, runbooks)

**Current state:** Tightly coupled notification system, high incident rate
**Desired state:** Reliable notifications with reduced incident load on team

---

## Step 2: Select lenses

I'm selecting five lenses because this is a strategic architecture decision with operational, technical, and organizational consequences:

1. **Technical** – Feasibility, coupling, implementation complexity
2. **Business** – Cost/benefit, ROI, payoff timeline
3. **Adversarial** – Failure modes, new risks introduced by extraction
4. **Temporal** – What the next 6 months, 2 years, 5 years look like
5. **Simplicity** – Is this the simplest solution, or a complex fix to an undiagnosed problem?

---

## Step 3: Analyse through each lens

### Lens 1: Technical

**Focus question:** What are the technical constraints, coupling patterns, and implementation feasibility?

**Analysis:**

The 8,000 lines almost certainly live in a job queue system (Sidekiq or similar)—Rails apps rarely build synchronous notification systems. That's good news for extraction: the async boundary is probably already there.

What needs extracting: email/push/SMS logic, retry logic, rate limiting, delivery status tracking.

What stays: the trigger points (user registration, order placed, etc.) and probably the user model references.

The hidden complexity lives in **state**. Where is delivery status stored? If it's in the monolith's database, extraction requires a schema split or careful coordination. If it's already isolated (separate tables or Redis), extraction is cleaner.

**Sub-questions:**
1. **How deep is the coupling?** If notifications already use a queue (probable), extraction is wrapping an existing async boundary. If not, extraction is much harder.
2. **Database schema ownership:** Do notifications own their own schema, or share tables with users/orders? Shared schema = migration complexity.
3. **Scale:** Is 8k lines because notifications are complex, or because they handle high throughput? If low throughput, the code could be simplified rather than extracted.

**Findings unique to this lens:**
1. If notifications already use a job queue, the async seam exists—extraction wraps existing infrastructure. Clean extraction path.
2. Database schema coupling is the hidden gotcha. Many notification systems embed delivery status, rate limits, and preferences in the monolith's DB. Moving those without coordination causes subtle bugs.
3. Extraction *adds* operational complexity: two services to deploy, two failure domains, network between them. This complexity has to be worth it.

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Shared database schema requires coordination, blocks independent deployment | High | High | Inventory schema dependencies upfront; plan schema migration as prerequisite |
| New service introduces network failures (down, timeouts) where monolith had in-process failures | Medium | High | Design graceful degradation: monolith queues locally if service is down, retries async |
| Dual-write during migration keeps systems in sync until cutover | High | High | Use shadow mode (service runs, results discarded) before real traffic shift |
| Service becomes bottleneck if monolith floods it with notifications | Medium | Medium | Backpressure mechanism: service rejects if queue too large; monolith backs off |

**Open questions:**
- What queue system is in place? Does it already isolate notifications?
- Where is delivery status stored (DB, Redis, elsewhere)?
- What's the throughput (email/push/SMS per day)?
- Are transactional guarantees required (user registration atomically triggers welcome email)?

---

### Lens 2: Business

**Focus question:** What's the cost/benefit trade-off? What's the ROI?

**Analysis:**

The business case rests on: incident reduction → operational cost saved → team capacity freed → faster delivery.

**Sub-question 1: Current cost of 40% incident rate**
- Assume 10-15 production incidents per week (typical mid-size service)
- 40% = 4-6 incidents per week in notifications
- Incident response: ~2 hours per incident (on-call engineer, triage, fix, deploy)
- That's 8-12 engineer-hours per week lost to incident response
- With 3 engineers, roughly **0.25 FTE (one quarter of a person) spent on notification firefighting**

**Sub-question 2: Cost of extraction**
- Design & planning: 1-2 weeks
- Implementation: 4-6 weeks
- Dual-write, testing, cutover: 2-3 weeks
- Stabilization: 1-2 weeks
- **Total: ~10-12 weeks of engineering effort (~2.5 FTE-weeks)**

**Sub-question 3: Payback period**
- Extraction might reduce notification incidents from 40% to 10% (optimistic: removes half the problem)
- That frees up ~2-3 incidents per week = 4-6 hours per week = 0.05-0.1 FTE
- Payoff = 2.5 FTE-weeks ÷ 0.1 FTE/week = **25+ weeks of incident reduction before break-even**
- That's **6+ months of incident-free operation to justify the extraction effort**

**Sub-question 4: But is the assumption valid?**
- Are incidents in notification *logic* (bugs, race conditions) or *dependencies* (SendGrid timeout, Twilio rate limit)?
- If it's external provider failures, extraction doesn't help—still get timeouts and rate limits.
- If it's coupling (notification job locks a table, blocks registration), extraction helps.
- If it's bugs, extraction helps only if the new service is better-designed.

**Findings unique to this lens:**
1. The business case is **marginal**. Six months of perfect incident-free operation just to break even. That's not compelling.
2. The assumption that "extraction = fewer incidents" is **unvalidated**. If 30% of those incidents are external provider failures, extraction gains you almost nothing.
3. **Opportunity cost:** 10-12 weeks of engineering is a half-quarter. That could build new features, fix other systems, or improve other incident sources. Is notification reliability worth more than alternatives?
4. **Incident severity matters.** Are these P1 incidents (user signup fails) or P4 incidents (welcome email arrives late)? The business impact is very different.

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Extraction effort underestimated (common in monolith refactors) | Medium | High | Timebox a 1-week spike to estimate scope. If >12 weeks, revisit decision. |
| Incidents don't decrease post-extraction (root cause is external or bugs, not architecture) | Medium | High | **Do RCA first.** Categorize incidents: logic bugs vs. provider failures vs. coupling issues. |
| Team loses knowledge during extraction; new incidents appear during transition | Medium | Medium | Pair extraction work with team who didn't do the extraction. Post-extraction on-call training. |
| Operational overhead (monitoring, alerting, runbooks) eats into ROI gains | Medium | Medium | Treat extracted service like a third-party dependency: heavy instrumentation, defensive design. |

**Open questions:**
- What's the root cause distribution of the 40%? (bugs, external failures, coupling, monitoring gaps)
- If you fixed just the top 3 causes, how much would incident rate drop?
- Is there a simpler first step (better monitoring, dedicated on-call, targeted bug fixes)?

---

### Lens 3: Adversarial

**Focus question:** How could extraction fail? What new failure modes appear?

**Analysis:**

Extraction replaces "notifications fail" (bad) with "notifications service is down or unreachable" (worse). The boundary between monolith and service becomes a new failure point.

**Sub-question 1: New failure modes**
- Service down: monolith cannot send notifications (unless it has a fallback queue)
- Network partition: monolith queues but service can't process; queue grows unbounded until disk fills
- Latency: if monolith waits for service ack, slow service stalls user signup
- Dual-write inconsistency: during migration, monolith and service disagree on what was delivered
- Cascading: if service is down and monolith queues locally, a big queue can crash the monolith itself

**Sub-question 2: Attack surface**
- If the service is network-accessible, it's a new attack surface
- If the service is slow, it becomes a DoS vector for the monolith
- If the service talks to external providers, compromise of the service = spam/phishing risk
- Rate limiting must be enforced at both service and provider, or service becomes a vulnerability

**Sub-question 3: Migration period risk**
- Dual-write (monolith and service both writing, need to agree) is the most dangerous period
- If dual-write code is buggy, data corruption
- If dual-write is only half-deployed, rollback is complex
- Shadow mode (service runs but results discarded) is safer but requires more engineering

**Findings unique to this lens:**
1. **Network boundary creates ambiguity.** Current system: "notification delivery failed" is clear. Extracted system: "service accepted the request but hasn't confirmed delivery yet" is ambiguous. If monolith and service disagree, you have silent failures.
2. **Single point of failure.** Current system: notifications fail independently (one user's email fails, others succeed). Extracted system: service down = all notifications down.
3. **Migration period is the most vulnerable.** Dual-write is where data corruption happens. This is non-trivial to get right.
4. **The extracted service must be more reliable than the current system, or extraction made things worse.** This requires excellent design, not just code movement.

**Contradictions with previous lenses:**
- Technical lens says extraction is feasible. Adversarial says extraction introduces new failure modes that could be worse than current problems.
- Business lens says payoff is 6+ months. Adversarial says if extraction goes wrong in the first 6 months, you've wasted time AND made reliability worse.

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Service down during cutover causes all notifications to fail | High | High | Have fallback queue in monolith. Service down → monolith queues locally, retries when service recovers. Circuit breaker pattern. |
| Dual-write causes data inconsistency (monolith thinks sent, service thinks failed) | Medium | High | Shadow mode first (service runs but results discarded). 100% consistency verification before cutover. Idempotency keys. |
| Network failures cause delivery state ambiguity | Medium | High | Every notification gets unique ID. Service deduplicates. Monolith can query status. No "I don't know what happened" states. |
| Service becomes bottleneck, monolith floods it | Medium | Medium | Backpressure design: service rejects oversized requests, monolith retries later. Load test first. |
| Incident response now fragmented (is this a monolith issue or service issue?) | Medium | Medium | Clear ownership, shared runbooks, joint on-call training. Faster MTTR requires clarity. |

**Open questions:**
- What's acceptable for "notification in-flight" (sent but status unknown)?
- What's the fallback if service is down?
- SLA for notifications: best-effort or hard requirement?

---

### Lens 4: Temporal

**Focus question:** What does the trajectory look like at 6 months, 2 years, 5 years?

**Analysis:**

Extraction is not a change; it's a multi-quarter project with ongoing consequences.

**Sub-question 1: First 6 months (extraction + stabilization)**
- Months 1-2: Design, spike, planning. Team learns new architecture.
- Months 2-4: Implementation. Service built, tested, integrated.
- Months 4-5: Dual-write, shadow mode, gradual cutover.
- Months 5-6: Stabilization, on-call hardening, bug fixes.
- Best case: incident rate drops, on-call burden eases. Worst case: new issues appear, team scrambles to rollback.

**Sub-question 2: 2-year horizon**
- Service is now a permanent system. New features requested (scheduling, templating, A/B testing). Where do they go?
- Team knowledge: split between monolith and service experts. Who on-calls the service?
- Scaling: if notifications grow, great—service scales independently. If they shrink, service is underutilized overhead.
- Dependency risk: service depends on Redis, external providers, possibly shared DB. Any could become bottleneck.

**Sub-question 3: 5-year horizon**
- **Option A:** Service becomes strategic, owned by dedicated team. Heavy investment pays off.
- **Option B:** Service is stable and low-incident, but was it worth the overhead? Regret extraction.
- **Option C:** Service becomes neglected, features pile up, reliability degrades. Regret extraction.

The big temporal risk: **extraction locks you into a bet.** You're betting that notifications will become important enough to justify separate infrastructure. If not, you've added permanent operational complexity.

**Findings unique to this lens:**
1. **Extraction is a 6-12 month project, not a 4-week change.** That's half a year where the system is in transition, risky, and people are heads-down on extraction instead of shipping features. Second and third-order effects matter.
2. **Payoff is entirely in the future.** If priorities shift, budget tightens, or team changes, the project could be abandoned midway. Abandoned extraction is the worst outcome.
3. **In 2 years, the real question is organizational, not technical.** Do you have a team owning the service? Clear ownership = success. Scattered ownership = you haven't solved the problem, just moved it.
4. **Notifications might not be strategic long-term.** Email/push/SMS delivery could become commoditized (fully managed by external providers, cheap). Extracting now could be premature.

**Contradictions with previous lenses:**
- Business lens says payoff is 6+ months. Temporal lens says the project itself is 6-12 months, so payoff could be 12-18 months away.
- Technical lens says extraction is feasible. Temporal lens says feasibility over 6 months ≠ sustainability over 2+ years.

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Project scope expands (feature requests, refactoring), extraction stretches beyond 6 months | High | High | Strict scope: service handles delivery ONLY. Preferences, templating, scheduling = future work. Fixed timeline. |
| Team ownership unclear after extraction; service becomes orphaned | Medium | High | **Assign ownership before extraction starts.** Plan for handoff. Clear SLAs. |
| External provider ecosystem changes, invalidates architecture | Low | Medium | Build provider abstraction layer. Keep option to swap providers without rewriting. |
| Monolith continues to grow, pulls notifications back in (integration points multiply) | Medium | Medium | Governance: define clear async boundary. All requests → queue. No sneaky sync calls. |
| Notifications become lower priority, service maintenance deferred, reliability degrades | Medium | Medium | Decide upfront: is notifications strategic or commodity? If strategic, staff it. If commodity, maybe don't extract. |

**Open questions:**
- What's the 2-year vision for notifications? (dedicated team? shared responsibility? outsourced?)
- Are there other extraction candidates (payment, auth, analytics)? Extraction strategy should account for migration pattern.
- If extracted, how do you prevent the service from becoming a "second monolith"?

---

### Lens 5: Simplicity

**Focus question:** Is extraction the simplest solution? Or are we reaching for a complex solution when simpler fixes would work?

**Analysis:**

The stated problem: "40% of production incidents are in the notification subsystem."

The complex solution: extract into separate service.

But before choosing the solution, we need to diagnose the problem.

**Sub-question 1: What's really causing the 40%?**
- Logic bugs (email retry loop, race conditions)? → **Fix the bugs.**
- External failures (SendGrid timeout, Twilio rate limit)? → **Improve fallbacks, circuit breakers.**
- Coupling (notification job locks a table, blocks other queries)? → **Refactor the query.**
- Operational (queue too small, service underdimensioned)? → **Scale it, add monitoring.**
- Knowledge/process (few people know the code, slow response)? → **Document, pair program, training.**

**The principle:** Match the solution to the root cause.

If root cause is bugs, extraction doesn't help—you've just moved buggy code.
If root cause is external, extraction might help slightly (retry logic) but you can't fix the provider's timeouts.
If root cause is coupling, extraction solves it, but so does refactoring the query in-place.
If root cause is operational, you need scaling and monitoring, not a separate service.
If root cause is knowledge, extraction could help (fresh start) but only if new service is designed better.

**Sub-question 2: What's the simplest thing that would reduce incidents?**
- **Option 1: RCA + targeted fixes.** Analyze the 40%, find top causes, fix them. *Effort: 1-2 weeks. Payoff: maybe 30-50% reduction.*
- **Option 2: Monitoring & alerting.** Know about problems before users. *Effort: 1-2 weeks. Payoff: faster response = less pain.*
- **Option 3: Dedicated on-call.** Assign someone to notifications. *Effort: none. Payoff: faster response.*
- **Option 4: Refactor in monolith.** Clean up 8k lines, improve code quality. *Effort: 2-3 weeks. Payoff: maybe 20-30% reduction.*
- **Option 5: Extract.** *Effort: 10-12 weeks. Payoff: maybe 30-50% reduction (if root cause is architectural).*

If Options 1-4 reduce incidents to 20%, extraction is now unjustified.

**Sub-question 3: What's "good enough"?**
- Do we need to go from 40% to 5%? Or is 20% acceptable?
- If 20% is fine, simpler solutions work.
- If 5% is required, maybe extraction is necessary (or maybe it's not—depends on root cause).

**Findings unique to this lens:**
1. **The solution is being chosen before the problem is diagnosed.** "40% of incidents" is a symptom. Extraction assumes the diagnosis is "notifications are inherently complex" when it might be "we have three bugs" or "we don't monitor well enough."
2. **Extraction is a structural solution to what might be a procedural problem.** If the issue is "too few people know this code", extraction doesn't fix it—it just moves the problem. If it's "we don't have RCA discipline", extraction doesn't fix that either.
3. **The simplest solution is probably: (a) RCA, (b) fix identified bugs/issues, (c) improve monitoring, (d) document code.** Total cost: 2-3 weeks. Payoff: probably 30-50% incident reduction. If that's enough, you're done.

**Contradictions with previous lenses:**
- Technical lens says extraction is feasible. Simplicity lens says: **feasibility ≠ necessity.**
- Business lens assumes extraction reduces incidents. Simplicity lens says: **validate that assumption first.**
- Temporal lens says extraction is a 6-12 month project. Simplicity lens says: **do RCA first (1 week), then reassess. Only extract if RCA validates it.**

**Risks identified:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Extraction done without RCA; doesn't solve the problem; wastes 10-12 weeks | High | High | **Do RCA as a gate.** No extraction work starts until RCA is done and team agrees on root causes. |
| Team falls prey to "rewrite will fix it" bias | High | Medium | Pre-mortem: ask "what if simple fixes work?" Commit to decision criteria upfront. |
| Monitoring approach underestimated ("if we just monitor better, incidents will stop") | Medium | Medium | RCA must distinguish between unknown-unknowns (need monitoring) vs. known issues (need fixing). |

**Open questions:**
- Has RCA been done on the 40%? What are the findings?
- What percentage is bugs (fixable) vs. external (unfixable by extracting) vs. operational (fixable by scaling)?
- If you fixed the top 3 causes, what would incident rate drop to?

---

## Step 4: Synthesise

### Convergent findings

| Finding | Supported by lenses | Confidence | Implication |
|---|---|---|---|
| Root cause of the 40% is unknown and must be determined first | Simplicity, Business, Adversarial | **High** | RCA is a prerequisite, not optional. Don't decide on extraction until you know what's causing incidents. |
| Extraction is technically feasible but adds operational complexity | Technical, Adversarial | **High** | Feasibility alone doesn't justify it. The new complexity (network failures, dual-write, two services) must be worth the ROI. |
| Payoff period is long (6-18 months total) and uncertain | Business, Temporal | **High** | Not a quick win. Multi-quarter commitment with deferred payoff. Must be confident in root cause analysis. |
| Simpler alternatives exist that might work faster | Simplicity, Business | **Medium** | RCA + targeted fixes (2-3 weeks) might achieve 30-50% incident reduction. Validate before committing to 12-week extraction. |
| Extraction introduces new failure modes that must be designed for | Technical, Adversarial | **High** | If you extract, plan defensively: fallback queues, circuit breakers, idempotency, dual-write safety. This adds complexity. |

### Tensions and trade-offs

| Tension | Lens A says | Lens B says | Recommended resolution | Rationale |
|---|---|---|---|---|
| **Feasibility vs. Necessity** | Technical: "extraction is feasible" | Simplicity: "haven't validated it's necessary" | **Resolve in favor of Simplicity.** Do RCA first. | Building something you don't need is waste. Validation before effort. |
| **Speed to improvement vs. Quality** | Business: "payoff is 6+ months" | Temporal: "total timeline is 12-18 months" | **Choose faster path: RCA + quick fixes (2-3 weeks).** | Bird in hand beats two in bush. Test simpler solutions before multi-quarter project. |
| **Operational simplicity vs. Scale** | Technical: "extraction enables independent scaling" | Simplicity: "if you don't need scale, you don't need extraction" | **Accept the trade-off only if notifications growth is anticipated.** | Scale is real benefit, but only matters if you need it. |
| **Clear ownership vs. Overhead** | Temporal: "extraction needs dedicated team" | Simplicity: "dedicated team for notifications might be overkill" | **Resolve based on strategic importance.** If notifications are strategic, staff it. If not, keep in monolith. | Organizational structure should match strategic priority. |

**Recommended resolution:**
Do not extract yet. **Conduct RCA first (1 week).** Only extract if RCA indicates architectural root causes (coupling, scaling) rather than procedural ones (bugs, monitoring, knowledge gaps). If RCA shows bugs and operational issues, fix those first (2-3 weeks), measure impact, and reassess in 3 months.

### Blind spots filled

| Blind spot | Revealed by | Would have caused | Prevention |
|---|---|---|---|
| Root cause of incidents is unknown | Simplicity, Business | Solving the wrong problem. Extraction won't help if incidents are bugs or external failures. | Mandatory RCA before architectural decisions. Make it a gate. |
| New failure modes created by extraction (network partition, dual-write inconsistency) | Adversarial | Silent failures, data corruption, worse reliability post-extraction. Regret. | Design extraction defensively upfront. Plan for service-down scenarios, fallbacks, idempotency. |
| Payoff timeline is unclear and possibly optimistic | Business, Temporal | Underestimated effort (actually 12-18 months total), unmet ROI targets, demoralized team. | Create realistic project plan: design 2w + impl 4w + dual-write 2w + cutover 2w + stabilize 2w = 12w minimum. |
| Simpler alternatives not explored | Simplicity | Solving 80% of the problem the hard way when 60% could be solved easily. | Mandatory step before extraction: 1 week RCA + quick wins. Document what was fixed. Only extract if gaps remain. |
| Extraction is a bet on future importance | Temporal | Creating permanent infrastructure for a component that stays low-priority. Orphaned service. Regret. | Decide now: is notifications strategic enough to justify a dedicated team in 2+ years? If not, keep in monolith and improve it. |

### Revised problem framing

**Original:** Should we extract the notification subsystem? It's 8k lines, touches 3 engineers in 6 months, causes 40% of incidents.

**Revised:** Should we extract the notification subsystem? **Not until we understand why it causes 40% of incidents.** The decision should be conditional:
- Extract IF root causes are architectural (coupling, scaling, independent deploy needs)
- Invest in in-monolith improvements IF root causes are procedural (bugs, monitoring, code quality, knowledge)
- Mandatory first step: 1-week RCA to categorize the 40% of incidents

**Key difference:** Original framing treats extraction as The Solution. Revised framing recognizes extraction as One Option—and maybe not the best one. The real question is: *what's causing the incidents?* Answer that, and the architecture decision becomes obvious.

### Refined success criteria

| Criterion | Source lens | Metric | Threshold |
|---|---|---|---|
| Root causes identified and categorized | Simplicity, Business | RCA document with incident distribution (bugs vs. external vs. coupling vs. operational) | 100% of the 40% categorized with evidence |
| Quick wins prioritized | Simplicity | List of fixable bugs, monitoring gaps, scaling issues | Top 3 causes identified and estimated |
| Incident reduction from quick wins measured | Business | Incident rate after fixes | ≥20% reduction (or ≥30% preferred) |
| Extraction business case validated | Business, Temporal | Payoff calculation: effort × incident reduction = break-even timeline | Payoff period < 12 months total, or >50% incident reduction |
| Operational risk of extraction quantified | Adversarial, Technical | Design document: fallbacks, circuit breakers, dual-write strategy, service-down scenarios | Every failure mode has a mitigation |
| Team commitment confirmed | Temporal | Written commitment from eng lead and product on 18+ month ownership | Ownership assigned, capacity reserved |

---

## Recommendation

**Do not extract yet. Conduct RCA first. Only extract if RCA indicates architectural root causes.**

### Phased approach

**Phase 1: RCA (1 week)**
- Analyze the 40% of incidents.
- Categorize by root cause:
  - **Logic bugs** (fixable in monolith, e.g., retry loop bug, race condition)
  - **External failures** (unfixable by extracting, e.g., SendGrid timeout, Twilio rate limit)
  - **Coupling/scaling** (fixable by extraction or refactoring, e.g., notification job locks table)
  - **Operational** (fixable by scaling/monitoring, e.g., queue too small)
  - **Knowledge** (fixable by documentation/training, e.g., few people understand code)
- Document findings with examples from incidents.

**Phase 2: Quick wins (2-3 weeks)**
- Fix the top bugs identified in RCA.
- Add monitoring and alerting for visibility.
- Improve queue sizing or scaling if needed.
- Measure incident rate post-fixes.

**Phase 3: Reassess (after Phase 2)**
- If incidents drop to <15%, extraction is likely unnecessary. **Stop here.** You've solved the problem the simple way.
- If incidents stay >25% AND are due to coupling/architectural issues, extraction becomes justified. Proceed.
- If incidents are due to external provider failures, neither extraction nor fixes will help much. Adjust expectations and improve fallbacks.

### Confidence

**Medium-Low** right now (because root causes are unknown). **Will be High** after RCA completes and team reviews findings.

### Key risks

1. **RCA reveals no clear culprit** (incidents are scattered, random). → Mitigation: Invest in observability and logging to catch patterns.
2. **RCA shows extraction is necessary, but team has no capacity.** → Mitigation: Prioritize it, or accept higher incident rate and staff on-call better.
3. **Extraction starts, but root causes were misunderstood, so extraction doesn't solve the problem.** → Mitigation: Strict gate—don't start extraction until team agrees on root causes and extraction's expected benefit.

### Next steps

1. **Immediate (this week):** Assign 1 engineer to RCA. Define incident categories. Analyze the last 40 incidents. Document findings.
2. **Follow-up (if RCA suggests quick wins):** Plan 2-3 week sprint to fix bugs, add monitoring, improve scaling.
3. **Validation (3 months later):** Measure incident rate. If <15%, success. If >25%, re-evaluate extraction.
4. **Extraction decision gate:** Only if RCA + quick wins don't solve it AND team is confident in root cause analysis.

### What would change this recommendation

- **If RCA shows >80% of incidents are coupling/architectural**, extraction is justified immediately.
- **If team has zero capacity in next 6 months**, defer extraction. Staff on-call instead.
- **If extraction architecture reveals prohibitive complexity** (very deep coupling), reconsider. Refactor in-place instead.
- **If notifications become strategic priority** (new feature velocity, new providers), extraction might be justified even without RCA, to unlock faster iteration.

---

**Bottom line:** You have a symptom (40% incidents) but not a diagnosis. Before making a 12-week architectural decision, spend 1 week diagnosing. The diagnosis will tell you whether extraction is the right answer or if simpler fixes work.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 176643 ms |
| Target cost | $0.1148 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 produces a complete problem framing with problem statement, context, constraints, stakeholders, current state, and desired state | PASS | Step 1 explicitly covers all six elements: problem statement ('Should we extract the notification subsystem...'), context (8k lines, 3 engineers, 40% incidents, weekly deploy), constraints (weekly deploy frequency, incident burden, limited bandwidth), stakeholders (engineering team, product, operations), current state ('Tightly coupled notification system, high incident rate'), and desired state ('Reliable notifications with reduced incident load on team'). |
| c2 | Step 2 selects 3-5 lenses from the eight available and states which were chosen and why | PASS | Step 2 selects exactly 5 lenses: Technical, Business, Adversarial, Temporal, Simplicity. Rationale given: 'I'm selecting five lenses because this is a strategic architecture decision with operational, technical, and organizational consequences.' Each lens is named with a focus area description. |
| c3 | Lens selection includes at least one human lens (User or Business) and one system lens (Technical or Edge case) per the skill's selection rules | PASS | Business is selected as a human lens. Technical is selected as a system lens. Both are present in the five-lens set. |
| c4 | Each lens analysis produces at least one finding not surfaced by any previous lens — not just restating earlier observations | PASS | Technical: 'Database schema coupling is the hidden gotcha.' Business: quantified 0.25 FTE lost to firefighting and 6+ month payback. Adversarial: 'Current system: notifications fail independently... Extracted system: service down = all notifications down.' Temporal: 'Extraction is a 6-12 month project, not a 4-week change.' Simplicity: 'The solution is being chosen before the problem is diagnosed.' Each lens adds a distinct finding. |
| c5 | Contradictions between lenses are explicitly called out — not smoothed over | PASS | Adversarial section: 'Technical lens says extraction is feasible. Adversarial says extraction introduces new failure modes that could be worse.' Temporal section: 'Business lens says payoff is 6+ months. Temporal lens says the project itself is 6-12 months, so payoff could be 12-18 months away.' Simplicity section: 'Technical lens says extraction is feasible. Simplicity lens says: feasibility ≠ necessity.' Three explicit cross-lens contradictions are labeled. |
| c6 | Step 4 synthesis produces a convergent findings table, a tensions table with recommended resolutions, and a clear recommendation | PASS | Step 4 contains: (1) 'Convergent findings' table with Finding/Lenses/Confidence/Implication columns; (2) 'Tensions and trade-offs' table with Tension/Lens A says/Lens B says/Recommended resolution/Rationale columns; (3) clear recommendation 'Do not extract yet. Conduct RCA first. Only extract if RCA indicates architectural root causes.' |
| c7 | Revised problem framing at the end of Step 4 differs from the Step 1 framing in a meaningful way | PASS | Original framing: 'Should we extract the notification subsystem? It's 8k lines...' Revised framing: 'Should we extract the notification subsystem? Not until we understand why it causes 40% of incidents.' Explicitly noted: 'Original framing treats extraction as The Solution. Revised framing recognizes extraction as One Option—and maybe not the best one. The real question is: what's causing the incidents?' |
| c8 | Confidence level for the recommendation is stated with the evidence basis (not just "Medium confidence" but what data would raise or lower it) | PARTIAL | States 'Medium-Low right now (because root causes are unknown). Will be High after RCA completes and team reviews findings.' Under 'What would change this recommendation,' lists four specific conditions: RCA showing >80% architectural causes, team capacity, extraction complexity findings, and notifications becoming strategic priority. Provides the directional evidence basis. |
| c9 | Output's problem framing reproduces the prompt's specific facts — 8,000 lines, 3 engineers in 6 months, 40% of incidents originate here, weekly monolith deploys, three channels (email/push/SMS) — and ties them to the decision | PASS | Step 1 context reproduces all facts: '8,000 lines, 3 engineers in past 6 months, 40% of production incidents,' 'Weekly deploy cycle for whole monolith,' and email/push/SMS appear in the problem statement. Business lens uses 3 engineers in its FTE calculation. All facts are tied to the architectural decision. |
| c10 | Output selects 3-5 lenses and names them — e.g. Technical (extraction cost vs benefit), Operational (deploy independence, blast radius), Team (cognitive load, expertise), Business (incident reduction value), User (delivery reliability) — and explains why each was chosen for THIS decision | PASS | Five lenses named with focus questions anchored to this specific decision: Technical ('Feasibility, coupling, implementation complexity'), Business ('Cost/benefit trade-off? What's the ROI?'), Adversarial ('How could extraction fail? What new failure modes appear?'), Temporal ('What does the trajectory look like at 6 months, 2 years, 5 years?'), Simplicity ('Is extraction the simplest solution, or a complex fix to an undiagnosed problem?'). Each focus question is specific to the extraction question. |
| c11 | Output's lens selection includes at least one human lens (Team or Business or User) AND one system lens (Technical or Operational or Edge case) per the skill's selection rules | PASS | Business lens is the human lens. Technical lens is the system lens. Both explicitly selected and analyzed. |
| c12 | Output addresses the 40% incident origination directly — does extracting the service reduce the blast radius (yes — incidents stay isolated to notifications) or just shift the failure surface (now needs reliable inter-service comms)? | PASS | Adversarial lens directly addresses this: 'Extraction replaces "notifications fail" (bad) with "notifications service is down or unreachable" (worse).' Also: 'Current system: notifications fail independently (one user's email fails, others succeed). Extracted system: service down = all notifications down.' This explicitly answers the blast-radius vs. failure-surface shift question. |
| c13 | Output's lens analyses produce DIFFERENT findings — the technical lens surfaces e.g. "service extraction cost ~3 engineer-months", the operational lens surfaces "deploy frequency could go from weekly to daily for notifications", the team lens surfaces "ownership clarification" — not all converging on the same point | PASS | Technical: schema coupling hidden gotcha, async seam feasibility. Business: 0.25 FTE lost to firefighting, 6+ month payback period, effort quantified at 10-12 weeks. Adversarial: new SPOF, dual-write inconsistency risk, migration period vulnerability. Temporal: 6-12 month total timeline, organizational ownership in 2 years, strategic bet framing. Simplicity: RCA-first as gate, five simpler alternatives enumerated. No two lenses converge on the same primary finding. |
| c14 | Output's contradiction-surfacing step calls out tensions between lenses explicitly — e.g. "the team lens favours extraction (clear ownership), the operational lens cautions extraction (operational complexity for the same 3 engineers)" | PASS | Each lens section after the first contains a 'Contradictions with previous lenses' subsection. Examples: 'Technical lens says extraction is feasible. Adversarial says extraction introduces new failure modes.' 'Business lens assumes extraction reduces incidents. Simplicity lens says: validate that assumption first.' Tensions are explicitly labeled and not smoothed over. |
| c15 | Output's synthesis produces a convergent findings table (where lenses agree), a tensions table (where lenses disagree, with proposed resolution path), and a clear recommendation | PASS | Same as c6 — convergent findings table present (5 rows with Finding/Lenses/Confidence/Implication), tensions table present (4 rows with Tension/Lens A/Lens B/Recommended resolution/Rationale), recommendation stated: 'Do not extract yet. Conduct RCA first.' |
| c16 | Output's recommendation considers the alternative of fixing-in-place — extracting is one option, addressing the 40% incident root causes within the monolith is another, and the synthesis weighs both rather than only debating extraction | PASS | Simplicity lens explicitly enumerates five options including 'Option 1: RCA + targeted fixes (1-2 weeks)', 'Option 4: Refactor in monolith (2-3 weeks)'. Revised problem framing: 'Invest in in-monolith improvements IF root causes are procedural.' Phased approach Phase 2 is in-monolith fixes before even deciding on extraction. The synthesis explicitly weighs both. |
| c17 | Output's revised problem framing differs from the Step 1 framing — e.g. shifts from "should we extract?" to "what's driving the 40% incidents, and is extraction the leverage point?" | PASS | Revised framing explicitly reframes: 'The real question is: what's causing the incidents? Answer that, and the architecture decision becomes obvious.' The output labels the key difference: 'Original framing treats extraction as The Solution. Revised framing recognizes extraction as One Option.' The shift from 'should we extract?' to 'what's causing incidents, is extraction the right lever?' is explicit. |
| c18 | Output's confidence level is stated with the evidence basis — e.g. "MEDIUM confidence; would rise to HIGH if we had a 2-week incident root-cause analysis showing they're notifications-internal vs HIGH if they're integration boundaries" | PARTIAL | States 'Medium-Low right now (because root causes are unknown). Will be High after RCA completes.' Four specific conditions listed under 'What would change this recommendation' (RCA showing >80% architectural causes, team capacity zero, prohibitive coupling complexity, strategic priority shift). Provides directional conditions but not the precise numeric threshold phrasing the criterion example illustrates. |

### Notes

The output is a thorough, well-structured iterative-depth analysis that satisfies every criterion. All five lenses generate genuinely distinct findings; cross-lens contradictions are explicitly surfaced within each lens section rather than deferred to synthesis; the convergent-findings and tensions tables are complete with rationales; and the revised problem framing meaningfully reorients the question from 'should we extract?' to 'diagnose root causes first.' The two PARTIAL-ceiling criteria (c8, c18) are both addressed at the PARTIAL level — confidence is stated with evidence basis and directional conditions, but falls slightly short of the detailed numerical threshold phrasing the criterion examples illustrate (e.g., 'would rise to HIGH if RCA showed X% are notifications-internal'). No criteria are missed or skipped.
