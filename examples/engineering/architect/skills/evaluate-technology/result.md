# Evaluate technology skill structure

Checking that the evaluate-technology skill enforces an honest, evidence-based evaluation process — criteria defined before research, weighted scoring with justifications, and a clear recommendation with reconsideration triggers.

## Prompt

> Review the evaluate-technology skill definition and verify it produces a structured, bias-resistant technology comparison.

The evaluate-technology skill, applied to a representative scenario (evaluating Redis Pub/Sub vs. RabbitMQ as a message broker for the FreightFlow notification system), would produce the following output.

---

## Output

# Technology Evaluation: Redis Pub/Sub vs. RabbitMQ

### Evaluation Criteria

Weights defined before research begins, to prevent post-hoc rationalisation.

| Criterion | Weight (1-5) | Why it matters |
|---|---|---|
| Maturity / stability | 4 | Production messaging infrastructure — must be battle-tested |
| Community / ecosystem | 3 | Long-term support, Django libraries available |
| Team familiarity | 5 | Highest weight — unfamiliar tooling adds delivery risk |
| Performance | 3 | At 700 events/minute peak, both candidates handle the load |
| Maintenance burden | 4 | Operational overhead on a small team matters |
| Lock-in risk | 3 | Migration cost if we change later |
| Cost | 2 | Both are open source; hosting cost difference is marginal |
| Integration | 4 | Must integrate cleanly with Django Channels |

---

### Research

#### Redis Pub/Sub


| Field | Value |
|---|---|
| What | In-memory data store with pub/sub messaging. Used for low-latency fan-out. |
| Version | 7.2.4 (stable), February 2024 |
| License | BSD 3-Clause |
| Notable adopters | GitHub, Twitter, Stack Overflow, Shopify, Airbnb |


**Maturity signals:**
- First stable release: 2009
- Release cadence: Minor releases every 3–4 months
- Breaking changes in last 2 major versions: 1 (RESP3 protocol in v6, mostly transparent)

**Community signals:**
- GitHub stars: 63,000
- Stack Overflow: 90,000+ questions, ~85% answer rate
- Active maintainers: Redis Ltd. core team (~15 engineers)

**Known limitations:**
- Fire-and-forget — no message persistence, no delivery guarantees. Offline subscribers miss messages.
- No acknowledgement or retry built in
- Fan-out at very high subscriber counts requires careful connection pooling

#### RabbitMQ


| Field | Value |
|---|---|
| What | Open source message broker implementing AMQP. Designed for reliable, durable messaging with ACKs, routing, and dead-letter queues. |
| Version | 3.13.0 (stable), March 2024 |
| License | Mozilla Public License 2.0 |
| Notable adopters | VMware, Reddit, Mozilla, NASA, Instagram |


**Maturity signals:**
- First stable release: 2007
- Release cadence: Minor releases every 4–6 months
- Breaking changes in last 2 major versions: 2 (management API changes in v3.11, Erlang requirements in v3.12)

**Community signals:**
- GitHub stars: 12,000
- Stack Overflow: 40,000+, ~80% answer rate
- Active maintainers: VMware/Broadcom-backed team (~10 engineers)

**Known limitations:**
- Higher operational complexity — Erlang runtime, management UI, cluster configuration
- AMQP protocol has a learning curve
- Broadcom acquisition (2023) creates uncertainty about long-term stewardship

---

### Scoring Matrix

| Criterion | Weight | Redis Raw | Redis Weighted | RabbitMQ Raw | RabbitMQ Weighted |
|---|---|---|---|---|---|
| Maturity / stability | 4 | 5 | 20 | 5 | 20 |
| Community / ecosystem | 3 | 5 | 15 | 4 | 12 |
| Team familiarity | 5 | 4 | 20 | 2 | 10 |
| Performance | 3 | 5 | 15 | 4 | 12 |
| Maintenance burden | 4 | 4 | 16 | 2 | 8 |
| Lock-in risk | 3 | 4 | 12 | 4 | 12 |
| Cost | 2 | 4 | 8 | 3 | 6 |
| Integration | 4 | 5 | 20 | 3 | 12 |
| **Total** | | | **126** | | **92** |

**Score justifications (one sentence each):**

- Redis maturity (5): 15+ years in production at global scale; no credible stability concerns.
- Redis community (5): Largest in-memory store community; `channels-redis` is the officially supported Django Channels layer.
- Redis team familiarity (4): Team has used Redis for caching — pub/sub is a minor extension of known tooling. Scored 4 not 5 because pub/sub guarantees differ from caching semantics.
- Redis performance (5): Sub-millisecond fan-out for hundreds of events/minute is well within documented envelope.
- Redis maintenance burden (4): Single-process, no runtime dependencies beyond Redis itself. Scored 4 not 5 because `channels-redis` requires version compatibility maintenance.
- Redis lock-in (4): Pub/sub is a commodity pattern; migrating to Redis Streams is straightforward.
- Redis cost (4): Redis Cloud free tier sufficient; self-hosted adds only server cost.
- Redis integration (5): `channels-redis` is the official Django Channels layer — zero custom integration work.
- RabbitMQ maturity (5): 17+ years production use; AMQP is a well-understood standard.
- RabbitMQ community (4): Smaller but active community; Python `pika` client is well-maintained.
- RabbitMQ team familiarity (2): No team experience with RabbitMQ or Erlang; AMQP protocol is a significant learning curve.
- RabbitMQ performance (4): Sufficient at this scale; slight overhead vs. Redis due to AMQP protocol.
- RabbitMQ maintenance burden (2): Erlang runtime, cluster ops, management UI, Broadcom uncertainty — meaningfully higher overhead.
- RabbitMQ lock-in (4): AMQP is a standard; similar reversibility to Redis.
- RabbitMQ cost (3): Hosting cost slightly higher due to Erlang resource usage.
- RabbitMQ integration (3): No official Django Channels integration; requires building a custom channel layer.

---

### Trade-offs

| Choosing Redis Pub/Sub means... | Choosing RabbitMQ means... |
|---|---|
| Fire-and-forget — no persistence or ACKs | Durable messaging with ACKs, dead-letter queues, retry |
| Zero custom integration work (channels-redis is official) | Custom Django Channels layer must be built and maintained |
| Lowest operational overhead — team already knows Redis | Erlang runtime, cluster ops, management UI |
| If delivery guarantees needed later, migrate to Redis Streams | Built-in complex routing, priority queues, durable consumption |

---

### Risks

| Risk | Trigger signal | Mitigation |
|---|---|---|
| Status update lost when subscriber offline | Users report missing notifications; monitoring shows pub/sub drops | Migrate channel layer to Redis Streams for at-least-once delivery |
| Redis single point of failure | Notification feature down during Redis outage | Redis Sentinel or Cluster for HA |
| Broadcom deprecates RabbitMQ | Official end-of-life announcement or fork | N/A — not choosing RabbitMQ |
| Volume spike exceeds capacity | p95 latency > 3s; connection pool exhausted | Redis Cluster; reduce connection pool size |

---

### Recommendation

**Choose: Redis Pub/Sub (via `channels-redis`)**

**Primary reason:** Team already knows Redis, and `channels-redis` is the official zero-integration-work channel layer for Django Channels. At 700 events/minute peak, delivery guarantees are not required.

**What we sacrifice:** Fire-and-forget semantics. If a client disconnects, they may miss status updates. Acceptable for a real-time dashboard (a page refresh shows current state) but not for an audit trail.

**Reconsideration triggers:**
- Delivery guarantee requirements emerge (drivers must never miss a change even when offline)
- Redis stability incidents occur more than once per quarter in production
- Team scales to a point where dedicated message broker expertise exists

---

### Recommended Follow-ups

- [ ] ADR for this decision — real-time transport + message broker is a significant architectural choice
- [ ] Spike: verify `channels-redis` reconnection behaviour when Redis restarts under load
- [ ] Re-evaluate on 2027-01-01 or if concurrent client count exceeds 20,000

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill requires criteria and weights defined before research — Step 1 opens: "Before researching, establish what matters." Rules explicitly state: "Assign weights BEFORE research to prevent post-hoc rationalisation." The phrase "post-hoc rationalisation" is verbatim in the skill definition. The output's criteria table is the first section and explicitly notes weights are pre-research.

- [x] PASS: Skill provides default criteria set including all seven specified criteria — Step 1 table lists: Maturity/stability, Community/ecosystem, Team familiarity, Performance, Maintenance burden, Lock-in risk, Cost, Integration. All seven required criteria present (with Performance as an additional eighth).

- [x] PASS: Skill mandates research brief per option with all specified fields — Step 2 template includes: Version (current stable), License, Notable adopters (3–5), Maturity signals (first stable release, release cadence, breaking changes, open issues), Community signals (GitHub stars, Stack Overflow, active maintainers), and Known limitations. All required fields present in the template.

- [x] PASS: Skill requires weighted scoring matrix with per-score justification — Step 3: matrix shows raw score (1–5) and weighted score per option. Rule: "Every score must have a one-sentence justification — no bare numbers." The output provides 16 one-sentence justifications across both options.

- [x] PASS: Skill requires trade-off table and risk register with trigger signals — Step 4 specifies a trade-off comparison table and a risk register with "Trigger signal" and "Mitigation" columns. Both are present in the output with relevant content.

- [x] PASS: Skill's recommendation states what is sacrificed and reconsideration triggers — Step 5 recommendation template includes "What we sacrifice: [Explicit trade-off acknowledgement]" and "Reconsideration triggers: [Conditions that would change this recommendation]." Both are present in the output.

- [x] PASS: Skill lists anti-patterns including all three specified — Anti-Patterns section lists: "Conclusion-first evaluation — deciding the winner before scoring, then fitting criteria to match," "Popularity as proxy — GitHub stars and npm downloads measure awareness, not quality," and "Binary scoring — scoring everything 1 or 5 defeats the purpose." All three present verbatim.

- [~] PARTIAL: Skill handles tie case with time-boxed spike — Step 5: "If neither option is clearly better, say so — recommend a time-boxed spike or prototype instead of a forced choice." This is present as an explicit instruction in Step 5. PARTIAL ceiling per test author.

### Notes

The tie-case handling is an explicit instruction in Step 5, not merely an anti-pattern footnote. The PARTIAL ceiling is test-author-imposed. The per-score justification requirement is the most valuable bias-prevention mechanism in the skill — 16 one-sentence justifications make the scoring transparent and auditable. The Broadcom/VMware acquisition risk appearing in Known Limitations is a good example of the "search for known limitations" instruction producing domain-relevant output.
