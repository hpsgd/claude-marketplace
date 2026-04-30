# Result: Write SDK guide

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

---

## Output

The following simulates what the skill produces for the prompt:

> `/developer-docs-writer:write-sdk-guide for our Python SDK — it wraps our REST API and currently has no documentation beyond the README installation instructions.`

The skill begins with a research phase before writing a single word.

---

### Step 1 research summary (internal — not published)

After running `Glob` and `Grep` across the codebase the skill identifies:

- **Package:** `acme-sdk` (pip), importable as `acme`
- **Public classes:** `AcmeClient`, `AsyncAcmeClient`
- **Resources:** `client.users`, `client.orders`, `client.webhooks`
- **Auth:** API key via `ACME_API_KEY` env var or `api_key` constructor arg; raises `acme.exceptions.MissingCredentialsError` if absent
- **Supported Python:** 3.9+
- **Exceptions:** `ValidationError`, `AuthenticationError`, `RateLimitError`, `NotFoundError`, `ServerError`
- **Pagination:** cursor-based via `.list()` returning `PagedResponse`; iterator via `.auto_page()`
- **Async:** `AsyncAcmeClient` mirrors the sync API; all methods are coroutines

---

# Acme Python SDK Guide

**SDK version:** 2.3.1 | **Python:** 3.9+

## Installation

```bash
pip install acme-sdk
```

Verify the install:

```bash
python -c "import acme; print(acme.__version__)"
# 2.3.1
```

**Requirements:** Python 3.9 or later. No system-level dependencies.

---

## Quick start

```python
import os
from acme import AcmeClient

client = AcmeClient(api_key=os.environ["ACME_API_KEY"])

user = client.users.get("usr_01HXYZ")
print(user.email)        # jane@example.com
print(user.created_at)  # 2024-11-03T09:14:22Z
```

**Expected output:**

```
jane@example.com
2024-11-03T09:14:22Z
```

Run it:

```bash
ACME_API_KEY=sk_live_... python examples/quickstart.py
```

---

## Authentication

The SDK reads credentials in this order:

1. `api_key` constructor argument — `AcmeClient(api_key="sk_live_...")`
2. `ACME_API_KEY` environment variable — set it and omit the argument

If neither is present, the constructor raises `acme.exceptions.MissingCredentialsError` immediately — before any network call is made.

```python
import os
from acme import AcmeClient
from acme.exceptions import MissingCredentialsError

try:
    client = AcmeClient()          # relies on ACME_API_KEY env var
except MissingCredentialsError as exc:
    print(f"Set ACME_API_KEY before running: {exc}")
```

Never hardcode the API key in source files. Use `os.environ["ACME_API_KEY"]` or a secrets manager.

---

## Configuration

### Client options

| Option | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str` | — (required) | Your API key. Get it from the [Acme dashboard](https://app.acme.io/settings/api). |
| `base_url` | `str` | `https://api.acme.io/v2` | Override for staging: `https://api-staging.acme.io/v2`. |
| `timeout` | `float` | `30.0` | Per-request timeout in seconds. |
| `max_retries` | `int` | `3` | Automatic retries on 5xx responses. Set `0` to disable. |
| `logger` | `logging.Logger \| None` | `None` | Pass your app logger for request/response traces. |

### Environment variables

| Variable | Maps to | Example |
|---|---|---|
| `ACME_API_KEY` | `api_key` | `sk_live_abc123` |
| `ACME_BASE_URL` | `base_url` | `https://api-staging.acme.io/v2` |

### Custom configuration example

```python
import logging
import os
from acme import AcmeClient

logger = logging.getLogger("acme")
logger.setLevel(logging.DEBUG)

client = AcmeClient(
    api_key=os.environ["ACME_API_KEY"],
    base_url="https://api-staging.acme.io/v2",
    timeout=10.0,
    max_retries=1,
    logger=logger,
)
```

---

## Common patterns

### Pagination

`list()` returns the first page. Use `auto_page()` to iterate all results without manual cursor tracking:

```python
import os
from acme import AcmeClient

client = AcmeClient(api_key=os.environ["ACME_API_KEY"])

# One page — manual
page = client.users.list(limit=50)
for user in page.items:
    print(user.id, user.email)

# All pages — automatic
for user in client.users.auto_page(limit=100):
    print(user.id, user.email)
```

### Error handling

Catch specific exception types — bare `except Exception` hides the cause and prevents correct recovery:

```python
import os
from acme import AcmeClient
from acme.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

client = AcmeClient(api_key=os.environ["ACME_API_KEY"])

try:
    user = client.users.get("usr_does_not_exist")
except NotFoundError as exc:
    print(f"User not found: {exc.resource_id}")
except ValidationError as exc:
    for field, message in exc.details.items():
        print(f"  {field}: {message}")
except RateLimitError as exc:
    print(f"Rate limited. Retry after {exc.retry_after}s")
except AuthenticationError:
    print("Check your ACME_API_KEY")
```

**Error types:**

| Exception | HTTP status | When it occurs | Key attributes |
|---|---|---|---|
| `ValidationError` | 400 | Invalid request parameters | `.details` — field-level error map |
| `AuthenticationError` | 401 | Invalid or expired API key | `.message` |
| `NotFoundError` | 404 | Resource does not exist | `.resource_id`, `.resource_type` |
| `RateLimitError` | 429 | Too many requests | `.retry_after` (seconds) |
| `ServerError` | 5xx | Service-side failure | `.request_id` — include in support tickets |

### Retry and timeout

```python
import os
from acme import AcmeClient

# High-reliability background job
client = AcmeClient(
    api_key=os.environ["ACME_API_KEY"],
    max_retries=5,
    timeout=60.0,
)

# Disable retries for writes you control yourself
client_no_retry = AcmeClient(
    api_key=os.environ["ACME_API_KEY"],
    max_retries=0,
)
```

Retries apply to 5xx responses only. 4xx responses are not retried.

### Async usage

`AsyncAcmeClient` mirrors the sync API — every method is a coroutine:

```python
import asyncio
import os
from acme import AsyncAcmeClient

async def main() -> None:
    client = AsyncAcmeClient(api_key=os.environ["ACME_API_KEY"])
    user = await client.users.get("usr_01HXYZ")
    print(user.email)

asyncio.run(main())
```

Use `AsyncAcmeClient` in FastAPI, async Django views, or any `asyncio`-based application. The sync `AcmeClient` blocks the event loop.

### Batch operations

The SDK does not batch internally. Loop and collect results:

```python
import os
from acme import AcmeClient

client = AcmeClient(api_key=os.environ["ACME_API_KEY"])

user_ids = []
for email in ["alice@example.com", "bob@example.com", "carol@example.com"]:
    user = client.users.create({"email": email, "role": "member"})
    user_ids.append(user.id)

print(user_ids)
# ['usr_01HXYZ', 'usr_02ABCD', 'usr_03EFGH']
```

### Logging and debugging

```python
import logging
import os
from acme import AcmeClient

logging.basicConfig(level=logging.DEBUG)

client = AcmeClient(
    api_key=os.environ["ACME_API_KEY"],
    logger=logging.getLogger("acme"),
)

# Each request logs: method, URL, status, latency
user = client.users.get("usr_01HXYZ")
```

Remove `logger=` before deploying to production — debug output includes request headers.

---

## Method reference

### Users (`client.users`)

| Method | Signature | Returns | Description |
|---|---|---|---|
| `list` | `list(limit=20, cursor=None)` | `PagedResponse[User]` | List users. Supports pagination. |
| `auto_page` | `auto_page(limit=100)` | `Iterator[User]` | Iterate all users across pages. |
| `get` | `get(user_id: str)` | `User` | Get a user by ID. Raises `NotFoundError` if absent. |
| `create` | `create(data: dict)` | `User` | Create a user. Raises `ValidationError` on bad input. |
| `update` | `update(user_id: str, data: dict)` | `User` | Partial update (merge patch semantics). |
| `delete` | `delete(user_id: str)` | `None` | Delete a user. Idempotent. |

### Orders (`client.orders`)

| Method | Signature | Returns | Description |
|---|---|---|---|
| `list` | `list(user_id=None, limit=20, cursor=None)` | `PagedResponse[Order]` | List orders, optionally by user. |
| `get` | `get(order_id: str)` | `Order` | Get an order by ID. |
| `create` | `create(data: dict)` | `Order` | Create an order. |
| `cancel` | `cancel(order_id: str)` | `Order` | Cancel an order. Returns the updated order. |

### Webhooks (`client.webhooks`)

| Method | Signature | Returns | Description |
|---|---|---|---|
| `list` | `list()` | `list[Webhook]` | List registered webhook endpoints. |
| `create` | `create(data: dict)` | `Webhook` | Register a new endpoint. |
| `delete` | `delete(webhook_id: str)` | `None` | Remove an endpoint. |
| `verify` | `verify(payload: bytes, signature: str)` | `bool` | Verify an incoming webhook signature. |

---

## Key types

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: str              # "usr_01HXYZ"
    email: str
    role: str            # "admin" | "member" | "viewer"
    created_at: datetime
    updated_at: datetime

@dataclass
class Order:
    id: str              # "ord_01HXYZ"
    user_id: str
    status: str          # "pending" | "processing" | "completed" | "cancelled"
    total_cents: int
    created_at: datetime

@dataclass
class PagedResponse:
    items: list          # typed per-resource
    next_cursor: str | None    # None on the last page
    has_more: bool
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `MissingCredentialsError` on startup | `ACME_API_KEY` not set | `export ACME_API_KEY=sk_live_...` |
| `AuthenticationError` on first call | Wrong or revoked key | Regenerate key in the dashboard |
| All requests time out | `timeout` too short for your network | Raise `timeout` — default is 30s |
| `ValidationError` with empty `.details` | SDK version mismatch | `pip install --upgrade acme-sdk` |
| `ServerError` on every call | Wrong base URL | Check `ACME_BASE_URL` env var |

---

## Quality checklist

| Check | Verification |
|---|---|
| Quick start runs | `ACME_API_KEY=sk_live_... python examples/quickstart.py` → prints a real email address |
| All code examples run | `ACME_API_KEY=sk_live_... python examples/all_patterns.py` → zero exceptions |
| All config options documented | Compare table against `AcmeClient.__init__` signature — every parameter accounted for |
| Error table complete | Compare against `acme/exceptions.py` — every public exception class in the table |
| Realistic data | No `"test"`, `"foo"`, or `"string"` in any example |
| SDK version stated | Version `2.3.1` in the document header |
| Auth explained once | Single auth section; other examples reference it, not re-explain it |

**Rule:** examples must be run before publication. A code block that has not been executed is a liability, not documentation.

---

## Evaluation

### Criteria (against the skill definition)

- [x] PASS: Skill requires a quickstart section that gets developers to a working example in 15 lines or fewer — Step 2 explicitly states "Under 15 lines of code" as a hard rule.
- [x] PASS: Skill requires a method reference section documenting each public method with parameters, return types, and exceptions — Step 5 mandates grouped method tables with return types; Step 4 mandates error type coverage.
- [x] PASS: Skill requires a research step — Step 1 explicitly instructs reading the SDK source via Grep/Glob before writing anything.
- [x] PASS: Skill requires installation instructions as a prerequisite before the quickstart — Step 2 template and the Output Format both place Installation before Quick start.
- [x] PASS: All code examples must be syntactically correct and complete — Rules section: "Every code example must run. A code block that requires the reader to 'fill in the rest' is not an example."
- [x] PASS: Skill includes a quality checklist that verifies examples actually work — Step 6 is a dedicated checklist with "Every code example runs" and "Quick start works" as named checks.
- [~] PARTIAL: Skill covers common patterns section with real-world usage examples beyond the quickstart — Step 4 mandates pagination, error handling, retry, and debugging as required subsections, but the Output Format does not label this section "Common patterns" explicitly, creating a minor naming inconsistency. Content requirement is fully present; section heading label is not.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three fields present.

### Output expectations (against the simulated output above)

- [x] PASS: Quickstart produces a working first-call example in 15 lines or fewer — the block is 7 lines including blank lines.
- [x] PASS: Installation instructions cover `pip install`, supported Python versions, system prerequisites, and an install-verification command.
- [x] PASS: Method reference documents each public method with signature, return type, and exceptions noted — per-resource tables used throughout.
- [x] PASS: Code examples use SDK-specific exception types — `NotFoundError`, `RateLimitError`, etc. used explicitly; no bare `except Exception`.
- [x] PASS: Authentication section explains env var, constructor argument, and the specific error raised for missing credentials.
- [x] PASS: Common-patterns section covers pagination, batch operations, async usage, and retry/timeout — all four present as named subsections.
- [x] PASS: Quality checklist includes exact run commands and states the rule that examples must be tested before publication.
- [x] PASS: Code examples are complete and copy-pasteable — no `...` placeholders, all variables defined or marked as user-supplied.
- [x] PASS: Quickstart uses `os.environ["ACME_API_KEY"]` rather than a hardcoded key.
- [x] PASS: Output addresses sync vs async distinction — async section is present and explicitly notes that the sync client blocks the event loop.

### Score detail

| Section | Met | Total |
|---|---|---|
| Criteria (skill definition) | 7.5 | 8 |
| Output expectations | 10 | 10 |
| **Combined** | **17.5** | **18** |

## Notes

The skill is well-constructed. All eight structural criteria pass except for a minor naming inconsistency: Step 4 mandates the common-patterns content but the Output Format section at the end does not label a "Common patterns" heading, creating a small gap between what Step 4 requires and what the template prescribes. In practice a developer following the skill would produce the section regardless.

The quality checklist in Step 6 asks questions ("Can a developer copy-paste and get a response?") rather than requiring documented run commands. The simulated output goes further by including exact commands and expected output — the skill would benefit from mandating this format explicitly.

The cross-reference to `/developer-docs-writer:write-api-docs` for per-method REST links is a good structural touch. The rules prohibiting internal methods and requiring realistic data (not `"test"` or `"foo"`) reflect mature documentation standards.
