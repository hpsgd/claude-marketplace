# Capacity Plan

Scenario: Developer invokes the capacity-plan skill for a document processing API that currently handles 200 requests/day but is expected to grow to 10,000 requests/day within 6 months after a major product launch.

## Prompt

> Create a capacity plan for our document processing API. Current load: ~200 requests/day, peak of about 20 concurrent requests during business hours. Each request takes 2-8 seconds (it calls an LLM and writes to Postgres). The server is a single t3.large (2 vCPU, 2GB RAM) on AWS currently at ~30% CPU and ~45% memory at peak. We expect to grow 50x over the next 6 months after our product launch in 3 months.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the capacity plan systematically using the framework.

## Step 1: Current Load Profile

Converting your metrics:
- **200 req/day** = ~0.002 req/sec average
- **Peak: 20 concurrent, 2-8s response time**
  - Using Little's Law (L = λ × W): 20 concurrent ÷ 5s avg response = **4 req/sec at peak**
  - Peak occurs during business hours (8 hours/day)

## Step 2: Resource Utilisation Baseline

| Resource | Current peak | Target | Status |
|---|---|---|---|
| CPU | 30% | < 70% at normal | ✓ OK |
| Memory | 45% | < 70% at normal | ✓ OK |
| Headroom | 2.3x | 2.0x minimum | ✓ Safe |

**Current status:** Comfortable headroom, but this is **before launch**. The real test comes at month 3+.

## Step 3: Growth Projection (50x over 6 months post-launch)

| Horizon | Req/day | Peak req/sec | Peak concurrent | CPU (extrapolated) |
|---|---|---|---|---|
| Today (month 0) | 200 | 4 | 20 | 30% |
| Launch (month 3) | ~200 | 4 | 20 | 30% |
| Month 6 post-launch | 10,000 | 200 | 1,000 | **1,500%** ❌ |

**Growth model:** Assuming exponential curve, ~2.2x monthly multiplier post-launch.

Critical timeline:
- **Month 3 (launch):** ~200 req/day → manageable
- **Month 5:** ~2,100 req/day → CPU ~120% (exceeds capacity)
- **Month 6:** ~4,600 req/day → CPU ~230% (cascading failures)

## Step 4: Breaking Point Identification

**Critical gap:** No load test data. Your breaking point is unknown. Likely candidates:
1. **Postgres connection pool** — each request holds a connection for 2-8s; at 200 req/sec you need 400-1,600 concurrent connections (t3.large default is often 100-500)
2. **CPU saturation** — t3.large hits 100% around 8-10 req/sec (rough estimate; actual depends on LLM call overhead)
3. **Memory pressure** — 2GB fills quickly under load; kernel OOM killer triggers cascading restarts
4. **LLM API rate limits** — if you're calling a shared LLM endpoint, throughput may be throttled upstream

**Recommendation:** Run a load test NOW (month 1-2) to find the actual breaking point. Don't scale blind.

## Step 5: Headroom Calculation

| Component | Current peak | Estimated breaking point | Current headroom | Time to scale (at 2.2x/month) |
|---|---|---|---|---|
| CPU | 30% | ~90% (7.5 req/sec) | 1.9x | **1 month after launch** |
| Memory | 45% | ~90% (1.8GB) | 1.0x | **Urgent now** |
| Postgres connections | Unknown | 100-500 | Unknown | **CRITICAL GAP** |

**Red flag:** Memory headroom is razor-thin. At 50x growth, you hit swap/OOM within weeks. This is your first bottleneck.

## Step 6: Scaling Options & Cost Impact

| Strategy | Lead time | Cost/month | Capacity gain | Viable? |
|---|---|---|---|---|
| **Vertical (t3.xlarge→ t3.2xlarge)** | 1-2 hours | +$140/mo | 2-3x CPU, 4x memory | ✓ Bridge to month 5 |
| **Horizontal (ALB + 3-4 instances)** | 1-2 days | +$400-500/mo | 3-4x scaling, headroom to month 7 | ✓ Needed by month 4 |
| **Async + queues (SQS → worker pool)** | 2-4 weeks | +$50-150/mo | Decouples peak, allows batching | ✓ Reduces per-request latency variance |
| **Postgres read replicas** | 1 week | +$200-300/mo | Helps read-heavy queries only | ? Need to profile |
| **Connection pooling (PgBouncer)** | 1 day | ~$0 | 5-10x connection multiplier | ✓ Quick win |
| **LLM batching / caching** | 2-3 weeks | ~$0 | Unknown, highly dependent | ? Depends on workload |

## Step 7: Lead Time Assessment

| Decision | Must be made by | Reason |
|---|---|---|
| Load test (measure breaking points) | **Week 1-2 (month 1)** | Results inform all downstream decisions |
| Postgres connection strategy | **Week 2 (month 1)** | Low-cost, high-impact; quick to implement |
| Horizontal scaling plan (ALB + instance count) | **Month 2** | 2-day lead time; decision must precede month 4 traffic spike |
| Async/queue architecture | **Month 2** | 2-4 week lead time; decide now if you want it by month 4 |
| LLM optimization strategy | **Month 2** | Biggest unknown; measure & optimize early |

## Step 8: Recommendation

**Phase 1 (Month 1-2, before launch): Measure & Optimize**
1. **Load test immediately** — stress the current instance to find breaking points. Don't guess.
   - Test concurrent connections, database pool saturation, LLM API throttling
   - Cost: 2-4 hours of engineering
2. **Implement connection pooling** (PgBouncer) — 1-day effort, ~5-10x capacity gain at zero cost
3. **Profile the LLM call path** — is 80% of time spent in the LLM API? If so, batching or caching yields massive wins
4. **Auto-scaling policy** — configure CloudWatch alarms + auto-scale groups (do this before launch)

**Phase 2 (Month 2-3, at launch)**
- Move to **horizontal scaling (2-3 instances behind ALB)** if load testing shows connection pool or CPU limits
- Cost: ~$300-400/month, buys 3-4x capacity
- Headroom extends to month 6-7

**Phase 3 (Month 4-6, post-launch)**
- Monitor headroom weekly; plan next scale event when headroom drops to 1.5x
- If async/batching is viable (depends on use case), implement concurrent request processing via queues
- Evaluate read replicas only after profiling; don't scale the database until you know the bottleneck

**Cost-vs-risk trade-off:**
- **Do nothing:** Free until month 4-5, then cascading failures, lost revenue, angry users
- **Scale now (horizontal):** ~$300/month, overkill before launch, but removes risk and buys development time
- **Phased approach (recommended):** $0 month 1-2 (optimize), +$300/mo month 3-6 (horizontal), +$200/mo month 7+ (replicas if needed). Total: ~$2,400-3,000 over 6 months.

**Critical decision point: Month 2**  
If load test shows CPU/memory is the bottleneck (not connections), approve horizontal scaling by end of month 2. If it shows connection exhaustion, fix with pooling first. If it shows LLM throttling, optimize there instead.

Would you like me to help design the load test (Step 6 → `/performance-engineer:load-test-plan`) or profile the LLM call path to identify optimization opportunities?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/18.0 (83%) |
| Evaluated | 2026-04-30 |
| Target duration | 41328 ms |
| Target cost | $0.0389 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill captures current load profile: average and peak requests, concurrent users, resource utilisation at normal and peak | PASS | Step 1 and Step 2 explicitly state '200 req/day = ~0.002 req/sec average', 'Peak: 20 concurrent, 2-8s response time', 'CPU 30%', 'Memory 45%' in a baseline table. |
| c2 | Skill applies Little's Law to translate between concurrent requests and required capacity (200ms-8s response time × concurrent users) | PASS | Step 1 states 'Using Little's Law (L = λ × W): 20 concurrent ÷ 5s avg response = 4 req/sec at peak' — explicit formula and arithmetic shown. |
| c3 | Skill identifies headroom: current peak vs breaking point, time until scaling is needed at projected growth rate | PASS | Step 5 headroom table shows 'CPU: 1.9x headroom, time to scale: 1 month after launch'; 'Memory: 1.0x headroom — Urgent now'; breaking points stated as ~90% thresholds. |
| c4 | Skill projects forward 3, 6, and 12 months with request volume, concurrent user count, and storage estimates | PARTIAL | Step 3 table projects month 0, month 3 (launch), and month 6 post-launch with request volume and concurrent counts. No 12-month projection is included and no storage estimates for LLM/Postgres footprint growth appear anywhere. |
| c5 | Skill identifies the minimum 2x headroom rule and flags when that threshold will be breached | PASS | Step 2 table shows 'Headroom: 2.3x, Target: 2.0x minimum ✓ Safe'. Step 5 headroom table gives specific breach months: 'CPU headroom 1.9x — Time to scale: 1 month after launch', and 'Month 5: CPU ~120%' in the growth table. |
| c6 | Skill raises a decision checkpoint before recommending infrastructure scaling changes (cost and architecture implications) | PASS | 'Critical decision point: Month 2' section explicitly frames the checkpoint: 'If load test shows CPU/memory is the bottleneck... approve horizontal scaling by end of month 2. If it shows connection exhaustion, fix with pooling first.' |
| c7 | Skill evaluates multiple scaling options (vertical, horizontal, caching, async processing) with cost, capacity gain, and lead time for each | PASS | Step 6 table covers vertical (t3.xlarge→2xlarge), horizontal (ALB + instances), async+SQS, Postgres read replicas, PgBouncer, and LLM batching/caching — each with Lead time, Cost/month, and Capacity gain columns. |
| c8 | Skill references the Universal Scalability Law to explain why doubling servers doesn't double throughput | FAIL | The Universal Scalability Law is not mentioned anywhere in the captured output. The output assumes roughly linear scaling without referencing contention or coherency costs. |
| c9 | Output includes a decision timeline with immediate actions, 30-day decisions, and 90-day planned activities | PASS | Step 7 table lists 'Week 1-2 (month 1)' immediate actions, 'Week 2 (month 1)' and 'Month 2' decisions. Step 8 organises phases: Phase 1 (Month 1-2), Phase 2 (Month 2-3), Phase 3 (Month 4-6), anchored to the 3-month launch date. |
| c10 | Output's current load profile reproduces the prompt facts — 200 req/day, ~20 concurrent peak, 2-8s response time, t3.large at 30% CPU / 45% mem at peak — verbatim or close paraphrase | PASS | Step 1 states '200 req/day', '20 concurrent', '2-8s response time'; Step 2 table shows 'CPU 30%', 'Memory 45%'; server is identified as 't3.large (2 vCPU, 2GB RAM)'. |
| c11 | Output applies Little's Law explicitly (e.g. 'concurrency = throughput × avg response time'), showing the math from current 20 concurrent to projected concurrency at 50x growth, not just naming the law | PASS | Step 1 shows 'L = λ × W: 20 concurrent ÷ 5s avg response = 4 req/sec at peak'. Growth table shows peak concurrent scaling to 1,000 at month 6 (50x of 20), consistent with Little's Law extrapolation. |
| c12 | Output projects 3, 6, and 12 months forward with both request volume and concurrent capacity needs, plus storage if the LLM/Postgres footprint grows with usage | PARTIAL | Step 3 projects month 0, month 3, and month 6 with request volume and peak concurrent. The 12-month horizon is absent entirely. No storage estimates for Postgres or LLM output growth appear in the output. |
| c13 | Output identifies when the 2x headroom rule will be breached given 50x growth in 6 months — a specific date or month, not just 'soon' | PASS | Step 5 headroom table states 'CPU headroom 1.9x — Time to scale (at 2.2x/month): 1 month after launch'. Growth model table pins 'Month 5: ~2,100 req/day → CPU ~120% (exceeds capacity)'. |
| c14 | Output evaluates at least 3 scaling options — vertical (larger instance), horizontal (multiple instances + load balancer), and async (queue + workers, given LLM 2-8s latency) — with cost, capacity gain, and lead-time per option | PASS | Step 6 table includes Vertical (t3.xlarge→2xlarge, +$140/mo, 1-2hr lead), Horizontal (ALB + 3-4 instances, +$400-500/mo, 1-2 day), and Async+SQS (worker pool, +$50-150/mo, 2-4 weeks) — all three required options with all three required attributes. |
| c15 | Output addresses the LLM dependency as a likely bottleneck — it's the source of the 2-8s response time and is not solved by scaling the t3.large; capacity planning has to include LLM provider rate limits and concurrent request quotas | PASS | Step 4 lists 'LLM API rate limits — if you're calling a shared LLM endpoint, throughput may be throttled upstream' as a critical candidate. Step 8 says 'Profile the LLM call path — is 80% of time spent in the LLM API? If so, batching or caching yields massive wins'. |
| c16 | Output stops and asks before committing to an infrastructure direction, framing the cost trade-off between vertical (simpler, hits a ceiling) and horizontal (more complex, requires statelessness) | PARTIAL | The 'Cost-vs-risk trade-off' section frames three options with costs and explicitly labels one 'recommended'. It does not pause to ask the user before committing to the phased direction. The closing question asks about follow-up work (load test, LLM profiling), not which infrastructure path to take. |
| c17 | Output references the Universal Scalability Law to explain that doubling capacity won't double throughput (contention and coherency), grounding the recommendation rather than assuming linear scaling | FAIL | The Universal Scalability Law is not referenced anywhere in the captured output. The growth projections in Step 3 use a simple multiplier model with no acknowledgment of contention or coherency penalties. |
| c18 | Output's decision timeline separates immediate (this sprint), 30-day, and 90-day actions, with the 50x launch date (3 months out) anchoring the 90-day deadline | PASS | Step 7 table lists 'Week 1-2 (month 1)' immediate actions, 'Month 2' for 30-day decisions, and 'Month 2' for 90-day architectural decisions ahead of the month-3 launch. Step 8 Phase structure uses month-3 launch as the anchor. |
| c19 | Output addresses async processing as a structural shift (job queue + worker pool) for the 2-8s LLM call, since synchronous request-response will tie up server resources at scale | PARTIAL | Step 6 includes 'Async + queues (SQS → worker pool)' with 'Decouples peak, allows batching'. Step 8 Phase 3 mentions 'implement concurrent request processing via queues — if async/batching is viable (depends on use case)'. Present but framed as optional/conditional rather than a structural recommendation for the 2-8s LLM latency scenario. |

### Notes

The output is a strong capacity plan that correctly applies Little's Law with arithmetic, projects growth with specific breach months, evaluates 6 scaling options with cost/lead-time, and flags the LLM bottleneck. The two clear gaps are: (1) the Universal Scalability Law (c8, c17) is entirely absent — neither criterion is addressed — representing the largest single scoring loss; (2) no 12-month projection and no storage growth estimates (c4, c12), limiting those to PARTIAL. The output also falls slightly short of 'stopping to ask' before recommending infrastructure direction (c16), instead presenting a 'recommended' phased plan and asking only about follow-up work. Async processing (c19) is present but weakly framed as conditional. Overall the output is technically solid and actionable, earning PASS at 83.3%.
