---
name: define-okrs
description: Define OKRs (Objectives and Key Results) for a product initiative, quarter, or team.
argument-hint: "[initiative, quarter, or team to define OKRs for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Define OKRs for $ARGUMENTS.

## Structure

```
Objective: [Qualitative, inspiring, time-bound goal]

  KR1: [Quantitative measure] — from [baseline] to [target]
  KR2: [Quantitative measure] — from [baseline] to [target]
  KR3: [Quantitative measure] — from [baseline] to [target]
```

## Rules

- **Objectives are qualitative.** They describe the desired outcome in human terms, not numbers
- **Key Results are quantitative.** Each has a number, a baseline, and a target. "Improve onboarding" is an objective. "Reduce time-to-first-value from 15 minutes to 3 minutes" is a key result
- **3-5 key results per objective.** Fewer means the objective isn't well-defined. More means it's too broad
- **Key results are outcomes, not outputs.** "Ship feature X" is an output. "Increase activation rate from 40% to 65%" is an outcome
- **Include the baseline.** A target without a baseline is meaningless. If the baseline is unknown, the first KR should be to measure it
- **Stretch but achievable.** 70% completion should feel like a good result. 100% means the targets were too easy

## Output

Present 2-4 objectives with 3-5 key results each. Include the measurement method for each KR (how will we know?).
