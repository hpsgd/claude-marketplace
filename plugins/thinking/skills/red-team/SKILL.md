---
name: red-team
description: Adversarial analysis to stress-test an idea, plan, or argument. Use to find weaknesses before they find you.
argument-hint: "[idea, plan, or argument to attack]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Apply adversarial analysis to stress-test $ARGUMENTS. The goal is to find every weakness, not to be balanced.

**When to use red-team vs council:** Red team is purely adversarial — attack the idea to find breaking points. Council (`/council`) is collaborative-adversarial — experts debate to find the best path forward. Use red-team when you need to validate robustness; use council when you need to decide between options.

## Process

### 1. Decompose

Break the argument into atomic claims. Each claim should be independently testable. A plan with 5 sections might decompose into 15-25 atomic claims.

For each claim, classify:
- **Stated**: explicitly claimed
- **Implied**: assumed but not stated
- **Required**: necessary for the argument to hold but not mentioned

### 2. Attack each claim

For every claim, ask:
- What evidence would disprove this?
- Under what conditions does this fail?
- What's the weakest link in the reasoning?
- What's being assumed that hasn't been verified?
- Who would disagree and what's their strongest argument?

### 3. Steelman

Before presenting the attack, construct the **strongest possible version** of the argument:
- Fix obvious weaknesses
- Add the best supporting evidence
- Frame it in its most compelling form

This ensures the red team is attacking the best version, not a strawman.

### 4. Counter-argument

Present the devastating case against, structured as:

**Critical weaknesses** (would cause failure):
- [weakness] — evidence and reasoning

**Significant risks** (could cause failure under certain conditions):
- [risk] — conditions and likelihood

**Assumptions requiring verification** (unknown whether true):
- [assumption] — how to verify

### Output

1. **Steelman** — the strongest version of the argument (8 key points)
2. **Counter-argument** — the strongest case against (8 key points)
3. **Verdict** — overall assessment of robustness
4. **Recommendations** — what to address before proceeding
