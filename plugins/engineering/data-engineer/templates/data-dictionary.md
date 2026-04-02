# Data Dictionary: [table_name]

| Field        | Value                          |
|--------------|--------------------------------|
| Schema       | [e.g., public, analytics]      |
| Database     | [e.g., production_db]          |
| Owner        | [Team or individual]           |
| Last Updated | YYYY-MM-DD                     |

---

## Description

[What this table represents in business terms. Explain why it exists, what process produces it, and what decisions it supports. Avoid purely technical descriptions — a product manager should understand this paragraph.]

---

## Column Inventory

| Column Name | Type | Nullable | Description | PII | Example Value | Constraints |
|-------------|------|----------|-------------|-----|---------------|-------------|
| id | BIGINT | NO | [Primary identifier, auto-generated] | No | 12345 | PK, auto-increment |
| [column_name] | VARCHAR(255) | NO | [What this column represents in business terms] | [Yes/No] | [Realistic example] | [UNIQUE, CHECK, FK, etc.] |
| [column_name] | TIMESTAMP | NO | [When the record was created] | No | 2025-01-15T10:30:00Z | DEFAULT now() |
| [column_name] | ENUM/VARCHAR | YES | [Allowed values and what each means] | No | active | CHECK (active, inactive, archived) |
| [column_name] | DECIMAL(10,2) | YES | [What this measures, units] | No | 99.95 | >= 0 |

---

## Keys & Indexes

| Type        | Column(s)          | Name                  | Rationale                              |
|-------------|--------------------|-----------------------|----------------------------------------|
| Primary Key | id                 | pk_[table]            | Row identity                           |
| Foreign Key | [column]           | fk_[table]_[ref]      | References [other_table](id)           |
| Unique      | [column, column]   | uq_[table]_[columns]  | [Business rule requiring uniqueness]   |
| Index       | [column]           | idx_[table]_[column]   | [Query pattern this supports]          |

---

## Partitioning

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| Strategy       | [Range / List / Hash / None]                       |
| Partition Key  | [Column used for partitioning]                     |
| Retention      | [How long partitions are kept, e.g., 90 days]      |
| Pruning        | [How old partitions are dropped or archived]        |

---

## Volume & Freshness

| Metric           | Value                                            |
|------------------|--------------------------------------------------|
| Current row count| [Approximate, e.g., ~50M rows]                   |
| Growth rate      | [e.g., ~100K rows/day]                           |
| Update frequency | [Real-time / hourly / daily batch / event-driven] |
| Freshness SLA    | [e.g., data must be no more than 1 hour old]      |

---

## Lineage

**Upstream (what populates this table):**
- [Source system or pipeline] via [mechanism, e.g., CDC, ETL job, API sync]

**Downstream (what reads this table):**
- [Dashboard / service / report name] — [how it uses the data]
- [Another consumer] — [usage description]

---

## Access Control

| Permission | Granted To                  | Notes                         |
|------------|-----------------------------|-------------------------------|
| Read       | [Roles / teams / services]  | [Any row-level security rules]|
| Write      | [Roles / services]          | [Via which process]           |
| Admin      | [DBA / data engineering]    | [Schema changes only]         |

---

## Change History

| Date       | Change Description                    | Migration Reference        |
|------------|---------------------------------------|----------------------------|
| YYYY-MM-DD | Table created                         | [migration file or PR link]|
| YYYY-MM-DD | [e.g., Added column X for feature Y] | [migration reference]      |
