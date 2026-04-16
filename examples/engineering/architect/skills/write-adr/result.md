# Write adr skill structure

Checking that the write-adr skill produces ADRs that follow the MADR format with all required sections, honest trade-offs, and measurable confirmation criteria.

## Prompt

> Review the write-adr skill definition and verify it produces complete, honest ADR documents rather than decision justifications written after the fact.

The write-adr skill, applied to documenting the decision to use PostgreSQL BYTEA for binary content storage, would produce the following ADR.

---

```markdown
---
status: "proposed"
date: 2026-04-16
decision-makers: [Platform Architect, Backend Lead]
consulted: [Infrastructure Lead, Security Team]
informed: [Engineering Team, Product Engineering]
---

## Output

# ADR-0005: Use PostgreSQL BYTEA for binary content storage

### Context and Problem Statement

The platform currently stores uploaded binary content (PDF reports, CSV exports) as file paths
to an S3-compatible object store. We need to decide how to store binary artefacts produced
during processing — intermediate pipeline outputs that are <5MB each, have a 24-hour TTL, and
are accessed exclusively within a single transaction context. Do we store them inline in
PostgreSQL, or continue routing all binary content through the object store?

### Decision Drivers

- Access latency: artefacts are read immediately after write in the same request
- Operational complexity: reducing external service dependencies reduces failure modes
- Content size: artefacts average 500KB–2MB, all under the BYTEA practical limit
- Retention: 24-hour TTL makes object store lifecycle rules awkward to configure
- Consistency: if a pipeline transaction fails, orphaned S3 objects are hard to clean up

### Considered Options

1. PostgreSQL BYTEA inline storage
2. Object store (S3/MinIO) — status quo
3. Do nothing — keep routing all binary content through the object store unchanged

### Decision Outcome

Chosen option: **Option 1 — PostgreSQL BYTEA inline storage**, because the content is small,
transactionally-scoped, and short-lived. Keeping the data in the transaction context eliminates
the consistency problem and the extra network hop. Object store benefits (scale, independence)
are designed for persistent, large, independently-accessed content — none of which applies here.

### Consequences

**Positive:**
- No orphaned objects after pipeline failures — BYTEA rolls back with the transaction
- Eliminates a network round-trip for content written and read in the same request
- Simpler local development — no object store emulator needed for this use case

**Negative:**
- PostgreSQL row sizes increase; large TOAST tables can slow vacuum and index scans if
  artefacts frequently exceed the 8KB inline threshold
- Migration path is harder if content size requirements grow beyond practical BYTEA limits
- pg_dump backup sizes increase proportionally with stored binary content

**Risks:**
- If average artefact size grows to >5MB, query performance will degrade — this decision
  should be revisited if that threshold is crossed

### Confirmation

- Review date: 2027-01-01 (or sooner if median artefact size exceeds 3MB)
- Metric: `SELECT avg(pg_column_size(content)) FROM pipeline_artefacts` — alert if median
  exceeds 2MB
- Automated: vacuum duration alert on artefacts table in monitoring dashboard
- Reconsideration trigger: any new binary content type with expected size >5MB must be
  evaluated against this decision before being routed to the artefacts table

### Pros and Cons of Options

#### Option 1: PostgreSQL BYTEA inline storage

- Good, because transactional atomicity — no orphaned files on rollback
- Good, because eliminates network dependency for transactionally-scoped content
- Bad, because TOAST overhead increases as content grows
- Bad, because makes horizontal PostgreSQL sharding harder in future
- Neutral, because BYTEA supports up to ~1GB; current envelope is 2MB

#### Option 2: Object store (S3/MinIO) — status quo

- Good, because proven pattern for binary storage already in use elsewhere
- Good, because scales to any content size without schema changes
- Bad, because orphaned objects accumulate if pipeline fails mid-transaction
- Bad, because adds a network round-trip within a synchronous request
- Neutral, because lifecycle rules can handle TTL but require separate configuration

#### Option 3: Do nothing

- Good, because no migration work required
- Bad, because the consistency problem (S3 artefacts not rolled back with transactions) persists
- Bad, because adds an external dependency for a use case that doesn't benefit from it
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8/8 (100%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Skill uses MADR format and requires all key sections — Step 3 lists every section as "(none optional)": frontmatter with status, date, decision-makers, consulted, and informed; Title; Context and Problem Statement; Decision Drivers; Considered Options; Decision Outcome; Consequences (positive/negative/risks); Confirmation; and Pros and Cons of Options. Each has explicit instructions.

- [x] PASS: Skill requires title to describe both problem and solution — line 58: `` `# ADR-NNNN: {Short title — describes the problem AND solution}` `` with concrete good/bad examples: "ADR-0005: Database decision" (too vague) and "ADR-0005: We should use PostgreSQL" (no problem stated) both called out explicitly.

- [x] PASS: Skill mandates at least two options including do-nothing — Considered Options instruction: "At least 2 options. Always include 'do nothing / status quo' if applicable."

- [x] PASS: Skill requires at least one negative consequence with explicit honesty check — Consequences section: "every decision has downsides — if you can't name one, you haven't thought hard enough." Quality Checklist item 5 repeats this as a named honesty check.

- [x] PASS: Skill requires measurable confirmation criteria — Confirmation section lists four specific mechanisms (review date, metric, automated test/CI check, reconsideration conditions). Quality Checklist item 7: "Confirmation criteria are measurable or observable."

- [x] PASS: Skill provides a quality checklist — 9-item checklist framed as a pre-delivery gate: "Before declaring the ADR complete." Covers title, context, options count, decision drivers specificity, consequences honesty, risks, confirmation measurability, rejected options fairness, and related ADR links.

- [x] PASS: Skill lists all four required anti-patterns — Anti-Patterns table names "Retroactive ADR," "No alternatives," "Strawman options," and "Orphaned ADR" (described as no confirmation criteria). All four present with problem and fix columns.

- [x] PASS: Skill specifies file naming and target directory — Output section: `NNNN-kebab-case-title.md` with a concrete example, and target directory fallback list: `docs/adr/`, `docs/architecture-decisions/`, `docs/decisions/`. Creates `docs/adr/` if none exists.

### Notes

The SKILL.md references a template file at `${CLAUDE_PLUGIN_ROOT}/templates/adr-template.md`. If that file is missing from the plugin's `templates/` directory, Step 3 falls back to the inline section instructions, which are complete enough to stand alone. The quality checklist includes "Rejected options have fair representation (not strawmen)" as a distinct item beyond the strawman anti-pattern — it catches cases where technically-described options are still unrealistic in practice.
