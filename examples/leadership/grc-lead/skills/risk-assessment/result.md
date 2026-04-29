# Result: risk-assessment

**Verdict:** PASS
**Score:** 19/20 criteria met (95%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Step 1 defines scope boundaries explicitly — met. The scope section requires Subject, Boundaries, Exclusions, Time horizon, Assessment date, and Stakeholders as mandatory fields.
- [x] PASS: Risk identification covers all seven categories — met. Step 2 mandates all seven categories and explicitly states "Do not skip a category because you think it does not apply — document 'no identified risks' with reasoning."
- [x] PASS: Every identified risk has a unique ID, a likelihood level with a percentage estimate, and an impact level — met. Step 3 requires the likelihood table with percentage ranges and the impact table; unique IDs ("assign a unique ID, e.g. R-001") are required.
- [x] PASS: Inherent risk scores are derived from the matrix — met. Step 3 requires using the risk matrix; the output template notation "Inherent risk: [level] (from matrix)" enforces this explicitly.
- [x] PASS: Existing controls are documented per risk — met. Step 4 requires documenting what controls exist, whether automated or manual, when last verified, and whether documented; the anti-pattern "Controls without verification" explicitly prohibits claiming a control without evidence.
- [x] PASS: Residual risk is calculated after controls — met. Step 5 defines control effectiveness (Full/Partial/None) and the one-level or two-level reduction rule; residual risk must reflect controls applied.
- [x] PASS: Every risk has a treatment decision with specific detail — met. Step 6 requires treatment type and treatment detail with specific actions; the anti-pattern "'We'll deal with it later' is not a treatment" is explicit.
- [x] PASS: Accepted risks have owner, justification, and review date (max 6 months) — met. Step 6 acceptance rules require "an owner (a person, not a team)", "an expiry date (maximum 6 months)", and "Acceptance is documented with reasoning — 'low priority' is not a justification."
- [x] PASS: Output compiled into risk register format with summary table and prioritised action list — met. The Output Format section includes the per-risk blocks, Risk Summary table, Prioritised Actions list, and Review Schedule as required sections.
- [~] PARTIAL: Identifies Twilio as vendor risk and AWS RDS as data residency and availability risk — partially met. Twilio appears in the Vendor category guidance; AWS RDS data residency is addressable under Regulatory (APP 8) and Vendor. The skill's Vendor category guidance lists "data residency" as an explicit sub-concern, but the skill does not mandate breaking out RDS residency as a separate risk vs. subsuming it under a regulatory risk. A thorough assessment would surface both residency and availability as distinct RDS risks, but the skill text doesn't require it explicitly.

### Output expectations

- [x] PASS: Output's scope section names Prescribe, the in-scope subsystems, the time horizon, and the affected stakeholders — met. Step 1 requires Subject (Prescribe), Boundaries (prescription store, repeat-prescription processor, SMS reminder service), Time horizon, and Stakeholders (patients in AU/NZ, prescribers, pharmacy partners, regulators) as mandatory scope fields.
- [x] PASS: Output identifies risks in all seven categories with at least one risk per category — met. Step 2 mandates all seven categories including Regulatory (Privacy Act / Health Records / TGA applies directly), AI/ML (N/A with reasoning if no ML), Data (PHI breach), Operational (SMS delivery failure), Financial, Reputational, and Vendor (Twilio, AWS).
- [x] PASS: Output assigns each risk a unique ID, a likelihood with a percentage estimate, and an impact level — met. The output template requires `**Likelihood:** [level] ([percentage estimate])` and `**Impact:** [level]` with a unique R-NNN ID per risk.
- [x] PASS: Output's inherent risk scores are derived from a likelihood × impact matrix shown in the output — met. Step 3 provides the full 4×4 matrix and the output template notation "(from matrix)" enforces visible derivation.
- [x] PASS: Output documents existing controls per risk with verification evidence — met. Step 4 requires "when were controls last verified?" and the anti-pattern "Controls without verification" explicitly prohibits unverified controls. The output template field "Current controls" is a required per-risk field.
- [x] PASS: Output calculates residual risk per risk after existing controls are applied, with a clear reduction shown — met. The output template includes `**Control effectiveness:** [Full / Partial / None]` and `**Residual risk:** [level]`, with Step 5 defining the reduction rules explicitly.
- [x] PASS: Output assigns a treatment decision per risk with specifics — met. The output template requires both `**Treatment:** [Accept / Mitigate / Transfer / Avoid]` and `**Treatment detail:** [specific action or justification]` as required fields.
- [x] PASS: Output's accepted risks have a named owner, justification, and a review date no more than 6 months out — met. Step 6 acceptance rules are explicit: named person (not team), maximum 6-month expiry, documented reasoning.
- [x] PASS: Output addresses Twilio specifically as a vendor risk — met. The Vendor category in Step 2 lists "Provider outage, security posture, contract terms, data residency" — all directly applicable to Twilio (DPA, breach notification, TGA / Privacy Act-compliant handling, outage risk for critical reminders). The skill guides identification of these concerns.
- [~] PARTIAL: Output addresses AWS RDS in ap-southeast-2 as a data residency choice and a single-AZ vs multi-AZ availability decision with trade-offs surfaced — partially met. The Vendor and Regulatory categories cover data residency and availability; however, the skill does not specifically prompt for single-AZ vs multi-AZ trade-off analysis. A well-executed assessment would surface this, but the skill text does not require it explicitly, making this dependent on assessor judgment rather than the skill's structure.

## Notes

The skill is structurally strong. All mandatory fields are enforced via the output template, the matrix derivation is visible, and the anti-patterns cover the most common failure modes (orphaned acceptances, unverified controls, missing residual risk). The one gap is that AWS-specific availability topology (single-AZ vs multi-AZ) is not prompted for — the skill addresses residency and availability at a category level but doesn't drill into infrastructure topology decisions. For a telehealth system with critical reminders, that's a meaningful omission worth noting. The Twilio vendor risk coverage is solid through the Vendor category guidance.
