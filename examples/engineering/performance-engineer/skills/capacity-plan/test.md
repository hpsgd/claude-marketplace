# Test: Capacity plan for a document processing API

Scenario: Developer invokes the capacity-plan skill for a document processing API that currently handles 200 requests/day but is expected to grow to 10,000 requests/day within 6 months after a major product launch.

## Prompt

Create a capacity plan for our document processing API. Current load: ~200 requests/day, peak of about 20 concurrent requests during business hours. Each request takes 2-8 seconds (it calls an LLM and writes to Postgres). The server is a single t3.large (2 vCPU, 2GB RAM) on AWS currently at ~30% CPU and ~45% memory at peak. We expect to grow 50x over the next 6 months after our product launch in 3 months.

## Criteria

- [ ] PASS: Skill captures current load profile: average and peak requests, concurrent users, resource utilisation at normal and peak
- [ ] PASS: Skill applies Little's Law to translate between concurrent requests and required capacity (200ms-8s response time × concurrent users)
- [ ] PASS: Skill identifies headroom: current peak vs breaking point, time until scaling is needed at projected growth rate
- [ ] PASS: Skill projects forward 3, 6, and 12 months with request volume, concurrent user count, and storage estimates
- [ ] PASS: Skill identifies the minimum 2x headroom rule and flags when that threshold will be breached
- [ ] PASS: Skill raises a decision checkpoint before recommending infrastructure scaling changes (cost and architecture implications)
- [ ] PASS: Skill evaluates multiple scaling options (vertical, horizontal, caching, async processing) with cost, capacity gain, and lead time for each
- [ ] PARTIAL: Skill references the Universal Scalability Law to explain why doubling servers doesn't double throughput
- [ ] PASS: Output includes a decision timeline with immediate actions, 30-day decisions, and 90-day planned activities

## Output expectations

- [ ] PASS: Output's current load profile reproduces the prompt facts — 200 req/day, ~20 concurrent peak, 2-8s response time, t3.large at 30% CPU / 45% mem at peak — verbatim or close paraphrase
- [ ] PASS: Output applies Little's Law explicitly (e.g. "concurrency = throughput × avg response time"), showing the math from current 20 concurrent to projected concurrency at 50x growth, not just naming the law
- [ ] PASS: Output projects 3, 6, and 12 months forward with both request volume and concurrent capacity needs, plus storage if the LLM/Postgres footprint grows with usage
- [ ] PASS: Output identifies when the 2x headroom rule will be breached given 50x growth in 6 months — a specific date or month, not just "soon"
- [ ] PASS: Output evaluates at least 3 scaling options — vertical (larger instance), horizontal (multiple instances + load balancer), and async (queue + workers, given LLM 2-8s latency) — with cost, capacity gain, and lead-time per option
- [ ] PASS: Output addresses the LLM dependency as a likely bottleneck — it's the source of the 2-8s response time and is not solved by scaling the t3.large; capacity planning has to include LLM provider rate limits and concurrent request quotas
- [ ] PASS: Output stops and asks before committing to an infrastructure direction, framing the cost trade-off between vertical (simpler, hits a ceiling) and horizontal (more complex, requires statelessness)
- [ ] PASS: Output references the Universal Scalability Law to explain that doubling capacity won't double throughput (contention and coherency), grounding the recommendation rather than assuming linear scaling
- [ ] PASS: Output's decision timeline separates immediate (this sprint), 30-day, and 90-day actions, with the 50x launch date (3 months out) anchoring the 90-day deadline
- [ ] PARTIAL: Output addresses async processing as a structural shift (job queue + worker pool) for the 2-8s LLM call, since synchronous request-response will tie up server resources at scale
