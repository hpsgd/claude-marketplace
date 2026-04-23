---
description: "Design recurring actions as mechanisms with triggers, execution, outcomes, and retry logic"
---

# Mechanism Design

## Build mechanisms, not habits

Every recurring action that matters should be a mechanism, not a habit. Habits depend on memory and discipline. Mechanisms fire reliably because they have structure.

A mechanism needs four parts:

1. **Trigger** — what causes it to fire (a hook event, a file pattern, a session start)
2. **Execution** — what it does, stated precisely enough that any agent could follow it
3. **Outcome** — what success looks like, verifiable after the fact
4. **Failure handling** — what happens when it doesn't work (retry up to N times, then notify)

If a recurring action can't be expressed this way, it's a wish, not a process.

## When to mechanise

Good signals: you've done the same thing manually three or more times. You've forgotten to do it at least once. The consequence of forgetting is real (broken build, lost data, missed context).

Bad signals: it's happened once. The cost of forgetting is negligible. The mechanism would be more complex than the problem it solves.

## Mechanisms fail silently unless you prevent it

The default failure mode for any automated process is silence. A hook that errors gets swallowed. A check that doesn't run looks the same as a check that passed. Design for failure visibility: if the mechanism can't complete, it must say so. Exit codes, error output, notifications. Never assume success from absence of failure.
