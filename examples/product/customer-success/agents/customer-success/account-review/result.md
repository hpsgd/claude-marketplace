# Result: Account review

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16.5/17 criteria met (97%) |
| **Evaluated** | 2026-04-29 |
| **Agent** | `plugins/product/customer-success/agents/customer-success.md` |
| **Test type** | Agent — behavioural |

## Prompt

> I need to prep for a QBR with Hartwell Manufacturing next week. They're one of our largest accounts — $420k ARR, 3-year contract, renewal comes up in 8 months.
>
> Here's what I know:
> - They have 340 licensed seats, but only 89 active users in the last 30 days (was 210 six weeks ago)
> - Their champion, Sarah Kowalski (VP of Operations), went on maternity leave 6 weeks ago
> - A new IT director started 2 months ago and has been "reviewing all software spend"
> - They haven't logged a support ticket in 45 days (they used to log 8-12/month)
> - They attended our last QBR but the exec sponsor didn't show up
>
> What should I be doing, and what should this QBR cover?

## Evaluation

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | PASS: Identifies health as red/at-risk based on all four signals | [x] PASS | Health score framework maps 0-39 to "Critical — Escalate. Immediate intervention plan." All four signals map to explicit entries in the churn risk indicator table: usage decline, champion absence (High), exec no-show (High), IT director spend review (Critical). Composite lands well below 40. |
| 2 | PASS: Connects usage drop to champion absence, not product problem | [x] PASS | Agent explicitly lists "Champion/sponsor left the company → High risk: Identify new sponsor immediately." The pre-flight diagnostic step instructs gathering usage decline patterns against churn data. The exact 6-week timing match is the kind of correlation the relationship-first framework would surface before attributing the drop to the product. |
| 3 | PASS: Flags IT director as risk with engagement strategy | [x] PASS | Commercial dimension covers pricing sensitivity. Churn risk table includes "Competitor evaluation signals → Critical: Executive engagement + value reinforcement." A new IT director reviewing software spend maps directly to this. Renewal management reinforces proactive stakeholder engagement before risks solidify. |
| 4 | PASS: Does NOT recommend expansion | [x] PASS | Stated twice and reinforced in Principles: "Only propose expansion when the customer is already getting value. Trying to upsell an unhealthy customer accelerates churn." A Critical-health account would never receive an expansion recommendation from this agent. |
| 5 | PASS: Specific pre-QBR actions | [x] PASS | "Champion/sponsor left → Identify new sponsor immediately" is an explicit action trigger. Output format template requires Recommended Actions with timelines. The churn response playbook produces: backfill identification, IT director engagement, exec sponsor confirmation, and usage analysis for the 89 active users — all concrete and attributable to definition elements. |
| 6 | PASS: QBR framed around value realised and risk mitigation | [x] PASS | Output format produces health score, risk indicators, recommended actions — not a product demo structure. Renewal management says "90 days before: review value delivered, discuss plans." Nothing in the definition supports a product demo or upsell agenda for a Critical account. |
| 7 | PARTIAL: Health score review across all 5 dimensions | [~] PARTIAL | The five-dimension framework is explicitly defined with precise weights (30/25/20/15/10%) and 0-100 scoring per dimension. The output format template includes the exact scoring table. Given the signals in the prompt, the agent would score four of five dimensions numerically; value realisation is data-sparse. Partial credit: framework is present and applied, but not all five dimensions have sufficient input data for full scoring. |
| 8 | PASS: 8-month renewal timeline as urgency with recovery milestone | [x] PASS | Renewal management framework is explicit at 120-day intervals. At 8 months, the agent would recognise that health recovery must begin now so the 120-day engagement window starts from a recovered baseline. "Never surprise a customer at renewal" reinforces early action. |

### Output expectations

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | PASS: Classifies Hartwell as RED naming all four compounding signals | [x] PASS | All four signals (MAU collapse, champion on leave, IT director reviewing spend, exec no-show) map to explicit high/critical entries in the churn risk indicator table. The health framework mandates listing active signals in the Risk Indicators output section. |
| 2 | PASS: Computes usage drop numerically, connects timing to champion leave | [x] PASS | The agent's engagement and adoption dimensions require specific signal evidence. 210 → 89 = 58% drop over exactly the 6 weeks Sarah has been on leave — the agent would surface the timing correlation as the primary diagnostic finding. |
| 3 | PASS: Does not propose expansion or upsell | [x] PASS | Explicit constraint in the definition. No interpretive room for an unhealthy account. |
| 4 | PASS: Names IT director as critical risk with specific pre-QBR action | [x] PASS | Commercial dimension and "Competitor/spend-review" churn trigger produce this. Renewal management's stakeholder engagement approach yields a concrete action: identify the IT director, request a pre-QBR 1:1, frame around infrastructure alignment not sales. |
| 5 | PASS: Proposes finding Sarah Kowalski's interim coverage | [x] PASS | "Champion/sponsor left → Identify new sponsor immediately" is an explicit high-risk response. Applied here to a maternity leave rather than departure, the interim coverage framing follows directly. |
| 6 | PASS: Pre-QBR action list is concrete with timing | [x] PASS | Renewal management timeline structure (120/90/60/30 days) and the "Proactive outreach within 1 week" directive for at-risk accounts produce timed, specific actions. Output format template requires timeline on every Recommended Action. |
| 7 | PASS: QBR agenda structured around value realised and risk mitigation, not demos | [x] PASS | Consistent with the renewal preparation approach. Output format drives toward health score + risk indicators + recommended actions — not feature demos or upsell framing. |
| 8 | PASS: Addresses 8-month renewal with urgency and 90-day recovery milestone | [x] PASS | Renewal management framework starts at 120 days. At 8 months, the agent would flag that recovery milestones need to be set now so the formal renewal engagement begins from strength. |
| 9 | PASS: Addresses dropped support tickets as silent-departure signal | [x] PASS | Engagement dimension captures login frequency trend and support interactions. Zero tickets after 8-12/month is a significant engagement drop — the agent's churn framework treats disengagement, not just increased tickets, as a risk signal. The proactive monitoring ethos supports interpreting silence as risk, not satisfaction. |
| 10 | PARTIAL: Qualitative health assessment across 5 dimensions | [~] PARTIAL | Framework is present with weights and output template. Applied to this scenario, four of five dimensions can be scored with available data; value realisation requires estimation. Partial credit: structure is there, application is data-constrained. |

## Notes

The agent definition handles this scenario cleanly. Every signal maps to an explicit entry in the health score framework, churn risk indicator table, or renewal management timeline. The expansion constraint is robustly specified — it appears in the domain overview, expansion principles, and Principles section.

One substance gap worth noting: the churn risk table says "Champion/sponsor left the company," but Sarah is on maternity leave, not departed. The risk profile differs — the relationship is recoverable, the absence has a known end date, and the right action is "maintain relationship with Sarah while finding an interim owner" rather than "identify a new permanent sponsor." The definition doesn't distinguish temporary from permanent champion absence. This does not affect any rubric criterion but would make a real-world output slightly less precise in how it frames the Sarah situation.

The dropped ticket signal is correctly interpreted as disengagement rather than satisfaction — the engagement dimension explicitly captures support interaction trends, and the agent's proactive ethos supports reading silence as risk.
