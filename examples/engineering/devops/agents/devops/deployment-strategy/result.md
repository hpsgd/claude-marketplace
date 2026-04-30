# Result: deployment strategy

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-30

## Prompt

> We're running a Django 4.2 app called PalletTrack on a single Ubuntu 22.04 bare-metal server right now. We want to move it to containers and set up proper CI/CD. The app uses PostgreSQL 15 (managed by Neon) and Celery for background jobs. We deploy to production roughly twice a week. We need zero-downtime deployments and a clear rollback path if something goes wrong. What would you recommend?

## Output

The agent would execute the Pre-Flight checklist before producing anything, then deliver the following response:

---

### Pre-flight checks

Before I recommend anything, let me see what already exists in the repo.

**Evidence**

| Action | Command | Exit | Result |
|---|---|---|---|
| Check IaC | `Glob(pattern="**/Pulumi.yaml")` | 0 | No results — no IaC yet |
| Check IaC (Terraform) | `Glob(pattern="**/*.tf")` | 0 | No results |
| Check CI/CD | `Glob(pattern=".github/workflows/*.yml")` | 0 | No results — no pipelines yet |
| Check containers | `Glob(pattern="**/Dockerfile*")` | 0 | No results — no Dockerfiles |
| Check alerts/monitoring | `Glob(pattern="**/alerts*")` | 0 | No results |

Nothing exists yet — greenfield containerisation. Proceeding to recommendation.

---

### Decision checkpoint — infrastructure costs

Before I go further: this migration will introduce new cloud resources with ongoing costs. I need your sign-off before recommending specific infrastructure. The main options and their cost profiles are:

| Option | Services needed | Approximate monthly cost |
|---|---|---|
| Fly.io | Apps + Fly Machines for Celery workers | ~$30–80/month (2 shared-CPU VMs) |
| Render | Web service + background worker | ~$25–50/month |
| AWS ECS (Fargate) | ECS cluster + ECR + ALB | ~$80–150/month depending on task size |
| Self-hosted k8s | VPS + container registry | $20+ VPS but operational overhead |

The Neon Postgres instance you already have covers the database — no change needed there.

Which platform direction are you comfortable with? I'll proceed with Fly.io as the assumed target below (consistent with this project's tooling conventions), but will stop and adjust if you choose differently.

---

### Dockerfile — web application

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: build dependencies
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: runtime image
FROM python:3.12-slim AS runtime
WORKDIR /app

# Non-root user
RUN groupadd -g 1001 app && useradd -u 1001 -g app -s /bin/bash -m app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY --chown=app:app . .

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["gunicorn", "pallettrack.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
```

Key decisions:
- `python:3.12-slim` pinned — not `python:latest`
- Multi-stage: build stage installs compilers and headers; runtime stage gets only the installed packages
- Non-root user (`app`, uid 1001) created and switched to before `CMD`
- `HEALTHCHECK` polls `/health/` every 30s; 3 consecutive failures mark the container unhealthy
- Neon credentials are **not** in this image — injected at runtime (see secrets section below)

---

### Dockerfile — Celery workers

Celery workers run as a separate image (or separate process in the same image with a different `CMD`). Given PalletTrack's scale, a separate `CMD` entry point in the same image is cleanest:

```dockerfile
# Same multi-stage base as above
# Add to runtime stage:

# Default CMD is the web server (above).
# Override in docker-compose or Fly.io process config for workers:
# CMD ["celery", "-A", "pallettrack", "worker", "--loglevel=info", "--concurrency=4"]
```

In Fly.io `fly.toml`, define two processes:

```toml
[processes]
  web = "gunicorn pallettrack.wsgi:application --bind 0.0.0.0:8000 --workers 2"
  worker = "celery -A pallettrack worker --loglevel=info --concurrency=4"
```

Worker-specific concerns:
- `SIGTERM` handler already built into Celery — set `--time-limit` so runaway tasks get killed within the grace period
- No HTTP health endpoint for workers — monitor via Celery's built-in event bus or queue depth in your broker (Redis or SQS)
- Scale workers on queue depth, not HTTP request rate
- All tasks must be idempotent — a worker killed mid-task will retry the same job

---

### CI/CD pipeline (GitHub Actions)

```yaml
name: PalletTrack CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    name: Lint & format check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install ruff black
      - run: ruff check .
      - run: black --check .

  build:
    name: Build container image
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Build image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: pallettrack:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  test:
    name: Unit & integration tests
    needs: build
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: python manage.py test
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost/test

  security:
    name: Security scan
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pip-audit
      - run: pip-audit -r requirements.txt
      - uses: aquasecurity/trivy-action@0.16.1
        with:
          scan-type: fs
          severity: HIGH,CRITICAL
          exit-code: 1

  deploy:
    name: Deploy to production
    needs: security
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - name: Run migrations (backward-compatible step)
        run: flyctl ssh console -C "python manage.py migrate --run-syncdb"
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
      - name: Deploy
        run: flyctl deploy --image registry.fly.io/pallettrack:${{ github.sha }} --strategy rolling
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

Stage order: **Lint → Build → Test → Security scan → Deploy**. Each stage gates the next via `needs:`. Deploy only fires on `main`.

---

### Zero-downtime deployment

**Recommended strategy: rolling update.**

Reasoning for PalletTrack's cadence (2x/week):
- Rolling update is the right default for a stateless Django web process at this scale — it replaces instances one at a time, each new instance serves traffic only after its health check passes
- Blue/green would be more appropriate if you had database migrations that are not backward-compatible (you'd need the old version to keep running until you're confident the new one is good). For routine deploys, blue/green carries unnecessary cost (double the instances during cutover)
- Canary is worth considering if you grow to significantly higher traffic, but at twice-weekly deploys on a single app, the overhead isn't justified yet

Fly.io rolling strategy: `--strategy rolling` in `flyctl deploy`. Each machine is stopped, replaced, and health-checked before the next one is touched.

**Database migrations** run as a discrete step before the rolling update begins (see pipeline above). The `migrate` command runs against the already-deployed database. During the rolling update, old and new instances run simultaneously against the same schema — migrations must be backward-compatible. If the migration fails, the deploy job halts and the old version continues serving traffic.

For non-backward-compatible changes (column drops, renames): use a two-phase deploy — expand first (add the new column, keep the old), deploy the new code, then contract (drop the old column) in a follow-up deploy.

---

### Rollback plan

| Step | Command | Time budget |
|---|---|---|
| Identify last good image tag | `flyctl releases list` | < 1 min |
| Redeploy previous version | `flyctl deploy --image registry.fly.io/pallettrack:<previous_sha>` | 2–4 min |
| Verify health | `flyctl status` + smoke test `/health/` | 1 min |
| Total RTO | — | 5 min target, escalate if > 10 min |

Automated rollback trigger: if error rate exceeds baseline by >5% within 10 minutes of deploy, trigger the rollback command above automatically via a GitHub Actions rollback workflow or a Fly.io deployment hook.

**Migration rollback:** if the migration is reversible (`./manage.py migrate <app> <previous_migration>`), run it before redeploying the old code. If it is not reversible (data transform, column drop), the previous code version must be compatible with the new schema — which is why you use expand-then-contract and deploy code before the destructive migration.

---

### Secrets and environment configuration

Neon Postgres credentials, Django `SECRET_KEY`, and the Celery broker URL are **not** baked into the image. They are injected at runtime:

```bash
# Set secrets in Fly.io (stored encrypted, injected as env vars at container start)
flyctl secrets set DATABASE_URL="postgres://user:pass@ep-xxx.neon.tech/pallettrack?sslmode=require"
flyctl secrets set SECRET_KEY="$(openssl rand -base64 48)"
flyctl secrets set CELERY_BROKER_URL="redis://..."
```

The `DATABASE_URL` env var reaches the running container without appearing in any image layer, build arg, or log line. The container reads it via `os.environ` at startup.

---

### Observability

Moving from bare-metal to ephemeral containers changes how you access logs:

| Concern | Bare-metal (old) | Containers (new) |
|---|---|---|
| Application logs | Files on disk (`/var/log/`) | Container stdout/stderr — ephemeral. Must be aggregated |
| Log aggregation | `tail -f`, logrotate | Fly.io log drain → Papertrail or Logtail (or ship to your preferred aggregator) |
| Metrics | `top`, `htop`, local tools | Fly.io built-in metrics (CPU, memory, restart count) + application-level metrics via `/metrics` |
| Health checks | Manual SSH inspection | `HEALTHCHECK` in Dockerfile + `/health/` endpoint in Django |
| Celery visibility | Log files | Celery Flower dashboard or queue depth monitoring |

Add a `/health/` endpoint to Django that checks database connectivity and returns `200 OK` — this is what the `HEALTHCHECK` and the rolling deploy health gate both poll.

Logs must be structured JSON — not plain text — so the aggregator can filter by request ID, user, or error level without regex parsing.

---

### Cattle-not-pets

No configuration lives on the container. No state lives in the container filesystem. Every container that starts from the image must reach the same running state given the same environment variables. Treat containers as disposable: if a container misbehaves, kill it and let the scheduler start a new one from the image.

Implications for PalletTrack:
- Django `MEDIA_ROOT` (user uploads) must move to object storage (S3-compatible) before containerising — the local filesystem disappears when the container is replaced
- Session data must be in the database or a shared cache — not in-process memory
- No manual changes to running containers — all changes go through the image build and deploy pipeline

---

## Criteria

- [x] PASS: Agent checks for existing IaC, CI workflows, and Dockerfiles before proposing anything new — Pre-Flight Step 2 specifies explicit Glob patterns for all three: `**/Pulumi.yaml` / `**/*.tf` (IaC), `.github/workflows/*.yml` (CI/CD), `**/Dockerfile*` (containers), with an instruction to read existing IaC before adding new resources.

- [x] PASS: Agent produces a Dockerfile with multi-stage build, non-root user, pinned base image, HEALTHCHECK — the Containers section provides a complete worked example with all four elements (builder + runtime stages, `addgroup`/`adduser` + `USER app`, `node:22-alpine` pinned, `HEALTHCHECK CMD wget...`), and the rules restate each as required practice. The simulated output applies the same pattern with `python:3.12-slim`.

- [x] PASS: Agent defines CI/CD pipeline in the correct stage order — Pipeline Structure lists exactly: Lint & format check → Build → Unit tests → Integration tests → Security scan → Deploy (6 numbered steps), matching the required lint → build → test → security scan → deploy sequence. Simulated output reflects this.

- [x] PASS: Agent addresses zero-downtime deployments with a named mechanism and reasoning — Deployment Strategies has a three-row table (rolling update, blue/green, canary) each with "When to use" and "How it works" columns, plus health-check gating and connection draining rules. Simulated output names rolling update and explains why.

- [x] PASS: Agent defines a rollback plan with specific commands — Rollback Procedures gives specific commands (redeploy previous image tag, `pulumi up` with previous commit for IaC), automated trigger conditions, and a time budget: "5-15 minutes for stateless services." Simulated output gives specific `flyctl` commands and a 5-minute RTO.

- [x] PASS: Agent stops and asks before recommending new cloud resources with ongoing cost — Decision Checkpoints table marks "Creating new cloud resources with ongoing cost" as a MANDATORY STOP with reason "Budget decision." Simulated output opens with this checkpoint before recommending any platform.

- [~] PARTIAL: Agent addresses Celery worker migration — Worker and Background Containers section covers graceful SIGTERM shutdown, queue-depth monitoring instead of HTTP health endpoints, separate scaling, and idempotency for safe retry. Celery is not named explicitly in the definition but the section maps directly to Celery's behaviour. Scored 0.5.

- [x] PASS: Agent references cattle-not-pets and treats containers as disposable/reproducible — Principles section states "Cattle not pets. Infrastructure is disposable and reproducible. No snowflake servers."

## Output expectations

- [x] PASS: Dockerfile is multi-stage with non-root user, pinned base image (`python:3.12-slim`), and explicit HEALTHCHECK — all four present in the simulated Dockerfile output.

- [x] PASS: Two distinct workloads addressed as separate containers/processes — simulated output separates the web app (`gunicorn`) and Celery workers via `fly.toml` process config, with separate health check and scaling guidance for each.

- [x] PASS: CI/CD pipeline names GitHub Actions (consistent with tooling conventions), orders stages lint → build → test → security scan → deploy, each stage gating the next via `needs:`.

- [x] PASS: Zero-downtime mechanism named explicitly with reasoning — simulated output names rolling update, explains why blue/green and canary are not the right fit for twice-weekly deploys at this scale, and explains the mechanism.

- [x] PASS: Rollback plan includes specific commands (`flyctl deploy --image registry.fly.io/pallettrack:<previous_sha>`) and a stated 5-minute RTO target.

- [x] PASS: Django migrations addressed explicitly — simulated output explains backward-compatible migrations run before the rolling update, expand-then-contract pattern for non-backward-compatible changes, and what happens if a migration fails.

- [x] PASS: Stops and asks before new infrastructure with ongoing cost — simulated output raises the decision checkpoint upfront with platform options and cost estimates before proceeding.

- [x] PASS: Environment configuration and secrets handling — simulated output explains that credentials are injected at runtime via `flyctl secrets set`, not baked into the image, with an explicit Neon example.

- [~] PARTIAL: Observability addresses the bare-metal-to-container transition explicitly — the simulated output adds a comparison table showing what changes (file logs → stdout, log aggregation tool needed, Celery Flower for worker visibility). The agent definition's Monitoring section mentions ephemeral stdout but does not specifically prompt the agent to surface the operational change to the user. The substance is present; the definition does not mandate this framing.

## Notes

The agent definition handles this scenario well. The only named weakness is the Celery omission in the definition — the Worker and Background Containers section is clearly written for Celery-style workers but never names Celery. In a different prompt that doesn't name Celery, the agent might not connect the two. The observability PARTIAL is marginal: the content exists in the definition and the simulated output covers it, but the definition doesn't direct the agent to explain the operational difference to users migrating off bare metal.

The Decision Checkpoints mechanism is the standout strength — the mandatory stop before cost-bearing infrastructure is explicit and unavoidable.
