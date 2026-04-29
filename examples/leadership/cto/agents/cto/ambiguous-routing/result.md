# Result: Ambiguous routing between architect and developer

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 15/16 criteria met (93.75%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: CTO reads the request fully before classifying — "Read the request fully. Extract explicit requirements, implied requirements, anti-requirements, and gotchas" is the first mandatory step in Assess Before Acting — met
- [x] PASS: CTO produces a trade-off summary before delegating — "before delegating to the architect, produce a trade-off summary in your output: what options exist, what each sacrifices, and your initial assessment" is explicit for architecture decisions — met
- [x] PASS: CTO correctly identifies this as needing BOTH — "Cross-cutting → decompose into specialist tasks, coordinate" applies; architecture decision + implementation maps to two separate specialists — met
- [x] PASS: Delegation to architect specifies `system-design` — "System structure, bounded contexts, integration patterns → system-design" maps directly to cross-service rate limiting strategy — met
- [x] PASS: Delegation sequence is correct — architecture classification delegates to architect first; implementation follows via the appropriate developer — met
- [~] PARTIAL: CTO identifies that the immediate performance issue may need a quick fix before the architectural solution — Section 6 explicitly covers active service degradation (not just declared incidents) and mandates mitigation-first including "emergency limit on the offending path" BEFORE the architectural fix. The instruction is present and applies to this scenario. Marked partial because the definition handles this as a general degradation pattern rather than surfacing it as an explicit output requirement for the dispatch plan format — partially met
- [x] PASS: Delegation includes clear scope boundaries — "Define the scope — what's in, what's explicitly out" is a required element of every delegation — met
- [x] PASS: ADR is included as a required deliverable — "Every architecture decision must produce an ADR → include write-adr as a required deliverable in the acceptance criteria" is explicit — met

### Output expectations

- [x] PASS: Output explicitly identifies that the request requires BOTH architecture and implementation work — cross-cutting decomposition pattern + architecture classification + implementation delegation combine to produce this — met
- [x] PASS: Output dispatches to architect first using `/architect:system-design` (or equivalent), then to developer — agent table maps cross-service structure to `system-design`; sequencing rules enforce architect-first — met
- [x] PASS: Output identifies the immediate problem as a candidate for quick mitigation — Section 6 covers active degradation, names "emergency limit on the offending path" as a mitigation move, and explicitly requires this BEFORE the architectural fix. The scenario ("getting hammered", "degrading performance for everyone else") triggers Section 6 — met
- [x] PASS: Output's delegation includes clear scope boundaries — delegation protocol requires explicit scope (what's in, what's explicitly out) for every dispatch — met
- [x] PASS: Output requires an ADR as a deliverable from the architect — acceptance criteria must include `write-adr` for every architecture decision — met
- [x] PASS: Output frames the bulk-import scenario explicitly as the anchor case — "When the request names a specific triggering scenario, treat it as the anchor case any solution must satisfy — frame it explicitly in your dispatch plan" is explicit instruction — met
- [x] PASS: Output includes customer communication coordinated with CPO/customer success — Section 6 step 4 says "coordinate the message, don't impose unilaterally" and routes to coordinator → CPO's support team; planned rate-limiting changes that alter customer-visible behaviour are explicitly in scope — met
- [~] PARTIAL: Output identifies success criteria with measurable p95 latency baseline — the delegation protocol requires "acceptance criteria — how you'll know it's done" and "evidence requirements" for every delegation, so criteria will appear. However, no instruction explicitly directs quantitative performance baselines (latency percentiles, throughput targets) as the measure of success — partially met

## Notes

The definition handles this scenario well. The combination of the mandatory "anchor case" framing instruction, the active-degradation section that explicitly names "emergency limit on the offending path" as a mitigation move (covering non-declared incidents), the mandatory ADR requirement, the explicit cross-cutting decomposition pattern, and the customer-communication escalation path together address every criterion. The previous result (PARTIAL, 70%) underscored the definition on the quick-mitigation and customer-communication criteria because it read Section 6 as incident-only — but the definition explicitly says it covers "active service degradation that hasn't been formally declared an incident." The only genuine gap is quantitative performance success criteria: the definition asks for acceptance criteria but does not specifically require performance baselines as a measurable deliverable.
