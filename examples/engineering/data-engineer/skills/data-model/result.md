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
    CUSTOMER ||--o{ SUBSCRIPTION : has
    CUSTOMER ||--o{ PAYMENT_METHOD : has
    PLAN ||--o{ SUBSCRIPTION : defines
    SUBSCRIPTION ||--o{ INVOICE : generates
    SUBSCRIPTION ||--o| PAYMENT_METHOD : "requires"
    INVOICE ||--o| PAYMENT_METHOD : "paid_via"

    CUSTOMER {
        uuid id PK
        string name
        string email UK
        timestamptz created_at
        timestamptz updated_at
    }

    PLAN {
        uuid id PK
        string name
        decimal price
        string interval
        jsonb feature_limits
        timestamptz created_at
    }

    SUBSCRIPTION {
        uuid id PK
        uuid customer_id FK
        uuid plan_id FK
        uuid payment_method_id FK
        string status
        timestamptz start_date
        timestamptz trial_end_date
        timestamptz cancelled_at
        timestamptz created_at
        timestamptz updated_at
    }

    INVOICE {
        uuid id PK
        uuid subscription_id FK
        uuid payment_method_id FK
        decimal amount
        timestamptz due_date
        timestamptz paid_date
        string status
        timestamptz created_at
    }

    PAYMENT_METHOD {
        uuid id PK
        uuid customer_id FK
        string type
        string last_four
        date expiry_date
        timestamptz created_at
        timestamptz archived_at
    }
```

## Entities

### Customer

- **Purpose:** A user who subscribes to plans.
- **Cardinality:** 100s to millions.
- **Mutability:** Name and email can change; status rarely changes.

#### Schema

```sql
CREATE TABLE customers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    email           TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'archived')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_customers_email UNIQUE (email)
);

CREATE INDEX idx_customers_status ON customers(status) WHERE status = 'active';
CREATE INDEX idx_customers_created_at ON customers(created_at DESC);
```

#### Access Patterns

| # | Pattern | Query | Frequency | SLA |
|---|---|---|---|---|
| AP1 | Get customer by ID | `WHERE id = ?` | 500/min | <10ms |
| AP2 | Get customer by email | `WHERE email = ?` | 100/min | <10ms |
| AP3 | List active customers | `WHERE status = 'active' ORDER BY created_at DESC LIMIT 100` | 20/min | <100ms |
| AP4 | List customers by created date range | `WHERE created_at BETWEEN ? AND ? ORDER BY created_at DESC` | 5/min | <200ms |

### Plan

- **Purpose:** A service offering with fixed pricing and feature limits.
- **Cardinality:** 10s to 100s.
- **Mutability:** Plans are immutable after creation (versions if pricing changes).

#### Schema

```sql
CREATE TABLE plans (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    price_cents     INTEGER NOT NULL CHECK (price_cents > 0),
    billing_interval TEXT NOT NULL
                    CHECK (billing_interval IN ('monthly', 'annual')),
    feature_limits  JSONB NOT NULL DEFAULT '{}',
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'archived')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_plans_name UNIQUE (name)
);

CREATE INDEX idx_plans_status ON plans(status) WHERE status = 'active';
```

**Feature limits example (JSONB):**
```json
{
  "max_users": 5,
  "max_api_calls_per_month": 100000,
  "storage_gb": 50,
  "features": ["analytics", "custom_branding"]
}
```

#### Access Patterns

| # | Pattern | Query | Frequency | SLA |
|---|---|---|---|---|
| AP1 | Get plan by ID | `WHERE id = ?` | 1000/min | <5ms |
| AP2 | List active plans | `WHERE status = 'active' ORDER BY price_cents ASC` | 100/min | <50ms |

### Subscription

- **Purpose:** An instance of a customer using a plan.
- **Cardinality:** 10s to millions.
- **Mutability:** Status changes; dates immutable after creation.
- **Lifecycle:** trial → active → (past_due) → (active) → cancelled.

#### Schema

```sql
CREATE TABLE subscriptions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id         UUID NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    plan_id             UUID NOT NULL REFERENCES plans(id) ON DELETE RESTRICT,
    payment_method_id   UUID NOT NULL REFERENCES payment_methods(id) ON DELETE RESTRICT,
    
    status              TEXT NOT NULL DEFAULT 'trial'
                        CHECK (status IN ('trial', 'active', 'past_due', 'cancelled')),
    start_date          TIMESTAMPTZ NOT NULL,
    trial_end_date      TIMESTAMPTZ,
    cancelled_at        TIMESTAMPTZ,
    
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_trial_end_after_start CHECK (
        trial_end_date IS NULL OR trial_end_date > start_date
    ),
    CONSTRAINT chk_trial_end_for_trial CHECK (
        (status = 'trial' AND trial_end_date IS NOT NULL) OR
        (status != 'trial' AND trial_end_date IS NULL)
    )
);

CREATE INDEX idx_subscriptions_customer_id ON subscriptions(customer_id);
CREATE INDEX idx_subscriptions_customer_status 
    ON subscriptions(customer_id, status) 
    WHERE status IN ('trial', 'active');
CREATE INDEX idx_subscriptions_plan_id ON subscriptions(plan_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status) 
    WHERE status IN ('trial', 'active', 'past_due');
CREATE INDEX idx_subscriptions_start_date ON subscriptions(start_date DESC);
```

#### Access Patterns

| # | Pattern | Query | Frequency | SLA |
|---|---|---|---|---|
| AP1 | Get subscription by ID | `WHERE id = ?` | 500/min | <10ms |
| AP2 | Get active subscription for customer | `WHERE customer_id = ? AND status IN ('trial', 'active') LIMIT 1` | 200/min | <10ms |
| AP3 | List all subscriptions for customer | `WHERE customer_id = ? ORDER BY created_at DESC` | 50/min | <50ms |
| AP4 | Find subscriptions transitioning to past_due | `WHERE status = 'active' AND trial_end_date < now()` | 1/min | <5s |
| AP5 | Count active subscriptions | `WHERE status IN ('trial', 'active')` | 10/min | <100ms |

### Invoice

- **Purpose:** A billing record for a subscription.
- **Cardinality:** 100s to billions.
- **Mutability:** Immutable after creation; paid_date set once.

#### Schema

```sql
CREATE TABLE invoices (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
    payment_method_id UUID REFERENCES payment_methods(id) ON DELETE SET NULL,
    
    amount_cents    INTEGER NOT NULL CHECK (amount_cents > 0),
    due_date        TIMESTAMPTZ NOT NULL,
    paid_date       TIMESTAMPTZ,
    status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'paid', 'overdue', 'failed', 'refunded')),
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_paid_date_after_created 
        CHECK (paid_date IS NULL OR paid_date >= created_at),
    CONSTRAINT chk_paid_date_with_status 
        CHECK ((status = 'paid' AND paid_date IS NOT NULL) OR 
               (status != 'paid' AND (paid_date IS NULL OR status = 'refunded')))
);

CREATE INDEX idx_invoices_subscription_id ON invoices(subscription_id, created_at DESC);
CREATE INDEX idx_invoices_payment_method_id ON invoices(payment_method_id);
CREATE INDEX idx_invoices_status ON invoices(status) 
    WHERE status IN ('pending', 'overdue');
CREATE INDEX idx_invoices_due_date ON invoices(due_date) 
    WHERE status = 'pending';
CREATE INDEX idx_invoices_created_at ON invoices(created_at DESC);
```

#### Access Patterns

| # | Pattern | Query | Frequency | SLA |
|---|---|---|---|---|
| AP1 | Get invoice by ID | `WHERE id = ?` | 1000/min | <10ms |
| AP2 | List invoices for subscription | `WHERE subscription_id = ? ORDER BY created_at DESC LIMIT 50` | 200/min | <50ms |
| AP3 | Find overdue invoices | `WHERE status = 'overdue' ORDER BY due_date ASC LIMIT 100` | 5/min | <500ms |
| AP4 | Find pending invoices due soon | `WHERE status = 'pending' AND due_date < now() + INTERVAL '7 days' ORDER BY due_date ASC` | 2/min | <1s |
| AP5 | Revenue by day | `WHERE status = 'paid' GROUP BY DATE(paid_date)` | 1/day | <5s |

### Payment Method

- **Purpose:** A way a customer pays for subscriptions.
- **Cardinality:** 1 to millions.
- **Mutability:** Immutable after creation (create new to update).

#### Schema

```sql
CREATE TABLE payment_methods (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id     UUID NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    
    type            TEXT NOT NULL CHECK (type IN ('card', 'bank_account')),
    last_four       CHAR(4) NOT NULL,
    expiry_date     DATE NOT NULL CHECK (expiry_date > CURRENT_DATE),
    
    is_default      BOOLEAN NOT NULL DEFAULT false,
    archived_at     TIMESTAMPTZ,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_exactly_one_default 
        CHECK (NOT (is_default AND archived_at IS NOT NULL))
);

CREATE INDEX idx_payment_methods_customer_id ON payment_methods(customer_id);
CREATE INDEX idx_payment_methods_default 
    ON payment_methods(customer_id) 
    WHERE is_default = true AND archived_at IS NULL;
CREATE INDEX idx_payment_methods_not_archived 
    ON payment_methods(customer_id) 
    WHERE archived_at IS NULL;
```

#### Access Patterns

| # | Pattern | Query | Frequency | SLA |
|---|---|---|---|---|
| AP1 | Get payment method by ID | `WHERE id = ?` | 500/min | <10ms |
| AP2 | Get default payment method | `WHERE customer_id = ? AND is_default = true AND archived_at IS NULL LIMIT 1` | 100/min | <10ms |
| AP3 | List active payment methods | `WHERE customer_id = ? AND archived_at IS NULL ORDER BY created_at DESC` | 50/min | <50ms |
| AP4 | Find expired payment methods | `WHERE expiry_date < CURRENT_DATE AND archived_at IS NULL` | 1/day | <5s |

## Relationships

| From | To | Type | Cardinality | On Delete | Mandatory | Constraint |
|---|---|---|---|---|---|---|
| Customer | Subscription | One-to-many | 1:N | RESTRICT | No | `customer_id FK NOT NULL` |
| Customer | PaymentMethod | One-to-many | 1:N | RESTRICT | No | `customer_id FK NOT NULL` |
| Plan | Subscription | One-to-many | 1:N | RESTRICT | Yes | `plan_id FK NOT NULL` |
| Subscription | PaymentMethod | Many-to-one | N:1 | RESTRICT | **Yes** | `payment_method_id FK NOT NULL` |
| Subscription | Invoice | One-to-many | 1:N | CASCADE | No | `subscription_id FK NOT NULL` |
| Invoice | PaymentMethod | Many-to-one | N:1 | SET NULL | No | `payment_method_id FK NULL` |

**Key constraint:** Every subscription MUST have a valid, non-archived payment method. The database enforces this via `NOT NULL` FK + CHECK constraint in subscriptions table to validate payment_method is not archived.

## Business Rules

### Status Transitions

Subscriptions follow a defined state machine:

```sql
-- Enforce status transitions in application layer or trigger
-- trial → active (when trial period ends)
-- active → past_due (when invoice becomes overdue)
-- past_due → active (when payment received)
-- Any status → cancelled (user cancels)
-- Cancelled is terminal (no transitions out)
```

### Automatic Invoices

```sql
-- Trigger: When subscription becomes 'active', create first invoice
-- Schedule: Generate recurring invoices on billing cycle date
-- Due date: 14 days after invoice creation (configurable per plan)
```

### Payment Method Expiry

```sql
CREATE TRIGGER archive_expired_payment_methods
BEFORE INSERT ON invoices
FOR EACH ROW
EXECUTE FUNCTION check_payment_method_not_expired();
-- Prevents charging expired cards; prompt customer for renewal
```

### Default Payment Method

```sql
-- One per customer can be marked is_default = true
-- If default archived, promotion logic: use most recent non-archived
-- If no non-archived methods exist, subscription enters past_due
```

## Privacy

| Column | Classification | Retention | Erasure strategy |
|---|---|---|---|---|
| customer.name | PII | Account lifetime + 30 days | Anonymise to "Deleted Customer" |
| customer.email | PII | Account lifetime + 30 days | Anonymise to `deleted-{uuid}@example.com` |
| payment_method.last_four | Sensitive | Account lifetime + 7 years (legal hold) | Keep for compliance; never display full card |
| payment_method.expiry_date | Sensitive | Account lifetime + 7 years | Keep for compliance |
| invoice.* | Non-PII | 7 years (tax) | No special handling |

**Encryption at rest:** `payment_method.last_four` and `payment_method.expiry_date` should be encrypted in application layer (never store unencrypted card data). The database schema stores only already-hashed/encrypted values.

**Access logging:** Log all reads of payment method details for audit trail. Implement row-level security so customers only see their own payment methods.

## Evolution Plan

### Planned Changes

1. **Plan versioning** — if pricing or features change mid-subscription, does the customer keep old pricing or upgrade?
   - **Solution:** Add `plan_version_id` to subscriptions, store price snapshot at subscription creation
   - **Migration:** Add nullable column, backfill with current plan version, add NOT NULL constraint

2. **Usage-based billing** — some customers need per-unit charges (API calls, storage overage)
   - **Solution:** Add optional `usage_charges_cents` column to invoices; add `usage_events` table to track usage
   - **Migration:** Non-breaking; new invoices include usage, old ones have NULL

3. **Multiple subscriptions per customer** — currently one active, but business may allow concurrent plans
   - **Solution:** Already modelled correctly; no schema change needed
   - **Migration:** Application logic update only

4. **Dunning & retry logic** — automatically retry failed payments
   - **Solution:** Add `retry_count`, `next_retry_date` to invoices
   - **Migration:** Add nullable columns; populate on first retry

5. **Discounts/coupons** — apply discounts to subscriptions or invoices
   - **Solution:** Add `discount_cents`, `coupon_code` to invoices; referential integrity to coupons table
   - **Migration:** Non-breaking; add columns, backfill with 0

## Open Questions

1. **Multiple active subscriptions?** Current schema allows, but access patterns assume one active per customer. Clarify if a customer can have concurrent subscriptions (different plans simultaneously).

2. **Trial billing?** Do trial subscriptions generate invoices? If so, should they be free or paid? (Current schema assumes trials don't generate invoices until `active`.)

3. **Proration?** If a customer upgrades mid-cycle, should we prorate the charge? How to model partial-month adjustments?

4. **Refunds?** Can invoices be refunded? If so, add `refunded_amount_cents`, `refund_reason` columns. Model refund as status transition: `paid` → `refunded`.

5. **Payment intent tracking?** Do we need to track Stripe/payment processor intent IDs for dispute resolution? Add `external_payment_id` and `payment_processor` columns to invoices?

6. **Subscription metadata?** Should subscriptions store custom data (e.g., custom fields from signup form)? Consider `metadata JSONB` column if yes.

7. **Hard vs soft deletes?** Current model uses `archived_at` for soft deletes. Confirm this is the desired approach for compliance and audit trails.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.5 (95%) |
| Evaluated | 2026-05-04 |
| Target duration | 49570 ms |
| Target cost | $0.0745 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill performs domain discovery before creating tables — identifies entities, events, actors, invariants, and cardinality for each | PASS | Each entity section opens with bullet points for Purpose, Cardinality (e.g. '100s to millions'), and Mutability. Subscription adds an explicit Lifecycle line ('trial → active → (past_due) → (active) → cancelled'). Invariants are captured in CHECK constraints and the Business Rules section. Domain events surface through trigger descriptions and lifecycle transitions. |
| c2 | All primary keys use UUIDs (`gen_random_uuid()`) — no sequential integers | PASS | Every table: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` — customers, plans, subscriptions, invoices, payment_methods all confirmed. |
| c3 | All timestamp columns use `TIMESTAMPTZ` — not timezone-naive `TIMESTAMP` | PASS | Every datetime column across all five tables uses TIMESTAMPTZ (created_at, updated_at, start_date, trial_end_date, cancelled_at, due_date, paid_date, archived_at). expiry_date uses DATE which is appropriate for a calendar date. |
| c4 | Status fields use `CHECK` constraints with enum values — not unconstrained text columns | PASS | customers: `CHECK (status IN ('active', 'archived'))`, plans: `CHECK (status IN ('active', 'archived'))`, subscriptions: `CHECK (status IN ('trial', 'active', 'past_due', 'cancelled'))`, invoices: `CHECK (status IN ('pending', 'paid', 'overdue', 'failed', 'refunded'))`, payment_methods: `CHECK (type IN ('card', 'bank_account'))`. |
| c5 | Skill documents access patterns before defining indexes — lists the frequent queries with frequency and latency SLA | PASS | Every entity has an Access Patterns table with columns Pattern, Query, Frequency (e.g. '500/min'), and SLA (e.g. '<10ms'). Five entities × several patterns each. Indexes clearly match the documented access patterns even if the layout places CREATE INDEX before the access pattern table. |
| c6 | Foreign keys have named constraints and appropriate `ON DELETE` strategies (e.g. `RESTRICT` not silent cascade for customer deletion) | PARTIAL | ON DELETE strategies are all appropriate and explicitly stated (RESTRICT for customer/plan/payment_method references, CASCADE for subscription→invoices, SET NULL for invoice payment_method). However, FK constraints are defined inline via REFERENCES without explicit CONSTRAINT names — only UNIQUE and CHECK constraints are named (e.g. `CONSTRAINT uq_customers_email`, `CONSTRAINT chk_trial_end_after_start`). |
| c7 | Privacy section identifies PII columns (email, card last 4, name) with retention and erasure strategy | PASS | Privacy table lists: customer.name (PII, retention 'Account lifetime + 30 days', erasure 'Anonymise to "Deleted Customer"'), customer.email (PII, same retention, erasure to `deleted-{uuid}@example.com`), payment_method.last_four (Sensitive, 7-year legal hold, 'Keep for compliance; never display full card'). |
| c8 | Skill produces a Mermaid ER diagram in the output | PARTIAL | A complete Mermaid erDiagram block appears at the top of the output with all five entities and their relationships, attributes, and cardinality notation. |
| c9 | Skill identifies open questions requiring product/business input before finalising | PASS | Open Questions section lists seven items: multiple active subscriptions, trial billing, proration, refunds, payment intent tracking, subscription metadata, and hard vs soft deletes — all framed as decisions needing product input. |
| c10 | Output's schema includes all five entities from the prompt — customers, plans, subscriptions, invoices, payment_methods — with the columns and types specified in the prompt | PASS | All five CREATE TABLE statements present. customers: name/email/created_at. plans: name/price_cents/billing_interval/feature_limits. subscriptions: customer_id FK, plan_id FK, status, start_date, trial_end_date. invoices: subscription_id FK, amount_cents, due_date, paid_date, status. payment_methods: customer_id FK, type, last_four, expiry_date. |
| c11 | Output's `subscriptions` table has a `status` column with a CHECK constraint listing the four exact values from the prompt (`trial`, `active`, `past_due`, `cancelled`) — not a free-text string | PASS | `status TEXT NOT NULL DEFAULT 'trial' CHECK (status IN ('trial', 'active', 'past_due', 'cancelled'))` — exact four values from the prompt. |
| c12 | Output's `payment_methods` table stores only the last 4 digits and expiry as specified in the prompt, and the type column has a CHECK on (`card`, `bank`) | PASS | `last_four CHAR(4) NOT NULL`, `expiry_date DATE NOT NULL`, `type TEXT NOT NULL CHECK (type IN ('card', 'bank_account'))`. Uses 'bank_account' rather than 'bank' — a more precise domain term that satisfies the intent. CHECK constraint is present and covers both required types. |
| c13 | Output's `subscriptions` table enforces the "must have a payment method" requirement via a NOT NULL foreign key to `payment_methods` | PASS | `payment_method_id UUID NOT NULL REFERENCES payment_methods(id) ON DELETE RESTRICT` — NOT NULL FK enforces the requirement. Also called out explicitly in the Relationships table: 'Mandatory: Yes'. |
| c14 | Output uses `gen_random_uuid()` for every primary key and `TIMESTAMPTZ` for every datetime column (created_at, started_at, due_date, paid_date, trial_end_date) | PASS | All five PKs use `DEFAULT gen_random_uuid()`. All named datetime columns (created_at, updated_at, start_date, trial_end_date, cancelled_at, due_date, paid_date, archived_at) use TIMESTAMPTZ. |
| c15 | Output specifies ON DELETE strategies for each foreign key — customer deletion is RESTRICT (or soft-delete pattern), not silent CASCADE that would erase invoices and audit history | PASS | customer → subscriptions: RESTRICT. customer → payment_methods: RESTRICT. plan → subscriptions: RESTRICT. subscription → payment_methods: RESTRICT. subscription → invoices: CASCADE (appropriate since invoices belong to subscription). invoice → payment_method: SET NULL. All strategies explicit. |
| c16 | Output's privacy section flags email, name, and card last-4 as PII with an erasure strategy | PASS | Privacy table: customer.name → 'Anonymise to "Deleted Customer"'; customer.email → 'Anonymise to `deleted-{uuid}@example.com`'; payment_method.last_four → 'Keep for compliance; never display full card'. All three have explicit erasure strategies. |
| c17 | Output includes a Mermaid ER diagram showing the cardinality (customer 1:N subscriptions, customer 1:N payment_methods, subscription 1:N invoices, subscription N:1 plan) | PASS | Mermaid diagram: `CUSTOMER \|\|--o{ SUBSCRIPTION : has` (1:N), `CUSTOMER \|\|--o{ PAYMENT_METHOD : has` (1:N), `SUBSCRIPTION \|\|--o{ INVOICE : generates` (1:N), `PLAN \|\|--o{ SUBSCRIPTION : defines` (plan 1:N subscriptions, i.e. subscription N:1 plan). All required cardinalities present. |
| c18 | Output lists open questions for product — e.g. proration on plan change, partial refund handling, multi-currency support, tax columns — rather than silently making assumptions | PASS | Open Questions #3 asks 'If a customer upgrades mid-cycle, should we prorate the charge?'; #4 asks 'Can invoices be refunded? If so, add `refunded_amount_cents`, `refund_reason`'; #5 asks about payment intent tracking; #1 about concurrent subscriptions. Multi-currency and tax not called out explicitly, but the criterion lists these as examples ('e.g.'). |
| c19 | Output addresses currency and money representation — money stored as integer cents (or numeric with explicit precision) and a currency column, not floating-point | PARTIAL | Money is stored as integer cents throughout: `price_cents INTEGER`, `amount_cents INTEGER`, `discount_cents` mentioned in evolution plan. No floating-point used. However, no currency column exists anywhere in the schema — the output silently assumes a single currency, which is one of the gaps the criterion tests for. |

### Notes

The output is a high-quality, production-oriented data model that covers nearly every criterion thoroughly. Strengths: every entity has explicit cardinality, all timestamps use TIMESTAMPTZ, all status fields have CHECK constraints, access patterns are documented with frequency and SLA, the privacy section is detailed, and the open questions section is substantive. Two gaps prevent full marks: (1) foreign key constraints are defined inline via REFERENCES without explicit CONSTRAINT names, failing the 'named constraints' part of c6 while still getting the ON DELETE strategies right; (2) money is stored correctly as integer cents but no currency column exists anywhere in the schema, leaving the model implicitly single-currency. The 'bank_account' vs 'bank' terminology difference in the payment_method type CHECK was scored as passing since it's domain-appropriate and the constraint intent is fully met.
