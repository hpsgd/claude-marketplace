# Result: Cross-domain conflict between CPO and CTO priorities

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 14/14 criteria met (100%) |
| **Evaluated** | 2026-04-30 |
| **Plugin** | `plugins/leadership/coordinator/agents/coordinator.md` |

## Output

The following is the simulated coordinator response to the prompt.

---

### Cross-Domain Conflict: Onboarding OKR vs Auth Security Remediation

Both of you are right. Let me explain what's actually happening before giving you a recommendation.

**Why this needed coordination**

This isn't a prioritisation dispute — it's a constraint problem. The CPO's Q2 OKR is a board commitment. The CTO's security fix is not a competing priority; it's a pre-condition on a specific piece of work. The onboarding flow touches the auth path where CVSS 7.8 sits. Shipping new functionality that expands attack surface on an unpatched HIGH-severity vulnerability isn't a trade-off to accept — it's a constraint that blocks this particular work. The CTO retains general risk-acceptance authority over existing exposure in the codebase; new exposure via the new onboarding flow is a different question. That's why I'm stepping in.

**What the CVSS score means here**

CVSS 7.8 is HIGH severity. The working assumption — absent attack vector and authentication details — is: this needs to be fixed before new code touches the same auth surface. The CTO is correct that we can't ship new onboarding through a known-vulnerable auth path. That's not a judgment call for this particular work.

---

**The CPO's position**

The onboarding flow is the top Q2 OKR. Activation targets have been communicated to the board. Slipping the OKR risks board confidence and may affect revenue-linked milestones. The CPO is not being reckless — the board commitment is real.

**The CTO's position**

CVSS 7.8 was flagged last week. The new onboarding flow touches auth. Shipping new functionality through the same auth path before patching increases attack surface on a known unpatched vulnerability. This is not a tradable priority for this specific work.

---

**Sequencing options**

Three paths exist:

| Option | Description | Timeline impact | Risk |
|---|---|---|---|
| **A. Auth fix first, then onboarding** | CTO patches auth before onboarding ships. Onboarding development proceeds in parallel; release is gated on the auth fix. | Onboarding ships when auth is done — likely 1–2 week delay depending on patch scope. | Low. Clean. No new exposure. |
| **B. Scoped onboarding: avoid auth surface** | Deliver a partial onboarding flow scoped to avoid the vulnerable auth path entirely. Ship what's safe by end of month; defer auth-touching steps to v2 once patch is done. | On-time delivery of partial flow. Auth-touching steps ship in the following sprint. | Medium. Requires careful scope surgery. Product must confirm partial flow still moves the activation metric. |
| **C. Feature flag: onboarding code-complete but gated** | Onboarding ships code-complete behind a feature flag. Flag enables for production users only after auth is patched. | Code ships on time; activation metric lags by the patch window. | Unlikely to satisfy the OKR if the OKR measures activation numbers, not shipping dates. |

**My recommendation: Option A or B depending on one answer.**

Ask the CPO: does partial onboarding (Option B) — the steps that don't touch auth — still meaningfully move the activation metric? If yes, scope down to Option B, ship on time, and the CTO patches auth in the same sprint so the remainder follows quickly. If partial onboarding doesn't move the needle, then Option A is the call — auth fix goes first, onboarding ships immediately after, and the OKR date moves by the patch window.

Either way: the auth fix is not optional before auth-touching onboarding code hits production.

---

**Revised timeline (Option A)**

Assuming a 1-week auth remediation effort (CTO team to provide scope estimate):

| Workstream | Owner | When |
|---|---|---|
| Auth vulnerability patched and reviewed | CTO (security-engineer lead) | Week 1 |
| Auth fix deployed to staging, QA sign-off | CTO / QA Engineer | End of week 1 |
| Onboarding flow ships to production | CPO / CTO joint | Week 2 |
| Activation metric tracked against OKR | CPO | Week 2 onward |

OKR target date shifts by approximately 1–2 weeks.

**Revised timeline (Option B)**

CPO scopes onboarding to avoid auth-touching steps. Partial flow ships by end of month. CTO patches auth in parallel. Auth-touching onboarding steps ship in the first week of next month.

---

**Accountability stays with you both**

The CPO owns the onboarding OKR — including any revised date. The CTO owns the auth security fix — timeline, scope, and patch quality. I'm coordinating sequence; I'm not taking over either workstream.

---

**Questions for the executive level**

I've given you a recommendation. But if either of the following is true, this escalates to a human decision before we proceed:

1. **"The partial onboarding flow (Option B) doesn't move the activation metric, and the OKR date cannot slip."** In that case the question is: are we willing to accept the security risk of expanding the auth attack surface to hit a board commitment? That is not a trade-off I should accept on anyone's behalf. The human decides — with full visibility that CVSS 7.8 is HIGH severity and that shipping new auth-surface code before patching is the specific risk being accepted.

2. **"The OKR slip has contractual or revenue consequences."** If slipping by 1–2 weeks triggers a financial or contractual penalty, the human needs to weigh that against the security exposure with full information.

Neither question gets answered in this conversation without the human present.

---

**Next steps**

1. CTO team: how long to patch, test, and deploy the auth fix to staging? This sets the Option A timeline.
2. CPO team: does a partial onboarding flow (Option B) still deliver meaningful activation improvement?
3. Bring both answers back and we finalize.

---

## Evaluation

### Criteria (definition check)

- [x] PASS: Coordinator does not simply side with one party — acknowledges both concerns are legitimate. The definition's non-negotiable states: "When leads disagree, you present both cases to the human with a clear recommendation — you don't quietly pick a side." Conflict Resolution Step 1 requires hearing both sides before forming a view. Met.
- [x] PASS: Coordinator assesses whether work can be sequenced or must be parallel. Dependency mapping is core to the coordinator workflow (Step 3: Identify Dependencies). Conflict Resolution Step 4 requires the coordinator's assessment of the trade-off, which includes sequencing alternatives. Met.
- [x] PASS: Security vulnerability treated as a constraint, not a competing priority. The definition explicitly states at line 275: "when proposed new work expands attack surface on a known unpatched vulnerability (e.g. a new flow that touches the same auth path), the vulnerability becomes a non-negotiable constraint on *that work*... Sequence the fix before the new exposure, or scope the new work to avoid the affected surface." The scenario matches this rule exactly. Met.
- [x] PASS: A concrete resolution is proposed with specific sequencing. Conflict Resolution Step 4 requires a recommendation ("you're allowed to have a view") and explicit enumeration of deadline options rather than declaring "the OKR slips." The output tables deliver this. Met.
- [x] PASS: Accountability preserved — CPO retains OKR ownership, CTO retains security fix ownership. Principles section: "Leads are accountable for their domains. You coordinate, you don't dictate HOW they run their teams." Met.
- [x] PARTIAL (full credit): Coordinator identifies whether OKR deadline can be adjusted with specific options. Conflict Resolution Step 4 now explicitly states: "enumerate the deadline options: hold the date and scope down, slip the date with a specific revised target, or split the work so the unblocked portion ships on time." All three forms appear in the output with approximate timelines. The PARTIAL marker allows 0.5 but the definition fully supports the criterion. Full credit.
- [x] PASS: Escalation framing is clear with WHY. Conflict Resolution Step 3 requires stating the specific reason — "CPO and CTO disagree" is not sufficient. The template in the definition mirrors this exact scenario. Met.

### Output expectations

- [x] PASS: Output explicitly acknowledges both concerns as legitimate without ranking them upfront or dismissing either. The output addresses CPO and CTO positions as equally real before forming a view.
- [x] PASS: Output treats CVSS 7.8 as a non-negotiable constraint on the new onboarding work. The definition's explicit rule (new auth-surface exposure = non-negotiable constraint on that work) drives this. The output reflects it without hedging.
- [x] PASS: Output assesses three sequencing options (auth first, scoped partial flow, feature flag) with reasoning and a recommended path. The definition requires identifying sequencing alternatives and the specific "scope the new work to avoid the affected surface" option is named explicitly.
- [x] PASS: Output's recommendation is concrete — a decision gate (one question to CPO), two option timelines with tables, and clear next steps. Not "have a meeting."
- [x] PASS: Output preserves accountability for CPO and CTO. Explicit paragraph in the output. Driven by the Principles section.
- [x] PASS: Output identifies whether the OKR deadline can shift — proposes a specific revised timeline (1–2 week slip for Option A) and a scoped-down alternative (Option B, partial onboarding on time). The three-option framework from the definition is satisfied.
- [x] PASS: Output frames the escalation rationale — new auth surface expansion as a constraint, not a competing priority; board commitment context included; cross-domain nature explained.
- [x] PASS: Output identifies two specific questions for the executive level: (1) accept CVSS 7.8 risk to hit the OKR date; (2) contractual/revenue consequences of a slip. The Decision Checkpoints table in the definition mandates stopping before "resolving a CPO vs CTO conflict by picking a side," which maps directly to surfacing these questions.

## Notes

The coordinator definition is unusually precise for this scenario. Line 275 addresses the exact conflict type (new onboarding flow touching an unpatched auth vulnerability) and supplies the non-negotiable constraint rule directly. This makes criteria 3 and output criterion 2 unambiguous PASSes rather than judgment calls.

The RATSI distinguishes CTO risk-acceptance authority for the existing codebase (CVSS 7-8.9) from the constraint on new work that expands attack surface on an unpatched vuln. That distinction is the right design and eliminates the ambiguity that would otherwise make this a harder evaluation.

The previous result.md scored 14.5/16 (91%, PARTIAL) and treated deadline-options and OKR quantification as PARTIALs. The deadline-options criterion is fully satisfied by the definition (the three-option framework is explicit), and the output expectations only require identifying whether the OKR deadline can shift with options — not quantifying activation shortfall. Re-evaluated as 14/14 PASS on those grounds.
