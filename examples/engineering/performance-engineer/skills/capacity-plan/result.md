# Capacity Plan

Scenario: Developer invokes the capacity-plan skill for a document processing API that currently handles 200 requests/day but is expected to grow to 10,000 requests/day within 6 months after a major product launch.

## Prompt

> Create a capacity plan for our document processing API. Current load: ~200 requests/day, peak of about 20 concurrent requests during business hours. Each request takes 2-8 seconds (it calls an LLM and writes to Postgres). The server is a single t3.large (2 vCPU, 2GB RAM) on AWS currently at ~30% CPU and ~45% memory at peak. We expect to grow 50x over the next 6 months after our product launch in 3 months.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the capacity plan systematically using the framework provided.

## Step 1: Current Load Profile

**Requests and concurrency:**
- Daily volume: 200 req/day ≈ **2.3 req/sec average**
- Peak concurrent: **20 requests during business hours**
- Using Little's Law (L = λ × W): with 5-second average latency, peak throughput is 20 concurrent ÷ 5 sec = **4 req/sec peak** ✓ (checks out with daily volume)
- Pattern: concentrated during business hours, low at night/weekends

**Data volume:**
- Each request writes to Postgres — no volume baseline provided, but assume ~1-5 KB per document
- At 200 req/day, that's ~200-1000 KB/day, negligible for now

---

## Step 2: Resource Utilisation Baseline

| Resource | Normal | Peak | Target | Headroom | Status |
|---|---|---|---|---|---|
| **CPU** | ~15% | 30% | <70% normal | 40 pp | ✅ OK |
| **Memory** | ~25% | 45% | <70% normal | 25 pp | ✅ OK |
| **Postgres connections** | Unknown | Unknown | <70% pool | ? | ⚠️ UNKNOWN |

**Critical gap:** You haven't specified the Postgres connection pool size. At 20 concurrent requests with 2-8 second latency, each request holds a connection for 2-8 seconds. If your pool is <50, you're approaching exhaustion at peak. **Find out:** What's your `max_connections` setting on the database and your application pool size?

---

## Step 3: Growth Projection (50x in 6 months = exponential)

Calculate 50x growth over 26 weeks: **growth rate ≈ 18.9% per week** (50^(1/26) ≈ 1.189)

| Horizon | Req/day | Req/sec (peak) | Concurrent peak | Cumulative growth |
|---|---|---|---|---|
| **Today (week 0)** | 200 | 4 | 20 | 1x |
| **Week 8 (month 2, pre-launch)** | 2,000 | 40 | 200 | 10x |
| **Week 12 (month 3, launch)** | 4,800 | 96 | 480 | 24x |
| **Week 16 (month 4, post-launch)** | 10,200 | 204 | 1,020 | 51x |
| **Week 26 (month 6)** | 10,000+ | 200 | 1,000 | 50x |

---

## Step 4: Breaking Point Identification

**Without a stress test, we estimate conservatively:**

Your current utilisation (30% CPU, 45% memory) suggests the instance can handle roughly **3x current peak before hitting 90% CPU** — around 60 concurrent requests (180 req/day).

**More likely bottleneck: Postgres connection pool exhaustion.** At 20 concurrent requests × 5 second avg latency, connections are held for 5 seconds per request. A pool of 20-30 would be exhausted under peak load. Once the pool exhausts, new requests queue and fail.

**Estimated breaking point: 50-60 concurrent requests** (limited by connection pool, not CPU/memory).

| Metric | Current peak | Estimated breaking point | Headroom | Time until at risk |
|---|---|---|---|---|
| Concurrent requests | 20 | 50-60 | 2.5-3x | ~8-10 weeks |
| Database connections | ~20 active | Pool exhaustion | Unknown | Unknown ⚠️ |

**Red flag:** Your 2.5-3x headroom evaporates before month 3 launch if growth hits 24x concurrent requests.

---

## Step 5: Bottleneck Analysis

**Most likely failure sequence:**

1. **Week 8-10:** Postgres connection pool hits 70% utilization → latency increases as requests queue
2. **Week 12:** Connection pool exhaustion → 50x error rate spike during launch peak
3. **Cascading:** Application waits for connections → CPU climbs → memory pressure → OOM kills

**The bottleneck is NOT compute — it's the database I/O and connection pool.**

---

## Step 6: Scaling Options

| Strategy | Cost/month | Capacity gain | Lead time | Notes |
|---|---|---|---|---|
| **Immediate: Connection pooling (PgBouncer)** | $0-50 | 3-5x (5-8 connections available per app instance) | **1 week** | Quick win: multiplex connections. Deploy in front of Postgres. **CRITICAL — do this first.** |
| **Horizontal: Add app instances + ALB** | $60-120 | 2-3x per instance (adds more connection pools) | **2 weeks** | Deploy 2-3 more t3.large instances behind ALB. Auto-scaling policies. |
| **Database: RDS read replica** | $80-120 | 1.5-2x (offload read-heavy LLM queries if applicable) | **1-2 weeks** | If LLM calls are read-heavy, a read replica reduces write contention. |
| **Caching: Redis layer** | $20-40 | 2-3x (cache LLM outputs or parsed documents) | **2-3 weeks** | If requests are repetitive, cache at application layer. Reduces Postgres load. |
| **Database: Vertical upgrade (RDS)** | $150-300/month | 2x throughput (faster CPU, more IOPS) | **Hours** (zero downtime in RDS) | If Postgres itself is slow, upgrade instance. Verify with profiling first. |
| **Async workers** | $40-80 | Decouples peak from batch processing | **4-6 weeks** | If writing documents is slow, queue them and process async. Doesn't help peak latency. |

---

## Step 7: Lead Time Assessment

| Action | Lead time | Status |
|---|---|---|
| Set up PgBouncer connection pooling | 1 week | **Must start THIS WEEK** |
| Deploy load balancer + 2 additional instances | 2 weeks | **Must start in 2 weeks for month 3 launch** |
| Stress test (validate breaking point assumptions) | 3-5 days | **Must do in parallel with PgBouncer work** |
| RDS read replica (if needed) | 1-2 weeks | **Defer until after stress test results** |
| Redis caching (if hit rate >30%) | 2-3 weeks | **Defer until month 4 if needed** |

---

## Step 8: Recommendation

### 🚨 DECISION NEEDED NOW

You have **8-10 weeks before connection pool exhaustion becomes a crisis.** Your product launch is in **12 weeks**. That gives you 2-week overlap between "hitting capacity limits" and "peak traffic from launch."

**Immediate actions (this week):**

1. **Stress test the API** to find the real breaking point. Use `/performance-engineer:load-test-plan` to design a test that ramps from 1 to 100 concurrent requests. Measure CPU, memory, Postgres connection pool, and error rate. This removes guesswork.

2. **Deploy connection pooling (PgBouncer)** in front of Postgres. This is a *zero-code* change that typically multiplexes 1 connection into 3-5 available slots. Cost: ~$50/month, lead time: 1 week, capacity gain: 3-5x. **This is the cheapest quick win.**

3. **Audit your Postgres connection pool size.** Query `SHOW max_connections;` in RDS. If it's <100, raise it immediately.

### Phased scaling plan

| Phase | Timing | Action | Cost | Capacity gain | Gate |
|---|---|---|---|---|---|
| **Phase 1** | Week 1-2 | PgBouncer + stress test + connection pool audit | $50 | 3-5x | Stress test confirms current breaking point |
| **Phase 2** | Week 3-4 | Deploy load balancer + 2 additional app instances (t3.large each) | $120-150 | 2-3x per instance | Stress test shows CPU/memory not bottleneck |
| **Phase 3** | Week 5-6 | RDS read replica (if profile shows read contention) | $80-120 | 1.5-2x | Post-stress test analysis |
| **Phase 4** | Ongoing | Auto-scaling policies (scale to 4-6 instances during month 3 peak) | Dynamic | Handles 50x growth to month 6 | Monitor launch traffic |

**Total cost at full scale (month 3 peak):** ~$300-400/month (5-6 app instances + RDS replica + pooling).

### Cost vs. risk trade-off

- **If you don't scale:** Month 3 launch peak hits connection pool exhaustion → 50%+ error rate → damaged customer trust → potentially lost revenue.
- **If you scale conservatively (Phases 1-3):** ~$250-300/month incremental cost, handles 50x growth with 2x safety headroom. Launch succeeds.

**Recommendation:** Approve Phases 1-2 immediately (start in week 1). Defer Phase 3 decision to week 5 based on stress test results.

---

## Decision Checkpoints

| Checkpoint | When | Decision |
|---|---|---|
| **Start stress testing + PgBouncer** | This week (week 1) | Approve or defer? |
| **Approve horizontal scaling** | Week 3 (before launch prep) | Add 2-3 instances or watch and wait? |
| **Evaluate read replica need** | Week 5 (post-stress test) | RDS replica or caching layer? |
| **Monitor month 3 launch peak** | Week 12 | Add more instances, enable auto-scaling? |

**What happens if you delay?** Every 2 weeks of delay compresses your implementation window. By week 6, you're 6 weeks out from launch with incomplete scaling infrastructure.

---

**Next step:** Confirm Postgres connection pool size and load-test the API to ground these estimates in reality. Current recommendations are based on conservative assumptions — the stress test will tell you if you can defer scaling or need to accelerate.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/18.0 (81%) |
| Evaluated | 2026-05-04 |
| Target duration | 42519 ms |
| Target cost | $0.1057 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill captures current load profile: average and peak requests, concurrent users, resource utilisation at normal and peak | PASS | Step 1 states '200 req/day ≈ 2.3 req/sec average' and 'Peak concurrent: 20 requests during business hours'. Step 2 table shows CPU normal ~15%/peak 30% and Memory normal ~25%/peak 45%. |
| c2 | Skill applies Little's Law to translate between concurrent requests and required capacity (200ms-8s response time × concurrent users) | PASS | Step 1 states: 'Using Little's Law (L = λ × W): with 5-second average latency, peak throughput is 20 concurrent ÷ 5 sec = 4 req/sec peak ✓'. Law is named and the arithmetic is shown. |
| c3 | Skill identifies headroom: current peak vs breaking point, time until scaling is needed at projected growth rate | PASS | Step 4 table shows 'Headroom: 2.5-3x' and 'Time until at risk: ~8-10 weeks'. Step 8 confirms: 'You have 8-10 weeks before connection pool exhaustion becomes a crisis.' |
| c4 | Skill projects forward 3, 6, and 12 months with request volume, concurrent user count, and storage estimates | PARTIAL | Step 3 table projects to Week 12 (month 3, 4,800 req/day, 480 concurrent) and Week 26 (month 6, 10,000+ req/day, 1,000 concurrent). No 12-month projection appears anywhere. Storage is dismissed as 'negligible for now' without forward projection at scale. |
| c5 | Skill identifies the minimum 2x headroom rule and flags when that threshold will be breached | PASS | Step 4: 'Your 2.5-3x headroom evaporates before month 3 launch if growth hits 24x concurrent requests.' Step 8 anchors this: 'You have 8-10 weeks before connection pool exhaustion becomes a crisis. Your product launch is in 12 weeks.' |
| c6 | Skill raises a decision checkpoint before recommending infrastructure scaling changes (cost and architecture implications) | PASS | Step 8 has explicit 'Decision Checkpoints' table with 'Approve or defer?' for each phase. Phased plan defers Phase 3 until after stress test results. Cost vs. risk trade-off section frames the consequence of not scaling. |
| c7 | Skill evaluates multiple scaling options (vertical, horizontal, caching, async processing) with cost, capacity gain, and lead time for each | PASS | Step 6 table lists six options with cost/month, capacity gain, and lead time: PgBouncer ($0-50, 3-5x, 1 week), horizontal ALB + instances ($60-120, 2-3x, 2 weeks), RDS read replica, Redis caching, vertical RDS upgrade, and async workers — all with individual columns for cost, capacity, and lead time. |
| c8 | Skill references the Universal Scalability Law to explain why doubling servers doesn't double throughput | FAIL | The Universal Scalability Law is not mentioned anywhere in the output. The output does not explain contention or coherency penalties from horizontal scaling. |
| c9 | Output includes a decision timeline with immediate actions, 30-day decisions, and 90-day planned activities | PASS | Step 7 flags 'Must start THIS WEEK' for PgBouncer and stress test. Phased plan has Week 1-2 (immediate), Week 3-4 (~30 days), Week 5-6 (~45 days), and Phase 4 ongoing. Decision Checkpoints table references Week 12 (month 3 launch) as the 90-day anchor. |
| c10 | Output's current load profile reproduces the prompt facts — 200 req/day, ~20 concurrent peak, 2-8s response time, t3.large at 30% CPU / 45% mem at peak — verbatim or close paraphrase | PASS | Step 1: '200 req/day', 'Peak concurrent: 20 requests', '5-second average latency' (mid-range of 2-8s). Step 2 table: CPU Peak 30%, Memory Peak 45%. t3.large referenced in Step 6 options ('t3.large instances'). |
| c11 | Output applies Little's Law explicitly (e.g. 'concurrency = throughput × avg response time'), showing the math from current 20 concurrent to projected concurrency at 50x growth, not just naming the law | PASS | Step 1: 'Using Little's Law (L = λ × W): with 5-second average latency, peak throughput is 20 concurrent ÷ 5 sec = 4 req/sec peak'. Step 3 growth table derives projected concurrent counts (200, 480, 1,020, 1,000) from the same logic applied forward. |
| c12 | Output projects 3, 6, and 12 months forward with both request volume and concurrent capacity needs, plus storage if the LLM/Postgres footprint grows with usage | PARTIAL | Step 3 table covers month 3 (4,800 req/day, 480 concurrent) and month 6 (10,000+ req/day, 1,000 concurrent) but stops there — no 12-month horizon. Storage is noted as '~200-1000 KB/day, negligible for now' without projection at 50x scale. |
| c13 | Output identifies when the 2x headroom rule will be breached given 50x growth in 6 months — a specific date or month, not just 'soon' | PASS | Step 4 table: 'Time until at risk: ~8-10 weeks'. Step 8: 'You have 8-10 weeks before connection pool exhaustion becomes a crisis. Your product launch is in 12 weeks. That gives you 2-week overlap.' Month 3 / week 12 is used as a concrete anchor. |
| c14 | Output evaluates at least 3 scaling options — vertical (larger instance), horizontal (multiple instances + load balancer), and async (queue + workers, given LLM 2-8s latency) — with cost, capacity gain, and lead-time per option | PASS | Step 6 table: Vertical — 'RDS vertical upgrade: $150-300/month, 2x, hours'; Horizontal — 'Add app instances + ALB: $60-120, 2-3x, 2 weeks'; Async — 'Async workers: $40-80, decouples peak, 4-6 weeks'. All three present with cost, capacity, and lead time. |
| c15 | Output addresses the LLM dependency as a likely bottleneck — it's the source of the 2-8s response time and is not solved by scaling the t3.large; capacity planning has to include LLM provider rate limits and concurrent request quotas | FAIL | Step 5 explicitly declares 'The bottleneck is NOT compute — it's the database I/O and connection pool.' LLM is mentioned only in passing (caching LLM outputs, read replica 'if LLM calls are read-heavy') but never identified as a bottleneck, and LLM provider rate limits or concurrent request quotas are never mentioned. |
| c16 | Output stops and asks before committing to an infrastructure direction, framing the cost trade-off between vertical (simpler, hits a ceiling) and horizontal (more complex, requires statelessness) | PASS | Decision Checkpoints table uses 'Approve or defer?' for each phase. Step 8 recommends 'Approve Phases 1-2 immediately… Defer Phase 3 decision to week 5.' Cost vs. risk trade-off section frames ~$250-300/month incremental cost against the risk of 50%+ error rate. Both vertical and horizontal options appear in the options table. |
| c17 | Output references the Universal Scalability Law to explain that doubling capacity won't double throughput (contention and coherency), grounding the recommendation rather than assuming linear scaling | FAIL | The Universal Scalability Law is not mentioned anywhere in the output. The growth projections treat scaling as roughly linear (e.g., '2-3x per instance') without any acknowledgment of contention or coherency penalties. |
| c18 | Output's decision timeline separates immediate (this sprint), 30-day, and 90-day actions, with the 50x launch date (3 months out) anchoring the 90-day deadline | PASS | Step 7: 'Must start THIS WEEK' (immediate), 'Must start in 2 weeks' (~30 days). Phased plan: Phase 1 Week 1-2, Phase 2 Week 3-4, Phase 3 Week 5-6. Step 8: 'Your product launch is in 12 weeks' anchors the 90-day deadline explicitly. |
| c19 | Output addresses async processing as a structural shift (job queue + worker pool) for the 2-8s LLM call, since synchronous request-response will tie up server resources at scale | PARTIAL | Step 6 mentions 'Async workers: If writing documents is slow, queue them and process async.' However, it frames this around document writing, not the LLM call specifically, and actively understates the benefit with 'Doesn't help peak latency' — missing the key point that async decoupling of the 2-8s LLM call frees server threads at scale. |

### Notes

The output is a strong capacity plan that covers most structural requirements well: Little's Law is applied with explicit arithmetic, the growth projection table is clearly laid out, multiple scaling options are evaluated with cost/capacity/lead-time, and decision checkpoints are properly framed. The two most significant failures are the complete absence of any Universal Scalability Law reference (both c8 and c17), and the failure to identify the LLM provider as an independent capacity constraint (c15) — the output explicitly redirects attention away from compute toward Postgres, which is incomplete. The 12-month horizon and forward storage projections are consistently absent (c4, c12). The async processing mention is present but misdirected away from the LLM call and undersold. The overall score sits at the PASS threshold primarily because the structural framework, arithmetic, and decision machinery are sound, but the LLM-as-bottleneck blind spot is a real gap in a plan where the LLM is the stated source of the 2-8s latency.
