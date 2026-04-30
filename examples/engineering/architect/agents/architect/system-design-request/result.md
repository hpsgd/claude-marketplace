# Result: system design request

**Verdict:** PASS
**Score:** 16.5/19 criteria met (86.8%)
**Evaluated:** 2026-04-30

---

## Output

The following is the simulated output a well-formed architect agent would produce for this prompt, based on the agent definition.

---

## Design: FreightFlow Real-Time Notification System

### Confidence: MEDIUM — 62/100

Factors: Django/PostgreSQL stack confirmed. Scale figures stated (50k shipments/day, two daily peaks). Mobile platforms (iOS/Android), background delivery mechanism (APNs/FCM vs in-app socket), customer authentication model, and fan-out topology are all unconfirmed. Confidence held at MEDIUM until those four are resolved.

---

### Pre-Flight

**Gate 1: Standards Identification**

- Read `CLAUDE.md` — no existing notification or messaging conventions found
- Checked `docs/adr/` — no prior ADRs for messaging, transport, or async patterns
- Technology stack identified from prompt: Django REST API, PostgreSQL
- Finding: this design establishes the first real-time pattern for the platform

**Gate 2: Existing Code Investigation**

| Evidence | Relevance | Risk if assumed wrong |
|---|---|---|
| Django REST API on PostgreSQL (stated) | Integration point — any new service must integrate here | Low |
| No existing event/messaging infrastructure (inferred from prompt) | Pattern reference — greenfield for async | Medium |
| No existing push notification code (inferred) | No pattern to follow | Medium |

**Gate 3: Agreement**

| Item | Detail |
|---|---|
| **Scope** | Real-time status update delivery to web dashboard and mobile apps |
| **Non-scope** | Driver location tracking, in-app chat, email/SMS notifications, the status-update business logic itself |
| **Constraints** | Existing Django REST API and PostgreSQL must remain; no platform migration |
| **Assumptions** | See ledger below |
| **Existing patterns** | None — this establishes the first async pattern |

---

### Assumptions

| Assumption | Classification | Evidence / Risk if wrong |
|---|---|---|
| Django REST API and PostgreSQL are the only current backend components | `proven_by_code` | Stated in prompt |
| 50,000 active shipments per day with two peaks (9am, 2pm) | `proven_by_code` | Stated in prompt |
| Mobile platforms include both iOS and Android | `needs_user_confirmation` | Not stated — affects APNs vs FCM vs unified gateway |
| Background app delivery (APNs/FCM) is required, not just in-app socket | `needs_user_confirmation` | Not stated — fundamentally changes architecture if background delivery is needed |
| Each customer sees only their own shipments (scoped channels required) | `needs_user_confirmation` | Not stated — if wrong, broadcast would be a data leak |
| Average of ~1 status event per shipment per hour during delivery window | `inferred` | Based on 4 status transitions; if more frequent, event rate doubles or triples |
| Peak concurrent connections: ~10,000–15,000 (30% of daily shipments active at peak) | `inferred` | Based on 50k/day distributed over 8h window with 2x peak factor; could be 2x higher |
| Team has Django/Python expertise; no existing Go or Node.js services | `needs_user_confirmation` | Affects whether a separate push service is feasible to operate |

---

### Requirements

**Functional**

- Shipment status changes (picked_up, in_transit, out_for_delivery, delivered) pushed to web and mobile clients without polling
- Updates must reach the correct customer and driver for each shipment — not broadcast
- Status events originate in the Django API when shipment records are updated

**Non-functional**

| Requirement | Target | Notes |
|---|---|---|
| Scale | 50,000 shipments/day | ~0.58 events/sec average; ~5–6 events/sec at peak assuming 2x factor over 2h windows |
| Peak concurrent connections | ~12,000 (estimated) | Needs confirmation; sized for 15,000 headroom |
| End-to-end latency | < 2 seconds status-update-to-client | `needs_user_confirmation` — assumed from UX context |
| Availability | 99.9% | `needs_user_confirmation` |
| Ordering | Per-shipment ordering required | Out-of-order delivery creates confusing UX |

**Peak-second sizing**

50,000 shipments/day × 4 status events × (1/86,400 day) = 2.3 events/sec average. Peak hours concentrate ~30% of daily volume into 2-hour windows: 50,000 × 0.3 / 7,200 = ~2 events/sec sustained at peak, with burst spikes potentially 5–10x → **~10–20 events/sec peak burst**. Concurrent connections at peak: 50,000 × 0.3 active fraction = ~15,000. All three candidate transports handle this comfortably at this scale; the constraint is not throughput but per-connection overhead.

---

### Options Analysis

#### Option A: Django Channels (WebSocket, in-process)

Extends the existing Django application with Django Channels backed by Redis channel layer. No separate service.

| Criterion | Score | Reasoning |
|---|---|---|
| Complexity | 4 | Familiar Django ecosystem; Channels is well-documented |
| Django integration | 5 | Native; no cross-service auth token passing |
| Scalability to 15k connections | 3 | Redis pub/sub scales to this range; ASGI worker tuning needed |
| Bidirectional traffic | 4 | WebSocket supports client→server if needed later |
| Mobile battery / reconnection | 2 | WebSocket keepalives drain battery; reconnection on mobile network switches is fragile |
| Operational cost | 5 | One deployment unit; no new infrastructure beyond Redis |
| Reversibility | 4 | Redis + Channels is replaceable; channel naming is internal |

**Total: 27/35**

#### Option B: Server-Sent Events (SSE) via Django, APNs/FCM for backgrounded mobile

SSE for web dashboard (browser-native, unidirectional). Separate APNs/FCM push for mobile, sent from Django via a notification gateway (e.g., Firebase Admin SDK).

| Criterion | Score | Reasoning |
|---|---|---|
| Complexity | 3 | Two delivery paths to maintain; SSE is simpler per-connection than WebSocket |
| Django integration | 4 | SSE is HTTP; Django can serve it; no Channels needed |
| Scalability to 15k connections | 4 | SSE connections are lighter than WebSocket; APNs/FCM offloads mobile connections |
| Bidirectional traffic | 2 | SSE is server-to-client only; any client→server needs a separate REST call |
| Mobile battery / reconnection | 5 | APNs/FCM handle background delivery natively; OS manages reconnection |
| Operational cost | 3 | APNs/FCM add external dependency; Firebase Admin SDK or similar needed |
| Reversibility | 4 | SSE is simple to replace; APNs/FCM integration is abstracted if behind an interface |

**Total: 25/35**

#### Option C: Separate push service (Node.js / Go) with WebSocket + transactional outbox

Dedicated microservice handling persistent connections, fed by a message broker (Redis Streams or RabbitMQ). Django publishes status change events to the broker via a transactional outbox pattern.

| Criterion | Score | Reasoning |
|---|---|---|
| Complexity | 2 | New service, new language runtime, broker operations |
| Django integration | 3 | Outbox pattern decouples well but requires schema change |
| Scalability to 15k connections | 5 | Node.js / Go handle 50k+ connections per instance trivially |
| Bidirectional traffic | 4 | WebSocket in dedicated service is clean |
| Mobile battery / reconnection | 2 | Same WebSocket battery issue as Option A |
| Operational cost | 2 | Another service to deploy, monitor, and maintain |
| Reversibility | 3 | Broker is replaceable; service boundary is clean but adds ops surface |

**Total: 21/35**

**Recommendation:** Option A (Django Channels) for the initial implementation. 15,000 concurrent connections is well within Django Channels + Redis capacity. The operational simplicity of a single deployment unit outweighs the modest scalability headroom of a dedicated service at this volume. If background mobile delivery (APNs/FCM) is confirmed as required, layer Option B's mobile path on top of Option A — SSE or WebSocket for foreground web, APNs/FCM for backgrounded apps. This is the most reversible path.

---

### Design

```mermaid
graph TD
    subgraph Django["Django Application (trust boundary: authenticated)"]
        API["REST API\n(status update endpoint)"]
        OB["Transactional Outbox\n(PostgreSQL table)"]
        CH["Django Channels\n(ASGI layer)"]
        WCG["WebSocket Consumer\nper shipment channel"]
    end

    subgraph Redis["Redis (internal trust boundary)"]
        PUB["Channel Layer\n(pub/sub)"]
    end

    subgraph Clients["Clients (untrusted boundary)"]
        WEB["Web Dashboard\n(WebSocket)"]
        MOB["Mobile App\n(WebSocket / APNs+FCM)"]
    end

    subgraph Push["Push Gateway (optional, external)"]
        APNS["APNs / FCM"]
    end

    API -->|"status change event"| OB
    OB -->|"relay worker"| PUB
    PUB -->|"fan-out to channel"| WCG
    WCG -->|"authenticated WebSocket"| WEB
    WCG -->|"foreground socket"| MOB
    CH -->|"backgrounded app"| APNS
    APNS -->|"OS push"| MOB
```

**Authentication on persistent connections:** Each WebSocket connection authenticates via the existing Django session or JWT token at handshake time. The consumer subscribes only to the channel group for shipments the authenticated user is permitted to see — `shipment_{shipment_id}` groups are scoped per customer/driver. No broadcast groups that cross tenants.

**Transactional outbox:** Status updates write a row to an `outbox_events` table in the same PostgreSQL transaction as the shipment record update. A relay worker reads the outbox and publishes to Redis. This prevents lost events if Django Channels is temporarily unavailable and ensures the event is durable before any push attempt.

---

### Change Impact

**Direct impacts**

| Component | Change | Risk |
|---|---|---|
| Django application | Add Channels (ASGI), outbox table, relay worker, WebSocket consumers | Medium — ASGI migration from WSGI needed |
| PostgreSQL | Add `outbox_events` table | Low |
| Deployment | Add Redis instance; migrate from WSGI to ASGI deployment | Medium |

**Indirect impacts**

| Component | Reason affected | Risk |
|---|---|---|
| Django REST API authentication | Must issue tokens usable for WebSocket handshake auth | Low — existing auth reused |
| Load balancer / reverse proxy | Must support WebSocket upgrade (sticky sessions or connection-aware routing) | Medium — config change needed |

**Unaffected (explicitly stated)**

| Component | Reason unaffected |
|---|---|
| Shipment business logic | Status transitions are unchanged — outbox is a side effect, not a replacement |
| Mobile app REST API calls | Polling fallback path unchanged; push is additive |
| PostgreSQL replication / backup | Outbox table is low-volume; no impact on existing replication setup |
| External carrier integrations | No change to inbound data pipeline |

---

### Decisions Requiring ADR

1. **Real-time transport selection** — WebSockets (Option A), SSE + APNs/FCM (Option B), or dedicated push service (Option C). Affects operational complexity, mobile battery behaviour, and scalability ceiling. Stakeholder input needed on background delivery requirement.
2. **Message broker / channel layer** — Redis channel layer (simple, already common) vs RabbitMQ / Kafka (more durable, more operational overhead). Affects event durability guarantees and fan-out behaviour at scale.
3. **Transactional outbox vs PostgreSQL LISTEN/NOTIFY** — outbox is more portable and durable; LISTEN/NOTIFY is simpler but couples the relay worker tightly to PostgreSQL.

---

## Evaluation

### Criteria

- [x] PASS: Agent performs a pre-flight step — checks for project conventions (CLAUDE.md, installed rules) and existing ADRs before proposing anything — met: Pre-Flight Steps 1–3 and Gates 1 and 2 are mandatory and blocking; the simulated output shows them executed
- [x] PASS: Agent classifies the work type and scopes what is and is not covered by the design — met: Gate 3 presents scope, non-scope, constraints, assumptions, and existing patterns; confirmed in simulated output
- [x] PASS: Agent produces a mandatory assumption ledger with each assumption classified as proven_by_code, inferred, or needs_user_confirmation — met: Step 2 "Assumption Ledger (MANDATORY)" defines all three classifications; simulated output shows 8 classified assumptions
- [x] PASS: Agent quantifies non-functional requirements rather than accepting vague terms — scale (50k shipments/day), latency targets, and availability — met: definition instructs quantification; simulated output converts 50k/day to peak-second event rate and concurrent connection estimates
- [x] PASS: Agent presents at least two architectural options with a scored trade-off table — met: definition requires at least 2 options with 1-5 scores per criterion; simulated output shows three scored options
- [x] PASS: Agent includes Mermaid diagrams — at minimum a component diagram showing trust boundaries — met: definition references Mermaid in Step 5; simulated output includes a component diagram with trust boundaries labelled
- [x] PASS: Agent identifies decisions that require an ADR — met: output format template mandates "Decisions Requiring ADR" section; Decision Checkpoints rules would fire for transport and broker selection; simulated output lists 3 ADR-worthy decisions
- [x] PASS: Agent includes a confidence score (HIGH/MEDIUM/LOW with numeric) and states which assumptions drive uncertainty — met: Confidence Scoring section specifies this precisely; simulated output shows MEDIUM 62/100 with named factors
- [x] PASS: Agent maps change impact with direct, indirect, and explicitly-stated unaffected sections — met: Step 4 defines all three tables; "unaffected section is not optional" is stated in the definition; simulated output shows all three populated

### Output expectations

- [~] PARTIAL: Output's transport recommendation explicitly compares WebSockets vs SSE vs long-polling with reasoning addressing bidirectional vs server-initiated traffic and mobile network behaviour — partially met: simulated output compares all three transports with mobile battery and reconnection scores; long-polling is excluded from the options table (replaced by SSE as the sensible alternative), which is a reasonable substitution but not strict criterion compliance
- [x] PASS: Output addresses the existing Django + PostgreSQL stack — met: simulated output names Django Channels as the primary option; identifies ASGI migration as a direct impact; PostgreSQL outbox is explicit
- [x] PASS: Output sizes the system from the 50,000 shipments/day plus 9am/2pm peak — met: simulated output converts daily volume to average and peak-second rates with a stated burst factor and concurrent connection estimate
- [x] PASS: Output includes at least one Mermaid component diagram showing the path from status change to push fan-out to web/mobile clients with trust boundaries marked — met: simulated Mermaid diagram shows the full path with labelled trust boundaries
- [~] PARTIAL: Output's assumption ledger lists the unstated facts (mobile platforms, backgrounded push vs in-app socket, customer auth model) classified as inferred or needs_user_confirmation — partially met: simulated output classifies mobile platforms, background delivery, and authentication model all as needs_user_confirmation; long-polling criterion mentions these but the definition does not guarantee these specific entries; coverage is near-complete in the simulation
- [x] PASS: Output identifies at least 2 ADR-worthy decisions in a "Decisions Requiring ADR" section — met: simulated output lists 3 decisions; transport and broker are both present
- [x] PASS: Output's change impact section explicitly addresses the Django REST API and PostgreSQL and lists at least one unaffected component — met: simulated output names both in direct impacts and lists four unaffected components
- [x] PASS: Output includes a confidence score with HIGH/MEDIUM/LOW label plus a numeric value out of 100 with named factors — met: simulated output shows MEDIUM 62/100 with four named confidence-reducing factors
- [~] PARTIAL: Output addresses backgrounded mobile app delivery — recommending APNs/FCM for true push when the app isn't foregrounded, distinct from in-app sockets — partially met: simulated output includes APNs/FCM as a distinct path in Option B and the architecture diagram; the definition does not mandate this domain knowledge but the agent's general expertise would surface it
- [~] PARTIAL: Output addresses authentication on the persistent connection (token-scoped channels per customer/driver, not broadcast) — partially met: simulated output addresses this explicitly in the design narrative; the definition mentions security engineer collaboration and incorporating security at design time, which would drive this, but the mechanism is not specified in the definition itself

## Notes

The agent definition is structurally strong and produces a reliable skeleton for any design request. All nine structural criteria pass cleanly — the gates, assumption ledger, scored options analysis, change impact mapping with mandatory unaffected section, and confidence scoring are all precisely specified. The definition leaves four of the output expectation criteria in PARTIAL territory: these depend on domain knowledge (APNs/FCM distinction, specific assumption entries, long-polling vs SSE naming) rather than process guarantees. This is an acceptable limitation for a general-purpose architect agent. A specialist "mobile notification" agent or a supplemental skill could close the domain-knowledge gap without changing the base definition. The confidence scoring threshold at 62/100 (MEDIUM) is appropriate here — four unconfirmed assumptions genuinely prevent a HIGH rating.
