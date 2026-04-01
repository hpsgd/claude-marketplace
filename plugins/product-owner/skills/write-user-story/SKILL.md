---
name: write-user-story
description: Write user stories with acceptance criteria from a feature description or PRD section.
argument-hint: "[feature description or PRD reference]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Write user stories for $ARGUMENTS.

## Format

```
As a [user type], I want [action] so that [outcome].

Acceptance criteria:
- [ ] [Verifiable criterion 1]
- [ ] [Verifiable criterion 2]
```

## Rules

- **One behaviour per story.** If a story has "and" in the action, split it
- **User type is specific.** "As a user" is too vague. "As a first-time visitor who hasn't created an account" is specific
- **Action is concrete.** What the user does, not what the system does
- **Outcome is the value.** Why the user cares — the benefit, not the implementation
- **Acceptance criteria are verifiable.** Each criterion passes the ISC Splitting Test — independently testable, no compound conditions
- **Include edge cases.** What happens on empty state? Error? Timeout? Concurrent access?
- **Include anti-requirements.** What this story deliberately does NOT cover

## Output

Write each story with its acceptance criteria. Group related stories under a heading if there are more than 3.
