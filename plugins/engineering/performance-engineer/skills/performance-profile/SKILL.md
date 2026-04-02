---
name: performance-profile
description: Profile a system or endpoint for performance bottlenecks — measure, identify, and prioritise optimisation targets.
argument-hint: "[endpoint, feature, or code path to profile]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Profile performance for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Baseline Measurement (MANDATORY — no optimisation without a baseline)

Measure current performance. "It feels slow" is not a measurement. `p95 = 2.3s on /api/search with 50 concurrent users` is.

| Metric | How to measure | Record |
|---|---|---|
| **p50 response time** | APM, load test, or application timing | [ms] — typical user experience |
| **p95 response time** | APM or load test | [ms] — worst case for most users |
| **p99 response time** | APM or load test | [ms] — tail latency |
| **Throughput** | Requests per second at current load | [rps] |
| **Error rate** | Percentage of requests returning errors | [%] |
| **Resource utilisation** | CPU, memory, disk I/O, network during test | [%] |

**Rules:**
- Measure under realistic conditions (production-like data, realistic concurrency)
- Record the exact conditions (load, data volume, environment) so measurements are reproducible
- These baseline numbers are your comparison point for every optimisation

### Step 2: End-to-End Timing Breakdown

Where does the total response time go? Break down the waterfall:

| Component | Time (ms) | % of total | Notes |
|---|---|---|---|
| **Network** | [ms] | [%] | DNS, TLS handshake, round trip |
| **Server processing** | [ms] | [%] | Application code execution |
| **Database queries** | [ms] | [%] | Total query time (may include multiple queries) |
| **External API calls** | [ms] | [%] | Third-party service latency |
| **Serialisation** | [ms] | [%] | JSON/XML encoding/decoding |
| **Rendering** (if frontend) | [ms] | [%] | Component rendering, DOM updates |

**The component consuming the most time is the first optimisation target.** Do not optimise a component that accounts for 5% of total time.

### Step 3: Database Profiling

Database queries are the most common bottleneck. Check systematically:

| Problem | How to detect | Impact |
|---|---|---|
| **N+1 queries** | Query count per request (should be < 10). Enable query logging and count | Linear slowdown with data size |
| **Missing indexes** | `EXPLAIN ANALYZE` on slow queries. Sequential scans on large tables | Dramatic slowdown at scale |
| **Full table scans** | Query plan shows Seq Scan on tables with > 10K rows | O(n) instead of O(log n) |
| **Lock contention** | Check for long-running transactions, deadlocks in logs | Cascading delays under concurrency |
| **Unnecessary queries** | Queries that fetch data not used in the response | Wasted time and database load |

```bash
# Check for ORM query patterns (N+1)
grep -rn "\.find\|\.get\|\.query\|\.select\|\.where\|\.include\|\.join" --include="*.ts" --include="*.py" --include="*.cs"

# Check for missing eager loading
grep -rn "lazy\|LazyLoad\|defer\|select_related\|prefetch_related" --include="*.ts" --include="*.py" --include="*.cs"
```

### Step 4: External Call Analysis

Third-party APIs and external services are latency you cannot control — but you can mitigate.

| Check | What to look for | Mitigation |
|---|---|---|
| **Timeouts configured?** | Every external call must have an explicit timeout | Set timeout to 3–5s for non-critical, 10–30s for critical |
| **Circuit breaker?** | Repeated failures should trip a circuit breaker, not keep retrying | Implement circuit breaker pattern |
| **Parallel calls?** | Sequential calls to independent services waste time | Use `Promise.all`, `Task.WhenAll`, `asyncio.gather` |
| **Caching?** | Stable data fetched on every request | Cache with appropriate TTL |
| **Retry logic?** | Retries without backoff cause thundering herd | Exponential backoff with jitter |

### Step 5: Computation Profiling

Profile CPU-bound work:

| Problem | How to detect | Fix |
|---|---|---|
| **O(n²) algorithms** | Nested loops over collections, response time grows quadratically with data | Replace with O(n log n) or O(n) algorithm |
| **Unnecessary serialisation** | JSON.parse/stringify, deep clone on every request | Avoid redundant serialisation, use streaming |
| **Redundant computation** | Same calculation repeated across requests | Memoisation, caching computed values |
| **Synchronous heavy work** | CPU-bound work blocking the event loop or request thread | Move to background worker, use async processing |
| **Regular expression** | Complex regex on large strings (ReDoS risk) | Simplify regex, set input length limits |

**Tools:**
- Node.js: `--prof`, [`clinic.js`](https://clinicjs.org/), [`0x`](https://github.com/davidmarkclements/0x) (flame graphs)
- Python: `cProfile`, [`py-spy`](https://github.com/benfred/py-spy), [`scalene`](https://github.com/plasma-umass/scalene)
- .NET: [`dotTrace`](https://www.jetbrains.com/profiler/), `dotnet-trace`, [`PerfView`](https://github.com/microsoft/perfview)

### Step 6: Resource Analysis Frameworks

Apply these systematic methods to ensure no resource or service is overlooked:

- **[USE Method](https://www.brendangregg.com/usemethod.html)** (Brendan Gregg): For every resource (CPU, memory, disk, network, connection pools), check **U**tilisation (% busy), **S**aturation (queue depth), and **E**rrors (error count). A resource can be at low utilisation but high saturation, which USE catches and ad-hoc monitoring misses.
- **[RED Method](https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/)** (Tom Wilkie): For every service, measure **R**ate (requests/sec), **E**rrors (failed requests/sec), and **D**uration (latency distribution). USE is for infrastructure resources, RED is for request-driven services. Use both together for full coverage.

### Step 7: Resource Contention

Under concurrency, contention creates bottlenecks that don't appear in single-request testing:

| Resource | Symptom | Check | Fix |
|---|---|---|---|
| **Connection pool** | Timeouts waiting for connection | Pool size vs concurrent requests | Increase pool size, reduce query time |
| **Thread pool** | Request queuing, rising latency under load | Thread count vs concurrent requests | Increase threads, move blocking I/O to async |
| **Memory pressure** | GC pauses, OOM errors under load | Memory usage trend during load test | Reduce allocation, increase memory, fix leaks |
| **File descriptors** | "Too many open files" errors | `ulimit -n`, open file count | Increase limits, close connections properly |

### Step 8: Frontend Profiling (if applicable)

| Metric | Target | How to measure |
|---|---|---|
| **Largest Contentful Paint (LCP)** | < 2.5s | Lighthouse, Web Vitals |
| **Interaction to Next Paint (INP)** | < 200ms | Lighthouse, Web Vitals |
| **Cumulative Layout Shift (CLS)** | < 0.1 | Lighthouse, Web Vitals |
| **JavaScript bundle size** | < 200KB gzipped | Bundlesize, webpack-bundle-analyzer |
| **Image optimisation** | WebP/AVIF, lazy loading, responsive sizes | Lighthouse audit |
| **Render blocking resources** | None in critical path | Lighthouse audit |
| **Unnecessary re-renders** | Minimal | React DevTools Profiler, Vue DevTools |

### Step 9: Prioritised Recommendations

Rank optimisations by: **impact (time saved) × frequency (requests affected) / effort (complexity to implement)**.

**Rules:**
- One optimisation at a time — measure after each change
- Measure the SAME metric with the SAME load — apples to apples
- Document what you changed and why — future engineers need the context
- If an optimisation makes code significantly more complex, justify the trade-off

## Anti-Patterns (NEVER do these)

- **Optimising without measuring** — no baseline means no proof of improvement. "It feels faster" is not evidence
- **Guessing bottlenecks** — intuition about bottlenecks is wrong more often than right. Profile, don't guess
- **Changing multiple things at once** — if you change three things and performance improves, you don't know which helped
- **Optimising for average** — p50 tells you about typical users. p95 and p99 tell you about the users most likely to churn
- **Premature optimisation** — if p95 is 50ms, don't optimise. Fix actual bottlenecks, not theoretical ones
- **Ignoring the waterfall** — optimising application code when 90% of time is in database queries is wasted effort

## Output Format

```markdown
# Performance Profile: [target]

## Baseline
| Metric | Value | Target | Status |
|---|---|---|---|
| p50 response | [ms] | < 200ms | PASS/FAIL |
| p95 response | [ms] | < 500ms | PASS/FAIL |
| p99 response | [ms] | < 1s | PASS/FAIL |
| Throughput | [rps] | [target] | PASS/FAIL |
| Error rate | [%] | < 0.1% | PASS/FAIL |

## Timing Breakdown
| Component | Time (ms) | % of total |
|---|---|---|
| [component] | [ms] | [%] |

## Bottlenecks Identified
| # | Component | Problem | Impact | Effort | Priority |
|---|---|---|---|---|---|
| 1 | [component] | [specific issue at file:line] | [time saved] | [complexity] | [High/Medium/Low] |

## Recommendations (ordered by priority)
1. **[Component — issue]** — [specific fix]. Expected improvement: [ms saved, % reduction]
2. **[Component — issue]** — [specific fix]. Expected improvement: [ms saved]

## Next Steps
- [ ] Implement recommendation #1
- [ ] Re-measure baseline after change
- [ ] Proceed to recommendation #2 only after verifying #1
```

## Related Skills

- `/performance-engineer:load-test-plan` — design load tests to reproduce and measure the bottlenecks you've profiled.
- `/performance-engineer:capacity-plan` — feed profiling results into capacity planning to understand scaling limits.
