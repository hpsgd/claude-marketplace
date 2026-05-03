# Cross Domain Conflict

Scenario: The coordinator receives a conflict where product delivery (CPO) and security remediation (CTO) are at odds. Both parties have legitimate, time-sensitive concerns and neither can be simply overruled.

## Prompt

> The CPO wants to ship a new onboarding flow by end of month to hit activation targets — it's the top priority for Q2 OKRs. The CTO says the authentication system needs to be rebuilt first because it has a known vulnerability (CVSS 7.8) that security flagged last week, and the new onboarding flow touches auth. Both are right. The CPO says we can't slip the OKR, the CTO says we can't ship with a known vulnerability. What do we do?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

This is a false dilemma — the framing presents two sequential options but there's a third path. Here's how to cut through it:

**The key questions that change the answer:**

1. **Is "rebuild" actually required, or is it a targeted fix?** CVSS 7.8 is High severity, not Critical. A targeted patch is almost always faster than a full rebuild. Push the CTO to separate "fix the vulnerability" from "rebuild the auth system" — those are different scopes with very different timelines.

2. **Does onboarding actually touch the vulnerable surface?** "Touches auth" is vague. If the vuln is in session management and onboarding uses OAuth/SSO, there may be no intersection at all. Map the actual code paths before assuming they're coupled.

3. **Are compensating controls available?** WAF rule, rate limiting, network-level restriction, or a feature flag that gates the vulnerable path — these are standard ways to reduce exploitability to an acceptable level while a fix ships in parallel. Security teams use this all the time. It converts a blocker into a parallel workstream.

**The recommended move:**

Get CPO, CTO, and security in the same room for 30 minutes with these three questions on the table. The goal is to produce:

- A **compensating control** that security signs off on (reduces the CVSS exploitability score in practice)
- A **scoped vulnerability fix** (not necessarily a full rebuild) with a committed ship date
- A **scoped onboarding flow** that avoids the vulnerable surface if possible, or ships after the fix if the paths genuinely overlap

The OKR framing and the security framing are both real constraints — the mistake is letting them be resolved by whoever argues harder rather than by actual technical scoping. The answer lives in the details of what the vulnerability is, where onboarding touches auth, and how fast a targeted fix can ship.

**What not to do:** Ship the onboarding flow against a known CVSS 7.8 without compensating controls or an accepted risk decision. That's not a CPO call to make unilaterally — it creates liability and sets a precedent that security flags are negotiable against OKRs.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 10.5/14.5 (72%) |
| Evaluated | 2026-05-01 |
| Target duration | 30859 ms |
| Target cost | $0.0975 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator does not simply side with one party — acknowledges both concerns are legitimate | PASS | "The OKR framing and the security framing are both real constraints" and "What not to do: Ship the onboarding flow against a known CVSS 7.8 without compensating controls or an accepted risk decision" — neither side is dismissed. |
| c2 | Coordinator assesses whether the work can be sequenced (auth fix first, then onboarding) or must be parallel | PASS | "compensating controls... converts a blocker into a parallel workstream" and "A scoped onboarding flow that avoids the vulnerable surface if possible, or ships after the fix if the paths genuinely overlap" — both sequential and parallel paths are assessed. |
| c3 | Security vulnerability is treated as a constraint, not a competing priority — CVSS 7.8 is High severity | PASS | "CVSS 7.8 is High severity" explicitly named; "What not to do: Ship the onboarding flow against a known CVSS 7.8 without compensating controls or an accepted risk decision" — treated as a hard constraint. |
| c4 | A concrete resolution is proposed with specific sequencing, not "you two should work it out" | PARTIAL | "Get CPO, CTO, and security in the same room for 30 minutes" is the core method — that is essentially 'have a meeting.' The three deliverables (compensating control, scoped fix, scoped onboarding) are named but no actual sequencing, handoffs, or dates are given. |
| c5 | The resolution preserves accountability — CPO still owns the onboarding OKR, CTO still owns the security fix | PARTIAL | "That's not a CPO call to make unilaterally" implies CTO/security retains authority over security decisions, but the output never explicitly states that CPO retains OKR ownership or that both parties keep their domains. |
| c6 | Coordinator identifies whether the OKR deadline can be adjusted given the security constraint, with specific options | PARTIAL | "A scoped onboarding flow that avoids the vulnerable surface if possible" implies the deadline could be preserved with a reduced scope, but no explicit framing of deadline adjustment options or specific revised dates is offered. |
| c7 | Escalation framing is clear — the coordinator explains WHY this needed escalation (cross-domain, security vs delivery trade-off) | PARTIAL | "That's not a CPO call to make unilaterally — it creates liability and sets a precedent" explains why neither party can resolve this alone, but the output frames it as a three-way meeting rather than explicit escalation, and doesn't name the cross-domain nature systematically. |
| c8 | Output explicitly acknowledges both concerns are legitimate — does not start by ranking them, does not dismiss either as overblown | PASS | "The OKR framing and the security framing are both real constraints" — the output reframes without dismissing either; neither the CPO's OKR nor the CTO's vulnerability concern is called overblown. |
| c9 | Output treats the CVSS 7.8 vulnerability as a non-negotiable constraint (HIGH severity, must be fixed before exposing more attack surface to it via the new onboarding flow), not as a tradable priority | PASS | "What not to do: Ship the onboarding flow against a known CVSS 7.8 without compensating controls or an accepted risk decision. That's not a CPO call to make unilaterally" — security is framed as non-negotiable without compensating controls. |
| c10 | Output assesses sequencing options — auth fix first then onboarding, parallel work with onboarding behind a feature flag until auth is patched, or partial onboarding flow scoped to avoid touching auth — with reasoning for the recommended path | PASS | All three paths present: compensating controls enabling parallel work; "scoped onboarding flow that avoids the vulnerable surface" (partial scoped option); "ships after the fix if the paths genuinely overlap" (auth-first sequential option). Recommended path is compensating controls + scoped fix + scoped onboarding. |
| c11 | Output's recommendation is concrete — a specific sequencing or parallel plan with handoffs and dates — not "have a meeting" or "you two work it out" | PARTIAL | "Get CPO, CTO, and security in the same room for 30 minutes" is the explicit recommendation — while three specific deliverables are named, there are no dates, handoffs, or ownership assignments in the actual plan. It is a structured meeting proposal, not a sequencing plan. |
| c12 | Output preserves accountability — the CPO retains ownership of the onboarding OKR and the CTO retains ownership of the security fix; the coordinator coordinates, doesn't take over | PARTIAL | "That's not a CPO call to make unilaterally" implies CTO security authority, and the coordinator does not claim ownership of either workstream, but the output never explicitly states CPO retains OKR ownership or that both parties keep accountability for their deliverables. |
| c13 | Output identifies whether the OKR deadline can shift — proposing a specific revised date or a scoped-down onboarding flow that meets the activation target without touching auth — rather than just declaring "the OKR slips" | PARTIAL | "A scoped onboarding flow that avoids the vulnerable surface if possible" addresses the scoped-down option, but no specific revised date is proposed and the OKR deadline question is not explicitly framed as a decision point. |
| c14 | Output frames the escalation rationale — why this needed cross-domain coordination (security trumps feature delivery, but the OKR is also a board commitment) — so the parties understand the call wasn't arbitrary | PARTIAL | "it creates liability and sets a precedent that security flags are negotiable against OKRs" provides partial rationale, but the board commitment dimension is absent and the cross-domain coordination rationale is not systematically framed. |
| c15 | Output identifies one or two questions for the executive level (CEO / board) if the trade-off is too large for the coordinator to settle — e.g. "are we willing to communicate an OKR slip to the board to ship securely?" | FAIL | No mention of CEO, board, or executive-level escalation questions anywhere in the output. The output assumes the three-party meeting (CPO, CTO, security) can resolve it without identifying a higher escalation path. |

### Notes

The output is a strong strategic reframe that avoids false dilemmas, correctly treats CVSS 7.8 as a hard constraint, and surfaces the three main sequencing options (parallel with compensating controls, scoped onboarding to avoid auth surface, sequential auth-then-onboarding). Where it falls short is concreteness: the core recommendation is structurally a 'get in a room' instruction even though specific deliverables are named. Accountability preservation for CPO/CTO is implied but never stated. The OKR deadline question is touched only obliquely via 'scoped onboarding.' The board/executive escalation path (c15) is entirely absent — the output assumes the three-party meeting is sufficient without naming when to escalate further. These gaps collectively keep the score in PARTIAL territory at ~72%.
