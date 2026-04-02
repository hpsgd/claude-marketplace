# Model Comparison — {{use_case_name}}

| Field       | Value          |
|-------------|----------------|
| Author      | {{author}}     |
| Date        | {{date}}       |
| Decision    | Pending / {{selected_model}} |

## Use case

{{Describe the task the model will perform — e.g. "Summarise support tickets into structured JSON for triage routing."}}

## Requirements

| # | Dimension | Threshold | Weight | Notes |
|---|-----------|-----------|--------|-------|
| 1 | Accuracy / quality | >= {{0.90}} | {{0.30}} | {{measured via eval suite}} |
| 2 | Latency (p95) | < {{threshold}} ms | {{0.20}} | {{end-to-end including network}} |
| 3 | Cost per 1K calls | < {{threshold}} USD | {{0.20}} | {{input + output tokens}} |
| 4 | Context window | >= {{threshold}} tokens | {{0.10}} | {{longest expected input}} |
| 5 | Safety / compliance | {{requirement}} | {{0.10}} | {{e.g. SOC 2, data residency}} |
| 6 | {{custom dimension}} | {{threshold}} | {{0.10}} | {{notes}} |

## Candidates

| # | Model | Provider | Version / Date | Context window | Pricing (input / output per 1M tokens) |
|---|-------|----------|---------------|---------------|----------------------------------------|
| 1 | {{model_a}} | {{provider}} | {{version}} | {{tokens}} | {{$X / $Y}} |
| 2 | {{model_b}} | {{provider}} | {{version}} | {{tokens}} | {{$X / $Y}} |
| 3 | {{model_c}} | {{provider}} | {{version}} | {{tokens}} | {{$X / $Y}} |
| 4 | {{model_d}} | {{provider}} | {{version}} | {{tokens}} | {{$X / $Y}} |

## Eval results

| Dimension | {{model_a}} | {{model_b}} | {{model_c}} | {{model_d}} |
|-----------|-------------|-------------|-------------|-------------|
| Accuracy / quality | {{score}} | {{score}} | {{score}} | {{score}} |
| Latency (p95) | {{ms}} | {{ms}} | {{ms}} | {{ms}} |
| Cost per 1K calls | {{$}} | {{$}} | {{$}} | {{$}} |
| Context window | {{tokens}} | {{tokens}} | {{tokens}} | {{tokens}} |
| Safety / compliance | {{pass/fail}} | {{pass/fail}} | {{pass/fail}} | {{pass/fail}} |
| {{custom}} | {{value}} | {{value}} | {{value}} | {{value}} |
| **Weighted score** | **{{score}}** | **{{score}}** | **{{score}}** | **{{score}}** |

## Cost projection

| Model | Avg tokens/call (in+out) | Calls/month | Monthly cost | Annual cost |
|-------|-------------------------|-------------|-------------|-------------|
| {{model_a}} | {{tokens}} | {{volume}} | {{$}} | {{$}} |
| {{model_b}} | {{tokens}} | {{volume}} | {{$}} | {{$}} |

## Side-by-side comparison

### Strengths and weaknesses

| Model | Strengths | Weaknesses |
|-------|-----------|------------|
| {{model_a}} | {{strengths}} | {{weaknesses}} |
| {{model_b}} | {{strengths}} | {{weaknesses}} |

### Example outputs

> Include 1-2 representative examples showing output differences on the same input.

## Recommendation

**Selected model:** {{model_name}}

**Rationale:** {{Why this model best fits the requirements — reference eval scores, cost, and operational considerations.}}

## Fallback plan

| Scenario | Fallback model | Switch criteria |
|----------|---------------|-----------------|
| Primary model degraded | {{fallback}} | {{e.g. latency > 2x SLA for 5 min}} |
| Primary model deprecated | {{fallback}} | {{provider announcement}} |
| Cost exceeds budget | {{fallback or throttle}} | {{monthly spend > $X}} |

## Re-evaluation schedule

| Trigger | Action |
|---------|--------|
| {{quarterly}} | Re-run eval suite against latest model versions |
| New model release | Ad-hoc comparison if relevant to use case |
| Accuracy regression | Immediate re-evaluation |

## Change log

| Date | Change | Author |
|------|--------|--------|
|      |        |        |
