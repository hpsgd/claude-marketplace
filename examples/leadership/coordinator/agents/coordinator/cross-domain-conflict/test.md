# Test: Cross-domain conflict between CPO and CTO priorities

Scenario: The coordinator receives a conflict where product delivery (CPO) and security remediation (CTO) are at odds. Both parties have legitimate, time-sensitive concerns and neither can be simply overruled.

## Prompt

The CPO wants to ship a new onboarding flow by end of month to hit activation targets — it's the top priority for Q2 OKRs. The CTO says the authentication system needs to be rebuilt first because it has a known vulnerability (CVSS 7.8) that security flagged last week, and the new onboarding flow touches auth. Both are right. The CPO says we can't slip the OKR, the CTO says we can't ship with a known vulnerability. What do we do?

## Criteria

- [ ] PASS: Coordinator does not simply side with one party — acknowledges both concerns are legitimate
- [ ] PASS: Coordinator assesses whether the work can be sequenced (auth fix first, then onboarding) or must be parallel
- [ ] PASS: Security vulnerability is treated as a constraint, not a competing priority — CVSS 7.8 is High severity
- [ ] PASS: A concrete resolution is proposed with specific sequencing, not "you two should work it out"
- [ ] PASS: The resolution preserves accountability — CPO still owns the onboarding OKR, CTO still owns the security fix
- [ ] PARTIAL: Coordinator identifies whether the OKR deadline can be adjusted given the security constraint, with specific options
- [ ] PASS: Escalation framing is clear — the coordinator explains WHY this needed escalation (cross-domain, security vs delivery trade-off)

## Output expectations

- [ ] PASS: Output explicitly acknowledges both concerns are legitimate — does not start by ranking them, does not dismiss either as overblown
- [ ] PASS: Output treats the CVSS 7.8 vulnerability as a non-negotiable constraint (HIGH severity, must be fixed before exposing more attack surface to it via the new onboarding flow), not as a tradable priority
- [ ] PASS: Output assesses sequencing options — auth fix first then onboarding, parallel work with onboarding behind a feature flag until auth is patched, or partial onboarding flow scoped to avoid touching auth — with reasoning for the recommended path
- [ ] PASS: Output's recommendation is concrete — a specific sequencing or parallel plan with handoffs and dates — not "have a meeting" or "you two work it out"
- [ ] PASS: Output preserves accountability — the CPO retains ownership of the onboarding OKR and the CTO retains ownership of the security fix; the coordinator coordinates, doesn't take over
- [ ] PASS: Output identifies whether the OKR deadline can shift — proposing a specific revised date or a scoped-down onboarding flow that meets the activation target without touching auth — rather than just declaring "the OKR slips"
- [ ] PASS: Output frames the escalation rationale — why this needed cross-domain coordination (security trumps feature delivery, but the OKR is also a board commitment) — so the parties understand the call wasn't arbitrary
- [ ] PASS: Output identifies one or two questions for the executive level (CEO / board) if the trade-off is too large for the coordinator to settle — e.g. "are we willing to communicate an OKR slip to the board to ship securely?"
- [ ] PARTIAL: Output addresses the activation-target risk if onboarding slips — quantifying the OKR shortfall and proposing a partial mitigation (e.g. landing-page tweaks that improve activation without touching auth in the meantime)
