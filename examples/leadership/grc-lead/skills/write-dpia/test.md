# Test: write-dpia

Scenario: A user invokes the skill for a processing activity that clearly triggers GDPR Article 35. Does the skill complete all six steps — processing description, necessity and proportionality, individual-perspective risk assessment, mitigation measures with residual risk reduction, DPO review section, and supervisory authority consultation determination?

## Prompt

/grc-lead:write-dpia "Behavioural Analytics Pipeline — Luminary (a fintech platform) wants to build a pipeline that tracks detailed user behaviour (page views, click sequences, session duration, feature usage patterns) and uses ML to predict which users are likely to churn or upgrade. This data will be combined with transaction history and account tier. Users are in the EU. The pipeline will run continuously and produce per-user scores updated daily."

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Step 1 produces a complete processing description — data categories, data subjects, purpose, how processed, retention period, recipients, and data flow
- [ ] PASS: Step 2 assesses necessity and proportionality against GDPR Article 5 principles — lawful basis, purpose limitation, data minimisation, storage limitation, and security
- [ ] PASS: Step 3 assesses risks from the individual's perspective — not the organisation's perspective
- [ ] PASS: Risk categories cover: unauthorised access, function creep, inaccurate decisions, lack of transparency, inability to exercise rights, and discriminatory effects
- [ ] PASS: Every risk rated Medium or above has at least one specific mitigation defined in Step 4
- [ ] PASS: Residual risk after mitigation is demonstrably lower than inherent risk for each mitigated risk
- [ ] PASS: Step 5 produces a DPO review section with a clear recommendation (Proceed / Proceed with conditions / Do not proceed)
- [ ] PASS: Step 6 determines whether Article 36 supervisory authority consultation is required with reasoning
- [ ] PASS: Output is written to a file in the correct DPIA format with version, date, owner, and status
- [ ] PARTIAL: Identifies that continuous ML-based profiling of EU users likely requires a DPIA under Article 35(3)(a) (large-scale profiling)

## Output expectations

- [ ] PASS: Output's processing description names the data categories (page views, click sequences, session duration, feature usage, transaction history, account tier), the data subjects (EU users), the purpose (churn / upgrade prediction), the processing means (continuous pipeline + ML model), retention period, recipients (internal CS / sales teams), and includes a data flow diagram
- [ ] PASS: Output's necessity and proportionality assessment evaluates each Article 5 principle — lawful basis (likely legitimate interest with LIA), purpose limitation (analytics only, not third-party sale), data minimisation (do all signals contribute?), storage limitation (retention proportionate to model training cycle), accuracy, security
- [ ] PASS: Output's risk assessment is from the individual's perspective — what could happen to a user — not from Luminary's perspective
- [ ] PASS: Output's risk categories cover unauthorised access, function creep (the score being repurposed for credit decisions or marketing), inaccurate decisions (false-positive churn predictions affecting service tier), lack of transparency (users unaware of scoring), inability to exercise rights (deletion, access), and discriminatory effects (proxy bias from behavioural signals correlating with protected characteristics)
- [ ] PASS: Output's mitigations target each Medium+ risk with at least one specific control — e.g. for function creep: documented purpose limitation in privacy notice, technical access controls preventing the score from feeding marketing systems
- [ ] PASS: Output's residual risk is demonstrably lower than inherent risk per mitigated risk, with a likelihood × impact recalculation shown after controls
- [ ] PASS: Output's DPO review section produces a clear recommendation — Proceed / Proceed with conditions (specifying the conditions) / Do not proceed — not a vague "this is risky"
- [ ] PASS: Output's Article 36 determination is explicit — supervisory authority consultation IS or IS NOT required, with reasoning tied to whether residual risk remains High
- [ ] PASS: Output is written to a file with version, date, owner (DPO), and status — not only returned in conversation
- [ ] PASS: Output explicitly states this processing triggers Article 35(3)(a) (systematic and extensive evaluation based on automated processing including profiling, on which decisions producing legal/significant effects are based) and likely (b) (large-scale processing of personal data)
