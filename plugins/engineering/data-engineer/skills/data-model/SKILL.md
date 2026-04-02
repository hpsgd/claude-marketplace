---
name: data-model
description: Design a data model — entities, relationships, constraints, and access patterns.
argument-hint: "[domain or feature to model]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Design a data model for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Domain Discovery

Before creating any tables or schemas, understand the domain:

1. **Identify the core entities** — what are the nouns? What are the things the system manages?
2. **Identify the events** — what happens to these entities? What changes over time?
3. **Identify the actors** — who or what creates, reads, updates, or deletes these entities?
4. **Identify the invariants** — what rules must ALWAYS be true? (e.g., "an order cannot have negative quantity")

**For each entity:**

| Property | Question |
|---|---|
| Identity | What uniquely identifies an instance? (UUID, natural key, composite key?) |
| Lifecycle | How is it created? Modified? Archived? Deleted? |
| Ownership | Who owns it? What parent entity does it belong to? |
| Cardinality | How many will exist? (10s, 1000s, millions, billions?) |
| Mutability | Does it change after creation? Which fields change? How often? |
| Temporal | Do we need to know its state at a point in time? |

### Step 2: Relationship Mapping

For every pair of related entities:

| Relationship type | Schema pattern | Example |
|---|---|---|
| **One-to-one** | FK on either side, or embed in same table | User ↔ UserProfile |
| **One-to-many** | FK on the "many" side pointing to the "one" | Source → Crawls |
| **Many-to-many** | Junction table with FKs to both sides | User ↔ Role via user_roles |
| **Hierarchical (tree)** | Self-referencing FK or materialised path | Category → SubCategory |
| **Temporal** | Validity period columns (valid_from, valid_to) | EmployeeRole with date range |

**For each relationship, answer:**
- Is it mandatory or optional? (NOT NULL constraint on FK?)
- What happens on delete? (CASCADE, SET NULL, RESTRICT, or soft delete?)
- Is it exclusive or shared? (Can a crawl belong to multiple sources?)
- Is it ordered? (Do items in a list have a position?)

### Step 3: Entity Design

For each entity, define the full schema:

```sql
CREATE TABLE sources (
    -- Identity
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Core attributes
    name            TEXT NOT NULL,
    url             TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'paused', 'archived')),

    -- Relationships
    owner_id        UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,

    -- Metadata
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID REFERENCES users(id),

    -- Constraints
    CONSTRAINT uq_sources_name_per_owner UNIQUE (owner_id, name)
);

-- Indexes for access patterns
CREATE INDEX idx_sources_owner_id ON sources(owner_id);
CREATE INDEX idx_sources_status ON sources(status) WHERE status = 'active';
```

**Schema design rules:**

| Rule | Implementation |
|---|---|
| UUIDs for primary keys | `UUID PRIMARY KEY DEFAULT gen_random_uuid()` — no sequential integers (enumeration risk, merge conflicts) |
| Timestamps with timezone | `TIMESTAMPTZ` not `TIMESTAMP` — always store UTC |
| `created_at` and `updated_at` on every table | Audit trail, debugging, optimistic concurrency |
| `NOT NULL` by default | Explicitly nullable fields are the exception, not the rule |
| `CHECK` constraints for enums | Database-level validation, not just application-level |
| Named constraints | `CONSTRAINT uq_sources_name_per_owner` — not anonymous |
| Soft delete via status | `status = 'archived'` not `DELETE FROM`. Hard delete only for GDPR/privacy |
| No premature denormalisation | Normalise first. Denormalise only when query performance demands it, with evidence |

### Step 4: Access Pattern Analysis (MANDATORY)

The schema must be optimised for the actual access patterns. Document every query pattern:

```markdown
### Access Patterns

| # | Pattern | Query shape | Frequency | Latency SLA |
|---|---|---|---|---|
| AP1 | List sources for a user | `WHERE owner_id = ? ORDER BY created_at DESC LIMIT 25` | 100/min | < 50ms |
| AP2 | Get source by ID | `WHERE id = ?` | 500/min | < 10ms |
| AP3 | Search sources by name | `WHERE name ILIKE '%query%'` | 20/min | < 200ms |
| AP4 | Count active sources per user | `WHERE owner_id = ? AND status = 'active'` | 50/min | < 50ms |
| AP5 | List recent crawls for a source | `WHERE source_id = ? ORDER BY started_at DESC LIMIT 10` | 200/min | < 50ms |
```

**Index strategy based on access patterns:**

| Access pattern | Index needed | Type |
|---|---|---|
| AP1 | `(owner_id, created_at DESC)` | Composite, covering the sort |
| AP2 | `(id)` — PK, already indexed | Primary key |
| AP3 | `gin(name gin_trgm_ops)` | Trigram index for ILIKE |
| AP4 | `(owner_id) WHERE status = 'active'` | Partial index |
| AP5 | `(source_id, started_at DESC)` | Composite |

**Rules:**
- Every WHERE clause in a frequent query must have an index
- Composite indexes: leftmost column is the equality filter, rightmost is the range/sort
- Partial indexes for common filters (`WHERE status = 'active'`)
- Don't index everything — indexes slow down writes and consume storage
- If a query is rare and slow, that may be acceptable. Index based on SLA, not completeness

### Step 5: Data Integrity Rules

#### Referential Integrity

| Relationship | ON DELETE strategy | Rationale |
|---|---|---|
| User → Sources | `RESTRICT` | Don't delete users with sources — orphaned data |
| Source → Crawls | `CASCADE` | Deleting a source removes all its crawls |
| Crawl → Pages | `CASCADE` | Deleting a crawl removes its pages |
| User → AuditLog | `SET NULL` | Keep the log entry, just anonymise the actor |

#### Business Rules (enforced at database level)

```sql
-- Quantity must be positive
ALTER TABLE order_items ADD CONSTRAINT chk_quantity_positive CHECK (quantity > 0);

-- End date must be after start date
ALTER TABLE subscriptions ADD CONSTRAINT chk_date_order CHECK (end_date > start_date);

-- Email format (basic)
ALTER TABLE users ADD CONSTRAINT chk_email_format CHECK (email ~* '^.+@.+\..+$');

-- Status transitions (enforced via trigger or application layer)
-- active -> paused -> active (allowed)
-- active -> archived (allowed)
-- archived -> active (NOT allowed without admin)
```

#### Uniqueness Constraints

| Constraint | Scope | Implementation |
|---|---|---|
| User email | Global | `UNIQUE (email)` |
| Source name per owner | Per-owner | `UNIQUE (owner_id, name)` |
| Crawl per source per day | Per-source | `UNIQUE (source_id, DATE(started_at))` |

### Step 6: Event Sourcing Considerations (if applicable)

If the domain benefits from event sourcing:

```sql
-- Events are immutable — append only, never update
CREATE TABLE source_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stream_id       UUID NOT NULL,           -- The aggregate ID
    stream_type     TEXT NOT NULL,            -- 'Source', 'Crawl', etc.
    event_type      TEXT NOT NULL,            -- 'SourceCreated', 'CrawlStarted'
    data            JSONB NOT NULL,           -- Event payload
    metadata        JSONB DEFAULT '{}',       -- Correlation IDs, causation, user
    version         INTEGER NOT NULL,         -- Sequence within the stream
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_stream_version UNIQUE (stream_id, version)
);

CREATE INDEX idx_events_stream ON source_events(stream_id, version);
```

**Event sourcing rules:**
- Events are immutable — once written, never modified. Corrections are new events
- Each fact has exactly one authoritative source (single writer per stream)
- Projections (read models) are derived from events — they can be rebuilt
- Version field prevents concurrent writes to the same stream (optimistic concurrency)

### Step 7: Schema Evolution Strategy

Design for change. Document how the schema evolves:

| Change type | Safe? | Strategy | Downtime required? |
|---|---|---|---|
| Add nullable column | YES | `ALTER TABLE ADD COLUMN` | No |
| Add column with default | YES | `ALTER TABLE ADD COLUMN DEFAULT` | No (Postgres 11+) |
| Add NOT NULL column | NO | Add nullable → backfill → add constraint | No (multi-step) |
| Remove column | NO | Stop reading → deploy → drop column | No (multi-step) |
| Rename column | NO | Add new → dual-write → migrate reads → drop old | No (multi-step) |
| Change column type | NO | Add new column → backfill → swap | Possibly |
| Add index | YES | `CREATE INDEX CONCURRENTLY` | No |
| Drop index | YES | `DROP INDEX CONCURRENTLY` | No |

**Evolution rules:**
- Additive changes are safe — new columns, new tables, new indexes
- Destructive changes need a migration plan with rollback
- `ALTER TABLE` on large tables can lock — use `CONCURRENTLY` for indexes
- Schema changes are versioned (migration files, not manual DDL)
- Every migration has a corresponding rollback migration

### Step 8: Privacy by Design

| Principle | Implementation |
|---|---|
| Data minimisation | Don't collect what you don't need. If you don't need date of birth, don't add the column |
| PII identification | Tag columns containing PII: name, email, phone, address, IP, payment info |
| Encryption at rest | PII columns encrypted. Key rotation plan documented |
| Retention policy | Define how long each data type is kept. Automate deletion |
| Right to erasure | Document the deletion path: which tables, which columns, cascade vs anonymise |
| Anonymisation | Replace PII with hashed/randomised values rather than hard delete (preserves analytics) |
| Access logging | Who accessed PII and when? Audit table for sensitive data access |

```sql
-- PII columns documented
COMMENT ON COLUMN users.email IS 'PII: email address. Retention: account lifetime + 30 days. Erasure: anonymise to hash.';
COMMENT ON COLUMN users.name IS 'PII: full name. Retention: account lifetime + 30 days. Erasure: set to "Deleted User".';
```

## Anti-Patterns (NEVER do these)

- **No primary key** — every table has a primary key. No exceptions
- **Sequential integer IDs as external identifiers** — use UUIDs. Integers enable enumeration attacks
- **`TIMESTAMP` without timezone** — always `TIMESTAMPTZ`. Timezone-naive timestamps cause bugs in every timezone except the server's
- **Storing computed values** — unless there's a proven performance need, compute on read. Stored computed values get stale
- **God tables** — a table with 40 columns covering multiple concepts. Split into focused tables
- **Implicit relationships** — "the user_id column refers to users.id" without a foreign key constraint. Add the FK
- **Missing indexes on foreign keys** — FK columns used in JOINs need indexes. PostgreSQL does not auto-index FKs
- **`VARCHAR(255)` everywhere** — use `TEXT` for unbounded strings. `VARCHAR(n)` only when the max length is a real business rule
- **EAV (Entity-Attribute-Value) pattern** — JSON columns for structured data, not key-value pairs in rows. EAV defeats type safety and query optimisation
- **No migration versioning** — manual DDL changes applied ad hoc. Use a migration tool (Flyway, Alembic, dbmate)

## Output Format

```markdown
# Data Model: [domain name]

## Entity-Relationship Diagram
[Mermaid ER diagram]

## Entities

### [Entity Name]
- **Purpose:** [one sentence]
- **Cardinality:** [expected count]
- **Mutability:** [immutable / rarely updated / frequently updated]

#### Schema
[CREATE TABLE SQL with constraints, indexes, comments]

#### Access Patterns
[Table of query patterns with frequency and latency SLA]

#### Indexes
[Table of indexes with rationale]

## Relationships
| From | To | Type | On delete | Constraint |
|---|---|---|---|---|

## Business Rules
[Constraints enforced at database level]

## Privacy
| Column | Classification | Retention | Erasure strategy |
|---|---|---|---|

## Evolution Plan
[Known upcoming changes and migration strategy]

## Open Questions
[Decisions that need product/business input before finalising]
```
