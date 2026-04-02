---
description: When delegating work across multiple domain agents (CTO, CPO, GRC, architect, etc.), always route through the coordinator agent. The coordinator owns cross-team communication, ensures shared context, and prevents inconsistent updates.
alwaysApply: true
---

# Coordination Rule

When work spans multiple domain agents (e.g., briefing CTO + CPO + GRC Lead, or making changes that affect multiple domains), always delegate through the `coordinator:coordinator` agent rather than dispatching to individual agents directly.

The coordinator:
- Ensures all agents receive the same context
- Identifies cross-cutting concerns between domains
- Produces a unified summary rather than fragmented individual reports
- Prevents conflicting updates to shared documents

Direct agent delegation is fine for single-domain tasks (e.g., "update the data dictionary" → data-engineer only).
