# First Principles

Scenario: An architect is questioning whether the team's assumption that REST API versioning via URL path (/v1/, /v2/) is the right approach. The first-principles skill is used to pressure-test the constraints.

## Prompt

> /first-principles We've always versioned our APIs with URL path prefixes (/api/v1/users, /api/v2/users). The team assumes this is required because "that's how APIs work" and "clients will break otherwise". I want to challenge whether this is actually necessary or if it's just habit. We have 3 internal services and 2 external partners as consumers.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll deconstruct this API versioning assumption from first principles.

## First Principles: API Versioning Strategy

### Component Inventory

| Component | Type | Evidence |
|---|---|---|
| Requirement: Don't break existing clients | Hard constraint | 5 consumers exist; downtime = operational disruption |
| Requirement: APIs will evolve | Hard constraint | Inevitable that endpoints change, features add/remove |
| HTTP as protocol | Hard constraint | This is what we're using |
| 3 internal services as consumers | Fact | Known and manageable |
| 2 external partners as consumers | Fact | Known but less controllable |
| URL path prefixes (/api/v1, /api/v2) | Soft constraint | Chosen implementation, not a law |
| "URL versioning is required" | **Assumption** | Never verified; believed because "that's how APIs work" |
| "Clients will break without versioning" | **Assumption** | Conflates "clients break" with "URL paths must differ" |
| "External partners expect this" | **Assumption** | Never asked them; inferred |
| Multiple versions must coexist | **Assumption** | May be false — depends on partner contracts |

---

### Challenge Ledger

| # | Assumption | Challenge | Verdict | Impact if removed |
|---|---|---|---|---|
| 1 | "URL versioning is required" | Who decided this? What was the actual business problem being solved? | **Remove** | Could use semantic versioning, headers, or deprecation policies instead |
| 2 | "External partners expect /v1, /v2 URLs" | Have you asked them? What's their actual constraint — the URL format, or "breaking changes announced in advance"? | **Test** | May be satisfied by explicit deprecation timeline; no URL change needed |
| 3 | "Multiple versions must run simultaneously" | Is this actually happening? How many versions are you actively maintaining right now? | **Test** | If you're really only on v2, you're carrying v1 code for no reason |
| 4 | "Clients can't upgrade" | Internal services: why not? You control them. External partners: what's their actual SLA? | **Test** | Internal clients can upgrade on your schedule; external ones need a contract, not a URL |
| 5 | "Backward compatibility requires URL versioning" | Does it? Or does it require "don't break existing behavior on a timeline"? | **Remove** | Backward compatibility ≠ URL structure. You can evolve the same endpoint with a deprecation policy |
| 6 | "It's easier to maintain multiple codepaths" | Is it? URL versioning = duplicate logic for each version. Cost analysis: lines of code × maintenance overhead. | **Test** | Single surface with feature flags or deprecation periods might be simpler |

---

### Reconstruction

**Starting from these truths only:**
1. We have 5 consumers: 3 internal (controllable), 2 external (contractual)
2. APIs must evolve without unexpectedly breaking callers
3. The actual requirement is: "predictable, managed change" — not "URL paths must have version numbers"
4. Semantic versioning exists as a standard way to signal change intensity

**Ignoring current implementation, the optimal solution would:**

- **Single API surface:** All consumers call `/api/users` (no version in path)
- **Breaking change policy:** 
  - Announce 6 months ahead of breaking change
  - Provide migration guide + code examples
  - Support old behavior during deprecation window (with explicit `Deprecation` header and `Sunset` header per RFC 8594)
  - Hard remove after deadline
- **For internal services:** Upgrade them together with the API. Version them in `package.json`/lock files, deploy as a unit.
- **For external partners:** Establish SLAs. "We'll give 6 months notice before breaking changes. You must upgrade by [date]."
- **API contract signalling:**
  - Use `Accept` headers or `application/vnd.company.api+json; version=2` if you need multiple representations
  - Document API version in response headers
  - Use [semantic versioning](https://semver.org/) for the API itself
- **Deprecation tracking:** 
  - Existing endpoints get `Deprecation: true, Sunset: <date>` headers when they're scheduled to end
  - Clients have clear timeline and warning

**Why this works:** It decouples URL structure from versioning strategy. The URL is a stable interface; the API's behavior evolves on a published timeline.

**Cross-domain insight:** Most mature APIs don't version in URLs. GitHub, Stripe, Twitter, AWS use header-based versioning or single surfaces with deprecation policies. They version like semantic versioning (major.minor.patch), not like `/api/v47`. The URL versioning pattern is mostly legacy (RPC-style APIs from the 2000s) or teams following cargo-cult practices without understanding why.

---

### Delta Analysis

| Aspect | Current (URL Versioning) | Reconstructed (Deprecation Policy) | Why Different |
|---|---|---|---|
| URL structure | `/api/v1/users`, `/api/v2/users` | `/api/users` | Removes assumption that version number belongs in path |
| Client upgrade path | Optional — clients can stay on v1 forever | Scheduled — clients must upgrade by deprecation date | Treats external partners as managed contracts, not optional clients |
| Internal service versioning | Each service has /api/v1 and /api/v2 | Single /api surface; version control via Git/package.json | Aligns with reality (you control internal services) |
| Code maintenance | Multiple code branches (v1 handler, v2 handler) | Single handler with deprecation wrapper (if needed) | Fewer codepaths = less complexity |
| Breaking change communication | Implicit (URL changed) | Explicit (Deprecation header + timeline) | Clearer contract with partners; no surprises |
| Contract clarity | Unclear — URL versioning doesn't define what "breaking" means | Explicit SLA (6 months notice, go/no-go date) | External partners know exactly what to expect |

---

### Migration Assessment

**Quick wins** (do immediately, low risk):
1. **Ask external partners:** Email them: "Does your system require URL versioning (/v1 vs /v2)? Or just timely notification of breaking changes?" The answer will surprise you.
2. **Audit current state:** How many API versions are actually running? If you're only on v2, kill v1 and measure the code deletion.
3. **Draft a deprecation policy:** "Breaking changes get 6 months notice, documented with migration examples, Sunset header when active."

**Requires validation** (experiment before committing):
1. **Cost comparison:** Count lines of code and maintenance hours for "multiple versions" vs. "deprecation overhead." You might find single surface is actually cheaper.
2. **Partner migration readiness:** Can external partners realistically update an API URL in their client? Or is it blocked by their deployment cycle? (If truly blocked, you may need both approaches temporarily.)
3. **Test deprecation headers:** Do your consumers (internal and external) actually respect `Deprecation` and `Sunset` headers? If not, you need alerting/monitoring.

**Requires authority** (stakeholder decision):
1. **Commit to explicit SLAs:** Moving away from implicit URL versioning means you need explicit break timelines. This might require conversations with product/customer success about "when can we actually break customers?"
2. **Partner notification process:** Set up mechanism to notify external partners 6 months ahead. Not email-when-we-feel-like-it, but systematic.
3. **Internal deployment coordination:** For internal services, align deployment of API and clients. May need tooling/process change.

---

### Recommendations

**The core insight:** You're following a convention that solves "how do we support multiple API versions simultaneously" without questioning whether that's your actual problem. Your actual problem is "how do we evolve APIs without surprising 5 specific consumers."

**Those are different problems with different solutions.**

- **If external partners truly can't upgrade on a timeline** → Keep URL versioning (temporary coexistence is real).
- **If external partners can upgrade on a 6-month timeline** → Deprecation policy is simpler and matches how modern APIs work.
- **For internal services** → No URL versioning needed at all. You control them.

**Start with the quick wins:** Ask the external partners directly. Their answer will likely surprise the team and inform everything else.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 40885 ms |
| Target cost | $0.0537 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 produces a complete component inventory classifying every constraint as hard constraint, soft constraint, or assumption with evidence for each | PASS | The 'Component Inventory' table lists items under types: Hard constraint (Don't break existing clients, APIs will evolve, HTTP as protocol), Fact (3 internal services, 2 external partners), Soft constraint (URL path prefixes /api/v1, /api/v2), and Assumption (URL versioning is required, Clients will break without versioning, External partners expect this, Multiple versions must coexist). Each row includes an Evidence column. |
| c2 | "That's how APIs work" and similar inherited conventions are correctly classified as assumptions, not hard constraints | PASS | In the Component Inventory, 'URL versioning is required' is typed as **Assumption** with evidence: 'Never verified; believed because "that's how APIs work"'. The inherited convention is explicitly named as an assumption. |
| c3 | Step 2 challenge ledger addresses every soft constraint and assumption from Step 1 with a verdict (keep/remove/test) and impact-if-removed analysis | PASS | The Challenge Ledger table has 6 rows covering all assumptions and the soft constraint. Each row has a Challenge question, a Verdict (Remove or Test), and an 'Impact if removed' column describing consequences. E.g., row 1: verdict Remove → 'Could use semantic versioning, headers, or deprecation policies instead'. |
| c4 | Step 3 reconstruction starts only from verified truths and hard constraints — ignores current URL path versioning form and asks what function requires | PASS | The Reconstruction section opens 'Starting from these truths only:' and lists functional truths (5 consumers, APIs must evolve without breaking callers, actual requirement is 'predictable, managed change'). The section explicitly frames the requirement without reference to URL shape: 'The actual requirement is: "predictable, managed change" — not "URL paths must have version numbers"'. |
| c5 | Step 4 delta analysis compares reconstructed approach against current state with a table showing which assumption removal enabled each difference | PASS | The Delta Analysis table has columns: Aspect, Current (URL Versioning), Reconstructed (Deprecation Policy), Why Different. The 'Why Different' column traces each difference to an assumption, e.g., 'Removes assumption that version number belongs in path', 'Treats external partners as managed contracts, not optional clients', 'Fewer codepaths = less complexity'. |
| c6 | Output uses the defined first-principles template with all four sections | PASS | All four sections are present under explicit headings: 'Component Inventory', 'Challenge Ledger', 'Reconstruction', and 'Delta Analysis'. Migration Assessment and Recommendations are additional bonus sections. |
| c7 | Migration assessment distinguishes quick wins from changes requiring stakeholder authority | PARTIAL | The Migration Assessment has three labeled tiers: 'Quick wins (do immediately, low risk)', 'Requires validation (experiment before committing)', and 'Requires authority (stakeholder decision)'. The authority tier includes 'Commit to explicit SLAs', 'Partner notification process', and 'Internal deployment coordination'. Ceiling is PARTIAL. |
| c8 | Reconstruction does not conclude "change nothing" — if it does, the skill's own rules require returning to Step 2 to challenge more assumptions | PASS | The reconstruction proposes a significant shift: single API surface (/api/users with no version in path), a formal deprecation policy with Deprecation/Sunset headers (RFC 8594), explicit SLAs with external partners, and unified internal deployments. Not a status-quo conclusion. |
| c9 | Output classifies "that's how APIs work" and "clients will break otherwise" explicitly as ASSUMPTIONS, not hard constraints — naming them as inherited convention, not a function-imposed requirement | PASS | Both are in the Component Inventory as **Assumption**: 'URL versioning is required' with evidence 'Never verified; believed because "that's how APIs work"', and 'Clients will break without versioning' with evidence 'Conflates "clients break" with "URL paths must differ"'. |
| c10 | Output's hard constraints are limited to truths grounded in function — e.g. "consumers must be able to upgrade independently", "old clients must keep working during transition windows", "the same identifier must reach the same code path" — not URL-shape conventions | PASS | Hard constraints listed are: 'Don't break existing clients' (functional), 'APIs will evolve' (functional), 'HTTP as protocol' (technical reality). No URL-shape convention appears as a hard constraint. |
| c11 | Output's challenge ledger gives every soft constraint and assumption a verdict (KEEP / REMOVE / TEST) with the impact-if-removed analysis — e.g. "if we remove URL-path versioning, what breaks for the 2 external partners?" | PASS | The Challenge Ledger table has a Verdict column (Remove or Test for each of 6 rows) and an 'Impact if removed' column. E.g., assumption 2 (External partners expect /v1, /v2 URLs): verdict Test, impact 'May be satisfied by explicit deprecation timeline; no URL change needed'. |
| c12 | Output's reconstruction starts from versioning's actual function — versioning exists to allow simultaneous old + new behaviour for different consumers — and considers all viable forms (URL path, header, query param, content-type, no version with additive-only changes) | PASS | Reconstruction frames function as 'predictable, managed change'. It considers: header-based versioning ('Accept headers or application/vnd.company.api+json; version=2'), single-surface with deprecation policy (no-version additive approach), and the cross-domain insight discusses URL vs. header patterns. Query param is not explicitly named, but the other major viable forms are addressed. |
| c13 | Output addresses the small consumer set (3 internal + 2 external) as a relevant fact — internal services can typically migrate together, external partners need a longer window, which influences the chosen versioning mechanism | PASS | The reconstruction explicitly distinguishes: 'For internal services: Upgrade them together with the API... deploy as a unit' and 'For external partners: Establish SLAs. "We'll give 6 months notice before breaking changes."' The migration assessment also separates internal vs. external upgrade considerations. |
| c14 | Output's delta analysis compares the reconstructed approach to the current `/v1/`, `/v2/` form with a table showing "this changed because we removed assumption X" — not just a "before/after" comparison without traceability | PASS | The Delta Analysis table's 'Why Different' column provides assumption-traceable reasoning for each row: e.g., URL structure row — 'Removes assumption that version number belongs in path'; client upgrade path row — 'Treats external partners as managed contracts, not optional clients'; internal service row — 'Aligns with reality (you control internal services)'. |
| c15 | Output's reconstruction does NOT conclude "no change" — it either identifies a meaningful shift (e.g. "internal APIs can use header-based versioning to keep the URL stable; external partners keep URL versioning") or returns to Step 2 to challenge more assumptions | PASS | The reconstruction proposes moving to a single-surface deprecation-policy model, including: no URL versioning, Deprecation/Sunset headers (RFC 8594), explicit SLAs, co-deployment of internal services. The Recommendations section summarizes: 'If external partners can upgrade on a 6-month timeline → Deprecation policy is simpler and matches how modern APIs work. For internal services → No URL versioning needed at all.' |
| c16 | Output's migration assessment distinguishes quick wins (e.g. add a deprecation header to v1 starting now) from changes requiring stakeholder authority (e.g. asking external partners to switch to header-based versioning needs lead time and contractual coordination) | PASS | Migration Assessment explicitly labels three tiers. 'Quick wins' include asking external partners and drafting a deprecation policy. 'Requires authority' includes 'Commit to explicit SLAs: Moving away from implicit URL versioning means you need explicit break timelines. This might require conversations with product/customer success' and 'Partner notification process: Set up mechanism to notify external partners 6 months ahead. Not email-when-we-feel-like-it, but systematic.' |
| c17 | Output addresses the API evolution mechanism alongside versioning — additive changes (new optional fields) don't need a new version, breaking changes do; this is more important than the version-shape choice | PASS | The Challenge Ledger (row 5) states 'Backward compatibility ≠ URL structure. You can evolve the same endpoint with a deprecation policy.' The reconstruction separates the breaking-change deprecation policy (6 months notice, migration guides) from endpoint evolution, and the Recommendations section frames the core insight as 'evolve APIs without surprising 5 specific consumers' vs. supporting simultaneous versions — implying additive changes need no new version URL. |
| c18 | Output references real-world examples of non-URL-path versioning (Stripe's date-based header versioning, GitHub's media-type versioning) as evidence the assumption is challengeable | PARTIAL | The cross-domain insight names 'GitHub, Stripe, Twitter, AWS use header-based versioning or single surfaces with deprecation policies' as counter-examples. However, the specific mechanisms (Stripe's date-based versioning, GitHub's media-type versioning) are not described — just a generic 'header-based versioning' attribution. The examples are named but not detailed. Ceiling is PARTIAL. |

### Notes

The output is an excellent application of the first-principles template. All four required sections (Component Inventory, Challenge Ledger, Reconstruction, Delta Analysis) are present and well-structured. The component inventory correctly distinguishes hard constraints (functional requirements) from soft constraints (URL path prefixes) and assumptions (inherited conventions). The challenge ledger covers all assumptions with explicit verdicts and impact analysis. The reconstruction is genuinely function-first rather than URL-shape-first, and the delta analysis traces each difference to a specific assumption removal. The migration assessment's three-tier structure (quick wins, validation, authority) fully satisfies the criterion for distinguishing stakeholder-gated changes. Two minor gaps: query param versioning is not explicitly enumerated as a viable alternative form, and real-world versioning mechanisms for Stripe (date-based) and GitHub (media-type) are named but not described. Neither gap materially affects the analysis quality. The additive-vs-breaking distinction is present implicitly throughout the deprecation policy framing but not stated as an explicit principle.
