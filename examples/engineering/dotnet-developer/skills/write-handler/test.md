# Test: Write handler for processing crawl completion

Scenario: Developer invokes the write-handler skill for a `CompleteCrawl` command handler. When a crawl completes, it should update the crawl status, record the completion time, and fan out to trigger extraction of each crawled page independently.

## Prompt

Write a handler for `CompleteCrawl`. The crawl has a list of pages (each with an ID and URL). When completed: mark the crawl status as Completed, set CompletedAt to now, then trigger extraction for each page as an independent unit of work. Each page extraction is a separate `ExtractPage` message. Use AggregateHandler pattern.

## Criteria

- [ ] PASS: Skill reads existing handlers before writing — matches `[AggregateHandler]` usage, return type conventions, and test naming patterns
- [ ] PASS: Handler fans out with `IEnumerable<ExtractPage>` return — does not loop through pages inline in a single handler
- [ ] PASS: Handler uses managed `IDocumentSession` injected as a method parameter — does not create sessions from `IDocumentStore`
- [ ] PASS: Skill does not call `SaveChangesAsync` manually — notes Wolverine manages the session lifecycle
- [ ] PASS: `CompleteCrawl` command record has an `Id` property (or `CrawlId`) to enable automatic aggregate loading
- [ ] PASS: Unit test class is named `WhenCompletingACrawl` and uses Shouldly assertions
- [ ] PASS: Integration test uses `Host.InvokeMessageAndWaitAsync` and verifies the crawl status after processing
- [ ] PARTIAL: Skill includes error handling guidance — distinguishes fatal errors (let propagate for Wolverine retry) from non-fatal errors (catch, log, return null)
- [ ] PASS: Output delivers handler class, command/event records, unit test, integration test, and evidence of tests passing

## Output expectations

- [ ] PASS: Output's handler is decorated with `[AggregateHandler]` (or matches the established convention) and operates on the Crawl aggregate, with the `CompleteCrawl` command and `Crawl` aggregate both as parameters
- [ ] PASS: Output's `CompleteCrawl` command record has an `Id` (or `CrawlId`) property — without it, automatic aggregate loading by ID won't work
- [ ] PASS: Output's command and emitted events (`CrawlCompleted`, `ExtractPage`) are C# `record` types with immutable properties, not classes
- [ ] PASS: Output emits a `CrawlCompleted` event recording the new status and `CompletedAt` timestamp via the aggregate (event sourcing) — not by mutating fields directly
- [ ] PASS: Output's handler returns `IEnumerable<ExtractPage>` (or yields one per page) so each page extraction is a separate Wolverine message processed in its own transaction — NOT looped inline
- [ ] PASS: Output's handler accepts `IDocumentSession` as a method parameter where persistence is needed and never instantiates a session from `IDocumentStore`, and never calls `SaveChangesAsync` manually
- [ ] PASS: Output's unit test class is named `WhenCompletingACrawl` and uses Shouldly assertions, asserting on the resulting events (not on persisted state in unit tests)
- [ ] PASS: Output's integration test uses `Host.InvokeMessageAndWaitAsync(new CompleteCrawl(...))` and verifies, after waiting, that the crawl status is `Completed` and that one `ExtractPage` message per page was published
- [ ] PASS: Output includes evidence of the tests running and passing (command + exit code or test output snippet)
- [ ] PARTIAL: Output's error handling guidance distinguishes fatal errors (let propagate so Wolverine retries) from non-fatal/expected errors (catch and short-circuit) — explicit policy, not silent try/catch
