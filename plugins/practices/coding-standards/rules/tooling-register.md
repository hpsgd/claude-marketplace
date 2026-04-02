---
description: Convention for documenting organisational tool choices. Ensures all agents know which tools are standard for each function.
---

# Tooling Register Convention

Every project should maintain a `docs/tooling-register.md` that maps functions to adopted tools. This prevents agents from recommending alternatives to tools the team has already committed to, and gives new team members a single place to find what's in use.

## Format

The register is a table with these columns:

| Column | Purpose |
|---|---|
| **Function** | What the tool does (e.g. "CI/CD", "Error tracking") |
| **Tool** | The specific product or service |
| **Why** | One-line rationale for choosing it |
| **Status** | Adopt / Trial / Hold (see below) |
| **Owner** | Team or person responsible for the tool |
| **Link** | Documentation or dashboard URL |

## Status Definitions

Based on the [ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar) ring model, simplified to three levels:

- **Adopt** — Standard choice. Use for all new work. No ADR needed to use it.
- **Trial** — Approved for limited use. Being evaluated. Document findings before promoting to Adopt.
- **Hold** — Do not use for new work. Existing usage is being migrated away. Requires an ADR to justify any new adoption.

## Standard Functions

Every register should cover at minimum:

- Source control
- Issue tracking
- CI/CD
- Monitoring / APM
- Error tracking
- Logging
- Communication
- Documentation hosting
- Design tools
- Cloud provider
- Container registry
- Secret management

## Rules for Agents

- **Check the register first.** Before recommending a tool, check `docs/tooling-register.md`. If the function has an Adopt-status tool, use it — don't suggest alternatives.
- **Tool changes require an ADR.** Switching from an adopted tool to a different one is an architecture decision. Document the rationale, trade-offs, and migration plan in `docs/adr/`.
- **Missing register is a finding.** If a project lacks a tooling register, flag it and offer to generate one from the template in `/coding-standards/templates/tooling-register.md`.
