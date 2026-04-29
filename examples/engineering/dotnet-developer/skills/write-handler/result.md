# Result: Write handler for processing crawl completion

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18.5/19 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill reads existing handlers before writing — Step 1 greps for `AggregateHandler` and `public static.*Handle(` before writing anything.
- [x] PASS: Handler fans out with `IEnumerable<ExtractPage>` return — Step 3 primary example returns `(CrawlCompleted, IEnumerable<ExtractPage>)`; Step 5 labels inline loops "WRONG" and `IEnumerable<T>` fan-out "CORRECT" with rationale.
- [x] PASS: Handler uses managed `IDocumentSession` injected as a method parameter — Step 6 shows correct injection and the anti-patterns section forbids `IDocumentStore`.
- [x] PASS: Skill does not call `SaveChangesAsync` manually — Step 6 states "Do not call `SaveChangesAsync` manually — Wolverine does it. Calling it yourself causes double-save." Anti-Patterns repeats this.
- [x] PASS: `CompleteCrawl` command record has an `Id` property — Step 3 rules: "The command MUST have an `Id` property (or a property named `{AggregateName}Id`)." Anti-Patterns reinforces it.
- [x] PASS: Unit test class is named `WhenCompletingACrawl` and uses Shouldly assertions — Step 9 unit test example uses exactly this class name with `ShouldBeOfType`, `ShouldBe`, `ShouldBeGreaterThan`, `ShouldAllBe`.
- [x] PASS: Integration test uses `Host.InvokeMessageAndWaitAsync` and verifies crawl status after processing — Step 9 integration test uses `Host.TrackActivity().IncludeExternalTransports().InvokeMessageAndWaitAsync(new CompleteCrawl(crawlId))` and asserts `crawl!.Status.ShouldBe(CrawlStatus.Completed)`.
- [~] PARTIAL: Skill includes error handling guidance distinguishing fatal from non-fatal — Step 7 provides full code examples for both categories with explicit rules and logging guidance. Fully satisfied in substance; scored 0.5 per PARTIAL type.
- [x] PASS: Output delivers handler class, command/event records, unit test, integration test, and evidence of tests passing — Output section lists all five deliverables explicitly.

### Output expectations

- [x] PASS: Output's handler is decorated with `[AggregateHandler]` and operates on the Crawl aggregate with `CompleteCrawl` and `Crawl` as parameters — Step 3 primary example demonstrates this exactly.
- [x] PASS: Output's `CompleteCrawl` command record has an `Id` property — Step 3 rules and Anti-Patterns both enforce this; unit test example uses `new CompleteCrawl(crawl.Id)`.
- [x] PASS: Output's command and emitted events are C# `record` types — Step 3 AggregateHandler rules state "Commands and events are C# `record` types with immutable properties — never classes with setters." Anti-Patterns repeats: "Classes for commands/events — commands and events are immutable `record` types, not classes with setters."
- [x] PASS: Output emits a `CrawlCompleted` event via the aggregate (event sourcing), not by mutating fields directly — Step 3 states "Return the event from `Handle` — Wolverine + Marten append it to the stream automatically" and "Never mutate aggregate fields directly (`crawl.Status = ...`) — the change won't be persisted as an event and is invisible on replay." Anti-Patterns: "Mutating event-sourced aggregates directly — `crawl.Status = ...` on an event-sourced aggregate is silently lost."
- [x] PASS: Output's handler returns `IEnumerable<ExtractPage>` so each page extraction is a separate Wolverine message — Step 3 example and Step 5 both show and enforce this.
- [x] PASS: Output's handler accepts `IDocumentSession` as a method parameter and never calls `SaveChangesAsync` manually — Steps 6 and Anti-Patterns enforce both constraints clearly.
- [x] PASS: Output's unit test class is named `WhenCompletingACrawl`, uses Shouldly, and asserts on resulting events — Step 9 unit test example matches all three requirements; the comment "Assert — on the events, not on mutated state" is explicit.
- [x] PASS: Output's integration test uses `Host.InvokeMessageAndWaitAsync` and verifies crawl status and one `ExtractPage` per page published — Step 9 integration test checks both `crawl!.Status.ShouldBe(CrawlStatus.Completed)` and `extracts.Count.ShouldBe(3)` with a `MessagesOf<ExtractPage>()` assertion.
- [ ] FAIL: Output includes evidence of the tests running and passing — the Output section lists "Evidence that tests pass (command + exit code)" as a deliverable, but the skill contains no example of what this looks like (no `dotnet test` snippet, no exit code sample). The instruction is present; the model is absent.
- [~] PARTIAL: Output's error handling guidance distinguishes fatal from non-fatal with explicit policy — Step 7 does this fully with code examples and named rules. Scored 0.5 per PARTIAL type.

## Notes

The edited skill is substantially improved over the prior run. The three previous failure points — record types for commands/events, event-sourced emit pattern, and unit test asserting on events — are all now explicitly addressed with rule statements and code examples.

The sole remaining gap is the evidence-of-passing criterion: the skill tells the agent to produce test output but provides no example of what that output looks like. This is a minor authoring gap. A developer would know to run `dotnet test` and paste the result, but without a model they may omit it or format it inconsistently.

The integration test in Step 9 now correctly uses `TrackedSession` via `Host.TrackActivity().InvokeMessageAndWaitAsync(...)` and asserts on both aggregate state and the count of `ExtractPage` messages published — the full pattern required by the output expectations.
