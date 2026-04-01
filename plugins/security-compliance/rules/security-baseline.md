---
description: Security baseline — always-on rules for writing secure code
---

# Security Baseline

## Input validation
- Validate all external input at system boundaries (API endpoints, form handlers, CLI args)
- Use allowlists over denylists for input validation
- Sanitize output based on context (HTML, SQL, shell, URL)
- Use typed schemas (Zod, JSON Schema) for validation at boundaries

## Authentication & authorization
- Never store passwords in plaintext — use bcrypt, scrypt, or argon2
- Check authorization on every request, not just at the UI level
- Use short-lived tokens; implement token refresh for long sessions
- Never expose internal IDs in URLs without authorization checks
- Use HMAC-signed httpOnly cookies for session/auth tokens

## Bot protection
- Layer bot protection: server-side verification (e.g., Vercel BotID) + honeypot fields
- Return fake success responses to detected bots (don't leak detection)
- Abstract bot protection into shared utilities for consistent application across forms

## Secrets management
- Never commit secrets, API keys, or credentials to version control
- Use environment variables or a secrets manager for sensitive configuration
- Store provider tokens as encrypted config (e.g., Pulumi encrypted config)
- Add sensitive file patterns to `.gitignore`: `.env`, `.env.local`, `*.pem`, `credentials.*`
- Use `.env.example` to document required environment variables without values

## Data handling
- Encrypt sensitive data at rest and in transit
- Log carefully — never log passwords, tokens, PII, or full credit card numbers
- Apply principle of least privilege to database access and API scopes
- Use optimistic concurrency (e.g., `lastUpdatedAt`) for state-changing operations

## Dependencies
- Keep dependencies up to date
- Use central package management (e.g., `Directory.Packages.props` for .NET)
- Pin dependency versions in production deployments
- Review new dependencies before adding — check maintenance status and security history

## External dependencies in code
- Abstract external dependencies (HTTP, AI/LLM, email) behind interfaces
- Never use concrete HTTP clients or AI clients directly — go through the interface
- This enables faking in tests and swapping providers without code changes

## Common vulnerabilities to avoid
- SQL injection: use parameterized queries / ORMs, never string concatenation
- XSS: escape output, use Content-Security-Policy headers
- CSRF: use anti-CSRF tokens for state-changing requests
- Command injection: avoid `exec`/`eval` with user input; use safe APIs
- Path traversal: validate and sanitize file paths; never join user input directly

## Container security
- Run containers sandboxed: `--network=none`, `--read-only`, `--cap-drop=ALL`
- Use image allowlists (default-deny) for container registries
- JSON on stdin/stdout protocol for container communication
