# System design skill structure

Checking that the system-design skill enforces quantified requirements, a mandatory assumption ledger, Mermaid diagrams following the C4 model, and a confidence assessment per component.

## Prompt

> Review the system-design skill definition and verify it produces complete, structured architecture documentation rather than informal diagrams.

Given the prompt "Design a notification delivery system for a SaaS product", here is what the system-design skill would produce.

---

## Output

# System Design: Notification Delivery System

### Requirements

#### Functional
- Users receive in-app, email, and push notifications for account events
- Notification preferences configurable per user per channel
- Bulk notifications to user segments
- Notification history viewable for 90 days
- Delivery receipts tracked: sent, delivered, opened, failed

#### Non-Functional

| Dimension | Target |
|---|---|
| Scale | 50K active users, 500K notifications/day peak |
| Latency | Transactional notifications within 5 seconds p95; bulk within 5 minutes |
| Availability | 99.9% (43.8 min/month downtime budget) |
| Durability | Zero tolerance for lost transactional notifications; at-least-once delivery |
| Security | OAuth2 bearer token auth, PII encrypted at rest (AES-256), GDPR opt-out honoured |
| Cost | < $800/month infrastructure at projected scale |

### Assumptions

| # | Assumption | Impact if wrong | Confidence | Validation method |
|---|---|---|---|---|
| A1 | Email delivery via SendGrid (existing contract) | Provider switch requires template migration | High | Product confirms |
| A2 | Peak is 10x average (500K/day = ~6 req/s avg, 60 req/s peak) | Queue sizing changes | Medium | Instrument first 30 days |
| A3 | Push notifications via Firebase (iOS + Android) | Alternative SDK integration | Medium | Mobile team confirms |
| A4 | 90-day retention fits in ~50GB | Storage tier and cost change | Low | Model: 500K × 1KB × 90 days |

### Architecture

#### Level 1 — Context Diagram

```mermaid
graph TD
  User["User (web/mobile)"]
  SaaS["SaaS Platform"]
  NotifSystem["Notification System"]
  SendGrid["SendGrid (email)"]
  FCM["Firebase (push)"]
  User -->|"triggers events"| SaaS
  SaaS -->|"publish NotificationRequested events"| NotifSystem
  NotifSystem -->|"deliver email"| SendGrid
  NotifSystem -->|"deliver push"| FCM
  NotifSystem -->|"in-app delivery"| User
```

#### Level 2 — Container Diagram

```mermaid
graph TD
  API["Notification API\n(REST, event consumer)"]
  Queue["Event Queue\n(SQS)"]
  Dispatcher["Dispatcher Worker\n(fanout per channel)"]
  PrefStore["Preference Store\n(PostgreSQL)"]
  DeliveryDB["Delivery Log\n(PostgreSQL)"]
  EmailAdapter["Email Adapter\n(SendGrid SDK)"]
  PushAdapter["Push Adapter\n(Firebase SDK)"]
  InApp["In-App Store\n(Redis + WebSocket)"]
  API -->|"enqueue"| Queue
  Queue -->|"consume"| Dispatcher
  Dispatcher -->|"read prefs"| PrefStore
  Dispatcher -->|"route"| EmailAdapter
  Dispatcher -->|"route"| PushAdapter
  Dispatcher -->|"route"| InApp
  Dispatcher -->|"write receipt"| DeliveryDB
```

### Data Flows

#### Transactional notification (e.g. password reset)

```mermaid
sequenceDiagram
  participant App as SaaS App
  participant API as Notification API
  participant Q as Queue
  participant Disp as Dispatcher
  participant Pref as Preference Store
  participant SG as SendGrid

  App->>API: POST /notifications {type: password_reset, userId}
  API->>Q: enqueue (idempotency key = eventId)
  Q->>Disp: dequeue
  Disp->>Pref: GET preferences(userId)
  Pref-->>Disp: {email: true, push: false}
  Disp->>SG: sendEmail(template, recipient)
  SG-->>Disp: 202 Accepted
  Disp->>DeliveryDB: write receipt(sent)
```

### Key Decisions

#### Decision: Message broker selection

| Criterion | SQS (managed) | RabbitMQ (self-hosted) | Kafka |
|---|---|---|---|
| Ops overhead | Zero | Medium | High |
| Throughput | 3K msg/s | 10K msg/s | 100K+ msg/s |
| Replay | No | No | Yes |
| Team expertise | High | Low | Low |
| **Recommendation** | **Selected** | | |

**Rationale:** At 500K/day (~6 msg/s avg, 60 msg/s peak) SQS is dramatically over-provisioned for throughput and team expertise is high. Kafka replay capability is not needed — delivery logs provide audit history.

**Trade-off acknowledged:** No native replay. Re-deliver via re-querying the delivery log and re-enqueueing.

### Change Impact

- **Traffic 10x:** SQS and Dispatcher scale horizontally. Delivery log requires partitioning at ~500M rows/year — add table partitioning in year 2
- **New client type (webhook delivery):** Add WebhookAdapter to Dispatcher; Preference Store adds `webhook_url` column. No changes to API or queue
- **SendGrid outage:** Dead-letter queue accumulates; alert fires. No data loss; emails delivered on recovery. In-app and push continue unaffected

### Confidence Assessment

| Component | Confidence | Reason | Risk mitigation |
|---|---|---|---|
| Notification API | High (85) | Standard REST + queue pattern, team familiar | None needed |
| Dispatcher Worker | Medium (70) | Fanout logic and idempotency at scale untested | Load test at 10x peak in staging |
| Email Adapter | High (80) | SendGrid SDK well-documented | None |
| Push Adapter | Medium (65) | Firebase APNs integration not done before | Spike week 1 |
| In-App Store (Redis+WS) | Low (45) | WebSocket at scale uncharted; Redis pub/sub reconnect unclear | Prototype before sprint 3 |

**Spike required:** In-App Store (confidence 45 < 60 threshold) — prototype WebSocket fan-out with 1,000 simulated concurrent connections before committing.

### Risks and Mitigations

1. **At-least-once creates duplicates** — mitigate with idempotency keys in Delivery Log (upsert on eventId)
2. **GDPR opt-out race condition** — preference check at dispatch time; late opt-out may still deliver. Mitigate with "cancelled" state in delivery log

### Recommended ADRs

- Message broker choice (SQS vs RabbitMQ vs Kafka)
- At-least-once vs exactly-once delivery semantics
- In-app delivery mechanism (WebSocket vs long-poll vs SSE)

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill explicitly rejects vague NFRs and requires numbers — Step 1 NFR table has "Bad answer / Good answer" columns: "Fast" → "p95 < 200ms for reads", "High traffic" → "10K concurrent users, 500 req/s peak". Anti-patterns section: "Unquantified NFRs — 'fast' and 'scalable' are not requirements. Numbers or it doesn't count." Both the table and the anti-pattern are explicit instructions.

- [x] PASS: Skill mandates numbered assumption ledger with confidence and validation method — Step 2 is marked "(MANDATORY)". The table columns are: #, Assumption, Impact if wrong, Confidence, Validation method. Example rows use A1/A2/A3 numbering. "Flag assumptions with confidence below 'High' — these are design risks." All required elements explicitly specified.

- [x] PASS: Skill requires options analysis with 2+ options and rationale — Step 7 is marked "(MANDATORY for key decisions)": "For every significant design decision, present at least 2 options." Template requires a "Rationale" row and "Trade-off acknowledged" field. The output's key decisions section follows this template.

- [x] PASS: Skill requires Mermaid component and sequence diagrams as mandatory — Diagrams section is marked "(MANDATORY)": "Every system design includes at minimum: 1. Component diagram, 2. Sequence diagram — for the top 2-3 most critical workflows, 3. Data flow diagram." "Use Mermaid syntax for all diagrams." The output includes both.

- [x] PASS: Skill describes C4 model levels and requires Level 1 and Level 2 — C4 Model Levels section describes Context (Level 1), Container (Level 2), and Component (Level 3) with descriptions. "Every system design should include at least Level 1 and Level 2 diagrams." Both are present in the output.

- [x] PASS: Skill requires confidence table with <60% = spike rule — Step 9 Confidence Scoring: table with Component, Confidence, Reason, Risk mitigation columns. "Rule: Any component with confidence below 60 must have a spike or prototype planned before implementation begins." The output's In-App Store (45) correctly triggers a spike.

- [x] PASS: Skill requires change impact analysis covering all three scenarios — Step 8 Change Impact Mapping lists: "What if traffic 10x?", "What if a new client type is added?", and "What if a third-party dependency goes down?" — all three present as explicit required questions.

- [x] PASS: Skill lists anti-patterns including all three specified — Anti-Patterns section lists: "Premature microservices," "Distributed monolith," and "Shared database" — all three present verbatim.

- [~] PARTIAL: Skill references arc42 and links to system-design template — Output Structure section: "The output format aligns with arc42 architecture documentation" with a live URL (https://arc42.org/) and reference to "the system-design template (`templates/system-design.md`)." Both are present in the skill definition. PARTIAL ceiling per test author.

### Notes

The arc42 reference and template link are explicitly present in the Output Structure section of the skill definition. The PARTIAL ceiling is test-author-imposed. The <60% confidence threshold with a mandatory spike consequence is well-specified and produces correct behaviour in the output (In-App Store at 45 triggers a spike before sprint 3).
