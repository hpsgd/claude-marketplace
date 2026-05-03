# Write Dockerfile

Scenario: Checking that the write-dockerfile skill enforces multi-stage builds, non-root user, pinned base images, HEALTHCHECK, and a .dockerignore — and rejects common anti-patterns like running as root or using latest tags.

## Prompt

> Review the write-dockerfile skill definition and verify it produces production-hardened Dockerfiles rather than minimal single-stage examples.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The skill is solid overall. Here's my assessment:

**Production hardening is genuinely enforced — not minimal:**
- Multi-stage builds are mandatory ("Every Dockerfile uses multi-stage builds. Minimum two stages")
- Non-root user is MANDATORY in the security checklist
- HEALTHCHECK required in every Dockerfile
- `.dockerignore` is MANDATORY
- Version pinning enforced — `latest` is an explicit anti-pattern
- CVE scanning (`trivy`/`docker scout`) marked MANDATORY

**Gaps worth addressing:**

1. **Health check / package contradiction** — Step 5 says "No curl, wget, bash in production" (RECOMMENDED), but Steps 6 and 8 use `wget` in `HEALTHCHECK`. Only the distroless path avoids this. Alpine images without wget installed will have broken health checks.

2. **Missing stack examples** — Go and Rust appear in the base image table (Step 4) but have no Step 8 concrete patterns, unlike Node.js, .NET, and Python.

3. **Python missing standard env vars** — `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1` are standard production settings; neither appears in the Python pattern.

4. **`npm prune --production`** — This approach is functional but the modern idiom is a clean `npm ci --omit=dev` in the runtime stage rather than pruning after a full install.

5. **No multi-arch guidance** — No mention of `--platform` / `BUILDPLATFORM` for arm64/amd64 cross-builds, increasingly relevant for Apple Silicon dev → Linux prod pipelines.

**Verdict:** The skill does enforce production-hardened, multi-stage Dockerfiles — the anti-pattern list explicitly calls out single-stage builds as NEVER. The gaps above are real but secondary. The health check / wget contradiction is the most actionable fix since it produces a subtly broken health check on minimal alpine images.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 10.5/17.5 (60%) |
| Evaluated | 2026-04-30 |
| Target duration | 43443 ms |
| Target cost | $0.1293 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires multi-stage builds — build tools and dev dependencies must never appear in the runtime stage | PASS | Output states 'Multi-stage builds are mandatory ("Every Dockerfile uses multi-stage builds. Minimum two stages")' and 'the anti-pattern list explicitly calls out single-stage builds as NEVER' |
| c2 | Skill mandates layer caching optimisation — dependency manifests copied and installed before source code to preserve cache on source changes | FAIL | No mention of layer caching optimisation, dependency manifests, or copy-order discipline anywhere in the captured output |
| c3 | Skill provides a base image selection table covering Node.js, .NET, Python, Go, and Rust with specific pinned versions (no latest) | PARTIAL | Output notes 'Go and Rust appear in the base image table (Step 4)' and 'Version pinning enforced — `latest` is an explicit anti-pattern', implying the table exists and covers all five, but does not confirm specific pinned versions for each language |
| c4 | Skill requires a non-root user created and switched to before copying application files — and marks this as MANDATORY | PASS | Output states 'Non-root user is MANDATORY in the security checklist' — MANDATORY designation confirmed |
| c5 | Skill requires a HEALTHCHECK instruction in every Dockerfile with interval, timeout, start-period, and retries | PARTIAL | Output confirms 'HEALTHCHECK required in every Dockerfile' but does not confirm all four parameters (interval, timeout, start-period, retries) are mandated; only generic requirement stated |
| c6 | Skill requires a .dockerignore file and states it is mandatory — describes what must be excluded (.git, node_modules, .env, tests) | PARTIAL | Output confirms '`.dockerignore` is MANDATORY' but does not list or verify the required exclusions (.git, node_modules, .env, tests) |
| c7 | Skill provides stack-specific patterns (Node.js, .NET, Python) with complete working examples | PASS | Output explicitly distinguishes that Node.js, .NET, and Python have 'Step 8 concrete patterns' while noting Go and Rust are missing — confirming the three stacks have examples |
| c8 | Skill lists anti-patterns including single-stage build, running as root, latest tag, secrets in build args, and no health check | PARTIAL | Output confirms single-stage build ('NEVER'), latest tag ('explicit anti-pattern'), and non-root user (MANDATORY implies root is anti-pattern), but does not confirm 'secrets in build args' or 'no health check' appear in the anti-pattern list |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample Dockerfile | PASS | The entire response reviews the skill definition, provides section-by-section assessment of what is enforced and what is missing, and ends with an explicit 'Verdict:' — no sample Dockerfile generated |
| c10 | Output verifies the multi-stage build rule and explicitly checks that build tools and dev dependencies cannot leak into the runtime stage | PASS | 'Multi-stage builds are mandatory' confirmed and anti-pattern list 'explicitly calls out single-stage builds as NEVER' — leakage prevention is implicit in the mandatory multi-stage rule verification |
| c11 | Output verifies the layer-cache optimisation rule — dependency manifests (package.json, requirements.txt, *.csproj) copied and installed before source code | FAIL | No reference to layer caching, dependency manifest copy order, package.json, requirements.txt, or *.csproj in the output |
| c12 | Output confirms the base image table covers Node.js, .NET, Python, Go, and Rust with specific pinned versions (no `:latest`, no floating major tags) | PARTIAL | Output mentions 'Go and Rust appear in the base image table (Step 4)' and 'Version pinning enforced — `latest` is an explicit anti-pattern', but does not confirm specific pinned version strings for any of the five stacks |
| c13 | Output verifies the non-root user requirement is marked MANDATORY and that the USER directive is set before COPY of application files | PARTIAL | Output confirms 'Non-root user is MANDATORY in the security checklist' but does not verify the ordering constraint that USER directive precedes the COPY of application files |
| c14 | Output confirms HEALTHCHECK is required in every Dockerfile with all four parameters — interval, timeout, start-period, retries — not just a check command | FAIL | Output only states 'HEALTHCHECK required in every Dockerfile' — the four parameters (interval, timeout, start-period, retries) are never enumerated or confirmed |
| c15 | Output confirms .dockerignore is mandatory and lists the required exclusions (.git, node_modules, .env, tests) explicitly | PARTIAL | Output confirms '`.dockerignore` is MANDATORY' but does not list .git, node_modules, .env, or tests as required exclusions |
| c16 | Output verifies stack-specific complete examples exist for at least Node.js, .NET, and Python — not just generic templates | PASS | 'Go and Rust appear in the base image table (Step 4) but have no Step 8 concrete patterns, unlike Node.js, .NET, and Python' — explicitly confirms all three stacks have concrete patterns |
| c17 | Output confirms the anti-pattern list names single-stage build, running as root, latest tag, secrets in build args, and no health check | PARTIAL | Output confirms single-stage ('NEVER'), latest tag ('explicit anti-pattern'), and non-root user (MANDATORY); secrets in build args and 'no health check' as explicit anti-pattern entries are not confirmed |
| c18 | Output identifies any genuine gaps — e.g. no SBOM/provenance guidance, no buildx/multi-arch instructions, no rule on minimising final image size (distroless / alpine considerations) | PARTIAL | 'No multi-arch guidance — No mention of `--platform` / `BUILDPLATFORM` for arm64/amd64 cross-builds' directly matches the buildx/multi-arch gap; distroless is also mentioned in context of the wget/health-check contradiction |

### Notes

The output does a credible job verifying the headline requirements — multi-stage builds, non-root MANDATORY, HEALTHCHECK presence, .dockerignore mandatory, stack-specific patterns for Node/NET/Python, and version pinning. It also identifies genuine gaps (multi-arch, missing Go/Rust patterns, Python env vars). The two most significant failures are layer-cache optimisation (c2/c11): not a single word about copy order for dependency manifests, which is a fundamental Dockerfile performance concern. Additionally, HEALTHCHECK parameter completeness (c5/c14) is never drilled into — the output notes health checks are required but never confirms the four attributes (interval, timeout, start-period, retries). The .dockerignore exclusion list (c6/c15) and full anti-pattern set (c8/c17) are also only partially verified. These gaps together keep the score at the PARTIAL threshold.
