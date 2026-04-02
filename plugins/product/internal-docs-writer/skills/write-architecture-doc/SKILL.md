---
name: write-architecture-doc
description: "Write or update architecture documentation — system overview, component diagrams, data flows, bounded contexts, and key decisions."
argument-hint: "[system, service, or area to document]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write architecture documentation for $ARGUMENTS. Structure: context (what problem, who uses it) → key decisions (link to ADRs) → component overview with Mermaid diagram → data flow for key operations → bounded contexts (what each owns, how they communicate) → non-functional requirements → known limitations. Diagrams are mandatory. Document BOUNDARIES, not internals. Link to ADRs for every significant decision. Explain WHY, not just WHAT.
