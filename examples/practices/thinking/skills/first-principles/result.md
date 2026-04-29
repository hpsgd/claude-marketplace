# First principles API versioning assumptions

An architect is questioning whether the team's assumption that REST API versioning via URL path (/v1/, /v2/) is the right approach. The first-principles skill is used to pressure-test the constraints.

## Prompt

> /first-principles We've always versioned our APIs with URL path prefixes (/api/v1/users, /api/v2/users). The team assumes this is required because "that's how APIs work" and "clients will break otherwise". I want to challenge whether this is actually necessary or if it's just habit. We have 3 internal services and 2 external partners as consumers.

```markdown

## Output

### First Principles: REST API versioning via URL path prefixes

#### Component Inventory

| Component | Type | Evidence |
|---|---|---|
| HTTP as transport protocol | Hard constraint | Platform requirement — all consumers use HTTP |
| Request routing must be deterministic | Hard constraint | Distributed system requirement |
| Breaking changes cannot propagate to all consumers simultaneously | Hard constraint | Physical constraint — cannot atomically update all consumers |
| External partners require advance notice of breaking changes | Soft constraint | SLA convention, not an HTTP requirement |
| Version signalled in URL path (/v1/, /v2/) | Assumption | Industry convention adopted without evaluation; HTTP has header-based versioning alternatives |
| "That's how APIs work" | Assumption | No evidence — convention masquerading as fact |
| Clients will break on any schema change | Assumption | Believed true but depends on change type; additive changes are safe under most JSON parsers |
| All consumers need the same version simultaneously | Assumption — unverified | Unverified — 3 internal services may be on different release cadences |
| We need multiple concurrent versions running | Assumption — unverified | Currently true? How long do we maintain v1 after v2 ships? |

---

#### Challenge Ledger

| # | Constraint/Assumption | Challenge | Verdict | Impact if removed |
|---|---|---|---|---|
| 1 | Version in URL path | HTTP 1.1 supports Accept headers for content negotiation. URL versioning pollutes resource identity. | Test | Could use header versioning — cleaner resource identity, harder to test manually |
| 2 | "That's how APIs work" | Not a constraint — a convention. GraphQL doesn't version at all. | Remove | Frees evaluation to focus on actual requirement: stable contracts |
| 3 | Clients will break on schema change | JSON is additive by default. Removing or renaming a field breaks clients. Adding a field does not. | Keep (but refine) | Additive-only changes may eliminate the need for versioning |
| 4 | External partners require advance notice | Real constraint — but about communication and deprecation windows, not URL structure. | Keep (as deprecation policy) | Partners need a contract; enforced through additive-only + Sunset headers |
| 5 | Need concurrent versions running | Verified? If v1 and v2 aren't both running now, this constraint doesn't apply. | Test | If no concurrent versions needed, version URLs are premature infrastructure |

---

#### Reconstruction

**Starting from these truths only:**
1. Breaking changes cannot propagate to all consumers simultaneously
2. External partners need advance notice before any breaking change
3. All JSON consumers handle additive changes safely

**Ignoring current URL versioning form, the optimal solution would:**
- Use additive-only API evolution — add fields, never remove or rename without a deprecation window
- Use deprecation notices in response headers — `Deprecation: true`, `Sunset:` per RFC 8594
- Eliminate URL versioning entirely — `/api/users/{id}` is the resource; the contract evolves additively
- If a breaking change truly becomes necessary — create a new endpoint for the new resource shape rather than wholesale versioning the entire API

**Cross-domain insight:** How does a relational database handle schema evolution? Additive migrations are non-breaking. Removal migrations are breaking. The principle is identical.

---

#### Delta Analysis

| Aspect | Current | Reconstructed | Why different |
|---|---|---|---|
| Version signalling | URL path prefix (`/api/v1/`) | `Deprecation:` / `Sunset:` response headers | Assumption 2 removed: URL versioning not required by HTTP |
| Concurrent versions | Implicit — multiple URL namespaces | Eliminated — single resource path with additive evolution | Assumption 5 removed: concurrent versions may not be needed |
| Breaking change strategy | New URL prefix | Additive-only + deprecation window | Assumption 3 refined: most "breaking" changes are actually additive |
| Partner notification | Convention | Formalised deprecation policy with Sunset: headers | Soft constraint 4 kept but implemented differently |

#### Migration Assessment
- **Quick wins:** Implement `Deprecation:` and `Sunset:` headers on currently-deprecated fields now — no breaking change required
- **Requires validation:** Audit all consumers for fields that depend on removed/renamed behaviour; additive-only may already be de-facto
- **Requires authority:** Committing to additive-only API evolution is a policy change that affects every future API decision; migrating existing consumers off `/v1/` URLs requires partner coordination
```

## Evaluation

**Verdict:** PASS
**Score:** 15.5/17 criteria met (91%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Step 1 produces a complete component inventory classifying every constraint as hard constraint, soft constraint, or assumption with evidence for each — the SKILL.md mandates a classified component inventory table with Type and Evidence columns, covering all three categories with explicit guidance on how to distinguish them
- [x] PASS: "That's how APIs work" and similar inherited conventions are correctly classified as assumptions — the skill's "How to identify assumptions" section explicitly maps "We've always done it this way → assumption", directly covering the prompt's phrasing
- [x] PASS: Step 2 challenge ledger addresses every soft constraint and assumption with a verdict and impact-if-removed analysis — the template requires Verdict and "Impact if removed" columns, and the rules state "Assumptions MUST be challenged"
- [x] PASS: Step 3 reconstruction starts only from verified truths and hard constraints — the skill states "Starting from ONLY the verified truths and hard constraints" and "Ignore current form — focus on function"
- [x] PASS: Step 4 delta analysis compares reconstructed approach against current state with assumption-removal traceability — the delta table template includes "Why different" requiring "which assumption removal enabled this"
- [x] PASS: Output uses the defined first-principles template with all four sections — Output Format section defines all four mandatory sections and the simulated output includes all of them
- [~] PARTIAL: Migration assessment distinguishes quick wins from changes requiring stakeholder authority — the three migration tiers are present (quick wins, requires validation, requires authority), satisfying the distinction; partial applied per criterion prefix
- [x] PASS: Reconstruction does not conclude "change nothing" — the skill's self-correcting rule ("return to Step 2 if reconstruction looks identical") structurally prevents this outcome

### Output expectations

- [x] PASS: Output classifies "that's how APIs work" and "clients will break otherwise" explicitly as ASSUMPTIONS — the simulated output labels both as Assumption with evidence stating "convention masquerading as fact" and "believed true but depends on change type"
- [x] PASS: Hard constraints are limited to function-grounded truths — hard constraints in the output are physical/logical (atomic update impossibility, deterministic routing), not URL-shape conventions
- [x] PASS: Challenge ledger gives every soft constraint and assumption a verdict with impact-if-removed analysis — all five rows in the challenge ledger have Verdict and Impact columns populated
- [x] PASS: Reconstruction starts from versioning's actual function and considers viable forms — the reconstruction section considers additive-only evolution, header-based deprecation, and endpoint-level isolation as alternatives to URL versioning
- [x] PASS: Output addresses the small consumer set (3 internal + 2 external) as a relevant fact — the component inventory flags the internal/external split as a constraint, and the migration assessment addresses partner coordination separately
- [x] PASS: Delta analysis compares reconstructed approach to current /v1/, /v2/ form with traceability to removed assumptions — the delta table maps each row to a specific numbered assumption
- [x] PASS: Reconstruction does NOT conclude "no change" — the output proposes eliminating URL versioning in favour of additive evolution and deprecation headers
- [x] PASS: Migration assessment distinguishes quick wins from stakeholder-authority changes — three-tier migration assessment covers this explicitly
- [~] PARTIAL: Output addresses API evolution mechanism (additive vs breaking) alongside versioning — the reconstruction section covers additive-only evolution, but the skill definition doesn't explicitly prompt for this as a separate topic; the simulated output addresses it as part of reconstruction rather than as a distinct mechanism analysis
- [ ] FAIL: Output references real-world examples (Stripe, GitHub) as evidence — the simulated output does not name Stripe, GitHub, or any concrete external example; the skill's "cross-domain insight" prompt yields a database analogy rather than named API versioning precedents; the skill does not require named examples

## Notes

The skill definition is structurally strong and well-suited to the API versioning scenario. The self-correcting "return to Step 2" rule is the standout quality mechanism. The main gap between the skill's output ceiling and the output expectations is the absence of named real-world versioning examples (Stripe, GitHub) — the skill prompts for cross-domain analogies but doesn't specifically require named industry examples. The API evolution mechanism (additive vs breaking changes) is covered but as part of reconstruction rather than as a named standalone topic, which is consistent with the skill's function-over-form framing.
