# Output: review-git non-conventional commits

**Verdict:** PASS
**Score:** 16/16.5 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill executes all five mandatory passes — Pass 1 through Pass 5 are all defined with explicit checks; the mandatory process header states "Execute all five passes"
- [x] PASS: Commits using past tense ("Updated", "Added") are flagged as Pass 1 findings with the specific commit subject line as evidence — Pass 1 step 3 explicitly targets past tense ("Updated", "Changed", "Removed") and requires the Evidence Format citing the actual message
- [x] PASS: Commit without a type prefix ("Updated the email template...") is flagged as a missing conventional commit type — Pass 1 step 1 requires `<type>[optional scope]: <description>`; a bare description with no prefix violates the format check
- [x] PASS: WIP commit is flagged as a Pass 5 hygiene finding — Pass 5 step 1 explicitly targets "wip" in the grep pattern and states it is acceptable in branch history but must not survive as the squash commit message
- [x] PASS: PR title "User notification improvements" is flagged for lacking a conventional commit type prefix — Pass 2 step 1 applies the same type rules from Pass 1 to PR titles
- [x] PASS: PR description missing a test plan is flagged as a Pass 2 finding — Pass 2 step 3 lists "Test plan" as a required section; missing it is an explicit finding
- [x] PASS: Output uses the defined summary template with per-pass finding counts — the Output Template defines per-pass counts for all five passes including passes with zero findings
- [~] PARTIAL: Each finding includes a concrete rewrite suggestion, not just identification — the Evidence Format mandates a "Fix: [concrete rewording or action]" field, making rewrites structurally required; however the skill does not explicitly require showing the imperative rewrite verbatim as a formatted example

### Output expectations

- [x] PASS: Output flags both past-tense commits by exact subject line with imperative-mood rewrite suggestion — Pass 1 step 3 requires checking each subject line; Evidence Format mandates the exact message as evidence and a Fix field with concrete rewording
- [x] PASS: Output flags the missing type prefix on "Updated the email template for welcome messages" and assigns a specific Conventional Commits type with reasoning — Pass 1 step 1 format check catches the missing prefix; the Fix field requires concrete rewording with a valid type assigned
- [x] PASS: Output identifies the WIP commit as a Pass 5 hygiene finding with the recommendation to rewrite or squash before merge — Pass 5 step 1 addresses this precisely including the squash-merge workflow nuance
- [x] PASS: Output flags the PR title for missing the conventional commit prefix and being too vague — Pass 2 step 1 applies type and imperative mood rules; the Fix field requires a concrete rewrite
- [x] PASS: Output flags the PR description's missing test plan as a Pass 2 finding with a concrete suggestion — Pass 2 step 3 lists the three required sections; the Fix field mandates actionable guidance
- [x] PASS: Output executes all five mandatory passes and reports per-pass finding counts including passes with zero findings — the Output Template includes all five pass counts; "Execute all five passes" is stated as mandatory
- [x] PASS: Output's findings each cite the exact subject line or PR text as evidence — the Evidence Format requires `**Evidence:** [the actual message or diff output]`, not paraphrased
- [x] PASS: Output provides concrete rewrite suggestions per finding — the Evidence Format requires `**Fix:** [concrete rewording or action]`
- [~] PARTIAL: Output's PR-description recommendation aligns with the project's PR template and points to Conventional Commits + project README convention — the skill requires "What changed", "Why", and "Test plan" sections, which partially aligns with the project template; however it does not reference the project README or PR template by name, only generic section labels

## Notes

The skill is well-specified for this scenario. Pass 1 enumerates every common past-tense form so "Updated" and "Added" are unambiguously caught. The WIP nuance in Pass 5 — acceptable in branch history, not in the final squash message — is precise and matches real-world squash-merge workflows. The mandatory Fix field in the Evidence Format means a finding-without-rewrite is not a valid output.

One subtlety: `fix: sending duplicate emails when user registers twice` has the right type prefix but "sending" is a gerund, which Pass 1 step 3 lists as a violation. The scenario presents this as a clean commit, but the skill would flag it too. Not a gap in the skill — the skill is more thorough than the test scenario credits.
