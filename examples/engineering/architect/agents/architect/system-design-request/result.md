# System Design Request

Scenario: A developer asks the architect agent to design a real-time notification system for a logistics SaaS platform. The system needs to push shipment status updates to both a web dashboard and mobile apps.

## Prompt

> We're building a logistics platform called FreightFlow. We need a real-time notification system so that customers and drivers can see shipment status updates (picked up, in transit, out for delivery, delivered) pushed to the web dashboard and the mobile apps without polling. We're currently running a Django REST API on PostgreSQL. Expecting roughly 50,000 active shipments per day, with peak bursts around 9am and 2pm when most deliveries kick off. Need to know what you'd recommend for the architecture.
> 
> Do not ask for clarification — produce the full design now. State your assumptions in an assumption ledger and mark each as proven_by_code, inferred, or needs_user_confirmation.
> 
> Output structure (use these section names):
> 
> 1. **Pre-flight** — list project conventions checked: `CLAUDE.md`, `docs/architecture/adr/` (existing ADRs), `docs/tooling-register.md` (tool stack), `pyproject.toml` (Django version). Even if files not accessible, state what would be checked.
> 2. **Work classification + scope** — explicitly classify: this is **architecture design** (not implementation, not bug fix). In-scope: notification delivery design, transport choice, scaling for 50k/day with peak bursts. Out-of-scope: mobile app implementation, push provider account setup, business rules for shipment state transitions.
> 3. **Assumption Ledger** — numbered table with columns `# | Assumption | Classification (proven_by_code / inferred / needs_user_confirmation) | Validation method | Confidence`. At least 8 assumptions covering: DB load capacity, push provider choice (FCM/APNs/Web Push), authentication model, multi-tenancy isolation, peak burst sizing, message ordering guarantees, retry semantics, dashboard browser support.
> 4. **Quantified NFRs** — numeric targets only: p95 delivery latency < 5s end-to-end, throughput 50k events/day with peak 5k/hour at 9am+2pm, availability 99.9%, message ordering guaranteed per shipment.
> 5. **C4 Level 1 + Level 2 Mermaid diagrams**.
> 6. **Options analysis per significant decision** (transport: WebSocket vs SSE vs long-poll vs push-notification-only) — at least 2 options each, rejected alternative with reasoning.
> 7. **Confidence assessment table per component** — components <60% confidence get a spike planned.
> 8. **Change impact analysis** — what-if traffic 10× growth, what-if a new client type (3PL partner API), what-if push-provider outage.
> 9. **Anti-patterns flagged**: premature microservices for a notification feature, distributed monolith via shared DB, unbounded WebSocket connection growth without backpressure.
> 10. **Recommended ADR**: title + summary + rejected alternative.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

# Architecture Design: Real-Time Notification System for FreightFlow

## 1. Pre-flight

**Files checked/to-be-checked:**
- `CLAUDE.md` (not present) — would establish Django version, notification patterns, push provider standards
- `docs/architecture/adr/` (not present) — would check for existing authentication, scaling, or event-handling decisions
- `docs/tooling-register.md` (not present) — would verify notification provider (FCM/APNs/OneSignal) selection and web framework standards
- `pyproject.toml` (not present) — would confirm Django/DRF versions, async worker setup (Celery/Dramatiq)
- `docs/specs/` (not present) — would check for existing notification requirement specs

**Assumption:** Working with vanilla Django + PostgreSQL. Proceeding with design that assumes Django 4.2+, PostgreSQL 13+, and no existing real-time infrastructure.

---

## 2. Work Classification + Scope

**Classification:** This is **architecture design** (system boundaries, technology selection, scalability model). Not implementation, not deployment.

**In-scope:**
- Notification transport layer design (WebSocket vs SSE vs long-polling vs native push)
- Event flow from shipment status change → notification delivery
- Scalability model for 50k/day peak bursts (5k/hour at 9am & 2pm)
- Multi-client support (web dashboard, iOS, Android)
- Message ordering and reliability guarantees
- Push provider integration points (FCM, APNs)

**Out-of-scope:**
- Mobile app implementation
- Push provider account setup or credential management
- Business logic for state transitions (when does status actually change?)
- Customer/driver role-based access control implementation details
- Frontend UI/UX
- Deployment pipeline or observability instrumentation

---

## 3. Assumption Ledger

| # | Assumption | Classification | Validation Method | Confidence |
|---|---|---|---|---|
| 1 | 50k active shipments/day, 5k events/hour peak (9am & 2pm) | **inferred** from user spec | Check actual event rate post-launch; scale model from usage | 90% |
| 2 | Event arrival distribution: 70% during peak windows, 30% off-peak | **inferred** | Monitoring burst patterns in first 2 weeks; adjust queue sizing | 75% |
| 3 | Database can sustain 50-100 writes/sec for notifications + queries | **needs_user_confirmation** | Load test PostgreSQL write throughput; assess connection pool | 40% (SPIKE) |
| 4 | Web clients: browsers (Safari, Chrome, Firefox); mobile clients: iOS/Android with FCM+APNs | **needs_user_confirmation** | Enumerate actual client types and OS support; finalize push provider choice | 50% (SPIKE) |
| 5 | Each shipment notification must preserve temporal order (e.g., "picked up" before "in transit") | **inferred** from domain | Trace message ordering guarantees through queue; test replay scenarios | 85% |
| 6 | Acceptable end-to-end latency: status change → customer sees update is <5 seconds p95 | **inferred** from "real-time" requirement | Measure latency from Django write to client receipt; adjust batch sizing | 75% |
| 7 | Push provider (FCM/APNs) credentials managed via environment variables; no hard-coded keys | **inferred** from security baseline | Audit Django settings for secrets management; deploy via CI secret store | 80% |
| 8 | Web notifications use browser Web Push API; fallback to WebSocket for real-time if Web Push unavailable | **inferred** | Test push permission flow; measure browser support (98%+ modern browsers) | 80% |
| 9 | Authentication: same JWT tokens used for API auth also validate WebSocket/SSE subscriptions | **inferred** from Django pattern | Confirm JWT strategy; verify token refresh on mobile | 70% |
| 10 | Connection limits: max 1M concurrent WebSocket connections across fleet (or <100k if using SSE) | **inferred** from 50k active shipments + multiple watchers per shipment | Validate against hosting infrastructure (Fly.io/Heroku/AWS capacity); re-assess if 10× growth | 60% (SPIKE) |

---

## 4. Quantified NFRs

| NFR | Target | Rationale |
|---|---|---|
| **End-to-end latency** | p95 < 5s (status change → client receipt) | Real-time expectation for logistics; 5s acceptable for non-critical updates |
| **Throughput** | 50,000 events/day; peak 5,000 events/hour (bursts at 9am & 2pm) | User spec; translate to ~1.4 writes/sec baseline, ~1.4k writes/sec peak |
| **Availability** | 99.9% uptime (SLA: ~22 min downtime/month) | Standard for customer-facing logistics; push provider downtime excluded |
| **Message ordering** | Guaranteed per-shipment (all updates for shipment X arrive in sequence) | Critical: "picked up" must precede "in transit"; cross-shipment order optional |
| **Fanout ratio** | Avg 3–5 subscribers per shipment (customer + driver + ops; may include 3PL) | Scales notification burst: 5k events × 4 subscribers = 20k downstream pushes/hour peak |
| **Connection management** | Max 100k WebSocket connections (20–30% overhead during peak) | Conservative estimate for fleet size; triggers vertical or horizontal scale |
| **Retry semantics** | Exponential backoff: 1s, 2s, 4s, 8s, 16s max; drop after 3 attempts or 5 min TTL | Avoid overwhelming receivers; balance delivery vs stale notifications |
| **Data retention** | Notifications persisted in queue for 24h (allow client reconnect/sync) | Browser tabs may lose connection; clients must be able to fetch missed updates |
| **Push provider uptime** | Assume FCM/APNs at 99.99%; fallback to in-app polling if down | Design must tolerate provider outage without losing shipments |

---

## 5. C4 Level 1 + Level 2 Mermaid Diagrams

**Level 1: System Context**

```mermaid
graph TB
    Customer["👤 Customer"]
    Driver["👤 Driver"]
    Ops["👤 Operations"]
    
    WebApp["🌐 Web Dashboard<br/>(browser)"]
    MobileApp["📱 Mobile Apps<br/>(iOS/Android)"]
    
    FreightFlow["FreightFlow<br/>Logistics Platform"]
    
    FCM["🔔 Firebase Cloud<br/>Messaging"]
    APNs["🔔 Apple Push<br/>Notification Service"]
    WebPush["🌐 Web Push<br/>Notifications"]
    
    Customer -->|uses| WebApp
    Driver -->|uses| MobileApp
    Ops -->|uses| WebApp
    
    WebApp -->|subscribe| FreightFlow
    MobileApp -->|subscribe| FreightFlow
    
    FreightFlow -->|push token| FCM
    FreightFlow -->|push token| APNs
    FreightFlow -->|send notification| WebPush
    
    FCM -.->|deliver| MobileApp
    APNs -.->|deliver| MobileApp
    WebPush -.->|deliver| WebApp
```

**Level 2: Container Architecture**

```mermaid
graph TB
    subgraph "Client Layer"
        WEB["Web Dashboard<br/>(React/Vue)"]
        IOS["iOS App"]
        ANDROID["Android App"]
    end
    
    subgraph "Django REST API Layer"
        API["Django REST API<br/>(drf-spectacular)"]
        AUTH["JWT Auth"]
        QUEUE["Task Queue<br/>(Celery/Dramatiq)"]
    end
    
    subgraph "Real-Time Layer"
        WS["WebSocket Server<br/>(daphne/uvicorn)"]
        SSE["SSE Fallback<br/>(HTTP streaming)"]
        CONN_MGR["Connection Manager<br/>(in-memory state)"]
    end
    
    subgraph "Persistence Layer"
        PG["PostgreSQL<br/>- shipments<br/>- notifications log"]
        REDIS["Redis<br/>- subscriptions cache<br/>- fanout queue"]
        MSGQ["Message Queue<br/>(Kafka/RabbitMQ)"]
    end
    
    subgraph "External Services"
        FCM["Firebase Cloud<br/>Messaging"]
        APNs["Apple Push<br/>Notification"]
        WEBPUSH["Web Push API"]
    end
    
    WEB -->|JWT + subscribe| WS
    IOS -->|JWT + device token| API
    ANDROID -->|JWT + device token| API
    
    API -->|emit event| QUEUE
    QUEUE -->|publish| MSGQ
    
    MSGQ -->|shipment.status_changed| CONN_MGR
    CONN_MGR -->|fanout to subscribers| WS
    CONN_MGR -->|fanout to subscribers| SSE
    
    CONN_MGR -->|send push| FCM
    CONN_MGR -->|send push| APNs
    CONN_MGR -->|send notification| WEBPUSH
    
    CONN_MGR -->|read/write subscriptions| REDIS
    CONN_MGR -->|audit log| PG
    
    WS -->|broadcast| WEB
    SSE -->|stream| WEB
```

---

## 6. Options Analysis: Transport Layer

### **Decision: How do clients receive real-time shipment status updates?**

#### **Option A: WebSocket (Bidirectional, persistent)**

**Pros:**
- Lowest latency (p95 <500ms feasible)
- Bidirectional: client can acknowledge, ask for resend
- Handles mobile reconnect gracefully
- Scales to 100k+ concurrent connections with modern servers

**Cons:**
- Requires persistent server connections (memory overhead ~10MB per 10k connections)
- Firewall/proxy incompatibility in some corporate networks
- More complex server state management (graceful disconnect, reconnect logic)
- Harder to scale horizontally (sticky sessions or shared connection state needed)

**Verdict:** ✅ **Recommended for primary transport**. Mobile apps benefit most; web browsers can use fallback.

---

#### **Option B: Server-Sent Events (SSE, one-way streaming)**

**Pros:**
- Simpler than WebSocket (standard HTTP)
- Better firewall/proxy compatibility
- Browser-native API; easier for web clients
- Automatic reconnect with `Last-Event-ID`

**Cons:**
- One-way only (client can't easily signal acknowledgment)
- Slightly higher latency (p95 ~2–3s) due to HTTP chunking
- Max 6 connections per domain (HTTP/1.1 limit) — works only if single endpoint
- Less efficient than WebSocket for high-frequency updates

**Verdict:** ✅ **Fallback for web browsers if WebSocket unavailable** (corporate proxies, older infrastructure).

---

#### **Option C: Long-Polling**

**Pros:**
- Works in all networks (just HTTP GET)
- Requires no persistent connection state

**Cons:**
- High latency (p95 >5s from polling interval)
- Inefficient: ~2.5 reqs/sec baseline × 100k clients = 250k unnecessary requests/sec
- Hammers database with repeated queries
- Exceeds our 5s latency SLA during peak

**Verdict:** ❌ **Rejected.** Violates p95 <5s latency requirement and scales poorly.

---

#### **Option D: Native Push Notifications Only (FCM + APNs)**

**Pros:**
- Works offline; can wake app
- Native mobile experience (badges, sounds)
- No persistent server connections needed

**Cons:**
- Cannot deliver to web dashboard (no native push for browsers running in tabs)
- Delivery SLA: 99.99% but not real-time (1–10s typical)
- Cannot display real-time updates while app running (only notification badge)
- Increased battery drain on mobile
- Cannot sync missed notifications efficiently

**Verdict:** ❌ **Rejected as primary.** Only viable as **supplementary** for mobile when app is backgrounded; insufficient for web dashboard.

---

### **Hybrid Recommendation**

| Client | Primary | Fallback |
|--------|---------|----------|
| **Web Dashboard** | WebSocket | SSE |
| **Mobile (foreground)** | WebSocket | SSE |
| **Mobile (backgrounded)** | Native Push (FCM/APNs) | None |

**Rationale:** WebSocket handles real-time web/active mobile. Native push handles offline mobile scenario. Two-tier approach maximizes coverage.

---

## 7. Confidence Assessment Table

| Component | Confidence | Risk | Spike/Validation Needed |
|---|---|---|---|
| WebSocket transport design | 85% | Low | Proof-of-concept: 1k concurrent connections under load |
| SSE fallback implementation | 80% | Low | Test corporate proxy scenarios; verify `Last-Event-ID` semantics |
| PostgreSQL write throughput (50–100 writes/sec) | **40%** | **HIGH** | 🔴 **SPIKE:** Load test with production schema; measure connection pool saturation |
| Message ordering per-shipment | 85% | Low | Verify event sequencing in queue; add ordering tests |
| Push provider integration (FCM/APNs) | 75% | Medium | 🟡 **Spike:** Validate credential flow; test outage handling |
| Connection limit scaling (100k concurrent) | **60%** | **MEDIUM** | 🔴 **SPIKE:** Capacity plan for infrastructure; benchmark memory/CPU per connection |
| Redis subscription cache consistency | 80% | Low | Stress test under peak; verify fanout batching |
| Cross-device sync (browser + mobile for same user) | **50%** | **HIGH** | 🔴 **SPIKE:** Design sync protocol; avoid duplicate notifications |
| Retry/backoff without overwhelming receivers | 70% | Medium | 🟡 **Spike:** Simulate receiver slowness; measure queue depth under backpressure |
| **Total spikes identified:** | | | 4 spikes block confident design handoff |

**Spike Planning:**
1. **PostgreSQL Load Test** (1–2 days) — provision test DB, measure write latency at 100 writes/sec, identify connection pool bottleneck
2. **WebSocket Capacity Test** (1–2 days) — prototype with daphne, load to 10k connections, measure memory footprint and latency
3. **Push Provider Failover** (1 day) — mock FCM/APNs outage, verify web/in-app fallback paths work
4. **Cross-Device Deduplication** (2 days) — design subscription model that prevents same notification hitting user via web + mobile simultaneously

---

## 8. Change Impact Analysis

### **What-If: Traffic 10× Growth (500k active shipments/day, 50k events/hour peak)**

**Impact on each component:**

| Component | Current Capacity | 10× Load | Mitigation |
|---|---|---|---|
| PostgreSQL writes | 50–100 writes/sec | 500–1000 writes/sec | ❌ **Breach:** Requires sharding (by shipment ID range or by tenant if multi-tenant). Add read replicas for audit log queries. |
| WebSocket connections | 100k | 1M | ⚠️ **Breach:** Single daphne instance saturates at ~50k. Horizontal scale to 20 instances + sticky session router (nginx/HAProxy) or move to managed service (e.g., Fly.io). |
| Redis fanout queue | 5k events/hour | 50k events/hour | ✅ **OK:** Redis can sustain 100k ops/sec. Monitor memory (estimate: 1–2GB baseline → 20–40GB). Add replication. |
| Push provider throughput | 20k downstream pushes/hour | 200k pushes/hour | ⚠️ **Caution:** FCM/APNs support >1M requests/sec each. Costs increase proportionally; may need rate limiting per customer. |

**Decision point:** At 10× growth, **must shard PostgreSQL by shipment ID or tenant**. Design notifications table with explicit shipment_id partition key.

---

### **What-If: New Client Type (3PL Partner API: 500+ external integrations)**

**New requirement:** Partner systems (Shopify, WooCommerce plugins) subscribe to shipment events via REST API (webhook model, not WebSocket).

**Impact:**

| Aspect | Change |
|---|---|
| **Event model** | Add webhook subscription table: `(partner_id, shipment_type_filter, callback_url, signing_key)`. Emit events to both WebSocket AND webhook deliverer. |
| **Delivery semantics** | WebSocket = push; webhooks = pull (retries, exponential backoff). Use separate queue (Celery job) for webhook dispatch. |
| **Fanout cost** | Each event now triggers: N web clients + N mobile clients + N partners. Estimate: 5k events/hour × (4 subscribers + 10 partners avg) = 70k downstream deliveries/hour. |
| **Idempotency** | Partners require idempotent notifications (same event may retry). Add event ID to payload; partners implement dedup via event ID. |
| **Spec update** | ADR-0007 must document webhook model alongside WebSocket. |

**Decision:** Webhook model orthogonal to WebSocket; can be added in Phase 2 without rearchitecting. Add to design as optional Phase 2 extension.

---

### **What-If: Push Provider Outage (FCM down for 1 hour)**

**Scenario:** Firebase Cloud Messaging unavailable for mobile apps during 9am peak.

**Mitigation:**

| Layer | Fallback |
|---|---|
| **Mobile (backgrounded)** | Degrade to no push notifications. Driver/customer won't see banner until they open app. Accept SLA breach. |
| **Mobile (foreground, connected to WebSocket)** | In-app notification banner displayed instead (no native badge/sound). Seamless. |
| **Web dashboard** | Unaffected (uses WebSocket + SSE, no FCM dependency). ✅ Uninterrupted. |

**Design requirement:** Add FCM health check to dashboard. If FCM down >5 min, display banner to mobile users: "Notifications delayed. Refresh to check status." Implement fallback to APNs for iOS (primary FCM → APNs + silent notification).

**Post-incident:** Measure FCM uptime SLA monthly. If <99.9%, add APNs as primary for iOS; FCM secondary.

---

## 9. Anti-Patterns Flagged

### ❌ **Anti-Pattern 1: Premature Microservices for a Single Feature**

**The trap:** "Notifications need real-time, so let's split into a separate service."

**Why it's wrong:** Notification delivery is tightly coupled to shipment state changes. Splitting creates a distributed transaction (shipment updated, service-to-service call fails, notification lost). No independent scaling benefit at 50k/day.

**What to do instead:** Keep notifications as a subsystem within Django (via async tasks + WebSocket server running in the same codebase or adjacent process). Use Celery/Dramatiq only for I/O-bound work (push API calls), not to justify a separate service.

---

### ❌ **Anti-Pattern 2: Distributed Monolith via Shared Database**

**The trap:** Multiple WebSocket servers all write to the same `notifications` table, relying on the DB as the message bus.

**Why it's wrong:** PostgreSQL isn't a message queue. Concurrent writes to a hot table (5k/hour) cause lock contention. No ordering guarantees. Client-server affinity breaks when connections migrate.

**What to do instead:** Use an actual message queue (Kafka, RabbitMQ) as the hub. Multiple WebSocket servers consume from the queue independently. Each server maintains in-memory subscription state via Redis. DB is for audit/persistence only, not real-time dispatch.

---

### ❌ **Anti-Pattern 3: Unbounded WebSocket Connection Growth Without Backpressure**

**The trap:** Accept all WebSocket subscriptions without limit. At 100k connections, server memory balloons; no queue to handle slow clients.

**Why it's wrong:** One slow client (slow network) backs up the broadcast queue. p95 latency degrades. Server OOM kills all connections.

**What to do instead:** Implement backpressure: set max buffer per connection (e.g., 100 pending messages). If buffer overflows, close the connection. Clients reconnect and catch up from Redis cache. Also set max concurrent connections per server (e.g., 10k per daphne instance); reject new connections with 503 and force load balancer to try next server.

---

### ❌ **Anti-Pattern 4: Ignoring Message Ordering in Distributed System**

**The trap:** Use independent push API calls for each notification. Event A (picked up) and Event B (in transit) for the same shipment may arrive out of order on the client.

**Why it's wrong:** Client UI shows "In transit" then "Picked up" after, confusing customers.

**What to do instead:** Enforce ordering guarantee: all events for a shipment go through a single queue with a sequence number. Receiver must apply events in sequence number order. Discard out-of-order events. Add this requirement to the push payload schema.

---

### ❌ **Anti-Pattern 5: Over-Provisioning for Peak That Never Comes**

**The trap:** "We expect 5k events/hour peak, so provision for 10k/hour capacity."

**Why it's wrong:** Wastes money. Real peak is often lower than estimated.

**What to do instead:** Provision for stated 5k/hour. Monitor actual peak. If 80% of capacity consumed for >2 consecutive weeks, scale up. Use auto-scaling groups with target utilization (e.g., scale when CPU >70%).

---

## 10. Recommended ADR

### **ADR-0008: Real-Time Notification Delivery via WebSocket + Hybrid Push**

**Status:** Proposed

**Context**

FreightFlow logistics customers and drivers need real-time visibility into shipment status updates (picked up, in transit, out for delivery, delivered). Current REST API polling is inefficient. Platform must handle 50,000 active shipments per day with peak bursts (5,000 events/hour at 9am & 2pm) while maintaining <5 second end-to-end latency and 99.9% availability.

**Decision**

Implement **hybrid notification architecture:**

1. **WebSocket (primary transport for web + active mobile clients)**
   - Daphne (async HTTP server) with Django Channels for WebSocket upgrades
   - Sticky session load balancer (nginx) for horizontal scaling
   - Redis PubSub for cross-server fanout
   - Max 100k concurrent connections per fleet

2. **Server-Sent Events (fallback for web clients, fallback for web if WebSocket unavailable)**
   - HTTP/1.1 chunked streaming with `Last-Event-ID` for reconnect
   - Better firewall compatibility than WebSocket
   - Suitable for corporate network scenarios

3. **Native Push Notifications (supplementary for backgrounded mobile apps)**
   - Firebase Cloud Messaging (FCM) for Android
   - Apple Push Notification Service (APNs) for iOS
   - Device tokens persisted in database with last-activity timestamp for cleanup
   - Fallback: if FCM down >5min, promote APNs to primary for iOS

4. **Message Queue (async fan-out orchestration)**
   - RabbitMQ or Kafka for reliable event delivery
   - Each shipment status change published to queue
   - Async workers consume and fanout to subscribed clients
   - Enables scaling WebSocket count independently of event producers

5. **Subscription State (Redis cache)**
   - Store subscriptions in-memory on each WebSocket server
   - Redis cluster mirrors subscriptions for cross-server visibility
   - Subscription: `shipment_id:*` or `user_id:*` granularity

6. **Audit Log (PostgreSQL)**
   - Persist all notifications to `notifications` table for compliance/debug
   - Indexed by `shipment_id` for retrieval of missed updates
   - Retention: 30 days (configurable)

**Rejected Alternatives**

1. **Long-Polling only:** Violates <5s latency SLA; creates 250k unnecessary HTTP requests/sec at peak. ❌

2. **Native Push only (no WebSocket):** Cannot deliver real-time updates to web dashboard; cannot show in-app banner for foreground mobile. ❌

3. **Single WebSocket server (no scaling):** Hits connection limits at ~50k; doesn't scale to 10× growth. ❌

4. **Synchronous REST API polling:** Baseline approach; customer requirement explicitly "without polling." ❌

**Consequences**

**Positive:**
- Real-time delivery <5s p95 meets customer expectations
- Scales to 100k concurrent connections with horizontal scaling
- Hybrid approach maximizes coverage (web + mobile + offline)
- Message queue decouples producers from consumers

**Negative:**
- Operational complexity: daphne + RabbitMQ + Redis requires ops discipline
- Requires sticky sessions or shared state (Redis) for horizontal scaling
- Push provider outages (FCM/APNs) require fallback coordination
- 4 spikes needed before confident implementation (see Section 7)

**Risks**
- Database write bottleneck at 100+ writes/sec (PostgreSQL connection pool saturation)
  - **Mitigation:** Load test before build; shard by shipment ID if needed
- WebSocket memory overhead at 100k connections (~1–2GB per server)
  - **Mitigation:** Set connection limits per server; use auto-scaling to add servers at 70% capacity
- Message ordering: distributed system may reorder events
  - **Mitigation:** Enforce sequence numbers per shipment; client applies events in order

**Implementation Phases**

1. **Phase 1 (MVP):** WebSocket + Redis + RabbitMQ + PostgreSQL audit log
   - Supports web + active mobile clients
   - Estimated 3–4 weeks

2. **Phase 2:** Native push integration (FCM + APNs) + backgrounded mobile support
   - Estimated 2–3 weeks

3. **Phase 3 (optional):** Webhook API for 3PL partners
   - Requires separate Celery job for retry orchestration
   - Estimated 1–2 weeks

---

## Summary

**Key Design Decisions:**
1. ✅ WebSocket primary, SSE fallback for web layer
2. ✅ Native push supplementary for backgrounded mobile
3. ✅ RabbitMQ for reliable event fan-out
4. ✅ Redis for subscription state (cross-server visibility)
5. ✅ PostgreSQL for audit persistence only

**Confidence Level:** 60% (4 high-risk spikes pending validation)

**Next Steps:** Execute spikes in Section 7 (PostgreSQL load test, WebSocket capacity, push failover, cross-device dedup). Design is architecture-sound but infrastructure assumptions require proof before build begins.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/18.5 (92%) |
| Evaluated | 2026-05-04 |
| Target duration | 84029 ms |
| Target cost | $0.1360 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent performs a pre-flight step — checks for project conventions (CLAUDE.md, installed rules) and existing ADRs before proposing anything | PASS | Section 1 'Pre-flight' explicitly lists CLAUDE.md, docs/architecture/adr/, docs/tooling-register.md, pyproject.toml, and docs/specs/ — each stating what would be checked and noting files are not present. Assumption stated: 'Working with vanilla Django + PostgreSQL. Proceeding with design that assumes Django 4.2+, PostgreSQL 13+, and no existing real-time infrastructure.' |
| c2 | Agent classifies the work type and scopes what is and is not covered by the design | PASS | Section 2 'Work Classification + Scope' explicitly states: 'Classification: This is architecture design (system boundaries, technology selection, scalability model). Not implementation, not deployment.' In-scope and Out-of-scope items are each listed as bullet points. |
| c3 | Agent produces a mandatory assumption ledger with each assumption classified as proven_by_code, inferred, or needs_user_confirmation | PASS | Section 3 'Assumption Ledger' has a 10-row table with columns '# \| Assumption \| Classification \| Validation Method \| Confidence'. Classifications used: 'inferred' (#1,2,5,6,7,8,9,10) and 'needs_user_confirmation' (#3,4). Covers DB load (#3), push provider (#4), auth model (#9), burst sizing (#1,2), message ordering (#5), retry (#6/implicit), browser support (#8). |
| c4 | Agent quantifies non-functional requirements rather than accepting vague terms — scale (50k shipments/day), latency targets, and availability | PASS | Section 4 'Quantified NFRs' table states: 'End-to-end latency: p95 < 5s', 'Throughput: 50,000 events/day; peak 5,000 events/hour', 'Availability: 99.9% uptime (SLA: ~22 min downtime/month)', 'Message ordering: Guaranteed per-shipment'. Converts daily rate to writes/sec: '~1.4 writes/sec baseline, ~1.4k writes/sec peak'. |
| c5 | Agent presents at least two architectural options (e.g. WebSockets vs SSE vs polling) with a scored trade-off table | PASS | Section 6 presents four options: Option A (WebSocket), Option B (SSE), Option C (Long-Polling), Option D (Native Push Only). Each has Pros/Cons lists and an explicit Verdict (✅ or ❌ with reasoning). A Hybrid Recommendation table at the end maps client type to primary/fallback transport. |
| c6 | Agent includes Mermaid diagrams — at minimum a component diagram showing trust boundaries | PASS | Section 5 contains two fenced mermaid blocks: Level 1 System Context (graph TB with external actors, FreightFlow platform, and external push services) and Level 2 Container Architecture (with subgraphs 'Client Layer', 'Django REST API Layer', 'Real-Time Layer', 'Persistence Layer', 'External Services' acting as trust boundary delineators). |
| c7 | Agent identifies decisions that require an ADR (e.g. choice of message broker or real-time transport) | PASS | Section 10 'Recommended ADR' presents ADR-0008 covering: WebSocket as primary transport, RabbitMQ/Kafka message queue, Redis for subscription state, native push (FCM/APNs) for backgrounded mobile, and PostgreSQL for audit. Rejected alternatives are listed with reasoning. |
| c8 | Agent includes a confidence score (HIGH/MEDIUM/LOW with numeric) and states which assumptions drive uncertainty | PASS | Section 7 'Confidence Assessment Table' has per-component rows with percentage confidence and a Risk column using Low/Medium/High labels. Summary states: 'Confidence Level: 60% (4 high-risk spikes pending validation)'. Spike items explicitly link to assumptions driving uncertainty (e.g., PostgreSQL at 40% confidence flagged as HIGH risk, WebSocket connection limits at 60% MEDIUM). |
| c9 | Agent maps change impact — what existing FreightFlow components are directly or indirectly affected, and explicitly lists what is unaffected | PARTIAL | Section 8 covers three what-if scenarios with per-component impact tables. Under push provider outage: 'Web dashboard: Unaffected (uses WebSocket + SSE, no FCM dependency). ✅ Uninterrupted.' However, there is no comprehensive 'unaffected components' list across all scenarios — only one component (web dashboard) is explicitly labeled unaffected in one scenario. The change impact is addressed but the unaffected listing is sparse. |
| c10 | Output's transport recommendation explicitly compares WebSockets vs SSE vs long-polling for the push-to-browser-and-mobile use case, with reasoning that addresses bidirectional vs server-initiated traffic and mobile network behaviour (background sockets, reconnection) | PASS | Section 6 Options A/B/C/D cover WebSocket ('Bidirectional: client can acknowledge, ask for resend'; 'Handles mobile reconnect gracefully'), SSE ('one-way only'), Long-Polling (rejected, violates 5s SLA). Hybrid table distinguishes Mobile (foreground) WebSocket vs Mobile (backgrounded) Native Push. Mobile reconnect behaviour and bidirectionality are explicitly compared. |
| c11 | Output addresses the existing Django + PostgreSQL stack — either uses Django Channels / a Django-compatible push solution, or names a separate service with clear integration points to the existing API | PASS | ADR-0008 states: 'Daphne (async HTTP server) with Django Channels for WebSocket upgrades.' Level 2 diagram shows 'Django REST API (drf-spectacular)' as a container. Task Queue is listed as 'Celery/Dramatiq'. PostgreSQL role is defined: 'Persist all notifications to notifications table for compliance/debug.' |
| c12 | Output sizes the system from the 50,000 shipments/day plus 9am/2pm peak — converting daily volume into a peak-second concurrent connection or message rate (e.g. burst factor of 5-10x average) and validating the chosen transport handles it | PASS | Section 4 converts: '50,000 events/day; peak 5,000 events/hour (bursts at 9am & 2pm)... translate to ~1.4 writes/sec baseline, ~1.4k writes/sec peak.' Fanout calculation: '5k events × 4 subscribers = 20k downstream pushes/hour peak.' Section 8 10× growth validates transport capacity: 'Single daphne instance saturates at ~50k [connections]. Horizontal scale to 20 instances.' |
| c13 | Output includes at least one Mermaid component diagram showing the path from shipment status change → message broker → push fan-out → web/mobile clients, with trust boundaries marked | PASS | Level 2 Container Architecture mermaid diagram traces: 'API → QUEUE → MSGQ → CONN_MGR → WS/SSE/FCM/APNs → WEB/IOS/ANDROID'. Subgraphs ('Django REST API Layer', 'Real-Time Layer', 'Persistence Layer', 'External Services') serve as trust boundary demarcation. The full fan-out path is visible in one diagram. |
| c14 | Output's assumption ledger lists the unstated facts (mobile platforms iOS/Android both, push notification vs in-app socket for backgrounded apps, customer authentication model) classified as `inferred` or `needs_user_confirmation` | PASS | Assumption #4: 'Web clients: browsers...; mobile clients: iOS/Android with FCM+APNs' — classified needs_user_confirmation. Assumption #8: 'Web notifications use browser Web Push API; fallback to WebSocket for real-time if Web Push unavailable' — inferred. Assumption #9: 'Authentication: same JWT tokens...validate WebSocket/SSE subscriptions' — inferred. All three required categories are present. |
| c15 | Output identifies at least 2 ADR-worthy decisions (e.g. message broker selection, push transport, fan-out service vs in-Django) and lists them in a "Decisions Requiring ADR" section | PARTIAL | Section 10 'Recommended ADR' presents ADR-0008 which contains multiple decisions (transport selection, message broker RabbitMQ/Kafka, Redis for subscriptions, native push integration). However, the section name is 'Recommended ADR' not 'Decisions Requiring ADR', and all decisions are bundled into one combined ADR rather than listed as multiple separately identified ADR-worthy decisions. The substance is present but not structured as the criterion requires. |
| c16 | Output's change impact section explicitly addresses the Django REST API (extended with status-change events) and PostgreSQL (transactional outbox or change capture) and lists at least one component that is unaffected | PARTIAL | Section 8 addresses PostgreSQL under 10× growth ('Requires sharding by shipment ID range') but does not mention transactional outbox or change capture patterns. Django REST API is implicit in diagrams but Section 8 does not explicitly address it as a component being extended with status-change events. Unaffected component is listed: 'Web dashboard: Unaffected (uses WebSocket + SSE, no FCM dependency). ✅ Uninterrupted.' One of three sub-criteria fully met, two partially. |
| c17 | Output includes a confidence score with HIGH/MEDIUM/LOW label plus a numeric value out of 100, and lists the assumptions or unknowns driving any confidence reduction | PASS | Section 7 table has numeric confidence percentages (85%, 80%, 40%, 85%, 75%, 60%, 80%, 50%, 70%) and Risk column with Low/Medium/High labels. Summary states '60% (4 high-risk spikes pending validation).' Four spikes are explicitly planned (PostgreSQL Load Test, WebSocket Capacity Test, Push Provider Failover, Cross-Device Deduplication), each linked to specific low-confidence assumptions. |
| c18 | Output addresses backgrounded mobile app delivery — recommending APNs/FCM for true push when the app isn't foregrounded, distinct from in-app socket for live dashboards | PARTIAL | Hybrid Recommendation table explicitly distinguishes: 'Mobile (foreground): WebSocket / SSE fallback' vs 'Mobile (backgrounded): Native Push (FCM/APNs) / None'. Section 8 push provider outage scenario differentiates: 'Mobile (backgrounded): Degrade to no push notifications' vs 'Mobile (foreground, connected to WebSocket): In-app notification banner displayed instead.' The foreground/background distinction is consistently maintained. |
| c19 | Output addresses authentication on the persistent connection (token-scoped channels per customer/driver, not broadcast) so customers can't see other customers' shipments | PARTIAL | Assumption #9 states 'same JWT tokens used for API auth also validate WebSocket/SSE subscriptions' (inferred). Level 2 diagram includes 'JWT Auth' as a container. ADR mentions 'Subscription: shipment_id:* or user_id:* granularity'. However, the output does not explicitly address isolation guarantees (customers can't see other customers' shipments) or how channels are scoped per customer/driver identity as a security constraint. |

### Notes

The output is a thorough, well-structured architecture design that satisfies the vast majority of criteria. Strongest areas: assumption ledger with proper tripartite classification, quantified NFRs with unit conversions, four-option transport comparison with explicit verdicts, and dual Mermaid diagrams with trust boundaries. The main gaps are: (1) c15 bundles all decisions into a single combined ADR rather than listing multiple ADR-worthy decisions in a dedicated section by that name; (2) c16 omits the transactional outbox/change capture pattern for PostgreSQL and doesn't explicitly name the Django REST API as a change impact item in Section 8; (3) c19 mentions JWT validation at connection time but doesn't articulate per-customer channel isolation as a security property. The PARTIAL-ceilinged criteria (c9, c18, c19) are all addressed with reasonable depth. Overall confidence and spike planning in Section 7 is a standout strength.
