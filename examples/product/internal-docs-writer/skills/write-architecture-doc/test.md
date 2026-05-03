# Test: Write architecture doc

Scenario: Testing whether the write-architecture-doc skill requires Mermaid diagrams, bounded context documentation, key decisions with rationale, and NFRs.

## Prompt

First, create the notification system source files:

```bash
mkdir -p src/notifications src/notifications/channels src/notifications/queue docs
```

Write to `src/notifications/__init__.py`:

```python
from notifications.service import NotificationService
from notifications.models import Notification, NotificationPreference

__all__ = ["NotificationService", "Notification", "NotificationPreference"]
```

Write to `src/notifications/models.py`:

```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class NotificationChannel(str, Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    PUSH = "push"


class NotificationPriority(str, Enum):
    HIGH = "high"      # Immediate delivery, bypasses quiet hours
    NORMAL = "normal"  # Standard delivery with quiet hours applied
    LOW = "low"        # Batched delivery (digest mode)


@dataclass(frozen=True)
class Notification:
    id: str
    user_id: str
    type: str           # e.g. "project.status_changed", "task.assigned", "comment.mention"
    title: str
    body: str
    priority: NotificationPriority
    channels: list[NotificationChannel]
    data: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""


@dataclass(frozen=True)
class NotificationPreference:
    user_id: str
    channel: NotificationChannel
    enabled: bool
    quiet_hours_start: str | None = None  # e.g. "22:00"
    quiet_hours_end: str | None = None    # e.g. "08:00"
    digest_mode: bool = False             # LOW priority: batch into daily digest
```

Write to `src/notifications/service.py`:

```python
from __future__ import annotations

from notifications.models import Notification, NotificationChannel
from notifications.queue import NotificationQueue
from notifications.channels.inapp import InAppChannel
from notifications.channels.email import EmailChannel
from notifications.channels.push import PushChannel


class NotificationService:
    """Entry point for dispatching notifications across all channels."""

    def __init__(self, queue: NotificationQueue) -> None:
        self._queue = queue
        self._channels = {
            NotificationChannel.IN_APP: InAppChannel(),
            NotificationChannel.EMAIL: EmailChannel(),
            NotificationChannel.PUSH: PushChannel(),
        }

    def send(self, notification: Notification) -> None:
        """Enqueue a notification for delivery. Applies preference filtering."""
        self._queue.enqueue(notification)

    def deliver(self, notification: Notification) -> dict[str, bool]:
        """Deliver a notification directly (called by queue worker)."""
        results = {}
        for channel in notification.channels:
            handler = self._channels.get(channel)
            if handler:
                results[channel] = handler.deliver(notification)
        return results
```

Write to `src/notifications/queue.py`:

```python
from __future__ import annotations

from collections import deque
from notifications.models import Notification


class NotificationQueue:
    """
    In-memory queue for development. Production uses Redis + Celery workers.
    Queue workers call NotificationService.deliver() for each dequeued notification.
    Dead-letter queue (DLQ) for failed deliveries after 3 retries.
    """

    def __init__(self) -> None:
        self._queue: deque[Notification] = deque()
        self._dlq: list[Notification] = []

    def enqueue(self, notification: Notification) -> None:
        self._queue.append(notification)

    def dequeue(self) -> Notification | None:
        return self._queue.popleft() if self._queue else None

    def move_to_dlq(self, notification: Notification) -> None:
        self._dlq.append(notification)
```

Write to `src/notifications/channels/email.py`:

```python
from __future__ import annotations

from notifications.models import Notification


class EmailChannel:
    """Sends notifications via email using SendGrid."""

    SENDGRID_TEMPLATE_MAP = {
        "project.status_changed": "d-abc123",
        "task.assigned": "d-def456",
        "comment.mention": "d-ghi789",
    }

    def deliver(self, notification: Notification) -> bool:
        template_id = self.SENDGRID_TEMPLATE_MAP.get(notification.type)
        if not template_id:
            return False
        # SendGrid API call here
        return True
```

Write to `src/notifications/channels/push.py`:

```python
from __future__ import annotations

from notifications.models import Notification


class PushChannel:
    """
    Sends push notifications via FCM (Android) and APNs (iOS).
    Device tokens stored in user_devices table.
    Silent push for LOW priority — updates badge count only.
    """

    def deliver(self, notification: Notification) -> bool:
        # FCM/APNs dispatch here
        return True
```

Write to `src/notifications/channels/inapp.py`:

```python
from __future__ import annotations

from notifications.models import Notification


class InAppChannel:
    """
    Stores in-app notifications in the notifications table.
    Frontend polls /api/notifications every 30s or subscribes via WebSocket.
    Unread count cached in Redis with TTL 5min.
    """

    def deliver(self, notification: Notification) -> bool:
        # DB insert here
        return True
```

Then run:

/internal-docs-writer:write-architecture-doc for our notification system — it handles in-app, email, and push notifications, with a queue-based delivery system and user preference management.

Execution requirements (the architecture doc MUST include these sections):

- **Research step with citations** — at the top, a "Research" or "Sources" subsection listing the file paths read (e.g. `src/notifications/service.py`, `src/notifications/channels/email.py`, `src/notifications/queue.py`, `src/notifications/models.py`). Cite source file paths inline throughout the document where you describe code-derived facts (e.g. `SENDGRID_TEMPLATE_MAP — see src/notifications/channels/email.py`).
- **Sequence diagram** — Mermaid `sequenceDiagram` for the dispatch flow with EVERY external provider as its own participant: `Caller`, `API`, `PreferencesSvc`, `Queue`, `Worker`, `InAppChannel`, `EmailChannel`, `PushChannel`, `SendGrid`, `FCM`, `APNs`, `Callback`. Show the external provider→callback step explicitly. Do not collapse external providers into self-calls.
- **Key Decisions with rejected alternatives** — for each decision document: Decision, Chosen approach, **Alternative considered** (named), **Why rejected** (reason), Rationale. E.g. "Queue-based delivery: chosen because external providers fail unpredictably. Alternative considered: synchronous dispatch. Rejected because caller latency couples to slowest provider and a SendGrid outage would block order placement." Provide at least 3 such decisions with explicit rejected alternatives.
- **Known Limitations with backlog links** — every limitation MUST link to a backlog item or issue. Use placeholder issue references like `BACKLOG-NOTIF-12: no retry policy on SendGrid 5xx` or `[GH-123]: preferences cache not invalidated on update` if no real tracker exists.
- **Preferences (first-class section)** — a dedicated section that includes (1) a channel × event-type matrix table (rows = event types like `project.status_changed`, `task.assigned`, `comment.mention`; columns = `IN_APP`, `EMAIL`, `PUSH`; cell = default + overridable), (2) opt-out enforcement statement at delivery time, AND (3) an explicit "Race Condition" subsection covering what happens when a preference change races with a notification already mid-flight (e.g. enqueued before opt-out, dequeued after — re-checked at deliver time, but cache TTL of 5min creates a stale window — document the resolution).
- **Observability section** — list specific metrics (`notification_delivery_rate`, `notification_queue_depth`, `notification_provider_error_rate{provider}`, `notification_dlq_growth`), named dashboards (`Notifications Overview`, `Provider Health`), and named alert conditions (`DLQ depth > 100 over 5min`, `Email provider error rate > 5%`, `Queue lag > 60s`).
- **Quality Checklist (mandatory final section)** — a markdown checklist:
  ```
  - [ ] All Mermaid diagrams render without syntax errors (validated in mermaid.live)
  - [ ] Every architectural decision references an ADR (or `ADR-TBD by YYYY-MM-DD`)
  - [ ] Every NFR has a numeric target and a measurement method
  - [ ] Every limitation links to a backlog item
  - [ ] Source code citations resolve to existing files
  ```

## Criteria


- [ ] PASS: Skill requires Mermaid diagrams for component architecture — not text descriptions of boxes and arrows
- [ ] PASS: Skill requires sequence diagrams for data flows — showing the temporal order of interactions, not just the components involved
- [ ] PASS: Skill documents key architectural decisions with rationale — why this approach was chosen, not just what was built
- [ ] PASS: Skill documents non-functional requirements (NFRs) — latency, throughput, availability — with specific targets
- [ ] PASS: Skill requires a research step before writing — reading existing code, configs, or ADRs
- [ ] PASS: Skill documents bounded contexts or system boundaries — what this system owns vs what it depends on externally
- [ ] PARTIAL: Skill documents known limitations or technical debt — partial credit if this section is mentioned but not required as mandatory
- [ ] PASS: Skill includes a quality checklist that verifies diagrams render and decisions are traceable
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's component architecture is rendered as a Mermaid graph — showing the in-app channel, email sender, push sender, queue, preferences service, and external providers (Sendgrid / FCM / APNs) — with arrows for control flow
- [ ] PASS: Output includes a Mermaid sequence diagram for the notification dispatch flow — caller → API → preferences check → queue → channel-specific worker → external provider → callback — showing temporal ordering, not just topology
- [ ] PASS: Output documents the bounded context — what the notification system OWNS (delivery decisions, channel routing, retry logic, audit) and what it DEPENDS ON (preferences service, user identity, message templates) — so consumers know the contract surface
- [ ] PASS: Output's NFR section has specific numeric targets — latency (p95 < 5s for in-app, < 60s for email/push), throughput (50K notifications/day at launch, 500K target), availability (99.9% uptime SLO) — not "fast" or "scalable"
- [ ] PASS: Output documents at least 3 key architectural decisions with rationale — e.g. "queue-based delivery: chosen over synchronous because external providers fail unpredictably; allows retries without affecting the caller", with the alternative considered and why it was rejected
- [ ] PASS: Output's known-limitations section is mandatory — naming current debt (e.g. "no retry policy on Sendgrid 5xx; deliveries are dropped after 1 attempt", "preferences cache is not invalidated on update") with a link to backlog items
- [ ] PASS: Output's research step shows evidence — read existing code, ADRs, configs — with citations (file paths) so the reader can verify the documentation matches reality
- [ ] PASS: Output's quality checklist verifies Mermaid diagrams render without syntax errors AND that every architectural decision has a referenced ADR (or "to be written" with a date)
- [ ] PASS: Output addresses preferences as a first-class concern — channel × event-type matrix, opt-out enforcement at delivery time, and what happens when a preference change races with a notification mid-flight
- [ ] PARTIAL: Output addresses observability — what metrics are emitted (delivery rate, queue depth, provider error rate), which dashboards exist, and which alerts fire
