---
name: first-principles
description: "Deconstruct a problem to fundamental truths and rebuild from scratch. Use when stuck, challenging inherited constraints, or making architecture decisions where convention may be wrong."
argument-hint: "[problem or assumption to decompose]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Apply first-principles thinking to decompose $ARGUMENTS to fundamental truths rather than reasoning by analogy.

## Step 1: Deconstruct — "What is this really made of?" (mandatory)

Break the problem into its constituent parts and classify every constraint:

```markdown
### Component inventory

| Component | Type | Evidence |
|---|---|---|
| [component] | Hard constraint | [why this cannot change — physics, math, platform limit] |
| [component] | Soft constraint | [why this could change — policy, convention, habit] |
| [component] | Assumption | [believed true but never verified — no evidence] |
```

**How to identify assumptions:**
- "We've always done it this way" → assumption
- "The framework requires this" → verify — is it the framework or your usage of it?
- "Users expect this" → assumption unless backed by data
- "It won't scale" → assumption unless load-tested
- "It's too expensive" → assumption unless costed

For each assumption, state: **"What evidence would prove this wrong?"** If no evidence exists either way, mark it as unverified.

**Output:** Complete component inventory with every constraint classified and assumptions flagged.

## Step 2: Challenge — "Is this real or inherited?" (mandatory)

Take every soft constraint and assumption from Step 1 and pressure-test it:

```markdown
### Challenge ledger

| # | Constraint/Assumption | Challenge | Verdict | Impact if removed |
|---|---|---|---|---|
| 1 | [item] | [What evidence supports it? Who decided this and when?] | Keep / Remove / Test | [What becomes possible if this isn't true] |
| 2 | [item] | [challenge] | [verdict] | [impact] |
```

**Challenge questions for each item:**
- Who created this constraint and what was their context? (Context may have changed)
- What would a newcomer with no history question about this?
- Does this constraint exist in comparable systems? If not, why here?
- What's the cost of keeping this constraint vs. removing it?

**Rules for challenges:**
- Hard constraints cannot be challenged — they are laws of physics or mathematics
- Soft constraints CAN be challenged — the question is whether the cost of change is worth it
- Assumptions MUST be challenged — they are the primary source of unnecessary complexity

**Output:** Challenge ledger with verdicts and impact analysis.

## Step 3: Reconstruct — "Given only the truths, what's optimal?" (mandatory)

Starting from ONLY the verified truths and hard constraints (everything marked "Keep" or "Hard constraint"):

```markdown
### Reconstruction

**Starting from these truths only:**
1. [truth 1 — hard constraint or verified fact]
2. [truth 2]
3. [truth N]

**Ignoring current implementation, the optimal solution would:**
- [design decision] — because [reasoning from first principles]
- [design decision] — because [reasoning]

**Cross-domain insight:** [How does biology/physics/another field solve an analogous problem?]
```

**Rules for reconstruction:**
- Design as if no prior solution existed. Ignore current form — focus on function
- If the reconstruction looks identical to the current approach, you haven't challenged enough assumptions — return to Step 2
- Cross-domain analogies are not mandatory but often unlock breakthroughs

**Output:** Reconstructed approach built from verified truths only.

## Step 4: Delta analysis (mandatory)

Compare the reconstructed approach with the current state:

```markdown
### Delta from current approach

| Aspect | Current | Reconstructed | Why different |
|---|---|---|---|
| [aspect] | [current approach] | [first-principles approach] | [which assumption removal enabled this] |

### Migration assessment
- **Quick wins:** [Changes that can be made immediately with low risk]
- **Requires validation:** [Changes that depend on unverified assumptions — need experiments first]
- **Requires authority:** [Changes that challenge soft constraints set by policy — need stakeholder buy-in]
```

**Output:** Delta table and migration assessment.

## Rules

- **Physics first.** Start from what is physically or logically possible, not what is conventional. Convention is a local optimum; first principles finds the global one.
- **Function over form.** The current shape of a solution is irrelevant. Only the function it serves matters. "We use a queue here" is form. "We need to decouple the producer from the consumer" is function.
- **Question everything, but respect hard constraints.** "Because that's how it's done" is an assumption. "Because of the speed of light" is not. Know the difference.
- **Rebuild, don't patch.** If the fundamentals point to a different architecture, say so. First-principles thinking that concludes "change nothing" has failed.
- **Never confuse unfamiliarity with impossibility.** "We've never done it that way" is not evidence that it won't work. It's evidence that it hasn't been tried.

## Output Format

```markdown
## First Principles: [problem]

### Component Inventory
[Classified constraints table from Step 1]

### Challenge Ledger
[Pressure-tested assumptions from Step 2]

### Reconstruction
[Solution built from verified truths from Step 3]

### Delta Analysis
[Comparison with current approach from Step 4]

### Recommendations
- Quick wins: [immediately actionable]
- Needs validation: [requires experiment]
- Needs authority: [requires stakeholder decision]
```

## Related Skills

- `/council` — when reconstruction reveals multiple valid paths and a decision is needed.
- `/red-team` — to stress-test the reconstructed approach before committing.
- `/scientific-method` — when assumptions need experimental validation, not just logical challenge.
