# Result: review-dotnet handler loop violation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18.5/19 criteria met (97%) |
| **Evaluated** | 2026-04-29 |
| **Skill** | `plugins/practices/coding-standards/skills/review-dotnet/SKILL.md` |

## Results

### Criteria

- [x] PASS: Skill executes all seven mandatory passes — seven numbered passes are defined and the skill states "Execute all seven passes" unconditionally
- [x] PASS: Loop inside handler flagged as Pass 1 — Pass 1 step 2 explicitly targets `foreach`, `for (`, `while (` inside handlers that perform I/O or database access, with `_repository.Save(item)` cited as the exact wrong pattern
- [x] PASS: In-memory filtering flagged as Pass 3 — Pass 3 step 3 states "If a list endpoint loads all records and filters in memory (`.ToList()` followed by `.Where()`), that is a critical finding"
- [x] PASS: Evidence format with severity, pass label, file path, evidence, standard violated, and concrete fix — the Evidence Format section defines all six required fields
- [x] PASS: Output template with summary counts per pass category — the Output Template lists per-pass counts covering all seven passes
- [x] PASS: Zero-finding gate respected — the Zero-Finding Gate section states "Do not fabricate issues" explicitly
- [~] PARTIAL: Pass 6 and Pass 7 run even with no test files in the diff — the skill mandates all seven passes unconditionally, satisfying the intent; it does not explicitly instruct the reviewer to confirm execution with "0 findings" notation when no relevant files exist in the diff, which is what this criterion probes
- [x] PASS: Missing idempotency guard on `CreateChildWorkItemHandler` flagged — Pass 2 step 3 explicitly covers creation handlers that must check aggregate existence before calling create, naming the duplicate-version conflict on event replay with a wrong/right example matching the `WorkItemTriggered` scenario
- [x] PASS: Related skills `review-standards` and `review-git` referenced at end

### Output expectations

- [x] PASS: Loop-in-handler finding would cite `OrderProcessor.cs::HandleBatchOrdersCommand` — the skill mandates file+line evidence via `path/to/File.cs:42` format and provides grep commands targeting changed files; the evidence format is specific enough to produce line-level citation of the `foreach` and `_repository.SaveAsync` call
- [x] PASS: Loop-in-handler finding explains "one message, one unit of work" violation — Pass 1 step 3 describes the atomicity issue (handler doing multiple operations), and the fix (publish individual messages, let the bus dispatch each) is prescribed in step 2
- [x] PASS: In-memory-filter finding would cite `OrderSummaryController.cs::/api/orders` — Pass 3 step 3 targets collection-returning endpoints with the exact `.ToList()` + `.Where()` pattern; the critical finding statement and fix (translate to database query) are present
- [x] PASS: Idempotency-guard finding would cite `CreateChildWorkItemHandler.cs` — Pass 2 step 3 names coordination event handlers, the replay risk (Wolverine retries, manual replay), and the exact fix pattern (try load → return if found; on `AggregateNotFound` create)
- [x] PASS: Each finding includes severity, pass label, file path, evidence snippet, standard violated, and concrete fix — the Evidence Format section mandates all six fields
- [x] PASS: All seven passes reported with per-pass finding counts in the summary, including passes with no findings — the Output Template shows counts for all seven categories; mandatory execution means zero-finding passes appear as "0 findings"
- [x] PASS: Zero-finding gate on passes with no genuine issues — the skill explicitly prohibits fabricating findings
- [~] PARTIAL: Pass 6 and Pass 7 confirmed as executed even with no test files in the diff — the mandatory seven-pass structure implies this, but the skill does not explicitly instruct noting "pass ran, 0 findings" when no matching files are present; an agent might silently omit rather than confirm
- [x] PASS: Overall verdict reflects HIGH/blocker severity — the loop-in-handler is defined as a finding requiring a critical severity label; the severity grouping in the output template and the correctness-blocker nature of the violation would produce REQUEST_CHANGES
- [x] PASS: Cross-references `/coding-standards:review-standards` and `/coding-standards:review-git` in the Related Skills section at the end

## Notes

The PARTIAL on Pass 6/7 (criteria row 7 and output expectation row 8) is the same minor documentation gap: the skill's mandatory-seven-pass structure implies execution must be confirmed for all passes, but it does not spell out "write 0 findings if no relevant files exist." A single sentence would close this. Not a quality blocker.

The idempotency guard coverage is the strongest part of the skill. Pass 2 step 3 names the exact failure mode (duplicate-version conflict on event replay), lists replay triggers (Wolverine retries, manual replay, recovery), and provides a copy-pasteable fix pattern. The test scenario is covered without ambiguity.
