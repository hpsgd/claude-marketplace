# Result: Data model for a subscription billing domain

**Verdict:** PASS
**Score:** 18.5/19 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

What follows is the simulated output this skill would produce for the prompt: design a data model for subscription billing with entities customers, plans, subscriptions, invoices, and payment_methods.

---

# Data Model: Subscription Billing

## Entity-Relationship Diagram

```mermaid
erDiagram
    customers {
        uuid id PK
        text name
        text email
        timestamptz created_at
    }
    plans {
        uuid id PK
        text name
        integer price_cents
        text currency
        text billing_interval
        jsonb feature_limits
        timestamptz created_at
    }
    payment_methods {
        uuid id PK
        uuid customer_id FK
        text type
        text last_four
        text expiry_month
        text expiry_year
        timestamptz created_at
    }
    subscriptions {
        uuid id PK
        uuid customer_id FK
        uuid plan_id FK
        uuid payment_method_id FK
        text status
        timestamptz started_at
        timestamptz trial_end_date
        timestamptz created_at
        timestamptz updated_at
    }
    invoices {
        uuid id PK
        uuid subscription_id FK
        integer amount_cents
        text currency
        text status
        timestamptz due_date
        timestamptz paid_date
        timestamptz created_at
    }

    customers ||--o{ subscriptions : "has"
    customers ||--o{ payment_methods : "owns"
    plans ||--o{ subscriptions : "governs"
    subscriptions }o--|| payment_methods : "charges"
    subscriptions ||--o{ invoices : "generates"
```

## Entities

### customers

- **Purpose:** Represents a billing account holder — the person or organisation being charged.
- **Cardinality:** 100k–10M rows expected at scale.
- **Mutability:** Email and name updated occasionally (support corrections, legal name changes).

#### Schema

```sql
CREATE TABLE customers (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    -- PII: full name. Retention: account lifetime + 30 days. Erasure: set to 'Deleted User'.
    email       TEXT NOT NULL,
    -- PII: email address. Retention: account lifetime + 30 days. Erasure: anonymise to hash.
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'suspended', 'closed')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_customers_email UNIQUE (email),
    CONSTRAINT chk_customers_email_format CHECK (email ~* '^.+@.+\..+$')
);

CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_status ON customers(status) WHERE status = 'active';
```

#### Access Patterns

| # | Pattern | Query shape | Frequency | Latency SLA |
|---|---|---|---|---|
| AP1 | Look up customer by email (login/billing) | `WHERE email = ?` | 1000/min | < 10ms |
| AP2 | Fetch customer by ID | `WHERE id = ?` | 2000/min | < 10ms |
| AP3 | List active customers (admin) | `WHERE status = 'active' ORDER BY created_at DESC` | 5/min | < 200ms |

#### Indexes

| Index | Columns | Type | Rationale |
|---|---|---|---|
| `uq_customers_email` | `email` | Unique | Enforces uniqueness; supports AP1 |
| `idx_customers_status` | `status` WHERE active | Partial | AP3 admin listing |

---

### plans

- **Purpose:** Defines a purchasable product tier — price, billing cadence, and feature entitlements.
- **Cardinality:** 10–100 rows; small, rarely changing reference data.
- **Mutability:** Prices and limits change via new plan versions, not in-place edits (existing subscriptions are grandfathered).

#### Schema

```sql
CREATE TABLE plans (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name             TEXT NOT NULL,
    price_cents      INTEGER NOT NULL CHECK (price_cents >= 0),
    currency         TEXT NOT NULL DEFAULT 'USD',
    billing_interval TEXT NOT NULL
                     CHECK (billing_interval IN ('monthly', 'annual')),
    feature_limits   JSONB NOT NULL DEFAULT '{}',
    active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_plans_name UNIQUE (name)
);

CREATE INDEX idx_plans_active ON plans(active) WHERE active = TRUE;
```

#### Access Patterns

| # | Pattern | Query shape | Frequency | Latency SLA |
|---|---|---|---|---|
| AP1 | List available plans (signup page) | `WHERE active = TRUE` | 500/min | < 20ms |
| AP2 | Fetch plan by ID (subscription lookup) | `WHERE id = ?` | 1000/min | < 10ms |

---

### payment_methods

- **Purpose:** Stores tokenised payment instrument references for charging subscriptions.
- **Cardinality:** 1–5 per customer; same order of magnitude as customers.
- **Mutability:** Expiry can be updated; type and last four are immutable once stored.

#### Schema

```sql
CREATE TABLE payment_methods (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id  UUID NOT NULL REFERENCES customers(id)
                 ON DELETE RESTRICT,
    -- PII: card last four digits. Retention: account lifetime + 30 days. Erasure: delete row.
    type         TEXT NOT NULL
                 CHECK (type IN ('card', 'bank')),
    last_four    TEXT NOT NULL
                 CHECK (last_four ~ '^\d{4}$'),
    expiry_month TEXT,
    expiry_year  TEXT,
    is_default   BOOLEAN NOT NULL DEFAULT FALSE,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_payment_methods_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT
);

CREATE INDEX idx_payment_methods_customer_id ON payment_methods(customer_id);
```

#### Access Patterns

| # | Pattern | Query shape | Frequency | Latency SLA |
|---|---|---|---|---|
| AP1 | List payment methods for a customer | `WHERE customer_id = ?` | 200/min | < 20ms |
| AP2 | Fetch single payment method by ID | `WHERE id = ?` | 500/min | < 10ms |

---

### subscriptions

- **Purpose:** Represents an active or historical relationship between a customer, a plan, and a payment method.
- **Cardinality:** 1–10 per customer; same order of magnitude as customers.
- **Mutability:** Status transitions frequently; plan and payment method can change.

#### Schema

```sql
CREATE TABLE subscriptions (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id        UUID NOT NULL REFERENCES customers(id)
                       ON DELETE RESTRICT,
    plan_id            UUID NOT NULL REFERENCES plans(id)
                       ON DELETE RESTRICT,
    payment_method_id  UUID NOT NULL REFERENCES payment_methods(id)
                       ON DELETE RESTRICT,
    -- NOT NULL enforces the "subscription must have a payment method" invariant
    status             TEXT NOT NULL DEFAULT 'trial'
                       CHECK (status IN ('trial', 'active', 'past_due', 'cancelled')),
    started_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    trial_end_date     TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    cancelled_at       TIMESTAMPTZ,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_subscriptions_trial_end
        CHECK (trial_end_date IS NULL OR trial_end_date > started_at),
    CONSTRAINT fk_subscriptions_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT,
    CONSTRAINT fk_subscriptions_plan
        FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE RESTRICT,
    CONSTRAINT fk_subscriptions_payment_method
        FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id) ON DELETE RESTRICT
);

CREATE INDEX idx_subscriptions_customer_id ON subscriptions(customer_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status) WHERE status IN ('trial', 'active', 'past_due');
CREATE INDEX idx_subscriptions_payment_method_id ON subscriptions(payment_method_id);
```

#### Access Patterns

| # | Pattern | Query shape | Frequency | Latency SLA |
|---|---|---|---|---|
| AP1 | List subscriptions for a customer | `WHERE customer_id = ? ORDER BY created_at DESC` | 500/min | < 30ms |
| AP2 | Fetch subscription by ID | `WHERE id = ?` | 1000/min | < 10ms |
| AP3 | Find all past_due subscriptions (billing job) | `WHERE status = 'past_due'` | 10/min | < 500ms |
| AP4 | Find subscriptions with trial ending soon | `WHERE status = 'trial' AND trial_end_date < now() + interval '3 days'` | 5/min | < 200ms |

---

### invoices

- **Purpose:** Immutable record of each billing event — amount charged, due date, and payment outcome.
- **Cardinality:** 12–120 per subscription per year; grows without bound.
- **Mutability:** Status transitions (`open → paid`, `open → overdue`); paid_date set once.

#### Schema

```sql
CREATE TABLE invoices (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID NOT NULL REFERENCES subscriptions(id)
                    ON DELETE RESTRICT,
    amount_cents    INTEGER NOT NULL CHECK (amount_cents >= 0),
    currency        TEXT NOT NULL DEFAULT 'USD',
    status          TEXT NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open', 'paid', 'void', 'overdue')),
    due_date        TIMESTAMPTZ NOT NULL,
    paid_date       TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_invoices_paid_date
        CHECK (paid_date IS NULL OR paid_date >= due_date - interval '90 days'),
    CONSTRAINT fk_invoices_subscription
        FOREIGN KEY (subscription_id) REFERENCES subscriptions(id) ON DELETE RESTRICT
);

CREATE INDEX idx_invoices_subscription_id ON invoices(subscription_id, created_at DESC);
CREATE INDEX idx_invoices_status_due ON invoices(status, due_date) WHERE status IN ('open', 'overdue');
```

#### Access Patterns

| # | Pattern | Query shape | Frequency | Latency SLA |
|---|---|---|---|---|
| AP1 | List invoices for a subscription | `WHERE subscription_id = ? ORDER BY created_at DESC` | 300/min | < 30ms |
| AP2 | Fetch overdue invoices (collections job) | `WHERE status = 'overdue' AND due_date < now()` | 5/min | < 500ms |
| AP3 | Fetch invoice by ID | `WHERE id = ?` | 500/min | < 10ms |

---

## Relationships

| From | To | Type | On delete | Constraint name |
|---|---|---|---|---|
| customers | subscriptions | One-to-many | RESTRICT | `fk_subscriptions_customer` |
| customers | payment_methods | One-to-many | RESTRICT | `fk_payment_methods_customer` |
| plans | subscriptions | One-to-many | RESTRICT | `fk_subscriptions_plan` |
| payment_methods | subscriptions | One-to-many | RESTRICT | `fk_subscriptions_payment_method` |
| subscriptions | invoices | One-to-many | RESTRICT | `fk_invoices_subscription` |

All customer-facing relationships use `RESTRICT` — deleting a customer with billing history would destroy audit records. Deletion is handled via a soft-delete status transition (`status = 'closed'`) followed by GDPR anonymisation, not a hard `DELETE`.

## Business Rules

```sql
-- Subscription must reference a payment method that belongs to the same customer
ALTER TABLE subscriptions ADD CONSTRAINT chk_subscriptions_payment_owner
    CHECK (
        (SELECT customer_id FROM payment_methods WHERE id = payment_method_id) = customer_id
    );
-- Note: this cross-table CHECK is not natively supported in PostgreSQL — enforce via trigger or application layer

-- Price must be non-negative
ALTER TABLE plans ADD CONSTRAINT chk_plans_price_non_negative CHECK (price_cents >= 0);

-- Invoice amount must be non-negative
ALTER TABLE invoices ADD CONSTRAINT chk_invoices_amount_non_negative CHECK (amount_cents >= 0);
```

## Privacy

| Column | Classification | Retention | Erasure strategy |
|---|---|---|---|
| `customers.name` | PII — full name | Account lifetime + 30 days | Set to `'Deleted User'` |
| `customers.email` | PII — email address | Account lifetime + 30 days | Anonymise to SHA-256 hash |
| `payment_methods.last_four` | PII — partial card number | Account lifetime + 30 days | Delete row (payment method deactivated) |
| `payment_methods.expiry_month/year` | PII — card expiry | Account lifetime + 30 days | Delete row |

Encryption at rest applies to the `customers` and `payment_methods` tables. Key rotation plan to be documented in the security runbook. Access to PII columns logged via audit triggers.

## Evolution Plan

| Change | Strategy | Safe? |
|---|---|---|
| Add `tax_amount_cents` to invoices | Add nullable column → backfill → add NOT NULL | No downtime |
| Add `coupon_id` FK to subscriptions | Add nullable FK → backfill defaults | No downtime |
| Rename `last_four` to `last_four_digits` | Add new column → dual-write → migrate reads → drop old | No downtime, multi-step |
| Add `metadata JSONB` to customers | `ALTER TABLE ADD COLUMN DEFAULT '{}'` | No downtime |

## Open Questions

Product and business input needed before finalising:

1. **Proration on plan change** — when a customer upgrades mid-cycle, do we issue a credit invoice for unused time, charge the difference immediately, or wait until the next billing date? This determines whether `invoices` needs a `credit_note` type and a `related_invoice_id` FK.
2. **Multi-currency** — are prices in `plans` fixed in USD and converted at invoice time, or are separate plan variants maintained per currency? The current schema stores `currency` per invoice but a single `price_cents` on the plan.
3. **Tax handling** — are taxes calculated per invoice and stored as a separate column, or managed externally (Stripe Tax, Avalara)? If stored, `invoices` needs `tax_amount_cents`, `tax_rate`, and `tax_region`.
4. **Partial refunds** — can an invoice be partially refunded? If so, a `refunds` table linked to `invoices` is needed rather than a status mutation.
5. **Payment method ownership at subscription time** — if a customer deletes a payment method that is still attached to an active subscription, should the subscription move to `past_due` immediately or prompt the customer to update? Affects `ON DELETE` strategy on the `payment_method_id` FK.
6. **Subscription pausing** — is there a `paused` status beyond the four specified? Affects CHECK constraint on `subscriptions.status`.
7. **Plan versioning** — can a plan's price change without creating a new plan? If yes, existing subscription pricing becomes ambiguous. A `subscription_price_cents` override column on `subscriptions` or a `plan_versions` table may be needed.

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Skill performs domain discovery before creating tables — Step 1 explicitly requires identifying entities, events, actors, invariants, and a per-entity property table covering identity, lifecycle, ownership, cardinality, mutability, and temporal. All five discovery elements are mandatory before any schema work.
- [x] PASS: All primary keys use UUIDs — Step 3 schema rules state `UUID PRIMARY KEY DEFAULT gen_random_uuid()` with explicit rationale against sequential integers; the anti-patterns section reinforces it with "Sequential integer IDs as external identifiers — use UUIDs."
- [x] PASS: All timestamp columns use `TIMESTAMPTZ` — Step 3 schema rules state "Timestamps with timezone — `TIMESTAMPTZ` not `TIMESTAMP` — always store UTC"; anti-patterns section adds a second explicit prohibition.
- [x] PASS: Status fields use `CHECK` constraints with enum values — Step 3 example shows `CHECK (status IN ('active', 'paused', 'archived'))` and the schema rules table lists CHECK constraints for enums as mandatory.
- [x] PASS: Skill documents access patterns before defining indexes — Step 4 is labelled MANDATORY and requires frequency and latency SLA columns; index strategy table follows within the same step.
- [x] PASS: Foreign keys have named constraints and appropriate ON DELETE strategies — Step 3 example shows `CONSTRAINT uq_sources_name_per_owner`; Step 5 provides an ON DELETE strategy table with RESTRICT rationale.
- [x] PASS: Privacy section identifies PII columns with retention and erasure strategy — Step 8 covers PII identification, retention policy, right to erasure, and anonymisation; SQL comment example tags `email` and `name`; payment info is listed as PII.
- [x] PASS: Skill produces a Mermaid ER diagram — Output Format section lists `[Mermaid ER diagram]` as the first deliverable under `## Entity-Relationship Diagram`.
- [x] PASS: Skill identifies open questions requiring product/business input — Output Format includes `## Open Questions` described as "Decisions that need product/business input before finalising."

### Output expectations (simulated output above)

- [x] PASS: Output includes all five entities — customers, plans, subscriptions, invoices, payment_methods — with the columns and types specified in the prompt.
- [x] PASS: `subscriptions.status` uses a CHECK with the four exact values from the prompt (`trial`, `active`, `past_due`, `cancelled`).
- [x] PASS: `payment_methods` stores only last four digits and expiry; type column has `CHECK (type IN ('card', 'bank'))`.
- [x] PASS: `subscriptions.payment_method_id` is `NOT NULL` — enforces the "subscription must have a payment method" invariant.
- [x] PASS: Every primary key uses `gen_random_uuid()` and every datetime column uses `TIMESTAMPTZ`.
- [x] PASS: All foreign keys specify `ON DELETE RESTRICT`; rationale for preserving audit history is documented in the Relationships section.
- [x] PASS: Privacy section flags `customers.name`, `customers.email`, and `payment_methods.last_four` as PII with erasure strategies.
- [x] PASS: Mermaid ER diagram shows all five entities with cardinality — `customers 1:N subscriptions`, `customers 1:N payment_methods`, `subscriptions 1:N invoices`, `subscriptions N:1 plans`.
- [x] PASS: Open Questions lists proration, multi-currency, tax, partial refunds, and plan versioning — product decisions, not silent assumptions.
- [~] PARTIAL: Money representation — the skill has no explicit rule on floating-point money, integer cents, or currency columns. The simulated output uses `amount_cents INTEGER` and a `currency TEXT` column (correct practice), but this comes from general domain knowledge rather than skill guidance. An agent following only this skill could produce `DECIMAL` or `FLOAT` without correction.

## Notes

The skill is structurally strong across all eight steps. The MANDATORY label on Step 4 and the explicit anti-patterns section would produce a correct and defensible schema for most billing domains.

One clear gap: money representation is absent from the schema rules and anti-patterns sections. For a billing domain this is a critical correctness concern — floating-point money is a well-known production bug. A single anti-pattern bullet ("Never use `FLOAT` or `REAL` for monetary values — use `INTEGER` cents or `NUMERIC(19,4)` with an explicit currency column") would close it without restructuring anything else.

The skill also has no explicit guidance on the cross-table CHECK constraint limitation in PostgreSQL (enforcing that a subscription's payment method belongs to the same customer). The business rules section in Step 5 covers database-level constraints but doesn't mention this common billing invariant or the trigger-based workaround.
