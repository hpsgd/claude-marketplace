# Result: decompose-initiative

**Verdict:** PARTIAL
**Score:** 15/17 criteria met (88%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Completes Step 1 (initiative context table) — Step 1 mandates a five-field table (User problem, Target user, Success criteria, Appetite, Constraints) with explicit "Output: Completed initiative context table."
- [x] PASS: Assesses workstream relevance for both CPO and CTO teams — Step 2 requires a "Relevant?" column with Yes/No reasoning for every row in both team tables; rule states "include only what's relevant" and requires reasoning for exclusions.
- [x] PASS: Dependency map showing what blocks what — Step 3 mandates a four-column table; template explicitly shows Design and Architecture depending on Product requirements.
- [x] PASS: Phased execution sequence with named gates — Step 4 requires a "Gate to next phase" column; Rules section states "'Move on when ready' is not a gate."
- [x] PASS: Critical path and parallel opportunities identified explicitly — Step 4 output template includes both "Critical path" and "Parallel opportunities" as required subsections.
- [x] PASS: Summary table with owner roles, dependencies, key deliverables, phase, and effort estimates as ranges — Step 5 mandates a six-column table; all required columns are present.
- [x] PASS: Effort estimates are ranges, not point estimates — Rules section explicitly states "'2 weeks' is a guess. '1–3 weeks, depending on API complexity' is an estimate."
- [~] PARTIAL: Follow-up actions pointing to related skills — Output Format template includes `/coordinator:define-okrs` explicitly but does not reference `/coordinator:write-spec` by name. "Create detailed specs for each workstream" is present as unrouted text. Score: 0.5.
- [x] PASS: Does not include GTM, support prep, or formal UX research without warrant — Rule "Not every workstream applies to every initiative — and state WHY you excluded the rest" combined with required Yes/No reasoning enforces selective inclusion.

### Output expectations

- [x] PASS: Initiative context table reproduces prompt facts — Step 1 uses `$ARGUMENTS` and the table fields would capture Notification Centre, Taskwave, the three notification types, medium scope, and 6-week appetite directly from the invocation.
- [x] PASS: Workstreams include relevant ones and exclude GTM/support/research — Step 2 covers Design, Architecture, and Development (with `[developer role]` placeholder that would be populated specifically), QA is present. The required exclusion reasoning handles GTM, Support, Research for an internal feature.
- [~] PARTIAL: Dependency map shows architect and UX feeding developer implementation AND backend event-source work preceding frontend subscriptions — the template captures the former (Development depends on Design and Architecture) but does not explicitly model the frontend/backend split within development or the per-notification-type event-source dependency. Score: 0.5.
- [x] PASS: Phased execution sequence has named gates — the template shows "Gate to next phase" column with examples like "PRD approved, system design reviewed."
- [x] PASS: Critical path identifies real-time delivery mechanism decision as the blocking item — Step 4's "Critical path" subsection would capture this; the architecture workstream (real-time delivery: WebSockets vs polling) is the first blocker, and the "Parallel opportunities" subsection would capture UI mockups proceeding concurrently.
- [x] PASS: Summary table has all required columns — owner role, dependencies, key deliverables, phase, and effort estimate as ranges are all present in the Step 5 template.
- [~] PARTIAL: Effort estimates fit within 6-week appetite with reasoning shown — the "Timeline estimate" section (best case, likely case, risk factors) addresses this, but the skill does not explicitly verify that the critical path total is ≤6 weeks or flag when it is not. Score: 0.5.
- [~] PARTIAL: Follow-up actions include both write-spec and define-okrs — `/coordinator:define-okrs` is explicit in the Output Format and Related Skills; `/coordinator:write-spec` is not referenced by name. Score: 0.5.
- [~] PARTIAL: Output addresses user-actionable nature of notifications (passive read vs active act interactions) — the skill's template does not prompt for interaction mode analysis; a decomposition from this definition would likely produce notification delivery design without explicitly distinguishing passive (read) from active (mark done, snooze, assign) interactions. Score: 0.5.

## Notes

The skill is well-structured and covers the core decomposition process tightly. Three gaps account for the partial verdict. First, `/coordinator:write-spec` is missing from the follow-up actions despite being the natural next step after decomposition — define-okrs is there but specs are not routed through a named skill. Second, the dependency template doesn't model intra-development dependencies (backend event sources before frontend subscriptions), which matters for a feature like Notification Centre where the backend pipeline must exist before the frontend can subscribe. Third, the skill doesn't prompt for interaction mode analysis — for a feature explicitly described as one where users "act on" notifications, the decomposition should flag passive vs active interaction design as a distinct concern for the UX workstream.
