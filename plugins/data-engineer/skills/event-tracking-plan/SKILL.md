---
name: event-tracking-plan
description: Define an event tracking plan — what events to capture, with what properties, for what purpose.
argument-hint: "[feature, flow, or product area to track]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Define an event tracking plan for $ARGUMENTS.

## For each event

| Field | Description |
|---|---|
| Event name | `snake_case`, verb_noun format (e.g., `report_viewed`, `search_performed`) |
| Trigger | What user action or system event fires this |
| Properties | Key-value pairs captured with the event (with types) |
| Purpose | What question does this event help answer? |

## Rules

- Every event has a clear purpose — if you can't state what question it answers, don't track it
- Property names are consistent across events (use `user_id` everywhere, not sometimes `userId`)
- Avoid high-cardinality properties (don't track full URLs, use route patterns)
- Include a timestamp, user identifier, and session identifier on every event
- Document what constitutes a "unique" event (deduplication logic)
- Over-tracking is as bad as under-tracking — each event has a maintenance cost

## Output

An event tracking plan table, plus instrumentation notes (where in the code to add tracking).
