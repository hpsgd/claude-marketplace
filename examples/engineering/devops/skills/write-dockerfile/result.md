# Write Dockerfile

Scenario: Checking that the write-dockerfile skill enforces multi-stage builds, non-root user, pinned base images, HEALTHCHECK, and a .dockerignore — and rejects common anti-patterns like running as root or using latest tags.

## Prompt

> Review the write-dockerfile skill definition and verify it produces production-hardened Dockerfiles rather than minimal single-stage examples.
> 
> In your verification report, confirm or flag each item by name. Quote the skill text where present:
> 
> - **Multi-stage build requirement** + the layer-caching rule: dependency manifests (`package.json`, `requirements.txt`, `*.csproj`, `go.mod`, `Cargo.toml`) MUST be copied and installed BEFORE source code, to preserve cache on source-only changes.
> - **Base image table** for all 5 stacks (Node.js, .NET, Python, Go, Rust) with **specific pinned versions** (not `:latest`, not floating major). Quote the actual versions from the skill.
> - **Non-root USER directive** marked MANDATORY, with the ordering rule: `USER` must come BEFORE the `COPY` of application files (so source files are owned correctly).
> - **HEALTHCHECK in every Dockerfile** with all FOUR parameters: `--interval`, `--timeout`, `--start-period`, `--retries`.
> - **`.dockerignore` MANDATORY** with required exclusions named: `.git`, `node_modules`, `.env`, `tests/`, `*.md` (and similar build noise).
> - **Anti-patterns list (5)**: (1) single-stage build, (2) running as root, (3) `:latest` tag, (4) secrets in build args (`ARG SECRET=...`), (5) no HEALTHCHECK.
> - **Identified gaps**: explicitly call out `--platform`/`BUILDPLATFORM`/buildx for multi-arch (arm64+amd64), distroless / alpine final-image-size guidance, SBOM/provenance generation.
> 
> Confirm or flag each by name — do not paraphrase.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Verification Report: `write-dockerfile` Skill

**Status: PRODUCTION-READY with minor gaps in multi-arch and provenance guidance**

---

### ✅ Confirmed: Multi-Stage Build & Layer Caching

**Multi-stage architecture:** Step 2 mandates multi-stage builds with explicit rule: "Every Dockerfile uses multi-stage builds. Minimum two stages, often three."

**Dependency-before-source caching rule:** Step 3 explicitly requires this order:
> "COPY dependency manifest files (lockfile) BEFORE copying source code"
> "Never `COPY . .` before installing dependencies — it invalidates the cache on every source change"

All stack-specific examples follow this pattern (deps stage copies `package.json`, `requirements.txt`, `*.csproj` before source).

---

### ✅ Confirmed: Base Image Table with Pinned Versions

**Full 5-stack table in Step 4:**

| Stack | Build | Runtime | Version Status |
|---|---|---|---|
| Node.js | `node:22-alpine` | `node:22-alpine` / `gcr.io/distroless/nodejs22` | ✅ Pinned to major.minor |
| .NET | `mcr.microsoft.com/dotnet/sdk:9.0` | `mcr.microsoft.com/dotnet/aspnet:9.0-alpine` | ✅ Pinned to 9.0 |
| Python | `python:3.13-slim` | `python:3.13-slim` / `gcr.io/distroless/python3` | ⚠️ distroless not pinned |
| Go | `golang:1.23-alpine` | `gcr.io/distroless/static-debian12` (scratch for CGO=0) | ⚠️ distroless not pinned |
| Rust | `rust:1.80-slim` | `gcr.io/distroless/cc-debian12` / `scratch` | ⚠️ distroless not pinned |

**Pinning rules stated:** "NEVER use `latest` tag — pin to a specific version" and "Pin base images by digest for reproducibility in production: `node:22-alpine@sha256:abc123...`"

**Gap:** distroless final-stage images lack digest pinning guidance.

---

### ✅ Confirmed: Non-Root USER Directive with Correct Ordering

**Marked MANDATORY in Step 5 security table:**
> "Non-root user | `USER appuser` | MANDATORY"

**Ordering rule explicitly stated:**
> "Switch to non-root user BEFORE copying application files"

**Example shows correct order:**
```dockerfile
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

USER appuser

COPY --from=build --chown=appuser:appgroup /app/dist ./dist
```

All 5 stack-specific patterns follow this ordering.

---

### ✅ Confirmed: HEALTHCHECK with All Four Parameters

**Step 6 "Health Check" provides the standard:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8080/health"]
```

**All four parameters present in every example:**
- `--interval=30s` ✅
- `--timeout=5s` ✅
- `--start-period=10s` ✅
- `--retries=3` ✅

Distroless variant provided with built-in health binary fallback (no wget). **Every Dockerfile includes a HEALTHCHECK instruction** rule enforced.

---

### ✅ Confirmed: .dockerignore MANDATORY with Required Exclusions

**Step 7 ".dockerignore (MANDATORY)" with comprehensive list:**

Required exclusions present:
- `.git` ✅
- `node_modules` ✅
- `.env` ✅
- `tests` ✅
- `*.md` ✅

**Mandatory rule enforced:**
> ".dockerignore MUST exist — without it, `COPY . .` sends everything to the daemon (including `.git`, `node_modules`, secrets)"

Full list includes 30+ patterns (`.venv`, `__pycache__`, `bin`, `obj`, `dist`, `.vscode`, `.github`, etc.).

---

### ✅ Confirmed: Anti-Patterns List (5 Core + Extended)

**Step 8 "Anti-Patterns (NEVER do these)" explicitly covers:**

1. ✅ **Single-stage build** — "build tools and dev dependencies bloat the runtime image"
2. ✅ **Running as root** — listed as third item; Step 5 reinforces: "NEVER run as root in production"
3. ✅ **`:latest` tag** — "non-reproducible builds. Pin versions"
4. ✅ **Secrets in build args or ENV** — "they persist in image layers. Use runtime secrets"
5. ✅ **No health check** — "orchestrators can't determine container health without it"

Extended anti-patterns also covered (8 total items):
- `COPY . .` before dependency install ✅
- Installing unnecessary packages ✅
- No `.dockerignore` ✅
- `npm install` instead of `npm ci` ✅

---

### ⚠️ Identified Gaps

Three production-hardening areas are **not covered:**

1. **Multi-architecture (ARM64 + AMD64) builds**
   - No mention of `docker buildx`
   - No `--platform` or `BUILDPLATFORM` ARG examples
   - Production services often need arm64 (Apple Silicon, AWS Graviton)
   - **Gap:** Skill should include:
     ```dockerfile
     ARG BUILDPLATFORM
     ARG TARGETOS
     ARG TARGETARCH
     ```
     And buildx usage example

2. **Final-image size & distroless guidance**
   - Table mentions distroless but no size comparison
   - No guidance on when to choose `alpine` vs `distroless` vs `scratch`
   - Alpine has shell/apk for debugging; distroless is smaller but opaque
   - **Gap:** Should include size estimates and trade-off matrix

3. **SBOM & provenance generation**
   - No mention of `--sbom` or buildx provenance (`--provenance`)
   - Modern supply-chain security requires SBOM generation
   - **Gap:** Should cover:
     ```bash
     docker buildx build --sbom=type=image --provenance=mode=max
     ```

---

### Summary Table

| Requirement | Status | Evidence |
|---|---|---|
| Multi-stage + layer caching | ✅ Complete | Step 2–3, "Never COPY . . before install" |
| Base image table (5 stacks) | ✅ Complete | Step 4 table, pinned versions |
| Non-root USER (MANDATORY) + ordering | ✅ Complete | Step 5 security table, "BEFORE copying" |
| HEALTHCHECK (4 parameters) | ✅ Complete | Step 6, all examples include interval/timeout/start-period/retries |
| .dockerignore (MANDATORY) | ✅ Complete | Step 7, 30+ patterns, enforcement rule |
| Anti-patterns (5 core) | ✅ Complete | Step 8, all 5 listed explicitly |
| **Multi-arch (buildx/--platform)** | ❌ Missing | No buildx or TARGETARCH examples |
| **Image-size guidance (alpine vs distroless)** | ❌ Missing | Mentioned but no comparison |
| **SBOM/provenance generation** | ❌ Missing | Not mentioned |

---

**Verdict:** The skill produces production-hardened Dockerfiles for single-platform builds. To be **complete for enterprise/supply-chain scenarios**, add multi-arch buildx patterns, distroless decision matrix, and SBOM generation guidance.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/17.5 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 45429 ms |
| Target cost | $0.1259 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires multi-stage builds — build tools and dev dependencies must never appear in the runtime stage | PASS | Output quotes Step 2: 'Every Dockerfile uses multi-stage builds. Minimum two stages, often three.' Anti-patterns section confirms 'build tools and dev dependencies bloat the runtime image'. |
| c2 | Skill mandates layer caching optimisation — dependency manifests copied and installed before source code to preserve cache on source changes | PASS | Output quotes Step 3: 'COPY dependency manifest files (lockfile) BEFORE copying source code' and 'Never `COPY . .` before installing dependencies — it invalidates the cache on every source change'. Also states 'deps stage copies `package.json`, `requirements.txt`, `*.csproj` before source'. |
| c3 | Skill provides a base image selection table covering Node.js, .NET, Python, Go, and Rust with specific pinned versions (no latest) | PASS | Output reproduces the 5-stack table from Step 4 with pinned versions: node:22-alpine, mcr.microsoft.com/dotnet/sdk:9.0, python:3.13-slim, golang:1.23-alpine, rust:1.80-slim. Quotes skill rule: 'NEVER use `latest` tag — pin to a specific version'. |
| c4 | Skill requires a non-root user created and switched to before copying application files — and marks this as MANDATORY | PASS | Output quotes Step 5 security table: 'Non-root user \| `USER appuser` \| MANDATORY' and ordering rule: 'Switch to non-root user BEFORE copying application files'. Dockerfile snippet shows USER before COPY --from=build. |
| c5 | Skill requires a HEALTHCHECK instruction in every Dockerfile with interval, timeout, start-period, and retries | PASS | Output reproduces Step 6 HEALTHCHECK example with all four flags: --interval=30s, --timeout=5s, --start-period=10s, --retries=3, each confirmed with a checkmark. States 'Every Dockerfile includes a HEALTHCHECK instruction rule enforced'. |
| c6 | Skill requires a .dockerignore file and states it is mandatory — describes what must be excluded (.git, node_modules, .env, tests) | PASS | Output confirms Step 7 '.dockerignore (MANDATORY)' with all four named exclusions checked: .git ✅, node_modules ✅, .env ✅, tests ✅, *.md ✅. Quotes: '.dockerignore MUST exist'. |
| c7 | Skill provides stack-specific patterns (Node.js, .NET, Python) with complete working examples | PASS | Output states 'All 5 stack-specific patterns follow this ordering' and 'All stack-specific examples follow this pattern (deps stage copies `package.json`, `requirements.txt`, `*.csproj` before source)'. The base image table and references to stack-specific patterns confirm complete examples exist. |
| c8 | Skill lists anti-patterns including single-stage build, running as root, latest tag, secrets in build args, and no health check | PASS | Output lists all five from Step 8 with checkmarks: (1) single-stage build, (2) running as root, (3) :latest tag, (4) secrets in build args or ENV, (5) no health check. Notes 8 total anti-patterns covered. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample Dockerfile | PASS | The entire output is a verification report with ✅/⚠️/❌ verdicts per named requirement and a summary table. No sample Dockerfile is generated. |
| c10 | Output verifies the multi-stage build rule and explicitly checks that build tools and dev dependencies cannot leak into the runtime stage | PASS | Output confirms Step 2 multi-stage mandate and references the anti-pattern: 'build tools and dev dependencies bloat the runtime image'. The multi-stage verification section is explicitly labelled and confirmed. |
| c11 | Output verifies the layer-cache optimisation rule — dependency manifests (package.json, requirements.txt, *.csproj) copied and installed before source code | PASS | Output explicitly names package.json, requirements.txt, and *.csproj in the layer-caching confirmation, quoting the skill rule and stating all stack-specific examples follow this pattern. |
| c12 | Output confirms the base image table covers Node.js, .NET, Python, Go, and Rust with specific pinned versions (no `:latest`, no floating major tags) | PASS | Output reproduces the full 5-stack table with specific version strings (node:22-alpine, dotnet/sdk:9.0, python:3.13-slim, golang:1.23-alpine, rust:1.80-slim) and confirms 'NEVER use `latest` tag — pin to a specific version'. |
| c13 | Output verifies the non-root user requirement is marked MANDATORY and that the USER directive is set before COPY of application files | PASS | Output quotes 'Non-root user \| `USER appuser` \| MANDATORY' and ordering rule 'Switch to non-root user BEFORE copying application files', and shows a code snippet with USER preceding COPY --from=build. |
| c14 | Output confirms HEALTHCHECK is required in every Dockerfile with all four parameters — interval, timeout, start-period, retries — not just a check command | PASS | Output explicitly checks each of the four parameters (--interval=30s ✅, --timeout=5s ✅, --start-period=10s ✅, --retries=3 ✅) and confirms 'Every Dockerfile includes a HEALTHCHECK instruction rule enforced'. |
| c15 | Output confirms .dockerignore is mandatory and lists the required exclusions (.git, node_modules, .env, tests) explicitly | PASS | Output lists all four named exclusions with checkmarks (.git ✅, node_modules ✅, .env ✅, tests ✅) and confirms '.dockerignore MUST exist' is the enforcement rule. |
| c16 | Output verifies stack-specific complete examples exist for at least Node.js, .NET, and Python — not just generic templates | PASS | Output states 'All 5 stack-specific patterns follow this ordering' and names package.json (Node.js), requirements.txt (Python), *.csproj (.NET) as the dependency manifests each example copies before source. The summary table row confirms 'Step 2–3, stack-specific examples'. |
| c17 | Output confirms the anti-pattern list names single-stage build, running as root, latest tag, secrets in build args, and no health check | PASS | All five anti-patterns confirmed with numbered checkmarks from Step 8: (1) single-stage build, (2) running as root, (3) :latest tag, (4) secrets in build args or ENV, (5) no health check. |
| c18 | Output identifies any genuine gaps — e.g. no SBOM/provenance guidance, no buildx/multi-arch instructions, no rule on minimising final image size (distroless / alpine considerations) | PARTIAL | Output identifies all three gap categories: (1) multi-arch — 'No mention of `docker buildx`', 'No `--platform` or `BUILDPLATFORM` ARG examples'; (2) image-size/distroless — 'no size comparison', 'No guidance on when to choose alpine vs distroless vs scratch'; (3) SBOM/provenance — 'No mention of `--sbom` or buildx provenance'. Summary table marks all three ❌ Missing. Ceiling is PARTIAL. |

### Notes

The captured output is a thorough, well-structured verification report that confirms every requirement in the skill definition with direct quotes and code snippets. All 17 PASS-ceiling criteria are fully satisfied with specific evidence — quoted skill text, step numbers, and code examples. The one PARTIAL-ceiling criterion (gap identification) is also fully addressed, identifying all three expected gaps (multi-arch/buildx, distroless/alpine size guidance, SBOM/provenance) with concrete detail. The report earns 17.5/17.5, the maximum possible score.
