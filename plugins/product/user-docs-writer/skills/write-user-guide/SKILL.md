---
name: write-user-guide
description: "Write a task-oriented user guide for a feature or workflow. Written in product language for non-technical readers."
argument-hint: "[feature or workflow to document]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a user guide for $ARGUMENTS. Structure: title (what the user wants to accomplish) → introduction (one paragraph) → prerequisites → numbered steps (one action each with expected result) → troubleshooting → next steps. Use product language, no jargon. Test every step yourself before publishing. Every step must have an expected result so the reader knows they're on track.
