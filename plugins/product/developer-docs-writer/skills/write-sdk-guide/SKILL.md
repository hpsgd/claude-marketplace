---
name: write-sdk-guide
description: "Write an SDK or client library guide — installation, quick start, configuration, common patterns, and error handling. Produces a complete developer reference from zero to production usage."
argument-hint: "[SDK, client library, or language to document]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write an SDK guide for $ARGUMENTS using the mandatory process and structure below.

## Step 1 — Research the SDK

Before writing, understand the full surface area:

1. Search the codebase for the SDK source, type definitions, and public API using `Grep` and `Glob`
2. Identify every public class, method, and configuration option
3. Find the authentication mechanism (API keys, OAuth tokens, service accounts)
4. Check for existing examples, tests, or README content
5. Identify the package manager and supported language/runtime versions

**Output:** A list of public API methods, configuration options, auth mechanisms, and supported versions.

## Step 2 — Write installation and quick start

The first thing a developer reads. It must get them from zero to a working API call in under 2 minutes.

```markdown
# [SDK Name] Guide

## Installation

\`\`\`bash
[Package manager command — e.g., npm install @acme/sdk]
\`\`\`

**Requirements:** [Language] [minimum version]+

## Quick start

\`\`\`[language]
[Complete working example: import, authenticate, make one API call, print result.
 Must be under 15 lines. Must work with copy-paste.]
\`\`\`

**Expected output:**
\`\`\`
[What the developer should see]
\`\`\`
```

**Rules for quick start:**
- Under 15 lines of code — this is not the place for error handling or edge cases
- Must include the import/require statement
- Must include authentication — show how to pass the API key or token
- Must make a real API call, not just instantiate a client
- Use realistic response data, not `"string"` or `"foo"`

**Output:** Installation command and a working quick-start example.

## Step 3 — Write configuration reference

Document every configuration option the SDK accepts:

```markdown
## Configuration

### Client options

| Option | Type | Default | Description |
|---|---|---|---|
| `apiKey` | string | — (required) | Your API key. Get it from: [dashboard location] |
| `baseUrl` | string | `https://api.example.com/v1` | API base URL. Override for staging or self-hosted. |
| `timeout` | number | `30000` | Request timeout in milliseconds |
| `retries` | number | `3` | Number of automatic retries on 5xx errors |
| `logger` | Logger \| null | `null` | Custom logger instance. Pass `console` for debug output. |

### Environment variables

The SDK reads these environment variables as fallbacks:

| Variable | Maps to | Example |
|---|---|---|
| `ACME_API_KEY` | `apiKey` | `sk_live_abc123` |
| `ACME_BASE_URL` | `baseUrl` | `https://api-staging.example.com/v1` |

### Example: custom configuration

\`\`\`[language]
[Complete example showing non-default configuration]
\`\`\`
```

**Rules for configuration:**
- Every option must have a type, default value, and description
- Required options must be marked as required — no silent failures
- If an option has valid values (enum), list them all
- Show environment variable alternatives if supported

**Output:** Complete configuration reference table with examples.

## Step 4 — Write common patterns

Document the patterns developers will use most frequently:

```markdown
## Common patterns

### Pagination

\`\`\`[language]
[Complete example: fetch a paginated list, iterate through all pages]
\`\`\`

### Error handling

\`\`\`[language]
[Complete example: try/catch with typed errors, show how to inspect error details]
\`\`\`

**Error types:**

| Error class | HTTP status | When it occurs | How to handle |
|---|---|---|---|
| `ValidationError` | 400 | Invalid request parameters | Fix the request — check `error.details` for field-level errors |
| `AuthenticationError` | 401 | Invalid or expired credentials | Refresh token or check API key |
| `RateLimitError` | 429 | Too many requests | Wait `error.retryAfter` seconds, then retry |
| `ServerError` | 5xx | Service issue | Automatic retry (configurable). If persistent, contact support |

### Retry and timeout

\`\`\`[language]
[Example: configuring retry behaviour, handling timeouts]
\`\`\`

### Logging and debugging

\`\`\`[language]
[Example: enabling debug logging to troubleshoot requests]
\`\`\`
```

Add patterns specific to the SDK — e.g., file uploads, streaming responses, batch operations, webhook verification — based on what the SDK actually supports.

**Output:** Code examples for pagination, error handling, retry, and debugging at minimum.

## Step 5 — Write type definitions and method reference

For typed languages, document the key types. For all languages, provide a method quick-reference:

```markdown
## Method reference

### [Resource name]

| Method | Description | Returns |
|---|---|---|
| `client.users.list(options?)` | List all users. Supports pagination. | `PagedResponse<User>` |
| `client.users.get(id)` | Get a user by ID. | `User` |
| `client.users.create(data)` | Create a new user. | `User` |
| `client.users.update(id, data)` | Update an existing user. | `User` |
| `client.users.delete(id)` | Delete a user. | `void` |

### Key types

\`\`\`[language]
[Type definitions for the most important models — User, Order, etc.]
\`\`\`
```

**Rules for method reference:**
- Group by resource, not by HTTP method
- Include the return type for every method
- If a method accepts options, link to or show the options type
- Mark deprecated methods clearly

**Output:** Method reference table and key type definitions.

## Step 6 — Quality checks

| Check | Requirement |
|---|---|
| Quick start works | Can a developer copy-paste and get a response in < 2 minutes? |
| Every code example runs | No incomplete snippets, no missing imports |
| Every config option documented | Nothing discoverable only by reading source |
| Error types are complete | Does the error table cover all error classes the SDK throws? |
| Realistic data | Are examples using plausible values, not `"test"` or `"foo"`? |
| Version stated | Is the SDK version this guide covers stated in the header? |
| Auth explained once, referenced everywhere | Is there one clear auth section, not repeated setup in every example? |

## Rules

- Every code example must run. A code block that requires the reader to "fill in the rest" is not an example.
- Use realistic data in all examples — `"jane@example.com"`, not `"user@test.com"` or `"string"`.
- Do not document internal or private methods. If it's not part of the public API, it's not in the guide.
- If the SDK wraps a REST API, link to the API reference for each method so developers can see the raw request/response. Cross-reference `/developer-docs-writer:write-api-docs`.
- If the SDK has versioning (v1, v2), document the latest version and note breaking changes from the previous version in a migration section.
- For integration tutorials showing the SDK in context, cross-reference `/developer-docs-writer:write-integration-guide`.

## Output Format

```markdown
# [SDK Name] Guide

## Installation
[Package manager command, requirements]

## Quick start
[Under-15-line working example]

## Configuration
[Options table, env vars, custom config example]

## Common patterns
### Pagination
### Error handling
### Retry and timeout
### Logging and debugging
[Additional SDK-specific patterns]

## Method reference
[Per-resource method tables]

## Key types
[Type definitions]

## Troubleshooting
[Common errors and fixes]

## Migration guide (if applicable)
[Breaking changes from previous version]
```
