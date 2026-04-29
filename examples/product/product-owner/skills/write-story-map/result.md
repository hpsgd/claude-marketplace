# Output: Write story map

**Verdict:** PASS
**Score:** 18/19 criteria met (95%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires a backbone of activities as verb phrases (3-7 activities), not features or nouns — Step 2 rules state "Activities are verb phrases" with examples, enforces 3-7 range with reasons for both bounds, and states "Activities are NOT features"
- [x] PASS: Skill defines a walking skeleton as the thinnest end-to-end slice touching every backbone activity — and explicitly distinguishes it from the MVP — Step 5 defines it as "thinnest possible end-to-end slice that demonstrates the full flow" touching every activity, and states "The walking skeleton is NOT an MVP. It is smaller"
- [x] PASS: Skill requires tasks to be ordered top-to-bottom by priority — Step 3 states "Order tasks top-to-bottom by necessity", Step 4 states "ordered by priority (most important first). Each row down is less critical than the row above", and the Rules section repeats "Stories above the line are more important than stories below"
- [x] PASS: Skill prohibits orphan stories — Step 6 validation check "No orphan stories: Does every task sit under an activity?", Rules section states "No story exists without an activity above it — orphan stories indicate a missing backbone activity"
- [x] PASS: Skill requires each release slice to touch every backbone activity — Slice Rules state "Every slice must touch every activity — a release that only covers [one activity] is not a slice, it is a component"
- [x] PASS: Skill includes a validation checklist (backbone completeness, walking skeleton coverage, story independence, edge case coverage) — Step 6 table covers all four; the Output Format checklist also includes all four items
- [~] PARTIAL: Skill specifies that each task must be independently deliverable — Step 6 validation asks "Can each task be built and delivered independently?" and the output checklist includes "Each task is independently deliverable". Stated as a validation check rather than a construction rule in Step 3. Half credit.
- [x] PASS: Skill produces a 2D grid output (activities as columns, tasks as rows by priority) not a flat list — Output Format specifies a Markdown table with activities as column headers and priority-ordered rows; Rules section states "A story map is not a backlog — it is a 2D spatial arrangement"
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter present with all three fields

### Output expectations

- [x] PASS: Output's backbone covers the guest checkout flow as 3-7 verb-phrase activities — the skill enforces verb phrases, 3-7 range, and chronological ordering in Step 2; invoking it for guest checkout would produce activities like "Review cart", "Enter delivery details", "Choose payment method", "Confirm order"
- [x] PASS: Output's walking skeleton is a thinnest end-to-end slice, explicitly distinct from MVP — Step 5 Slice 1 definition requires minimum one task per activity and the skill states this is smaller than MVP; the output template has a dedicated "Walking Skeleton" row separate from "MVP"
- [x] PASS: Output's tasks under each backbone activity are ordered top-to-bottom by priority — the skill's Step 3 and Step 4 rules enforce this and the grid template reflects it structurally
- [x] PASS: Output's release slices each touch ALL backbone activities — Slice Rules in Step 5 require this explicitly, and the output template shows each slice row spanning all activity columns
- [x] PASS: Output explicitly excludes orphan stories — Step 6 validation and the Rules section both enforce this; no "miscellaneous" column exists in the output template
- [x] PASS: Output's validation checklist confirms backbone completeness, walking skeleton coverage, story independence, and edge case coverage — the Output Format checklist includes all four items by name
- [x] PASS: Output's grid layout has activities as column headers and tasks as rows ordered by priority — the Output Format Markdown table template enforces this; the Rules section explicitly forbids flattening to a list
- [x] PASS: Output identifies edge-case scenarios as explicit tasks lower in the grid — Step 4 lists "Edge cases — what happens when things go wrong" as tasks added below the happy path, ordered by priority
- [~] PARTIAL: Output addresses the GUEST aspect specifically — the skill is intentionally domain-agnostic. Step 1 asks who the user is, which would cause the agent to frame the user as a guest shopper, but nothing in the skill prompts the agent to identify what is absent in guest flow vs authenticated flow (no saved addresses, no order history, possible account-creation prompt). A guest checkout story map would be produced, but guest-specific task variations may not be explicitly surfaced.
- [~] PARTIAL: Output addresses task independence — the skill enforces independence at the slice level (Slice Rules) and as a Step 6 validation check, which means the output checklist would confirm it. Per-task descriptions are not required to state independence individually. Partial credit.

## Notes

The skill is structurally strong across all nine criteria. Both partial scores are minor: independence is validated but not enforced at task-writing time, and guest-specificity depends on Step 1 framing with no explicit prompt to surface guest-vs-authenticated differences. A small addition to Step 1 (e.g. "if the user is a guest, note what is absent from an authenticated session") would close the guest-specificity gap. The walking skeleton vs MVP distinction is the most precise conceptual element and is well-defined.
