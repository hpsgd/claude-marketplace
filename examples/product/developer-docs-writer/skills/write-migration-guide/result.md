# Write migration guide

Testing whether the write-migration-guide skill requires before/after code examples for every breaking change, a rollback plan, and a deprecation timeline with actual dates.

## Prompt

> /developer-docs-writer:write-migration-guide for our API v2 to v3 upgrade — we renamed several fields, changed authentication from API keys to OAuth 2.0, and removed two deprecated endpoints.

## Output

**Migration Guide: API v2 → v3**

**What's changing:** Authentication method changed from API key headers to OAuth 2.0 Bearer tokens. Three field renames. Two endpoints removed.

**Before/After (auth change):**

```bash
# v2 — API key
curl -H "X-API-Key: sk_live_abc123" https://api.clearpath.app/v2/projects

# v3 — OAuth 2.0
curl -H "Authorization: Bearer eyJhbGciOiJSUzI1NiJ9..." https://api.clearpath.app/v3/projects
```

**Impact assessment:**

| Dimension | Detail |
|---|---|
| Who is affected | All API integrations using v2 auth or renamed fields |
| What code must change | Auth header construction, field references in 3 endpoints |
| Estimated effort | 2-4 hours for small integrations; 1-2 days for large ones — be honest, OAuth setup takes longer than expected |
| Who is NOT affected | UI-only users, Zapier integrations (handled by connector team) |
| Can old and new coexist? | Yes — both supported until 2026-11-01 |

**Breaking changes table:**

| # | What changed | Old | New | Action required |
|---|---|---|---|---|
| 1 | Auth method | `X-API-Key: sk_...` header | `Authorization: Bearer <token>` | Implement OAuth 2.0 client credentials flow |
| 2 | Field rename | `user_id` | `owner_id` | Update all field references |
| 3 | Field rename | `created` | `created_at` | Update field references |
| 4 | Endpoint removed | `GET /v2/reports/legacy` | Removed | Migrate callers to `GET /v3/reports` |
| 5 | Endpoint removed | `POST /v2/bulk-import` | Removed | Use `POST /v3/imports` (streaming) |

**Deprecation timeline:**

| Date | Event |
|---|---|
| 2026-05-01 | v3 available; migration guide published |
| 2026-08-01 | v2 logs deprecation warning headers |
| 2026-11-01 | v2 end-of-life — returns 410 Gone |

**Coexistence:** v2 and v3 run in parallel until 2026-11-01. Migrate one endpoint at a time. Dual-write guidance: point auth at v3 while keeping v2 field names temporarily — the v3 API accepts both `user_id` and `owner_id` during the transition window.

**Rollback plan:**
1. Revert auth header to `X-API-Key` format
2. Change base URL back to `/v2/`
3. Verify with `GET /v2/projects`

**Rollback limitations:** Once callers of `GET /v2/reports/legacy` are migrated to `GET /v3/reports`, rollback requires reimplementing against the removed endpoint. **Point of no return:** migrating off the removed endpoints.

**Verification:**
```bash
# Automated check
curl -H "Authorization: Bearer $TOKEN" https://api.clearpath.app/v3/projects | jq '.data[0].owner_id'
# Expected: a valid owner ID string, no "user_id" key present
```

Manual checklist:
- [ ] `GET /v3/projects` returns 200
- [ ] Response contains `owner_id`, not `user_id`
- [ ] Removed endpoints return 410 on v2

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 (94.4%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Before/after code per breaking change — Step 3 rules state "Every step must have a before/after code example. Prose alone is not sufficient for a migration guide"; this is also reinforced in the global Rules section
- [x] PASS: Rollback plan with point of no return — Step 6 is "Write rollback instructions (mandatory)" and explicitly requires a `#### Point of no return` subsection identifying which migration step makes rollback impossible
- [x] PASS: Deprecation timeline with actual dates — Step 5 rules state "Every deprecation needs a timeline with actual dates (or 'X months after release'), not 'eventually'"; "eventually deprecated" is listed as explicitly unacceptable
- [x] PASS: Impact assessment — Step 2 "Assess impact (mandatory)" requires a table covering who is affected, what code changes, effort estimate, risk level, and who is NOT affected
- [x] PASS: Exhaustive breaking changes table — Step 4 rules state "EVERY breaking change gets its own row. Do not combine multiple changes into 'various API improvements'"
- [x] PASS: Verification steps — Step 7 "Add verification steps (mandatory)" requires automated verification code, a manual checklist, and a common post-migration issues table
- [~] PARTIAL: Coexistence guidance — Step 5 includes both "Running old and new simultaneously" and "Dual-write/dual-read guidance" as required subsections; the skill fully satisfies this but the PARTIAL prefix caps the score at 0.5
- [x] PASS: Honest effort estimates — Rules section states "Effort estimates must be honest. Underestimating migration effort is a form of lying to your developers. Round up, not down."
- [x] PASS: Valid YAML frontmatter — frontmatter contains `name: write-migration-guide`, `description`, and `argument-hint` fields

## Notes

The skill is thorough. The "honest effort estimates" rule is explicit and uses the word "lying" — that's a strong signal it was added deliberately from real experience. The dual-write guidance in Step 5 is present as an explicit required subsection, not just a mention, so it almost warrants full PASS on that criterion — but the PARTIAL prefix in the test holds the ceiling at 0.5 regardless. Step 7 having both automated verification code and a manual checklist is a good design choice for migration guides where automated checks may not cover all paths.
