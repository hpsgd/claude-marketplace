# Event Tracking Plan

Scenario: Developer invokes the event-tracking-plan skill to define tracking for the report creation and export user flow — covering report creation, viewing, sharing, and exporting.

## Prompt

> Define an event tracking plan for the report creation and export flow. We want to understand: how many users who create a report actually export it? What export format is most popular? How long do users spend viewing a report before exporting? Do power users (>5 reports) export more often than casual users? The flow is: user creates a report → views it → optionally shares it → optionally exports it.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Plan written to `docs/data/event-tracking-plan--report-export.md`. Here's a summary:

**4 events defined:**

| Event | Purpose |
|---|---|
| `report_created` | Funnel entry; power-user segmentation (count per user) |
| `report_viewed` | Timestamp anchor for time-to-export (Q3) |
| `report_shared` | Optional funnel step |
| `report_exported` | Primary value event — answers Q1, Q2, Q3, Q4 |

**How each question is answered:**
- **Q1 (conversion rate):** `DISTINCT user_id` in `report_exported` ÷ `report_created` — no extra property needed.
- **Q2 (format popularity):** `GROUP BY export_format` on `report_exported`.
- **Q3 (time-to-export):** Join `report_viewed` (first per session) with `report_exported` on `report_id` + `session_id` — warehouse computes the diff; no client-side timing sent.
- **Q4 (power users):** Segment users by `COUNT(report_created) > 5` in the warehouse, then compare export rates.

Ready-to-run SQL for all four questions is included in the plan.

### Artifacts written

#### `work/docs/data/event-tracking-plan--report-export.md`

```
# Event Tracking Plan: Report Creation and Export Flow

## Business Questions

1. **Conversion rate:** What percentage of users who create a report also export it?
2. **Format popularity:** Which export format (PDF, CSV, XLSX, etc.) is used most often?
3. **Time-to-export:** How long do users spend viewing a report before they export it?
4. **Power user behaviour:** Do users with more than 5 reports export more often than users with 5 or fewer?

## Consumer Map

| Consumer | Primary events | Purpose |
|---|---|---|
| Product | All four events | Funnel drop-off, feature investment |
| Engineering | `report_exported` (duration_ms) | Export pipeline performance |

---

## Event Catalogue

### `report_created`

**Trigger:** The report is successfully persisted server-side and the user is redirected to the report view. Not triggered on draft saves or failed submissions.

**Purpose:** Defines the funnel entry point. Combined with `report_exported`, answers Q1 and Q4 (power user segmentation is computed from the count of this event per user in the warehouse).

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Unique identifier of the newly created report | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Category of report | `"analytics"`, `"financial"`, `"operational"` |
| `template_id` | string (UUID/null) | Yes | Template used, or null if created from scratch | `"tmpl_abc123"`, `null` |
| `data_source_count` | integer | Yes | Number of data sources connected to the report | `3` |
| `filter_count` | integer | Yes | Number of filters applied at creation time | `2` |

**Deduplication:** `report_id` is a natural key — one creation event per report. Discard any duplicate within 10 seconds of the first.

**Volume estimate:** ~300 events/day (1 000 DAU × 30% create a report). ~30 KB/day.

---

### `report_viewed`

**Trigger:** The report view page reaches a ready state (data loaded, not just navigation start). Fires once per page load — not on tab focus or scroll.

**Purpose:** Provides the timestamp anchor for Q3. The warehouse computes time-to-export by joining the earliest `report_viewed` for a given `report_id` + `session_id` with the corresponding `report_exported`.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Identifier of the report being viewed | `"550e8400-..."` |
| `report_type` | string (enum) | Yes | Category of report | `"analytics"` |
| `view_source` | string (enum) | Yes | How the user arrived at this report | `"report_list"`, `"direct_link"`, `"share_link"`, `"notification"` |
| `is_own_report` | boolean | Yes | Whether the viewing user created this report | `true` |

**Deduplication:** Same `user_id` + `report_id` + `session_id` within 5 seconds = duplicate (page re-render). Keep the first occurrence.

**Volume estimate:** ~700 events/day (300 creators × avg 2 views, plus recipients viewing shared reports). ~70 KB/day.

---

### `report_shared`

**Trigger:** User completes a share action: copies a link, sends an email invite, or adds a collaborator. Not triggered when the share modal opens.

**Purpose:** Optional step in the funnel. Allows future analysis of whether sharing correlates with export behaviour.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Identifier of the shared report | `"550e8400-..."` |
| `report_type` | string (enum) | Yes | Category of report | `"analytics"` |
| `share_method` | string (enum) | Yes | How the report was shared | `"copy_link"`, `"email_invite"`, `"collaborator_added"` |
| `recipient_count` | integer | Yes | Number of recipients (1 for link copy) | `3` |

**Deduplication:** Same `user_id` + `report_id` + `share_method` within 5 seconds = duplicate (button mash). Keep the first occurrence.

**Volume estimate:** ~75 events/day (~25% of creators share). ~7 KB/day.

---

### `report_exported`

**Trigger:** The export file is successfully generated and the download begins. Not triggered when the export modal opens, or if generation fails (use `report_export_failed` for error tracking, defined separately when needed).

**Purpose:** The primary value event. Answers Q1 (conversion), Q2 (format popularity), and Q3 (time-to-export, computed in the warehouse from `report_viewed` timestamp). Q4 (power user segmentation) is a warehouse computation joining this event against the per-user count of `report_created`.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Identifier of the exported report | `"550e8400-..."` |
| `report_type` | string (enum) | Yes | Category of report | `"analytics"` |
| `export_format` | string (enum) | Yes | Format selected by the user | `"pdf"`, `"csv"`, `"xlsx"`, `"json"` |
| `row_count` | integer | Yes | Number of data rows in the export | `1 523` |
| `duration_ms` | integer | Yes | Time from export request to download start, in milliseconds | `2 450` |
| `is_filtered` | boolean | Yes | Whether the user applied filters before exporting | `true` |
| `plan_tier` | string (enum) | Yes | User's subscription tier at export time | `"free"`, `"pro"`, `"enterprise"` |

**Deduplication:** Same `user_id` + `report_id` + `export_format` within 10 seconds = duplicate (double-click). Keep the first occurrence.

**Volume estimate:** ~120 events/day (~40% of viewers export). ~15 KB/day.

---

## Standard Properties (auto-attached to every event)

These are set by the tracking SDK and do not appear in individual event definitions above.

| Property | Type | Source | Description |
|---|---|---|---|
| `event_id` | string (UUID) | SDK | Unique identifier for this event occurrence |
| `event_name` | string | SDK | Event name (e.g. `report_exported`) |
| `timestamp` | string (ISO 8601) | SDK | When the event fired, with timezone |
| `user_id` | string (UUID) | Auth context | Authenticated user — null for anonymous |
| `anonymous_id` | string (UUID) | Cookie | Device-level identifier for pre-auth stitching |
| `session_id` | string (UUID) | Session context | Resets after 30 min of inactivity |
| `page_url` | string | SDK | Route pattern, not full URL — e.g. `/reports/{id}` |
| `user_agent` | string | SDK | Browser/client user agent |
| `app_version` | string | Build | Commit SHA or release tag |

---

## Volume Estimates

| Event | Daily volume | Avg event size | Monthly storage |
|---|---|---|---|
| `report_created` | ~300 | ~100 B | ~900 KB |
| `report_viewed` | ~700 | ~100 B | ~2.1 MB |
| `report_shared` | ~75 | ~100 B | ~225 KB |
| `report_exported` | ~120 | ~125 B | ~450 KB |

Total: well under 5 MB/month at current scale. No sampling required.

---

## Privacy

- **PII:** None. Users are identified by `user_id` (UUID) only — no email, name, or IP in any event property.
- **Consent:** Events fire only after the user has granted analytics consent.
- **Retention:** 90 days raw events; 2 years aggregated (daily rollups).
- **Deletion key:** `user_id` — all events for a user can be purged on erasure request.
- **Classification:** `internal` — not shared externally, not subject to geo restriction.

---

## Warehouse Queries for Each Business Question

### Q1: Conversion rate (created → exported)
```sql
SELECT
  COUNT(DISTINCT e.user_id) AS exporters,
  COUNT(DISTINCT c.user_id) AS creators,
  ROUND(100.0 * COUNT(DISTINCT e.user_id) / COUNT(DISTINCT c.user_id), 1) AS export_rate_pct
FROM report_created c
LEFT JOIN report_exported e USING (user_id)
WHERE c.timestamp >= CURRENT_DATE - INTERVAL '30 days';
```

### Q2: Format popularity
```sql
SELECT
  export_format,
  COUNT(*) AS export_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS share_pct
FROM report_exported
WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1
ORDER BY 2 DESC;
```

### Q3: Time-to-export (first view → export, same session)
```sql
WITH first_views AS (
  SELECT report_id, session_id, MIN(timestamp) AS first_viewed_at
  FROM report_viewed
  GROUP BY 1, 2
)
SELECT
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (e.timestamp - v.first_viewed_at))) AS median_seconds,
  PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (e.timestamp - v.first_viewed_at))) AS p90_seconds
FROM report_exported e
JOIN first_views v ON v.report_id = e.report_id AND v.session_id = e.session_id
WHERE e.timestamp >= CURRENT_DATE - INTERVAL '30 days';
```

### Q4: Power users vs casual users
```sql
WITH user_report_counts AS (
  SELECT user_id, COUNT(*) AS report_count
  FROM report_created
  GROUP BY 1
),
segments AS (
  SELECT user_id,
    CASE WHEN report_count > 5 THEN 'power' ELSE 'casual' END AS segment
  FROM user_report_counts
)
SELECT
  s.segment,
  COUNT(DISTINCT c.user_id) AS creators,
  COUNT(DISTINCT e.user_id) AS exporters,
  ROUND(100.0 * COUNT(DISTINCT e.user_id) / COUNT(DISTINCT c.user_id), 1) AS export_rate_pct
FROM report_created c
JOIN segments s USING (user_id)
LEFT JOIN report_exported e ON e.user_id = c.user_id
GROUP BY 1;
```

---

## Funnel Definition

| Step | Event | Conversion measured |
|---|---|---|
| 1 — Creation | `report_created` | Entry |
| 2 — Engagement | `report_viewed` | % of creators who view their report |
| 3 — Share (optional) | `report_shared` | % of viewers who share |
| 4 — Export (value) | `report_exported` | % of creators who export (Q1) |

---

## Instrumentation Checklist

| Event | File | Function | Trigger point | Status |
|---|---|---|---|---|
| `report_created` | `src/features/reports/create-report.ts` | `handleCreateSuccess()` | After server confirms creation | TODO |
| `report_viewed` | `src/features/reports/report-view.tsx` | `onReportReady()` | After report data loads | TODO |
| `report_shared` | `src/features/reports/share-modal.tsx` | `handleShareConfirm()` | After share API call succeeds | TODO |
| `report_exported` | `src/features/reports/export-button.tsx` | `handleExportSuccess()` | After download begins | TODO |

**Implementation rules for all events:**
- Fire on success, not on user intent (click/open). A failed action that fires a success event is worse than a missed event.
- If the tracking call fails, do not block the user action. Fail silently and log to the error monitoring service.
- Add each event to the analytics test suite with property assertions before shipping.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.0/18.0 (100%) |
| Evaluated | 2026-04-30 |
| Target duration | 99076 ms |
| Target cost | $0.1817 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines the business questions this tracking plan must answer BEFORE defining any events | PASS | The document opens with a '## Business Questions' section (Q1–Q4) before the '## Event Catalogue' section begins. |
| c2 | All event names use `snake_case` `object_action` past-tense format (e.g. `report_created`, `report_exported`) | PASS | All four events: `report_created`, `report_viewed`, `report_shared`, `report_exported` — all snake_case, object_action, past-tense. |
| c3 | Each event definition includes: trigger, NOT triggered by (exclusions), purpose, properties table with types and required flag, deduplication strategy, and volume estimate | PASS | All four events include: **Trigger** sentence, explicit exclusion ('Not triggered on...'), **Purpose** paragraph, properties table with Type/Required/Description columns, a **Deduplication** paragraph, and a **Volume estimate** line. E.g. `report_created`: 'Not triggered on draft saves or failed submissions'; deduplication: '`report_id` is a natural key — one creation event per report. Discard any duplicate within 10 seconds'; volume: '~300 events/day'. |
| c4 | No PII appears in event properties — users identified by `user_id` UUID, not email or name | PASS | Standard properties table shows `user_id` as 'string (UUID)' and `anonymous_id` as 'string (UUID)'. No event-level properties contain email, name, or IP. Privacy section confirms: 'Users are identified by `user_id` (UUID) only — no email, name, or IP in any event property.' |
| c5 | No high-cardinality properties — report title is excluded or replaced with a category/type; full URLs replaced with route patterns | PASS | No report title field appears in any event. `report_type` is typed as 'string (enum)' with values like `analytics`, `financial`, `operational`. Standard properties table shows `page_url` as 'Route pattern, not full URL — e.g. `/reports/{id}`'. |
| c6 | Standard properties (event_id, timestamp, user_id, session_id, page_url, app_version) are listed as auto-attached — not repeated in individual event definitions | PASS | '## Standard Properties (auto-attached to every event)' section lists event_id, event_name, timestamp, user_id, anonymous_id, session_id, page_url, user_agent, app_version with source 'SDK'/'Auth context'/'Build'. None of these appear in individual event property tables. |
| c7 | Every event has a documented deduplication strategy | PASS | All four events have explicit **Deduplication** paragraphs: `report_created` — natural key `report_id`, discard within 10s; `report_viewed` — same user+report+session within 5s; `report_shared` — same user+report+method within 5s; `report_exported` — same user+report+format within 10s. |
| c8 | Skill defines a funnel from the four events (report_created → report_viewed → report_exported) and notes conversion rate tracking | PARTIAL | '## Funnel Definition' table lists all four steps (Creation → Engagement → Share optional → Export) with a 'Conversion measured' column. Q1 SQL computes export_rate_pct as DISTINCT exporters / DISTINCT creators. Ceiling is PARTIAL. |
| c9 | Output includes volume estimates per event and a privacy section with retention period and deletion key | PASS | '## Volume Estimates' table gives daily volume, avg event size, and monthly storage per event. '## Privacy' section states: 'Retention: 90 days raw events; 2 years aggregated (daily rollups)' and 'Deletion key: `user_id` — all events for a user can be purged on erasure request.' |
| c10 | Output's business questions section reproduces all four questions from the prompt — create-to-export conversion, popular export format, view-time-before-export, power-user vs casual export rate — before any event definitions | PASS | Business Questions section (before Event Catalogue) lists Q1 'What percentage of users who create a report also export it?', Q2 'Which export format... used most often?', Q3 'How long do users spend viewing a report before they export it?', Q4 'Do users with more than 5 reports export more often than users with 5 or fewer?' |
| c11 | Output defines at least four events covering the flow: `report_created`, `report_viewed`, `report_shared`, `report_exported` — all in `object_action` past-tense snake_case | PASS | Event Catalogue contains exactly these four events as H3 headings: `report_created`, `report_viewed`, `report_shared`, `report_exported` — all snake_case, object_action, past-tense. |
| c12 | Output's `report_exported` event includes a `format` property (with enum values like pdf/csv/xlsx) so the popular-format question can be answered | PASS | `report_exported` properties table includes `export_format` typed 'string (enum)' with example values `"pdf"`, `"csv"`, `"xlsx"`, `"json"`. |
| c13 | Output's `report_viewed` event captures view duration (e.g. `duration_seconds` on view-end, or paired view-start/view-end events) so the time-before-export question is answerable | PASS | `report_viewed` fires on page ready (view-start timestamp) and `report_exported` fires on download-start (end timestamp). Q3 SQL joins 'MIN(timestamp)' from `report_viewed` with `report_exported` on report_id+session_id to compute PERCENTILE_CONT — a valid paired-event approach. The plan explicitly states 'The warehouse computes time-to-export by joining the earliest `report_viewed` for a given `report_id` + `session_id` with the corresponding `report_exported`'. |
| c14 | Output's events identify users via `user_id` UUID and never include email, full name, or other PII in properties | PASS | No event property table contains email, name, or IP fields. Standard properties table identifies users via `user_id` 'string (UUID)'. Privacy section confirms no PII in event properties. |
| c15 | Output excludes high-cardinality fields like full report titles or user-typed content; if title information is needed, it's a category or template type, not free text | PASS | No `report_title` or free-text field exists in any event. `report_type` is 'string (enum)'; `template_id` is a UUID (not a name); `view_source`, `share_method`, `export_format` are all enums. No user-typed content anywhere. |
| c16 | Output specifies a deduplication strategy per event (e.g. `event_id` UUID generated client-side and deduplicated server-side) so retried network calls don't double-count | PASS | Each event has a **Deduplication** paragraph with specific key combinations and time windows: `report_created` uses natural key `report_id`; `report_viewed` uses user_id+report_id+session_id within 5s; `report_shared` uses user_id+report_id+share_method within 5s; `report_exported` uses user_id+report_id+export_format within 10s. |
| c17 | Output defines a funnel from `report_created` → `report_viewed` → `report_exported` with conversion-rate calculation, addressing the first business question directly | PASS | Funnel Definition section shows the three-step progression. Q1 SQL computes: 'COUNT(DISTINCT e.user_id) AS exporters, COUNT(DISTINCT c.user_id) AS creators, ROUND(100.0 * COUNT(DISTINCT e.user_id) / COUNT(DISTINCT c.user_id), 1) AS export_rate_pct' via LEFT JOIN on `report_created` and `report_exported`. |
| c18 | Output's "power user" definition (>5 reports) is operationalised — e.g. a derived user property computed daily from `report_created` count — rather than left as prose | PASS | Q4 SQL provides a full CTE-based operationalisation: `user_report_counts` CTE counts `report_created` per user, `segments` CTE applies `CASE WHEN report_count > 5 THEN 'power' ELSE 'casual' END`, and final SELECT computes export_rate_pct per segment. Not prose — executable SQL. |
| c19 | Output addresses sample-rate or volume estimates per event with a brief retention/deletion policy section keyed on user_id for GDPR-style erasure | PARTIAL | Volume Estimates table covers all four events with daily volume and monthly storage. Privacy section states 'No sampling required'. Retention: '90 days raw events; 2 years aggregated'. Deletion key: '`user_id` — all events for a user can be purged on erasure request.' Ceiling is PARTIAL. |

### Notes

The output is exceptionally comprehensive and meets every criterion. The document structure follows best practices: business questions first, then event catalogue, then supporting infrastructure (standard properties, volume, privacy, SQL, funnel, instrumentation checklist). Notably strong: the 'NOT triggered by' exclusion pattern on every event, the explicit deduplication windows using natural key combinations, and the ready-to-run SQL addressing all four questions. The only criterion with a ceiling below PASS (c8, c19) are scored at their maximum PARTIAL ceiling — both are well-addressed in the output. The time-before-export question (c13) is answered via a paired-event timestamp approach rather than a client-side duration property, which is architecturally sounder and fully demonstrated by the Q3 SQL. The power-user operationalisation (c18) uses warehouse CTE SQL rather than a pre-computed property, which satisfies the spirit of the criterion.
