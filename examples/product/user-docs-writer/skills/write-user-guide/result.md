# Output: Write user guide

**Verdict:** PARTIAL
**Score:** 12.5/17 criteria met (74%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires a research step — Step 1 explicitly requires searching the codebase for UI components, routes, handlers, permissions, and existing docs before writing.
- [x] PASS: Skill produces numbered steps for procedural tasks — Step 3 mandates numbered steps; the format template shows numbered sub-steps within each section.
- [x] PASS: Each step includes what the user should see after completing it — Step 3 rules require "**Expected result:**" for every step.
- [x] PASS: Skill requires a troubleshooting section covering the most common problems — Step 4 mandates a Troubleshooting section with 3+ entries including common errors, mistakes, and environment differences.
- [x] PASS: Skill uses only product terminology — Rules section explicitly prohibits developer language and references matching UI vocabulary.
- [x] PASS: Skill requires related content links at the end — Step 5 mandates a "Related guides" section.
- [x] PASS: Skill requires role-based or permissions context — Step 1 research explicitly includes finding permissions/roles; the header template has **Required role:** and **Required plan:** as required standard documentation elements.
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter includes all three fields.

### Output expectations

- [ ] FAIL: Output covers the three named time-tracking capabilities as distinct task sections — the skill's structure would likely produce sections, but nothing in the skill definition guarantees three distinct sections for each named capability when given this prompt.
- [ ] FAIL: Output's "log time" section walks through both timer-based and retrospective logging flows — the skill's research step requires identifying "most common user tasks" but doesn't mandate covering multiple flows for the same action.
- [ ] FAIL: Output's "set estimates" section explains WHY estimates feed into reports and covers project vs task estimates — the skill says to explain "why, if not obvious" in steps but cannot derive this domain-specific content without product knowledge.
- [ ] FAIL: Output's "utilisation reports" section explains how to read the report and what utilisation % means — the skill produces steps and expected results but doesn't ensure conceptual explanations are embedded when needed for feature-specific literacy.
- [x] PASS: Output's steps are numbered with explicit expected results — Step 3 format mandates exactly this, including the "**Expected result:**" field with descriptive content after each step group.
- [~] PARTIAL: Output's troubleshooting covers common time-tracking problems — Step 4 mandates troubleshooting with 3+ entries covering errors, mistakes, and environment differences. The structure is right but the skill cannot guarantee coverage of these specific scenarios (browser-close data loss, locked entries, month-boundary edge cases). Partially met: structure guaranteed, scenario depth not.
- [x] PASS: Output uses product terminology consistently without jargon — the skill's rules section enforces this and forbids internal technical terms.
- [~] PARTIAL: Output addresses role/permissions explicitly at the task level — the skill requires a **Required role:** header and permissions research, but doesn't mandate inline per-action permission notes (e.g., "only project leads can edit another user's entry" within the relevant step). Header-level gating is guaranteed; step-level permissions are not.
- [ ] FAIL: Output's related-content links cover adjacent features — the skill requires a Related guides section but the specific adjacent features for time tracking are not derivable from the skill definition without domain knowledge.
- [~] PARTIAL: Output addresses mobile time entry if the product supports it — the skill mentions mobile vs desktop in troubleshooting context only. Mobile as a primary workflow variant is not guaranteed.

## Notes

The skill definition is structurally strong. The first eight criteria (structural checks) all pass cleanly. The gaps are entirely in the output expectations section, which tests scenario-specific depth that a generic skill definition cannot encode. The skill's research step is the intended mechanism for surfacing domain knowledge, but whether the output agent would derive timer-based vs retrospective flows, project vs task estimate hierarchies, or utilisation % explanations depends on what the codebase research surfaces — not on the skill definition itself. The output expectations are written as if evaluating a live execution against a real product, not a structural evaluation of a skill definition.

The previous evaluation (2026-04-16) only scored the Criteria section (7.5/8, 94%). This evaluation scores both sections as required: 12.5/17 (74%), yielding a PARTIAL verdict.
