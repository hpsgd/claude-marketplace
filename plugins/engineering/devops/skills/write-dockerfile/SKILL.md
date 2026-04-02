---
name: write-dockerfile
description: Write a Dockerfile for a service — multi-stage build, minimal image, security hardening.
argument-hint: "[service or application to containerise]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a Dockerfile for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Reconnaissance

Before writing the Dockerfile:

1. **Identify the stack** — language, framework, build tool, runtime requirements
2. **Check existing Dockerfiles** — look for `Dockerfile`, `Dockerfile.*`, `docker-compose.yml`
3. **Identify the build output** — compiled binary, bundled JS, Python wheel, .NET DLL
4. **Identify runtime dependencies** — system packages, native libraries, certificates
5. **Check the entry point** — what command starts the application?

### Step 2: Multi-Stage Build Architecture

Every Dockerfile uses multi-stage builds. Minimum two stages, often three:

```dockerfile
# Stage 1: Dependencies (cached layer — changes only when lockfile changes)
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production=false

# Stage 2: Build (changes when source changes)
FROM deps AS build
COPY . .
RUN npm run build

# Stage 3: Runtime (minimal — only production artifacts)
FROM node:22-alpine AS runtime
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./
```

**Rules:**
- Build tools, dev dependencies, and source code NEVER appear in the runtime stage
- Each stage has a descriptive name (`deps`, `build`, `runtime`, `test`)
- The runtime stage starts from a minimal base image

### Step 3: Layer Caching Optimisation

Layer order matters. Layers that change less frequently go first:

```
1. Base image (changes: rarely)
2. System package installation (changes: rarely)
3. Dependency lockfile copy + install (changes: when deps change)
4. Source code copy (changes: every build)
5. Build command (changes: every build)
```

**Rules:**
- COPY dependency manifest files (lockfile) BEFORE copying source code
- Install dependencies in a separate layer from source copy
- Use `npm ci` (not `npm install`) for reproducible installs
- Group `RUN` commands with `&&` to reduce layers, but keep logical separation for cache efficiency
- Never `COPY . .` before installing dependencies — it invalidates the cache on every source change

### Step 4: Base Image Selection

| Stack | Build stage | Runtime stage |
|---|---|---|
| Node.js | `node:22-alpine` | `node:22-alpine` or `gcr.io/distroless/nodejs22` |
| .NET | `mcr.microsoft.com/dotnet/sdk:9.0` | `mcr.microsoft.com/dotnet/aspnet:9.0-alpine` |
| Python | `python:3.13-slim` | `python:3.13-slim` or `gcr.io/distroless/python3` |
| Go | `golang:1.23-alpine` | `gcr.io/distroless/static-debian12` (scratch for CGO_ENABLED=0) |
| Rust | `rust:1.80-slim` | `gcr.io/distroless/cc-debian12` or `scratch` |

**Rules:**
- NEVER use `latest` tag — pin to a specific version
- Prefer `-alpine` variants for smaller images (unless native deps require glibc)
- Consider `distroless` for production — no shell, no package manager, smaller attack surface
- Pin base images by digest for reproducibility in production: `node:22-alpine@sha256:abc123...`
- Same base image version in build and runtime stages to avoid glibc mismatch

### Step 5: Security Hardening (MANDATORY)

```dockerfile
# Create non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

# Switch to non-root user BEFORE copying application files
USER appuser

# Copy application files (owned by non-root user)
COPY --from=build --chown=appuser:appgroup /app/dist ./dist
```

**Security checklist:**

| Control | Implementation | Required |
|---|---|---|
| Non-root user | `USER appuser` | MANDATORY |
| No secrets in image | Use runtime env vars or mounted secrets | MANDATORY |
| Read-only filesystem | `--read-only` flag at runtime | RECOMMENDED |
| Drop capabilities | `--cap-drop=ALL` at runtime | RECOMMENDED |
| No shell (distroless) | Use distroless base | RECOMMENDED |
| Minimal packages | No curl, wget, bash in production | RECOMMENDED |
| CVE scanning | `trivy image` or `docker scout` | MANDATORY |

**Rules:**
- NEVER put secrets (API keys, passwords, tokens) in the Dockerfile, build args, or image layers
- NEVER use `--privileged` in runtime
- NEVER run as root in production
- If the app needs to write files, use a specific volume mount — not a writable container filesystem
- Set `ENV NODE_ENV=production` (or equivalent) in the runtime stage

### Step 6: Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8080/health"] \
  || exit 1
```

For distroless images (no shell, no wget):
```dockerfile
# Use the application's built-in health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/app/healthcheck"]
```

**Rules:**
- Every Dockerfile includes a HEALTHCHECK instruction
- Health check endpoint should be lightweight — no database queries, no auth
- `start-period` accounts for application startup time
- `retries=3` before marking unhealthy — avoid flapping

### Step 7: .dockerignore (MANDATORY)

Every Dockerfile is accompanied by a `.dockerignore` file:

```
# Version control
.git
.gitignore

# Dependencies (installed in container)
node_modules
__pycache__
.venv

# Build output (built in container)
dist
build
bin
obj

# Development files
*.md
LICENSE
.editorconfig
.eslintrc*
.prettierrc*
tsconfig*.json
jest.config.*
vitest.config.*

# IDE
.vscode
.idea
*.swp
*.swo

# Environment and secrets
.env
.env.*
*.pem
*.key

# Tests
tests
test
__tests__
*.test.ts
*.spec.ts
coverage

# Docker
Dockerfile*
docker-compose*
.dockerignore

# CI
.github
.gitlab-ci.yml
```

**Rules:**
- `.dockerignore` MUST exist — without it, `COPY . .` sends everything to the daemon (including `.git`, `node_modules`, secrets)
- Test files, documentation, and CI configuration do not belong in production images
- `.env` files are NEVER included in the image

### Step 8: Stack-Specific Patterns

#### Node.js
```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM deps AS build
COPY . .
RUN npm run build
RUN npm prune --production  # Remove dev dependencies

FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 app && adduser --system --uid 1001 --ingroup app app
USER app
COPY --from=build --chown=app:app /app/dist ./dist
COPY --from=build --chown=app:app /app/node_modules ./node_modules
COPY --from=build --chown=app:app /app/package.json ./
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/health"]
CMD ["node", "dist/index.js"]
```

#### .NET
```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src
COPY *.csproj ./
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:9.0-alpine AS runtime
WORKDIR /app
RUN addgroup --system --gid 1001 app && adduser --system --uid 1001 --ingroup app app
USER app
COPY --from=build --chown=app:app /app/publish .
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8080/health"]
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

#### Python
```dockerfile
FROM python:3.13-slim AS build
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
COPY . .

FROM python:3.13-slim AS runtime
WORKDIR /app
RUN groupadd --system --gid 1001 app && useradd --system --uid 1001 --gid app app
COPY --from=build /install /usr/local
COPY --from=build --chown=app:app /app .
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Anti-Patterns (NEVER do these)

- **Single-stage build** — build tools and dev dependencies bloat the runtime image
- **`COPY . .` before dependency install** — invalidates the dependency cache on every source change
- **Running as root** — container compromise = host compromise
- **`latest` tag** — non-reproducible builds. Pin versions
- **Secrets in build args or ENV** — they persist in image layers. Use runtime secrets
- **Installing unnecessary packages** — `apt-get install curl vim wget` in production images
- **No `.dockerignore`** — sending `.git` and `node_modules` to the build context
- **No health check** — orchestrators can't determine container health without it
- **`npm install` instead of `npm ci`** — `npm install` modifies the lockfile and is non-deterministic

## Output

Deliver:
1. `Dockerfile` with multi-stage build, security hardening, and health check
2. `.dockerignore` file
3. Brief explanation of stage strategy and base image choice
4. Any `docker-compose.yml` additions needed for local development
