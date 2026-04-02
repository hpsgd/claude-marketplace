---
status: "{proposed | accepted | deprecated | superseded by ADR-NNNN}"
date: {YYYY-MM-DD}
decision-makers: []
consulted: []
informed: []
---

# ADR-NNNN: {Short title — describes the problem and solution}

## Context and Problem Statement

{Describe the context and problem statement in 2-3 sentences. What situation requires a decision? What forces are at play? Frame as a question if helpful.}

## Decision Drivers

* {Decision driver 1 — a force, constraint, or concern}
* {Decision driver 2}
* {Decision driver 3}

## Assumptions

| Assumption | Classification | Evidence / Risk if wrong |
|---|---|---|
| {What you believe to be true} | `proven_by_code` / `inferred` / `needs_confirmation` | {Citation or consequence} |
| {Another assumption} | | |

## Considered Options

1. {Title of option 1}
2. {Title of option 2}
3. {Title of option 3}

### Options Analysis

| Criterion | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| {Decision driver 1} | {1-5 + reasoning} | {1-5 + reasoning} | {1-5 + reasoning} |
| {Decision driver 2} | | | |
| {Decision driver 3} | | | |
| Complexity | | | |
| Reversibility | | | |
| Team familiarity | | | |

## Decision Outcome

Chosen option: **"{title of chosen option}"**, because {justification — which decision drivers does it satisfy? What makes it better than the alternatives?}.

### Consequences

**Positive:**
* {What gets better as a result of this decision}

**Negative:**
* {What gets worse or harder — be honest}
* {What technical debt is accepted}

**Risks:**
* {What could go wrong with this decision}
* {What would trigger reconsideration}

### Change Impact

**Direct impacts:**

| Component | Change | Risk |
|---|---|---|
| {affected component} | {what changes} | Low / Medium / High |

**Indirect impacts:**

| Component | Reason affected | Risk |
|---|---|---|
| {component} | {why it's impacted} | Low / Medium / High |

**Unaffected (explicitly stated):**

| Component | Reason unaffected |
|---|---|
| {component} | {why it is NOT impacted — state explicitly} |

### Confirmation

{How will we know this decision is working? Review criteria, automated tests, metrics to watch, or conditions that would trigger revisiting this ADR.}

## Pros and Cons of the Options

### Option 1: {title}

{Brief description or link to more detail}

* Good, because {argument}
* Good, because {argument}
* Bad, because {argument}
* Neutral, because {argument}

### Option 2: {title}

* Good, because {argument}
* Bad, because {argument}

### Option 3: {title}

* Good, because {argument}
* Bad, because {argument}

## More Information

{Additional context: links to related ADRs, research, prototypes, or team discussions. Include when this decision should be reviewed.}
