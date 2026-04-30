# Test: code-review skill applied to an Express middleware PR

Scenario: A senior backend engineer opens a PR adding a token-bucket rate limiter to an Express API. The diff introduces an in-memory Map keyed on IP, removes an existing distributed-rate-limit Redis client, and ships without tests. The README, runbooks, and observability dashboards aren't updated. The reviewer needs to apply the four-pass code-review methodology.

## Prompt

Review this PR. The author is removing the Redis-backed rate limiter and replacing it with an in-process implementation to "reduce infrastructure dependencies."

```typescript
// src/middleware/rateLimit.ts (new file)
import type { Request, Response, NextFunction } from 'express'

const buckets = new Map<string, { tokens: number; lastRefill: number }>()
const RATE = 100         // tokens per minute
const CAPACITY = 100

export function rateLimit(req: Request, res: Response, next: NextFunction) {
  const key = req.ip
  const now = Date.now()
  let bucket = buckets.get(key)

  if (!bucket) {
    bucket = { tokens: CAPACITY, lastRefill: now }
    buckets.set(key, bucket)
  }

  const elapsed = (now - bucket.lastRefill) / 60000
  bucket.tokens = Math.min(CAPACITY, bucket.tokens + elapsed * RATE)
  bucket.lastRefill = now

  if (bucket.tokens < 1) {
    return res.status(429).json({ error: 'rate_limited' })
  }

  bucket.tokens -= 1
  next()
}
```

```diff
// src/app.ts
- import { redisRateLimit } from './middleware/redisRateLimit'
+ import { rateLimit } from './middleware/rateLimit'
- app.use(redisRateLimit({ host: process.env.REDIS_HOST }))
+ app.use(rateLimit)
```

The PR description says: "Removes Redis dependency. Same 100/min limit. All existing tests pass."

## Criteria

- [ ] PASS: Skill defines four passes in sequence — Context, Correctness, Security, Quality — and requires reading full file context not just the diff
- [ ] PASS: Skill distinguishes HARD signals (blockers — will cause wrong behaviour in production) from SOFT signals (important but conditional)
- [ ] PASS: Skill's correctness pass covers logic errors, null/undefined handling, race conditions, edge cases, and error propagation
- [ ] PASS: Skill's security pass covers injection, auth/authz, data exposure, and cryptography
- [ ] PASS: Skill includes a friction scan assessing developer experience, debuggability, rollback safety, and feature flag need
- [ ] PASS: Skill defines a zero-finding gate — if clean, must name a specific positive assertion with file:line to prove review depth
- [ ] PASS: Skill's output format includes a verdict (APPROVE, REQUEST_CHANGES, NEEDS_DISCUSSION) with a count of blockers, important, and suggestion findings
- [ ] PASS: Skill's calibration rules prohibit findings without evidence, findings without fix suggestions, and style preferences not codified in team standards

## Output expectations

- [ ] PASS: Output flags the per-process in-memory Map as a HARD signal — rate limit no longer enforced across instances, won't survive restart, defeats the purpose of rate limiting in any horizontally scaled deployment
- [ ] PASS: Output flags the absence of tests as a HARD signal given the change to a security-relevant control, and proposes specific test cases (refill arithmetic, concurrent requests, capacity boundary, IP key collision behind a proxy)
- [ ] PASS: Output flags `req.ip` as fragile behind a proxy/load balancer — depends on `trust proxy` configuration, can be spoofed via `X-Forwarded-For` if not configured correctly
- [ ] PASS: Output flags the unbounded `Map` growth as a memory leak — no eviction, every unique IP forever, OOM risk under botnet or large user base
- [ ] PASS: Output identifies a concurrency / TOCTOU issue — read-modify-write on `bucket.tokens` is not atomic across simultaneous requests on the same Node process
- [ ] PASS: Output flags the lack of `Retry-After` header on the 429 response as a friction signal (clients can't back off intelligently)
- [ ] PASS: Output produces a verdict of `REQUEST_CHANGES` or `NEEDS_DISCUSSION` (not APPROVE) with explicit blocker / important / suggestion counts
- [ ] PASS: Each finding cites a specific file:line and includes a concrete suggested fix (e.g. switch to `express-rate-limit` with Redis store, or document the trade-off and stay with the existing distributed limiter)
- [ ] PASS: Output runs an adversarial pass — what happens at 10K req/sec, what happens with one client behind NAT representing 1000 users, what happens during a deploy when in-memory state resets
- [ ] PARTIAL: Output flags the missing observability — no logged events, no metrics, no dashboard for rate-limit hits/misses — given this is a security control
