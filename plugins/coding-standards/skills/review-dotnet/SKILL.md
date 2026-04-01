---
name: review-dotnet
description: Review .NET / C# code against team conventions. Auto-invoked when reviewing .cs files.
allowed-tools: Read, Grep, Glob, Bash
paths:
  - "**/*.cs"
---

When reviewing .NET / C# code, check against these standards:

- One message, one unit of work — no loops with heavy inline work
- `[AggregateHandler]` with cascading returns, not manual event publishing
- Static `LoadAsync` for pre-conditions on endpoints
- All list endpoints: pagination + sort + text filter, always in the database
- Hierarchical API URLs matching entity ownership
- External dependencies behind interfaces (constructor injection)
- BDD test naming: `WhenDoingSomething`
- Central package management via `Directory.Packages.props`
- Analysers enforced as warnings-as-errors

For each violation found, report:
1. The file and line
2. Which standard is violated
3. A concrete suggestion for fixing it

Summarize findings grouped by severity: critical, important, suggestion.
