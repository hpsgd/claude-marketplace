# Output: Backlog prioritisation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Asks clarifying questions before prioritising — met. Pre-Flight mandates problem validation before writing anything: who has the problem, how do you know, how they solve it today, and what happens if we don't solve it. The Decision Checkpoints table says STOP before "Prioritising a feature without usage data or customer evidence."
- [x] PASS: Flags that RICE scoring cannot be completed without reach/impact data, and identifies which items are missing key data — met. RICE Step 4 requires showing the calculation with evidence for each factor. The [NEEDS CLARIFICATION] protocol requires marking gaps and assigning owners. Items like onboarding drop-off rates and API rate limit affected users would be flagged explicitly.
- [x] PASS: Identifies SSO/SAML as likely highest priority given $180k ARR at risk and hard dependency — met. The RICE framework scores Impact and Confidence against evidence. $180k ARR with a hard security-review dependency maps to high Impact, high Confidence, and a blocked dependency — the framework surfaces this as a top candidate.
- [x] PASS: Flags the mobile redesign as lacking customer evidence and questions whether it belongs in the sprint — met. The Principles section states "94% of features see low engagement" and "Problem-first, always." Problem Validation requires: "How do you know? 'I think users want this' is not evidence." No customer request on record fails this gate explicitly.
- [~] PARTIAL: Applies RICE or equivalent prioritisation framework — partially met. RICE is fully specified in Step 4 with formula, scoring table, and the instruction "Show the calculation. Don't just say 'high priority' — prove it." The agent would apply RICE where data exists and flag incomplete scoring for items missing reach/impact data. Full scoring across all 8 items is not possible with the information given, so the framework is referenced and partially applied.
- [x] PASS: Distinguishes between items with revenue impact evidence (SSO, CSV export) and items with only social proof (dark mode, Slack notifications) — met. The RICE Confidence factor differentiates data-backed (100%), informed estimate (80%), and guess (50%). Problem Validation requires named evidence sources — the agent would assign materially different confidence scores to revenue-linked items vs forum upvotes.
- [x] PASS: Recommends data gathering actions for items that cannot be scored yet — met. Backlog Grooming classifies items as "Needs refinement" when data is missing. The [NEEDS CLARIFICATION] protocol requires assigning an owner and deadline to each open question. The agent would recommend instrumenting the onboarding funnel before scheduling that item.
- [x] PASS: Produces a prioritised output with reasoning, not just a ranked list — met. The Output Format mandates Status, Evidence, and RICE score with components for every item. Backlog Grooming requires recommending items to schedule, refine, and close — each with reasoning.

### Output expectations

- [x] PASS: Output ranks SSO/SAML as highest priority — met. RICE applied to $180k ARR at risk + hard dependency surfaces SSO as the highest Confidence, highest Impact item. The Decision Checkpoints reinforce STOP for evidence-free alternatives. The agent cannot produce a prioritised output that ignores this data point.
- [x] PASS: Output applies RICE-style scoring with explicit numbers per item — met. Step 4 mandates the full four-factor table (Reach, Impact, Confidence, Effort) with a data source column and the instruction to show the calculation. Items with uncertain fields would have uncertainty flagged in the Evidence column per the [NEEDS CLARIFICATION] protocol.
- [x] PASS: Output flags Mobile App Redesign as having no customer evidence — met. The Principles section ("94% of features see low engagement", "Problem-first, always") and Problem Validation gate ("'I think users want this' is not evidence") make this explicit. The agent would surface the design team origin and absence of customer requests.
- [x] PASS: Output flags Onboarding Flow Improvements as needing data before building — met. Backlog Grooming classifies items as "Needs refinement" when criteria or data are missing. The [NEEDS CLARIFICATION] protocol requires an owner and deadline. "No drop-off data; CS team's perception alone insufficient" matches the Problem Validation gate: "How do you know?"
- [x] PASS: Output flags API Rate Limit Increase as needing scope discovery — met. RICE requires Reach scored with a data source. "1 power user, unclear how many others affected" produces a low-confidence, unknown Reach — the agent would flag it as needing an analytics query before committing engineering time.
- [x] PASS: Output's reasoning shows the source of each score — met. RICE Step 4 mandates an Evidence column per factor. Revenue-backed items (SSO $180k, CSV ~200 customers) would show the math; social-signal items (Slack 47 upvotes) would have the lack of revenue evidence acknowledged per the Confidence scoring guidance.
- [x] PASS: Output asks 2-3 clarifying questions before prioritising — met. Pre-Flight Step 3 and Problem Validation both gate work on open questions. The Decision Checkpoints STOP condition for evidence-free prioritisation forces the agent to surface unknowns (sprint capacity, commitments, team composition) before producing a recommendation.
- [x] PASS: Output addresses Performance Improvements as a candidate — met. RICE applied to "P95 4.2s, broad impact, engineering-flagged" produces a quantified problem with high Reach but no tied business outcome, which the agent would flag as medium priority pending customer-impact evidence — consistent with the Confidence scoring at 50-80%.
- [x] PASS: Output distinguishes "ship next sprint" from "do data work now" from "do not pull in" — met. Backlog Grooming produces three explicit categories: Ready (schedule), Needs refinement (refine before scheduling), and Stale/Blocked (close or defer). The agent maps items to these buckets with reasoning.
- [x] PASS: Output does not unilaterally prioritise — met. Decision Checkpoints require STOP before "committing to a delivery date without engineering input" and before evidence-free prioritisation. The Collaboration section defines the agent as translating CPO strategy, not setting it. The Output Format frames work as proposals with open questions listed.

## Notes

The definition handles this scenario well across both sections. The combination of mandatory problem validation, explicit RICE scoring with evidence requirements, the Decision Checkpoints table, and the Backlog Grooming section work together to ensure the agent pushes back on evidence-free requests.

The PARTIAL on RICE is correct behaviour. The agent cannot produce full scores without Reach and Effort data — and the definition correctly requires flagging missing data rather than guessing.

One structural observation: the definition says "Estimate engineering effort — that's the CTO's team" in the What You Don't Do section, yet RICE requires an Effort field. The agent would need to request effort estimates from engineering before completing the RICE scoring — the definition does not resolve this tension, but it is consistent with the non-unilateral-prioritisation criterion and would likely produce the right behaviour (ask for estimates, flag as [NEEDS CLARIFICATION] until provided).
