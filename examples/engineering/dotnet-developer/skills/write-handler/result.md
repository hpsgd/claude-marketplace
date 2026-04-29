# Result: Write handler for processing crawl completion

**Verdict:** PARTIAL
**Score:** 14.5/19 criteria met (76%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill reads existing handlers before writing — Step 1 mandates `grep -rn "AggregateHandler\|public static.*Handle("` before writing anything. Steps 1.2–1.5 then identify the aggregate, message, side effects, and existing types to reuse.
- [x] PASS: Handler fans out with `IEnumerable<ExtractPage>` return — Step 4 provides an explicit "Fan-out — return IEnumerable for N cascading messages" example. Step 5 labels the inline loop anti-pattern "WRONG" and the `IEnumerable<T>` fan-out "CORRECT" with a four-point rationale.
- [x] PASS: Handler uses managed `IDocumentSession` injected as a method parameter — Step 6 code shows `IDocumentSession session` as a method parameter. Anti-Patterns lists "Manual sessions — `store.LightweightSession()` bypasses Wolverine's unit of work."
- [x] PASS: Skill does not call `SaveChangesAsync` manually — Step 6 rule states "Do not call `SaveChangesAsync` manually — Wolverine does it. Calling it yourself causes double-save." Anti-Patterns repeats the constraint.
- [x] PASS: `CompleteCrawl` command record has `Id` property — Step 3 `[AggregateHandler]` rules: "The command MUST have an `Id` property (or a property named `{AggregateName}Id`) that maps to the aggregate identity." Anti-Patterns reinforces: "Missing aggregate ID on command — `[AggregateHandler]` can't load without an `Id` property."
- [x] PASS: Unit test class named `WhenCompletingACrawl` with Shouldly assertions — Step 9 unit test example uses `WhenTriggeringCrawlExtraction`, establishing the `When[VerbingTheNoun]` pattern. It transfers to `WhenCompletingACrawl`. Shouldly assertions (`ShouldBeOfType`, `ShouldBeNull`, `ShouldBe`) are used throughout.
- [x] PASS: Integration test uses `Host.InvokeMessageAndWaitAsync` — Step 9 integration test shows `await Host.InvokeMessageAndWaitAsync(new TriggerCrawlExtraction(crawl.Id))` followed by loading the aggregate and asserting updated state.
- [~] PARTIAL: Skill includes error handling guidance distinguishing fatal from non-fatal — Step 7 provides full code examples for both categories with clear rules and logging guidance. Coverage is thorough. Maximum is 0.5 per PARTIAL rubric ceiling.
- [x] PASS: Output delivers handler class, command/event records, unit test, integration test, and evidence — Output section lists all five artefacts explicitly including "evidence that tests pass (command + exit code)."

### Output expectations

- [x] PASS: Output's handler is decorated with `[AggregateHandler]` and operates on the Crawl aggregate with `CompleteCrawl` command and `Crawl` as parameters — Step 3 demonstrates this pattern directly.
- [x] PASS: Output's `CompleteCrawl` command record has an `Id` property — Step 3 rules and Anti-Patterns both enforce this; the skill would produce a command with the required identity property.
- [~] PARTIAL: Output's command and emitted events are C# `record` types — skill examples use records throughout (e.g., `new CrawlCompleted(crawl.Id)`, `new ExtractPage(...)`) but never states "use record types, not classes" as an explicit rule. A developer following the skill would likely use records by imitation, not by instruction. Partially met.
- [ ] FAIL: Output emits a `CrawlCompleted` event via the aggregate (event sourcing), not by mutating fields directly — the skill teaches CRUD mutation. Step 3's primary example does `crawl.Status = CrawlStatus.Extracting; crawl.ExtractionStartedAt = DateTimeOffset.UtcNow; session.Store(crawl)`. There is no `Raise()`, `Events.Append()`, `Apply()`, or any event-sourcing append pattern anywhere in the skill. A developer following this skill would mutate fields directly rather than emit domain events. This is a real gap: the `CompleteCrawl` scenario specifically calls for event sourcing semantics.
- [x] PASS: Output's handler returns `IEnumerable<ExtractPage>` — Steps 4 and 5 both show and enforce this pattern explicitly.
- [x] PASS: Output's handler uses injected `IDocumentSession` and never calls `SaveChangesAsync` — Steps 6 and Anti-Patterns section enforce both constraints clearly.
- [~] PARTIAL: Output's unit test is named `WhenCompletingACrawl` and uses Shouldly, asserting on resulting events — the naming pattern transfers cleanly. Shouldly is used. However, the unit test example in Step 9 asserts on a return value (cast to a concrete command type), not on an events list. Because the skill doesn't teach event-sourced aggregates with a separable events collection, "asserting on resulting events" doesn't map cleanly to the skill's output. Partially met.
- [~] PARTIAL: Output's integration test uses `Host.InvokeMessageAndWaitAsync` and verifies crawl status AND one `ExtractPage` message per page published — `InvokeMessageAndWaitAsync` is shown and the status assertion is present. But the skill's integration test example does not include any assertion on published outbound messages (no check that one `ExtractPage` per page was published). Half the requirement is covered.
- [x] PASS: Output includes evidence of tests running and passing — Output section: "Evidence that tests pass (command + exit code)."
- [~] PARTIAL: Output's error handling guidance distinguishes fatal from non-fatal with explicit policy — Step 7 does this well with code and rules. Maximum is 0.5 per PARTIAL ceiling.

## Notes

The most significant gap is the event-sourcing mutation issue. The skill consistently uses direct field mutation (`crawl.Status = ...`, `crawl.ExtractionStartedAt = ...`) rather than aggregate event emission. For the `CompleteCrawl` scenario, which explicitly requires event-sourced state change, a developer following this skill would produce a handler that sets fields and calls `session.Store()` — not one that appends a `CrawlCompleted` event to the aggregate stream. The skill's architecture section (Step 3) needs a separate example or note for event-sourced aggregates where state changes flow through `Apply` methods and domain events, not direct mutation.

The integration test gap (no assertion on outbound message count) is a subtler problem. `Host.InvokeMessageAndWaitAsync` verifies the pipeline executed, but verifying that N `ExtractPage` messages were published requires either an in-memory bus inspection or a message spy — neither is shown.

The fan-out criterion is the skill's strongest point: Steps 4 and 5 together make the `IEnumerable<T>` requirement unambiguous, with the inline loop explicitly labelled wrong and the fan-out pattern explicitly labelled correct with four reasons.
