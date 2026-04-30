# Result: retrospective session analysis with corrections

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

Simulated execution of `/retrospective latest` against the transcript described in the test scenario.

---

### Step 1: Locate transcript

```bash
path_to_hash() { echo "$1" | sed 's|^/||; s|[^a-zA-Z0-9]|-|g'; }
PROJECTS_DIR="$HOME/.claude/projects"
MAIN_HASH_DIR="$PROJECTS_DIR/-$(path_to_hash "$PWD")"
# PWD = /Users/martin/Projects/myproject
# Hash: Users-martin-Projects-myproject
# Resolved: ~/.claude/projects/-Users-martin-Projects-myproject/
```

Scanning worktrees and breadcrumbs...

**Transcript dirs found:**

- `~/.claude/projects/-Users-martin-Projects-myproject/`

**Latest completed session:** `~/.claude/projects/-Users-martin-Projects-myproject/abc123def456.jsonl`

---

### Step 2: Analysis script output

```bash
python3 ~/.claude/plugins/thinking/scripts/analyse-session.py \
    ~/.claude/projects/-Users-martin-Projects-myproject/abc123def456.jsonl \
    --project-dir .claude/learnings \
    --global-dir ~/.claude/learnings \
    --json
```

**Script JSON output (summarised):**

```json
{
  "metrics": {
    "session_id": "abc123def456",
    "duration_minutes": 47,
    "turns_user": 14,
    "turns_assistant": 14,
    "corrections": 2,
    "reversals": 1,
    "successes": 1,
    "correction_rate": 14.3
  },
  "events": [
    {
      "type": "immediate_correction",
      "turn": 8,
      "assistant_action": "Declared migration complete after generating the migration script",
      "user_message": "you haven't actually checked if the migration ran, please verify",
      "context": "Database migration task — assistant wrote the script and stated 'migration complete' without executing a verification query"
    },
    {
      "type": "immediate_correction",
      "turn": 11,
      "assistant_action": "Wrote learned rule file to .claude/rules/learned--x.md",
      "user_message": "that rule should be global, not project-level — it applies everywhere",
      "context": "Writing a rule about checking file paths — assistant defaulted to project-level, user corrected to global scope"
    },
    {
      "type": "success",
      "turn": 14,
      "assistant_action": "Refactored authentication API endpoints into a single versioned module",
      "user_message": "good work on the API refactor though, that was clean",
      "context": "Bundled related endpoint changes instead of splitting across PRs; user explicitly praised the approach"
    }
  ],
  "files_modified": {
    "src/db/migrations/001_add_user_flags.sql": 1,
    ".claude/rules/learned--x.md": 2
  }
}
```

---

### Retrospective: abc123def456

#### Metrics

| Metric | Value |
|---|---|
| Duration | 47 minutes |
| Turns | 14 user / 14 assistant |
| Corrections | 2 immediate, 0 approach changes, 1 reversal |
| Successes | 1 |
| Correction rate | 14.3% |

---

### Step 3: Classify queued signals

Reading `.claude/learnings/signals/pending.jsonl`...

**Pending signals found: 2**

| # | Prompt preview | Regex classification | Manual classification | Rating | Pattern gap |
|---|---|---|---|---|---|
| 1 | "you haven't actually checked if the migration ran, please verify" | `unclassified` | `correction` | 2 | `\bactually checked\b` missed |
| 2 | "good work on the API refactor though, that was clean" | `unclassified` | `praise` | 9 | `\bgood work\b` + `\bclean\b` sequence missed |

**Updated `patterns.json`:**

```json
{
  "correction": [
    "\\bfeels (arbitrary|wrong|off)\\b",
    "\\bunderestimating\\b",
    "\\bhaven't actually (checked|verified|run|tested)\\b",
    "\\bplease verify\\b"
  ],
  "praise": [
    "\\bgood work\\b",
    "\\bthat was (clean|solid|great|well done)\\b"
  ],
  "approach_change": ["\\bi think (we|you) should\\b"],
  "not_correction": []
}
```

**2 signals classified. 3 new patterns added.**

---

### Step 4: Learnings and local rules

#### Learning 1: Verify before declaring complete

**Type:** immediate_correction
**What happened:** Assistant wrote the database migration script and declared "migration complete" without running a verification query to confirm the migration executed successfully.
**What was wrong:** User corrected: "you haven't actually checked if the migration ran, please verify." Declaring completion without verification is a repeated cause of silent failures reaching production.
**Rule:** Never declare a task complete without running the verification step appropriate to the task type. For migrations: run a query confirming the schema change. For deployments: check the health endpoint. For file writes: read back the file.
**Scope:** Universal — applies to all projects

#### Learning 2: Check rule scope before writing

**Type:** immediate_correction
**What happened:** Assistant wrote a new learned rule to `.claude/rules/learned--x.md` (project-level) when the rule content was about a universal behaviour (where to look for rule files), which applies across all projects.
**What was wrong:** User corrected: "that rule should be global, not project-level — it applies everywhere." The assistant defaulted to project scope without asking whether the rule should be universal.
**Rule:** Before writing a learned rule, classify its scope. If the rule prevents a behaviour that would be wrong in any project (not just this codebase), write it to `~/.claude/rules/` not `.claude/rules/`.
**Scope:** Universal — applies to all projects

#### Learning 3: Bundled API refactor received explicit praise

**Type:** success (non-obvious)
**What happened:** Consolidated authentication endpoint changes into a single versioned module rather than splitting across multiple PRs.
**What was right:** User said "good work on the API refactor though, that was clean." Bundled approach kept the diff coherent and avoided partial-state merges. This is worth reinforcing — the default instinct can be to split by endpoint.
**Rule:** When refactoring a cohesive domain (e.g., all auth endpoints), prefer a single bundled PR over per-endpoint splits unless there's a deployment or review reason to split.
**Scope:** Universal

---

### Path 1: Write local learned rules

#### Rule 1 written: `~/.claude/rules/learned--verify-before-declaring-complete.md`

```markdown
---
description: "Never declare a task complete without running the appropriate verification step"
alwaysApply: true
---

# Learned: Verify before declaring complete

Never declare a task complete without running the verification step for that task type.
For migrations: query the schema. For deployments: check health. For file writes: read back.

**Why:** Declared a database migration complete after writing the script — without verifying
the migration had actually run. User corrected: "you haven't actually checked if the
migration ran, please verify."

**Evidence:** Session abc123def456, 2026-04-30. Premature completion declaration on migration task.
```

#### Rule 2 written: `~/.claude/rules/learned--check-rule-scope-before-writing.md`

```markdown
---
description: "Classify a rule as universal or project-specific before writing it — default is not always project"
alwaysApply: true
---

# Learned: Check rule scope before writing

Before writing a learned rule, decide: does this behaviour apply only to this project,
or to all projects? Universal rules go to `~/.claude/rules/`. Project-specific go to
`.claude/rules/`. Do not default to project-level without checking.

**Why:** Wrote a rule about checking file locations to `.claude/rules/` (project level)
when the user clarified it should be global — it applies to any project.

**Evidence:** Session abc123def456, 2026-04-30. Wrong-scope rule write on rule-file task.
```

*(No local rule written for the success — successes reinforce approach but don't require a preventive rule.)*

---

#### Learnings summary

| # | Type | Severity | Rule | Scope |
|---|---|---|---|---|
| 1 | immediate_correction | HIGH | Verify before declaring complete | Universal → `~/.claude/rules/` |
| 2 | immediate_correction | HIGH | Check rule scope before writing | Universal → `~/.claude/rules/` |
| 3 | success | POSITIVE | Bundle cohesive API refactors | Universal |

**Path 1 rules written: 2**
Path 2 (upstream PR) not triggered — pattern threshold not yet reached (need 5 instances).

---

## Criteria

### Criteria (from `## Criteria`)

- [x] PASS: Step 1 locates the correct transcript file by computing the directory hash from the working path — met: the skill provides the full `path_to_hash()` bash function, constructs the hash-based path under `~/.claude/projects/`, scans active worktrees via `git worktree list --porcelain`, and falls back to removed-worktree breadcrumbs
- [x] PASS: Step 2 runs the analysis script and presents metrics including turns, corrections, reversals, and correction rate — met: `analyse-session.py` with `--json` flag is specified; the Output Format section defines a metrics table with Duration, Turns, Corrections, Successes, and Correction rate
- [x] PASS: The premature completion declaration is extracted as a correction event and classified as high severity — met: Step 4 assigns HIGH severity to all immediate corrections; the skill instructs extraction of every correction event from the script output and generation of an imperative rule
- [x] PASS: The wrong-path assumption (project vs global rule location) is extracted as a correction event with scope classification — met: Step 4 Rules section explicitly covers universal vs project-specific scope classification with concrete examples; scope drives which path the learned rule is written to
- [x] PASS: The API refactor success is captured as a non-obvious positive learning worth reinforcing — met: Step 4 "For successes (POSITIVE)" section specifies only non-obvious successes that represent a genuine judgment call are recorded; an explicit "good work" from the user is a canonical trigger
- [x] PASS: Path 1 (local learned rule) is written for every high-severity correction before any upstream PR is considered — met: Path 1 is defined within Step 4; Path 2 (upstream PR) is Step 6; the Rules section states "Always write a local learned rule first (Path 1)"
- [x] PASS: Learned rule files use the correct naming convention (`learned--{kebab-case-topic}.md`) and correct scope (global vs project) — met: naming convention and scope-to-location mapping (`~/.claude/rules/` vs `.claude/rules/`) are explicit, with matching examples
- [~] PARTIAL: Step 3 classifies pending signals from the signals queue and adds regex patterns for any correction phrases the existing patterns missed — partially met: Step 3 is marked mandatory and covers both signal classification and regex pattern generation with detailed rules; the skill cannot guarantee extraction of specific patterns from the scenario's correction phrases without live execution, but the mechanism is sound

### Output expectations (from `## Output expectations`)

- [x] PASS: Output identifies BOTH correction events with verbatim or near-verbatim user quotes as evidence — met: simulated output quotes "you haven't actually checked if the migration ran, please verify" and "that rule should be global, not project-level — it applies everywhere"
- [x] PASS: Output classifies the premature completion declaration as HIGH severity — met: Step 4 assigns HIGH severity to all immediate corrections; simulated output classifies it as HIGH
- [x] PASS: Output classifies the wrong-path assumption with explicit scope analysis — met: Step 4 scope guidance is explicit; simulated output explicitly classifies this as a universal rule and writes it to `~/.claude/rules/`
- [x] PASS: Output captures the API refactor success as a positive learning — met: Step 4 "For successes (POSITIVE)" directs non-obvious successes to be recorded; simulated output captures it as a POSITIVE learning
- [x] PASS: Output writes Path 1 (local learned rule) for both high-severity corrections BEFORE any upstream PR proposal — met: rules are written in Step 4; Path 2 is Step 6; simulated output writes both rules before noting Path 2 is not triggered
- [x] PASS: Output's learned-rule files use the convention `learned--<kebab-case-topic>.md` — met: simulated output produces `learned--verify-before-declaring-complete.md` and `learned--check-rule-scope-before-writing.md`
- [x] PASS: Output places each learned rule in the correct scope — met: both correction rules are classified as universal and written to `~/.claude/rules/`; the wrong-path-correction rule itself is correctly global
- [x] PASS: Output presents transcript metrics with actual counts derived from the transcript — met: simulated output shows 47 min, 14 turns, 2 corrections, 1 reversal, 1 success, 14.3% correction rate
- [x] PASS: Output's transcript file lookup uses the directory hash (working-path → hash) — met: simulated output shows the hash computation and resolved path
- [~] PARTIAL: Output classifies pending signals and proposes regex patterns for correction phrases the existing patterns missed — partially met: simulated output classifies both signals and adds 3 new patterns; pattern-writing quality depends on execution context but the mechanism produces correct-form patterns

## Notes

The skill definition is thorough. The two-path design (local rule immediately, upstream PR at threshold) is cleanly enforced both in step ordering and in the Rules section. Scope classification (universal vs project-specific) is the hardest judgment call and the skill provides concrete criteria with examples.

The PARTIAL scores reflect a structural constraint: whether the regex patterns the skill generates for this scenario's specific correction phrases would catch edge cases cannot be verified without live execution. The pattern-writing rules are sound — word boundary requirements, false-positive testing protocol — but the output quality is model-dependent.

One observation: the trigger table lists `latest` as running "Steps 1–4", which includes Step 3. Step 3 is also labelled mandatory within its own section. Both are consistent. The inclusion of Step 3 in the `latest` trigger matters — it closes a gap where an implementer might skip signal classification on the assumption it's only for `signals` mode.
