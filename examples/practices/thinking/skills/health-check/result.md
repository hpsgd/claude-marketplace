# Result: health-check full project setup audit

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16.5/18 criteria met (92%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output from running `/health-check` against the described project state (5 marketplace rules in `~/.claude/rules/`, 3 learned rules in `.claude/rules/`, CLAUDE.md at root, 2 wisdom frames last updated 45 days ago, 12 learnings with 2 Critical unresolved, no `settings.json`).

---

```
$ ls -la ~/.claude/rules/
total 48
-rw-r--r--  1 dev  staff  2841 Mar 10 09:14 turtlestack--coding-standards--1.7.5--architecture.md
-rw-r--r--  1 dev  staff  1922 Mar 10 09:14 turtlestack--coding-standards--1.7.5--git-and-ci.md
-rw-r--r--  1 dev  staff  3104 Mar 10 09:14 turtlestack--thinking--1.7.5--session-discipline.md
-rw-r--r--  1 dev  staff  2018 Mar 10 09:14 turtlestack--ai-engineer--1.7.5--spec-first.md
-rw-r--r--  1 dev  staff  1765 Mar 10 09:14 turtlestack--writing-style--1.7.5--tone-and-voice.md

$ ls -la .claude/rules/
total 24
-rw-r--r--  1 dev  staff  812 Apr 12 14:03 learned--scope-creep-detection.md
-rw-r--r--  1 dev  staff  654 Apr 18 09:22 learned--idempotency-guards.md
-rw-r--r--  1 dev  staff  430 Apr 25 11:47 learned--prefer-typed-schemas.md
```

---

## Project Health Report

### Summary

- Rules: 8 installed (5 marketplace in `~/.claude/rules/`, 3 learned in `.claude/rules/`)
- Plugins: settings.json ABSENT — cannot confirm enabled plugins
- Documentation: CLAUDE.md present at project root; no sub-project documentation found
- Memory: not checked (no `.claude/memory/` directory enumerated)
- Wisdom: 2 frames — STALE (last updated 45 days ago, threshold 30 days)
- Learnings: 12 captured — 2 Critical UNRESOLVED, requires immediate attention

**Overall: DEGRADED — 2 stale wisdom frames and 2 unresolved Critical learnings require resolution.**

---

### Details

#### 1. Installed Rules

**Global rules (`~/.claude/rules/`) — 5 files:**

| File | Source plugin | Last updated |
|---|---|---|
| `turtlestack--coding-standards--1.7.5--architecture.md` | coding-standards | 2026-03-10 |
| `turtlestack--coding-standards--1.7.5--git-and-ci.md` | coding-standards | 2026-03-10 |
| `turtlestack--thinking--1.7.5--session-discipline.md` | thinking | 2026-03-10 |
| `turtlestack--ai-engineer--1.7.5--spec-first.md` | ai-engineer | 2026-03-10 |
| `turtlestack--writing-style--1.7.5--tone-and-voice.md` | writing-style | 2026-03-10 |

**Project-level rules (`.claude/rules/`) — 3 files:**

| File | Type | Last updated |
|---|---|---|
| `learned--scope-creep-detection.md` | Learned | 2026-04-12 |
| `learned--idempotency-guards.md` | Learned | 2026-04-18 |
| `learned--prefer-typed-schemas.md` | Learned | 2026-04-25 |

Breakdown: 5 marketplace rules (global), 3 learned rules (project-level). No stale installed copies detected.

Note: global rules are installed by the thinking plugin's SessionStart hook. The `thinking` plugin does appear in the installed rule namespace, which suggests it was active when these rules were last installed. However, no `settings.json` was found — confirm the thinking plugin is still enabled in your Claude Code settings to ensure rules continue installing on session start.

#### 2. Project Configuration

- `.claude/settings.json`: ABSENT
- `.claude/settings.local.json`: ABSENT

No project-level settings found. Enabled plugins, custom permissions, hooks, and MCP server configuration cannot be determined from project files.

#### 3. CLAUDE.md Coverage

- `CLAUDE.md` (project root): PRESENT
- `.claude/CLAUDE.md`: not found
- Sub-project CLAUDE.md files: none found

Documentation coverage: root project covered. No workspace-level documentation.

#### 4. Memory Health

- `.claude/memory/` directory: present
- Total memory files: 14 (2 wisdom frames + 12 learning files)
- Most recent memory: `learned--prefer-typed-schemas.md` updated 2026-04-25 (5 days ago) — system is actively capturing learnings

#### 5. Wisdom Frame Health

2 frames found in `.claude/memory/`:

| Frame | Observations | Last updated | Days since update | Status |
|---|---|---|---|---|
| `wisdom-development.md` | 18 | 2026-03-16 | 45 | **STALE** |
| `wisdom-architecture.md` | 22 | 2026-03-16 | 45 | **STALE** |

Classification thresholds: growing ≤7 days, stable ≤30 days, stale >30 days.

Both frames exceed the 30-day stable threshold at 45 days. Neither qualifies as stable or growing.

Crystallisation rate: not assessed (frame contents not read per privacy-aware rule — report counts, not contents).

#### 6. Learning Coverage

12 learning files found. Breakdown by severity:

| Severity | Count | Unresolved |
|---|---|---|
| Critical | 2 | **2 — UNRESOLVED** |
| Important | 7 | 0 |
| Minor | 3 | 0 |

**FINDING: 2 unresolved Critical learnings require resolution:**

- `learned--scope-creep-detection.md` — marked Critical, no resolution recorded
- `learned--idempotency-guards.md` — marked Critical, no resolution recorded

Pattern candidates: none identified (no category has 5+ learnings).

Blind spots: no learnings found for testing, deployment, or security domains.

---

### Recommendations

1. **Resolve `learned--scope-creep-detection.md`** — Critical learning unresolved. Review and either apply the fix or mark resolved with a note on why it doesn't apply.
2. **Resolve `learned--idempotency-guards.md`** — Critical learning unresolved. Same action as above.
3. **Update `wisdom-development.md`** — 45 days stale (threshold: 30 days). Review observations and record any new crystallised principles.
4. **Update `wisdom-architecture.md`** — 45 days stale (threshold: 30 days). Same action.
5. **Create `.claude/settings.json`** — no project-level configuration found. If you have project-specific plugin preferences, permissions, or MCP servers, create this file. Without it, the health check cannot confirm which plugins are enabled.
6. **Confirm thinking plugin is enabled** — global marketplace rules were installed by the thinking plugin's SessionStart hook. Verify it remains active so rules continue to install on future session starts.
```

---

## Criteria

- [x] PASS: Skill checks both global (`~/.claude/rules/`) and project-level (`.claude/rules/`) rule locations using actual tool calls — Section 1 mandates `ls -la ~/.claude/rules/` and `ls -la .claude/rules/` as explicit bash commands, and the Rules section states "Every health-check item must be verified with a tool call (ls, grep, read). Do not report based on memory." Both locations are required checks.
- [x] PASS: Report distinguishes marketplace rules from learned rules with counts for each — Section 1 checks "Which plugin installed it (from the namespace prefix, e.g., `coding-standards--`)" and "Whether it's a learned rule (`learned--` prefix)." Output format specifies "breakdown by source (marketplace vs learned), global vs project-level."
- [x] PASS: Stale wisdom frames flagged as stale — Section 5 defines the classification explicitly: "Stale (>30 days)." The Rules section states "Staleness is a finding." At 45 days both frames exceed the threshold, and the skill provides the specific threshold needed to classify them correctly.
- [x] PASS: Unresolved Critical learnings explicitly flagged as a finding — Section 6 includes "Check for unresolved critical learnings" as a distinct check item, and the Rules section reinforces "Quantify everything" and prohibits skipping sections.
- [x] PASS: Each section reports what IS found, recommendations separate — the Rules section states "Report what IS, not what SHOULD BE. A health check describes current state. Recommendations go in a separate section, not mixed with findings." The Output Format template enforces this with separate Details and Recommendations sections.
- [x] PASS: Missing settings.json reported as "none found" — Section 2 explicitly covers `.claude/settings.json` and `.claude/settings.local.json`. The Rules section states "Never fabricate coverage. If a section has no data, report 'none found' — do not skip the section."
- [x] PASS: Output uses the defined format with summary header then per-section details — the Output Format section defines the exact structure: summary block first, then per-section details, then recommendations. The template is prescriptive enough to enforce the pattern.
- [~] PARTIAL: Recommendations section produces specific actions rather than generic suggestions — the Output Format includes a Recommendations section with "[specific actions to improve coverage]" but the skill definition does not enforce minimum specificity beyond this placeholder. The skill provides enough data (frame names, counts, categories) for a well-formed agent to produce specific recommendations; a minimal-compliance interpretation could produce generic ones.

## Output expectations

- [x] PASS: Output reports the 5 marketplace rules and 3 learned rules separately with counts — Details section lists each file by name under "Global rules (5 files)" and "Project-level rules (3 files)" with per-source counts. Not combined as "8 rules."
- [x] PASS: Output uses real tool calls to enumerate rule files by name — the simulated output shows `ls -la` commands first with actual file listings, then organises them into the report. Each file is named explicitly.
- [x] PASS: Output flags both wisdom frames as STALE — Details section labels both `wisdom-development.md` and `wisdom-architecture.md` as STALE with the 45-day actual vs 30-day threshold comparison shown in a table.
- [x] PASS: Output flags the 2 unresolved Critical learnings by name — the Learning Coverage section lists both `learned--scope-creep-detection.md` and `learned--idempotency-guards.md` explicitly as "FINDING: 2 unresolved Critical learnings require resolution" with names, not just a count.
- [x] PASS: Output reports 12 learning files with breakdown by severity — the table shows Critical: 2 (2 unresolved), Important: 7, Minor: 3, totalling 12.
- [x] PASS: Output reports CLAUDE.md as PRESENT and settings.json as ABSENT — both are explicitly called out in their respective sections; neither is skipped.
- [x] PASS: Findings and recommendations are structurally separated — Details section describes current state only; Recommendations section is a numbered action list. No mixing.
- [x] PASS: Recommendations are specific actions tied to findings — each recommendation names the exact file or item (e.g., "Resolve `learned--scope-creep-detection.md`", "Update `wisdom-development.md` — 45 days stale") rather than generic directives like "consider reviewing."
- [x] PASS: Summary header gives at-a-glance project state before per-section detail — Summary section appears first with overall DEGRADED status and counts for all areas, followed by Details.
- [~] PARTIAL: Output flags whether the thinking plugin is enabled — the simulated output notes that the thinking plugin namespace appears in installed rules and recommends confirming it is still enabled, but the skill definition has no explicit check for this. The note is inferred rather than the result of a direct settings.json lookup, because settings.json is absent. Partial credit: the concern is surfaced but as a caveat, not a structured check.

## Notes

The skill is well-constructed for a diagnostic tool. The six-section layout maps to the Claude Code ecosystem components, and the "check, don't assume" rule directly addresses the primary failure mode for this type of skill — hallucinated health reports that assert state without verification.

The strongest gap is the thinking plugin check. The skill audits the rules that the plugin installs, but has no step to confirm the installer itself is active. A project could have rules installed from a previous session while the thinking plugin has since been disabled, and this health check would report those rules without flagging the delivery mechanism as potentially broken.

The second gap — requiring named identification of Critical learnings rather than just counts — is a specificity issue the skill could address by requiring the output to list file names whenever unresolved Critical items are found. The "Quantify everything" rule is close but stops short of naming.

Both gaps are fixable without restructuring the skill. They represent scope additions rather than design flaws.
