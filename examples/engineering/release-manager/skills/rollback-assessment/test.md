# Test: Rollback assessment after deployment causes elevated errors

Scenario: Developer invokes the rollback-assessment skill after deploying v3.0.1 — 20 minutes post-deploy, error rate on `/api/invoices` climbed from 0.1% to 8%, and two customers have raised support tickets about invoice generation failures.

## Prompt

Assess rollback for v3.0.1. Deployed 20 minutes ago. Seeing: error rate on `/api/invoices` jumped from 0.1% (baseline) to 8%. p95 latency on that endpoint went from 220ms to 1.8s. Two support tickets in the last 15 minutes — customers can't generate invoices. The release included: a refactor of the invoice calculation logic, a DB migration adding a `tax_rate` column (non-nullable with default 0), and a dependency upgrade for our PDF library. No feature flags were used — it was a big-bang deploy.

## Criteria

- [ ] PASS: Skill classifies the signal correctly — error rate spike (High urgency) + health impact — and does not downplay severity
- [ ] PASS: Skill applies the verification step — checks the signal is real, correlated with the release timing, and not a false positive or external factor
- [ ] PASS: Skill assesses blast radius — quantifies affected users/requests, identifies trajectory (growing/stable/shrinking)
- [ ] PASS: Skill applies the rollback threshold criteria — error rate >2x baseline for 5 minutes is the threshold, and 8% vs 0.1% baseline clearly exceeds it
- [ ] PASS: Skill recommends ROLLBACK (not forward-fix) given: unknown root cause confidence, wide blast radius, no feature flag available, and threshold exceeded
- [ ] PASS: Skill identifies the big-bang deploy as the reason rollback is slower (full redeploy) vs feature flag (toggle off)
- [ ] PASS: Skill specifies post-rollback verification — confirm error rate returns to baseline before declaring resolution
- [ ] PARTIAL: Skill narrows the root cause hypothesis to the three changes (invoice refactor, migration, PDF library upgrade) and rates confidence level for each
- [ ] PASS: Output includes Signal table, Verification, Blast Radius, Root Cause Hypothesis, Decision with reasoning, Execution Plan, and Post-Action steps
