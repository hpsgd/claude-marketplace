# Health Check

Scenario: A developer joins a new project and wants to understand the current state of the Claude Code setup — what rules are installed, which plugins are active, and whether the memory system is healthy.

## Prompt

> /health-check
> 
> (Running in a project that has: 5 marketplace rules installed in ~/.claude/rules/, 3 learned rules in .claude/rules/, a CLAUDE.md at the project root, 2 wisdom frames in .claude/memory/ last updated 45 days ago, 12 learning files with 2 marked Critical and unresolved, and no project-level settings.json.)

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I now have enough data. Here's the full health report:

---

## Project Health Report

### Summary

| Area | Status |
|------|--------|
| Rules | 7 installed (0 marketplace, 7 learned) — global only |
| Plugins | 8 enabled globally |
| Documentation | **None** — no CLAUDE.md, no .claude/ directory |
| Memory | Empty — directory exists, 0 files |
| Wisdom frames | None found |
| Learnings | 0 captured in session directories |

---

### 1. Rules

**Global (`~/.claude/rules/`) — 7 files, all learned:**

| Rule | Last Updated | Age |
|------|-------------|-----|
| `learned--confirm-before-launching-agents.md` | Apr 16 | 15 days |
| `learned--dont-minimise-scope.md` | Apr 3 | 28 days |
| `learned--dont-rewrite-personal-voice.md` | Apr 16 | 15 days |
| `learned--es-mindset-review.md` | Apr 4 | 27 days |
| `learned--evaluate-platforms-as-package.md` | Apr 4 | 27 days |
| `learned--flag-paid-services.md` | Apr 16 | 15 days |
| `learned--justify-numeric-thresholds.md` | Apr 3 | 28 days |

**Project-level (`.claude/rules/`) — none.** No `.claude/` directory exists in this project.

**Staleness:** All rules are 15–28 days old. No marketplace-namespaced rules (e.g., `coding-standards--`, `thinking--`) are installed despite 8 marketplace plugins being enabled. This is expected — marketplace plugins deliver skills, not rules, unless explicitly configured to push rules.

---

### 2. Project Configuration

**Project settings:** None — no `.claude/settings.json` or `.claude/settings.local.json`.

**Global settings (`~/.claude/settings.json`):**
- **8 plugins enabled:** `ai-engineer`, `coding-standards`, `python-stack`, `security-compliance`, `thinking`, `tooling`, `workflow-tools`, `writing-style` (all from `turtlestack` marketplace)
- **3 extra marketplaces registered:** `caveman`, `tortoisestack`, `turtlestack`
- **Hooks configured:** `claudebar` hooks on 6 events (SessionStart, SessionEnd, Stop, SubagentStart, SubagentStop, TaskCompleted) — all route to localhost claudebar service
- **Permissions:** Broad allow (`Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `NotebookEdit`, `Skill`, `mcp__*`); explicit deny list covers destructive operations and credential reads
- **MCP servers:** None found
- **Advisor model:** `opus`
- **Status line:** `npx -y ccstatusline@latest`

---

### 3. CLAUDE.md Coverage

- **Root `CLAUDE.md`:** Not found
- **`.claude/CLAUDE.md`:** Not found (`.claude/` directory doesn't exist)
- **Sub-project docs:** Only file found is `README.md`
- **Project-specific rules:** None

This project has no Claude Code documentation at all. Any agent working here has no context about conventions, architecture, or tooling.

---

### 4. Memory Health

- **Project memory directory:** Exists at `~/.claude/projects/.../memory/` but contains **0 files**
- **Global memory:** No `~/.claude/memory/` directory
- **MEMORY.md:** Not present
- **Freshness:** N/A — system has never written a memory for this project

---

### 5. Wisdom Frame Health

- **Frames found:** None

No wisdom frames exist globally or at project level.

---

### 6. Learning Coverage

- **Session learning files:** 0 (learnings directory is empty)
- **Critical unresolved:** 0 found (directory empty)
- **Patterns:** None to report

---

### Recommendations

**High priority:**
1. **Create a `CLAUDE.md`** — this project has zero context for agents. Run `/init` to bootstrap one. Without it, every session starts cold.
2. **Add project settings** — create `.claude/settings.json` to pin plugin configuration at the project level rather than relying solely on global settings.

**Medium priority:**

3. **Bootstrap memory** — the memory directory exists but is empty. After any substantive session, run `/learning` to capture decisions made. With 7 global learned rules already accumulated, project-level learnings would complement them.
4. **Evaluate wisdom frames** — 8 plugins enabled but no wisdom frames exist. If recurring architectural patterns emerge in this project, run `/wisdom` to crystallise them.

**Low priority:**

5. **Review global rule freshness** — oldest rules are 28 days old (Apr 3). Cross-check against the `thinking:reconcile-rules` skill to verify none have been superseded by upstream plugin updates.
6. **Confirm claudebar is running** — 6 hooks all depend on a localhost claudebar service. If it's not running, hooks fail silently.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 7.0/17.0 (41%) |
| Evaluated | 2026-05-01 |
| Target duration | 88244 ms |
| Target cost | $0.1751 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill checks both global (`~/.claude/rules/`) and project-level (`.claude/rules/`) rule locations using actual tool calls, not assumptions | FAIL | Output mentions both locations but reports `~/.claude/rules/` with 7 rules and `.claude/rules/` as non-existent ('No `.claude/` directory exists in this project'). The test scenario states 3 learned rules ARE in `.claude/rules/`. The wrong result for the project-level location indicates the tool calls either were not made or returned incorrect data for that path. |
| c2 | Report distinguishes marketplace rules from learned rules with counts for each | PARTIAL | Summary table shows '7 installed (0 marketplace, 7 learned)' — the structure correctly distinguishes both types with counts. However, the counts are wrong vs. the test scenario (5 marketplace + 3 learned = 8 total). The distinction mechanism is present but the data is incorrect. |
| c3 | Stale wisdom frames (last updated 45 days ago, exceeding the 30-day stable threshold) are flagged as stale — not reported as stable | FAIL | Section 5 reads: 'Frames found: None' and summary table shows 'Wisdom frames \| None found'. The 2 wisdom frames described in the test scenario are completely absent from the output — not flagged as stale, not listed as present, not mentioned at all. |
| c4 | Unresolved Critical learnings are explicitly flagged as a finding, not just counted | FAIL | Section 6 states: 'Critical unresolved: 0 found (directory empty)' and 'Session learning files: 0'. The 2 unresolved Critical learnings from the test scenario are not found, not flagged, and not named. Completely absent. |
| c5 | Each section reports what IS found, not what should be — recommendations go in a separate section | PASS | Sections 1–6 each describe observed state (e.g., 'Global (~/.claude/rules/) — 7 files', 'Project settings: None', 'Frames found: None'). A separate final 'Recommendations' section is clearly delineated with its own header and numbered items. |
| c6 | Missing project-level settings.json is reported as "none found" — section is not skipped | PASS | Summary table row: 'Project Configuration \| None — no `.claude/settings.json` or `.claude/settings.local.json`'. Section 2 repeats: 'Project settings: None — no `.claude/settings.json` or `.claude/settings.local.json`'. Not skipped. |
| c7 | Report uses the defined output format with a summary header then per-section details | PASS | Output opens with '## Project Health Report' followed by a '### Summary' table with 6 area rows, then numbered sections '### 1. Rules' through '### 6. Learning Coverage', then '### Recommendations'. Clear summary-then-detail structure. |
| c8 | Recommendations section produces specific actions (e.g., "update wisdom-development frame" or "resolve 2 Critical learnings") rather than generic suggestions | PARTIAL | Some recommendations are actionable: 'Run `/init` to bootstrap one', 'create `.claude/settings.json`', 'run `/learning`', 'run `thinking:reconcile-rules` skill'. However they are not tied to the actual test-scenario findings (no mention of updating specific wisdom frames or resolving named Critical learnings), so the specificity is generic rather than finding-driven. |
| c9 | Output reports the 5 marketplace rules in `~/.claude/rules/` and the 3 learned rules in `.claude/rules/` separately with their counts — not a single combined "8 rules" total | FAIL | Output reports only 7 global rules, all learned, and explicitly states no project-level `.claude/` directory. Neither the 5 marketplace rules in `~/.claude/rules/` nor the 3 learned rules in `.claude/rules/` appear anywhere in the output. The required two-bucket separation is absent. |
| c10 | Output uses real tool calls (Glob / ls) to enumerate the rule files and lists each by name — not asserting counts without evidence | PARTIAL | Section 1 lists 7 rule files by name with last-updated dates (e.g., `learned--confirm-before-launching-agents.md \| Apr 16 \| 15 days`). Files are individually named, not just counted. However the enumeration is incomplete — the 5 marketplace rules and 3 project-level learned rules from the test scenario are missing entirely. |
| c11 | Output flags the 2 wisdom frames as STALE (45 days since last update, exceeding the 30-day threshold) — not just listed as "present" | FAIL | Section 5 says 'Frames found: None'. Wisdom frames are not present in the output at all, so staleness cannot be flagged. |
| c12 | Output flags the 2 unresolved Critical learnings explicitly as a finding requiring resolution — with their names, not just a count of "2 unresolved" | FAIL | Section 6 says 'Critical unresolved: 0 found (directory empty)'. No critical learnings are found, named, or flagged. The test scenario's 2 Critical unresolved learnings are entirely absent. |
| c13 | Output reports the 12 learning files with the breakdown by severity (e.g. "12 total: 2 Critical unresolved, X Important, Y Minor") | FAIL | Section 6 states 'Session learning files: 0 (learnings directory is empty)'. No learning files found, no breakdown reported. Test scenario's 12 files with severity breakdown are completely absent. |
| c14 | Output reports CLAUDE.md as PRESENT (project root) and project-level `settings.json` as ABSENT — neither section skipped | PARTIAL | Settings.json correctly reported as absent: 'No `.claude/settings.json` or `.claude/settings.local.json`'. But CLAUDE.md is incorrectly reported as absent: 'Root `CLAUDE.md`: Not found' — the test scenario states a CLAUDE.md IS present at the project root. Half correct. |
| c15 | Output's findings are descriptive (what IS), separated from recommendations (what to do) — not mixed in the same paragraph | PASS | All six numbered sections (Rules, Project Configuration, CLAUDE.md Coverage, Memory Health, Wisdom Frame Health, Learning Coverage) are purely descriptive. The separate '### Recommendations' section is where all action items appear. No mixing within paragraphs. |
| c16 | Output's recommendations are specific actions tied to findings — e.g. "Update `wisdom-development.md` (45 days stale)", "Resolve the 2 Critical learnings: <name1>, <name2>", "Consider creating `.claude/settings.json` if project-specific overrides are needed" — not "consider reviewing" | FAIL | Recommendations include: 'Create a CLAUDE.md — run /init' (CLAUDE.md actually exists), 'Bootstrap memory', 'Evaluate wisdom frames', 'Review global rule freshness'. None are tied to the actual test-scenario findings (no wisdom frame staleness alert, no Critical learning resolution, no marketplace rule gap). Generic rather than finding-specific. |
| c17 | Output's summary header gives an at-a-glance project state (e.g. "Setup HEALTHY with 2 stale items requiring attention") before the per-section detail | PARTIAL | The output opens with '## Project Health Report' and a '### Summary' table listing 6 areas with statuses. However there is no single overall health status line (e.g., HEALTHY / ATTENTION NEEDED / CRITICAL) — just the per-area table. At-a-glance overview is partially present via the table but lacks the rolled-up status verdict. |
| c18 | Output flags whether the thinking plugin (the rule installer) is enabled — without it, marketplace rules in `~/.claude/rules/` may not be reaching the project, which is a common silent failure | PARTIAL | Section 2 lists 8 enabled plugins including 'thinking' explicitly. However the output does not call out the thinking plugin's specific role as the rule installer or note whether its absence would be a silent failure. The plugin appears in the list but is not specifically flagged for its rule-installation function. |

### Notes

The captured output demonstrates strong structural compliance — correct format, clear findings-vs-recommendations separation, and proper handling of the settings.json absence. However it fundamentally fails to reflect the test scenario's described project state. The skill found no project-level .claude/rules/ directory (missing 3 learned rules), no marketplace rules in ~/.claude/rules/ (missing 5), reported CLAUDE.md as absent when it should be present, found zero wisdom frames (should find 2 stale ones), and found zero learnings (should find 12 with 2 Critical unresolved). This appears to be a case where the skill ran real tool calls against the actual environment rather than processing the described scenario from the prompt — the globally-installed learned rules appear in the output because they genuinely exist, but the test-scenario-specific artifacts do not. As a result, all criteria requiring correct data (staleness flags, critical learning escalation, rule counts/separation, CLAUDE.md presence) fail, driving the score to 41%.
