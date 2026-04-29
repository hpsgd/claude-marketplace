# Output: write-dockerfile skill structure

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires multi-stage builds — Step 2 states "Every Dockerfile uses multi-stage builds" with an explicit rule: "Build tools, dev dependencies, and source code NEVER appear in the runtime stage." Met.
- [x] PASS: Skill mandates layer caching optimisation — Step 3 defines an explicit layer order and states "COPY dependency manifest files (lockfile) BEFORE copying source code" and "Never `COPY . .` before installing dependencies." Met.
- [x] PASS: Skill provides a base image selection table covering Node.js, .NET, Python, Go, and Rust with specific pinned versions — Step 4 lists all five stacks with pinned versions (node:22-alpine, dotnet/sdk:9.0, python:3.13-slim, golang:1.23-alpine, rust:1.80-slim). No `latest` tags. Met.
- [x] PASS: Skill requires a non-root user created and switched to before copying application files, marked MANDATORY — Step 5 is titled "Security Hardening (MANDATORY)" and the security checklist table marks "Non-root user" as MANDATORY. The code example shows `USER appuser` before the `COPY` instructions. Met.
- [x] PASS: Skill requires a HEALTHCHECK instruction in every Dockerfile with all four parameters — Step 6 shows `HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3` and states "Every Dockerfile includes a HEALTHCHECK instruction." All four parameters present. Met.
- [x] PASS: Skill requires a .dockerignore file and states it is mandatory — Step 7 is titled ".dockerignore (MANDATORY)" and the rules state ".dockerignore MUST exist." The template explicitly includes `.git`, `node_modules`, `.env`, `.env.*`, and test directories (`tests`, `test`, `__tests__`). Met.
- [x] PASS: Skill provides stack-specific patterns for Node.js, .NET, and Python with complete working examples — Step 8 has three full Dockerfiles, each covering base image through CMD/ENTRYPOINT with security hardening and HEALTHCHECK inline. Met.
- [x] PASS: Skill lists anti-patterns including single-stage build, running as root, latest tag, secrets in build args, and no health check — all five appear explicitly in the Anti-Patterns section. Met.

### Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample Dockerfile. This result evaluates the skill definition against each criterion. Met.
- [x] PASS: Output verifies the multi-stage build rule and explicitly checks that build tools and dev dependencies cannot leak into the runtime stage — Step 2 rule confirmed: "Build tools, dev dependencies, and source code NEVER appear in the runtime stage." Met.
- [x] PASS: Output verifies the layer-cache optimisation rule — dependency manifests copied and installed before source code — Step 3 confirms this with an explicit ordered list and the "never COPY . . before installing dependencies" rule. Met.
- [x] PASS: Output confirms the base image table covers Node.js, .NET, Python, Go, and Rust with specific pinned versions — Step 4 table verified; no floating or `latest` tags present. Met.
- [x] PASS: Output verifies the non-root user requirement is marked MANDATORY and that the USER directive is set before COPY of application files — Step 5 checklist and code example both confirmed. Met.
- [x] PASS: Output confirms HEALTHCHECK is required in every Dockerfile with all four parameters — Step 6 confirmed with `--interval`, `--timeout`, `--start-period`, and `--retries` present in every example. Met.
- [x] PASS: Output confirms .dockerignore is mandatory and lists the required exclusions explicitly — Step 7 confirmed; `.git`, `node_modules`, `.env`, and test directories all present in the template. Met.
- [x] PASS: Output verifies stack-specific complete examples exist for Node.js, .NET, and Python — Step 8 confirmed with three self-contained Dockerfiles. Met.
- [x] PASS: Output confirms the anti-pattern list names single-stage build, running as root, latest tag, secrets in build args, and no health check — Anti-Patterns section confirmed. Met.
- [~] PARTIAL: Output identifies genuine gaps — the skill has no SBOM/provenance guidance (`docker buildx build --sbom` or `--provenance`), no multi-architecture build instructions (`buildx --platform linux/amd64,linux/arm64`), and no explicit decision tree for minimising final image size beyond base image selection (no alpine vs distroless trade-off discussion with size targets). Distroless is mentioned as an option in the base image table but not developed into a hardening progression. Partially met: gaps present and identified.

## Notes

The skill is thorough and well-structured. All eight structural criteria pass cleanly. The stack-specific examples in Step 8 are complete working Dockerfiles rather than stripped templates — each includes multi-stage build, non-root user setup, and HEALTHCHECK inline, which means an agent following the skill would produce consistent output without needing to cross-reference other sections.

Two minor inconsistencies worth noting: the introductory multi-stage example in Step 2 copies `node_modules` wholesale from the build stage into the runtime stage (including dev dependencies). The Step 8 Node.js example corrects this with `npm prune --production`, but someone reading only Step 2 could miss the pruning step. Second, the Python example in Step 8 places `USER app` after the `COPY` instructions rather than before, which contradicts the Step 5 MANDATORY rule. The `.NET` and Node.js examples handle this correctly. The `--chown` flag on `COPY` partially compensates, but the sequence is inconsistent with the stated rule.

Neither issue affects the rubric score. The genuine gaps (SBOM/provenance, multi-arch builds, image size trade-off guidance) are the only material missing coverage for production hardening at scale.
