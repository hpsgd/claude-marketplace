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
