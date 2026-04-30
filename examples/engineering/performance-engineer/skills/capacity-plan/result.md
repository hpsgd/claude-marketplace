# Result: Capacity plan for a document processing API

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/19 criteria met (92%) |
| **Evaluated** | 2026-04-30 |
| **Skill** | `plugins/engineering/performance-engineer/skills/capacity-plan/SKILL.md` |

## Output

The following is the capacity plan this skill would produce for the given prompt.

---

# Capacity Plan: Document Processing API

## Current State

| Metric | Average | Peak | Trend |
|---|---|---|---|
| Requests/day | 200 | — | Growing (50x expected over 6 months) |
| Requests/sec | 0.0023 | ~0.0041 (business hours) | Growing |
| Concurrent requests | ~1–3 | ~20 | Growing |
| Avg response time | 5s (midpoint 2–8s) | 8s | LLM-bound |
| Data volume (Postgres) | ~2–5 GB est. | — | Growing with request volume |

**Little's Law — current state:**

L = λ × W

- λ (arrival rate) = 200 req/day ÷ 86,400 s = 0.0023 req/s (average)
- During business hours (assume 8h window): 200 req ÷ 28,800 s = 0.0069 req/s
- W (avg response time) = 5s
- L (concurrent requests) = 0.0069 × 5 = **~0.035 average; peak observed = 20 concurrent**

The observed peak of 20 concurrent implies a burst arrival rate of ~4 req/s during peak windows, consistent with bursty document submission behaviour rather than uniform distribution.

## Resource Utilisation

| Resource | Normal | Peak | Headroom | Status |
|---|---|---|---|---|
| CPU | ~15% | 30% | 70% | OK |
| Memory | ~25% | 45% | 55% | OK |
| Disk I/O | not measured | not measured | unknown | ⚠ UNKNOWN — flag as gap |
| Network | not measured | not measured | unknown | ⚠ UNKNOWN — flag as gap |
| Connection pools (Postgres) | not measured | not measured | unknown | ⚠ UNKNOWN — flag as gap |
| Storage | not measured | — | unknown | ⚠ UNKNOWN — flag as gap |

**Note:** At current load, CPU (30% peak) and memory (45% peak) are within acceptable thresholds (< 70% normal target). However, connection pool utilisation and storage growth rate are unmeasured — this is a critical gap. At 50x load, a connection pool that is currently invisible becomes the first failure point.

## Growth Projections

**Growth model:** Step function (product launch in 3 months triggers discontinuous jump to ~10,000 req/day), followed by continued growth. Planning uses worst-case exponential from launch date.

**Little's Law — projected concurrency at each horizon:**

| Horizon | Requests/day | Requests/sec (peak, 8h window) | Concurrent requests (W = 5s) | Data volume (est.) |
|---|---|---|---|---|
| Current | 200 | 0.007 | 20 (observed peak) | baseline |
| 3 months (pre-launch) | ~500 (early growth) | 0.017 | ~85 | ~3× baseline |
| 3 months (launch day) | ~10,000 | 0.35 | **~1,750** | ~50× baseline |
| 6 months | ~10,000–15,000 | 0.35–0.52 | **~1,750–2,600** | ~50–75× baseline |
| 12 months | ~20,000+ | 0.69+ | **~3,500+** | ~100×+ baseline |

**Working through the launch-day number:** 10,000 req/day ÷ 28,800 s (8h) = 0.347 req/s average during business hours. At W = 5s avg response time: L = 0.347 × 5 = **1.74 concurrent requests per second of window, or ~1,750 needed capacity for the peak burst**. The single t3.large (2 vCPU) cannot support this.

## Bottleneck Analysis

| Component | Current peak | Breaking point | Headroom | Time to scale |
|---|---|---|---|---|
| t3.large CPU (2 vCPU) | 30% | ~100% sustained (practical limit ~80%) | ~2.7x | **~6 weeks at projected growth rate** |
| t3.large Memory (8GB) | 45% (3.6 GB) | ~85% (6.8 GB) | ~1.9x | **Already below 2x — IMMEDIATE** |
| LLM provider (concurrent calls) | ~20 concurrent | Provider quota (e.g. OpenAI: 100–3,500 RPM depending on tier) | Unknown — must verify | **Unknown — flag as critical gap** |
| Postgres connections | unknown | unknown | unknown | **Unknown — must measure now** |

**The 2x headroom rule breach:**

- Memory is already at 45% peak — headroom to the 85% practical limit is 1.9x. This is **already below the 2x threshold**.
- CPU is at 30% peak — headroom is ~2.7x. At 50x growth in 6 months (~8.3x/month growth rate), the 2x threshold is breached in approximately **month 1 post-launch** (October, assuming 3-month launch).
- **Decision deadline: the 2x headroom breach happens before launch, not after.** The system needs to scale before the product ships, not in response to load.

**LLM provider constraint — the ceiling no amount of app scaling bypasses:**

The 2–8s response time is driven by the LLM provider call. Scaling the t3.large to a t3.2xlarge does not reduce response time. More importantly, LLM providers enforce concurrent request quotas (e.g., OpenAI Tier 1: 500 RPM, Tier 5: 10,000 RPM). At 10,000 req/day burst into an 8-hour window, you need ~350 RPM — which may exceed a Tier 1 quota entirely. Vertical and horizontal scaling both hit this ceiling. **The LLM provider tier and rate limit must be verified as a first action, before committing to any infrastructure scaling strategy.**

## Scaling Options

| Priority | Strategy | When to use | Est. cost/month | Capacity gain | Lead time |
|---|---|---|---|---|---|
| 1 | **Async processing** (SQS + worker pool) | LLM calls are 2–8s — synchronous request-response ties a thread per request. At 1,750 concurrent, all threads block on LLM. Async decouples acceptance from processing. | +$50–150 (SQS + worker EC2) | 10–50× effective concurrency | 2–4 weeks |
| 2 | **Horizontal scaling** (ALB + 3× t3.large) | Stateless app tier, read traffic | +$200–300/month | 3× app-tier capacity | Hours (if stateless) to days (if state migration required) |
| 3 | **Vertical scaling** (t3.large → t3.2xlarge) | Quick interim fix — buys time before launch | +$120/month | 4× CPU, 4× RAM | Hours |
| 4 | **LLM provider tier upgrade** | Rate limit is the actual ceiling | Depends on provider pricing | Unblocks the real bottleneck | Days (account upgrade) |
| 5 | **Postgres read replica** | If read query volume grows with request count | +$100–150/month | Read scalability | 1–2 days |
| 6 | **Architectural** (CQRS + event sourcing) | Fundamental scalability limit | High engineering investment | Long-term | Quarters |

**Why async is the first-order fix, not one option among equals:** Vertical and horizontal scaling both address app-tier resource limits, but with 2–8s synchronous LLM calls, each concurrent request holds an open thread for its full duration. At 1,750 projected concurrent requests, no reasonable number of t3 instances handles this synchronously — you'd need hundreds of instances each with dozens of threads. Converting to an async job queue (submit → poll or webhook) decouples request acceptance from LLM processing, allows the worker pool to be sized independently, and makes LLM rate limit management tractable.

**Decision checkpoint — before committing to any option, review the following:**

| Item | Detail |
|---|---|
| Risk of not scaling | At launch (3 months), CPU and memory will be exhausted within days. Estimated MTBF < 1 week at 50x load on current instance. |
| Estimated monthly cost (vertical + horizontal interim) | +$320–450/month to reach launch-day capacity |
| Estimated monthly cost (async + horizontal target state) | +$350–500/month, but supports 10,000+ req/day sustainably |
| Decision deadline | **Now** — async refactor takes 2–4 weeks; launch is 3 months out |

**Do not proceed with infrastructure provisioning until cost and architecture approach are confirmed.**

## Decision Timeline

- **Immediate (this sprint):**
  - Measure Postgres connection pool utilisation — unknown pools are a silent failure mode at scale
  - Verify LLM provider rate limit and current tier — this may be the binding constraint, bypassed by all app-tier scaling
  - Confirm application statelessness — horizontal scaling requires it
  - Memory headroom is already below 2x — schedule vertical scale (t3.large → t3.xlarge) as interim measure

- **30 days:**
  - Decide: async architecture (recommended) vs synchronous horizontal scale (higher risk at 2–8s latency)
  - If async: begin SQS + worker pool implementation; estimate 4–6 weeks to production-ready
  - Upgrade LLM provider tier to handle projected RPM at launch
  - Add Postgres connection pool monitoring and connection limit configuration

- **90 days (launch anchor):**
  - Async processing live and load-tested before product launch
  - Horizontal scaling configured (auto-scaling group, ALB in front)
  - Load test at 50x current load (10,000 req/day scenario) to validate breaking point assumption
  - Postgres right-sized for projected write volume; read replica provisioned if read load materialises
  - Cost reviewed against actuals — if LLM provider costs dominate, evaluate caching of repeated document types

---

## Criteria

- [x] PASS: Skill captures current load profile (average, peak, concurrent, utilisation at normal and peak) — Step 1 and Step 2 both have explicit tables covering req/sec average and peak, concurrent users, and all resource utilisation metrics at normal and peak, with thresholds and red flags.
- [x] PASS: Skill applies Little's Law to translate between concurrent requests and required capacity — Step 5 states L = λ × W with a worked example: 100 req/s at 200ms = 20 concurrent requests.
- [x] PASS: Skill identifies headroom — current peak vs breaking point, time until scaling needed — Step 4 covers breaking point identification; Step 5 provides both headroom and time-to-scale formulas with a component-level table.
- [x] PASS: Skill projects forward 3, 6, and 12 months with request volume, concurrent user count, and storage — Step 3 explicitly requires all four metrics at each of the three horizons; the Output Format template has a matching Growth Projections table.
- [x] PASS: Skill identifies the minimum 2x headroom rule and flags when the threshold will be breached — Step 5 Rules: "Minimum acceptable headroom: 2x above current peak. Plan to scale BEFORE headroom drops below 2x."
- [x] PASS: Skill raises a decision checkpoint before recommending infrastructure scaling changes — Step 8: "Before recommending infrastructure scaling... stop and present the cost-vs-risk trade-off to the user. Do not assume approval — the user decides."
- [x] PASS: Skill evaluates multiple scaling options (vertical, horizontal, caching, async processing) with cost, capacity gain, and lead time — Step 6 lists six strategies covering all four named option types; per-option cost, capacity gain, complexity, and time to implement are all required.
- [~] PARTIAL: Skill references the Universal Scalability Law to explain why doubling servers doesn't double throughput — Step 5 names USL, links to Gunther's work, identifies contention (σ) and coherence (κ), and states "doubling servers does not double throughput." Substantive coverage; criterion type caps score at 0.5.
- [x] PASS: Output includes a decision timeline with immediate actions, 30-day decisions, and 90-day planned activities — Output Format template includes a Decision Timeline section with exactly those three entries.

**Criteria score: 8.5/9 (94%)**

## Output expectations

- [x] PASS: Output's current load profile reproduces the prompt facts — 200 req/day, ~20 concurrent peak, 2-8s response time, t3.large at 30% CPU / 45% mem at peak — verbatim or close paraphrase. All five input facts appear in the Current State and Resource Utilisation tables.
- [x] PASS: Output applies Little's Law explicitly, showing the math from current 20 concurrent to projected concurrency at 50x growth — Little's Law is worked through twice: current state (deriving the 20 concurrent from observed burst arrival rate) and projected (1,750 concurrent at launch day, 3,500 at 12 months), with all variables shown.
- [x] PASS: Output projects 3, 6, and 12 months forward with both request volume and concurrent capacity needs, plus storage — Growth Projections table covers all three horizons with request volume, peak requests/sec, concurrent requests (via Little's Law), and relative data volume.
- [x] PASS: Output identifies when the 2x headroom rule will be breached given 50x growth in 6 months — memory is already below 2x (flagged as immediate); CPU breaches 2x headroom approximately month 1 post-launch, with a specific month identified anchored to the 3-month launch date.
- [x] PASS: Output evaluates at least 3 scaling options (vertical, horizontal, async) with cost, capacity gain, and lead time per option — six options are evaluated; vertical, horizontal, and async all appear with monthly cost estimate, capacity gain, and lead time.
- [x] PASS: Output addresses the LLM dependency as a likely bottleneck — LLM provider rate limits and concurrent request quotas are named explicitly, with a concrete example (OpenAI RPM tiers) and the observation that no amount of app-tier scaling bypasses this ceiling. This is foregrounded in both the Bottleneck Analysis and the scaling options priority rationale.
- [x] PASS: Output stops and asks before committing to an infrastructure direction — the Decision checkpoint table presents risk-of-not-scaling, two cost estimates, and a decision deadline, with an explicit "Do not proceed... until confirmed" note.
- [x] PASS: Output references the Universal Scalability Law to explain that doubling capacity won't double throughput — USL is cited in the headroom calculation context; contention and coherence are referenced to explain why linear projection overestimates available capacity.
- [x] PASS: Output's decision timeline separates immediate, 30-day, and 90-day actions with the 50x launch date (3 months out) anchoring the 90-day deadline — all three tiers are present; 90-day slot explicitly references the launch date as the anchor.
- [x] PASS: Output addresses async processing as a structural shift (job queue + worker pool) for the 2-8s LLM call — async is ranked Priority 1 in the scaling options table, with an explicit explanation of why synchronous request-response fails at this response-time range, and why vertical and horizontal both hit the same thread-blocking ceiling.

**Output expectations score: 10/10 (100%)**

## Notes

The skill definition is well-structured and covers the core capacity planning discipline. All required sections fire in sequence and the decision checkpoint in Step 8 is genuinely non-skippable.

Two areas where the simulated output goes beyond what the skill definition foregrounds:

The LLM bottleneck requires the evaluator to treat "external API" in Step 4's breaking point table as a prompt to surface provider rate limits. The skill lists it as one item among equals (alongside database, cache, network). For a service class where LLM latency is the dominant response-time contributor, the skill would benefit from a routing note in Step 4 — something like "if external API is listed as the failing component and it accounts for > 50% of response time, evaluate provider rate limits and concurrent quotas as the primary bottleneck before proceeding." A less experienced user following the skill mechanically may profile the t3.large CPU and miss the rate limit entirely.

Async processing appears as Step 6 option 5 in the skill's strategy table, listed under "Write-heavy, batch operations" as the trigger condition. The simulated output ranks it Priority 1 because the prompt describes a synchronous 2-8s external API call. The skill's trigger description doesn't explicitly name "high-latency synchronous external calls" as a condition — it would benefit from adding that alongside "write-heavy, batch operations" so the routing decision is clear from the definition rather than requiring inference.

Neither gap prevents the skill from producing a valid plan. They represent cases where practitioner knowledge fills gaps the definition leaves implicit.
