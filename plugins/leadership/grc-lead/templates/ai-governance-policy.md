# AI Governance Policy

## 1. Purpose

This policy establishes the principles, requirements, and processes for the responsible development, procurement, and use of artificial intelligence systems within {organisation}. It ensures AI use aligns with legal obligations, ethical standards, and organisational values.

## 2. Scope

This policy applies to all employees, contractors, and third parties who develop, deploy, procure, or operate AI systems on behalf of {organisation}. It covers generative AI, machine learning models, automated decision-making systems, and AI-powered features embedded in third-party products.

## 3. AI Risk Classification

Every AI use case must be classified before deployment.

| Risk Level     | Criteria                                                        | Examples                                                  |
| -------------- | --------------------------------------------------------------- | --------------------------------------------------------- |
| **Prohibited** | Unacceptable risk to rights, safety, or legal compliance        | Social scoring, real-time biometric surveillance, manipulation of vulnerable groups |
| **High**       | Significant impact on individuals or critical business decisions | Credit decisions, hiring screening, medical diagnosis, autonomous safety systems |
| **Medium**     | Moderate impact; errors are recoverable                         | Content moderation, customer segmentation, demand forecasting |
| **Low**        | Minimal impact; human review readily available                  | Internal search, code completion, meeting summaries, spell-check |

## 4. Approval Requirements

| Risk Level     | Approval Required                              | Review Cadence |
| -------------- | ---------------------------------------------- | -------------- |
| **Prohibited** | Not permitted                                  | N/A            |
| **High**       | AI Governance Board + Legal + DPO              | Quarterly      |
| **Medium**     | Department head + AI Governance representative | Semi-annually  |
| **Low**        | Line manager                                   | Annually       |

## 5. Data Governance

- **Training data** -- document the source, licensing, and representativeness of all training data. Conduct bias assessments before model training.
- **PII handling** -- apply data minimisation. Do not send personal data to external AI services without a Data Protection Impact Assessment (DPIA) and appropriate contractual safeguards.
- **Consent** -- where AI processes personal data, ensure a lawful basis exists under applicable privacy legislation. Obtain explicit consent where required.
- **Retention** -- AI-generated outputs containing personal data follow the same retention schedules as source data.

## 6. Transparency Requirements

- **Disclosure** -- users must be informed when they are interacting with an AI system or when AI materially influenced a decision affecting them.
- **Explainability** -- High-risk AI systems must produce explanations sufficient for a non-technical reviewer to understand the key factors behind a decision.
- **Documentation** -- maintain a register of all deployed AI systems including purpose, risk level, data inputs, and responsible owner.

## 7. Human Oversight

- High-risk AI decisions require a qualified human reviewer before action is taken.
- Automated decisions must include an accessible appeal mechanism.
- Operators must have the ability to override or shut down any AI system without delay.

## 8. Monitoring and Review

- Track accuracy, fairness, and drift metrics for all High and Medium risk systems.
- Conduct bias and performance audits at the cadence specified in Section 4.
- Log AI inputs and outputs for High-risk systems with retention aligned to regulatory requirements.

## 9. Incident Response for AI Failures

- Report AI-related incidents (incorrect outputs with material impact, data leakage, bias events) through the existing incident management process with the additional tag **AI-INCIDENT**.
- Conduct a root cause analysis within {n} business days.
- Notify affected individuals and regulators where legally required.
- Suspend the AI system pending investigation if the incident poses ongoing risk.

## 10. Roles and Responsibilities

| Role                        | Responsibilities                                                      |
| --------------------------- | --------------------------------------------------------------------- |
| AI Governance Board         | Policy approval, risk classification disputes, prohibited-use waivers |
| Data Protection Officer     | DPIA oversight, consent and lawful basis review                       |
| AI System Owner             | Risk classification, monitoring, incident escalation                  |
| Development / Procurement   | Compliance with this policy during build or buy                       |
| All employees               | Adherence to approved-use guidelines, incident reporting              |

## 11. Review Schedule

| Field                  | Value          |
| ---------------------- | -------------- |
| **Policy owner**       | {role / name}  |
| **Approved by**        | {board / role} |
| **Effective date**     | {date}         |
| **Last reviewed**      | {date}         |
| **Next review**        | {date}         |
| **Review frequency**   | Annual or upon material regulatory change |
