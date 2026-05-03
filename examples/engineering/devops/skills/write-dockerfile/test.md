# Test: write-dockerfile skill structure

Scenario: Checking that the write-dockerfile skill enforces multi-stage builds, non-root user, pinned base images, HEALTHCHECK, and a .dockerignore — and rejects common anti-patterns like running as root or using latest tags.

## Prompt

Review the write-dockerfile skill definition and verify it produces production-hardened Dockerfiles rather than minimal single-stage examples.

In your verification report, confirm or flag each item by name. Quote the skill text where present:

- **Multi-stage build requirement** + the layer-caching rule: dependency manifests (`package.json`, `requirements.txt`, `*.csproj`, `go.mod`, `Cargo.toml`) MUST be copied and installed BEFORE source code, to preserve cache on source-only changes.
- **Base image table** for all 5 stacks (Node.js, .NET, Python, Go, Rust) with **specific pinned versions** (not `:latest`, not floating major). Quote the actual versions from the skill.
- **Non-root USER directive** marked MANDATORY, with the ordering rule: `USER` must come BEFORE the `COPY` of application files (so source files are owned correctly).
- **HEALTHCHECK in every Dockerfile** with all FOUR parameters: `--interval`, `--timeout`, `--start-period`, `--retries`.
- **`.dockerignore` MANDATORY** with required exclusions named: `.git`, `node_modules`, `.env`, `tests/`, `*.md` (and similar build noise).
- **Anti-patterns list (5)**: (1) single-stage build, (2) running as root, (3) `:latest` tag, (4) secrets in build args (`ARG SECRET=...`), (5) no HEALTHCHECK.
- **Identified gaps**: explicitly call out `--platform`/`BUILDPLATFORM`/buildx for multi-arch (arm64+amd64), distroless / alpine final-image-size guidance, SBOM/provenance generation.

Confirm or flag each by name — do not paraphrase.

## Criteria

- [ ] PASS: Skill requires multi-stage builds — build tools and dev dependencies must never appear in the runtime stage
- [ ] PASS: Skill mandates layer caching optimisation — dependency manifests copied and installed before source code to preserve cache on source changes
- [ ] PASS: Skill provides a base image selection table covering Node.js, .NET, Python, Go, and Rust with specific pinned versions (no latest)
- [ ] PASS: Skill requires a non-root user created and switched to before copying application files — and marks this as MANDATORY
- [ ] PASS: Skill requires a HEALTHCHECK instruction in every Dockerfile with interval, timeout, start-period, and retries
- [ ] PASS: Skill requires a .dockerignore file and states it is mandatory — describes what must be excluded (.git, node_modules, .env, tests)
- [ ] PASS: Skill provides stack-specific patterns (Node.js, .NET, Python) with complete working examples
- [ ] PASS: Skill lists anti-patterns including single-stage build, running as root, latest tag, secrets in build args, and no health check

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample Dockerfile
- [ ] PASS: Output verifies the multi-stage build rule and explicitly checks that build tools and dev dependencies cannot leak into the runtime stage
- [ ] PASS: Output verifies the layer-cache optimisation rule — dependency manifests (package.json, requirements.txt, *.csproj) copied and installed before source code
- [ ] PASS: Output confirms the base image table covers Node.js, .NET, Python, Go, and Rust with specific pinned versions (no `:latest`, no floating major tags)
- [ ] PASS: Output verifies the non-root user requirement is marked MANDATORY and that the USER directive is set before COPY of application files
- [ ] PASS: Output confirms HEALTHCHECK is required in every Dockerfile with all four parameters — interval, timeout, start-period, retries — not just a check command
- [ ] PASS: Output confirms .dockerignore is mandatory and lists the required exclusions (.git, node_modules, .env, tests) explicitly
- [ ] PASS: Output verifies stack-specific complete examples exist for at least Node.js, .NET, and Python — not just generic templates
- [ ] PASS: Output confirms the anti-pattern list names single-stage build, running as root, latest tag, secrets in build args, and no health check
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no SBOM/provenance guidance, no buildx/multi-arch instructions, no rule on minimising final image size (distroless / alpine considerations)
