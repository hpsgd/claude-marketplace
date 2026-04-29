# Test: write-iac skill structure

Scenario: Checking that the write-iac skill produces a complete, deployable module with resource graph, validated variables, remote state, consistent tagging, and documentation — not a skeleton or snippet.

## Prompt

Review the write-iac skill definition and verify it enforces production-ready infrastructure-as-code standards rather than illustrative examples.

## Criteria

- [ ] PASS: Skill requires reconnaissance first — detecting the IaC tool in use (Terraform vs Pulumi), checking existing modules to reuse before creating, and identifying naming conventions
- [ ] PASS: Skill requires planning the resource graph before writing code — listing every resource and mapping dependencies
- [ ] PASS: Skill defines the complete module file structure for both Terraform (main.tf, variables.tf, outputs.tf, versions.tf) and Pulumi
- [ ] PASS: Skill requires every variable to have a description, type, and validation rule — and marks undocumented variables as tech debt
- [ ] PASS: Skill prohibits local state — requires remote state with encryption and locking (S3+DynamoDB or Pulumi Cloud)
- [ ] PASS: Skill requires consistent tagging on all resources — minimum tags: environment, team, service, managed-by
- [ ] PASS: Skill requires a README.md with usage example, input/output tables, and prerequisites
- [ ] PASS: Skill requires running terraform validate or pulumi preview before delivering and listing anti-patterns including hardcoded secrets and use of count over for_each

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample IaC module
- [ ] PASS: Output verifies the reconnaissance step — detect Terraform vs Pulumi, scan for existing reusable modules, and identify naming conventions before writing
- [ ] PASS: Output confirms the resource-graph-before-code rule — every resource and its dependencies enumerated before any HCL/code is written
- [ ] PASS: Output verifies the file structure templates for both Terraform (main.tf, variables.tf, outputs.tf, versions.tf) and Pulumi
- [ ] PASS: Output confirms every variable requires description, type, and validation — and that undocumented variables are flagged as tech debt
- [ ] PASS: Output verifies the prohibition on local state and the requirement for remote state with encryption + locking (S3+DynamoDB or Pulumi Cloud), naming both options
- [ ] PASS: Output confirms tagging requirements — minimum tags environment, team, service, managed-by — applied to every taggable resource
- [ ] PASS: Output verifies README.md requirements: usage example, input table, output table, prerequisites
- [ ] PASS: Output confirms the pre-delivery validation step (terraform validate / pulumi preview) and lists anti-patterns including hardcoded secrets and `count` instead of `for_each`
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no policy on provider version pinning beyond versions.tf, no drift-detection guidance, no rule on workspace/stack naming
