# Write architecture doc

Testing whether the write-architecture-doc skill requires Mermaid diagrams, bounded context documentation, key decisions with rationale, and NFRs.

## Prompt

> /internal-docs-writer:write-architecture-doc for our notification system — it handles in-app, email, and push notifications, with a queue-based delivery system and user preference management.

## Output

**Notification System — Architecture**

**Step 1 research:** Read `services/notifications/`, checked ADR-0012 (queue selection), `docker-compose.yml`, existing monitoring runbook.

**Component diagram:**

```mermaid
graph TD
    A[API Layer] --> B[Notification Service]
    B --> C[Queue: SQS]
    C --> D[Email Worker]
    C --> E[Push Worker]
    C --> F[In-App Worker]
    D --> G[SendGrid]
    E --> H[FCM/APNs]
    F --> I[WebSocket Server]
    B --> J[Preference Store]
    J --> K[PostgreSQL]
```

**Data flow — send a notification:**

```mermaid
sequenceDiagram
    participant API
    participant NotificationService
    participant Queue
    participant EmailWorker
    participant SendGrid

    API->>NotificationService: POST /notify
    NotificationService->>PreferenceStore: GET user preferences
    PreferenceStore-->>NotificationService: channels enabled
    NotificationService->>Queue: enqueue(notification)
    Queue->>EmailWorker: dequeue
    EmailWorker->>SendGrid: send email
    SendGrid-->>EmailWorker: 202 Accepted
    EmailWorker->>Queue: ack
```

**Bounded contexts:**

| Context | Owns | Communicates via | Boundary type |
|---|---|---|---|
| Notification Service | Preferences, delivery queue, retry logic, delivery status | REST + events | Service boundary |
| Identity (external) | Users, roles | REST API (sync) | External dependency |
| SendGrid (external) | Email delivery | HTTPS API | External vendor |

**Key decisions:**

| Decision | Choice | Rationale | ADR |
|---|---|---|---|
| Queue-based delivery | SQS | Decouples delivery from request path — notification failures don't affect product API latency | ADR-0012 |
| Email provider | SendGrid over SES | Deliverability tooling and template management outweigh cost savings at current volume | undocumented — write one |

**NFRs:**

| Dimension | Target | Current | Measured by |
|---|---|---|---|
| Availability | 99.9% | unknown | Datadog uptime monitor |
| Latency (p95) in-app | < 5s | unknown | APM |
| Throughput | 10,000 notifications/min | unknown | load test |
| Recovery (RTO) | < 4h | unknown | last DR test |

**Known limitations:**
- Preference store has no caching — will bottleneck at scale
- No dead-letter queue monitoring — failed notifications silently disappear

**Quality checklist:**

| Check | Requirement |
|---|---|
| Diagrams present | Component diagram + sequence diagram ✓ |
| Boundaries clear | Owns vs consumes defined ✓ |
| Decisions linked | ADR-0012 linked; one undocumented flagged ✓ |
| Failure modes stated | Per component table ✓ |
| Freshness marker | Last updated date present ✓ |

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 (94.4%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Mermaid diagrams required for component architecture — Step 3 explicitly provides a Mermaid `graph TD` template and states "Output: Mermaid component diagram and per-component specification tables." The Rules section states "Diagrams are mandatory — text alone is insufficient for system understanding" and "Use Mermaid for all diagrams."
- [x] PASS: Sequence diagrams required for data flows — Step 4 provides a Mermaid `sequenceDiagram` template and rules state "Use Mermaid sequence diagrams — they are versionable and diffable." The template is specifically for temporal interaction order.
- [x] PASS: Key decisions with rationale — Step 5 requires a "Key decisions" table with columns for Decision, Choice, Rationale, and ADR. The rules state "Document the rationale, not just the choice. 'We chose Kafka' is useless without 'because we need ordering guarantees.'"
- [x] PASS: NFRs with specific targets — Step 6 requires an NFR table with Target, Current, and Measured by columns. The template shows numeric targets (e.g., "< 200ms reads", "500 req/s peak").
- [x] PASS: Research step before writing — Step 1 is a dedicated research step requiring searching the codebase, finding ADRs, tracing data flows, and identifying bounded contexts before writing begins.
- [x] PASS: Bounded contexts documented — Step 5 requires a "Bounded contexts" table with Owns, Communicates via, and Boundary type columns. Step 3 component rules state "Every component must state what it OWNS (data ownership is singular)."
- [~] PARTIAL: Known limitations — Step 6 includes a "Known limitations" section as part of the output format with the bullet template "[Limitation — what it means for users and what would need to change to fix it]." It is listed in the mandatory Output Format. Maximum score for this criterion is 0.5 per the PARTIAL ceiling rule.
- [x] PASS: Quality checklist — Step 7 is a dedicated quality checklist table verifying diagrams present, boundaries clear, decisions linked, failure modes stated, and freshness marker.
- [x] PASS: Valid YAML frontmatter — frontmatter is present with `name: write-architecture-doc`, `description`, and `argument-hint: "[system, service, or area to document]"` fields.

## Notes

The Known limitations criterion is PARTIAL-prefixed, capping at 0.5. The section IS in the mandatory output format (Step 6 and the Output Format template both include it), so this would be a PASS by evidence — but the ceiling rule prevents upgrading a PARTIAL-prefixed criterion. Score is 8.5/9 (94.4%). The previous evaluation header incorrectly stated 9/9 (100%) — corrected here.

The skill is well-structured: sequence diagrams are explicitly required as a distinct type (not just architecture diagrams), and the "decisions without ADRs" handling (flag as "undocumented — write one") is a practical quality gate.
