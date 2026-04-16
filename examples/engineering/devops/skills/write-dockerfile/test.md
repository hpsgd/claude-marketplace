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
