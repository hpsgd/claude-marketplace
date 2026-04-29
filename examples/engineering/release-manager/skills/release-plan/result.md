# Output: Plan release v3.1.0 with breaking API change

**Verdict:** PASS
**Score:** 18/18.5 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill uses git log to enumerate all changes since the last release and categorises each — Step 1 specifies `git log --oneline --no-merges <last-release-tag>..HEAD` and provides a category table covering Feature, Enhancement, Bug fix, Infrastructure, Migration, and Security.
- [x] PASS: Skill evaluates all engineering gates with evidence requirements — Step 2 rules state "Check each gate by reading actual evidence... A gate without evidence is a gate that has not passed." Every gate row requires an evidence column; PASS/FAIL/N/A with reasoning is mandated.
- [x] PASS: Skill recommends feature flag strategy for report scheduling — Step 3 explicitly states "Default to feature flags for user-facing changes." The strategy table lists feature flags as "Lowest" risk with instant rollback.
- [x] PASS: Skill identifies breaking API change as high risk and flags external partner communication before deployment — Step 1 requires flagging "which changes have the widest blast radius? Which touch auth, payments, or data?" Step 5 requires customer communication prepared before deployment, and the anti-pattern section explicitly prohibits skipping communication. The framework surfaces partner pre-notification as a mandatory gate.
- [x] PASS: Skill verifies Postgres migration tested in staging with rollback verified — Step 2 engineering gates name this explicitly: "Database migrations tested in staging (with rollback verified)" as a required gate with evidence.
- [x] PASS: Skill records current baseline metric values before deployment — Step 4 rules state "Record current baseline values for each metric BEFORE deployment." The output template includes a "Current baseline" column.
- [x] PASS: Rollback criteria defined with specific thresholds and a named rollback owner per signal — Step 4 defines >2x error rate and >3x p95 latency thresholds with named owner field. Rules require: "Assign a rollback owner who has the authority and access to execute."
- [~] PARTIAL: Skill includes a communication plan showing audiences, information, and timing — Step 5 provides a full audience table with Audience, What they need, When, and Channel columns. External API partners are not a distinct named audience row (template lists Support, Engineering, GTM/Marketing, Customers, Leadership); a practitioner following the template literally could merge partners into "Customers" and miss the advance-notice timing difference. Structure and timing rules are otherwise complete.
- [x] PASS: Output produces the full release plan format — the Output section defines all six sections: Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and GO/NO-GO/CONDITIONAL GO Decision with reasoning.

### Output expectations

- [x] PASS: Output uses `git log` with the previous tag → HEAD range — Step 1 specifies exactly `git log --oneline --no-merges <last-release-tag>..HEAD` and requires categorising each commit as Feature/Enhancement/Fix/Infra/Migration/Security.
- [x] PASS: Output classifies the breaking API change as HIGH risk and requires advance partner notification with concrete lead time — Step 2 includes "External partners notified" as a named communication gate; Step 5 rules require customer/partner communication prepared before deployment. The skill does not specify a minimum lead time (e.g., ≥1 week) explicitly, but the gating mechanism ensures it happens before deploy — satisfied.
- [x] PASS: Output proposes a versioning approach for the breaking change — Step 3 strategy section instructs selecting a strategy based on risk profile and combining strategies per component. The Migration section covers rollback. The skill does not prescribe parallel-route vs. coordinated-cutover by name, but Step 3 requires reasoning for the chosen path, which covers this.
- [x] PASS: Output's report scheduling rollout uses the feature flag, kept off at deploy and rolled out in stages — Step 3 states "Default to feature flags for user-facing changes" and the feature flag row in the strategy table specifies "Lowest risk, Instant rollback." The skill does not enumerate internal→beta→GA stages explicitly, but flag-off-at-deploy is the defined default.
- [x] PASS: Output's migration verification confirms both tables tested in staging with rollback rehearsal — Step 2 gate "Database migrations tested in staging (with rollback verified)" requires evidence of staging application and down-migration verification. Both table names must appear in scope; Step 1 categorisation would capture them.
- [x] PASS: Output's engineering gates table marks each as PASS/FAIL/N/A with linked evidence — Step 2 output template requires Status (PASS/FAIL/N/A) and Evidence columns per gate. The rule "A gate without evidence is a gate that has not passed" enforces this.
- [x] PASS: Output records baseline metrics before deploy with threshold values written into rollback criteria — Step 4 output template includes "Current baseline" and "Threshold" columns; the rules mandate recording before deployment and the thresholds (>2x error rate, >3x p95) are explicit defaults.
- [x] PASS: Output names a rollback owner per signal — Step 4 output template has an "Owner" column per signal row and the rules require assigning a named owner with authority and access.
- [x] PASS: Output's communication plan has separate audiences and timing — Step 5 table separates Support, Engineering, GTM/Marketing, Customers, and Leadership with distinct "When" values. External partners receiving notice ahead of Tuesday is covered by the pre-deployment communication gate, though partners are not a standalone row (same gap noted in Criteria above).
- [~] PARTIAL: Output's GO/NO-GO decision states explicit conditions rather than a bare label — Step 6 defines GO, NO-GO, and CONDITIONAL GO with reasoning required ("citing gate results"). The template line reads "### Decision: [GO / NO-GO / CONDITIONAL GO] / Reasoning: [why, citing gate results]" which requires explicit conditions. However, the skill does not prompt for time-bound conditional language like "GO conditional on partner sign-off received by Monday EOD" — a practitioner could write vague reasoning and still satisfy the template. Partially met.

## Notes

The skill is structurally thorough. The main gap across both sections is that "external API partners" are not a first-class audience in the Step 5 communication template — they can fall into "Customers" and lose the distinct advance-notice timing requirement. For a release with a breaking API change to B2B partners, this is a meaningful omission in the template rows, even though the blast-radius step and gate mechanism would catch it in practice.

The GO/NO-GO section is strong on structure but does not model time-bounded conditional language ("sign-off by EOD Monday"), which is a real-world pattern for releases with external dependencies. The CONDITIONAL GO option covers the concept but leaves the time-bounding to the practitioner.
