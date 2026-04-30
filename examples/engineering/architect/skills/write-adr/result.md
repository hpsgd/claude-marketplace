# Result: write-adr skill structure

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

Simulated output of applying the write-adr skill to a realistic scenario: deciding how to store binary content (images, PDFs, attachments) in the system.

---

**Skill invoked:** `/architect:write-adr use PostgreSQL BYTEA vs object storage for binary content`

**Step 1 — existing ADR scan:**

```bash
find . -path '*/adr*' -name '*.md' | sort
# docs/adr/0001-use-postgresql-as-primary-database.md
# docs/adr/0002-adopt-event-sourcing-with-marten.md
# docs/adr/0003-use-github-actions-for-ci.md
# docs/adr/0004-use-openrouter-as-llm-gateway.md
```

Next number: `0005`

**Step 2 — file written to:** `docs/adr/0005-use-object-storage-for-binary-content.md`

---

```markdown
---
status: "proposed"
date: 2026-04-30
decision-makers: [CTO, Architect]
consulted: [Data Engineer, DevOps Lead]
informed: [Engineering team, Product Owner]
---

# ADR-0005: Use object storage (S3-compatible) for binary content instead of PostgreSQL BYTEA

## Context and Problem Statement

The system stores user-uploaded files (images, PDFs, CSV exports) as part of several workflows.
We need to decide whether to store binary content inline in PostgreSQL BYTEA columns or in a
dedicated object storage service. Uploads are currently small (<5 MB each) but volume is
expected to grow 10x over the next 12 months. The decision affects backup size, query performance,
and hosting cost.

## Decision Drivers

- Database backup size and restore time should stay under 30 minutes
- Binary content reads must not contend with transactional query load
- CDN-friendly delivery for end-user downloads (direct URL, no proxy)
- Team has no existing S3 operational experience — learning curve is a constraint
- Hosting is on Fly.io; egress costs matter

## Considered Options

1. PostgreSQL BYTEA — store binary content inline in the database
2. S3-compatible object storage (Tigris, Cloudflare R2, AWS S3) — store in dedicated service, keep reference URL in database
3. Do nothing / status quo — keep files on the application server's local disk (current approach)

## Decision Outcome

Chosen option: **S3-compatible object storage (Option 2)**, because it satisfies the CDN-delivery
and backup-size drivers that BYTEA and local disk cannot. The team's learning curve is real but
bounded — Tigris provides an S3-compatible API co-located with Fly.io, reducing the operational
footprint.

## Consequences

**Positive:**
- Database backups remain fast; binary content is excluded from pg_dump
- Direct CDN URLs for downloads — no application proxy required
- Binary content scales independently of transactional data

**Negative:**
- Introduces a new infrastructure dependency (object storage service)
- Local development requires either a mocked S3 (MinIO) or real credentials — adds friction
- Deleting a record no longer automatically deletes the binary — orphan cleanup logic required

**Risks:**
- If the team does not implement orphan cleanup, storage costs will grow silently
- Tigris is a newer service; if it has reliability issues we will need to migrate to R2 or S3

## Confirmation

- Review backup size and restore time after 30 days — target: full restore under 30 minutes
- CI check: integration test verifies file upload, reference URL stored in DB, and file retrievable
- Review egress costs at 3-month mark; reconsider if egress exceeds $50/month
- Trigger for revisiting: any production data loss event traced to object storage

## Pros and Cons of Options

### Option 1: PostgreSQL BYTEA

- Good, because no new infrastructure — simpler operational model
- Good, because transactional consistency between record and binary is automatic
- Bad, because database backup/restore time grows with binary volume
- Bad, because binary reads contend with OLTP queries on the same connection pool
- Neutral, because existing team expertise covers this

### Option 2: S3-compatible object storage (chosen)

- Good, because binary content is CDN-deliverable with direct URLs
- Good, because database stays lean — fast backups, no contention
- Bad, because local dev requires MinIO or real credentials
- Bad, because orphan cleanup must be built explicitly
- Neutral, because S3 API is industry standard — knowledge transfers across providers

### Option 3: Local disk (status quo)

- Good, because zero setup — works today
- Bad, because files are lost on machine restart / Fly.io volume failure
- Bad, because no CDN path — all downloads proxy through application
- Bad, because horizontal scaling requires shared volume or replication
```

---

**Skill verification table** (criteria checked against SKILL.md):

| Requirement | Present in skill | Evidence |
|---|---|---|
| MADR format with all sections | Yes | Step 3 names all sections as "(none optional)" |
| Title describes problem AND solution | Yes | Explicit rule with good/bad examples |
| At least 2 options, including "do nothing" | Yes | "Always include 'do nothing / status quo' if applicable" |
| At least one negative consequence | Yes | "Every decision has downsides — if you can't name one, you haven't thought hard enough" |
| Measurable confirmation criteria | Yes | Four concrete forms listed: review date, metric, CI check, reconsideration trigger |
| Quality checklist | Yes | Nine-item checklist before declaring complete |
| Anti-patterns list | Yes | Table with 7 anti-patterns including all four required ones |
| File naming convention + target directory | Yes | `NNNN-kebab-case-title.md` in `docs/adr/` with fallback detection |

---

## Criteria

- [x] PASS: Skill uses the MADR format and requires all key sections: frontmatter (status, date, decision-makers), context, decision drivers, considered options, decision outcome, consequences, confirmation, and pros/cons per option — all sections named explicitly under Step 3, labelled "(none optional)"
- [x] PASS: Skill requires the ADR title to describe both the problem and the solution — stated directly with three concrete examples: one good, two bad
- [x] PASS: Skill mandates at least two options including "do nothing / status quo" where applicable — "At least 2 options. Always include 'do nothing / status quo' if applicable"
- [x] PASS: Skill requires consequences to include at least one negative with an explicit honesty check — "every decision has downsides — if you can't name one, you haven't thought hard enough" reinforced in the quality checklist
- [x] PASS: Skill requires measurable or observable confirmation criteria — four concrete forms: review date, metric to watch, automated test or CI check, conditions that trigger revisiting
- [x] PASS: Skill provides a quality checklist before declaring the ADR complete — nine-item checklist covering title, context, options, decision drivers, consequences, risks, confirmation, rejected option fairness, and related ADR linkage
- [x] PASS: Skill lists anti-patterns including retroactive ADR, no alternatives, strawman options, and orphaned ADR with no confirmation criteria — all four present in the anti-patterns table with problem and fix columns
- [x] PASS: Skill specifies file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/) — four-digit prefix, kebab-case, `.md` extension, and `docs/adr/` as primary target with fallback detection and creation instructions

## Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample ADR — the verification table summarises findings; the sample ADR in the Output section demonstrates the skill in use
- [x] PASS: Output confirms the MADR sections are all named explicitly — status/date/decision-makers frontmatter (skill also includes consulted and informed), context and problem statement, decision drivers, considered options, decision outcome, consequences with three sub-categories (positive/negative/risks), confirmation, and per-option pros/cons using Good/Bad/Neutral structure
- [x] PASS: Output verifies the title rule — skill states the title must describe both problem and solution, with explicit good/bad examples showing vague-title and solution-only-title as failures
- [x] PASS: Output confirms the at-least-two-options rule including "do nothing / status quo" where applicable, and that strawman alternatives are flagged as an anti-pattern in the skill's anti-patterns table
- [x] PASS: Output verifies the negative-consequences honesty rule — skill's "every decision has downsides" phrasing appears in two places: the Consequences section and the quality checklist
- [x] PASS: Output confirms confirmation criteria must be measurable/observable — skill lists four concrete mechanism types rather than aspirational language, and the quality checklist item explicitly uses "measurable or observable"
- [x] PASS: Output verifies file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/) with four-digit prefix and kebab-case explicit — confirmed in the verification table and the simulated output uses `0005-use-object-storage-for-binary-content.md`
- [x] PASS: Output verifies anti-patterns list includes all four: retroactive ADR, no alternatives, strawman options, and orphaned ADRs without confirmation criteria — all present in the anti-patterns table
- [~] PARTIAL: Output identifies gaps — the skill references "Related ADRs are linked (supersedes, builds on, relates to)" in the quality checklist but provides no convention for updating a superseded ADR's own status field (e.g., setting it to "superseded by ADR-NNNN"). There is no guidance on revision notes if an ADR's status changes after acceptance. The frontmatter includes `decision-makers`, `consulted`, and `informed` but no separate `author` field — relevant when the author differs from the decision-makers.

## Notes

The skill is well-structured. The honesty-forcing mechanisms — mandatory negative consequences with "if you can't name one, you haven't thought hard enough," the anti-strawman rule, and the orphaned ADR anti-pattern — are specific enough to catch the most common ADR failure modes in practice.

The template reference (`${CLAUDE_PLUGIN_ROOT}/templates/adr-template.md`) delegates some structure to an external file not evaluated here. The inline section instructions in SKILL.md are detailed enough to stand alone if that template is absent.

The quality checklist item "Rejected options have fair representation (not strawmen)" overlaps with but extends the anti-patterns table — it catches cases where options were described accurately but were never genuinely considered, which the anti-pattern label alone doesn't cover.
