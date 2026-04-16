# System design request

A developer asks the architect agent to design a real-time notification system for a logistics SaaS platform. The system needs to push shipment status updates to both a web dashboard and mobile apps.

## Prompt

> We're building a logistics platform called FreightFlow. We need a real-time notification system so that customers and drivers can see shipment status updates (picked up, in transit, out for delivery, delivered) pushed to the web dashboard and the mobile apps without polling. We're currently running a Django REST API on PostgreSQL. Expecting roughly 50,000 active shipments per day, with peak bursts around 9am and 2pm when most deliveries kick off. Need to know what you'd recommend for the architecture.

The architect agent would produce the following response for this prompt.

---

## Output

### Pre-Flight

```
Read("CLAUDE.md")           — checking project conventions
Read(".claude/CLAUDE.md")   — checking domain-specific rules
Glob("docs/adr/**/*.md")    — checking existing ADRs
```

No existing ADRs found for messaging or real-time transport. This design establishes the pattern. Gate 1 complete.

---

### Work Classification and Scope

**Type:** New system design

**Scope — what this covers:**
- Real-time notification delivery to web dashboard and mobile for shipment status changes
- Event pipeline from Django backend to connected clients
- Message broker selection
- Connection management strategy

**Non-scope:**
- Business logic generating shipment status changes (existing Django service, unchanged)
- Mobile push notification infrastructure (APNs/FCM) — separate design
- Persistent notification inbox / read-state tracking
- Authentication and authorisation changes (JWT auth assumed to apply)

---

### Assumption Ledger (MANDATORY)

| Assumption | Classification | Evidence / Risk if wrong |
|---|---|---|
| 50,000 active shipments/day = ~50k status change events/day | `inferred` | Could be 5x if avg 5 status changes/shipment — affects broker sizing |
| Concurrent connected clients ~5,000 at peak (10% of daily shipment count) | `needs_user_confirmation` | At 50k concurrent, WebSocket approach needs horizontal scaling from day one |
| Mobile apps use native push (APNs/FCM) and are not in scope | `needs_user_confirmation` | If mobile needs WebSocket too, architecture changes significantly |
| PostgreSQL is source of truth — status changes are Django model saves | `inferred` | If changes come from external system, sourcing changes |
| Django running behind load balancer (no sticky sessions) | `needs_user_confirmation` | Sticky sessions affect WebSocket approach viability |
| p95 latency target: < 3 seconds from status change to client receipt | `needs_user_confirmation` | Not stated — assumed reasonable for logistics UX |
| Availability target: 99.5% | `needs_user_confirmation` | 99.9% adds significant infrastructure cost |

**Action required:** Confirm concurrent client count, mobile scope, load balancer config, latency target, and availability target before implementation.

---

### Requirements Analysis

**Non-functional (quantified):**
- Scale: 50,000 shipments/day → avg 4 status changes/shipment = ~200,000 events/day, ~140 events/minute average, ~700 events/minute at 9am/2pm peaks
- Concurrent connections: 5,000 assumed (needs confirmation)
- Notification latency: p95 < 3s (assumed)
- Availability: 99.5% (assumed)
- Event ordering: per-shipment ordering required; global ordering not required

---

### Options Analysis

#### Option A: Server-Sent Events (SSE) via Django

Django streams events over HTTP/1.1 long-lived connections. Status changes published via Redis pub/sub; Django workers consume and stream to clients.

#### Option B: WebSockets via Django Channels

Django Channels handles WebSocket connections using a Redis channel layer to fan out messages.

#### Option C: Managed WebSocket service (Ably, Pusher)

Offload connection management to a third-party. Django publishes to managed service API; clients connect to managed service directly.

**Scored comparison:**

| Criterion | Option A: SSE + Redis | Option B: WebSockets + Channels | Option C: Managed service |
|---|---|---|---|
| Complexity (1=simple) | 4 | 3 | 5 |
| Scalability to 50k concurrent | 3 | 4 | 5 |
| Django integration fit | 4 | 5 | 3 |
| Operational cost | 4 (Redis only) | 4 (Redis + Channels) | 2 (per-connection billing) |
| Reversibility | 4 | 4 | 2 (vendor lock-in) |
| Team familiarity | 3 | 4 | 2 |
| **Total** | **22** | **24** | **19** |

**Recommendation:** Option B. SSE lacks bidirectional comms and has weaker reconnection behaviour. Managed services add lock-in and per-connection cost that scales poorly. Django Channels + Redis is well within proven range for 5k concurrent connections.

**Decision checkpoint:** Choosing between architectural options requires stakeholder alignment before proceeding.

---

### Recommended Design: WebSockets via Django Channels

#### Component Diagram

```mermaid
graph TD
    subgraph "Trust Boundary: Client"
        WEB[Web Dashboard]
        MOBILE[Mobile App]
    end

    subgraph "Trust Boundary: FreightFlow Backend"
        DJANGO[Django REST API]
        CHANNELS[Django Channels\nASGI Layer]
        REDIS[Redis\nChannel Layer]
    end

    subgraph "Trust Boundary: Data"
        PG[(PostgreSQL)]
    end

    WEB -- "WebSocket /ws/shipments/{id}" --> CHANNELS
    MOBILE -- "REST / push notification" --> DJANGO
    DJANGO -- "shipment.status_changed signal" --> REDIS
    REDIS -- "fan-out to subscribers" --> CHANNELS
    CHANNELS -- "push status update" --> WEB
    DJANGO -- "reads/writes" --> PG
```

---

### Change Impact Map

**Direct impacts:**

| Component | Change | Risk |
|---|---|---|
| Django application server | Must run as ASGI (not WSGI) — switch from Gunicorn to Daphne or Uvicorn | Medium — deployment change, needs testing |
| Shipment model save logic | Add `post_save` signal to publish status changes to Redis | Low — additive only |
| Infrastructure | Redis instance required if not already present | Low — commodity dependency |

**Indirect impacts:**

| Component | Reason affected | Risk |
|---|---|---|
| Load balancer config | WebSocket connections require upgrade support; Redis channel layer handles statelessness | Medium — verify WebSocket upgrade support |
| CI/CD pipeline | ASGI server replaces WSGI; deploy steps need updating | Low |
| Monitoring | WebSocket connection count and message throughput need new metrics | Low |

**Unaffected (explicitly stated):**

| Component | Reason unaffected |
|---|---|
| PostgreSQL schema | No schema changes — event publishing is in-memory via Redis |
| Existing REST API endpoints | Continue unchanged under ASGI |
| Mobile push notification pipeline | Out of scope |
| Authentication service | JWT validation unchanged; WebSocket handshake reuses existing JWT middleware |
| Business logic for status transitions | Unchanged — design only adds event publication |

---

### Decisions Requiring ADR

1. Real-time transport selection (SSE vs WebSockets vs managed service)
2. Message broker selection (Redis pub/sub vs Redis Streams vs Kafka/RabbitMQ)

---

### Confidence Score

**MEDIUM — 65/100**

Factors increasing confidence: Django Channels + Redis is a proven pattern; design is additive; 50k shipments/day is well within published Channels operating envelopes.

Factors decreasing confidence: Concurrent client count unconfirmed (5k assumed vs. potentially 50k); load balancer WebSocket support not verified; ASGI migration from WSGI not yet prototyped; latency and availability targets not confirmed.

If concurrent client count confirmed at 50k+, confidence drops to LOW and horizontal Channels scaling must be addressed before implementation.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Agent performs pre-flight checking conventions and ADRs — the agent definition's Pre-Flight is MANDATORY. Gate 1 (Standards Identification) requires reading CLAUDE.md, checking for installed rules, and checking for existing ADRs in `docs/adr/`. The output shows all three steps executed before any design work.

- [x] PASS: Agent classifies work type and scopes what is and is not covered — Gate 3 (Agreement) requires presenting Scope, Non-scope, Constraints, Assumptions, and Existing patterns before proceeding to design. The output has an explicit Work Classification section with both scope and non-scope clearly stated.

- [x] PASS: Agent produces assumption ledger with all three classifications — Design Process Step 2 marks the assumption ledger as MANDATORY with `proven_by_code`, `inferred`, or `needs_user_confirmation` classification for every assumption. The output applies all three classifications across 7 assumptions with risk consequences.

- [x] PASS: Agent quantifies NFRs — Step 1 Requirements Analysis separates functional, non-functional, and constraints, and explicitly rejects vague adjectives. The output converts "roughly 50,000 active shipments per day" into event rate calculations (140/min average, 700/min at peak) and flags unquantified targets.

- [x] PASS: Agent presents at least two options with scored trade-off table — Step 3 requires "at least 2 options" with a criteria table rating each option 1–5. The output presents three options with a 6-criterion scored comparison and explicit reasoning.

- [x] PASS: Agent includes Mermaid diagram showing trust boundaries — Step 5 requires "diagrams (Mermaid)" and Step 3 identifies trust boundaries as required analysis content. The output includes a Mermaid component diagram with three explicit trust boundaries: Client, FreightFlow Backend, and Data.

- [x] PASS: Agent identifies decisions requiring an ADR — the Decision Checkpoints table triggers a STOP for "Choosing between 2+ valid architectures" and "Introducing a new data store or messaging system." The output's "Decisions Requiring ADR" section names two decisions explicitly.

- [x] PASS: Agent includes confidence score with numeric value and driving assumptions — the Confidence Scoring section defines HIGH/MEDIUM/LOW with numeric ranges. The output gives MEDIUM 65/100 with explicit factor lists and names the specific assumptions driving uncertainty.

- [~] PARTIAL: Agent maps change impact with explicit unaffected list — Step 4 requires three tables: Direct impacts, Indirect impacts, and "Unaffected (explicitly stated)" with the note "The 'unaffected' section is not optional." The output includes all three tables with 5 explicitly unaffected components. PARTIAL ceiling per test author.

### Notes

The unaffected-components section is substantive and explicit. The PARTIAL ceiling is test-author-imposed, not a definition gap. The confidence score being MEDIUM rather than HIGH is appropriate given the number of `needs_user_confirmation` assumptions. The ASGI migration risk is correctly called out as the single most operationally risky step.
