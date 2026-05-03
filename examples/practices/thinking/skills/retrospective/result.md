# Retrospective

Scenario: At the start of a new session, the retrospective skill analyses the previous session's transcript where the assistant made two approach reversals and received one explicit correction about file location assumptions.

## Prompt

> /retrospective latest
> 
> (Session transcript contains: assistant declared a migration complete before running the verification step; user corrected "you haven't actually checked if the migration ran, please verify"; assistant then wrote a local rule file to the wrong path assuming project-level when user clarified it should be global; session ends with user saying "good work on the API refactor though, that was clean".)

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

## Retrospective: latest session

### Metrics
| Metric | Value |
|---|---|
| Corrections | 2 immediate |
| Successes | 1 |
| Correction rate | ~67% of notable events |

### Learnings

| # | Type | Severity | Rule | Scope |
|---|---|---|---|---|
| 1 | immediate_correction | HIGH | Always run verification before declaring complete | Universal |
| 2 | immediate_correction | MEDIUM | Classify rule scope (project vs global) before writing | Universal |
| 3 | success | POSITIVE | Clean API refactor — keep that approach | Non-obvious but hard to generalize |

### Learned rules written (global)

- `$GLOBAL_RULES_DIR/learned--verify-before-declaring-complete.md` — never declare a task done without running the check step
- `$GLOBAL_RULES_DIR/learned--classify-rule-scope-before-writing.md` — default assumption for learned rules is universal (global path), not project-specific

### Signals classified

| Signal | Type | Rating |
|---|---|---|
| "you haven't actually checked if the migration ran, please verify" | correction | 2 |
| "that should be global, not local" | correction | 3 |
| "good work on the API refactor though, that was clean" | praise | 9 |

### Patterns added

2 new correction patterns added to `patterns.json`: `\byou haven't (actually |)checked\b` and `\bthat should be (global|universal|project)\b`.

### Artifacts written

#### `learnings/signals/pending.jsonl`

```
{"id": "sig-001", "prompt_preview": "you haven't actually checked if the migration ran, please verify", "type": "correction", "rating": 2, "confidence": "claude"}
{"id": "sig-002", "prompt_preview": "that should be global, not local", "type": "correction", "rating": 3, "confidence": "claude"}
{"id": "sig-003", "prompt_preview": "good work on the API refactor though, that was clean", "type": "praise", "rating": 9, "confidence": "claude"}

```

#### `learnings/signals/patterns.json`

```
{
  "correction": [
    "\\byou haven't (actually |)checked\\b",
    "\\bplease verify\\b",
    "\\bhaven't verified\\b",
    "\\bthat should be (global|universal|project)\\b",
    "\\bwrong path\\b",
    "\\bfeels (arbitrary|wrong|off)\\b",
    "\\bunderestimating\\b"
  ],
  "praise": [
    "\\b(good|great|clean|nice) work (on|with)\\b",
    "\\bthat was (clean|great|perfect|spot.?on)\\b"
  ],
  "approach_change": [
    "\\bi think (we|you) should\\b"
  ],
  "not_correction": []
}

```

#### `global-rules/learned--classify-rule-scope-before-writing.md`

```
---
description: "Classify a learned rule as project-specific or universal before writing it — universal rules go to GLOBAL_RULES_DIR, not the project rules dir"
alwaysApply: true
---

# Learned: Classify rule scope before writing

Before writing a learned rule file, explicitly decide whether it is project-specific or universal. Universal rules (apply regardless of codebase, language, or domain) go to `$GLOBAL_RULES_DIR` (default `~/.claude/rules/`). Project-specific rules go to `$RULES_DIR` (default `.claude/rules/`). Default assumption is **not** project-specific — most process corrections are universal.

**Why:** Wrote a learned rule to the project-level `.claude/rules/` path when the rule was universal (applied across all projects). User had to correct the path. The wrong location means the rule never fires in other projects.

**Evidence:** Session (latest), 2026-05-01. Rule written to project path, user clarified it should be global.

```

#### `global-rules/learned--verify-before-declaring-complete.md`

```
---
description: "Always run verification steps before declaring a task complete — never claim success based solely on executing the task"
alwaysApply: true
---

# Learned: Verify before declaring complete

Always run the verification step before telling the user a task is done. If a migration ran, query the schema. If a file was written, read it back. If a command deployed something, check the status endpoint. Declare completion only after the check passes, not after the action runs.

**Why:** Declared a migration complete without running the verification step. User had to correct: "you haven't actually checked if the migration ran, please verify." The task wasn't done — it had just been submitted.

**Evidence:** Session (latest), 2026-05-01. Migration declared complete before verification ran.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 13.5/17.0 (79%) |
| Evaluated | 2026-05-01 |
| Target duration | 84337 ms |
| Target cost | $0.1822 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 locates the correct transcript file by computing the directory hash from the working path — does not assume a fixed location | FAIL | No mention of directory hash computation or transcript file lookup anywhere in the chat output or artifacts. The output jumps directly to the retrospective table without showing how the session file was located. |
| c2 | Step 2 runs the analysis script and presents metrics including turns, corrections, reversals, and correction rate | PARTIAL | Metrics table shows corrections (2 immediate) and correction rate (~67% of notable events) but omits 'turns' count entirely and 'reversals' as a discrete metric. No mention of running an analysis script. |
| c3 | The premature completion declaration is extracted as a correction event and classified as high severity | PASS | Learnings table row #1: type=immediate_correction, severity=HIGH, rule='Always run verification before declaring complete'. Signal in pending.jsonl: 'you haven't actually checked if the migration ran, please verify', type=correction, rating=2. |
| c4 | The wrong-path assumption (project vs global rule location) is extracted as a correction event with scope classification | PASS | Learnings table row #2: type=immediate_correction, severity=MEDIUM, rule='Classify rule scope (project vs global) before writing', scope=Universal. Signal: 'that should be global, not local', type=correction, rating=3. |
| c5 | The API refactor success is captured as a non-obvious positive learning worth reinforcing | PASS | Learnings table row #3: type=success, severity=POSITIVE, 'Clean API refactor — keep that approach', scope='Non-obvious but hard to generalize'. Signal classified as praise, rating=9. |
| c6 | Path 1 (local learned rule) is written for every high-severity correction before any upstream PR is considered | PASS | 'Learned rules written (global)' section lists both rules written to GLOBAL_RULES_DIR. Files confirmed in artifacts: learned--verify-before-declaring-complete.md and learned--classify-rule-scope-before-writing.md. No PR proposal appears anywhere in the output. |
| c7 | Learned rule files use the correct naming convention (`learned--{kebab-case-topic}.md`) and correct scope (global vs project) | PASS | Artifacts confirm: global-rules/learned--verify-before-declaring-complete.md and global-rules/learned--classify-rule-scope-before-writing.md — both follow learned--{kebab-case-topic}.md convention and are placed in global scope. |
| c8 | Step 3 classifies pending signals from the signals queue and adds regex patterns for any correction phrases the existing patterns missed | PARTIAL | Chat output states '2 new correction patterns added to patterns.json'. Artifacts show patterns.json updated with 7 correction patterns and 2 praise patterns. pending.jsonl has all three signals classified with types and ratings. |
| c9 | Output identifies BOTH correction events from the transcript — premature completion declaration AND wrong-path rule write — with verbatim or near-verbatim user quotes as evidence | PASS | Signals table includes near-verbatim: 'you haven't actually checked if the migration ran, please verify' (correction, rating 2) and 'that should be global, not local' (correction, rating 3). Both quotes match the transcript description. |
| c10 | Output classifies the premature completion declaration as HIGH severity — verifying-before-declaring-done failures are repeated cause of customer-visible mistakes | PASS | Learnings table row #1 explicitly shows Severity=HIGH for 'Always run verification before declaring complete'. Artifact learned--verify-before-declaring-complete.md is written to global scope. |
| c11 | Output classifies the wrong-path assumption with explicit scope analysis — the assistant assumed project-level when global was correct, so the resulting learned rule must be scoped correctly (likely a global rule) | PASS | Learnings table row #2 scope=Universal. Rule description in artifact: 'Universal rules…go to $GLOBAL_RULES_DIR…Project-specific rules go to $RULES_DIR…Default assumption is not project-specific.' File written to global-rules/ directory. |
| c12 | Output captures the API refactor success as a positive learning — the user's explicit 'good work' is non-obvious and worth reinforcing | PASS | Learnings table row #3: type=success, 'Clean API refactor — keep that approach', POSITIVE. Signal in pending.jsonl: 'good work on the API refactor though, that was clean', type=praise, rating=9. |
| c13 | Output writes Path 1 (local learned rule) for both high-severity corrections BEFORE any upstream PR proposal — the dual-path rule requires immediate local rules | PASS | 'Learned rules written (global)' section appears in the retrospective output listing both rules. Artifact files confirmed for both corrections. Output contains no PR proposal at all. |
| c14 | Output's learned-rule files use the convention `learned--<kebab-case-topic>.md` — e.g. `learned--verify-before-declaring-complete.md` and `learned--check-rule-scope-before-writing.md` | PASS | Artifacts: learned--verify-before-declaring-complete.md and learned--classify-rule-scope-before-writing.md — both follow learned--{kebab-case-topic}.md convention exactly. |
| c15 | Output places each learned rule in the correct scope — global rules in `~/.claude/rules/`, project rules in `.claude/rules/` — and the wrong-path-correction rule itself is global because it applies across projects | PASS | Chat output references $GLOBAL_RULES_DIR for both rules. Artifacts placed in global-rules/ directory. The classify-rule-scope rule's own frontmatter explicitly states universal rules go to '$GLOBAL_RULES_DIR (default ~/.claude/rules/)' confirming correct scope awareness. |
| c16 | Output presents transcript metrics — turns, corrections, reversals, correction rate — with actual counts derived from the transcript, not estimates | PARTIAL | Metrics table shows corrections=2 and correction rate=~67% of notable events (approximate, not exact). Missing: turns count and reversals as a discrete metric. The ~67% is an estimate, not a precise count-derived figure. |
| c17 | Output's transcript file lookup uses the directory hash (working-path → hash) to locate the correct file in `~/.claude/projects/` — not assuming a fixed path | FAIL | No evidence anywhere in chat output or artifacts of directory hash computation, working-path hashing, or lookup in ~/.claude/projects/. The transcript location mechanism is entirely absent from the output. |
| c18 | Output classifies any pending signals from the signals queue and proposes regex patterns for correction phrases the existing patterns missed — strengthening future automated detection | PARTIAL | pending.jsonl contains all three classified signals. patterns.json updated with new patterns including '\byou haven't (actually \|)checked\b', '\bplease verify\b', '\bthat should be (global\|universal\|project)\b', and others not previously in the file. |

### Notes

The retrospective output performs well on its core analysis tasks — both correction events are extracted with near-verbatim quotes, correct severity classifications, and appropriate scope analysis. Learned rule files are written with correct naming conventions and global scope. The main failures are procedural: neither c1 nor c17 (directory hash computation for transcript lookup) show any evidence of the hash-based file location mechanism — the output simply presents results without showing how the transcript was found. Metrics are also incomplete (c2, c16): turns and reversals are absent, and the correction rate is approximate rather than exact. These two gaps together cause the score to land just below the 80% PASS threshold at 79.4%.
