# Write iac skill structure

Checking that the write-iac skill produces a complete, deployable module with resource graph, validated variables, remote state, consistent tagging, and documentation — not a skeleton or snippet.

## Prompt

> Review the write-iac skill definition and verify it enforces production-ready infrastructure-as-code standards rather than illustrative examples.

Given the prompt "write Terraform for an S3 bucket with versioning and server-side encryption", the skill would run Step 1 reconnaissance (detect `*.tf` files, check `modules/` for an existing S3 module, read naming conventions), then Step 2 (plan the resource graph as a comment block), then produce four files: `main.tf` with all resources and a `locals` block for consistent tagging, `variables.tf` with description/type/validation on every variable, `outputs.tf`, and `versions.tf` with S3 backend config, encrypt=true, and a DynamoDB lock table. A `README.md` with usage example, inputs table, outputs table, and prerequisites follows. The skill closes with `terraform validate` before delivery.

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8/8 criteria met (100%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill requires reconnaissance first — Step 1 covers all three: detect IaC tool (look for `*.tf`, `Pulumi.yaml`), check existing modules ("scan for reusable modules in `modules/`, `infra/`, or a shared infrastructure repo. Reuse before creating"), and identify naming conventions ("Check naming conventions — how are existing resources named?").

- [x] PASS: Skill requires resource graph planning before code — Step 2 "Design the Resource Graph": "Before writing code, plan the resources." Requires listing every resource, mapping dependencies, and documenting as a comment block at the top of the main file.

- [x] PASS: Skill defines complete module file structure for both tools — Step 3 shows Terraform structure (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `data.tf`, `locals.tf`, `README.md`) and Pulumi structure (`Pulumi.yaml`, `Pulumi.dev.yaml`, `Pulumi.prod.yaml`, `index.ts`/`__main__.py`, `README.md`).

- [x] PASS: Skill requires description, type, and validation on every variable, marks undocumented as tech debt — Step 3 shows worked examples with all three fields. Rules: "Variables must have descriptions, types, and validation rules — undocumented variables are tech debt."

- [x] PASS: Skill prohibits local state, requires remote with encryption and locking — Step 4 rules: "Never use local state (`terraform.tfstate` on disk) outside local development" and "DynamoDB (AWS) or equivalent lock table is mandatory for team use." The `versions.tf` example shows `encrypt = true` and `dynamodb_table`.

- [x] PASS: Skill requires consistent tagging with the four specified minimum tags — Rules section: "Tag all resources consistently — every resource must have at minimum: `environment`, `team`, `service`, and `managed-by` tags. Use a `locals` block or default tags on the provider."

- [x] PASS: Skill requires README with all three required elements — Step 5 lists five required sections. The template includes a copy-pasteable usage example, an Inputs table, an Outputs table, and a Prerequisites section.

- [x] PASS: Skill requires validation before delivery and lists specified anti-patterns — Step 6 lists `terraform validate` (and `pulumi preview`) as required before delivering. Rules include "Never hardcode secrets" and "Use `for_each` over `count`" (with rationale: count creates index-based resources that break when items are removed).

## Notes

The preamble states explicitly: "The output must be a complete, deployable module — not a skeleton or snippet." This intent is backed by the step-by-step structure. The remote state prohibition is nuanced: "outside local development" rather than an absolute ban, which is the appropriate exception. The `for_each` over `count` rule includes the reasoning (index-based resources break on removal), making it more instructive than a bare prohibition.
