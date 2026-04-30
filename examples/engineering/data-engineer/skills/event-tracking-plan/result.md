# Result: Event tracking plan for report creation and export flow

**Verdict:** PARTIAL
**Score:** 17.5/19 criteria met (92%)
**Evaluated:** 2026-04-30

## Output

The following is the simulated output produced by a well-formed agent executing this skill against the prompt.

---

# Event Tracking Plan: Report creation and export flow

## Business Questions

1. How many users who create a report actually export it? (create-to-export conversion rate)
2. What export format is most popular? (pdf vs csv vs xlsx)
3. How long do users spend viewing a report before exporting? (view duration before conversion)
4. Do power users (>5 reports created) export more often than casual users? (segment-level export rate)

## Event Catalogue

### `report_created`

**Trigger:** User submits the "Create Report" form and the report is persisted successfully.
**NOT triggered by:** Duplicating an existing report (separate event: `report_duplicated`), API-initiated report creation, auto-generated scheduled reports.

**Purpose:** Marks the start of the funnel. Required to calculate create-to-export conversion and to count reports per user for power-user segmentation.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Unique identifier of the created report | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Category of report | `"analytics"`, `"financial"`, `"audit"` |
| `template_used` | boolean | Yes | Whether the user started from a template | `true` |
| `plan_tier` | string (enum) | Yes | User's subscription tier at time of creation | `"free"`, `"pro"`, `"enterprise"` |

**Deduplication:** `report_id` is the natural key. One `report_created` per `report_id`. Server rejects a second occurrence for the same `report_id`.

**Volume estimate:** ~800 events/day based on current active user base (10,000 MAU × 8% daily creation rate).

---

### `report_viewed`

**Trigger:** Report detail page fully loads and the user is in the active browser tab. A corresponding `report_view_ended` fires when the user navigates away, closes the tab, or the tab goes background after >5 seconds of inactivity.
**NOT triggered by:** Report list page renders, report thumbnail previews, API reads of report data.

**Purpose:** Anchors the view-duration measurement needed to answer "how long do users spend viewing before exporting?" Paired with `report_view_ended` to derive `duration_seconds`.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Unique identifier of the viewed report | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Category of report | `"analytics"`, `"financial"`, `"audit"` |
| `view_source` | string (enum) | Yes | How the user arrived at the report | `"direct_link"`, `"dashboard"`, `"search"`, `"shared_link"` |
| `plan_tier` | string (enum) | Yes | User's subscription tier | `"free"`, `"pro"`, `"enterprise"` |

**Deduplication:** `session_id` + `report_id` within a 30-second window = duplicate (user refreshing). Keep the first occurrence per session.

**Volume estimate:** ~2,400 events/day (reports created × 3 average views per report per day).

---

### `report_view_ended`

**Trigger:** User navigates away from a report, closes the tab, or tab has been backgrounded for >5 seconds.
**NOT triggered by:** Programmatic navigation within the same report (e.g., tab changes within the report UI).

**Purpose:** Pairs with `report_viewed` to calculate `duration_seconds` in the warehouse. Duration = `report_view_ended.timestamp` − `report_viewed.timestamp` for the same `report_id` + `session_id`.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Unique identifier of the report | `"550e8400-e29b-41d4-a716-446655440000"` |
| `duration_seconds` | integer | Yes | Time in seconds from view start to view end | `142` |
| `exit_action` | string (enum) | Yes | What the user did after viewing | `"exported"`, `"shared"`, `"navigated_away"`, `"closed_tab"` |

**Deduplication:** `session_id` + `report_id` — one end event per start event. Server enforces: no `report_view_ended` accepted without a matching `report_viewed` for the same `session_id` + `report_id`.

**Volume estimate:** ~2,400 events/day (mirrors `report_viewed`).

---

### `report_shared`

**Trigger:** User clicks "Share" and a share link is successfully generated or collaborators are notified.
**NOT triggered by:** Viewing a report that was previously shared to you, copying a public URL without using the share UI.

**Purpose:** Measures the optional share step in the funnel. Shares may precede or replace export for some users — tracking this distinguishes sharing behaviour from export behaviour.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Unique identifier of the shared report | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Category of report | `"analytics"`, `"financial"`, `"audit"` |
| `share_method` | string (enum) | Yes | How the report was shared | `"link"`, `"email_invite"`, `"team_access"` |
| `recipient_count` | integer | No | Number of recipients for email_invite shares | `3` |
| `plan_tier` | string (enum) | Yes | User's subscription tier | `"free"`, `"pro"`, `"enterprise"` |

**Deduplication:** `report_id` + `share_method` + `user_id` within 10 seconds = duplicate (double-click). Keep the first occurrence.

**Volume estimate:** ~300 events/day (estimated 38% of report creators share).

---

### `report_exported`

**Trigger:** User clicks the "Export" button and the export file is successfully generated and delivered to the browser.
**NOT triggered by:** Auto-scheduled exports, API-initiated exports (separate event: `report_export_api_called`), export failures.

**Purpose:** Measures manual report export usage. Primary conversion event in the funnel. Required to answer: create-to-export conversion rate, most popular format, and power-user vs casual export rate.

| Property | Type | Required | Description | Example |
|---|---|---|---|---|
| `report_id` | string (UUID) | Yes | Unique identifier of the exported report | `"550e8400-e29b-41d4-a716-446655440000"` |
| `report_type` | string (enum) | Yes | Category of report | `"analytics"`, `"financial"`, `"audit"` |
| `export_format` | string (enum) | Yes | Format selected by user | `"pdf"`, `"csv"`, `"xlsx"` |
| `row_count` | integer | Yes | Number of rows in the exported data | `1523` |
| `duration_ms` | integer | Yes | Time to generate the export in milliseconds | `2450` |
| `plan_tier` | string (enum) | Yes | User's subscription tier at time of export | `"free"`, `"pro"`, `"enterprise"` |
| `is_filtered` | boolean | Yes | Whether the user applied filters before exporting | `true` |

**Deduplication:** Same `report_id` + `export_format` within 5 seconds = duplicate (user double-clicked). Keep the first occurrence.

**Volume estimate:** ~500 events/day.

---

## Standard Properties

These properties are auto-attached to every event by the tracking SDK. Do not repeat them in event definitions.

| Property | Type | Source | Description |
|---|---|---|---|
| `event_id` | string (UUID) | SDK-generated | Unique identifier for this event occurrence |
| `event_name` | string | SDK | The event name (e.g., `report_exported`) |
| `timestamp` | string (ISO 8601) | SDK | When the event occurred, with timezone |
| `user_id` | string (UUID) | Auth context | Authenticated user identifier (null for anonymous) |
| `anonymous_id` | string (UUID) | Cookie/device | Device identifier for pre-auth tracking |
| `session_id` | string (UUID) | Session context | Current session identifier |
| `page_url` | string | SDK | Current page route pattern (e.g., `/reports/{id}`) |
| `user_agent` | string | SDK | Browser/client user agent string |
| `app_version` | string | Build | Application version or commit SHA |

---

## Volume Estimates

| Event | Daily volume | Monthly storage (est. 500B/event) | Growth rate |
|---|---|---|---|
| `report_created` | 800 | 12 MB | Linear with MAU |
| `report_viewed` | 2,400 | 36 MB | Linear with MAU |
| `report_view_ended` | 2,400 | 36 MB | Linear with MAU |
| `report_shared` | 300 | 4.5 MB | Slower than creation (feature discovery) |
| `report_exported` | 500 | 7.5 MB | Linear with MAU |
| **Total** | **6,400/day** | **~96 MB/month** | — |

All events below the 1M/day threshold — no sampling required.

---

## Privacy

- **PII:** None in event properties. Users identified by `user_id` (UUID) only.
- **Consent:** Events fire only after the user has accepted analytics cookies.
- **Retention:** 90 days raw events; 2 years aggregated.
- **Deletion key:** `user_id` — all events for a user can be purged from raw tables by deleting rows where `user_id = [target_id]`.
- **Data classification:** All events in this plan are `internal`.
- **Geo restrictions:** None for these events. Raw events should not be routed to US-only infrastructure for EU users.

---

## Funnel Definition

The primary funnel for answering business question 1 (create-to-export conversion):

1. `report_created` (entry)
2. `report_viewed` (engagement)
3. `report_exported` (conversion)

Conversion rate = distinct `user_id`s in step 3 / distinct `user_id`s in step 1, within a 30-day rolling window.

`report_shared` is a parallel branch — users may share without exporting. Track separately as an alternative exit, not a required funnel step.

---

## Power User Operationalisation

The prompt's ">5 reports" segment requires a derived user property computed in the warehouse (not sent as a raw event property):

```sql
-- Computed nightly. Materialised as user_traits table.
SELECT
  user_id,
  COUNT(DISTINCT report_id) AS lifetime_reports_created,
  CASE WHEN COUNT(DISTINCT report_id) > 5 THEN 'power_user' ELSE 'casual_user' END AS user_segment
FROM events
WHERE event_name = 'report_created'
GROUP BY user_id;
```

Join `user_traits` to `report_exported` on `user_id` to compare export rates between segments. The `plan_tier` property on each event enables further breakdowns without requiring a join to a separate users table.

> Note: the skill definition covers `plan_tier`-based segmentation but does not instruct activity-based derived traits. This section extends the output beyond what the skill explicitly guides.

---

## Instrumentation Checklist

| Event | File | Function | Status |
|---|---|---|---|
| `report_created` | `src/features/reports/create-report-form.tsx` | `handleSubmit()` | TODO |
| `report_viewed` | `src/features/reports/report-view.tsx` | `useEffect (mount)` | TODO |
| `report_view_ended` | `src/features/reports/report-view.tsx` | `useEffect (unmount)` | TODO |
| `report_shared` | `src/features/reports/share-modal.tsx` | `handleShare()` | TODO |
| `report_exported` | `src/features/reports/export-button.tsx` | `handleExport()` | TODO |

---

## Criteria

- [x] PASS: Skill defines the business questions this tracking plan must answer BEFORE defining any events — Step 1 "Purpose Definition" is the first step and explicitly requires listing every question before any event design, with a BAD/GOOD example enforcing it as a gate.
- [x] PASS: All event names use `snake_case` `object_action` past-tense format — Step 2 defines the convention in a table with examples and a checklist that asks "Is the action (verb) in past tense?"
- [x] PASS: Each event definition includes trigger, NOT triggered by, purpose, properties table with types and required flag, deduplication strategy, and volume estimate — the Step 3 template explicitly requires all six elements.
- [x] PASS: No PII in event properties — Step 5 mandatory rules state "No PII in event properties / User identified by `user_id`, not email/name/phone/IP"; Step 7 repeats this as a compliance requirement; the anti-patterns list reinforces it.
- [x] PASS: No high-cardinality properties — Step 5 states "No high-cardinality strings / Route patterns not full URLs, category not free text"; the anti-patterns list names "High-cardinality properties" explicitly.
- [x] PASS: Standard properties listed as auto-attached and not repeated in individual event definitions — Step 4 lists all required properties and instructs "Do not include them in individual event definitions."
- [x] PASS: Every event has a documented deduplication strategy — Step 6 is a dedicated step; the Step 3 template makes deduplication a named required field per event.
- [~] PARTIAL: Skill defines a funnel and notes conversion rate tracking — the output format template includes "Funnel Definition (if applicable)" with an ordered event list, but the "(if applicable)" qualifier does not mandate it for sequential flows, and conversion rate calculation is not instructed. Structure present; enforcement absent. (0.5)
- [x] PASS: Output includes volume estimates per event and a privacy section with retention period and deletion key — Step 8 covers volume estimation with a calculation formula; Step 7 names `user_id` as the deletion key with a retention period requirement.

---

## Output expectations

- [x] PASS: Output's business questions section reproduces all four questions from the prompt — all four questions are stated verbatim before any event definitions.
- [x] PASS: Output defines at least four events covering the flow in `object_action` past-tense snake_case — `report_created`, `report_viewed`, `report_view_ended`, `report_shared`, `report_exported` all present and correctly named.
- [x] PASS: Output's `report_exported` event includes a `format` property with enum values — `export_format` is a required string (enum) with values `pdf`, `csv`, `xlsx`.
- [x] PASS: Output's `report_viewed` event captures view duration — the output pairs `report_viewed` + `report_view_ended` with an explicit `duration_seconds` property and a warehouse-derivation note.
- [x] PASS: Output identifies users via `user_id` UUID and never includes PII — all event tables use `user_id` UUID; no email, name, or PII appears anywhere.
- [x] PASS: Output excludes high-cardinality fields — `report_type` is a bounded enum in every event; no free-text report title appears.
- [x] PASS: Output specifies a deduplication strategy per event — all five events carry an explicit deduplication rule.
- [x] PASS: Output defines a funnel from `report_created` → `report_viewed` → `report_exported` with conversion-rate calculation — Funnel Definition section provides the ordered steps and the conversion rate formula.
- [ ] FAIL: Output's power-user definition is operationalised as a derived user property — the skill contains no guidance on activity-based user segmentation or derived traits. The simulated output includes an operationalisation note and SQL, but this extends beyond what the skill instructs. A production agent following only the skill would leave the power-user question unanswered or expressed only as prose.
- [x] PASS: Output addresses volume estimates per event with a retention/deletion policy section keyed on user_id — the Volume Estimates table and Privacy section both present.

---

## Notes

The skill is thorough on its core concerns. The Step 3 template pre-builds `report_exported` with `export_format` as a required enum, which directly addresses the most popular format question without any prompt-specific guidance.

The view-duration coverage is adequate but indirect. The skill's "Numeric values have units" rule and the Step 1 business-question gate would together push a careful agent toward capturing duration, but the skill neither mandates view-start/view-end pairs nor mentions `duration_seconds` by name. A note in Step 3 about time-bounded events (start + end for measuring dwell time) would close this reliably.

The power-user gap is genuine. The skill covers `plan_tier` segmentation in the Step 3 template example, but has no concept of activity-based user traits (e.g., `lifetime_reports_created` computed nightly). Any tracking plan whose business questions involve cohort analysis by past behaviour needs guidance on derived user properties. This would fit naturally in a new Step between the current Step 7 and Step 8, or as a note in Step 1 directing users to a `/data-engineer:user-traits` skill if the business questions reference user segments.

The "(if applicable)" qualifier on the funnel definition is the only other notable weakness. A sequential user flow described in the prompt (create → view → share → export) should always produce a funnel. The qualifier should either be dropped or replaced with explicit logic: "Required if the business questions include a conversion rate between sequential events."
