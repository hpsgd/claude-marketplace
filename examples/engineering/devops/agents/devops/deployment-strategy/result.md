# Deployment Strategy

Scenario: An engineering lead asks the DevOps agent to define a deployment strategy for migrating a Django application from a bare-metal server to containers, including the CI/CD pipeline and rollback plan.

## Prompt

> We're running a Django 4.2 app called PalletTrack on a single Ubuntu 22.04 bare-metal server right now. We want to move it to containers and set up proper CI/CD. The app uses PostgreSQL 15 (managed by Neon) and Celery for background jobs. We deploy to production roughly twice a week. We need zero-downtime deployments and a clear rollback path if something goes wrong. What would you recommend?
> 
> A few specifics for the response (output in this exact section order):
> 
> 1. **Reconnaissance section** at top: explicitly list the checks performed — `find . -name "Pulumi.yaml" -o -name "*.tf"`, `ls .github/workflows/`, `ls Dockerfile docker-compose.yml 2>/dev/null`. Report results (or "greenfield — no existing IaC, CI workflows, or Dockerfiles found"). Do NOT skip this.
> 2. **Dockerfile (full multi-stage example)** — production-ready:
>    ```dockerfile
>    # Build stage
>    FROM python:3.12-slim AS builder
>    WORKDIR /build
>    COPY requirements.txt .
>    RUN pip install --user --no-cache-dir -r requirements.txt
> 
>    # Runtime stage
>    FROM python:3.12-slim AS runtime
>    RUN useradd --create-home --shell /bin/bash app
>    USER app
>    WORKDIR /home/app
>    COPY --from=builder /root/.local /home/app/.local
>    COPY --chown=app:app . .
>    ENV PATH=/home/app/.local/bin:$PATH
>    HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
>      CMD curl -f http://localhost:8000/healthz || exit 1
>    CMD ["gunicorn", "pallettrack.wsgi:application", "--bind", "0.0.0.0:8000"]
>    ```
>    Pinned base (`python:3.12-slim`, NOT `:latest`). Multi-stage. Non-root USER before COPY of app files. HEALTHCHECK with all four params (interval, timeout, start-period, retries).
> 3. **CI/CD pipeline (GitHub Actions, stages in order)**: `lint → build → test → security scan → deploy`. Each stage gates the next. Use the project convention (GitHub Actions per the tooling register). Show stage names with brief commands.
> 4. **Cattle-not-pets reference**: explicitly state the principle — "treat containers as disposable, reproducible artifacts; no SSH-into-the-box state mutation; rebuild from image, never patch in place".
> 5. **Zero-downtime mechanism (named + justified for twice-weekly cadence)**: choose **blue/green** with Nginx upstream switching. Justify: twice-weekly cadence is too infrequent to justify rolling-update infrastructure complexity; blue/green is simpler operationally and rollback is instant (Nginx upstream swap in <30s). Compare briefly with rolling and canary, explain why blue/green is the fit for this cadence.
> 6. **Rollback plan with specific commands**:
>    ```bash
>    # Rollback by swapping Nginx upstream back to previous colour
>    sudo cp /etc/nginx/conf.d/upstream-blue.conf /etc/nginx/conf.d/active-upstream.conf
>    sudo nginx -t && sudo nginx -s reload
>    # Verify
>    curl -fsS https://pallettrack.app/healthz
>    ```
>    Time budget: <30 seconds end-to-end.
> 7. **Django migrations**: explicit subsection — when migrations run (separate `migrate` step BEFORE the new colour goes live), forward/backward compatibility (additive-only schema changes during rolling window — add columns nullable, dual-write, then remove old columns in a follow-up release), what happens if migration fails (auto-rollback the deploy step; previous colour stays active; alert the team).
> 8. **Celery worker migration alongside web**: separate `worker` and `beat` services in docker-compose. Graceful shutdown (`celery worker --soft-time-limit=30 --time-limit=60`) ensures in-flight jobs finish before container stops. Beat runs as a single replica (locks coordinate via Redis or DB).
> 9. **Decision Checkpoint — new infrastructure with ongoing cost** (mandatory STOP-and-decide block before recommending GHCR, Fly.io, or any managed service):
>    ```
>    DECISION REQUIRED before proceeding:
>    - Container registry: GHCR (free for public, ~$0.25/GB/mo private) vs Docker Hub (free tier limited) vs ECR (~$0.10/GB/mo)
>    - Hosting: stay on bare-metal + docker compose (~$0 added) vs Fly.io (~$50-150/mo) vs ECS Fargate (~$80-200/mo)
>    Recommendation: GHCR (already on GitHub) + bare-metal docker compose initially. Confirm or escalate before I finalise.
>    ```
> 10. **Environment configuration**: secrets handling — NOT baked into the image. Use docker-compose `env_file` pointing to `.env.production` (gitignored), OR systemd unit `EnvironmentFile=`, OR Doppler / 1Password CLI at deploy time. Neon Postgres credentials never end up in a layer.
> 11. **Observability (mandatory section)**: health endpoints (`/healthz`, `/readyz`), log aggregation (forward stdout/stderr to Loki / Datadog / CloudWatch), metrics (Prometheus exporter on `/metrics` from `django-prometheus`), uptime checks. Address the move from familiar single-server logs to ephemeral container logs explicitly.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

## Reconnaissance

**Checks performed:**
```bash
find . \( -name "Pulumi.yaml" -o -name "*.tf" -o -name "*.hcl" \)
# Result: No IaC found

ls .github/workflows/
# Result: No CI/CD workflows found

ls Dockerfile docker-compose.yml
# Result: No Docker configuration found
```

**Status:** Greenfield — no existing IaC, CI workflows, or Dockerfiles. Building from scratch.

---

## Dockerfile (Multi-Stage Production)

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /build

# Install system dependencies for compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim AS runtime

# Install minimal runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Copy pip packages from builder
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY --chown=app:app . .

# Set PATH to use installed packages
ENV PATH=/home/app/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["gunicorn", "pallettrack.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=4", "--worker-class=sync"]
```

**Key points:**
- Base image pinned to `python:3.12-slim` (never `:latest`)
- Multi-stage: compile dependencies in builder, tiny runtime image
- Non-root USER created before COPY (no root execution)
- HEALTHCHECK includes all four parameters (interval, timeout, start-period, retries)
- `PYTHONUNBUFFERED=1` ensures logs appear immediately in container stdout (critical for log aggregation)

---

## CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - run: pip install flake8 black isort
      - run: black --check .
      - run: isort --check .
      - run: flake8 .

  build:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v2
      - uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  test:
    needs: build
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: python manage.py migrate --no-input
      - run: python manage.py test
      - run: coverage run --source='.' manage.py test && coverage report

  security:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
      - uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: trivy-results.sarif

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          mkdir -p ~/.ssh
          echo "$DEPLOY_KEY" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan -H ${{ secrets.PROD_HOST }} >> ~/.ssh/known_hosts
          ssh app@${{ secrets.PROD_HOST }} \
            "cd /opt/pallettrack && \
             /opt/pallettrack/deploy.sh ghcr.io/${{ github.repository }}:${{ github.sha }}"
```

**Stage breakdown:**
- `lint` (flake8, black, isort) — catches style/import issues early
- `build` (Docker, pushed to GHCR) — gates on lint passing
- `test` (Django tests + coverage, real Postgres service) — gates on build
- `security` (Trivy container scan) — runs in parallel with test
- `deploy` (blue/green swap) — gates on test AND security; only runs on main

---

## Cattle, Not Pets

**Principle:** Treat every container as disposable and reproducible. The source of truth is the image, not the running container. If a container has a problem, you don't SSH in and patch it — you rebuild the image from source, push a new version, and redeploy.

**Implications:**
- No manual state mutation inside running containers (no `docker exec app apt-get install`; add to Dockerfile)
- No hand-curated `nginx.conf` files on the server; version them in Git
- No "this box is special" configuration; everything in code or environment variables
- Container crashes or stops? Docker automatically starts a new one; the state is already back from the image
- Server dies? Redeploy the same image to a new server; you get identical behaviour

**For PalletTrack:** If a library needs an update, or a config bug is found, the path is: fix the Dockerfile or config, push a new image, trigger the deploy pipeline. Never `docker exec` into production to apply a hotfix.

---

## Zero-Downtime Deployment: Blue/Green

**Mechanism:** Two complete application stacks (blue and green) run on the same server, behind a single Nginx reverse proxy. Traffic points to one colour (blue). When you deploy, bring up the new version on the other colour (green), run migrations, health-check it, then flip Nginx upstream in one atomic swap.

**Why blue/green for PalletTrack (twice-weekly cadence):**
- **Rolling updates** (gradual instance replacement) are operationally heavier: requires orchestration (K8s, Nomad, or custom logic), state awareness, and careful monitoring. Overkill for twice-weekly.
- **Canary deployments** (route 5% to new version, monitor, then ramp) add observability complexity and delayed rollback. Again, overkill.
- **Blue/green** is simple: entire old version stays live until the new version is tested. Rollback is instant (flip Nginx upstream back). No partial deployment states. Clear decision boundary: "is the new version healthy?" If yes, swap. If no, discard and keep blue.

For a twice-weekly schedule, simple and clear beats optimized. Blue/green gives you that.

---

## Rollback Plan

**Scenario:** Deploy goes live, but a bug is discovered in the new version. Rollback in <30 seconds.

```bash
# On production server, as root or via sudo:

# 1. Check current active colour
cat /etc/nginx/conf.d/active-upstream.conf
# Output: "upstream backend { server localhost:8001; }"  (green is active)

# 2. Rollback: revert Nginx config to point to the previous colour (blue)
sudo cp /etc/nginx/conf.d/upstream-blue.conf /etc/nginx/conf.d/active-upstream.conf

# 3. Validate the config
sudo nginx -t
# Output: "nginx: the configuration file /etc/nginx/nginx.conf syntax is ok"

# 4. Reload Nginx (zero downtime, existing connections drain)
sudo nginx -s reload

# 5. Verify the rollback
sleep 5
curl -fsS https://pallettrack.app/healthz
# Output: "ok" (if blue is healthy, it will be; the previous deploy was working)

# 6. Alert the team
# (Send notification to #alerts Slack channel with timestamp and reason)
```

**Time budget:** ~30 seconds end-to-end (config copy, validation, reload, verification).

**Key property:** Because blue is still running from the previous successful deploy, rollback is as safe as the last working version. No data loss (both versions share the same database). No state corruption (containers are stateless).

---

## Django Migrations

**When migrations run:** Separate `migrate` step BEFORE the new colour goes live. Flow:

1. New colour (green) starts with the old code
2. Run `python manage.py migrate` on the new version's database connection
3. Wait for health check to pass
4. Flip Nginx upstream to green
5. Blue continues serving (during migration window) until swap happens

**Forward/backward compatibility:** During the 5-10 minute window between deploy and swap:
- Old code (blue) and new code (green) may both run against the database
- New migrations must be **additive only**: add nullable columns, add new tables, add indexes — operations that don't break old code
- Remove old columns in a follow-up release (one-release lag)
- **Never** do `ALTER TABLE ... DROP COLUMN` or `ALTER ... NOT NULL` in the same release as code changes that use the new schema

**If migration fails:**
```bash
# Migration error detected during green startup
# → auto-abort the deploy step (CI catches the error)
# → keep blue active (it's still healthy)
# → alert team with the migration error

# Developer fixes migration, commits, reruns pipeline
```

**Celery task compatibility:** Ensure tasks serialized on blue can be deserialized on green (queue may have old-version tasks). Use job versioning or a compat layer if schema changes affect task payloads.

---

## Celery Worker Deployment

**Separate services:** In `docker-compose.prod.yml`, define three services:

```yaml
version: "3.9"
services:
  web-blue:
    image: ghcr.io/yourorg/pallettrack:${IMAGE_TAG}
    ports:
      - "8000:8000"
    env_file: .env.production
    environment:
      - DJANGO_SETTINGS_MODULE=pallettrack.settings.production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 30s
      timeout: 5s
      retries: 3

  worker-blue:
    image: ghcr.io/yourorg/pallettrack:${IMAGE_TAG}
    env_file: .env.production
    environment:
      - DJANGO_SETTINGS_MODULE=pallettrack.settings.production
    command: >
      celery -A pallettrack worker
      --loglevel=info
      --soft-time-limit=30
      --time-limit=60
      --concurrency=4
    depends_on:
      - redis
    healthcheck:
      test: ["CMD", "celery", "-A", "pallettrack", "inspect", "ping"]
      interval: 30s
      timeout: 5s
      retries: 3

  beat-blue:
    image: ghcr.io/yourorg/pallettrack:${IMAGE_TAG}
    env_file: .env.production
    environment:
      - DJANGO_SETTINGS_MODULE=pallettrack.settings.production
    command: >
      celery -A pallettrack beat
      --loglevel=info
      --scheduler django_celery_beat.schedulers:DatabaseScheduler
    depends_on:
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5555/flower || exit 1"]
      interval: 60s
      timeout: 5s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

**Graceful shutdown:**
- `--soft-time-limit=30`: worker finishes current task (hard cutoff at 30s)
- `--time-limit=60`: if still running after 30s, kill the worker (safety cutoff at 60s)
- Docker's `stop_grace_period: 60s` gives the container time to shut down cleanly before SIGKILL

**Beat (scheduler):** Single replica. Lock coordination via Redis or Django ORM prevents duplicate scheduled tasks if beat restarts.

**Deploy sequence:** Stop old workers, start new workers. In-flight tasks finish (or timeout), new tasks queue on new workers. No data loss.

---

## 🛑 Decision Required Before Proceeding

Before I finalise the deployment architecture, you need to decide on infrastructure and registry:

| Decision | Option A | Option B | Option C |
|---|---|---|---|
| **Container Registry** | GHCR (free for public, ~$0.25/GB/mo private) | Docker Hub (free tier limited to public) | ECR (~$0.10/GB/mo, AWS lock-in) |
| **Hosting** | Bare-metal + docker-compose (~$0 added cost) | Fly.io (~$50–150/mo, managed, global) | ECS Fargate (~$80–200/mo, AWS) |

**Recommendation:** GHCR + bare-metal docker-compose initially. You already have GitHub, GHCR is included, and your single Ubuntu server can run docker-compose without additional infrastructure. No new vendor lock-in. Revisit if you scale beyond one server.

**What do you choose?** Confirm the registry and hosting approach, or escalate if the options need adjustment before I write the deployment script.

---

## Environment Configuration & Secrets

**Never bake secrets into the image.** Use one of these approaches:

**Option 1: `.env.production` file (simplest for single server)**
```bash
# .env.production (gitignored, created on server by ops)
DATABASE_URL=postgresql://user:pass@neon.endpoint/dbname
CELERY_BROKER_URL=redis://localhost:6379/0
SECRET_KEY=<django-generated-key>
DEBUG=False
ALLOWED_HOSTS=pallettrack.app,www.pallettrack.app
```

Then in `docker-compose.prod.yml`:
```yaml
services:
  web:
    env_file: .env.production
```

**Option 2: Systemd environment (if not using docker-compose)**
```ini
# /etc/systemd/system/pallettrack.service
[Service]
EnvironmentFile=/opt/pallettrack/.env.production
ExecStart=/usr/bin/docker run ...
```

**Option 3: 1Password CLI or Doppler (if scaling to multiple servers)**
```bash
# At deploy time, fetch secrets from 1Password/Doppler
op run --env-file=/dev/stdout -- docker-compose up
```

**Never:**
- Commit `.env.production` to Git
- Bake `DATABASE_URL` into the Dockerfile
- Export secrets in the image layer

**For Neon credentials:** Store connection string in `.env.production` only. Docker will inject it into the container at runtime.

---

## Observability

Moving from a single bare-metal server to containerized deployment changes how you see what's happening. Logs are now ephemeral (container stops → logs gone unless forwarded). You need:

### Health Endpoints

Add to `pallettrack/urls.py`:
```python
from django.http import JsonResponse

def healthz(request):
    """Readiness check — is the app ready to serve traffic?"""
    try:
        from django.db import connection
        connection.ensure_connection()  # Quick DB connectivity check
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"status": "error", "reason": str(e)}, status=503)

def readyz(request):
    """Liveness check — is the app still alive and responsive?"""
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("healthz", healthz),
    path("readyz", readyz),
    # ... rest of your URLs
]
```

Nginx blue/green checks `/healthz` before flipping traffic. Container orchestration (if you add K8s later) uses `/readyz` to decide restart policy.

### Log Aggregation

Container stdout/stderr are ephemeral. Forward them:

**Option 1: Journald (simplest, single server)**
```bash
# Docker logs automatically go to systemd journal
docker run --log-driver=journald ...
# Query: journalctl -u pallettrack-web -f
```

**Option 2: Loki (if scaling)**
```yaml
# docker-compose.prod.yml
services:
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - loki-data:/loki
  
  web:
    logging:
      driver: loki
      options:
        loki-url: "http://localhost:3100/loki/api/v1/push"
        loki-external-labels: "job=pallettrack,env=prod"
```

**Option 3: CloudWatch / Datadog (managed)**
```yaml
web:
  logging:
    driver: awslogs
    options:
      awslogs-group: /pallettrack/web
      awslogs-region: us-east-1
```

### Metrics

Add Prometheus exporter:
```bash
pip install django-prometheus
```

```python
# settings.py
INSTALLED_APPS = [
    "django_prometheus",
    # ... your apps
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    # ... your middleware
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]
```

Expose on `/metrics`:
```python
# urls.py
from django_prometheus.views import ExportToDjangoView
urlpatterns = [
    path("metrics", ExportToDjangoView.as_view()),
    # ...
]
```

Nginx scrapes `http://localhost:8000/metrics` every 30s.

### Uptime Checks

Set up external monitoring (Uptime Robot, StatusCake, or your own):
```bash
# Every 60s, hit the health endpoint from outside your network
curl -f https://pallettrack.app/healthz
# If it fails 3 times in a row, alert #oncall
```

### The Mental Model Shift

**Before (single server):**
```
SSH into server → tail /var/log/pallettrack.log → see recent events
```

**After (containers):**
```
Container stops → logs are lost (unless forwarded)
Need: structured logging (JSON to stdout) → log aggregator → search/view in UI
```

**Action now:** Configure one of the three log options above. Test it by deploying green, watching logs appear in your aggregator, then rolling back.

---

**Next step:** Confirm the infrastructure decision (GHCR + bare-metal, or an alternative), and I'll provide the deployment script, docker-compose.prod.yml, and Nginx blue/green configuration.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/16.0 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 58870 ms |
| Target cost | $0.0856 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent checks for existing IaC (Pulumi.yaml, .tf files), existing CI workflows, and existing Dockerfiles before proposing anything new | PASS | Reconnaissance section explicitly shows three commands: `find . \( -name "Pulumi.yaml" -o -name "*.tf" -o -name "*.hcl" \)`, `ls .github/workflows/`, and `ls Dockerfile docker-compose.yml`, all returning no results. Reports: 'Greenfield — no existing IaC, CI workflows, or Dockerfiles. Building from scratch.' |
| c2 | Agent produces a Dockerfile that uses multi-stage builds, a non-root user, pinned base image versions, and a HEALTHCHECK instruction | PASS | Dockerfile shows `FROM python:3.12-slim AS builder` and `FROM python:3.12-slim AS runtime` (multi-stage, pinned), `RUN useradd ... app` + `USER app` (non-root before COPY), and `HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3` with all four parameters. |
| c3 | Agent defines a CI/CD pipeline with stages in the correct order: lint → build → test → security scan → deploy | PASS | GitHub Actions workflow defines jobs: `lint` → `build` (needs: lint) → `test` (needs: build) and `security` (needs: build, parallel with test) → `deploy` (needs: [test, security]). All five required stages present; deploy gates on both test and security. |
| c4 | Agent addresses zero-downtime deployments explicitly — describes a mechanism (blue/green, rolling update, or health-check-gated) with reasoning | PASS | Dedicated section 'Zero-Downtime Deployment: Blue/Green' names the mechanism, explains the upstream-swap mechanics, and explicitly compares rolling updates ('Overkill for twice-weekly') and canary ('Again, overkill') before concluding 'Blue/green gives you that.' |
| c5 | Agent defines a rollback plan with specific commands or steps, not just "roll back the deployment" | PASS | Rollback Plan section provides numbered bash commands: `sudo cp /etc/nginx/conf.d/upstream-blue.conf /etc/nginx/conf.d/active-upstream.conf`, `sudo nginx -t && sudo nginx -s reload`, and `curl -fsS https://pallettrack.app/healthz`, with stated time budget of '~30 seconds end-to-end.' |
| c6 | Agent stops and asks before recommending new cloud resources with ongoing cost (as required by the decision checkpoints) | PASS | '🛑 Decision Required Before Proceeding' section presents a table with registry options (GHCR ~$0.25/GB/mo, Docker Hub, ECR ~$0.10/GB/mo) and hosting options (bare-metal ~$0 added, Fly.io ~$50–150/mo, ECS Fargate ~$80–200/mo), makes a recommendation, then asks 'What do you choose? Confirm … before I finalise.' |
| c7 | Agent addresses the Celery worker migration alongside the web server — not just the Django app in isolation | PARTIAL | Dedicated 'Celery Worker Deployment' section includes separate docker-compose services (`worker-blue`, `beat-blue`), specifies `--soft-time-limit=30 --time-limit=60`, notes `stop_grace_period: 60s`, and describes deploy sequence ('Stop old workers, start new workers'). Ceiling is PARTIAL per criterion prefix. |
| c8 | Agent references the cattle-not-pets principle and ensures the deployment design treats containers as disposable/reproducible | PASS | Dedicated 'Cattle, Not Pets' section states: 'Treat every container as disposable and reproducible. The source of truth is the image, not the running container.' Includes PalletTrack-specific example: 'Never `docker exec` into production to apply a hotfix.' |
| c9 | Output's Dockerfile (or container build description) is a multi-stage build with a non-root user, a pinned base image version (e.g. `python:3.12-slim` not `python:latest`), and an explicit HEALTHCHECK | PASS | Same Dockerfile: `FROM python:3.12-slim AS builder` / `FROM python:3.12-slim AS runtime` (pinned, multi-stage), `USER app` after `useradd`, `HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3` with `CMD curl -f http://localhost:8000/healthz \|\| exit 1`. |
| c10 | Output addresses the two distinct workloads — the Django web app and the Celery workers — as separate container images or processes, not bundled into one image | PASS | docker-compose.prod.yml defines three separate services: `web-blue` (gunicorn), `worker-blue` (celery worker with separate command), and `beat-blue` (celery beat with separate command). All use the same base image but run as distinct processes. |
| c11 | Output's CI/CD pipeline orders stages as lint → build → test → security scan → deploy, with each stage gating the next, and names the tool (GitHub Actions / GitLab CI / Jenkins) consistent with the project conventions | PASS | GitHub Actions (matching tooling register) workflow named `.github/workflows/deploy.yml`. All five required stages present with proper `needs:` dependencies. Stage breakdown comment confirms: 'deploy — gates on test AND security; only runs on main.' |
| c12 | Output's zero-downtime mechanism is named explicitly (rolling update, blue/green, or canary) with reasoning for the choice given the twice-weekly deploy cadence — not just "we'll do zero-downtime" | PASS | 'Why blue/green for PalletTrack (twice-weekly cadence)' subsection explicitly names blue/green and explains: 'Rolling updates... Overkill for twice-weekly. Canary deployments... Overkill. For a twice-weekly schedule, simple and clear beats optimized.' |
| c13 | Output's rollback plan includes specific commands or steps (kubectl rollout undo, fly deploy --image previous_tag, swap traffic back to old colour) with a stated time budget — not "redeploy the previous version" | PASS | Five numbered bash commands shown (check active colour, cp config, nginx -t, nginx -s reload, curl healthz), and explicitly states 'Time budget: ~30 seconds end-to-end (config copy, validation, reload, verification).' |
| c14 | Output addresses Django migrations explicitly — when migrations run in the deployment, how forward/backward compatibility is preserved across the rolling update, and what happens if a migration fails | PASS | 'Django Migrations' section covers: timing ('separate `migrate` step BEFORE the new colour goes live'), additive-only schema changes ('add nullable columns... Remove old columns in a follow-up release'), and failure path ('auto-abort the deploy step... keep blue active... alert team'). |
| c15 | Output stops and asks before recommending new infrastructure with ongoing cost (e.g. Kubernetes cluster, container registry, managed Redis for Celery broker), framing the cost trade-offs | PASS | Decision checkpoint presents cost table for registry (GHCR, Docker Hub, ECR with per-GB costs) and hosting (bare-metal $0 added, Fly.io $50–150/mo, ECS Fargate $80–200/mo). Ends with 'Confirm the registry and hosting approach, or escalate if the options need adjustment before I finalise.' |
| c16 | Output addresses environment configuration — secrets handling (not baked into the image), env var injection at runtime, and how Neon Postgres credentials reach the container without ending up in a layer | PASS | 'Environment Configuration & Secrets' section opens with 'Never bake secrets into the image', shows three options (env_file pointing to gitignored .env.production, systemd EnvironmentFile, Doppler/1Password CLI), and explicitly states 'For Neon credentials: Store connection string in `.env.production` only. Docker will inject it into the container at runtime.' |
| c17 | Output addresses observability for the new deployment — health endpoints, log aggregation, metrics — given the move from a single bare-metal server with familiar logs to ephemeral containers | PARTIAL | Comprehensive 'Observability' section covers: `/healthz` and `/readyz` endpoints with code, log aggregation (journald, Loki, CloudWatch), metrics via `django-prometheus` on `/metrics`, uptime checks, and an explicit 'Mental Model Shift' subsection contrasting 'SSH into server → tail log' with 'Container stops → logs are lost (unless forwarded)'. Ceiling is PARTIAL per criterion prefix. |

### Notes

The captured output is a near-perfect match against the test requirements. All 17 criteria are addressed with specific, actionable content. The reconnaissance section is present and correctly formatted. The Dockerfile includes all four required attributes. The GitHub Actions pipeline covers all five stages with proper gating (security and test run in parallel, which is a pragmatic optimisation that still gates deploy on both). Blue/green is named, justified against twice-weekly cadence, and compared against alternatives. The rollback plan has concrete bash commands and a sub-30-second time budget. The Decision Checkpoint stops and presents cost trade-offs before recommending GHCR + bare-metal. Django migrations, Celery worker handling, secrets management, and observability are all addressed substantively. The two PARTIAL criteria (c7, c17) hit their ceilings and are both scored at 0.5. No criteria failed.
