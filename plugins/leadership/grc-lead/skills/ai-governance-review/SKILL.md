---
name: ai-governance-review
description: Review AI/ML features for governance compliance — risk classification, bias assessment, transparency, and guardrail verification.
argument-hint: "[AI feature, model, or use case to review]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Review AI governance for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: AI Use Case Classification (MANDATORY)

Classify the use case by risk level. Classification determines which controls are required.

| Risk level | Criteria | Examples |
|---|---|---|
| **Low** | Human reviews output, no decisions about individuals, limited blast radius | Content generation, code completion, summarisation |
| **Medium** | Customer-facing responses, human approves decisions, moderate blast radius | Chatbot responses, data analysis, recommendations |
| **High** | Decisions affecting individuals, human makes final decision, wide blast radius | Financial decisions, access control, hiring/screening |
| **Prohibited** | Autonomous decisions affecting rights, safety, or wellbeing without human oversight | Fully autonomous hiring, unsupervised medical diagnosis |

**Frameworks:** Use the [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence/risk-management-framework) and the [EU AI Act](https://artificialintelligenceact.eu/) as reference frameworks for AI risk classification and governance requirements.

**Rules:**
- When uncertain, classify one level higher. Downgrading is safer than upgrading after deployment
- Classification must be documented with reasoning
- Prohibited use cases are blocked — escalate to coordinator if requested

### Step 2: Risk Identification

Evaluate each AI-specific risk category for this use case:

| Risk | Questions to answer | Evidence to check |
|---|---|---|
| **Bias** | Does the model produce different outcomes for different demographic groups? Is the training/context data representative? When input data includes demographic-adjacent fields (age, location, name, gender) and the use case affects individuals (hiring, lending, access control), rate bias risk as High minimum. | Evaluation results across segments, training data composition, demographic-adjacent field inventory |
| **Hallucination** | Does the model present false information as fact? Is output grounded in retrieved context? | Factual accuracy eval, citation rate, grounding mechanism |
| **Privacy** | Does PII enter prompts? Can the model leak PII from context? Is consent obtained? | Grep for PII in prompt templates, data flow analysis |
| **Transparency** | Do users know AI is involved? Can they understand how decisions are made? | User disclosure, explainability mechanism |
| **Dependency** | Single model/provider? What happens if the provider is unavailable? | Provider count, fallback mechanism, vendor risk |
| **Cost** | Per-request cost? Monthly budget? Rate limits in place? | Cost monitoring, budget alerts, rate limiting code |
| **Security** | Prompt injection resistance? Data exfiltration prevention? Input/output validation? | Input sanitisation, output filtering, sandboxing |

### Step 3: Requirements Check by Risk Level

Verify that all controls required for this risk level are in place:

| Requirement | Low | Medium | High | Evidence to check |
|---|---|---|---|---|
| Human review of output | Recommended | Required | Mandatory | Review workflow, approval gates |
| Evaluation suite | Basic | Comprehensive | Comprehensive + adversarial | Eval scripts, test cases, results |
| Bias testing | Optional | Required | Required + external audit | Bias eval results, demographic splits |
| Audit trail | Logs | Logs + I/O recording | Full provenance trail | Logging config, storage, retention |
| Fallback mechanism | Graceful error | Alternative path | Human takeover | Error handling code, fallback logic |
| Cost controls | Monthly budget | Per-request limits | Per-request + approval for high-cost | Rate limiting, budget alerts |

For each requirement: **MET** (evidence exists), **PARTIAL** (partially implemented), **GAP** (not implemented).

### Step 4: Technical Guardrail Verification

Verify guardrails exist in the codebase:

```bash
# Input validation / prompt injection protection
grep -rn "sanitize\|validate\|filter\|escape\|inject" --include="*.ts" --include="*.py" --include="*.cs"

# Output validation / schema enforcement
grep -rn "schema\|validate.*output\|parse.*response\|json.*mode\|structured.*output" --include="*.ts" --include="*.py" --include="*.cs"

# Rate limiting / cost controls
grep -rn "rate.limit\|throttle\|budget\|max.*token\|max.*request" --include="*.ts" --include="*.py" --include="*.cs"

# PII filtering
grep -rn "pii\|redact\|mask\|anonymise\|anonymize\|personal.*data" --include="*.ts" --include="*.py" --include="*.cs"

# Fallback / error handling for AI calls
grep -rn "fallback\|retry\|timeout\|circuit.break\|catch.*error" --include="*.ts" --include="*.py" --include="*.cs"
```

| Guardrail | Status | Evidence |
|---|---|---|
| Input validation | PRESENT / ABSENT | [file:line or "not found"] |
| Output validation | PRESENT / ABSENT | [file:line] |
| Rate limiting | PRESENT / ABSENT | [file:line] |
| PII filtering | PRESENT / ABSENT | [file:line] |
| Fallback mechanism | PRESENT / ABSENT | [file:line] |
| Cost monitoring | PRESENT / ABSENT | [file:line or dashboard] |

### Step 5: Model Governance Check

Every model in production must have:

| Check | Status | Evidence |
|---|---|---|
| **Documented owner** | Has someone accountable for this model's behaviour? | Team/person named |
| **Evaluation suite** | Does an eval set exist? When was it last run? | Eval scripts, results, date |
| **Cost budget** | Is there a defined per-request and monthly cost limit? | Budget config, alerts |
| **Version control** | Are prompts versioned in the repo (not edited in dashboards)? | Prompt files in git |
| **Change process** | Do prompt/model changes run through eval before deployment? | CI pipeline, review process |

### Step 6: Data Governance for AI

| Question | Finding |
|---|---|
| What data enters AI prompts? | [list data types] |
| Does any PII enter prompts? | [yes/no — if yes, is consent obtained?] |
| Where is prompt/response data stored? | [location, retention period] |
| Are AI outputs used to make decisions about individuals? | [yes/no — if yes, what is the review process?] |
| Can individuals request deletion of their data from AI systems? | [yes/no — mechanism] |

### Step 7: Findings and Remediation

Compile all gaps into a prioritised remediation plan.

## Anti-Patterns (NEVER do these)

- **Classifying everything as low risk** — classification determines controls. Under-classifying to avoid controls creates unmanaged risk
- **No evaluation suite** — deploying AI without eval is deploying AI you cannot measure. Eval is not optional at any risk level
- **Prompts edited in production** — prompts are code. Unversioned prompt changes bypass review, testing, and audit trails
- **No fallback for model failure** — models go down, time out, and hallucinate. Every call path has a fallback
- **PII in prompts without consent** — sending personal data to AI models without user consent is a compliance violation under GDPR (EU), Privacy Act 1988 (AU), CCPA/CPRA (US-CA), and equivalent frameworks in most other jurisdictions
- **"Don't hallucinate" as a guardrail** — instructions to the model are not controls. Grounding in context, output validation, and citation requirements are controls
- **AI governance after launch** — governance is designed in, not bolted on. Review before deployment, not after the first incident

## Output Format

```markdown
# AI Governance Review: [feature/use case]

## Classification
- **Use case:** [description]
- **Risk level:** [Low / Medium / High / Prohibited]
- **Reasoning:** [why this classification]
- **Review date:** [date]
- **Reviewer:** [who performed this review]

## Deployment Decision
- **Decision:** [APPROVED / CONDITIONALLY APPROVED / BLOCKED]
- **Conditions (if conditional):** [specific gaps that must be closed before deployment]
- **Blocking gaps (if blocked):** [which findings prevent deployment and what remediation is required]

## Risk Assessment
| Risk category | Level | Controls in place | Gaps |
|---|---|---|---|
| Bias | Low/Medium/High (High minimum if demographic-adjacent + individual decisions) | [controls] | [gaps] |
| Hallucination | Low/Medium/High | [controls] | [gaps] |
| Privacy | Low/Medium/High | [controls] | [gaps] |
| Transparency | Low/Medium/High | [controls] | [gaps] |
| Dependency | Low/Medium/High | [controls] | [gaps] |
| Cost | Low/Medium/High | [controls] | [gaps] |
| Security | Low/Medium/High | [controls] | [gaps] |

## Requirements Compliance
| Requirement | Required | Status | Evidence |
|---|---|---|---|
| Human review | [level] | MET/PARTIAL/GAP | [evidence] |
| Evaluation suite | [level] | MET/PARTIAL/GAP | [evidence] |
| Bias testing | [level] | MET/PARTIAL/GAP | [evidence] |
| Audit trail | [level] | MET/PARTIAL/GAP | [evidence] |
| Fallback | [level] | MET/PARTIAL/GAP | [evidence] |
| Cost controls | [level] | MET/PARTIAL/GAP | [evidence] |

## Technical Guardrails
| Guardrail | Status | Evidence |
|---|---|---|
| [guardrail] | PRESENT/ABSENT | [file:line] |

## Model Governance
| Check | Status | Evidence |
|---|---|---|
| [check] | MET/GAP | [detail] |

## Data Governance
| Question | Finding |
|---|---|
| [question] | [answer] |

## Remediation Plan
| Gap | Severity | Remediation | Owner | Target date |
|---|---|---|---|---|
| [gap] | [level] | [action] | [person] | [date] |

## Review Schedule
- **Next review:** [date or trigger]
- **Review triggers:** [model changes, new data sources, regulatory updates, incidents]
```

## Related Skills

- `/grc-lead:risk-assessment` — for broader risk assessment when governance gaps have system-wide risk implications.
- `/grc-lead:compliance-audit` — when governance findings have regulatory compliance implications (GDPR, SOC 2, etc.).
