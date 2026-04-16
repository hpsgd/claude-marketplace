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
