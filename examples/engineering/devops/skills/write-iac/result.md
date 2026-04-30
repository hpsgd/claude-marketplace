# Result: write-iac skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Source** | `plugins/engineering/devops/skills/write-iac/SKILL.md` |

## Output

Simulated response for: *Review the write-iac skill definition and verify it enforces production-ready infrastructure-as-code standards rather than illustrative examples.*

---

### Verification: write-iac skill — production-ready IaC standards

**Scope:** structural review of `plugins/engineering/devops/skills/write-iac/SKILL.md` against eight production-readiness requirements.

---

#### Requirement 1 — Reconnaissance before writing

PASS. Step 1 requires detecting the IaC tool (scans for `*.tf`, `Pulumi.yaml`, `__main__.py`, `index.ts`), scanning `modules/` and `infra/` for reusable modules before creating new ones, identifying the provider and backend from existing config, checking naming conventions from existing resources, and identifying the existing tagging strategy. Tool detection includes a fallback: default to Terraform HCL if nothing is detected, with a confirmation prompt before using Pulumi.

---

#### Requirement 2 — Resource graph before code

PASS. Step 2 runs before Step 3. It requires listing every resource the module will create, mapping dependencies, identifying data sources, planning outputs, and documenting the full graph as a comment block at the top of the main file:

```hcl
# Resource Graph:
# VPC → Subnets (public, private) → Route Tables → NAT Gateway
#                                  → Security Groups
#                                  → Load Balancer → Target Group
```

Code writing starts at Step 3, after the graph is documented.

---

#### Requirement 3 — Complete file structure for both tools

PASS. Step 3 defines both:

**Terraform:**

```
modules/{module-name}/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── data.tf          (optional)
├── locals.tf        (optional)
└── README.md
```

**Pulumi:**

```
infra/{stack-name}/
├── Pulumi.yaml
├── Pulumi.dev.yaml
├── Pulumi.prod.yaml
├── index.ts / __main__.py
└── README.md
```

All four required Terraform files are present. Pulumi project metadata, per-stack config files, and program entry point are all defined.

---

#### Requirement 4 — Variables with description, type, and validation

PASS. Step 3 shows worked examples for both tools. For Terraform:

```hcl
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}
```

The Rules section reinforces: *"Variables must have descriptions, types, and validation rules — undocumented variables are tech debt."* The Pulumi section shows `config.require()` and `config.get()` with typed accessors, though explicit validation logic is not shown (see Notes).

---

#### Requirement 5 — Remote state required; local state prohibited

PASS. Step 4 shows the full S3+DynamoDB backend config with `encrypt = true` and `dynamodb_table`. The Rules section is explicit: *"Never use local state (`terraform.tfstate` on disk) outside local development."* For Pulumi, Pulumi Cloud is the stated equivalent. Both named options are present.

---

#### Requirement 6 — Consistent tagging on all resources

PASS. The Rules section requires: *"every resource must have at minimum: `environment`, `team`, `service`, and `managed-by` tags."* All four minimum tags are named. The skill recommends applying them via a `locals` block or provider-level default tags to avoid repetition.

---

#### Requirement 7 — README.md with usage example, input table, output table, prerequisites

PASS. Step 5 provides a complete README template with all four required sections: a usage code block, an Inputs table (name, type, default, description columns), an Outputs table (name, description columns), and a Prerequisites section. The template is copy-pasteable.

---

#### Requirement 8 — Pre-delivery validation and anti-pattern list

PASS. Step 6 requires `terraform fmt -check -recursive`, `terraform validate`, and `terraform plan` before delivery for Terraform, and `pulumi preview` for Pulumi. The skill explicitly handles the case where credentials or tooling are unavailable: note the steps for the user to run manually. Anti-patterns listed in the Rules section include hardcoded secrets and `count` over `for_each` (with reasoning: index-based resources break when items are removed from the middle of a list).

---

### Gaps identified

Two genuine gaps not covered by the rubric criteria:

1. **No drift-detection guidance.** The skill covers `terraform plan` as a pre-delivery dry-run but says nothing about detecting configuration drift in running infrastructure. A note about running `terraform plan` on a schedule in CI, or using `terraform refresh`, would close this for production operations teams.

2. **No workspace or stack naming rules.** Resource naming conventions are defined (`{env}-{service}-{resource-type}`) but Terraform workspace names and Pulumi stack names are left unspecified. Teams commonly end up with inconsistent workspace names (`default`, `prod`, `production`) without a rule here.

Provider version pinning is not a gap — the skill covers it explicitly in Step 4 and the Rules section (`~>` pessimistic constraint with rationale).

---

## Results

### Criteria

- [x] PASS: Reconnaissance first — Step 1 detects the IaC tool via file patterns (`*.tf`, `Pulumi.yaml`, `__main__.py`, `index.ts`), scans `modules/` and `infra/` for reusable modules, and checks naming conventions from existing resources before any code is written.
- [x] PASS: Resource graph before code — Step 2 lists every resource, maps dependencies, identifies data sources, and requires a comment block documenting the graph at the top of the main file. Step 3 (code writing) follows.
- [x] PASS: Complete file structure for both tools — Terraform (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, plus optional `data.tf` and `locals.tf`) and Pulumi (`Pulumi.yaml`, per-stack configs, program entry point) are both defined in Step 3.
- [x] PASS: Variables must have description, type, and validation — worked examples with `validation` blocks in Step 3, reinforced by the Rules section which labels undocumented variables as tech debt.
- [x] PASS: Local state prohibited, remote state required — Step 4 shows the S3+DynamoDB backend with `encrypt = true`; Rules section explicitly forbids local state outside local development. Pulumi Cloud named as equivalent.
- [x] PASS: Consistent tagging on all resources — Rules section names the four minimum tags (`environment`, `team`, `service`, `managed-by`) and recommends applying via `locals` block or provider default tags.
- [x] PASS: README.md with all required elements — Step 5 provides a complete template covering usage example, input table, output table, and prerequisites.
- [x] PASS: Pre-delivery validation and anti-patterns — Step 6 requires `terraform validate` / `pulumi preview` before delivery. Anti-patterns include hardcoded secrets and `count` over `for_each`, both with explicit reasoning.

### Output expectations

- [x] PASS: Simulated output is structured as a verification of the skill — per-requirement verdicts rather than a sample IaC module.
- [x] PASS: Reconnaissance step verified — detect Terraform vs Pulumi, scan for existing reusable modules, identify naming conventions before writing.
- [x] PASS: Resource-graph-before-code rule confirmed — Step 2 enumerates resources and dependencies before Step 3, with a comment block documenting the graph in the main file.
- [x] PASS: File structure templates for both tools verified — Terraform (main.tf, variables.tf, outputs.tf, versions.tf) and Pulumi (Pulumi.yaml, stack configs, entry point) both present in Step 3.
- [x] PASS: Variable requirements confirmed — description, type, validation, and explicit labelling of undocumented variables as tech debt. Present in Step 3 and the Rules section with worked examples.
- [x] PASS: Remote state prohibition verified — S3+DynamoDB for Terraform and Pulumi Cloud for Pulumi named explicitly. Local state prohibited outside local development.
- [x] PASS: Tagging requirement confirmed — minimum tags `environment`, `team`, `service`, `managed-by` applied to every taggable resource via `locals` block or provider default tags.
- [x] PASS: README.md requirements verified — usage example, input table, output table, prerequisites all present in Step 5 with a complete template.
- [x] PASS: Pre-delivery validation step confirmed — `terraform validate` / `pulumi preview` required. Anti-patterns include hardcoded secrets and `count` over `for_each`.
- [~] PARTIAL: Gaps identified — two genuine gaps found: (1) no drift-detection guidance beyond pre-delivery `terraform plan`; (2) no workspace or stack naming rules despite resource naming conventions being defined. Provider version pinning is not a gap.

## Notes

The skill is well-structured. The six-step progression (Reconnaissance → Resource Graph → Module → Provider/Backend → Documentation → Verify) maps cleanly to every rubric criterion, with each criterion traceable to a specific step or rule.

Two genuine gaps worth flagging for a future revision:

1. **No drift-detection guidance.** The skill covers `terraform plan` as a pre-delivery dry-run but does not address detecting configuration drift in running infrastructure — a common production operations concern.

2. **No workspace or stack naming rules.** Resource naming conventions are defined but Terraform workspace names and Pulumi stack names are unspecified. Without a rule, teams default to inconsistent names (`default`, `prod`, `production`).

The Pulumi variable validation section is lighter than the Terraform equivalent. The `pulumi.Config` example shows `require()` and `get()` but does not show explicit validation logic. This is a genuine asymmetry — Pulumi's config API is more limited here, but the skill could at minimum show a runtime guard for allowed values.

The final line references `templates/terraform-module/` but whether that template exists in the plugin is unverified. Agents following the skill will reference a missing resource if the template directory is absent.
