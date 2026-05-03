# Iterative Depth

Scenario: A team is deciding whether to extract their monolith's notification subsystem into a separate microservice. The iterative-depth skill is used to examine the decision from multiple angles.

## Prompt

> /iterative-depth Should we extract the notification subsystem from our Rails monolith into a separate service? It currently handles email, push, and SMS. It has 8,000 lines, 3 engineers have touched it in the past 6 months, and it's the source of 40% of our production incidents. It handles email, push, and SMS. We deploy the whole monolith weekly.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Step 1 — Frame the problem

```
Problem: Whether to extract the notification subsystem (email, push, SMS) from the
         Rails monolith into a separate service to reduce a 40% incident rate.

Context: The subsystem is the single largest source of production incidents.
         Weekly monolith deploys mean notification failures and unrelated changes
         can block each other.

Constraints: 8,000-line Rails codebase; 3 engineers with context; weekly deploy
             cadence; unknown team size; unknown root cause of incidents.

Stakeholders: Notification engineers, on-call engineers, end users, product/business.

Current state: Subsystem embedded in monolith, 40% of production incidents,
               weekly deployments.

Desired state: Lower incident rate, predictable deployments, faster notification
               iteration.
```

---

## Step 2 — Lens selection

| Lens | Why selected |
|---|---|
| **Technical** | Any extraction decision requires understanding the coupling, new failure modes, and what "extract" actually means in Rails |
| **Adversarial** | 40% incident rate is the core pain signal — need to challenge whether extraction addresses it |
| **Business** | Large investment; proportionality check is required |
| **Temporal** | Extraction is a long-term bet; need to know if it holds up under growth |
| **Simplicity** | Counterweight — the instinct to extract is strong but may not be the minimum effective intervention |

---

## Step 3 — Analysis

---

### Lens 1: Technical

**Focus question:** What does extraction actually require, and what failure modes does it introduce?

**Analysis:**

*Sub-question 1: What does the coupling look like?*

In a Rails monolith, notification calls are typically synchronous (`UserMailer.welcome.deliver_later`) or async via Sidekiq/ActiveJob. If already async: the architectural coupling is already loose — the monolith enqueues a job, the worker fires the provider call. In that case, extraction means pulling Sidekiq workers and provider clients into a separate process, and the failure propagation characteristics barely change. If synchronous: extraction adds a network hop to the critical path of user-facing requests, which is worse.

*Sub-question 2: What new infrastructure does extraction require?*

At minimum: separate repo, separate deploy pipeline, a message queue or HTTP API contract, service discovery, inter-service auth, separate monitoring/alerting, and separate on-call runbooks. Critically: the notification service likely reads user preferences, contact details, and unsubscribe state from the monolith's DB. Options are: shared read replica (tight coupling preserved), API callback to the monolith (circular dependency, new failure mode), or replicated data store (consistency problem). None of these are free.

*Sub-question 3: What is the actual cause of the 40% incident rate?*

This is the pivotal unknown. Possible categories:
- **External provider outages** (Twilio, SendGrid, APNs): extraction does not fix this — you're still dependent on those providers from the new service
- **Missing resiliency patterns** (no circuit breakers, bad retry logic, no idempotency): fixable in place
- **Deployment coupling** (a bad notification deploy takes down the monolith, or vice versa): extraction is the correct fix for this specifically
- **Resource contention** (notification workers saturating DB connections or queue capacity): fixable with pool limits in place

Extraction only definitively solves one of these four categories.

**Findings unique to this lens:**
1. If notification calls are already async (Sidekiq/ActiveJob), the failure propagation is already decoupled — extraction changes operational boundaries but not reliability in a fundamental way.
2. The notification service will likely need access to user/preference data from the monolith; every option for providing it introduces a new coupling or consistency problem.
3. Extraction introduces new failure modes (network partition, inter-service auth failures, queue depth) that don't exist today — the incident count could increase even if the incident category distribution changes.

**Contradictions with previous lenses:** N/A — first lens.

**Risks:**
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Incidents shift from "notification code bugs" to "inter-service communication failures" | Medium | High | Design async contract (events, not RPCs) from day one |
| Subsystem has deep Rails magic (callbacks, concerns, shared models) that's hard to cleanly extract | Medium | High | Spike one channel extraction before committing to the full effort |
| Shared DB access is required and creates tighter coupling than the service boundary suggests | High | Medium | Audit all DB reads in the notification subsystem before committing |

**Open questions:**
- Are notification calls sync or async today?
- What tables does the notification subsystem read from? Does it write to shared tables?
- What are the top 3 incident root cause types?

---

### Lens 2: Adversarial

**Focus question:** How could this go wrong, and is extraction treating the symptom rather than the disease?

**Analysis:**

*Sub-question 1: Is extraction the right response to a 40% incident rate?*

40% of incidents from one subsystem signals one of four things: (a) the subsystem is complex and undertested, (b) it has no resiliency patterns against external provider failures, (c) it's causing cascading failures across the monolith, or (d) it's just bad code. Extraction definitively solves only (c). For (a), (b), and (d), you can fix the code in place at 10% of the cost. The adversarial framing: are we proposing open-heart surgery when the patient needs antibiotics?

*Sub-question 2: What happens during the migration phase?*

The migration window is the highest-risk phase. You'll run dual paths (old and new code), use feature flags, and maintain both codebases simultaneously. Every incident during this period is harder to diagnose — is it the old path, the new service, the message queue, or the contract mismatch? The team that currently generates 40% of incidents will temporarily own two production systems. This is precisely the conditions under which a high-severity incident is most likely.

*Sub-question 3: What new attack surfaces does extraction create?*

A standalone notification service that can send email, push, and SMS to all users is a high-value security target. In the monolith, this code path is protected by the monolith's auth model. As a separate service, it needs its own inter-service auth (API keys, JWTs, mTLS) and its own access controls. If misconfigured, an attacker who compromises the notification service can send arbitrary messages to your entire user base. This attack surface doesn't exist today.

**Findings unique to this lens:**
1. The migration phase itself is the highest-risk period — the team with the worst incident rate in the org will temporarily maintain two production systems. This is when a high-severity incident is most likely, not least likely.
2. A standalone notification service (arbitrary messages to all users) is a critical security target; extraction creates a new high-value attack surface that doesn't currently exist.
3. The 40% figure may be a monitoring artifact: if the notification subsystem is well-instrumented and other subsystems are poorly instrumented, the proportion is misleading. Better observability everywhere might discover incidents in other subsystems and change the denominator.

**Contradictions with previous lenses:**
- Technical lens noted that if calls are already async, failure propagation is already loose. Adversarial lens adds a harder constraint: the migration phase creates a *worse* failure condition during transition than either steady state. Together: don't extract unless you're committed to doing it carefully and incrementally.

**Risks:**
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Migration phase doubles incident rate temporarily | High | High | Extract incrementally — one channel at a time, with rollback plan at each stage |
| Extraction completed; root causes were not provider coupling; incident rate unchanged | Medium | High | Mandate root-cause retrospectives before committing to extraction |
| Auth misconfiguration exposes notification service to unauthorized callers | Medium | Critical | Design auth contract first; security review before any production traffic |
| Observability gaps follow the code into the new service | High | Medium | Instrument the new service before migrating traffic, not after |

**Open questions:**
- What do post-mortems say about notification incidents? Are they categorised by root cause?
- What's the current observability state of the notification subsystem?
- Has circuit breaker / retry hardening been tried and abandoned, or never attempted?

---

### Lens 3: Business

**Focus question:** Is extraction economically proportionate, given team size, deployment cadence, and the absolute cost of incidents?

**Analysis:**

*Sub-question 1: What is the incident cost, and is extraction proportionate?*

40% of production incidents is a striking number but we need the absolute count to evaluate cost. 5 total incidents/month → 2 notification-related → maybe 4 engineer-hours/month. 50 total incidents/month → 20 notification-related → potentially 40-60 engineer-hours/month plus customer trust damage. Extraction is a 3-6 month focused engineering investment plus ongoing operational overhead (own deploy pipeline, monitoring, runbooks, on-call). The break-even point shifts dramatically based on absolute volume. Making this decision without the absolute count is like saying "40% of our budget is wasted" without knowing the budget.

*Sub-question 2: What is the ongoing operational overhead of a separate service?*

A separate service requires: CI/CD pipeline, monitoring/alerting, runbooks, secrets management, service-to-service auth rotation, and on-call escalation paths. For small teams, each additional service meaningfully increases cognitive overhead and on-call surface area. 3 engineers touched the notification code in 6 months — this is either a small specialist team or a low-churn codebase. Either way, adding a service to own and operate is not free.

*Sub-question 3: Does the weekly deploy cadence actually justify extraction?*

The weekly deploy cycle means notifications are potentially blocked by other changes and vice versa. But this only matters if: notification changes are being delayed by unrelated changes, or notification changes are blocking others' deploys. If the notification team ships one change every two weeks and it's never a blocker, the deploy cadence benefit is theoretical. Before treating this as a driver, confirm it's actually causing friction.

**Findings unique to this lens:**
1. The economic case for extraction is unquantifiable without the absolute incident count — 40% of 5 incidents/month justifies a bug fix sprint, not a 4-month extraction project.
2. Operational overhead of a separate service may outweigh savings if the team is small; 3 engineers touching a subsystem over 6 months suggests modest team size.
3. The weekly deploy cadence only provides extraction value if deployment conflicts are actually occurring — this should be confirmed in incident data before being used as a justification.

**Contradictions with previous lenses:**
- Technical and Adversarial lenses engaged with extraction as architecturally valid. Business lens challenges whether the economics justify it, particularly for a team that may be small. The contradiction is: extraction may be architecturally right and economically wrong simultaneously.

**Risks:**
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Extraction takes 5 months but breaks even in 4 years — not worth it | Medium | High | Do a break-even analysis with real incident cost numbers before committing |
| Small team can't absorb operational overhead of a new service | Medium | High | Count current services in the estate; assess operational overhead per service |
| Incident rate reduction is partial (external providers still fail); ROI lower than projected | High | Medium | Forecast incident reduction by root cause type, not overall percentage |

**Open questions:**
- What is the absolute incident count per month? What fraction are P1/P2?
- How large is the total engineering team?
- How often do notification changes conflict with other deployment changes in practice?
- Is there an SLA on notification delivery that's being breached?

---

### Lens 4: Temporal

**Focus question:** What does the notification domain look like in 2-3 years, and does the extraction decision hold up under that trajectory?

**Analysis:**

*Sub-question 1: Is the notification subsystem likely to grow significantly?*

Notification systems have a well-known growth trajectory: new channels (in-app, WhatsApp, Slack webhooks), templating engines, user preference management, A/B testing on notification content, delivery scheduling, throttling, deduplication, and compliance logging. If the product is growing and notification features are on the roadmap, the 8,000 lines will become 15,000-20,000 lines within two years. A service boundary becomes more defensible as complexity grows; the question is whether to extract now under incident pressure or plan a deliberate extraction.

*Sub-question 2: Is the monolith on a decomposition trajectory?*

If the organisation is already planning to extract other subsystems, notification extraction fits the direction of travel and amortises the investment in service infrastructure (deploy pipeline, service mesh, monitoring patterns). If this would be an isolated extraction — monolith stays, one service extracted — you've taken on distributed systems complexity with none of the organisational scale benefits. A one-service microservices architecture is often worse than both alternatives.

*Sub-question 3: What is the team trajectory?*

If the notification engineers leave, an extracted service needs runbooks, architecture docs, and onboarding material. A well-bounded service can actually make onboarding easier (clear domain, clear interface). But if the team stays small and notification is considered "platform," extraction creates context-switching overhead without ownership clarity.

**Findings unique to this lens:**
1. If notification features are on the product roadmap (new channels, preference management, scheduling), extraction value grows over time — the question is whether to extract *now* under incident pressure or *plan* it deliberately in 3-6 months with better preparation.
2. Extracting notifications as a one-off (monolith stays otherwise intact) creates a two-piece system with distributed systems complexity but none of the organisational scaling benefits — this is often the worst outcome.
3. The notification domain has high churn potential as products scale — every new product line, geography, or compliance requirement touches notifications — which argues for an independent deploy cadence eventually.

**Contradictions with previous lenses:**
- Business lens warned against extraction for small teams given operational overhead. Temporal lens argues extraction becomes more economical as the domain grows. The resolution is timing: extracting *now* under incident pressure has high risk and unclear ROI, while *planning* extraction as a deliberate investment in 3-6 months (after fixing immediate causes) has better economics.

**Risks:**
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Extraction is completed; monolith otherwise stays — distributed system complexity with no scale benefit | Medium | Medium | Clarify whether this is part of a broader decomposition strategy before starting |
| Notification domain grows faster than expected; early extraction under-designs the API contract | Low | High | Design the contract as events (not RPCs) to remain extensible |
| Key engineers leave during or after extraction, leaving an undocumented service | Medium | High | Runbooks and architecture docs must be acceptance criteria for the extraction |

**Open questions:**
- Is there a broader microservices strategy, or would this be an isolated extraction?
- What notification features are on the 12-month product roadmap?
- Is the team growing, stable, or shrinking?

---

### Lens 5: Simplicity

**Focus question:** What is the minimum effective intervention, and is extraction necessary to achieve it?

**Analysis:**

*Sub-question 1: Can the incident rate be materially reduced without extraction?*

Most notification subsystem incidents in Rails monoliths trace to a small set of patterns: missing circuit breakers on provider calls (a Twilio outage backs up the queue and causes cascading retries), misconfigured retry logic (thundering herds on provider recovery), missing idempotency keys (duplicate sends after retries), and DB lock contention from notification workers. Each of these can be fixed in the existing codebase in 1-4 weeks. If the top 3 incident root causes can be identified and fixed in place, the incident rate could drop from 40% to 10-15% without extraction.

*Sub-question 2: Is there a "module boundary" short of full extraction that provides meaningful isolation?*

Rails engines and well-defined module namespaces (`Notifications::`) can create a logical boundary without a physical service boundary. The notification code can be wrapped in a namespace with a clearly defined public interface, tested independently, and constrained to not reference models outside its namespace — all without distributed systems complexity. This "internal service" approach provides code isolation, independent testability, and a clean interface that would make eventual extraction far cheaper. It's not a permanent answer but it's a valuable intermediate step.

*Sub-question 3: What does the minimum viable intervention look like?*

Phase 1 (4-6 weeks): (1) root-cause the last 15 notification incidents, (2) fix the top 3 causes, (3) add circuit breakers and proper retry logic, (4) wrap the subsystem in a `Notifications::` namespace with a clean interface, (5) add structured logging and per-channel metrics.

This is the cheap path. If it fails — if the incident rate remains above 25% after 8 weeks — then extraction is the evidence-backed answer, with a much cleaner codebase to extract from.

**Findings unique to this lens:**
1. A phased approach — fix in place first, extract only if insufficient — dramatically reduces risk and preserves optionality while generating the root-cause data needed to justify the extraction decision.
2. Rails module namespacing (`Notifications::` engine/namespace with a defined interface) provides most of the coupling benefits of a service boundary at a fraction of the cost — and makes eventual extraction cheaper by pre-defining the interface.
3. The 40% figure may be a monitoring artifact. If the notification subsystem is the only well-instrumented part of the monolith, you're measuring a proportion of a non-representative sample. Adding observability everywhere first may reveal a different picture.

**Contradictions with previous lenses:**
- Technical, Adversarial, and Temporal lenses all accept extraction as a valid path and discuss how to do it. Simplicity challenges whether it's necessary. This is the most significant tension in the analysis: the other four lenses ask "how should we extract?" while Simplicity asks "should we extract at all, and why now?"
- This contradiction is load-bearing: if you skip this lens, you commit to extraction by default, when the evidence doesn't yet require it.

**Risks:**
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Fix-in-place reduces incidents partially but not enough, "wasting" 6 weeks | Medium | Low | This is acceptable — 6 weeks of learning is far cheaper than a failed extraction and surfaces root-cause data |
| Team interprets "fix in place" as "we're not extracting ever" and the problem is never fully resolved | Medium | Medium | Set explicit extraction trigger criteria upfront: "if incident rate > X% after 8 weeks, we extract" |
| Simplicity lens misses a structural coupling problem that only extraction can solve | Low | High | Technical lens analysis shows only cascading deployment failures are uniquely solved by extraction — confirm via root-cause data |

**Open questions:**
- What are the top 3 causes of notification incidents? (This question has appeared in every lens — it is the single most important input to this decision.)
- Has resiliency hardening (circuit breakers, retry logic) been attempted and failed?
- What is the current test coverage of the notification subsystem?

---

## Step 4 — Synthesis

### Convergent findings

| Finding | Supported by | Confidence | Implication |
|---|---|---|---|
| The root cause of the 40% incident rate is unknown and must be identified before committing to extraction | Technical, Adversarial, Simplicity | **High** | Do not commit to extraction without incident retrospectives — this is the single most important input |
| Extraction solves deployment coupling but may not solve provider reliability, code quality, or observability gaps | Technical, Adversarial, Simplicity | **High** | Extraction is a partial solution; set realistic expectations and measure by root cause, not total percentage |
| The migration phase is independently high-risk and requires an incremental plan | Adversarial, Business, Temporal | **High** | If extracting, extract one channel at a time with explicit rollback criteria at each stage |
| Team size, microservices strategy, and product roadmap significantly change the economics | Business, Temporal | **Medium** | Five open questions must be answered before the decision has high confidence |

### Tensions and trade-offs

| Tension | Lens A | Lens B | Recommended resolution | Rationale |
|---|---|---|---|---|
| Extract now vs. fix in place | Technical/Temporal: extraction is architecturally valid and forward-looking | Simplicity/Business: extraction is expensive and may not address root causes | **Fix in place first, with explicit extraction trigger criteria** | Lower risk, preserves optionality, generates root-cause data that either justifies or eliminates extraction |
| Speed of relief vs. quality of solution | Business: incident rate has ongoing cost; urgency is real | Adversarial: migration phase increases risk before it decreases it | **Parallel path: immediate resiliency fixes + extraction planning** | Immediate fixes address the incident rate; extraction planning proceeds so you're ready if fixes are insufficient |
| Small team overhead vs. long-term scalability | Business: separate service has real operational overhead | Temporal: notification domain will grow and reward independent deploys | **Condition extraction on team growth and notification roadmap** | Extract if team and domain are growing; defer if both are stable |

### Blind spots filled

| Blind spot | Revealed by | Would have caused | Prevention |
|---|---|---|---|
| Extraction doesn't fix external provider failures | Adversarial | Extraction completed; incident rate unchanged; team demoralized | Root-cause incidents by type before any architectural intervention |
| Migration phase is itself a high-risk period | Adversarial | High-severity incident during extraction window; no rollback plan | Plan incremental extraction with explicit rollback criteria before committing |
| 40% figure may be a monitoring artifact | Simplicity | A major architectural decision driven by a proportion of a non-representative sample | Audit observability coverage across the monolith before drawing conclusions |
| Business case depends on absolute incident volume | Business | Investment decision made without proportionality check | Always anchor percentage figures to absolute counts and engineer-hours |
| One-off extraction (monolith otherwise intact) may be the worst outcome | Temporal | Distributed system complexity with no organisational scale benefit | Clarify whether this is part of a broader decomposition strategy |

### Revised problem framing

**Original framing:** Should we extract the notification subsystem to reduce incidents?

**Revised framing:** The notification subsystem generates 40% of production incidents, but the root causes are uncharacterised. Before committing to extraction (a 3-6 month investment with its own high-risk migration phase), we need to determine whether those incidents stem from: code quality and missing resiliency patterns (fixable in place in 4-6 weeks), deployment coupling (uniquely solved by extraction), or external provider dependencies (not solved by extraction at all). The decision is not binary — a fix-in-place phase should precede the extraction decision, and extraction should only proceed as a confirmed, deliberate investment aligned with a broader decomposition strategy.

**Key difference:** The original framing assumes extraction is the solution and asks whether to do it. The revised framing asks whether extraction is the right solution, and requires evidence before committing to it.

### Refined success criteria

| Criterion | Source | Metric | Threshold |
|---|---|---|---|
| Incident rate reduction | Business, Adversarial | % of production incidents from notification subsystem | Below 15% within 6 months of intervention |
| No migration regression | Adversarial | P1/P2 incident count during extraction window vs. 6-week baseline | Zero increase in P1/P2 count |
| Independent deploy capability | Temporal, Technical | Notification-only changes deployable without monolith deploy | 100% of notification-only changes |
| Operational overhead acceptable | Business | Hours/week maintaining notification service vs. current | No more than 1.5× current maintenance burden |
| Root cause characterised | Simplicity, Technical | % of notification incidents with documented root cause before decision | 100% — this is a gate, not a metric |

---

### Recommendation

**Recommendation:** Do not extract yet. Run a 6-week "fix and characterise" sprint first. Extraction is a live option, not a rejection — trigger it if the sprint is insufficient.

**Sprint plan:**
1. Pull the last 15 notification incidents and root-cause each one. Categorise into: provider failures, code quality/resiliency, deployment coupling, resource contention.
2. Fix the top 2-3 categories in place: add circuit breakers on all provider calls, fix retry logic (exponential backoff + jitter + idempotency keys), set worker pool limits.
3. Wrap the subsystem in a `Notifications::` namespace with a defined public interface. This costs little and makes extraction far cheaper if you proceed.
4. Add structured logging and per-channel metrics so the post-sprint measurement is trustworthy.
5. After 6 weeks, measure. If incident rate is still above 25%: extract. If it drops below 20%: you solved the problem at 10% of the cost.

If extraction is confirmed, extract incrementally: email first (lowest real-time sensitivity), then SMS, then push. Use an async message contract (events, not RPCs) so the monolith is not synchronously coupled to the notification service.

**Confidence:** Medium — the technical and business analysis is strong, but five critical questions remain unanswered (root cause breakdown, absolute incident count, team size, microservices strategy, notification roadmap). The recommendation would shift to High confidence once those are answered.

**Key risks:**
1. Root-cause analysis reveals deep structural coupling (circular model dependencies, shared transactions) where extraction is genuinely the only path — the sprint surfaces this within 2 weeks, so it's still the right first step.
2. Leadership pressure to "do something big" makes the fix-in-place approach feel inadequate — frame it explicitly as Phase 1 of a possible extraction, not a rejection of it, and set clear trigger criteria.
3. The sprint is treated as "done" if it partially works — set the threshold explicitly upfront: "if incident rate is still above 25% after 8 weeks, we extract, no further debate."

**Next steps:**
1. **This week:** Pull or create post-mortems for the last 15 notification incidents. Categorise by root cause. This is the gate for everything else.
2. **Weeks 2-4:** Fix top 2-3 root causes in place. Add `Notifications::` namespace boundary. Add structured logging and per-channel metrics.
3. **Week 6:** Measure incident rate against baseline. Gate the extraction decision on the data.
4. **In parallel now:** Clarify whether there is a broader microservices strategy and what's on the notification feature roadmap. This shapes the extraction design if you proceed.

**What would change this recommendation:**
- If root-cause analysis shows >50% of incidents are caused by deployment coupling (a notification deploy bringing down the monolith, or vice versa): extract immediately — that's a structural problem only extraction fixes.
- If the team is >25 engineers and microservices decomposition is already in motion: the business case for extraction improves substantially; move extraction forward rather than running the sprint first.
- If there is a hard contractual SLA on notification delivery that is being systematically violated: urgency overrides the phased approach; extract while simultaneously fixing resiliency.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-01 |
| Target duration | 283974 ms |
| Target cost | $0.2435 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 produces a complete problem framing with problem statement, context, constraints, stakeholders, current state, and desired state | PASS | Step 1 explicitly lists all six elements: Problem ('Whether to extract...'), Context ('single largest source of production incidents'), Constraints ('8,000-line Rails codebase; 3 engineers; weekly deploy cadence; unknown team size'), Stakeholders ('Notification engineers, on-call engineers, end users, product/business'), Current state ('Subsystem embedded in monolith, 40% of production incidents'), Desired state ('Lower incident rate, predictable deployments, faster notification iteration') |
| c2 | Step 2 selects 3-5 lenses from the eight available and states which were chosen and why | PASS | Step 2 presents a table selecting exactly 5 lenses (Technical, Adversarial, Business, Temporal, Simplicity) each with a 'Why selected' column explaining the reasoning specific to this decision |
| c3 | Lens selection includes at least one human lens (User or Business) and one system lens (Technical or Edge case) per the skill's selection rules | PASS | Business lens serves as the human lens ('Large investment; proportionality check is required'); Technical lens serves as the system lens ('Any extraction decision requires understanding the coupling, new failure modes') |
| c4 | Each lens analysis produces at least one finding not surfaced by any previous lens — not just restating earlier observations | PASS | Technical: unique DB access coupling issue ('notification service likely needs access to user/preference data from the monolith'). Adversarial: unique security attack surface ('standalone notification service...is a high-value security target'). Business: unique proportionality issue ('40% of 5 incidents/month justifies a bug fix sprint'). Temporal: unique one-off extraction risk ('one-off extraction...is often worse than both alternatives'). Simplicity: unique namespace boundary idea ('Rails engines and well-defined module namespaces') |
| c5 | Contradictions between lenses are explicitly called out — not smoothed over | PASS | Each lens has a 'Contradictions with previous lenses' section. Adversarial: 'Together: don't extract unless you're committed to doing it carefully.' Business: 'extraction may be architecturally right and economically wrong simultaneously.' Simplicity: 'the most significant tension in the analysis: the other four lenses ask how should we extract? while Simplicity asks should we extract at all' |
| c6 | Step 4 synthesis produces a convergent findings table, a tensions table with recommended resolutions, and a clear recommendation | PASS | Step 4 contains: 'Convergent findings' table with 4 rows showing supporting lenses and confidence; 'Tensions and trade-offs' table with 3 tensions, both lenses, and 'Recommended resolution' column; Recommendation section: 'Do not extract yet. Run a 6-week fix and characterise sprint first.' |
| c7 | Revised problem framing at the end of Step 4 differs from the Step 1 framing in a meaningful way | PASS | Original framing: 'Should we extract the notification subsystem to reduce incidents?' Revised framing: 'root causes are uncharacterised...the decision is not binary — a fix-in-place phase should precede the extraction decision.' Explicitly notes: 'The original framing assumes extraction is the solution and asks whether to do it. The revised framing asks whether extraction is the right solution' |
| c8 | Confidence level for the recommendation is stated with the evidence basis (not just "Medium confidence" but what data would raise or lower it) | PARTIAL | States 'Medium — the technical and business analysis is strong, but five critical questions remain unanswered (root cause breakdown, absolute incident count, team size, microservices strategy, notification roadmap).' Also lists specific conditions that would change the recommendation: '>50% incidents from deployment coupling → extract immediately', '>25 engineers + microservices in motion → move forward', 'hard contractual SLA violated → extract while fixing' |
| c9 | Output's problem framing reproduces the prompt's specific facts — 8,000 lines, 3 engineers in 6 months, 40% of incidents originate here, weekly monolith deploys, three channels (email/push/SMS) — and ties them to the decision | PASS | Step 1 Constraints section: '8,000-line Rails codebase; 3 engineers with context; weekly deploy cadence.' Problem: 'email, push, and SMS.' '40% incident rate' appears throughout. Business lens: '3 engineers touched the notification code in 6 months.' All facts are tied to the analysis (e.g., weekly deploys tied to deployment coupling argument) |
| c10 | Output selects 3-5 lenses and names them — e.g. Technical (extraction cost vs benefit), Operational (deploy independence, blast radius), Team (cognitive load, expertise), Business (incident reduction value), User (delivery reliability) — and explains why each was chosen for THIS decision | PASS | Step 2 table names 5 lenses and gives decision-specific justifications: Technical: 'extraction decision requires understanding the coupling, new failure modes...in Rails'; Adversarial: '40% incident rate is the core pain signal — need to challenge whether extraction addresses it'; Business: 'Large investment; proportionality check is required'; Temporal: 'Extraction is a long-term bet'; Simplicity: 'Counterweight — the instinct to extract is strong' |
| c11 | Output's lens selection includes at least one human lens (Team or Business or User) AND one system lens (Technical or Operational or Edge case) per the skill's selection rules | PASS | Business lens is the human lens. Technical lens is the system lens. Both are present and substantively analyzed. |
| c12 | Output addresses the 40% incident origination directly — does extracting the service reduce the blast radius (yes — incidents stay isolated to notifications) or just shift the failure surface (now needs reliable inter-service comms) | PASS | Technical lens: 'Extraction introduces new failure modes (network partition, inter-service auth failures, queue depth) that don't exist today — the incident count could increase.' Also: 'Extraction only definitively solves one of these four categories' (deployment coupling). Adversarial lens: 'are we proposing open-heart surgery when the patient needs antibiotics?' Both shifting and reducing blast radius are directly addressed. |
| c13 | Output's lens analyses produce DIFFERENT findings — the technical lens surfaces e.g. "service extraction cost ~3 engineer-months", the operational lens surfaces "deploy frequency could go from weekly to daily for notifications", the team lens surfaces "ownership clarification" — not all converging on the same point | PASS | Technical: DB access coupling issue. Adversarial: migration phase itself is high-risk; security attack surface created. Business: absolute incident count required for proportionality; operational overhead per service. Temporal: notification domain growth trajectory; one-off extraction is worst outcome. Simplicity: Rails namespace boundary as cheaper alternative; monitoring artifact hypothesis. These are substantively different findings. |
| c14 | Output's contradiction-surfacing step calls out tensions between lenses explicitly — e.g. "the team lens favours extraction (clear ownership), the operational lens cautions extraction (operational complexity for the same 3 engineers)" | PASS | Tensions table explicitly names both lenses per row: 'Extract now vs. fix in place: Technical/Temporal vs. Simplicity/Business'; 'Speed of relief vs. quality of solution: Business vs. Adversarial'; 'Small team overhead vs. long-term scalability: Business vs. Temporal.' Individual lens sections also have 'Contradictions with previous lenses' subsections. |
| c15 | Output's synthesis produces a convergent findings table (where lenses agree), a tensions table (where lenses disagree, with proposed resolution path), and a clear recommendation | PASS | Step 4 contains all three: 'Convergent findings' table (4 rows), 'Tensions and trade-offs' table (3 rows with 'Recommended resolution' and 'Rationale' columns), Recommendation: 'Do not extract yet. Run a 6-week fix and characterise sprint first.' |
| c16 | Output's recommendation considers the alternative of fixing-in-place — extracting is one option, addressing the 40% incident root causes within the monolith is another, and the synthesis weighs both rather than only debating extraction | PASS | Simplicity lens is entirely about fix-in-place. The recommendation: 'Do not extract yet. Run a 6-week fix and characterise sprint first.' Sprint plan explicitly describes fixing in place: 'add circuit breakers on all provider calls, fix retry logic, wrap the subsystem in a Notifications:: namespace.' Sprint outcome gate: 'If incident rate is still above 25%: extract. If it drops below 20%: you solved the problem at 10% of the cost.' |
| c17 | Output's revised problem framing differs from the Step 1 framing — e.g. shifts from "should we extract?" to "what's driving the 40% incidents, and is extraction the leverage point?" | PASS | Step 1 framing: 'Whether to extract the notification subsystem.' Revised framing: 'root causes are uncharacterised...we need to determine whether those incidents stem from: code quality and missing resiliency patterns (fixable in place), deployment coupling (uniquely solved by extraction), or external provider dependencies (not solved by extraction at all).' Explicitly notes original assumed extraction is the solution; revised asks whether it is. |
| c18 | Output's confidence level is stated with the evidence basis — e.g. "MEDIUM confidence; would rise to HIGH if we had a 2-week incident root-cause analysis showing they're notifications-internal vs HIGH if they're integration boundaries" | PARTIAL | States 'Medium — five critical questions remain unanswered.' Lists specific data that would change recommendation: '>50% incidents are deployment coupling → extract immediately', '>25 engineers and microservices in motion → move extraction forward', 'hard contractual SLA violated → extract while fixing.' This is a solid evidence basis, meeting the PARTIAL ceiling. |

### Notes

The captured output is an exceptionally thorough iterative-depth analysis that meets or exceeds every criterion. The five-lens structure is well-executed with genuine differentiation between lenses — each surfaces findings the others don't. The explicit 'Contradictions with previous lenses' subsections in each lens analysis are a strong feature, as is the Simplicity lens serving as a genuine counterweight rather than just endorsing extraction. The synthesis is complete with convergent findings, tensions with resolutions, blind spots identified, revised problem framing, refined success criteria, and a concrete sprint plan recommendation. The confidence statement names five specific unanswered questions and three concrete conditions that would change the recommendation, which meets the PARTIAL ceiling for c8 and c18. No criteria were missed or addressed only superficially.
