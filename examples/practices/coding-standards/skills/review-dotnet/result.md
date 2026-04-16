# Result: review-dotnet handler loop violation

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 8.5 / 9 criteria met (94%) |
| **Evaluated** | 2026-04-16 |
| **Skill** | `plugins/practices/coding-standards/skills/review-dotnet/SKILL.md` |

## Results

- [x] PASS: Skill executes all seven mandatory passes — seven numbered passes are defined and the skill states "Execute all seven passes" unconditionally
- [x] PASS: Loop inside handler flagged as Pass 1 finding — Pass 1 item 2 explicitly targets `foreach`, `for (`, `while (` inside handlers that perform I/O, with a wrong/right example that matches the `HandleBatchOrdersCommand` scenario directly
- [x] PASS: In-memory filtering flagged as Pass 3 finding — Pass 3 item 3 states "If a list endpoint loads all records and filters in memory (`.ToList()` followed by `.Where()`), that is a critical finding", which matches `OrderSummaryController.cs` exactly
- [x] PASS: Evidence format with severity, pass label, file, evidence, standard, and fix — the Evidence Format section defines all six required fields
- [x] PASS: Output template with summary counts per pass category — the Output Template defines per-pass finding counts covering all seven passes
- [x] PASS: Zero-finding gate respected — the Zero-Finding Gate section states "Do not fabricate issues" explicitly
- [~] PARTIAL: Pass 6 and Pass 7 run even with no test files in diff — the skill mandates all seven passes unconditionally, satisfying the intent; it does not explicitly instruct the reviewer to confirm execution when no relevant files are present, which is what this criterion probes
- [x] PASS: Missing idempotency guard on `CreateChildWorkItemHandler` flagged — Pass 2 item 3 now explicitly covers creation handlers that must check aggregate existence before calling create, naming the duplicate-version conflict failure mode on event replay and providing a wrong/right example that matches the `WorkItemTriggered` scenario directly
- [x] PASS: Related skills `review-standards` and `review-git` referenced at end of output

## Notes

The idempotency guard fix is well-targeted. Pass 2 item 3 describes the exact pattern the test probes: a coordination event triggers a child aggregate creation, the handler skips the existence check, event replay creates a duplicate. The wrong example (`new WorkItem(command.Id); await repository.Save(item)`) and the right example (load first, return early on hit, proceed on `AggregateNotFound`) give a reviewer enough to catch and fix the violation without ambiguity.

The remaining PARTIAL on Pass 6/7 is a minor documentation gap. Adding "if no matching files exist in the diff, confirm the pass ran and note zero findings" would close it. Not a meaningful quality problem.
