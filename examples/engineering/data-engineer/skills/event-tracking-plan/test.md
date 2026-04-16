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
