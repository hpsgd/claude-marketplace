# Result: health-check full project setup audit

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16/18 criteria met (89%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill checks both global (`~/.claude/rules/`) and project-level (`.claude/rules/`) rule locations using actual tool calls — Section 1 mandates `ls -la ~/.claude/rules/` and `ls -la .claude/rules/` as explicit bash commands, and the Rules section states "Every health-check item must be verified with a tool call (ls, grep, read). Do not report based on memory." Both locations are required checks.
- [x] PASS: Report distinguishes marketplace rules from learned rules with counts for each — Section 1 checks "Which plugin installed it (from the namespace prefix, e.g., `coding-standards--`)" and "Whether it's a learned rule (`learned--` prefix)." The output format specifies "breakdown by source (marketplace vs learned), global vs project-level."
- [x] PASS: Stale wisdom frames flagged as stale — Section 5 defines the classification explicitly: "Stale (>30 days)." The Rules section states "Staleness is a finding." At 45 days both frames exceed the threshold, and the skill provides the specific threshold needed to classify them correctly.
- [x] PASS: Unresolved Critical learnings explicitly flagged as a finding — Section 6 includes "Check for unresolved critical learnings" as a distinct check item. The Rules section reinforces: "Never fabricate coverage... report 'none found' — do not skip the section."
- [x] PASS: Each section reports what IS found, recommendations separate — the Rules section states "Report what IS, not what SHOULD BE. A health check describes current state. Recommendations go in a separate section, not mixed with findings." The Output Format template enforces this with separate Details and Recommendations sections.
- [x] PASS: Missing settings.json reported as "none found" — Section 2 explicitly covers `.claude/settings.json` and `.claude/settings.local.json`. The Rules section states "Never fabricate coverage. If a section has no data, report 'none found' — do not skip the section."
- [x] PASS: Output uses the defined format with summary header then per-section details — the Output Format section defines the exact structure: summary block first, then per-section details, then recommendations. The template is prescriptive enough to enforce the pattern.
- [~] PARTIAL: Recommendations section produces specific actions rather than generic suggestions — the Output Format includes a Recommendations section with "[specific actions to improve coverage]" but the skill definition does not enforce minimum specificity beyond this placeholder. The skill provides the data needed (frame names, counts, categories) but does not require specificity by rule.

### Output expectations

- [x] PASS: Skill output would report the 5 marketplace rules and 3 learned rules separately — Section 1 requires breakdown "by source (marketplace vs learned), global vs project-level" with counts for each, not a combined total.
- [x] PASS: Skill mandates real tool calls to enumerate files by name — the Rules section opens with "Every health-check item must be verified with a tool call (ls, grep, read). Do not report based on memory." The skill includes the explicit bash commands needed.
- [x] PASS: Skill would flag both wisdom frames as STALE — Section 5 classifies frames as "stale (>30 days)" and the Rules section states "Staleness is a finding." At 45 days, both frames exceed the threshold and would be marked STALE, not just listed as present.
- [ ] FAIL: Skill does not require naming the unresolved Critical learnings — Section 6 says "Check for unresolved critical learnings" but does not require the skill to name each critical learning individually. The output format specifies counts and severity breakdown but not file-level identification of named items.
- [x] PASS: Skill would report the 12 learning files with a breakdown by severity — Section 6 states "Count by severity (critical, important, minor)" and "Quantify everything" is a hard rule.
- [x] PASS: CLAUDE.md presence and settings.json absence both covered — Section 3 checks for `CLAUDE.md` existence and Section 2 checks for `settings.json`. The Rules section explicitly prohibits skipping sections with no data.
- [x] PASS: Findings and recommendations are structurally separated — the Output Format template separates `### Details` from `### Recommendations` and the Rules section states findings describe current state, recommendations go in a separate section.
- [~] PARTIAL: Recommendations are specific actions tied to findings — the skill provides enough data (frame names, counts, critical learning categories) to produce specific recommendations, but the definition only says "[specific actions to improve coverage]" without mandating specificity. A well-formed agent would produce specific recommendations; a minimal one could produce generic ones.
- [x] PASS: Summary header gives at-a-glance state before per-section detail — the Output Format template places the `### Summary` block before `### Details`, listing counts for rules, plugins, documentation, memory, wisdom, and learnings.
- [ ] FAIL: Skill does not address whether the thinking plugin is enabled — none of the six sections check for the thinking plugin's status. The skill checks installed rules and project configuration but has no step for verifying whether the rule installer (thinking plugin) is active.

## Notes

The skill is well-constructed for a diagnostic tool. The six-section layout maps clearly to the Claude Code ecosystem components. The strongest design decision is requiring tool calls for every check — this directly prevents hallucinated health reports, the primary failure mode for a skill of this type.

Two genuine gaps: first, the skill identifies unresolved Critical learnings by count but does not require naming them. The test expects named identification ("resolve 2 Critical learnings: `<name1>`, `<name2>`"), which is necessary for actionable follow-through. Second, the skill has no mechanism to detect whether the thinking plugin is active — a silent failure mode where marketplace rules appear installed in `~/.claude/rules/` but are not reaching the project. This is a real operational blind spot the health check should cover.

The wisdom frame thresholds (growing ≤7 days, stable ≤30 days, stale >30 days) are well-defined with specific numeric boundaries, which is the right design approach.
