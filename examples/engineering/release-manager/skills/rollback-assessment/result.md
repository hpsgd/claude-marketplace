# Rollback Assessment

Scenario: Developer invokes the rollback-assessment skill after deploying v3.0.1 — 20 minutes post-deploy, error rate on `/api/invoices` climbed from 0.1% to 8%, and two customers have raised support tickets about invoice generation failures.

## Prompt

> Assess rollback for v3.0.1. Deployed 20 minutes ago. Seeing: error rate on `/api/invoices` jumped from 0.1% (baseline) to 8%. p95 latency on that endpoint went from 220ms to 1.8s. Two support tickets in the last 15 minutes — customers can't generate invoices. The release included: a refactor of the invoice calculation logic, a DB migration adding a `tax_rate` column (non-nullable with default 0), and a dependency upgrade for our PDF library. No feature flags were used — it was a big-bang deploy.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Rollback Assessment: v3.0.1

### Signal
| Signal | Baseline | Current | Threshold | Exceeded? |
|---|---|---|---|---|
| Error rate `/api/invoices` | 0.1% | 8.0% | >2x (0.2%) | **YES** (80x) |
| p95 latency `/api/invoices` | 220ms | 1,800ms | >3x (660ms) | **YES** (8.2x) |
| Support tickets (invoicing) | ~0 in 15min | 2 in 15min | Customer impact signal | **YES** |

### Verification
- **False positive ruled out:** No — these are real user requests failing. Multi-signal confirmation: error rate spike + latency spike + customer reports all align
- **Correlated with release:** Yes — all signals appeared within 20 minutes of v3.0.1 deployment. Timing is conclusive
- **External factors ruled out:** No evidence of third-party outage or traffic anomaly mentioned; assume release-related until proven otherwise

### Blast Radius
- **Users affected:** Core invoicing flow — unknown exact percentage, but "customers can't generate invoices" suggests broad impact to billing-critical path
- **Features affected:** `/api/invoices` endpoint (single endpoint, but critical)
- **Trajectory:** Stable or growing — 2 support tickets in 15 minutes is ongoing, not declining
- **Downstream:** If invoices can't generate, payment/reconciliation workflows likely blocked

### Root Cause Hypothesis
**Suspected causes (in order of likelihood):**
1. **Invoice calculation logic refactor** — Direct correlation with `/api/invoices` spike; likely contains a bug introduced during refactor
2. **DB migration (tax_rate column)** — Non-nullable column with default 0 should work, but if refactored code has assumptions about column presence/state or migration didn't propagate cleanly, could cause failures
3. **PDF library upgrade** — Less likely; would need to break in a way that causes latency spike

**Confidence:** Medium — the refactor correlates directly with the endpoint, but root cause requires code inspection

### **Decision: ROLLBACK**

**Reasoning:**
- **Error rate threshold exceeded** (80x baseline, threshold is 2x) ✓
- **Latency threshold exceeded** (8.2x baseline, threshold is 3x) ✓
- **No feature flags to isolate** — this is a big-bang deploy; cannot selectively disable
- **Root cause unclear** — would need >15 min investigation + fix + testing
- **Customer impact is active** — invoicing is core revenue functionality
- **Rollback is faster and safer** than forward-fixing an unknown issue

Forward-fix is not viable here: the invoice refactor is significant in scope, you don't have the root cause pinned, and the cost of guessing wrong is extending the outage.

---

### Execution Plan

1. **Redeploy v3.0.0** (previous stable release)
   - Rollback mechanism: Standard deploy redeploy (5–10 minutes)
   - Use the same pipeline/tooling as the original v3.0.1 deploy

2. **Monitor during rollback**
   - Watch `/api/invoices` error rate and p95 latency
   - Confirm both return to baseline (0.1% error, ~220ms p95)
   - No new support tickets

3. **Verify resolution** (critical — do not skip)
   - Error rate back to 0.1%: ✓
   - Latency back to 220ms: ✓
   - No ongoing customer reports: ✓

4. **Notify stakeholders immediately**
   - **Engineering:** "Rolled back v3.0.1 due to 80x error rate spike on `/api/invoices`. Previous version restored. Retrospective scheduled for [date]."
   - **Support:** "Invoicing issue resolved. Service is stable. Customers should be able to generate invoices now."
   - **Leadership:** SEV-2 incident (customer-facing, revenue path). 20 min outage. Root cause investigation TBD.

---

### Post-Action

- **Retrospective:** Schedule for tomorrow (within 48 hours). Investigate:
  - What in the invoice refactor caused the spike?
  - Why did the DB migration not catch the issue?
  - How do we test invoice calculation before release next time?
  - Should this have had a feature flag or canary?

- **Before re-deploying v3.0.1:**
  - Code review the invoice refactor specifically
  - Add integration tests for invoice calculation + tax_rate column interaction
  - Test with production-like data volumes
  - Use a feature flag or canary for the next attempt

**Rollback decision: EXECUTE IMMEDIATELY.** Every minute in an outage costs trust and revenue. Roll back now, investigate after service is restored.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/17.5 (86%) |
| Evaluated | 2026-04-30 |
| Target duration | 30062 ms |
| Target cost | $0.0335 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill classifies the signal correctly — error rate spike (High urgency) + health impact — and does not downplay severity | PASS | Signal table labels threshold as exceeded at 80x baseline; decision section states 'ROLLBACK EXECUTE IMMEDIATELY. Every minute in an outage costs trust and revenue.' |
| c2 | Skill applies the verification step — checks the signal is real, correlated with the release timing, and not a false positive or external factor | PASS | Verification section explicitly addresses: 'False positive ruled out: No — these are real user requests failing', 'Correlated with release: Yes — all signals appeared within 20 minutes of v3.0.1 deployment', 'External factors ruled out: No evidence of third-party outage or traffic anomaly' |
| c3 | Skill assesses blast radius — quantifies affected users/requests, identifies trajectory (growing/stable/shrinking) | PASS | Blast Radius section states 'core invoicing flow — broad impact to billing-critical path'; signal table quantifies 8% error rate; trajectory identified as 'Stable or growing — 2 support tickets in 15 minutes is ongoing, not declining' |
| c4 | Skill applies the rollback threshold criteria — error rate >2x baseline for 5 minutes is the threshold, and 8% vs 0.1% baseline clearly exceeds it | PASS | Signal table column 'Threshold' shows '>2x (0.2%)' and 'Exceeded? YES (80x)'; decision reasoning restates 'Error rate threshold exceeded (80x baseline, threshold is 2x)' |
| c5 | Skill recommends ROLLBACK (not forward-fix) given: unknown root cause confidence, wide blast radius, no feature flag available, and threshold exceeded | PASS | Decision section: 'ROLLBACK' with four explicit bullet reasons: threshold exceeded, latency exceeded, 'No feature flags to isolate', 'Root cause unclear — would need >15 min investigation'. Also 'Forward-fix is not viable here' |
| c6 | Skill identifies the big-bang deploy as the reason rollback is slower (full redeploy) vs feature flag (toggle off) | PARTIAL | Output mentions 'No feature flags to isolate — this is a big-bang deploy; cannot selectively disable' and execution plan gives 'Standard deploy redeploy (5–10 minutes)', but never explicitly contrasts rollback speed against a feature-flag toggle-off as being faster/simpler |
| c7 | Skill specifies post-rollback verification — confirm error rate returns to baseline before declaring resolution | PASS | 'Verify resolution (critical — do not skip)' step lists: 'Error rate back to 0.1%: ✓, Latency back to 220ms: ✓, No ongoing customer reports: ✓' |
| c8 | Skill narrows the root cause hypothesis to the three changes (invoice refactor, migration, PDF library upgrade) and rates confidence level for each | PARTIAL | Root Cause Hypothesis section lists all three changes in order of likelihood with brief reasoning per each; overall 'Confidence: Medium' stated, but individual per-item confidence ratings are not given — only an ordinal ranking |
| c9 | Output includes Signal table, Verification, Blast Radius, Root Cause Hypothesis, Decision with reasoning, Execution Plan, and Post-Action steps | PASS | All seven named sections are present with headers: '### Signal', '### Verification', '### Blast Radius', '### Root Cause Hypothesis', '### Decision: ROLLBACK', '### Execution Plan', '### Post-Action' |
| c10 | Output's signal table lists the exact prompt facts — error rate jumped from 0.1% baseline to 8% (80x), p95 went from 220ms to 1.8s (8x), 2 support tickets in 15 min, 20 minutes since deploy — with the timestamp anchors | PASS | Signal table rows: 0.1% → 8.0% (80x), 220ms → 1,800ms (8.2x), customer ticket row '~0 in 15min → 2 in 15min'; verification section references '20 minutes of v3.0.1 deployment' |
| c11 | Output's verification step correlates the spike with the deploy timestamp (20 min ago) and rules out external factors (no upstream provider outage, no traffic spike, no adjacent unrelated deploy) | PASS | 'Correlated with release: Yes — all signals appeared within 20 minutes of v3.0.1 deployment. Timing is conclusive' and 'External factors ruled out: No evidence of third-party outage or traffic anomaly mentioned; assume release-related until proven otherwise' |
| c12 | Output's blast radius quantifies affected requests/customers — e.g. "8% of `/api/invoices` traffic affected; if endpoint runs at X req/min, that's Y failed invoice generations per minute" — and notes the trajectory is growing (2 tickets in 15 min suggests more pending) | PARTIAL | Output states '8.0%' error rate in signal table and trajectory 'Stable or growing — 2 support tickets in 15 minutes is ongoing, not declining', but does not perform req/min math (explicitly acknowledges 'unknown exact percentage' without computing absolute failure volumes) |
| c13 | Output applies the rollback threshold rule explicitly — "error rate >2x baseline for ≥5 min triggers rollback; we have 80x for ≥15 min" — and concludes the threshold is decisively breached | PARTIAL | Signal table and decision reasoning both state threshold is 2x and current is 80x, concluding decisively breached. However, the time-duration component of the rule ('for ≥5 min') is never invoked — the output does not state 'we've had 80x for ≥15 min' or reference the minimum duration requirement |
| c14 | Output recommends ROLLBACK (not forward-fix) and names the four reasons: unknown root cause confidence, wide blast radius, no feature flag toggle, threshold exceeded for >5 minutes | PASS | Decision bullet list covers: 'Error rate threshold exceeded (80x baseline)', 'No feature flags to isolate — big-bang deploy', 'Root cause unclear — would need >15 min investigation', 'Customer impact is active'. All four substantive reasons present; 'Forward-fix is not viable' |
| c15 | Output flags the big-bang deploy as the reason rollback is slower (full redeploy of the previous artefact) — and quantifies the expected rollback duration | PARTIAL | Execution plan states 'Rollback mechanism: Standard deploy redeploy (5–10 minutes)' — duration quantified. Big-bang deploy and no feature flags are noted. However, the output never explicitly frames full redeploy as being *slower than a feature-flag toggle*, which is the comparative framing the criterion requires |
| c16 | Output's root cause hypothesis lists all three changes (invoice refactor, `tax_rate` migration, PDF library upgrade) with a confidence rating and reasoning per — e.g. migration is high suspicion if non-nullable default-0 doesn't match expected per-customer rates; refactor is medium; PDF library is low unless it touches calculation | PARTIAL | All three changes listed in order of likelihood with brief reasoning. However, per-item confidence ratings are absent (only ordinal ranking); the specific migration suspicion about 'default 0 not matching expected per-customer tax rates' is not raised — output only mentions 'assumptions about column presence/state or migration didn't propagate cleanly' |
| c17 | Output's execution plan includes specific steps — initiate redeploy of previous version, decide whether to roll back the migration (and how — `tax_rate` column with default may be safe to leave; the `subscription_events` table is additive so it stays), notify support, watch error rate | PARTIAL | Execution plan covers: redeploy v3.0.0, monitor error rate and latency, notify stakeholders (engineering/support/leadership). Missing: any decision about whether to roll back the DB migration — the `tax_rate` column and its safety to leave in place is not addressed at all |
| c18 | Output's post-rollback verification requires confirming error rate returns to the 0.1% baseline AND p95 returns to ~220ms BEFORE declaring resolution — not just "errors stopped climbing" | PASS | 'Verify resolution (critical — do not skip)' explicitly lists both: 'Error rate back to 0.1%: ✓' and 'Latency back to 220ms: ✓' as required conditions before declaring resolution |
| c19 | Output's post-action steps include a blameless retro to identify why no feature flag was used, why the staging tests didn't catch this, and whether this category of change should have a stricter gate | PARTIAL | Post-Action retro includes 'Should this have had a feature flag or canary?' and 'Add integration tests for invoice calculation + tax_rate column interaction' and 'Use a feature flag or canary for the next attempt'. Coverage of feature flag question and future gate is clear; 'why staging tests didn't catch this' is only partially addressed via migration-specific question rather than a broader staging adequacy question. 'Blameless' framing is not explicit. |

### Notes

The output is comprehensive and well-structured, correctly identifying all signal components, recommending immediate rollback with sound reasoning, and covering most required sections. Its main gaps are: (1) it never invokes the time-duration component of the rollback threshold rule (≥5 min), which the criteria treat as an explicit requirement; (2) the blast radius lacks req/min arithmetic for absolute failure volumes; (3) the migration rollback decision is entirely absent from the execution plan — the output doesn't address whether to roll back the `tax_rate` column; (4) the big-bang vs feature-flag speed contrast is implied but never stated explicitly; and (5) per-item confidence ratings in the root cause section are missing — only ordinal ranking is given. Despite these gaps, the output exceeds the 80% threshold and demonstrates a clear understanding of incident response decision-making.
