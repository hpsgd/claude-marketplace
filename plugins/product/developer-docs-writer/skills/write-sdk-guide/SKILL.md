---
name: write-sdk-guide
description: "Write an SDK or client library guide — installation, quick start, configuration, common patterns, error handling."
argument-hint: "[SDK, client library, or language to document]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write an SDK guide for $ARGUMENTS. Structure: installation (package manager command) → quick start (authenticate + first API call in < 10 lines, must work with copy-paste) → configuration (all options with defaults) → common patterns (pagination, error handling, retry) → type definitions. Every code example must run. Use realistic data, not "test" or "foo".
