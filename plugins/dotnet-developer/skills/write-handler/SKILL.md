---
name: write-handler
description: Write a Wolverine command handler with aggregate loading and cascading messages.
argument-hint: "[handler description, e.g. 'TriggerCrawlExtraction']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.cs"
---

Write a Wolverine handler for $ARGUMENTS.

## Pattern

```csharp
[AggregateHandler]
public static class MyHandler
{
    public static async Task<object?> Handle(
        MyCommand command,
        MyAggregate aggregate,
        IDocumentSession session)
    {
        // One thing, return next command
    }
}
```

## Rules

- `[AggregateHandler]` for automatic aggregate loading from Marten
- One message, one unit of work — never loop through N items inline
- Managed sessions only (`IDocumentSession`, never `store.LightweightSession()`)
- Cascading returns publish follow-on commands
- Polymorphic cascade: return `object?` for branching
- Non-fatal failures caught and logged — pipeline continues
- Constructor injection for external dependencies
- Unit test with NSubstitute mocks + integration test via Alba
