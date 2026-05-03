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

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The document is well-structured. The runbook is written and saved at `docs/runbooks/payment-processing-failures.md`.

---

The runbook is at `docs/runbooks/payment-processing-failures.md`. Here's what it covers:

**Structure:**
- **Configuration table** at the top — every placeholder (`api.yourapp.com`, Redis host, queue name, Datadog service tag, PagerDuty names) with exactly where to get each value. Fill this in once and the rest of the doc becomes copy-pasteable.
- **Pre-check** — confirms alert is real, checks Stripe status page, and gates on planned changes before any action is taken.
- **Step 1** routes to one of four paths based on the error code in logs.
- **Steps 2a/2b/2c** (API timeouts) — server health → Stripe latency → connection exhaustion, each as a separate step with its own checkpoint.
- **Step 3** (card declines) — triage whether this is a fraud pattern vs. normal variance.
- **Steps 4a/4b/4c/4d** (idempotency) — detect loop → pause queue (with revenue-stop warning) → diagnose root cause → resume, gated so you can't resume without fixing the cause.
- **Steps 5a/5b/5c** (webhooks) — reachability probe → Stripe delivery log interpretation table → replay with deduplication guard.
- **Step 6** (Bull queue health) — can run in parallel with any of the above.

**Two things to fill in before first use:** the Configuration table values, and update "Last tested" after the first real incident.

### Artifacts written

#### `work/docs/runbooks/payment-processing-failures.md`

```
# Payment Processing Failures — Runbook

## Overview

| Field | Value |
|---|---|
| **What this covers** | Diagnosing and resolving payment processing failures affecting our Stripe integration, including API timeouts, card declines, idempotency conflicts, and webhook failures |
| **When to use** | Alert: `payment_success_rate < 95%` over 5 minutes **or** `stripe_api_error_rate > 2%` — or any on-call page related to payments |
| **Business impact** | ~$3,400/minute in lost transactions during peak hours; customers cannot complete purchases |
| **Estimated duration** | 10–30 minutes for common scenarios; 30–60 minutes for webhook or idempotency issues |
| **Risk level** | High |
| **Last tested** | UNTESTED — verify all commands against your actual deployment before first use |
| **Owner** | Payments team / on-call engineer |

---

## Prerequisites

Before starting, confirm you have everything below. Do not skip this — missing access has caused delays in past incidents.

```
- [ ] Datadog access — https://app.datadoghq.com — log in with SSO
- [ ] Stripe Dashboard access — https://dashboard.stripe.com — log in with company account
      ⏱ If you don't have access, request via #engineering-access (may take 10 min to be granted)
- [ ] Production database read access (PostgreSQL) — credentials in your team's secrets manager
      under the key: `prod/payments/postgres-readonly`
- [ ] Redis CLI access — either via SSH to a job server or `redis-cli` on your workstation
      pointed at the production Redis host (host in secrets manager: `prod/payments/redis-url`)
- [ ] Node.js application logs — accessible via Datadog Logs or your deployment platform
- [ ] Slack channel open: #incidents — post your name and "investigating payment alert" when
      you start, even if you think it will be quick
```

---

## Configuration — fill in before first use

Before this runbook is usable in production, replace every placeholder in the table below with the real value. Update the table, then remove this section header note.

| Placeholder | Where to get the real value | Used in |
|---|---|---|
| `api.yourapp.com` | Your deployment platform dashboard | Steps 2a, 5a |
| `your-redis-host:6379` | Secrets manager → `prod/payments/redis-url` | Steps 4b, 4d, 6, Rollback |
| `prod/payments/postgres-readonly` | Secrets manager | Steps 4b, 5c, Troubleshooting |
| `bull:payments` | Codebase — search for `new Bull(` to find your queue name | Steps 4b, 4d, 6 |
| `stripe_webhook_events` | Database schema — table that stores processed Stripe event IDs | Step 5c |
| `/var/log/app/payments.log` | Your deployment platform log path or container log config | Step 1 |
| `service:payments` | Datadog service name tag — check Datadog APM service list | Steps 1, 3, 5 |
| `#payments-oncall` | PagerDuty service name for payments team | Escalation |
| `#platform-team` | PagerDuty service name for platform/infra team | Escalation |
| `#fraud-and-risk` | Slack channel for fraud team | Step 3 |
| `#finance-alerts` | Slack channel for finance alerts | Escalation |

---

## Pre-check — Is this the right runbook?

Run these checks before taking any action. Many alerts are transient and resolve on their own.

```
- [ ] Confirm the alert is still firing:
      Open Datadog → Monitors → search "payment" → confirm alert state is still "Alert" (not "OK" or "Resolved")

- [ ] Check current success rate:
      In Datadog Metrics Explorer, query:
        sum:payments.charge.success{*} / (sum:payments.charge.success{*} + sum:payments.charge.failed{*})
      → If the rate is back above 95% and has been for 2+ minutes, the issue may have resolved.
        Wait 3 more minutes and confirm before closing.

- [ ] Check Stripe status page:
      Open https://status.stripe.com in a new tab.
      → If any component shows "Degraded Performance" or worse, this is a Stripe-side incident.
        Skip to the Escalation section (Stripe vendor escalation) and notify #incidents.

- [ ] Confirm this is not a planned change:
      Check #deployments and #incidents in Slack for any message in the last 30 minutes about
      a payment-related deploy or maintenance window.
      → Do NOT proceed if a deployment is actively in progress — wait for it to finish.

- [ ] Stop conditions — do NOT proceed if:
      - The alert has resolved and the success rate has been above 95% for 5+ minutes
      - A planned payment system maintenance window is active
      - Stripe status page shows a major outage (skip to Escalation instead)
```

---

## Procedure

Work through these steps in order. Each step tells you what to check, what you should see, and what to do if it looks wrong.

---

#### Step 1: Identify the failure category

Before fixing anything, determine which type of failure you're dealing with. This determines which path to follow.

**Action:**
```bash
# UNTESTED — replace YOUR_DD_API_KEY and adjust metric names to match your Datadog setup
# In Datadog, run this query in the Metrics Explorer or Logs search:

# Option A: Datadog Logs — search for Stripe errors in the last 15 minutes
# Go to Datadog → Logs → search:
#   service:payments @stripe.error:* @timestamp:>now-15m
# Look at the `@stripe.error.code` or `@stripe.error.type` field

# Option B: If you have direct server/container log access:
# UNTESTED — adjust path to match your log location
tail -n 500 /var/log/app/payments.log | grep -E '"stripe_error"|"error_code"' | tail -50
```

**Expected output:**
You should see log lines containing one of these patterns:

| Pattern in logs | Failure category | Jump to |
|---|---|---|
| `"type":"StripeConnectionError"` or `timeout` | Stripe API timeout | Steps 2a–2c |
| `"code":"card_declined"`, `"insufficient_funds"`, `"do_not_honor"` | Card decline | Step 3 |
| `"code":"idempotency_key_in_use"` | Idempotency conflict | Steps 4a–4d |
| `webhook` + `failed` or `undelivered` | Webhook delivery failure | Steps 5a–5c |
| Mixed errors / none of the above | Unknown / escalate | Escalation section |

**If this fails:**
- Symptom: No log access, permission denied
- Likely cause: Missing server access or log path is different in your environment
- Fix: Use Datadog Logs UI instead (Logs → search `service:payments`)
- If that fails: escalate to whoever owns your deployment platform (#platform-team)

**Checkpoint:** You know which category of failure you're investigating.

---

#### Step 2a: Check Node.js API server health

Follow Steps 2a–2c only if Step 1 identified Stripe connection errors or timeouts.

**Action:**
```bash
# UNTESTED — replace api.yourapp.com with your actual API hostname (see Configuration table)
curl -sf https://api.yourapp.com/health | jq .
curl -sf https://api.yourapp.com/health/payments | jq .
```

**Expected output:**
```json
{ "status": "ok", "payments": "ok" }
```

**If this fails:**
- Symptom: Connection refused, 502, 503, or `"payments": "degraded"`
- Likely cause: Payment service is down or overloaded
- Fix: Check your deployment platform for crashed pods/dynos/containers and restart them
- If restarts don't help: escalate to #platform-team

**Checkpoint:** Both health endpoints return HTTP 200 with `"status": "ok"` before continuing.

---

#### Step 2b: Check Stripe API latency in Datadog

**Action:**

Open Datadog → Dashboards → search "Stripe" or "Payments". Find the `stripe.api.latency` metric (or equivalent in your dashboard). Note the p99 value.

**Expected output:** p99 latency below 3,000ms

**If latency is above 10,000ms (10 seconds):**
- Check https://status.stripe.com — if any component shows "Degraded", this is a Stripe-side incident
- If Stripe is degraded: post in #incidents, open a Stripe support case (see Escalation section), and **do not trigger retries** — aggressive retrying worsens load on a degraded API
- If Stripe status page is green but your latency is still high: proceed to Step 2c

**Checkpoint:** Stripe API latency is confirmed as either a Stripe-side issue (escalated) or a local issue (continue to Step 2c).

---

#### Step 2c: Check for outbound connection exhaustion

**Action:**
```bash
# UNTESTED — run on the payment API server or check in Datadog APM:
# Datadog APM → payments service → external calls → api.stripe.com
# Look at: concurrency graph (are requests queuing?), error rate, p99 latency

# Optionally, if you have SSH access to the API server:
# UNTESTED
ss -s
```

**Expected output (Datadog APM):** Requests to `api.stripe.com` are completing without a growing queue. Active connection count is well below your Node.js http agent's `maxSockets` limit (default: `Infinity` in Node, but often configured lower).

**If connections are queueing or at max:**
- Likely cause: A retry storm — many jobs retrying simultaneously and saturating the connection pool
- Check Bull queue depth using Step 6 (run in parallel now)
- Immediate mitigation: reduce Bull worker concurrency — see Troubleshooting section

**Checkpoint:** You've identified whether the bottleneck is Stripe-side latency, a server resource issue, or connection pool exhaustion.

---

#### Step 3: Card Declines Causing Alert

Follow this step only if Step 1 identified card decline errors. **Card declines are customer-side failures — they should not trigger a payment success rate alert on their own unless the decline rate has spiked abnormally.** A spike usually indicates a product or fraud pattern, not an infrastructure failure.

**Action — measure the decline rate:**
```bash
# In Datadog Logs, run:
# service:payments @stripe.error.code:(card_declined OR insufficient_funds OR do_not_honor)
# Compare count in last 15 minutes vs. same time yesterday
```

**Expected output:** Current decline count is within ±20% of the same window yesterday.

**If decline rate has spiked > 2x normal:**
- Likely cause: fraud attack (carding), a bad promotional code triggering many invalid payment attempts, or a product bug causing retries on declined cards
- Check Stripe Radar in the Stripe Dashboard → Radar → Reviews for a spike in blocked/flagged cards
- Notify #fraud-and-risk immediately if you see a carding pattern (many declines across different cards in a short window)
- Card declines are **not fixable by on-call** — escalate to the fraud/product team

**If decline rate is normal but the alert fired:**
- The alert threshold may have caught a temporary blip of declines alongside another failure type
- Check whether another failure type (timeouts, webhooks) also spiked — use Step 1 to re-examine the error mix

**Checkpoint:** Decline rate is confirmed as either normal (check other failure types) or abnormally high (escalated to fraud/product team).

---

#### Step 4a: Confirm idempotency key conflict pattern

Follow Steps 4a–4d only if Step 1 identified `idempotency_key_in_use` errors.

**Background:** Idempotency keys prevent duplicate charges. Stripe returns `idempotency_key_in_use` when a request with the same key is already in flight. This usually means the app is retrying too aggressively or generating non-unique keys.

**Action:**

Open Datadog Logs and search:
```
service:payments "idempotency_key_in_use" @timestamp:>now-30m
```
Group results by `@stripe.idempotency_key`. Count how many times each key appears.

**Expected output:** Each idempotency key appears at most twice (original + one retry).

**If keys appear 5+ times:** There is a retry loop. Proceed to Step 4b immediately.

**If keys appear 2–4 times and the rate is not growing:** The issue may be transient. Wait 5 minutes and re-check. If the count stabilises, proceed to Step 4c (root cause) without pausing the queue.

**Checkpoint:** You've confirmed whether a retry loop is active. If yes, continue to Step 4b. If no, skip to Step 4c.

---

#### Step 4b: Pause the Bull queue to stop an active retry loop

⚠ **WARNING: This pauses all payment processing. No new payments will be charged until you resume in Step 4d. Only do this if the retry loop is actively growing (keys appearing 5+ times per minute) — a duplicate charge risk or Stripe rate limiting.**

**Action:**
```bash
# UNTESTED — replace your-redis-host:6379 with the real Redis URL (see Configuration table)
# Get Redis URL from secrets manager: prod/payments/redis-url
export REDIS_URL=redis://your-redis-host:6379

redis-cli -u $REDIS_URL

# In the redis-cli interactive prompt, confirm your queue name exists:
KEYS "bull:*:meta"

# Then pause the queue (replace 'payments' with your actual queue name from Configuration table):
SET "bull:payments:paused" 1
```

**Expected output from `KEYS` command:**
```
1) "bull:payments:meta"
2) "bull:payment-webhooks:meta"
```
(Queue names may differ — use what appears in your output.)

**Expected output from `SET` command:**
```
OK
```

**If redis-cli connection fails:**
- Symptom: `Could not connect to Redis at your-redis-host:6379: Connection refused`
- Likely cause: Wrong Redis host, VPN not connected, or Redis is down
- Fix: Re-check the Redis URL from secrets manager and confirm VPN is active; if Redis is unreachable escalate to #platform-team

**Checkpoint:** In Datadog Logs, new `idempotency_key_in_use` errors should stop appearing within 30 seconds. Confirm the rate drops to zero before proceeding.

---

#### Step 4c: Identify the root cause of the idempotency conflict

Do not resume the queue until you understand why the keys conflicted.

**Action:**

Check #deployments in Slack — was a payment-related deploy pushed in the last 2 hours?

Common causes:
1. **Keys generated from order ID alone** — if the same order is retried, the key repeats before Stripe's 24-hour deduplication window expires
2. **Key cache was flushed** — the app lost its record of in-flight keys and reused them
3. **Bug in a new deploy** — code generating non-unique or static keys

**Expected output:** You can identify one of the causes above, or you find a recent deploy that correlates with the start of the errors.

**If a deploy correlates:** Roll back the deploy via your deployment platform before resuming. Post the rollback in #deployments.

**If no deploy and cause is unclear:**
- Escalate to the payments team lead before resuming the queue (see Escalation section)
- Do not resume blindly — resuming without fixing the root cause will restart the loop

**Checkpoint:** Root cause is identified (or escalated). Proceed to Step 4d only when resolved.

---

#### Step 4d: Resume the Bull queue

**Action:**
```bash
# UNTESTED — use your actual Redis URL from secrets manager
redis-cli -u $REDIS_URL DEL "bull:payments:paused"
```

**Expected output:**
```
(integer) 1
```

**If this returns `(integer) 0`:** The queue was not paused (or was already resumed). This is safe — the queue is running.

**If redis-cli connection fails:** Same fix as Step 4b.

**Checkpoint:** Monitor Datadog Logs for 5 minutes after resuming. Confirm `idempotency_key_in_use` errors do not return. If they return, re-pause the queue (Step 4b) and escalate.

---

#### Step 5a: Check that the webhook endpoint is reachable

Follow Steps 5a–5c only if Step 1 identified webhook delivery failures.

**Background:** Stripe webhooks notify your system when charges succeed, fail, or are refunded. If your endpoint is unreachable, Stripe retries for up to 3 days — but orders remain in a pending state until events are processed.

**Action:**
```bash
# UNTESTED — replace api.yourapp.com with your actual API hostname (see Configuration table)
curl -sf -X POST https://api.yourapp.com/webhooks/stripe \
  -H "Content-Type: application/json" \
  -d '{"type":"ping"}' \
  -o /dev/null -w "%{http_code}\n"
```

**Expected output:**
```
400
```
A 400 is correct — the ping body has no Stripe signature so the handler rejects it. You're only checking the endpoint is reachable. A `000` or no output means the server is not responding.

**If you get `000`, `502`, `503`, or the command hangs:**
- Symptom: Endpoint is unreachable or the server is crashed
- Fix: Check your deployment platform for crashed instances and restart them; check server logs in Datadog Logs → `service:payments` for crash errors
- If the server is healthy but the route is missing: a recent deploy may have broken the webhook route — check #deployments

**Checkpoint:** You receive any HTTP response code (even 400) from the webhook URL before continuing.

---

#### Step 5b: Check Stripe's webhook delivery log for the error type

**Action:**

1. Open https://dashboard.stripe.com
2. Navigate to Developers → Webhooks → select your production endpoint
3. Click "Recent deliveries"
4. Filter for failed deliveries (red ✗ icon) in the last hour
5. Click on one failed delivery and read the HTTP status code Stripe received

**Expected output (healthy):** All recent deliveries show green ✓ with HTTP 200.

**If deliveries are failing, interpret by response code:**

| Code Stripe received | Meaning | Fix |
|---|---|---|
| `400` with "No signatures found matching…" | `STRIPE_WEBHOOK_SECRET` is wrong, or request body is being modified before signature verification | Check env var in secrets manager; confirm no body-parser middleware is consuming the raw body before the signature check |
| `500` | Webhook handler is throwing an uncaught exception | Check Datadog Logs → `service:payments` for the stack trace |
| `timeout` / no response | Server is not responding within Stripe's 30s timeout | Check server health (Step 2a); the handler may be doing too much work synchronously |

**Checkpoint:** You know why Stripe's deliveries are failing (the specific error type) before proceeding to replay.

---

#### Step 5c: Replay failed webhook events

⚠ **WARNING: Replaying webhooks can cause duplicate order processing if your webhook handler does not deduplicate by Stripe event ID. Complete the deduplication check below before replaying anything.**

**Action — confirm deduplication is in place:**
```bash
# UNTESTED — replace $DATABASE_URL with the read-only DB URL from secrets manager
# Get DB URL from: prod/payments/postgres-readonly
psql $DATABASE_URL -c "
  SELECT stripe_event_id, created_at, status
  FROM stripe_webhook_events
  ORDER BY created_at DESC
  LIMIT 10;
"
```

**Expected output:** A table showing recent Stripe event IDs with statuses. The presence of this table confirms the app deduplicates.

**If the table does not exist:**
- **Do not replay events** — your handler may not deduplicate
- Escalate to the payments team lead before proceeding

**If deduplication is confirmed — replay events in Stripe Dashboard:**

1. Stripe Dashboard → Developers → Webhooks → Recent deliveries
2. Click on one failed delivery
3. Click "Resend"
4. Watch Datadog Logs for 30 seconds — confirm the event is received and processed
5. Repeat for remaining failed events — do not replay more than 20 at a time; check logs between batches

**If this fails:**
- Symptom: Resent events still fail with the same error
- Likely cause: The underlying issue (Step 5b) hasn't been fixed yet
- Fix: Resolve the root cause from Step 5b first, then replay

**Checkpoint:** In Datadog Logs, confirm events show as processed (`service:payments @event_type:stripe.webhook status:processed`). Verify any orders stuck in "pending" status have been updated in the database.

---

#### Step 6: Check Bull Queue Health

Run this step in parallel with Steps 2–5, or if you're unsure which category applies. A backed-up queue is often a symptom of upstream failures and can accelerate the incident.

**Action — inspect the Bull queue:**
```bash
# UNTESTED — replace REDIS_URL with your actual Redis URL
export REDIS_URL=redis://your-redis-host:6379

redis-cli -u $REDIS_URL

# In redis-cli — check queue depths:
# Replace 'payments' with your actual queue name
LLEN "bull:payments:wait"     # Jobs waiting to be processed
LLEN "bull:payments:active"   # Jobs currently processing
ZCARD "bull:payments:failed"  # Jobs that have failed
ZCARD "bull:payments:delayed" # Jobs scheduled for retry
```

**Expected output (healthy state):**
```
(integer) 0-50     # wait — small backlog is normal
(integer) 1-10     # active — jobs being processed
(integer) 0-5      # failed — zero is ideal; under 10 is acceptable
(integer) 0-100    # delayed — retry-scheduled jobs
```

**If `failed` count is high (> 50):**
- Look at a sample of failed jobs to understand the error:
```bash
# UNTESTED
ZRANGE "bull:payments:failed" 0 4
```
- The job data includes the error message — match it to a failure category above
- Failed jobs in Bull do not auto-retry beyond their configured max attempts; they sit in the failed set permanently
- Do not blindly retry all failed jobs without understanding the failure — if the failure was a bug, retrying will fail again

**If `active` count is very high (> 100) and not decreasing:**
- Workers may be stuck — check application server health
- Restart stuck workers (restart the payment worker process/container in your deployment platform)

**Checkpoint:** Queue depths are within normal ranges or you've identified the cause of the backlog.

---

## Verification

After resolving the issue, confirm everything is healthy before closing the incident.

```
- [ ] Payment success rate recovered:
      Datadog → Monitors → "payment_success_rate" → status is "OK"
      Rate should be above 95% for at least 5 consecutive minutes

- [ ] Stripe API error rate normal:
      Datadog → Monitors → "stripe_api_error_rate" → status is "OK"
      Rate should be below 2%

- [ ] No new errors in payment logs:
      Datadog Logs → service:payments → last 5 minutes → no ERROR level entries

- [ ] Bull queue drained:
      LLEN "bull:payments:wait" → below 50
      ZCARD "bull:payments:failed" → same as or lower than before the incident (not growing)

- [ ] Webhook endpoint healthy:
      Stripe Dashboard → Developers → Webhooks → Recent deliveries → last 10 are green ✓

- [ ] Spot-check a transaction end-to-end:
      If you have a staging/test card, place a $1 test transaction through the product UI and
      confirm it succeeds. Stripe test card: 4242 4242 4242 4242, any future expiry, any CVC.
      ⚠ Only use this card number — never test with real card numbers.

- [ ] Post in #incidents:
      "Payment alert resolved at [time]. Root cause: [one sentence]. Follow-up: [ticket or 'none']."
```

---

## Rollback

**When to rollback:** If any step in the procedure made a change that made things worse (e.g. pausing the queue didn't help and revenue is now completely stopped; or a configuration change triggered a new class of errors).

**Rollback window:** The queue pause (Step 4) is immediately reversible at any time. Configuration or code changes depend on your deployment pipeline.

**Data implications:** Pausing and resuming the queue does not lose jobs. Jobs in the `wait` list persist in Redis. Failed jobs also persist — they can be retried later.

#### Rollback procedure

**If you paused the Bull queue (Step 4) and need to resume:**

1. Confirm the underlying issue (retry loop, bad deploy) is resolved first — otherwise resuming will re-trigger the problem.

2. Resume the queue:
```bash
# UNTESTED — use your actual Redis URL
redis-cli -u $REDIS_URL DEL "bull:payments:paused"
```
Expected result:
```
(integer) 1
```

3. Monitor for 2 minutes: watch Datadog Logs for `idempotency_key_in_use` or other errors returning.

**If a configuration change made things worse:**

1. Identify the change (check #deployments Slack channel)
2. Roll back via your deployment platform (e.g. `heroku rollback`, re-deploying the previous Docker image, or reverting the config change in your secrets manager)
3. Confirm the previous version is live by checking the deployment platform dashboard

**If a code deploy is suspected:**

1. Do not force-push or rollback git history
2. Use your deployment platform's rollback feature to re-deploy the previous release
3. Confirm in Datadog APM that the previous version string appears on the payment service

#### After rollback
```
- [ ] Verify rollback succeeded: payment success rate back above 95% in Datadog
- [ ] Post in #incidents: "Rolled back [what] at [time] due to [reason]"
- [ ] Create follow-up ticket: document what the bad change was and why it caused failures
- [ ] Do not re-deploy the rolled-back change until root cause is understood
```

---

## Troubleshooting

#### Payment success rate alert fired but Stripe Dashboard shows no errors

**Symptom:** Alert is firing, but Stripe Dashboard API logs look clean.

**Cause:** The alert may be measuring the wrong thing — counting pending/processing payments as failures, or there's a metric calculation bug.

**Solution:**
```bash
# In Datadog, inspect the raw metric:
# Metrics Explorer → sum:payments.charge.success{*}
# Check if the metric stopped reporting (gaps in the graph = your app stopped sending metrics,
# not that payments are failing)
```

**Prevention:** Add a "metric not reporting" monitor alongside the rate monitor.

---

#### Bull jobs are stuck in "active" state indefinitely

**Symptom:** `LLEN "bull:payments:active"` is high and not decreasing. Jobs are not completing or failing.

**Cause:** Worker process crashed mid-job without releasing the lock. Bull's stalled job detection will eventually re-queue them (default: 30 seconds), but if workers are all crashed, jobs stay stuck.

**Solution:**
```bash
# Restart the payment worker process in your deployment platform.
# After restart, stalled jobs will be automatically moved back to the wait queue.
# Confirm with:
redis-cli -u $REDIS_URL LLEN "bull:payments:active"
# Should decrease within 60 seconds of worker restart
```

**Prevention:** Configure Bull's `stalledInterval` and `maxStalledCount` in your queue options.

---

#### Idempotency errors stopped but duplicate charges may have occurred

**Symptom:** After resolving idempotency conflicts, a customer reports being charged twice.

**Cause:** Before the retry loop was detected, one or more duplicate charges succeeded (Stripe de-duplication only protects within a 24-hour window for the same key; different keys = different charges).

**Solution:**
```bash
# UNTESTED — search for duplicate charges in your database
psql $DATABASE_URL -c "
  SELECT customer_id, amount, count(*) as charge_count, array_agg(stripe_charge_id) as charges
  FROM payments
  WHERE created_at > NOW() - INTERVAL '2 hours'
    AND status = 'succeeded'
  GROUP BY customer_id, amount
  HAVING count(*) > 1;
"
```

If duplicates are found, **do not issue refunds without confirming with the payments team** — the customer may have legitimately made two purchases.

**Prevention:** Ensure idempotency keys encode both the order ID and a stable attempt number, and that keys are persisted before the Stripe call.

---

#### The procedure was interrupted midway through

**Symptom:** You started the procedure (e.g. paused the queue) and then lost connection, had to hand off, or the alert resolved unexpectedly.

**What to do:**

1. Check the queue state first:
```bash
redis-cli -u $REDIS_URL GET "bull:payments:paused"
# If this returns "1", the queue is still paused — resume it if the issue is resolved
```

2. Check Stripe Dashboard for any in-flight requests at the time of interruption
3. Re-run the Verification checklist from the top to confirm system state
4. Post in #incidents with what state you found and what you did

---

#### Running this procedure twice

**Pausing the queue twice:** Safe — `SET "bull:payments:paused" 1` is idempotent.

**Replaying webhooks twice:** Not safe unless your webhook handler deduplicates by `stripe_event_id`. Check the database for duplicate event IDs before replaying a second time.

---

## Escalation

| Condition | Escalate to | Contact | Expected response time |
|---|---|---|---|
| Stripe status page shows degraded or outage for any component | Stripe support | https://support.stripe.com — open a Priority support case; include your account ID and error logs | Per Stripe SLA (Priority: 1 hour) |
| Stripe API errors exceed 5% for > 10 minutes with no Stripe status page incident | Stripe support | https://support.stripe.com — open Priority case | 1 hour |
| Payment success rate below 80% for > 5 minutes (severe incident) | Payments team lead | #payments-oncall PagerDuty, or direct message payments team lead | Immediate (< 5 min) |
| Duplicate charges confirmed | Payments team lead + Finance | #payments-oncall PagerDuty; also post in #finance-alerts | Immediate (< 5 min) |
| Database query in troubleshooting section returns unexpected results or DB is unreachable | Platform / DBA team | #platform-team PagerDuty | 15 minutes |
| Redis is unreachable (Bull queue inaccessible) | Platform team | #platform-team PagerDuty | 15 minutes |
| Error type is not covered in this runbook and success rate has not recovered after 20 minutes | Payments team lead | #payments-oncall PagerDuty | 15 minutes |
| Payments team lead is unavailable | Engineering manager on-call | Check PagerDuty escalation policy under "payments" service | 15 minutes |

---

## Appendix

### References

- Stripe error codes: https://stripe.com/docs/error-codes
- Stripe webhook events: https://stripe.com/docs/api/events/types
- Stripe idempotency keys: https://stripe.com/docs/api/idempotent_requests
- Bull (Redis queue) documentation: https://github.com/OptimalBits/bull
- Datadog payment monitors: https://app.datadoghq.com/monitors (search "payment")
- This runbook was written without access to application source code — **all commands marked UNTESTED must be verified against your actual codebase before first use**

### Related runbooks

- Refund processing failures (if it exists)
- Redis / Bull queue operations (if it exists)
- Database failover procedure (if it exists)

### Architecture context

Payments flow: Customer browser → Node.js API → Stripe API (charge creation) → Stripe webhook → Node.js webhook handler → PostgreSQL (order update) → Bull job queue (post-payment fulfillment jobs) → Redis.

Alert thresholds: `payment_success_rate < 95%` over 5 minutes, or `stripe_api_error_rate > 2%`. ~$3,400/minute revenue impact at peak.

### Change log

| Date | Change | Author |
|---|---|---|
| 2026-05-01 | Initial version — created from incident retrospective (4 incidents, 45+ min MTTR each) | Payments team |

> **Note to maintainer:** After the first real use of this runbook, update the "Last tested" date in the Overview table and note any commands that needed correction. The goal is for the second incident to take less than 20 minutes.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/16.5 (97%) |
| Evaluated | 2026-05-01 |
| Target duration | 481769 ms |
| Target cost | $1.1255 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Written for a first-timer at 2am — no assumed knowledge of the system, all commands are copy-pasteable with expected output shown | PASS | Prerequisites section lists every tool with login URL and fallback instructions. Configuration table maps every placeholder to its source. Every step includes Action / Expected output / If this fails sub-sections. Commands include expected output blocks (e.g., `{ "status": "ok", "payments": "ok" }` for the health check, `OK` for the Redis SET, `(integer) 1` for DEL). |
| c2 | Includes a decision tree or clear branching logic for different failure modes (API timeout vs card declines vs webhook failures vs idempotency conflicts) | PASS | Step 1 contains an explicit routing table: `StripeConnectionError` / `timeout` → Steps 2a–2c; `card_declined` / `insufficient_funds` → Step 3; `idempotency_key_in_use` → Steps 4a–4d; `webhook` + `failed` → Steps 5a–5c. Each subsequent step begins with 'Follow this step only if Step 1 identified…' |
| c3 | Every diagnostic step includes the exact command or query to run, not just 'check the logs' or 'look in Datadog' | PASS | Most steps include exact copy-pasteable commands: `tail -n 500 /var/log/app/payments.log \| grep -E '"stripe_error"\|"error_code"'`, `redis-cli KEYS "bull:*:meta"`, `psql $DATABASE_URL -c "SELECT stripe_event_id..."`, `curl -sf https://api.yourapp.com/health \| jq .`. Step 2b uses UI navigation for Datadog p99 latency but is the only exception; all other steps have specific syntax. |
| c4 | Includes a rollback or safe revert step for any action that could make the situation worse | PASS | Dedicated Rollback section. Step 4b includes an explicit ⚠ warning before pausing the queue. Step 4d provides the exact resume command `redis-cli -u $REDIS_URL DEL "bull:payments:paused"` with expected output `(integer) 1`. Rollback section also covers configuration rollback and deploy rollback via deployment platform. |
| c5 | Specifies an escalation path with roles and contact method — who to wake up and when, not 'escalate if needed' | PASS | Escalation table lists condition, escalate-to role, contact method, and expected response time for 8 scenarios: e.g., 'Payment success rate below 80% for > 5 minutes → Payments team lead → #payments-oncall PagerDuty → Immediate (< 5 min)'; 'Duplicate charges confirmed → Payments team lead + Finance → #payments-oncall PagerDuty; also post in #finance-alerts → Immediate (< 5 min)'. |
| c6 | Documents how to verify the incident is resolved (what metric to watch, what threshold confirms recovery) | PASS | Dedicated Verification checklist with 6 items including specific thresholds: 'payment_success_rate above 95% for at least 5 consecutive minutes', 'stripe_api_error_rate below 2%', `LLEN "bull:payments:wait"` < 50, last 10 Stripe webhook deliveries green, and a $1 test transaction via Stripe test card 4242 4242 4242 4242. |
| c7 | Covers all four failure modes mentioned — partial credit if 2-3 are covered but one is missing | PARTIAL | All four failure modes are fully covered: Stripe API timeouts (Steps 2a–2c), card declines (Step 3), idempotency key conflicts (Steps 4a–4d), and webhook delivery failures (Steps 5a–5c). Ceiling is PARTIAL per test design. |
| c8 | Includes severity classification or impact assessment so the on-call engineer can judge urgency (the $3,400/minute context should inform this) | PASS | Overview table states 'Risk level: High' and '~$3,400/minute in lost transactions during peak hours; customers cannot complete purchases'. Escalation table includes a 'severe incident' threshold ('Payment success rate below 80% for > 5 minutes') triggering immediate (< 5 min) response. |
| c9 | Output's runbook header states the alert trigger conditions verbatim — payment success rate < 95% over 5 min, OR Stripe API error rate > 2% — and the $3,400/minute business impact, so the on-call knows the urgency immediately | PASS | Overview table: 'Alert: `payment_success_rate < 95%` over 5 minutes **or** `stripe_api_error_rate > 2%`' and 'Business impact: ~$3,400/minute in lost transactions during peak hours'. Both conditions quoted verbatim from the scenario. |
| c10 | Output's decision tree branches on the first observable signal (which alert fired? what's the dominant error code from logs/Datadog?) and routes to one of four specific failure modes — Stripe API timeout, card declines, idempotency conflict, webhook delivery failure | PASS | Step 1 routing table keys on observable error patterns from logs: `"type":"StripeConnectionError"` or `timeout` → Steps 2a–2c; `"code":"card_declined"` → Step 3; `"code":"idempotency_key_in_use"` → Steps 4a–4d; `webhook` + `failed` → Steps 5a–5c. The table is the first action after identifying the failure category. |
| c11 | Output's diagnostic commands are exact and copy-pasteable — e.g. `datadog query payment.errors{service:payment-api} \| sum:1m` or `psql -c "SELECT COUNT(*) FROM payments WHERE status='failed' AND created_at > NOW() - INTERVAL '5 minutes';"` — not 'check the logs' | PASS | Commands include `tail -n 500 /var/log/app/payments.log \| grep -E '"stripe_error"\|"error_code"' \| tail -50`; `ZRANGE "bull:payments:failed" 0 4`; `psql $DATABASE_URL -c "SELECT customer_id, amount, count(*) as charge_count... HAVING count(*) > 1;"`; Datadog log filter strings like `service:payments @stripe.error.code:(card_declined OR insufficient_funds OR do_not_honor)`. |
| c12 | Output's commands each show the expected output / threshold — e.g. 'expected: error count < 50/min in healthy state; if you see 200+/min, this confirms an API outage' | PASS | Every step has an Expected output block: health endpoint shows `{ "status": "ok" }`; Redis SET shows `OK`; Redis DEL shows `(integer) 1`; Bull queue depths show `(integer) 0-50` for wait, with explanatory ranges; curl webhook probe shows `400` with explanation that 400 is correct; Stripe latency threshold stated as 'p99 below 3,000ms'. |
| c13 | Output handles each of the four failure modes with branch-specific diagnostics — Stripe outage (check status.stripe.com, fail-over to retry queue), card declines (check decline code distribution, no rollback needed), idempotency conflicts (check Redis key collisions, clear stuck keys with named command), webhook failures (check Bull queue depth, retry failed webhooks) | PASS | Stripe timeouts: checks status.stripe.com, advises 'do not trigger retries' during degraded state (Steps 2b–2c). Card declines: check rate vs. yesterday, Stripe Radar review for fraud pattern (Step 3). Idempotency: Redis key frequency check, pause queue with `SET "bull:payments:paused" 1`, root cause before resume (Steps 4a–4d). Webhooks: reachability probe, Stripe delivery log with error-code interpretation table, deduplicated replay (Steps 5a–5c). |
| c14 | Output's rollback steps are explicit for any destructive action — e.g. 'if you disable the payment processor, re-enable with `kubectl scale deployment/payment-processor --replicas=3`' | PASS | Rollback section provides `redis-cli -u $REDIS_URL DEL "bull:payments:paused"` with expected output `(integer) 1` and a 2-minute monitoring window. Addresses configuration rollback (secrets manager revert) and deploy rollback ('use your deployment platform's rollback feature to re-deploy the previous release'). Step 4b warns before the destructive pause action. |
| c15 | Output's escalation thresholds are defined — e.g. 'if no resolution after 30 min OR Stripe status page shows incident, page the engineering manager via PagerDuty severity 1' | PASS | Escalation table defines: 'Stripe API errors exceed 5% for > 10 minutes'; 'Payment success rate below 80% for > 5 minutes (severe incident)'; 'Error type not covered and success rate not recovered after 20 minutes → Payments team lead via #payments-oncall PagerDuty'. Each row includes expected response time. |
| c16 | Output's verification step shows what success looks like — payment success rate back above 95% for 10 consecutive minutes, error rate below 0.5%, no new alerts firing — with an illustrative Datadog query in the same syntax style as the diagnostic commands | PARTIAL | Verification section exists with thresholds (95% for 5 minutes, error rate < 2%), but the criterion asks for 10 consecutive minutes and error rate below 0.5% — the runbook uses the alert-trigger values, not tighter recovery values. No Datadog metrics query appears in the verification section (the pre-check section has `sum:payments.charge.success{*} / (sum:payments.charge.success{*} + sum:payments.charge.failed{*})` but verification relies on Datadog Monitors UI navigation, not an explicit query). |
| c17 | Output is written for a first-timer at 2am — every step has a single action, no assumed knowledge of which dashboard or which Redis key, all paths absolute | PASS | Each step has a single Action block, single Expected output, and single If this fails path. Configuration table maps every variable to its source (e.g., `your-redis-host:6379` → 'Secrets manager → prod/payments/redis-url'). Prerequisites section tells the engineer exactly where to log in and what access to request. Steps reference Slack channel names explicitly (#incidents, #deployments, #fraud-and-risk). |

### Notes

The runbook is exceptionally thorough and well-structured for its stated purpose. It passes 15 of 17 criteria fully, with one PARTIAL ceiling (c7, all four failure modes covered) and one earned PARTIAL (c16). The main gap in c16 is that the Verification section uses Datadog Monitors UI navigation rather than a Datadog metrics query, and the recovery thresholds (95% / 2%) mirror the alert-trigger values rather than using tighter confirmation thresholds. The runbook's 'UNTESTED' labelling on all commands is a notable transparency strength — it sets realistic expectations for a first-timer without pretending the commands will work out of the box. The configuration placeholder table is a strong design choice that makes the runbook reusable across environments.
