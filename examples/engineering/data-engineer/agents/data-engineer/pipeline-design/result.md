# Result: Event-sourced user activity pipeline

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16.5/19 criteria met (87%) |
| **Evaluated** | 2026-04-29 |
| **Agent** | `plugins/engineering/data-engineer/agents/data-engineer.md` |
| **Test type** | Agent — behavioural |

## Prompt

> We're building out our analytics capability and need a pipeline for user activity data. Our backend emits domain events to a Postgres event store (Marten) — things like `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`. We want to track retention (did the user come back 7 days after signup?), feature adoption (which features do users engage with in their first 30 days?), and funnel conversion from trial to paid. The events are immutable once written. Can you design the pipeline and data model?

## Criteria

- [x] PASS: Agent starts by identifying data sources, checking for existing metric definitions and infrastructure, and reviewing what events are already tracked — Pre-Flight Step 1 is MANDATORY and requires all three: check existing infrastructure, identify data sources, check existing metric definitions, review event tracking
- [x] PASS: Agent produces precise metric definitions before designing the pipeline — "Metric Definitions (MANDATORY before implementation)" requires all six fields (definition, calculation, data source, granularity, filters, time window, caveats, owner); work classification puts "Define precisely" as the first step for any new metric
- [x] PASS: Agent applies immutable event sourcing — no UPDATE/DELETE on event data — "Immutable events. Once written, event data doesn't change. Corrections are new events, not edits to old ones" is an explicit Data Modelling principle
- [x] PASS: Agent addresses data quality checks at every pipeline boundary — seven-check table (null, type, range, uniqueness, referential, freshness, volume) with "Where to implement" placement guidance; "Validate at ingestion" is a named rule
- [x] PASS: Agent documents data lineage from source through transformations to analytics layer — mandatory lineage format (source → ingestion → transformations → destination) with all required fields
- [x] PASS: Agent raises a decision checkpoint before choosing storage technology — Decision Checkpoints table lists "Choosing a new data storage technology" as a STOP trigger
- [~] PARTIAL: Agent includes privacy considerations — "Privacy by design" principle and validation checklist item present; Decision Checkpoint for adding PII; but no mandatory step requiring a structured PII audit (which properties contain PII, erasure key, retention period, deletion mechanism) as a pipeline deliverable
- [x] PASS: Agent produces a validation checklist covering lineage, privacy, property types, and sanity checks — Output Format section includes all four items explicitly
- [x] PASS: Agent distinguishes correlation from causation for retention metrics — dedicated "Event Correlation and Causation" section; "Default assumption: correlation, not causation" is explicit

**Criteria score: 8.5/9**

## Output expectations

- [x] PASS: Output names the four source events and traces each to the analytics use case — Pre-Flight requires reviewing what events are tracked, and metric definitions require naming the data source; the agent's workflow structurally surfaces all four events
- [~] PARTIAL: Output's retention metric defines exact 7-day window logic with boundary handling — the metric definition template requires a Time Window field, but the SQL example in the definition uses cohort-week grain (`cohort_week + INTERVAL '7 days' AND cohort_week + INTERVAL '14 days'`) rather than per-user T+7 boundary logic from individual signup timestamp; boundary handling (e.g. inclusive/exclusive at T+6d vs T+7d) is not structurally guaranteed
- [~] PARTIAL: Output's feature adoption metric specifies fixed 30-day cohort window, maps events to features, and defines de-duplication rule — the metric template covers time window and granularity; "Document what constitutes a 'unique' event (deduplication logic)" appears in Event Tracking Plans; but the specific "one count per user-feature" de-duplication framing is not structurally required, and the event-to-feature mapping depends on the agent applying prompt context rather than a workflow step
- [x] PASS: Output's funnel metric defines trial-to-paid conversion with start state, terminal state, exclusion rules, and time bounds — the metric definition template's calculation, filters, and time window fields cover these; funnel analysis is named as a pattern; the definition would drive this output
- [x] PASS: Output's data flow describes append-only semantics with no UPDATE/DELETE — "Immutable events" principle is explicit and applies to all pipeline stages; the lineage format mandates tracing source to destination
- [x] PASS: Output documents at least three quality checks at named pipeline stages — the seven-check table names null, type, range, uniqueness, referential, freshness, and volume checks, each with a named "Where to implement" stage
- [~] PARTIAL: Output addresses event versioning in the immutable Marten context — schema evolution guidance is present ("Additive changes are safe; breaking changes need migration plans") and a Decision Checkpoint covers changing event schemas; but the specific scenario of reading historical immutable events that predate a new property (forward compatibility, nullable handling) is not addressed
- [x] PASS: Output raises a decision checkpoint on analytics destination before committing — "Choosing a new data storage technology" is explicitly in the Decision Checkpoints table as STOP
- [~] PARTIAL: Output identifies PII and privacy implications including erasure handling — privacy principle and Decision Checkpoint for adding PII are present; but right-to-be-forgotten handling in an append-only immutable event store (a non-trivial problem) is not addressed in the definition
- [x] PASS: Output includes a sanity-check on retention causality — "Default assumption: correlation, not causation" is explicit; dedicated section documents three paths to establish causation; the agent would flag this structurally

**Output expectations score: 8.0/10**

## Notes

The definition is well-structured for this scenario. The mandatory Pre-Flight, metric definition template, immutability principle, and correlation/causation section all map directly to what the prompt requires.

The gaps are in precision and edge-case coverage rather than structural absence:

The retention window (criterion 2 in output expectations) is the clearest gap. The SQL example in the definition computes retention at cohort-week grain, not per-user T+7. A prompt asking for "did the user come back 7 days after signup" could produce either interpretation. A definition that explicitly covered the per-user T+7 window with boundary handling (is it day 7 exactly? a window around day 7?) would be unambiguous.

Event versioning in an immutable store is a genuinely hard problem the definition doesn't address. Marten's event store doesn't allow retroactive schema changes, so a new property on `report_created` only exists on events from the point it was added. Downstream projections and analytics queries have to handle both old and new shapes. The definition's "additive changes are safe" guidance is correct for mutable systems but incomplete for append-only stores where old events are fixed.

The privacy treatment (criteria 7 in both sections) is real but thin. The principle and checklist item are there, but the definition would benefit from a required PII audit step — a table enumerating which event properties are PII, what the erasure key is (user_id?), and what the deletion mechanism is. For JSONB payloads from a user-facing product, this isn't something to leave to the agent's judgment.

The de-duplication criterion for feature adoption (output expectation 3) reflects a genuine ambiguity: should a user who views the same dashboard 50 times count as "adopting" the dashboard feature 50 times, or once? The definition has deduplication guidance in Event Tracking Plans but doesn't require the metric definition to specify a de-duplication rule. Requiring a "Deduplication" field alongside the other metric definition fields would close this.
