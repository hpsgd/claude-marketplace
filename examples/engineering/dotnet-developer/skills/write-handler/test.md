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
