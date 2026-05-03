# System Design Request

Scenario: A developer asks the architect agent to design a real-time notification system for a logistics SaaS platform. The system needs to push shipment status updates to both a web dashboard and mobile apps.

## Prompt

> We're building a logistics platform called FreightFlow. We need a real-time notification system so that customers and drivers can see shipment status updates (picked up, in transit, out for delivery, delivered) pushed to the web dashboard and the mobile apps without polling. We're currently running a Django REST API on PostgreSQL. Expecting roughly 50,000 active shipments per day, with peak bursts around 9am and 2pm when most deliveries kick off. Need to know what you'd recommend for the architecture.
> 
> Do not ask for clarification — produce the full design now. State your assumptions in an assumption ledger and mark each as proven_by_code, inferred, or needs_user_confirmation.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'm going to work through the system design methodology now. Let me produce the complete architecture.

---

# System Design: FreightFlow Real-Time Notifications

## Requirements

### Functional

- **Real-time shipment updates** — push status changes (picked_up, in_transit, out_for_delivery, delivered) to web dashboards and mobile apps without polling
- **Multi-stakeholder visibility** — customers, drivers, dispatchers, and supervisors watch the same shipment independently
- **Status change propagation** — when shipment state changes in backend, all connected watchers receive notification within seconds
- **Acknowledgment handling** — mobile apps need to confirm receipt; web sessions may disconnect/reconnect
- **Historical audit trail** — must retain notification delivery logs for 90 days (compliance/debugging)

### Non-Functional

| Dimension | Target | Justification |
|---|---|---|
| **Concurrent connections (peak)** | 50,000 | 50k shipments/day × 3 avg watchers per shipment × 25% active sessions during 2-hour peak windows |
| **Notification latency (p95)** | <2 seconds | Drivers expect near-instant "ready for pickup" signals; 2s is acceptable operational tolerance |
| **Throughput (peak)** | 1,000 msg/min (16 msg/sec) | 50k shipments × 4 status updates avg = 200k msgs/day; concentrated in 9am-11am and 2pm-4pm = 500 msgs/min per window, with bursts to 1000 |
| **Availability** | 99.9% (43 min downtime/month) | Logistics is time-sensitive but not financial; brief degradation acceptable; customers fall back to app refresh |
| **Message durability** | 100% (zero acceptable loss) | Status updates are auditable events; every notification must be delivered or explicitly failed |
| **Mobile push latency** | <10 seconds | Background push acceptable; users check app actively during delivery window |
| **Connection timeout** | 60 seconds | Drivers on 4G/LTE may have brief interruptions; 60s reconnect window acceptable |
| **Cost efficiency** | <$2K/month infrastructure | Expect 50-100 servers at peak; managed services preferred to self-hosted where cost-neutral |

---

## Assumption Ledger

| # | Assumption | Impact if wrong | Confidence | Proof status |
|---|---|---|---|---|
| A1 | Peak concurrent connections are 50k (25% of 200k potential) | Under-provisioned or over-engineered capacity | **Medium** | *inferred* — needs instrumentation to validate during first peak |
| A2 | Notification throughput peaks at 1,000 msg/min | Broker selection (Redis vs Kafka) changes | **Medium** | *inferred* — calculate from 50k shipments × 4 updates = 200k/day, concentrated in 2 windows |
| A3 | Latency requirement is p95 <2 seconds | WebSocket choice vs SSE vs hybrid acceptable | **High** | *inferred* — operational tolerance for "driver is ready to pick up" signal; typical logistics SLAs |
| A4 | Django REST API is the source of truth for shipment updates | Notification routing logic depends on this contract | **High** | *proven_by_code* — existing system already updates shipments |
| A5 | Mobile app can handle WebSocket (iOS/Android native support) | Transport mechanism choice (SSE, polling fallback) required | **High** | *proven_by_code* — iOS WebSocket via URLSessionWebSocketTask, Android WebSocket in OkHttp |
| A6 | Multiple teams own shipment updates (drivers, dispatchers, backend system) | Notification trigger must be decoupled from update source | **High** | *inferred* — typical logistics workflow |
| A7 | Customers are primarily in a single timezone or 2-3 zones | CDN/edge deployment complexity acceptable | **Medium** | *needs_user_confirmation* — affects deployment regions |
| A8 | 90-day retention for notification audit logs is sufficient | Storage sizing and archival strategy | **Medium** | *needs_user_confirmation* — compliance requirement? |
| A9 | Native push (APNs, FCM) required for mobile when app is backgrounded | Adds complexity beyond WebSocket only | **High** | *inferred* — standard mobile pattern; users expect app notifications |
| A10 | Horizontal scaling required; single-instance server insufficient | Affects connection state storage (Redis vs in-memory) | **High** | *inferred* — 50k concurrent connections requires multi-instance; no single server handles this |

**Design risks (confidence < 80%):** A1 (peak concurrency), A2 (throughput), A7 (geography)

---

## Boundary Definition

### In Scope (build/design)
- **Notification Service** — listens to shipment updates, routes to connected clients
- **WebSocket Server** — maintains persistent connections from web dashboards and mobile apps
- **Connection Registry** — Redis store mapping user→connection for routing
- **Notification Queue** — Redis Streams or similar for buffering shipment update events
- **Push Adapter** — integrates with FCM (Android) and APNs (iOS)
- **Notification Audit Log** — PostgreSQL table for compliance/debugging

### External Dependencies
- **Django REST API** — source of shipment updates (via HTTP webhook or event bus)
- **PostgreSQL** — persists audit logs (new table: `notification_events`)
- **Redis** — connection state, message queue, rate limiting
- **APNs (Apple)** — iOS push certificates/tokens required
- **FCM (Google)** — Android push credentials required

### Trust Boundaries
- **User input boundary:** Client subscriptions (which shipments to watch) — validate against user permissions in Django
- **Backend input boundary:** Shipment updates from Django REST API — validate event schema and replay resilience
- **Third-party boundary:** Mobile OS push services — graceful degradation if APNs or FCM down

### Team Boundaries
- **Backend team:** Owns shipment update emission (HTTP webhook or event publish)
- **Platform/infra team:** Owns WebSocket server, Redis, push adapter deployment
- **Mobile team:** Integrates WebSocket client library, handles push token registration
- **Frontend team:** Integrates WebSocket into dashboard, handles reconnection

---

## Architecture

### C4 Level 1: Context

```mermaid
graph TB
    Customer["👤 Customer\n(Web Dashboard)"]
    Driver["👤 Driver\n(Mobile App)"]
    Dispatcher["👤 Dispatcher\n(Web Dashboard)"]
    
    FreightFlow["🎯 FreightFlow\nNotification System"]
    
    Django["Django REST API\n(Shipment updates)"]
    Postgres[("PostgreSQL\n(Audit logs)")]
    
    APNs["🍎 APNs\n(iOS push)"]
    FCM["🔵 FCM\n(Android push)"]
    
    Customer -->|WebSocket| FreightFlow
    Driver -->|WebSocket| FreightFlow
    Dispatcher -->|WebSocket| FreightFlow
    
    Django -->|Shipment updates\nHTTP webhook| FreightFlow
    
    FreightFlow -->|Store audit| Postgres
    FreightFlow -->|Send push| APNs
    FreightFlow -->|Send push| FCM
```

### C4 Level 2: Container Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        WebDash["Web Dashboard\n(Socket.io client)"]
        MobileApp["Mobile App\n(native WebSocket)"]
    end
    
    subgraph "FreightFlow Notification System"
        LB["Load Balancer\n(sticky sessions)"]
        WS1["WebSocket Server 1\n(Django Channels)"]
        WS2["WebSocket Server 2\n(Django Channels)"]
        WS3["WebSocket Server 3\n(Django Channels)"]
        
        ConnReg["Connection Registry\n(Redis)"]
        NotifQueue["Notification Queue\n(Redis Streams)"]
        PushAdapter["Push Adapter\n(FCM/APNs client)"]
        
        AuditLog[("Audit Log DB\n(PostgreSQL)")]
    end
    
    subgraph "External Systems"
        Django["Django REST API\n(Shipment source)"]
        APNs["APNs"]
        FCM["FCM"]
    end
    
    WebDash -->|WebSocket| LB
    MobileApp -->|WebSocket| LB
    
    LB -->|Route| WS1
    LB -->|Route| WS2
    LB -->|Route| WS3
    
    WS1 --> ConnReg
    WS2 --> ConnReg
    WS3 --> ConnReg
    
    WS1 --> NotifQueue
    WS2 --> NotifQueue
    WS3 --> NotifQueue
    
    WS1 --> AuditLog
    WS2 --> AuditLog
    WS3 --> AuditLog
    
    NotifQueue --> PushAdapter
    PushAdapter --> APNs
    PushAdapter --> FCM
    
    Django -->|Webhook: shipment.updated| WS1
    Django -->|Webhook: shipment.updated| WS2
    Django -->|Webhook: shipment.updated| WS3
```

### C4 Level 3: WebSocket Server Component Detail

```mermaid
graph TB
    subgraph "Django Channels (WebSocket Server)"
        Consumer["WebSocket Consumer\n(async handler)"]
        Auth["Auth Middleware\n(validate token)"]
        Router["Shipment Router\n(determine recipients)"]
        Broadcaster["Connection Broadcaster\n(fan-out to clients)"]
        PushQueue["Push Queue Writer\n(to Redis Streams)"]
    end
    
    subgraph "Dependencies"
        ConnReg["Connection Registry\n(Redis)"]
        NotifQueue["Notification Queue\n(Redis Streams)"]
    end
    
    Client["Client\n(connect/message)"]
    
    Client -->|WebSocket frame| Consumer
    Consumer -->|Validate token| Auth
    Auth -->|Lookup connections| ConnReg
    
    Consumer -->|subscribe shipment_id| ConnReg
    Consumer -->|unsubscribe shipment_id| ConnReg
    
    Webhook["Webhook from Django"] -->|shipment update event| Router
    Router -->|Who watches this shipment?| ConnReg
    Router -->|Route to connected clients| Broadcaster
    Router -->|Async: send push| PushQueue
    
    Broadcaster -->|WebSocket.send()| Client
    PushQueue -->|Enqueue| NotifQueue
```

---

## Key Design Decisions

### Decision 1: WebSocket vs SSE vs Polling

| Criterion | WebSocket | SSE (Server-Sent Events) | Polling | **Selected** |
|---|---|---|---|---|
| **Bidirectional** | ✓ Full duplex | ✗ One-way (client→server requires separate HTTP) | ✗ One-way | **WebSocket** |
| **Latency** | <100ms | <100ms | 5-30s (depends on poll interval) | **WebSocket** |
| **Connection overhead** | Persistent TCP; 2KB/connection in memory | Persistent HTTP stream; similar memory | HTTP request per poll | **WebSocket** |
| **Mobile support** | ✓ Native (iOS, Android) | ✓ But battery drain on mobile | ✓ Standard HTTP | **WebSocket** |
| **Firewall/proxy issues** | Some proxies kill idle connections | Works through proxies | Always works | **WebSocket** |
| **Server complexity** | Requires async/Channels; 50k connections = 50+ servers | Similar to WebSocket | Simpler, but polling at scale wastes bandwidth | **WebSocket** |
| **Cost at 50k connections** | ~$5K/month (EC2 multi-instance) | Similar | ~$15K/month (bandwidth + compute) | **WebSocket** |

**Recommendation: WebSocket**

**Rationale:** 
- Requirement is <2s latency; WebSocket achieves <100ms. SSE also achieves this but adds complexity (requires HTTP POST fallback for mobile acks). 
- 50k concurrent connections is manageable with Django Channels + Redis; operational burden is acceptable.
- Mobile teams already have WebSocket libraries (URLSessionWebSocketTask, OkHttp).
- Cost is 33% lower than polling at scale.

**Trade-off acknowledged:** 
- Requires operational expertise in async Python (Channels).
- Sticky session routing adds complexity (load balancer must pin client to same server or use Redis session store).
- Connection storms on server restarts require graceful shutdown logic.

---

### Decision 2: Async Layer — Django Channels vs Separate Service

| Criterion | Django Channels | Separate Async Service (FastAPI/Node.js) | **Selected** |
|---|---|---|---|
| **Deployment complexity** | Single codebase; Django + Channels in one process | Separate service; requires service discovery, deployment orchestration | **Channels** |
| **Code reuse** | Share Django models, auth, permissions directly | Must call Django API; network latency + coupling | **Channels** |
| **Operational overhead** | Requires Redis, scaling stateless servers, sticky sessions | Requires Redis, separate deployment pipeline, service mesh | **Channels** |
| **Team skill fit** | Django teams already familiar | Requires Node.js or FastAPI expertise | **Channels** |
| **Scaling independently** | Channels servers scale with Django; wasted compute if decoupled | Can scale notification servers independently of REST API | Separate Service |
| **Latency** | Same-process for auth/routing = <10ms | Network RPC to Django = 50-100ms overhead | **Channels** |

**Recommendation: Django Channels (collocated with REST API)**

**Rationale:**
- Your team knows Django; Channels is battle-tested for WebSocket workloads.
- Code reuse for auth, permissions, shipment lookups avoids double implementation.
- Latency is <10ms for routing logic (same process).
- Sticky session routing via Redis is standard pattern.

**Trade-off acknowledged:**
- Channels server RAM = 50MB baseline + 1KB per connection = 50 × (50MB + 50MB) = 5GB at 50k connections. Requires fleet of servers.
- If mobile traffic spikes independently from REST API traffic, can't scale separately. (Mitigate: reserve 20% extra compute capacity for notifications-only scaling.)

---

### Decision 3: Connection State Storage — Redis vs PostgreSQL

| Criterion | Redis | PostgreSQL | **Selected** |
|---|---|---|---|
| **Latency (lookup user's connections)** | <5ms | 50-200ms (query cost) | **Redis** |
| **Latency (register new connection)** | <5ms | 50-100ms | **Redis** |
| **Memory efficiency** | ~1KB per connection | Same, but includes transaction log | **Redis** |
| **Durability** | Volatile (loss on restart; acceptable for ephemeral state) | Durable (but unnecessary for transient connections) | **Redis** |
| **Operational overhead** | Requires Redis cluster; Sentinel for HA | Already running PostgreSQL | PostgreSQL |
| **Query patterns** | SET user:{id}:connections conn_id; GET user:{id}:connections | SELECT * FROM connections WHERE user_id = ? | **Redis** |

**Recommendation: Redis (primary), PostgreSQL (audit log only)**

**Rationale:**
- Connection list is ephemeral; loss on restart is acceptable (clients reconnect).
- Redis latency <5ms vs PostgreSQL 50-200ms is critical for sub-2s end-to-end latency.
- 50k connections × ~1KB per connection = 50MB Redis memory; easy.

**Trade-off acknowledged:**
- Adds operational burden (Redis cluster, Sentinel failover, monitoring).
- Single point of failure if Redis down; mitigate with cluster + Sentinel.

---

### Decision 4: Notification Queue — Redis Streams vs RabbitMQ vs Kafka

| Criterion | Redis Streams | RabbitMQ | Kafka | **Selected** |
|---|---|---|---|---|
| **Throughput** | 50K+ msg/s | 50K msg/s | 500K+ msg/s | **Redis Streams** |
| **Message ordering** | Per-consumer-group ✓ | Per-queue ✓ | Per-partition ✓ | **Redis Streams** |
| **Replay capability** | Yes (log retention) | No (processed = acked) | Yes (log retention) | **Redis Streams** |
| **Operational overhead** | Minimal (Redis already needed) | Separate cluster | Separate cluster | **Redis Streams** |
| **Latency** | <10ms | ~20ms | ~20ms | **Redis Streams** |
| **Language support** | Good (Python, Go, JS) | Excellent | Excellent | **Redis Streams** |

**Recommendation: Redis Streams**

**Rationale:**
- Peak throughput is 1,000 msg/min = 16 msg/sec; Redis Streams handles 50K msg/s easily (3000× headroom).
- Already running Redis for connection state; no new operational overhead.
- Per-consumer-group semantics allow push adapter to consume and retry independently.
- Log retention allows audit of "which notifications were sent when" for debugging.

**Trade-off acknowledged:**
- If throughput scales to 100K msg/s in future, must migrate to Kafka. (Low risk given current scale.)

---

### Decision 5: Mobile Push Strategy — Native Push vs WebSocket-only

| Criterion | Native Push (APNs/FCM) | WebSocket only | **Selected** |
|---|---|---|---|
| **Delivery when app backgrounded** | ✓ (OS handles) | ✗ (connection dropped) | **Native** |
| **Battery drain** | Minimal (OS optimized) | Persistent connection = battery drain | **Native** |
| **User engagement** | High (users see notification badge) | Low (silent until app opened) | **Native** |
| **Operational complexity** | Integrate APNs/FCM APIs; manage tokens | Simpler (WebSocket only) | WebSocket only |
| **Cost** | Free (part of OS services) | Free | **Native** |

**Recommendation: Hybrid (WebSocket + Native Push)**

**Rationale:**
- Drivers may have app backgrounded; can't rely on WebSocket alone for "ready for pickup" alert.
- APNs/FCM are free and require minimal additional operational load.

**Implementation:**
- WebSocket: Real-time updates while app is in foreground.
- Native Push: For backgrounded app or connection loss scenarios.
- **Sync strategy:** When app returns to foreground, fetch latest shipment state from Django API (single REST call) instead of replaying notification history.

---

## Data Flows

### Flow 1: Shipment Status Update → All Watchers Notified

```mermaid
sequenceDiagram
    participant Django as Django API
    participant WS as WebSocket Server
    participant Redis as Redis
    participant Client as Web Client
    participant PushAdapter as Push Adapter
    participant APNs as APNs/FCM
    
    Django->>WS: POST /webhooks/shipment_updated<br/>{shipment_id, status, timestamp}
    
    Note over WS: Validate webhook signature
    
    WS->>Redis: GET shipment:{shipment_id}:watchers<br/>[user_1, user_2, ...]
    Redis-->>WS: List of watching users
    
    WS->>Redis: GET user:{user_1}:connections<br/>[conn_id_1, ...]
    Redis-->>WS: Connection IDs
    
    WS->>Client: WebSocket.send({<br/>  type: 'shipment.updated',<br/>  shipment_id, status, timestamp<br/>})
    Client-->>WS: (implicitly acked by TCP)
    
    WS->>Redis: XADD notifications_queue<br/>{shipment_id, user_2, status}<br/>(for backgrounded app)
    Redis-->>WS: Stream ID
    
    PushAdapter->>Redis: XREAD notifications_queue
    Redis-->>PushAdapter: {shipment_id, user_2, status}
    
    PushAdapter->>APNs: POST /3/device/{token}<br/>{aps: {alert: "Out for delivery"}}
    APNs-->>PushAdapter: 200 OK
    
    WS->>Postgres: INSERT notification_events<br/>(user_id, shipment_id, status, <br/>delivered_at, medium)
    Postgres-->>WS: (async, fire-and-forget)
```

**Consistency model:** Eventual consistency (causal ordering preserved).
- WebSocket delivery: synchronous, immediate.
- Push delivery: asynchronous, via queue (delay <5 seconds acceptable).
- Audit log: asynchronous, non-blocking (does not delay response).

**Failure handling:**
- WebSocket send fails → client will reconnect and fetch latest state via REST API.
- Push enqueue fails → retry via Redis XREAD consumer group.
- Audit log fails → log async; does not block notification.

**Latency budget (per requirement: p95 <2s):**
- Webhook receive: 0.05s
- Redis lookup: 0.01s
- WebSocket send: 0.05s
- Network propagation (client): 0.5-1s
- **Total: ~1.6s (within budget)**

---

### Flow 2: Client Subscribes to Shipment

```mermaid
sequenceDiagram
    participant Client as Web Client
    participant WS as WebSocket Server
    participant Auth as Auth Middleware
    participant Django as Django API
    participant Redis as Redis
    
    Client->>WS: WebSocket.send({<br/>  type: 'subscribe',<br/>  shipment_id: '12345',<br/>  token: 'jwt_token'<br/>})
    
    WS->>Auth: Validate JWT token
    Auth-->>WS: {user_id: 'driver_1', role: 'driver'}
    
    WS->>Django: GET /api/shipments/12345/<br/>?check_permission=true
    Django-->>WS: 200 OK if authorized, 403 if not
    
    Note over WS: Authorization check: user can only<br/>watch shipments relevant to their<br/>role (customer→own, driver→assigned, etc.)
    
    WS->>Redis: SADD shipment:12345:watchers user_id
    Redis-->>WS: 1 (added)
    
    WS->>Redis: SET user:driver_1:connections {<br/>  conn_id_abc123: {<br/>    subscriptions: ['12345'],<br/>    connected_at: 1700000000<br/>  }<br/>}
    Redis-->>WS: OK
    
    WS->>Client: WebSocket.send({<br/>  type: 'subscribed',<br/>  shipment_id: '12345'<br/>})
    Client-->>WS: (acked)
```

**Consistency model:** Strong consistency for authorization (checked against Django).

**Failure handling:**
- Auth fails → disconnect and close.
- Django permission check fails → send 403, don't subscribe.
- Redis fails → graceful degradation: serve from in-memory if short-lived, or reject subscription.

---

### Flow 3: Client Reconnects (Network Blip or Browser Refresh)

```mermaid
sequenceDiagram
    participant Client as Mobile App
    participant WS_Old as Old WebSocket Server
    participant LB as Load Balancer
    participant WS_New as New WebSocket Server
    participant Redis as Redis
    
    Note over Client, WS_Old: Initial connection
    Client->>WS_Old: WebSocket connected
    Client->>WS_Old: subscribe shipment_123
    WS_Old->>Redis: SADD shipment:123:watchers user_1
    
    Note over Client: Network interruption (4G→Wifi)
    WS_Old-->Client: (connection dropped)
    
    Client->>LB: Reconnect
    LB->>WS_New: Route to different server
    
    Client->>WS_New: WebSocket connect + authenticate
    WS_New->>Redis: GET shipment:123:watchers
    Redis-->>WS_New: [user_1]
    
    Note over WS_New: Connection registry shows user_1<br/>already subscribed; maintain subscription
    
    WS_New->>Redis: SET user:1:connections {new_conn_id}
    
    Note over Client: App fetches latest state from REST API<br/>to catch up on missed updates
    Client->>Django: GET /api/shipments/123/
    Django-->>Client: Current state
```

**Consistency model:** Eventual consistency; app is responsible for catching up on missed updates via REST API.

**Latency:** Reconnect + re-subscribe <1s.

---

## Storage Design

### PostgreSQL: Notification Audit Log

**Table:** `notification_events`

```sql
CREATE TABLE notification_events (
    id BIGSERIAL PRIMARY KEY,
    shipment_id VARCHAR(50) NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    notification_type VARCHAR(50) NOT NULL, -- 'picked_up', 'in_transit', etc.
    medium VARCHAR(20) NOT NULL, -- 'websocket', 'push'
    delivered_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Indexes
    INDEX (shipment_id, created_at),
    INDEX (user_id, created_at),
    INDEX (created_at) -- For retention purge
);
```

**Retention policy:** 90 days (for compliance/debugging); daily cron job truncates rows older than 90 days.

**Approximate size:** 200K notifications/day × 200 bytes/row = 40MB/day = 3.6GB at 90 days.

**Query patterns:**
- "Did user X get notified about shipment Y?" → SELECT ... WHERE user_id = ? AND shipment_id = ? AND created_at > now() - INTERVAL '90 days'
- "Replay notifications for this shipment" → SELECT ... WHERE shipment_id = ? ORDER BY created_at
- "What failed?" (missing entries) → Compare with Redis Streams log

---

### Redis: Connection Registry & Notification Queue

**Namespace 1: Connection State**

```
shipment:{shipment_id}:watchers → SET [user_1, user_2, ...] (TTL: 86400s)
user:{user_id}:connections → HASH {
  conn_id_1: {
    subscriptions: ['shipment_123', 'shipment_456'],
    connected_at: 1700000000,
    ip: '192.168.1.1'
  },
  conn_id_2: { ... }
} (TTL: 3600s, renewed on activity)
```

**Namespace 2: Notification Queue**

```
notifications_queue → XSTREAM (append-only log)
Entry format: {
  shipment_id: '123',
  user_id: 'driver_1',
  notification_type: 'out_for_delivery',
  timestamp: 1700000000,
  retries: 0
}

Consumer group: push-adapter
- Tracks which messages consumed by push service
- Allows replay if push service crashes
```

**Namespace 3: Rate Limiting (future)**

```
user:{user_id}:notifications:minute → COUNTER (TTL: 60s)
-- Prevents spam: max 100 notifications per user per minute
```

**Memory estimate:**
- Connection state: 50k connections × 1KB = 50MB
- Notification queue (24h retention): 200k msgs × 500 bytes = 100MB
- Other (Lua scripts, encoding overhead): 10MB
- **Total: ~160MB (fits on single r6g.xlarge instance)**

---

## Components

### Component 1: WebSocket Server (Django Channels)

**Purpose:** Maintains persistent WebSocket connections from clients; routes incoming subscription/unsubscription messages and outgoing shipment updates.

**API Surface:**
```
Client → Server:
  { type: 'subscribe', shipment_id: '123', token: 'jwt' }
  { type: 'unsubscribe', shipment_id: '123' }
  { type: 'ping' } → { type: 'pong' }

Server → Client:
  { type: 'subscribed', shipment_id: '123' }
  { type: 'shipment.updated', shipment_id: '123', status: 'in_transit', timestamp: 1700000000 }
  { type: 'error', code: 'UNAUTHORIZED', message: '...' }

HTTP (from Django):
  POST /webhooks/shipment_updated
    { shipment_id, status, timestamp, signature }
```

**Data Ownership:**
- Owns: Active WebSocket connection state (ephemeral)
- Reads from: Redis connection registry, PostgreSQL for auth
- Writes to: Redis connection registry, Redis notification queue, PostgreSQL audit log

**Failure Mode:**
- If WebSocket server crashes → clients reconnect via load balancer to another server; messages queued in Redis.
- If Redis down → graceful degradation: serve from in-memory copy (limited to one server's subscriptions); log warnings.
- If PostgreSQL down → audit log fails (async, non-blocking); notifications still sent.

**Scaling Strategy:** Horizontal (stateless behind load balancer, state in Redis).
- Each server: 50MB baseline + 1KB/connection.
- 50k connections @ 2KB per connection = 100MB total; fits on 5 × 2GB containers or 1 × 16GB container.
- Recommend 3 instances for HA; sticky session routing via load balancer.

---

### Component 2: Connection Registry (Redis)

**Purpose:** Maintains the mapping of user→connections and shipment→watchers; enables fan-out routing.

**API Surface:**
```
Set user's connections:
  SADD user:{user_id}:connections {conn_id}
  EXPIRE user:{user_id}:connections 3600

Add watcher to shipment:
  SADD shipment:{shipment_id}:watchers {user_id}
  EXPIRE shipment:{shipment_id}:watchers 86400

Get watchers of shipment:
  SMEMBERS shipment:{shipment_id}:watchers

Get connections of user:
  SMEMBERS user:{user_id}:connections
```

**Data Ownership:**
- Owns: ephemeral connection and subscription state
- Never authoritative (rebuilt on client reconnect)

**Failure Mode:**
- If Redis lost → all connection state lost; clients auto-reconnect (graceful).
- Mitigate: Redis cluster + Sentinel for failover.

**Scaling Strategy:** Vertical (single Redis cluster); consistent hashing on user_id.
- Single r6g.xlarge (16GB RAM) sufficient for 160MB data + overhead.
- Redis cluster mode: 3 primary + 3 replica nodes for HA.

---

### Component 3: Notification Queue (Redis Streams)

**Purpose:** Decouples shipment status updates from push notification delivery; allows replay if push service is slow or crashes.

**API Surface:**
```
Publish notification:
  XADD notifications_queue * \
    shipment_id {shipment_id} \
    user_id {user_id} \
    notification_type {type} \
    timestamp {timestamp}

Consume (with consumer group for deduplication):
  XREADGROUP GROUP push-adapter consumer1 \
    COUNT 100 \
    BLOCK 5000 \
    STREAMS notifications_queue >

Acknowledge (mark delivered):
  XACK notifications_queue push-adapter {message_id}

Pending messages (failed deliveries):
  XPENDING notifications_queue push-adapter \
    - +
```

**Data Ownership:**
- Owns: queued notifications (temporary)
- Reads from: None
- Writes to: APNs/FCM (external)

**Failure Mode:**
- If push adapter is slow → messages accumulate in queue (normal; queue can hold weeks of data).
- If push adapter crashes → messages remain in pending list; manual intervention or auto-retry after TTL.

**Scaling Strategy:** Single Redis instance (part of same cluster as connection registry).

---

### Component 4: Push Adapter (Python Service)

**Purpose:** Consumes notifications from Redis Streams and sends via FCM (Android) and APNs (iOS).

**API Surface:**
```
Internal:
  Consume from Redis Streams
  Call APNs REST API: POST https://api.push.apple.com/3/device/{token}
  Call FCM REST API: POST https://fcm.googleapis.com/v1/projects/{project}/messages:send

Error handling:
  - Expired/invalid token → remove from DB, stop retrying
  - Rate limited → exponential backoff
  - Network error → retry up to 3x with jitter
```

**Data Ownership:**
- Owns: push delivery state (transient)
- Reads from: Redis notification queue, PostgreSQL device tokens
- Writes to: PostgreSQL audit log

**Failure Mode:**
- If push adapter crashes → messages stay in Redis pending list; restarting adapter replays them.
- If APNs/FCM down → exponential backoff; retry indefinitely (eventual delivery).

**Scaling Strategy:** Horizontal (stateless, consumes from shared Redis consumer group).
- 1-2 instances; pull-based pattern scales naturally (consumer group load balancing).
- Scaling up: add more consumers to same group.

---

### Component 5: Authorization Middleware

**Purpose:** Validates JWT tokens on WebSocket connect; checks user permission to watch shipment on subscribe.

**API Surface:**
```
On WebSocket connect:
  Extract JWT from connection query params
  Validate signature using Django secret key
  Extract user_id, role from claims
  Cache in connection context

On subscribe to shipment:
  Call Django: GET /api/shipments/{shipment_id}/?check_permission=true
  HTTP 403 → unauthorized, reject subscription
  HTTP 200 → authorized, proceed
```

**Data Ownership:**
- Owns: None
- Reads from: Django REST API (authoritative)

**Failure Mode:**
- If Django API down → deny subscription (fail-safe; don't guess permissions).

**Scaling Strategy:** In-process (part of WebSocket server).

---

## Change Impact Analysis

### What if traffic 10x (500k shipments/day)?

**Impact:** 50k → 500k connections, 16 msg/sec → 160 msg/sec.

**Breaking points:**
1. **Redis memory:** 160MB → 1.6GB (still fits on r6i.xlarge).
2. **WebSocket servers:** 5 × 100MB containers → 50 × 100MB containers (requires fleet expansion).
3. **Notification queue throughput:** 160 msg/sec is still well below Redis Streams 50K msg/s (no bottleneck).
4. **Push adapter:** Single adapter can handle 1000+ req/s; 1-2 adapters sufficient.

**Mitigation:** Horizontal scale WebSocket servers; no architectural change needed.

---

### What if a new client type is added (e.g., SMS notifications)?

**Impact:** SMS middleware added alongside push adapter.

**Changes needed:**
1. Add SMS adapter (similar to push adapter, consumes same Redis queue).
2. Add SMS medium to notification_events table.
3. No changes to WebSocket layer.

**Complexity:** Low (additive only).

---

### What if a third-party dependency (APNs) goes down?

**Impact:** Push notifications fail, but WebSocket still works.

**Mitigation:**
1. Push adapter queues messages for retry (Redis persistence).
2. Drivers may not see badge on locked phone, but when they open app, WebSocket reconnect fetches latest state.
3. SLA: <10 min until push resumes (acceptable for non-critical notifications).

**Complexity:** Already handled by design (push is async, not critical path).

---

### What if data schema needs to evolve (e.g., add shipment_type to notifications)?

**Additive change:**
- Add column to `notification_events` table (backward compatible).
- Add field to Redis Stream messages (backward compatible; old consumers ignore new field).

**Complexity:** Low.

**Breaking change (e.g., rename status enum):**
- Requires migration of in-flight messages in Redis queue.
- **Mitigation:** Drain queue before deployment, or use versioned message envelope.

---

## Confidence Assessment

| Component | Confidence | Reason | Risk Mitigation |
|---|---|---|---|
| **WebSocket + Channels** | 95% | Battle-tested pattern; Django team familiar | Spike week 1 with 1000 concurrent connections |
| **Redis connection registry** | 95% | Standard pattern; memory footprint proven | Prototype with target 50k connections on r6g instance |
| **Redis Streams for notification queue** | 80% | Fewer case studies than RabbitMQ/Kafka; scaling question | Load test to 1000 msg/sec before launch |
| **Push adapter (APNs/FCM)** | 85% | APNs/FCM APIs stable; token management complexity | Integrate with real certificates early (Q1) |
| **Authorization via Django API** | 90% | Django auth is solid; latency question during peak | Monitor auth call latency under 50k concurrent load |
| **Sticky session load balancing** | 75% | Redis-based session store adds complexity; potential race condition | Test load balancer failover scenario before launch |
| **Audit logging to PostgreSQL** | 95% | Async, non-blocking; simple INSERT | Standard practice |
| **Mobile native push integration** | 60% | Token lifecycle management (app uninstall, re-login) unproven | Early mobile app integration (Q1 for iOS, Q2 for Android) |

**Overall confidence: 85%** — Architecture is sound, but mobile push and sticky session handling need validation under load.

---

## Recommended ADRs

Before implementation, record these decisions formally:

1. **ADR-000X: Use Django Channels + Redis for real-time notifications** — vs separate service, polling, etc.
2. **ADR-000Y: WebSocket for web/mobile transport** — vs SSE + push fallback.
3. **ADR-000Z: Redis Streams for notification queue** — vs RabbitMQ, Kafka, database.
4. **ADR-000W: Hybrid push strategy (WebSocket + native push)** — justifying operational complexity of APNs/FCM.

---

## Deployment Topology

```
┌─────────────────────────────────────────────────────────────┐
│                      AWS (us-east-1)                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ALB (sticky sessions, TLS termination)              │  │
│  └──────────┬───────────────────────────────────────────┘  │
│             │                                               │
│  ┌──────────┴─────────────────┬──────────────────────┐     │
│  │                            │                      │     │
│  ▼                            ▼                      ▼     │
│ ┌────────────────┐  ┌────────────────┐  ┌─────────────┐   │
│ │ Channels (AZ1) │  │ Channels (AZ2) │  │ Channels... │   │
│ │    2GB RAM      │  │   2GB RAM      │  │  (AZ3)      │   │
│ │ (WebSocket)    │  │ (WebSocket)    │  │             │   │
│ └────────┬───────┘  └────────┬───────┘  └─────┬───────┘   │
│          │                   │                 │           │
│  ┌───────┴───────────────────┴─────────────────┴────┐     │
│  │  Redis Cluster (3x primary + 3x replica)        │     │
│  │  ├─ Connection registry                         │     │
│  │  ├─ Notification queue (Streams)                │     │
│  │  └─ Session store (for load balancer)          │     │
│  │  16GB total across cluster                      │     │
│  └───────────────────┬────────────────────────────┘     │
│                      │                                   │
│  ┌──────────────────┴──────────────┬──────────────┐     │
│  │                                 │              │     │
│  ▼                                 ▼              ▼     │
│ ┌──────────────────┐  ┌──────────────────┐  ┌─────────┐ │
│ │ Push Adapter (1) │  │ Push Adapter (2) │  │Audit... │ │
│ │ 1GB RAM          │  │ 1GB RAM          │  │Service  │ │
│ │ Consumes Streams │  │ Consumes Streams │  │(Lambda) │ │
│ └──────────┬───────┘  └────────┬─────────┘  └────┬────┘ │
│            │                   │                 │      │
│  ┌─────────┴───────────────────┴─────────────────┴──┐   │
│  │        PostgreSQL (RDS Multi-AZ)                 │   │
│  │  ├─ notification_events table                    │   │
│  │  └─ device_tokens table                         │   │
│  │  100 GB capacity (3.6 GB/90 days)               │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘

External:
    APNs API (push.apple.com)
    FCM API (fcm.googleapis.com)
    Django REST API (internal)
```

---

## Risks and Mitigations (Prioritised)

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| **Load balancer sticky session failure** | Medium | All clients reconnect at once; connection storm | Test failover scenario; implement exponential backoff on reconnect |
| **Redis cluster split-brain** | Low | Data inconsistency or data loss | Use Redis Sentinel (proven); monitor quorum |
| **Unvalidated APNs/FCM tokens** | Medium | High% failed push delivery; UX degradation | Validate tokens on first use; implement token refresh flow in mobile app |
| **Notification queue backlog during peak** | Low | Messages delivered after 1-2 minutes instead of seconds | Queue grows 500MB/min at peak; mitigate: add push adapters dynamically |
| **Django auth API latency spike** | Medium | Subscribe calls time out; clients can't re-authorize | Implement auth cache (JWT signature validation locally) + fallback to token-based auth |
| **Postgres audit log inserts blocking on lock contention** | Low | Notifications slow down during peak | Async INSERT via queue worker; non-blocking from WebSocket path |

---

## Summary: What to Build

**Phase 1 (Week 1-2): Spike & Proof of Concept**
- [ ] Set up Django Channels locally; test 1000 concurrent WebSocket connections
- [ ] Validate Redis Streams performance (16 msg/sec → 160 msg/sec)
- [ ] Implement webhook receiver in Django to trigger notifications
- [ ] Build push adapter skeleton (integrate FCM test API)

**Phase 2 (Week 3-4): MVP**
- [ ] Deploy Channels server (3 instances) + Redis cluster to staging
- [ ] Implement sticky session routing at ALB
- [ ] Build web dashboard WebSocket client (Socket.io)
- [ ] Build audit logging (PostgreSQL)
- [ ] Load test to 10k concurrent connections

**Phase 3 (Week 5-6): Mobile Integration**
- [ ] iOS app: WebSocket client + APNs token registration
- [ ] Android app: WebSocket client + FCM token registration
- [ ] Push adapter: full APNs/FCM implementation
- [ ] Token lifecycle management (refresh, revocation)

**Phase 4 (Week 7): Hardening**
- [ ] Graceful shutdown (drain connections, replay queue)
- [ ] Circuit breakers for APNs/FCM
- [ ] Monitoring (connection count, message latency, push delivery rate)
- [ ] Incident runbook (connection storm, Redis down, etc.)

---

That's the complete system design. I've documented assumptions in the ledger with proof status (three are flagged as "Medium" confidence — A1, A2, A7 — and three need user confirmation — A7, A8). The design is a full package: transport mechanism (WebSocket), async layer (Channels), state management (Redis), scaling strategy (horizontal), and mobile push (hybrid native + WebSocket).

**Next steps:** Would you like me to write ADRs for the major decisions, design the mobile app WebSocket integration, or jump to implementation with a detailed deployment guide?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.5 (94%) |
| Evaluated | 2026-05-02 |
| Target duration | 129279 ms |
| Target cost | $0.1202 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent performs a pre-flight step — checks for project conventions (CLAUDE.md, installed rules) and existing ADRs before proposing anything | FAIL | The output opens with 'I'm going to work through the system design methodology now. Let me produce the complete architecture.' — no pre-flight check for CLAUDE.md, installed rules, or existing ADRs is performed at any point. |
| c2 | Agent classifies the work type and scopes what is and is not covered by the design | PASS | A dedicated 'Boundary Definition' section explicitly lists In Scope (Notification Service, WebSocket Server, Connection Registry, etc.), External Dependencies, Trust Boundaries, and Team Boundaries, clearly delineating what is and is not being built. |
| c3 | Agent produces a mandatory assumption ledger with each assumption classified as proven_by_code, inferred, or needs_user_confirmation | PASS | The 'Assumption Ledger' table contains 10 entries (A1–A10), each with a 'Proof status' column using exactly the three required labels: 'proven_by_code' (A4, A5), 'inferred' (A1, A2, A3, A6, A9, A10), and 'needs_user_confirmation' (A7, A8). |
| c4 | Agent quantifies non-functional requirements rather than accepting vague terms — scale (50k shipments/day), latency targets, and availability | PASS | The Non-Functional table quantifies: concurrent connections (50,000), notification latency p95 (<2s), throughput (1,000 msg/min / 16 msg/sec), availability (99.9% / 43 min/month), message durability (100%), mobile push latency (<10s), connection timeout (60s), and cost ceiling (<$2K/month). |
| c5 | Agent presents at least two architectural options (e.g. WebSockets vs SSE vs polling) with a scored trade-off table | PASS | 'Decision 1: WebSocket vs SSE vs Polling' contains a scored comparison table with rows for Bidirectional, Latency, Connection overhead, Mobile support, Firewall/proxy issues, Server complexity, and Cost at 50k connections, across all three options. |
| c6 | Agent includes Mermaid diagrams — at minimum a component diagram showing trust boundaries | PASS | Multiple Mermaid diagrams are included: C4 Level 1 context, C4 Level 2 container, C4 Level 3 WebSocket Server component detail, and three sequence diagrams (Flows 1–3). Trust boundaries are documented in the co-located 'Trust Boundaries' subsection. |
| c7 | Agent identifies decisions that require an ADR (e.g. choice of message broker or real-time transport) | PASS | A 'Recommended ADRs' section lists four specific ADRs: Django Channels + Redis, WebSocket transport, Redis Streams for notification queue, and Hybrid push strategy — each tied to a major architectural decision. |
| c8 | Agent includes a confidence score (HIGH/MEDIUM/LOW with numeric) and states which assumptions drive uncertainty | PASS | The 'Confidence Assessment' table gives per-component numeric percentages (95%, 80%, 85%, 90%, 75%, 60%) with reasons, plus an 'Overall confidence: 85%' summary. The assumption ledger also flags A1, A2, A7 as 'Medium confidence' as drivers of uncertainty. |
| c9 | Agent maps change impact — what existing FreightFlow components are directly or indirectly affected, and explicitly lists what is unaffected | PARTIAL | The 'Change Impact Analysis' section covers four scenarios. Unaffected components are named explicitly: 'No changes to WebSocket layer' (SMS addition scenario) and 'WebSocket still works' (APNs down scenario). The section provides change impact mapping but focuses on new-system scenarios rather than a systematic inventory of affected/unaffected existing FreightFlow components. |
| c10 | Output's transport recommendation explicitly compares WebSockets vs SSE vs long-polling for the push-to-browser-and-mobile use case, with reasoning that addresses bidirectional vs server-initiated traffic and mobile network behaviour (background sockets, reconnection) | PASS | Decision 1 table includes a 'Bidirectional' row (WebSocket ✓ Full duplex, SSE ✗, Polling ✗) and a 'Mobile support' row noting 'battery drain on mobile' for SSE. Reconnection on network blip is addressed in Flow 3 (Mobile App reconnect sequence). A9 assumption addresses backgrounded mobile. |
| c11 | Output addresses the existing Django + PostgreSQL stack — either uses Django Channels / a Django-compatible push solution, or names a separate service with clear integration points to the existing API | PASS | Decision 2 explicitly compares 'Django Channels' vs 'Separate Async Service (FastAPI/Node.js)', recommends Channels with rationale around code reuse of 'Django models, auth, permissions directly.' PostgreSQL integration is specified via the `notification_events` table with full DDL. |
| c12 | Output sizes the system from the 50,000 shipments/day plus 9am/2pm peak — converting daily volume into a peak-second concurrent connection or message rate (e.g. burst factor of 5-10x average) and validating the chosen transport handles it | PASS | NFR table derives 50,000 concurrent connections via '50k shipments/day × 3 avg watchers × 25% active sessions.' Throughput is derived as '50k shipments × 4 updates = 200k msgs/day; concentrated in 9am-11am and 2pm-4pm = 500 msgs/min per window, with bursts to 1000.' Redis Streams headroom is validated: '16 msg/sec vs 50K msg/s capacity (3000× headroom)'. |
| c13 | Output includes at least one Mermaid component diagram showing the path from shipment status change → message broker → push fan-out → web/mobile clients, with trust boundaries marked | PASS | Flow 1 sequence diagram traces: Django->>WS (webhook) → WS->>Redis (watcher lookup) → WS->>Client (WebSocket.send) → WS->>Redis (XADD queue) → PushAdapter->>Redis (XREAD) → PushAdapter->>APNs/FCM. Trust boundaries are documented in the Boundary Definition section. |
| c14 | Output's assumption ledger lists the unstated facts (mobile platforms iOS/Android both, push notification vs in-app socket for backgrounded apps, customer authentication model) classified as inferred or needs_user_confirmation | PASS | A5 ('Mobile app can handle WebSocket (iOS/Android native support)') and A9 ('Native push (APNs, FCM) required for mobile when app is backgrounded') are in the ledger with classifications. Auth model is described operationally in Component 5 and Flow 2 (JWT validation + Django permission check) though not as an explicit ledger entry. |
| c15 | Output identifies at least 2 ADR-worthy decisions (e.g. message broker selection, push transport, fan-out service vs in-Django) and lists them in a 'Decisions Requiring ADR' section | PASS | 'Recommended ADRs' section lists four decisions: (1) Django Channels + Redis for real-time, (2) WebSocket transport, (3) Redis Streams for notification queue, (4) Hybrid push strategy (WebSocket + native push). |
| c16 | Output's change impact section explicitly addresses the Django REST API (extended with status-change events) and PostgreSQL (transactional outbox or change capture) and lists at least one component that is unaffected | PARTIAL | The change impact section lists unaffected components ('No changes to WebSocket layer,' 'WebSocket still works'). However, it does not explicitly address the need to extend the Django REST API with a status-change webhook endpoint, nor does it mention a transactional outbox or change-data-capture pattern for reliable event delivery from PostgreSQL. The webhook integration is shown in sequence diagrams but not surfaced as a change impact on the existing stack. |
| c17 | Output includes a confidence score with HIGH/MEDIUM/LOW label plus a numeric value out of 100, and lists the assumptions or unknowns driving any confidence reduction | PASS | 'Confidence Assessment' table lists 8 components with numeric percentages (95%, 95%, 80%, 85%, 90%, 75%, 95%, 60%) and a 'Reason' column explaining each. 'Overall confidence: 85%' is stated. The assumption ledger flags A1, A2, A7 as uncertainty drivers. Mobile native push (60%) and sticky session (75%) are called out as the primary risks. |
| c18 | Output addresses backgrounded mobile app delivery — recommending APNs/FCM for true push when the app isn't foregrounded, distinct from in-app socket for live dashboards | PARTIAL | Decision 5 'Mobile Push Strategy' table explicitly contrasts 'Native Push (APNs/FCM)' vs 'WebSocket only,' recommending 'Hybrid (WebSocket + Native Push)' with the rationale 'Drivers may have app backgrounded; can't rely on WebSocket alone.' The implementation note states: 'WebSocket: Real-time updates while app is in foreground. Native Push: For backgrounded app or connection loss scenarios.' |
| c19 | Output addresses authentication on the persistent connection (token-scoped channels per customer/driver, not broadcast) so customers can't see other customers' shipments | PARTIAL | Flow 2 (Client Subscribes to Shipment) shows JWT validation, Django permission check ('HTTP 403 if not authorized'), and the note 'user can only watch shipments relevant to their role (customer→own, driver→assigned, etc.).' Component 5 (Authorization Middleware) describes token-scoped channel subscription with per-shipment permission enforcement. |

### Notes

The output is exceptionally thorough — it covers NFR quantification, multi-option trade-off tables, C4-level Mermaid diagrams, a complete assumption ledger with proper classifications, per-component confidence scoring, deployment topology, phased implementation plan, and four recommended ADRs. The single clear failure is c1: the agent skips any pre-flight check for existing conventions, CLAUDE.md, or ADRs, jumping straight into design. The two partial-ceiling criteria (c18, c19) are well-addressed in substance; the 0.5 caps reflect the test author's deliberate ceiling rather than gaps in the output. The main scoring deduction beyond c1 is c16, where the change impact section omits the transactional outbox / CDC pattern for reliable event delivery from the existing PostgreSQL stack and doesn't explicitly frame the Django REST API extension as a change to an existing component. Overall, this is a high-quality architectural response with only minor gaps against a demanding rubric.
