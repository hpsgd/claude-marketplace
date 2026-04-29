# Test: create-skill new skill for existing agent

Scenario: A contributor asks the create-skill skill to add a `review-go` skill to the coding-standards agent, covering Go-specific conventions for type safety, error handling, and testing patterns.

## Prompt

/create-skill review-go for coding-standards — Go code review skill covering error handling patterns, interface usage, goroutine safety, and table-driven tests.

## Criteria

- [ ] PASS: Step 1 reads the skill template and CLAUDE.md before creating anything
- [ ] PASS: Step 2 reads the parent agent (coding-standards) and checks for existing sibling skills to understand boundaries and avoid duplication
- [ ] PASS: SKILL.md frontmatter includes all required fields: name, description, argument-hint, user-invocable, and allowed-tools
- [ ] PASS: Description is specific enough for auto-invocation — includes what it produces and when to use it, not just "helps review Go code"
- [ ] PASS: Skill body includes sequential mandatory steps, rules with anti-patterns, and a structured output format template
- [ ] PASS: Step 6 self-containment check is performed — skill is verified to work without reading the parent agent
- [ ] PASS: README is updated to add review-go to the coding-standards agent's skill list
- [ ] PARTIAL: Examples in the skill use generic identifiers (e.g., `myservice`, `@org/shared`) — no private company names or internal package references

## Output expectations

- [ ] PASS: Output creates `plugins/practices/coding-standards/skills/review-go/SKILL.md` (or the equivalent path for the existing coding-standards plugin) — not a new top-level plugin
- [ ] PASS: Output's frontmatter contains all required fields — name (`review-go`), description, argument-hint, user-invocable, allowed-tools — with no fields missing
- [ ] PASS: Output's description is auto-invocation-friendly — names what the skill produces (Go code review report) and when to use it (`Auto-invoked when reviewing .go files`), not just "helps review Go code"
- [ ] PASS: Output's body covers the four areas from the prompt — error handling patterns (named return errors, sentinel errors vs wrapped errors with `errors.Is`/`errors.As`), interface usage (small interfaces, accept interfaces / return structs), goroutine safety (race detection, channel ownership, context cancellation), and table-driven tests (subtests with `t.Run`)
- [ ] PASS: Output includes mandatory sequential steps (similar to other review skills — Pass 1, Pass 2, etc.) and a structured output format template with findings table
- [ ] PASS: Output includes a Rules / Anti-patterns section with named anti-patterns specific to Go — e.g. ignored errors with `_`, panicking outside main / init, returning concrete types where an interface is expected, unbounded goroutine spawning
- [ ] PASS: Output's self-containment is verified — the skill works when invoked without reading the parent coding-standards agent, with all required Go-specific guidance inside SKILL.md
- [ ] PASS: Output updates README.md to add `review-go` to the coding-standards skill list — and updates the parent coding-standards agent's skill cross-reference if applicable
- [ ] PASS: Output's examples use generic identifiers (`myservice`, `@org/shared`, `internal/pkg/...`) — no private company names, no internal Go module paths
- [ ] PARTIAL: Output addresses Go-specific concurrency review patterns — `sync.Mutex` vs `sync.RWMutex` choice, channel direction (`chan<-` / `<-chan`) in function signatures, context propagation as the first parameter
