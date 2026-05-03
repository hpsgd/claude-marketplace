# Data Model

Scenario: Developer invokes the data-model skill to design the schema for a subscription billing domain. Key entities are customers, subscriptions, plans, invoices, and payment methods.

## Prompt

> Design a data model for subscription billing. Entities: customers (name, email, created date), plans (name, price, billing interval monthly/annual, feature limits), subscriptions (customer to plan, status: trial/active/past_due/cancelled, start date, trial end date), invoices (subscription, amount, due date, paid date, status), and payment methods (customer, type: card/bank, last 4 digits, expiry). A customer can have multiple subscriptions and payment methods. Subscriptions must have a payment method.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Data Model: Subscription Billing

## Entity-Relationship Diagram

```mermaid
erDiagram
    customers {
        uuid id PK
        text name
        text email
        timestamptz created_at
        timestamptz updated_at
    }
    plans {
        uuid id PK
        text name
        bigint price_cents
        text billing_interval
        jsonb feature_limits
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }
    payment_methods {
        uuid id PK
        uuid customer_id FK
        text type
        char last4
        smallint expiry_month
        smallint expiry_year
        timestamptz created_at
    }
    subscriptions {
        uuid id PK
        uuid customer_id FK
        uuid plan_id FK
        uuid payment_method_id FK
        bigint locked_price_cents
        text status
        timestamptz started_at
        timestamptz trial_ends_at
        timestamptz cancelled_at
        timestamptz created_at
        timestamptz updated_at
    }
    invoices {
        uuid id PK
        uuid subscription_id FK
        bigint amount_cents
        date due_date
        timestamptz paid_at
        text status
        timestamptz created_at
        timestamptz updated_at
    }

    customers ||--o{ payment_methods : "owns"
    customers ||--o{ subscriptions : "holds"
    plans ||--o{ subscriptions : "governs"
    payment_methods ||--o{ subscriptions : "charges"
    subscriptions ||--o{ invoices : "generates"
```

---

## Entities

### customers
- **Purpose:** Represents a billable account.
- **Cardinality:** Millions
- **Mutability:** Rarely updated (name/email changes)

#### Schema
```sql
CREATE TABLE customers (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT        NOT NULL,
    email       TEXT        NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_customers_email   UNIQUE (email),
    CONSTRAINT chk_customers_email  CHECK  (email ~* '^.+@.+\..+$')
);

COMMENT ON COLUMN customers.name  IS 'PII: full name. Erasure: set to "Deleted User".';
COMMENT ON COLUMN customers.email IS 'PII: email address. Erasure: anonymise to SHA-256 hash.';

CREATE INDEX idx_customers_email ON customers (email);
```

---

### plans
- **Purpose:** Defines a purchasable tier with pricing and feature entitlements.
- **Cardinality:** Dozens (stable)
- **Mutability:** Rarely updated; price changes create a new plan rather than mutating the existing one (see [Open Questions](#open-questions))

```sql
CREATE TABLE plans (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name             TEXT        NOT NULL,
    price_cents      BIGINT      NOT NULL,
    billing_interval TEXT        NOT NULL
                     CHECK (billing_interval IN ('monthly', 'annual')),
    feature_limits   JSONB       NOT NULL DEFAULT '{}',
    is_active        BOOLEAN     NOT NULL DEFAULT true,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_plans_name             UNIQUE (name),
    CONSTRAINT chk_plans_price_non_neg   CHECK  (price_cents >= 0)
);

-- Partial index: active plan lookups are the hot path
CREATE INDEX idx_plans_active ON plans (id) WHERE is_active = true;
```

`feature_limits` stores structured entitlements as JSONB rather than EAV rows — e.g.:
```json
{ "max_users": 10, "max_storage_gb": 100, "api_calls_per_month": 50000 }
```
Shape is validated in the application layer; add a `CHECK` constraint if the key set is stable.

---

### payment_methods
- **Purpose:** A stored payment instrument belonging to a customer.
- **Cardinality:** Tens of millions
- **Mutability:** Immutable after creation; expiry is fixed at time of tokenisation

```sql
CREATE TABLE payment_methods (
    id            UUID      NOT NULL DEFAULT gen_random_uuid(),
    customer_id   UUID      NOT NULL REFERENCES customers (id) ON DELETE RESTRICT,
    type          TEXT      NOT NULL CHECK (type IN ('card', 'bank')),
    last4         CHAR(4)   NOT NULL CHECK (last4 ~ '^[0-9]{4}$'),
    expiry_month  SMALLINT,          -- NULL for bank accounts
    expiry_year   SMALLINT,          -- NULL for bank accounts
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),

    PRIMARY KEY (id),

    -- Composite unique key enables the cross-customer FK on subscriptions
    CONSTRAINT uq_payment_methods_id_customer UNIQUE (id, customer_id),

    CONSTRAINT chk_card_has_expiry CHECK (
        type != 'card' OR (expiry_month IS NOT NULL AND expiry_year IS NOT NULL)
    ),
    CONSTRAINT chk_expiry_month CHECK (
        expiry_month IS NULL OR expiry_month BETWEEN 1 AND 12
    ),
    CONSTRAINT chk_expiry_year CHECK (
        expiry_year IS NULL OR expiry_year >= 2000
    )
);

COMMENT ON COLUMN payment_methods.last4        IS 'PCI-DSS: last 4 digits only. Full PAN stored in payment processor vault.';
COMMENT ON COLUMN payment_methods.expiry_month IS 'PCI-DSS: expiry month. Low sensitivity but treat as payment data.';

CREATE INDEX idx_payment_methods_customer ON payment_methods (customer_id);
```

---

### subscriptions
- **Purpose:** Links a customer to a plan via a payment method; tracks lifecycle state.
- **Cardinality:** Millions
- **Mutability:** Status changes frequently; `plan_id` and `payment_method_id` may change on upgrades/card updates

```sql
CREATE TABLE subscriptions (
    id                  UUID        NOT NULL DEFAULT gen_random_uuid(),
    customer_id         UUID        NOT NULL REFERENCES customers (id)       ON DELETE RESTRICT,
    plan_id             UUID        NOT NULL REFERENCES plans (id)            ON DELETE RESTRICT,
    payment_method_id   UUID        NOT NULL,
    locked_price_cents  BIGINT      NOT NULL,   -- price at time of subscription (see note)
    status              TEXT        NOT NULL DEFAULT 'trial'
                        CHECK (status IN ('trial', 'active', 'past_due', 'cancelled')),
    started_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    trial_ends_at       TIMESTAMPTZ,
    cancelled_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    PRIMARY KEY (id),

    -- Enforces payment_method belongs to the same customer at the DB level
    CONSTRAINT fk_subscriptions_payment_method
        FOREIGN KEY (payment_method_id, customer_id)
        REFERENCES payment_methods (id, customer_id),

    CONSTRAINT chk_trial_end_after_start CHECK (
        trial_ends_at IS NULL OR trial_ends_at > started_at
    ),
    CONSTRAINT chk_cancelled_at_only_when_cancelled CHECK (
        cancelled_at IS NULL OR status = 'cancelled'
    ),
    CONSTRAINT chk_locked_price_non_neg CHECK (locked_price_cents >= 0)
);

-- Hot paths: customer dashboard, billing jobs
CREATE INDEX idx_subscriptions_customer     ON subscriptions (customer_id, created_at DESC);
CREATE INDEX idx_subscriptions_plan         ON subscriptions (plan_id);
CREATE INDEX idx_subscriptions_payment_method ON subscriptions (payment_method_id);

-- Billing job: find all past_due subscriptions
CREATE INDEX idx_subscriptions_past_due
    ON subscriptions (updated_at DESC)
    WHERE status = 'past_due';

-- Cancellation job / churn report
CREATE INDEX idx_subscriptions_cancelled
    ON subscriptions (cancelled_at DESC)
    WHERE status = 'cancelled';
```

> **`locked_price_cents`** — captures the agreed price at subscription time. If a plan's price changes, existing subscriptions are not affected. This avoids surprise billing. Invoices are generated from this value, not from `plans.price_cents`.

---

### invoices
- **Purpose:** A billing record for one billing cycle of a subscription.
- **Cardinality:** Billions (one per subscription per period)
- **Mutability:** Status transitions: `open → paid` or `open → past_due → void`. `paid_at` is written once.

```sql
CREATE TABLE invoices (
    id              UUID        NOT NULL DEFAULT gen_random_uuid(),
    subscription_id UUID        NOT NULL REFERENCES subscriptions (id) ON DELETE RESTRICT,
    amount_cents    BIGINT      NOT NULL,
    due_date        DATE        NOT NULL,
    paid_at         TIMESTAMPTZ,
    status          TEXT        NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open', 'paid', 'past_due', 'void')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    PRIMARY KEY (id),

    CONSTRAINT chk_invoices_amount_positive CHECK (amount_cents > 0),

    -- paid_at must be set iff status = 'paid'
    CONSTRAINT chk_invoices_paid_consistency CHECK (
        (status = 'paid') = (paid_at IS NOT NULL)
    )
);

-- Subscription billing history
CREATE INDEX idx_invoices_subscription ON invoices (subscription_id, due_date DESC);

-- Dunning job: unpaid invoices past due
CREATE INDEX idx_invoices_open_overdue
    ON invoices (due_date)
    WHERE status IN ('open', 'past_due');
```

---

## Relationships

| From | To | Type | FK Column | On Delete | Note |
|---|---|---|---|---|---|
| `customers` | `payment_methods` | 1→many | `payment_methods.customer_id` | RESTRICT | Can't delete customer with stored payment methods |
| `customers` | `subscriptions` | 1→many | `subscriptions.customer_id` | RESTRICT | Audit trail preserved |
| `plans` | `subscriptions` | 1→many | `subscriptions.plan_id` | RESTRICT | Plans cannot be deleted while subscriptions exist |
| `payment_methods` | `subscriptions` | 1→many | `subscriptions.(payment_method_id, customer_id)` | RESTRICT | Composite FK enforces same-customer ownership |
| `subscriptions` | `invoices` | 1→many | `invoices.subscription_id` | RESTRICT | Invoice history preserved on cancellation |

---

## Business Rules

```sql
-- Subscription payment method must belong to the same customer (enforced by composite FK above)

-- Trial end must be after subscription start
CONSTRAINT chk_trial_end_after_start CHECK (trial_ends_at IS NULL OR trial_ends_at > started_at)

-- cancelled_at only set when status is cancelled
CONSTRAINT chk_cancelled_at_only_when_cancelled CHECK (cancelled_at IS NULL OR status = 'cancelled')

-- Invoice paid_at set iff status = 'paid'
CONSTRAINT chk_invoices_paid_consistency CHECK ((status = 'paid') = (paid_at IS NOT NULL))

-- Price and amount are never negative
CONSTRAINT chk_plans_price_non_neg    CHECK (price_cents >= 0)
CONSTRAINT chk_invoices_amount_pos    CHECK (amount_cents > 0)
CONSTRAINT chk_locked_price_non_neg   CHECK (locked_price_cents >= 0)

-- Card payment methods must have expiry; bank accounts need not
CONSTRAINT chk_card_has_expiry CHECK (type != 'card' OR (expiry_month IS NOT NULL AND expiry_year IS NOT NULL))
```

Status transition enforcement (trial → active → past\_due; active → cancelled; etc.) is an application-layer concern — the database only constrains the valid set, not the valid transitions.

---

## Access Patterns

| # | Pattern | Query shape | Index used |
|---|---|---|---|
| AP1 | Customer's subscriptions | `WHERE customer_id = ? ORDER BY created_at DESC` | `idx_subscriptions_customer` |
| AP2 | Invoices for a subscription | `WHERE subscription_id = ? ORDER BY due_date DESC` | `idx_invoices_subscription` |
| AP3 | Customer's payment methods | `WHERE customer_id = ?` | `idx_payment_methods_customer` |
| AP4 | All past\_due subscriptions (billing job) | `WHERE status = 'past_due'` | `idx_subscriptions_past_due` |
| AP5 | Unpaid invoices past due date (dunning) | `WHERE status IN ('open','past_due') AND due_date < now()` | `idx_invoices_open_overdue` |
| AP6 | Lookup customer by email | `WHERE email = ?` | `idx_customers_email` |
| AP7 | Active plans for plan picker | `WHERE is_active = true` | `idx_plans_active` |

---

## Privacy

| Column | Classification | Retention | Erasure strategy |
|---|---|---|---|
| `customers.name` | PII | Account lifetime + 30 days | Set to `"Deleted User"` |
| `customers.email` | PII | Account lifetime + 30 days | Anonymise to SHA-256 hex |
| `payment_methods.last4` | PCI (partial) | Payment method lifetime | Hard delete row |
| `payment_methods.expiry_month/year` | PCI (partial) | Payment method lifetime | Hard delete row |

Full PANs and bank account numbers are never stored — delegate to a PCI-compliant vault (Stripe, Adyen). `last4` and expiry are for display only.

---

## Schema Evolution Plan

| Change | Safe? | Strategy |
|---|---|---|
| Add new plan billing interval (e.g. `quarterly`) | No | Add to `CHECK` constraint in a migration; old rows unaffected |
| Add `default_payment_method_id` on customers | Yes | Add nullable column; backfill; add NOT NULL later |
| Add invoice line items | Yes | New `invoice_line_items` table with FK to `invoices` |
| Rename `status` values | No | Add new column → dual-write → migrate reads → drop old |
| Add plan price tiers (per-seat) | Breaking | New `plan_tiers` table; `price_cents` becomes a base price |

---

## Open Questions

1. **Plan price changes** — current model recommends creating a new plan rather than updating `price_cents`. Is that acceptable operationally, or should plans support versioned pricing?
2. **Default payment method** — should customers have a designated default payment method (`customers.default_payment_method_id`), or is the payment method always chosen explicitly at subscription creation?
3. **Multi-currency** — is `amount_cents` always in a single currency? If multi-currency is needed, add a `currency` column (ISO 4217 `CHAR(3)`) to both `plans` and `invoices`.
4. **Invoice line items** — should invoices support multiple line items (base plan + add-ons, proration credits)? If so, add an `invoice_line_items` table now rather than retro-fitting it.
5. **Subscription plan changes (upgrades/downgrades)** — when a customer changes plan mid-cycle, should the old subscription be cancelled and a new one created, or should `subscriptions.plan_id` be updated in place? The former preserves a complete audit trail.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.0 (97%) |
| Evaluated | 2026-04-30 |
| Target duration | 105931 ms |
| Target cost | $0.1674 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill performs domain discovery before creating tables — identifies entities, events, actors, invariants, and cardinality for each | PASS | Each entity section includes explicit Purpose, Cardinality (e.g. 'Millions', 'Dozens', 'Billions'), and Mutability fields. Business Rules section enumerates invariants (trial_end_after_start, cancelled_at consistency, paid_at consistency, etc.). |
| c2 | All primary keys use UUIDs (`gen_random_uuid()`) — no sequential integers | PASS | Every table: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` (or `NOT NULL DEFAULT gen_random_uuid()` with explicit PRIMARY KEY). No SERIAL or integer PKs appear. |
| c3 | All timestamp columns use `TIMESTAMPTZ` — not timezone-naive `TIMESTAMP` | PASS | created_at, updated_at, started_at, trial_ends_at, cancelled_at, paid_at all declared TIMESTAMPTZ. due_date uses DATE type, which is semantically correct for a calendar date, not a tz-naive TIMESTAMP. |
| c4 | Status fields use `CHECK` constraints with enum values — not unconstrained text columns | PASS | plans.billing_interval: `CHECK (billing_interval IN ('monthly', 'annual'))`. subscriptions.status: `CHECK (status IN ('trial', 'active', 'past_due', 'cancelled'))`. invoices.status: `CHECK (status IN ('open', 'paid', 'past_due', 'void'))`. payment_methods.type: `CHECK (type IN ('card', 'bank'))`. |
| c5 | Skill documents access patterns before defining indexes — lists the frequent queries with frequency and latency SLA | PARTIAL | An 'Access Patterns' table (AP1–AP7) is present with query shapes and index mappings, but it appears AFTER the entity/index definitions, not before. No frequency estimates or latency SLAs are included — only query shape and which index is used. |
| c6 | Foreign keys have named constraints and appropriate `ON DELETE` strategies (e.g. `RESTRICT` not silent cascade for customer deletion) | PASS | Named constraint `fk_subscriptions_payment_method` is explicit. All FK columns use `ON DELETE RESTRICT` (customers→payment_methods, customers→subscriptions, plans→subscriptions, subscriptions→invoices). Relationship table confirms RESTRICT with rationale. |
| c7 | Privacy section identifies PII columns (email, card last 4, name) with retention and erasure strategy | PASS | Privacy section table lists customers.name (PII, set to 'Deleted User'), customers.email (PII, anonymise to SHA-256 hash), payment_methods.last4 (PCI, hard delete row), payment_methods.expiry_month/year (PCI, hard delete row) with retention periods. |
| c8 | Skill produces a Mermaid ER diagram in the output | PARTIAL | A full ```mermaid erDiagram``` block is present at the top of the output, showing all five entities with their columns and relationship lines. |
| c9 | Skill identifies open questions requiring product/business input before finalising | PASS | 'Open Questions' section lists 5 items: plan price changes strategy, default payment method, multi-currency, invoice line items, and subscription plan upgrade/downgrade handling. |
| c10 | Output's schema includes all five entities from the prompt — customers, plans, subscriptions, invoices, payment_methods — with the columns and types specified in the prompt | PASS | All five CREATE TABLE statements are present: customers (name, email, created_at), plans (name, price_cents, billing_interval, feature_limits), subscriptions (customer_id, plan_id, payment_method_id, status, started_at, trial_ends_at), invoices (subscription_id, amount_cents, due_date, paid_at, status), payment_methods (customer_id, type, last4, expiry_month, expiry_year). |
| c11 | Output's `subscriptions` table has a `status` column with a CHECK constraint listing the four exact values from the prompt (`trial`, `active`, `past_due`, `cancelled`) — not a free-text string | PASS | `CHECK (status IN ('trial', 'active', 'past_due', 'cancelled'))` appears verbatim in the subscriptions DDL. |
| c12 | Output's `payment_methods` table stores only the last 4 digits and expiry as specified in the prompt, and the type column has a CHECK on (`card`, `bank`) | PASS | `last4 CHAR(4) NOT NULL CHECK (last4 ~ '^[0-9]{4}$')`, `expiry_month SMALLINT`, `expiry_year SMALLINT`, `type TEXT NOT NULL CHECK (type IN ('card', 'bank'))`. PCI comment confirms full PAN is not stored. |
| c13 | Output's `subscriptions` table enforces the 'must have a payment method' requirement via a NOT NULL foreign key to `payment_methods` | PASS | `payment_method_id UUID NOT NULL` with `CONSTRAINT fk_subscriptions_payment_method FOREIGN KEY (payment_method_id, customer_id) REFERENCES payment_methods (id, customer_id)`. |
| c14 | Output uses `gen_random_uuid()` for every primary key and `TIMESTAMPTZ` for every datetime column (created_at, started_at, due_date, paid_date, trial_end_date) | PASS | All five tables use `DEFAULT gen_random_uuid()`. created_at/updated_at/started_at/trial_ends_at/cancelled_at/paid_at all TIMESTAMPTZ. due_date is DATE (correct semantic type). No TIMESTAMP without TZ anywhere. |
| c15 | Output specifies ON DELETE strategies for each foreign key — customer deletion is RESTRICT (or soft-delete pattern), not silent CASCADE that would erase invoices and audit history | PASS | All FK declarations include `ON DELETE RESTRICT`. Relationships table column 'On Delete' lists RESTRICT for all five relationships with explicit rationale ('Audit trail preserved', 'Invoice history preserved on cancellation'). |
| c16 | Output's privacy section flags email, name, and card last-4 as PII with an erasure strategy | PASS | Privacy table: customers.name → set to 'Deleted User'; customers.email → anonymise to SHA-256 hex; payment_methods.last4 → hard delete row. All three are explicitly named with erasure strategies. |
| c17 | Output includes a Mermaid ER diagram showing the cardinality (customer 1:N subscriptions, customer 1:N payment_methods, subscription 1:N invoices, subscription N:1 plan) | PASS | Mermaid diagram uses `\|\|--o{` notation: `customers \|\|--o{ payment_methods`, `customers \|\|--o{ subscriptions`, `plans \|\|--o{ subscriptions`, `subscriptions \|\|--o{ invoices` — all four required cardinalities shown. |
| c18 | Output lists open questions for product — e.g. proration on plan change, partial refund handling, multi-currency support, tax columns — rather than silently making assumptions | PASS | Open Questions Q3: multi-currency support with explicit suggestion to add `currency CHAR(3)`; Q4: invoice line items for add-ons/proration credits; Q5: plan upgrade/downgrade audit trail. Partial refunds and tax columns not explicitly named but proration and multi-currency are covered. |
| c19 | Output addresses currency and money representation — money stored as integer cents (or numeric with explicit precision) and a currency column, not floating-point | PARTIAL | Money columns consistently use BIGINT cents (`price_cents`, `amount_cents`, `locked_price_cents`). No currency column is included in the schema — it's deferred to Open Question #3 ('add a `currency` column (ISO 4217 CHAR(3))'), so integer representation is addressed but currency column is absent from the actual DDL. |

### Notes

The output is comprehensive and professional, covering all five entities with correct types, UUID PKs, TIMESTAMPTZ columns, CHECK constraints, named FKs with RESTRICT semantics, a PCI/PII privacy section, Mermaid ER diagram, and open questions. The composite FK trick to enforce same-customer payment method ownership is a particularly strong design detail. Two minor gaps: the access patterns section appears after the index definitions rather than before (failing the 'before indexes' ordering requirement) and omits frequency/latency SLAs; and the currency column is mentioned only as a future open question rather than included in the baseline schema. Both are minor relative to the overall quality.
