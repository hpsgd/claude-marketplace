# Test: Ticket handling

Scenario: A support agent receives a ticket about a data export timing out, and needs to classify, investigate, and respond appropriately.

## Prompt


New ticket just came in:

## Criteria


- [ ] PASS: Leads with empathy and acknowledgment of urgency before any technical content — the board report deadline is recognised, not ignored
- [ ] PASS: Classifies the ticket across all dimensions: category (bug/data/performance), severity (high — time-sensitive business impact), and routing (likely escalation to engineering given dataset size)
- [ ] PASS: Identifies the likely root cause (180,000 records likely exceeding export timeout threshold) as a hypothesis, not a definitive answer
- [ ] PASS: Provides an immediate workaround or interim path — e.g. date range slicing, filtered export, async export if available — so Marcus can get data before the board meeting
- [ ] PASS: Drafts a customer-facing response that is empathetic, concrete, and does not expose internal technical uncertainty
- [ ] PARTIAL: Flags this ticket for pattern detection — if other customers have hit export timeouts with large datasets, this warrants a bug report or known issue — partial credit if escalation is recommended but pattern check is not mentioned
- [ ] PASS: Specifies next internal steps with owners — who investigates, what they check, by when given the urgency
