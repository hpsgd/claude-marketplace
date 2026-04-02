---
name: compliance-audit
description: Audit compliance against a regulatory framework — gap analysis, evidence collection, and remediation planning.
argument-hint: "[framework to audit against, e.g. GDPR, SOC 2, ISO 27001, Privacy Act, Essential Eight]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit compliance against $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Framework Identification

Identify the specific framework, version, and applicable controls:

| Framework | Key reference | Scope |
|---|---|---|
| [GDPR](https://gdpr.eu) | Articles 5–49 | EU personal data processing |
| [Australian Privacy Principles](https://www.oaic.gov.au/privacy/australian-privacy-principles) | 13 APPs | Australian personal information |
| [NZ Privacy Act 2020](https://www.privacy.org.nz/privacy-act-2020/) | 13 IPPs | NZ personal information |
| [SOC 2](https://www.aicpa.org/soc2) | Trust Service Criteria | Service organisation security, availability, processing integrity, confidentiality, privacy |
| [ISO 27001](https://www.iso.org/standard/27001) | Annex A controls | Information security management system |
| [Essential Eight](https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight) | 8 strategies, maturity 0–3 | Australian cyber security baseline |
| [NZISM](https://www.nzism.gcsb.govt.nz) | Security manual | NZ government information security |
| [Cyber Essentials](https://www.ncsc.gov.uk/cyberessentials/overview) | 5 controls | UK cyber security baseline |
| [HIPAA](https://www.hhs.gov/hipaa/index.html) | Security Rule, Privacy Rule | US health data |
| [PCI DSS](https://www.pcisecuritystandards.org/) | 12 requirements | Payment card data |
| [NIST CSF 2.0](https://www.nist.gov/cyberframework) | 6 functions (Govern, Identify, Protect, Detect, Respond, Recover) | US cybersecurity baseline |
| [CIS Controls v8](https://www.cisecurity.org/controls) | 18 prioritised controls | Practical security baseline |

**Determine:** Which version of the framework? Which controls are applicable given the project's data, users, and jurisdiction? Not every control applies to every system.

### Step 2: Scope Definition

1. **Systems in scope** — which applications, databases, infrastructure?
2. **Data in scope** — what data types are processed? (PII, financial, health, credentials)
3. **Processes in scope** — what workflows handle regulated data? (collection, processing, storage, deletion, sharing)
4. **Teams in scope** — who has access to regulated data or systems?

### Step 3: Control Mapping

Map each applicable framework requirement to an existing control (or lack thereof):

| Requirement ID | Requirement | Current control | Evidence | Status |
|---|---|---|---|---|
| [e.g. GDPR Art. 6] | [description] | [what exists] | [where evidence is] | MET / PARTIAL / GAP |

**Evidence types to check:**

```bash
# Access controls
grep -rn "auth\|authorize\|permission\|role" --include="*.ts" --include="*.py" --include="*.cs"

# Encryption configuration
grep -rn "encrypt\|tls\|ssl\|certificate\|kms" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.tf"

# Logging and audit trails
grep -rn "audit\|log\.\|logger\.\|track\|event" --include="*.ts" --include="*.py" --include="*.cs"

# Data retention/deletion
grep -rn "retention\|purge\|delete\|expire\|ttl" --include="*.ts" --include="*.py" --include="*.cs" --include="*.yaml"

# CI/CD security gates
find . -name "*.yml" -path "*ci*" -o -name "*.yml" -path "*pipeline*" -o -name "*.yml" -path "*workflow*"
```

### Step 4: Evidence Collection

For each control marked as MET or PARTIAL, collect verifiable evidence:

| Evidence type | What to look for | Reliability |
|---|---|---|
| **Code** | Implementation of the control in source code | High — verifiable, versioned |
| **Configuration** | Infrastructure, CI/CD, or application config | High — verifiable |
| **Documentation** | Policies, procedures, runbooks | Medium — may be outdated |
| **Logs** | Audit trails, access logs, change logs | High — if centralised and tamper-resistant |
| **Interviews** | Team member confirmation of process | Low — self-reported, no verification |

**Rules:**
- Automated evidence > manual evidence
- Current evidence > stale evidence (check dates)
- Code-level evidence > documentation claims
- If evidence requires "just ask [person]", it is not auditable evidence

### Step 5: Gap Analysis

For each requirement with status PARTIAL or GAP:

1. **What is missing?** — specific control or evidence not present
2. **Why is it missing?** — never implemented, partially implemented, implemented but not documented
3. **What is the exposure?** — what could happen if this gap is exploited or discovered during audit

### Step 6: Risk-Rank the Gaps

Not all gaps are equal. Rank by regulatory exposure:

| Severity | Criteria | Examples |
|---|---|---|
| **Critical** | Active non-compliance with mandatory requirement, data currently at risk | No encryption for PII at rest, no breach notification process, no consent mechanism |
| **High** | Missing control for a high-impact requirement, audit finding likely | Incomplete access controls, no audit trail for data access, no deletion capability |
| **Medium** | Partial compliance, control exists but has weaknesses | Encryption configured but not verified, logging exists but incomplete, policy exists but unenforced |
| **Low** | Documentation gap, minor process improvement needed | Policy needs updating, evidence needs better organisation, training records incomplete |

### Step 7: Remediation Plan

For each gap, define a remediation action:

| Gap ID | Requirement | Severity | Remediation | Owner | Target date | Verification |
|---|---|---|---|---|---|---|
| G-001 | [requirement] | [level] | [specific action] | [person] | [date] | [how to verify completion] |

**Prioritisation rules:**
- Critical gaps: immediate action, escalate to coordinator
- High gaps: this sprint/iteration
- Medium gaps: planned within 30 days
- Low gaps: planned within 90 days

## Anti-Patterns (NEVER do these)

- **Checkbox compliance** — ticking "yes" without verifiable evidence is audit theatre. Every MET status needs a specific evidence reference
- **One-time audits** — compliance is continuous. Define the re-audit schedule and triggers
- **Treating all gaps equally** — a missing encryption control and a missing policy document are not the same severity
- **Documentation without enforcement** — a policy that exists in a wiki but is not automated or audited does not exist in practice
- **Self-reported evidence only** — "we do this" without code, config, or logs to prove it is not evidence
- **Ignoring partial compliance** — PARTIAL is still a gap. Document what is missing and remediate

## Output Format

```markdown
# Compliance Audit: [framework] — [scope]

## Audit Summary
- **Framework:** [name and version]
- **Scope:** [systems, data, processes]
- **Date:** [audit date]
- **Auditor:** [who performed this audit]
- **Overall status:** [Compliant / Partially Compliant / Non-Compliant]

## Results Summary
| Status | Count | Percentage |
|---|---|---|
| MET | [n] | [%] |
| PARTIAL | [n] | [%] |
| GAP | [n] | [%] |
| N/A | [n] | [%] |

## Control Matrix
| Req ID | Requirement | Control | Evidence | Status |
|---|---|---|---|---|
| [id] | [description] | [control] | [evidence ref] | MET/PARTIAL/GAP |

## Gap Register
| Gap ID | Requirement | Severity | Description | Exposure |
|---|---|---|---|---|
| G-001 | [req] | Critical/High/Medium/Low | [what is missing] | [what could happen] |

## Remediation Plan
| Gap ID | Remediation | Owner | Target date | Verification |
|---|---|---|---|---|
| G-001 | [action] | [person] | [date] | [how to verify] |

## Re-Audit Schedule
- **Next audit:** [date]
- **Audit triggers:** [regulatory changes, system changes, incidents, 12-month maximum]
- **Evidence refresh:** [how evidence will be kept current between audits]
```

## Related Skills

- `/grc-lead:risk-assessment` — risk-rank gaps found during the compliance audit to prioritise remediation.
- `/grc-lead:ai-governance-review` — when AI/ML systems are in scope and require specialised governance checks.
