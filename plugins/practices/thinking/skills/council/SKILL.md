---
name: council
description: Simulate a structured debate between diverse expert perspectives. Use when weighing options, making decisions, or needing multiple viewpoints on a problem.
argument-hint: "[question, decision, or proposal to debate]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Convene a council of diverse perspectives to debate $ARGUMENTS through genuine intellectual friction.

## How This Differs From Red Team

Council is **collaborative-adversarial** — experts debate to find the best path forward, building on each other's points. Red Team is **purely adversarial** — the goal is to break the argument.

## Process

### Round 1 — Opening positions

Define 4 perspectives relevant to the topic. Each perspective:
- States their position clearly
- Provides their strongest argument
- Identifies their primary concern

Choose perspectives that create genuine tension — not 4 people who agree.

Example perspectives for a technical decision:
- **The Pragmatist**: What ships fastest and works well enough?
- **The Architect**: What's the right long-term design?
- **The User Advocate**: What do users actually experience?
- **The Skeptic**: What could go wrong? What are we not seeing?

### Round 2 — Responses

Each perspective responds to the others' actual points:
- Where they agree (and why)
- Where they disagree (and why — with specifics)
- What the other perspectives are missing

This must be genuine engagement, not performative disagreement.

### Round 3 — Synthesis

Each perspective:
- States what they learned from the debate
- Identifies where they've shifted position
- Proposes a path forward that addresses the strongest objections

### Final Synthesis

Across all perspectives:
1. **Points of consensus** — what everyone agrees on
2. **Remaining tensions** — genuine disagreements that can't be resolved by debate alone
3. **Recommended decision** — weighing the strongest arguments from all sides
4. **Risk register** — concerns raised that should be monitored regardless of decision
