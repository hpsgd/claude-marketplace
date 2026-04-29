# Output: Write onboarding playbook

**Verdict:** PASS
**Score:** 18/18.5 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines time-to-first-value (TTFV) as a customer-perceived outcome — Step 2 explicitly rejects "completed onboarding call" and requires outcomes like "generated first report with their own data"
- [x] PASS: Skill requires TTFV to be measurable automatically — "If you cannot measure TTFV automatically, it is not a real metric. Build the instrumentation first"
- [x] PASS: Every milestone has an escalation trigger with a specific day threshold — the milestone table template includes an "Escalation trigger" column with explicit day numbers (e.g. "No login by Day 10", "Setup not started by Day 5")
- [x] PASS: Skill requires a segment definition before designing milestones — Step 1 is mandatory and states "Enterprise onboarding is NOT self-serve onboarding with more meetings. They are fundamentally different playbooks"
- [x] PASS: Skill includes a kickoff meeting agenda with timing, owners, and outputs per topic — Step 4 provides a full table with time slots, Owner column, and Output column per topic
- [x] PASS: Skill defines handoff criteria as a checklist — Step 6 provides a checklist table with the gate "Handoff is complete when ALL of the following are true"
- [x] PARTIAL: Skill maps common blockers with early warning signs — Step 5 requires a four-column table including "Early warning sign" per blocker, with the rule "Every blocker needs an early warning sign." This fully satisfies both the base and warning-sign requirements; scored at 1.0 rather than 0.5 since the skill meets the strict interpretation
- [x] PASS: Skill requires measurable success criteria for every milestone — Rules section states "Milestones must have measurable success criteria. 'Complete onboarding call' is not a success criterion"
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — lines 1–7 contain all three required fields

### Output expectations

- [x] PASS: The TTFV examples in the skill ("sent first campaign", "processed first payment", "generated first report with their own data") are customer-perceived outcomes tied to specific product events, not activity completions
- [x] PASS: TTFV measurement is required to name the specific product event or metric; if not currently instrumented, the skill mandates building it before the playbook ships
- [x] PASS: Segment definition step is mandatory and the skill explicitly distinguishes enterprise from self-serve; the segment table captures contract type, company size, and technical sophistication — covering the 200+ seats, dedicated IT, $100k+ criteria from the prompt
- [x] PASS: The milestone table template requires measurable success criteria per milestone; the Rules section and examples explicitly reject activity-based milestones ("complete onboarding call is not measurable")
- [x] PASS: Escalation triggers use concrete day thresholds (e.g. "No login by Day 10", "Health score not green by Day 40") — not vague "follow up if no response"
- [x] PASS: The kickoff agenda table has time blocks, named owners (CS, CS + Champion, CS + Tech lead), and output per topic (e.g. "Integration plan, data migration scope", "Shared timeline with dates")
- [x] PASS: The handoff checklist uses checkboxes and an ALL-must-be-true gate covering TTFV, adoption %, champion, exec sponsor, success criteria, health score, and QBR scheduled
- [x] PASS: Common blockers table includes Security/compliance review (maps to IT security / SSO) with an early warning sign ("InfoSec blocks integration, SSO requirements not met"); other enterprise-specific blockers (technical integration, stakeholder misalignment) are also present with early warning signs
- [x] PASS: Rules section and milestone template explicitly reject "complete onboarding call" as a success criterion; all milestone examples are outcome-based
- [~] PARTIAL: Post-onboarding handoff to AE / sustain CSM is addressed in Step 6 with a 5-step handoff process (warm intro, BAU CS relationship call, first QBR within 30 days) and a handoff document with milestone history — but the specific artefacts that travel forward are not enumerated; partial credit for process presence without explicit artefact inventory

## Notes

The skill's strongest element is the TTFV instrumentation gate in Step 2 — making an unmeasured TTFV a blocker rather than a warning forces teams to build observability before the playbook ships. The escalation trigger per milestone converts escalation from a judgment call into a protocol.

The PARTIAL criterion 7 in the Criteria section is scored at full credit (1.0) because the skill fully satisfies the strict interpretation — early warning signs are required per blocker, not optional. The rubric marked it PARTIAL to allow for skill definitions that list blockers without warning signs, which is not the case here.

The only genuine gap is the post-onboarding artefact inventory. The handoff process is present and well-structured, but the skill does not name what the sustain CSM or AE inherits (success metrics, integration map, champion contact, health history, agreed QBR cadence). That earns the PARTIAL on output expectation 10.

One structural note: the skill references `templates/onboarding-playbook.md` in its closing line. That template does not exist in the plugin directory. If the skill relies on it for output structure, the missing file is a runtime gap worth flagging to the plugin author.
