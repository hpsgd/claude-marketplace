---
name: write-runbook
description: Write an operational runbook for a service, deployment, or incident response procedure.
argument-hint: "[service, procedure, or incident type]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a runbook for $ARGUMENTS using the mandatory structure below.

**Core principle: This runbook will be used by someone who has never done this procedure before, at 2am, while stressed.** Every decision must serve that reader. No assumed knowledge. No missing steps. No ambiguity.

## Step 1 — Research the procedure

Before writing, gather information:

1. Search the codebase for relevant scripts, deployment configs, infrastructure definitions using `Grep` and `Glob`
2. Identify the services, databases, and external dependencies involved
3. Find existing monitoring, alerting, and logging for the systems in question
4. Check for existing runbooks or documentation to avoid duplication

## Step 2 — Write the runbook

Use this exact structure. Every section is mandatory.

---

### Title

`[Procedure name] — Runbook`

### Overview

| Field | Value |
|---|---|
| **What this covers** | [one sentence] |
| **When to use** | [trigger conditions — alert name, symptom, or scheduled occasion] |
| **Estimated duration** | [time range for the full procedure] |
| **Risk level** | Low / Medium / High / Critical |
| **Last tested** | [date] |
| **Owner** | [team or person responsible for maintaining this runbook] |

### Prerequisites

A checklist of everything needed BEFORE starting. Be exhaustive:

```
- [ ] Access to [system] — how to get it: [link or instructions]
- [ ] CLI tool [name] installed — version [X]+ — install: `[command]`
- [ ] Environment variable [NAME] set — get it from: [location]
- [ ] VPN connected to [network] — connect: [instructions]
- [ ] Permissions: [specific role/group] in [system] — request via: [link]
- [ ] Communication channel open: [Slack channel / war room] — notify: [who]
```

Rules for prerequisites:
- Every tool must include the install command
- Every access requirement must include how to get access
- Every credential must include where to find it (never hardcode credentials)
- If a prerequisite takes more than 5 minutes to obtain, note it: "⏱ This may take [time] — request in advance"

### Procedure

Numbered steps. Each step MUST follow this format:

```
#### Step N: [what you're doing and why]

**Action:**
\`\`\`bash
[exact command to run — copy-pasteable, no placeholders without explanation]
\`\`\`

**Expected output:**
\`\`\`
[what you should see if this worked correctly]
\`\`\`

**If this fails:**
- Symptom: [what you might see instead]
- Likely cause: [why this happens]
- Fix: [what to do about it]
- If the fix doesn't work: [escalate to whom, or which step to go to]

**Checkpoint:** [how to confirm this step succeeded before moving on]
```

Rules for steps:
- **One action per step.** "Run the migration and restart the service" is two steps.
- **Every command must be copy-pasteable.** No `<placeholder>` without explaining what to substitute and how to find the value. Use this pattern: `export SERVICE_NAME=my-service  # Replace with the actual service name from: kubectl get services`
- **Every step needs expected output.** The operator must be able to confirm what they see matches what they should see.
- **Every step needs failure handling.** What could go wrong? What does it look like? What to do about it?
- **Include wait times.** If a step takes time, say so: "This typically takes 2-5 minutes. Do not proceed until you see [indicator]."
- **No jargon without definition.** If you must use a term the reader might not know, define it inline on first use.
- **Dangerous steps get warnings.** Prefix with: `⚠ WARNING: This step [modifies production data / causes downtime / is irreversible]. Double-check [what] before proceeding.`

### Verification

After the procedure is complete, verify the system is healthy:

```
#### Verification checklist

- [ ] Service is responding: `curl -s https://[endpoint]/health | jq .status` → should return `"ok"`
- [ ] Logs are clean: `[log command]` → no errors in the last 5 minutes
- [ ] Metrics are normal: [dashboard link] → [what to look for]
- [ ] Dependent services unaffected: [how to check]
- [ ] Users can perform [core action]: [how to test]
```

Every verification check must include the exact command to run and the expected result.

### Rollback

If the procedure fails or causes issues, how to undo it. This section is not optional — every runbook needs a rollback plan.

```
#### Rollback procedure

**When to rollback:** [specific conditions that trigger a rollback decision]
**Rollback window:** [how long after the procedure can you still roll back?]
**Data implications:** [will rollback cause data loss? What data?]

1. [Rollback step with exact command]
   Expected result: [what you should see]

2. [Next rollback step]
   Expected result: [what you should see]

#### After rollback
- [ ] Verify rollback succeeded: [how]
- [ ] Notify: [who needs to know]
- [ ] Create incident ticket: [where, with what information]
```

### Troubleshooting

Common issues that arise during or after this procedure, even if not directly caused by the steps:

```
#### [Problem description]
**Symptom:** [what you see]
**Cause:** [why it happens]
**Solution:**
\`\`\`bash
[fix command]
\`\`\`
**Prevention:** [how to avoid this in the future]
```

Include at minimum:
- The most common failure mode for this procedure
- What happens if the procedure is interrupted midway
- What happens if the procedure is run twice

### Escalation

| Condition | Escalate to | Contact | Expected response time |
|---|---|---|---|
| Procedure fails after troubleshooting | [team/person] | [Slack/phone/page] | [time] |
| Data loss suspected | [team/person] | [Slack/phone/page] | Immediate |
| Customer impact detected | [team/person] | [Slack/phone/page] | Immediate |
| Unsure whether to proceed | [team/person] | [Slack/phone/page] | [time] |

Include both primary and backup contacts. If the primary is unavailable, who is next?

### Appendix

- **Related runbooks:** [links to runbooks for related procedures]
- **Architecture context:** [brief description of the system architecture relevant to this procedure, or link to diagram]
- **Change log:** [when was this runbook last updated and why]

---

## Step 3 — Quality checks

Before finalising, verify against every rule:

| Check | Requirement |
|---|---|
| Copy-paste test | Could someone paste every command and have it work? |
| Failure coverage | Does every step have a "what if this fails" section? |
| No assumed knowledge | Could a new team member follow this on their first week? |
| Rollback exists | Is there a complete rollback procedure? |
| Escalation contacts | Are real people or teams listed, with contact methods? |
| Timing estimates | Does the reader know how long things should take? |
| Warnings present | Are destructive or irreversible steps clearly marked? |
| Verification complete | Can the operator confirm success at the end? |

## Rules

- Never write "the reader should know" or "this is straightforward." If it were straightforward, there wouldn't be a runbook.
- Prefer explicit over clever. `kubectl delete pod my-pod-name -n production` is better than a bash one-liner that constructs the pod name dynamically.
- Include the "why" for non-obvious steps. "Drain the node before upgrading (this ensures active connections are moved to healthy nodes)" is better than just "Drain the node."
- Test every command in the runbook if possible. If you cannot test, mark untested commands with `# UNTESTED — verify in staging first`.
- Never put credentials, tokens, or secrets in the runbook. Always reference where to find them.
- If a step requires judgement (e.g., "if the error count is high, consider scaling up"), define "high" with a specific number.
