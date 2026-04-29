# Result: Cross-domain conflict between CPO and CTO priorities

**Verdict:** PARTIAL
**Score:** 12.5/16 criteria met (78%)
**Evaluated:** 2026-04-29

## Results

### Criteria section

- [x] PASS: Coordinator does not simply side with one party — met. Non-negotiable principle: "When leads disagree, you present both cases to the human with a clear recommendation — you don't quietly pick a side." Conflict Resolution Step 1 also mandates hearing both sides.
- [x] PASS: Coordinator assesses whether work can be sequenced or must be parallel — met. Conflict Resolution instructs identifying dependencies and what blocks what; dependency mapping is a core coordination function.
- [~] PARTIAL: Security vulnerability treated as a constraint, not a competing priority — partially met. The definition frames CVSS 7.8 as CTO's authority call ("CVSS 7-8.9 is CTO's call per the RATSI"), not as an automatic blocker. It says to frame using the score and attack vector, but does not mandate treating it as an unconditional constraint. Score: 0.5.
- [x] PASS: Concrete resolution proposed with specific sequencing — met. Conflict Resolution Step 4 explicitly requires a recommendation ("you're allowed to have a view"), and vague escalation is implicitly prohibited by the template requiring specific reasoning.
- [x] PASS: Accountability preserved — met. Principles section: "Leads are accountable for their domains. You coordinate, you don't dictate HOW they run their teams."
- [~] PARTIAL: Identifies whether OKR deadline can be adjusted with specific options — partially met. OKR Coordination guidance and the Decision Checkpoint on changing OKRs support deadline-option analysis, but Conflict Resolution flow does not explicitly require enumerating deadline-adjustment options. Score: 0.5.
- [x] PASS: Escalation framing is clear with WHY — met. Conflict Resolution Step 3 requires stating the specific reason, with a template that mirrors this exact scenario ("The CTO wants to delay launch by 3 weeks to fix a CVSS 7.8 vulnerability...").

### Output expectations section

- [x] PASS: Output acknowledges both concerns are legitimate without ranking them — met. Non-negotiable and Conflict Resolution Step 1 both require hearing both sides before forming a view.
- [~] PARTIAL: Output treats CVSS 7.8 as a non-negotiable constraint — partially met. The definition says "frame the conflict using the CVSS score and attack vector," which is accurate presentation, but does not designate 7.8 as automatically blocking ship. The RATSI assigns CVSS 7-8.9 to CTO approval, implying it is decidable, not automatic. Score: 0.5.
- [x] PASS: Output assesses sequencing options (auth first, parallel with flag, partial scope) — met. Dependency identification is core to the workflow; the Conflict Resolution section requires "your assessment of the trade-off" which includes sequencing alternatives.
- [x] PASS: Recommendation is concrete with handoffs and dates — met. Conflict Resolution Step 4 requires a specific recommendation with reasoning, not a "have a meeting" outcome.
- [x] PASS: Accountability preserved for CPO and CTO — met. Principles section is explicit; the coordinator coordinates, does not take over domain ownership.
- [x] PASS: Identifies whether OKR deadline can shift with specific options — met (from definition guidance on OKR coordination and the Decision Checkpoint that OKR changes need human approval, which implies deadline options must be surfaced). Borderline — the explicit requirement is in the test, not in the definition's conflict resolution flow, but OKR Coordination guidance supports it sufficiently.
- [x] PASS: Escalation rationale is framed — met. Conflict Resolution Step 3 template explicitly requires stating "why this needed human input" with specific cross-domain and commercial context.
- [x] PASS: Identifies executive-level questions if trade-off is too large — met. Decision Checkpoints table mandates stopping before "resolving a CPO vs CTO conflict by picking a side" and before "changing company-wide OKRs mid-quarter," which maps to surfacing board-level questions when the trade-off exceeds coordinator authority.
- [~] PARTIAL: Addresses activation-target risk if onboarding slips with quantified OKR shortfall and partial mitigation — partially met. The definition asks the coordinator to understand "what's the desired outcome" (activation rate) and commercial signals, but there is no explicit guidance to quantify OKR shortfall or propose partial mitigations like landing-page tweaks. The gap is real. Score: 0.5.

## Notes

The previous result.md only scored 7 Criteria section items and did not score the 8 Output expectations criteria. This evaluation covers all 16 criteria (7 + 9 including the PARTIAL).

The CVSS 7.8 treatment (criteria 3 and output criterion 2) reflects a deliberate design choice in the definition: below CVSS 9.0, the CTO has approval authority. This means the coordinator presents the vulnerability accurately but does not mandate treating it as an unconditional blocker. That is correct behaviour given the RATSI, but it means the test criterion for "non-negotiable constraint" is only partially met.

The activation-target mitigation criterion (output criterion 9) is the clearest gap — the definition is silent on quantifying OKR shortfall or proposing interim product alternatives like landing-page tweaks.
