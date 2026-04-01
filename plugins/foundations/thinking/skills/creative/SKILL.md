---
name: creative
description: Divergent ideation and creative brainstorming. Use when you need novel solutions, want to break out of conventional thinking, or need multiple distinct approaches.
argument-hint: "[problem or challenge to brainstorm]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Generate diverse, creative solutions for $ARGUMENTS using structured divergent thinking.

## Process

### 1. Reframe the problem

Before generating solutions, reframe the problem in at least 3 different ways:
- As a user story: "A person who needs X because Y"
- As a constraint: "We can't do Z, so what else could work?"
- As an analogy: "This is like [something from another domain] because..."

Pick the framing that opens the most creative space.

### 2. Generate diverse options

Produce 5+ genuinely different approaches. Each must be:
- **Distinct** — not a variation of another option, but a fundamentally different approach
- **Feasible** — could actually work given real constraints
- **Specific** — concrete enough to evaluate, not vague platitudes

Techniques to force diversity:
- **Inversion**: What if you did the opposite?
- **Extreme scale**: What if this needed to serve 1 user? 1 million?
- **Remove constraints**: What if budget/time/technology weren't limits?
- **Cross-domain**: How does nature/music/architecture/gaming solve this?
- **Worst idea first**: What's the worst solution? Now find what's interesting about it

### 3. Evaluate and combine

For each option:
- What's genuinely good about it?
- What's the biggest risk?
- Could elements combine with other options?

### Output

Present as:
1. **Problem reframing** — the 3 reframes and which was chosen
2. **Options** — each with a name, one-paragraph description, and honest pros/cons
3. **Recommended path** — which option (or combination) and why
4. **Wild card** — one option that's unconventional but worth considering
