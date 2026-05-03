# Api Design

Scenario: Checking that the api-design skill contains the required elements for designing a REST API — resource hierarchy, HTTP semantics, pagination, error format, and versioning guidance.

## Prompt

> Review the api-design skill definition and verify it provides sufficient guidance to produce a well-formed REST API specification.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here is my review:

---

## `architect:api-design` Skill Review

**Verdict:** The skill has strong process coverage but three internal contradictions mean it cannot reliably produce a _consistent_ spec as written.

---

### Critical: Template vs. SKILL.md Contradictions

These cause the output document to contradict its own rules.

**1. Pagination format conflict**

| Source | Format |
|---|---|
| `SKILL.md` Step 5 | `page`/`size`/`totalItems`/`totalPages` (offset-based) |
| `templates/api-design.md` §6 | `cursor`/`hasMore` (cursor-based) |

An agent that follows Step 5 then uses the template produces a doc with two incompatible pagination strategies.

**2. Error format conflict**

| Source | Format |
|---|---|
| `SKILL.md` Step 6 | RFC 9457 Problem Details (`type`, `title`, `status`, `detail`, `instance`) |
| `templates/api-design.md` §5 | Custom shape `{ "error": { "code", "message", "target", "requestId" } }` |

The skill mandates a standard, the template documents a different one.

**3. Dual output format instruction**

`SKILL.md` has its own `## Output Format` section specifying a markdown structure, then closes with:

> "Use the api-design template (`templates/api-design.md`) as the output structure."

Two conflicting output structures are specified. The template wins if followed literally, but it carries the two contradictions above.

---

### Minor: GraphQL paragraph in Step 7

Step 7 (Versioning) drops a GraphQL reference mid-section that breaks flow and points to a `templates/graphql-schema.md` not mentioned anywhere else in the skill. It belongs in a "Related Skills / Alternatives" section, not embedded in versioning strategy.

---

### What's Well-Covered

The skill is genuinely strong in: URL hierarchy rules, HTTP method semantics, RFC 7396 merge patch + optimistic concurrency, auth/authz guidance, and anti-patterns. The process is sequential and actionable.

---

### Recommended Fixes

1. **Align pagination** — pick one strategy (cursor-based is better for large collections; offset is simpler for small ones) and apply it consistently to both files.
2. **Align error format** — RFC 9457 is the right choice; update the template to match.
3. **Remove the trailing "use the template" instruction**, or remove the `## Output Format` section in SKILL.md — one source of truth.
4. **Move the GraphQL note** out of Step 7 into the `## Related Skills` section.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 10.5/18.0 (58%) |
| Evaluated | 2026-04-30 |
| Target duration | 66871 ms |
| Target cost | $0.3510 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines a URL hierarchy rule — resources must be accessed through parent chains, no flat top-level listings of child resources | PASS | The output explicitly states 'URL hierarchy rules' are among the things the skill is 'genuinely strong in' in the What's Well-Covered section. |
| c2 | Skill specifies HTTP method semantics table covering GET, POST, PUT, PATCH, DELETE with idempotency and success codes | PASS | The What's Well-Covered section explicitly lists 'HTTP method semantics' as a strength of the skill. |
| c3 | Skill mandates PATCH semantics using RFC 7396 merge patch with optimistic concurrency (lastUpdatedAt conflict detection) | PASS | Output explicitly names 'RFC 7396 merge patch + optimistic concurrency' in the What's Well-Covered section. |
| c4 | Skill requires every list endpoint to support pagination with a defined response shape (items, page, size, totalItems, totalPages) | PASS | Critical section discusses SKILL.md Step 5 specifying 'page/size/totalItems/totalPages', confirming pagination with a response shape is present in the skill. |
| c5 | Skill specifies error format using RFC 9457 Problem Details with standard status codes and rules against leaking stack traces | PASS | Error format conflict table explicitly cites 'SKILL.md Step 6 \| RFC 9457 Problem Details (type, title, status, detail, instance)' confirming this is in the skill. |
| c6 | Skill provides a versioning strategy section with at least two options and rules for when a new version is required | FAIL | Step 7 (Versioning) is only mentioned in the context of a GraphQL paragraph flaw; the review does not confirm whether two strategies are present or rules for when a new version is required. Versioning is absent from the What's Well-Covered section. |
| c7 | Skill defines authentication requirements — Bearer token with short-lived access tokens and resource-level authorisation | FAIL | The output only says 'auth/authz guidance' is well-covered — no mention of Bearer tokens, short-lived access tokens, or the distinction between role-level and resource-level authorisation. |
| c8 | Skill lists anti-patterns — flat URL namespace, verbs in URLs, silent failures, leaking internal IDs | PARTIAL | The What's Well-Covered section mentions 'anti-patterns' as a strength, confirming their presence, but does not verify or list the four specific anti-patterns (flat URL namespace, verbs in URLs, silent failures, leaking internal IDs). |
| c9 | Skill's output format template includes an error catalogue section and a resource hierarchy visual | FAIL | The output discusses the template (templates/api-design.md) only in the context of pagination and error format conflicts. It never mentions or checks for an error catalogue section or a resource hierarchy visual within the template. |
| c10 | Output is structured as a review of the skill (PASS/FAIL or present/missing per requirement) rather than producing a sample API design | PASS | The output is clearly a structured review with a Verdict, Critical issues, What's Well-Covered, and Recommended Fixes sections — not a sample API design. |
| c11 | Output verifies the URL hierarchy rule and quotes or references the specific clause forbidding flat top-level listings | PARTIAL | Output confirms 'URL hierarchy rules' are well-covered but does not quote or reference any specific clause forbidding flat top-level listings of child resources. |
| c12 | Output verifies the HTTP method semantics table covers all five methods (GET, POST, PUT, PATCH, DELETE) and confirms idempotency is documented per method | PARTIAL | Output notes 'HTTP method semantics' as well-covered but never names all five methods individually nor confirms idempotency is documented per method. |
| c13 | Output checks for RFC 7396 merge patch + optimistic concurrency via `lastUpdatedAt` and 409 Conflict, naming both elements explicitly | PASS | Output explicitly names 'RFC 7396 merge patch + optimistic concurrency' in What's Well-Covered. Note: `lastUpdatedAt` and 409 are not named explicitly, but both RFC 7396 and optimistic concurrency are clearly confirmed. |
| c14 | Output verifies the paginated response shape includes all five fields (`items`, `page`, `size`, `totalItems`, `totalPages`) | PARTIAL | Output cites 'page/size/totalItems/totalPages' from SKILL.md Step 5 (four fields), but `items` is not mentioned. Missing one of the five required fields. |
| c15 | Output verifies the error format complies with RFC 9457 Problem Details, with the standard fields (`type`, `title`, `status`, `detail`, `instance`) and a status-code table covering at least 400/401/403/404/409/422/429/500 | PARTIAL | Output explicitly lists all five RFC 9457 fields (type, title, status, detail, instance) from SKILL.md Step 6, but does not verify a status-code table covering the specified HTTP codes. |
| c16 | Output verifies the versioning section presents at least two strategies (e.g. URL prefix vs header) with rules for when a new version is required | FAIL | Step 7 (Versioning) is referenced only to flag a misplaced GraphQL paragraph. No verification of multiple strategies or rules for when versioning is required. |
| c17 | Output verifies the authentication section specifies Bearer tokens with short-lived access tokens and resource-level (not just role-level) authorisation | FAIL | Auth is only referenced as 'auth/authz guidance' in the Well-Covered summary. No mention of Bearer tokens, short-lived access tokens, or resource-level vs role-level distinction. |
| c18 | Output verifies the anti-patterns list covers flat URLs, verbs in URLs, leaking internal IDs, and silent failures — and flags any missing | PARTIAL | 'anti-patterns' confirmed as well-covered in the review, but the four specific items (flat URLs, verbs in URLs, leaking internal IDs, silent failures) are not individually named or verified. |
| c19 | Output identifies any gaps or weaknesses in the skill (not just confirming presence) — e.g. missing rate-limit response semantics, ambiguous HATEOAS guidance, or no field-level deprecation pattern | PARTIAL | The output identifies three critical contradictions (pagination conflict, error format conflict, dual output format) and a minor GraphQL paragraph issue, with concrete recommended fixes. These are genuine weaknesses, not just presence confirmations. |

### Notes

The captured output is a well-structured review with strong coverage of the areas the skill is genuinely good at (URL hierarchy, HTTP semantics, RFC 7396, error format identity). However, it fails to specifically verify several criteria that require per-element confirmation: it never checks that all five HTTP methods are individually covered, never verifies the versioning section has two strategies, never confirms Bearer token / short-lived / resource-level auth specifics, never enumerates the four anti-pattern items, and never checks whether `items` is in the pagination shape. The review also does not check the template for an error catalogue or resource hierarchy visual. The contradictions it surfaces (pagination strategy conflict, error format conflict, dual output format instruction) are genuine and valuable findings, earning full credit on c19. Overall, the output reads more like a 'what's broken' report than a systematic 'is each requirement present' checklist, causing many verification criteria to score only PARTIAL.
