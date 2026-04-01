---
name: write-dockerfile
description: Write a Dockerfile for a service — multi-stage build, minimal image, security hardening.
argument-hint: "[service or application to containerise]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a Dockerfile for $ARGUMENTS.

## Principles

- Multi-stage build (build stage → runtime stage)
- Minimal runtime image (alpine or distroless where possible)
- Non-root user
- `.dockerignore` to exclude build artifacts, tests, docs
- Pin base image versions (not `latest`)
- Copy dependency files first, install, then copy source (layer caching)
- Health check instruction
- Security: no secrets in the image, `--cap-drop=ALL` at runtime
