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
