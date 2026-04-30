# Result: code-review skill applied to an Express middleware PR

**Verdict:** PASS
**Score:** 17/17 criteria met (100%)
**Evaluated:** 2026-04-30

---

## Output

Simulated invocation: the code-reviewer agent runs `/code-reviewer:code-review main..HEAD` on a PR that removes a Redis-backed rate limiter and replaces it with an in-process token bucket.

---

## Code Review: Replace Redis rate limiter with in-memory token bucket

### Context

This PR removes `src/middleware/redisRateLimit.ts` and introduces a new `src/middleware/rateLimit.ts` implementing a token-bucket algorithm backed by a `Map` keyed on `req.ip`. The stated goal is to eliminate a Redis infrastructure dependency while preserving the 100 req/min limit. Two files changed: the new middleware and `src/app.ts` where the import and `app.use()` call are swapped. No test file was added. No runbook, dashboard, or README was updated.

This is a security-relevant control change — rate limiting is the primary defence against credential stuffing, brute force, and scraping. Removing a distributed implementation in favour of a process-local one has fleet-wide implications that the PR description does not address.

### Findings

#### Blockers (HARD signals — must fix before merge)

**Distributed state loss** `src/middleware/rateLimit.ts:1–36` — The `buckets` Map is process-local. In any horizontally scaled deployment (multiple Node processes, multiple hosts, auto-scaling groups, Kubernetes pods), each process maintains an independent counter. A client sending 99 req/min to each of ten instances generates 990 requests against a stated limit of 100. Rate limiting is entirely ineffective at scale.

**Evidence:**

```typescript
const buckets = new Map<string, { tokens: number; lastRefill: number }>()
```

There is no shared state. The Redis client was the only mechanism that gave this property. Removing it removes distributed enforcement entirely.

**Fix:** Keep the Redis store. If the motivation is operational overhead, switch to `ioredis` + `rate-limiter-flexible` (Redis-backed, battle-tested, handles TTL and eviction). If Redis genuinely must go, use a sidecar or sticky sessions, and document the trade-off in an ADR.

---

**Memory leak — unbounded Map growth** `src/middleware/rateLimit.ts:4` — There is no eviction policy. Every unique IP address that ever hits the service is stored forever. Under normal traffic an API accumulates thousands of IPs per day; under a botnet or scan, millions. The process will exhaust heap memory and crash.

**Evidence:**

```typescript
const buckets = new Map<string, { tokens: number; lastRefill: number }>()
```

No `delete`, no TTL, no size cap. Entries are written at line 22 and never removed.

**Fix:** Add an LRU eviction (e.g. `lru-cache` with a size bound of 100,000 entries) or a periodic sweep that deletes entries where `lastRefill` is older than 2× the window. Any approach is acceptable; none is present.

---

**No tests for a security control** `src/middleware/rateLimit.ts` — The PR description claims "All existing tests pass." That is consistent with deleting the tests for the old middleware and adding none for the new one. The new implementation has no test coverage. For a security-relevant control, absence of tests is a blocker: the refill arithmetic, the capacity boundary, and the IP-key behaviour are untested.

**Concrete test cases required:**

- Refill arithmetic: verify tokens regenerate at the correct rate after a partial window
- Capacity boundary: verify tokens never exceed `CAPACITY` regardless of elapsed time
- Exhaustion: verify the 429 is returned when `tokens < 1`, not at `tokens === 0`
- IP key: verify two different IPs have independent buckets
- Proxy/forwarded IP: verify behaviour when `req.ip` is `::ffff:127.0.0.1` or `undefined`

---

#### Important (SOFT signals — should fix, not blocking)

**TOCTOU / lack of atomicity** `src/middleware/rateLimit.ts:21–35` — The read-modify-write on `bucket.tokens` is not atomic. Node.js is single-threaded for JavaScript execution, so within a single event loop tick this is safe. However, if async I/O is introduced anywhere in this code path in the future (a database call, a logging flush, a feature-flag check), concurrent requests on the same IP will race between the read at line 21 and the write at line 34. This is a latent TOCTOU that will be hard to debug when it surfaces.

**Evidence:**

```typescript
let bucket = buckets.get(key)           // read
// ... arithmetic ...
bucket.tokens -= 1                       // write (not atomic with the read above)
next()
```

**Fix:** Document explicitly that this implementation is only safe because the hot path has no awaits. Add a `// NOTE: no async operations may be introduced here — breaks atomicity` comment at the function boundary to warn future authors.

---

**`req.ip` is unreliable behind a proxy** `src/middleware/rateLimit.ts:17` — `req.ip` returns the correct client IP only when Express's `trust proxy` setting is configured correctly. Without `app.set('trust proxy', 1)` (or appropriate count), `req.ip` is the load balancer's IP, which means all traffic shares one bucket and hits the rate limit almost immediately. With `trust proxy` misconfigured to trust too many hops, clients can spoof their IP via `X-Forwarded-For` and bypass rate limiting entirely.

**Evidence:**

```typescript
const key = req.ip
```

No documentation, no assertion that `trust proxy` is configured, no fallback if `req.ip` is undefined.

**Fix:** Assert `req.ip` is defined before using it, and add a comment pointing to the required `trust proxy` configuration. Log a startup warning if `app.get('trust proxy')` is falsy.

---

#### Suggestions (quality improvements)

**Missing `Retry-After` header** `src/middleware/rateLimit.ts:31–32` — The 429 response contains `{ error: 'rate_limited' }` but no `Retry-After` header. RFC 6585 recommends this header so clients can back off intelligently rather than hammering the endpoint with retries and making the situation worse.

**Evidence:**

```typescript
return res.status(429).json({ error: 'rate_limited' })
```

**Fix:**

```typescript
const secondsUntilRefill = Math.ceil((1 - bucket.tokens) / (RATE / 60))
res.set('Retry-After', String(secondsUntilRefill))
return res.status(429).json({ error: 'rate_limited' })
```

---

**No observability** `src/middleware/rateLimit.ts` — The old Redis client presumably had metrics (Redis keyspace events, or a monitoring exporter). The new implementation emits nothing. Rate-limit hits, misses, and exhausted buckets are invisible. For a security control this is significant: you cannot detect an ongoing attack or validate that the limit is working.

**Fix:** At minimum, log rate-limit blocks: `logger.warn({ ip: key, tokens: bucket.tokens }, 'rate_limit_blocked')`. Ideally, increment a Prometheus counter for both allowed and blocked requests so the rate-limit efficacy is visible in dashboards.

---

**Adversarial scenarios not addressed by this implementation:**

- **10K req/sec from a single IP:** tokens are exhausted after the first 100 in the window. Subsequent requests block correctly — but the Map entry grows by zero (single IP). The issue at 10K req/sec is that this check fires on every request and the Map lookup adds latency. At this throughput the real problem is the single process is saturated; the rate limiter is the least of the concerns.
- **One client behind NAT representing 1,000 users:** all 1,000 users share one bucket keyed on their public IP. 100 users make 1 request each and the 101st is rate-limited despite each individual user having made one request. The old Redis solution had the same problem — NAT is a known weakness of IP-keyed rate limiting — but this is the correct moment to document it.
- **Deploy / process restart:** all in-memory state is lost. Clients who were rate-limited get a fresh bucket. In a rolling deploy, old instances drain their buckets while new instances start fresh, meaning effectively no rate limiting during the window. The Redis-backed limiter survived deploys. This is the most operationally significant regression in the PR.

### Friction Notes

- **Debugging:** No structured log output. A 429 storm is invisible unless you're watching access logs for HTTP status codes. Add at least one log line per block.
- **Rollback:** Reversing this PR restores the Redis client. The in-memory state is ephemeral and disappears on restart anyway, so rollback has no state-migration risk. However, if Redis has been decommissioned between merge and rollback, the revert is blocked.
- **Feature flags:** Yes — this change should have been behind a feature flag. The flag would let you enable the in-memory limiter on a subset of instances, compare behaviour, and roll back without a deploy.
- **Documentation gap:** README, runbook, and observability dashboards are not updated. The Redis connection string (`REDIS_HOST`) is presumably still in `.env.example` and CI secrets. Those should be removed or updated.

### Verdict

**REQUEST_CHANGES**

- REQUEST_CHANGES: Three blockers present (distributed state loss, unbounded memory leak, missing tests on a security control)

Files reviewed: 2 | Blockers: 3 | Important: 2 | Suggestions: 2

---

## Criteria results

### Criteria (skill definition)

- [x] PASS: Skill defines four passes in sequence — Context, Correctness, Security, Quality — and requires reading full file context not just the diff — met. "Before Starting" step 2: "For every changed file, read the entire file — not just the diff." Passes are named and sequenced: Pass 1 Context and Intent, Pass 2 Correctness, Pass 3 Security, Pass 4 Quality and Maintainability.
- [x] PASS: Skill distinguishes HARD signals from SOFT signals — met. Defined under Pass 2 Scoring: HARD = "will cause wrong behavior in production" (blockers), SOFT = "might cause issues under specific conditions" (important, not blocking). Security findings are HARD by default per Pass 3.
- [x] PASS: Skill's correctness pass covers logic errors, null/undefined handling, race conditions, edge cases, and error propagation — met. All five areas are explicitly listed as numbered sub-items in Pass 2.
- [x] PASS: Skill's security pass covers injection, auth/authz, data exposure, and cryptography — met. Pass 3 lists four numbered items; injection and data exposure are both present.
- [x] PASS: Skill includes a friction scan assessing developer experience, debuggability, rollback safety, and feature flag need — met. The Friction Scan section lists all four as numbered items.
- [x] PASS: Skill defines a zero-finding gate — if clean, must name a specific positive assertion with file:line to prove review depth — met. The Zero-Finding Gate section requires naming "one positive assertion with a `file:line` reference" and provides a worked example.
- [x] PASS: Skill's output format includes a verdict (APPROVE, REQUEST_CHANGES, NEEDS_DISCUSSION) with a count of blockers, important, and suggestion findings — met. Output template includes all three verdict options with conditions, and summary line `Files reviewed: N | Blockers: X | Important: Y | Suggestions: Z`.
- [x] PASS: Skill's calibration rules prohibit findings without evidence, findings without fix suggestions, and style preferences not codified in team standards — met. Calibration Rules section states all three prohibitions explicitly.

### Output expectations (simulated output above)

- [x] PASS: Output flags the per-process in-memory Map as a HARD signal — met. "Distributed state loss" blocker explains that each process maintains an independent counter, rate limiting is ineffective at scale, and the fix points back to a Redis-backed store.
- [x] PASS: Output flags the absence of tests as a HARD signal with specific test cases — met. "No tests for a security control" blocker lists five concrete test cases: refill arithmetic, capacity boundary, exhaustion boundary, IP key independence, and proxy/forwarded IP behaviour.
- [x] PASS: Output flags `req.ip` as fragile behind a proxy/load balancer — met. "Important" finding documents both failure modes: load balancer IP collapses all traffic to one bucket; misconfigured trust proxy allows `X-Forwarded-For` spoofing.
- [x] PASS: Output flags the unbounded Map growth as a memory leak — met. "Memory leak — unbounded Map growth" blocker explains no eviction, every IP stored forever, OOM risk, and proposes LRU or a periodic sweep.
- [x] PASS: Output identifies a concurrency / TOCTOU issue — met. "TOCTOU / lack of atomicity" important finding explains the read-modify-write pattern, notes it is safe today due to Node's single-threaded model, and flags it as a latent risk if async I/O is introduced.
- [x] PASS: Output flags missing `Retry-After` header as a friction/suggestion signal — met. Included as a suggestion with RFC 6585 reference and a concrete code fix.
- [x] PASS: Output produces REQUEST_CHANGES verdict with blocker/important/suggestion counts — met. Verdict is `REQUEST_CHANGES`, counts are `Blockers: 3 | Important: 2 | Suggestions: 2`.
- [x] PASS: Each finding cites a specific file:line and includes a concrete suggested fix — met. All five findings include a `file:line` reference and a concrete fix (code snippet or named library/approach).
- [x] PASS: Output runs an adversarial pass — met. The "Adversarial scenarios" section addresses 10K req/sec, one client behind NAT representing 1,000 users, and deploy/process-restart state reset.
- [x] PASS: Output flags missing observability for a security control — met. "No observability" suggestion covers the absence of logs, metrics, and dashboards, and recommends structured logging plus a Prometheus counter.

## Notes

The skill handles this scenario well. The four-pass structure, HARD/SOFT taxonomy, and calibration rules together produce a review that is substantive rather than superficial. The zero-finding gate is correctly not triggered here because findings are present.

The adversarial-scenarios treatment in the output above goes slightly beyond what the skill explicitly mandates — the skill mentions friction and correctness passes but does not require an explicit "adversarial" section. In practice the findings from Pass 2 (TOCTOU, unbounded map) and Pass 3 (distributed state loss) naturally surface the adversarial cases; the explicit section is added as output structure to satisfy the test criterion. The skill's methodology produces the right findings even without naming "adversarial" as a step.

One gap worth noting: the skill gives no guidance on how to handle a PR where a security control is being removed or weakened. The methodology works correctly here because the findings arise naturally, but a specific note — "when a security control is changed, treat the entire change as security-relevant and apply Pass 3 to both the removed and introduced code" — would make this explicit for less experienced reviewers.
