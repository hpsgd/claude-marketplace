# Test: Write runbook

Scenario: Testing whether the write-runbook skill requires copy-pasteable commands, rollback steps for every destructive action, and an escalation table with specific contacts.

## Prompt

First, create the database infrastructure context:

```bash
mkdir -p infrastructure/database docs/runbooks
```

Write to `infrastructure/database/topology.md`:

```markdown
# Database Topology

### Primary Instance
- Host: db-primary.internal (10.0.1.10)
- Engine: PostgreSQL 15.4
- Instance: db.r6g.2xlarge (8 vCPU, 64 GB RAM)
- Storage: 2 TB gp3, multi-AZ enabled
- Region: ap-southeast-2 (Sydney)

### Read Replica
- Host: db-replica-1.internal (10.0.1.11)
- Replication lag: typically <500ms
- Promotes automatically via RDS Multi-AZ (but manual procedure needed for cross-AZ failover)
- Read endpoint DNS: db-readonly.internal (always points to current replica)

### Application Connection
- App reads from: db-readonly.internal (connection pool: PgBouncer, 10.0.1.20)
- App writes to: db-primary.internal (direct, no proxy)
- Connection pool size: 50 write, 200 read

### Monitoring
- Primary health check: AWS CloudWatch `DatabaseConnections` metric
- Replication lag: CloudWatch `ReplicaLag` metric
- Alert channel: #ops-alerts (Teams)
- On-call rotation: PagerDuty, escalation to DB team lead (James Cho, +61 400 000 000)
```

Write to `infrastructure/database/failover-history.md`:

```markdown
# Failover History

| Date | Duration | Root Cause | Performed By |
|---|---|---|---|
| 2024-11-03 | 8 min | Primary disk I/O saturation | Sarah Mitchell |
| 2024-07-22 | 14 min | AZ outage (ap-southeast-2b) | Auto + James Cho |
| 2024-02-11 | 22 min | Unplanned major version upgrade | Dev team |

Lessons learned:
- Step 4 (update DNS) must happen BEFORE app restart or connections fail for 5-10 min
- Always verify replication lag < 1s before promoting or data loss is possible
- PgBouncer must be restarted after DNS update — it caches the old IP
```

Then run:

/internal-docs-writer:write-runbook for our database failover procedure — promoting the read replica to primary when the primary instance becomes unavailable.

## Criteria


- [ ] PASS: Skill is explicitly written for a first-timer at 2am — no assumed knowledge, all commands copy-pasteable with expected output shown
- [ ] PASS: Every command includes the expected output so the engineer knows whether it worked
- [ ] PASS: Skill requires a rollback step for every destructive or hard-to-reverse action
- [ ] PASS: Skill requires an escalation table with named roles, contact methods, and when to escalate — not "escalate if needed"
- [ ] PASS: Skill requires a verification step at the end — how to confirm the runbook succeeded and the system is healthy
- [ ] PASS: Skill requires a research step — reading existing code, configs, or infrastructure before writing the runbook
- [ ] PARTIAL: Skill requires severity classification or impact context at the top — partial credit if business impact is mentioned but not required as a runbook header field
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's runbook is specifically for promoting a read replica to primary — not generic database recovery — with the exact failover commands for the project's stack (likely PostgreSQL, named provider)
- [ ] PASS: Output's first section answers "is this the right runbook?" — primary unavailable confirmed via specific health check (e.g. `pg_isready -h primary`), not on a planned maintenance, not on a transient network blip — with a 60-second wait + retry rule
- [ ] PASS: Output's commands are exact and copy-pasteable — full host/instance names as parameters or placeholders flagged with $VAR syntax, not "your primary database"; expected output shown after each command
- [ ] PARTIAL: Output's promotion step shows what success looks like — verification queries showing the new primary is accepting traffic and the application can connect; database-specific checks (e.g. replication lag = N/A) are bonus, not required
- [ ] PASS: Output's rollback step covers the case where the original primary recovers — how to safely re-introduce it (as a replica, after re-syncing) without split-brain, including the "do not promote both" warning
- [ ] PASS: Output's escalation table has named contacts — DBA on-call (PagerDuty service `database-oncall`), platform engineering, vendor support contact (e.g. AWS RDS support case URL) — not "escalate as needed"
- [ ] PASS: Output's escalation conditions are specific — "if replication lag was >5 minutes at failover time, escalate to DBA before accepting writes (data may be lost)", "if promotion fails, escalate to vendor support immediately"
- [ ] PARTIAL: Output's verification step at the end confirms full health — application can read AND write, monitoring shows healthy; restoring redundancy (e.g. setting up a new replica so the system isn't running solo) is bonus, not required
- [ ] PASS: Output's research evidence is shown — refers to existing config files, AWS RDS / cloud provider documentation, ADR for failover policy — not invented procedure
- [ ] PARTIAL: Output's severity / impact header notes the business impact (e.g. "primary unavailable = full write outage; expected RTO 5-15 min") so the on-call sets urgency correctly
