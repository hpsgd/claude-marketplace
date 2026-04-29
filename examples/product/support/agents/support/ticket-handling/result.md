# Result: Ticket handling

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16/17.5 criteria met (91%) |
| **Evaluated** | 2026-04-29 |

## Scenario

A support agent receives a ticket about a data export timing out. The customer (Marcus) needs data for an upcoming board meeting. The dataset is 180,000 records and the export is failing with a timeout. The agent must classify, investigate, and respond appropriately under time pressure.

Note: the test prompt is structurally incomplete — the ticket body is absent (the prompt ends at "New ticket just came in:"). Evaluation relies on the scenario described in the test header and the criteria themselves, which supply the specifics (Marcus, 180,000 records, board deadline).

## Results

### Criteria

- [x] PASS: Leads with empathy first — the Communication Principles section mandates the order explicitly: "Empathy first, solution second. 'I can see why that's frustrating' before 'Here's how to fix it'." Repeated verbatim in the Principles section. A board deadline makes urgency recognition mandatory under "One contact resolution: If escalating, tell the customer what happens next and when."

- [x] PASS: Classifies across all dimensions — the Ticket Triage section states classification is "MANDATORY for every ticket" and lists five required fields: Category, Severity, Routing, Workaround, and Pattern. The Severity table places "major feature broken" at High with a same-business-day response target, which fits an export failure with a named time constraint.

- [x] PASS: Root cause as hypothesis — Communication Principles include "Be honest about timelines. 'I don't know when this will be fixed, but I'll update you when I have information' beats false promises." The Decision Checkpoints table blocks "Promising a fix timeline to a customer" without engineering input. These constraints prevent presenting an unconfirmed diagnosis as fact.

- [x] PASS: Immediate workaround provided — the Classification table requires "Workaround: Known workaround? Include it." This is a mandatory field, not a suggested one. Escalation and workaround paths run in parallel per the definition.

- [x] PASS: Customer response empathetic, concrete, no internal uncertainty — three Communication Principles converge: empathy-first ordering, "One contact resolution," and the Decision Checkpoint blocking "Sharing internal technical details with a customer."

- [~] PARTIAL: Flags for pattern detection — the Pattern Detection section requires escalation when "3+ tickets on the same issue within a week" and the mandatory Classification table includes a Pattern field. The mechanism exists and is required. However, the criterion asks whether this also warrants a bug report or known issue designation — that outcome depends on checking ticket history not present in this test. 0.5 points.

- [x] PASS: Internal next steps with owners — the Escalation Rules specify who receives bug escalations (engineering), under what conditions, and in what format. The Bug Report Format requires structured fields including Customer impact and Frequency. The Collaboration table defines engineering, QA, and Customer Success roles with explicit handoff patterns.

### Output expectations

- [x] PASS: Customer-facing reply opens with empathy naming the board meeting deadline — the Communication Principles mandate empathy-first and the urgency-acknowledgment pattern. The definition produces this behaviour.

- [x] PASS: Reply provides at least one immediate workaround — mandatory Classification field "Workaround: Known workaround? Include it" ensures a workaround path is always included.

- [x] PASS: Classification labels the ticket consistently across category, severity, and routing — the mandatory triage table covers all three with defined options.

- [x] PASS: Root-cause hypothesis names the specific suspected cause but frames it as a hypothesis — the definition's constraints (honest timelines, block on promising fixes) ensure hypothesis framing. The 180K/timeout diagnosis follows from the scenario details and the agent's reasoning about known export behaviour.

- [x] PASS: Reply does NOT expose internal uncertainty or technical-debt admissions — Decision Checkpoint explicitly blocks "Sharing internal technical details with a customer." This is a hard stop, not a guideline.

- [x] PASS: Internal escalation note names engineering owner, specific investigation steps, and target response time — Bug Report Format requires structured fields; Collaboration table names engineering as the escalation target; Severity table gives response targets for High severity.

- [x] PASS: Output flags for pattern detection — Pattern Detection section mandates searching for the same issue across the ticket queue. The definition requires this check, not just recommends it.

- [x] PASS: Customer reply includes a commitment with a time anchor — "Be honest about timelines" and "One contact resolution" together require a concrete next-step commitment, not vague "we'll get back to you."

- [x] PASS: Output addresses follow-up communication proactively — the "Close the loop" principle explicitly states "When a bug is fixed or a feature ships, tell the customers who reported it." This applies directly to a high-stakes case like this one.

- [~] PARTIAL: Output recommends creating a KB article on exporting large datasets if pattern detection confirms recurrence — the definition states "Every resolved ticket is a KB candidate" and the KB article creation trigger includes "the question is likely to recur." The conditional framing (if pattern is confirmed) means the definition supports this recommendation but only produces it after pattern confirmation, which cannot be confirmed without ticket history. 0.5 points.

## Notes

The missing ticket body is a test authoring issue, not an agent definition issue. The criteria supply enough specifics for evaluation to proceed.

Both PARTIAL scores are structural: they depend on ticket history that is not present in the test scenario. The definition's mechanisms are sound — pattern detection is mandatory, KB creation is triggered by recurrence — but the full-pass conditions require data the agent cannot have in this isolated test.

The definition is strong overall. The Decision Checkpoints table is unusually precise about what requires a pause, which matters for a time-pressured scenario. The Communication Principles are unambiguous about ordering and framing. The mandatory classification fields leave no optional gaps in the triage output.
