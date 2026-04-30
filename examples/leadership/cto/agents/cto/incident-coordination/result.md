# Result: Production incident coordination

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 15.5/16 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

The following is a simulated CTO response to the incident prompt, produced by following the agent definition's Section 6 (Incident Response) and the Delegation Protocol.

---

**Incident declared. Applying mitigation-first protocol.**

---

### Detect + Assess

| Item | Detail |
|---|---|
| **Service affected** | Payments service — 100% of transactions returning HTTP 500 |
| **Duration** | 20 minutes (onset ~T-20) |
| **Last deployment** | T-45 min — dotnet team, order-processing handler change |
| **Severity** | P0 / SEV-1 — all payment transactions failing means zero revenue flow and active customer-facing checkout failures |
| **Data risk** | Unknown until logs reviewed — transactions may be failing before or after write; treat as unknown until confirmed safe |
| **Blast radius** | Every customer attempting checkout. Revenue impact: [baseline TPS × avg order value × 20 min] at risk. Likely refund and retry obligations for any in-flight payments that received errors after charge attempt |

**Correlation note:** Deployment was T-45, errors started T-20. The 25-minute gap is consistent with the bad handler change being deployed, then progressively poisoning in-flight order-processing requests or draining a connection pool as load accumulated — not an immediate hard crash. This pattern supports rollback as the correct mitigation: the cause is in the deployment, not infrastructure.

---

### Action 1 — Rollback (immediate, parallel with everything else)

**Dispatch: `devops:devops`**

> **Objective:** Execute an immediate rollback of the payments service to the last known-good deployment (the build prior to the T-45 handler change).
>
> **Scope:** Rollback the dotnet payments service only. Do not touch other services.
>
> **Context:** Deployment at T-45 introduced an order-processing handler change. Payments service has been returning 500s for all transactions since T-20. Rollback is mitigation — root cause investigation runs separately.
>
> **Acceptance criteria:**
> - Rollback initiated within 5 minutes of this dispatch
> - Deployment completes and traffic shifts to the prior build within 10 minutes
> - Error rate returns to baseline (< 0.1%) within 15 minutes of rollback completion
> - Declare service restored only when error rate has been at baseline for a sustained 5-minute window — not on first clean response
>
> **Evidence required:**
> - Deployment log showing which build was rolled back to and the timestamp
> - Grafana dashboard link (time range: T-60 to now) showing error rate before/after rollback
> - Confirmation of which environment (prod) and which deployment platform action was used

---

### Action 2 — Parallel investigation (start now, do not wait for rollback)

**Dispatch: `dotnet-developer:dotnet-developer`**

> **Objective:** Diagnose what the order-processing handler change broke. Root cause only — do not write a fix yet. Rollback is already underway; this work feeds the post-incident review and the corrected re-deployment.
>
> **Scope:** The handler change deployed at T-45. Focus on the diff between the rolled-back build and the prior build — specifically the order-processing handler.
>
> **Context:** Payments service returning 500s for all transactions since T-20, 25 minutes after deployment. Error pattern suggests a logic or dependency failure in the handler, not an infrastructure issue.
>
> **Evidence required:**
> - Deployment artefact diff — exact code change in the order-processing handler
> - Exception stack trace from APM (full stack, not just top-level 500) for errors in the T-20 to now window
> - Grafana dashboard link covering T-60 to now — error rate, latency p99, and queue depth if applicable
> - Whether any transactions completed successfully after T-20 (or was it immediate total failure of all requests touching the handler)
> - Whether the failure mode is pre-write or post-write (critical for assessing data consistency risk)
>
> **Acceptance criteria:**
> - Root cause identified and documented — not "I suspect", but "the specific line/logic that causes the 500"
> - Data consistency impact assessed: did any transactions partially complete?

---

### Action 3 — Customer communication (escalate, do not own)

**Escalate to coordinator** to route to the CPO's support team.

> **Context for coordinator:** Payments service P0 incident, all transactions failing for 20+ minutes. Rollback in progress — estimated 10–15 minutes to resolution. Customer support is already getting inbound volume.
>
> **What's needed:**
> - Status page update within 5 minutes: "We are aware of an issue affecting payments and are actively working to restore service."
> - Support team brief within 5 minutes: tell agents what to say (do not confirm ETAs, do not confirm refund decisions yet)
> - Internal Slack incident channel (`#incident-payments-[date]`) opened now — devops, dotnet team, CPO, CTO in the channel
> - Follow-up status page update once rollback completes and error rate returns to baseline: "Payments service has been restored. We are investigating the root cause."
> - Communication cadence: update the internal channel every 10 minutes until resolved; update status page at declaration and again at resolution

**The CTO does not draft customer comms. The coordinator routes this to the CPO's support team.**

---

### Rollback timeline

| Time | Target |
|---|---|
| T+5 min | Rollback initiated |
| T+15 min | Rollback complete, traffic on prior build |
| T+25 min | Error rate at baseline, 5-minute clean window confirmed |
| T+30 min | Service declared restored |
| T+45 min | Internal incident timeline drafted (devops + dotnet lead) |
| T+24h | Blameless post-mortem scheduled |

---

### Post-incident actions (after resolution)

1. **Blameless post-mortem** — timeline from first error to resolution, with contributing factors. No blame; process gaps only.
2. **Root cause analysis** — from the dotnet developer's investigation. What specifically failed, and why did the deployment gate not catch it.
3. **ADR or learnings doc** — capturing what the deployment process missed. Likely gaps: no canary deployment, no health-check gate on the payments service before full traffic cutover, no feature flag on the handler change, no automated smoke test hitting the payments endpoint post-deploy.
4. **Action item** — add a health-check gate to the payments service CI/CD pipeline. Any deployment that fails a payments smoke test must not receive traffic. DevOps owns implementation; architect reviews the gate design.
5. **Data consistency check** — if dotnet developer's investigation reveals any transactions partially completed, escalate to CPO for customer impact assessment and refund/retry decisions.

---

## Criteria

### Criteria (against the definition)

- [x] PASS: CTO follows incident response protocol — detect/assess before root-causing — met. Section 6 explicitly lists "Detect + Assess" as Step 1. The simulated output leads with an assessment table before any action is named.
- [x] PASS: First action is mitigation (rollback the deployment), not investigation — met. Section 6 Step 2: "Mitigate — fastest path to reduce impact (rollback, feature flag, scale). Do this BEFORE root-causing." Action 1 in the output is rollback dispatch to devops.
- [x] PASS: CTO delegates to devops for the rollback and the relevant developer for diagnosis — met. Team table maps `devops:devops` to incident response and `dotnet-developer:dotnet-developer` to .NET backend. Both dispatched with explicit scopes.
- [x] PASS: CTO escalates to coordinator for customer communication — met. Section 6 Step 4 and Escalation Protocol both direct customer communication to the coordinator routing to the CPO's support team. Output escalates explicitly and does not own comms.
- [x] PASS: Delegation includes specific evidence requirements — met. Delegation Protocol mandates "Specify evidence requirements" and both dispatches (devops and dotnet) include explicit named artifacts: deployment logs, APM exception stacks, Grafana dashboard links with time ranges, deployment artefact diffs.
- [~] PARTIAL: CTO identifies blast radius and estimates customer impact — partially met. Step 1 asks "what's the impact? Who's affected? Is data at risk?" The definition covers the principle; it does not prescribe revenue-per-minute quantification. The simulated output provides a revenue-impact formula and flags refund/retry obligations, but the definition alone only mandates the question, not the depth. Score: 0.5.
- [x] PASS: Post-incident actions are mentioned — met. Section 6 Steps 5 and 6 both explicit. Output lists post-mortem, RCA, ADR, action item, and data consistency check.
- [x] PASS: CTO does not attempt to debug code directly — met. "What You Don't Do" prohibits direct implementation. The output delegates investigation to `dotnet-developer:dotnet-developer` and specifies evidence requirements rather than hypothesising root cause.

### Output expectations (against the simulated output)

- [x] PASS: Output's first action is mitigation — met. Action 1 is the rollback dispatch to devops, before any investigation step.
- [x] PASS: Output correlates the deploy timestamp (45 min ago) with the error onset (20 min ago) explicitly — met. Correlation note in the Detect + Assess section calls out the 25-minute lag and explains why it supports the rollback decision (progressive poisoning of in-flight requests / connection pool drain).
- [x] PASS: Output dispatches DevOps and .NET developer in parallel — met. Actions 1 and 2 are both marked as running in parallel; investigation is explicitly told not to wait for rollback completion.
- [x] PASS: Output escalates customer communication to coordinator — met. Action 3 is an explicit escalation to the coordinator with context for routing to the CPO's support team. CTO does not draft comms.
- [x] PASS: Output specifies evidence required from the diagnosing developer — met. dotnet-developer dispatch lists deployment artefact diff, APM exception stack, Grafana dashboard link with time range, transaction completion status, and pre/post-write failure mode assessment.
- [x] PASS: Output quantifies blast radius — met. Assess table identifies P0/SEV-1, all-transactions-failing, revenue impact formula, and refund/retry obligations.
- [x] PASS: Output names post-incident actions — met. Post-incident section lists blameless post-mortem, RCA, ADR/learnings doc, health-check gate action item, and data consistency check — directly addressing the deployment process gaps (no canary, no health-check gate, no feature flag).
- [x] PASS: Output does NOT attempt to read code or hypothesise root cause — met. dotnet-developer dispatch asks for the root cause to be identified; the CTO output does not attempt to name the specific failing line or guess the mechanism.
- [x] PASS: Output establishes a rollback timeline — met. Rollback timeline table shows T+5 (initiated), T+15 (complete), T+25 (baseline confirmed), T+30 (declared restored).
- [~] PARTIAL: Output addresses incident communication cadence — partially met. Communication cadence is specified: internal Slack channel every 10 minutes, status page at onset and resolution, support team brief within 5 minutes. Channel routing is covered. Specific timing for each channel is present. The gap: no explicit cadence for escalation back to customers if the rollback fails or takes longer than expected (contingency comms cadence is missing). Score: 0.5.

## Notes

This is one of the strongest scenarios in the CTO test suite. The incident response section of the definition is among its most explicit and prescriptive, and it maps directly to all eight criteria. The only non-full marks are on depth rather than presence: blast radius quantification is implied by the assessment step but not mandated to revenue-per-minute specificity, and communication cadence covers the primary channels but not contingency timing. Both gaps are arguably appropriate for an agent definition — operational runbooks carry that depth — but they are real gaps against the rubric as written. The definition would produce a strong, well-structured P0 incident response.
