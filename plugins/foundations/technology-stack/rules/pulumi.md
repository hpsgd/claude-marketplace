---
description: Pulumi infrastructure-as-code patterns and conventions
paths:
  - "**/infrastructure/**"
  - "**/Pulumi.*"
  - "**/Pulumi.yaml"
---

# Pulumi IaC Conventions

## Project structure
- All infrastructure managed with Pulumi (TypeScript, ESM)
- Each provider is a separate Pulumi project under `infrastructure/`
- State stored in Pulumi Cloud (not local files, not S3)

## Provider authentication
- Each stack stores its provider token as encrypted Pulumi config
- Only `PULUMI_ACCESS_TOKEN` needed in CI (GitHub Actions)
- Never store provider tokens in environment variables or plaintext config

## Cross-stack secrets
- Use Pulumi stack outputs/references for cross-stack secret sharing
- Example: Resend stack exports `sendingApiKey` → Vercel stack reads and sets `RESEND_API_KEY`
- Secrets auto-propagate when dependent stacks are deployed

## API key rotation
- Age-based rotation (e.g., 90-day) via weekly cron
- Rotation auto-propagates to dependent stacks (e.g., Vercel env vars)
- Never rely on manual key rotation

## Auto-discovery in CI
- Workflows use matrix strategy from `infrastructure/*/Pulumi.yaml`
- Zero config for new stacks — add a directory with `Pulumi.yaml` and CI picks it up automatically

## Deployment pipeline
```
feature/my-thing ──squash──> main
                               │
                         Pulumi deploy (infrastructure)
                         Vercel deploy (web)
```

- Infrastructure deploys triggered on merge to main
- Web deploys via Vercel (automatic on push)
- PR previews for web apps
