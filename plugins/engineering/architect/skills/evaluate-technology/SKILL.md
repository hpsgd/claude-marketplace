---
name: evaluate-technology
description: Evaluate a technology, framework, or tool against specific criteria. Produces a structured comparison with trade-offs and a recommendation.
argument-hint: "[technology to evaluate, or 'X vs Y' comparison]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep, WebSearch, WebFetch
---

Evaluate $ARGUMENTS for fitness against the project's needs.

## Process

### 1. Define evaluation criteria

Before researching, establish what matters:

| Criterion | Weight | Why it matters |
|---|---|---|
| Maturity / stability | | Production readiness |
| Community / ecosystem | | Long-term support, plugins, answers |
| Team familiarity | | Ramp-up cost |
| Performance | | Meets non-functional requirements |
| Maintenance burden | | Ongoing cost of ownership |
| Lock-in risk | | Can we switch later? |
| Cost | | Licensing, infrastructure, operational |
| Integration | | Works with existing stack |

Adjust criteria and weights based on the specific evaluation.

### 2. Research each option

For each technology:
- What is it? One-sentence description
- Who uses it? Notable adopters
- How mature is it? Version, release cadence, breaking change history
- What's the community like? GitHub stars, npm downloads, Stack Overflow activity, Discord/forum activity
- What are the known issues? Search for "[tech] problems", "[tech] limitations", "[tech] alternatives"

### 3. Score against criteria

Rate each option against each criterion (1-5). Show your reasoning, not just the score.

### 4. Recommendation

- Which option and why
- What you'd monitor after adoption (risks to watch)
- What would trigger reconsideration

## Output

Present as a structured comparison table with scores, then a written recommendation with reasoning. If the evaluation warrants it, suggest writing a formal ADR using `/hpsgd:write-adr`.
