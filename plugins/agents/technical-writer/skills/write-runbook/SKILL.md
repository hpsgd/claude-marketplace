---
name: write-runbook
description: Write an operational runbook for a service, deployment, or incident response procedure.
argument-hint: "[service, procedure, or incident type]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a runbook for $ARGUMENTS.

## Structure

1. **Overview** — What this runbook covers, when to use it
2. **Prerequisites** — Access, tools, permissions needed
3. **Steps** — Numbered, each step is one action with expected outcome. Include the exact commands to run
4. **Verification** — How to confirm each step succeeded
5. **Rollback** — How to undo if something goes wrong
6. **Troubleshooting** — Common issues and their fixes
7. **Contacts** — Who to escalate to if the runbook doesn't resolve it

Every command should be copy-pasteable. Every step should have a verification check. Never assume the reader knows the system — write for someone handling this for the first time at 2am.
