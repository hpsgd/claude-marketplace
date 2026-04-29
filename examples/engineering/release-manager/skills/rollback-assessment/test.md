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

## Output expectations

- [ ] PASS: Output's signal table lists the exact prompt facts — error rate jumped from 0.1% baseline to 8% (80x), p95 went from 220ms to 1.8s (8x), 2 support tickets in 15 min, 20 minutes since deploy — with the timestamp anchors
- [ ] PASS: Output's verification step correlates the spike with the deploy timestamp (20 min ago) and rules out external factors (no upstream provider outage, no traffic spike, no adjacent unrelated deploy)
- [ ] PASS: Output's blast radius quantifies affected requests/customers — e.g. "8% of `/api/invoices` traffic affected; if endpoint runs at X req/min, that's Y failed invoice generations per minute" — and notes the trajectory is growing (2 tickets in 15 min suggests more pending)
- [ ] PASS: Output applies the rollback threshold rule explicitly — "error rate >2x baseline for ≥5 min triggers rollback; we have 80x for ≥15 min" — and concludes the threshold is decisively breached
- [ ] PASS: Output recommends ROLLBACK (not forward-fix) and names the four reasons: unknown root cause confidence, wide blast radius, no feature flag toggle, threshold exceeded for >5 minutes
- [ ] PASS: Output flags the big-bang deploy as the reason rollback is slower (full redeploy of the previous artefact) — and quantifies the expected rollback duration
- [ ] PASS: Output's root cause hypothesis lists all three changes (invoice refactor, `tax_rate` migration, PDF library upgrade) with a confidence rating and reasoning per — e.g. migration is high suspicion if non-nullable default-0 doesn't match expected per-customer rates; refactor is medium; PDF library is low unless it touches calculation
- [ ] PASS: Output's execution plan includes specific steps — initiate redeploy of previous version, decide whether to roll back the migration (and how — `tax_rate` column with default may be safe to leave; the `subscription_events` table is additive so it stays), notify support, watch error rate
- [ ] PASS: Output's post-rollback verification requires confirming error rate returns to the 0.1% baseline AND p95 returns to ~220ms BEFORE declaring resolution — not just "errors stopped climbing"
- [ ] PARTIAL: Output's post-action steps include a blameless retro to identify why no feature flag was used, why the staging tests didn't catch this, and whether this category of change should have a stricter gate
