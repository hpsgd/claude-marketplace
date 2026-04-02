---
name: creative
description: Divergent ideation and creative brainstorming. Use when you need novel solutions, want to break out of conventional thinking, or need multiple distinct approaches.
argument-hint: "[problem or challenge to brainstorm]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Generate diverse, creative solutions for $ARGUMENTS using structured divergent thinking. Follow every step — creativity without structure produces noise, not options.

## Step 1 — Understand before ideating

Before generating a single idea, understand the problem deeply:

```
Problem as stated: [what the user asked for]
Who has this problem: [specific people in specific situations]
Why it matters: [consequences of not solving it]
What's been tried: [existing approaches and why they're insufficient]
Constraints: [real constraints — budget, time, technical, organisational]
```

Do not skip this step. The most common failure mode in brainstorming is solving the wrong problem creatively.

## Step 2 — Reframe the problem (3 ways)

The way you frame a problem determines the solutions you can see. Reframe the problem in three fundamentally different ways:

### Reframe 1 — As a user story
"A [specific person] who needs [outcome] because [motivation], but currently [obstacle]."

This frame centres the human and their context. It often reveals that the real problem is different from the stated problem.

### Reframe 2 — As a constraint
"We can't do [assumed approach], so what else could work?"

Remove the most obvious solution and see what emerges. This forces you past the first idea.

### Reframe 3 — As an analogy
"This is like [something from a completely different domain] because [shared structure]."

Cross-domain analogies break fixedness. How does nature solve this? How does a restaurant solve this? How does a game solve this?

**After all three reframes, pick the framing that opens the most creative space.** State which one and why. This becomes the basis for ideation.

## Step 3 — Generate options using diversity-forcing techniques

Produce at least 5 genuinely different approaches. "Genuinely different" means each option represents a fundamentally different strategy, not a variation on the same idea.

### Mandatory diversity techniques

Apply each technique to generate at least one option. Not every technique will produce a winner — that's fine. The goal is to ensure you've explored the solution space widely.

#### Technique 1 — Inversion
**What if you did the opposite of the obvious approach?**
- If the obvious solution adds something, what if you removed something instead?
- If the obvious solution automates, what if you made it manual but better?
- If the obvious solution centralises, what if you distributed?

Generate one option from inversion.

#### Technique 2 — Extreme scale
**What if this needed to serve 1 user? What about 1 million?**
- The 1-user version strips away infrastructure and reveals the core value
- The 1-million-user version forces architectural thinking and reveals bottlenecks
- Often the best solution lives between these extremes but is visible from one of them

Generate one option from extreme scale thinking.

#### Technique 3 — Remove constraints
**What if [biggest constraint] didn't exist?**
- If budget weren't a limit, what would you build?
- If time weren't a factor, what would you do?
- If technology could do anything, what would be ideal?

Then work backwards: what fraction of that ideal solution is achievable within constraints?

Generate one option from constraint removal.

#### Technique 4 — Cross-domain transfer
**How does [unrelated field] solve a structurally similar problem?**

Domains to borrow from:
- **Nature** — evolution, ecosystems, ant colonies, immune systems
- **Games** — incentive design, progression systems, feedback loops
- **Architecture** — load-bearing structures, modularity, public vs. private space
- **Music** — composition, improvisation, harmony, rhythm
- **Cooking** — mise en place, flavour balancing, timing, presentation
- **Transportation** — routing, scheduling, hub-and-spoke, last-mile

Pick one domain. Identify the structural similarity. Extract the solution pattern.

Generate one option from cross-domain transfer.

#### Technique 5 — Worst idea first
**What's the absolute worst solution you could propose?**

Write it out. Then examine it seriously:
- What's accidentally interesting about it?
- What assumption does it violate that might be worth violating?
- What kernel of a good idea is hiding in the bad idea?

Generate one option by finding the good idea inside the bad one.

### Quality bar for options

Every option must pass all three tests:
1. **Distinct** — it represents a fundamentally different approach, not a variation of another option
2. **Feasible** — it could actually work given real constraints (or with clearly identified constraint changes)
3. **Specific** — it's concrete enough to evaluate. "Use AI" is not an option. "Train a classifier on historical support tickets to auto-route incoming tickets to the right team, reducing triage time from 4 hours to 15 minutes" is an option.

If you have fewer than 5 options that pass all three tests, go back to the techniques and push harder. If you have more than 8, you're probably not being distinct enough — consolidate.

## Step 4 — Evaluate honestly

For each option, provide:

```
### Option [N]: [Descriptive name]

**One-paragraph description:**
[What this option is and how it works]

**What's genuinely good about it:**
- [Specific strength — not "it's innovative" but "it reduces the feedback loop from days to minutes"]

**What's the biggest risk:**
- [The most likely way this fails]

**Effort to implement:**
[Low / Medium / High] — [one sentence justifying the estimate]

**Reversibility:**
[Easy to undo / Hard to undo / Irreversible] — this matters for decision-making

**Combinability:**
[Can elements of this option combine with other options? Which ones and how?]
```

### Evaluation rules
- Be genuinely honest about pros and cons. Advocacy for a favourite kills the value of divergent thinking.
- "Innovative" is not a pro. "Reduces cost by 60%" is a pro.
- "Risky" is not a con. "Requires 3 months of engineering time with uncertain demand" is a con.
- The effort estimate must be realistic, not optimistic. Double your first instinct.

## Step 5 — Combine and synthesise

After evaluating individually, look for combinations:

- Can the best elements of two options merge into something better?
- Can one option serve as the short-term solution while another is the long-term target?
- Can one option be the "safe bet" while another is the "high upside bet" — and can you pursue both?

If a combination emerges that's stronger than any individual option, describe it as a new hybrid option.

## Step 6 — Output

Present the results in this order:

### 1. Problem reframing
Show all three reframes. State which was selected and why.

### 2. Options (the full set)
Each option with the evaluation from Step 4, numbered and named.

### 3. Recommended path
Which option (or combination) to pursue and why. Structure as:

```
**Recommendation:** [Option name or combination]

**Why this one:**
- [Primary reason tied to the problem and constraints]
- [Secondary reason]

**What to do first:**
- [Immediate next step — make it concrete]

**What to watch for:**
- [Early signal that this is working or not working]
```

### 4. Wild card
One option that is unconventional, possibly uncomfortable, but worth serious consideration. Explain why it shouldn't be dismissed.

```
**Wild card: [Name]**
Why it seems wrong: [the obvious objection]
Why it might be right: [the non-obvious argument]
When to revisit: [under what conditions this becomes the best option]
```

## Rules

- The goal is options, not answers. Resist the urge to converge too early. Step 3 is about expanding the solution space; Step 5 is about converging.
- Genuinely different means genuinely different. Five variations on "build a web app" is one option, not five. Push past the obvious.
- Every option must be concrete enough that someone could say "yes, let's do that" and know what happens next.
- The wild card is mandatory. It's a hedge against groupthink and conventional wisdom. The best ideas often start as the weird one.
- Don't filter ideas by what's been tried before. If something was tried and failed, ask why it failed — the reason might no longer apply.
- Quantity enables quality. Generate broadly in Step 3, evaluate ruthlessly in Step 4. Mixing generation and evaluation kills creativity.
- Name every option. A named option is easier to discuss, reference, and decide on than "Option 3." Names should be descriptive and memorable.
