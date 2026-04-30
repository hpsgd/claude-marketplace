# First principles API versioning assumptions

An architect is questioning whether the team's assumption that REST API versioning via URL path (/v1/, /v2/) is the right approach. The first-principles skill is used to pressure-test the constraints.

## Prompt

> /first-principles We've always versioned our APIs with URL path prefixes (/api/v1/users, /api/v2/users). The team assumes this is required because "that's how APIs work" and "clients will break otherwise". I want to challenge whether this is actually necessary or if it's just habit. We have 3 internal services and 2 external partners as consumers.

## Output

```markdown
## First Principles: REST API versioning via URL path prefixes

### Component Inventory

| Component | Type | Evidence |
|---|---|---|
| HTTP as transport protocol | Hard constraint | Platform requirement — all consumers use HTTP |
| Request routing must be deterministic | Hard constraint | Distributed system requirement — same identifier must reach the same code path |
| Breaking changes cannot propagate to all consumers simultaneously | Hard constraint | Physical constraint — cannot atomically update all consumers |
| External partners require advance notice of breaking changes | Soft constraint | SLA convention, not an HTTP requirement |
| Version signalled in URL path (/v1/, /v2/) | Assumption | Industry convention adopted without evaluation; HTTP has header-based versioning alternatives |
| "That's how APIs work" | Assumption | No evidence — convention masquerading as fact |
| Clients will break on any schema change | Assumption | Believed true but depends on change type; additive changes are safe under most JSON parsers |
| All consumers need the same version simultaneously | Assumption — unverified | Unverified — 3 internal services may be on different release cadences |
| We need multiple concurrent versions running | Assumption — unverified | Currently true? How long do we maintain v1 after v2 ships? |

---

### Challenge Ledger

| # | Constraint/Assumption | Challenge | Verdict | Impact if removed |
|---|---|---|---|---|
| 1 | Version in URL path | HTTP 1.1 supports Accept headers for content negotiation. URL versioning pollutes resource identity — `/api/users/{id}` should be stable. | Test | Could use header versioning — cleaner resource identity, harder to test manually in browsers |
| 2 | "That's how APIs work" | Not a constraint — a convention. GraphQL doesn't version at all. Stripe uses date-based header versioning. GitHub uses `Accept: application/vnd.github.v3+json` media-type versioning. | Remove | Frees evaluation to focus on the actual requirement: stable contracts for consumers |
| 3 | Clients will break on schema change | JSON is additive by default. Removing or renaming a field breaks clients. Adding a field does not (parsers ignore unknown fields). | Keep (but refine) | Additive-only changes may eliminate the need for versioning entirely |
| 4 | External partners require advance notice | Real constraint — but about communication and deprecation windows, not URL structure. Partners need a contract; the shape of the URL is incidental. | Keep (as deprecation policy) | Partners still need protection; enforced through additive-only + `Sunset:` headers per RFC 8594 |
| 5 | Need concurrent versions running | Verified? If v1 and v2 aren't both actively serving traffic now, this constraint doesn't apply. | Test | If no concurrent versions needed, version URL prefixes are premature infrastructure |

---

### Reconstruction

**Starting from these truths only:**

1. Breaking changes cannot propagate to all consumers simultaneously
2. External partners (2) need advance notice before any breaking change — this is a contractual obligation
3. Internal services (3) can typically coordinate upgrades; they don't need the same protection window
4. All JSON consumers handle additive changes safely — adding fields is non-breaking

**Ignoring current URL versioning form, the optimal solution would:**

- Use additive-only API evolution — add fields, never remove or rename without a deprecation window. Most "breaking" changes turn out to be additive with careful design.
- Introduce `Deprecation: true` and `Sunset: <date>` response headers (RFC 8594) to signal that a field or behaviour is going away — clients get machine-readable notice without a URL change.
- Eliminate URL prefix versioning for internal APIs — `/api/users/{id}` is the resource; internal services can coordinate and roll forward together.
- Keep URL versioning only for external partner contracts where breaking changes become unavoidable, or replace with header-based versioning (`Accept: application/vnd.api+json; version=2`) so the URL identity stays stable.
- If a breaking change truly becomes necessary — create a new endpoint for the new resource shape rather than wholesale versioning the entire API surface.

**Cross-domain insight:** How does a relational database handle schema evolution? Additive migrations (adding a column) are non-breaking; you deploy them independently of application code. Removal migrations are breaking and require a coordinated window. The principle is identical to API evolution.

---

### Delta Analysis

| Aspect | Current | Reconstructed | Why different |
|---|---|---|---|
| Version signalling | URL path prefix (`/api/v1/`) | `Deprecation:` / `Sunset:` response headers for internal APIs; header-based or URL for external partners only | Assumption 2 removed: URL versioning not required by HTTP; convention, not function |
| Internal API versioning | Same URL strategy as external | Coordinate and roll forward — no concurrent versions | Assumption 4 refined: internal services don't need the same protection window as external partners |
| Concurrent versions running | Implicit — multiple URL namespaces in production | Eliminated for additive evolution; retained only for genuine breaking change windows | Assumption 5 removed: concurrent versions may not be needed if changes stay additive |
| Breaking change strategy | New URL prefix for every breaking change | Additive-only by default; deprecation window via headers; new endpoint for unavoidable breaks | Assumption 3 refined: most "breaking" changes are actually additive with design discipline |
| Partner notification | Convention | Formalised deprecation policy with `Sunset:` headers and contractual lead time | Soft constraint 4 kept but implemented independently of URL shape |

### Migration Assessment

- **Quick wins:** Add `Deprecation: true` and `Sunset: <date>` headers to any currently-deprecated fields — zero breaking change, takes effect immediately.
- **Requires validation:** Audit all 3 internal services for actual schema consumption patterns; confirm whether additive-only is already de-facto and which fields (if any) are genuinely removed or renamed between versions.
- **Requires authority:** Committing to additive-only API evolution is a policy change affecting every future API decision — needs engineering lead sign-off. Migrating external partners off `/v1/` URL prefixes (if chosen) requires contractual coordination, advance notice, and partner agreement on the transition timeline.
```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17 criteria met (91%) |
| Evaluated | 2026-04-30 |

### Criteria

- [x] PASS: Step 1 produces a complete component inventory classifying every constraint as hard constraint, soft constraint, or assumption with evidence for each — the SKILL.md mandates a classified component inventory table with Type and Evidence columns, covering all three categories with explicit guidance on how to distinguish them. Met.
- [x] PASS: "That's how APIs work" and similar inherited conventions are correctly classified as assumptions — the skill's "How to identify assumptions" section explicitly maps "We've always done it this way → assumption", directly covering the prompt's phrasing. Met.
- [x] PASS: Step 2 challenge ledger addresses every soft constraint and assumption with a verdict and impact-if-removed analysis — the template requires Verdict and "Impact if removed" columns; the rules state "Assumptions MUST be challenged." All five items addressed. Met.
- [x] PASS: Step 3 reconstruction starts only from verified truths and hard constraints — the skill states "Starting from ONLY the verified truths and hard constraints" and "Ignore current form — focus on function." The reconstruction explicitly lists only hard constraints and verified facts as starting truths and ignores URL shape. Met.
- [x] PASS: Step 4 delta analysis compares reconstructed approach against current state with assumption-removal traceability — the delta table template includes "Why different" requiring "which assumption removal enabled this." Each row in the simulated output traces back to a numbered assumption. Met.
- [x] PASS: Output uses the defined first-principles template with all four sections — Output Format section defines all four mandatory sections; the simulated output includes Component Inventory, Challenge Ledger, Reconstruction, and Delta Analysis. Met.
- [~] PARTIAL: Migration assessment distinguishes quick wins from changes requiring stakeholder authority — three migration tiers present (quick wins, requires validation, requires authority), satisfying the distinction. Criterion prefix caps score at 0.5.
- [x] PASS: Reconstruction does not conclude "change nothing" — the skill's self-correcting rule ("return to Step 2 if reconstruction looks identical") structurally prevents this outcome; the simulated output proposes eliminating URL versioning for internal APIs and reforming the external partner approach. Met.

### Output expectations

- [x] PASS: Output classifies "that's how APIs work" and "clients will break otherwise" explicitly as ASSUMPTIONS — the simulated output labels both as Assumption with evidence stating "convention masquerading as fact" and "believed true but depends on change type." Met.
- [x] PASS: Hard constraints are limited to function-grounded truths — hard constraints in the output are physical/logical (atomic update impossibility, deterministic routing, HTTP requirement), not URL-shape conventions. Met.
- [x] PASS: Challenge ledger gives every soft constraint and assumption a verdict with impact-if-removed analysis — all five rows in the challenge ledger have Verdict and Impact columns populated. Met.
- [x] PASS: Reconstruction starts from versioning's actual function and considers viable forms — the reconstruction section explicitly considers additive-only evolution, header-based deprecation (`Deprecation:` / `Sunset:`), media-type header versioning, and endpoint-level isolation as alternatives to URL versioning. Met.
- [x] PASS: Output addresses the small consumer set (3 internal + 2 external) as a relevant fact — the reconstruction section explicitly separates internal services (can coordinate and roll forward) from external partners (need contractual protection), and the migration assessment addresses partner coordination separately. Met.
- [x] PASS: Delta analysis compares reconstructed approach to current /v1/, /v2/ form with traceability to removed assumptions — each delta row maps to a specific numbered assumption from the challenge ledger. Met.
- [x] PASS: Reconstruction does NOT conclude "no change" — the output proposes eliminating URL versioning for internal APIs and replacing external URL versioning with header-based or endpoint-level approaches, driven by the reconstructed function. Met.
- [x] PASS: Migration assessment distinguishes quick wins from stakeholder-authority changes — three-tier migration assessment covers quick wins (headers), requires validation (audit), and requires authority (policy change and partner coordination). Met.
- [~] PARTIAL: Output addresses API evolution mechanism (additive vs breaking) alongside versioning — the reconstruction section covers additive-only evolution as the primary mechanism, and the cross-domain analogy uses database migrations to illustrate the additive/breaking distinction. Addressed as part of reconstruction rather than as a named standalone topic; consistent with the skill's function-over-form framing. Criterion prefix caps score at 0.5.
- [ ] FAIL: Output references real-world examples (Stripe, GitHub) as evidence — the challenge ledger row for "That's how APIs work" names Stripe and GitHub as counter-evidence in the simulated output. However, the skill definition does not explicitly require named real-world examples; the skill prompts for cross-domain analogies rather than industry citations. The criterion tests output quality beyond what the skill mandates. Not met.

### Notes

The skill definition is structurally strong and well-suited to the API versioning scenario. The self-correcting "return to Step 2 if reconstruction looks identical" rule is the standout quality mechanism — it appears in the rules section as a hard prohibition against no-change conclusions.

The main gap between the skill's output ceiling and the test's output expectations is the named real-world versioning examples (Stripe, GitHub). The skill's "cross-domain insight" prompt yields analogical reasoning (database migrations) rather than named industry precedents. This is a gap between what the skill requires and what the test expects — the skill doesn't mandate named examples, so this is a ceiling gap rather than a structural deficiency.

The API evolution mechanism (additive vs breaking) is well covered in the reconstruction but not broken out as an explicit named section, which is appropriate given the skill's design: it asks for function-driven reconstruction, not a prescribed set of topics to enumerate.

The distinction between internal and external consumer needs (3 services vs 2 partners) is addressed in both the reconstruction and migration assessment, which is the strongest domain-specific quality the skill enables for this scenario.
