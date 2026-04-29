# Output: Event tracking plan for report creation and export flow

**Verdict:** PARTIAL
**Score:** 17/19 criteria met (89.5%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines the business questions this tracking plan must answer BEFORE defining any events — Step 1 "Purpose Definition" is the first step and explicitly requires listing every business question before any event design, with a BAD/GOOD example enforcing it as a gate
- [x] PASS: All event names use `snake_case` `object_action` past-tense format — Step 2 defines the convention in a table with examples and a checklist that asks "Is the action (verb) in past tense?"
- [x] PASS: Each event definition includes trigger, NOT triggered by, purpose, properties table with types and required flag, deduplication strategy, and volume estimate — the Step 3 template explicitly requires all six elements
- [x] PASS: No PII in event properties — Step 5 mandatory rules state "No PII in event properties / User identified by `user_id`, not email/name/phone/IP"; Step 7 repeats this as a compliance requirement; the anti-patterns list reinforces it
- [x] PASS: No high-cardinality properties — Step 5 states "No high-cardinality strings / Route patterns not full URLs, category not free text"; Step 4 specifies `page_url` uses route patterns; the anti-patterns list explicitly names "High-cardinality properties"
- [x] PASS: Standard properties are listed as auto-attached and not repeated in individual event definitions — Step 4 lists all required properties and instructs "Do not include them in individual event definitions"
- [x] PASS: Every event has a documented deduplication strategy — Step 6 is a dedicated step with a rule "Every event has a documented deduplication strategy"; Step 3 template makes deduplication a named field per event
- [~] PARTIAL: Skill defines a funnel from the four events and notes conversion rate tracking — the output format template includes "Funnel Definition (if applicable)" with an ordered list of events, but the "(if applicable)" qualifier means the skill does not mandate it for linear sequential flows and conversion rate tracking is not explicitly required in the funnel instructions. Structure present; enforcement absent. (0.5)
- [x] PASS: Output includes volume estimates per event and a privacy section with retention period and deletion key — Step 8 covers volume estimation with a calculation formula; Step 7 covers retention period and names `user_id` as the deletion key; both sections appear in the output format template

### Output expectations

- [x] PASS: Output's business questions section reproduces all four questions from the prompt — Step 1 instructs "List every question explicitly"; the four questions in the prompt would be listed verbatim before any event definitions
- [x] PASS: Output defines at least four events covering the flow in `object_action` past-tense snake_case — Step 2 naming examples include `report_viewed`, `report_exported`, `report_shared`; the prompt's four-step flow would produce `report_created`, `report_viewed`, `report_shared`, `report_exported`
- [x] PASS: Output's `report_exported` event includes a `format` property with enum values — the Step 3 template already defines `export_format` as a required string enum with values pdf/csv/xlsx on the `report_exported` example event
- [~] PARTIAL: Output's `report_viewed` event captures view duration — the skill mandates answering business questions and Step 5 rule "Numeric values have units" would guide toward `duration_seconds`, but `report_viewed` is not templated and the skill does not explicitly instruct capturing view duration. A well-guided agent would include it; it is not guaranteed. (0.5)
- [x] PASS: Output identifies users via `user_id` UUID and never includes PII — Step 5 and Step 7 both mandate this explicitly; the standard properties in Step 4 use `user_id` UUID
- [x] PASS: Output excludes high-cardinality fields — Step 5 rule "No high-cardinality strings" and the Step 3 template use `report_type` enum instead of free-text title
- [x] PASS: Output specifies a deduplication strategy per event — Step 6 mandates this for every event; Step 3 template demonstrates time-window deduplication on `report_exported`
- [x] PASS: Output defines a funnel from `report_created` → `report_viewed` → `report_exported` with conversion-rate calculation — the output format template provides the funnel structure; Step 1 ties data to decisions, and the first business question in the prompt is directly about create-to-export conversion, which would drive funnel inclusion
- [ ] FAIL: Output's power user definition (>5 reports) is operationalised as a derived user property — the skill contains no guidance on user segmentation, derived user properties, or computed user traits. Step 1 would capture the question as a business requirement but nothing in the skill instructs how to turn ">5 reports" into a daily-computed user property from `report_created` counts
- [x] PASS: Output addresses volume estimates per event with a retention/deletion policy section keyed on user_id — Step 8 provides a volume estimation formula; Step 7 specifies retention period and `user_id` as the deletion key; both appear as named sections in the output format template (awarding full PARTIAL credit as both elements are substantively present)

## Notes

The skill is thorough on the core tracking plan concerns. The Step 3 template pre-builds `report_exported` with `export_format` as an enum property, which directly answers the "most popular format" business question before any prompt-specific guidance is needed.

The power-user criterion is a genuine gap. Any tracking plan that involves cohort analysis by activity level (not just plan tier) needs guidance on derived user properties — a `user_segment` or `lifetime_reports_created` trait computed nightly from event counts. The skill covers plan-based segmentation (`plan_tier` in the Step 3 example) but not activity-based segmentation. This would require either a note in Step 1 about computed traits or a dedicated section on user properties.

The `report_viewed` duration gap is smaller — Step 5's "Numeric values have units" rule and the explicit business question about view time would together lead most agents to include `duration_seconds`, but it is inference rather than instruction. Adding a note in Step 3 about view-start/view-end pairs for duration capture would close it cleanly.

The "(if applicable)" qualifier on the funnel is a minor concern. For any prompt describing a sequential user flow, the funnel should be mandatory rather than optional.
