---
name: event-tracking-plan
description: Define an event tracking plan — what events to capture, with what properties, for what purpose.
argument-hint: "[feature, flow, or product area to track]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Define an event tracking plan for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Purpose Definition

Before defining any events, answer these questions:

1. **What business questions must this tracking answer?**
   - List every question explicitly. If you can't articulate the question, you don't need the event
   - BAD: "Track user engagement"
   - GOOD: "What percentage of users who view a report also export it? Does this differ by plan tier?"

2. **Who will consume this data?**
   - Product team (feature usage, funnel analysis)
   - Marketing (attribution, campaign effectiveness)
   - Engineering (performance, error rates)
   - Finance (billing events, revenue attribution)
   - Each consumer may need different properties on the same event

3. **What decisions will this data inform?**
   - Feature investment (should we build more of X?)
   - UX changes (where do users drop off?)
   - Pricing (which features drive upgrades?)
   - If no decision is tied to the data, don't track it

### Step 2: Event Naming Convention

All events follow these naming rules:

| Rule | Convention | Example |
|---|---|---|
| Format | `snake_case` | `report_exported` |
| Structure | `object_action` (noun_verb past tense) | `search_performed`, `report_viewed`, `subscription_upgraded` |
| Consistency | Same object name everywhere | `report_viewed`, `report_exported`, `report_shared` — not `report_viewed`, `doc_exported` |
| Specificity | Specific enough to be unambiguous | `payment_failed` not `error_occurred` |
| No redundancy | No `event_` prefix | `report_viewed` not `event_report_viewed` |

**Naming checklist:**
- Is the object (noun) a domain concept the business understands?
- Is the action (verb) in past tense? (something happened, not something is happening)
- Would a non-technical person understand what this event means?
- Is this name unique across the entire tracking plan?

### Step 3: Event Design

For EACH event, define:

```markdown
### `report_exported`

**Trigger:** User clicks the "Export" button and the export completes successfully.
**NOT triggered by:** Auto-scheduled exports, API-initiated exports (separate event: `report_export_api_called`).

**Purpose:** Measures manual report export usage to inform whether the export feature is valuable enough to invest in further formats.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Unique identifier of the exported report | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Type of report | `"analytics"`, `"financial"`, `"audit"` |
| `export_format` | string (enum) | Yes | Format selected by user | `"pdf"`, `"csv"`, `"xlsx"` |
| `row_count` | integer | Yes | Number of rows in the exported data | `1523` |
| `duration_ms` | integer | Yes | Time to generate the export in milliseconds | `2450` |
| `plan_tier` | string (enum) | Yes | User's subscription tier at time of export | `"free"`, `"pro"`, `"enterprise"` |
| `is_filtered` | boolean | Yes | Whether the user applied filters before exporting | `true` |

**Deduplication:** Same `report_id` + `export_format` within 5 seconds = duplicate (user double-clicked). Keep the first occurrence.

**Volume estimate:** ~500 events/day based on current user base. Expected to grow linearly with user count.
```

### Step 4: Standard Properties (on EVERY event)

These properties are automatically attached to every event by the tracking SDK. Do not include them in individual event definitions:

| Property | Type | Source | Description |
|---|---|---|---|
| `event_id` | string (UUID) | SDK-generated | Unique identifier for this event occurrence |
| `event_name` | string | SDK | The event name (e.g., `report_exported`) |
| `timestamp` | string (ISO 8601) | SDK | When the event occurred, with timezone |
| `user_id` | string (UUID) | Auth context | Authenticated user identifier (null for anonymous) |
| `anonymous_id` | string (UUID) | Cookie/device | Device identifier for pre-auth tracking |
| `session_id` | string (UUID) | Session context | Current session identifier |
| `page_url` | string | SDK | Current page URL (route pattern, not full URL) |
| `user_agent` | string | SDK | Browser/client user agent string |
| `app_version` | string | Build | Application version or commit SHA |

**Rules:**
- `user_id` and `anonymous_id` enable identity stitching (pre-login to post-login)
- `page_url` uses route patterns (`/reports/{id}`) not full URLs (avoid high cardinality)
- `session_id` resets after 30 minutes of inactivity (define session boundary)
- `app_version` enables correlation with deployments

### Step 5: Property Design Rules (MANDATORY)

| Rule | Rationale | Example |
|---|---|---|
| Consistent naming across events | Enables cross-event analysis without mapping | `user_id` everywhere, never `userId` or `uid` |
| No high-cardinality strings | Explodes storage, breaks GROUP BY | Route patterns not full URLs, category not free text |
| Enums over free text | Enables reliable aggregation | `export_format: "pdf"` not `format: "PDF file"` |
| Numeric values have units | Prevents misinterpretation | `duration_ms` not `duration`, `size_bytes` not `size` |
| Boolean properties are positive | Avoids double negatives in queries | `is_filtered: true` not `is_unfiltered: false` |
| IDs are UUIDs | Consistent format, no sequential enumeration | `report_id: "550e8400-..."` |
| No PII in event properties | Privacy compliance, data retention | No email, name, phone, or IP address in event properties |
| No derived/computed properties | Compute in the warehouse, not at capture | Don't send `average_session_time` — compute from raw events |

### Step 6: Deduplication Strategy

For each event, define what constitutes a "unique" occurrence:

| Strategy | When to use | Implementation |
|---|---|---|
| **Idempotency key** | API-driven events | Client generates a UUID, server deduplicates |
| **Time window** | UI-driven events (double-click) | Same user + same action + same target within N seconds |
| **State change** | Status transition events | Only fire when state actually changes (not on every render) |
| **Natural key** | Events tied to a unique action | `report_id` + `export_format` is unique per export |

**Rules:**
- Every event has a documented deduplication strategy
- Time windows are short (5-10 seconds) for UI events
- State change deduplication prevents re-firing on page re-renders
- The deduplication key is documented in the event definition

### Step 7: Privacy and Compliance

| Requirement | Implementation |
|---|---|
| No PII in events | User identified by `user_id`, not email/name/phone |
| Consent tracking | Events only fire after consent is granted (respect cookie preferences) |
| Data retention | Define retention period per event (e.g., 90 days raw, 2 years aggregated) |
| Right to erasure | `user_id` is the deletion key — all events for a user can be purged |
| Data classification | Tag each event as `public`, `internal`, `confidential` |
| Geo restrictions | Note if events should not be sent to specific regions |

### Step 8: Volume Estimation

For each event, estimate:

| Metric | Estimation method |
|---|---|
| Events per day | [users] x [frequency per user] x [% of users who trigger this] |
| Storage per event | [avg properties size in bytes] x [events per day] |
| Monthly volume | [events per day] x 30 |
| Growth rate | [user growth rate] or [feature adoption curve] |

**Why this matters:**
- Events with >1M/day may need sampling or batching
- Storage costs compound — 1KB per event x 1M events/day = 30GB/month
- High-volume events need efficient schemas (short property names, compact types)
- Alerting thresholds depend on expected volume

### Step 9: Instrumentation Notes

For each event, specify where in the code to add tracking:

```markdown
#### Instrumentation: `report_exported`

- **Location:** `src/features/reports/export-button.tsx:handleExport()`
- **Trigger point:** After the export API call succeeds (not on click — on success)
- **Error handling:** If tracking fails, do NOT block the user action. Log the failure silently
- **Testing:** Add to the analytics test suite — verify event fires with correct properties
```

## Anti-Patterns (NEVER do these)

- **Tracking without a question** — every event must answer a specific business question. "Just in case" tracking creates noise
- **Over-tracking** — each event has a maintenance cost (schema, validation, storage, queries). Track what you need, not what you can
- **Inconsistent naming** — `reportExported` in JS, `report_exported` in the warehouse, `Report Exported` in the dashboard. Pick one convention
- **PII in events** — emails, names, phone numbers in event properties are a compliance risk
- **Tracking implementation details** — `api_response_received` is infrastructure. `report_exported` is product behaviour
- **High-cardinality properties** — full URLs, user-generated text, raw SQL queries in event properties
- **No deduplication** — double-click, re-render, retry all fire duplicate events. Define deduplication upfront
- **Blocking on analytics** — if the tracking SDK fails, the user's action must still succeed

## Output Format

```markdown
# Event Tracking Plan: [feature/flow name]

## Business Questions
1. [Question this tracking plan answers]
2. [Second question]
3. [Third question]

## Event Catalogue

### `event_name_1`
[Full event definition per Step 3 template]

### `event_name_2`
[Full event definition]

## Standard Properties
[Table of auto-attached properties]

## Volume Estimates
| Event | Daily volume | Monthly storage | Growth rate |
|---|---|---|---|

## Privacy
- **PII:** None in event properties
- **Consent:** Required before tracking
- **Retention:** [period]
- **Deletion key:** `user_id`

## Instrumentation Checklist
| Event | File | Function | Status |
|---|---|---|---|
| `event_name_1` | `src/...` | `handleX()` | TODO |
| `event_name_2` | `src/...` | `handleY()` | TODO |

## Funnel Definition (if applicable)
[Ordered list of events that form a conversion funnel]
1. `page_viewed` (entry)
2. `report_created` (activation)
3. `report_exported` (value)
4. `subscription_upgraded` (revenue)
```
