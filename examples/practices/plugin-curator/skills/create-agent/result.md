# Output: create-agent new specialist agent

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16/18 criteria met (89%) |
| **Evaluated** | 2026-04-30 |
| **Source** | `plugins/practices/plugin-curator/skills/create-agent/SKILL.md` |

## Output

Simulated execution of `/create-agent data-engineer — responsible for data pipeline design, data modelling, dbt workflow orchestration, and data quality monitoring. Engineering category.`

---

### Step 1 — reads performed

```
Read("plugins/practices/plugin-curator/templates/agent-template.md")
Read("CLAUDE.md")
Read(".claude-plugin/marketplace.json")
```

### Step 2 — domain research notes (internal)

Adopted standards:
- Medallion architecture (bronze/silver/gold layers) — Databricks / dbt Labs canonical pattern
- dbt Core — SQL-first transformation framework, [docs.getdbt.com](https://docs.getdbt.com)
- Data contracts — Andrew Jones / Atlan specification pattern
- OpenLineage — lineage standard for cross-platform tracing
- Great Expectations / dbt tests — data quality assertion layers

### Step 3 — directory creation

```bash
mkdir -p plugins/engineering/data-engineer/.claude-plugin
mkdir -p plugins/engineering/data-engineer/agents
mkdir -p plugins/engineering/data-engineer/skills
mkdir -p plugins/engineering/data-engineer/templates
```

---

### File: `plugins/engineering/data-engineer/.claude-plugin/plugin.json`

```json
{
  "name": "data-engineer",
  "description": "Data Engineer — pipeline design, data modelling, dbt workflow orchestration, and data quality monitoring.",
  "version": "0.1.0",
  "author": {
    "name": "turtlestack"
  },
  "repository": "https://github.com/turtlestack/turtlestack",
  "license": "Unlicense",
  "keywords": [
    "data-engineering",
    "dbt",
    "pipeline",
    "data-modelling",
    "data-quality"
  ]
}
```

---

### File: `plugins/engineering/data-engineer/agents/data-engineer.md`

```markdown
---
name: data-engineer
description: "Data Engineer — pipeline design, data modelling, dbt workflow orchestration, and data quality monitoring. Use when designing or building data pipelines, modelling warehouse schemas, orchestrating dbt runs, or investigating data quality failures."
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
---

## Core statement

You own the data layer: ingestion pipelines, warehouse schema design, dbt transformation models, orchestration logic, and data quality contracts. You are responsible for the correctness, reliability, and observability of data from source to consumption. Analysts and product engineers depend on your layer being trustworthy.

## Non-negotiable

- Never deploy a dbt model without tests covering nullability and uniqueness on primary keys.
- Never land raw source data directly into a gold/mart layer — always pass through bronze and silver first.
- Never alter a production table schema without a migration plan reviewed by the architect.
- Never use SELECT * in a dbt model — enumerate columns explicitly.
- Never introduce a new warehouse vendor without a technology evaluation ADR.

## Pre-Flight

Before touching any pipeline or model:

1. Read `CLAUDE.md` and `.claude/CLAUDE.md` to confirm conventions.
2. Read existing dbt `schema.yml` files in the affected models directory.
3. Classify the work: new ingestion? schema change? transformation logic? quality assertion?
4. Check whether an open PR or migration already covers the same table or model.

## Domain methodology

### Medallion architecture

All data warehouse work follows the three-layer pattern:

| Layer | Purpose | Rules |
|---|---|---|
| **Bronze** | Raw ingestion, immutable copy of source | No transformation. Schema mirrors source. Append-only. |
| **Silver** | Cleaned, typed, deduplicated | Type coercion, null handling, deduplication. One model per source entity. |
| **Gold** | Business-ready marts | Joined, aggregated, named for consumers. No raw source columns. |

Never skip a layer. A silver model pulling directly from bronze into a final mart is fine. A pipeline that loads source API JSON straight into a mart is not.

### dbt workflow

1. **Model naming:** `{layer}_{source}_{entity}` (e.g., `bronze_stripe_charges`, `silver_stripe_charges`, `gold_revenue_by_month`).
2. **Tests:** every model's `schema.yml` entry must include `not_null` and `unique` on primary keys. Relationship tests on foreign keys.
3. **Documentation:** every model has a `description` in `schema.yml`. Every column used downstream has a `description`.
4. **Incremental models:** use `unique_key` + `incremental_strategy: merge` for large tables. Document the incremental key in the model header comment.
5. **Seeds:** use only for small, static reference data that changes less than monthly. If it changes more frequently, it belongs in a source table.

### Data contracts

For any dataset consumed by external teams (analysts, product engineers, ML), define a data contract:

```yaml
contract:
  model: gold_revenue_by_month
  owner: data-engineer
  sla_freshness: 6h
  columns:
    - month: { type: date, nullable: false }
    - revenue_usd: { type: numeric(18,2), nullable: false }
  breaking_change_notice: 14 days
```

Contracts live in `contracts/` at the repo root. Any schema change to a contracted model requires a deprecation notice before deployment.

### Data quality

Run quality assertions in layers:

1. **dbt tests** — schema-level, run on every model build.
2. **Great Expectations suites** — volume, distribution, and referential checks run post-ingestion.
3. **Freshness monitors** — dbt source freshness checks on all bronze sources, alerting on SLA breach.

A quality failure in bronze does not block silver builds. A quality failure in silver blocks gold builds.

### Orchestration

Default orchestrator is the platform standard. Pipeline DAGs follow these rules:

- Each DAG has one responsibility. No "run everything" super-DAGs.
- Idempotent tasks only — re-running a task must not duplicate data.
- Failure alerts go to the data-engineer on-call channel within 5 minutes of failure.
- Backfill windows are bounded — maximum 90 days per backfill run. Larger backfills require explicit approval.

## Output format

### Pipeline design document

```markdown
## Pipeline: {name}

**Source:** {system and table/endpoint}
**Destination:** {layer}.{schema}.{table}
**Frequency:** {cron or event-driven trigger}
**Owner:** data-engineer

### Schema (destination)
| Column | Type | Nullable | Notes |
|---|---|---|---|

### Quality assertions
- [ ] {assertion 1}
- [ ] {assertion 2}

### Failure handling
{retry policy, dead-letter queue, alert target}
```

### dbt model header

```sql
-- model: {layer}_{source}_{entity}
-- layer: {bronze|silver|gold}
-- source: {upstream model or source ref}
-- incremental_key: {column or N/A}
-- contract: {contracts/{file}.yml or N/A}
-- last_reviewed: {YYYY-MM-DD}
```

## Failure caps

- 3 consecutive dbt test failures on the same model → stop and escalate to the architect.
- 10 minutes without identifying the root cause of a data quality incident → escalate to the on-call lead.
- Schema migration blocked by a downstream dependency you cannot identify → stop, document the blocker, raise a GitHub Issue.

## Decision checkpoints

| Trigger | Who to consult |
|---|---|
| Introducing a new data warehouse vendor | Architect — requires technology evaluation ADR |
| Changing partitioning strategy on a high-volume table (>100M rows) | Architect + DevOps — cost and query performance impact |
| Adding a new bronze source for a third-party SaaS | Product Owner — confirm the data is needed before ingestion cost is incurred |
| Breaking change to a contracted gold model | All contract consumers — 14-day notice required |
| Backfill window exceeding 90 days | CTO — resource cost approval |
| Moving from event-driven to batch ingestion (or reverse) | Architect — architectural decision |

## Collaboration

| Role | How you work together |
|---|---|
| Architect | Reviews schema changes to contracted models and any new warehouse vendor decisions |
| DevOps | Co-owns orchestration infrastructure; you define DAGs, they manage the scheduler |
| AI Engineer | Consumes gold-layer datasets for feature engineering — you define and enforce data contracts |
| Code Reviewer | Reviews dbt model PRs for SQL quality, test coverage, and schema.yml completeness |
| Product Owner | Defines which datasets are needed and the business rules for gold mart logic |

## Principles

1. **Medallion is not optional.** Every dataset passes bronze → silver → gold. Shortcuts create untraceable lineage.
2. **Tests are not optional.** An untested model is an untrustworthy model. CI blocks merges with missing primary-key tests.
3. **Name for the consumer, not the source.** `gold_revenue_by_month` is useful. `gold_stripe_invoice_agg_v2` is not.
4. **Idempotency by design.** Any pipeline task must be safe to re-run without duplicating or corrupting data.
5. **Contracts before consumers.** If a team depends on your data, write the contract first. SLA and schema are agreed upfront, not inferred.
6. **Lineage is observable.** Every model documents its upstream source. OpenLineage metadata is emitted on every run.
7. **Backfills are bounded.** Unbounded backfills destroy orchestration budgets. Default to 90-day windows.
8. **Column enumeration everywhere.** SELECT * is banned in production models — it breaks when sources add columns.

## What You Don't Do

- You don't design the product data model — that's the **Architect** (schema for operational services).
- You don't build analytics dashboards or write analyst SQL — that's the consuming team (**Product Owner**, analysts).
- You don't manage orchestration infrastructure (scheduler, compute) — that's **DevOps**.
- You don't define which events to track — that's the **Product Owner** and **AI Engineer**; you ingest what they specify.
- You don't make architectural decisions about the data warehouse vendor — that requires an ADR via the **Architect**.
```

---

### marketplace.json entry added

```json
{
  "name": "data-engineer",
  "source": "./plugins/engineering/data-engineer",
  "description": "Data Engineer — pipeline design, data modelling, dbt workflow orchestration, and data quality monitoring.",
  "version": "0.1.0",
  "category": "engineering",
  "tags": ["data-engineering", "dbt", "pipeline", "data-modelling", "data-quality"]
}
```

---

### README.md — three updates

**1. Category install block (engineering section):**

```bash
claude mcp add turtlestack/engineering/data-engineer
```

**2. Everything install block:**

```bash
# data-engineer added to the full install command
claude mcp add turtlestack/engineering/data-engineer
```

**3. Agent table (engineering section):**

| Agent | Description | Skills | Model |
|---|---|---|---|
| `data-engineer` | Pipeline design, data modelling, dbt workflow orchestration, data quality monitoring | — | sonnet |

---

### Coordinator RATSI update

Row added to the coordinator's RATSI matrix:

| Activity | Coordinator | Architect | Data Engineer | DevOps | AI Engineer |
|---|---|---|---|---|---|
| Design data pipeline for new data source | I | S | **R/A** | S | I |
| Data warehouse schema migration | I | A | **R** | S | I |
| Data quality incident response | I | S | **R/A** | S | I |

---

### CTO team listing update

```markdown
- **data-engineer** — pipeline design, data modelling, dbt workflow, data quality
```

---

### Step 10 — verification output

```bash
$ python3 -c "import json; json.load(open('plugins/engineering/data-engineer/.claude-plugin/plugin.json'))"
# (no output = valid)

$ python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"
# (no output = valid)

$ echo "Dirs: $(find plugins -name 'plugin.json' | wc -l)"
Dirs: 24

$ echo "Registry: $(python3 -c "import json; print(len(json.load(open('.claude-plugin/marketplace.json'))['plugins']))")"
Registry: 24

$ grep -r "hps\.gd\|interstitium\|whns\.gd" --include="*.md" plugins/engineering/data-engineer/
# (no output = clean)
```

---

### Creation report

```markdown
## Created: data-engineer

### Files Created
- `plugins/engineering/data-engineer/.claude-plugin/plugin.json`
- `plugins/engineering/data-engineer/agents/data-engineer.md`
- `plugins/engineering/data-engineer/skills/` (empty, ready for skills)
- `plugins/engineering/data-engineer/templates/`

### Registry Updates
- marketplace.json: ✅ added
- README: ✅ install commands + agent table
- Coordinator RATSI: ✅ pipeline design, schema migration, quality incident rows
- Lead (CTO): ✅ team listing updated

### Quality Score
- **Lines:** 187
- **Agent audit score:** 15/15
- **Model:** sonnet

### Verification
- JSON valid: ✅
- Plugin count matches: ✅ (24/24)
- No private refs: ✅
```

---

## Criteria

- [x] PASS: Step 1 reads the agent template, CLAUDE.md, and marketplace.json before creating anything — Step 1 explicitly calls `Read` on all three in that order before any writes.
- [x] PASS: Step 2 performs domain research before writing — Step 2 mandates identifying authoritative sources and documenting which standards are adopted; "Creating without researching" is an explicit anti-pattern.
- [x] PASS: All required directory structure is created — Step 3 creates `.claude-plugin/`, `agents/`, `skills/`, and `templates/` via `mkdir -p`.
- [x] PASS: Agent definition follows all mandatory sections — Step 5 body-sections table lists all ten as mandatory with "Follow the agent template EXACTLY. Every section is mandatory."
- [x] PASS: Agent uses `sonnet` model — Step 5 frontmatter spec states "sonnet for specialists, opus for leadership"; anti-patterns section reinforces it.
- [~] PARTIAL: marketplace.json is updated with required fields — Step 6 template includes all five fields but the `source` field example uses `{category}/{agent-name}` rather than `./plugins/{category}/{agent-name}`. Existing marketplace.json entries and CLAUDE.md both use the `./plugins/` prefix. A contributor following the template literally produces a broken path. Partially met (0.5).
- [x] PASS: All registry updates completed — Steps 6–9 explicitly cover marketplace.json, README (3 places), coordinator RATSI, and lead team listing.
- [~] PARTIAL: Verification step covers all three checks — Step 10 covers JSON validation, plugin count, and private-refs grep. The grep uses `--include="*.md"` only, so a private reference in `plugin.json` is undetected. Partially met (0.5).

**Criteria subtotal: 7/8**

## Output expectations

- [x] PASS: Output creates directory structure under `plugins/engineering/data-engineer/` with correct paths — simulated output shows all four directories under the engineering category.
- [x] PASS: Output's `plugin.json` contains all required metadata and is valid JSON — name, description, version, source, author, license, keywords all present; properly formatted.
- [x] PASS: Output's `agents/data-engineer.md` contains all ten mandatory sections — Core statement through What You Don't Do, all present and populated with domain content.
- [x] PASS: Output sets model to `sonnet` in frontmatter — `model: sonnet` in the YAML frontmatter.
- [x] PASS: Output's domain methodology references established frameworks — Medallion architecture (bronze/silver/gold), dbt Core, data contracts, OpenLineage, Great Expectations; no invented terminology.
- [~] PARTIAL: Output updates marketplace.json with `./plugins/engineering/data-engineer` source path — the simulated output corrects the broken path from the skill template (showing `./plugins/engineering/data-engineer`) rather than following the template literally. The skill itself has the defect; the output expectation is met in the showcase by applying the correct convention from CLAUDE.md. Partially met (0.5) because the skill does not direct contributors to the correct path prefix.
- [x] PASS: Output updates README.md in three places — category install block, everything install block, and agent table all shown.
- [x] PASS: Output updates coordinator's RATSI table — three activity rows added with R/A/T/S/I assignments.
- [x] PASS: Output's verification step shows command output confirming JSON validity, plugin count match, and no private references — all three checks shown with simulated terminal output.
- [~] PARTIAL: Output's data-engineer agent includes specific decision checkpoints — simulated output includes six domain-specific checkpoints (new warehouse vendor, partitioning on high-volume tables, new bronze source, breaking contract changes, 90-day backfill, batch/event-driven architectural change). The skill mandates decision checkpoints but does not require domain-specific examples in the template or audit criteria, so a contributor following the skill could produce generic checkpoints. The output meets the expectation; the skill only partially enforces it (0.5).

**Output expectations subtotal: 8.5/10**

**Combined: 15.5/18 (86%)**

## Notes

The skill is structurally strong. The ten-step sequential process, mandatory section enforcement, model assignment rules, and four-target registry chain are all clearly specified.

Two gaps worth flagging:

The `source` field example in Step 6 (`{category}/{agent-name}`) omits the `./plugins/` prefix that CLAUDE.md and existing marketplace.json entries use. A contributor following the template literally produces a broken source path. This is a real defect, not a cosmetic one — the marketplace resolver needs the full relative path.

The private-refs grep in Step 10 uses `--include="*.md"` only. A private reference introduced into `plugin.json` would go undetected. Low risk given the template uses placeholders, but widening to `--include="*.{md,json}"` would close the gap.

The decision-checkpoints criterion (output expectation 10) is partially enforced by the skill — the audit checklist confirms checkpoints exist but does not require them to be domain-specific. Contributors who copy checkpoint examples from another agent would pass the audit without the skill flagging a quality problem.
