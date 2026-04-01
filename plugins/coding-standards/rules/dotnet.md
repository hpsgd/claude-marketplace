---
description: .NET / C# language conventions and project patterns
paths:
  - "**/*.cs"
  - "**/*.csproj"
  - "**/*.sln"
---

# .NET / C# Conventions

## Project structure
- Domain-sliced projects — each bounded context is a separate assembly
- Domain libraries don't reference each other — communicate via events
- Only host projects compose domain libraries

```
Solution.sln
├── Project.Api                          # Host app
├── Project.Common                       # Shared infrastructure
├── Project.<Domain>                     # Domain library
├── Project.<Domain>.Tests               # Unit tests
├── Project.<Domain>.Tests.Integration   # Integration tests
└── Project.Tests.Integration            # Shared integration infrastructure
```

## Package management
- Central package management via `Directory.Packages.props`
- Analysers enforced as warnings-as-errors via `Directory.Build.props`
- Use Meziantou, Roslynator, SonarAnalyzer

## API design
- Hierarchical URLs mirroring semantic entity ownership
- No flat top-level listings — every entity accessed through its parent chain
- All list endpoints support: pagination (`page`, `size`), sorting (sensible default), text filter (`?q=`)
- All three operations MUST be in the database — never fetch full result set to filter in memory
- Always return `PagedResult<T>` from list endpoints
- Optimistic concurrency via `lastUpdatedAt` (409 Conflict on mismatch)
- PATCH updates use RFC 7396 merge patch semantics

## Testing
- Test runner: xunit.v3 with Shouldly assertions and NSubstitute mocks
- BDD naming: test classes named `WhenDoingSomething`
- Pure domain logic, handler behaviour, endpoint logic in unit tests
- External dependencies (HTTP, AI/LLM) must be abstracted behind interfaces for faking
- Every new handler accepting an external dependency must use constructor injection

## External dependency abstraction
- HTTP fetching: abstract behind interfaces (e.g., `IContentFetcher`)
- AI/LLM calls: use `IChatClient` (Microsoft.Extensions.AI) abstraction
- Never use concrete HTTP clients or AI clients directly
