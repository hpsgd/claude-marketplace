# Test: Event tracking plan for report creation and export flow

Scenario: Developer invokes the event-tracking-plan skill to define tracking for the report creation and export user flow — covering report creation, viewing, sharing, and exporting.

## Prompt

Define an event tracking plan for the report creation and export flow. We want to understand: how many users who create a report actually export it? What export format is most popular? How long do users spend viewing a report before exporting? Do power users (>5 reports) export more often than casual users? The flow is: user creates a report → views it → optionally shares it → optionally exports it.

## Criteria

- [ ] PASS: Skill defines the business questions this tracking plan must answer BEFORE defining any events
- [ ] PASS: All event names use `snake_case` `object_action` past-tense format (e.g. `report_created`, `report_exported`)
- [ ] PASS: Each event definition includes: trigger, NOT triggered by (exclusions), purpose, properties table with types and required flag, deduplication strategy, and volume estimate
- [ ] PASS: No PII appears in event properties — users identified by `user_id` UUID, not email or name
- [ ] PASS: No high-cardinality properties — report title is excluded or replaced with a category/type; full URLs replaced with route patterns
- [ ] PASS: Standard properties (event_id, timestamp, user_id, session_id, page_url, app_version) are listed as auto-attached — not repeated in individual event definitions
- [ ] PASS: Every event has a documented deduplication strategy
- [ ] PARTIAL: Skill defines a funnel from the four events (report_created → report_viewed → report_exported) and notes conversion rate tracking
- [ ] PASS: Output includes volume estimates per event and a privacy section with retention period and deletion key

## Output expectations

- [ ] PASS: Output's business questions section reproduces all four questions from the prompt — create-to-export conversion, popular export format, view-time-before-export, power-user vs casual export rate — before any event definitions
- [ ] PASS: Output defines at least four events covering the flow: `report_created`, `report_viewed`, `report_shared`, `report_exported` — all in `object_action` past-tense snake_case
- [ ] PASS: Output's `report_exported` event includes a `format` property (with enum values like pdf/csv/xlsx) so the popular-format question can be answered
- [ ] PASS: Output's `report_viewed` event captures view duration (e.g. `duration_seconds` on view-end, or paired view-start/view-end events) so the time-before-export question is answerable
- [ ] PASS: Output's events identify users via `user_id` UUID and never include email, full name, or other PII in properties
- [ ] PASS: Output excludes high-cardinality fields like full report titles or user-typed content; if title information is needed, it's a category or template type, not free text
- [ ] PASS: Output specifies a deduplication strategy per event (e.g. `event_id` UUID generated client-side and deduplicated server-side) so retried network calls don't double-count
- [ ] PASS: Output defines a funnel from `report_created` → `report_viewed` → `report_exported` with conversion-rate calculation, addressing the first business question directly
- [ ] PASS: Output's "power user" definition (>5 reports) is operationalised — e.g. a derived user property computed daily from `report_created` count — rather than left as prose
- [ ] PARTIAL: Output addresses sample-rate or volume estimates per event with a brief retention/deletion policy section keyed on user_id for GDPR-style erasure
