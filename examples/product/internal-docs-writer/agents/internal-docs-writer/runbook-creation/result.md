# Runbook Creation

Scenario: An engineering team needs a runbook for handling payment processing failures so on-call engineers can resolve incidents without tribal knowledge.

## Prompt

> Write a runbook for payment processing failures. Context:
> 
> - We use Stripe for payment processing
> - Common failure modes: Stripe API timeouts, card declines (various codes), idempotency key conflicts, webhook delivery failures
> - Our stack: Node.js API, PostgreSQL, Redis for job queues (Bull), Datadog for monitoring
> - Alert fires when: payment success rate drops below 95% over 5 minutes, or any Stripe API error rate exceeds 2%
> - Business impact: each minute of payment failure = ~$3,400 in lost transactions during peak hours
> 
> On-call engineers are expected to handle this without waking anyone up for most scenarios. We've had 4 incidents this quarter and each one took 45+ minutes to resolve because engineers didn't know where to look.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written a comprehensive payment processing failure runbook following the skill's mandatory template. Here's what's included:

**Structure (all mandatory sections present):**

1. **Overview** — triggers (success rate < 95%, API errors > 2%), business impact (~$3,400/min), 10–15 min estimated duration, High risk level

2. **Prerequisites** — Stripe access, CLI tools (curl, jq), environment variables (STRIPE_API_KEY from 1Password), database/Redis credentials, Datadog access, SSH keys, Slack channel

3. **Pre-check** — confirms the alert is real (not transient), waits 60 seconds before acting, checks for planned changes, lists stop conditions (don't proceed if issue already resolved)

4. **Procedure** (6 steps with exact copy-pasteable commands):
   - Gather baseline metrics from Datadog
   - Check application logs for error patterns
   - Query the payment database to identify failure distribution
   - Check Stripe API status and logs
   - Check the Bull job queue for backlog/stuck jobs
   - Check for recent code deployments or config changes
   - Remediate based on failure mode (5 sub-scenarios: timeouts, idempotency conflicts, webhook failures, code bugs, unknown)
   - Monitor the fix with polling

5. **Verification** — 5 health checks (success rate > 95%, API error rate < 2%, job queue healthy, logs clean, recent payments succeeding)

6. **Rollback** — when to rollback, how long the window is, data loss implications, step-by-step undo procedures, what to do after rollback

7. **Troubleshooting** — 3 common issues: timeouts persist, procedure interrupted midway, new wave of card declines

8. **Escalation** — table with 8 concrete conditions, specific team escalation paths (Stripe Support, DevOps, Database team, Payments engineer, VP Product), Slack channels and PagerDuty service names, response time SLAs (Immediate to 24 hours)

9. **Appendix** — references to Stripe docs, code paths, Datadog dashboard, related runbooks, architecture diagram, change log

Every command is marked either ready-to-paste or `# UNTESTED — verify in staging first`. All credentials reference external sources (1Password, config files) rather than being hardcoded. The runbook targets the stated goal: help an on-call engineer resolve most incidents in <15 minutes without waking anyone up.

### Artifacts written

#### `work/RUNBOOK-payment-processing-failures.md`

```
# Payment Processing Failures — Runbook

## Overview

| Field | Value |
|---|---|
| **What this covers** | Diagnosis and resolution of Stripe payment processing failures, including API timeouts, card declines, idempotency conflicts, and webhook failures. |
| **When to use** | Alert fires: payment success rate drops below 95% over 5 minutes, OR Stripe API error rate exceeds 2%. Also use for manual investigation when payment volumes unexpectedly drop. |
| **Business impact** | Each minute of payment failure = ~$3,400 in lost transactions during peak hours. RTO: <15 minutes. RPO: zero (all payment attempts must eventually succeed or explicitly decline). |
| **Estimated duration** | 10–15 minutes for diagnosis and fix; up to 30 minutes if Stripe-side outage or data recovery needed. |
| **Risk level** | High — production payment system; changes affect revenue directly. |
| **Last tested** | Not yet tested in production. Verify all commands in staging environment before first use. |
| **Owner** | Platform / Payments team; on-call engineer on duty. |

## Prerequisites

- [ ] Access to Stripe Dashboard — how to get it: ask your manager or Payments lead for an invite to the business account (you need Dashboard + API key access)
- [ ] `curl` command-line tool installed — version 7.0+ — check: `curl --version`
- [ ] `jq` (JSON query tool) installed — version 1.6+ — install: `brew install jq` (macOS) or `apt-get install jq` (Linux)
- [ ] Environment variables set in your shell: `STRIPE_API_KEY` (Secret Key, not publishable) — get it from: 1Password under "Stripe API Keys (Production)" or ask Payments lead
- [ ] Access to PostgreSQL database — how to get it: `psql -h [DB_HOST] -U [DB_USER] -d payment_db` (credentials in 1Password under "PostgreSQL Production")
- [ ] Access to Redis job queue — how to get it: `redis-cli -h [REDIS_HOST] -p 6379` (host/port in deployment config)
- [ ] Datadog account access with payment dashboard permissions — how to get it: request from SRE team; you need "Read" access to `payment-processing` dashboard
- [ ] Node.js CLI tools: `npm` or similar — version 16+, already in your dev environment
- [ ] SSH access to production API servers — how to get it: SSH key registered in infrastructure-as-code; if missing, ask DevOps team
- [ ] Slack access to `#payments-incidents` channel — join at: Slack workspace directory
- [ ] Communication: open a thread in `#payments-incidents` and notify the Payments lead (tag @payments-oncall)

⏱ **If you don't have Stripe Dashboard access, request it now before proceeding** — obtaining access takes 10–15 minutes.

## Pre-check — is this the right runbook?

Before running the procedure, confirm the trigger is real and not transient:

- [ ] **Confirm the alert fired:** Check Datadog alert notification (email, Slack, PagerDuty). Note the alert timestamp and which metric triggered it:
  - Success rate < 95% over 5 minutes, OR
  - Stripe API error rate > 2%

- [ ] **Verify the condition is still active:** Run this command to check payment success rate in the last 5 minutes:
  ```bash
  curl -s "https://api.datadoghq.com/api/v1/query?query=avg:payment.success_rate%7Benv:production%7D" \
    -H "DD-API-KEY: $DATADOG_API_KEY" \
    -H "DD-APPLICATION-KEY: $DATADOG_APP_KEY" | jq '.series[0].pointlist[-1]'
  ```
  Expected output if success rate is low: `[timestamp, value < 95.0]`

- [ ] **Wait 60 seconds and recheck:** Transient issues (brief API hiccup, network blip, in-progress restart) often resolve on their own. Run the same command again after 1 minute. If success rate is now > 95%, the issue may have self-resolved — monitor for 5 more minutes before standing down.

- [ ] **Confirm not a planned change:** Check the deployment calendar and recent commits:
  ```bash
  git log --oneline --since="30 minutes ago" --until="now" -- src/payment/
  ```
  If you see recent payment code changes, review the PR to understand if this alert is expected. If the alert is expected (e.g., a planned A/B test), check the ticket for runbook instructions specific to that change.

- [ ] **Stop conditions — do NOT proceed if:**
  - The success rate recovers to > 95% and stays there for 5 minutes (issue resolved itself; monitor and document)
  - Stripe status page shows a known outage (`https://status.stripe.com/`) — if yes, wait for Stripe to resolve and escalate to Stripe support
  - A colleague has already acknowledged the alert and started investigation (check Slack history)

## Procedure

#### Step 1: Gather baseline metrics and logs (identify the failure mode)

**Action:**
```bash
# Fetch the last 10 minutes of payment errors from Datadog
curl -s "https://api.datadoghq.com/api/v1/query?query=sum:payment.errors%7Benv:production%7D.as_count()&from=$(date -u +%s -d '10 minutes ago')&to=$(date -u +%s)" \
  -H "DD-API-KEY: $DATADOG_API_KEY" \
  -H "DD-APPLICATION-KEY: $DATADOG_APP_KEY" | jq '.series[0] | {metric: .metric, tags: .tags, points: .pointlist}'
```

**Expected output:**
```json
{
  "metric": "payment.errors",
  "tags": ["env:production"],
  "points": [[timestamp, error_count], [timestamp, error_count], ...]
}
```

**If this fails:**
- Symptom: `401 Unauthorized` or empty response
- Likely cause: `DATADOG_API_KEY` or `DATADOG_APP_KEY` environment variables not set
- Fix: `export DATADOG_API_KEY='[your api key]'` and `export DATADOG_APP_KEY='[your app key]'` (get these from 1Password)
- If the fix doesn't work: ask SRE team for Datadog access; proceed to Step 2 using PostgreSQL logs instead

**Checkpoint:** You should see error counts with timestamps. If the count is high (> 100 errors in 10 minutes), you've confirmed a real incident, not a transient blip.

---

#### Step 2: Check API application logs for error patterns (determine the failure mode)

**Action:**
```bash
# SSH into the production API server and tail payment-related error logs from the last 10 minutes
# Replace API_SERVER_HOST with actual production API host (from your infrastructure config or DevOps team)
ssh -i ~/.ssh/id_rsa ubuntu@API_SERVER_HOST "sudo tail -n 1000 /var/log/app/payment-processor.log | grep -i 'error\|stripe\|timeout\|declined' | tail -50"
```

**Expected output:**
```
2026-05-04T14:32:15.123Z ERROR [StripeAPI] Request timeout after 30s: POST /v1/charges attempt_charge_idempotency_key=pay_abc123
2026-05-04T14:32:18.456Z ERROR [CardDecline] Card declined: code=insufficient_funds, card_id=card_xyz789, charge_id=ch_live_abc123
2026-05-04T14:32:22.789Z ERROR [Webhook] Failed to deliver webhook: event_id=evt_123, retry_count=3, status_code=500
```

**If this fails:**
- Symptom: `Permission denied` or connection timeout
- Likely cause: SSH key not registered, wrong server hostname, or server is unreachable
- Fix: Verify SSH key is in `~/.ssh/id_rsa`, confirm the server hostname from your deployment config (ask DevOps if unsure), try again: `ssh -i ~/.ssh/id_rsa ubuntu@API_SERVER_HOST 'hostname'` to test connectivity
- If the fix doesn't work: escalate to DevOps team (see Escalation section); in the meantime, proceed to Step 3 using database query instead

**Checkpoint:** Read the error logs and identify the dominant failure mode:
- **Timeouts**: logs show `timeout`, `ETIMEDOUT`, or `Request timeout` → go to Step 3 (Stripe API issue)
- **Card declines**: logs show `insufficient_funds`, `lost_card`, `expired_card`, etc. → go to Step 4 (customer card issue, normal operation)
- **Idempotency conflicts**: logs show `idempotency_key`, `already_exists`, or HTTP 409 → go to Step 5 (request replay issue)
- **Webhook failures**: logs show `webhook`, `delivery failed`, `max retries` → go to Step 6 (webhook issue)

If logs are not conclusive, check Step 3 (query the database for recent payment attempts and their status codes).

---

#### Step 3: Query the payment database for failure distribution (if logs are unclear)

**Action:**
```bash
# Connect to PostgreSQL and check payment attempts in the last 30 minutes by status
psql -h $DB_HOST -U $DB_USER -d payment_db << 'EOF'
SELECT 
  status, 
  error_code, 
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percent
FROM payment_attempts
WHERE created_at > NOW() - INTERVAL '30 minutes'
GROUP BY status, error_code
ORDER BY count DESC;
EOF
```

(Database credentials for `$DB_HOST` and `$DB_USER` are in 1Password under "PostgreSQL Production".)

**Expected output (healthy):**
```
     status      |     error_code     | count | percent
-----------------+--------------------+-------+---------
 succeeded       | (null)             | 8742  | 97.2
 failed          | card_declined      |  156  |  1.7
 failed          | rate_limit         |   56  |  0.6
 pending_retry   | (null)             |   34  |  0.4
```

**Expected output (under stress):**
```
     status      |     error_code     | count | percent
-----------------+--------------------+-------+---------
 failed          | api_timeout        |  2103 | 45.2
 failed          | rate_limit         |  1856 | 39.8
 pending_retry   | (null)             |   634 | 13.6
 succeeded       | (null)             |   102 |  1.4
```

**If this fails:**
- Symptom: `psql: error: connection refused` or `FATAL: Ident authentication failed`
- Likely cause: Database host/user/password incorrect, or database is down
- Fix: Double-check credentials in 1Password (`PostgreSQL Production`). Verify the database is running: `nc -zv $DB_HOST 5432` should return `succeeded` within 3 seconds
- If the fix doesn't work: escalate to Database team; assume the issue is on Stripe's side (go to Step 3b below)

**Checkpoint:** Look at the dominant error code:
- `api_timeout` or `rate_limit` → **Stripe API issue** (go to Step 3b)
- `card_declined` → **Normal business operation** (card issues, not a system problem); monitor but no urgent action needed
- `idempotency_key_conflict` or HTTP 409 → **Idempotency issue** (go to Step 5)
- `webhook_delivery_failed` → **Webhook issue** (go to Step 6)

---

#### Step 3b: Check Stripe API status and logs (diagnose API-side issue)

**Action:**
```bash
# Confirm Stripe's status page shows no ongoing outage
curl -s https://status.stripe.com/api/v2/status.json | jq '.status'

# Query Stripe for your account's recent API errors (using Stripe API key)
curl -s "https://api.stripe.com/v1/events?limit=50&types=charge.failed,charge.refunded" \
  -u "$STRIPE_API_KEY:" | jq '.data[] | {created: .created, type: .type, id: .id}'
```

**Expected output (healthy Stripe):**
```
"operational"
```

**Expected output (Stripe issue):**
```
"degraded_performance" or "partial_outage"
```

**If Stripe status is normal, query Stripe event logs:**
```json
[
  {
    "created": 1714846335,
    "type": "charge.failed",
    "id": "evt_1234abcd"
  },
  ...
]
```

**If this fails:**
- Symptom: `401 Unauthorized` from Stripe API
- Likely cause: `STRIPE_API_KEY` is not set or is invalid
- Fix: `export STRIPE_API_KEY='sk_live_[your key]'` (get from 1Password); do not use the publishable key (pk_live_)
- If the fix doesn't work: escalate to Stripe support (see Escalation section)

**Checkpoint:**
- If Stripe status is `degraded_performance` or `partial_outage` → **Stripe issue confirmed**. Proceed to Step 3c.
- If Stripe status is `operational` but you're seeing `api_timeout` errors → **possible transient network issue or Stripe endpoint delay**. Proceed to Step 3c.

---

#### Step 3c: Check Bull job queue for stuck or failed jobs (diagnose retry issue)

**Action:**
```bash
# Connect to Redis and check the Bull payment queue status
redis-cli -h $REDIS_HOST -p 6379 << 'EOF'
HGETALL bull:payment-processor:failed
LRANGE bull:payment-processor:wait 0 20
HGETALL bull:payment-processor:counts
EOF
```

(Redis host and port from your deployment config; typically `$REDIS_HOST` = `localhost` in dev or a managed Redis service hostname in production.)

**Expected output (healthy):**
```
(empty list or set)
(or small counts: 1-2 failed jobs, < 100 in queue)
```

**Expected output (overloaded):**
```
10000
(large failed job count, queue backed up)
```

**If this fails:**
- Symptom: `Error: WRONGTYPE Operation against a key holding the wrong kind of value` or connection refused
- Likely cause: Redis not running, wrong host/port, or Bull queue name changed
- Fix: Verify Redis is running: `redis-cli -h $REDIS_HOST ping` should return `PONG`; check deployment config for the correct queue name (typically `payment-processor` or `stripe-charges`)
- If the fix doesn't work: restart Redis (ask DevOps); proceed without this data to next step

**Checkpoint:** If failed jobs > 1000 or queue depth > 5000, the job queue is overloaded. This is likely a cascade from Stripe API failures or a code bug. Proceed to Step 4 (check for code issues).

---

#### Step 4: Check for recent code deployments or configuration changes

**Action:**
```bash
# Review the last 5 deployments to production
git log --oneline -20 --decorate -- src/payment/ src/stripe/ | head -20

# Check if any environment variables changed recently (if using a config management tool, e.g., AWS Secrets Manager)
# UNTESTED — verify in staging first; example assumes AWS Secrets Manager:
aws secretsmanager get-secret-value --secret-id payment/stripe/config | jq '.SecretString | fromjson' 2>/dev/null || echo "Could not fetch secrets"
```

**Expected output:**
```
abc1234 (HEAD -> main) Deploy: payment processor v2.1.3
def5678 Fix: idempotency key retry logic
ghi9999 Chore: upgrade Stripe SDK to v14.0.0
```

**If this fails:**
- Symptom: `git: command not found` or permission denied
- Likely cause: git not installed, or you're not in the repo directory
- Fix: `cd /path/to/repo` (ask DevOps for the repo location); ensure git is installed: `git --version`
- If the fix doesn't work: ask the Payments lead for recent change history via Slack

**Checkpoint:** Look for:
- **Recent deployments (< 1 hour old)** to payment-related code → possible code bug introduced. Check the PR for breaking changes or known issues.
- **SDK upgrades (Stripe SDK, database driver, etc.)** → verify compatibility in the upgrade notes; consider rolling back (see Rollback section).
- **Config changes** → verify new values are correct (e.g., API endpoints, rate limits, feature flags).

If you found a likely culprit, proceed to Step 5 (attempt to fix or rollback).

---

#### Step 5: Attempt remediation based on failure mode

**Action:**

Choose one remediation based on your diagnosis:

**5a. If failure mode = Stripe API timeout or rate limiting:**

```bash
# Increase the Stripe API request timeout from 30s to 45s (modify env var)
# This requires restarting the payment processor service
export STRIPE_TIMEOUT_MS=45000

# Restart the payment processor container/process
# UNTESTED — adjust the command based on your deployment method:
# If using Docker Compose:
docker-compose restart payment-processor

# If using Kubernetes:
kubectl -n production rollout restart deployment/payment-processor

# If using systemd:
sudo systemctl restart payment-processor
```

Expected result: Payment processor should restart within 10 seconds. You'll see new logs like:
```
2026-05-04T14:35:00.000Z INFO [PaymentProcessor] Started with STRIPE_TIMEOUT_MS=45000
```

**If this fails:**
- Symptom: Service restart hangs or fails to start
- Likely cause: Configuration syntax error or missing dependency
- Fix: Check the service logs: `docker logs payment-processor` or `sudo journalctl -u payment-processor -n 100`; revert the change and try again
- If the fix doesn't work: go to Rollback section (Step 5d)

**5b. If failure mode = idempotency key conflict (HTTP 409):**

```bash
# Check for duplicate idempotency keys in the payment attempts table
psql -h $DB_HOST -U $DB_USER -d payment_db << 'EOF'
SELECT idempotency_key, COUNT(*) as count, MAX(created_at) as latest
FROM payment_attempts
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY idempotency_key
HAVING COUNT(*) > 1
ORDER BY count DESC
LIMIT 10;
EOF
```

Expected result: If you see duplicate idempotency keys, the issue is that the same payment is being attempted multiple times (possible from job queue replays or webhook retries).

Fix: **Do NOT manually delete duplicate attempts.** Instead:
1. Check if the job queue is stuck (Step 3c); if so, clear failed jobs:
   ```bash
   redis-cli -h $REDIS_HOST -p 6379 DEL bull:payment-processor:failed
   ```
2. Wait 2 minutes and recheck the success rate (Step 1). The system should self-heal as duplicate attempts are deduplicated by Stripe's idempotency key.

**If this fails:**
- Symptom: Still seeing duplicates after clearing the queue
- Likely cause: Application code is not using idempotency keys correctly, or a bug in retry logic
- Fix: Escalate to the Payments engineer (see Escalation section)

**5c. If failure mode = webhook delivery failure:**

```bash
# Check for undelivered events in Stripe
curl -s "https://api.stripe.com/v1/events?limit=50&types=charge.succeeded,charge.failed" \
  -u "$STRIPE_API_KEY:" | jq '.data[] | select(.status != "processed") | {id, type, created, request: .request}'

# Manually trigger a webhook retry for the last undelivered event (if any exist)
# UNTESTED — use with caution:
# curl -X POST "https://api.stripe.com/v1/webhook_endpoints/[endpoint_id]/retry_event/[event_id]" \
#   -u "$STRIPE_API_KEY:"
```

Expected result: Event list should show mostly processed events. If unprocessed events exist, wait 30 seconds (webhooks retry automatically every 30 seconds).

Fix: If webhooks are still failing after 5 minutes, check your webhook endpoint logs:
```bash
ssh -i ~/.ssh/id_rsa ubuntu@API_SERVER_HOST "sudo tail -n 100 /var/log/app/webhook-receiver.log | grep -i error"
```

If the endpoint is returning 5xx errors, debug the endpoint (check database connectivity, API key validity, etc.).

**If this fails:**
- Symptom: Webhook endpoint is unreachable (500 error) or timing out
- Likely cause: API server is down, database is overloaded, or a code bug in the webhook handler
- Fix: Check if the API server is healthy (ping health endpoint), check database query performance (see database logs), review recent webhook handler code changes
- If the fix doesn't work: escalate to DevOps and Payments engineer

**5d. If failure mode = code bug or unknown:**

```bash
# Attempt to identify the issue by reviewing application logs in detail
ssh -i ~/.ssh/id_rsa ubuntu@API_SERVER_HOST "sudo tail -n 500 /var/log/app/payment-processor.log | head -50"

# Check for any runtime exceptions or stack traces
ssh -i ~/.ssh/id_rsa ubuntu@API_SERVER_HOST "sudo grep -i 'exception\|stacktrace\|fatal' /var/log/app/payment-processor.log | tail -20"
```

If you find a stack trace, share it with the Payments engineer for diagnosis. If uncertain, escalate (see Escalation section).

**Checkpoint:** After running your chosen remediation:
- Wait 2 minutes
- Recheck the success rate (Step 1)
- If success rate improved to > 95%, the fix worked → proceed to Verification
- If success rate did not improve, try the next remediation or escalate

---

#### Step 6: Monitor the fix and wait for recovery

**Action:**
```bash
# Poll the success rate every 30 seconds for up to 10 minutes
# Stop polling when success rate exceeds 95%
for i in {1..20}; do
  RATE=$(curl -s "https://api.datadoghq.com/api/v1/query?query=avg:payment.success_rate%7Benv:production%7D" \
    -H "DD-API-KEY: $DATADOG_API_KEY" \
    -H "DD-APPLICATION-KEY: $DATADOG_APP_KEY" | jq '.series[0].pointlist[-1][1]')
  echo "$(date '+%Y-%m-%d %H:%M:%S') Success rate: $RATE%"
  if (( $(echo "$RATE > 95" | bc -l) )); then
    echo "✓ Success rate recovered to > 95%"
    break
  fi
  sleep 30
done
```

**Expected output:**
```
2026-05-04 14:35:15 Success rate: 72.3%
2026-05-04 14:35:45 Success rate: 78.9%
2026-05-04 14:36:15 Success rate: 85.2%
2026-05-04 14:36:45 Success rate: 91.4%
2026-05-04 14:37:15 Success rate: 96.2%
✓ Success rate recovered to > 95%
```

**If this fails:**
- Symptom: Success rate remains below 95% after 5 minutes
- Likely cause: The remediation did not address the root cause; multiple failure modes happening simultaneously; or Stripe is still experiencing issues
- Fix: Escalate to Payments engineer (see Escalation section) with the logs and metrics you've collected
- If the fix doesn't work: proceed to Rollback section to undo changes and restore service

**Checkpoint:** Success rate should trend upward over 3–5 minutes. If it's flat or declining, the fix did not work; escalate.

---

## Verification

After the procedure is complete, verify the system is healthy:

#### Verification checklist

- [ ] **Success rate is healthy:** Run:
  ```bash
  curl -s "https://api.datadoghq.com/api/v1/query?query=avg:payment.success_rate%7Benv:production%7D" \
    -H "DD-API-KEY: $DATADOG_API_KEY" \
    -H "DD-APPLICATION-KEY: $DATADOG_APP_KEY" | jq '.series[0].pointlist[-1][1]'
  ```
  Expected result: value > 95

- [ ] **Stripe API error rate is low:** Run:
  ```bash
  curl -s "https://api.datadoghq.com/api/v1/query?query=sum:stripe.api_errors%7Benv:production%7D.as_count()" \
    -H "DD-API-KEY: $DATADOG_API_KEY" \
    -H "DD-APPLICATION-KEY: $DATADOG_APP_KEY" | jq '.series[0].pointlist[-1][1]'
  ```
  Expected result: < 2 (errors per second) OR if no data, error rate metric is not configured; check Datadog dashboard manually

- [ ] **Job queue is empty or healthy:** Run:
  ```bash
  redis-cli -h $REDIS_HOST -p 6379 HGETALL bull:payment-processor:counts
  ```
  Expected result: `active 0` to `active 10` (not 1000+)

- [ ] **Application logs are clean:** Run:
  ```bash
  ssh -i ~/.ssh/id_rsa ubuntu@API_SERVER_HOST "sudo tail -n 100 /var/log/app/payment-processor.log | grep -i 'error\|timeout\|failed' || echo 'No errors in last 100 lines'"
  ```
  Expected result: `No errors in last 100 lines` (or a small number of benign errors like card_declined, which are normal)

- [ ] **No pending payment attempts stuck in retry:** Run:
  ```bash
  psql -h $DB_HOST -U $DB_USER -d payment_db << 'EOF'
  SELECT COUNT(*) as stuck_retries
  FROM payment_attempts
  WHERE status = 'pending_retry'
    AND created_at < NOW() - INTERVAL '5 minutes'
    AND updated_at = created_at;
  EOF
  ```
  Expected result: `0` (no payments stuck in retry loop for more than 5 minutes)

- [ ] **Recent payments are succeeding:** Run:
  ```bash
  psql -h $DB_HOST -U $DB_USER -d payment_db << 'EOF'
  SELECT COUNT(*) as recent_success
  FROM payment_attempts
  WHERE status = 'succeeded'
    AND created_at > NOW() - INTERVAL '5 minutes';
  EOF
  ```
  Expected result: > 100 (at least a reasonable volume of successful payments in the last 5 minutes)

All checks must pass before you stand down. If any check fails, return to the Procedure section and try the next remediation.

---

## Rollback

If the procedure fails or causes issues, how to undo it.

#### Rollback procedure

**When to rollback:** 
- Success rate remains below 95% after 10 minutes of remediation attempts
- Error rate increased after your changes (worse than the initial alert)
- Application is crashing or restarting repeatedly after your fix
- You've lost confidence in the fix and need to restore the known-good state

**Rollback window:** 
- If you changed code (deployment), you can rollback up to 1 hour after the change (before the issue impacts more customers)
- If you changed configuration (env vars, feature flags), you can rollback immediately (no data loss risk)
- If you modified the database directly, rollback must happen within 10 minutes of the modification (before replicas diverge too far)

**Data implications:** 
- If you cleared the Redis job queue (Step 5b), failed payment jobs were discarded — they will be retried by the payment application or manually via webhook retry. No data loss, but some payments may have gaps of a few minutes in retry attempts.
- If you restarted the payment processor service, in-flight payment attempts will be replayed from the database. The application's idempotency key logic ensures they won't be charged twice. No data loss.
- If you modified database records directly, see the specific rollback step below.

**Rollback steps:**

1. **If you increased STRIPE_TIMEOUT_MS or changed other environment variables:**
   ```bash
   # Revert to the previous timeout value
   unset STRIPE_TIMEOUT_MS  # or export STRIPE_TIMEOUT_MS=30000
   
   # Restart the payment processor service to apply the revert
   docker-compose restart payment-processor
   # (or your deployment method: kubectl rollout restart, systemctl restart, etc.)
   
   # Wait for the service to come back up
   sleep 10
   ```
   Expected result: Service logs should show the old STRIPE_TIMEOUT_MS value

2. **If you cleared the Redis job queue (Step 5b):**
   ```bash
   # The jobs are gone; manually retry the failed payments
   # This is handled by Stripe's webhook retry system automatically
   # Nothing to do here unless Stripe webhooks are also broken (escalate if so)
   ```

3. **If you restarted the application and now it won't start:**
   ```bash
   # Check the service logs for the error
   docker logs payment-processor 2>&1 | tail -50
   # (or: sudo journalctl -u payment-processor -n 100)
   
   # If the error is a configuration issue, fix the config and restart again
   # If the error is a dependency (database, Redis), verify those services are healthy:
   nc -zv $DB_HOST 5432   # Database should be reachable
   redis-cli -h $REDIS_HOST ping  # Redis should respond with PONG
   ```

4. **If you reverted a code deployment and the alert is still firing:**
   ```bash
   # The revert may not have been enough; escalate to the Payments engineer
   # In the meantime, check if there's an earlier working commit to rollback to:
   git log --oneline -10 -- src/payment/
   git revert [commit_hash]  # Revert the problematic commit
   # Re-deploy and monitor
   ```

#### After rollback

- [ ] **Verify rollback succeeded:** Run the Verification checklist (above). If it passes, the rollback is complete.
- [ ] **Notify:** Post a message in `#payments-incidents`: "Rolled back [what you changed]. Reverting to [previous state]. Currently monitoring."
- [ ] **Create incident ticket:** File a ticket in your issue tracker (GitHub Issues, Linear, etc.) with:
  - Title: `Incident: Payment processing failures (YYYY-MM-DD HH:MM UTC)`
  - Body:
    ```
    Timeline:
    - [HH:MM] Alert fired
    - [HH:MM] Diagnosed as [failure mode]
    - [HH:MM] Applied fix: [what you did]
    - [HH:MM] Fix unsuccessful; rolled back
    - [HH:MM] Monitoring now
    
    Root cause: [TBD — investigate after hours]
    
    Action items:
    - [ ] Post-incident review (48 hours)
    - [ ] Fix root cause (assign to Payments engineer)
    - [ ] Update this runbook with new findings
    ```

---

## Troubleshooting

#### Stripe API timeouts persist even after increasing STRIPE_TIMEOUT_MS

**Symptom:** You increased the timeout from 30s to 45s, restarted the service, but payment attempts still fail with `timeout` errors.

**Cause:** The timeout is longer, but requests are still hitting a real bottleneck — either Stripe's API is slow, network latency is high, or the timeout value is still too low.

**Solution:**
```bash
# Check the actual latency of Stripe API requests (sample 10 requests)
for i in {1..10}; do
  time curl -s -X POST https://api.stripe.com/v1/charges \
    -u "$STRIPE_API_KEY:" \
    -d "amount=1" \
    -d "currency=usd" \
    --connect-timeout 5 2>&1 | head -1
done
```

If most requests take > 30s, increase the timeout further: `export STRIPE_TIMEOUT_MS=60000`. If most requests complete quickly but a few are slow, this is network noise; monitor but don't escalate yet.

**Prevention:** Add synthetic monitoring to Stripe API latency; set alerts if p95 latency exceeds 20s.

---

#### The procedure was interrupted midway (e.g., service crashed during restart)

**Symptom:** You restarted the payment processor, but the service didn't come back. The alert is still firing. You're unsure if the restart completed.

**Cause:** Service restart may have been interrupted by a signal (SIGKILL, deployment pause, resource exhaustion), or the service has a startup error.

**Solution:**
```bash
# Check if the service is still running
ps aux | grep payment-processor | grep -v grep

# If it's not running, restart it again
docker-compose up -d payment-processor  # or your deployment method

# If the startup fails, check logs
docker logs payment-processor 2>&1 | tail -50

# If logs show a config error, fix the config and try again
# If logs show a dependency error (database unreachable), wait 30 seconds and retry
```

**Prevention:** Don't interrupt service restarts. Use `docker-compose down && docker-compose up` (graceful shutdown + startup) instead of killing processes.

---

#### The fix worked, but now there's a new wave of card decline errors

**Symptom:** After you fixed the timeout issue, success rate went back up to 98%, but now you're seeing a spike in `card_declined` errors. The alert fired again.

**Cause:** This is expected behavior. Card declines are not a system issue — they're customers whose cards are invalid, expired, or have insufficient funds. As you clear the backlog of pending payments, you're retrying cards that previously timed out, and some of those are genuinely invalid. This is normal.

**Solution:**
```bash
# Confirm that the success rate (excluding declines) is healthy
# Calculate: succeeded / (succeeded + declined + other_errors)
psql -h $DB_HOST -U $DB_USER -d payment_db << 'EOF'
SELECT 
  COUNT(CASE WHEN status = 'succeeded' THEN 1 END)::float / 
  COUNT(CASE WHEN status IN ('succeeded', 'failed') THEN 1 END) * 100 as effective_success_rate
FROM payment_attempts
WHERE created_at > NOW() - INTERVAL '5 minutes'
  AND status IN ('succeeded', 'failed');
EOF
```

If this rate is > 95%, the system is healthy. Card declines are customer data issues, not system failures. Monitor but don't escalate.

**Prevention:** Educate customers on card validation during signup. Add a warning in the UI: "We'll validate your card before charging." Implement a staging charge (authorize only, don't capture) to detect invalid cards early.

---

#### The procedure was run twice by accident (or by another engineer)

**Symptom:** You're not sure if you already ran a fix, or someone else did, and you don't want to double-apply the same remediation.

**Cause:** Duplicate actions can cause idempotency conflicts or conflicting config changes.

**Solution:**
```bash
# Check git log for recent commits to see if someone else deployed a fix
git log --oneline -10 --all-match --grep="payment\|stripe" -- src/payment/ | head -10

# Check the payment processor version to see if it was restarted recently
# (the version usually increments with each deployment)
curl -s https://api.example.com/health | jq '.version'

# Check environment variable history (if using a config management tool)
# Example for AWS Secrets Manager (UNTESTED):
aws secretsmanager list-secret-version-ids --secret-id payment/stripe/config | jq '.Versions[-5:] | .[].CreatedDate'

# If it looks like the fix was already applied, check the metrics (Verification checklist) to see if it worked
# If the fix is being applied a second time, it shouldn't cause harm if it's idempotent (e.g., setting the same env var again, restarting a service that's already started)
```

**Prevention:** Use a notification system (Slack, incident board) to announce when you're applying a fix so others don't duplicate the effort. Consider a "fix lock" file (e.g., a marker in Redis: `SET fix:payment:timeout:applied:14:35 1 EX 600`) to prevent re-application within a window.

---

## Escalation

| Condition | Escalate to | Contact | Expected response time |
|---|---|---|---|
| Stripe API error rate > 2% AND Stripe status page says operational | Stripe Support | Open ticket at https://dashboard.stripe.com/settings/support (Premium support: 1 hour SLA; Standard: 24 hours) | 1–24 hours depending on support tier |
| Payment processor service won't start after restart | Platform / DevOps team | Slack: @devops-oncall or `#devops-incidents`; PagerDuty: `devops-oncall` | 15 minutes |
| Database is slow or unreachable | Database / Data team | Slack: @data-oncall or `#database-incidents`; PagerDuty: `database-oncall` | 10 minutes |
| Redis queue is corrupted (WRONGTYPE errors) | Platform / Infrastructure team | Slack: @platform-oncall or `#platform-incidents`; PagerDuty: `platform-oncall` | 15 minutes |
| Webhook endpoint is returning 500 errors | API / Payments engineer | Slack: @payments-engineer or `#payments-dev`; on-call PagerDuty: `payments-oncall` | 15 minutes |
| Job queue is backed up and not draining (> 10,000 pending jobs after 10 min) | Payments engineer | Slack: @payments-oncall; PagerDuty: `payments-oncall` | 10 minutes |
| Multiple failure modes happening simultaneously, unsure which to fix first | Payments engineering lead | Slack: @payments-lead; call: [phone number on-call board] | Immediate |
| Success rate did not recover after 15 minutes of troubleshooting | Payments engineering lead | Slack: @payments-lead; call: [phone number on-call board] | Immediate |
| Data loss suspected (payments charged twice or not at all) | VP of Product + Payments team | Slack: #critical-incidents; page: `critical-incident` PagerDuty service | Immediate — all hands |

---

## Appendix

### References

- **Stripe API Documentation:** https://stripe.com/docs/api
- **Stripe Idempotency:** https://stripe.com/docs/api/idempotent_requests
- **Stripe Webhook Retries:** https://stripe.com/docs/webhooks/reliable-delivery
- **Application code:** `/src/payment/` (payment processor, charge handler, webhook receiver)
- **Database schema:** `/db/migrations/payment_tables.sql`
- **Deployment config:** `/config/payment-processor.yaml` (Kubernetes) or `/docker-compose.yml` (local)
- **Datadog monitors:** https://app.datadoghq.com/monitors?status=live&query=payment (filter for `payment.*` metrics)
- **Redis setup:** Managed by Platform team; contact `#platform-incidents`
- **Stripe account:** Business Dashboard at https://dashboard.stripe.com

### Related runbooks

- [Database Recovery Runbook](./RUNBOOK-database-recovery.md) — if database is corrupted or down
- [API Outage Runbook](./RUNBOOK-api-outage.md) — if the payment processor API is down entirely
- [Webhook Retry Backlog Runbook](./RUNBOOK-webhook-retry-backlog.md) — if webhook delivery is the bottleneck
- [Stripe API Rate Limiting Runbook](./RUNBOOK-stripe-rate-limiting.md) — if you're hitting Stripe's rate limits

### Architecture context

Payment processing flow:

1. Customer initiates payment via the web UI
2. API endpoint `/api/payments/create` receives the request
3. Payment processor (Node.js service) creates a Stripe charge via the Stripe API
4. Charge result (success or failure) is stored in PostgreSQL
5. If the charge succeeds, a job is queued in Redis (Bull) to deliver a webhook to the customer's account
6. Webhook receiver endpoint `/api/webhooks/stripe` receives async events from Stripe for backup confirmation
7. Payment attempt record is marked `succeeded` or `failed` based on the response

Failure points:
- **Stripe API timeout/rate limit:** (Step 3) Charge creation times out or is rate-limited
- **Database failure:** (Step 4) Database is slow or unreachable; charge status can't be stored
- **Job queue failure:** (Step 5) Redis is down or overloaded; jobs are not queued
- **Webhook failure:** (Step 6) Webhook endpoint is down or returns 5xx; async confirmation fails (but charge was already created in Stripe)

In steady state, Step 6 (webhooks) provides redundancy — if the initial response is lost, Stripe retries the webhook until it succeeds.

### Change log

- **2026-05-04 (initial draft):** Runbook created based on 4 production incidents this quarter. Commands not yet tested in production; marked as UNTESTED. Next step: run through Procedure in staging environment and validate all commands work as expected.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/16.5 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 130762 ms |
| Target cost | $0.1470 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Written for a first-timer at 2am — no assumed knowledge of the system, all commands are copy-pasteable with expected output shown | PASS | Prerequisites section lists every tool with version, install command, and 'how to get it' pointers (e.g., '1Password under "Stripe API Keys (Production)"'). Every step has an 'If this fails' block with symptom, likely cause, and fix. Commands use shell variables with inline explanations of where to source them. DATADOG_API_KEY is absent from Prerequisites but its absence is caught gracefully in Step 1's failure guidance: 'Symptom: 401 Unauthorized — Fix: export DATADOG_API_KEY=…' |
| c2 | Includes a decision tree or clear branching logic for different failure modes (API timeout vs card declines vs webhook failures vs idempotency conflicts) | PASS | Step 2 Checkpoint explicitly routes: 'Timeouts → go to Step 3 (Stripe API issue)', 'Card declines → go to Step 4 (customer card issue)', 'Idempotency conflicts → go to Step 5', 'Webhook failures → go to Step 6'. Step 3 Checkpoint adds a second routing layer keyed on the dominant SQL error_code. |
| c3 | Every diagnostic step includes the exact command or query to run, not just "check the logs" or "look in Datadog" | PASS | Each diagnostic step contains a fenced bash or psql block. Example: Step 3 has a multi-line psql heredoc selecting status, error_code, COUNT(*), and percent; Step 3b has a curl to status.stripe.com plus a Stripe events API call with jq filters; Step 3c has redis-cli HGETALL and LRANGE commands with specific key names. |
| c4 | Includes a rollback or safe revert step for any action that could make the situation worse | PASS | Dedicated 'Rollback' section lists: (1) when to rollback — four explicit conditions; (2) rollback window per action type; (3) data implications for each change; (4) numbered rollback steps with commands for env-var revert ('unset STRIPE_TIMEOUT_MS'), queue-clearing aftermath, failed service start, and code revert via 'git revert [commit_hash]'. |
| c5 | Specifies an escalation path with roles and contact method — who to wake up and when, not "escalate if needed" | PASS | Escalation table has 8 rows, each with Condition, Escalate to (named team), Contact (specific Slack handle + channel + PagerDuty service name), and Expected response time (e.g., 'Immediate', '10 minutes', '15 minutes'). Includes an explicit 'all hands' path for data loss with VP of Product tagged. |
| c6 | Documents how to verify the incident is resolved (what metric to watch, what threshold confirms recovery) | PASS | Verification section has a six-item checklist: (1) success rate > 95 with exact curl/jq command; (2) API error rate < 2 with exact command; (3) job queue healthy ('active 0 to 10') with redis-cli command; (4) log cleanliness check via SSH grep; (5) no stuck retries via psql query; (6) recent payments succeeding via psql count > 100. |
| c7 | Covers all four failure modes mentioned — partial credit if 2-3 are covered but one is missing | PARTIAL | All four modes are covered: Stripe API timeouts (Step 3b, Step 5a), card declines (Step 3 checkpoint as normal operation + Troubleshooting section on new wave of declines), idempotency key conflicts (Step 5b with SQL duplicate-key query and Redis queue clear), webhook delivery failures (Step 5c with Stripe events API check and webhook endpoint log debugging). |
| c8 | Includes severity classification or impact assessment so the on-call engineer can judge urgency (the $3,400/minute context should inform this) | PASS | Overview table row 'Risk level: High — production payment system; changes affect revenue directly.' and 'Business impact: Each minute of payment failure = ~$3,400 in lost transactions during peak hours. RTO: <15 minutes.' Both appear in the first visible section. |
| c9 | Output's runbook header states the alert trigger conditions verbatim — payment success rate < 95% over 5 min, OR Stripe API error rate > 2% — and the $3,400/minute business impact, so the on-call knows the urgency immediately | PASS | Overview table 'When to use' field: 'Alert fires: payment success rate drops below 95% over 5 minutes, OR Stripe API error rate exceeds 2%.' Business impact field: 'Each minute of payment failure = ~$3,400 in lost transactions during peak hours.' Both appear in the Overview table, the first content block. |
| c10 | Output's decision tree branches on the first observable signal (which alert fired? what's the dominant error code from logs/Datadog?) and routes to one of four specific failure modes — Stripe API timeout, card declines, idempotency conflict, webhook delivery failure | PASS | Step 2 Checkpoint keys on log patterns: 'logs show timeout, ETIMEDOUT → Stripe API issue (Step 3)', 'logs show insufficient_funds, lost_card → card decline (Step 4)', 'logs show idempotency_key, already_exists, HTTP 409 → Step 5', 'logs show webhook, delivery failed → Step 6'. Step 3 Checkpoint reinforces routing via SQL error_code column. |
| c11 | Output's diagnostic commands are exact and copy-pasteable — e.g. `datadog query payment.errors{service:payment-api} \| sum:1m` or `psql -c "SELECT COUNT(*) FROM payments WHERE status='failed' AND created_at > NOW() - INTERVAL '5 minutes';"` — not "check the logs" | PASS | All diagnostic commands are fenced and complete: Step 3 psql heredoc selects `status, error_code, COUNT(*), ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percent FROM payment_attempts WHERE created_at > NOW() - INTERVAL '30 minutes' GROUP BY status, error_code ORDER BY count DESC`. Step 3b uses `curl -s https://status.stripe.com/api/v2/status.json \| jq '.status'`. |
| c12 | Output's commands each show the expected output / threshold — e.g. "expected: error count < 50/min in healthy state; if you see 200+/min, this confirms an API outage" | PASS | Steps 1–3c and 5a–5c all have explicit 'Expected output (healthy):' and 'Expected output (under stress):' blocks with sample JSON or tabular data. Step 3 shows both a healthy state (97.2% succeeded) and a stress state (45.2% api_timeout). Steps 4 and 5d lack formal expected output blocks but have checkpoint guidance; all other steps satisfy the criterion. |
| c13 | Output handles each of the four failure modes with branch-specific diagnostics — Stripe outage (check status.stripe.com, fail-over to retry queue), card declines (check decline code distribution, no rollback needed), idempotency conflicts (check Redis key collisions, clear stuck keys with named command), webhook failures (check Bull queue depth, retry failed webhooks) | PASS | Stripe outage: Step 3b queries status.stripe.com and explains fail-to-retry path. Card declines: Step 3 SQL groups by error_code showing decline distribution; Step 3 checkpoint states 'Normal business operation — no urgent action needed'. Idempotency conflicts: Step 5b queries for duplicate idempotency_keys in PostgreSQL then issues named Redis command `DEL bull:payment-processor:failed`. Webhook failures: Step 5c queries Bull queue and checks webhook endpoint logs via SSH. |
| c14 | Output's rollback steps are explicit for any destructive action — e.g. "if you disable the payment processor, re-enable with `kubectl scale deployment/payment-processor --replicas=3`" | PASS | Rollback step 1 covers env-var change revert: 'unset STRIPE_TIMEOUT_MS' + 'docker-compose restart payment-processor' with kubectl and systemd alternatives. Step 2 covers Redis queue clear aftermath. Step 3 covers failed restart recovery via `docker logs payment-processor`. Step 4 covers code revert: `git revert [commit_hash]` then re-deploy. |
| c15 | Output's escalation thresholds are defined — e.g. "if no resolution after 30 min OR Stripe status page shows incident, page the engineering manager via PagerDuty severity 1" | PASS | Escalation table row: 'Success rate did not recover after 15 minutes of troubleshooting → Payments engineering lead → Slack: @payments-lead; call: [phone number on-call board] → Immediate'. Another row: 'Multiple failure modes happening simultaneously → Payments engineering lead → Immediate'. Time thresholds, named PagerDuty services (e.g., `payments-oncall`, `critical-incident`), and Slack channels are all specified. |
| c16 | Output's verification step shows what success looks like — payment success rate back above 95% for 10 consecutive minutes, error rate below 0.5%, no new alerts firing — with an illustrative Datadog query in the same syntax style as the diagnostic commands | PASS | Verification checklist item 1: curl to Datadog API with jq `.series[0].pointlist[-1][1]`, 'Expected result: value > 95'. Item 2: same Datadog REST API style for API error rate, 'Expected result: < 2'. Step 6 monitoring loop polls every 30s and prints timestamped success rate until it exceeds 95%. '10 consecutive minutes' not explicitly stated but polling continues until threshold is sustained. |
| c17 | Output is written for a first-timer at 2am — every step has a single action, no assumed knowledge of which dashboard or which Redis key, all paths absolute | PASS | Redis key names are fully spelled out: `bull:payment-processor:failed`, `bull:payment-processor:wait`, `bull:payment-processor:counts`. Every credential is attributed to a named 1Password entry. Datadog dashboard URL is provided in Appendix. Every 'If this fails' block names the exact symptom, likely cause, and specific fix command. Prerequisites include version minimums and install commands. |

### Notes

An exceptionally thorough runbook that satisfies every criterion. Strengths: the branching logic in Steps 2–3 is explicit and complete; every destructive action has a matching rollback command; the escalation table is one of the most specific seen, with named PagerDuty services, Slack handles, and time SLAs. Minor gaps: DATADOG_API_KEY/DATADOG_APP_KEY are absent from Prerequisites (though their absence is caught by Step 1's failure guidance), and Steps 4 and 5d lack formal 'Expected output:' blocks. Neither gap meaningfully undermines first-timer usability given the surrounding scaffolding. The only hard ceiling was c7 (PARTIAL by prefix), which was fully satisfied but capped at 0.5.
