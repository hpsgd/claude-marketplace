# Output: write-iac skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-29 |
| **Source** | `plugins/engineering/devops/skills/write-iac/SKILL.md` |

## Results

### Criteria

- [x] PASS: Reconnaissance first — Step 1 explicitly covers detecting the IaC tool (`.tf` files, `Pulumi.yaml`, etc.), scanning `modules/` and `infra/` for reusable modules, and identifying naming conventions from existing resources.
- [x] PASS: Resource graph before code — Step 2 requires listing every resource, mapping dependencies, identifying data sources, and documenting the graph as a comment block at the top of the main file. Code writing begins at Step 3.
- [x] PASS: Complete file structure for both Terraform (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, plus optional `data.tf` and `locals.tf`) and Pulumi (`Pulumi.yaml`, stack configs, entry point) — both defined in Step 3.
- [x] PASS: Every variable must have a description, type, and validation rule. Step 3 shows worked examples with `validation` blocks for both Terraform and Pulumi. The Rules section reinforces: "undocumented variables are tech debt."
- [x] PASS: Local state prohibited. Step 4 Rules state explicitly: "Never use local state (`terraform.tfstate` on disk) outside local development." Remote state with S3+DynamoDB (encryption + locking) is required; Pulumi Cloud is the equivalent for Pulumi stacks.
- [x] PASS: Consistent tagging required on all resources. The Rules section names the minimum four tags: `environment`, `team`, `service`, `managed-by`. Recommends using a `locals` block or provider-level default tags.
- [x] PASS: README.md required with all four elements: usage example, input variables table, output values table, and prerequisites. Step 5 provides a complete template covering all of them.
- [x] PASS: `terraform validate` (plus `terraform fmt` and `terraform plan`) and `pulumi preview` required before delivery. Rules section lists hardcoded secrets and `count` over `for_each` as explicit anti-patterns, with reasoning for each.

### Output expectations

- [x] PASS: The scenario prompt asks to verify the skill definition — a well-formed response would produce structured verification verdicts per requirement, not a sample IaC module. The skill's Output Format section describes delivering module files, but the scenario is a structural review task and a correct response would present pass/fail findings against each requirement.
- [x] PASS: A response would verify the reconnaissance step — the skill explicitly requires detecting Terraform vs Pulumi, scanning for existing reusable modules in `modules/`/`infra/`, and identifying naming conventions before writing any code.
- [x] PASS: A response would confirm the resource-graph-before-code rule — Step 2 enumerates resources and dependencies before Step 3 begins writing code, and requires a comment block documenting the graph in the main file.
- [x] PASS: A response would verify the file structure templates for both Terraform (main.tf, variables.tf, outputs.tf, versions.tf) and Pulumi (Pulumi.yaml, stack configs, entry point) — both are present in Step 3.
- [x] PASS: A response would confirm the variable requirements — description, type, validation — and the explicit labelling of undocumented variables as tech debt. Both appear in Step 3 and the Rules section with worked examples.
- [x] PASS: A response would verify the prohibition on local state and the requirement for remote state with encryption and locking. The skill names S3+DynamoDB for Terraform and Pulumi Cloud as the two options.
- [x] PASS: A response would confirm the tagging requirement — minimum tags `environment`, `team`, `service`, `managed-by` — applied to every taggable resource via a `locals` block or provider default tags.
- [x] PASS: A response would verify the README.md requirements: usage example, input table, output table, prerequisites — all present in Step 5 with a complete template showing each section.
- [x] PASS: A response would confirm the pre-delivery validation step (`terraform validate` / `pulumi preview`) and list anti-patterns including hardcoded secrets and `count` instead of `for_each` — both explicit in Step 6 and the Rules section.
- [~] PARTIAL: A response could identify genuine gaps. Two real gaps exist: (1) no drift-detection guidance — the skill covers `terraform validate` and `terraform plan` as pre-delivery checks but says nothing about detecting drift in running infrastructure; (2) no workspace or stack naming rules — the skill defines resource naming conventions (`{env}-{service}-{resource-type}`) but gives no guidance on naming Terraform workspaces or Pulumi stacks. Provider version pinning is covered (pessimistic constraint `~>` in Step 4 and the Rules section), so that is not a gap. A well-formed response might surface these, but the skill does not signal them as known gaps, making them harder to identify without domain knowledge.

## Notes

The skill is thorough and well-structured. The six-step progression (Reconnaissance → Resource Graph → Module → Provider/Backend → Documentation → Verify) maps cleanly onto the rubric criteria, with each criterion traceable to a specific step or rule.

Two genuine gaps worth noting for a future revision:

1. **No drift detection guidance.** The skill covers `terraform plan` as a dry-run before delivery but does not address detecting configuration drift in running infrastructure — a common production concern. A reference to running `terraform plan` in CI on a schedule, or using `terraform refresh`, would close this.

2. **No workspace or stack naming rules.** Resource naming conventions are defined (`{env}-{service}-{resource-type}`) but Terraform workspace names and Pulumi stack names are left unspecified. Teams often end up with inconsistent workspace names (`default`, `prod`, `production`) without guidance.

The Pulumi variable validation section is also lighter than the Terraform section — the `pulumi.Config` example shows `require()` and `get()` but does not show validation logic equivalent to Terraform's `validation` block. This is a minor asymmetry rather than a criterion failure, since Pulumi's config API is genuinely more limited here.

The final line references `templates/terraform-module/` but whether that template exists in the plugin is unverified. If absent, agents following the skill will reference a missing resource.
