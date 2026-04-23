---
description: "Session focus and deferred work: keep sessions to one concern, persist anything out of scope"
---

# Session Discipline

## One focused thing per session

Each session should address one concern. Mixing concerns inflates blast radius and muddies git history. When a second topic surfaces mid-session, note it as deferred work (see below) and stay on the original thread.

**Active scope-drift detection:** when you notice the session expanding beyond its original focus (a "while we're at it" moment, a tangent that's turning into real work, a second PR forming), flag it explicitly. Say something like "this is drifting from what we started on — want me to note it for a separate session?" Don't wait for the user to notice. The user has asked for this warning because they know they're prone to scope expansion.

Signs of drift:
- Touching files unrelated to the original task
- A second commit message forming that doesn't match the first
- "Oh, and also..." followed by a different concern
- The session has been running long and the topic has shifted

## Deferred work needs persistent markers

When something out of scope surfaces, write it down somewhere durable. A mention in chat is not durable. Sessions are stateless. Next session starts fresh with no memory of what was discussed.

Persist deferred work as one of:
- A `TODO` comment in the relevant code file
- A GitHub Issue
- A memory file (if it's a pattern or learning, not a task)
- A note in an existing tracking document

Pair with a session-start scan: at the start of each session, check for deferred markers (`TODO`, open issues, stale branches) so nothing falls through the cracks.
