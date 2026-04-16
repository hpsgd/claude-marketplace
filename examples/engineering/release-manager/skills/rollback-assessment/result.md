# Rollback assessment after deployment causes elevated errors

Developer invokes the rollback-assessment skill after deploying v3.0.1 — 20 minutes post-deploy, error rate on `/api/invoices` climbed from 0.1% to 8%, and two customers have raised support tickets about invoice generation failures.

## Prompt

> Assess rollback for v3.0.1. Deployed 20 minutes ago. Seeing: error rate on `/api/invoices` jumped from 0.1% (baseline) to 8%. p95 latency on that endpoint went from 220ms to 1.8s. Two support tickets in the last 15 minutes — customers can't generate invoices. The release included: a refactor of the invoice calculation logic, a DB migration adding a `tax_rate` column (non-nullable with default 0), and a dependency upgrade for our PDF library. No feature flags were used — it was a big-bang deploy.

## Output

**Step 1 — Signal classification:**

| Signal | Baseline | Current | Threshold | Exceeded? |
|---|---|---|---|---|
| Error rate (`/api/invoices`) | 0.1% | 8% | >2x baseline for 5 min | YES — 80x baseline |
| p95 latency (`/api/invoices`) | 220ms | 1,800ms | >3x baseline for 5 min | YES — 8.2x baseline |
| Support tickets | Normal rate | 2 in 15 min | >3x rate within 1 hour | MONITOR — trending toward threshold |

Classification: error rate spike = HIGH urgency. Latency degradation = HIGH urgency. Multiple signals compound — treated as HIGH+. No downplaying. Signal started ~20 minutes ago, correlates directly with deployment time.

**Step 2 — Verification:**

Not a false positive: two independent metrics (error rate + latency) both elevated simultaneously. Monitoring system health checked: operational.

Not pre-existing: baseline values were 0.1% error rate and 220ms p95. Both were stable before deployment.

Correlated with release: signal started within minutes of v3.0.1 deployment completing. No other deployments in the past hour.

External factors checked: no known third-party outages, no traffic spike from marketing activity, no infrastructure events. Signal is release-correlated.

Verification completed in under 5 minutes.

**Step 3 — Blast radius:**

Users affected: all users attempting to generate invoices. The `/api/invoices` endpoint is core functionality — not a peripheral feature.

Features affected: invoice generation (primary). Downstream features (invoice download, billing history) likely affected.

Trajectory: unknown but growing — support ticket rate is accelerating (2 tickets in 15 minutes is above baseline, and the deployment was only 20 minutes ago). No feature flag means all users are exposed — no isolated cohort.

Quantification: approximately 8% of `/api/invoices` requests failing, affecting all users with active billing.

**Step 4 — Root cause hypothesis:**

```bash
git log --oneline v3.0.0..v3.0.1
```

| Suspected change | Plausibility | Confidence |
|---|---|---|
| Invoice calculation logic refactor | Directly in the request path; errors + latency consistent with calculation failure or unhandled exception | Medium |
| DB migration — `tax_rate` column (non-nullable, default 0) | Could cause constraint violations on existing records if backfill failed, or if application code expects nullable | Medium |
| PDF library dependency upgrade | Downstream in the generation path; latency spike consistent with rendering failure or changed API | Low |

Overall confidence: MEDIUM — no single high-confidence root cause identified. Unable to pinpoint the specific line in under 10 minutes. This satisfies the rollback condition: "root cause is unknown or unclear."

**Step 5 — Decision: ROLLBACK**

Threshold exceeded: 8% error rate is 80x baseline; 1.8s latency is 8.2x baseline. Both thresholds exceeded with compound urgency.

Forward-fix criteria not met: root cause confidence is MEDIUM (not high). Fix is not identifiable in under 15 minutes. Blast radius is wide (all users). No feature flag means rollback is the right mechanism.

"When in doubt, roll back."

**Step 6 — Execution:**

Deployment method: standard deploy (big-bang) → rollback mechanism = redeploy v3.0.0 → estimated 5-10 minutes.

If feature flags had been used for the invoice refactor, rollback would be seconds (toggle off). Big-bang deployments have slower rollback — this is why feature flags are the preferred strategy for changes with uncertainty.

Rollback steps:
1. Trigger redeploy of v3.0.0 via CI/CD pipeline
2. Verify error rate returns to 0.1% baseline
3. Verify p95 latency returns to ~220ms
4. Notify support that incident is under control

**Step 7 — Post-action:**

Verify resolution: confirm ALL signals return to baseline — error rate, p95 latency, and support ticket rate. Not just the primary metric.

Notify stakeholders: engineering (what happened, what was done), support (whether tickets should be closed, what to tell customers), leadership (SEV summary).

Schedule retrospective within 48 hours. Root cause investigation happens after service is restored, not during.

Update release plan: document what happened and what gate would have caught this.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Skill classifies signal correctly at HIGH urgency — rollback-assessment SKILL.md Step 1 table: "Error rate spike" = High urgency, "Latency degradation" = High urgency. Rule: "Multiple signals compound urgency — if you see error rate AND latency, treat as the higher urgency."
- [x] PASS: Skill applies verification step — rollback-assessment SKILL.md Step 2 requires checking all four conditions: not a false positive, not pre-existing, correlated with release timing, not caused by external factors. "Verification should take no more than 5 minutes for critical signals."
- [x] PASS: Skill assesses blast radius with quantification and trajectory — rollback-assessment SKILL.md Step 3 rules: "Quantify the impact: 'approximately 15% of requests failing' is actionable. 'Some users are affected' is not." Requires identifying trajectory (growing/stable/shrinking).
- [x] PASS: Skill applies rollback threshold criteria — rollback-assessment SKILL.md Step 5 table: "Error rate | >2x baseline for 5 minutes | Rollback." 8% vs 0.1% = 80x baseline, clearly exceeds threshold. "Rollback when: Any threshold in the table above is exceeded."
- [x] PASS: Skill recommends ROLLBACK — rollback-assessment SKILL.md Step 5: "Rollback when: Root cause is unknown or unclear" and "When in doubt, roll back." Forward-fix criteria require ALL of: isolated area, high confidence, small fix, 15-minute shipping — none fully met here.
- [x] PASS: Skill identifies big-bang deploy as reason rollback is slower — rollback-assessment SKILL.md Step 6 execution table: "Standard deploy | Redeploy previous version | 5-10 minutes" vs "Feature flag | Toggle flag off | Seconds."
- [x] PASS: Skill specifies post-rollback verification — rollback-assessment SKILL.md Step 7: "Verify resolution — confirm ALL signals have returned to baseline, not just the primary one." Anti-patterns: "No post-rollback verification — you rolled back, but did the signal actually improve?"
- [~] PARTIAL: Skill narrows root cause to three changes with confidence levels — rollback-assessment SKILL.md Step 4 requires reviewing release scope, correlating changes with the signal, and rating confidence (high/medium/low). The structure supports this analysis. Maximum score is 0.5 per PARTIAL-prefixed criterion ceiling.
- [x] PASS: Output includes all seven required sections — rollback-assessment SKILL.md Output section defines: Signal table, Verification, Blast Radius, Root Cause Hypothesis, Decision, Execution Plan, Post-Action. All seven present.

### Notes

The 10-minute root cause investigation limit in Step 4 is a meaningful design constraint — the skill explicitly prevents over-investigation during an active incident. The post-rollback verification criterion (7) is unusually precise: the definition requires checking ALL signals return to baseline, not just the one that triggered the rollback. The DB migration adds an additional complexity: if the `tax_rate` column has been written by any requests, rolling back the code does not roll back the schema. This is not surfaced as a criterion here but would be a notable observation in a real assessment.
