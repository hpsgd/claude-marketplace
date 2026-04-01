# Event Tracking Specification Template

Based on Segment's Tracking Plan format and Amplitude's taxonomy best practices.

---

## Event: {event_name}

### Metadata
- **Name:** {`snake_case` verb_noun — e.g., `report_viewed`, `search_performed`}
- **Category:** {user_action / system_event / lifecycle / error}
- **Purpose:** {What business question does this event answer?}
- **Owner:** {Who maintains this event definition}
- **Status:** Draft | Active | Deprecated

### Trigger
- **When fired:** {Exact condition — e.g., "When a user clicks the 'Generate Report' button AND the report renders successfully"}
- **Where instrumented:** {Client-side / server-side / both}
- **Deduplication:** {How to handle duplicate events — e.g., "Dedupe by user_id + event_name within 1 second window"}

### Properties

| Property | Type | Required | Example | Description |
|---|---|---|---|---|
| `user_id` | string | Yes | `usr_abc123` | Authenticated user identifier |
| `session_id` | string | Yes | `ses_xyz789` | Session identifier |
| `timestamp` | ISO 8601 | Yes | `2026-04-02T10:00:00Z` | Event timestamp (server time) |
| {custom_property} | {type} | {yes/no} | {example value} | {what it represents} |

### Standard Properties (included on ALL events)

| Property | Type | Source | Description |
|---|---|---|---|
| `user_id` | string | Auth context | Authenticated user |
| `anonymous_id` | string | Cookie/device | Pre-auth identifier |
| `session_id` | string | Session manager | Current session |
| `timestamp` | ISO 8601 | Server clock | Event time |
| `platform` | string | User agent | `web` / `ios` / `android` |
| `app_version` | string | Build config | Application version |

### Volume Estimate
- **Expected volume:** {events/day}
- **Growth factor:** {how volume scales — e.g., "Linear with user count"}
- **Storage impact:** {approximate bytes/event × volume}

### Privacy and Compliance
- **Contains PII:** {Yes/No — if yes, list which properties}
- **Retention policy:** {How long this data is kept}
- **Consent required:** {Which consent category — analytics / marketing / functional}
- **Anonymisation:** {How to anonymise for data exports}

### Consumers
- {Dashboard/report that uses this event}
- {Downstream pipeline that processes this event}
- {Alert that triggers on this event}

### Related Events
- **Precedes:** {Events that typically follow this one}
- **Follows:** {Events that typically precede this one}
- **Correlated with:** {Events that co-occur — for funnel/sequence analysis}
