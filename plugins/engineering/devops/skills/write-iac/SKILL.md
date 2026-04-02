---
name: write-iac
description: "Write infrastructure-as-code using Terraform or Pulumi. Produces a module or stack with resource definitions, variables, outputs, and documentation. Use when provisioning cloud infrastructure, defining environments, or creating reusable infrastructure modules."
argument-hint: "[infrastructure resource or module to create]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write infrastructure-as-code for $ARGUMENTS.

Follow every step below. The output must be a complete, deployable module — not a skeleton or snippet.

---

## Step 1: Reconnaissance

Before writing any IaC:

1. **Detect the IaC tool** — look for `*.tf` files (Terraform), `Pulumi.yaml` / `Pulumi.*.yaml` (Pulumi), `main.tf`, `provider.tf`, `versions.tf`, or `__main__.py` / `index.ts` (Pulumi programs)
2. **Check existing modules** — scan for reusable modules in `modules/`, `infra/`, or a shared infrastructure repo. Reuse before creating
3. **Identify the provider** — AWS, Azure, GCP, or multi-cloud. Check `provider` blocks or `Pulumi.yaml` runtime
4. **Identify the backend** — where is state stored? Look for `backend` blocks or `Pulumi.*.yaml` backend config
5. **Check naming conventions** — how are existing resources named? Follow the same pattern (e.g., `{env}-{service}-{resource}`)
6. **Identify existing tagging strategy** — look for common tags applied across resources

If no IaC tool is detected, default to Terraform with HCL. Ask the user to confirm before proceeding with Pulumi.

---

## Step 2: Design the Resource Graph

Before writing code, plan the resources:

1. **List every resource** the module will create (e.g., VPC, subnets, security groups, IAM roles)
2. **Map dependencies** — which resources reference others? Draw the dependency chain
3. **Identify data sources** — what existing resources does this module need to look up (e.g., existing VPC, DNS zone, KMS key)?
4. **Name resources consistently** — follow the pattern: `{environment}-{service}-{resource-type}`
5. **Plan for outputs** — what will consuming modules or stacks need from this module?

Document the resource graph as a comment block at the top of the main file:

```hcl
# Resource Graph:
# VPC → Subnets (public, private) → Route Tables → NAT Gateway
#                                  → Security Groups
#                                  → Load Balancer → Target Group
```

---

## Step 3: Write the Module

### Terraform Structure

```
modules/{module-name}/
├── main.tf          # Resource definitions
├── variables.tf     # Input variables
├── outputs.tf       # Output values
├── versions.tf      # Provider and Terraform version constraints
├── data.tf          # Data sources (if needed)
├── locals.tf        # Local values (if needed)
└── README.md        # Usage documentation
```

### Pulumi Structure

```
infra/{stack-name}/
├── Pulumi.yaml         # Project metadata
├── Pulumi.dev.yaml     # Dev stack config
├── Pulumi.prod.yaml    # Prod stack config
├── index.ts / __main__.py  # Program entry
└── README.md           # Usage documentation
```

### Variable Definitions (Terraform)

Every variable must have a description, type, and validation rule where applicable:

```hcl
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "instance_type" {
  description = "EC2 instance type for the application server"
  type        = string
  default     = "t3.medium"

  validation {
    condition     = can(regex("^t3\\.", var.instance_type))
    error_message = "Only t3 instance types are permitted for this module."
  }
}
```

### Variable Definitions (Pulumi)

Use `pulumi.Config` with typed accessors and validation:

```typescript
const config = new pulumi.Config();
const environment = config.require("environment"); // Fails if not set
const instanceType = config.get("instanceType") || "t3.medium";
```

---

## Step 4: Add Provider Constraints and Backend Config

### Terraform

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "modules/{module-name}/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}
```

### Pulumi

```yaml
# Pulumi.yaml
name: module-name
runtime: nodejs  # or python
description: What this stack provisions
```

**Rules:**
- Pin provider versions with pessimistic constraint (`~>`) — allows patch updates, blocks breaking changes
- State backend must be remote with encryption and locking
- Never use local state (`terraform.tfstate` on disk) outside local development
- DynamoDB (AWS) or equivalent lock table is mandatory for team use

---

## Step 5: Write Documentation

Every module includes a `README.md` with:

1. **Purpose** — one paragraph describing what the module provisions
2. **Usage example** — a complete, copy-pasteable example
3. **Input variables table** — name, type, default, description
4. **Output values table** — name, description
5. **Prerequisites** — what must exist before using this module

### Template

```markdown
# Module: {name}

{One paragraph: what this module provisions and why.}

## Usage

\```hcl
module "example" {
  source = "./modules/{name}"

  environment   = "dev"
  instance_type = "t3.medium"
  vpc_id        = module.network.vpc_id
}
\```

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| environment | string | — | Deployment environment |
| instance_type | string | "t3.medium" | EC2 instance type |

## Outputs

| Name | Description |
|------|-------------|
| instance_id | ID of the created EC2 instance |
| public_ip | Public IP address (if assigned) |

## Prerequisites

- VPC must exist (use the `network` module)
- IAM role for the instance profile must exist
```

---

## Step 6: Verify

Run validation checks before delivering:

### Terraform

```bash
terraform fmt -check -recursive    # Format check
terraform validate                 # Syntax and reference validation
terraform plan                     # Dry run (if credentials available)
```

### Pulumi

```bash
pulumi preview    # Dry run
```

If validation commands are not available (no credentials, no Terraform installed), note the required verification steps for the user to run.

---

## Rules

- **One resource type per module** — a module that creates a VPC and an RDS instance is doing two things. Split into `network` and `database` modules. Compose them at the stack level.
- **Variables must have descriptions, types, and validation rules** — undocumented variables are tech debt. Validation catches misconfiguration before `apply`.
- **Never hardcode secrets** — use variables, SSM Parameter Store, Secrets Manager, or Vault. No API keys, passwords, or tokens in `.tf` or Pulumi code.
- **Tag all resources consistently** — every resource must have at minimum: `environment`, `team`, `service`, and `managed-by` tags. Use a `locals` block or default tags on the provider.
- **State must be remote** — local state files are not shared, not locked, and not backed up. Use S3+DynamoDB, GCS, Azure Blob, or Pulumi Cloud.
- **Use `for_each` over `count`** — `count` creates index-based resources that break when items are removed from the middle of a list. `for_each` uses stable keys.
- **Never use `terraform destroy` without confirmation** — document the destroy procedure in the README.
- **Pin provider versions** — unpinned providers will break silently on major releases.
- Reference [HashiCorp Terraform Style Conventions](https://developer.hashicorp.com/terraform/language/style) for Terraform or [Pulumi Best Practices](https://www.pulumi.com/docs/iac/concepts/best-practices/) for Pulumi.

---

## Output Format

Deliver:

1. **Module files** — `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf` (Terraform) or `index.ts`/`__main__.py` + `Pulumi.yaml` (Pulumi)
2. **README.md** — usage example, input/output tables, prerequisites
3. **Resource graph** — comment block showing resource dependencies
4. **Verification results** — output of `terraform validate` / `pulumi preview` (or instructions to run)

---

## Related Skills

- `/devops:write-pipeline` — the CI/CD pipeline deploys the infrastructure. Add `terraform plan` to PR checks and `terraform apply` to the deploy stage.
- `/devops:write-dockerfile` — containers run on the infrastructure this module provisions. Coordinate instance types, networking, and security groups.
