---
name: persona-definition
description: "Define a research-backed user persona grounded in real behaviour, not demographics or stereotypes. Use to represent a customer segment for product and design decisions."
argument-hint: "[user segment or product area to define persona for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Persona Definition

Define a persona for $ARGUMENTS.

## Rules

- Ground every attribute in evidence (support tickets, analytics, interviews, sales data)
- Focus on goals and behaviours, not demographics
- 3-5 personas maximum per product — more means segments aren't distinct
- A persona is an archetype, not a fictional character. No backstories, no human names
- Update when new evidence contradicts existing personas

## Persona Format

```markdown
## Persona: [descriptive name — e.g., "First-time evaluator" not "Sarah"]

**Segment:** [which customer segment]
**Evidence:** [data sources — N interviews, M support tickets, analytics from X]

### Context
- **Role:** [professional context]
- **Technical sophistication:** [novice / intermediate / advanced]
- **Decision authority:** [can buy solo, needs approval, influences but doesn't decide]
- **Time pressure:** [exploring leisurely / evaluating with deadline / urgent need]

### Goals
1. [Primary goal — what success looks like in their words]
2. [Secondary goal]

### Frustrations
1. [Current pain with existing solutions]
2. [What they've tried that didn't work]

### Behaviour Patterns
- **Discovery:** [how they find solutions]
- **Evaluation:** [how they compare options — features? price? reviews? trial?]
- **Decision:** [what tips them over the edge]
- **Learning:** [how they learn new tools — docs? video? trial-and-error?]

### Success Criteria
[How THEY would judge the product successful — in their words, not ours]

### Anti-Persona Signals
[Characteristics that indicate someone is NOT this persona — helps with segmentation]
```

## Validation Questions

After defining a persona, verify:
- Could two people on the team independently assign a real customer to this persona? (if not, it's too vague)
- Does this persona make different product decisions than another persona? (if not, merge them)
- Is every attribute backed by at least 3 data points? (if not, it's speculation)
