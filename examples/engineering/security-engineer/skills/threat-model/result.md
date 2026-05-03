# Threat Model

Scenario: Checking that the threat-model skill mandates data flow mapping before STRIDE analysis, requires risk scoring (likelihood x impact) for every threat, and produces an actionable risk register rather than a generic threat catalogue.

## Prompt

> Review the threat-model skill definition and verify it produces a system-specific threat model rather than a generic security checklist.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Verdict: structure pushes toward specificity, but two gaps create real generic-output risk.**

---

## What works

- Step 2 (Data Flow Mapping) is mandatory — you can't skip it, which forces topology-specific thinking
- The anti-pattern "generic threats without specifics — 'SQL injection is a risk' without identifying WHERE is useless" is an explicit guard
- Risk scoring is mandatory per-threat, which prevents the equal-weight-everything problem

---

## What creates generic-output risk

**Gap 1 — No system-discovery step.**
The skill has `allowed-tools: Read, Bash, Glob, Grep` but the process starts at scope definition, not at reading the actual system. If invoked as `/threat-model payment-service` with no path, a model can fabricate a "specific" model from training data without reading any code or docs. A **Step 0** should be explicit: "Use Read/Glob/Grep to discover the actual system topology, tech stack, endpoints, and data stores before defining scope."

**Gap 2 — Pre-filled examples are unmarked as illustrative.**
Three places embed concrete generic content without flagging it as "replace this":

- Step 2 Mermaid DFD: a complete topology (`WAF → LB → API → Redis → Queue → Worker → ThirdParty`) — not labelled as an example to replace
- Step 1 threat actor table: all four generic actors pre-filled with descriptions, no instruction to prune or customise
- Step 5 mitigation table: T1–T4 (`XSS token theft, SQL injection, PII in logs, IDOR /users/{id}`) read as a starter list, not as illustrative

A model under time pressure may emit these with minor substitutions and call the model "specific."

**Gap 3 — STRIDE questions are universal checklists.**
Step 3's question tables (`Can someone impersonate a user? Can tokens be stolen or forged?`) apply identically to any system. There's no instruction to first map which questions are live concerns for the specific components identified in Step 2, or to skip/justify-away categories that don't apply. This makes it easy to produce a boilerplate STRIDE grid rather than a component-specific one.

---

## Recommended fixes

1. **Add Step 0** before scope definition:
   ```
   ### Step 0: System Discovery (MANDATORY)
   Before defining scope, use Read/Glob/Grep to examine the actual system:
   - Read CLAUDE.md, README, architecture docs
   - Identify tech stack, entry points, data stores, external dependencies
   - List actual endpoints and workflows
   You cannot threat model a system you haven't read.
   ```

2. **Mark all pre-filled content as illustrative** — add `<!-- example — replace entirely -->` comments to the DFD, threat actor table, and mitigation table, and state explicitly "the DFD must reflect the actual topology discovered in Step 0, not this generic example."

3. **Anchor STRIDE to discovered components** — before the question tables, add: "For each component and flow identified in Step 2, apply only the STRIDE questions that are relevant to that component's role. Note explicitly which questions are N/A and why."

---

This is a static definition review — behavioural verification (actually running the skill on a known codebase and checking whether the output is generic) would be the next step to confirm the gaps are real.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 6.0/17.0 (35%) |
| Evaluated | 2026-05-01 |
| Target duration | 129885 ms |
| Target cost | $0.4855 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires scope definition first — system name, included components, excluded components, and a threat actor table with motivation and capability for each actor type | PASS | Output confirms Step 1 is threat actor table ('Step 1 threat actor table: all four generic actors pre-filled with descriptions') and that Step 2 is Data Flow Mapping — establishing the scope-first ordering. |
| c2 | Skill mandates data flow mapping using a Mermaid diagram with trust boundaries before any STRIDE analysis begins | PARTIAL | Output explicitly confirms 'Step 2 (Data Flow Mapping) is mandatory' and references 'Step 2 Mermaid DFD: a complete topology (WAF → LB → API → Redis → Queue → Worker → ThirdParty)'. Trust boundaries are never mentioned. |
| c3 | Skill requires a data flow inventory table annotating each flow with protocol, authentication, encryption, and data classification | FAIL | Output makes no mention of a data flow inventory table or any per-flow annotation of protocol, authentication mechanism, encryption status, or data classification. Only the Mermaid DFD is discussed. |
| c4 | Skill applies STRIDE analysis per component and data flow with specific evidence-based questions for each of the six categories | PARTIAL | Output references 'Step 3's question tables' with example questions ('Can someone impersonate a user? Can tokens be stolen or forged?') but criticises them as universal checklists. No confirmation that all six STRIDE categories are present, nor that analysis is applied per data flow. |
| c5 | Skill requires every identified threat to be scored using a likelihood x impact risk matrix — not just labelled as high/medium/low without justification | PARTIAL | Output states 'Risk scoring is mandatory per-threat, which prevents the equal-weight-everything problem.' Confirms scoring is required but never specifies a likelihood × impact matrix or grid format — could be a simple label system. |
| c6 | Skill requires mitigations table with control type (preventive/detective/corrective) and implementation status for each threat | FAIL | Output mentions 'Step 5 mitigation table: T1–T4' exists, but only comments on its generic pre-filled examples. No confirmation of control type (preventive/detective/corrective) or implementation status fields. |
| c7 | Skill requires at least one preventive control per threat — detective/corrective controls are additions, not substitutes | FAIL | Output does not mention any requirement for at least one preventive control per threat. The mitigations table is mentioned only in the context of its generic pre-filled examples. |
| c8 | Skill addresses residual risk assessment after mitigations — accepted risks must have an owner and review date | FAIL | Output contains no mention of residual risk assessment, accepted risk owners, or review dates anywhere in the review. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than running an actual threat model | PASS | Output explicitly concludes 'This is a static definition review — behavioural verification (actually running the skill on a known codebase and checking whether the output is generic) would be the next step.' Entire response reviews the skill definition rather than producing a threat model. |
| c10 | Output verifies the scope-first rule — system name, included components, excluded components, and a threat actor table with motivation and capability per actor type | PARTIAL | Output mentions Step 1 threat actor table with 'four generic actors pre-filled with descriptions', establishing scope-first ordering. However, 'system name, included components, excluded components' and explicit 'motivation and capability' fields are not verified. |
| c11 | Output confirms data flow diagrams are mandatory and rendered in Mermaid with trust boundaries marked, BEFORE any STRIDE analysis | PARTIAL | Output confirms 'Step 2 (Data Flow Mapping) is mandatory' and references 'Step 2 Mermaid DFD'. Step ordering (DFD before 'Step 3' STRIDE) is confirmed. Trust boundaries are never mentioned. |
| c12 | Output verifies the data flow inventory annotates each flow with protocol, authentication mechanism, encryption status, and data classification | FAIL | Output makes no mention of a data flow inventory or per-flow annotations. Only the Mermaid DFD topology is discussed. |
| c13 | Output confirms STRIDE analysis is applied per component AND per data flow with specific evidence-based questions for each of the six STRIDE categories (Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege) | PARTIAL | Output references STRIDE question tables in Step 3 but only quotes two example questions (Spoofing, Tampering implied). Does not confirm all six categories exist, does not confirm per-data-flow application, and criticises questions as not evidence-based. |
| c14 | Output verifies every threat is scored using a likelihood × impact risk matrix (e.g. 5×5 grid) — not just a verbal high/medium/low | PARTIAL | Output states 'Risk scoring is mandatory per-threat' under 'What works'. Does not confirm likelihood × impact matrix structure or any grid format — the scoring mechanism's specific form is not verified. |
| c15 | Output confirms the mitigations table requires control type per mitigation (preventive / detective / corrective) and implementation status (planned / in-progress / done) | FAIL | Output mentions 'Step 5 mitigation table: T1–T4' but only in the context of pre-filled generic examples. Control type categories and implementation status are never mentioned. |
| c16 | Output verifies every threat must have at least one preventive control — detective and corrective controls are additions, not substitutes | FAIL | Output contains no mention of the at-least-one-preventive-control rule anywhere. |
| c17 | Output confirms residual risk after mitigations is documented, with accepted risks requiring a named owner and a review date | FAIL | Output contains no mention of residual risk documentation, risk owners, or review dates. |
| c18 | Output identifies any genuine gaps — e.g. no rule on threat-model versioning (when does the model need to be re-run after architectural change?), no link between threats and detection / monitoring requirements | PARTIAL | Output identifies three genuine gaps: no system-discovery step (Gap 1), pre-filled examples not marked as illustrative (Gap 2), and STRIDE questions are universal checklists not anchored to discovered components (Gap 3). These are real gaps but not the exemplified ones (versioning, monitoring linkage). |

### Notes

The output performs a surface-level review that correctly identifies the skill's major structural sequence (scope → DFD → STRIDE → risk scoring → mitigations) and flags three legitimate gaps around system discovery, pre-filled generic content, and non-contextual STRIDE questions. However, it misses almost all of the detailed structural requirements: the data flow inventory with per-flow protocol/auth/encryption/classification annotations, confirmation of all six STRIDE categories, the likelihood × impact matrix specifics, control type classification in the mitigations table, the at-least-one-preventive-control rule, and residual risk documentation with owners and review dates. Trust boundaries in the DFD are also not verified. The review reads as a high-level commentary on specificity vs. genericity rather than a systematic checklist verification of each required skill component.
