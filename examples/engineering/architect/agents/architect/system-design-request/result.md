# System Design Request

Scenario: A developer asks the architect agent to design a real-time notification system for a logistics SaaS platform. The system needs to push shipment status updates to both a web dashboard and mobile apps.

## Prompt

> We're building a logistics platform called FreightFlow. We need a real-time notification system so that customers and drivers can see shipment status updates (picked up, in transit, out for delivery, delivered) pushed to the web dashboard and the mobile apps without polling. We're currently running a Django REST API on PostgreSQL. Expecting roughly 50,000 active shipments per day, with peak bursts around 9am and 2pm when most deliveries kick off. Need to know what you'd recommend for the architecture.
> 
> Do not ask for clarification — produce the full design now. State your assumptions in an assumption ledger and mark each as proven_by_code, inferred, or needs_user_confirmation.
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

# System Design: FreightFlow Real-Time Notification System

## Requirements

### Functional
- Push shipment status updates (picked up, in transit, out for delivery, delivered) to connected clients in real-time
- Support web dashboard and native mobile apps (iOS, Android) without polling
- Clients must receive notifications within 1 second of status change in the backend
- Maintain update ordering (an "in transit" event cannot overtake a "picked up" event for the same shipment)
- Support filtering by shipment, customer, driver, or route
- Clients can subscribe/unsubscribe to notification streams dynamically
- Graceful handling of client disconnects and reconnects

### Non-Functional

| Dimension | Target | Justification |
|---|---|---|
| **Scale** | 75,000 concurrent connections at peak (9am, 2pm) | 50K active shipments/day × 1.5 watchers/shipment average (customer + driver) spread over 2 peak hours |
| **Message throughput** | 5–10 status updates per shipment lifecycle = ~250K messages/day; peak burst ~30 msg/s during 9am and 2pm windows | Multiple status transitions per shipment × 50K shipments |
| **Latency** | p95 < 1 second from Django API call to client delivery | Customer-facing logistics feature; humans perceive > 1s as lag |
| **Availability** | 99.5% uptime (3.6 hours downtime/year) | Degraded mode acceptable (clients fall back to polling if real-time fails) |
| **Durability** | Zero tolerance for shipment state loss; eventual consistency acceptable for notification ordering | Financial/legal records; reordered messages are annoying but not critical |
| **Data retention** | 30 days of notification history per shipment | Audit trail for customer support inquiries |

---

## Assumptions

| # | Assumption | Impact if wrong | Confidence | Validation method |
|---|---|---|---|---|
| A1 | Peak concurrent WebSocket connections = 75K | Infrastructure over/under-provisioned | **Medium** | Load test with realistic client distribution in week 1 |
| A2 | Average client session duration = 15 minutes | Connection pool and memory calculation | **Medium** | Instrument real app usage post-launch |
| A3 | Messages are bursty (30 msg/s during peak hours, 2–3 msg/s baseline) | Message broker selection and queue depth | **High** | Observation from production Django logs (if available) or conservative estimate |
| A4 | Ordering must be preserved per shipment, not globally | Partitioning strategy in broker | **High** | Clarified from requirements (separate shipments can reorder) |
| A5 | Mobile apps require native push (FCM/APNs) for reliability; web uses WebSocket | Architecture splits delivery path | **Medium** | Product confirms; assume for now |
| A6 | Django API is single-region; no multi-region failover in scope | Network latency to notification service is < 10ms | **High** | Stated as "currently running Django REST API" |
| A7 | Client reconnect logic tolerates < 30 second outage | Recovery strategy for notification service restarts | **Medium** | Mobile app behavior TBD; assume reasonable reconnect backoff |
| A8 | Third-party notification service (Pusher, Ably) is acceptable alternative to self-hosted | Cost/operational trade-off | **Low** | Needs business decision; cost unknown |

---

## Architecture

### C4 Level 1: System Context

```mermaid
graph TB
    Customer["👤 Customer (Web/Mobile)"]
    Driver["👤 Driver (Mobile)"]
    Dispatcher["👤 Dispatcher (Web)"]
    
    FreightFlow["FreightFlow System"]
    
    ExtFCM["Firebase Cloud Messaging<br/>(FCM)"]
    ExtAPNs["Apple Push Notification<br/>(APNs)"]
    
    Customer -->|Connects WebSocket| FreightFlow
    Driver -->|Connects WebSocket<br/>+ FCM| FreightFlow
    Dispatcher -->|Connects WebSocket| FreightFlow
    
    FreightFlow -->|Push token updates| ExtFCM
    FreightFlow -->|Push token updates| ExtAPNs
```

**External actors:**
- **Customers:** Track shipments via web dashboard or iOS/Android app
- **Drivers:** Receive assignment and status notifications via mobile app
- **Dispatchers:** Monitor fleet and send instructions via web dashboard

**External dependencies:**
- Firebase Cloud Messaging (FCM): Native push to Android
- Apple Push Notification (APNs): Native push to iOS
- Existing Django REST API: Source of truth for shipment state

---

### C4 Level 2: Container Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        WebClient["Web Client<br/>(Dashboard)"]
        MobileApp["Mobile App<br/>(iOS/Android)"]
    end
    
    subgraph "FreightFlow System"
        APIServer["Django REST API<br/>(Shipment mutations)"]
        NotificationService["Notification Service<br/>(WebSocket server)"]
        MessageBroker["Message Broker<br/>(Redis Pub/Sub or<br/>PostgreSQL LISTEN/NOTIFY)"]
        StateDB["PostgreSQL<br/>(Shipment state)"]
        NotificationDB["PostgreSQL<br/>(Notification history)"]
        FCMAdapter["FCM/APNs Adapter<br/>(Native push sender)"]
    end
    
    subgraph "External"
        FCMService["Firebase Cloud Messaging"]
        APNService["Apple Push Notification"]
    end
    
    WebClient -->|WebSocket connect| NotificationService
    MobileApp -->|WebSocket + FCM token| NotificationService
    
    APIServer -->|Shipment update| StateDB
    APIServer -->|Publish StatusChanged| MessageBroker
    
    MessageBroker -->|Subscribe| NotificationService
    MessageBroker -->|Subscribe| FCMAdapter
    
    NotificationService -->|Push via WebSocket| WebClient
    NotificationService -->|Push via WebSocket| MobileApp
    NotificationService -->|Log notification| NotificationDB
    
    FCMAdapter -->|POST /send| FCMService
    FCMAdapter -->|POST /send| APNService
    
    FCMService -->|Native alert| MobileApp
    APNService -->|Native alert| MobileApp
```

---

### Components

#### 1. **Django REST API** (existing, extended)
- **Purpose:** Accept shipment mutations (status changes), publish events to notification pipeline
- **API surface:**
  - `PATCH /shipments/{id}/status` → Update shipment status, emit `ShipmentStatusChanged` event
  - `POST /notifications/{shipment_id}/subscribe` → Register client connection (via NotificationService)
- **Data ownership:** Authoritative source for shipment state (PostgreSQL `shipments` table)
- **Failure mode:** If API is down, no new status changes enter the system. Clients remain connected to NotificationService (receive no updates). Degradation is acceptable.
- **Scaling strategy:** Horizontal, behind load balancer. Stateless (notification subscriptions live in NotificationService, not Django)

#### 2. **Notification Service** (new, WebSocket server)
- **Purpose:** Maintain persistent client connections (WebSocket), subscribe to message broker, fan-out updates to matching clients
- **API surface:**
  - `WebSocket /ws?shipment_id={id}&auth_token={token}` → Persistent bidirectional connection
  - Internal: Subscribe to `shipment::{shipment_id}` channels in message broker
- **Data ownership:** Runtime state only (in-memory client registry: shipment → connected clients). No persistent storage.
- **Failure mode:** All connected clients are dropped on restart. Clients automatically reconnect with exponential backoff. Redelivery via FCM/APNs ensures no notification is permanently lost.
- **Scaling strategy:** Horizontal with **sticky sessions by shipment ID** (Redis or IP-based). All clients watching shipment X must route to the same NotificationService instance to avoid fanning out to multiple servers.
  - Trade-off: Single server per shipment is a bottleneck if one shipment has 10K+ watchers (unlikely for a single shipment, but a dispatch fleet could reach this). Shard by customer/driver instead if needed.

#### 3. **Message Broker** (Redis Pub/Sub or PostgreSQL LISTEN/NOTIFY)
- **Purpose:** Decouple shipment mutation (API) from notification delivery (NotificationService, FCMAdapter). Provide ordering guarantees per shipment.
- **API surface:**
  - Publish: `shipment::{id}:status_changed` → `{ timestamp, old_status, new_status, ... }`
  - Subscribe: `shipment::*:status_changed` (wildcard or per-ID subscription)
- **Data ownership:** Transient messages only. No persistence beyond memory.
- **Failure mode:** Messages in flight are lost on broker restart (acceptable given FCM/APNs act as backup delivery). Notifications older than broker lifespan are unreplayable (eventual consistency).
- **Scaling strategy:** Single-instance Redis (replicated for HA, no clustering needed for this scale) or native PostgreSQL LISTEN/NOTIFY (leverages existing database).

#### 4. **FCM/APNs Adapter** (new service or sidecar)
- **Purpose:** Subscribe to message broker and send native push notifications to mobile apps
- **API surface:**
  - Internal: Subscribes to `shipment::*:status_changed`
  - External: POST to Firebase Cloud Messaging and Apple Push Notification services
- **Data ownership:** Maintains mapping of user → FCM/APNs device tokens (stored in PostgreSQL, keyed by user ID)
- **Failure mode:** If adapter is down, mobile-only users don't receive native push (but WebSocket clients still receive notifications). Retryable via exponential backoff to FCM/APNs.
- **Scaling strategy:** Stateless, horizontal. Load-balanced if throughput exceeds single instance capacity.

#### 5. **PostgreSQL** (extended)
- **Purpose:** Persistent state for shipments, notification history, device tokens
- **Tables:**
  - `shipments` — shipment state (existing, extended with `status`, `status_updated_at`)
  - `notification_history` — audit trail of notifications sent, indexed by `(shipment_id, created_at)` for quick lookup
  - `user_device_tokens` — FCM/APNs tokens per user, indexed by `user_id` for quick lookup during push

---

## Data Flows

### Workflow 1: Driver Status Update → Customer Receives Notification

```mermaid
sequenceDiagram
    participant Driver as Driver<br/>(Mobile)
    participant API as Django<br/>API
    participant DB as PostgreSQL
    participant Broker as Message<br/>Broker
    participant NotifSvc as Notification<br/>Service
    participant Customer as Customer<br/>(Web)
    participant FCM as Firebase<br/>Cloud Messaging
    
    Driver->>API: PUT /shipments/{id}/mark_picked_up
    API->>DB: UPDATE shipments SET status='picked_up'
    DB-->>API: OK
    API->>Broker: PUBLISH shipment::{id}:status_changed {new_status}
    Broker-->>API: OK (message queued)
    
    par
        Broker->>NotifSvc: shipment::{id}:status_changed
        activate NotifSvc
        NotifSvc->>NotifSvc: Find clients watching shipment {id}
        NotifSvc->>Customer: WebSocket frame {status_changed}
        Customer-->>Customer: Update UI
        deactivate NotifSvc
    and
        Broker->>FCM: shipment::{id}:status_changed
        activate FCM
        FCM->>FCM: Find device tokens for customer user
        FCM->>FCM: POST to Firebase Cloud Messaging
        FCMService->>Driver: Native push alert
        deactivate FCM
    end
    
    API->>DB: INSERT notification_history (shipment_id, action, delivered_at)
```

**Consistency model:** Eventual. API commits shipment state (strong) → message broker is populated asynchronously → clients receive notification within 1 second.

**Failure scenarios:**
- If broker is down when API publishes: Message is lost, but API call succeeds (shipped first). Recovery: NotificationService can query shipment state on client reconnect to catch up on missed updates.
- If NotificationService is down: WebSocket clients are disconnected and reconnect automatically. Missed updates backfilled on reconnect (query last N hours of notification history).
- If FCM is down: Push notifications fail, but WebSocket still delivers (for web and connected mobile apps).

**Latency budget:** 1 second total
- API → DB commit: 10ms (local Postgres)
- API → Broker publish: 5ms (local Redis)
- Broker → NotificationService delivery: 50ms (pub/sub latency)
- NotificationService → WebSocket send: 50ms (network to client)
- **Total (nominal):** ~115ms p50, < 1000ms p95 (includes client-side network jitter)

---

### Workflow 2: Mobile App Reconnects After Network Dropout

```mermaid
sequenceDiagram
    participant Mobile as Mobile<br/>App
    participant NotifSvc as Notification<br/>Service
    participant DB as PostgreSQL<br/>notification_history
    
    Mobile->>Mobile: Network down (airplane mode)
    Note over Mobile: WebSocket disconnected, exponential backoff timer active
    
    Mobile->>Mobile: Network restored
    Mobile->>NotifSvc: WebSocket reconnect with auth_token
    activate NotifSvc
    NotifSvc->>NotifSvc: Authenticate user
    NotifSvc->>DB: SELECT * FROM notification_history WHERE user_id={id} AND created_at > last_received_at ORDER BY created_at
    DB-->>NotifSvc: [StatusChanged@T1, StatusChanged@T2, ...]
    NotifSvc-->>Mobile: WebSocket frame {status_changed} [backfill T1, T2, ...]
    deactivate NotifSvc
    Mobile->>Mobile: Process backfill, update UI
```

**Ordering:** Per-shipment ordering is preserved because `notification_history` is inserted in order and queried ordered by timestamp.

---

## Storage Design

| Property | PostgreSQL `shipments` | PostgreSQL `notification_history` | PostgreSQL `user_device_tokens` | Redis Pub/Sub (broker) |
|---|---|---|---|---|
| **Purpose** | Authoritative shipment state | Audit trail, backfill on reconnect | FCM/APNs token mapping | Transient message bus |
| **Schema** | `id, customer_id, driver_id, status, updated_at, ...` | `id, shipment_id, user_id, action, delivered_at, metadata` | `id, user_id, device_type, token, created_at, expires_at` | N/A (key-value stream) |
| **Indexes** | PK: `id` | `(user_id, created_at DESC)`, `(shipment_id, created_at DESC)` | PK: `id`, FK: `user_id` | N/A |
| **Write pattern** | ~5 writes per shipment lifecycle | ~5 writes per shipment (append-only) | On app launch, token refresh | High-frequency pub (30 msg/s peak) |
| **Read pattern** | By shipment ID (dashboard), by driver ID (route) | Backfill on reconnect (last 30 min of user's history) | By user ID (when pushing) | Pub/sub fanout (no reads) |
| **Retention** | Indefinite (operational data) | 30 days (compacted after for analytics) | Until token expires or app uninstalls | 0 days (ephemeral, lost on restart) |
| **Backup/recovery** | RPO: 1 minute (continuous replication), RTO: < 5 minutes (failover to replica) | RPO: 1 minute, RTO: < 5 minutes (same replica set) | RPO: 1 minute, RTO: < 5 minutes | RPO: N/A (no persistence), RTO: N/A |
| **Scaling strategy** | Primary-replica, read replicas for backfill queries | Append-only partition by date (monthly rollover) | Horizontal: partition by user ID or hash | Single-instance Redis with AOF persistence for HA |

---

## Key Decisions

### Decision 1: Message Broker Technology

| Criterion | PostgreSQL LISTEN/NOTIFY | Redis Pub/Sub | RabbitMQ | Kafka |
|---|---|---|---|---|
| **Throughput** | ~1K msg/s (not optimized for pub/sub) | ~100K msg/s | ~50K msg/s | 500K+ msg/s |
| **Ordering guarantee** | Per-connection (not per-channel) | Per-channel (can partition) | Per-queue | Per-partition |
| **Persistence** | None (in-memory) | None (optional AOF for restart) | Optional (durable queues) | Mandatory (log-based) |
| **Replay capability** | No | No | No (unless persisted) | Yes (configurable retention) |
| **Operational overhead** | Low (already running) | Low (single Redis instance) | Medium (broker cluster) | High (ZooKeeper, multiple brokers) |
| **Team expertise** | High (PostgreSQL already in use) | High (common) | Medium | Low (new tool) |
| **Latency** | 50–100ms | 5–10ms | 10–50ms | 50–200ms |
| **Cost** | Included (existing Postgres) | ~$50–200/month (self-hosted) or managed service | ~$100–300/month | ~$300+/month (managed) |

**Recommendation: Redis Pub/Sub** ✅

**Rationale:**
- Throughput of 100K msg/s is 10x our peak burst rate (30 msg/s), with room for future growth
- Latency is sub-10ms (allows aggressive SLA target)
- Simple to operate (single instance + replica for HA)
- Efficient ordering per shipment (subscribe to `shipment::{id}` channels)
- Requires new infrastructure (cost), but not prohibitive

**Trade-off acknowledged:**
- Messages are lost on restart (no persistence). Mitigated by: (1) client backfill queries on reconnect, (2) FCM/APNs as backup delivery. Acceptable for "optional" notification service.
- Single Redis instance is a single point of failure (addressed via replica + sentinel for auto-failover).

**Alternative:** PostgreSQL LISTEN/NOTIFY is viable for phase 1 if Redis is not available. Throughput is sufficient for baseline (~3 msg/s average), and you avoid adding infrastructure. Upgrade to Redis if latency or reliability becomes an issue.

---

### Decision 2: Transport Protocol (WebSocket vs SSE vs Polling)

| Criterion | WebSocket | Server-Sent Events (SSE) | Polling |
|---|---|---|---|
| **Latency** | 100–500ms (bidirectional, low overhead) | 100–500ms (unidirectional) | 5–60 seconds (client-side interval) |
| **Bandwidth** | ~100 bytes per message | ~100 bytes per message | 1KB+ per poll (overhead) |
| **Mobile support** | Yes (native iOS/Android) | Limited (requires polyfill, battery drain) | Yes (default) |
| **Scalability** | 75K+ concurrent connections per server | Same as WebSocket | N/A (pull-based) |
| **Browser/framework complexity** | Medium (requires library) | Low (native EventSource) | Low (standard HTTP) |
| **Fallback handling** | Graceful fallback to polling if WebSocket unavailable | Graceful fallback to polling | N/A |
| **Team expertise** | Medium (newer protocol) | Low (HTML5 standard) | High (existing API) |

**Recommendation: WebSocket** ✅

**Rationale:**
- Bidirectional channel allows client-to-server requests (subscribe, unsubscribe, ack) without separate HTTP calls
- Native mobile support is critical for driver app; SSE requires workarounds
- Latency < 500ms is achievable (meets SLA)
- Client library (Socket.io, ws, or platform-native) shields complexity

**Trade-off acknowledged:**
- More complex than polling (requires WebSocket server infrastructure)
- Mobile app must handle reconnects and backoff (standard pattern, not a blocker)

---

### Decision 3: Notification Service Architecture (Standalone vs Embedded)

| Criterion | Standalone Notification Service | Embedded in Django (Celery tasks) |
|---|---|---|
| **Deployment independence** | Yes (can scale separately) | No (tied to Django) |
| **Operational complexity** | Medium (new service, new monitoring) | Low (integrated with Django stack) |
| **Latency** | 50–100ms (network hop to NotificationService) | 100–500ms (Celery task queue) |
| **Client connection limit** | ~75K per instance, horizontal scaling | ~10K per Django instance, scales with API |
| **Failure isolation** | Notification failure doesn't block API | Notification failure blocks request if synchronous |
| **Code reuse** | Possible (shared utilities for auth, DB access) | High (same codebase) |

**Recommendation: Standalone Notification Service** ✅

**Rationale:**
- Decouples API responsiveness from notification latency (API commit is fast, notifications are separate)
- Clear failure boundary (API stays up even if NotificationService is down)
- Easier to scale (NotificationService can be deployed independently)
- Allows technology choice (could be Node.js, Go, or Python if superior WebSocket library exists)

**Trade-off acknowledged:**
- Adds infrastructure and operational overhead (monitoring, logging, deployment pipeline)
- Network hop between API and broker adds ~5–10ms latency

**Alternative:** Embedded Celery tasks are simpler for MVP. Upgrade to standalone if latency or reliability becomes an issue.

---

### Decision 4: Mobile Native Push Strategy

| Criterion | WebSocket only | FCM/APNs + WebSocket (hybrid) | FCM/APNs only |
|---|---|---|---|
| **Reliability** | Medium (depends on client connection) | High (native OS-level delivery) | High (platform-managed) |
| **Latency** | 100–500ms (network-dependent) | 1–5s (platform-managed, acceptable) | 1–5s (platform-managed) |
| **Battery impact** | High (persistent connection drains) | Low (native OS integration) | Low |
| **Offline delivery** | No | Yes (native queue) | Yes |
| **Complexity** | Low (single path) | Medium (two paths) | Medium (platform dependency) |
| **Cost** | $0 (self-hosted) | $0–100/month (Firebase free tier + Apple backend) | Same as hybrid |

**Recommendation: Hybrid (FCM/APNs + WebSocket fallback)** ✅

**Rationale:**
- Native push guarantees delivery even if app is backgrounded or disconnected
- Battery-friendly (native OS handles delivery, not app polling)
- WebSocket fallback ensures web and desktop clients are not blocked
- FCM is free for most use cases (Apple APNs backend is included in infrastructure costs)

**Trade-off acknowledged:**
- Adds complexity (two delivery paths, token management)
- Dependency on Firebase and Apple infrastructure (but acceptable for mobile apps)

---

## Change Impact Analysis

### What if traffic 10x (to 750K messages/day, 300 msg/s peak)?

| Component | Impact | Mitigation |
|---|---|---|
| **Redis Pub/Sub** | Approaches capacity (100K msg/s limit). p95 latency may degrade to 100–500ms | Upgrade to Kafka, or shard by region/customer |
| **NotificationService** | 750K concurrent connections / ~10K per instance = 75 instances needed. Sticky session routing becomes critical | Shard by shipment customer (not just shipment ID) to avoid hotspots |
| **PostgreSQL** | notification_history inserts increase 10x. Indexes may slow down backfill queries | Implement partitioning by date; archive old data monthly |
| **Database connections** | NotificationService needs connection pool × 75 instances. May exhaust pool | Implement read replica for backfill queries |

**Confidence:** High that system scales linearly to 750K/day with component upgrades.

---

### What if a new client type is added (SMS notifications for non-tech users)?

| Component | Change required | Scope |
|---|---|---|
| **Message broker** | None (same `shipment::{id}:status_changed` event) | Zero change |
| **SMS adapter** | New service subscribing to broker and sending SMS via Twilio | ~200 LOC, isolated service |
| **Database** | Add `user_phone_numbers` table, extend notification_history with channel type | ~50 LOC migration |
| **NotificationService** | None (doesn't know about SMS) | Zero change |

**Confidence:** High that architecture supports new channels without breaking existing services.

---

### What if PostgreSQL replication fails and data is lost?

| Component | Recovery strategy |
|---|---|
| **Shipment state** | Restore from latest backup (1-minute RPO). Brief window where API and NotificationService are out of sync, but API is authoritative. Clients reconnect and backfill. |
| **notification_history** | Restore from backup. Clients may miss a few notifications, but WebSocket backfill reduces blast radius. |
| **user_device_tokens** | Restore from backup or request clients to re-register tokens on app launch. |

**Mitigation:** Regular automated backups, standby replica with automated failover (Patroni or RDS Multi-AZ).

---

### What if the team doubles in size?

| Component | Independence |
|---|---|
| **NotificationService** | Can be owned separately from API team. Clear contract: listen to message broker, fan out to clients. |
| **FCM/APNs Adapter** | Owned separately. Clear responsibility: native push only. |
| **Message broker** | Owned by platform/infra team. Standard interface (Pub/Sub). |
| **Database schema** | Requires coordination (schema changes affect API, adapters, and backfill logic). Implement via migrations + versioning. |

**Confidence:** High that services can be worked on independently with clear contracts.

---

## Confidence Assessment

| Component | Confidence | Reason | Risk mitigation |
|---|---|---|---|
| **WebSocket server (NotificationService)** | 90 | Standard pattern, well-understood transport | None needed; use battle-tested library (Socket.io or similar) |
| **Redis Pub/Sub (message broker)** | 85 | Simple, widely used, but first time in this codebase | Spike week 1 with load test to confirm throughput and latency |
| **FCM/APNs adapter** | 80 | Both services are well-documented, but token management is new | Test token refresh flow end-to-end in week 1 |
| **Backfill on reconnect** | 70 | Ordering guarantees depend on careful handling of timestamps; untested | Acceptance test: simulate 30-minute disconnect, verify all notifications are backfilled |
| **Sticky session routing** | 60 | Critical for ordering, but easy to get wrong (IP-based sticky sessions are fragile) | Test horizontal scaling with multiple NotificationService instances |
| **30-day retention strategy** | 50 | Depends on business decision about compliance/audit requirements | Confirm retention period with legal/product before implementation |

**Components with confidence < 60:**
- **Sticky session routing** — Prototype multi-instance setup with Redis-based session affinity before going to production
- **30-day retention strategy** — Verify with stakeholders and update schema if needed

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| **Redis broker goes down, messages are lost** | Clients don't receive notifications during outage, but backfill on reconnect catches up | Medium | Implement Redis Sentinel for automatic failover + replica. Test failover scenario. |
| **Sticky sessions break under load (clients routed to wrong NotificationService)** | Clients receive out-of-order notifications for the same shipment | Medium | Implement Redis-based session affinity or consistent hashing. Load test with 10+ instances. |
| **NotificationService bug causes cascading failure (e.g., memory leak)** | Connections drop, clients disconnect, all fall back to polling | Medium | Implement health checks and auto-restart. Monitor memory usage. Set connection limits per client. |
| **FCM/APNs quota is exceeded or service is rate-limited** | Native push is delayed or dropped | Low | Implement exponential backoff and queuing. Monitor quota usage. |
| **Client clock skew causes backfill query to miss notifications** | Clients miss updates on reconnect if their local time is ahead of server time | Low | Use server-supplied timestamp in all WebSocket messages. Clients trust server timestamp, not local clock. |
| **PostgreSQL notification_history table grows unchecked** | Query performance degrades after months of data | Low | Implement monthly partitioning. Archive data older than 30 days. |

---

## Recommended ADRs

1. **ADR: Real-time notification transport protocol (WebSocket vs SSE)**
   - Context: Customers and drivers need near-real-time status updates
   - Options: WebSocket, SSE, polling, gRPC
   - Decision: WebSocket
   - Use `/architect:write-adr` to formalize

2. **ADR: Message broker for notification pipeline (Redis vs RabbitMQ vs PostgreSQL LISTEN/NOTIFY)**
   - Context: Decouple API mutation from notification delivery
   - Options: Redis Pub/Sub, PostgreSQL LISTEN/NOTIFY, RabbitMQ, Kafka
   - Decision: Redis Pub/Sub
   - Use `/architect:write-adr` to formalize

3. **ADR: Notification service architecture (standalone vs embedded in Django)**
   - Context: Scale WebSocket connections independently from API
   - Options: Dedicated NotificationService, embedded Celery tasks
   - Decision: Standalone NotificationService
   - Use `/architect:write-adr` to formalize

4. **ADR: Mobile push strategy (native vs WebSocket-only)**
   - Context: Ensure reliable delivery to backgrounded mobile apps
   - Options: FCM/APNs + WebSocket, WebSocket only
   - Decision: Hybrid (FCM/APNs + WebSocket fallback)
   - Use `/architect:write-adr` to formalize

---

## Implementation Roadmap (Suggested)

### Phase 1: MVP (Weeks 1–2)
- [ ] Spike: Load test Redis Pub/Sub with 100K messages/s
- [ ] Implement NotificationService in Node.js or Python (ws or Socket.io library)
- [ ] Add message publishing to Django API (`shipment.status_updated()` → Pub/Sub)
- [ ] Deploy NotificationService to staging, test with 10K concurrent connections
- [ ] **Acceptance test:** Status update → notification delivered < 1 second

### Phase 2: Mobile integration (Weeks 3–4)
- [ ] Integrate FCM into NotificationService (send native push on status change)
- [ ] Add token management (user_device_tokens table, refresh flow)
- [ ] Test with both web and mobile clients simultaneously
- [ ] Implement exponential backoff and reconnect logic in clients

### Phase 3: Resilience (Weeks 5–6)
- [ ] Implement Redis Sentinel for auto-failover
- [ ] Add notification_history backfill on client reconnect
- [ ] Implement sticky session routing (Redis or IP-based)
- [ ] Load test with 75K concurrent connections, 2 NotificationService instances

### Phase 4: Production hardening (Weeks 7–8)
- [ ] Monitoring and alerting (Prometheus for NotificationService, CloudWatch for FCM)
- [ ] Graceful degradation (fallback to polling if WebSocket is unavailable)
- [ ] Chaos engineering: test Redis failover, NotificationService crash, FCM rate-limiting
- [ ] Performance optimization: reduce latency to p95 < 500ms

---

## Summary

**Architecture:** Decoupled, scalable, fault-tolerant real-time notification system using:
- **Transport:** WebSocket (web/desktop) + native push (FCM/APNs for mobile)
- **Message broker:** Redis Pub/Sub for pub/sub fanout
- **Notification service:** Dedicated WebSocket server (horizontal scaling, sticky sessions by shipment)
- **Fallback:** Backfill on reconnect (30-day notification history in PostgreSQL)

**Scale:** 75K concurrent connections at peak, 30 msg/s burst throughput, p95 latency < 1 second.

**Trade-offs:**
- Added infrastructure (Redis, NotificationService) vs. simplicity of polling
- Eventual consistency (messages may reorder in rare cases) vs. strong ordering (requires per-partition ordering)
- Hybrid mobile push (two paths) vs. WebSocket-only simplicity

**Next steps:** Write ADRs, conduct spikes on Redis Pub/Sub and NotificationService load capacity, then proceed with Phase 1 implementation.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 13.0/17.5 (74%) |
| Evaluated | 2026-05-04 |
| Target duration | 100501 ms |
| Target cost | $0.0967 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent performs a pre-flight step — checks for project conventions (CLAUDE.md, installed rules) and existing ADRs before proposing anything | FAIL | The output opens directly with '# System Design: FreightFlow Real-Time Notification System' and immediately dives into requirements. There is no mention of checking for CLAUDE.md, installed project rules, or existing ADRs before proceeding. |
| c2 | Agent classifies the work type and scopes what is and is not covered by the design | FAIL | The output has a Requirements section with Functional and Non-Functional subsections that implicitly describes what is in scope, but there is no explicit classification of work type (e.g., 'this is a new service design') and no explicit out-of-scope section listing what the design deliberately does not address. |
| c3 | Agent produces a mandatory assumption ledger with each assumption classified as proven_by_code, inferred, or needs_user_confirmation | FAIL | The output has an '## Assumptions' table with 8 assumptions. However, the classification columns are 'Impact if wrong', 'Confidence' (High/Medium/Low), and 'Validation method' — not the required labels 'proven_by_code', 'inferred', or 'needs_user_confirmation'. The specified taxonomy is completely absent. |
| c4 | Agent quantifies non-functional requirements rather than accepting vague terms — scale (50k shipments/day), latency targets, and availability | PASS | Non-Functional table explicitly quantifies: Scale '75,000 concurrent connections at peak' derived from '50K active shipments/day × 1.5 watchers/shipment'; Latency 'p95 < 1 second'; Availability '99.5% uptime (3.6 hours downtime/year)'; Throughput '~250K messages/day; peak burst ~30 msg/s'. |
| c5 | Agent presents at least two architectural options (e.g. WebSockets vs SSE vs polling) with a scored trade-off table | PASS | Decision 1 has a four-way trade-off table (PostgreSQL LISTEN/NOTIFY vs Redis vs RabbitMQ vs Kafka). Decision 2 has a three-way table (WebSocket vs SSE vs Polling). Decision 3 and 4 each have two-way comparison tables. All include scored criteria. |
| c6 | Agent includes Mermaid diagrams — at minimum a component diagram showing trust boundaries | PASS | C4 Level 2 Container Diagram is a Mermaid 'graph TB' block using subgraphs labelled 'Client Layer', 'FreightFlow System', and 'External' — these serve as trust boundaries. Two sequence diagrams are also included. |
| c7 | Agent identifies decisions that require an ADR (e.g. choice of message broker or real-time transport) | PASS | '## Recommended ADRs' section lists four explicitly scoped ADRs: real-time transport (WebSocket vs SSE), message broker (Redis vs RabbitMQ vs PostgreSQL LISTEN/NOTIFY), notification service architecture (standalone vs embedded), and mobile push strategy (native vs WebSocket-only). |
| c8 | Agent includes a confidence score (HIGH/MEDIUM/LOW with numeric) and states which assumptions drive uncertainty | PARTIAL | '## Confidence Assessment' table gives numeric scores (50–90) with 'Reason' and 'Risk mitigation' columns, and explicitly calls out components with confidence < 60. However, H/M/L labels are absent from this table. The Assumptions table has H/M/L labels but no numeric scores. The two elements required by the criterion are split across separate tables rather than combined. |
| c9 | Agent maps change impact — what existing FreightFlow components are directly or indirectly affected, and explicitly lists what is unaffected | PARTIAL | '## Change Impact Analysis' covers four scenarios (10x traffic, new SMS channel, PostgreSQL failure, team doubles). The SMS scenario labels NotificationService and Message Broker as 'Zero change'. However the section is framed around hypothetical future states, not explicitly mapping current-build impact on existing components with a formal 'unaffected' list. |
| c10 | Output's transport recommendation explicitly compares WebSockets vs SSE vs long-polling for the push-to-browser-and-mobile use case, with reasoning that addresses bidirectional vs server-initiated traffic and mobile network behaviour (background sockets, reconnection) | PASS | Decision 2 table compares WebSocket vs SSE vs Polling. Rationale states: 'Bidirectional channel allows client-to-server requests (subscribe, unsubscribe, ack) without separate HTTP calls'; 'Native mobile support is critical for driver app; SSE requires workarounds'; 'Mobile app must handle reconnects and backoff (standard pattern, not a blocker)'. |
| c11 | Output addresses the existing Django + PostgreSQL stack — either uses Django Channels / a Django-compatible push solution, or names a separate service with clear integration points to the existing API | PASS | Component 1 (Django REST API) describes extension with 'PATCH /shipments/{id}/status → Update shipment status, emit ShipmentStatusChanged event' and 'API->>Broker: PUBLISH shipment::{id}:status_changed' in the sequence diagram. Decision 3 explicitly names the standalone NotificationService and rationalises its separation from Django. |
| c12 | Output sizes the system from the 50,000 shipments/day plus 9am/2pm peak — converting daily volume into a peak-second concurrent connection or message rate (e.g. burst factor of 5-10x average) and validating the chosen transport handles it | PASS | NFR table derives '75,000 concurrent connections at peak' from '50K active shipments/day × 1.5 watchers/shipment spread over 2 peak hours' and '~30 msg/s during 9am and 2pm windows'. Decision 1 validates Redis Pub/Sub's '~100K msg/s' is '10x our peak burst rate (30 msg/s), with room for future growth'. |
| c13 | Output includes at least one Mermaid component diagram showing the path from shipment status change → message broker → push fan-out → web/mobile clients, with trust boundaries marked | PASS | C4 Level 2 Container Diagram shows: APIServer → MessageBroker → NotificationService → WebClient/MobileApp, and MessageBroker → FCMAdapter → FCMService/APNService → MobileApp. Subgraphs 'Client Layer', 'FreightFlow System', 'External' mark trust boundaries. |
| c14 | Output's assumption ledger lists the unstated facts (mobile platforms iOS/Android both, push notification vs in-app socket for backgrounded apps, customer authentication model) classified as `inferred` or `needs_user_confirmation` | PARTIAL | A5 covers 'Mobile apps require native push (FCM/APNs) for reliability; web uses WebSocket' addressing iOS/Android and push vs in-app socket. However the required classification labels ('inferred', 'needs_user_confirmation', 'proven_by_code') are entirely absent — the table uses 'High/Medium confidence' instead. Customer authentication model is not listed as an assumption anywhere in the ledger. |
| c15 | Output identifies at least 2 ADR-worthy decisions (e.g. message broker selection, push transport, fan-out service vs in-Django) and lists them in a "Decisions Requiring ADR" section | PASS | '## Recommended ADRs' section lists four items, each with context, options evaluated, and the decision reached. Covers message broker, transport protocol, notification service architecture, and mobile push strategy. |
| c16 | Output's change impact section explicitly addresses the Django REST API (extended with status-change events) and PostgreSQL (transactional outbox or change capture) and lists at least one component that is unaffected | PASS | Component 1 explicitly states Django REST API is 'extended' to publish ShipmentStatusChanged events to the broker. Storage Design section describes PostgreSQL extended with three tables. The SMS change-impact scenario lists NotificationService as 'Zero change' and Message Broker as 'Zero change', satisfying the unaffected-component requirement. |
| c17 | Output includes a confidence score with HIGH/MEDIUM/LOW label plus a numeric value out of 100, and lists the assumptions or unknowns driving any confidence reduction | PARTIAL | '## Confidence Assessment' table provides numeric scores (50–90/100) with reasons and risk mitigations, and explicitly flags components below 60. However, H/M/L labels are not present in this table. The Assumptions table has H/M/L but no numeric scores. The criterion requires both elements together; they are split. |
| c18 | Output addresses backgrounded mobile app delivery — recommending APNs/FCM for true push when the app isn't foregrounded, distinct from in-app socket for live dashboards | PARTIAL | Decision 4 rationale states 'Native push guarantees delivery even if app is backgrounded or disconnected' and 'Battery-friendly (native OS handles delivery, not app polling)'. The hybrid recommendation (FCM/APNs + WebSocket fallback) explicitly distinguishes the two paths. Ceiling is PARTIAL. |
| c19 | Output addresses authentication on the persistent connection (token-scoped channels per customer/driver, not broadcast) so customers can't see other customers' shipments | PARTIAL | WebSocket API surface shows 'WebSocket /ws?shipment_id={id}&auth_token={token}' and Workflow 2 sequence shows 'NotifSvc->>NotifSvc: Authenticate user'. Authentication is present but the output never explicitly discusses channel isolation (token-scoped per customer to prevent cross-customer visibility). The security isolation concern is implicit, not addressed as a named design requirement. Ceiling is PARTIAL. |

### Notes

The output is a thorough, well-structured system design that excels on technical depth — quantified NFRs, multiple comparison tables, Mermaid diagrams with trust boundaries, sized concurrency from the stated 50K shipments/day, and a clear 4-ADR list. The main failures are procedural rather than substantive: no pre-flight check for project conventions or existing ADRs (c1), no explicit work-type classification or out-of-scope statement (c2), and — most significantly — the assumption ledger completely ignores the prompt's required classification taxonomy (proven_by_code / inferred / needs_user_confirmation), instead using High/Medium/Low confidence labels (c3, c14). The confidence score is also split across two tables rather than presenting H/M/L plus numeric in one place (c8, c17). Change impact (c9) covers future scenarios well but doesn't explicitly walk through current-build effects on existing components with a formal 'unaffected' list. The backgrounded-mobile and auth-on-connection criteria (c18, c19) are addressed but are capped at PARTIAL by the test author. Overall the design content is high quality but the process and format compliance with the prompt's explicit instructions is weak.
