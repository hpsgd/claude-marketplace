# Output: Triage tickets

**Verdict:** PARTIAL
**Score:** 15.5/18 criteria met (86%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill classifies each ticket across multiple dimensions — category (bug/question/feature/billing), severity, and routing destination — met: Step 2 covers category (8 types), severity (4 levels), and routing (6 destinations)
- [x] PASS: Skill includes pattern detection — when 3 or more tickets match the same root issue, they should be grouped and escalated — met: Step 3 explicitly defines "Escalation trigger: 3+ tickets on the same issue"
- [x] PASS: Skill generates a bug report or incident escalation for patterns that suggest a systemic issue — met: Step 3 includes a PATTERN ESCALATION template; Step 4 produces structured bug reports for engineering
- [x] PASS: Skill produces a structured triage table as output — met: Step 5 specifies a table with defined columns
- [x] PASS: Skill requires an ingest step — reading all tickets before classifying any — met: Step 1 reads every ticket; classification is Step 2, sequenced after ingest
- [~] PARTIAL: Skill assigns a response SLA or priority to each ticket — partially met: severity table in Step 2 includes explicit response targets (Critical: 1h ack, High: 4h ack, Medium: 1BD, Low: 2BD) but the triage table output does not include a Priority or SLA column — severity does this work implicitly rather than surfacing it per row
- [x] PASS: Skill routes tickets to appropriate teams or owners, not just classifies them — met: routing table maps issue types to six named destinations; Step 2 requires routing as a classification dimension on every ticket
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — met: frontmatter at lines 1-7 contains all three required fields plus user-invocable and allowed-tools

### Output expectations

- [x] PASS: Output's ingest step reads ALL tickets BEFORE classifying any — met: Step 1 (Ingest and normalise) is a discrete step preceding Step 2 (Classify); instructions say "Read every ticket" before classification begins
- [x] PASS: Output's triage table classifies each ticket across the dimensions — category, severity, and routing destination — met: triage table in Step 5 includes Category, Severity, and Route to columns
- [x] PASS: Output detects the login-error pattern — multiple tickets sharing the same root cause are GROUPED — met: Step 3 defines duplicate clusters (2+) and escalation trigger (3+) for grouping
- [x] PASS: Output generates an incident escalation for the login pattern — met: PATTERN ESCALATION template in Step 3 includes affected user count, first reported date (time window), sample ticket IDs, and recommends escalation to product/engineering
- [ ] FAIL: Output's structured triage table has the required columns — Ticket ID, Customer, Category, Severity, Routing, Priority, Pattern Group, Suggested Owner — not met: Step 5 table schema has Ticket ID, Summary, Category, Severity, Route to, Workaround, Pattern cluster — missing Customer, Priority, and Suggested Owner columns
- [ ] FAIL: Output assigns a response SLA per ticket based on severity with explicit values per row — not met: SLA targets exist in the Step 2 severity reference table but are not a column in the output triage table; each ticket does not carry an explicit SLA field in the deliverable
- [x] PASS: Output routes billing tickets to billing/finance, feature requests to product, bugs to engineering, questions to support agents — met: routing table in Step 2 distinguishes these destinations; "Support (self)" handles account/billing/known-issue
- [x] PASS: Output identifies tickets answerable from KB articles or self-serve — met: Documentation route exists for how-to questions; workaround column cites KB articles; Step 5 pattern summary flags workaround gaps needing KB articles
- [x] PASS: Output's pattern detection rule is explicit — 3+ tickets matching the same root cause trigger an incident escalation — met: Step 3 states this threshold explicitly
- [~] PARTIAL: Output addresses tickets that need follow-up classification — tickets needing more info get a separate state — partially met: Step 4 says to state what is missing and recommend the support agent ask for specifics, but there is no formal "needs more info" state in the triage table schema; incomplete tickets blend into the regular classification flow rather than getting a distinct output state

## Notes

The skill's five-step pipeline is logically sequenced and structurally sound. The main scoring gaps are in the triage table's column schema: Suggested Owner and Priority are absent, and per-row SLA is not surfaced in the output table (it exists only in the Step 2 reference table). For a handoff artifact, missing the assigned owner and the explicit SLA per ticket pushes decisions downstream to whoever reads the table.

The "needs more info" handling is procedural (Step 4 asks support agents to seek more data) but doesn't formalise this as a ticket state in the output. A triage table used in practice needs a clear column state so unclassified tickets don't get misrouted or silently dropped.

The skill is otherwise well-constructed: escalation rules are explicit (3+ threshold), severity auto-escalation for enterprise customers and data-loss signals is present, and the Related Skills links close the loop to KB creation and feedback synthesis.
