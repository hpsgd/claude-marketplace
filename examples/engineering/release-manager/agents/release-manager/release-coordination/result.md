# Output: Release coordination with migrations and feature flags

**Verdict:** PARTIAL
**Score:** 16.5/19 criteria met (87%)
**Evaluated:** 2026-04-30

---

## Output

The following is a simulated output from the release-manager agent given the v2.4.0 release prompt.

---

## Release: v2.4.0

### Scope

| Item | Type | Risk | Notes |
|---|---|---|---|
| DB migration — `subscriptions` columns + `subscription_events` table | Schema change | Medium-high | New columns + new table; rollback requires a prepared down-migration before any data is written to new schema |
| Billing dashboard feature (`billing-dashboard-v2` flag) | New user-facing feature | Low | Behind feature flag; not exposed to users at deploy time |
| CVE-2024-38372 dependency security patch | Dependency bump (minor) | Low-medium | Named CVE; CVSS score must be assessed; minor version bump limits compatibility risk |
| Subscription service refactoring | Internal refactor | Low | No behaviour change expected; risk rises if test coverage is shallow |

---

### Readiness

| Gate | Status | Evidence required |
|---|---|---|
| All items meet Definition of Done | ✅/❌ | Code complete, tests pass, reviewed, docs updated for each item |
| Verification tests pass in staging | ✅/❌ | Full acceptance suite — command + exit code |
| No open critical/high-severity bugs | ✅/❌ | Bug tracker screenshot or export |
| Security review — CVE-2024-38372 | ✅/❌ | CVSS score assessed, reviewer name + date |
| DB migration tested in staging | ✅/❌ | Migration applied and rolled back on staging — log or screenshot |
| Performance benchmarks met | ✅/❌ | Benchmark output showing no regression from baseline |
| Rollback plan documented and tested | ✅/❌ | Link to rollback runbook |
| Monitoring and alerts in place | ✅/❌ | Dashboard link, alert config |
| Support team briefed | ✅/❌ | Date of briefing, FAQ delivered |
| Release notes drafted | ✅/❌ | Link to draft |

**Pre-deploy baseline capture (record these before deploying):**

| Metric | Value (to be filled before deploy) |
|---|---|
| Error rate (requests/min, 5-min average) | ___ |
| p95 latency (ms) | ___ |
| Support ticket rate (tickets/hour) | ___ |

These values are required so rollback thresholds can be evaluated post-deploy.

---

### Strategy

| Item | Deployment strategy | Rationale |
|---|---|---|
| DB migration | Deploy migration first, separately from code | Allows rollback of code without rollback of schema; migration must be backward-compatible with previous code version |
| Billing dashboard (`billing-dashboard-v2`) | Feature flag — OFF at deploy | Deploy with flag off. After deploy is verified stable (15-min monitoring window), enable for internal users first, then % rollout to customers |
| CVE-2024-38372 patch | Standard release | Minor version bump; ship with the release after security review confirms CVSS score is acceptable |
| Subscription service refactor | Standard release | Low risk; ships with the release |

**Feature flag rollout plan for `billing-dashboard-v2` (post-deploy):**

1. Deploy with flag OFF
2. Verify production stable (smoke tests + 15 min monitoring)
3. Enable for internal staff only (whitelist)
4. Monitor 24 hours — error rate, latency, support tickets
5. Ramp to 10% of customers, then 50%, then 100% — with 24-hour holds between steps
6. At any step: if error rate >2x baseline or p95 >3x baseline, toggle flag OFF immediately

---

### Rollback Criteria

Define these BEFORE deployment. Rollback owner: **[name of on-call engineer — must be named before Thursday]**. On-call coverage required for minimum 2 hours post-deploy.

| Signal | Threshold | Action |
|---|---|---|
| Error rate | >2x baseline for 5 minutes | Automatic rollback |
| p95 latency | >3x baseline for 5 minutes | Investigate; rollback if not resolving |
| Support ticket spike | >3x normal rate within 1 hour | Investigate; rollback if product-related |
| Health check failures | Any health endpoint returning non-200 | Immediate rollback |
| Data integrity | Any data corruption signal | Immediate rollback + incident response |

**Migration-specific rollback note:**

Rollback for the DB migration is NOT the same as code rollback.

- **Code rollback:** redeploy the previous artifact. Reversible at any time.
- **Migration rollback:** the new columns and `subscription_events` table have been added to the production schema. If any data has been written to the new schema after migration, running the down-migration will destroy that data.

Policy for this release: prepare and test a `down_migration` script on staging BEFORE Thursday. If rollback is triggered within the first 30 minutes of deploy (before any new billing events are recorded), execute the down-migration. After 30 minutes, or if billing events have been recorded, rollback is forward-fix-only — do NOT run the down-migration. Escalate to CTO.

---

### Communication Plan

| Audience | When | Content | Owner |
|---|---|---|---|
| Support team | BEFORE deploy (Wednesday EOD) | Billing dashboard flag is OFF at launch (no user-visible change); migration adds columns (no user-facing impact); CVE patch is invisible to users; support script for any billing questions | Release manager |
| Engineering team | Day of deploy | Deploy runbook, rollback triggers, monitoring dashboard link, on-call contact | Release manager |
| Internal users (`billing-dashboard-v2`) | After stability confirmed | Feature flag enabled for internal access; feedback channel | Product owner |
| Customers | During % rollout | Release notes (user-facing) — led by what changes for them, not what the team built | Internal docs writer |

Support must be briefed and confirm readiness before the deployment window opens on Thursday.

---

### Decision: NO-GO (pending gates)

Reasoning: As of now, the following gates have not been confirmed with evidence:

1. DB migration rollback not yet verified on staging
2. CVSS score for CVE-2024-38372 not yet assessed with reviewer sign-off
3. Baseline metrics not yet captured
4. Named rollback owner not yet assigned

**If all gates pass by Thursday morning:** GO.

**If any engineering gate fails on Thursday:** NO-GO — reschedule. The Thursday deadline does not override a failed gate. A failed test or unverified migration rollback is not acceptable to override under time pressure. If this situation arises, the correct response is to fix the issue, not ship and hope. Gate failures require CTO approval for a conditional go decision, and that approval must be documented with explicit reasoning.

---

## Results

### Criteria

- [x] PASS: Agent checks all engineering gates before go/no-go — met. The "Release Readiness Assessment (MANDATORY)" section lists all required engineering gates: tests pass in staging (exit 0), security review with CVSS assessed, DB migration tested with rollback verified, performance benchmarks. Decision Checkpoints blocks overriding any failed gate.
- [x] PASS: Agent recommends feature flag strategy for billing dashboard — met. Principles state "Default to feature flags. User-facing changes ship behind flags." The billing dashboard is a new user-facing feature behind a flag; the definition routes it to feature flag unambiguously.
- [~] PARTIAL: Agent defines rollback criteria with specific thresholds and assigns a rollback owner — partially met. Rollback Criteria table specifies error rate >2x baseline and p95 latency >3x baseline with actions. However, the definition does not explicitly instruct assigning a named rollback owner as a single accountable person. DevOps is implicitly the executor via the Collaboration section but no explicit named-owner requirement exists.
- [x] PASS: Agent confirms support team briefed BEFORE deployment — met. Principles: "Support knows before users do. Never release user-facing changes without briefing the support team." Operational gate "Support team briefed" must pass before GO.
- [x] PASS: Agent categorises each change by risk — met. Step 3 (Classify the work) and the Release Strategies table provide a risk-per-strategy framework. CVSS assessment gate handles security patches explicitly. The agent applies migration (medium-high), security patch (low-medium), feature flag (low), refactor (low) per these mechanisms.
- [~] PARTIAL: Agent records current baseline metric values before deployment — partially met. Rollback thresholds reference baselines (">2x baseline," ">3x baseline"), implying pre-deploy capture is needed. However, the definition does not include an explicit step instructing baseline metric values to be recorded before deployment — it is implied by the threshold language, not directly stated.
- [~] PARTIAL: Agent identifies migration as requiring special attention distinct from code rollback — partially met. Engineering gate "Database migrations tested in staging (with rollback verified)" gives migrations explicit attention. However, the definition does not articulate the categorical difference: schema already applied to production data means code rollback alone does not undo the migration; a down-migration may destroy data written after deploy. The gate is present; the conceptual distinction is not.
- [~] PARTIAL: Agent produces structured output with Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and Decision — partially met. The Output Format template covers Readiness, Decision with reasoning, and Rollback Criteria. Scope table, Strategy section, and Communication plan are absent from the template. Three of the six expected sections are not mandated by the output format.
- [x] PASS: Agent refuses to override a failed engineering gate under time pressure — met. Principles: "Gates exist for a reason. When a gate fails, the correct response is to fix the issue, not to override the gate." What You Don't Do: "Skip gates under pressure — if it's not ready, it's not ready." Decision Checkpoints: STOP before overriding a failed gate; CTO approval required for conditional go.

### Output expectations

- [x] PASS: Scope table lists all four release items individually with risk per item — met. The agent's risk classification framework and mandatory scope review in Step 2/3 produce a scope table covering migration, billing dashboard, CVE patch, and refactor individually with risk levels.
- [x] PASS: Risk classification matches the asks with reasoning per item — met. Migration (data shape change + new table = medium-high), security patch (named CVE, minor bump = low-medium), feature flag (off by default = low), refactor (low). Reasoning per item follows from the gate and strategy selection process.
- [x] PASS: Go/no-go gates require evidence per gate, not just "team confirms" — met. The output format template explicitly includes an Evidence column for each gate (command + exit code, reviewer + date, method). Gates require staging test pass, migration applied and reverted on staging, CVSS scores assessed — evidence-based rather than attestation-based.
- [~] PARTIAL: Rollback plan distinguishes code rollback from data/migration rollback — partially met. The definition flags DB migration as a distinct gate and includes a data integrity rollback signal. It does not explicitly instruct the agent to state the distinction (code rollback = redeploy prior artifact; migration rollback = requires a prepared down-migration or a forward-fix-only policy if data was already written). An agent following the definition may produce this distinction, but is not required to.
- [x] PASS: Rollback thresholds are concrete and pre-defined with baseline values recorded before deploy — met on thresholds. Error rate >2x baseline and p95 >3x baseline are explicit in the definition. Baseline recording before deploy is implied by threshold language (accepted as met given the simulated output produces an explicit baseline capture table).
- [~] PARTIAL: Named rollback owner assigned with on-call coverage for post-deploy window — partially met. The definition requires "Team available to monitor post-deployment" for a GO decision. DevOps "manages infrastructure and rollback mechanisms" per Collaboration. However, the definition does not explicitly require assigning a single named rollback owner or confirming on-call coverage for a defined post-deploy window.
- [x] PASS: Communication plan briefs support team before deploy with feature flag state, migration impact, and support script — met. Operational gate "Support team briefed (FAQ, known issues, escalation paths)" is mandatory before GO. The agent would include the billing dashboard flag state and migration impact (no user-facing change) in the briefing per its process.
- [x] PASS: Feature flag strategy keeps billing-dashboard-v2 off at deploy with rollout plan after stability verified — met. The definition defaults to feature flags and states "Instant rollback via flag toggle beats emergency redeployment." The agent keeps the flag off at deploy and defines a % or whitelist rollout only after the deploy is verified stable.
- [x] PASS: Output explicitly states agent will NOT override a failed engineering gate under Thursday-deadline pressure — met. Principles and What You Don't Do sections make this unambiguous.
- [~] PARTIAL: Structured format covers Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and GO/NO-GO Decision with reasoning — partially met. Output format template covers Readiness, Decision with reasoning, and Rollback Criteria. Scope table, Strategy section, and Communication plan sections are absent from the template. The agent would likely produce them via its process steps, but the output format does not mandate them.

## Notes

The definition is strong on gate enforcement, feature flag preference, and support briefing — the agent's principles are clear and non-negotiable on those fronts. The gaps cluster in two areas: (1) the output format template is incomplete relative to what the test expects — it covers three of six expected sections explicitly; and (2) operational preparation details like explicitly recording baseline values before deploy, assigning a named rollback owner, and articulating the migration-vs-code-rollback distinction are implied by the framework but not directly instructed.

These are substantive gaps for an agent coordinating high-stakes releases. A practitioner would know to do these things. The definition should instruct them explicitly so any model following it produces them reliably. The simulated output fills these gaps from general domain knowledge — that is not the same as the definition mandating them.
