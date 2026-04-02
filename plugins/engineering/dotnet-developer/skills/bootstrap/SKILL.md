---
name: bootstrap
description: "Bootstrap .NET conventions into the architecture documentation. Appends .NET-specific sections to docs/architecture/CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap .NET Conventions

Bootstrap .NET development conventions for **$ARGUMENTS**.

This skill does NOT create its own domain directory. It appends .NET-specific sections to `docs/architecture/CLAUDE.md`.

## Process

### Step 1: Verify architecture domain exists

```bash
mkdir -p docs/architecture
```

If `docs/architecture/CLAUDE.md` does not exist, stop and report that the architect bootstrap should run first.

### Step 2: Append .NET conventions to `docs/architecture/CLAUDE.md`

Check if `docs/architecture/CLAUDE.md` already contains a ".NET Conventions" section. If not, append the following:

```markdown

<!-- Added by dotnet-developer bootstrap v0.1.0 -->
## .NET Conventions

### Wolverine and Marten

- **Wolverine** for message handling (commands, events, HTTP endpoints)
- **Marten** for document DB and event store (PostgreSQL-backed)
- Use Wolverine's `[WolverineHandler]` conventions — no manual DI wiring
- Prefer Marten's `IDocumentSession` over raw SQL for document operations

### Event Sourcing and CQRS

- Commands mutate state via event streams — never update documents directly for event-sourced aggregates
- Projections build read models from event streams
- Use Marten's inline projections for simple cases, async projections for complex
- Event naming: past tense, domain language (e.g., `OrderPlaced`, `PaymentReceived`)
- Stream identity: `{AggregateType}-{id}` convention

### Testing

- **Alba** for integration testing of HTTP endpoints (in-process test server)
- **xUnit** as the test framework
- **NSubstitute** for mocking dependencies
- **Shouldly** for fluent assertions
- Test naming: `Should_{expected_behaviour}_When_{condition}`
- Use `IAlbaHost` for end-to-end handler testing with real Marten sessions

### Project Structure

```
src/
├── {Project}.Api/           # HTTP endpoints, middleware
├── {Project}.Domain/        # Aggregates, events, domain logic
├── {Project}.Application/   # Handlers (commands, queries, events)
├── {Project}.Infrastructure/ # Marten config, external services
tests/
├── {Project}.Tests.Unit/
├── {Project}.Tests.Integration/
└── {Project}.Tests.Alba/     # Alba HTTP integration tests
```

### Coding Style

- Nullable reference types enabled (`<Nullable>enable</Nullable>`)
- File-scoped namespaces
- Primary constructors for DI (C# 12+)
- Records for DTOs, events, and value objects
- `sealed` by default — unseal only when inheritance is needed

### .NET Tooling

| Tool | Purpose |
|------|---------|
| [SonarCloud](https://sonarcloud.io) | .NET code quality and coverage gate |
| [GitHub Actions](https://docs.github.com/en/actions) | `dotnet test` in CI on every PR |

### Available .NET Skills

| Skill | Purpose |
|-------|---------|
| `/dotnet-developer:write-endpoint` | Write a Wolverine HTTP endpoint |
| `/dotnet-developer:write-handler` | Write a Wolverine command/event handler |
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## .NET Developer Bootstrap Complete

### Files updated
- `docs/architecture/CLAUDE.md` — appended .NET Conventions section

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Configure Wolverine and Marten in `Program.cs`
- Set up Alba test project for integration testing
- Use `/dotnet-developer:write-endpoint` for new HTTP endpoints
- Use `/dotnet-developer:write-handler` for command/event handlers
```
