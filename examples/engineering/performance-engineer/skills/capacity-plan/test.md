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
