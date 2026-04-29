# Test: review-dotnet handler loop violation

Scenario: A developer submits a PR containing a .NET message handler with a foreach loop that performs I/O on each iteration — a direct violation of the "one message, one unit of work" rule.

## Prompt

Review this PR. The main change is in `OrderProcessor.cs` — we added a `HandleBatchOrdersCommand` handler that loops over a list of order IDs and calls `_repository.SaveAsync(order)` inside the loop for each one. There's also a new `OrderSummaryController.cs` with a `/api/orders` endpoint that fetches all orders then filters in memory with `.Where()`. Finally, `CreateChildWorkItemHandler.cs` creates a new `WorkItem` aggregate from a `WorkItemTriggered` event but doesn't check whether the aggregate already exists — if the event replays, it'll try to create a duplicate.

## Criteria

- [ ] PASS: Skill executes all seven mandatory passes — does not skip any pass
- [ ] PASS: Loop inside handler (`foreach` with `_repository.SaveAsync`) is flagged as a Pass 1 finding with file name and line-level evidence
- [ ] PASS: In-memory filtering on a list endpoint is flagged as a Pass 3 finding (list endpoints must filter in the database query, not in memory)
- [ ] PASS: Each finding follows the evidence format — severity, pass label, file path, evidence, standard violated, and a concrete fix
- [ ] PASS: Output uses the defined output template with summary counts per pass category
- [ ] PASS: Zero-finding gate is respected — skill does not fabricate additional findings where none exist
- [ ] PARTIAL: Pass 6 (analyser compliance) and Pass 7 (testing) are run even when no new test files are in the diff — at minimum the skill confirms the passes were executed
- [ ] PASS: Missing idempotency guard on creation handler is flagged — `CreateChildWorkItemHandler` creates an aggregate without checking if it already exists, risking duplicate-version conflicts on event replay
- [ ] PASS: Related skills are referenced at the end of the output (review-standards and review-git)

## Output expectations

- [ ] PASS: Output's loop-in-handler finding cites `OrderProcessor.cs::HandleBatchOrdersCommand` with line-level evidence of the `foreach` and the `_repository.SaveAsync(order)` call — not generic "the handler has a loop"
- [ ] PASS: Output's loop-in-handler finding explains the violation of "one message, one unit of work" — a failure mid-loop leaves some orders saved and others not, with no compensation, and prescribes the fix (publish one `SaveOrder` message per order and let the bus dispatch each)
- [ ] PASS: Output's in-memory-filter finding cites `OrderSummaryController.cs::/api/orders` and explains why filtering with `.Where()` after fetching all orders is wrong (memory blow-up at scale, slow under load, breaks pagination semantics) with the fix (translate filter to LINQ-to-Marten / IQueryable in the database)
- [ ] PASS: Output's idempotency-guard finding cites `CreateChildWorkItemHandler.cs` and shows the missing existence check — explaining that `WorkItemTriggered` events can replay (Wolverine retries, manual replay, recovery), and the fix pattern (try `repository.get(id)` → if found return; on `AggregateNotFound` create) consistent with the project's idempotency guard rule
- [ ] PASS: Output's findings each include severity, the pass label (Pass 1, 3, etc.), file path, evidence snippet, the standard violated (named or quoted), and a concrete fix — not just a list of issues
- [ ] PASS: Output runs all seven mandatory passes and reports per-pass finding counts in the summary — even passes with no findings get a "0 findings" line, not silently omitted
- [ ] PASS: Output respects the zero-finding gate on passes that genuinely have no issues — does NOT fabricate findings to fill quota
- [ ] PASS: Output runs Pass 6 (analyser compliance) and Pass 7 (testing) even though no test files are in the diff — at minimum confirming the passes ran and noting that the new handlers should be paired with tests in a follow-up
- [ ] PASS: Output's overall verdict reflects the severity of the findings — at least one HIGH/blocker finding (loop-in-handler is a correctness blocker for atomicity), so the verdict is REQUEST_CHANGES not APPROVE
- [ ] PASS: Output cross-references related skills at the end — `/coding-standards:review-standards` and `/coding-standards:review-git` — for follow-up reviews
