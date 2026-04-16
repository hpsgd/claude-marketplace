# Test: review-dotnet handler loop violation

Scenario: A developer submits a PR containing a .NET message handler with a foreach loop that performs I/O on each iteration — a direct violation of the "one message, one unit of work" rule.

## Prompt

Review this PR. The main change is in `OrderProcessor.cs` — we added a `HandleBatchOrdersCommand` handler that loops over a list of order IDs and calls `_repository.SaveAsync(order)` inside the loop for each one. There's also a new `OrderSummaryController.cs` with a `/api/orders` endpoint that fetches all orders then filters in memory with `.Where()`. Both files are in the diff.

## Criteria

- [ ] PASS: Skill executes all seven mandatory passes — does not skip any pass
- [ ] PASS: Loop inside handler (`foreach` with `_repository.SaveAsync`) is flagged as a Pass 1 finding with file name and line-level evidence
- [ ] PASS: In-memory filtering on a list endpoint is flagged as a Pass 3 finding (list endpoints must filter in the database query, not in memory)
- [ ] PASS: Each finding follows the evidence format — severity, pass label, file path, evidence, standard violated, and a concrete fix
- [ ] PASS: Output uses the defined output template with summary counts per pass category
- [ ] PASS: Zero-finding gate is respected — skill does not fabricate additional findings where none exist
- [ ] PARTIAL: Pass 6 (analyser compliance) and Pass 7 (testing) are run even when no new test files are in the diff — at minimum the skill confirms the passes were executed
- [ ] PASS: Related skills are referenced at the end of the output (review-standards and review-git)
