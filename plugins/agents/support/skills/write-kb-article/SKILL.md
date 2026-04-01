---
name: write-kb-article
description: Write a knowledge base article from a resolved support issue, common question, or how-to topic.
argument-hint: "[topic, question, or resolved ticket summary]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Write a knowledge base article for $ARGUMENTS.

## Structure

1. **Title** — the question the user is asking, in their words
2. **Short answer** — 1-2 sentences answering the question directly (for scanners)
3. **Detailed steps** — numbered, each step is one action with expected outcome
4. **Troubleshooting** — common issues encountered while following the steps
5. **Related articles** — links to related topics

## Rules

- Write for the user's vocabulary, not the internal vocabulary
- One article answers one question completely
- Include screenshots or code examples where they clarify
- Test every step before publishing
- Date-stamp if the answer is version-specific
