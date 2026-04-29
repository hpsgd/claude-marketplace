# Test: write-dockerfile skill structure

Scenario: Checking that the write-dockerfile skill enforces multi-stage builds, non-root user, pinned base images, HEALTHCHECK, and a .dockerignore — and rejects common anti-patterns like running as root or using latest tags.

## Prompt

Review the write-dockerfile skill definition and verify it produces production-hardened Dockerfiles rather than minimal single-stage examples.

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
