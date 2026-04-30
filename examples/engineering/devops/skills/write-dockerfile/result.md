# Result: write-dockerfile skill structure

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

*Simulated verification report — what a developer reviewing this skill against production-hardening requirements would produce.*

---

### write-dockerfile skill: production-hardening verification

Reviewing `plugins/engineering/devops/skills/write-dockerfile/SKILL.md` against eight production-hardening requirements.

---

**Requirement 1 — Multi-stage builds**

Step 2 states explicitly: "Every Dockerfile uses multi-stage builds. Minimum two stages, often three." The rule block reads: "Build tools, dev dependencies, and source code NEVER appear in the runtime stage." Stage naming convention (`deps`, `build`, `runtime`, `test`) is specified. The introductory three-stage Node.js example demonstrates the pattern: deps stage installs, build stage compiles, runtime stage receives only artifacts.

Verdict: MET.

---

**Requirement 2 — Layer caching optimisation**

Step 3 defines an explicit five-position layer order with the instruction "COPY dependency manifest files (lockfile) BEFORE copying source code" and the prohibition "Never `COPY . .` before installing dependencies — it invalidates the cache on every source change." The ordered list makes the cache rationale explicit: base image and system packages change rarely; lockfile changes only when dependencies change; source code changes every build.

Verdict: MET.

---

**Requirement 3 — Pinned base image table (Node.js, .NET, Python, Go, Rust)**

Step 4 provides a two-column table (build stage / runtime stage) for all five stacks:

| Stack | Build stage | Runtime stage |
|---|---|---|
| Node.js | `node:22-alpine` | `node:22-alpine` or `gcr.io/distroless/nodejs22` |
| .NET | `mcr.microsoft.com/dotnet/sdk:9.0` | `mcr.microsoft.com/dotnet/aspnet:9.0-alpine` |
| Python | `python:3.13-slim` | `python:3.13-slim` or `gcr.io/distroless/python3` |
| Go | `golang:1.23-alpine` | `gcr.io/distroless/static-debian12` |
| Rust | `rust:1.80-slim` | `gcr.io/distroless/cc-debian12` or `scratch` |

All versions are pinned (22, 9.0, 3.13, 1.23, 1.80). Rule: "NEVER use `latest` tag — pin to a specific version." Digest pinning is mentioned as a production option.

Verdict: MET.

---

**Requirement 4 — Non-root user, MANDATORY, USER before COPY**

Step 5 is titled "Security Hardening (MANDATORY)". The security checklist table lists Non-root user with status MANDATORY. The code example in Step 5 shows:

```dockerfile
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

# Switch to non-root user BEFORE copying application files
USER appuser

# Copy application files (owned by non-root user)
COPY --from=build --chown=appuser:appgroup /app/dist ./dist
```

The comment "BEFORE copying application files" is explicit. The rule block adds: "NEVER run as root in production."

Note: the Python example in Step 8 places `USER app` after the `COPY` of application files, contradicting this rule. The Node.js and .NET examples handle the order correctly.

Verdict: MET (rule and mandate are present; Step 8 Python is inconsistent — noted in Notes).

---

**Requirement 5 — HEALTHCHECK with all four parameters**

Step 6 shows:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8080/health"] \
  || exit 1
```

All four parameters present: `--interval`, `--timeout`, `--start-period`, `--retries`. Rule: "Every Dockerfile includes a HEALTHCHECK instruction." A distroless variant (no wget) uses a compiled binary healthcheck endpoint. All three stack-specific examples in Step 8 include HEALTHCHECK with all four parameters.

Verdict: MET.

---

**Requirement 6 — .dockerignore, MANDATORY, required exclusions**

Step 7 is titled ".dockerignore (MANDATORY)". Rule: "`.dockerignore` MUST exist — without it, `COPY . .` sends everything to the daemon (including `.git`, `node_modules`, secrets)." The template explicitly includes:

- `.git` — version control
- `node_modules` — dependencies installed in container
- `.env` / `.env.*` — environment and secrets
- `tests`, `test`, `__tests__`, `*.test.ts`, `*.spec.ts`, `coverage` — test files

All four required exclusion categories are present.

Verdict: MET.

---

**Requirement 7 — Stack-specific examples (Node.js, .NET, Python)**

Step 8 contains three complete Dockerfiles:

- **Node.js**: deps → build (with `npm prune --production`) → runtime. Includes ENV, USER before COPY (with `--chown`), EXPOSE, HEALTHCHECK, CMD.
- **.NET**: build → runtime. Includes USER, COPY with `--chown`, ENV for ASPNETCORE_URLS, EXPOSE, HEALTHCHECK, ENTRYPOINT.
- **Python**: build → runtime. Includes groupadd/useradd, COPY of installed packages and source, USER, EXPOSE, HEALTHCHECK, CMD.

Each is a self-contained working Dockerfile, not a stripped template.

Verdict: MET.

---

**Requirement 8 — Anti-patterns list**

The Anti-Patterns section explicitly names:

- Single-stage build
- `COPY . .` before dependency install
- Running as root
- `latest` tag
- Secrets in build args or ENV
- Installing unnecessary packages
- No `.dockerignore`
- No health check
- `npm install` instead of `npm ci`

All five required anti-patterns (single-stage build, running as root, latest tag, secrets in build args, no health check) are present. The list exceeds the minimum with four additional items.

Verdict: MET.

---

### Summary

All eight production-hardening requirements are satisfied by the skill definition. The skill is structured as a sequential process with explicit rules, mandatory markers, and complete stack-specific examples that would produce consistent output without cross-referencing.

---

## Criteria

- [x] PASS: Skill requires multi-stage builds — Step 2 states "Every Dockerfile uses multi-stage builds" with rule: "Build tools, dev dependencies, and source code NEVER appear in the runtime stage." Met.
- [x] PASS: Skill mandates layer caching optimisation — Step 3 defines explicit layer order, "COPY dependency manifest files (lockfile) BEFORE copying source code," and "Never `COPY . .` before installing dependencies." Met.
- [x] PASS: Skill provides a base image selection table covering Node.js, .NET, Python, Go, and Rust with specific pinned versions — Step 4 table lists all five with pinned versions. No `latest` tags. Met.
- [x] PASS: Skill requires a non-root user created and switched to before copying application files, marked MANDATORY — Step 5 security checklist marks Non-root user MANDATORY; code example shows `USER appuser` before `COPY`. Met.
- [x] PASS: Skill requires a HEALTHCHECK instruction in every Dockerfile with all four parameters — Step 6 shows `--interval=30s --timeout=5s --start-period=10s --retries=3` and states "Every Dockerfile includes a HEALTHCHECK instruction." Met.
- [x] PASS: Skill requires a .dockerignore file and states it is mandatory — Step 7 titled ".dockerignore (MANDATORY)"; template includes `.git`, `node_modules`, `.env`, `.env.*`, and test directories. Met.
- [x] PASS: Skill provides stack-specific patterns for Node.js, .NET, and Python with complete working examples — Step 8 has three full Dockerfiles each covering base image through CMD/ENTRYPOINT with security hardening and HEALTHCHECK. Met.
- [x] PASS: Skill lists anti-patterns including single-stage build, running as root, latest tag, secrets in build args, and no health check — all five present in the Anti-Patterns section. Met.

## Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample Dockerfile. The simulated output above evaluates the skill definition against each criterion. Met.
- [x] PASS: Output verifies the multi-stage build rule and explicitly checks that build tools and dev dependencies cannot leak into the runtime stage — Step 2 rule confirmed and quoted. Met.
- [x] PASS: Output verifies the layer-cache optimisation rule — dependency manifests copied and installed before source code — Step 3 confirmed with ordered list and prohibition quoted. Met.
- [x] PASS: Output confirms the base image table covers Node.js, .NET, Python, Go, and Rust with specific pinned versions — Step 4 table reproduced; no floating or `latest` tags. Met.
- [x] PASS: Output verifies the non-root user requirement is marked MANDATORY and that the USER directive is set before COPY of application files — Step 5 checklist and code example both confirmed; Python inconsistency flagged. Met.
- [x] PASS: Output confirms HEALTHCHECK is required in every Dockerfile with all four parameters — Step 6 confirmed with all four flags quoted; Step 8 examples each include HEALTHCHECK. Met.
- [x] PASS: Output confirms .dockerignore is mandatory and lists the required exclusions explicitly — Step 7 confirmed; all four exclusion categories present in the template. Met.
- [x] PASS: Output verifies stack-specific complete examples exist for Node.js, .NET, and Python — Step 8 confirmed with three self-contained Dockerfiles. Met.
- [x] PASS: Output confirms the anti-pattern list names single-stage build, running as root, latest tag, secrets in build args, and no health check — Anti-Patterns section confirmed. Met.
- [~] PARTIAL: Output identifies genuine gaps — the skill has no SBOM/provenance guidance (`docker buildx build --sbom` or `--provenance`), no multi-architecture build instructions (`buildx --platform linux/amd64,linux/arm64`), and no explicit decision guide for minimising final image size beyond base image selection (distroless appears in the table but no alpine vs distroless trade-off with size targets). Partially met: gaps present and identified.

## Notes

The skill is thorough and well-structured. All eight structural criteria pass cleanly. The Step 8 examples are complete working Dockerfiles rather than stripped templates — each includes multi-stage build, non-root user setup, and HEALTHCHECK inline, meaning an agent following the skill would produce consistent output without needing to cross-reference other sections.

Two internal inconsistencies worth flagging for a skill author:

**Step 2 copies `node_modules` wholesale.** The introductory example in Step 2 copies `node_modules` from the build stage directly into runtime without pruning dev dependencies. The Step 8 Node.js example corrects this with `npm prune --production`, but a reader or agent consuming only Step 2 would miss the pruning step and carry dev dependencies into the production image — exactly the anti-pattern the skill is meant to prevent.

**Step 8 Python places `USER app` after `COPY`.** The Step 5 MANDATORY rule reads "Switch to non-root user BEFORE copying application files" with an inline comment to that effect. The Python example in Step 8 places `USER app` after `COPY --from=build --chown=app:app /app .`. The `--chown` flag means files are owned by the app user, which softens the security impact, but the sequence contradicts the stated rule. The Node.js and .NET examples handle the order correctly.

Neither issue fails the rubric — the rules and mandatory markers are clearly stated — but both are the kind of subtle inconsistency an agent might follow in preference to the stated rule.

The genuine coverage gaps are: SBOM and provenance attestation (`docker buildx build --sbom --provenance`), multi-architecture build instructions (`buildx --platform linux/amd64,linux/arm64`), and a structured decision guide for the distroless vs alpine trade-off (attack surface, tooling availability, debugging constraints, image size targets). These matter for production hardening at scale and are absent from the skill.
