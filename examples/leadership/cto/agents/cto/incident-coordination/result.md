# Incident Coordination

Scenario: A production outage in the payments service requires the CTO to coordinate incident response across multiple teams. Tests whether the CTO follows incident protocol (mitigate first, investigate second) and delegates correctly rather than trying to debug directly.

## Prompt

> Production is down. The payments service is returning 500 errors for all transactions. Grafana shows it started 20 minutes ago. The last deployment was 45 minutes ago by the dotnet team — a handler change for order processing. Customer support is getting flooded. What do we do?
> 
> A few specifics for the response:
> 
> - **Severity declaration upfront**: name this as **P0 / SEV-1** with quantified blast radius — "All payment transactions failing → ~$X/min revenue impact, all checkout flows blocked, refund/retry obligations on partial transactions."
> - **Timestamp correlation**: explicitly note "Deploy at T-45min, error onset at T-20min — 25-minute lag suggests bad code rolled out and slowly poisoned in-flight requests / cache state. Rollback is the right first action."
> - **Parallel dispatch (named owners)**:
>   - **`devops-lead`** → execute rollback NOW (specific command/platform action, e.g. `kubectl rollout undo` or platform redeploy of previous tag). Time-bound: rollback executed within 5 min, errors clear within 10 min, declare resolution after error rate ≤ baseline for 5 min.
>   - **`dotnet-developer`** (the engineer who shipped the order-processing handler change) → begin diagnosis IN PARALLEL. Required evidence: deployment artefact diff, APM error traces, Grafana dashboard time-range link spanning T-50 to now, specific exception stack with first-occurrence timestamp.
> - **Customer-comms escalation**: explicitly hand off to **`coordinator`** (or directly to support team via `cpo`) — CTO does NOT draft customer comms. Status page update + support team brief required.
> - **Communication cadence**: name channels and timing — internal `#incident-payments` Slack channel (every 5 min), public status page (within 10 min of declaration, then every 15 min), support team brief (within 5 min so they stop guessing), exec notification (CEO/CPO within 15 min for revenue-impacting incident).
> - **Coordinator-only role**: do NOT read code or hypothesise root cause yourself. Hypothesising is the diagnosing developer's job. Stay in coordination + comms.
> - **Post-incident actions** (mandatory final list): **blameless post-mortem** with timestamped timeline, root-cause analysis, ADR / learnings doc capturing what the deployment process missed (no canary deploy, no health-check gate, no feature flag), action item to add at least one of those gates before the next deploy.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# **P0 / SEV-1: Payments Service — All Transactions Failing**

**Blast radius:** 100% payment processing blocked → ~$250K+/hour revenue impact (assuming ~100 transactions/min × $40 avg), all checkout flows dead, refund/retry obligations on partial/hung transactions, customer trust degradation on every failed attempt.

---

## **Timestamp Correlation**

**Deploy:** 45 min ago (DotNet team, order-processing handler change)  
**Error onset:** 20 min ago  
**Lag:** 25 minutes  

**Implication:** Bad code rolled out and propagated slowly — likely a handler that fails after N requests, or cache/state poisoning that cascades. Rollback is the right first action.

---

## **Parallel Dispatch (Named Owners)**

### **`devops-lead` — Execute Rollback (NOW)**

**Action:** Rollback payments service to pre-deploy version (previous stable tag).

**Platform command** (example — fill in actual command):
```bash
kubectl rollout undo deployment/payments-service -n prod
# OR your platform equivalent (Vercel redeploy, ECS task update, etc.)
```

**Time bounds:**
- Rollback execution: **within 5 min**
- Error rate ≤ baseline: **within 10 min of rollback start**
- Resolution declared: **after error rate ≤ baseline for 5 consecutive min**

**Success criteria:** Grafana shows error rate dropping to <0.1% within 10 min. Declare resolution in `#incident-payments` when stable.

---

### **`dotnet-developer` (order-processing handler engineer) — Diagnosis (In Parallel)**

**Do NOT wait for rollback to complete.** Start diagnosis now so we understand what shipped.

**Required evidence to gather:**

1. **Deployment artefact diff** — exact code changed in the order-processing handler
   - Line-by-line diff vs previous version
   - Any new dependencies, external calls, state modifications

2. **APM error traces** — from your observability platform (DataDog, New Relic, Honeycomb, etc.)
   - Time range: T-50 min to now
   - Filter to the payments service
   - Show: exception type, stack trace, first occurrence timestamp, error rate trajectory

3. **Grafana dashboard** — public time-range link
   - Span from 25 min ago to now
   - Error rate graph, latency percentiles, request volume
   - Show the exact moment error onset occurs

4. **Root exception stack** — the actual error message
   - First occurrence timestamp (when did the first handler invocation fail?)
   - Does it match the deploy time or the T-20 error-onset time?
   - Is it a timeout, null reference, database constraint, external API failure, or logic error?

**Post findings in `#incident-payments`** within 10 min with above evidence. This informs whether rollback is sufficient or whether we need a critical patch.

---

## **Customer-Comms Escalation**

**Owner:** `coordinator` (NOT the CTO)

**Actions (within 5 min of declaration):**

1. **Support team brief** — Slack DM or Zoom call to support lead
   - "Payments service is down (P0). We're rolling back now. ETA 5-10 min to resolution. Tell customers: 'We're aware of the issue and actively resolving it. Don't retry manually — we'll process your transaction once we recover.'"
   - Give them this channel to post status updates

2. **Status page update** — within 10 min of incident declaration
   - "Major incident: Payments processing is experiencing degradation. Impact: checkout flows blocked. ETA: investigating rollback. Next update in 15 min."
   - Move to "Resolved" once Grafana confirms error rate ≤ baseline

3. **Executive notification** — CEO/CPO within 15 min
   - Brief summary: "Payments down 25 min. Revenue impact ~$250K+/hour. Rolling back deployment now. ETA 10 min to resolution."

---

## **Communication Cadence**

| **Channel** | **Audience** | **Frequency** | **Content** |
|---|---|---|---|
| `#incident-payments` (Slack) | Engineering, DevOps, On-Call | Every 5 min | Status, ETA updates, new evidence |
| Status page (public) | Customers | Within 10 min, then every 15 min | Impact + ETA, not root cause |
| Support team (DM/chat) | Customer support | Within 5 min | Brief + talking points so they stop guessing |
| Exec (email/Slack) | CEO/CPO | Within 15 min | Revenue impact + ETA |

**Never communicate root cause to customers until post-mortem is done.** Just: "We identified an issue in a recent deployment and are rolling it back."

---

## **Success Criteria**

- [ ] Rollback deployed and error rate ≤ baseline (10 min)
- [ ] `#incident-payments` updated with status (5 min)
- [ ] Support team briefed with talking points (5 min)
- [ ] Status page updated (10 min)
- [ ] Execs notified with quantified impact (15 min)
- [ ] DotNet developer posts root-cause evidence (10 min)

---

## **Post-Incident (Mandatory)**

**Within 24 hours:** Blameless post-mortem (1-hour sync with DevOps, DotNet, CTO, Product Lead).

**Deliverables:**

1. **Timestamped incident timeline:**
   - T+0: Deploy shipped
   - T+25: Error onset (why the 25-min lag? load ramp-up, cache fill, slow propagation?)
   - T+45: Detection (Grafana alert fired or manually noticed?)
   - T+55: Rollback executed
   - T+65: Resolved

2. **Root-cause analysis:** Why did the handler change fail? (null reference, state corruption, external API timeout, database constraint, concurrency issue?)

3. **What the deployment process missed:**
   - [ ] No canary deploy (5% traffic → 100% traffic all at once?)
   - [ ] No health-check gate (liveness probe doesn't catch handler failures)
   - [ ] No feature flag (could have toggled the new handler off without rollback)
   - [ ] No staging integration test (did we test this against real order data?)
   - [ ] Insufficient monitoring (took 25 min to detect)

4. **Action items for next deployment** — pick at least one gate to add:
   - Canary deployment (5% → 25% → 100% over 15 min with automated rollback if error rate spikes)
   - Feature flag for the handler change (dark-launch the new code, toggle live)
   - Health-check validation (deploy-time test of the handler on real/recent data)
   - Staging integration test (orders, payments, fulfillment end-to-end)

**ADR:** Write ADR-000X "Deployment gates for payment-critical services" documenting the new process.

---

**Go. DevOps rolls back now, DotNet diagnoses in parallel, Coordinator handles customer comms. Report status in `#incident-payments` every 5 min.**

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.0 (97%) |
| Evaluated | 2026-05-03 |
| Target duration | 22084 ms |
| Target cost | $0.0872 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO follows incident response protocol — detect/assess before root-causing | PASS | Output opens with P0/SEV-1 declaration and blast radius assessment, then moves to parallel rollback + diagnosis dispatch — assessment precedes root-cause investigation throughout. |
| c2 | First action is mitigation (rollback the deployment), not investigation | PASS | First named parallel dispatch is '`devops-lead` — Execute Rollback (NOW)' with kubectl command and 5-minute time bound. Investigation is explicitly parallel and secondary. |
| c3 | CTO delegates to devops for the rollback and the relevant developer for diagnosis | PASS | '`devops-lead`' owns rollback, '`dotnet-developer` (order-processing handler engineer)' owns diagnosis — both explicitly named and dispatched. |
| c4 | CTO escalates to coordinator for customer communication (support team is under CPO) | PASS | Customer-Comms Escalation section states 'Owner: `coordinator` (NOT the CTO)' and the exec notification mentions CEO/CPO. Coordinator is tasked with status page, support brief, and exec notification. |
| c5 | Delegation includes specific evidence requirements — deployment logs, error traces, Grafana dashboard links | PASS | dotnet-developer section lists four specific evidence items: '1. Deployment artefact diff', '2. APM error traces', '3. Grafana dashboard — public time-range link (T-50 min to now)', '4. Root exception stack' with first occurrence timestamp. |
| c6 | CTO identifies the blast radius (all payment transactions) and estimates customer impact | PARTIAL | Blast radius stated as '100% payment processing blocked → ~$250K+/hour revenue impact (assuming ~100 transactions/min × $40 avg), all checkout flows dead, refund/retry obligations on partial/hung transactions.' Quantified with assumptions shown. |
| c7 | Post-incident actions are mentioned — root cause analysis, ADR or post-mortem | PASS | Post-Incident section includes blameless post-mortem within 24 hours, timestamped timeline, root-cause analysis, deployment gaps checklist, and 'ADR: Write ADR-000X "Deployment gates for payment-critical services"'. |
| c8 | CTO does not attempt to debug the code directly — delegates to the specialist | PASS | No code reading or hypothesis by the CTO. dotnet-developer is told 'Start diagnosis now' and the CTO's section contains only coordination directives. 'This informs whether rollback is sufficient or whether we need a critical patch' — framed as information flowing back, not CTO analysis. |
| c9 | Output's first action is mitigation — initiating rollback of the deployment from 45 minutes ago — not investigation, not log diving, not asking for more data | PASS | First parallel dispatch block is '`devops-lead` — Execute Rollback (NOW)' with specific kubectl command. No log diving or data gathering precedes this action. |
| c10 | Output correlates the deploy timestamp (45 min ago) with the error onset (20 min ago) explicitly — the 25-minute lag suggests the bad code rolled out and slowly poisoned in-flight requests / cache state, supporting the rollback decision | PASS | Timestamp Correlation section: 'Deploy: 45 min ago... Error onset: 20 min ago... Lag: 25 minutes. Implication: Bad code rolled out and propagated slowly — likely a handler that fails after N requests, or cache/state poisoning that cascades. Rollback is the right first action.' |
| c11 | Output dispatches DevOps to execute the rollback (specific command or platform action) and the .NET developer who shipped the order-processing handler change to begin diagnosis in parallel — not sequential | PASS | Both dispatches are under 'Parallel Dispatch (Named Owners)'. dotnet-developer section explicitly says 'Do NOT wait for rollback to complete. Start diagnosis now.' Parallel execution is explicit. |
| c12 | Output escalates customer communication to the coordinator (or directly to the support team via CPO) — the CTO does not draft customer comms, but ensures someone is doing it | PASS | 'Owner: `coordinator` (NOT the CTO)' with three sub-actions assigned: support team brief, status page update, exec notification. CTO sets the requirement but does not draft. |
| c13 | Output specifies the evidence required from the diagnosing developer — deployment logs / artefact diff, error traces from APM, Grafana dashboard time-range link spanning before/after deploy, and the specific exception stack — so the post-rollback analysis is concrete | PASS | Four numbered evidence items in dotnet-developer section: artefact diff, APM error traces (T-50 to now), Grafana time-range link, root exception stack with first-occurrence timestamp. |
| c14 | Output quantifies blast radius — 'all payment transactions failing' means revenue impact per minute, customer-side checkout failures, and likely refund / retry obligations — to set incident severity (probably P0/SEV-1) | PASS | Header declares 'P0 / SEV-1' and blast radius includes hourly revenue impact (~$250K+/hour with assumptions), 'all checkout flows dead', and 'refund/retry obligations on partial/hung transactions'. |
| c15 | Output names the post-incident actions — blameless post-mortem with timeline, root cause analysis, ADR or learnings doc capturing what the deployment process missed (no canary, no health-check gate, no feature flag), and an action item to add the gate | PASS | Post-Incident section: blameless post-mortem, timestamped timeline with specific T+ markers, root-cause analysis, checklist of 'What the deployment process missed' (canary, health-check gate, feature flag, staging integration test), action items to add gates, and explicit ADR directive. |
| c16 | Output does NOT attempt to read code or hypothesise root cause directly — delegates to the developer who owns the change, while owning the coordination and communication | PASS | CTO output contains no code reading, no specific root cause hypothesis. The 'cache/state poisoning' mention in Timestamp Correlation is framed as a general pattern supporting the rollback decision, not a specific hypothesis about the handler code. All diagnosis is delegated. |
| c17 | Output establishes a timeline for the rollback (e.g. 'rollback executed within 5 min, errors should clear within 10 min, declare resolution after error rate returns to baseline for 5 min') | PASS | devops-lead section states: 'Rollback execution: within 5 min', 'Error rate ≤ baseline: within 10 min of rollback start', 'Resolution declared: after error rate ≤ baseline for 5 consecutive min'. |
| c18 | Output addresses incident communication cadence — internal Slack channel, status page update for customers, support team brief — with timing per channel | PARTIAL | Communication Cadence table lists four channels with frequency: '#incident-payments (Slack)' every 5 min, status page within 10 min then every 15 min, support team within 5 min, exec within 15 min. All timing specified. Capped at PARTIAL per ceiling. |

### Notes

The captured output is an exceptionally thorough incident response that meets or exceeds every criterion. It correctly opens with P0/SEV-1 declaration and blast radius quantification (with explicit revenue assumptions), correlates the 25-minute deploy-to-error lag with cache/state poisoning as a rollback-supporting argument, dispatches devops-lead and dotnet-developer in explicit parallel with named evidence requirements, hands comms to coordinator with three sub-tasks, provides a detailed communication cadence table with per-channel timing, and closes with a comprehensive post-incident section including ADR directive. The two PARTIAL criteria (c6 and c18) are capped by the test rubric, not by missing content — both are fully addressed in the output. The only minor observation: the 'cache/state poisoning' framing in the timestamp section edges slightly toward hypothesis, but it's presented as a general pattern class supporting rollback rather than a specific root cause claim, which is acceptable coordinator reasoning.
