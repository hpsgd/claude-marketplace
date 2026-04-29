# Result: deployment strategy

**Verdict:** PARTIAL
**Score:** 14/18 criteria met (77.8%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent checks for existing IaC, CI workflows, and Dockerfiles first — Pre-Flight Step 2 is MANDATORY and lists explicit glob patterns for all three: `**/Pulumi.yaml` or `**/*.tf` (IaC), `.github/workflows/*.yml` (CI/CD), `**/Dockerfile*` (containers), with an instruction to read existing IaC before adding anything new.

- [x] PASS: Agent produces a Dockerfile with multi-stage build, non-root user, pinned base image, HEALTHCHECK — the Containers section provides a complete worked example with all four elements (builder + runtime stages, `addgroup`/`adduser` + `USER app`, `node:22-alpine` pinned, `HEALTHCHECK CMD wget...`), plus rules below the example restating each requirement.

- [x] PASS: Agent defines CI/CD pipeline in the correct stage order — Pipeline Structure lists exactly: Lint & format check → Build → Unit tests → Integration tests → Security scan → Deploy (6 numbered steps), matching the required lint → build → test → security scan → deploy sequence.

- [x] PASS: Agent addresses zero-downtime deployments with a named mechanism and reasoning — Deployment Strategies has a three-row table (rolling update, blue/green, canary) each with "When to use" and "How it works" columns, plus rules on health-check gating before traffic and connection draining before termination.

- [x] PASS: Agent defines a rollback plan with specific commands — Rollback Procedures gives four numbered steps including specific commands: "redeploy the previous image tag" for containers and "`pulumi up` with the previous commit" for IaC, plus automated trigger conditions and post-rollback verification.

- [x] PASS: Agent stops and asks before recommending new cloud resources — Decision Checkpoints table marks "Creating new cloud resources with ongoing cost" as a MANDATORY STOP with reason "Budget decision."

- [~] PARTIAL: Agent addresses Celery worker migration — Worker and Background Containers section covers graceful SIGTERM shutdown, queue-depth monitoring instead of HTTP health endpoints, separate scaling, and idempotency for safe retry. Celery is not named but the patterns apply directly. Capped at 0.5 per criterion label.

- [x] PASS: Agent references cattle-not-pets — Principles section states "Cattle not pets. Infrastructure is disposable and reproducible. No snowflake servers." Core section repeats it as a headline principle.

### Output expectations

- [x] PASS: Output's Dockerfile is a multi-stage build with non-root user, pinned base image, and explicit HEALTHCHECK — the Containers section includes a complete worked example with all four elements and the agent would apply the same template to a Python base image.

- [x] PASS: Output addresses two distinct workloads as separate containers/processes — the dedicated "Worker and Background Containers" section distinguishes workers from web services (different health checks, different scaling approach), which drives separate treatment of the Django web app and Celery workers.

- [x] PASS: Output's CI/CD pipeline names the tool consistent with project conventions — Pipeline Structure gives the correct stage order; the installed tooling-conventions rule names GitHub Actions as the standard CI/CD tool; Pre-Flight Step 1 instructs the agent to read installed rules before acting.

- [x] PASS: Output's zero-downtime mechanism is named explicitly with reasoning — the Deployment Strategies table names rolling update, blue/green, and canary with "When to use" guidance, giving the agent a basis for a named, reasoned recommendation. The twice-weekly cadence is not a named selection factor in the definition, but the agent would choose and justify based on service characteristics (stateless, migration presence).

- [ ] FAIL: Output's rollback plan includes a stated time budget — Rollback Procedures gives specific commands (redeploy previous image tag, `pulumi up` with previous commit) but is silent on a time budget for restoration. The criterion requires a stated time target (e.g. "restore service within 5 minutes"); the definition provides no basis for one.

- [~] PARTIAL: Output addresses Django migrations explicitly — Deployment Strategies states "Database migrations must be backward-compatible" and "deploy the migration separately from the code change if needed"; Rollback Procedures covers migration reversibility and blue/green for irreversible migrations. But the definition does not address when migrations run within the deployment sequence, or what happens if a migration fails mid-rolling-update. Coverage is present but incomplete for the full criterion.

- [x] PASS: Output stops and asks before recommending new infrastructure with ongoing cost — Decision Checkpoints MANDATORY table covers this explicitly.

- [~] PARTIAL: Output addresses environment configuration — Pipeline Rules state "Secrets via environment variables — never hardcoded, never in logs"; the Pulumi section covers encrypted config for provider tokens. But the agent definition does not explicitly address runtime env var injection into containers or how Neon Postgres credentials reach the container at runtime without being baked into an image layer. Pipeline secrets and container runtime secrets are distinct concerns; only the former is clearly covered.

- [~] PARTIAL: Output addresses observability for the new deployment — Monitoring & Alerting section covers metrics (p50/p95/p99, error rate, throughput), structured JSON logging, and health endpoints. However, the definition does not specifically address the transition challenge: moving from a single bare-metal server with familiar logs to ephemeral containers where log aggregation and health endpoints need deliberate setup.

- [ ] FAIL: Output addresses migration path as incremental cutover rather than big-bang — the agent definition has no section, rule, or principle covering parallel running, traffic shifting, or incremental cutover patterns from bare-metal to containers. "Cattle not pets" describes the end state, not the migration approach. The definition gives no basis for this output.

## Notes

The agent definition handles the structural and operational aspects of container deployments well — the Pre-Flight checks, Dockerfile template, pipeline stages, rollback commands, and worker separation are all concrete and actionable.

The two outright failures both relate to things the definition never needed to cover before: rollback time budgets and bare-metal-to-container migration paths. Neither is an unreasonable omission for a general-purpose DevOps agent definition, but they are gaps for this specific scenario.

The three PARTIAL results (migrations, secrets, observability) reflect cases where the definition has relevant material that falls short of the criterion's specificity. The Django migration coverage is the closest to a pass — the backward-compatibility rule and blue/green guidance for irreversible migrations are substantive, but the timing and failure-path questions are unanswered.

The environment configuration gap is worth flagging: the Pulumi section explicitly says provider tokens go in encrypted Pulumi config and *not* in environment variables, which is in tension with the Pipeline Rules saying secrets go via environment variables. This ambiguity would surface if the agent tried to address how Neon credentials reach the container.
