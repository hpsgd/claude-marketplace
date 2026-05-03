# Test: Write integration guide

Scenario: Testing whether the write-integration-guide skill requires numbered steps with expected output, a complete runnable example, and a troubleshooting section.

## Prompt

First, set up the project context:

```bash
mkdir -p docs/integrations src/integrations
```

Write to `docs/integrations/clearpath-api-overview.md`:

```markdown
# Clearpath API Overview

Base URL: https://api.clearpath.io/v2

### Authentication
All requests require Bearer token authentication.
- Header: `Authorization: Bearer <api_token>`
- Tokens created in Settings → API → Personal Access Tokens
- Scopes: `projects:read`, `projects:write`, `members:read`

### Key Endpoints
- `GET /projects` — list all projects
- `POST /projects` — create a project
- `PATCH /projects/{id}` — update project fields (title, status, owner)
- `POST /webhooks` — register a webhook for project events
- `DELETE /webhooks/{id}` — remove a webhook

### Project Status Values
`active` | `on_hold` | `completed` | `archived`

### Webhook Events
Fires on: `project.created`, `project.status_changed`
Payload: `{ event, project_id, project_title, new_status, timestamp }`

### Rate Limits
100 requests/minute. Headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`
```

Write to `docs/integrations/salesforce-setup.md`:

```markdown
# Salesforce Connected App Setup

1. Salesforce Setup → App Manager → New Connected App
2. Enable OAuth: Callback URL `https://app.clearpath.io/integrations/salesforce/callback`, scopes: `api`, `refresh_token`
3. Note Consumer Key (client_id) and Consumer Secret (client_secret)
4. Clearpath Settings → Integrations → Salesforce: enter client_id and client_secret

Salesforce Opportunity fields:
- `Id` → Clearpath project `external_id`
- `Name` → project title
- `StageName` → Clearpath status: Closed Won → `completed`, Closed Lost → `archived`, all others → `active`
- `OwnerId` → project owner
```

Then run:

/developer-docs-writer:write-integration-guide for connecting Clearpath to Salesforce — syncing deal status from Salesforce opportunities to Clearpath projects automatically.

## Criteria


- [ ] PASS: Skill requires numbered steps — not bullet points — so developers can follow sequentially and know exactly where they are
- [ ] PASS: Each step includes the expected output or visible result after completion, not just the action
- [ ] PASS: Skill requires a complete runnable end-to-end example that exercises the full integration
- [ ] PASS: Skill requires a troubleshooting section covering common failure modes with specific fixes
- [ ] PASS: Skill requires a prerequisites section before the integration steps begin
- [ ] PASS: Skill requires a research step — understanding both systems before writing the guide
- [ ] PARTIAL: Skill covers how to verify the integration is working correctly — partial credit if verification is embedded in steps but not a dedicated section
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's prerequisites section names what the developer needs before starting — Salesforce admin access (with required permissions like API enabled, Connected App permission), Clearpath admin role, OAuth credentials (Salesforce Connected App client_id/client_secret) — explicit, not assumed
- [ ] PASS: Output's steps are numbered (1, 2, 3...) — not bullet points — so the developer can follow sequentially and report which step failed
- [ ] PASS: Output's steps each include expected output / visible result — e.g. "Step 4 expected: you should see 'Connection verified ✓' in the Clearpath integrations panel" — not just the action to perform
- [ ] PASS: Output's complete runnable example covers an end-to-end deal-status sync — creating or updating a Salesforce opportunity, observing the Clearpath project status update — with the full flow demonstrable in a sandbox
- [ ] PASS: Output's troubleshooting section covers at least 4 common failure modes — each with the symptom, the cause, and a specific fix
- [ ] PASS: Output's verification section (or embedded verification per step) explains how the developer confirms the integration is working — specific test data, expected behaviour, what to check
