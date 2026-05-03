# Review Dotnet

Scenario: A developer submits a PR containing a .NET message handler with a foreach loop that performs I/O on each iteration — a direct violation of the "one message, one unit of work" rule.

## Prompt

> Review this PR. The main change is in `OrderProcessor.cs` — we added a `HandleBatchOrdersCommand` handler that loops over a list of order IDs and calls `_repository.SaveAsync(order)` inside the loop for each one. There's also a new `OrderSummaryController.cs` with a `/api/orders` endpoint that fetches all orders then filters in memory with `.Where()`. Finally, `CreateChildWorkItemHandler.cs` creates a new `WorkItem` aggregate from a `WorkItemTriggered` event but doesn't check whether the aggregate already exists — if the event replays, it'll try to create a duplicate.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Three issues to flag, all well-defined by this project's conventions:

---

**1. `HandleBatchOrdersCommand` — N+1 saves inside a loop**

Calling `_repository.SaveAsync(order)` in a loop violates the "one message, one unit of work" rule. A failure on item 3 of 10 leaves items 1–2 saved and items 4–10 not, with no retry boundary. The handler should publish one independent command per order ID and let the message bus dispatch each in its own transaction. That makes each item individually retriable and a single failure doesn't poison the batch.

**2. `OrderSummaryController.cs` — in-memory `.Where()` on `/api/orders`**

Two violations here:

- Fetching the full result set and filtering in application memory is explicitly prohibited — all filtering, sorting, and pagination must happen in the database.
- The endpoint must return `PagedResult<T>` and accept `page`, `size`, and `?q=` query parameters. There's also a question of whether a flat `/api/orders` listing should exist at all — the convention is hierarchical URLs through the parent chain, not flat top-level collections.

**3. `CreateChildWorkItemHandler.cs` — missing idempotency guard**

On event replay, this handler will attempt to create a `WorkItem` aggregate that already exists in the event store, producing a duplicate-version conflict. The required guard: try `repository.Get(aggregateId)` first — if it succeeds, return early; if it throws `AggregateNotFound`, proceed with creation. This applies to any handler triggered by a coordination event like `WorkItemTriggered`.

---

All three are blocking. The batch handler needs architectural rethink (publish-per-item), the endpoint needs DB-side filtering + pagination, and the creation handler needs the idempotency guard before this can ship.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 8.0/18.5 (43%) |
| Evaluated | 2026-05-01 |
| Target duration | 34240 ms |
| Target cost | $0.1400 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all seven mandatory passes — does not skip any pass | FAIL | The output contains no pass structure whatsoever — no Pass 1 through Pass 7 headers or labels. It presents three numbered findings with no reference to a multi-pass execution framework. |
| c2 | Loop inside handler (`foreach` with `_repository.SaveAsync`) is flagged as a Pass 1 finding with file name and line-level evidence | PARTIAL | Finding 1 header is '`HandleBatchOrdersCommand` — N+1 saves inside a loop' and the body cites '`_repository.SaveAsync(order)` in a loop' with reference to `OrderProcessor.cs` in the PR context. File name and line-level evidence are present but there is no 'Pass 1' label. |
| c3 | In-memory filtering on a list endpoint is flagged as a Pass 3 finding (list endpoints must filter in the database query, not in memory) | PARTIAL | Finding 2 correctly flags in-memory `.Where()` filtering on `/api/orders` and states 'all filtering, sorting, and pagination must happen in the database.' However, the label 'Pass 3' is absent entirely. |
| c4 | Each finding follows the evidence format — severity, pass label, file path, evidence, standard violated, and a concrete fix | FAIL | None of the three findings include an explicit severity level (e.g., HIGH) or a pass label (e.g., Pass 1). File paths appear in bold headers but not in a structured field. The format template is not used. |
| c5 | Output uses the defined output template with summary counts per pass category | FAIL | There is no output template structure, no per-pass summary section, and no finding counts anywhere in the output. The response is free-form prose. |
| c6 | Zero-finding gate is respected — skill does not fabricate additional findings where none exist | PASS | The output flags exactly three issues, all of which correspond directly to problems described in the PR prompt. No fabricated or speculative findings are introduced. |
| c7 | Pass 6 (analyser compliance) and Pass 7 (testing) are run even when no new test files are in the diff — at minimum the skill confirms the passes were executed | FAIL | Pass 6 and Pass 7 are never mentioned in the output. There is no confirmation that analyser compliance or testing passes were run, even in a 'no findings' note. |
| c8 | Missing idempotency guard on creation handler is flagged — `CreateChildWorkItemHandler` creates an aggregate without checking if it already exists, risking duplicate-version conflicts on event replay | PASS | Finding 3 explicitly flags '`CreateChildWorkItemHandler.cs` — missing idempotency guard' and explains 'On event replay, this handler will attempt to create a WorkItem aggregate that already exists in the event store, producing a duplicate-version conflict.' |
| c9 | Related skills are referenced at the end of the output (review-standards and review-git) | FAIL | The output ends with 'All three are blocking…' and no skill cross-references. Neither `/coding-standards:review-standards` nor `/coding-standards:review-git` appear anywhere. |
| c10 | Output's loop-in-handler finding cites `OrderProcessor.cs::HandleBatchOrdersCommand` with line-level evidence of the `foreach` and the `_repository.SaveAsync(order)` call — not generic 'the handler has a loop' | PASS | The heading '`HandleBatchOrdersCommand` — N+1 saves inside a loop' names the handler, and the body states 'Calling `_repository.SaveAsync(order)` in a loop' — specific to both the method call and the looping context. `OrderProcessor.cs` is named in the PR context and referenced in the heading. |
| c11 | Output's loop-in-handler finding explains the violation of 'one message, one unit of work' — a failure mid-loop leaves some orders saved and others not, with no compensation, and prescribes the fix (publish one `SaveOrder` message per order and let the bus dispatch each) | PASS | 'violates the "one message, one unit of work" rule. A failure on item 3 of 10 leaves items 1–2 saved and items 4–10 not, with no retry boundary. The handler should publish one independent command per order ID and let the message bus dispatch each in its own transaction.' |
| c12 | Output's in-memory-filter finding cites `OrderSummaryController.cs::/api/orders` and explains why filtering with `.Where()` after fetching all orders is wrong (memory blow-up at scale, slow under load, breaks pagination semantics) with the fix (translate filter to LINQ-to-Marten / IQueryable in the database) | PARTIAL | The finding cites `OrderSummaryController.cs` and the `/api/orders` endpoint and states filtering must happen in the database. However, it does not explain the WHY in terms of memory blow-up, slow under load, or broken pagination semantics — it only says it is 'explicitly prohibited.' The fix does not mention LINQ-to-Marten or IQueryable. |
| c13 | Output's idempotency-guard finding cites `CreateChildWorkItemHandler.cs` and shows the missing existence check — explaining that `WorkItemTriggered` events can replay (Wolverine retries, manual replay, recovery), and the fix pattern (try `repository.get(id)` → if found return; on `AggregateNotFound` create) consistent with the project's idempotency guard rule | PARTIAL | The finding correctly cites `CreateChildWorkItemHandler.cs`, provides the fix pattern 'try `repository.Get(aggregateId)` first — if it succeeds, return early; if it throws `AggregateNotFound`, proceed with creation,' and mentions 'coordination event like `WorkItemTriggered`.' However, specific replay causes (Wolverine retries, manual replay, recovery) are not enumerated — it only says 'event replay' generically. |
| c14 | Output's findings each include severity, the pass label (Pass 1, 3, etc.), file path, evidence snippet, the standard violated (named or quoted), and a concrete fix — not just a list of issues | FAIL | No finding includes an explicit severity rating or a pass label. The structured field format (severity / pass label / file path / evidence / standard / fix) is not followed. The output is prose with bold headers. |
| c15 | Output runs all seven mandatory passes and reports per-pass finding counts in the summary — even passes with no findings get a '0 findings' line, not silently omitted | FAIL | No per-pass finding count summary exists. The output ends with a single closing paragraph ('All three are blocking…') with no pass-by-pass accounting. |
| c16 | Output respects the zero-finding gate on passes that genuinely have no issues — does NOT fabricate findings to fill quota | PASS | Only the three issues explicitly described in the PR prompt are reported. No additional speculative or fabricated issues are introduced. |
| c17 | Output runs Pass 6 (analyser compliance) and Pass 7 (testing) even though no test files are in the diff — at minimum confirming the passes ran and noting that the new handlers should be paired with tests in a follow-up | FAIL | Pass 6 and Pass 7 are entirely absent from the output. No mention of analyser compliance or testing, no 'passes ran with 0 findings,' no note about missing tests for new handlers. |
| c18 | Output's overall verdict reflects the severity of the findings — at least one HIGH/blocker finding (loop-in-handler is a correctness blocker for atomicity), so the verdict is REQUEST_CHANGES not APPROVE | PASS | The closing line states 'All three are blocking.' While the formal REQUEST_CHANGES label is not used, the verdict is unambiguously a block on merging, not an approval. |
| c19 | Output cross-references related skills at the end — `/coding-standards:review-standards` and `/coding-standards:review-git` — for follow-up reviews | FAIL | The output ends after 'All three are blocking…' with no skill cross-references. Neither `/coding-standards:review-standards` nor `/coding-standards:review-git` appear anywhere in the response. |

### Notes

The captured output demonstrates strong content quality — it correctly identifies all three issues from the PR, provides accurate fix prescriptions, and explains the 'one message, one unit of work' rule violation with appropriate specificity. However, it fails almost entirely on structural compliance with the skill's defined format. The seven-pass framework is completely absent: no pass labels, no severity ratings, no per-pass finding counts, no summary table, no confirmation that zero-finding passes (Pass 6, Pass 7) were executed, and no related-skills cross-references at the end. The output reads as a competent ad-hoc code review rather than an execution of the structured `review-dotnet` skill. Approximately 60% of the criteria relate to structural/format compliance, and those all fail, dragging the score to 43%.
