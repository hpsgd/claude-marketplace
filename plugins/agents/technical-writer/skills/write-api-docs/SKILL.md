---
name: write-api-docs
description: Generate API reference documentation from code, OpenAPI specs, or endpoint implementations.
argument-hint: "[API file, directory, or OpenAPI spec path]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Generate API documentation for $ARGUMENTS.

For each endpoint, document: method, path, description, authentication, parameters (path, query, body with types), response (success and error codes with examples), and usage example (curl or SDK).

Follow the project's writing style rules. Organise endpoints by resource, not by HTTP method.
