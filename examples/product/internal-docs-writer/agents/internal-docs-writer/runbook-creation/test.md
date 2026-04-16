# Test: Runbook creation

Scenario: An engineering team needs a runbook for handling payment processing failures so on-call engineers can resolve incidents without tribal knowledge.

## Prompt


Write a runbook for payment processing failures. Context:

- We use Stripe for payment processing
- Common failure modes: Stripe API timeouts, card declines (various codes), idempotency key conflicts, webhook delivery failures
- Our stack: Node.js API, PostgreSQL, Redis for job queues (Bull), Datadog for monitoring
- Alert fires when: payment success rate drops below 95% over 5 minutes, or any Stripe API error rate exceeds 2%
- Business impact: each minute of payment failure = ~$3,400 in lost transactions during peak hours

On-call engineers are expected to handle this without waking anyone up for most scenarios. We've had 4 incidents this quarter and each one took 45+ minutes to resolve because engineers didn't know where to look.

## Criteria


- [ ] PASS: Written for a first-timer at 2am — no assumed knowledge of the system, all commands are copy-pasteable with expected output shown
- [ ] PASS: Includes a decision tree or clear branching logic for different failure modes (API timeout vs card declines vs webhook failures vs idempotency conflicts)
- [ ] PASS: Every diagnostic step includes the exact command or query to run, not just "check the logs" or "look in Datadog"
- [ ] PASS: Includes a rollback or safe revert step for any action that could make the situation worse
- [ ] PASS: Specifies an escalation path with roles and contact method — who to wake up and when, not "escalate if needed"
- [ ] PASS: Documents how to verify the incident is resolved (what metric to watch, what threshold confirms recovery)
- [ ] PARTIAL: Covers all four failure modes mentioned — partial credit if 2-3 are covered but one is missing
- [ ] PASS: Includes severity classification or impact assessment so the on-call engineer can judge urgency (the $3,400/minute context should inform this)
