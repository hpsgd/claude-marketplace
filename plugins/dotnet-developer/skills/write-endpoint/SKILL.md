---
name: write-endpoint
description: Write a Wolverine HTTP endpoint with pre-conditions, handler, and tests.
argument-hint: "[endpoint description, e.g. 'GET /api/sources/{id}/crawls']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.cs"
---

Write a Wolverine endpoint for $ARGUMENTS.

## Pattern

```csharp
public static class MyEndpoint
{
    // Pre-conditions (returns ProblemDetails to short-circuit)
    public static async Task<ProblemDetails?> LoadAsync(/* params */) { }

    // Handler (instance method on aggregate for decisions)
    [WolverinePost("/api/...")]
    public MyEvent Handle(MyCommand command) { }
}
```

## Checklist

- [ ] Static `LoadAsync` for pre-conditions
- [ ] Instance `Handle` on the aggregate
- [ ] Return events as cascading messages
- [ ] Hierarchical URL matching entity ownership
- [ ] List endpoints: pagination + sort + filter in the database
- [ ] Return `PagedResult<T>` for list endpoints
- [ ] Unit test (handler logic)
- [ ] Integration test (full HTTP round-trip via Alba)
