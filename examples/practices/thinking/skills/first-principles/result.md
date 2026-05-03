# First Principles

Scenario: An architect is questioning whether the team's assumption that REST API versioning via URL path (/v1/, /v2/) is the right approach. The first-principles skill is used to pressure-test the constraints.

## Prompt

> /first-principles We've always versioned our APIs with URL path prefixes (/api/v1/users, /api/v2/users). The team assumes this is required because "that's how APIs work" and "clients will break otherwise". I want to challenge whether this is actually necessary or if it's just habit. We have 3 internal services and 2 external partners as consumers.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## First Principles: API versioning via URL path prefixes

---

### Component Inventory

| Component | Type | Evidence |
|---|---|---|
| Clients must not break when the server changes | **Hard constraint** | Breaking changes = real business/operational cost |
| Change coordination must happen somewhere | **Hard constraint** | Distributed systems require a contract mechanism |
| URL path prefixes specifically (`/v1/`) | **Assumption** | Convention, not a protocol requirement |
| "All clients update together" is impossible | **Soft constraint** | Policy choice — you could require simultaneous deploys |
| Versioning must be visible to humans/logs | **Assumption** | Useful but never verified as required |
| One URL = one resource (REST principle) | **Assumption** | A design philosophy, not HTTP law |
| External partners require URL-stable contracts | **Soft constraint** | Common practice, not technically mandated |
| Internal services need the same mechanism as external | **Assumption** | Completely unverified — different trust/control levels |

**Key assumption pattern:** Every constraint is on *change coordination*, not on the *mechanism* that implements it. The `/v1/` prefix is a mechanism, not the function.

---

### Challenge Ledger

| # | Constraint/Assumption | Challenge | Verdict | Impact if removed |
|---|---|---|---|---|
| 1 | URL path prefixes are required | HTTP has no such requirement. `Accept:` headers, query params, content negotiation all work. Who decided URLs? Nobody — it spread by imitation of early public APIs (Stripe, Twitter). | **Remove** | URL space stays clean; resources don't multiply |
| 2 | Internal services need URL versioning | You own both sides. You can deploy them together, share contracts via code, or use feature flags. The versioning problem doesn't exist the same way. | **Remove** | 3 of your 5 consumers need zero version ceremony |
| 3 | External partners require URL versioning | Partners need *stability guarantees*, not specifically URL stability. A contract expressed via headers or content negotiation is equally stable — arguably more precise. | **Test** | Still need contract; mechanism is negotiable |
| 4 | "Clients will break otherwise" | This is true of *any* breaking change regardless of mechanism. URL versioning doesn't prevent breaks — it just namespaces them. Evidence that clients break without `/v2/`? None stated. | **Remove as stated** | The real constraint is: communicate breaking changes. Mechanism is separate. |
| 5 | Versioning must be human-readable in the URL | Useful for debugging and logs. But not a correctness requirement — header-based versioning is equally inspectable with tooling. | **Test** | Operational convenience, not a hard need |
| 6 | One version strategy for all consumers | Internal services and external partners have radically different coupling tolerance. Treating them identically adds overhead to the low-risk case. | **Remove** | Can use different strategies per consumer class |

---

### Reconstruction

**Starting from these truths only:**
1. Breaking changes must be communicated — consumers need to know when a contract changes
2. Different consumers may be ready to migrate at different times
3. Internal services are under your deployment control; external partners are not
4. HTTP is a rich protocol with multiple contract negotiation mechanisms (URL, headers, content type, query params)
5. You have exactly 5 consumers: 3 internal, 2 external

**Ignoring current implementation, the optimal solution would:**

- **For internal services (3 consumers):** Use no versioning mechanism at all — instead, use contract tests (Pact or equivalent) that fail CI if either side breaks the contract. Deploy in coordination. Version is implicit in the commit graph, not the URL. This is how microservices teams at scale actually operate.

- **For external partners (2 consumers):** Maintain an explicit, stable contract. The mechanism that best fits: `Accept: application/vnd.yourapi.v2+json` (content negotiation). Why: the resource is the same resource — `/users` is users. The representation varies. URL versioning conflates "this resource" with "this representation of this resource."

- **For both:** Deprecation is a process, not a URL. Run old and new behaviour in parallel, communicate via `Sunset` HTTP headers (RFC 8594), give consumers a migration window, then remove.

**Cross-domain insight:** Physical standards bodies (USB, Bluetooth) version the *protocol spec*, not the *socket*. The USB-C port doesn't become USB-D — the capability negotiation happens in the handshake. HTTP was designed with exactly this in mind (content negotiation, `Accept` headers) and it's never been fully used by the industry.

---

### Delta Analysis

| Aspect | Current | Reconstructed | Why different |
|---|---|---|---|
| Internal service contracts | URL versioned same as external | Contract tests + coordinated deploys, no URL version | Assumption removed: internal ≠ external |
| External partner contracts | `/v1/` path prefix | Content negotiation (`Accept` header) or explicit partner SLAs | Assumption removed: URL is the only stable anchor |
| Breaking change detection | Implicit — consumers discover at runtime | Explicit — contract tests catch it in CI before deploy | Function (coordination) preserved, mechanism improved |
| URL space | Doubles with each version (`/v1/`, `/v2/`) | Stays clean — `/users` is always users | Assumption removed: version must live in URL |
| New consumer onboarding | Must choose a version URL | Defaults to latest; explicit version opt-in via header | Simpler default, explicit opt-out |
| Operational visibility | Version visible in URL/logs | Version visible in request headers — equally inspectable | Assumption removed: URL is the only visible place |

### Migration Assessment

**Quick wins (do now, no authority needed):**
- Stop URL-versioning the 3 internal services. Replace with contract tests. Internal deploys are coordinated anyway — URL versioning is pure overhead here.
- Add `Sunset` header to existing `/v1/` endpoints so partners have machine-readable deprecation signals.

**Requires validation (run experiments first):**
- Check whether your 2 external partners' clients can send `Accept` headers — some legacy clients (especially mobile SDKs or generated clients) cannot. If they can't, header versioning isn't viable for them specifically.
- Verify your API gateway/load balancer supports header-based routing if you go that path.

**Requires authority (stakeholder decision):**
- Changing the external partner contract mechanism requires their agreement — even if technically equivalent. This is a relationship decision, not just a technical one.
- Whether to maintain `/v1/` paths for existing partners while moving new APIs to header-based versioning (a hybrid that's coherent but requires a policy decision).

---

### Recommendations

**Immediate:** Drop URL versioning for internal services entirely. Replace with Pact/contract tests. This affects 3 of 5 consumers and you control both sides — there's no coordination problem to solve with a URL.

**Validate next:** Survey whether your 2 external partners' HTTP clients support `Accept` headers. One email/Slack message. This determines whether the full reconstruction is viable or whether you keep URL prefixes for the external surface only.

**Frame the real question:** Your team's assumption is "versioning = URL prefix." The first principle is "change coordination = some shared contract mechanism." The URL is one valid mechanism — not the only one, and not always the best one. The internal/external distinction is the key leverage point you're currently ignoring.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/17.0 (88%) |
| Evaluated | 2026-05-01 |
| Target duration | 50668 ms |
| Target cost | $0.0679 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 produces a complete component inventory classifying every constraint as hard constraint, soft constraint, or assumption with evidence for each | PASS | The Component Inventory table lists 8 items with Type column showing Hard constraint (2), Soft constraint (2), and Assumption (4), each with an Evidence column explaining the classification — e.g. 'Convention, not a protocol requirement' for URL path prefixes, 'Distributed systems require a contract mechanism' for change coordination. |
| c2 | "That's how APIs work" and similar inherited conventions are correctly classified as assumptions, not hard constraints | PASS | URL path prefixes classified as Assumption with evidence 'Convention, not a protocol requirement'. Challenge Ledger #1 reinforces: 'Who decided URLs? Nobody — it spread by imitation of early public APIs (Stripe, Twitter).' Challenge Ledger #4 on 'clients will break otherwise' verdicts 'Remove as stated'. |
| c3 | Step 2 challenge ledger addresses every soft constraint and assumption from Step 1 with a verdict (keep/remove/test) and impact-if-removed analysis | PARTIAL | The challenge ledger has 6 entries covering most assumptions, but two inventory items are absent: 'All clients update together is impossible' (Soft constraint) and 'One URL = one resource (REST principle)' (Assumption) have no dedicated challenge ledger row with verdict and impact-if-removed analysis. |
| c4 | Step 3 reconstruction starts only from verified truths and hard constraints — ignores current URL path versioning form and asks what function requires | PASS | 'Starting from these truths only' lists 5 function-grounded truths, then 'Ignoring current implementation, the optimal solution would:' explicitly brackets out the existing form. Recommends contract tests and content negotiation — neither assumes URL-path as required. |
| c5 | Step 4 delta analysis compares reconstructed approach against current state with a table showing which assumption removal enabled each difference | PASS | Delta Analysis table's 'Why different' column explicitly cites assumption removals: 'Assumption removed: internal ≠ external', 'Assumption removed: URL is the only stable anchor', 'Assumption removed: version must live in URL', 'Assumption removed: URL is the only visible place'. |
| c6 | Output uses the defined first-principles template with all four sections | PASS | All four sections present: Component Inventory, Challenge Ledger, Reconstruction ('Starting from these truths only'), and Delta Analysis table. Migration Assessment and Recommendations appear as additional sections beyond the core four. |
| c7 | Migration assessment distinguishes quick wins from changes requiring stakeholder authority | PARTIAL | Migration Assessment has three labelled sub-sections: 'Quick wins (do now, no authority needed)', 'Requires validation (run experiments first)', and 'Requires authority (stakeholder decision)' — the last states 'Changing the external partner contract mechanism requires their agreement — even if technically equivalent. This is a relationship decision'. |
| c8 | Reconstruction does not conclude "change nothing" — if it does, the skill's own rules require returning to Step 2 to challenge more assumptions | PASS | Reconstruction recommends dropping URL versioning for internal services entirely (replace with contract tests) and moving to content negotiation headers for external partners — substantial change from current state. |
| c9 | Output classifies "that's how APIs work" and "clients will break otherwise" explicitly as ASSUMPTIONS, not hard constraints — naming them as inherited convention, not a function-imposed requirement | PASS | URL path prefixes explicitly labelled Assumption: 'Convention, not a protocol requirement'. Challenge Ledger #4 labels 'clients will break otherwise' and verdicts 'Remove as stated', noting 'URL versioning doesn't prevent breaks — it just namespaces them. Evidence that clients break without /v2/? None stated.' |
| c10 | Output's hard constraints are limited to truths grounded in function — e.g. "consumers must be able to upgrade independently", "old clients must keep working during transition windows", "the same identifier must reach the same code path" — not URL-shape conventions | PASS | Only two hard constraints: 'Clients must not break when the server changes' (evidence: 'Breaking changes = real business/operational cost') and 'Change coordination must happen somewhere' (evidence: 'Distributed systems require a contract mechanism'). Neither references URL shape. |
| c11 | Output's challenge ledger gives every soft constraint and assumption a verdict (KEEP / REMOVE / TEST) with the impact-if-removed analysis — e.g. "if we remove URL-path versioning, what breaks for the 2 external partners?" | PARTIAL | The 6 challenge ledger entries each have a verdict and impact analysis (e.g. 'Remove → URL space stays clean; resources don't multiply'; 'Test → Still need contract; mechanism is negotiable'). However, 'One URL = one resource (REST principle)' from the inventory is never given a ledger row with verdict and impact. |
| c12 | Output's reconstruction starts from versioning's actual function — versioning exists to allow simultaneous old + new behaviour for different consumers — and considers all viable forms (URL path, header, query param, content-type, no version with additive-only changes) | PASS | Reconstruction truth #4 lists 'multiple contract negotiation mechanisms (URL, headers, content type, query params)'. Recommends Accept header/content negotiation for external. The 'cross-domain insight' section discusses capability negotiation in handshake. For internal: no versioning (contract tests instead). |
| c13 | Output addresses the small consumer set (3 internal + 2 external) as a relevant fact — internal services can typically migrate together, external partners need a longer window, which influences the chosen versioning mechanism | PASS | Reconstruction has distinct sub-sections 'For internal services (3 consumers)' and 'For external partners (2 consumers)'. States 'Internal services are under your deployment control; external partners are not' as a foundational truth. Challenge Ledger #2: '3 of your 5 consumers need zero version ceremony'. |
| c14 | Output's delta analysis compares the reconstructed approach to the current `/v1/`, `/v2/` form with a table showing "this changed because we removed assumption X" — not just a "before/after" comparison without traceability | PASS | Delta Analysis has Aspect/Current/Reconstructed/Why-different columns. 'Why different' column traces each change to a removed assumption: e.g. 'Internal service contracts' row: Current='/v1/' same as external', Reconstructed='contract tests + coordinated deploys', Why='Assumption removed: internal ≠ external'. |
| c15 | Output's reconstruction does NOT conclude "no change" — it either identifies a meaningful shift (e.g. "internal APIs can use header-based versioning to keep the URL stable; external partners keep URL versioning") or returns to Step 2 to challenge more assumptions | PASS | Reconstruction recommends eliminating URL versioning for 3 internal services (replacing with Pact contract tests) and switching to Accept header content negotiation for external partners — materially different from current state. |
| c16 | Output's migration assessment distinguishes quick wins (e.g. add a deprecation header to v1 starting now) from changes requiring stakeholder authority (e.g. asking external partners to switch to header-based versioning needs lead time and contractual coordination) | PASS | 'Quick wins (do now, no authority needed)' includes 'Add Sunset header to existing /v1/ endpoints'. 'Requires authority (stakeholder decision)' states 'Changing the external partner contract mechanism requires their agreement — even if technically equivalent. This is a relationship decision, not just a technical one.' |
| c17 | Output addresses the API evolution mechanism alongside versioning — additive changes (new optional fields) don't need a new version, breaking changes do; this is more important than the version-shape choice | PARTIAL | Output frames breaking changes as the core problem ('Breaking changes must be communicated') and uses Sunset headers for deprecation signalling. However, it never explicitly states that additive changes (new optional fields, new endpoints) do not require a version increment — the additive-safe/breaking-unsafe distinction is absent. |
| c18 | Output references real-world examples of non-URL-path versioning (Stripe's date-based header versioning, GitHub's media-type versioning) as evidence the assumption is challengeable | FAIL | Output mentions Stripe only as a propagator of URL-path versioning convention ('it spread by imitation of early public APIs (Stripe, Twitter)'), not as an example of non-URL versioning. GitHub media-type versioning is not mentioned. The USB/Bluetooth cross-domain example is used instead, which is not a REST API example. |

### Notes

The output is an exceptionally strong first-principles analysis — well-structured, traces every recommendation back to assumption removal, and correctly separates internal-service concerns from external-partner concerns. The two main gaps are: (1) the 'One URL = one resource' REST assumption from the inventory is never given a challenge-ledger entry, leaving one assumption formally unchallenged; (2) the additive-change / breaking-change distinction is missing — the output treats all change as breaking-change territory without noting that backward-compatible additions require no versioning at all, which is arguably the more important design insight. The real-world non-URL versioning examples (Stripe header versioning, GitHub media types) are absent; Stripe appears only in the wrong direction. These gaps are minor relative to the overall quality.
