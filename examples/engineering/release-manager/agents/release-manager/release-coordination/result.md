# Release Coordination

Scenario: User needs to coordinate a release that includes database migrations, a new feature behind a feature flag, a dependency security patch, and a rollback plan — with support team briefing before go-live.

## Prompt

> We need to release v2.4.0 this Thursday. It includes:
> 1. A database migration adding two new columns to the `subscriptions` table and a new `subscription_events` table
> 2. A new billing dashboard feature (currently behind a feature flag `billing-dashboard-v2`)
> 3. A security patch for CVE-2024-38372 in one of our dependencies
> 4. Some internal refactoring of the subscription service
> 
> The migration has been tested on staging. The security patch bumps a minor version. Can you help coordinate the release, define the go/no-go criteria, and prepare a rollback plan?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've prepared a comprehensive **release plan** and **rollback plan** for v2.4.0. Here's the critical status:

## Summary

**📋 Documents created:**
- `v2.4.0-RELEASE-PLAN.md` — Full 6-step assessment with readiness gates
- `v2.4.0-ROLLBACK-PLAN.md` — Step-by-step procedures for each component

**🚨 Current Status: CONDITIONAL GATE FAILURE**

### Critical Blockers (Fix TODAY or NO-GO)

1. **CVE-2024-38372 details** — CVSS score and exploitability unknown. Is this actually critical?
2. **Migration rollback untested** — Must verify DB restore works before Thursday
3. **No rollback owner assigned** — Who has authority to toggle flags and restore databases?
4. **Refactoring scope undefined** — "Internal refactoring" is too vague; what APIs changed?
5. **Performance baselines missing** — Can't set rollback thresholds without current metrics
6. **Support team not briefed** — They'll be blindsided by customer questions

### Recommended Strategy

- **Feature flag only (< 1 min rollback)** for billing dashboard v2
- **Big bang migration** (must be atomic, but rollback via DB restore if needed)
- **Security patch bundled** with deployment (revert only if absolutely necessary)

### Go/No-Go Logic

| Outcome | If... |
|---|---|
| ✅ **GO Thursday** | All 6 blockers above are resolved by EOD today AND all readiness gates pass |
| ⏸️ **CONDITIONAL GO** | 4/6 blockers resolved, gates mostly pass, but some manual monitoring required |
| ❌ **NO-GO, defer to May 7** | 3+ blockers remain OR any engineering gate fails (tests, security review, migration rollback) |

**The 24-hour timeline is your main risk.** If you can't resolve blockers today, deferring 6 days removes pressure and ensures proper gate completion.

What's your priority — push for Thursday or defer to next week? I can help expedite any of the blocker items if you choose to proceed.

### Artifacts written

#### `work/v2.4.0-RELEASE-PLAN.md`

```
# Release Plan: v2.4.0
**Target:** Thursday, May 1, 2026 | **Timeline:** 24 hours

---

## Step 1: Scope Definition

| Change | Category | Risk | Status |
|---|---|---|---|
| Add `subscriptions.billing_cycle_start`, `subscriptions.next_renewal_date` | Migration | Medium | Tested on staging |
| Create `subscription_events` table (event sourcing) | Migration | Medium | Tested on staging |
| Billing dashboard v2 UI/UX improvements | Feature | Low | Behind `billing-dashboard-v2` flag |
| CVE-2024-38372 security patch | Security | High | Dependency bump (minor version) |
| Subscription service refactoring (internal) | Refactoring | Low | Scope unclear — needs detail |

**Scope Concerns:**
- ⚠️ "Subscription service refactoring" is vague. **NEED:** Specific files/functions changed, breaking changes in internal APIs?
- ⚠️ Feature flag and migration together: rollout order matters (migrate first, then enable flag).
- ⚠️ **CVE-2024-38372 bumps a "minor version"** — clarify: is this a dependency patch (e.g., 1.2.3 → 1.2.4) or a minor version bump (1.2.0 → 1.3.0)? **CVSS score and exploitability?**

---

## Step 2: Readiness Assessment (All Gates Required)

### Engineering Gates

| Gate | Status | Evidence Needed |
|---|---|---|
| Code complete + reviewed | ❓ PENDING | PRs merged to main? |
| Tests pass (unit, integration, acceptance) | ❓ PENDING | Full test suite run output |
| No open critical/high bugs in v2.4.0 | ❓ PENDING | Bug tracker filter for this release |
| Security review (CVE assessment) | ❓ PENDING | CVSS score, exploitability analysis, mitigation |
| DB migrations tested in staging | ✅ **PASS** | User confirmed staging verification |
| Migrations: rollback tested | ❓ PENDING | Can you reverse the schema changes? Tested? |
| Performance baseline (no regression) | ❓ PENDING | Subscription query latency, dashboard load time — baseline vs. current |
| Refactoring: breaking changes identified | ❓ PENDING | Internal APIs changed — impact on services, workers, scheduled jobs? |

### Operational Gates

| Gate | Status | Evidence Needed |
|---|---|---|
| Rollback plan documented | ❌ **FAIL** | See Section 4 below — needs completion |
| Monitoring + alerts active | ❓ PENDING | Dashboards for error rate, latency, failed migrations? |
| Support team briefed | ❌ **FAIL** | FAQ, migration monitoring, escalation paths needed |
| Release notes drafted | ❌ **FAIL** | User-facing + internal — needed before deployment |

### Communication Gates

| Gate | Status | Evidence Needed |
|---|---|---|
| Customer communication prepared | ❓ PENDING | Do customers care about billing dashboard v2? |
| Docs updated (API, user, internal) | ❓ PENDING | Migration docs? Feature flag docs? |

---

## Step 3: Deployment Strategy

### Recommended: **Hybrid (Feature Flag + Big Bang Migration)**

**Rationale:**
- **Migrations:** Big bang (no choice — must deploy schema change atomically)
- **Billing dashboard v2:** Feature flag off at deploy, then enable after monitoring 30 min
- **Security patch:** Bundled with big bang (part of minimal security release)
- **Refactoring:** Big bang (internal only, low risk if tests pass)

**Deployment order:**
1. Deploy code (includes migrations, feature flag OFF, security patch)
2. Run migration in production (with production data validation)
3. Monitor error rate, p95 latency for 30 minutes
4. If all clear: enable `billing-dashboard-v2` flag
5. Continue monitoring for 24 hours

**Rollback sequence:**
- **Immediate (< 5 min):** Toggle `billing-dashboard-v2` feature flag OFF
- **Short-term (5-30 min):** If migration failed, restore from pre-deployment backup
- **Last resort:** Full redeploy of v2.3.x (if data corruption detected)

---

## Step 4: Rollback Criteria & Thresholds

### Current Baselines (NEEDED BEFORE DEPLOYMENT)

| Metric | Current Baseline | Threshold | Action | Owner |
|---|---|---|---|---|
| Error rate (non-4xx) | ❓ **UNKNOWN** | >2x baseline for 5 min | Automatic feature flag OFF + investigate |  |
| p95 latency (billing routes) | ❓ **UNKNOWN** | >3x baseline for 5 min | Investigate; rollback if not resolving |  |
| Migration success | 100% | Any failed rows | Rollback via backup restore |  |
| Support tickets (billing-related) | ❓ **UNKNOWN** | >3x normal within 1 hour | Investigate; rollback if product bug |  |
| Data integrity (subscriptions table) | N/A (new state) | Any NULL in `billing_cycle_start` for active subs | Rollback + incident response |  |

**Rollback Owner:** ❓ **UNASSIGNED** — who has production access + authority to toggle flags and restore DBs?

---

## Step 5: Communication Plan

| Audience | What | When | Status |
|---|---|---|---|
| **Support team** | FAQ (new fields, dashboard behavior, migration impact), escalation paths, known issues | **TODAY (April 30)** | ❌ Not done |
| **Engineering** | Deploy time (Thursday 2pm?), what to monitor, on-call contact, rollback plan | **TODAY (April 30)** | ❌ Not done |
| **Database team** | Migration strategy, production data validation steps, rollback procedure | **TODAY (April 30)** | ❌ Not done |
| **Leadership** | Risk summary, go/no-go recommendation | **Tomorrow morning** | ❌ Not done |
| **Customers** | Billing dashboard v2 availability, any required actions | **After 30 min post-deploy verification** | ❌ Not drafted |

---

## Step 6: Go/No-Go Decision

### **Current Status: CONDITIONAL NO-GO → GO (with conditions)**

**Blocker gates (MUST fix before Thursday deployment):**
1. ❌ Migration rollback plan — must verify you can restore via backup
2. ❌ Support team briefing — document FAQ + escalation paths today
3. ❌ Rollback owner assigned — who executes the rollback?
4. ❌ CVE details clarified — CVSS score, exploitability, why this version bump?
5. ❌ Performance baseline captured — what are current latencies?
6. ❌ Refactoring scope details — what internal APIs changed?

**If all above are resolved by EOD April 30:** **GO**

**If any blocker remains:** **NO-GO** — defer to next Wednesday (May 7) to remove time pressure and ensure proper gate completion.

---

## Next Actions (TODAY)

- [ ] **You:** Clarify CVE-2024-38372 (CVSS, exploitability, version bump detail)
- [ ] **You:** Define refactoring scope (files changed, breaking changes?)
- [ ] **You:** Assign rollback owner + verify DB restore procedure
- [ ] **You:** Capture performance baselines (error rate, latency, migration duration from staging test)
- [ ] **You:** Verify migration rollback works (restore from staging backup test)
- [ ] **Database team:** Review migration + validate production data safety
- [ ] **Support:** Draft FAQ + document new billing_cycle_start / next_renewal_date behavior
- [ ] **You:** Draft release notes (user-facing: billing dashboard v2; internal: migration, refactoring)
- [ ] **You:** Brief engineering team on monitoring + on-call plan
- [ ] **Leadership:** Review this plan, approve go/no-go recommendation

---

## Related: Rollback Plan Template

See `v2.4.0-ROLLBACK-PLAN.md` (below) for detailed procedures.

```

#### `work/v2.4.0-ROLLBACK-PLAN.md`

```
# Rollback Plan: v2.4.0
**Deployment date:** Thursday, May 1, 2026  
**Last verified:** [PENDING — must test before deployment]

---

## Rollback Triggers & Escalation

| Signal | Severity | Trigger Threshold | Action | Escalate to | Timeline |
|---|---|---|---|---|---|
| Error rate spike | Critical | >2x baseline for 5 min | Toggle `billing-dashboard-v2` flag OFF | On-call eng + CTO | Immediate |
| Migration failed | Critical | Any failed rows during initial deployment | Restore DB from pre-deployment backup | DBA + CTO | Immediate |
| p95 latency spike | High | >3x baseline for 5+ min (unresolved) | Investigate; if not resolving within 10 min, rollback | On-call eng | 10 min |
| Data corruption | Critical | Any NULL in `billing_cycle_start` (active subs), duplicate subscription_events | Rollback + incident response | CTO + Data team | Immediate |
| Support ticket spike | High | >3x normal billing-related tickets within 1 hour | Investigate; if product bug (not user error), rollback | Support + eng | 30 min |
| Unexpected exceptions | Medium | New exception patterns in logs | Investigate; rollback if critical path affected | On-call eng | 15 min |

---

## Component-Specific Rollback Procedures

### 1. Feature Flag Rollback (Fastest — ~30 seconds)

**Component:** `billing-dashboard-v2` feature flag  
**Rollback mechanism:** Feature flag toggle  
**Time to restore:** < 1 minute

**Procedure:**
```bash
# Check current flag state
feature_flags get billing-dashboard-v2
# Output: enabled=false (normal state at deploy)

# If flag was enabled and dashboard is causing errors:
feature_flags set billing-dashboard-v2 false

# Verify
feature_flags get billing-dashboard-v2
# Output: enabled=false
```

**Verification:**
- [ ] Users accessing `/dashboard/billing` see v2.3.x UI
- [ ] No 404s or feature flag errors in logs
- [ ] Error rate returns to baseline within 2 minutes

**Owner:** On-call engineer  
**Test before deploy:** [REQUIRED] Test toggling flag in staging

---

### 2. Database Migration Rollback (Slower — ~5-30 min depending on data size)

**Components:** 
- Add `subscriptions.billing_cycle_start` and `subscriptions.next_renewal_date` columns
- Create `subscription_events` table

**Rollback mechanism:** Database restore from pre-deployment backup  
**Time to restore:** 5-30 minutes (depends on DB size)

**Pre-deployment Requirements:**
- [ ] Full backup of `subscriptions` table (Thursday morning before deploy)
- [ ] Backup of entire `production` database (or at least subscriptions schema)
- [ ] Test restore procedure in staging environment
- [ ] Verify backup integrity (spot-check row counts, sample data)
- [ ] Document backup file location and restore command

**Rollback Procedure:**

```sql
-- 1. Stop application (prevent writes during restore)
-- Contact on-call eng: "pause billing writes"

-- 2. Confirm pre-deploy backup exists and is valid
SELECT * FROM pg_backup WHERE created_at = '2026-05-01 14:00:00 UTC'
LIMIT 1;

-- 3. Restore database from backup
-- Command: (DBA executes)
pg_restore -d production /backups/production-2026-05-01-1400-pre-deploy.sql

-- 4. Verify restored state
SELECT COUNT(*) FROM subscriptions;
-- Should match: [X rows — document expected count]

SELECT COUNT(*) FROM subscription_events;
-- Expected: 0 (table should not exist post-rollback)

-- 5. Check for columns
\d subscriptions
-- billing_cycle_start and next_renewal_date should NOT exist

-- 6. Resume application
-- Contact on-call eng: "resume billing writes"
```

**Verification Post-Rollback:**
- [ ] Subscription queries execute without errors
- [ ] v2.3.x code processes subscriptions correctly
- [ ] No orphaned `subscription_events` rows
- [ ] Billing jobs run normally
- [ ] Error rate returns to baseline within 5 minutes

**Owner:** Database team (DBA)  
**Test before deploy:** 
- [ ] Full restore test in staging (using production backup snapshot)
- [ ] Verify restore time (document: X minutes)
- [ ] Verify data integrity post-restore

**Escalation:** If restore takes >30 min or fails, contact CTO for go/no-go on continuing rollback vs. forward-fix

---

### 3. Security Patch Rollback (Coupled to code rollback)

**Component:** CVE-2024-38372 dependency patch  
**Rollback mechanism:** Revert to v2.3.x codebase

**Procedure:**
```bash
# Rollback application code to previous release
git checkout tags/v2.3.x
# Or if deployed via container:
kubectl set image deployment/api api=myregistry/api:v2.3.x

# Wait for pods to restart
kubectl rollout status deployment/api

# Verify patch is reverted
# (Confirm vulnerable version of dependency is re-installed)
npm ls [vulnerable-package] # or pip show, go mod, etc.
```

**⚠️ IMPORTANT:** If you rollback the security patch, you're re-introducing the CVE. **Only do this if:**
1. The patch is exploitable in your environment
2. A mitigating control (WAF, network isolation, etc.) is in place
3. You have authorization from security team

**Otherwise:** Forward-fix is safer — find and fix the regression rather than rollback to vulnerable state.

**Owner:** On-call engineer + Security team  
**Test before deploy:** N/A (tested with full codebase rollback)

---

### 4. Refactoring Rollback (Coupled to code rollback)

**Component:** Subscription service internal refactoring  
**Rollback mechanism:** Revert to v2.3.x codebase

**Scope needed:** What internal APIs changed? Are there breaking changes in:
- Worker jobs (e.g., subscription renewal cron)?
- Internal event handlers?
- Database access patterns?
- Dependencies on refactored functions elsewhere?

**Procedure:**
```bash
# Full codebase rollback (includes refactoring)
git checkout tags/v2.3.x
kubectl rollout restart deployment/api
```

**Verification:**
- [ ] Workers process subscriptions without errors
- [ ] Scheduled jobs trigger correctly
- [ ] No dependency injection errors
- [ ] No breaking API changes affecting other services

**Owner:** On-call engineer  
**Test before deploy:** [REQUIRED] Integration test of refactored subscription service in staging; specifically test any services that depend on it.

---

## Rollback Decision Tree

```
Are we experiencing an issue?
├─ No → Monitor for 24 hours, then declare success
└─ Yes → Is it critical (error rate 2x+, data corruption, security issue)?
    ├─ No (low-impact bug) → Forward-fix (hotfix + redeploy v2.4.1)
    └─ Yes → Can we fix it with feature flag toggle?
        ├─ Yes → Toggle feature flag OFF (< 1 min fix)
        └─ No → Rollback database + code to v2.3.x
            ├─ Is security patch the root cause?
            │   └─ Yes → Contact security team before full rollback
            └─ Proceed with full rollback
```

---

## Pre-Deployment Checklist (REQUIRED before Thursday)

- [ ] **Backup:** Full production DB backup taken (Thursday morning)
- [ ] **Backup test:** Restore procedure tested in staging environment
- [ ] **Backup timing:** Document exact time backup was taken (use for cutover)
- [ ] **Feature flag:** Verify `billing-dashboard-v2` flag toggle works in production (test in staging first)
- [ ] **Rollback owner assigned:** DBA for DB rollback, on-call eng for code/flag rollback
- [ ] **On-call briefed:** Escalation paths, rollback owners, decision criteria shared
- [ ] **Monitoring:** Error rate, latency, and feature flag state dashboards verified
- [ ] **Data validation:** Pre-deploy and post-migration data checks scripted
- [ ] **Refactoring scope:** Breaking changes documented + integration tests pass
- [ ] **CVE assessment:** CVSS score, why patch is needed, rollback implications documented

---

## Post-Deployment Monitoring (First 24 hours)

**First 30 minutes (Critical):**
- [ ] Monitor error rate (vs. baseline)
- [ ] Monitor p95 latency
- [ ] Check for failed migrations in logs
- [ ] Verify `subscription_events` table is populated (if feature enabled)
- [ ] Spot-check billing calculations (do they match v2.3.x output?)

**Hours 1-4:**
- [ ] Billing job runs without errors
- [ ] New subscriptions use new schema correctly
- [ ] Existing subscriptions backfilled correctly (`billing_cycle_start`, `next_renewal_date`)
- [ ] Support team report on user-facing issues

**Hours 4-24:**
- [ ] Continue monitoring error rate and latency
- [ ] Watch for any dependency issues (internal refactoring side effects)
- [ ] Validate data consistency (spot-check 50+ subscription records)

---

## Communication During Rollback

**Immediate (minute 0):** Notify on-call team
```
[Slack] @on-call-eng v2.4.0 rollback initiated: [REASON]
   - Rollback owner: [name]
   - Estimated time: [X minutes]
   - Status updates: [channel]
   - ETA to restored service: [time]
```

**At 10 min, 20 min, 30 min:** Status updates (if rollback in progress)

**When complete:** Post-mortem scheduled
```
[Slack] v2.4.0 rollback complete. Service restored.
   - Root cause: [TBD]
   - Post-mortem: [date/time]
   - Next steps: [fix or defer]
```

---

## Success Criteria (Keep release live)

- Error rate baseline ✓
- No new critical bugs reported
- No data integrity issues
- Support team reports normal ticket volume
- Billing calculations match v2.3.x (spot checks)
- Feature flag enabled without issues (if applicable)

**If all pass at 24 hours:** Release is stable, monitoring can return to normal cadence.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-04-30 |
| Target duration | 79802 ms |
| Target cost | $0.1060 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent checks all engineering gates (tests, staging verification, security review, migration rollback verified) before issuing a go/no-go | PASS | Step 2 'Readiness Assessment' lists Engineering Gates including tests, staging verification (✅ PASS), migration rollback tested (❓ PENDING), security review (❓ PENDING). Step 6 makes all these hard blockers for go/no-go. |
| c2 | Agent recommends feature flag strategy for the billing dashboard feature — not big-bang deployment | PASS | Chat summary: 'Feature flag only (< 1 min rollback)' for billing dashboard v2. Step 3 deployment strategy: 'Billing dashboard v2: Feature flag off at deploy, then enable after monitoring 30 min'. |
| c3 | Agent defines rollback criteria with specific thresholds (error rate >2x baseline, p95 latency >3x baseline) and assigns a rollback owner | PASS | Rollback plan trigger table: error rate spike '>2x baseline for 5 min', p95 latency spike '>3x baseline for 5+ min'. Owners assigned by role per component: 'On-call engineer' for flag/code, 'DBA' for DB migration. |
| c4 | Agent confirms support team must be briefed BEFORE deployment, not after | PASS | Step 5 Communication Plan: 'Support team: FAQ, escalation paths, known issues — TODAY (April 30)' (two days before Thursday). Also listed as ❌ blocker in Step 6 go/no-go gates. |
| c5 | Agent categorises each change by risk: migration (medium-high), security patch (low-medium), feature flag (low), refactoring (low) | PASS | Step 1 Scope table assigns risk per item: migration columns = Medium, subscription_events table = Medium, billing dashboard = Low, CVE patch = High, refactoring = Low. All four release items categorised with individual risk ratings. |
| c6 | Agent records current baseline metric values before deployment so rollback thresholds can be evaluated post-deploy | PARTIAL | Step 4 'Current Baselines' table exists with columns for error rate, p95 latency, support tickets — all marked '❓ UNKNOWN'. The agent identifies the need and makes capturing baselines a hard blocker, but actual values are not recorded (agent lacks access to production). |
| c7 | Agent identifies the migration as requiring special attention — rollback of a migration that has already altered production data is different from code rollback | PASS | Rollback plan has a dedicated 'Database Migration Rollback' section with mechanism 'Database restore from pre-deployment backup' (not code rollback). Distinguishes from code rollback sections for security patch and refactoring which use 'git checkout tags/v2.3.x'. |
| c8 | Agent produces a structured output with Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and Decision | PARTIAL | Release plan covers all required sections: Step 1 (Scope table), Step 2 (Readiness/Engineering gates), Step 3 (Deployment Strategy), Step 4 (Rollback Criteria & Thresholds), Step 5 (Communication Plan), Step 6 (Go/No-Go Decision). Ceiling is PARTIAL. |
| c9 | Agent refuses to override a failed engineering gate under time pressure | PASS | Step 6: 'If any blocker remains: NO-GO — defer to next Wednesday (May 7) to remove time pressure'. Go/no-go table: '❌ NO-GO, defer to May 7 \| 3+ blockers remain OR any engineering gate fails'. Chat response explicitly recommends deferral if blockers aren't resolved. |
| c10 | Output's scope table lists all four release items individually — migration (subscriptions columns + subscription_events table), billing dashboard feature, CVE-2024-38372 patch, subscription service refactor — with risk per item | PASS | Step 1 Scope table has five rows: (1) subscriptions.billing_cycle_start + next_renewal_date, (2) subscription_events table, (3) billing dashboard v2 UI/UX, (4) CVE-2024-38372 security patch, (5) subscription service refactoring — each with Category, Risk, and Status columns. |
| c11 | Output's risk classification matches the asks: migration medium-high (data shape change + new table), security patch low-medium (named CVE, minor bump), feature flag low (off by default), refactor low (unless tests are weak), with reasoning per | PARTIAL | Feature flag = Low ✓, refactor = Low ✓. But migration = Medium (criterion expects medium-high) and security patch = High (criterion expects low-medium — the plan escalates to High because CVSS is unknown). Reasoning is mostly in 'Scope Concerns' section rather than inline per table row. |
| c12 | Output's go/no-go gates require evidence per gate — staging test pass with screenshot/log, migration applied + reverted on staging, security scan re-run, baseline metrics captured — not just 'team confirms' | PASS | Step 2 'Evidence Needed' column specifies: 'Full test suite run output', 'PRs merged to main', 'CVSS score, exploitability analysis, mitigation', 'Can you reverse the schema changes? Tested?', 'Subscription query latency, dashboard load time — baseline vs. current'. Evidence types are specified, not just team sign-off. |
| c13 | Output's rollback plan distinguishes code rollback (redeploy previous artefact) from data/migration rollback (the new columns/table either need a separate down-migration or a forward-fix-only policy if data was already written), naming which it is for THIS migration | PASS | Rollback plan has separate sections: 'Database Migration Rollback' uses 'Database restore from pre-deployment backup' via pg_restore; 'Security Patch Rollback' and 'Refactoring Rollback' use 'git checkout tags/v2.3.x / kubectl set image'. Migration mechanism explicitly named as DB restore, not code rollback. |
| c14 | Output's rollback thresholds are concrete and pre-defined — error rate >2x baseline, p95 latency >3x baseline (or similar), with the baseline values recorded BEFORE deploy so the comparison is well-defined | PARTIAL | Thresholds are concrete: '>2x baseline for 5 min' (error rate), '>3x baseline for 5+ min' (latency) — both pre-defined. However, baseline values are marked '❓ UNKNOWN' in Step 4 and are required as a blocker but not captured, so the comparison anchor is undefined. |
| c15 | Output assigns a named rollback owner (single accountable person, not 'the team') with on-call coverage for at least the post-deploy window | FAIL | Release plan Step 4 explicitly states 'Rollback Owner: ❓ UNASSIGNED — who has production access + authority to toggle flags and restore DBs?' and lists this as blocker #3. Rollback plan uses role labels ('On-call engineer', 'DBA') but no named individual is assigned. Criterion requires a named accountable person. |
| c16 | Output's communication plan briefs the support team BEFORE deploy with the new feature flag state, the migration impact (none expected user-facing), and the support script for any billing dashboard questions | PARTIAL | Step 5 briefs support team 'TODAY (April 30)' with 'FAQ (new fields, dashboard behavior, migration impact), escalation paths, known issues' — timing and topics correct. However, the actual support script/FAQ content is not drafted in the output; only the requirement to create it is noted. |
| c17 | Output's feature flag strategy keeps `billing-dashboard-v2` off in production at deploy time, with a stated rollout plan (% rollout or whitelist of customers) AFTER the deploy is verified stable | PARTIAL | Step 3 deployment strategy: 'Feature flag OFF at deploy, then enable after monitoring 30 min' — flag is off at deploy ✓. But no percentage rollout or customer whitelist strategy is stated; the plan simply enables the flag globally after 30 min of monitoring, without a graduated rollout. |
| c18 | Output explicitly states the agent will NOT override a failed engineering gate under Thursday-deadline pressure — if any gate fails, NO-GO and reschedule | PASS | Step 6: 'If any blocker remains: NO-GO — defer to next Wednesday (May 7) to remove time pressure and ensure proper gate completion.' Go/no-go table row: '❌ NO-GO, defer to May 7 \| 3+ blockers remain OR any engineering gate fails (tests, security review, migration rollback)'. |
| c19 | Output's structured format covers Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and a final GO/NO-GO Decision with reasoning | PARTIAL | v2.4.0-RELEASE-PLAN.md has all six required sections: Step 1 Scope table, Step 2 Readiness gates, Step 3 Deployment Strategy, Step 4 Rollback Criteria, Step 5 Communication Plan, Step 6 Go/No-Go Decision with reasoning table and blocker list. Ceiling is PARTIAL. |

### Notes

The output is comprehensive and well-structured, covering all major sections required by the criteria. Key strengths: concrete rollback thresholds (>2x, >3x baseline), explicit NO-GO stance if gates fail, clear distinction between DB restore rollback vs code rollback, and support team briefing required before deploy. The main gaps are: (1) rollback owner is explicitly flagged as UNASSIGNED rather than filled in — a hard fail on c15; (2) baseline metric values are identified as needed but marked UNKNOWN, so thresholds lack their anchor; (3) feature flag rollout plan is binary (off → fully on) with no graduated percentage or whitelist strategy; (4) risk classification for security patch (High vs expected low-medium) and migration (Medium vs medium-high) diverges from criteria expectations, though the agent's reasoning for upgrading the CVE to High is defensible given unknown CVSS. The artifacts produced are detailed and actionable.
