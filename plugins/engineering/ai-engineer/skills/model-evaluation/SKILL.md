---
name: model-evaluation
description: Evaluate and compare models for a use case — quality, latency, cost, reliability, and safety benchmarks on your own data.
argument-hint: "[AI use case or feature to select a model for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Evaluate and select a model for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Requirements Definition

Define pass/fail criteria before evaluating any model. These are hard requirements, not nice-to-haves.

| Requirement | Question | Example |
|---|---|---|
| Quality threshold | What is the minimum acceptable accuracy on your eval set? | >= 90% accuracy on classification, >= 85% on generation |
| Latency budget | What is the maximum acceptable response time? | p95 < 2 seconds TTFT, p95 < 5 seconds total |
| Cost budget | What can you spend per request and per month? | < $0.02 per request, < $3,000/month at projected volume |
| Context window | How much input data must fit in a single request? | Typical: 2K tokens, maximum: 15K tokens |
| Reliability | What error and timeout rates are acceptable? | < 0.5% error rate, < 1% timeout rate |
| Safety | What refusal rate on valid inputs is tolerable? | < 2% false refusal rate on legitimate requests |

If any requirement is undefined, stop and clarify. Evaluating without requirements is benchmarking for entertainment, not engineering.

### Step 2: Candidate Selection

Identify 2-4 candidate models using the tiered strategy. Do not evaluate more than 4 — diminishing returns.

| Tier | Model class | When to consider | Cost profile |
|---|---|---|---|
| **Fast** | Small/cheap (Haiku-class) | Classification, extraction, formatting, routing, mechanical tasks | Lowest |
| **Standard** | Mid-range (Sonnet-class) | Most features — summarisation, analysis, general generation | Moderate |
| **Capable** | Large (Opus-class) | Complex reasoning, creative generation, critical decisions | Highest |

**Default to Standard.** Only include Capable-tier candidates when Standard demonstrably fails on representative examples. Only include Fast-tier when the task is mechanical and Standard is unnecessarily expensive.

Select candidates:

| # | Model | Tier | Provider | Rationale for inclusion |
|---|---|---|---|---|
| C1 | | | | |
| C2 | | | | |
| C3 | | | | |

### Step 3: Evaluation Dataset

Build a representative eval set from real usage data. Synthetic data is acceptable only when real data does not yet exist.

**Minimum requirements:**
- 50 examples total
- Happy path: 60% of examples — typical, well-formed inputs
- Edge cases: 25% of examples — boundary conditions, unusual but valid inputs
- Adversarial: 15% of examples — malformed inputs, injection attempts, contradictory data

**Each example must include:**
- Input data (the actual prompt input)
- Expected output (the correct/ideal response)
- Scoring criteria (how to judge correctness — exact match, semantic similarity, rubric)

Store the eval set in version control alongside the prompts. The eval set is as important as the code.

### Step 4: Evaluation Dimensions

Measure every candidate across all six dimensions. No partial evaluations — a model that scores well on quality but has unknown latency is not evaluated.

| Dimension | Metric | How to measure | Weight |
|---|---|---|---|
| **Quality** | Eval set accuracy | Run all 50+ examples, score against expected outputs. Use automated scoring where possible, human review for subjective quality | Primary |
| **Latency** | TTFT + total generation time | Time each request. Report p50, p95, p99. Test at expected concurrency, not just sequential | High |
| **Cost** | Per-request cost | (input tokens x input price) + (output tokens x output price) x projected volume | High |
| **Reliability** | Error rate + timeout rate | Run eval set 3 times. Record failures, timeouts (>30s), inconsistent outputs across runs | Medium |
| **Context window** | Maximum input capacity | Test with largest expected input. Verify quality does not degrade near the window limit | Pass/fail |
| **Safety** | Refusal rate on valid inputs | Count how many legitimate eval examples the model refuses. Also test adversarial inputs from the eval set | Medium |

### Step 5: Run Evaluation

Test each candidate against the full eval set under consistent conditions.

**Methodology rules:**
- Same prompts for every candidate. Adjust only for model-specific formatting requirements (e.g., system/user message structure)
- Same eval data, same order, same conditions
- Temperature 0 for deterministic tasks. Record temperature setting for non-deterministic tasks
- Run at least 3 passes to measure consistency. A model that scores 95% once and 70% the next time is not a 95% model
- Record raw outputs for every example — you will need them for failure analysis

**Record results per candidate:**

```markdown
### [Model Name] — Results

| Dimension | Result | Meets requirement? |
|---|---|---|
| Quality | [X]% accuracy (N/50 correct) | YES / NO |
| Latency (p95) | TTFT: [X]ms, Total: [X]ms | YES / NO |
| Cost | $[X] per request, $[X]/month projected | YES / NO |
| Reliability | [X]% error rate, [X]% timeout rate | YES / NO |
| Context window | Tested at [X] tokens, quality maintained | YES / NO |
| Safety | [X]% refusal rate on valid inputs | YES / NO |

**Failure analysis:**
- [List specific eval examples that failed and why]
- [Common failure patterns]
```

### Step 6: Comparison Analysis

Side-by-side comparison. The question is not "which model is best" but "which model meets all requirements at the lowest cost."

| Dimension | Requirement | C1: [model] | C2: [model] | C3: [model] |
|---|---|---|---|---|
| Quality | >= [X]% | [score] | [score] | [score] |
| Latency (p95) | < [X]ms | [value] | [value] | [value] |
| Cost/request | < $[X] | [value] | [value] | [value] |
| Cost/month | < $[X] | [value] | [value] | [value] |
| Reliability | < [X]% errors | [value] | [value] | [value] |
| Context window | [X] tokens | [pass/fail] | [pass/fail] | [pass/fail] |
| Safety | < [X]% refusals | [value] | [value] | [value] |
| **All requirements met?** | | YES / NO | YES / NO | YES / NO |

**Trade-off documentation:**
- If multiple candidates meet all requirements, select the cheapest
- If no candidate meets all requirements, document which requirements are missed and by how much. Escalate — do not compromise requirements silently
- If quality is close between two models, prefer the cheaper one. A 1% quality improvement rarely justifies 3x cost

### Step 7: Decision and Fallback

Document the selection with reasoning tied directly to requirements. No vague justifications.

**Decision template:**

```markdown
### Selected model: [model name]

**Rationale:**
- Meets all [N] requirements
- Quality: [X]% (above [threshold]% threshold)
- Latency: [X]ms p95 (within [budget]ms budget)
- Cost: $[X]/request, $[X]/month (within $[budget]/month budget)
- [Specific advantage over other candidates that met requirements]

**Trade-offs accepted:**
- [What you sacrifice by choosing this model over alternatives]
- [Any requirement that is met with thin margin — risk area]
```

**Fallback plan (MANDATORY):**

| Scenario | Fallback action |
|---|---|
| Primary model unavailable | Route to [fallback model] — tested against eval set, meets requirements with [trade-off] |
| Sustained latency degradation | Switch to [faster model] with [quality trade-off described] |
| Cost spike | Rate limit to [N] requests/minute, alert team |
| Quality degradation detected | Roll back to previous model version, trigger re-evaluation |

Without a fallback plan, you are one outage away from a broken feature.

## Anti-Patterns (NEVER do these)

- **Choosing based on benchmarks, not your data** — public benchmarks measure general capability. Your use case is specific. Evaluate on YOUR eval set
- **No eval set** — picking a model without evaluation data is guessing. Build the eval set first
- **Evaluating on happy path only** — edge cases and adversarial inputs reveal the real quality gap between models
- **Ignoring cost** — a feature that works perfectly but costs 10x budget is not a working feature. Cost is a first-class metric
- **No fallback plan** — every AI call can fail. Every model can degrade. Plan for it
- **Comparing under different conditions** — different prompts, different data, different concurrency levels. Evaluation must be controlled
- **Evaluating once and forgetting** — model performance changes over time (provider updates, traffic patterns). Schedule re-evaluation quarterly

## Output Format

```markdown
# Model Evaluation: [use case]

## Requirements
| Requirement | Threshold |
|---|---|

## Candidates
| # | Model | Tier | Provider | Rationale |
|---|---|---|---|---|

## Evaluation Dataset
- Total examples: [N]
- Happy path: [N] | Edge cases: [N] | Adversarial: [N]
- Location: [path to eval set]

## Results

### [Model 1]
[Per-dimension results table + failure analysis]

### [Model 2]
[Per-dimension results table + failure analysis]

## Comparison
[Side-by-side table with pass/fail per requirement]

## Decision
- **Selected:** [model]
- **Rationale:** [tied to requirements]
- **Trade-offs:** [what you sacrifice]

## Fallback Plan
| Scenario | Action |
|---|---|

## Re-evaluation Schedule
- Next evaluation: [date]
- Trigger conditions: [what forces an early re-evaluation]
```
