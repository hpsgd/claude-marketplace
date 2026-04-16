# Event tracking plan for report creation and export flow

Developer invokes the event-tracking-plan skill to define tracking for the report creation and export user flow — covering report creation, viewing, sharing, and exporting.

## Prompt

> Define an event tracking plan for the report creation and export flow. We want to understand: how many users who create a report actually export it? What export format is most popular? How long do users spend viewing a report before exporting? Do power users (>5 reports) export more often than casual users? The flow is: user creates a report → views it → optionally shares it → optionally exports it.

The event-tracking-plan skill, applied to this report flow, would produce the following.

---

## Output

### Event Tracking Plan: Report Creation and Export Flow

#### Business Questions (must answer before defining events)

1. What percentage of users who create a report export it?
2. Which export format is most popular (pdf, csv, xlsx)?
3. How long between `report_viewed` and `report_exported` for users who export?
4. Do users with >5 reports created export more often than users with 1-5?

#### Standard Properties (auto-attached — do not repeat in event definitions)

The following properties are automatically attached by the tracking SDK to every event. Do not include them in individual event definitions.

| Property | Type | Description |
|---|---|---|
| event_id | UUID | Unique event identifier — used for deduplication |
| event_name | string | Machine-readable event name |
| timestamp | ISO 8601 | UTC timestamp of event fire |
| user_id | UUID | Authenticated user identifier (no PII) |
| anonymous_id | UUID | Pre-login identifier for stitching |
| session_id | UUID | Browser/app session |
| page_url | string | Route pattern — `/reports/{id}`, not full URL |
| user_agent | string | Sanitised client string |
| app_version | string | Semantic version of the app |

#### Events

---

##### `report_created`

**Trigger:** User clicks "Create Report" and the report is successfully saved (API returns 201).

**NOT triggered by:** Report duplication via API, template-generated reports, admin-created reports on behalf of users.

**Purpose:** Answers Q4 (power user segmentation); starting point of the export funnel.

**Properties:**

| Property | Type | Required | Description |
|---|---|---|---|
| report_id | UUID | Yes | Unique report identifier |
| report_type | enum (dashboard\|summary\|detailed) | Yes | Category — not free text |
| template_used | boolean | Yes | Was a template applied? |

**Deduplication:** Same `report_id` within 10 seconds = duplicate (double-click protection on the save button). Deduplicate on `report_id` in the warehouse.

**Volume estimate:** ~300/day

---

##### `report_viewed`

**Trigger:** Report detail page renders with content visible (page load complete, not navigation start).

**NOT triggered by:** Report list page views, thumbnail previews, admin report views.

**Purpose:** Starting point for time-to-export calculation (Q3). Measures engagement before export.

**Properties:**

| Property | Type | Required | Description |
|---|---|---|---|
| report_id | UUID | Yes | Which report was viewed |
| report_type | enum | Yes | Category of report |
| view_source | enum (direct\|shared_link\|dashboard) | Yes | How the user arrived |

**Deduplication:** Same `user_id` + `report_id` within 30 seconds = duplicate page load. Keep first.

**Volume estimate:** ~1200/day

---

##### `report_shared`

**Trigger:** User clicks "Share" and a share link is generated.

**NOT triggered by:** Copying the report URL manually, sharing via API.

**Purpose:** Measures share rate for context on `report_viewed` events sourced from shared links.

**Properties:**

| Property | Type | Required | Description |
|---|---|---|---|
| report_id | UUID | Yes | Which report was shared |
| share_method | enum (link\|email_invite) | Yes | How sharing was initiated |

**Deduplication:** Same `report_id` + `user_id` within 5 seconds = duplicate.

**Volume estimate:** ~150/day

---

##### `report_exported`

**Trigger:** User clicks "Export" and the export file is successfully generated and download begins.

**NOT triggered by:** Scheduled exports, API-initiated exports (separate event `report_export_scheduled`), failed export attempts.

**Purpose:** Answers Q1 (export rate), Q2 (format popularity), Q3 (time delta with `report_viewed`).

**Properties:**

| Property | Type | Required | Description |
|---|---|---|---|
| report_id | UUID | Yes | Which report was exported |
| export_format | enum (pdf\|csv\|xlsx) | Yes | Answers Q2 |
| export_duration_ms | integer | No | Time from click to download start |

**Deduplication:** Same `report_id` + `export_format` within 5 seconds = duplicate (double-click). Keep first.

**Volume estimate:** ~500/day

---

#### Funnel Definition

| Step | Event | Condition |
|---|---|---|
| 1 | `report_created` | — |
| 2 | `report_viewed` | Same `user_id`, any `report_id` |
| 3 | `report_exported` | Same `user_id`, same `report_id` as viewed |

Conversion rate: step 1 → step 3 answers Q1 directly.

#### Volume Estimates

| Event | Est. volume/day |
|---|---|
| report_created | ~300 |
| report_viewed | ~1,200 |
| report_shared | ~150 |
| report_exported | ~500 |

#### Privacy

| Field | Value |
|---|---|
| PII in events | None — users identified by `user_id` UUID only |
| Retention | 90 days raw events; aggregated metrics retained indefinitely |
| Deletion key | `user_id` — delete or anonymise all events with matching `user_id` on erasure request |
| Consent | All tracking requires active session (implicit consent on login); opt-out suppresses all events |

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill defines business questions before events — Step 1 "Purpose Definition" is the first step and requires listing every business question the tracking plan must answer before any events are defined. The instruction "If you can't articulate the question, you don't need the event" enforces this as a gate.

- [x] PASS: All event names use snake_case object_action past tense — Step 2 naming convention specifies snake_case, object_action structure, and past tense with examples and a naming checklist. All four events in the simulated output (`report_created`, `report_viewed`, `report_shared`, `report_exported`) conform to this format.

- [x] PASS: Each event definition includes all required elements — Step 3 template requires: Trigger, NOT triggered by (exclusions), Purpose, properties table with Type/Required/Description columns, Deduplication, and Volume estimate. All six elements are present in each event definition in the simulated output.

- [x] PASS: No PII in event properties — Step 7 Privacy: "No PII in events — User identified by user_id, not email/name/phone." Step 5 property design rules list "No PII in event properties" as a mandatory rule. Users are identified by UUID only throughout.

- [x] PASS: No high-cardinality properties — Step 5 property design rules: "No high-cardinality strings — Explodes storage, breaks GROUP BY — Route patterns not full URLs, category not free text." Report title is absent; `report_type` is an enum. Anti-patterns explicitly name "High-cardinality properties — full URLs, user-generated text."

- [x] PASS: Standard properties listed as auto-attached — Step 4 explicitly states "These properties are automatically attached to every event by the tracking SDK. Do not include them in individual event definitions." Lists all six specified properties plus `anonymous_id` and `user_agent`.

- [x] PASS: Every event has a documented deduplication strategy — Step 6 "Deduplication Strategy" requires a strategy per event; Step 3 template makes deduplication a mandatory field; rule: "Every event has a documented deduplication strategy." All four events have distinct deduplication logic.

- [~] PARTIAL: Skill defines a funnel from the four events — output format template includes "## Funnel Definition (if applicable)" as a named section. Coverage is present but marked "if applicable" rather than required for flows with a clear sequence. PARTIAL ceiling is appropriate: the funnel section exists in the template but is not mandated for linear user flows.

- [x] PASS: Output includes volume estimates and privacy section with retention and deletion key — Step 8 Volume Estimation is a mandatory step; output format template requires a Volume Estimates table and a Privacy section with retention period and deletion key. Both are present in the simulated output.

## Notes

The "if applicable" qualifier on the funnel definition is the only soft spot. For a flow explicitly described as a linear sequence (create → view → share → export), the skill should arguably mandate a funnel definition rather than leaving it conditional. The Step 4 auto-attached properties list is notably thorough — including `anonymous_id` for pre-login identity stitching covers a real analytics gap that most tracking templates miss. The NOT triggered by field in each event definition is valuable and often omitted in tracking plans; it prevents double-counting from API exports, template generation, and admin actions.
