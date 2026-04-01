---
name: incident-response
description: Guide incident response — detect, assess, mitigate, root cause, prevent recurrence.
argument-hint: "[incident description, error logs, or alert details]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Respond to $ARGUMENTS.

## Process

1. **Detect** — what is the symptom? What alert fired? What did the user report?
2. **Assess impact** — who is affected? How many users? Is data at risk? Is the service down or degraded?
3. **Mitigate** — what's the fastest way to reduce impact? Rollback, feature flag, scaling, redirect? Do this before root-causing
4. **Root cause** — why did it happen? One change at a time when diagnosing. Check recent deployments, config changes, dependency updates, traffic patterns
5. **Fix** — surgical fix for the specific issue. Don't rearchitect under pressure
6. **Prevent recurrence** — what monitoring, test, or process change would catch this before users do?

## Output

An incident report: timeline, impact, root cause, resolution, and action items for prevention.
