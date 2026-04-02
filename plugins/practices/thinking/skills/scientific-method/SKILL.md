---
name: scientific-method
description: Apply the scientific method to any problem — define goal, hypothesise, experiment, measure, iterate. The meta-skill governing all structured thinking.
argument-hint: "[problem to investigate or goal to achieve]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Apply the scientific method to $ARGUMENTS. This is the universal cycle for turning uncertainty into knowledge.

## The Cycle

```
GOAL → OBSERVE → HYPOTHESISE → EXPERIMENT → MEASURE → ANALYSE → ITERATE
```

### 1. Define the goal

What does success look like? Without clear success criteria, you cannot judge results. Be specific:
- Bad: "Make it faster"
- Good: "Reduce p95 latency from 800ms to under 200ms on the /api/search endpoint"

### 2. Observe

What is the current state? Gather data before forming hypotheses:
- What do you actually see? (not what you expect to see)
- What measurements exist?
- What has been tried before? What happened?

### 3. Hypothesise

Generate MULTIPLE hypotheses, not just one. For each:
- What specifically do you think is happening and why?
- What would you expect to see if this hypothesis is correct?
- What would you expect to see if it's wrong?

### 4. Design experiment

For the most likely hypothesis:
- What's the smallest test that would confirm or refute it?
- What's the control? (what stays the same)
- What's the variable? (what changes)
- How will you measure the outcome?

### 5. Measure

Run the experiment. Record:
- What actually happened (not what you expected)
- Quantitative results where possible
- Unexpected observations

### 6. Analyse

Compare results to the goal:
- Did the hypothesis hold?
- How far are you from the goal?
- What did you learn that you didn't know before?

### 7. Iterate

Based on analysis:
- If goal met → document what worked and why
- If not met → update hypotheses with new evidence, return to step 3
- If stuck → challenge assumptions with first-principles thinking

## Scale of Application

- **Micro** (minutes): TDD — write test, write code, refactor
- **Meso** (hours-days): Feature — spec, implement, validate
- **Macro** (weeks-months): Product — MVP, launch, measure product-market fit

## Quick Diagnosis Mode

For debugging (the 15-minute rule):
1. What exactly is the symptom? (observe)
2. What are 3 possible causes? (hypothesise)
3. Which is most likely? Test that ONE thing (experiment)
4. Did it fix it? (measure)
5. If not, move to the next hypothesis. Don't change multiple things at once.
