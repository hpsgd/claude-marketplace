---
name: write-integration-guide
description: "Write a step-by-step integration tutorial — connecting your product with another service, framework, or platform."
argument-hint: "[integration target, e.g. 'Stripe payments' or 'GitHub webhooks']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write an integration guide for $ARGUMENTS. Structure: what you'll build (one sentence) → prerequisites (accounts, API keys, tools) → numbered steps with code AND expected output → complete runnable example at the end → troubleshooting. The complete example is mandatory — not just fragments. Developers want to clone and run.
