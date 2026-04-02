# Runbook: [Service Name]

| Field          | Value                     |
|----------------|---------------------------|
| Owner          | [Team / individual]       |
| Last Verified  | YYYY-MM-DD                |
| On-Call Contact| [Slack channel / PagerDuty escalation policy] |

---

## Service Overview

**What it does:**
[One-paragraph description of the service's purpose and core responsibility.]

**Architecture diagram:** [Link to diagram]

**Dependencies:**

| Direction  | Service           | Protocol | Failure Impact                  |
|------------|-------------------|----------|---------------------------------|
| Upstream   | [Service name]    | gRPC/HTTP| [What breaks if this is down]   |
| Downstream | [Service name]    | HTTP/SQL | [What breaks if we are down]    |

---

## Health Checks

| Check          | URL / Command                  | Expected Response         | Interval |
|----------------|--------------------------------|---------------------------|----------|
| Liveness       | `GET /healthz`                 | 200 OK                    | 10s      |
| Readiness      | `GET /readyz`                  | 200 OK                    | 10s      |
| Deep health    | `GET /healthz?full=true`       | 200 with all deps healthy | 60s      |

---

## Common Alerts & Response

| Alert Name                | Severity | Meaning                           | Response Steps |
|---------------------------|----------|-----------------------------------|----------------|
| [HighErrorRate]           | P1       | [Error rate exceeds 5% for 5min]  | 1. Check logs: `[command]` 2. Check deps: `[command]` 3. If deployment-related, rollback 4. Escalate if unresolved in 15min |
| [HighLatency]             | P2       | [p99 latency > threshold]         | 1. Check resource utilisation 2. Look for slow queries 3. Consider scaling |
| [DiskSpaceLow]            | P3       | [Disk usage > 85%]                | 1. Identify large files: `du -sh /var/log/*` 2. Rotate logs 3. Expand volume if needed |

---

## Scaling Procedures

**Scale up:** `kubectl scale deployment [name] --replicas=[N]`

**Scale down:** `kubectl scale deployment [name] --replicas=[N]`

**When to scale:** [Describe CPU/memory/queue-depth thresholds that trigger scaling decisions.]

**Auto-scaling config:** [Reference HPA/auto-scaling policy if applicable.]

---

## Deployment Procedures

**Deploy:** `[deploy command or CI/CD pipeline link]`

**Verify:** `[smoke test or verification command]`

**Rollback:** `[rollback command — must be copy-pasteable under pressure]`

---

## Data Recovery

| Item            | Value                                           |
|-----------------|-------------------------------------------------|
| Backup location | [S3 bucket / snapshot ID / backup service]       |
| Backup schedule | [e.g., daily at 02:00 UTC]                       |
| RPO             | [Maximum acceptable data loss, e.g., 1 hour]     |
| RTO             | [Maximum acceptable downtime, e.g., 30 minutes]  |

**Restore procedure:** `[Step-by-step restore commands]`

---

## Useful Commands

| Task                    | Command                          |
|-------------------------|----------------------------------|
| View recent logs        | `[command to tail logs]`         |
| Check resource usage    | `[command to check CPU/memory]`  |
| Connect to database     | `[command to open DB shell]`     |
| Check queue depth       | `[command to inspect queue]`     |
| Force restart           | `[command to restart service]`   |

---

## Escalation Path

| Severity | Contact                  | Response Time | Method       |
|----------|--------------------------|---------------|--------------|
| P1       | [On-call engineer]       | 15 min        | PagerDuty    |
| P2       | [Team lead]              | 1 hour        | Slack        |
| P3       | [Team channel]           | Next business day | Slack    |
| P1 (unresolved > 30min) | [Engineering manager] | Immediate | Phone  |

---

## Revision History

| Date       | Author | Change                        |
|------------|--------|-------------------------------|
| YYYY-MM-DD | [Name] | Initial runbook creation      |
| YYYY-MM-DD | [Name] | [Description of change]       |
