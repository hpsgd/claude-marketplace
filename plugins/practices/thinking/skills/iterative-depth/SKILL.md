---
name: iterative-depth
description: Analyse a problem through multiple structured passes from different lenses. Use for requirements analysis, architecture decisions, or any problem that benefits from multi-angle examination.
argument-hint: "[problem or decision to analyse]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Run structured multi-lens analysis on $ARGUMENTS. Follow every step below — the value of this approach comes from completing the full process, not from any single lens.

## Why multi-lens analysis works

Single-pass analysis captures one perspective and gives you confidence you don't deserve. Each additional lens surfaces requirements, edge cases, risks, and opportunities invisible from other angles. The combination yields richer understanding than any single perspective — and the contradictions between lenses are where the most important insights live.

Grounded in: Hermeneutic Circle (iterative interpretation), Triangulation (multiple evidence sources), Six Thinking Hats (de Bono), Causal Layered Analysis, Viewpoint-Oriented Requirements Engineering.

## Step 1 — Frame the problem

Before selecting lenses, write a clear problem statement:

```
Problem: [one sentence describing the decision or problem]
Context: [why this matters, what triggered the analysis]
Constraints: [known constraints — time, budget, technical, organisational]
Stakeholders: [who is affected by or has input on this decision]
Current state: [what exists today]
Desired state: [what "solved" looks like]
```

This framing will be tested and refined by each lens. Expect it to evolve.

## Step 2 — Select lenses

Choose 3-5 lenses from the eight below. Select based on the nature of the problem — not every lens applies to every problem. The table includes guidance on when each lens is most valuable.

### The eight lenses

| # | Lens | Core question | Best for | Key risk if skipped |
|---|---|---|---|---|
| 1 | **User** | Who uses this, what do they actually need, and what frustrates them? | Product decisions, UX, feature design | Building something nobody wants |
| 2 | **Technical** | What are the constraints, what's possible, and what's hard? | Architecture, implementation, feasibility | Committing to the impossible |
| 3 | **Business** | What's the cost, value, risk, and return? | Investment decisions, prioritisation, strategy | Spending money on the wrong thing |
| 4 | **Adversarial** | How could this fail, be attacked, or go wrong? | Security, reliability, risk management | Blind spots that become incidents |
| 5 | **Temporal** | What happens in 6 months, 2 years, 5 years? What's the migration path? | Architecture, strategy, hiring, process | Painting yourself into a corner |
| 6 | **Simplicity** | What's the simplest version that works? What can be removed? | Scope decisions, MVP definition, refactoring | Over-engineering, scope creep |
| 7 | **Precedent** | How have others solved this? What worked, what failed, and why? | Proven patterns, avoiding known mistakes | Repeating industry mistakes |
| 8 | **Edge case** | What about empty inputs, concurrent access, network failure, scale, abuse? | Technical design, API design, testing | Production surprises |

### Lens selection rules

- Always include at least one "human" lens (User or Business) and one "system" lens (Technical or Edge case)
- If the problem involves money, include Business
- If the problem involves security or reliability, include Adversarial
- If the problem has long-term consequences, include Temporal
- If the problem feels complex, include Simplicity as a counterweight
- If you're unsure which lenses to pick, start with User + Technical + Adversarial — this combination catches the most issues

State which lenses you selected and why.

## Step 3 — Analyse through each lens

For each selected lens, follow this exact structure:

```
### Lens [N]: [Name]

**Focus question:** [The specific question this lens asks about this problem]

**Analysis:**
[Deep analysis from this perspective. Not a surface-level paragraph — spend real effort here.
Ask and answer at least 3 sub-questions specific to this lens and this problem.]

**Findings unique to this lens:**
1. [Something this lens revealed that no previous lens surfaced]
2. [Another unique finding]
3. [Another unique finding]

**Contradictions with previous lenses:**
- [Where this lens disagrees with a finding from a previous lens, and why]
- [If no contradictions: "No contradictions — this lens reinforces [specific finding] from [lens name]"]

**Risks identified:**
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [risk] | High/Med/Low | High/Med/Low | [what to do] |

**Open questions:**
- [Questions this lens raised that need answers from stakeholders, data, or further investigation]
```

### Rules for per-lens analysis

- **Go deep, not wide.** Each lens should produce genuine insight, not a paragraph that restates the obvious. Ask "so what?" after every finding — if the answer is "obviously," dig deeper.
- **Findings must be specific to this problem.** "Users want good UX" is not a finding. "Users in this workflow switch between three tools, so a solution that requires a fourth tool will face adoption resistance" is a finding.
- **Contradictions are the most valuable output.** When two lenses disagree, you've found a tension that requires a deliberate trade-off. Don't smooth over contradictions — highlight them.
- **Each lens must produce at least one finding not surfaced by any previous lens.** If a lens adds nothing new, either the analysis was too shallow or the lens was a poor choice — go deeper or swap it.

## Step 4 — Synthesise

After completing all lenses, synthesise the findings. This is where the real value emerges.

### Convergent findings

What appeared across multiple lenses? These are your highest-confidence conclusions.

```
| Finding | Supported by lenses | Confidence | Implication |
|---|---|---|---|
| [finding] | [lens names] | High / Medium | [what this means for the decision] |
```

A finding supported by 3+ lenses is almost certainly important. Act on it.

### Tensions and trade-offs

Where do lenses contradict? These require deliberate choices.

```
| Tension | Lens A says | Lens B says | Recommended resolution | Rationale |
|---|---|---|---|---|
| [topic] | [position] | [position] | [which side to favour] | [why] |
```

For each tension, make a recommendation. Don't leave trade-offs unresolved — the whole point of this analysis is to reach a better decision.

### Blind spots filled

What did later lenses reveal that earlier ones missed? This demonstrates the value of multi-lens analysis and highlights areas where single-perspective thinking would have failed.

```
| Blind spot | Revealed by | Would have caused | Prevention |
|---|---|---|---|
| [what was missed] | [lens name] | [consequence of missing it] | [how to catch this in the future] |
```

### Revised problem framing

Based on the analysis, rewrite the problem statement from Step 1. It should now be sharper, more nuanced, and account for what you learned.

```
Original framing: [from Step 1]
Revised framing: [incorporating insights from all lenses]
Key difference: [what changed and why it matters]
```

### Refined success criteria

Based on all lenses, define what "success" looks like:

```
| Criterion | Source lens | Metric | Threshold |
|---|---|---|---|
| [criterion] | [which lens identified this] | [how to measure] | [what "good" looks like] |
```

### Recommendation

State a clear recommendation with:

```
**Recommendation:** [what to do]

**Confidence:** [High / Medium / Low] — based on [what evidence]

**Key risks:** [top 2-3 risks and their mitigations]

**Next steps:**
1. [Immediate action]
2. [Follow-up action]
3. [Validation step]

**What would change this recommendation:**
- [If X turns out to be true, reconsider Y]
- [If Z happens, switch to approach W]
```

## Rules

- The lenses are a tool for thinking, not a template to fill in. If a lens isn't generating insight, go deeper before moving on.
- Contradictions between lenses are not problems — they're the most valuable output. They reveal trade-offs that must be made consciously.
- Every finding must be actionable. "This is complex" is not a finding. "This has three competing constraints that require a trade-off between X and Y" is actionable.
- Don't anchor on the first lens. The purpose of multi-lens analysis is to challenge your initial perspective, not confirm it. If every lens agrees with the first one, you're not trying hard enough.
- State your confidence level honestly. An analysis with "Medium confidence due to missing user data" is more useful than one with false certainty.
- The synthesis matters more than any individual lens. Spend at least as much effort on Step 4 as on any single lens in Step 3.

## Related Skills

- `/council` — when iterative-depth reveals irreconcilable tensions between lenses, convene a council to debate the trade-offs.
- `/first-principles` — when a lens reveals that the problem framing itself is wrong, decompose to fundamentals.
