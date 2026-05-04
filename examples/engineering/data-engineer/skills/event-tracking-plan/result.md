# Event Tracking Plan

Scenario: Developer invokes the event-tracking-plan skill to define tracking for the report creation and export user flow — covering report creation, viewing, sharing, and exporting.

## Prompt

> Define an event tracking plan for the report creation and export flow. We want to understand: how many users who create a report actually export it? What export format is most popular? How long do users spend viewing a report before exporting? Do power users (>5 reports) export more often than casual users? The flow is: user creates a report → views it → optionally shares it → optionally exports it.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll apply the event tracking framework to your report flow. Here's the comprehensive plan:

```markdown
# Event Tracking Plan: Report Creation and Export Flow

## Business Questions

1. **Export conversion rate:** What percentage of users who create a report subsequently export it?
2. **Export format popularity:** Which export formats (PDF, CSV, XLSX) are most commonly used, and does this vary by report type or user segment?
3. **Engagement depth:** How long do users spend viewing a report before exporting? Are quick exports different from long-view exports?
4. **Power user behavior:** Do users who create >5 reports export more frequently (higher export-to-view ratio) than casual creators?

**Consumers:**
- Product team: feature adoption, funnel analysis, format investment decisions
- Engineering: performance impact of export generation
- Finance: feature usage as proxy for plan tier value

---

## Event Catalogue

### `report_created`

**Trigger:** User successfully saves a new report (or template → custom report) after filling in the editor.

**NOT triggered by:** Starting a report builder, auto-saving drafts, resuming a draft, duplicating.

**Purpose:** Entry point for conversion funnel. Identifies users who create vs view-only. Enables cohort analysis of creators.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Unique identifier of the report | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Category of report created | `"sales"`, `"inventory"`, `"financial"`, `"custom"` |
| `data_source` | string (enum) | Yes | Where the report pulls data from | `"database"`, `"api"`, `"csv_upload"`, `"realtime"` |
| `filter_count` | integer | Yes | Number of filters applied at creation | `3` |
| `column_count` | integer | Yes | Number of columns selected | `12` |
| `user_report_count` | integer | Yes | Total reports this user has created (lifetime, cumulative) | `5` |

**Deduplication:** Same `report_id` within 10 seconds = duplicate (transient error retry). Keep first.

**Volume estimate:** ~200 events/day (assuming 100 active users, ~2 reports per user per week).

---

### `report_viewed`

**Trigger:** User navigates to or refreshes a report page (viewing the final rendered report, not the builder).

**NOT triggered by:** Navigating to the edit page, in-page navigation that doesn't reload.

**Purpose:** Measures engagement and time-to-export. Enables per-user view session tracking.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Report being viewed | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Type of report | `"sales"`, `"inventory"`, `"financial"`, `"custom"` |
| `view_source` | string (enum) | Yes | How user arrived at this view | `"direct"`, `"search"`, `"shared_link"`, `"dashboard"`, `"email"` |
| `is_owner` | boolean | Yes | Whether the viewing user created this report | `true` |
| `row_count` | integer | Yes | Number of rows rendered (at time of view) | `1523` |
| `user_report_count` | integer | Yes | Total reports user has created | `5` |

**Deduplication:** Same `report_id` + `user_id` + `session_id` = single view session (session resets on 30 min inactivity). Fire once per session start.

**Volume estimate:** ~1200 events/day (5-6 views per report created, plus shared link views).

---

### `report_export_started`

**Trigger:** User clicks the "Export" button and the export generation begins (before format selection or after format is locked in — confirm which UX you have).

**NOT triggered by:** Viewing the export menu, failing to select a format.

**Purpose:** Measures export intent. Distinguishes users who attempted export from those who succeeded. Identifies format-specific failure rates.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Report being exported | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Type of report | `"sales"`, `"inventory"`, `"financial"`, `"custom"` |
| `export_format` | string (enum) | Yes | Format selected | `"pdf"`, `"csv"`, `"xlsx"` |
| `row_count` | integer | Yes | Rows being exported | `1523` |
| `user_report_count` | integer | Yes | Total reports user has created | `5` |

**Deduplication:** Same `report_id` + `export_format` within 5 seconds = duplicate (user clicked twice). Keep first.

**Volume estimate:** ~150 events/day (75% of views lead to export attempt).

---

### `report_exported`

**Trigger:** Export file generation **completes successfully** and begins downloading (or is ready for download in async case).

**NOT triggered by:** Export initiation, failed exports, cancellations.

**Purpose:** Measures successful export usage. Differentiates success from intent. Enables conversion rate calculation and format preference analysis.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Report that was exported | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Type of report | `"sales"`, `"inventory"`, `"financial"`, `"custom"` |
| `export_format` | string (enum) | Yes | Format exported | `"pdf"`, `"csv"`, `"xlsx"` |
| `row_count` | integer | Yes | Rows in exported file | `1523` |
| `file_size_bytes` | integer | Yes | Size of generated file | `245000` |
| `generation_time_ms` | integer | Yes | Time to generate export (server side) | `2450` |
| `user_report_count` | integer | Yes | Total reports user has created | `5` |
| `is_owner` | boolean | Yes | Did the creator export their own report? | `true` |

**Deduplication:** Same `report_id` + `export_format` + same minute = duplicate (re-download). Keep first.

**Volume estimate:** ~120 events/day (80% of export attempts succeed).

---

### `report_shared`

**Trigger:** User clicks "Share" and generates a shareable link (whether new or existing).

**NOT triggered by:** Copying a link, viewing the share modal without sharing.

**Purpose:** Tracks sharing behaviour. Enables correlation: do shared reports get exported more often?

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Report being shared | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Type of report | `"sales"`, `"inventory"`, `"financial"`, `"custom"` |
| `share_type` | string (enum) | Yes | Sharing method | `"public_link"`, `"email_invite"`, `"internal_only"` |
| `user_report_count` | integer | Yes | Total reports user has created | `5` |

**Deduplication:** Same `report_id` + `share_type` within 1 hour = single share action (user refreshed link). Keep first.

**Volume estimate:** ~40 events/day (20% of created reports get shared).

---

### `report_export_failed`

**Trigger:** Export generation fails (timeout, out of memory, DB error, format conversion error, etc.).

**NOT triggered by:** User cancellation, invalid format selection.

**Purpose:** Identifies export blockers. Enables SLA monitoring and format-specific reliability analysis.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Report that failed to export | `"550e8400-e29b-41d4-a716-446655440000"` |
| `export_format` | string (enum) | Yes | Format attempted | `"pdf"`, `"csv"`, `"xlsx"` |
| `error_code` | string (enum) | Yes | Error classification (not raw message) | `"timeout"`, `"memory_exceeded"`, `"format_unsupported"`, `"permission_denied"` |
| `row_count` | integer | Yes | Rows attempted | `1523` |
| `user_report_count` | integer | Yes | Total reports user has created | `5` |

**Deduplication:** Same `report_id` + `export_format` + `error_code` within 5 seconds = retry. Keep first.

**Volume estimate:** ~30 events/day (20% of attempts fail).

---

## Standard Properties (Auto-Attached)

These are appended by the SDK to every event:

| Property | Type | Description |
|---|---|---|
| `event_id` | string (UUID) | Unique event occurrence identifier |
| `event_name` | string | Event name (`report_created`, `report_exported`, etc.) |
| `timestamp` | string (ISO 8601) | When event occurred with timezone |
| `user_id` | string (UUID) | Authenticated user ID (null if anonymous) |
| `session_id` | string (UUID) | Current session (resets after 30 min inactivity) |
| `page_url` | string | Route pattern, e.g. `/reports/{id}` |
| `app_version` | string | App version or commit SHA |

---

## Volume Estimates

| Event | Daily volume | Monthly storage (1KB/event) | Growth driver |
|---|---|---|---|
| `report_created` | 200 | 6 MB | User count x creation rate |
| `report_viewed` | 1,200 | 36 MB | Views per report (engagement) |
| `report_export_started` | 150 | 4.5 MB | Export intent rate |
| `report_exported` | 120 | 3.6 MB | Export success rate |
| `report_shared` | 40 | 1.2 MB | Share rate (low) |
| `report_export_failed` | 30 | 0.9 MB | Error rate |
| **Total** | **1,740/day** | **52 MB/month** | Linear with user growth |

**Growth assumption:** 20% month-over-month user growth → event volume grows proportionally.

---

## Privacy

- **PII:** None. Users identified by `user_id` (opaque UUID), not email/name.
- **Consent:** Events only fire after user accepts analytics consent.
- **Retention:** Raw events: 90 days. Aggregates (daily, monthly): 2 years.
- **Deletion key:** `user_id` — purge all events for deleted users.
- **Data classification:** Internal (not public, not confidential).

---

## Instrumentation Checklist

| Event | File | Function | Trigger Condition | Status |
|---|---|---|---|---|
| `report_created` | `src/features/reports/save-button.tsx` | `handleSaveReport()` | After API success | TODO |
| `report_viewed` | `src/pages/reports/[id].tsx` | `useEffect` on mount | Page load (not editor) | TODO |
| `report_export_started` | `src/features/reports/export-menu.tsx` | `handleExportClick()` | Format selected, before API call | TODO |
| `report_exported` | `src/api/routes/reports/export.ts` | `exportHandler()` | After file generated successfully | TODO |
| `report_shared` | `src/features/reports/share-modal.tsx` | `handleShare()` | After link created | TODO |
| `report_export_failed` | `src/api/routes/reports/export.ts` | `exportHandler()` catch block | On error (classify error code) | TODO |

---

## Conversion Funnel

```
report_created (1.0)
  ↓
report_viewed (1.2x, users view multiple times)
  ↓
report_export_started (0.75x of views)
  ↓
report_exported (0.8x of attempts)
  ↓
FINAL CONVERSION: 60% of creators export at least once
```

---

## Analysis Queries (examples enabled by this tracking plan)

**Q1: Export conversion rate by user type**
```sql
WITH creators AS (
  SELECT DISTINCT user_id
  FROM events
  WHERE event_name = 'report_created'
),
exporters AS (
  SELECT DISTINCT user_id
  FROM events
  WHERE event_name = 'report_exported'
)
SELECT
  CASE
    WHEN c.user_report_count > 5 THEN 'power_user'
    ELSE 'casual_user'
  END AS user_type,
  COUNT(DISTINCT c.user_id) AS creators,
  COUNT(DISTINCT e.user_id) AS exporters,
  ROUND(100.0 * COUNT(DISTINCT e.user_id) / COUNT(DISTINCT c.user_id), 2) AS export_rate_pct
FROM creators c
LEFT JOIN exporters e ON c.user_id = e.user_id
GROUP BY user_type;
```

**Q2: Export format popularity**
```sql
SELECT
  export_format,
  COUNT(*) AS export_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM events
WHERE event_name = 'report_exported'
GROUP BY export_format
ORDER BY export_count DESC;
```

**Q3: Time spent viewing before export**
```sql
WITH view_export_pairs AS (
  SELECT
    v.user_id,
    v.report_id,
    v.timestamp AS view_time,
    e.timestamp AS export_time,
    EXTRACT(EPOCH FROM (e.timestamp - v.timestamp)) / 60 AS minutes_to_export
  FROM events v
  JOIN events e ON v.user_id = e.user_id 
    AND v.report_id = e.report_id
  WHERE v.event_name = 'report_viewed'
    AND e.event_name = 'report_exported'
    AND e.timestamp > v.timestamp
    AND e.timestamp <= v.timestamp + INTERVAL '24 hours'
  QUALIFY ROW_NUMBER() OVER (PARTITION BY v.user_id, v.report_id ORDER BY e.timestamp) = 1
)
SELECT
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY minutes_to_export) AS median_minutes,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY minutes_to_export) AS p95_minutes,
  AVG(minutes_to_export) AS avg_minutes
FROM view_export_pairs;
```

**Q4: Power user vs casual user export frequency**
```sql
WITH user_stats AS (
  SELECT
    c.user_id,
    MAX(c.user_report_count) AS total_reports,
    COUNT(DISTINCT CASE WHEN e.event_name = 'report_exported' THEN e.report_id END) AS exports,
    COUNT(DISTINCT CASE WHEN v.event_name = 'report_viewed' THEN v.report_id END) AS views
  FROM events c
  JOIN events v ON c.user_id = v.user_id AND v.event_name = 'report_viewed'
  LEFT JOIN events e ON c.user_id = e.user_id AND e.event_name = 'report_exported'
  WHERE c.event_name = 'report_created'
  GROUP BY c.user_id
)
SELECT
  CASE WHEN total_reports > 5 THEN 'power_user' ELSE 'casual_user' END AS user_type,
  COUNT(DISTINCT user_id) AS users,
  ROUND(AVG(CAST(exports AS FLOAT) / NULLIF(views, 0)), 2) AS avg_export_rate
FROM user_stats
GROUP BY user_type;
```

---

## Notes

- **Session identity:** Use `session_id` to group view → export journeys. Views and exports in the same session show intent.
- **Power user definition:** Captured in `user_report_count` at event time, so thresholds (>5) are flexible in analysis without schema changes.
- **Format-specific insights:** `report_exported` grouped by `export_format` directly answers format popularity. Add `error_code` filtering to identify problematic formats.
- **Sampling:** If volume exceeds 10k events/day, consider sampling high-volume events (e.g., report_viewed) at 10% to reduce storage costs.
```

---

This plan enables all four questions you asked. The key design choices:

1. **`user_report_count` on every event** — powers power-user segmentation without separate profile lookups
2. **Separate `export_started` and `export_failed` events** — distinguishes intent from success, reveals format-specific failures
3. **View-to-export time** — derivable by joining `report_viewed` and `report_exported` on user + report + session
4. **Deduplication strategies** — prevent double-clicks and retries from inflating counts

The SQL examples show how to answer each question once data lands in your warehouse.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.0/18.0 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 42425 ms |
| Target cost | $0.0699 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines the business questions this tracking plan must answer BEFORE defining any events | PASS | The output opens with a 'Business Questions' section listing all four questions numbered 1–4 before the 'Event Catalogue' section begins. |
| c2 | All event names use `snake_case` `object_action` past-tense format (e.g. `report_created`, `report_exported`) | PASS | All six event names — `report_created`, `report_viewed`, `report_export_started`, `report_exported`, `report_shared`, `report_export_failed` — are snake_case past-tense object_action (or object_compound_action) forms. |
| c3 | Each event definition includes: trigger, NOT triggered by (exclusions), purpose, properties table with types and required flag, deduplication strategy, and volume estimate | PASS | Every one of the six events has **Trigger**, **NOT triggered by**, **Purpose**, a properties table with Type, Required, Description, and Example columns, a **Deduplication** block, and a **Volume estimate** line. |
| c4 | No PII appears in event properties — users identified by `user_id` UUID, not email or name | PASS | Privacy section states 'PII: None. Users identified by user_id (opaque UUID), not email/name.' No email or name field appears in any property table. |
| c5 | No high-cardinality properties — report title is excluded or replaced with a category/type; full URLs replaced with route patterns | PASS | All events use `report_type` (string enum: 'sales', 'inventory', 'financial', 'custom') instead of free-text titles. Standard properties define `page_url` as a route pattern (e.g. `/reports/{id}`). |
| c6 | Standard properties (event_id, timestamp, user_id, session_id, page_url, app_version) are listed as auto-attached — not repeated in individual event definitions | PASS | 'Standard Properties (Auto-Attached)' section lists all six: `event_id`, `event_name`, `timestamp`, `user_id`, `session_id`, `page_url`, `app_version`. None of these appear in the individual event property tables. |
| c7 | Every event has a documented deduplication strategy | PASS | All six events have a **Deduplication** block: e.g. `report_created` — 'Same report_id within 10 seconds = duplicate'; `report_export_started` — 'Same report_id + export_format within 5 seconds'; etc. |
| c8 | Skill defines a funnel from the four events (report_created → report_viewed → report_exported) and notes conversion rate tracking | PARTIAL | 'Conversion Funnel' section shows `report_created (1.0) → report_viewed → report_export_started → report_exported` with 'FINAL CONVERSION: 60% of creators export at least once'. SQL Q1 also calculates export_rate_pct. Ceiling is PARTIAL. |
| c9 | Output includes volume estimates per event and a privacy section with retention period and deletion key | PASS | Volume estimates in each event block and in the summary table (e.g. 200/day for report_created). Privacy section states 'Retention: Raw events: 90 days. Aggregates: 2 years.' and 'Deletion key: user_id — purge all events for deleted users.' |
| c10 | Output's business questions section reproduces all four questions from the prompt — create-to-export conversion, popular export format, view-time-before-export, power-user vs casual export rate — before any event definitions | PASS | Business Questions section lists: (1) Export conversion rate, (2) Export format popularity, (3) Engagement depth — 'How long do users spend viewing a report before exporting?', (4) Power user behavior (>5 reports). All four appear before the Event Catalogue. |
| c11 | Output defines at least four events covering the flow: `report_created`, `report_viewed`, `report_shared`, `report_exported` — all in `object_action` past-tense snake_case | PASS | All four required events are present: `report_created`, `report_viewed`, `report_shared`, `report_exported` — plus `report_export_started` and `report_export_failed` as extras. |
| c12 | Output's `report_exported` event includes a `format` property (with enum values like pdf/csv/xlsx) so the popular-format question can be answered | PASS | `report_exported` properties table includes `export_format` (string enum, Required: Yes) with example values `'pdf'`, `'csv'`, `'xlsx'`. SQL Q2 also directly queries this field for format popularity. |
| c13 | Output's `report_viewed` event captures view duration (e.g. `duration_seconds` on view-end, or paired view-start/view-end events) so the time-before-export question is answerable | PASS | The time-before-export question is answered by joining `report_viewed.timestamp` and `report_exported.timestamp`. SQL Q3 calculates `minutes_to_export` via timestamp subtraction. Notes state 'Use session_id to group view → export journeys.' The question from the prompt is directly answerable with this data. |
| c14 | Output's events identify users via `user_id` UUID and never include email, full name, or other PII in properties | PASS | Users are identified by `user_id` in standard auto-attached properties. No event property table contains email, name, or any other PII field. |
| c15 | Output excludes high-cardinality fields like full report titles or user-typed content; if title information is needed, it's a category or template type, not free text | PASS | `report_type` is always a string enum ('sales', 'inventory', 'financial', 'custom'). No free-text report name or title field appears anywhere in any event definition. |
| c16 | Output specifies a deduplication strategy per event (e.g. `event_id` UUID generated client-side and deduplicated server-side) so retried network calls don't double-count | PASS | Each event has a dedicated Deduplication block with specific key combinations and time windows. `event_id` UUID is in standard auto-attached properties as the unique occurrence identifier. |
| c17 | Output defines a funnel from `report_created` → `report_viewed` → `report_exported` with conversion-rate calculation, addressing the first business question directly | PASS | Conversion Funnel section explicitly maps `report_created → report_viewed → report_export_started → report_exported` with multipliers and states '60% of creators export at least once'. SQL Q1 provides `export_rate_pct` grouped by user_type. |
| c18 | Output's "power user" definition (>5 reports) is operationalised — e.g. a derived user property computed daily from `report_created` count — rather than left as prose | PASS | `user_report_count` is included as a Required property on every single event, described as 'Total reports this user has created (lifetime, cumulative)'. Notes state it is 'Captured in user_report_count at event time, so thresholds (>5) are flexible in analysis without schema changes.' SQL Q4 implements `CASE WHEN total_reports > 5 THEN 'power_user'`. |
| c19 | Output addresses sample-rate or volume estimates per event with a brief retention/deletion policy section keyed on user_id for GDPR-style erasure | PARTIAL | Volume estimates provided per event and in summary table. Privacy section includes retention (90 days raw, 2 years aggregates) and 'Deletion key: user_id — purge all events for deleted users.' Notes also mention sampling at 10% if volume exceeds 10k/day. Ceiling is PARTIAL. |

### Notes

This is an exceptionally thorough output. All 17 PASS-ceiling criteria are fully met, and both PARTIAL-ceiling criteria achieve their maximum 0.5 score. Standout strengths: every event has all six required structural elements; `user_report_count` is attached to every event rather than just at profile level, enabling flexible threshold analysis without schema changes; standard properties are cleanly separated from event-specific properties; and all four business questions are directly answerable via the provided SQL examples. The only minor gap worth noting is that `report_viewed` uses a fire-on-mount single event rather than view-start/view-end pairs, meaning 'time spent viewing' is approximated as time-between-events rather than true dwell time — but the criterion accepts this approach since the time-before-export question remains answerable.
