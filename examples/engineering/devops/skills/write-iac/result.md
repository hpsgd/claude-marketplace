# Write Iac

Scenario: Checking that the write-iac skill produces a complete, deployable module with resource graph, validated variables, remote state, consistent tagging, and documentation — not a skeleton or snippet.

## Prompt

> Review the write-iac skill definition and verify it enforces production-ready infrastructure-as-code standards rather than illustrative examples.
> 
> Read the skill at `/Users/martin/Projects/turtlestack/plugins/engineering/devops/skills/write-iac/SKILL.md` and verify each item by name. Quote skill text where present:
> 
> - **Reconnaissance step** — detect IaC tool in use (Terraform vs Pulumi), scan for existing reusable modules before creating, identify naming conventions.
> - **Resource graph planning before code** — every resource enumerated, dependencies mapped before any HCL/code is written.
> - **Module file structure** for **Terraform** (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`) AND **Pulumi** equivalents.
> - **Variable contract**: every variable has `description`, `type`, AND `validation` rule. Undocumented variables flagged as tech debt.
> - **Remote state mandated** (local state PROHIBITED) with **encryption + locking**. Specific backends named: **S3+DynamoDB** (Terraform) OR **Pulumi Cloud**.
> - **README.md requirement**: usage example, input table, output table, prerequisites.
> - **Pre-delivery validation gate**: `terraform validate` / `pulumi preview` before delivering.
> - **Anti-patterns named**: hardcoded secrets, **`count` instead of `for_each`** (count is positional and breaks on reorder; for_each is keyed), `:latest` images, IAM `*` policies.
> - **Identified gaps**: any of — provider version pinning beyond versions.tf, drift-detection guidance, workspace/stack naming policy.
> 
> Confirm or flag each by name.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll verify each production-ready standard against the skill definition.

## Verification Results

### ✅ **Reconnaissance Step** (Present)
Lines 15-26 cover all three elements:
- **Tool detection**: "look for `*.tf` files (Terraform), `Pulumi.yaml` / `Pulumi.*.yaml` (Pulumi)"
- **Module scanning**: "scan for reusable modules in `modules/`, `infra/`, or a shared infrastructure repo. Reuse before creating"
- **Naming conventions**: "Check naming conventions — how are existing resources named? Follow the same pattern (e.g., `{env}-{service}-{resource}`)"

### ✅ **Resource Graph Planning** (Present)
Lines 30-47 mandate planning before code:
- "List every resource... Map dependencies... Identify data sources... Name resources consistently... Plan for outputs"
- Explicitly documents the resource graph as comment block: "Document the resource graph as a comment block at the top of the main file"

### ✅ **Module File Structure** (Present)
Lines 51-75 specify both:
- **Terraform** (lines 54-64): main.tf, variables.tf, outputs.tf, versions.tf, data.tf, locals.tf, README.md
- **Pulumi** (lines 68-74): Pulumi.yaml, Pulumi.*.yaml, index.ts/__main__.py, README.md

### ✅ **Variable Contract** (Present)
Lines 77-112 enforce all three:
- **Terraform** (lines 81-102): "Every variable must have a description, type, and validation rule where applicable"
- **Pulumi** (lines 104-112): `pulumi.Config` with typed accessors
- **Tech debt flagging**: Line 235 states "undocumented variables are tech debt"

### ⚠️ **Remote State + Encryption + Locking** (Partial)
Lines 116-155 enforce remote state strongly:
- **Mandated**: Line 154 "State backend must be remote with encryption and locking"
- **Prohibited**: Line 154 "Never use local state (`terraform.tfstate` on disk) outside local development"
- **S3+DynamoDB explicit**: Lines 132-138 show `backend "s3"` with `encrypt = true` and `dynamodb_table = "terraform-lock"`
- **Pulumi Cloud NOT NAMED**: The Pulumi section (lines 142-149) shows `Pulumi.yaml` structure but **does not explicitly require or name Pulumi Cloud as the backend**. It says "state backend must be remote" in rules, but doesn't specify where for Pulumi. **Gap: Pulumi backend requirement is vague.**

### ✅ **README.md Requirement** (Present)
Lines 159-206 mandate all four elements:
- Purpose (line 174): "one paragraph describing what the module provisions"
- Usage example (lines 176-185): "complete, copy-pasteable example"
- Input variables table (lines 187-193): name, type, default, description
- Output values table (lines 195-199): name, description
- Prerequisites (lines 201-204): "what must exist before using this module"

### ✅ **Pre-Delivery Validation Gate** (Present)
Lines 210-228 require:
- **Terraform**: `terraform fmt -check`, `terraform validate`, `terraform plan`
- **Pulumi**: `pulumi preview`

### ⚠️ **Anti-Patterns Named** (Partial — 2 of 4)
Lines 232-242 name:
- ✅ Hardcoded secrets (line 236)
- ✅ `count` vs `for_each` (line 239): Correctly explains "count creates index-based resources that break when items are removed from the middle of a list. `for_each` uses stable keys."

**Missing anti-patterns:**
- ❌ `:latest` container/AMI images — NOT MENTIONED
- ❌ IAM `*` (wildcard) policies — NOT MENTIONED

### ⚠️ **Identified Gaps** (Partial — 1 of 3)
The skill acknowledges some gaps implicitly but does **not explicitly list what is NOT covered**:
- ✅ Provider version pinning (line 241): "Pin provider versions"
- ❌ Drift detection guidance — no mention of `terraform refresh`, state drift detection, or continuous compliance scanning
- ❌ Workspace/stack naming policy — no guidance on multi-environment (dev/staging/prod) workspace/stack organization beyond Pulumi.*.yaml files

---

## Summary

| Item | Status | Confidence |
|---|---|---|
| Reconnaissance | ✅ Complete | High |
| Resource graph planning | ✅ Complete | High |
| Module structure (Terraform + Pulumi) | ✅ Complete | High |
| Variable contract | ✅ Complete | High |
| Remote state + encryption + locking | ⚠️ **Pulumi backend vague** | Medium |
| README.md tables | ✅ Complete | High |
| Pre-delivery validation | ✅ Complete | High |
| Anti-patterns named | ⚠️ **2/4 (missing `:latest` and IAM `*`)** | Medium |
| Identified gaps | ⚠️ **Partial (no drift detection, no stack naming policy)** | Low |

**Actionable gaps to close:**
1. Line 142-149: Explicitly require `Pulumi Cloud` as default backend for Pulumi
2. Line 236: Add anti-pattern: "Never use `:latest` tags for container or AMI images — use explicit semantic versions"
3. Line 236: Add anti-pattern: "Never use `*` in IAM policies — specify exact ARNs or actions"
4. Add new section: "Drift Detection" — cover `terraform refresh`, state locking during updates, and optional continuous compliance scanning
5. Add new section: "Stack/Workspace Naming" — document multi-environment organization patterns

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.5 (83%) |
| Evaluated | 2026-05-03 |
| Target duration | 29415 ms |
| Target cost | $0.0605 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires reconnaissance first — detecting the IaC tool in use (Terraform vs Pulumi), checking existing modules to reuse before creating, and identifying naming conventions | PASS | Output confirms all three elements citing lines 15-26: tool detection via '*.tf / Pulumi.yaml', module scanning in 'modules/, infra/', and naming convention check with example pattern '{env}-{service}-{resource}' |
| c2 | Skill requires planning the resource graph before writing code — listing every resource and mapping dependencies | PASS | Output confirms lines 30-47 mandate 'List every resource... Map dependencies...' and document the graph as a comment block at the top of the main file before any code is written |
| c3 | Skill defines the complete module file structure for both Terraform (main.tf, variables.tf, outputs.tf, versions.tf) and Pulumi | PASS | Output confirms lines 51-75 specify Terraform (main.tf, variables.tf, outputs.tf, versions.tf, data.tf, locals.tf, README.md) and Pulumi (Pulumi.yaml, Pulumi.*.yaml, index.ts/__main__.py, README.md) |
| c4 | Skill requires every variable to have a description, type, and validation rule — and marks undocumented variables as tech debt | PASS | Output confirms lines 77-112: 'Every variable must have a description, type, and validation rule where applicable' for Terraform, typed accessors for Pulumi, and line 235 'undocumented variables are tech debt' |
| c5 | Skill prohibits local state — requires remote state with encryption and locking (S3+DynamoDB or Pulumi Cloud) | PARTIAL | Output confirms S3+DynamoDB with encrypt=true and dynamodb_table for Terraform (lines 132-138), and prohibition on local state (line 154). However, output explicitly flags 'Pulumi Cloud NOT NAMED' — the Pulumi backend requirement is described as vague, so both specific backends are not confirmed present in the skill |
| c6 | Skill requires consistent tagging on all resources — minimum tags: environment, team, service, managed-by | FAIL | Tagging is entirely absent from the captured output. Neither the verification results, the summary table, nor the actionable gaps section mentions resource tagging or any required tags (environment, team, service, managed-by) |
| c7 | Skill requires a README.md with usage example, input/output tables, and prerequisites | PASS | Output confirms lines 159-206 mandate: purpose paragraph, 'complete copy-pasteable' usage example, input variables table (name/type/default/description), output values table (name/description), and prerequisites section |
| c8 | Skill requires running terraform validate or pulumi preview before delivering and listing anti-patterns including hardcoded secrets and use of count over for_each | PASS | Output confirms lines 210-228 require terraform fmt -check, terraform validate, terraform plan, and pulumi preview. Lines 232-242 name hardcoded secrets and count vs for_each with explanation: 'count creates index-based resources that break when items are removed' |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample IaC module | PASS | The entire output is a verification report with ✅/⚠️ verdicts per requirement, line number citations, a summary table with Status/Confidence columns, and an actionable gaps list — no IaC code is produced |
| c10 | Output verifies the reconnaissance step — detect Terraform vs Pulumi, scan for existing reusable modules, and identify naming conventions before writing | PASS | Under '✅ Reconnaissance Step (Present)', output quotes specific skill text for all three sub-elements: tool detection patterns, module scan directories, and naming convention check with example |
| c11 | Output confirms the resource-graph-before-code rule — every resource and its dependencies enumerated before any HCL/code is written | PASS | Under '✅ Resource Graph Planning (Present)', output cites lines 30-47 and quotes 'List every resource... Map dependencies...' plus the comment-block documentation requirement before any code |
| c12 | Output verifies the file structure templates for both Terraform (main.tf, variables.tf, outputs.tf, versions.tf) and Pulumi | PASS | Under '✅ Module File Structure (Present)', output lists all Terraform files by name including main.tf, variables.tf, outputs.tf, versions.tf, and Pulumi equivalents Pulumi.yaml, index.ts/__main__.py |
| c13 | Output confirms every variable requires description, type, and validation — and that undocumented variables are flagged as tech debt | PASS | Under '✅ Variable Contract (Present)', output confirms all three elements for Terraform (lines 81-102), typed accessors for Pulumi (lines 104-112), and explicitly quotes line 235 'undocumented variables are tech debt' |
| c14 | Output verifies the prohibition on local state and the requirement for remote state with encryption + locking (S3+DynamoDB or Pulumi Cloud), naming both options | PARTIAL | Output names S3+DynamoDB with encrypt=true and dynamodb_table and confirms local state prohibition. However, output explicitly states 'Pulumi Cloud NOT NAMED' — the criterion requires naming both options and the output confirms only one, flagging the other as a gap |
| c15 | Output confirms tagging requirements — minimum tags environment, team, service, managed-by — applied to every taggable resource | FAIL | Tagging requirements are not mentioned anywhere in the captured output — not verified, not flagged as absent, not listed as a gap. The topic does not appear in the verification results, summary table, or actionable gaps |
| c16 | Output verifies README.md requirements: usage example, input table, output table, prerequisites | PASS | Under '✅ README.md Requirement (Present)', output confirms all four: 'complete copy-pasteable example', input variables table with name/type/default/description columns, output values table, and prerequisites section listing what must exist before use |
| c17 | Output confirms the pre-delivery validation step (terraform validate / pulumi preview) and lists anti-patterns including hardcoded secrets and `count` instead of `for_each` | PASS | Under '✅ Pre-Delivery Validation Gate (Present)', output confirms terraform fmt -check, validate, plan and pulumi preview. Under '⚠️ Anti-Patterns Named', output confirms hardcoded secrets and count/for_each with the specific rationale about index-based vs keyed resources |
| c18 | Output identifies any genuine gaps — e.g. no policy on provider version pinning beyond versions.tf, no drift-detection guidance, no rule on workspace/stack naming | PARTIAL | Output identifies drift detection and workspace/stack naming as gaps in the actionable gaps section. It also identifies missing `:latest` and IAM `*` anti-patterns, and vague Pulumi backend. However, provider version pinning is noted as present (line 241), so the test criterion's first example gap is not confirmed missing |

### Notes

The output is a thorough, well-structured verification report that correctly identifies most production-ready standards. The two significant failures are both related to tagging (c6 and c15) — the output makes no mention of resource tagging requirements whatsoever, which is a notable blind spot given the test explicitly asked about minimum tags (environment, team, service, managed-by). The Pulumi Cloud backend gap is correctly identified and scored as partial for both the skill-content criteria (c5) and the verification criteria (c14). The output correctly flags drift detection and workspace/stack naming as gaps, meeting the partial ceiling on c18. Anti-patterns coverage is noted as incomplete (missing :latest and IAM wildcards) and scored accordingly in c8 vs c17 — c8 asks whether the skill lists these anti-patterns and the output confirms the two named ones while noting the missing ones, which is sufficient for PASS on the validation/delivery gate criterion.
