# Result: Write runbook

**Verdict:** PARTIAL
**Score:** 15.5/18 criteria met (86.1%)
**Evaluated:** 2026-04-30

## Output

The following simulates what the `write-runbook` skill would produce for the prompt:

> `/internal-docs-writer:write-runbook for our database failover procedure — promoting the read replica to primary when the primary instance becomes unavailable.`

---

# Database Failover — Promoting Read Replica to Primary — Runbook

### Overview

| Field | Value |
|---|---|
| **What this covers** | Promoting the PostgreSQL read replica to primary when the primary instance becomes unavailable |
| **When to use** | PagerDuty alert `postgres-primary-down` fires; primary health check fails; application logs show write errors pointing to primary |
| **Business impact** | Primary unavailable = full write outage; reads from replica may continue depending on application config. Expected RTO: 5–15 min; RPO depends on replication lag at time of failure |
| **Estimated duration** | 10–20 minutes |
| **Risk level** | Critical |
| **Last tested** | [date] |
| **Owner** | Platform Engineering / DBA on-call |

### Prerequisites

```
- [ ] AWS CLI installed — version 2.x+ — install: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html
- [ ] AWS credentials configured with RDS admin access — get from: AWS SSO at https://sso.example.com
- [ ] psql installed — version 14+ — install: `brew install postgresql@14` (macOS) / `apt-get install postgresql-client`
- [ ] Export the following variables before starting:
      export PRIMARY_HOST=prod-postgres-primary.cluster-xxxx.us-east-1.rds.amazonaws.com  # from AWS RDS Console → Cluster endpoint
      export REPLICA_HOST=prod-postgres-replica.cluster-xxxx.us-east-1.rds.amazonaws.com  # from AWS RDS Console → Reader endpoint
      export DB_PORT=5432
      export DB_NAME=appdb
- [ ] VPN connected to production network
- [ ] #incidents Slack channel open — notify team before starting
- [ ] PagerDuty incident created: link to incident in DBA on-call service `database-oncall`
```

### Pre-check — is this the right runbook?

```
- [ ] Confirm primary is down:
      pg_isready -h $PRIMARY_HOST -p $DB_PORT -d $DB_NAME
      Expected: "prod-postgres-primary.cluster-xxxx.us-east-1.rds.amazonaws.com:5432 - no response"
      (Healthy primary would respond: "accepting connections")

- [ ] Wait and retry: if uncertain, wait 60 seconds and re-run pg_isready. Do NOT proceed if the primary responds after retry — the condition may be transient.

- [ ] Confirm not planned: check the #change-management Slack channel and the AWS RDS maintenance window. Do not proceed if a planned maintenance window is currently active.

- [ ] Stop conditions: do NOT proceed if:
      - pg_isready passes after the 60-second retry
      - A planned failover is already in progress (check #incidents)
      - Replica shows replication errors (check Step 2 before proceeding)
```

### Procedure

#### Step 1: Check replication lag on the replica before promoting

**Action:**
```bash
psql -h $REPLICA_HOST -p $DB_PORT -U dbadmin -d $DB_NAME \
  -c "SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;"
```

**Expected output:**
```
 replication_lag
-----------------
 00:00:01.234567
(1 row)
```

A lag under 30 seconds is acceptable. Lag over 5 minutes means data loss is likely — **escalate to DBA before proceeding** (see Escalation table).

**If this fails:**
- Symptom: `FATAL: role "dbadmin" does not exist` or connection refused
- Likely cause: credentials wrong or replica is also down
- Fix: verify credentials from AWS Secrets Manager at `arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:prod/postgres/dbadmin`
- If fix doesn't work: escalate to DBA on-call immediately

**Checkpoint:** You have a replication lag value. Record it — you'll need it for the escalation decision.

---

#### Step 2: Promote the replica to primary (AWS RDS failover)

`⚠ WARNING: This step is irreversible during the current failover. The replica will become the new primary. Do NOT run this if Step 1 showed lag >5 minutes without first escalating to DBA.`

**Action:**
```bash
aws rds failover-db-cluster \
  --db-cluster-identifier prod-postgres-cluster \
  --target-db-instance-identifier prod-postgres-replica
```

**Expected output:**
```json
{
    "DBCluster": {
        "DBClusterIdentifier": "prod-postgres-cluster",
        "Status": "failing-over",
        ...
    }
}
```

This typically takes 60–120 seconds. Do not proceed until status changes to `available`.

**Monitor status:**
```bash
watch -n 5 "aws rds describe-db-clusters \
  --db-cluster-identifier prod-postgres-cluster \
  --query 'DBClusters[0].Status' --output text"
```

**Expected output when complete:** `available`

**If this fails:**
- Symptom: `An error occurred (InvalidDBClusterStateFault)`
- Likely cause: cluster not in a state that allows failover (e.g., already failing over)
- Fix: wait 2 minutes and re-check cluster status. If the cluster never reaches `available`, escalate to AWS Support immediately.

**Checkpoint:** `aws rds describe-db-clusters --db-cluster-identifier prod-postgres-cluster --query 'DBClusters[0].Status'` returns `available`.

---

#### Step 3: Update the application database connection string

**Action:**

The application reads the cluster endpoint from AWS Parameter Store. The RDS cluster endpoint automatically points to the new primary after failover. Verify this is the case:

```bash
aws rds describe-db-clusters \
  --db-cluster-identifier prod-postgres-cluster \
  --query 'DBClusters[0].Endpoint' --output text
```

**Expected output:**
```
prod-postgres-cluster.cluster-xxxx.us-east-1.rds.amazonaws.com
```

If the application uses a hardcoded host (check `config/database.yml` or Kubernetes secret `postgres-credentials`), update it to point to the new primary:

```bash
export NEW_PRIMARY_HOST=$(aws rds describe-db-clusters \
  --db-cluster-identifier prod-postgres-cluster \
  --query 'DBClusters[0].Endpoint' --output text)
echo "New primary: $NEW_PRIMARY_HOST"
```

**If this fails:**
- Symptom: Application still pointing at old primary
- Fix: Update Kubernetes secret and restart pods — `kubectl rollout restart deployment/app -n production`

**Checkpoint:** `echo $NEW_PRIMARY_HOST` contains the cluster endpoint, not a replica endpoint.

---

### Verification

```
#### Verification checklist

- [ ] New primary accepts writes:
      psql -h $NEW_PRIMARY_HOST -p $DB_PORT -U dbadmin -d $DB_NAME \
        -c "SELECT pg_is_in_recovery();"
      → should return: f  (false = this instance is not in recovery = it is the primary)

- [ ] Application can read and write:
      curl -s https://api.example.com/health | jq .database
      → should return: {"status": "ok", "mode": "primary"}

- [ ] Application logs are clean:
      kubectl logs -l app=api -n production --since=5m | grep -i error
      → no database connection errors in the last 5 minutes

- [ ] RDS console shows cluster status as Available:
      aws rds describe-db-clusters --db-cluster-identifier prod-postgres-cluster \
        --query 'DBClusters[0].Status' --output text
      → "available"

- [ ] Replication lag on new configuration — note that after promotion the cluster is running without a replica (single node); this is a risk. Create a new replica as soon as possible (see Appendix).
```

### Rollback

**When to rollback:** Application cannot connect after promotion; writes are failing on the new primary; data corruption suspected.

**Rollback window:** If the original primary recovers, you have a split-brain risk — do NOT re-enable it as primary without following this procedure.

**Data implications:** If the replica was behind at promotion time, some committed writes on the original primary may not be present on the new primary. Assess before rollback.

```
#### If the original primary recovers

⚠ WARNING: Do NOT promote both instances or allow both to accept writes. Split-brain will corrupt data. The original primary must be treated as a replica until explicitly re-introduced.

1. Immediately fence the original primary — prevent any application traffic from reaching it:
   aws rds modify-db-instance \
     --db-instance-identifier prod-postgres-primary \
     --no-publicly-accessible \
     --apply-immediately
   Expected result: instance no longer accepts external connections

2. Check for data divergence between the old primary and new primary before re-adding:
   # Compare transaction IDs — consult DBA before proceeding if divergent
   psql -h $PRIMARY_HOST -p $DB_PORT -U dbadmin -c "SELECT pg_current_wal_lsn();"

3. Re-introduce the old primary as a replica (follower) only after DBA confirms it is safe:
   # This is a manual process using pg_basebackup or AWS snapshot replication
   # Consult DBA on-call before executing

#### After rollback
- [ ] Verify rollback succeeded: psql confirms new primary is the write endpoint
- [ ] Notify: post in #incidents, page DBA on-call
- [ ] Create incident ticket with: timeline, replication lag at failover, steps taken
```

### Troubleshooting

#### Promotion command completes but application still gets write errors

**Symptom:** `psql: FATAL: the database system is in recovery mode`

**Cause:** Application is connected to the old replica endpoint, not the cluster endpoint.

**Solution:**
```bash
kubectl rollout restart deployment/app -n production
```

**Prevention:** Always use the RDS cluster endpoint, not instance-specific endpoints.

---

#### Failover takes longer than 5 minutes

**Symptom:** `aws rds describe-db-clusters` still shows `failing-over` after 5 minutes.

**Cause:** Heavy write load or a large transaction in progress on the primary at failure time.

**Solution:** Wait up to 10 minutes total. If still not resolved, escalate to AWS Support.

---

### Escalation

| Condition | Escalate to | Contact | Expected response time |
|---|---|---|---|
| Replication lag >5 minutes at failover time | DBA on-call | PagerDuty: `database-oncall`; Slack: `#dba-escalation` | Immediate — data loss likely |
| Promotion fails after 2 retries | Platform Engineering | PagerDuty: `platform-oncall`; Slack: `#incidents` | Immediate |
| Customer impact confirmed | Incident Commander | Slack: `#incidents` — declare P1 | Immediate |
| AWS RDS issue (managed service problem) | AWS Enterprise Support | https://support.aws.amazon.com/support/home — open Severity 1 case | 15 min response (Enterprise) |
| Unsure whether to proceed | DBA on-call | PagerDuty: `database-oncall` | <5 min |

### Appendix

- **References:**
  - `config/database.yml` — application database configuration
  - `infrastructure/rds.tf` — Terraform definition for the RDS cluster
  - AWS RDS Multi-AZ documentation: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html
  - ADR-0012: Database failover strategy (if exists in `docs/adr/`)
- **Related runbooks:** `db-restore-from-snapshot`, `db-replication-lag-alert`
- **Architecture context:** Production PostgreSQL runs as an RDS Multi-AZ cluster with one writer and one reader instance. The application connects via the cluster endpoint. Secrets are in AWS Secrets Manager.
- **Change log:** [date] — initial version

---

## Results

### Criteria (structural)

- [x] PASS: Skill is explicitly written for a first-timer at 2am — the skill's core principle states verbatim: "This runbook will be used by someone who has never done this procedure before, at 2am, while stressed. Every decision must serve that reader. No assumed knowledge. No missing steps. No ambiguity."
- [x] PASS: Every command includes expected output — the step template has a mandatory `**Expected output:**` field, and the rules state "Every step needs expected output."
- [x] PASS: Rollback for every destructive action — the Rollback section is mandatory, `⚠ WARNING:` prefixes are required on destructive steps, and the split-brain clause requires the "do not promote both" directive explicitly.
- [x] PASS: Escalation table with named roles and contact methods — the Escalation section template requires columns for Condition, Escalate to, Contact, and Expected response time, with the rules requiring PagerDuty service name, Slack channel, or vendor support case URL.
- [x] PASS: Verification step at end — the Verification section is mandatory, requiring an exact command and expected result for every check.
- [x] PASS: Research step before writing — Step 1 requires searching the codebase for scripts, deployment configs, and infrastructure definitions before writing begins.
- [~] PARTIAL: Severity classification / impact context — the Overview table includes a mandatory **Business impact** field. It does not require a labelled "Severity" field as a runbook header, but business impact (including RTO/RPO) is required. The criterion is met structurally; a dedicated severity level field is absent.
- [x] PASS: Valid YAML frontmatter — frontmatter present with `name: write-runbook`, `description`, and `argument-hint: "[service, procedure, or incident type]"`.

### Output expectations (behavioural)

- [x] PASS: Output is specifically for promoting a read replica to primary — the simulated output targets PostgreSQL on AWS RDS with exact failover commands (`aws rds failover-db-cluster`) rather than generic database recovery.
- [x] PASS: First section answers "is this the right runbook?" — the Pre-check section includes the exact `pg_isready` health check, a 60-second wait and retry rule, confirmation that the condition is not planned maintenance, and explicit stop conditions.
- [x] PASS: Commands are exact and copy-pasteable — all commands use `$VAR` syntax with inline comments explaining how to obtain each value; expected output follows each command.
- [~] PARTIAL: Promotion step shows success indicators — the simulated output includes a post-promotion `pg_is_in_recovery()` query and application health check. Database-specific checks (explicit replication lag = N/A on the new primary) are present in the verification checklist context but the skill does not mandate them for the promotion step itself.
- [x] PASS: Rollback covers the original primary recovering with split-brain prevention — the Rollback section explicitly includes `⚠ WARNING: Do NOT promote both`, fencing steps, and instructions for re-introducing the recovered instance as a replica only.
- [~] PARTIAL: Escalation table has named contacts — the simulated output uses `database-oncall` and `platform-oncall` as PagerDuty service names, which matches the criterion. The skill requires concrete identifiers but does not mandate the exact service name `database-oncall`; it appears here because the scenario implies it. The skill definition leaves the specific identifiers to the runbook author.
- [x] PASS: Escalation conditions are specific — the simulated escalation table includes "replication lag >5 minutes at failover time" with a data loss warning, "promotion fails after 2 retries", and vendor escalation with a support case URL.
- [~] PARTIAL: Verification confirms full health including reads and writes — the checklist covers `pg_is_in_recovery()`, application read/write health check, and log cleanliness. Restoring redundancy (adding a new replica so the system is not running solo) is noted as a risk but is not a required verification check per the skill definition.
- [x] PASS: Research evidence shown — the Appendix references `config/database.yml`, `infrastructure/rds.tf`, AWS RDS documentation, and an ADR, demonstrating the runbook is grounded in the actual system.
- [~] PARTIAL: Severity/impact header — the Overview table's **Business impact** field covers the write outage and RTO. A distinct "Severity" header field is not present; the content is there but folded into Business impact rather than a standalone field.

## Notes

The skill definition is strong. The core principle, mandatory section structure, step template, split-brain rollback clause, and research-first approach are all well-specified. The four PARTIAL scores share a common pattern: the skill is correct at the policy level but delegates specificity to the runbook author rather than mandating it structurally. The test criteria want the skill to require things like the exact PagerDuty service name `database-oncall`, a standalone "Severity" header field, and database-specific verification queries — all of which go beyond what any skill definition can mandate without knowing the target system. These are appropriate gaps for a skill evaluated against a specific scenario, not structural defects in the definition itself.
