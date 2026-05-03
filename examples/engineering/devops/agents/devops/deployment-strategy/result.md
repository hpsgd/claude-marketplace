# Deployment Strategy

Scenario: An engineering lead asks the DevOps agent to define a deployment strategy for migrating a Django application from a bare-metal server to containers, including the CI/CD pipeline and rollback plan.

## Prompt

> We're running a Django 4.2 app called PalletTrack on a single Ubuntu 22.04 bare-metal server right now. We want to move it to containers and set up proper CI/CD. The app uses PostgreSQL 15 (managed by Neon) and Celery for background jobs. We deploy to production roughly twice a week. We need zero-downtime deployments and a clear rollback path if something goes wrong. What would you recommend?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

My recommendation: **Docker Compose on your existing server + GitHub Actions CI/CD**, with blue-green deployment via Nginx upstream switching.

Here's the reasoning and the main tradeoff:

**Proposed stack**
- `docker compose` runs three services: `web` (Gunicorn), `worker` (Celery), `beat` (Celery beat)
- GitHub Actions builds and pushes images to GHCR on merge to `main`, then SSHes in to perform the cutover
- Nginx sits in front, switching between a `blue` and `green` compose stack — only the upstream pointer changes at cutover, giving you zero-downtime
- Rollback = point Nginx back at the previous stack (30-second operation, no redeploy)

**Why not a managed platform (Fly.io, Railway, ECS)?**
| | Bare-metal + Compose | Managed (Fly.io etc.) |
|---|---|---|
| Cost | Server you already pay for | ~$50–150/mo added |
| Rollback | Manual upstream switch | Built-in, one command |
| Ops burden | You maintain Docker/Nginx | Platform handles it |
| Neon compatibility | Fine | Fine |

If you're cost-sensitive and comfortable with a bit of ops, stay on bare-metal. If you'd rather have rollback, scaling, and zero-downtime handled for you without configuration, Fly.io is the strongest managed option (and plays well with Neon + Celery workers as separate processes).

**One thing to resolve before building:** Celery workers need to drain in-flight jobs before you kill the old stack. Do you have a max job runtime you can rely on, or do you need graceful shutdown signals wired up?

That answer shapes whether a simple `docker compose stop --timeout 60` is safe, or whether you need `SIGTERM` handling in your task code first.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 4.5/15.5 (29%) |
| Evaluated | 2026-04-30 |
| Target duration | 22515 ms |
| Target cost | $0.0909 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent checks for existing IaC (Pulumi.yaml, .tf files), existing CI workflows, and existing Dockerfiles before proposing anything new | FAIL | The output jumps directly into recommendations with no mention of checking for existing IaC, CI workflows, or Dockerfiles. No investigation step is described or implied. |
| c2 | Agent produces a Dockerfile that uses multi-stage builds, a non-root user, pinned base image versions, and a HEALTHCHECK instruction | FAIL | No Dockerfile is produced anywhere in the output. The response describes Docker Compose conceptually but provides zero container build artifacts. |
| c3 | Agent defines a CI/CD pipeline with stages in the correct order: lint → build → test → security scan → deploy | FAIL | The only CI/CD detail is 'GitHub Actions builds and pushes images to GHCR on merge to main, then SSHes in to perform the cutover.' No stages (lint, test, security scan) are defined or ordered. |
| c4 | Agent addresses zero-downtime deployments explicitly — describes a mechanism (blue/green, rolling update, or health-check-gated) with reasoning | PASS | The output explicitly names blue/green and describes the mechanism: 'Nginx sits in front, switching between a blue and green compose stack — only the upstream pointer changes at cutover, giving you zero-downtime.' |
| c5 | Agent defines a rollback plan with specific commands or steps, not just 'roll back the deployment' | PARTIAL | 'Rollback = point Nginx back at the previous stack (30-second operation, no redeploy)' describes the mechanism at a conceptual level but provides no actual commands (e.g., nginx reload, docker compose switch). |
| c6 | Agent stops and asks before recommending new cloud resources with ongoing cost (as required by the decision checkpoints) | FAIL | The output recommends GHCR (GitHub Container Registry) without pausing to ask. Fly.io costs are shown in a table but the agent does not stop and check before proceeding — it presents managed platforms as an option inline, not as a gated decision point. |
| c7 | Agent addresses the Celery worker migration alongside the web server — not just the Django app in isolation | PARTIAL | Output lists 'worker (Celery), beat (Celery beat)' as separate compose services and raises the graceful-shutdown question for in-flight jobs. Addressed but only at a high level without migration detail. |
| c8 | Agent references the cattle-not-pets principle and ensures the deployment design treats containers as disposable/reproducible | FAIL | No mention of cattle-not-pets, disposable containers, or reproducibility anywhere in the output. |
| c9 | Output's Dockerfile (or container build description) is a multi-stage build with a non-root user, a pinned base image version (e.g. `python:3.12-slim` not `python:latest`), and an explicit HEALTHCHECK | FAIL | No Dockerfile or container build description is present in the output. |
| c10 | Output addresses the two distinct workloads — the Django web app and the Celery workers — as separate container images or processes, not bundled into one image | PASS | Output explicitly lists three separate compose services: 'web (Gunicorn), worker (Celery), beat (Celery beat)', treating them as distinct processes. |
| c11 | Output's CI/CD pipeline orders stages as lint → build → test → security scan → deploy, with each stage gating the next, and names the tool (GitHub Actions / GitLab CI / Jenkins) consistent with the project conventions | FAIL | GitHub Actions is named, but no pipeline stages are defined. The output only states 'builds and pushes images to GHCR on merge to main.' No lint, test, or security scan stages appear. |
| c12 | Output's zero-downtime mechanism is named explicitly (rolling update, blue/green, or canary) with reasoning for the choice given the twice-weekly deploy cadence — not just 'we'll do zero-downtime' | PARTIAL | Blue/green is explicitly named and Nginx upstream switching is described. However, no reasoning is tied to the twice-weekly cadence — the choice is not justified relative to alternatives like rolling or canary given that specific rhythm. |
| c13 | Output's rollback plan includes specific commands or steps (kubectl rollout undo, fly deploy --image previous_tag, swap traffic back to old colour) with a stated time budget — not 'redeploy the previous version' | PARTIAL | 'Rollback = point Nginx back at the previous stack (30-second operation, no redeploy)' states a time budget (30 seconds) but provides no specific commands to execute the upstream switch. |
| c14 | Output addresses Django migrations explicitly — when migrations run in the deployment, how forward/backward compatibility is preserved across the rolling update, and what happens if a migration fails | FAIL | Django migrations are not mentioned anywhere in the output. |
| c15 | Output stops and asks before recommending new infrastructure with ongoing cost (e.g. Kubernetes cluster, container registry, managed Redis for Celery broker), framing the cost trade-offs | PARTIAL | The output frames cost trade-offs in a comparison table ('~$50–150/mo added' for managed platforms) but does not stop and ask before recommending GHCR or Fly.io — it proceeds inline without a decision checkpoint. |
| c16 | Output addresses environment configuration — secrets handling (not baked into the image), env var injection at runtime, and how Neon Postgres credentials reach the container without ending up in a layer | FAIL | No mention of secrets handling, environment variable injection, or how Neon credentials are passed to containers. The topic is entirely absent. |
| c17 | Output addresses observability for the new deployment — health endpoints, log aggregation, metrics — given the move from a single bare-metal server with familiar logs to ephemeral containers | FAIL | Observability, health endpoints, log aggregation, and metrics are not mentioned anywhere in the output. |

### Notes

The captured output is a high-level conversational recommendation rather than a structured deployment strategy. It correctly identifies blue/green as the zero-downtime mechanism and acknowledges Celery as a separate concern, but it fails on nearly every criterion requiring concrete artifacts or specificity: no Dockerfile, no CI/CD stage definition, no migration handling, no secrets management, no observability plan, and no cattle-not-pets framing. The rollback plan names the approach but lacks executable commands. The agent also does not audit existing infrastructure before making recommendations, which is a foundational gap. The response would be appropriate as an opening orientation message, but not as a deployment strategy deliverable.
