# Write Iac

Scenario: Checking that the write-iac skill produces a complete, deployable module with resource graph, validated variables, remote state, consistent tagging, and documentation — not a skeleton or snippet.

## Prompt

> Review the write-iac skill definition and verify it enforces production-ready infrastructure-as-code standards rather than illustrative examples.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've located and reviewed the write-iac skill definition. Here's my assessment:

## Production-Ready Strengths ✓

The skill enforces several strong production standards:

1. **Remote State Enforcement** (lines 154-155): Explicitly prohibits local state, requires remote backend with encryption and locking
2. **Version Pinning** (lines 152): Pessimistic constraints (`~>`) to prevent breaking changes while allowing patches
3. **Resource Validation** (lines 86-101): Every variable requires type, description, and validation rules
4. **Naming Conventions** (lines 23, 37): Enforces consistent resource naming patterns
5. **Comprehensive Tagging** (line 237): Mandates environment, team, service, managed-by tags
6. **Secrets Management** (line 236): Explicitly forbids hardcoding secrets
7. **Module Separation** (line 234): One resource type per module, composition at stack level
8. **Verification Gates** (Step 6): Requires `terraform validate` / `pulumi preview`

## Critical Gaps for Production Use ⚠️

However, several production concerns are **missing**:

1. **Security Scanning** — No mention of tfsec, checkov, or Pulumi policy as code for compliance checks
2. **Drift Detection** — No guidance on detecting/reconciling infrastructure drift
3. **State File Protection** — Requires remote state but doesn't prescribe access controls, replication, or backup
4. **Cost Estimation** — No `terraform cost` validation or budgeting before apply
5. **Change Control** — No mention of required approvals or change windows
6. **Testing** — Missing terratest, unit tests, or IaC test frameworks
7. **Audit Logging** — No CloudTrail/audit trail strategy for tracking changes
8. **Disaster Recovery** — No state file backup/recovery procedures
9. **Multi-Environment Promotion** — Minimal guidance on dev→staging→prod pipelines

## Recommendation

The skill is **solid for basic module creation** but lacks guardrails for regulated/large-scale environments. It should:
- Add a security scanning requirement (Step 4.5)
- Mandate audit logging configuration
- Require cost estimation for non-dev environments
- Document state backup/disaster recovery procedures
- Reference approval gate patterns for prod deployments

Would you like me to enhance the skill with these production-grade standards?

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 6.5/17.5 (37%) |
| Evaluated | 2026-04-30 |
| Target duration | 173364 ms |
| Target cost | $0.0825 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires reconnaissance first — detecting the IaC tool in use (Terraform vs Pulumi), checking existing modules to reuse before creating, and identifying naming conventions | FAIL | The output mentions 'Naming Conventions (lines 23, 37)' as a strength, but never frames this as a reconnaissance phase. No mention of detecting Terraform vs Pulumi tool in use, or checking existing modules before creating new ones. |
| c2 | Skill requires planning the resource graph before writing code — listing every resource and mapping dependencies | FAIL | No mention of resource graph planning or dependency mapping anywhere in the output. |
| c3 | Skill defines the complete module file structure for both Terraform (main.tf, variables.tf, outputs.tf, versions.tf) and Pulumi | FAIL | No mention of module file structure, specific file names (main.tf, variables.tf, outputs.tf, versions.tf), or Pulumi equivalents anywhere in the output. |
| c4 | Skill requires every variable to have a description, type, and validation rule — and marks undocumented variables as tech debt | PARTIAL | 'Resource Validation (lines 86-101): Every variable requires type, description, and validation rules' is explicitly confirmed. However, the tech-debt flagging for undocumented variables is not mentioned. |
| c5 | Skill prohibits local state — requires remote state with encryption and locking (S3+DynamoDB or Pulumi Cloud) | PARTIAL | 'Remote State Enforcement (lines 154-155): Explicitly prohibits local state, requires remote backend with encryption and locking' confirms the prohibition and encryption+locking. However, the specific named options (S3+DynamoDB or Pulumi Cloud) are not mentioned. |
| c6 | Skill requires consistent tagging on all resources — minimum tags: environment, team, service, managed-by | PASS | 'Comprehensive Tagging (line 237): Mandates environment, team, service, managed-by tags' — all four required tags are named explicitly. |
| c7 | Skill requires a README.md with usage example, input/output tables, and prerequisites | FAIL | No mention of README.md requirements, usage examples, input/output tables, or prerequisites anywhere in the output. |
| c8 | Skill requires running terraform validate or pulumi preview before delivering and listing anti-patterns including hardcoded secrets and use of count over for_each | PARTIAL | 'Verification Gates (Step 6): Requires terraform validate / pulumi preview' and 'Secrets Management (line 236): Explicitly forbids hardcoding secrets' are confirmed. However, the count-vs-for_each anti-pattern is not mentioned. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample IaC module | PASS | The entire output is a review assessment of the skill with 'Production-Ready Strengths' and 'Critical Gaps' sections — no sample IaC module or HCL code is produced. |
| c10 | Output verifies the reconnaissance step — detect Terraform vs Pulumi, scan for existing reusable modules, and identify naming conventions before writing | FAIL | Naming conventions are mentioned (lines 23, 37) but not as a verification of a reconnaissance step. Detecting Terraform vs Pulumi as a pre-step, and scanning for existing reusable modules, are both absent. |
| c11 | Output confirms the resource-graph-before-code rule — every resource and its dependencies enumerated before any HCL/code is written | FAIL | No mention of resource graph planning, dependency mapping, or a rule requiring this before writing code. |
| c12 | Output verifies the file structure templates for both Terraform (main.tf, variables.tf, outputs.tf, versions.tf) and Pulumi | FAIL | No mention of specific file names, module structure templates, or Pulumi equivalents anywhere in the output. |
| c13 | Output confirms every variable requires description, type, and validation — and that undocumented variables are flagged as tech debt | PARTIAL | 'Resource Validation (lines 86-101): Every variable requires type, description, and validation rules' confirms the first part. The tech-debt flagging for undocumented variables is not confirmed. |
| c14 | Output verifies the prohibition on local state and the requirement for remote state with encryption + locking (S3+DynamoDB or Pulumi Cloud), naming both options | PARTIAL | Prohibition on local state and encryption+locking requirement are confirmed. However, neither 'S3+DynamoDB' nor 'Pulumi Cloud' are named as the specific required implementations. |
| c15 | Output confirms tagging requirements — minimum tags environment, team, service, managed-by — applied to every taggable resource | PASS | 'Comprehensive Tagging (line 237): Mandates environment, team, service, managed-by tags' — all four tags named. 'Applied to every taggable resource' is implied by 'all resources' phrasing. |
| c16 | Output verifies README.md requirements: usage example, input table, output table, prerequisites | FAIL | README.md is not mentioned anywhere in the output — neither as confirmed present nor as an identified gap. |
| c17 | Output confirms the pre-delivery validation step (terraform validate / pulumi preview) and lists anti-patterns including hardcoded secrets and `count` instead of `for_each` | PARTIAL | 'Verification Gates (Step 6): Requires terraform validate / pulumi preview' and hardcoded secrets ('Secrets Management (line 236)') are confirmed. The `count` instead of `for_each` anti-pattern is never mentioned. |
| c18 | Output identifies any genuine gaps — e.g. no policy on provider version pinning beyond versions.tf, no drift-detection guidance, no rule on workspace/stack naming | PARTIAL | The output identifies several gaps including 'Drift Detection — No guidance on detecting/reconciling infrastructure drift', matching one of the criterion's examples. Also lists security scanning, state backup, cost estimation, testing, audit logging, DR, and multi-environment pipelines as gaps. |

### Notes

The captured output reads as a surface-level review that references specific line numbers, suggesting the reviewer did access the skill file, but it focuses almost entirely on security/compliance/operational gaps rather than verifying the core structural requirements that define a production-ready IaC skill. Key structural requirements — reconnaissance step, resource graph planning before code, module file structure templates (main.tf/variables.tf/outputs.tf/versions.tf), and README.md requirements — are completely absent from the review. Partial credit is given for variable validation, remote state, tagging, verification gates, and hardcoded secrets, all of which are mentioned but with incomplete detail (missing tech-debt flagging, specific backend options like S3+DynamoDB, and the count-vs-for_each anti-pattern). The output format (skill verification) is appropriate, but the verification is too shallow and omits roughly half the structural criteria the skill should enforce.
