---
name: rollback-assessment
description: Assess whether to rollback a release — evaluate signals, severity, blast radius, and recommend rollback vs forward-fix.
argument-hint: "[release version or incident to assess]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Assess rollback for $ARGUMENTS.

## Rollback Assessment Process (7 steps — sequential, do not skip)

The cardinal rule: **decide fast, act faster.** Every minute spent deliberating is a minute users are affected. When in doubt, roll back. You can always re-deploy — you cannot un-corrupt data or un-lose trust.

### Step 1: Identify the Signal

What triggered this assessment? Classify the signal:

| Signal type | Examples | Urgency |
|---|---|---|
| **Error rate spike** | 5xx responses, exception rate, failed transactions | High — users are failing |
| **Latency degradation** | p95/p99 increase, timeout rate increase | High — users are waiting |
| **Support ticket spike** | Customer reports, bug reports, confusion reports | Medium — users are struggling |
| **Health check failure** | Endpoint returning non-200, service unreachable | Critical — service is down |
| **Data integrity issue** | Wrong data returned, data loss, corruption signals | Critical — damage accumulating |

**Rules:**
- Record the exact signal: metric name, current value, normal baseline, when it started
- Multiple signals compound urgency — if you see error rate AND latency, treat as the higher urgency
- Data integrity signals always warrant immediate rollback consideration. Do not investigate first

### Step 2: Verify the Signal

Before acting, confirm the signal is real and release-related:

1. **Not a false positive** — is the monitoring system healthy? Are other metrics consistent? Check from multiple vantage points
2. **Not pre-existing** — was this metric elevated BEFORE the deployment? Compare with the pre-deployment baseline recorded in the release plan
3. **Correlated with the release** — does the timing align?
   ```bash
   git log --oneline -5
   ```
   Check: did the signal start within minutes of the deployment completing? Or hours later (less likely to be release-related)?
4. **Not caused by external factors** — is there a third-party outage, traffic spike from a marketing campaign, or infrastructure event unrelated to the release?

**Rules:**
- Verification should take no more than 5 minutes for critical signals. If you cannot verify in 5 minutes, assume it is real and proceed
- A signal you cannot explain is still a signal. Do not dismiss it because you cannot find the cause
- For data integrity signals, skip verification and proceed directly to Step 5. The cost of delay exceeds the cost of an unnecessary rollback

### Step 3: Assess Blast Radius

Determine the scope of impact:

1. **Users affected** — all users, a segment (region, plan tier, feature flag group), or isolated cases?
2. **Features affected** — one feature, multiple features, or core functionality?
3. **Trajectory** — is the impact stable, growing, or shrinking?
   - Growing blast radius = escalate urgency. The problem is spreading
   - Stable blast radius = you have time to assess, but do not delay
   - Shrinking blast radius = may be self-resolving, but verify before standing down

4. **Downstream effects** — are other services or teams affected? Is this cascading?

**Rules:**
- Growing blast radius with unknown cause = rollback immediately. Do not wait for root cause
- Even a small blast radius matters if it affects data integrity or financial transactions
- Quantify the impact: "approximately 15% of requests failing" is actionable. "Some users are affected" is not

### Step 4: Hypothesise Root Cause

Identify what in this release likely caused the issue:

1. **Review the release scope** — what PRs and changes were included?
   ```bash
   git log --oneline <previous-release-tag>..HEAD
   ```
2. **Correlate with the signal** — which change most plausibly explains the symptom?
   - Database migration = data integrity or latency issues
   - API change = error rate spike from clients sending old format
   - Config change = service behaviour change
   - Dependency update = unexpected behaviour from third-party code
3. **Check the diff** for the suspected change — look for obvious issues (missing error handling, wrong query, bad default)
4. **Rate your confidence** — high (found the specific line), medium (found the likely area), low (no clear candidate)

**Rules:**
- Low confidence in root cause is a strong signal to rollback rather than forward-fix
- Do not spend more than 10 minutes on root cause analysis during an active issue. If you have not found it, roll back
- A root cause hypothesis is not required to make a rollback decision. "Unknown cause, rolling back to restore service" is a valid and responsible decision

### Step 5: Decide — Rollback vs Forward-Fix

Apply the rollback criteria from the release plan:

| Signal | Threshold | Decision |
|---|---|---|
| Error rate | >2x baseline for 5 minutes | **Rollback** |
| p95 latency | >3x baseline for 5 minutes | **Rollback** if not resolving |
| Support ticket spike | >3x normal rate within 1 hour | **Rollback** if product-related |
| Health check failures | Any health endpoint returning non-200 | **Rollback** immediately |
| Data integrity | Any data corruption signal | **Rollback** immediately + incident response |

**Rollback when:**
- Any threshold in the table above is exceeded
- Data integrity is at risk (no threshold — any signal is enough)
- Blast radius is wide and growing
- Root cause is unknown or unclear
- The fix would take longer than 15 minutes to ship with confidence

**Forward-fix when (ALL must be true):**
- The issue is isolated to a specific, well-understood area
- Root cause is identified with high confidence
- The fix is small, obvious, and low-risk
- The fix can be shipped within 15 minutes including testing
- Rollback would cause more disruption than the fix (e.g., rolling back a migration that has already been applied to production data)

**When in doubt, roll back.** A rollback that was unnecessary costs you a re-deployment. A forward-fix that fails costs you an extended outage.

### Step 6: Execute the Decision

**If rolling back:**

1. **Select mechanism** based on what was used to deploy:

   | Deployment method | Rollback mechanism | Speed |
   |---|---|---|
   | Feature flag | Toggle flag off | Seconds |
   | Percentage rollout | Reduce to 0% | Seconds |
   | Blue/green | Switch traffic to previous environment | 1-2 minutes |
   | Canary | Redirect all traffic to stable | 1-2 minutes |
   | Standard deploy | Redeploy previous version | 5-10 minutes |

2. **Execute the rollback** — use the mechanism documented in the release plan
3. **Verify resolution** — confirm the signal that triggered the assessment has returned to baseline
4. **Notify stakeholders** — engineering, support, and anyone who was notified of the original release

**If forward-fixing:**

1. **Scope the fix** — minimal change, addresses only the identified issue
2. **Abbreviated testing** — unit tests + targeted integration test for the affected area
3. **Code review** — at least one reviewer, focused on the specific fix
4. **Deploy with enhanced monitoring** — watch the same signals that triggered this assessment for 30 minutes
5. **Have rollback ready** — if the forward-fix does not resolve the issue within 15 minutes of deployment, rollback

### Step 7: Post-Action

After the situation is resolved:

1. **Verify resolution** — confirm ALL signals have returned to baseline, not just the primary one
2. **Communicate status:**
   - Engineering: what happened, what was done, current state
   - Support: whether customers were affected, what to tell them
   - Leadership: summary for SEV-1/SEV-2 incidents
3. **Schedule retrospective** — within 48 hours while context is fresh. Every rollback gets a retrospective to understand what gates missed the issue
4. **Update the release plan** — document what happened and what was learned for the next attempt

## Anti-Patterns (NEVER do these)

- **Rolling back without verifying the signal** — a false positive rollback wastes time and erodes confidence in the process. Spend 5 minutes verifying (unless data integrity is at risk)
- **Forward-fixing when root cause is unknown** — you are guessing. If the fix does not work, you have extended the outage and now need to rollback anyway
- **Rolling back without notifying stakeholders** — support needs to know, engineering needs to know, and if customers were told about the release, they need to know
- **No post-rollback verification** — you rolled back, but did the signal actually improve? Verify before declaring resolution
- **Spending too long on root cause during an active issue** — 10 minutes maximum. If you have not found it, roll back and investigate after service is restored
- **Treating rollback as failure** — rollback is a success of the process. The release plan included a rollback plan for exactly this reason

## Output

Deliver a rollback assessment in this format:

```markdown
## Rollback Assessment: [release version/name]

### Signal
| Signal | Baseline | Current | Threshold | Exceeded? |
|---|---|---|---|---|
| [metric] | [normal value] | [current value] | [threshold] | YES/NO |

### Verification
- False positive ruled out: [yes/no — how]
- Correlated with release: [yes/no — timing evidence]
- External factors ruled out: [yes/no — what was checked]

### Blast Radius
- Users affected: [number/percentage]
- Features affected: [which]
- Trajectory: [growing / stable / shrinking]

### Root Cause Hypothesis
- Suspected cause: [specific PR, change, or "unknown"]
- Confidence: [high / medium / low]

### Decision: [ROLLBACK / FORWARD-FIX]
Reasoning: [why, citing criteria]

### Execution Plan
1. [Step 1]
2. [Step 2]
3. [Verification step]
4. [Communication step]

### Post-Action
- Retrospective scheduled: [date/time]
- Stakeholders notified: [list]
```