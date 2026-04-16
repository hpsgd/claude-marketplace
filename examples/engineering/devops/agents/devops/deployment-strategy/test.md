# Test: deployment strategy

Scenario: An engineering lead asks the DevOps agent to define a deployment strategy for migrating a Django application from a bare-metal server to containers, including the CI/CD pipeline and rollback plan.

## Prompt

We're running a Django 4.2 app called PalletTrack on a single Ubuntu 22.04 bare-metal server right now. We want to move it to containers and set up proper CI/CD. The app uses PostgreSQL 15 (managed by Neon) and Celery for background jobs. We deploy to production roughly twice a week. We need zero-downtime deployments and a clear rollback path if something goes wrong. What would you recommend?

## Criteria

- [ ] PASS: Agent checks for existing IaC (Pulumi.yaml, .tf files), existing CI workflows, and existing Dockerfiles before proposing anything new
- [ ] PASS: Agent produces a Dockerfile that uses multi-stage builds, a non-root user, pinned base image versions, and a HEALTHCHECK instruction
- [ ] PASS: Agent defines a CI/CD pipeline with stages in the correct order: lint → build → test → security scan → deploy
- [ ] PASS: Agent addresses zero-downtime deployments explicitly — describes a mechanism (blue/green, rolling update, or health-check-gated) with reasoning
- [ ] PASS: Agent defines a rollback plan with specific commands or steps, not just "roll back the deployment"
- [ ] PASS: Agent stops and asks before recommending new cloud resources with ongoing cost (as required by the decision checkpoints)
- [ ] PARTIAL: Agent addresses the Celery worker migration alongside the web server — not just the Django app in isolation
- [ ] PASS: Agent references the cattle-not-pets principle and ensures the deployment design treats containers as disposable/reproducible
