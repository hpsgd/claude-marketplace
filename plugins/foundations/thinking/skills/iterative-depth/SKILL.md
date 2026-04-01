---
name: iterative-depth
description: Analyse a problem through multiple structured passes from different lenses. Use for requirements analysis, architecture decisions, or any problem that benefits from multi-angle examination.
argument-hint: "[problem or decision to analyse]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Run structured passes through $ARGUMENTS from systematically different lenses to extract deeper understanding than single-pass analysis.

## Why This Works

Single-pass analysis captures one perspective. Each additional lens surfaces requirements, edge cases, and criteria invisible from other angles. The combination yields richer understanding than any single perspective.

Grounded in: Hermeneutic Circle (iterative interpretation), Triangulation (multiple data sources), Six Thinking Hats (de Bono), Causal Layered Analysis, Viewpoint-Oriented Requirements Engineering.

## The Lenses

Select 3-5 lenses appropriate to the problem from:

1. **User lens** — Who uses this? What do they actually need? What frustrates them?
2. **Technical lens** — What are the constraints? What's possible? What's hard?
3. **Business lens** — What's the cost? What's the value? What's the risk?
4. **Adversarial lens** — How could this fail? What would an attacker do? What's the worst case?
5. **Temporal lens** — What happens in 6 months? 2 years? What's the migration path?
6. **Simplicity lens** — What's the simplest version that works? What can be removed?
7. **Precedent lens** — How have others solved this? What worked? What didn't?
8. **Edge case lens** — What about empty inputs? Concurrent access? Network failure? Scale?

## Process

For each selected lens:
1. State the lens and its focus question
2. Analyse the problem through that specific lens
3. List findings unique to this perspective
4. Note any contradictions with previous lenses

## Synthesis

After all passes:
1. **Convergent findings** — What appeared across multiple lenses?
2. **Tensions** — Where do lenses contradict? How to resolve?
3. **Blind spots filled** — What did later lenses reveal that earlier ones missed?
4. **Refined criteria** — Updated success criteria incorporating all perspectives
