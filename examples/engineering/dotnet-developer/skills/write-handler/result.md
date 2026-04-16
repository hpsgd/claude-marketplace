# Write handler for processing crawl completion

Developer invokes the write-handler skill for a `CompleteCrawl` command handler. When a crawl completes, it should update the crawl status, record the completion time, and fan out to trigger extraction of each crawled page independently.

## Prompt

> Write a handler for `CompleteCrawl`. The crawl has a list of pages (each with an ID and URL). When completed: mark the crawl status as Completed, set CompletedAt to now, then trigger extraction for each page as an independent unit of work. Each page extraction is a separate `ExtractPage` message. Use AggregateHandler pattern.

Given the skill definition, a well-formed invocation of `write-handler` for this prompt would proceed as follows.

Step 1 (Reconnaissance) runs `grep -rn "AggregateHandler\|public static.*Handle("` to read existing handlers and match patterns before writing.

Step 2 routes to `[AggregateHandler]` with aggregate parameter — this handler operates on a Marten event-sourced aggregate.

Step 3 shows the `[AggregateHandler]` pattern: Wolverine loads the `Crawl` aggregate automatically from the command's `Id` property. The `CompleteCrawl` command must have `Id` (or `CrawlId`) for this to work.

The fan-out scenario maps directly to Step 4 (Cascading Returns) and Step 5 (One Message, One Unit of Work). Step 4 shows `IEnumerable<ExtractPage>` as the fan-out pattern explicitly. Step 5 labels inline loops "WRONG" and `IEnumerable<T>` return "CORRECT."

Step 6 (Session Management) states "Do not call `SaveChangesAsync` manually — Wolverine does it. Calling it yourself causes double-save." The managed session is injected as a method parameter.

Step 7 (Error Handling) distinguishes fatal errors (let propagate) from non-fatal errors (catch, log, return null) with code examples for both.

Step 9 produces a unit test class (`WhenTriggeringCrawlExtraction` in the example — the naming pattern would yield `WhenCompletingACrawl` for this handler) with Shouldly assertions, and an integration test using `Host.InvokeMessageAndWaitAsync`.

The Output section lists all five required artefacts including evidence (command + exit code).

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill reads existing handlers before writing — Step 1 requires `grep -rn "AggregateHandler\|public static.*Handle("` before writing anything. Steps 1.2-1.5 identify the aggregate, message, side effects, and existing message types.
- [x] PASS: Handler fans out with `IEnumerable<ExtractPage>` return — Step 4 shows "Fan-out — return IEnumerable for N cascading messages" with explicit code: `return command.PageIds.Select(pageId => new ExtractPage(...))`. Step 5 labels the inline loop anti-pattern "WRONG" and the `IEnumerable<T>` fan-out "CORRECT" with explanation.
- [x] PASS: Handler uses managed `IDocumentSession` injected as a method parameter — Step 6 code example shows `IDocumentSession session` as a method parameter. Anti-Patterns section lists "Manual sessions — `store.LightweightSession()` bypasses Wolverine's unit of work."
- [x] PASS: Skill does not call `SaveChangesAsync` manually — Step 6 rule: "Do not call `SaveChangesAsync` manually — Wolverine does it. Calling it yourself causes double-save." Anti-Patterns section repeats: "Manual SaveChangesAsync — Wolverine calls it. Calling it yourself causes double-save."
- [x] PASS: `CompleteCrawl` command record has `Id` property — Step 3 `[AggregateHandler]` rules: "The command MUST have an `Id` property (or a property named `{AggregateName}Id`) that maps to the aggregate identity." Anti-Patterns section: "Missing aggregate ID on command — `[AggregateHandler]` can't load without an `Id` property."
- [x] PASS: Unit test class named `WhenCompletingACrawl` with Shouldly assertions — Step 9 unit test example uses `WhenTriggeringCrawlExtraction` with the pattern `When[VerbingTheNoun]`. Shouldly assertions (`ShouldBeOfType`, `ShouldBeNull`, `ShouldBe`) are used throughout. The naming convention transfers directly to `WhenCompletingACrawl`.
- [x] PASS: Integration test uses `Host.InvokeMessageAndWaitAsync` — Step 9 integration test shows `await Host.InvokeMessageAndWaitAsync(new TriggerCrawlExtraction(crawl.Id))` explicitly, followed by loading the aggregate and asserting its state.
- [~] PARTIAL: Skill includes error handling guidance distinguishing fatal from non-fatal — Step 7 provides full code examples for both categories, explicit rule bullets, and logging guidance. The coverage is thorough. The criterion is prefixed PARTIAL so maximum score is 0.5 per rubric rules.
- [x] PASS: Output delivers all required artefacts with evidence — Output section lists all five: handler class, command and event records, unit test with NSubstitute mocks, integration test via Alba or message invocation, and evidence (command + exit code).

## Notes

The fan-out criterion is particularly well-supported: Step 4 provides the `IEnumerable<ExtractPage>` pattern with code, and Step 5 spends a full section labelling the inline loop "WRONG" with a four-point explanation of why. A developer following this skill would not produce an inline loop for this scenario.

The unit test criterion relies on a naming pattern transfer from the example (`WhenTriggeringCrawlExtraction`) to the specific scenario (`WhenCompletingACrawl`). The pattern is clear enough that this is a straightforward pass, not a stretch.

The error handling coverage in Step 7 is detailed enough that the PARTIAL ceiling undersells the definition's quality on this criterion. The limitation is the rubric rule, not the skill content.
