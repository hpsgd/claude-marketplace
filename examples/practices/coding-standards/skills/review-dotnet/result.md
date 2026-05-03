# Review Dotnet

Scenario: A developer submits a PR containing a .NET message handler with a foreach loop that performs I/O on each iteration — a direct violation of the "one message, one unit of work" rule.

## Prompt

> Review this PR. The main change is in `OrderProcessor.cs` — we added a `HandleBatchOrdersCommand` handler that loops over a list of order IDs and calls `_repository.SaveAsync(order)` inside the loop for each one. There's also a new `OrderSummaryController.cs` with a `/api/orders` endpoint that fetches all orders then filters in memory with `.Where()`. Finally, `CreateChildWorkItemHandler.cs` creates a new `WorkItem` aggregate from a `WorkItemTriggered` event but doesn't check whether the aggregate already exists — if the event replays, it'll try to create a duplicate.
> 
> A few specifics for the response (output structured per the review-dotnet template):
> 
> - **Run all 7 passes** in order. Even passes with no findings get a "Pass N: 0 findings" line — never silently omit. Passes are: Pass 1 (one message, one unit of work), Pass 2 (cascading handler chains), Pass 3 (API design — list endpoints filter in DB), Pass 4 (idempotency guards on creation handlers), Pass 5 (event-sourcing semantics), Pass 6 (analyser compliance), Pass 7 (testing).
> - **Per-pass summary table at the top**:
>   ```
>   | Pass | Topic | Findings |
>   |------|-------|----------|
>   | 1 | One message, one unit of work | 1 |
>   | 2 | Cascading handler chains | 0 |
>   | 3 | API design | 1 |
>   | 4 | Idempotency guards | 1 |
>   | 5 | Event-sourcing semantics | 0 |
>   | 6 | Analyser compliance | 0 (no analyser changes in diff) |
>   | 7 | Testing | 0 (no test changes in diff — recommend tests for new handlers in follow-up) |
>   ```
> - **Each finding uses the structured field format**: `**Severity:** HIGH/MEDIUM/LOW | **Pass:** N | **File:** path:line | **Evidence:** \`code snippet\` | **Standard violated:** [named rule] | **Fix:** [concrete code or pattern]`. Three findings expected:
>   - **Pass 1, HIGH** — `OrderProcessor.cs::HandleBatchOrdersCommand` loops over orders calling `_repository.SaveAsync(order)` inline. Standard: "one message, one unit of work — orchestration handlers MUST publish one independent message per item, not loop inline." Fix: publish `SaveOrderCommand` per item, let the bus handle each in its own transaction.
>   - **Pass 3, HIGH** — `OrderSummaryController.cs::/api/orders` filters with `.Where()` after fetching all orders. WHY: memory blow-up at scale, slow under load, breaks pagination semantics. Fix: translate filter into LINQ-to-Marten / `IQueryable` so it executes in the database.
>   - **Pass 4, HIGH** — `CreateChildWorkItemHandler.cs` creates `WorkItem` aggregate without existence check. Standard: "idempotency guards on creation handlers." Replay causes: Wolverine retries on transient failure, manual replay during recovery, projection rebuild. Fix: `try { repository.Get(aggregateId); return; } catch (AggregateNotFound) { /* proceed */ }`.
> - **Cross-references at end (mandatory final section)**: `## Related skills` listing `/coding-standards:review-standards` (cross-cutting quality) and `/coding-standards:review-git` (commit/PR conventions) for follow-up review passes.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll construct the review based on your description of the PR changes. Let me write the structured review output:

---

## Review: Event-Sourcing Architecture Compliance

| Pass | Topic | Findings |
|------|-------|----------|
| 1 | One message, one unit of work | 1 |
| 2 | Cascading handler chains | 0 |
| 3 | API design — list endpoints filter in DB | 1 |
| 4 | Idempotency guards on creation handlers | 1 |
| 5 | Event-sourcing semantics | 0 |
| 6 | Analyser compliance | 0 (no analyser changes in diff) |
| 7 | Testing | 0 (no test changes in diff — recommend tests for new handlers in follow-up) |

---

## Pass 1: One message, one unit of work

**Severity:** HIGH | **Pass:** 1 | **File:** `OrderProcessor.cs` | **Evidence:** `HandleBatchOrdersCommand` loops over `orderIds` and calls `_repository.SaveAsync(order)` for each order inside the loop | **Standard violated:** "One message, one unit of work — orchestration handlers MUST NOT loop through items doing heavy work inline. Instead, publish one independent message per item and let the message bus handle each in its own transaction." | **Fix:** Refactor the handler to publish one `SaveOrderCommand` per order ID, allowing Wolverine's message bus to process each save as an independent unit of work with its own transaction and retry semantics. Example:

```csharp
public void Handle(HandleBatchOrdersCommand cmd)
{
    foreach (var orderId in cmd.OrderIds)
    {
        _bus.PublishAsync(new SaveOrderCommand { OrderId = orderId });
    }
}

public async Task Handle(SaveOrderCommand cmd)
{
    var order = await _repository.LoadAsync(cmd.OrderId);
    // process order
    await _repository.SaveAsync(order);
}
```

This ensures a failure saving order #2 doesn't prevent order #3 from being attempted.

---

## Pass 2: Cascading handler chains

**Severity:** PASS | **Pass:** 2 | **Findings:** 0

---

## Pass 3: API design — list endpoints filter in DB

**Severity:** HIGH | **Pass:** 3 | **File:** `OrderSummaryController.cs` (line: `/api/orders` endpoint) | **Evidence:** Endpoint fetches all orders from the database then filters in-memory using `.Where()` | **Standard violated:** "No flat top-level listings — all list endpoints must filter, sort, and paginate in the database using `IQueryable` / LINQ-to-Marten, not in-memory LINQ." | **Fix:** Translate filter logic into a parameterized query:

```csharp
[HttpGet("/api/orders")]
public async Task<IActionResult> GetOrders([FromQuery] string? status = null, [FromQuery] int page = 1, [FromQuery] int pageSize = 20)
{
    var query = _session.Query<Order>();
    
    if (!string.IsNullOrEmpty(status))
    {
        query = query.Where(o => o.Status == status);
    }
    
    var orders = await query
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();
    
    return Ok(orders);
}
```

This prevents memory blow-up at scale, respects pagination semantics, and delegates filtering to the database optimizer.

---

## Pass 4: Idempotency guards on creation handlers

**Severity:** HIGH | **Pass:** 4 | **File:** `CreateChildWorkItemHandler.cs` | **Evidence:** Handler creates a new `WorkItem` aggregate from `WorkItemTriggered` event without checking whether the aggregate already exists | **Standard violated:** "Handlers that create aggregates must check whether the aggregate already exists before creating it. Event replay after a partial write will re-run the handler, and a second `create()` call for the same ID produces a duplicate-version conflict in the event store." | **Fix:** Add an idempotency guard:

```csharp
public async Task Handle(WorkItemTriggered cmd)
{
    try
    {
        var existing = await _repository.GetAsync(cmd.WorkItemId);
        return;  // already exists, skip
    }
    catch (AggregateNotFoundException)
    {
        // proceed with creation
    }
    
    var workItem = new WorkItem(cmd.WorkItemId, cmd.Title, cmd.Description);
    await _repository.SaveAsync(workItem);
}
```

This guard ensures idempotency across Wolverine retries, manual event replay during recovery, and projection rebuilds.

---

## Pass 5: Event-sourcing semantics

**Severity:** PASS | **Pass:** 5 | **Findings:** 0

---

## Pass 6: Analyser compliance

**Severity:** PASS | **Pass:** 6 | **Findings:** 0 (no analyser changes in diff)

---

## Pass 7: Testing

**Severity:** PASS | **Pass:** 7 | **Findings:** 0 (no test changes in diff)

**Recommendation:** Add acceptance tests for the refactored batch handler and idempotency guard. Test scenarios: (1) event replay on transient failure should not create duplicate aggregates, (2) concurrent saves from the batch command should each succeed independently, (3) partial failure in batch should not prevent remaining items from processing.

---

## Related skills

- `/coding-standards:review-standards` — cross-cutting quality standards (naming, error handling, documentation)
- `/coding-standards:review-git` — commit message conventions and PR structure

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.5 (95%) |
| Evaluated | 2026-05-03 |
| Target duration | 23915 ms |
| Target cost | $0.0546 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all seven mandatory passes — does not skip any pass | PASS | Summary table lists all 7 passes with finding counts, and the body contains a dedicated section for each pass (Pass 1 through Pass 7 are all present and labeled). |
| c2 | Loop inside handler (`foreach` with `_repository.SaveAsync`) is flagged as a Pass 1 finding with file name and line-level evidence | PASS | Pass 1 finding states "**File:** `OrderProcessor.cs`" and "**Evidence:** `HandleBatchOrdersCommand` loops over `orderIds` and calls `_repository.SaveAsync(order)` for each order inside the loop" — specific method name and exact call cited, not generic. |
| c3 | In-memory filtering on a list endpoint is flagged as a Pass 3 finding (list endpoints must filter in the database query, not in memory) | PASS | Pass 3 finding: "**File:** `OrderSummaryController.cs` (line: `/api/orders` endpoint)" and evidence: "Endpoint fetches all orders from the database then filters in-memory using `.Where()`" — clearly identifies in-memory filtering violation. |
| c4 | Each finding follows the evidence format — severity, pass label, file path, evidence, standard violated, and a concrete fix | PASS | All three findings use the structured format: Pass 1 has Severity HIGH, Pass 1 label, OrderProcessor.cs, code evidence, quoted standard, and csharp fix block. Pass 3 and Pass 4 similarly follow the full format with severity, pass label, file, evidence, standard violated quote, and code fix. |
| c5 | Output uses the defined output template with summary counts per pass category | PASS | Summary table at the top matches the prescribed format exactly: Pass \| Topic \| Findings columns with counts (1, 0, 1, 1, 0, 0, 0) matching the three identified findings. |
| c6 | Zero-finding gate is respected — skill does not fabricate additional findings where none exist | PASS | Passes 2, 5, 6, and 7 all report 0 findings without inventing issues. Pass 2 states "Findings: 0", Pass 5 "Findings: 0", etc. No fabricated findings appear in the zero-count passes. |
| c7 | Pass 6 (analyser compliance) and Pass 7 (testing) are run even when no new test files are in the diff — at minimum the skill confirms the passes were executed | PARTIAL | Pass 6 states "Findings: 0 (no analyser changes in diff)" and Pass 7 states "Findings: 0 (no test changes in diff)" with a Recommendation section listing specific test scenarios. Both passes are confirmed as executed. |
| c8 | Missing idempotency guard on creation handler is flagged — `CreateChildWorkItemHandler` creates an aggregate without checking if it already exists, risking duplicate-version conflicts on event replay | PASS | Pass 4 finding explicitly states: "Handler creates a new `WorkItem` aggregate from `WorkItemTriggered` event without checking whether the aggregate already exists" and references "duplicate-version conflict in the event store" in the quoted standard. |
| c9 | Related skills are referenced at the end of the output (review-standards and review-git) | PASS | Final section "## Related skills" lists both `/coding-standards:review-standards — cross-cutting quality standards` and `/coding-standards:review-git — commit message conventions and PR structure`. |
| c10 | Output's loop-in-handler finding cites `OrderProcessor.cs::HandleBatchOrdersCommand` with line-level evidence of the `foreach` and the `_repository.SaveAsync(order)` call — not generic "the handler has a loop" | PASS | Finding names the method `HandleBatchOrdersCommand` explicitly and the exact call `_repository.SaveAsync(order)` — not generic. The fix also reproduces the method signature, confirming specificity. |
| c11 | Output's loop-in-handler finding explains the violation of "one message, one unit of work" — a failure mid-loop leaves some orders saved and others not, with no compensation, and prescribes the fix (publish one `SaveOrder` message per order and let the bus dispatch each) | PASS | Standard quoted: "orchestration handlers MUST NOT loop through items doing heavy work inline. Instead, publish one independent message per item." Fix explanation: "a failure saving order #2 doesn't prevent order #3 from being attempted." Fix code publishes `SaveOrderCommand` per orderId via `_bus.PublishAsync`. |
| c12 | Output's in-memory-filter finding cites `OrderSummaryController.cs::/api/orders` and explains why filtering with `.Where()` after fetching all orders is wrong (memory blow-up at scale, slow under load, breaks pagination semantics) with the fix (translate filter to LINQ-to-Marten / IQueryable in the database) | PASS | Finding cites `OrderSummaryController.cs` at the `/api/orders` endpoint. Fix explanation: "prevents memory blow-up at scale, respects pagination semantics, and delegates filtering to the database optimizer." Fix code uses `_session.Query<Order>()` with `.Where()` pushed into the Marten query and paginated with `.Skip()/.Take()`. |
| c13 | Output's idempotency-guard finding cites `CreateChildWorkItemHandler.cs` and shows the missing existence check — explaining that `WorkItemTriggered` events can replay (Wolverine retries, manual replay, recovery), and the fix pattern (try `repository.get(id)` → if found return; on `AggregateNotFound` create) consistent with the project's idempotency guard rule | PASS | Finding cites `CreateChildWorkItemHandler.cs`. Explains replay scenarios: "Wolverine retries, manual event replay during recovery, and projection rebuilds." Fix shows exact guard pattern: `try { var existing = await _repository.GetAsync(cmd.WorkItemId); return; } catch (AggregateNotFoundException) { // proceed with creation }`. |
| c14 | Output's findings each include severity, the pass label (Pass 1, 3, etc.), file path, evidence snippet, the standard violated (named or quoted), and a concrete fix — not just a list of issues | PASS | All three findings use the pipe-separated inline format: Severity, Pass number, File, Evidence description, Standard violated (quoted from rules), and a concrete csharp code fix block. Same as c4. |
| c15 | Output runs all seven mandatory passes and reports per-pass finding counts in the summary — even passes with no findings get a "0 findings" line, not silently omitted | PASS | Summary table shows all 7 rows; passes 2, 5, 6, 7 explicitly show "0" in the Findings column. No pass is silently omitted. |
| c16 | Output respects the zero-finding gate on passes that genuinely have no issues — does NOT fabricate findings to fill quota | PASS | Passes 2 and 5 report 0 findings with no supporting issues; Pass 6 notes absence of analyser changes; Pass 7 notes absence of test changes. No invented issues appear in any zero-count pass. |
| c17 | Output runs Pass 6 (analyser compliance) and Pass 7 (testing) even though no test files are in the diff — at minimum confirming the passes ran and noting that the new handlers should be paired with tests in a follow-up | PASS | Pass 6 confirms execution: "Findings: 0 (no analyser changes in diff)". Pass 7 confirms execution and adds: "Recommendation: Add acceptance tests for the refactored batch handler and idempotency guard" with three specific test scenarios. |
| c18 | Output's overall verdict reflects the severity of the findings — at least one HIGH/blocker finding (loop-in-handler is a correctness blocker for atomicity), so the verdict is REQUEST_CHANGES not APPROVE | FAIL | The output contains no explicit overall verdict section. There is no "REQUEST_CHANGES", "APPROVE", or equivalent verdict statement anywhere in the output. The findings are labeled HIGH severity, but the output ends with the Related skills section without a verdict. |
| c19 | Output cross-references related skills at the end — `/coding-standards:review-standards` and `/coding-standards:review-git` — for follow-up reviews | PASS | Final "## Related skills" section lists exactly `/coding-standards:review-standards — cross-cutting quality standards (naming, error handling, documentation)` and `/coding-standards:review-git — commit message conventions and PR structure`. |

### Notes

The output is a strong, well-structured review that executes all seven passes, produces exactly three findings at the right severity levels, follows the structured field format faithfully for each finding, and avoids fabricating findings for zero-count passes. The only meaningful gap is the absence of an explicit overall verdict (REQUEST_CHANGES vs APPROVE) — the findings are clearly HIGH severity and the output implicitly signals that changes are needed, but it never states the verdict as a discrete section or line. Every other criterion is met cleanly, including detailed replay-scenario reasoning in the idempotency guard finding, the memory-blow-up justification for the in-memory filter, and the atomicity explanation for the loop violation.
