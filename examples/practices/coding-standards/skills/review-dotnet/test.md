# Test: review-dotnet handler loop violation

Scenario: A developer submits a PR containing a .NET message handler with a foreach loop that performs I/O on each iteration — a direct violation of the "one message, one unit of work" rule.

## Prompt

Review this PR. The main change is in `OrderProcessor.cs` — we added a `HandleBatchOrdersCommand` handler that loops over a list of order IDs and calls `_repository.SaveAsync(order)` inside the loop for each one. There's also a new `OrderSummaryController.cs` with a `/api/orders` endpoint that fetches all orders then filters in memory with `.Where()`. Finally, `CreateChildWorkItemHandler.cs` creates a new `WorkItem` aggregate from a `WorkItemTriggered` event but doesn't check whether the aggregate already exists — if the event replays, it'll try to create a duplicate.

A few specifics for the response (output structured per the review-dotnet template):

- **Run all 7 passes** in order. Even passes with no findings get a "Pass N: 0 findings" line — never silently omit. Passes are: Pass 1 (one message, one unit of work), Pass 2 (cascading handler chains), Pass 3 (API design — list endpoints filter in DB), Pass 4 (idempotency guards on creation handlers), Pass 5 (event-sourcing semantics), Pass 6 (analyser compliance), Pass 7 (testing).
- **Per-pass summary table at the top**:
  ```
  | Pass | Topic | Findings |
  |------|-------|----------|
  | 1 | One message, one unit of work | 1 |
  | 2 | Cascading handler chains | 0 |
  | 3 | API design | 1 |
  | 4 | Idempotency guards | 1 |
  | 5 | Event-sourcing semantics | 0 |
  | 6 | Analyser compliance | 0 (no analyser changes in diff) |
  | 7 | Testing | 0 (no test changes in diff — recommend tests for new handlers in follow-up) |
  ```
- **Each finding uses the structured field format**: `**Severity:** HIGH/MEDIUM/LOW | **Pass:** N | **File:** path:line | **Evidence:** \`code snippet\` | **Standard violated:** [named rule] | **Fix:** [concrete code or pattern]`. Three findings expected:
  - **Pass 1, HIGH** — `OrderProcessor.cs::HandleBatchOrdersCommand` loops over orders calling `_repository.SaveAsync(order)` inline. Standard: "one message, one unit of work — orchestration handlers MUST publish one independent message per item, not loop inline." Fix: publish `SaveOrderCommand` per item, let the bus handle each in its own transaction.
  - **Pass 3, HIGH** — `OrderSummaryController.cs::/api/orders` filters with `.Where()` after fetching all orders. WHY: memory blow-up at scale, slow under load, breaks pagination semantics. Fix: translate filter into LINQ-to-Marten / `IQueryable` so it executes in the database.
  - **Pass 4, HIGH** — `CreateChildWorkItemHandler.cs` creates `WorkItem` aggregate without existence check. Standard: "idempotency guards on creation handlers." Replay causes: Wolverine retries on transient failure, manual replay during recovery, projection rebuild. Fix: `try { repository.Get(aggregateId); return; } catch (AggregateNotFound) { /* proceed */ }`.
- **Cross-references at end (mandatory final section)**: `## Related skills` listing `/coding-standards:review-standards` (cross-cutting quality) and `/coding-standards:review-git` (commit/PR conventions) for follow-up review passes.

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
