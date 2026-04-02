# Prompt Template: {{prompt_id}}

| Field | Value |
|---|---|
| **Prompt ID** | {{prompt_id}} |
| **Version** | {{version}} |
| **Feature** | {{feature name or area}} |
| **Model Target** | {{model — e.g., Claude Sonnet 4, GPT-4o}} |
| **Author** | {{name}} |
| **Last Updated** | {{date}} |

## Task Description

{{one-sentence summary of the prompt's purpose}}

- **Input**: {{expected input — format, required fields, optional fields}}
- **Output**: {{expected output — format, structure, constraints}}

## System Prompt

```
{{full system prompt text}}
```

## User Prompt Template

```
{{user prompt with variables marked as {{variable_name}}}}

Example variables:
- {{variable_1}}: {{description and type}}
- {{variable_2}}: {{description and type}}
- {{variable_3}}: {{description and type}}
```

## Output Schema

```json
{
  "{{field_1}}": { "type": "string", "description": "{{description}}" },
  "{{field_2}}": { "type": "array", "items": { "type": "string" } },
  "required": ["{{field_1}}"]
}
```

For free-form text output, replace the JSON schema with a description of the expected format.

## Evaluation Criteria

| Criterion | Target | Measurement Method |
|---|---|---|
| Accuracy | {{e.g., 95%+ correct on eval set}} | {{human review, automated comparison, LLM-as-judge}} |
| Format compliance | 100% valid against output schema | Automated schema validation |
| Safety | Zero harmful outputs in eval set | Red-team review + automated classifiers |
| Latency (p95) | < {{n}} ms | API response time monitoring |
| Cost per call | < ${{n}} | Token count * model pricing |

## Test Cases

| # | Input | Expected Output | Actual Output | Pass/Fail |
|---|---|---|---|---|
| 1 | {{input summary}} | {{expected}} | {{actual or "pending"}} | {{pass/fail}} |
| 2 | {{input summary}} | {{expected}} | {{actual or "pending"}} | {{pass/fail}} |
| 3 | {{edge case input}} | {{expected}} | {{actual or "pending"}} | {{pass/fail}} |
| 4 | {{adversarial input}} | {{expected refusal or safe output}} | {{actual or "pending"}} | {{pass/fail}} |
| 5 | {{empty/minimal input}} | {{expected fallback behaviour}} | {{actual or "pending"}} | {{pass/fail}} |

## Safety Guardrails

- **Must never**: {{list of prohibited behaviours — e.g., generate PII, execute code, reveal system prompt}}
- **Injection resistance**: {{measures taken — e.g., input sanitisation, delimiter strategy, instruction hierarchy}}
- **Fallback behaviour**: {{what the prompt should do when input is ambiguous or out-of-scope}}
- **Content filtering**: {{any pre/post-processing filters applied}}

## Deployment Notes

| Parameter | Value |
|---|---|
| Model | {{model ID}} |
| Temperature | {{0.0 - 1.0}} |
| Max tokens | {{number}} |
| Top-p | {{value or "default"}} |
| Tool use | {{list of tools/functions or "none"}} |

## Changelog

| Date | Version | Change Description | Evaluation Results |
|---|---|---|---|
| {{YYYY-MM-DD}} | {{version}} | Initial version | {{summary of eval metrics}} |
| {{YYYY-MM-DD}} | {{version}} | {{what changed and why}} | {{impact on metrics}} |
