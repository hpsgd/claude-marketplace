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

## Output expectations

- [ ] PASS: Output's Dockerfile (or container build description) is a multi-stage build with a non-root user, a pinned base image version (e.g. `python:3.12-slim` not `python:latest`), and an explicit HEALTHCHECK
- [ ] PASS: Output addresses the two distinct workloads — the Django web app and the Celery workers — as separate container images or processes, not bundled into one image
- [ ] PASS: Output's CI/CD pipeline orders stages as lint → build → test → security scan → deploy, with each stage gating the next, and names the tool (GitHub Actions / GitLab CI / Jenkins) consistent with the project conventions
- [ ] PASS: Output's zero-downtime mechanism is named explicitly (rolling update, blue/green, or canary) with reasoning for the choice given the twice-weekly deploy cadence — not just "we'll do zero-downtime"
- [ ] PASS: Output's rollback plan includes specific commands or steps (kubectl rollout undo, fly deploy --image previous_tag, swap traffic back to old colour) with a stated time budget — not "redeploy the previous version"
- [ ] PASS: Output addresses Django migrations explicitly — when migrations run in the deployment, how forward/backward compatibility is preserved across the rolling update, and what happens if a migration fails
- [ ] PASS: Output stops and asks before recommending new infrastructure with ongoing cost (e.g. Kubernetes cluster, container registry, managed Redis for Celery broker), framing the cost trade-offs
- [ ] PASS: Output addresses environment configuration — secrets handling (not baked into the image), env var injection at runtime, and how Neon Postgres credentials reach the container without ending up in a layer
- [ ] PARTIAL: Output addresses observability for the new deployment — health endpoints, log aggregation, metrics — given the move from a single bare-metal server with familiar logs to ephemeral containers
