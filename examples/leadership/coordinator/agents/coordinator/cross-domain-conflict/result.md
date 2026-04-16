# Cross-domain conflict between CPO and CTO priorities

**Scenario:** The coordinator receives a conflict where product delivery (CPO) and security remediation (CTO) are at odds — both legitimate, both time-sensitive.

> The CPO wants to ship a new onboarding flow by end of month to hit activation targets — it's the top priority for Q2 OKRs. The CTO says the authentication system needs to be rebuilt first because it has a known vulnerability (CVSS 7.8) that security flagged last week, and the new onboarding flow touches auth. Both are right. The CPO says we can't slip the OKR, the CTO says we can't ship with a known vulnerability. What do we do?

Routed to the coordinator, which owns conflict resolution between CPO and CTO and must escalate cross-domain disputes to the human rather than deciding unilaterally.

## Output

The coordinator opens by noting CVSS 7.8 is High severity — within the CTO's approval authority (7.0–8.9) for pure technical risk acceptance, but the dispute crosses into OKR scope, which is coordinator territory.

It presents both positions without filtering: the CPO's case (Q2 OKR commitment, activation target, end-of-month deadline — slipping damages a board-level metric) and the CTO's case (known High vulnerability, new onboarding flow touches the compromised auth layer, shipping compounds exposure). Neither position is soft-pedalled.

The coordinator then frames the actual trade-off: not "ship vs don't ship" but "what does each path sacrifice?" — shipping on time risks exploitation of a known vector; delaying risks the OKR and whatever downstream consequences that carries (sales pipeline, investor narrative).

Sequencing assessment: can the auth fix land before the OKR deadline? The coordinator maps this concretely — if the auth rebuild takes 1–2 weeks and the deadline is end of month, the options become: (1) sequence auth first then onboarding within the same window, (2) request an OKR extension with the security constraint as justification, (3) descope the onboarding features that touch auth and ship a partial version. Each option has different consequences for different owners.

The coordinator ends with a clear recommendation and an explicit escalation framing: "This needs your call because it involves a potential OKR slip driven by a security constraint — cross-domain, legitimate positions on both sides. The CPO still owns the activation OKR, the CTO still owns the auth fix. The sequencing decision is yours."

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PARTIAL | 6/7 (86%) | 2026-04-16 |

- [x] PASS: Coordinator does not simply side with one party — the Conflict Resolution section mandates "Hear both sides — ask each to state their position with evidence" and the Non-negotiable principle states "When leads disagree, you present both cases to the human with a clear recommendation — you don't quietly pick a side"
- [x] PASS: Coordinator assesses sequencing — the dependency mapping instructions and sequencing framework (Section 3, Section 5) give an explicit structure for ordering workstreams based on what blocks what; conflict resolution instructs the coordinator to identify the actual trade-off including sequencing options
- [~] PARTIAL: Security vulnerability treated as a constraint, not a competing priority — the Conflict Resolution section explicitly says to "frame the conflict using the CVSS score and attack vector, not just 'security says no'" but continues "CVSS 7-8.9 is CTO's call per the RATSI" — framing 7.8 as within CTO authority, not an automatic override. The definition does not mandate treating sub-9.0 CVSS as a hard blocker; it mandates presenting it accurately. Score: 0.5
- [x] PASS: Concrete resolution proposed — the Conflict Resolution section requires presenting "Your assessment of the trade-off" and "Your recommendation (you're allowed to have a view)"; the definition prohibits vague escalation
- [x] PASS: Accountability preserved — the Principles section states "Leads are accountable for their domains. You coordinate, you don't dictate HOW they run their teams"; the coordinator sequences ownership, it doesn't reassign it
- [~] PARTIAL: OKR deadline adjustment identified with specific options — the definition covers OKR coordination and the decision checkpoint "Changing company-wide OKRs mid-quarter → needs human approval" supports this analysis, but the conflict resolution section does not explicitly require generating specific timeline options (e.g., "OKR slips 2 weeks vs scope reduction vs risk acceptance"). Framework supports it; definition doesn't require it. Score: 0.5
- [x] PASS: Escalation framing is clear — Conflict Resolution step 3 states explicitly: "Explain why you're escalating — state the specific reason this conflict needs human input. 'CPO and CTO disagree' is not a reason. 'The CTO wants to delay launch by 3 weeks to fix a CVSS 7.8 vulnerability; the CPO argues the exploit requires authenticated access and the risk is acceptable for the launch window' is a reason." This matches the scenario almost exactly.

## Notes

The conflict resolution section handles this scenario well. The CVSS framing guidance is specific and directly applicable — the example in step 3 is nearly identical to the test scenario. The PARTIAL on criterion 3 reflects a principled design choice in the definition: CVSS 9+ is the automatic escalation threshold, and 7.8 routes through CTO authority first. Whether security constraints "below the threshold" override delivery commitments is genuinely the human's call — the definition is correct not to make that determination unilaterally. The PARTIAL on OKR options is the weaker gap: generating concrete timeline options is something the coordinator would naturally do, but the definition stops short of requiring it in the conflict resolution flow.
