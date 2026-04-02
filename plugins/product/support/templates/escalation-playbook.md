# Escalation Playbook

## Severity Definitions

| Severity | Description | Response Target | Resolution Target | Example |
|----------|-------------|:---------------:|:-----------------:|---------|
| **SEV-1** | Critical — service down, data loss, security breach | 15 min | 4 hours | Production outage affecting all users |
| **SEV-2** | Major — significant degradation, no workaround | 30 min | 8 hours | Core feature broken for a segment of users |
| **SEV-3** | Moderate — impaired functionality, workaround exists | 2 hours | 48 hours | Non-critical feature broken, workaround documented |
| **SEV-4** | Low — minor issue, cosmetic, feature request | 24 hours | Next sprint | UI glitch, documentation error |

## Escalation Matrix

| Severity | Infrastructure | Application | Security | Billing | Data |
|----------|---------------|-------------|----------|---------|------|
| **SEV-1** | On-call SRE + VP Eng | On-call Dev + Eng Manager | Security Lead + CISO | Billing Lead + CFO | Data Lead + DPO |
| **SEV-2** | On-call SRE | Owning team lead | Security Lead | Billing Lead | Data Lead |
| **SEV-3** | SRE queue | Owning team | Security queue | Billing queue | Data queue |
| **SEV-4** | Backlog | Backlog | Backlog | Backlog | Backlog |

## Communication Templates

### SEV-1 — Critical

**Internal notification (Slack/PagerDuty):**
> [SEV-1] [Service] — [Brief description]. Incident commander: [Name]. War room: [Link]. Status: Investigating.

**Customer update (within 15 min):**
> We are aware of an issue affecting [service/feature]. Our team is actively investigating. We will provide an update within [30 minutes]. Status page: [Link].

**Resolution notice:**
> The issue affecting [service/feature] has been resolved as of [time UTC]. Root cause: [brief]. Duration: [X hours]. We will publish a full post-incident review within 48 hours.

### SEV-2 — Major

**Internal notification:**
> [SEV-2] [Service] — [Brief description]. Owner: [Team]. Tracking: [Ticket link].

**Customer update:**
> We are investigating reports of [issue]. A subset of users may experience [symptom]. We are working on a fix and will update you within [1 hour].

**Resolution notice:**
> [Issue] has been resolved. [Brief explanation]. No further action is required on your end.

### SEV-3/4 — Moderate/Low

**Customer update:**
> Thank you for reporting this. We have logged [ticket ID] and our team will address it in [timeframe]. Workaround: [steps if applicable].

## Override Process

Severity can be overridden by:

1. **Upgrade:** Any engineer or support agent can upgrade severity at any time — no approval required.
2. **Downgrade:** Requires approval from the incident commander (SEV-1/2) or team lead (SEV-3/4).
3. **Audit:** All severity changes are logged with reason and approver in the incident record.

## Post-Incident

- SEV-1/2: Blameless post-incident review within 48 hours
- SEV-3: Retrospective note added to sprint review
- SEV-4: No formal review required
