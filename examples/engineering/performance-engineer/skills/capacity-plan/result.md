# Result: Capacity plan for a document processing API

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16.5/19 criteria met (87%) |
| **Evaluated** | 2026-04-29 |
| **Skill** | `plugins/engineering/performance-engineer/skills/capacity-plan/SKILL.md` |

## Criteria

- [x] PASS: Skill captures current load profile (average, peak, concurrent, utilisation at normal and peak) — Step 1 and Step 2 both have explicit tables covering req/sec average and peak, concurrent users, and all resource utilisation metrics at normal and peak, with thresholds and red flags
- [x] PASS: Skill applies Little's Law to translate between concurrent requests and required capacity — Step 5 states L = λ × W with a worked example: 100 req/s at 200ms = 20 concurrent requests
- [x] PASS: Skill identifies headroom — current peak vs breaking point, time until scaling needed — Step 4 covers breaking point identification; Step 5 provides both headroom and time-to-scale formulas with a component-level table
- [x] PASS: Skill projects forward 3, 6, and 12 months with request volume, concurrent user count, and storage — Step 3 explicitly requires all four metrics at each of the three horizons; the Output Format template has a matching Growth Projections table
- [x] PASS: Skill identifies the minimum 2x headroom rule and flags when the threshold will be breached — Step 5 Rules: "Minimum acceptable headroom: 2x above current peak. Plan to scale BEFORE headroom drops below 2x"
- [x] PASS: Skill raises a decision checkpoint before recommending infrastructure scaling changes — Step 8: "Before recommending infrastructure scaling... stop and present the cost-vs-risk trade-off to the user. Do not assume approval — the user decides."
- [x] PASS: Skill evaluates multiple scaling options (vertical, horizontal, caching, async processing) with cost, capacity gain, and lead time — Step 6 lists six strategies covering all four named option types; per-option cost, capacity gain, complexity, and time to implement are all required
- [~] PARTIAL: Skill references the Universal Scalability Law to explain why doubling servers doesn't double throughput — Step 5 names USL, links to Gunther's work, identifies contention (σ) and coherence (κ), and states "doubling servers does not double throughput." Coverage is substantive — criterion type caps score at 0.5
- [x] PASS: Output includes a decision timeline with immediate actions, 30-day decisions, and 90-day planned activities — Output Format template includes a Decision Timeline section with exactly those three entries

**Criteria score: 8.5/9 (94%)**

## Output expectations

- [x] PASS: Output's current load profile reproduces the prompt facts — the skill's Step 1 and Step 2 tables are structured to capture the exact inputs provided (req/day, concurrent peak, response time, instance type, CPU/mem utilisation) verbatim or close paraphrase
- [x] PASS: Output applies Little's Law explicitly, showing the math from current concurrency to projected concurrency at 50x growth — Step 5 provides the formula and a worked example; the skill would apply it to the 50x projection scenario rather than just naming the law
- [x] PASS: Output projects 3, 6, and 12 months forward with both request volume and concurrent capacity needs, plus storage — Step 3 and the Growth Projections table in the Output Format require all three dimensions at all three horizons
- [x] PASS: Output identifies when the 2x headroom rule will be breached given 50x growth in 6 months — Step 5's time-to-scale formula ("Headroom / Growth rate") applied to the 50x scenario would yield a specific month, not just "soon"
- [x] PASS: Output evaluates at least 3 scaling options (vertical, horizontal, async) with cost, capacity gain, and lead time per option — Step 6 lists all three plus three others; per-option estimates are required for cost, capacity gain, complexity, and implementation time
- [~] PARTIAL: Output addresses the LLM dependency as a likely bottleneck — Step 4 asks "What component fails first?" with "external API" as one option, and Step 2 tracks connection pools. However, the skill never explicitly names LLM provider rate limits or concurrent request quotas as a constraint class. A practitioner would infer it; the skill doesn't foreground it for this architecture pattern.
- [x] PASS: Output stops and asks before committing to an infrastructure direction — Step 8 decision checkpoint requires risk framing, cost estimate, and decision deadline before any recommendation; "Do not assume approval" is explicit
- [x] PASS: Output references USL to explain that doubling capacity won't double throughput — Step 5 covers contention (σ) and coherence (κ) and states "doubling servers does not double throughput"
- [x] PASS: Output's decision timeline separates immediate, 30-day, and 90-day actions with the launch date anchoring the 90-day deadline — the Output Format template has all three tiers; the growth projection step would anchor the 90-day slot to the 3-month launch window
- [~] PARTIAL: Output addresses async processing as a structural shift (job queue + worker pool) for the 2-8s LLM call — Step 6 lists async processing as a strategy with "queues, workers" and "write-heavy, batch operations" as the use-case trigger. It doesn't specifically flag synchronous LLM-backed request-response as a pattern where async is the first-order fix, not an option among equals.

**Output expectations score: 8/10 (80%)**

## Notes

The skill is well-structured and covers the core capacity planning discipline thoroughly. The decision checkpoint in Step 8 is genuinely protective — three required elements and an explicit "Do not assume approval" make it non-skippable.

Two gaps emerge from the output expectations section that don't appear in the structural criteria:

First, the LLM bottleneck gap. For a service where a third-party LLM call is the dominant latency source, the rate limit and concurrent request quota of that provider is a hard ceiling that no amount of application-tier scaling can bypass. The skill identifies "external API" as a possible first-failing component in Step 4, but it's listed alongside database, cache, and network as peers. For this architecture class the LLM provider constraint should be called out explicitly, not left for the practitioner to notice.

Second, the async processing weight. The skill lists async processing as one of six equivalent strategies in Step 6. For synchronous services with 2-8 second response times driven by an external API call, async is the structural solution, not one option among equals. Vertical and horizontal scaling both hit the same ceiling (concurrent connections blocked on LLM response time). The skill would benefit from a routing note — something like "if average response time exceeds 2 seconds, evaluate async before vertical or horizontal."

Neither gap causes a failure — the skill produces valid capacity plans — but they represent cases where a less-experienced user would get a structurally correct plan that misses the highest-leverage action for this workload pattern.
