---
name: api-design
description: Design an API — resource hierarchy, endpoints, request/response shapes, error handling, and pagination.
argument-hint: "[API or resource to design]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Design an API for $ARGUMENTS.

## Principles

- Hierarchical URLs mirroring entity ownership (`/sources/{id}/crawls/{crawlId}`)
- No flat top-level listings — every entity accessed through its parent chain
- All list endpoints: pagination (`page`, `size`), sorting (sensible default), text filter (`?q=`)
- Optimistic concurrency via `lastUpdatedAt` (409 Conflict)
- PATCH with RFC 7396 merge semantics
- Consistent error responses (problem details format)

## Output

For each endpoint: method, path, description, parameters, request body (with types), response (success + error codes with examples). Present as a table, then detail each endpoint.
