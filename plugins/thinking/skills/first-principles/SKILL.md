---
name: first-principles
description: Deconstruct a problem to fundamental truths and rebuild from scratch. Use when stuck, challenging inherited constraints, or making architecture decisions.
argument-hint: "[problem or assumption to decompose]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Apply first principles thinking to decompose $ARGUMENTS to fundamental truths rather than reasoning by analogy.

## The Framework

### 1. DECONSTRUCT — "What is this really made of?"

Break the problem down to its constituent parts and fundamental truths:
- What are the absolute physical/logical constraints? (things that cannot be changed)
- What are the policy/convention constraints? (things that could be changed but currently aren't)
- What are the assumptions? (things believed true but never verified)

List every component. For each, ask: "Is this a truth or an assumption?"

### 2. CHALLENGE — "Is this a real constraint or an assumption?"

Classify every constraint:
- **Hard constraint**: Laws of physics, mathematical limits, platform capabilities. Cannot be changed.
- **Soft constraint**: Policy, convention, "how it's always been done." Could be changed with authority.
- **Assumption**: Believed true but never tested. Must be verified or discarded.

For each assumption, ask: "What evidence would prove this wrong?" If no evidence exists, treat it as unverified.

### 3. RECONSTRUCT — "Given only the truths, what's optimal?"

Starting from only the verified truths and hard constraints:
- Design the solution as if no prior solution existed
- Ignore current form — focus on function
- Look for cross-domain analogies (how does biology/physics/another field solve this?)
- Build up from fundamentals, don't patch from the current state

## Principles

- **Physics First**: Start from what is physically/logically possible, not what's conventional
- **Function Over Form**: The current shape of a solution is irrelevant. Only the function matters
- **Question Everything**: "Because that's how it's done" is not a reason. It's an assumption
- **Cross-Domain Synthesis**: Solutions from other fields often unlock breakthroughs
- **Rebuild Don't Patch**: If the fundamentals point to a different architecture, say so

## Output

Present findings as:
1. **Fundamental truths** — what is actually true and cannot change
2. **Challenged assumptions** — what was assumed but isn't necessarily true
3. **Reconstructed approach** — what the solution looks like when built from truths alone
4. **Delta from current** — how this differs from the current approach and why
