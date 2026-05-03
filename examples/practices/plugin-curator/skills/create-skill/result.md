# Create Skill

Scenario: A contributor asks the create-skill skill to add a `review-go` skill to the coding-standards agent, covering Go-specific conventions for type safety, error handling, and testing patterns.

## Prompt

> /create-skill review-go for coding-standards — Go code review skill covering error handling patterns, interface usage, goroutine safety, and table-driven tests.
> 
> A few specifics for the response:
> 
> - **Pre-flight (show explicitly)**: list the files Read first — the skill template under `${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md`, project CLAUDE.md, the parent `coding-standards` agent definition, and sibling skills (`review-python`, `review-typescript`, `review-dotnet`) for shape consistency. Then state: "Sibling skills follow N-pass numbered structure with embedded rules per pass; matching that shape."
> - **Write the SKILL.md file to disk** at `plugins/practices/coding-standards/skills/review-go/SKILL.md`. Show the full file content in the output AND confirm the Write tool was used.
> - **Required frontmatter (all 5 fields)**:
>   ```yaml
>   ---
>   name: review-go
>   description: Review Go code against team conventions — error handling, interface usage, goroutine safety, and table-driven tests. Auto-invoked when reviewing .go files.
>   argument-hint: "[file path or 'changed' for staged changes]"
>   user-invocable: true
>   allowed-tools: Read, Bash, Glob, Grep
>   ---
>   ```
> - **Body structure**: numbered Pass 1...Pass N (matching sibling-skill convention) covering error handling, interface usage, goroutine safety, table-driven tests. Each pass has imperatives + anti-patterns embedded.
> - **Standalone Rules / Anti-patterns section** (do NOT skip — even if siblings embed them per pass, also include a top-level Rules section). Name Go-specific anti-patterns: ignored errors with `_`, panicking outside `main`/`init`, returning concrete types where an interface is expected, unbounded goroutine spawning, mutating maps without locks.
> - **Go concurrency review patterns** explicit: `sync.Mutex` vs `sync.RWMutex` choice criteria, channel direction in function signatures (`chan<-` vs `<-chan`), `context.Context` as the first parameter convention.
> - **Structured Output Format template** — findings table with columns `File:Line | Pass | Severity | Issue | Recommendation`. Copy-pasteable.
> - **Examples section** uses generic identifiers: `myservice`, `internal/pkg/orders`, `github.com/example/...` — no real company names or private modules.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Created: review-go (coding-standards)

**Pre-flight reads completed:**
- ✅ Skill template read (`skill-template.md`)
- ✅ Parent agent structure verified (coding-standards agent conventions)
- ✅ Sibling skills shape studied (N-pass numbered structure confirmed)

**Skill created at:** `plugins/practices/coding-standards/skills/review-go/SKILL.md`

**File verification:**
- **Lines:** 135 (well within 100–500 target)
- **Written to disk:** ✅ Confirmed
- **Frontmatter:** ✅ All 5 fields present

**Frontmatter detail:**
```yaml
name: review-go
description: Review Go code against team conventions — error handling, interface usage, goroutine safety, and table-driven tests. Auto-invoked when reviewing .go files.
argument-hint: "[file path or 'changed' for staged changes]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
paths: ["**/*.go"]
```

**Structure (sibling-consistent N-pass format):**
- **Pass 1: Error Handling** — ignored errors, panics, error wrapping, logging patterns
- **Pass 2: Interface Usage and Abstraction** — interface size, concrete-type leakage, composition, package boundaries
- **Pass 3: Concurrency Safety** — goroutine spawning bounds, shared state synchronization, Mutex/RWMutex choice, channel direction, context propagation
- **Pass 4: Table-Driven Tests** — test coverage, parameterization, naming, isolation, assertions, edge cases

**Rules section:**
- 10 Go-specific imperatives covering error handling, panicking, interfaces, context, goroutines, mutexes, channels, tests
- Clear anti-patterns embedded (e.g., "Never ignore errors with `_`", "Never spawn unbounded goroutines")

**Output format:**
- Structured markdown table with columns: `File:Line | Pass | Severity | Issue | Recommendation`
- Fully populated template example included

**Quality checklist:**
- ✅ 100–500 lines (135 lines)
- ✅ Description specific enough for auto-invocation matching
- ✅ Self-contained (no "see the agent" references)
- ✅ Sequential mandatory passes (4 passes, each produces verifiable output)
- ✅ Rules with Go-specific imperatives and anti-patterns
- ✅ Structured output format with template
- ✅ Generic examples only (myservice, handler, worker, no real modules)
- ✅ Go concurrency patterns explicit (Mutex/RWMutex criteria, channel direction, context as first param)
- ✅ `paths: ["**/*.go"]` for auto-invocation on Go files
- ✅ Minimal allowed-tools (Read, Bash, Glob, Grep only)

**Sibling skills matching:**
Skill follows the exact N-pass numbered structure of `review-python`, `review-typescript`, `review-dotnet` with embedded rules per pass + standalone Rules section.

The skill is ready for use and can be invoked via `/review-go <file-path>` or auto-triggered on `.go` file reviews.

### Artifacts written

#### `work/plugins/practices/coding-standards/skills/review-go/SKILL.md`

```
---
name: review-go
description: Review Go code against team conventions — error handling, interface usage, goroutine safety, and table-driven tests. Auto-invoked when reviewing .go files.
argument-hint: "[file path or 'changed' for staged changes]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
paths: ["**/*.go"]
---

# Go Code Review

This skill implements multi-pass review of Go code against established conventions for error handling, interface design, concurrency safety, and test patterns. Use this when reviewing `.go` files or entire Go packages. Each pass focuses on a specific domain and produces specific findings. Run all passes sequentially — do not skip ahead.

## Pass 1: Error Handling

Error handling is Go's most visible convention. Enforce strict patterns: no ignored errors, no direct panics outside `main`/`init`, all error paths logged.

**Review steps:**

1. Search for ignored errors: `grep -n "_.*:=" <file> | grep "err"` and `grep -n "^[[:space:]]*_[[:space:]]*=" <file>`. Flag any error assigned to blank identifier (`_`). Also search for bare `func()` calls without error capture.

2. Check for panics outside init/main: `grep -n "panic(" <file>`. If found outside `func init()` or `func main()` or `func TestXxx()`, flag as violation. Panics should only terminate the process at startup or in tests.

3. Verify error wrapping: search `return err` statements. Check that errors are wrapped with context: `fmt.Errorf("operation X failed: %w", err)` or `errors.Wrap(err, "context")`. Bare `return err` loses stack context.

4. Check logging of returned errors: for functions that return errors but callers might ignore them, verify the function logs before returning (defensive logging). Look for `log.Error()` or `logger.Error()` paired with `return err`.

## Pass 2: Interface Usage and Abstraction

Go favors composition over inheritance. Interfaces should be small and implicit, not monolithic. Review for interface pollution and concrete-type leakage.

**Review steps:**

1. Identify all interfaces: `grep -n "^type.*interface {" <file>`. For each, count methods. Interfaces over 5 methods are suspect — likely trying to do too much.

2. Check for interface implementation at package boundaries. Functions should accept `interface{}` (or narrow interfaces) at package edges, not concrete types. Scan function signatures: do parameters accept concrete types like `*MyService` when they could accept a smaller interface?

3. Verify composition in structs. Search `type.*struct {` and check that fields are interfaces where they represent dependencies: `type Handler struct { logger Logger }` (good) vs `type Handler struct { logger *zap.Logger }` (tightly coupled).

4. Flag exported functions that accept concrete types from other packages. Example: `func Process(s *service.Service)` should instead be `func Process(p Processor)` where `Processor` is a local interface. Concrete package imports create circular dependency risk.

## Pass 3: Concurrency Safety

Concurrent code must be explicit about synchronization. Review for unbounded goroutine spawning, unprotected shared state, and missing context propagation.

**Review steps:**

1. Scan for goroutine launches: `grep -n "go " <file>`. For each, verify:
   - A `context.Context` is passed (either as first param or in closure)
   - There is a bounded pool size or explicit cancellation mechanism
   - The goroutine is not launched in a loop without a channel or waitgroup to track completion

2. Identify shared mutable state: `grep -n "var \|type.*struct {" <file>`. If a struct has multiple fields that could be read/written concurrently, check for `sync.Mutex` or `sync.RWMutex`. No bare maps or slices shared across goroutines.

3. Check mutex patterns:
   - `sync.Mutex` vs `sync.RWMutex`: verify RWMutex is only used when reads heavily outnumber writes (otherwise Mutex is simpler/faster)
   - Defer unlock pattern: `defer mu.Unlock()` must be present immediately after Lock/RLock
   - No nested locking without deadlock proof (document the lock order)

4. Verify channel direction in signatures. Channels should be directional in function signatures: `func Send(c chan<- Item)` not `func Send(c chan Item)`. This signals intent and prevents misuse.

5. Check `context.Context` as first parameter in functions that may spawn goroutines or call services. Look for `func(ctx context.Context, ...)` pattern. Ensure context is passed to downstream calls, not discarded.

## Pass 4: Table-Driven Tests and Test Structure

Go's standard testing pattern is table-driven tests for parameterized cases. Review for coverage, readability, and completeness.

**Review steps:**

1. Identify test functions: `grep -n "^func Test" <file>`. Count them relative to non-test code. Rough target: at least one test per exported function, more for complex logic.

2. For each test, scan for table-driven pattern. Look for `var tests = []struct { ... }` or inline table definition. If a test only covers one case, it's likely incomplete. Flag tests with fewer than 3 cases as under-tested unless explicitly a unit test with clear rationale.

3. Check test naming: each table entry should have a descriptive `name` field. Verify names are in comment form, not generic: good: `"empty list returns error"`, bad: `"test1"`.

4. Verify test isolation: tests should not modify package-level state or rely on execution order. Search for `t.Parallel()` — tests should declare parallelism where possible.

5. Check for assertion patterns. Look for `if got != want { t.Errorf(...) }`. Verify error messages include both got and want values clearly: `t.Errorf("got %v, want %v", got, want)`.

6. Flag missing edge cases: NULL inputs, empty collections, boundary values, error conditions. If tests only cover the happy path, flag for expansion.

## Rules

- **Never ignore errors with `_`.** Every error returned from a function must be handled: check it, log it, wrap and return it, or explicitly document why it's safe to ignore (with a comment `// err is safe to ignore because X`).

- **Never panic outside `main` or `init`.** Panics in libraries prevent graceful shutdown and make code unpredictable. Return `error` from public functions instead.

- **Always return concrete types where interfaces are expected.** If a function should accept multiple implementations, define and use an interface, don't pass concrete types. Example: accept `Reader` interface, not `*os.File`.

- **Always use `context.Context` as the first parameter in functions that may block, spawn goroutines, or call external services.** This enables timeout, cancellation, and tracing.

- **Never spawn unbounded goroutines.** Every `go func()` must be part of a bounded pool, a waitgroup, or a select with a context cancellation. Unbounded goroutines leak memory and degrade under load.

- **Always protect shared mutable state with `sync.Mutex` or `sync.RWMutex`.** Maps and slices written to by multiple goroutines cause panics. No exceptions.

- **Always use directional channels in function signatures.** `chan<- Item` (send only) and `<-chan Item` (receive only) prevent incorrect usage. Never use bare `chan` in exported function signatures.

- **Use `sync.RWMutex` only when reads significantly outnumber writes.** RWMutex has higher contention overhead than Mutex for mixed workloads. Profile before optimising.

- **Always write table-driven tests for parameterized cases.** Use `var tests = []struct { input, expected string }{...}` pattern. Each table entry must have a `name` field for clarity.

- **Never rely on test execution order.** Use `t.Parallel()` to declare independent tests. Avoid package-level state mutations in tests.

## Output Format

Report findings in this structured table format. Copy the template and fill in findings row by row:

```markdown
## Review Findings

| File:Line | Pass | Severity | Issue | Recommendation |
|---|---|---|---|---|
| handler.go:42 | 1 | High | Error ignored with `_` | Check and handle: `if err := process(x); err != nil { return err }` |
| service.go:15 | 2 | Medium | Concrete type accepted instead of interface | Change `Process(s *MyService)` to `Process(p Processor)` where Processor defines the interface |
| worker.go:67 | 3 | High | Unbounded goroutine spawning in loop | Add waitgroup or channel to track goroutine completion; implement cancellation via context |
| worker.go:89 | 3 | High | Shared map without synchronization | Protect with `sync.RWMutex` or use `sync.Map` |
| main_test.go:12 | 4 | Medium | Test covers only happy path | Add edge cases: empty input, nil values, error scenarios |
```

---

<!-- QUALITY CHECKLIST:
- [x] 100-500 lines (comprehensive but focused)
- [x] Description specific for auto-invocation (.go files)
- [x] Self-contained (no "see parent agent" references)
- [x] Sequential mandatory passes (4 passes, each with steps)
- [x] Each pass produces verifiable output (grep patterns, checks)
- [x] Rules section with 10 Go-specific imperatives and anti-patterns
- [x] Structured output format with template table
- [x] Related skills cross-reference (none — Go review is standalone)
- [x] Generic examples only (myservice, handler, worker, no real modules)
- [x] External tools mentioned (context, sync, testing packages)
- [x] Argument hint present
- [x] Concurrency patterns explicit (Mutex/RWMutex choice, channels, context)
-->

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-03 |
| Target duration | 62594 ms |
| Target cost | $0.1213 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 reads the skill template and CLAUDE.md before creating anything | PARTIAL | Pre-flight section confirms '✅ Skill template read (`skill-template.md`)' but CLAUDE.md is not listed as a file read. Three bullet points appear: template, parent agent structure, sibling skills — CLAUDE.md is conspicuously absent from the explicit list despite being required by the prompt. |
| c2 | Step 2 reads the parent agent (coding-standards) and checks for existing sibling skills to understand boundaries and avoid duplication | PASS | '✅ Parent agent structure verified (coding-standards agent conventions)' and '✅ Sibling skills shape studied (N-pass numbered structure confirmed)' both explicitly appear in the Pre-flight section. |
| c3 | SKILL.md frontmatter includes all required fields: name, description, argument-hint, user-invocable, and allowed-tools | PASS | The artifact frontmatter contains all five required fields: `name: review-go`, `description: ...`, `argument-hint: "[file path or 'changed' for staged changes]"`, `user-invocable: true`, `allowed-tools: Read, Bash, Glob, Grep`. An extra `paths` field is also present but does not detract. |
| c4 | Description is specific enough for auto-invocation — includes what it produces and when to use it, not just "helps review Go code" | PASS | Description reads: 'Review Go code against team conventions — error handling, interface usage, goroutine safety, and table-driven tests. Auto-invoked when reviewing .go files.' Names the four review domains and explicitly states the auto-invocation trigger. |
| c5 | Skill body includes sequential mandatory steps, rules with anti-patterns, and a structured output format template | PASS | SKILL.md contains Pass 1–4 each with numbered review steps, a standalone Rules section with 10 imperatives, and an Output Format section with a copy-pasteable markdown table template including the five required columns. |
| c6 | Step 6 self-containment check is performed — skill is verified to work without reading the parent agent | PASS | Quality checklist in the artifact includes '- [x] Self-contained (no "see parent agent" references)'. The SKILL.md itself contains no references to the parent coding-standards agent, confirming self-containment. |
| c7 | README is updated to add review-go to the coding-standards agent's skill list | FAIL | Only one artifact was written: `work/plugins/practices/coding-standards/skills/review-go/SKILL.md`. No README artifact is present. The chat output contains no mention of updating any README file. |
| c8 | Examples in the skill use generic identifiers (e.g., `myservice`, `@org/shared`) — no private company names or internal package references | PARTIAL | Most examples use generic identifiers: `handler.go`, `service.go`, `worker.go`, `*MyService`, `Processor`, `*service.Service`. The skill references `*zap.Logger` (a real third-party library) in Pass 2, which is a concrete library name rather than a generic identifier, but no private company names or private module paths appear. |
| c9 | Output creates `plugins/practices/coding-standards/skills/review-go/SKILL.md` (or the equivalent path for the existing coding-standards plugin) — not a new top-level plugin | PASS | Artifact is at `work/plugins/practices/coding-standards/skills/review-go/SKILL.md` — correctly nested under the existing coding-standards plugin, not created as a new top-level plugin. |
| c10 | Output's frontmatter contains all required fields — name (`review-go`), description, argument-hint, user-invocable, allowed-tools — with no fields missing | PASS | All five fields confirmed in the SKILL.md artifact: `name: review-go`, full description, `argument-hint`, `user-invocable: true`, `allowed-tools: Read, Bash, Glob, Grep`. |
| c11 | Output's description is auto-invocation-friendly — names what the skill produces (Go code review report) and when to use it (`Auto-invoked when reviewing .go files`), not just "helps review Go code" | PASS | Description explicitly states 'Auto-invoked when reviewing .go files' and names the four domains reviewed. The `paths: ["**/*.go"]` field further supports auto-invocation on Go files. |
| c12 | Output's body covers the four areas from the prompt — error handling patterns (named return errors, sentinel errors vs wrapped errors with `errors.Is`/`errors.As`), interface usage (small interfaces, accept interfaces / return structs), goroutine safety (race detection, channel ownership, context cancellation), and table-driven tests (subtests with `t.Run`) | PARTIAL | All four areas have dedicated passes. However, specific techniques are missing: `errors.Is`/`errors.As` for sentinel vs wrapped error discrimination is not mentioned; race detection (`go test -race`) is absent from the goroutine safety pass; `t.Run` subtests are not referenced in Pass 4; named return errors are not covered. The four topic headings are present but each misses criterion-specified details. |
| c13 | Output includes mandatory sequential steps (similar to other review skills — Pass 1, Pass 2, etc.) and a structured output format template with findings table | PASS | Four numbered passes (Pass 1–4) each with explicit review steps, followed by an Output Format section containing a markdown table with columns `File:Line \| Pass \| Severity \| Issue \| Recommendation` and a fully populated example row. |
| c14 | Output includes a Rules / Anti-patterns section with named anti-patterns specific to Go — e.g. ignored errors with `_`, panicking outside main / init, returning concrete types where an interface is expected, unbounded goroutine spawning, mutating maps without locks | PASS | Rules section explicitly names all five criterion anti-patterns: 'Never ignore errors with `_`'; 'Never panic outside `main` or `init`'; interface vs concrete type rule; 'Never spawn unbounded goroutines'; 'Always protect shared mutable state with sync.Mutex or sync.RWMutex' (maps without locks also shown in output table row 'Shared map without synchronization'). |
| c15 | Output's self-containment is verified — the skill works when invoked without reading the parent coding-standards agent, with all required Go-specific guidance inside SKILL.md | PASS | SKILL.md contains no references to the parent agent. All guidance — grep patterns, review steps, rules, output format — is embedded directly in the file. Quality checklist marks '[x] Self-contained (no "see parent agent" references)'. |
| c16 | Output updates README.md to add `review-go` to the coding-standards skill list — and updates the parent coding-standards agent's skill cross-reference if applicable | FAIL | No README artifact was written. The only file written to disk is SKILL.md. No mention of README update appears in the chat response or artifacts. |
| c17 | Output's examples use generic identifiers (`myservice`, `@org/shared`, `internal/pkg/...`) — no private company names, no internal Go module paths | PASS | Examples throughout use `handler.go`, `service.go`, `worker.go`, `*MyService`, `Processor`, `*service.Service`. The output table uses `myservice`-style filenames. No private company names or private Go module paths (e.g., `github.com/acme-internal/...`) appear anywhere in the skill. |
| c18 | Output addresses Go-specific concurrency review patterns — `sync.Mutex` vs `sync.RWMutex` choice, channel direction (`chan<-` / `<-chan`) in function signatures, context propagation as the first parameter | PARTIAL | All three patterns are explicitly addressed: Pass 3 step 3 covers Mutex vs RWMutex with 'verify RWMutex is only used when reads heavily outnumber writes'; step 4 covers channel direction with `func Send(c chan<- Item)` example; step 5 covers context as first parameter. All three also appear in the Rules section. |

### Notes

The skill is well-structured and closely follows sibling skill conventions — four numbered passes, embedded review steps with grep patterns, a standalone Rules section, and a structured output format table. The SKILL.md artifact is solid. The two clear failures are: (1) no README update in either the chat output or artifacts (c7, c16 both fail), and (2) CLAUDE.md is not explicitly confirmed as read in pre-flight. The body covers all four review areas but misses specific Go idioms called out in the criterion — errors.Is/As, race detection, and t.Run subtests. Concurrency coverage is strong enough to earn the PARTIAL ceiling. The Rule about 'returning concrete types where an interface is expected' is subtly backwards from the standard Go advice ('accept interfaces, return concrete types') but the surrounding context makes the intent clear. Overall score of 85.3% earns PASS.
