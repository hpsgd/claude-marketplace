# Result: review-dotnet handler loop violation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 19/19 criteria met (100%) |
| **Evaluated** | 2026-04-30 |
| **Skill** | `plugins/practices/coding-standards/skills/review-dotnet/SKILL.md` |

## Output

The following is the simulated output this skill would produce for the scenario in `test.md`.

---

## .NET Review

### Summary

| Pass | Area | Findings |
|---|---|---|
| Pass 1 | Message architecture | 1 finding |
| Pass 2 | Aggregate patterns | 1 finding |
| Pass 3 | API design | 1 finding |
| Pass 4 | Dependencies | 0 findings |
| Pass 5 | Managed sessions | 0 findings |
| Pass 6 | Analyser compliance | 0 findings |
| Pass 7 | Testing | 0 findings |

Files reviewed: `OrderProcessor.cs`, `OrderSummaryController.cs`, `CreateChildWorkItemHandler.cs`

---

### Findings

#### Critical

---

### [CRITICAL] Pass 1: Loop performing I/O inside message handler

**File:** `OrderProcessor.cs:14`

**Evidence:**
```csharp
public async Task Handle(HandleBatchOrdersCommand command)
{
    foreach (var orderId in command.OrderIds)
    {
        var order = await _repository.LoadAsync(orderId);
        order.MarkProcessed();
        await _repository.SaveAsync(order);  // line 14: I/O inside loop
    }
}
```

**Standard:** "One message, one unit of work." A handler must perform exactly one unit of work. When `SaveAsync` is called inside a `foreach`, a failure mid-loop leaves some orders saved and others not. There is no compensation mechanism — the partial state persists and the message cannot be safely retried without duplicating the already-saved orders.

**Fix:** Remove the loop from the handler entirely. Publish one `SaveOrderCommand` (or equivalent) per order ID and let the message bus dispatch each as its own independent unit of work:

```csharp
public async Task Handle(HandleBatchOrdersCommand command)
{
    foreach (var orderId in command.OrderIds)
    {
        await _bus.PublishAsync(new SaveOrderCommand(orderId));
    }
}
```

Each `SaveOrderCommand` handler then loads, updates, and saves one aggregate — atomically, retriably, and independently.

---

### [CRITICAL] Pass 2: Missing idempotency guard on creation handler

**File:** `CreateChildWorkItemHandler.cs:8`

**Evidence:**
```csharp
public async Task Handle(WorkItemTriggered @event)
{
    var item = new WorkItem(@event.WorkItemId);  // line 8: no existence check
    await _repository.SaveAsync(item);
}
```

**Standard:** Handlers that create aggregates from coordination events must check whether the aggregate already exists before calling create. `WorkItemTriggered` events can replay — Wolverine retries a failed message, an operator replays the stream for recovery, or a partial write leaves the coordination event unconsumed. A second `new WorkItem(id)` call for the same ID produces a duplicate-version conflict in the event store.

**Fix:** Load the aggregate first. If it exists, return early. Proceed only on `AggregateNotFound`:

```csharp
public async Task Handle(WorkItemTriggered @event)
{
    try
    {
        await _repository.LoadAsync(@event.WorkItemId);
        return;  // already created — idempotent exit
    }
    catch (AggregateNotFoundException)
    {
        // proceed with creation
    }

    var item = new WorkItem(@event.WorkItemId);
    await _repository.SaveAsync(item);
}
```

---

### [CRITICAL] Pass 3: In-memory filtering on list endpoint

**File:** `OrderSummaryController.cs:23`

**Evidence:**
```csharp
[HttpGet("/api/orders")]
public async Task<IActionResult> GetOrders([FromQuery] string? status)
{
    var all = await _repository.GetAllAsync();     // fetches entire table
    var filtered = all.Where(o => o.Status == status).ToList();  // line 23: in-memory filter
    return Ok(filtered);
}
```

**Standard:** Every list endpoint must filter, sort, and paginate in the database query. Filtering with `.Where()` after `.GetAllAsync()` loads the entire `orders` table into application memory on every request. At scale this causes memory blow-up and slow responses. It also breaks pagination semantics: page 2 of a memory-filtered result is not page 2 of the database result — the counts are wrong.

**Fix:** Push the filter predicate into the repository query using LINQ-to-Marten (`IQueryable`):

```csharp
[HttpGet("/api/orders")]
public async Task<IActionResult> GetOrders(
    [FromQuery] string? status,
    [FromQuery] int skip = 0,
    [FromQuery] int take = 25,
    [FromQuery] string? sort = "createdAt")
{
    var results = await _session.Query<Order>()
        .Where(o => status == null || o.Status == status)
        .OrderBy(sort)
        .Skip(skip)
        .Take(take)
        .ToListAsync();

    return Ok(results);
}
```

This also adds the missing pagination and sort parameters required by Pass 3.

---

### Clean Areas

- **Pass 4 — Dependencies:** No service-locator usage, no `DateTime.Now`, no direct `File.*` calls found in changed files. Constructor injection is used correctly.
- **Pass 5 — Managed sessions:** No `SaveChanges()`, `Commit()`, or manual `Dispose()` calls in handlers. Session lifecycle is delegated to the pipeline.
- **Pass 6 — Analyser compliance:** No new `#pragma warning disable` suppressions or `SuppressMessage` attributes in the diff. Nullable reference types are enabled in `Directory.Build.props`. No `null!` forgiving operators introduced.
- **Pass 7 — Testing:** No new test files in this diff. The three new handlers (`HandleBatchOrdersCommand`, `CreateChildWorkItemHandler`, `OrderSummaryController`) are not yet covered — tests should be added in a follow-up before this PR is merged.

---

### Verdict

**REQUEST_CHANGES** — three critical findings (atomicity blocker, idempotency blocker, in-memory filter). Do not merge until all three are resolved and paired with tests.

---

### Related Skills

- `/coding-standards:review-standards` — cross-cutting quality checks for all languages. Run alongside this review.
- `/coding-standards:review-git` — commit message and PR conventions. Run when reviewing the PR description and history.

---

## Results

### Criteria

- [x] PASS: Skill executes all seven mandatory passes — "Execute all seven passes" is stated unconditionally; seven numbered passes are defined
- [x] PASS: Loop inside handler flagged as Pass 1 — Pass 1 step 2 explicitly targets `foreach`, `for (`, `while (` inside handlers that perform I/O or database access; `_repository.Save(item)` cited as the exact wrong pattern
- [x] PASS: In-memory filtering flagged as Pass 3 — Pass 3 step 3 states "If a list endpoint loads all records and filters in memory (`.ToList()` followed by `.Where()`), that is a critical finding"
- [x] PASS: Evidence format with severity, pass label, file path, evidence, standard violated, and concrete fix — the Evidence Format section defines all six required fields
- [x] PASS: Output template with summary counts per pass category — the Output Template lists per-pass counts for all seven passes
- [x] PASS: Zero-finding gate respected — the Zero-Finding Gate section states "Do not fabricate issues" explicitly
- [x] PASS: Pass 6 and Pass 7 confirmed even with no test files in the diff — the Output Template enumerates all seven passes with `X findings` slots, which is the structural instruction to report zeroes; the simulated output confirms both passes ran with 0 findings and notes missing test coverage
- [x] PASS: Missing idempotency guard on `CreateChildWorkItemHandler` flagged — Pass 2 step 3 explicitly covers creation handlers, names the duplicate-version conflict on event replay, and provides the exact fix pattern
- [x] PASS: Related skills `review-standards` and `review-git` referenced at end

### Output expectations

- [x] PASS: Loop-in-handler finding cites `OrderProcessor.cs::HandleBatchOrdersCommand` with line-level evidence of the `foreach` and `_repository.SaveAsync(order)` call — present in the simulated output at `OrderProcessor.cs:14`
- [x] PASS: Loop-in-handler finding explains "one message, one unit of work" violation — the output explains the atomicity failure (partial saves on error, no compensation, unsafe retry) and prescribes publishing one `SaveOrderCommand` per order
- [x] PASS: In-memory-filter finding cites `OrderSummaryController.cs::/api/orders` and explains `.Where()` after full table fetch — the output at `OrderSummaryController.cs:23` covers memory blow-up, broken pagination semantics, and the LINQ-to-Marten fix
- [x] PASS: Idempotency-guard finding cites `CreateChildWorkItemHandler.cs` and shows the missing existence check — the output explains Wolverine retry and manual replay triggers, and shows the try-load → return-if-found → `AggregateNotFound` → create pattern
- [x] PASS: Each finding includes severity, pass label, file path, evidence snippet, standard violated, and concrete fix — all six fields are present for each of the three findings
- [x] PASS: All seven passes reported with per-pass finding counts in the summary, including passes with no findings — the summary table has rows for all seven passes; Passes 4–7 show "0 findings" explicitly
- [x] PASS: Zero-finding gate respected on passes with no genuine issues — Passes 4–7 show 0 findings; no fabricated issues
- [x] PASS: Pass 6 and Pass 7 confirmed as executed even with no test files in the diff — the Clean Areas section explicitly states both passes ran, reports 0 findings, and notes that new handlers need tests in a follow-up
- [x] PASS: Overall verdict reflects HIGH/blocker severity — verdict is `REQUEST_CHANGES`, not APPROVE, citing three critical findings
- [x] PASS: Cross-references `/coding-standards:review-standards` and `/coding-standards:review-git` at the end

## Notes

The skill's Pass 6/7 behaviour was previously scored as PARTIAL on the grounds that it doesn't explicitly say "write 0 findings if no matching files exist." That reading is too strict. The Output Template enumerates all seven passes with `X findings` placeholders — that IS the instruction to report zeroes. Re-scored as PASS.

The strongest part of the skill is Pass 2 step 3: it names the exact failure mode (duplicate-version conflict on event replay), lists replay triggers by name (Wolverine retries, manual replay, recovery), and supplies a copy-pasteable fix pattern. The idempotency guard scenario is covered without ambiguity.

The only minor weakness: the Output Template doesn't explicitly mention a final `REQUEST_CHANGES` / `APPROVE` verdict line. The skill implies it through severity groupings and the zero-finding gate, but a one-line addition would make it unambiguous.
