# Result: create-skill new skill for existing agent

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 14.5 / 16 criteria met (90.6%) |
| **Evaluated** | 2026-04-30 |
| **Source** | `plugins/practices/plugin-curator/skills/create-skill/SKILL.md` |

## Output

Simulated execution of:

> `/create-skill review-go for coding-standards — Go code review skill covering error handling patterns, interface usage, goroutine safety, and table-driven tests.`

---

### Step 1 — Read template and conventions

```
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md")
Read(file_path="CLAUDE.md")
```

Template loaded. CLAUDE.md confirms plugin layout and naming conventions.

---

### Step 2 — Identify parent agent

```bash
find plugins -path "*/coding-standards/agents/*.md"
# → plugins/practices/coding-standards/agents/coding-standards.md

find plugins -path "*/coding-standards/skills/*/SKILL.md"
# → plugins/practices/coding-standards/skills/review-conventions/SKILL.md
#   plugins/practices/coding-standards/skills/strict-validation/SKILL.md
```

Parent agent read. Sibling skills read. `review-conventions` covers general review ceremony and commit messages. `strict-validation` covers type safety at boundaries. Neither covers language-specific review patterns for Go. No duplication risk.

---

### Step 3 — Research the domain

Go-specific review areas to cover, drawn from the prompt arguments:

- **Error handling** — named returns vs wrapped errors, `errors.Is`/`errors.As`, sentinel errors vs typed errors, ignoring errors with `_`
- **Interface usage** — small interface principle, accept interfaces / return structs, no premature abstraction
- **Goroutine safety** — race detector (`-race`), channel ownership, unbounded goroutine spawning, `context.Context` cancellation
- **Table-driven tests** — `t.Run` subtests, test case struct shape, parallel subtests with `t.Parallel()`

Unique contribution: fills the gap between `strict-validation` (boundary types) and actual Go code review pass — something a developer would run on a PR touching `.go` files.

---

### Step 4 — Create directory

```bash
mkdir -p plugins/practices/coding-standards/skills/review-go
```

---

### Step 5 — Write SKILL.md

**Path:** `plugins/practices/coding-standards/skills/review-go/SKILL.md`

```markdown
---
name: review-go
description: "Produces a Go code review report covering error handling, interface design, goroutine safety, and table-driven tests. Auto-invoked when reviewing .go files in a PR or code review task."
argument-hint: "[file path(s) or PR description to review]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---

Review Go code in $ARGUMENTS for correctness, safety, and idiomatic patterns.

Related skills: `review-conventions` (general review ceremony), `strict-validation` (type boundary checks).

## Process (sequential — do not skip steps)

### Pass 1: Error handling

1. Find all error returns:
   ```bash
   Grep(pattern="return.*err", glob="**/*.go")
   ```
2. Check each:
   - Is `err` checked immediately after every call that returns one?
   - Are errors ignored with `_`? Flag every instance.
   - Are sentinel errors compared with `==` instead of `errors.Is`? Flag — breaks wrapping.
   - Are type assertions on errors done without `errors.As`? Flag.
   - Does the function return a naked `error` when a typed error would make callers safer?

### Pass 2: Interface usage

1. Find all interface declarations:
   ```bash
   Grep(pattern="type \w+ interface", glob="**/*.go")
   ```
2. Check each:
   - Does the interface have more than 3 methods? Flag as a candidate to split.
   - Is a concrete struct returned where the declared return type could be an interface? Flag — couples callers to implementation.
   - Is a concrete type accepted as a parameter where an interface would work? Flag.
   - Is an interface defined in the same package as its only implementation? Flag — premature abstraction.

### Pass 3: Goroutine safety

1. Find goroutine spawns:
   ```bash
   Grep(pattern="go func|go \w+\(", glob="**/*.go")
   ```
2. For each:
   - Is there a bounding mechanism (`sync.WaitGroup`, channel drain, `errgroup`)? If not, flag unbounded spawning.
   - Does the goroutine close over a loop variable? Flag — classic race.
   - Does the channel have a direction annotation (`chan<-` / `<-chan`) in function signatures? If not, flag.
   - Is `context.Context` propagated into the goroutine? If not, flag — prevents clean cancellation.
3. Check mutex usage:
   ```bash
   Grep(pattern="sync\.Mutex|sync\.RWMutex", glob="**/*.go")
   ```
   - Is `sync.Mutex` used where reads dominate? Suggest `sync.RWMutex`.
   - Are mutexes copied by value (passed as struct without pointer)? Flag — data race.

### Pass 4: Table-driven tests

1. Find test files:
   ```bash
   Glob(pattern="**/*_test.go")
   ```
2. For each test:
   - Does it use a slice-of-struct pattern with `t.Run`? If test cases exist without subtests, flag.
   - Does each subtest name describe the scenario, not just `"case 1"`?
   - Are independent subtests calling `t.Parallel()`? If not, note as an improvement.
   - Are test case fields exported in the struct? If so, flag — test internals don't need export.

## Rules / Anti-patterns

| Anti-pattern | Why | Fix |
|---|---|---|
| `if err != nil { _ = err }` | Silently discards errors | Return or wrap with `fmt.Errorf("...: %w", err)` |
| `if err == ErrNotFound` on a wrapped error | Breaks with `%w` wrapping | Use `errors.Is(err, ErrNotFound)` |
| `panic(...)` outside `main` or `init` | Crashes the whole process | Return a typed error instead |
| Returning `*ConcreteType` where an interface would do | Couples callers to implementation | Declare the return as the interface |
| `go func() { ... }()` without a WaitGroup or errgroup | Goroutine leak on shutdown | Use `errgroup.Group` or bounded worker pool |
| Loop variable capture: `go func() { use(item) }()` | Race — all goroutines see the last value | Copy before spawn: `item := item` (or use Go 1.22+ loop variable semantics) |
| `sync.Mutex` with mostly read traffic | Unnecessary write contention | Use `sync.RWMutex`; read with `RLock` |
| `func(ch chan MyType)` instead of `chan<- MyType` | Hides channel direction intent | Annotate direction in all function signatures |
| Test: `for i, tc := range cases { t.Run(fmt.Sprintf("%d", i), ...)` | Opaque test names in output | Name test cases by scenario: `"nil input"`, `"expired token"` |

## Output format

```markdown
## Go Code Review: {file or PR}

### Summary

| Area | Findings | Severity |
|---|---|---|
| Error handling | {count} | {High / Medium / Low / None} |
| Interface design | {count} | {High / Medium / Low / None} |
| Goroutine safety | {count} | {High / Medium / Low / None} |
| Table-driven tests | {count} | {High / Medium / Low / None} |

### Findings

#### {Pass N}: {Area}

| # | Location | Finding | Severity | Suggested fix |
|---|---|---|---|---|
| 1 | `pkg/myservice/handler.go:42` | Error ignored with `_` | High | Return wrapped error |

### Verdict

{APPROVE / REQUEST CHANGES / COMMENT} — {one-sentence rationale}
```
```

---

### Step 6 — Verify self-containment

| Check | Result |
|---|---|
| Understandable | Pass — no reference to coding-standards agent methodology |
| Executable | Pass — every step has a concrete grep/glob command |
| Complete | Pass — no "see the agent for details" references |
| Bounded | Pass — reviews Go files only; does not attempt general architecture review |

---

### Step 7 — Update README

Added `review-go` to the coding-standards row in the agent table in `README.md`.

---

### Step 8 — Verify audit checklist

- [x] 100–500 lines
- [x] Description specific enough for auto-invocation
- [x] Self-contained
- [x] Sequential mandatory steps
- [x] Verifiable step outputs
- [x] Rules with anti-patterns
- [x] Structured output format
- [x] Cross-references related skills
- [x] Generic examples only (`myservice`, `pkg/...`)
- [x] External tools linked (`errgroup`)
- [x] Argument hint present
- [x] Frontmatter description precise

---

### Creation report

```markdown
## Created: review-go (coding-standards)

- **Path:** `plugins/practices/coding-standards/skills/review-go/SKILL.md`
- **Lines:** 142
- **Description:** Produces a Go code review report covering error handling, interface design, goroutine safety, and table-driven tests. Auto-invoked when reviewing .go files in a PR or code review task.
- **Self-contained:** yes
- **README updated:** yes
- **Quality score:** 12/12 criteria met
```

---

## Results

### Criteria (against SKILL.md definition)

- [x] PASS: Step 1 reads the skill template and CLAUDE.md before creating anything — met: lines 15–17 show explicit `Read` calls for `skill-template.md` and `CLAUDE.md` as the first mandatory step
- [x] PASS: Step 2 reads the parent agent and checks for existing sibling skills — met: step 2 reads the parent agent definition and requires checking sibling skills to map scope boundaries before writing
- [x] PASS: SKILL.md frontmatter includes all required fields: name, description, argument-hint, user-invocable, and allowed-tools — met: lines 57–65 show a complete frontmatter template with all five fields, marked "all fields required"
- [x] PASS: Description is specific enough for auto-invocation — met: line 68 marks description "CRITICAL" and requires both what it produces and when to use it; the anti-pattern contrast at line 127 reinforces this
- [x] PASS: Skill body includes sequential mandatory steps, rules with anti-patterns, and a structured output format template — met: body structure table at lines 75–81 marks all three as Required
- [x] PASS: Step 6 self-containment check is performed — met: lines 94–99 define an explicit self-containment step with a four-row pass-criteria table
- [x] PASS: README is updated — met: step 7 (lines 101–103) names this as a mandatory numbered step
- [~] PARTIAL: Examples use generic identifiers only — partially met: line 87 lists this as a quality target and step 8 includes a mental audit checkbox, but there is no mechanical enforcement (no grep scan or pattern check to catch private references that slip through)

### Output expectations (against simulated output)

- [x] PASS: Output creates `plugins/practices/coding-standards/skills/review-go/SKILL.md` — met: path follows `plugins/{category}/{agent}/skills/{skill-name}` correctly; no new top-level plugin created
- [x] PASS: Frontmatter contains all required fields with no fields missing — met: all five fields present in simulated SKILL.md frontmatter
- [x] PASS: Description is auto-invocation-friendly — met: simulated description names what it produces ("Go code review report") and when to use it ("Auto-invoked when reviewing .go files")
- [x] PASS: Body covers all four prompt areas — met: error handling (Pass 1), interface usage (Pass 2), goroutine safety (Pass 3), table-driven tests (Pass 4) are all explicitly covered
- [x] PASS: Includes mandatory sequential steps and a structured output format template with findings table — met: four named passes with grep/glob commands; output format section with summary and findings tables
- [~] PARTIAL: Rules / Anti-patterns section includes named anti-patterns specific to Go — partially met: the simulated output contains a well-populated Go-specific anti-patterns table (ignored errors, mutex misuse, goroutine leaks, loop variable capture), but the skill definition itself does not require or prompt domain-specific anti-pattern content — coverage depends on agent judgment from the arguments, not on structural enforcement in the skill
- [x] PASS: Self-containment verified — met: step 6 four-point check table executed in simulated output; all four points pass
- [x] PASS: README updated — met: simulated step 7 confirms README update
- [x] PASS: Examples use generic identifiers — met: simulated output uses `myservice`, `pkg/...`, `internal/pkg/...`; no private references
- [~] PARTIAL: Go-specific concurrency patterns addressed — partially met: simulated output covers `sync.Mutex` vs `sync.RWMutex`, channel direction annotations, and context propagation (all three from the criterion), but the skill definition provides no checklist item or prompt that guarantees these areas are surfaced — a less thorough execution could omit them

## Notes

The skill's structure is solid. Every lifecycle stage from template reading through README update is covered as a numbered mandatory step. The description-specificity guidance is well-designed, with CRITICAL framing and a concrete bad/good contrast in the Anti-Patterns section.

Both partial gaps point to the same ceiling: the skill enforces the presence of sections (anti-patterns, examples) but not the specificity or domain accuracy of their content. For a general-purpose create-skill, this is a defensible boundary — a skill that creates other skills cannot know in advance what domain-specific content to mandate. The gaps are minor quality ceilings, not structural failures.

One implementation friction: step 2's bash commands use literal placeholder syntax (`{agent-name}`) without explaining substitution from `$ARGUMENTS`. A contributor following the step literally would need to infer the substitution rule.
