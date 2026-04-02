# Terraform Module Template

## Purpose

A reusable Terraform module template with standard structure, input validation, tagging, and outputs. Replace the placeholder S3 resources with your actual infrastructure.

## Usage

```hcl
module "example" {
  source = "./modules/example"

  environment  = "production"
  project_name = "my-service"

  tags = {
    Team  = "platform"
    Owner = "alice@example.com"
  }
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `environment` | Deployment environment (dev, staging, production) | `string` | — | yes |
| `project_name` | Project name for resource naming and tagging | `string` | — | yes |
| `tags` | Additional tags to apply to all resources | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The name of the S3 bucket |
| `bucket_arn` | The ARN of the S3 bucket |
| `bucket_domain_name` | The regional domain name of the S3 bucket |

## Requirements

| Dependency | Version |
|------------|---------|
| Terraform | >= 1.5 |
| AWS provider | >= 5.0, < 6.0 |
