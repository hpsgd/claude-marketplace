# Write dockerfile skill structure

Checking that the write-dockerfile skill enforces multi-stage builds, non-root user, pinned base images, HEALTHCHECK, and a .dockerignore — and rejects common anti-patterns like running as root or using latest tags.

## Prompt

> Review the write-dockerfile skill definition and verify it produces production-hardened Dockerfiles rather than minimal single-stage examples.

Given the prompt "write a Dockerfile for a FastAPI Python service", the skill would run Step 1 reconnaissance (identify stack, check for existing Dockerfiles), then produce a two-stage Dockerfile using `python:3.13-slim` for both stages, with dependency installation isolated to the build stage, a non-root system user created before any application files are copied, a HEALTHCHECK with all four parameters, and an accompanying `.dockerignore`. The Python example in Step 8 maps directly to this scenario.

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8/8 criteria met (100%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill requires multi-stage builds — Step 2 "Multi-Stage Build Architecture": "Every Dockerfile uses multi-stage builds." Rules explicitly state: "Build tools, dev dependencies, and source code NEVER appear in the runtime stage."

- [x] PASS: Skill mandates layer caching — Step 3 "Layer Caching Optimisation" provides explicit ordering with dependency lockfile copy before source. Rules: "COPY dependency manifest files (lockfile) BEFORE copying source code" and "Never `COPY . .` before installing dependencies — it invalidates the cache on every source change."

- [x] PASS: Skill provides base image table for all five stacks with pinned versions — Step 4 table covers Node.js (`node:22-alpine`), .NET (`mcr.microsoft.com/dotnet/sdk:9.0` / `mcr.microsoft.com/dotnet/aspnet:9.0-alpine`), Python (`python:3.13-slim`), Go (`golang:1.23-alpine`), Rust (`rust:1.80-slim`). Rule: "NEVER use `latest` tag."

- [x] PASS: Skill requires non-root user marked MANDATORY — Step 5 heading: "Security Hardening (MANDATORY)". The security checklist row for "Non-root user" is marked MANDATORY. The example creates the user with `addgroup`/`adduser` and switches with `USER appuser` before the `COPY --from=build` instruction.

- [x] PASS: Skill requires HEALTHCHECK with all four parameters — Step 6 shows `HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3`. Rule: "Every Dockerfile includes a HEALTHCHECK instruction."

- [x] PASS: Skill requires .dockerignore marked mandatory with required exclusions — Step 7 heading: ".dockerignore (MANDATORY)". Rule: "`.dockerignore` MUST exist." Exclusions listed include `.git`, `node_modules`, `.env`, `.env.*`, `tests`, `test`, `__tests__`.

- [x] PASS: Skill provides stack-specific patterns with complete working examples — Step 8 contains complete Dockerfiles for Node.js, .NET, and Python. Each is multi-stage with non-root user and HEALTHCHECK, not a skeleton.

- [x] PASS: Skill lists all five required anti-patterns — Anti-Patterns section: "Single-stage build", "Running as root", "`latest` tag", "Secrets in build args or ENV", "No health check" — all five present by name.

## Notes

The skill is complete against all criteria. The non-root user example in Step 5 shows the user being created with explicit GID/UID (1001) and the COPY using `--chown=appuser:appgroup`, which is the correct sequence. The security checklist distinguishes MANDATORY from RECOMMENDED controls — a useful signal for users prioritising hardening work.
