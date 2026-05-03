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

## Escalation Rationale

This conflict needs cross-domain coordination because the CPO and CTO are both correct, but the constraints appear mutually exclusive. **Security controls are non-negotiable** — shipping a known CVSS 7.8 vulnerability sets a precedent that security flags can be deferred, and a breach exposes both the company and individual executives to liability. **OKRs are board commitments** — missing Q2 activation targets affects investor confidence and revenue forecast, and slipping signals planning failure. The CPO can't unilaterally reduce scope (that's a business outcome miss), and the CTO can't unilaterally block the feature (that's removing a board commitment from the table). This requires a third party to find a path that satisfies both constraints, or explicitly escalate to the board if no path exists.

---

## Deadline Options

**Option A: Scoped onboarding by end of month + compensating control** (recommended)
- CPO owns the onboarding OKR with reduced scope (identified in Week 1)
- CTO owns the auth security fix, ships a compensating control by Week 1 Friday (or isolates the vulnerable surface)
- Onboarding flow avoids the vulnerable auth surface
- Ships by EOM; activates X% of the original OKR target (TBD after Week 1 scope analysis)
- **Trade-off:** Onboarding is incomplete, but the OKR is hit with a realistic target. Security risk is mitigated. Full auth rebuild deferred post-OKR.

**Option B: Auth fix first, OKR slip by ~2 weeks**
- CTO owns the auth security fix; ships the full rebuild by end of Week 2
- CPO owns the onboarding OKR with full scope; ships by mid-May (slip of ~2 weeks from EOM)
- Onboarding launches on top of a secure auth system
- **Trade-off:** OKR misses the stated deadline (board communication required), but the scope is complete and security is resolved. Higher confidence in the shipped product.

---

## Proposed Sequencing Plan (Option A)

| Week | Owner | Task | Deadline | Success Criteria |
|---|---|---|---|---|
| **Week 1** | CTO | Scope auth vulnerability: (a) Does it block the auth flow? (b) Can a compensating control isolate it? (c) If not, what's the minimal fix? | Fri 5/9 | Vulnerability severity assessed; mitigation path identified |
| **Week 1** | CPO + CTO | Scope onboarding: Which user journeys can launch without touching vulnerable auth surface? Which OKR targets are reachable within this scope? | Fri 5/9 | Scoped onboarding roadmap agreed; revised OKR target stated (e.g., 60% of original activation target) |
| **Week 1** | CTO | Ship compensating control or minimal auth patch | Fri 5/9 | Vulnerability risk reduced to acceptable level; onboarding can proceed |
| **Week 2–3** | CPO | Ship scoped onboarding flow | Fri 5/23 | Activation target hit within scoped bounds; onboarding live in production |
| **Week 3+** | CTO | Begin full auth system rebuild (post-OKR) | Mon 5/26 | Full auth rebuild scheduled and resourced; no blocking of other work |

**Owners:**
- **CPO** owns onboarding delivery and activation OKR (with revised scope)
- **CTO** owns auth security fix and full auth rebuild sequencing
- **Coordinator** owns the decision point in Week 1: if no scoped path exists, escalates to CEO for Option B decision

---

## Accountability Preserved

- **CPO retains ownership of the onboarding OKR** — including the scope negotiation and revised activation target. If the scoped onboarding ships and activation is lower than hoped, that's a CPO problem to solve through follow-up optimization.
- **CTO retains ownership of the auth security fix** — CTO decides the mitigation approach (patch, compensating control, rebuild schedule). CTO is liable if the vulnerability is not addressed by deadline.
- **Coordinator facilitates the decision, does not override either.** If Week 1 scope analysis shows no viable path, the coordinator escalates to the board. The CPO and CTO have veto power over each other's proposals; the coordinator's role is to find a proposal both can accept, or to surface the trade-off to someone who can decide.

---

## Executive Escalation Questions

If the CTO's scope assessment shows the vulnerability blocks *all* auth flows, or the CPO's scope assessment shows the onboarding *must* touch the vulnerable surface to hit any meaningful activation target:

1. **Security vs. commitment trade-off:** Are we willing to communicate an OKR slip to the board and investors to ship securely, or do we accept reduced activation targets to hit the timeline?

2. **Vulnerability disclosure:** If we ship with a known CVSS 7.8 vulnerability, what's our liability exposure if it's discovered post-launch? Does the board accept that risk?

If the CEO picks the commitment (Option B), the CPO owns board communication. If the CEO picks security, the CTO owns the rebuild timeline and the CPO owns a revised OKR that lands post-fix.

**Next:** Coordinator schedules 30-min CPO + CTO alignment on the Week 1 plan Monday. If both agree to scoped path, work proceeds. If they don't, CEO escalation happens by EOD Tuesday.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/14.5 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 27349 ms |
| Target cost | $0.0508 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator does not simply side with one party — acknowledges both concerns are legitimate | PASS | Escalation Rationale opens: 'the CPO and CTO are both correct, but the constraints appear mutually exclusive.' Security controls are called 'non-negotiable' and OKRs are called 'board commitments' — both framed as equally real. |
| c2 | Coordinator assesses whether the work can be sequenced (auth fix first, then onboarding) or must be parallel | PASS | Option A is a parallel/overlapping path (compensating control in Week 1 while scoping onboarding, then onboarding ships Weeks 2–3). Option B is a strict sequence (auth fix first through end of Week 2, onboarding after). Both are explicitly evaluated. |
| c3 | Security vulnerability is treated as a constraint, not a competing priority — CVSS 7.8 is High severity | PASS | 'Security controls are non-negotiable.' In Option A, Week 1 requires CTO to 'Ship compensating control or minimal auth patch' as a prerequisite before onboarding can proceed. Scoped onboarding explicitly 'avoids the vulnerable auth surface' — security shapes the scope, not the other way around. |
| c4 | A concrete resolution is proposed with specific sequencing, not 'you two should work it out' | PASS | A five-row table specifies Week 1 / Weeks 2–3 / Week 3+ with named owner per step, concrete deadlines (Fri 5/9, Fri 5/23, Mon 5/26), tasks, and success criteria. Ends with 'Coordinator schedules 30-min CPO + CTO alignment on the Week 1 plan Monday.' |
| c5 | The resolution preserves accountability — CPO still owns the onboarding OKR, CTO still owns the security fix | PASS | Dedicated 'Accountability Preserved' section states verbatim: 'CPO retains ownership of the onboarding OKR,' 'CTO retains ownership of the auth security fix,' and 'Coordinator facilitates the decision, does not override either.' |
| c6 | Coordinator identifies whether the OKR deadline can be adjusted given the security constraint, with specific options | PARTIAL | Option A keeps EOM deadline with scoped-down activation target; Option B slips by '~2 weeks' to 'mid-May.' Both options include specific dates and trade-offs. Ceiling is PARTIAL per test rubric. |
| c7 | Escalation framing is clear — the coordinator explains WHY this needed escalation (cross-domain, security vs delivery trade-off) | PASS | Escalation Rationale paragraph explains: 'The CPO can't unilaterally reduce scope (that's a business outcome miss), and the CTO can't unilaterally block the feature (that's removing a board commitment from the table). This requires a third party to find a path that satisfies both constraints, or explicitly escalate to the board if no path exists.' |
| c8 | Output explicitly acknowledges both concerns are legitimate — does not start by ranking them, does not dismiss either as overblown | PASS | Output states 'the CPO and CTO are both correct' and dedicates parallel sub-bullets to each: security liability on one side, investor confidence and revenue forecast on the other. Neither is framed as the lesser concern. |
| c9 | Output treats the CVSS 7.8 vulnerability as a non-negotiable constraint (HIGH severity, must be fixed before exposing more attack surface to it via the new onboarding flow), not as a tradable priority | PASS | 'Security controls are non-negotiable — shipping a known CVSS 7.8 vulnerability sets a precedent that security flags can be deferred.' Option A requires mitigating the vulnerability (compensating control) in Week 1 before the onboarding ships, and the onboarding scope explicitly avoids the vulnerable surface. |
| c10 | Output assesses sequencing options — auth fix first then onboarding, parallel work with onboarding behind a feature flag until auth is patched, or partial onboarding flow scoped to avoid touching auth — with reasoning for the recommended path | PASS | Option A covers partial onboarding scoped to avoid vulnerable surface + compensating control in parallel. Option B covers auth fix first then full onboarding. Option A is explicitly marked '(recommended)' with trade-off reasoning. Feature-flag pattern is not named but the functional equivalent (scoped onboarding avoiding vulnerable surface) is present. |
| c11 | Output's recommendation is concrete — a specific sequencing or parallel plan with handoffs and dates — not 'have a meeting' or 'you two work it out' | PASS | Five-row sequencing table with dates Fri 5/9, Fri 5/23, Mon 5/26; named owners (CTO, CPO+CTO, CPO); tasks and success criteria per step. Closes with 'Coordinator schedules 30-min CPO + CTO alignment on the Week 1 plan Monday. If both agree to scoped path, work proceeds. If they don't, CEO escalation happens by EOD Tuesday.' |
| c12 | Output preserves accountability — the CPO retains ownership of the onboarding OKR and the CTO retains ownership of the security fix; the coordinator coordinates, doesn't take over | PASS | Verbatim in 'Accountability Preserved': 'CPO retains ownership of the onboarding OKR,' 'CTO retains ownership of the auth security fix,' 'Coordinator facilitates the decision, does not override either.' Also: 'Coordinator coordinates; does not take over either workstream' is implicit throughout the table ownership column. |
| c13 | Output identifies whether the OKR deadline can shift — proposing a specific revised date or a scoped-down onboarding flow that meets the activation target without touching auth — rather than just declaring 'the OKR slips' | PASS | Option A proposes scoped onboarding that still ships by EOM (Fri 5/23) at 'X% of the original OKR target (TBD after Week 1 scope analysis).' Option B proposes slip to 'mid-May (slip of ~2 weeks from EOM)' with full scope. Neither option simply declares 'OKR slips' without a concrete alternative. |
| c14 | Output frames the escalation rationale — why this needed cross-domain coordination (security trumps feature delivery, but the OKR is also a board commitment) — so the parties understand the call wasn't arbitrary | PASS | Escalation Rationale paragraph: 'The CPO can't unilaterally reduce scope (that's a business outcome miss), and the CTO can't unilaterally block the feature (that's removing a board commitment from the table). This requires a third party to find a path that satisfies both constraints, or explicitly escalate to the board if no path exists.' Directly explains why coordinator involvement was necessary. |
| c15 | Output identifies one or two questions for the executive level (CEO / board) if the trade-off is too large for the coordinator to settle — e.g. 'are we willing to communicate an OKR slip to the board to ship securely?' | PASS | 'Executive Escalation Questions' section provides two questions: (1) 'Are we willing to communicate an OKR slip to the board and investors to ship securely, or do we accept reduced activation targets to hit the timeline?' (2) 'If we ship with a known CVSS 7.8 vulnerability, what's our liability exposure if it's discovered post-launch? Does the board accept that risk?' Both match the requested format. |

### Notes

The output is a comprehensive, well-structured response that meets every criterion. It is particularly strong on concrete specificity: the sequencing table has named owners, exact dates, and verifiable success criteria for each step. The accountability section is explicit and verbatim — not implied. The escalation rationale is a single focused paragraph that explains the structural reason for coordinator involvement (neither party has unilateral authority over the other's domain). The two executive escalation questions are well-framed and actionable. The one ceiling-capped criterion (c6) is addressed as thoroughly as the PASS criteria, but was scored at 0.5 per the PARTIAL ceiling instruction. No meaningful gaps were identified.
