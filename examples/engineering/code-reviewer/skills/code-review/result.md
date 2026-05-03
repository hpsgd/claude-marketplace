# Code Review

Scenario: A senior backend engineer opens a PR adding a token-bucket rate limiter to an Express API. The diff introduces an in-memory Map keyed on IP, removes an existing distributed-rate-limit Redis client, and ships without tests. The README, runbooks, and observability dashboards aren't updated. The reviewer needs to apply the four-pass code-review methodology.

## Prompt

> Review this PR. The author is removing the Redis-backed rate limiter and replacing it with an in-process implementation to "reduce infrastructure dependencies."
> 
> ```typescript
> // src/middleware/rateLimit.ts (new file)
> import type { Request, Response, NextFunction } from 'express'
> 
> const buckets = new Map<string, { tokens: number; lastRefill: number }>()
> const RATE = 100         // tokens per minute
> const CAPACITY = 100
> 
> export function rateLimit(req: Request, res: Response, next: NextFunction) {
>   const key = req.ip
>   const now = Date.now()
>   let bucket = buckets.get(key)
> 
>   if (!bucket) {
>     bucket = { tokens: CAPACITY, lastRefill: now }
>     buckets.set(key, bucket)
>   }
> 
>   const elapsed = (now - bucket.lastRefill) / 60000
>   bucket.tokens = Math.min(CAPACITY, bucket.tokens + elapsed * RATE)
>   bucket.lastRefill = now
> 
>   if (bucket.tokens < 1) {
>     return res.status(429).json({ error: 'rate_limited' })
>   }
> 
>   bucket.tokens -= 1
>   next()
> }
> ```
> 
> ```diff
> // src/app.ts
> - import { redisRateLimit } from './middleware/redisRateLimit'
> + import { rateLimit } from './middleware/rateLimit'
> - app.use(redisRateLimit({ host: process.env.REDIS_HOST }))
> + app.use(rateLimit)
> ```
> 
> The PR description says: "Removes Redis dependency. Same 100/min limit. All existing tests pass."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**PR Review: In-process rate limiter**

**Reject.** The claim "Same 100/min limit" is only true for single-instance deployments. This change silently breaks rate limiting at scale.

---

**Critical: Shared-state loss under horizontal scaling**

With Redis, all instances enforce a shared counter. With this Map, each instance enforces independently. A client can send 100 req/min to *each* instance — `N × 100` effective throughput. The PR description is factually wrong in any multi-instance deployment.

If this service runs behind a load balancer with 3 instances today (or ever will), the rate limiter is effectively dead.

---

**High: Unbounded memory growth**

```typescript
const buckets = new Map<string, { tokens: number; lastRefill: number }>()
```

Nothing evicts stale entries. Every unique IP seen since the process started lives here forever. Redis TTLs handled this automatically. Under normal traffic or any IP-cycling attack, this will grow until OOM.

Minimum fix: evict entries where `now - bucket.lastRefill > 60000` before or after the request.

---

**Medium: State lost on restart**

Process restarts (deploys, crashes) reset all buckets. Clients get a free 100 tokens immediately after every deploy. Redis survived restarts.

---

**On the tests**

"All existing tests pass" is expected — unit tests against a single in-process instance can't observe cross-instance drift. The tests validate the wrong thing for the claimed behavior.

---

**Verdict**

The infrastructure motivation is reasonable (Redis is operational overhead), but the replacement doesn't preserve the contract. If the goal is removing Redis, the right alternatives are:

- A distributed cache with TTL support (Memcached, Upstash, etc.)
- Nginx/gateway-layer rate limiting before the app
- Sticky sessions + this approach, with explicit documentation that it's per-instance

Don't merge as-is.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 5.0/17.5 (29%) |
| Evaluated | 2026-04-30 |
| Target duration | 22755 ms |
| Target cost | $0.0491 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines four passes in sequence — Context, Correctness, Security, Quality — and requires reading full file context not just the diff | FAIL | The output has no structured passes at all. It jumps directly to findings under ad-hoc headings (Critical, High, Medium, Verdict). No mention of Context, Correctness, Security, or Quality passes, and no reference to reading full file context beyond the diff. |
| c2 | Skill distinguishes HARD signals (blockers — will cause wrong behaviour in production) from SOFT signals (important but conditional) | FAIL | The output uses Critical/High/Medium severity labels, not the HARD/SOFT signal terminology the criterion requires. No findings are explicitly categorised as 'HARD' or 'SOFT' signals. |
| c3 | Skill's correctness pass covers logic errors, null/undefined handling, race conditions, edge cases, and error propagation | PARTIAL | The output covers one correctness dimension — scaling logic errors ('each instance enforces independently') and unbounded Map growth (an edge case/resource leak). Race conditions, null/undefined handling, and error propagation are not addressed. No explicit correctness pass is named or structured. |
| c4 | Skill's security pass covers injection, auth/authz, data exposure, and cryptography | FAIL | No security pass exists in the output. Injection, auth/authz, data exposure, and cryptography are not mentioned anywhere. The req.ip spoofing risk (a security concern) is also absent. |
| c5 | Skill includes a friction scan assessing developer experience, debuggability, rollback safety, and feature flag need | FAIL | No friction scan appears in the output. Debuggability, feature flag need, and rollback safety are not discussed. The output briefly mentions the 'infrastructure motivation is reasonable' but this does not constitute a friction scan. |
| c6 | Skill defines a zero-finding gate — if clean, must name a specific positive assertion with file:line to prove review depth | FAIL | No zero-finding gate is defined or referenced anywhere in the output. The concept of naming a positive assertion with file:line to prove review depth is entirely absent. |
| c7 | Skill's output format includes a verdict (APPROVE, REQUEST_CHANGES, NEEDS_DISCUSSION) with a count of blockers, important, and suggestion findings | PARTIAL | The output contains a 'Verdict' section that says 'Reject' / 'Don't merge as-is', which maps to REQUEST_CHANGES, but does not use the canonical terms APPROVE/REQUEST_CHANGES/NEEDS_DISCUSSION, and provides no explicit count of blockers, important findings, or suggestions. |
| c8 | Skill's calibration rules prohibit findings without evidence, findings without fix suggestions, and style preferences not codified in team standards | FAIL | The output does not describe or reference any calibration rules. While findings generally have evidence and fixes in this particular output, the calibration rules themselves are not stated, so the skill cannot be credited with defining them. |
| c9 | Output flags the per-process in-memory Map as a HARD signal — rate limit no longer enforced across instances, won't survive restart, defeats the purpose of rate limiting in any horizontally scaled deployment | PASS | 'Critical: Shared-state loss under horizontal scaling' explicitly flags that each instance enforces independently, giving 'N × 100 effective throughput.' 'Medium: State lost on restart' covers the process-restart concern. Both points are clearly identified as blocking issues. |
| c10 | Output flags the absence of tests as a HARD signal given the change to a security-relevant control, and proposes specific test cases (refill arithmetic, concurrent requests, capacity boundary, IP key collision behind a proxy) | PARTIAL | 'On the tests' section notes that existing tests 'can't observe cross-instance drift' and 'validate the wrong thing.' However, no specific test cases are proposed (no mention of refill arithmetic, concurrent requests, capacity boundary, or IP key collision), and it is not labelled as a HARD/blocker signal. |
| c11 | Output flags `req.ip` as fragile behind a proxy/load balancer — depends on `trust proxy` configuration, can be spoofed via `X-Forwarded-For` if not configured correctly | FAIL | The output never mentions req.ip, trust proxy configuration, or X-Forwarded-For spoofing. The alternatives section mentions 'sticky sessions' but does not discuss the IP-key fragility issue. |
| c12 | Output flags the unbounded `Map` growth as a memory leak — no eviction, every unique IP forever, OOM risk under botnet or large user base | PASS | 'High: Unbounded memory growth' section explicitly states 'Nothing evicts stale entries. Every unique IP seen since the process started lives here forever' and 'Under normal traffic or any IP-cycling attack, this will grow until OOM.' A concrete fix is also suggested. |
| c13 | Output identifies a concurrency / TOCTOU issue — read-modify-write on `bucket.tokens` is not atomic across simultaneous requests on the same Node process | FAIL | The output does not mention TOCTOU, read-modify-write atomicity, or concurrency issues within a single Node.js process. This finding is entirely absent. |
| c14 | Output flags the lack of `Retry-After` header on the 429 response as a friction signal (clients can't back off intelligently) | FAIL | The output does not mention the Retry-After header or client back-off behaviour anywhere. |
| c15 | Output produces a verdict of `REQUEST_CHANGES` or `NEEDS_DISCUSSION` (not APPROVE) with explicit blocker / important / suggestion counts | PARTIAL | The output's Verdict section clearly rejects the PR ('Reject', 'Don't merge as-is'), which corresponds to REQUEST_CHANGES. However, there are no explicit counts of blockers, important findings, or suggestions — only prose describing three alternatives. |
| c16 | Each finding cites a specific file:line and includes a concrete suggested fix (e.g. switch to `express-rate-limit` with Redis store, or document the trade-off and stay with the existing distributed limiter) | PARTIAL | Findings include concrete fix suggestions (eviction snippet, alternatives list including Memcached/Upstash/nginx/sticky sessions). However, no finding cites a specific file:line reference — the code is quoted inline without source attribution. |
| c17 | Output runs an adversarial pass — what happens at 10K req/sec, what happens with one client behind NAT representing 1000 users, what happens during a deploy when in-memory state resets | PARTIAL | 'Medium: State lost on restart' covers the deploy-reset scenario. 'IP-cycling attack' is mentioned under memory growth. The 10K req/sec scenario and the NAT/shared-IP scenario (1000 users appearing as one IP) are not explicitly addressed. |
| c18 | Output flags the missing observability — no logged events, no metrics, no dashboard for rate-limit hits/misses — given this is a security control | FAIL | The output does not mention observability, logging, metrics, or dashboards anywhere. The absence of rate-limit hit/miss instrumentation is entirely unaddressed. |

### Notes

The captured output is a competent informal code review that correctly identifies the two most important issues (cross-instance shared-state loss and unbounded memory growth) and gives a clear reject verdict. However, it completely fails to demonstrate the four-pass code-review methodology the skill is supposed to enforce. Criteria c1–c8 (structural/methodological requirements) almost uniformly fail: no pass structure, no HARD/SOFT taxonomy, no security pass, no friction scan, no zero-finding gate, and no calibration rules. On the content side, several significant findings are missing: req.ip fragility behind a proxy (c11), the TOCTOU/concurrency issue on token read-modify-write (c13), the absent Retry-After header (c14), and missing observability (c18). The output also never cites file:line for any finding, which is a basic review hygiene requirement. The overall score of ~29% reflects a good informal intuition but near-total absence of the structured methodology the skill was designed to enforce.
