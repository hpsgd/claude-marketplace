# Eval Suite — {{suite_name}}

| Field        | Value            |
|--------------|------------------|
| Author       | {{author}}       |
| Date         | {{date}}         |
| Status       | Draft / Active / Archived |

## Target

| Dimension | Value |
|-----------|-------|
| Component | {{prompt / model / pipeline / agent}} |
| Identifier| {{e.g. prompt v2.3, gpt-4o, retrieval-qa-pipeline}} |
| Version   | {{version or commit SHA}} |

## Eval dataset

| Field   | Value |
|---------|-------|
| Path    | {{e.g. evals/datasets/suite_name.jsonl}} |
| Format  | {{JSONL / CSV / HuggingFace dataset}} |
| Count   | {{number of examples}} |
| Splits  | {{e.g. 80 % test, 20 % edge cases}} |
| Curation| {{how examples were sourced — production logs, hand-crafted, synthetic}} |

## Scoring methods

| # | Metric | Method | Threshold | Weight |
|---|--------|--------|-----------|--------|
| 1 | Accuracy | Exact match / fuzzy match | >= {{0.90}} | {{0.3}} |
| 2 | Faithfulness | LLM-as-judge ({{judge model}}) | >= {{0.85}} | {{0.25}} |
| 3 | Relevance | LLM-as-judge or embedding similarity | >= {{0.80}} | {{0.2}} |
| 4 | Latency (p95) | Timer | < {{threshold}} ms | {{0.1}} |
| 5 | Cost per eval | Token counter | < {{threshold}} USD | {{0.1}} |
| 6 | Safety | Guardrail pass rate | >= {{0.99}} | {{0.05}} |

### RAG-specific metrics (if applicable)

| Metric | Method | Threshold |
|--------|--------|-----------|
| Context precision | RAGAS | >= {{0.85}} |
| Context recall | RAGAS | >= {{0.80}} |
| Answer faithfulness | RAGAS | >= {{0.90}} |
| Answer relevancy | RAGAS | >= {{0.85}} |

## Execution instructions

```bash
# Example — adjust to your tooling
{{eval_command}} \
  --suite {{suite_name}} \
  --dataset {{dataset_path}} \
  --model {{model_id}} \
  --output {{results_path}} \
  --concurrency {{n}}
```

- **Environment**: {{e.g. CI pipeline / local / staging}}
- **Secrets**: {{e.g. API keys via env vars, no keys in repo}}
- **Estimated run time**: {{duration}}
- **Estimated cost**: {{cost per run}}

## Result recording

| Field | Location |
|-------|----------|
| Results file | {{e.g. evals/results/suite_name/YYYY-MM-DD.json}} |
| Dashboard | {{URL or "N/A"}} |
| CI artifact | {{e.g. GitHub Actions artifact}} |

### Result schema

```json
{
  "suite": "{{suite_name}}",
  "run_id": "{{uuid}}",
  "timestamp": "{{ISO 8601}}",
  "target_version": "{{version}}",
  "scores": { "metric_name": 0.00 },
  "pass": true
}
```

## Regression detection

| Field | Value |
|-------|-------|
| Baseline run | {{run_id or path to baseline results}} |
| Regression threshold | Score drop > {{e.g. 0.05}} on any weighted metric |
| Action on regression | {{block merge / alert / create ticket}} |
| Comparison method | {{absolute diff / statistical significance test}} |

## Change log

| Date | Change | Author |
|------|--------|--------|
|      |        |        |
