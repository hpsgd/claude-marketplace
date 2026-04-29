# Output: wisdom recording a new principle

**Verdict:** PARTIAL
**Score:** 12.5/15.5 criteria met (81%)
**Evaluated:** 2026-04-29

## Results

### Criteria section

- [x] PASS: Skill classifies the domain (development) and observation type (principle) before writing anything — met: Steps 1 and 2 in the recording flow explicitly sequence domain classification and observation-type classification before the write step
- [x] PASS: Confidence level assigned is based on evidence count — 3 incidents earns below 85% — met: the rule "It takes 5+ consistent observations to reach crystallised (85%+). Never assign high confidence to a single data point" enforces this mechanically
- [x] PASS: Skill checks for an existing principle on the same topic before creating a new entry — met: "Update, don't duplicate. When a new observation matches an existing principle, increment its observation count and confidence — don't create a new entry"
- [x] PASS: Anti-pattern entry written with root cause, not just "don't do this" — met: the rule "Anti-patterns need root causes" is explicit and the example frame demonstrates the required format
- [x] PASS: Wisdom frame written in the correct format — frontmatter, core principles section, and evolution log entry — met: the format is fully specified with all required structural elements
- [x] PASS: Output uses the "When recording" template — observation type, added text, confidence with basis, frame status, and saved-to path — met: all five fields are defined in the Output Format section
- [~] PARTIAL: Cross-domain connection noted if one exists — partially met: the skill has a Cross-Domain Connections field in the frame structure and the synthesis mode, but the recording workflow (Steps 1-3) does not include a mandatory step to check other frames during a record operation; a conforming agent following only the recording steps would skip it
- [x] PASS: Confidence assignment rule respected — single data point cannot reach crystallised, 3 observations cannot reach 85%+ — met: rule is unambiguous

### Output expectations section

- [x] PASS: Output classifies the domain as DEVELOPMENT and the observation as PRINCIPLE with reasoning — met: the two-step classification sequence produces exactly this
- [x] PASS: Output assigns a confidence below 85% with specific value and basis stated — met: the confidence rule and the "based on M observations" field in the recording template together enforce this
- [x] PASS: Output checks the wisdom frames location for an existing principle BEFORE creating a new entry — met: the deduplication rule applies, and Read/Grep are in allowed-tools to support the lookup
- [x] PASS: Anti-pattern entry includes root cause — met: rule and example both require it
- [x] PASS: Wisdom frame uses correct format — frontmatter, Core Principles, Evolution Log — met: all structural elements are specified
- [ ] FAIL: Evolution log records the three specific incidents (auth April, billing February, payment January) as evidence — not met: the Evolution Log format shown in the template records date, principle name, and generic source only ("source: repeated correction"); the skill does not instruct the agent to enumerate named incidents in the log entry
- [x] PASS: "When recording" template is followed — met: all required fields are defined
- [x] PASS: Output respects the confidence assignment rule and states what would push it over — met: the 5+ threshold rule is clear; the "based on M observations" field makes the gap computable, even if the skill does not explicitly instruct naming what more is needed
- [~] PARTIAL: Output addresses a cross-domain connection with at least one mention — partially met: the skill supports cross-domain work as a first-class feature but does not require it during a recording operation; whether this surfaces depends on the agent connecting the synthesis rules to the recording context
- [ ] FAIL: Output addresses the 1-in-10 broad-rewrite-clean rate explicitly — not met: the skill has no mechanism for handling exception rates within a principle; the "Predictions must be falsifiable" rule applies to predictions, not principles, and nothing instructs the agent to acknowledge the 10% exception case

## Notes

The skill is well-designed for the core recording workflow. The two outright failures are both about evidence handling: the evolution log format lacks specificity requirements for named incidents, and the skill has no concept of acknowledging exception rates within a principle. The cross-domain gap is structural — synthesis is a separate invocation mode, not a step wired into the recording flow. A rigorous agent could bridge these gaps using the spirit of the rules, but the skill definition as written does not mandate it.
