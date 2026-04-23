---
description: SonarCloud code quality enforcement and configuration
---

# [SonarCloud](https://sonarcloud.io)

## Quality gate
- Enforced on PRs — PRs cannot merge unless the quality gate passes
- Workflow runs tests with coverage before scanning
- Configuration lives in `sonar-project.properties`

## Coverage requirements
- New or modified code **must** have unit tests
- Keep test coverage for changed files above 80%
- Tests co-located alongside source (`*.test.ts`)
- Coverage output: `coverage/lcov.info` (gitignored, consumed by SonarCloud)

## Coverage integration
- TypeScript: [Vitest](https://vitest.dev) with `@vitest/coverage-v8` generates lcov
- The SonarCloud workflow (`.github/workflows/sonarcloud.yml`) runs tests with coverage, then scans

## Configuration
- SonarCloud org and project keys defined in `sonar-project.properties`
- Source and test paths, exclusions, and coverage report paths configured there
- Quality gate rules configured in the SonarCloud web UI, not in repo
