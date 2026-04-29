# Test: risk-assessment

Scenario: A user invokes the skill to assess a system that handles sensitive data. Does the skill work through all seven steps in order, quantify every risk with likelihood and impact, document existing controls, calculate residual risk, and produce a treatment plan with owners and review dates?

## Prompt

/grc-lead:risk-assessment "Prescribe — a telehealth prescription management system that stores patient medication history, processes repeat prescriptions, and sends SMS reminders. Patients are in Australia and New Zealand. The system uses a third-party SMS provider (Twilio) and a cloud database (AWS RDS in ap-southeast-2)."

## Criteria

- [ ] PASS: Step 1 defines scope boundaries explicitly — what is in and out, time horizon, and affected stakeholders
- [ ] PASS: Risk identification covers all seven categories — including Regulatory, AI/ML (even if N/A), Data, Operational, Financial, Reputational, and Vendor
- [ ] PASS: Every identified risk has a unique ID, a likelihood level with a percentage estimate, and an impact level
- [ ] PASS: Inherent risk scores are derived from the matrix — not assigned arbitrarily
- [ ] PASS: Existing controls are documented per risk — not just assumed present
- [ ] PASS: Residual risk is calculated after controls, not just inheriting the inherent score
- [ ] PASS: Every risk has a treatment decision (Accept/Mitigate/Transfer/Avoid) with specific detail
- [ ] PASS: Accepted risks have an owner, a justification, and a review date (max 6 months)
- [ ] PASS: Output is compiled into the risk register format with a summary table and prioritised action list
- [ ] PARTIAL: Identifies Twilio as a vendor risk and AWS RDS as a data residency and availability risk

## Output expectations

- [ ] PASS: Output's scope section names Prescribe, the in-scope subsystems (prescription store, repeat-prescription processor, SMS reminder service), the time horizon (e.g. 12 months), and the affected stakeholders (patients in AU/NZ, prescribers, pharmacy partners, regulators)
- [ ] PASS: Output identifies risks in all seven categories with at least one risk per category — Regulatory (Privacy Act / Health Records / TGA), AI/ML (N/A noted explicitly if no ML), Data (PHI breach, ID disclosure), Operational (SMS delivery failure on critical reminder), Financial, Reputational, Vendor (Twilio, AWS)
- [ ] PASS: Output assigns each risk a unique ID (e.g. R-001, R-002), a likelihood with a percentage estimate (e.g. "Medium ~25%"), and an impact level (Low / Medium / High / Critical) — not just verbal labels
- [ ] PASS: Output's inherent risk scores are derived from a likelihood × impact matrix (e.g. 5×5) shown in the output — not assigned arbitrarily
- [ ] PASS: Output documents existing controls per risk — e.g. for "patient data breach via SMS provider" the existing controls are "Twilio TLS in transit, signed DPA, no PHI in SMS body" — not assumed
- [ ] PASS: Output calculates residual risk per risk after the existing controls are applied, with a clear reduction shown (e.g. "Inherent: High, Residual: Medium after controls")
- [ ] PASS: Output assigns a treatment decision (Accept / Mitigate / Transfer / Avoid) per risk with specifics — what mitigation will be added, what the transfer mechanism is (insurance), why an acceptance is reasonable
- [ ] PASS: Output's accepted risks have a named owner, justification, and a review date with the rule that the date is no more than 6 months out
- [ ] PASS: Output addresses Twilio specifically as a vendor risk — DPA in place, breach notification clauses, TGA / Privacy Act-compliant data handling, dependency risk if Twilio outage prevents critical reminders
- [ ] PASS: Output addresses AWS RDS in ap-southeast-2 as a data residency choice (Australia + NZ) and a single-AZ vs multi-AZ availability decision, with the trade-offs surfaced
