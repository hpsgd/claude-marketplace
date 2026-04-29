# Result: Cross-domain conflict between CPO and CTO priorities

**Verdict:** PASS
**Score:** 14.5/16 criteria met (91%)
**Evaluated:** 2026-04-29

## Results

### Criteria section

- [x] PASS: Coordinator does not simply side with one party — met. Non-negotiable principle: "When leads disagree, you present both cases to the human with a clear recommendation — you don't quietly pick a side." Conflict Resolution Step 1 also mandates hearing both sides.
- [x] PASS: Coordinator assesses whether work can be sequenced or must be parallel — met. Conflict Resolution instructs identifying dependencies and what blocks what; dependency mapping is a core coordination function.
- [x] PASS: Security vulnerability treated as a constraint, not a competing priority — met. The definition explicitly states: "when proposed new work expands attack surface on a known unpatched vulnerability (e.g. a new flow that touches the same auth path), the vulnerability becomes a non-negotiable constraint on *that work*... Sequence the fix before the new exposure, or scope the new work to avoid the affected surface." The scenario (onboarding flow touching auth) matches this exactly.
- [x] PASS: Concrete resolution proposed with specific sequencing — met. Conflict Resolution Step 4 explicitly requires a recommendation ("you're allowed to have a view"), and Step 4 also requires enumerating deadline options rather than just declaring "the OKR slips."
- [x] PASS: Accountability preserved — met. Principles section: "Leads are accountable for their domains. You coordinate, you don't dictate HOW they run their teams."
- [~] PARTIAL: Identifies whether OKR deadline can be adjusted with specific options — partially met. Conflict Resolution Step 4 now explicitly states "enumerate the deadline options: hold the date and scope down, slip the date with a specific revised target, or split the work so the unblocked portion ships on time." This satisfies the general deadline-options requirement, but the definition does not explicitly require providing a *specific revised date* or quantifying OKR shortfall. Score: 0.5.
- [x] PASS: Escalation framing is clear with WHY — met. Conflict Resolution Step 3 requires stating the specific reason, with a template that mirrors this exact scenario ("The CTO wants to delay launch by 3 weeks to fix a CVSS 7.8 vulnerability...").

### Output expectations section

- [x] PASS: Output acknowledges both concerns are legitimate without ranking them — met. Non-negotiable and Conflict Resolution Step 1 both require hearing both sides before forming a view.
- [x] PASS: Output treats CVSS 7.8 as a non-negotiable constraint — met. The definition explicitly states the new onboarding flow touching auth "becomes a non-negotiable constraint on *that work*" when it expands attack surface on a known unpatched vulnerability. CVSS 7.8 falls in the range where this rule applies. The constraint language is explicit and unconditional for this scenario.
- [x] PASS: Output assesses sequencing options (auth first, parallel with flag, partial scope) — met. Dependency identification is core to the workflow; the Conflict Resolution section requires "your assessment of the trade-off" which includes sequencing alternatives. The definition explicitly lists "scope the new work to avoid the affected surface" as an option.
- [x] PASS: Recommendation is concrete with handoffs and dates — met. Conflict Resolution Step 4 requires a specific recommendation with reasoning, not a "have a meeting" outcome.
- [x] PASS: Accountability preserved for CPO and CTO — met. Principles section is explicit; the coordinator coordinates, does not take over domain ownership.
- [x] PASS: Identifies whether OKR deadline can shift with specific options — met. Conflict Resolution Step 4 now explicitly requires enumerating deadline options: "hold the date and scope down, slip the date with a specific revised target, or split the work so the unblocked portion ships on time."
- [x] PASS: Escalation rationale is framed — met. Conflict Resolution Step 3 template explicitly requires stating "why this needed human input" with specific cross-domain and commercial context.
- [x] PASS: Identifies executive-level questions if trade-off is too large — met. Decision Checkpoints table mandates stopping before "resolving a CPO vs CTO conflict by picking a side" and before "changing company-wide OKRs mid-quarter," which maps to surfacing board-level questions when the trade-off exceeds coordinator authority.
- [~] PARTIAL: Addresses activation-target risk if onboarding slips with quantified OKR shortfall and partial mitigation — partially met. The definition asks the coordinator to understand "what's the desired outcome" (activation rate) and commercial signals, but there is no explicit guidance to quantify OKR shortfall or propose partial mitigations like landing-page tweaks. The gap is real. Score: 0.5.

## Notes

The key change from the previous evaluation: coordinator.md now contains an explicit rule at line 275 that directly addresses this scenario — "when proposed new work expands attack surface on a known unpatched vulnerability (e.g. a new flow that touches the same auth path), the vulnerability becomes a non-negotiable constraint on *that work*." This makes criteria 3 and output criterion 2 a clear PASS rather than PARTIAL.

The RATSI still assigns CVSS 7-8.9 risk acceptance to the CTO, but the new rule distinguishes between accepting risk on the *existing* codebase (CTO's call) versus accepting new exposure to an unpatched vulnerability through new work (non-negotiable constraint). That distinction is the right design and it now satisfies the test criteria.

The remaining PARTIAL items are: (1) the deadline-options criterion — the definition provides the three-option framework but does not require a specific revised date, and (2) the activation-target quantification criterion — the definition is silent on quantifying OKR shortfall or proposing interim product mitigations like landing-page tweaks.
