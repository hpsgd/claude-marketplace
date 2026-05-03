# Test: Write SDK guide

Scenario: Testing whether the write-sdk-guide skill requires a quickstart under 15 lines, a method reference, and code examples that are complete and runnable.

## Prompt

First, create the Python SDK source files:

```bash
mkdir -p clearpath_sdk/resources
```

Write to `clearpath_sdk/__init__.py`:

```python
from clearpath_sdk.client import ClearpathClient

__version__ = "1.2.0"
__all__ = ["ClearpathClient"]
```

Write to `clearpath_sdk/client.py`:

```python
from __future__ import annotations

import os
from typing import Any

import requests

from clearpath_sdk.exceptions import AuthenticationError, ClearpathAPIError, NotFoundError
from clearpath_sdk.resources.projects import ProjectsResource


class ClearpathClient:
    """Clearpath API client."""

    BASE_URL = "https://api.clearpath.io/v2"

    def __init__(self, api_key: str | None = None, timeout: int = 30) -> None:
        self._api_key = api_key or os.environ.get("CLEARPATH_API_KEY")
        if not self._api_key:
            raise AuthenticationError(
                "No API key provided. Pass api_key= or set CLEARPATH_API_KEY."
            )
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {self._api_key}"})
        self.projects = ProjectsResource(self)

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self.BASE_URL}{path}"
        resp = self._session.request(method, url, timeout=self._timeout, **kwargs)
        if resp.status_code == 401:
            raise AuthenticationError("Invalid or expired API key.")
        if resp.status_code == 404:
            raise NotFoundError(f"Resource not found: {path}")
        if not resp.ok:
            raise ClearpathAPIError(resp.status_code, resp.text)
        return resp.json()
```

Write to `clearpath_sdk/exceptions.py`:

```python
class ClearpathAPIError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"API error {status_code}: {message}")

class AuthenticationError(ClearpathAPIError):
    def __init__(self, message: str) -> None:
        super().__init__(401, message)

class NotFoundError(ClearpathAPIError):
    def __init__(self, message: str) -> None:
        super().__init__(404, message)

class RateLimitError(ClearpathAPIError):
    def __init__(self) -> None:
        super().__init__(429, "Rate limit exceeded. Retry after X-RateLimit-Reset.")
```

Write to `clearpath_sdk/resources/projects.py`:

```python
from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from clearpath_sdk.client import ClearpathClient


class Project:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id: str = data["id"]
        self.title: str = data["title"]
        self.status: str = data["status"]
        self.owner_id: str = data["owner_id"]
        self.created_at: str = data["created_at"]

    def __repr__(self) -> str:
        return f"Project(id={self.id!r}, title={self.title!r}, status={self.status!r})"


class ProjectsResource:
    def __init__(self, client: ClearpathClient) -> None:
        self._client = client

    def list(self, page: int = 1, per_page: int = 50) -> list[Project]:
        """List all projects. Paginates automatically if page/per_page specified."""
        data = self._client._request("GET", "/projects", params={"page": page, "per_page": per_page})
        return [Project(p) for p in data["projects"]]

    def get(self, project_id: str) -> Project:
        """Retrieve a single project by ID."""
        data = self._client._request("GET", f"/projects/{project_id}")
        return Project(data)

    def create(self, title: str, status: str = "active", owner_id: str | None = None) -> Project:
        """Create a new project."""
        payload: dict[str, Any] = {"title": title, "status": status}
        if owner_id:
            payload["owner_id"] = owner_id
        data = self._client._request("POST", "/projects", json=payload)
        return Project(data)

    def update(self, project_id: str, **fields: Any) -> Project:
        """Update project fields. Accepts title, status, owner_id."""
        data = self._client._request("PATCH", f"/projects/{project_id}", json=fields)
        return Project(data)

    def delete(self, project_id: str) -> None:
        """Archive (soft-delete) a project."""
        self._client._request("DELETE", f"/projects/{project_id}")
```

Write to `README.md`:

```markdown
# Clearpath Python SDK

Python client for the Clearpath API.

### Installation

pip install clearpath-sdk
```

Then run:

/developer-docs-writer:write-sdk-guide for our Python SDK — it wraps our REST API and currently has no documentation beyond the README installation instructions.

Execution requirements (the SDK_GUIDE.md MUST include these sections and conventions):

- **Installation** — `pip install clearpath-sdk`, `Requirements: Python 3.10+`, AND a verification command on its own line: `python -c "import clearpath_sdk; print(clearpath_sdk.__version__)"` with expected output `1.2.0`.
- **Quickstart** — ≤15 lines of runnable Python. The client MUST be instantiated reading the API key from the environment, never as a hardcoded string. Use this exact pattern:
  ```python
  import os
  from clearpath_sdk import ClearpathClient

  client = ClearpathClient(api_key=os.environ["CLEARPATH_API_KEY"])
  projects = client.projects.list()
  for p in projects:
      print(p)
  ```
- **Sync vs Async** — a dedicated subsection. State explicitly: "The Clearpath SDK is **synchronous-only** in version 1.2.0. There is no async variant. For asyncio integration, wrap calls with `asyncio.to_thread(client.projects.list)`."
- **Method Reference** — per-method structured sections (NOT a single flat table). For each public method (`projects.list`, `projects.get`, `projects.create`, `projects.update`, `projects.delete`) include:
  - A heading like `### projects.list(page: int = 1, per_page: int = 50) -> list[Project]` with the type-annotated signature
  - Parameters subsection with name, type, default, description
  - Returns subsection with type and description
  - **Raises** subsection naming the SDK exceptions: `AuthenticationError` (401), `NotFoundError` (404), `RateLimitError` (429), `ClearpathAPIError` (other 4xx/5xx)
- **Authentication** — explain (1) env var `CLEARPATH_API_KEY` is the default, (2) optional `api_key=` constructor argument overrides, (3) missing credentials raises `AuthenticationError` with the verbatim message `"No API key provided. Pass api_key= or set CLEARPATH_API_KEY."`.
- **Common Patterns** — a dedicated section with subsections: pagination iteration, error handling using SDK-specific exception classes (not bare `except`), retry/timeout configuration, and a CRUD workflow example. Every example must be complete and copy-pasteable — no `...` placeholders.
- **Quality Checklist (mandatory final section)** — markdown checklist:
  ```
  - [ ] Quickstart runs end-to-end: `python examples/quickstart.py` → expected output `[Project(id=...), ...]`
  - [ ] Method reference example runs: `python examples/method_reference.py`
  - [ ] All examples in this guide were executed before publication
  - [ ] No hardcoded API keys appear in any example
  - [ ] All code blocks are syntactically valid Python (passes `python -c "ast.parse(open('example.py').read())"`)
  - [ ] All exception types referenced exist in `clearpath_sdk.exceptions`
  ```

## Criteria


- [ ] PASS: Skill requires a quickstart section that gets developers to a working example in 15 lines or fewer
- [ ] PASS: Skill requires a method reference section documenting each public method with parameters, return types, and exceptions
- [ ] PASS: Skill requires a research step — reading the actual SDK source before writing docs
- [ ] PASS: Skill requires installation instructions as a prerequisite before the quickstart
- [ ] PASS: All code examples must be syntactically correct and complete — no "..." placeholders in runnable code
- [ ] PASS: Skill includes a quality checklist that verifies examples actually work
- [ ] PARTIAL: Skill covers common patterns section with real-world usage examples beyond the quickstart — partial credit if examples are required but common patterns as a distinct section is not
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's quickstart section produces a working "first call" example in 15 lines or fewer of Python — install, import, instantiate client with API key from env, make one method call, print result
- [ ] PASS: Output's installation instructions cover `pip install <package>` plus the supported Python versions and any system prerequisites — and verifies the install works (e.g. `python -c "import package; print(package.__version__)"`)
- [ ] PASS: Output's method reference documents each public method — signature with type annotations, parameter descriptions, return type, and exceptions raised — in a structured per-method format (not a flat list)
- [ ] PASS: Output's code examples use real return-value handling — exception handling shown with the SDK's specific exception types, not bare `try/except` — so developers learn the right patterns
- [ ] PASS: Output's authentication section explains how the SDK reads credentials — env var by default, optional explicit constructor argument, and handling of missing credentials with the specific error raised
- [ ] PASS: Output's common-patterns section shows real workflows — pagination iteration, batch operations, async usage if supported, retry/timeout configuration — beyond the quickstart's single-call demo
- [ ] PASS: Output's quality checklist verifies each example runs by including the exact command (e.g. `python examples/quickstart.py`) and the expected output, with the rule that examples must be tested before publication
- [ ] PASS: Output's code examples are complete and copy-pasteable — no `...` ellipsis in runnable code, no placeholder imports, all variables either defined or marked as user-supplied with a clear convention
- [ ] PASS: Output's quickstart instantiates the client without revealing the API key in the file — e.g. `client = Client(api_key=os.environ['MYAPI_KEY'])` rather than a hardcoded string
- [ ] PARTIAL: Output addresses the difference between sync and async client variants if the SDK supports both, or explicitly notes that the SDK is sync-only
