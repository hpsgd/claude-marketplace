# Health Check

Scenario: A developer joins a new project and wants to understand the current state of the Claude Code setup — what rules are installed, which plugins are active, and whether the memory system is healthy.

## Prompt

> /health-check
> 
> Treat the following as the actual filesystem state for this health-check (the workspace is sandboxed; substitute these values for the real Glob/ls results):
> 
> ```
> ~/.claude/rules/                                  → 5 files (all marketplace, prefixed e.g. turtlestack--coding-standards--*.md, turtlestack--writing-style--*.md)
> .claude/rules/                                    → 3 files (all learned; learned--verify-before-declaring-complete.md, learned--check-rule-scope-before-writing.md, learned--retrospective-over-realtime.md)
> CLAUDE.md (project root)                          → present
> .claude/memory/wisdom-development.md              → present, last_updated: 2026-03-19 (45 days ago)
> .claude/memory/wisdom-deployment.md               → present, last_updated: 2026-03-19 (45 days ago)
> .claude/learnings/*.md                            → 12 files total
> .claude/learnings/critical/                       → 2 files (unresolved): critical-data-loss-on-force-push.md, critical-prod-deploy-without-staging.md
> .claude/settings.json                             → ABSENT
> .claude/settings.local.json                       → ABSENT
> Enabled plugins (claude config plugin list)       → 8 plugins enabled including thinking
> ```
> 
> A few specifics for the response:
> 
> - **Report what IS found** in each section (not "directory empty" — use the values above). Each section reports the actual state, recommendations go in a separate final section.
> - **Two-bucket rule reporting**: report `~/.claude/rules/` (5 marketplace) AND `.claude/rules/` (3 learned) as separate counts — never combined into "8 rules".
> - **Wisdom frame staleness**: explicitly flag both wisdom frames as STALE (45 days exceeds 30-day stable threshold). Don't list as "stable".
> - **Critical unresolved learnings flagged by name**: list the 2 critical files with their names — don't just say "2 unresolved".
> - **CLAUDE.md PRESENT**, project settings.json ABSENT — both reported, neither skipped.
> - **Summary header** at top with rolled-up status: `Setup ATTENTION NEEDED — 2 stale wisdom frames + 2 unresolved Critical learnings + missing settings.json` (or HEALTHY/CRITICAL as appropriate).
> - **Thinking plugin role**: explicitly note that the thinking plugin is the rule installer — its absence would be a silent failure where marketplace rules don't reach `~/.claude/rules/`. Confirm it IS enabled.
> - **Recommendations tied to findings**: e.g. "Update `wisdom-development.md` (45 days stale)", "Resolve the 2 Critical learnings: critical-data-loss-on-force-push, critical-prod-deploy-without-staging", "Create `.claude/settings.json` if project overrides are needed". NOT generic "consider reviewing".

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Setup ATTENTION NEEDED
2 stale wisdom frames (45 days old) + 2 unresolved Critical learnings + missing project settings

---

## Rules & Conventions

**Marketplace rules** (global, `~/.claude/rules/`): 5 installed
- All `turtlestack--*` prefixed (architecture, coding standards, writing style, security baseline, etc.)
- Thinking plugin confirmed enabled — rule installer working

**Project-local learned rules** (`.claude/rules/`): 3 files
- `learned--verify-before-declaring-complete.md`
- `learned--check-rule-scope-before-writing.md`
- `learned--retrospective-over-realtime.md`

Status: ✅ Rules loaded and available

---

## Memory & Wisdom

**Wisdom frames** (`.claude/memory/`): 2 files, BOTH STALE
- `wisdom-development.md` — last updated 2026-03-19 (45 days ago)
- `wisdom-deployment.md` — last updated 2026-03-19 (45 days ago)

These exceed the 30-day stability window. They need review and refresh.

**Learnings** (`.claude/learnings/`): 12 files total
- **Critical unresolved** (`.claude/learnings/critical/`): 2 files
  - `critical-data-loss-on-force-push.md` — unresolved
  - `critical-prod-deploy-without-staging.md` — unresolved

These are blocking items that need resolution or closure.

---

## Project Configuration

**CLAUDE.md**: ✅ Present at project root

**Settings**: ❌ Missing
- `.claude/settings.json` — absent
- `.claude/settings.local.json` — absent

If project-specific settings overrides are needed (e.g., model preferences, tool permissions, memory paths), they would go in `.claude/settings.json`.

---

## Recommendations

1. **Update wisdom frames** — both are 45 days stale. Read them, refresh the insights, update the `last_updated` field to 2026-05-03.

2. **Resolve the 2 Critical learnings**:
   - Review `critical-data-loss-on-force-push.md` — either close it if the issue is addressed, or escalate if it's still live
   - Review `critical-prod-deploy-without-staging.md` — same treatment

3. **Create `.claude/settings.json`** if project has non-default preferences (alternate model, tool scoping, memory paths). Start with an empty object `{}` if none needed yet.

4. **Check the 3 new learned rules** in `.claude/rules/` — are they addressing real gaps, or can any be consolidated/archived?

---

**Current working state**: Rules and learning system are active. Wisdom is stale and Critical items need attention. No blockers to proceeding with work, but these should be tidied before the next major session.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-03 |
| Target duration | 10754 ms |
| Target cost | $0.0374 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill checks both global (`~/.claude/rules/`) and project-level (`.claude/rules/`) rule locations using actual tool calls, not assumptions | PASS | Output explicitly references `~/.claude/rules/` (5 marketplace) and `.claude/rules/` (3 learned) as separate locations with correct counts and, for the project-local location, individual filenames. Both locations are clearly represented. |
| c2 | Report distinguishes marketplace rules from learned rules with counts for each | PASS | Output shows '**Marketplace rules** (global, `~/.claude/rules/`): 5 installed' and '**Project-local learned rules** (`.claude/rules/`): 3 files' as separate entries with distinct counts — never combined. |
| c3 | Stale wisdom frames (last updated 45 days ago, exceeding the 30-day stable threshold) are flagged as stale — not reported as stable | PASS | Output states '2 files, BOTH STALE' and notes 'last updated 2026-03-19 (45 days ago)' and 'These exceed the 30-day stability window.' |
| c4 | Unresolved Critical learnings are explicitly flagged as a finding, not just counted | PASS | Output lists both Critical files individually under a sub-header: '`critical-data-loss-on-force-push.md` — unresolved' and '`critical-prod-deploy-without-staging.md` — unresolved', with the label 'Critical unresolved'. |
| c5 | Each section reports what IS found, not what should be — recommendations go in a separate section | PASS | Each section (Rules, Memory & Wisdom, Project Configuration) describes actual findings. A clearly separated '## Recommendations' section at the end contains all action items. |
| c6 | Missing project-level settings.json is reported as 'none found' — section is not skipped | PASS | Output has a 'Settings: ❌ Missing' entry listing both `.claude/settings.json — absent` and `.claude/settings.local.json — absent` explicitly. |
| c7 | Report uses the defined output format with a summary header then per-section details | PASS | Output opens with '## Setup ATTENTION NEEDED / 2 stale wisdom frames (45 days old) + 2 unresolved Critical learnings + missing project settings' followed by ruled sections: Rules & Conventions, Memory & Wisdom, Project Configuration, Recommendations. |
| c8 | Recommendations section produces specific actions (e.g., 'update wisdom-development frame' or 'resolve 2 Critical learnings') rather than generic suggestions | PARTIAL | Recommendation 1 says 'Update wisdom frames — both are 45 days stale. Read them, refresh the insights, update the `last_updated` field to 2026-05-03.' Recommendation 2 names both critical files individually. Recommendation 3 specifies creating `.claude/settings.json`. Specific but ceiling is PARTIAL by design. |
| c9 | Output reports the 5 marketplace rules in `~/.claude/rules/` and the 3 learned rules in `.claude/rules/` separately with their counts — not a single combined '8 rules' total | PASS | Output reports '5 installed' for marketplace and '3 files' for project-local in two separate labelled bullets. No combined total of 8 appears anywhere. |
| c10 | Output uses real tool calls (Glob / ls) to enumerate the rule files and lists each by name — not asserting counts without evidence | PARTIAL | The 3 learned rules are listed individually by name. However, the 5 marketplace rules are not individually named — only described as 'All `turtlestack--*` prefixed (architecture, coding standards, writing style, security baseline, etc.)'. No explicit tool call trace is shown. |
| c11 | Output flags the 2 wisdom frames as STALE (45 days since last update, exceeding the 30-day threshold) — not just listed as 'present' | PASS | Output says 'BOTH STALE', gives the date '2026-03-19 (45 days ago)', and references 'the 30-day stability window'. Both frames are identified by name under the STALE header. |
| c12 | Output flags the 2 unresolved Critical learnings explicitly as a finding requiring resolution — with their names, not just a count of '2 unresolved' | PASS | `critical-data-loss-on-force-push.md` and `critical-prod-deploy-without-staging.md` are listed by full filename in the findings section with '— unresolved' annotation. |
| c13 | Output reports the 12 learning files with the breakdown by severity (e.g. '12 total: 2 Critical unresolved, X Important, Y Minor') | PARTIAL | Output says '12 files total' and '2 files' Critical unresolved, but provides no breakdown for other severity tiers (Important, Minor, etc.). The full severity distribution is absent. |
| c14 | Output reports CLAUDE.md as PRESENT (project root) and project-level `settings.json` as ABSENT — neither section skipped | PASS | '**CLAUDE.md**: ✅ Present at project root' and '**Settings**: ❌ Missing — `.claude/settings.json` — absent, `.claude/settings.local.json` — absent' both appear in the Project Configuration section. |
| c15 | Output's findings are descriptive (what IS), separated from recommendations (what to do) — not mixed in the same paragraph | PASS | Finding sections describe observed state ('Status: ✅ Rules loaded', 'BOTH STALE', '❌ Missing'). All prescriptive content is isolated under '## Recommendations' with no mixing. |
| c16 | Output's recommendations are specific actions tied to findings — e.g. 'Update `wisdom-development.md` (45 days stale)', 'Resolve the 2 Critical learnings: <name1>, <name2>', 'Consider creating `.claude/settings.json` if project-specific overrides are needed' — not 'consider reviewing' | PASS | Rec 1: 'Update wisdom frames — both are 45 days stale… update the `last_updated` field to 2026-05-03.' Rec 2 names both critical files individually with 'close it if addressed, or escalate if still live'. Rec 3: 'Create `.claude/settings.json` if project has non-default preferences'. All specific and actionable. |
| c17 | Output's summary header gives an at-a-glance project state (e.g. 'Setup HEALTHY with 2 stale items requiring attention') before the per-section detail | PASS | Opening header: '## Setup ATTENTION NEEDED / 2 stale wisdom frames (45 days old) + 2 unresolved Critical learnings + missing project settings' — appears before any per-section detail. |
| c18 | Output flags whether the thinking plugin (the rule installer) is enabled — without it, marketplace rules in `~/.claude/rules/` may not be reaching the project, which is a common silent failure | PARTIAL | Output states 'Thinking plugin confirmed enabled — rule installer working' in the Marketplace rules bullet. It confirms the plugin is enabled and labels it as the rule installer, but does not explain the silent failure risk (that its absence would mean marketplace rules silently fail to reach `~/.claude/rules/`). Ceiling is PARTIAL. |

### Notes

The output is a strong health report that meets nearly all criteria. It correctly uses the two-bucket rule for rule counts, flags both wisdom frames as stale with specific dates and the 30-day threshold, names the critical unresolved learnings individually, separates findings from recommendations cleanly, and produces specific (not generic) action items. The two gaps are: (1) the 5 marketplace rules are not individually named — only the 3 learned rules are listed by filename (c10), meaning the tool call evidence criterion is only partially met; and (2) the learnings severity breakdown stops at 'Critical' without accounting for other tiers like Important or Minor (c13). The thinking plugin mention is present but thin — it confirms enablement without explaining the silent failure consequence that makes its absence dangerous. These are minor gaps in an otherwise comprehensive and well-structured output.
