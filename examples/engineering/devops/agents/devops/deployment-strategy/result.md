# Output: deployment strategy

**Verdict:** PASS
**Score:** 16/17 criteria met (94%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent checks for existing IaC, CI workflows, and Dockerfiles before proposing anything new — Pre-Flight Step 2 is MANDATORY and lists explicit Glob patterns for all three: `**/Pulumi.yaml` or `**/*.tf` (IaC), `.github/workflows/*.yml` (CI/CD), `**/Dockerfile*` (containers), with an instruction to read existing IaC before adding anything new.

- [x] PASS: Agent produces a Dockerfile with multi-stage build, non-root user, pinned base image, HEALTHCHECK — Containers section provides a complete worked example with all four elements (builder + runtime stages, `addgroup`/`adduser` + `USER app`, `node:22-alpine` pinned, `HEALTHCHECK CMD wget...`), plus rules restating each requirement.

- [x] PASS: Agent defines CI/CD pipeline in the correct stage order — Pipeline Structure lists exactly: Lint & format check → Build → Unit tests → Integration tests → Security scan → Deploy (6 numbered steps), matching the required lint → build → test → security scan → deploy sequence.

- [x] PASS: Agent addresses zero-downtime deployments with a named mechanism and reasoning — Deployment Strategies has a three-row table (rolling update, blue/green, canary) each with "When to use" and "How it works" columns, plus health-check gating and connection draining rules.

- [x] PASS: Agent defines a rollback plan with specific commands — Rollback Procedures gives specific commands (redeploy previous image tag for containers, `pulumi up` with previous commit for IaC), automated trigger conditions, and a time budget: "5-15 minutes for stateless services" with an instruction to record the target in the runbook.

- [x] PASS: Agent stops and asks before recommending new cloud resources — Decision Checkpoints table marks "Creating new cloud resources with ongoing cost" as a MANDATORY STOP with reason "Budget decision."

- [~] PARTIAL: Agent addresses Celery worker migration — Worker and Background Containers section covers graceful SIGTERM shutdown, queue-depth monitoring instead of HTTP health endpoints, separate scaling, and idempotency for safe retry. Celery is not named explicitly but the section maps directly. Criteria label is PARTIAL; scored 0.5.

- [x] PASS: Agent references cattle-not-pets and treats containers as disposable/reproducible — Principles section states "Cattle not pets. Infrastructure is disposable and reproducible. No snowflake servers." Core section repeats it as a headline principle.

### Output expectations

- [x] PASS: Dockerfile is multi-stage with non-root user, pinned base image, and explicit HEALTHCHECK — all four present in the Containers section template; agent would apply same pattern with a Python base image.

- [x] PASS: Two distinct workloads addressed as separate containers/processes — Worker and Background Containers section distinguishes workers from web services with different health checks, scaling approach, and graceful shutdown handling.

- [x] PASS: CI/CD pipeline names the tool consistent with project conventions — Pipeline Structure gives the correct stage order; tooling-conventions rule names GitHub Actions as the standard CI/CD tool; Pre-Flight Step 1 instructs reading installed rules before acting.

- [x] PASS: Zero-downtime mechanism named explicitly with reasoning — Deployment Strategies table names rolling update, blue/green, and canary with "When to use" guidance, giving the agent a basis for a named, reasoned recommendation.

- [x] PASS: Rollback plan includes specific commands and a stated time budget — Rollback Procedures section provides specific commands and states "5-15 minutes for stateless services" as the RTO target, with an instruction to record it in the runbook.

- [x] PASS: Django migrations addressed explicitly — Deployment Strategies states migrations must be backward-compatible, migrations run as a discrete step before code rollout, halt the rollout if a migration fails, and deploy separately when not backward-compatible. Rollback Procedures covers migration reversibility and blue/green for irreversible migrations.

- [x] PASS: Stops and asks before new infrastructure with ongoing cost — Decision Checkpoints MANDATORY table covers this explicitly.

- [x] PASS: Environment configuration and secrets handling — Pipeline Rules state "Secrets injected at runtime — pulled from a secret store and injected as environment variables into the running container. Never hardcoded, never baked into image layers, never written to logs" with an explicit Neon Postgres example.

- [~] PARTIAL: Observability for new deployment — Monitoring & Alerting covers metrics (p50/p95/p99, error rate, throughput), structured JSON logging with an explicit note that container stdout/stderr is ephemeral and must be aggregated, and health endpoints. Does not specifically address the bare-metal-to-container transition: what replaces familiar file-based logs, or which specific aggregation tooling to adopt.

## Notes

The agent definition handles this scenario well. The two criteria that were previously scored as FAILs in an earlier evaluation (rollback time budget, migrations) are actually covered — Rollback Procedures Section 5 explicitly gives a 5-15 minute RTO target, and the migrations coverage is substantive. The previous evaluation also counted an extra criterion (bare-metal migration path as incremental cutover) that does not appear in test.md.

The only genuine weakness is the observability PARTIAL: the content is present but doesn't address what changes operationally when moving from a single server with file-based logs to ephemeral containers.
