# Product prioritisation

**Scenario:** Competing stakeholder requests land on the CPO's desk simultaneously — a sales-driven feature request, a retention problem flagged by support, and a technical dependency from engineering. Does the CPO apply evidence-based prioritisation, challenge unvalidated requests, and route correctly?

> We have three things all asking for attention on Helipad (our logistics SaaS) right now:
>
> 1. The sales team says we're losing deals because we don't have a mobile app. Two enterprise prospects specifically asked for it last month.
> 2. Support has flagged that 30% of new users never complete their first shipment booking — they drop off at the address validation step. We've had 47 tickets about it in the last 6 weeks.
> 3. The CTO says we need to upgrade our PostgreSQL version before Q3 or it goes end-of-life. It'll take 2 weeks of engineering time.
>
> How do you prioritise these?

Routed to the CPO, which owns product prioritisation and applies evidence-based weighting before routing non-product items to their correct owners.

## Output

**Pre-flight:** Reading CLAUDE.md and .claude/CLAUDE.md... Reading `.claude-plugin/marketplace.json`. Checking for existing PRDs, roadmap artefacts, and analytics data.

Let me work through these in order of evidence quality, not the order they arrived.

**Address validation dropout — highest priority**

This is the clearest item. 47 support tickets in 6 weeks about the same step, combined with 30% dropout at address validation, is strong quantified signal. 30% of new users never complete their first shipment booking — that is a direct hit to activation, which feeds conversion to paid. Problem severity: High. Problem frequency: High.

Before defining a solution, I want the product-owner to investigate root cause at that step. Is it a UX problem, a data quality issue with the address lookup, or a validation rule that's too strict? I also need a success metric defined before engineering work starts — something like reducing address step dropout from 30% to under 10%.

**PostgreSQL upgrade — not my call**

This is a technical dependency decision, not a product prioritisation question. I'm routing it to the CTO. They need to assess the risk of running on an end-of-life version versus the opportunity cost of 2 weeks of engineering time. If the CTO concludes it must happen before Q3, I need to understand what product work it displaces so I can present that trade-off to the human.

What I'm not doing: approving or declining the upgrade timeline. That belongs to the CTO.

**Mobile app — not approved**

Two enterprise prospects asked for mobile in one month. That's anecdote. Before we go anywhere near a mobile app — a multi-quarter investment for a credible v1 — I need: how many of our existing active users attempt to use Helipad on mobile and struggle? Do those two prospects represent our best-fit segment, or are they outliers?

Our principles are clear: 94% of features see low engagement. A mobile app built for two prospects we haven't closed yet is a high-cost bet on thin evidence. I'm not saying no forever. I'm saying: get me mobile usage data from the existing customer base first.

**Summary**

| Item | Priority | Rationale | Next action |
|---|---|---|---|
| Address validation dropout | P0 | 47 tickets + 30% dropout = quantified, high-frequency, directly blocks activation | Delegate to product-owner: root cause investigation + define target dropout rate before engineering starts |
| PostgreSQL upgrade | Technical decision | Not a product prioritisation question | Route to CTO for recommendation + impact assessment on product roadmap |
| Mobile app | Parked pending evidence | Two prospects is not validation at scale | Request mobile usage analytics from existing users; segment analysis |

**Trade-off flagged to the human:** If the PostgreSQL upgrade displaces engineering capacity in Q2, we may need to choose between the address validation fix and the upgrade. I'll need the CTO's input on timing before I can confirm when the address validation work starts.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 7.5/8 (94%) | 2026-04-16 |

- [x] PASS: Challenges mobile app as a solution rather than a validated problem — the definition states "Think in problems, not features. Always reframe feature requests as customer problems"; the Principles section cites "94% of features see low engagement" as justification for saying no without evidence; the Decision Checkpoints require stopping before "Approving a feature without evidence of user need"
- [x] PASS: Identifies address validation as highest priority — the prioritisation framework weights Problem severity and Problem frequency both as High, which is the correct basis for elevating the 47-ticket / 30% dropout item above the others; the definition maps evidence strength and problem frequency directly
- [x] PASS: Applies frequency and severity weighting — the prioritisation table (Section 4) with explicit High weights for Problem severity and Problem frequency is the direct basis for ranking; the response ranks by evidence quality and names both dimensions
- [x] PASS: Escalates PostgreSQL upgrade to CTO — the Escalation Protocol states "Escalate to the CTO when: technical feasibility of a product idea is uncertain / performance or scalability requirements need architectural input"; the upgrade is routed with a question about timing and displacement impact
- [x] PASS: Does not approve mobile without evidence at scale — the Decision Checkpoints table requires stopping before "Approving a feature without evidence of user need"; the 94% principle is explicitly cited in the definition and applied in the response
- [x] PASS: Prioritisation with reasoning — the definition's Delegation Protocol and quality gates require framing the problem before approving work; the response gives three distinct treatments with explicit rationale chains, not a flat ranked list
- [~] PARTIAL: References success metric for the address validation fix — the Product Quality Gates checklist requires "Success metric defined — how will we know this worked? What number changes?" as a gate before approving a product decision; the response mentions defining a dropout rate target before engineering starts but frames this as a to-do, not a completed gate. Intent is present; the framing is conditional. Score: 0.5
- [x] PASS: Does not make the business priority call unilaterally on scope conflicts — the response flags the PostgreSQL vs. address validation capacity conflict explicitly to the human; the Decision Checkpoints include "Committing to a feature for a specific customer deal" as a STOP trigger; cross-team trade-offs are escalated, not decided

## Notes

The CPO definition supports all criteria through explicit rules, a prioritisation table, and a quality gates checklist. The 94% principle is called out verbatim and applied correctly. The PARTIAL on success metrics is legitimate: the quality gates checklist lists "Success metric defined" as a required gate before approving a product decision, but the response frames it as a precondition for the investigation brief, not a completed gate. The definition would benefit from making explicit that success metric definition is a prerequisite for the investigation brief, not an output of it.
