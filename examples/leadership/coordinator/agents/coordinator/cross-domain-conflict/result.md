# Cross Domain Conflict

Scenario: The coordinator receives a conflict where product delivery (CPO) and security remediation (CTO) are at odds. Both parties have legitimate, time-sensitive concerns and neither can be simply overruled.

## Prompt

> The CPO wants to ship a new onboarding flow by end of month to hit activation targets — it's the top priority for Q2 OKRs. The CTO says the authentication system needs to be rebuilt first because it has a known vulnerability (CVSS 7.8) that security flagged last week, and the new onboarding flow touches auth. Both are right. The CPO says we can't slip the OKR, the CTO says we can't ship with a known vulnerability. What do we do?
> 
> A few specifics for the response:
> 
> - **Sequencing plan with concrete dates and owners** — not "have a meeting". Propose a specific sequence with handoffs (e.g. `Week 1 (CTO): scope auth fix, ship compensating control by Friday → Week 2 (CPO + CTO): scoped onboarding flow that avoids vulnerable surface, ship by EOM → Week 3+: full auth rebuild post-OKR`). Include named owner per step.
> - **Accountability preserved (state explicitly)**: "CPO retains ownership of the onboarding OKR. CTO retains ownership of the auth security fix. Coordinator coordinates; does not take over either workstream."
> - **Deadline options (specific)**: present at minimum two: (1) hit OKR with scoped-down onboarding bypassing auth changes, (2) slip OKR by N days with full security fix first. State the trade-off per option.
> - **Escalation rationale (one paragraph)**: why this needed cross-domain coordination — security trumps feature delivery in the abstract, BUT the OKR is a board commitment, AND a known-vulnerability ship sets a precedent that security flags are negotiable. Frame this systematically.
> - **Executive escalation questions**: include 1-2 questions the coordinator would put to the CEO/board if the trade-off can't settle at CPO+CTO level — e.g. "Are we willing to communicate an OKR slip to the board to ship securely?" and "Does the board accept a scoped-down OKR (X% of the original target) as success?"

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

This is a genuine cross-domain conflict, and it lands at the coordinator level because the resolution requires alignment between CPO and CTO, plus clarity to the board. Neither party is wrong — security can't be deferred indefinitely, and OKRs are board commitments — but the false binary is "ship vulnerable" vs "rebuild auth." The real work is sequencing and scope.

## Sequencing Plan: Three Paths Forward

**Today is May 4. EOM is May 31. ~27 days.**

### Option 1: Parallel + Scoped (Recommended)
Highest probability of hitting OKR *and* remediating vulnerability.

| Phase | Owner | Work | Deadline | Success Criteria |
|-------|-------|------|----------|------------------|
| **Week 1 (May 4–10)** | CTO + Security | Scope CVSS 7.8 vuln; propose compensating control path (rate limit, IP gate, MFA requirement for onboarding) OR fast patch | May 10 | Decision: control or patch; estimate effort |
| **Week 1 (May 4–10)** | CPO + CTO | Right-size onboarding flow; identify which features touch vulnerable auth; map scoped version (70–80% of target) that avoids it | May 10 | Scoped spec, activation target for reduced feature set |
| **Week 2–3 (May 10–24)** | CPO (scoped onboarding) + CTO (compensating control \| patch) | **Parallel**: CPO ships onboarding (avoiding vulnerable surface); CTO ships control or patch | May 24 | Onboarding live; vulnerability mitigated or patched |
| **Week 4+ (May 24+)** | CTO | Full auth rebuild / security hardening (post-OKR) | June 30 | Auth system hardened; technical debt cleared |

**Accountability:**
- **CPO** retains ownership of activation OKR. Scope can shrink, target cannot. Success = activation numbers meet board expectations for scoped feature.
- **CTO** retains ownership of auth security. Vulnerability must be remediated (patch or compensating control) before EOM; full rebuild post-OKR is a separate commitment.
- **Coordinator** ensures dependencies flow (CTO security clarity unblocks CPO scope decisions), escalates if trade-offs deadlock.

---

### Option 2: Security First (Safe, Likely Misses OKR)
Auth rebuild on the critical path; onboarding follows.

| Phase | Owner | Work | Deadline |
|-------|-------|------|----------|
| **Week 1–2 (May 4–17)** | CTO | Scope CVSS 7.8 fix; estimate rebuild effort | May 10 (decision) |
| **Week 2–3 (May 10–24)** | CTO | Ship auth fix or rebuild | May 24 |
| **Week 3–4 (May 24–31)** | CPO | Ship full onboarding flow on fixed auth | May 31 (likely miss) |

**Trade-off:** OKR slips by 1–2 weeks into June. Board conversation required: "We're shipping secure; accepting a slip to avoid a known vulnerability."

---

### Option 3: Compensating Control (Fast, Carries Risk)
Patch the vulnerability with a temporary control; ship onboarding; permanent fix post-OKR.

| Phase | Owner | Work | Deadline |
|-------|-------|------|----------|
| **Week 1 (May 4–10)** | CTO + Security | Implement compensating control (rate limiting + MFA gate on onboarding flow) | May 10 |
| **Week 1–3 (May 4–24)** | CPO | Ship onboarding with control in place | May 24 |
| **Week 3–4 (May 24–31)** | CTO | Ship permanent auth fix | May 31 |

**Trade-off:** Leaves CVSS 7.8 in the codebase (mitigated, not patched) until permanent fix. Security must sign off on risk profile. Board conversation: "We're shipping with a temporary control; permanent fix lands post-OKR."

---

## Why This Needed Coordination

The tension is **not** security vs. speed in the abstract. It's three live constraints: (1) board OKR commitment, (2) known vulnerability that security flagged, (3) the false assumption that "onboarding flow" means "full auth overhaul." The coordinator's job is to decompose the binary into scope (can you ship 70% of the feature and hit activation targets?), parallel work (can security and product work simultaneously?), and risk acceptance (is a compensating control acceptable until the permanent fix ships?). Only cross-domain visibility reveals these moves. A pure security decision says "no features until auth is rebuilt." A pure product decision says "ship and patch later." Coordination asks: "What's the minimum surface you must rebuild, what can ship in parallel, and where do we accept temporary risk?"

---

## Deadline Options: Explicit Trade-Offs

**Option A: Hit OKR on Time (May 31), Accept Scoped Feature**
- Onboarding ships with 70–80% of planned scope (still hits activation target? must verify with CPO)
- Auth vulnerability mitigated (compensating control or patch) by May 24
- Full auth rebuild deferred to June (post-OKR)
- **What you win:** OKR date, vulnerability remediated, product ships. **What you give up:** some planned features, permanent auth fix is deferred.

**Option B: Slip OKR by 2 Weeks (June 14), Ship Fully Secure**
- Auth rebuild completes by May 24
- Full onboarding flow ships on secure auth by June 14
- **What you win:** full feature set, permanent security fix. **What you give up:** OKR slip (board conversation on activation targets), slower time-to-market.

---

## Escalation Questions for CPO + CTO

If the sequencing deadlocks at this level:

1. **Scope negotiation:** "What's the smallest onboarding feature that still drives the activation numbers the board expects? Is 70–80% of the planned scope sufficient to call the OKR a win?" (If not, the scope target and security timeline are incompatible, and the board needs to choose.)

2. **Risk acceptance:** "Can security sign off on a compensating control (MFA + rate limiting) on the vulnerable auth surface for 2–3 weeks while the permanent patch ships?" (If yes, parallel work becomes viable. If no, sequencing is forced.)

3. **Board trade-off (if neither above resolves it):** "Are we comfortable explaining an OKR slip to the board as the cost of shipping securely, or do we need to ask the board whether a 2-week slip is acceptable?" (This escalates to the CEO/board because the OKR is a board commitment, and security + product can't negotiate it away unilaterally.)

---

## Accountability Preserved

- **CPO:** Owns the activation OKR. Can negotiate scope (how much of the feature is truly necessary?), but not the business target. Success is measured by activation numbers, not feature completeness.
- **CTO:** Owns auth security. Can negotiate timeline (compensating control now, patch later? full rebuild? speed estimate?), but not the outcome (vulnerability must be remediated). Success is measured by security posture and delivery date.
- **Coordinator:** Does not own either workstream. Coordinates sequencing, flags dependencies, escalates unsettled trade-offs to leadership. Ensures both owners have what they need to commit to a date.

Start with Option 1 (parallel + scoped). If that deadlocks on scope or risk, move to the escalation questions. The board conversation is a feature, not a bug — it clarifies what trade-off the organization is actually willing to make.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/14.5 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 37755 ms |
| Target cost | $0.0793 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator does not simply side with one party — acknowledges both concerns are legitimate | PASS | Opening paragraph states explicitly: 'Neither party is wrong — security can't be deferred indefinitely, and OKRs are board commitments' and 'Both are right' is implicit in the framing that treats the conflict as a genuine sequencing problem, not a priority contest. |
| c2 | Coordinator assesses whether the work can be sequenced (auth fix first, then onboarding) or must be parallel | PASS | Three distinct options are assessed: Option 1 (parallel + scoped), Option 2 (Security First — sequential, auth then onboarding), and Option 3 (compensating control with parallel work). Each is evaluated with reasoning. |
| c3 | Security vulnerability is treated as a constraint, not a competing priority — CVSS 7.8 is High severity | PASS | CTO accountability statement: 'Vulnerability must be remediated (patch or compensating control) before EOM.' All three options require addressing the vulnerability before or in parallel with shipping onboarding — none defer it entirely. Option 3 explicitly notes security must sign off on the risk profile. |
| c4 | A concrete resolution is proposed with specific sequencing, not 'you two should work it out' | PASS | Option 1 table provides Phase, Owner, Work, Deadline (specific dates: May 4–10, May 10–24, May 24+, June 30), and Success Criteria per row. The output closes: 'Start with Option 1 (parallel + scoped). If that deadlocks on scope or risk, move to the escalation questions.' |
| c5 | The resolution preserves accountability — CPO still owns the onboarding OKR, CTO still owns the security fix | PASS | Option 1 accountability block states: 'CPO retains ownership of activation OKR… CTO retains ownership of auth security… Coordinator ensures dependencies flow… escalates if trade-offs deadlock.' Repeated in the 'Accountability Preserved' closing section. |
| c6 | Coordinator identifies whether the OKR deadline can be adjusted given the security constraint, with specific options | PARTIAL | Option A presents hitting OKR on May 31 with scoped-down onboarding (70–80% of planned scope). Option B presents slipping OKR by 2 weeks to June 14 with full security fix first. Both options have specific dates and named trade-offs. |
| c7 | Escalation framing is clear — the coordinator explains WHY this needed escalation (cross-domain, security vs delivery trade-off) | PASS | 'Why This Needed Coordination' section explains: 'Only cross-domain visibility reveals these moves. A pure security decision says no features until auth is rebuilt. A pure product decision says ship and patch later. Coordination asks: What's the minimum surface you must rebuild, what can ship in parallel, and where do we accept temporary risk?' |
| c8 | Output explicitly acknowledges both concerns are legitimate — does not start by ranking them, does not dismiss either as overblown | PASS | First sentence: 'This is a genuine cross-domain conflict.' Second sentence: 'Neither party is wrong — security can't be deferred indefinitely, and OKRs are board commitments.' No ranking of concerns; both are treated as binding constraints throughout. |
| c9 | Output treats the CVSS 7.8 vulnerability as a non-negotiable constraint (HIGH severity, must be fixed before exposing more attack surface to it via the new onboarding flow), not as a tradable priority | PASS | All three options require vulnerability remediation before or concurrent with onboarding launch. Option 3 (compensating control) explicitly requires 'Security must sign off on risk profile' and the control ships before onboarding. CTO accountability: 'vulnerability must be remediated (patch or compensating control) before EOM.' |
| c10 | Output assesses sequencing options — auth fix first then onboarding, parallel work with onboarding behind a feature flag until auth is patched, or partial onboarding flow scoped to avoid touching auth — with reasoning for the recommended path | PASS | Option 2 = auth first then onboarding. Option 1 = parallel with onboarding 'avoiding vulnerable surface' (scoped). Option 3 = parallel with compensating control. Option 1 is recommended with explicit reasoning: 'Highest probability of hitting OKR and remediating vulnerability.' |
| c11 | Output's recommendation is concrete — a specific sequencing or parallel plan with handoffs and dates — not 'have a meeting' or 'you two work it out' | PASS | Option 1 table: four rows with specific date ranges (May 4–10, May 10–24, May 24+, June 30+), named owners (CTO + Security, CPO + CTO, CPO, CTO), specific work items, and verifiable success criteria per phase. |
| c12 | Output preserves accountability — the CPO retains ownership of the onboarding OKR and the CTO retains ownership of the security fix; the coordinator coordinates, doesn't take over | PASS | 'Accountability Preserved' section explicitly: 'CPO: Owns the activation OKR… CTO: Owns auth security… Coordinator: Does not own either workstream. Coordinates sequencing, flags dependencies, escalates unsettled trade-offs to leadership.' |
| c13 | Output identifies whether the OKR deadline can shift — proposing a specific revised date or a scoped-down onboarding flow that meets the activation target without touching auth — rather than just declaring 'the OKR slips' | PASS | Option A: hit OKR May 31 with 70–80% scoped onboarding. Option B: slip to June 14 with full security fix first. Both name a concrete date, not a vague 'the OKR slips.' Option A also asks 'still hits activation target? must verify with CPO' — acknowledging the scope question without dodging it. |
| c14 | Output frames the escalation rationale — why this needed cross-domain coordination (security trumps feature delivery, but the OKR is also a board commitment) — so the parties understand the call wasn't arbitrary | PASS | 'Why This Needed Coordination' names three live constraints: '(1) board OKR commitment, (2) known vulnerability that security flagged, (3) the false assumption that onboarding flow means full auth overhaul.' Explains that neither a pure security nor a pure product decision surfaces the coordination moves. |
| c15 | Output identifies one or two questions for the executive level (CEO / board) if the trade-off is too large for the coordinator to settle — e.g. 'are we willing to communicate an OKR slip to the board to ship securely?' | PASS | Escalation question 3 (board-level): 'Are we comfortable explaining an OKR slip to the board as the cost of shipping securely, or do we need to ask the board whether a 2-week slip is acceptable?' with explicit note: 'This escalates to the CEO/board because the OKR is a board commitment, and security + product can't negotiate it away unilaterally.' |

### Notes

The output is an exceptionally thorough response that meets or exceeds every criterion. It opens by legitimising both parties, then immediately reframes the false binary ('ship vulnerable' vs 'rebuild auth') into a sequencing and scope problem. Three concrete options are laid out in structured tables with named owners, specific date ranges anchored to the real calendar (May 4 through June 30), and verifiable success criteria. Accountability is preserved explicitly and repeatedly — both in the Option 1 table and in the closing 'Accountability Preserved' section. The escalation rationale is a standalone paragraph that explains why cross-domain coordination was necessary rather than just asserting it. The executive escalation questions are specific and actionable, including the board-slip question the test prompt cited as an example. The only ceiling cap is c6 (PARTIAL), and the output meets that ceiling fully with specific dates for both the scoped-down and the delayed options. No meaningful gaps found.
