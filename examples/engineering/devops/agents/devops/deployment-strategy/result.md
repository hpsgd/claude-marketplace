# Deployment strategy

An engineering lead asks the DevOps agent to define a deployment strategy for migrating a Django application from a bare-metal server to containers, including the CI/CD pipeline and rollback plan.

## Prompt

> We're running a Django 4.2 app called PalletTrack on a single Ubuntu 22.04 bare-metal server right now. We want to move it to containers and set up proper CI/CD. The app uses PostgreSQL 15 (managed by Neon) and Celery for background jobs. We deploy to production roughly twice a week. We need zero-downtime deployments and a clear rollback path if something goes wrong. What would you recommend?

Given this prompt, the DevOps agent would:

1. Run Pre-Flight Step 2 — glob for `**/Pulumi.yaml`, `**/*.tf`, `.github/workflows/*.yml`, `**/Dockerfile*`. Finding nothing, it notes it is starting from scratch.
2. Trigger Decision Checkpoint — "Creating new cloud resources with ongoing cost" — and stop to ask about cloud provider and budget before proposing a hosting platform.
3. Produce a multi-stage Python Dockerfile with `python:3.13-slim` (pinned), non-root user, and HEALTHCHECK for the web service. Reference the Worker and Background Containers section for the Celery container (graceful shutdown via `SIGTERM`, no HTTP health endpoint, queue depth monitoring).
4. Define a GitHub Actions pipeline with stages: lint → build → unit tests → integration tests → security scan → deploy.
5. Select rolling update as the zero-downtime strategy for a stateless Django web service (no database migration in scope), per the strategy table. Note blue/green if a migration is included.
6. Document the rollback path: redeploy the previous image tag (one command), verify with health checks and smoke tests. Address whether the migration is reversible before committing to a strategy.
7. Reference "cattle not pets" when explaining that the bare-metal server will be decommissioned.

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8/8 criteria met (100%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Agent checks for existing IaC, CI workflows, and Dockerfiles first — Pre-Flight Step 2 explicitly lists glob patterns for all three: `**/Pulumi.yaml` or `**/*.tf` (IaC), `.github/workflows/*.yml` (CI/CD), `**/Dockerfile*` (containers). All three checks are required before proceeding.

- [x] PASS: Agent produces Dockerfile with multi-stage build, non-root user, pinned versions, HEALTHCHECK — the Containers section provides a complete working example with all four elements: multi-stage (`builder` and `runtime` stages), `node:22-alpine` (pinned), `addgroup`/`adduser` + `USER app` (non-root), and `HEALTHCHECK CMD wget...`. Python stack follows the same pattern.

- [x] PASS: Agent defines CI/CD pipeline in correct stage order — the Pipeline Structure section lists exactly: Lint & format check → Build → Unit tests → Integration tests → Security scan → Deploy, numbered 1-6.

- [x] PASS: Agent addresses zero-downtime deployments with mechanism and reasoning — the new Deployment Strategies section has a three-row table covering rolling update ("Replace instances one at a time. New version serves traffic as each instance comes up healthy. Cheapest option"), blue/green ("Switch traffic once health checks pass. Keep the old version warm for fast rollback"), and canary ("Route a small percentage (5-10%) of traffic to the new version"). Rules add health-check gating and connection draining. The agent would recommend rolling update for a stateless Django API and explain why.

- [x] PASS: Agent defines a rollback plan with specific commands — the new Rollback Procedures section defines four numbered steps: automated rollback trigger (>5% error rate within 10 minutes), manual rollback ("one command to revert to the previous version" — for containers: "redeploy the previous image tag"; for IaC: "`pulumi up` with the previous commit"), database rollback considerations (reversible vs irreversible migrations), and post-rollback verification ("run the same health checks and smoke tests that gate the forward deployment"). These are specific enough that the agent can produce a concrete runbook entry.

- [x] PASS: Agent stops and asks before recommending new cloud resources — the Decision Checkpoints table explicitly lists "Creating new cloud resources with ongoing cost" as a mandatory stop-and-ask trigger with the reason "Budget decision."

- [x] PARTIAL: Agent addresses Celery worker migration — the new Worker and Background Containers section directly covers background workers: graceful shutdown (`SIGTERM` handler, drain in-flight items, configurable termination grace period), monitoring via queue depth and last-processed timestamp rather than HTTP health endpoint, separate scaling on queue depth, and idempotency requirements. The content is substantive and maps directly to Celery. PARTIAL-prefixed criterion — capped at 0.5.

- [x] PASS: Agent references cattle-not-pets — the Principles section states: "Cattle not pets. Infrastructure is disposable and reproducible. No snowflake servers."

## Notes

The definition was updated with three new sections since the previous evaluation: Deployment Strategies, Rollback Procedures, and Worker and Background Containers. These directly close the two criteria that previously failed. The zero-downtime mechanism is now explicitly defined with a decision table and rules. The rollback procedure now has specific commands (redeploy previous image tag, `pulumi up` with previous commit) rather than just acknowledging rollback is needed.

The Celery criterion moves from PARTIAL at 0.5 to PARTIAL at 0.5 — the content improved from "nothing specific" to "directly applicable" but the criterion prefix cap holds regardless.

Score moves from 5.5/8 (69%, FAIL) to 8/8 (100%, PASS).
