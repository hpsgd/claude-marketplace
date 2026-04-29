# Output: retrospective session analysis with corrections

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria (from test.md `## Criteria` section)

- [x] PASS: Step 1 locates the correct transcript file by computing the directory hash from the working path — met: Step 1 provides the full `path_to_hash()` bash function, constructs the hash-based path under `~/.claude/projects/`, scans active worktrees via `git worktree list --porcelain`, and falls back to removed-worktree breadcrumbs
- [x] PASS: Step 2 runs the analysis script and presents metrics including turns, corrections, reversals, and correction rate — met: `analyse-session.py` with `--json` flag is specified; the Output Format section defines a metrics table with Duration, Turns, Corrections, Successes, and Correction rate
- [x] PASS: The premature completion declaration is extracted as a correction event and classified as high severity — met: Step 4 assigns HIGH severity to all immediate corrections; the skill instructs extraction of every correction event from the script output and generation of an imperative rule
- [x] PASS: The wrong-path assumption (project vs global rule location) is extracted as a correction event with scope classification — met: Step 4 Rules section explicitly covers universal vs project-specific scope classification with concrete examples; scope drives which path the learned rule is written to
- [x] PASS: The API refactor success is captured as a non-obvious positive learning worth reinforcing — met: Step 4 "For successes (POSITIVE)" section specifies only non-obvious successes that represent a genuine judgment call are recorded; an explicit "good work" from the user is a canonical trigger
- [x] PASS: Path 1 (local learned rule) is written for every high-severity correction before any upstream PR is considered — met: Path 1 is defined within Step 4; Path 2 (upstream PR) is Step 6; the Rules section states "Always write a local learned rule first (Path 1)"
- [x] PASS: Learned rule files use the correct naming convention (`learned--{kebab-case-topic}.md`) and correct scope (global vs project) — met: naming convention and scope-to-location mapping (`~/.claude/rules/` vs `.claude/rules/`) are explicit, with matching examples
- [~] PARTIAL: Step 3 classifies pending signals from the signals queue and adds regex patterns for any correction phrases the existing patterns missed — partially met: Step 3 is marked mandatory and covers both signal classification and regex pattern generation with detailed pattern-writing rules; however the skill cannot demonstrate extraction of specific patterns for the scenario's correction phrases without execution

### Output expectations (from test.md `## Output expectations` section)

- [x] PASS: Output identifies BOTH correction events with verbatim or near-verbatim user quotes as evidence — met: Step 4 correction format requires "What happened" and "What was wrong" fields capturing the user's actual intent; the Output Format mandates an event list
- [x] PASS: Output classifies the premature completion declaration as HIGH severity — met: Step 4 explicitly assigns HIGH severity to immediate corrections; the "never assert without verification" rule is classified as universal in the Rules section
- [x] PASS: Output classifies the wrong-path assumption with explicit scope analysis — met: Step 4 scope guidance is explicit: universal behaviour rules go to `~/.claude/rules/`; a wrong-path-correction about where to write rules is itself a universal rule, placing it in global scope
- [x] PASS: Output captures the API refactor success as a positive learning — met: "For successes (POSITIVE)" in Step 4 directs non-obvious successes to be recorded; user explicit praise ("good work") is the exact trigger
- [x] PASS: Output writes Path 1 (local learned rule) for both high-severity corrections BEFORE any upstream PR proposal — met: structural ordering of Step 4 (Path 1) before Step 6 (Path 2) and the explicit rule "Always write a local learned rule first"
- [x] PASS: Output's learned-rule files use the convention `learned--<kebab-case-topic>.md` — met: naming convention is defined with examples including `learned--verify-before-declaring-complete.md`
- [x] PASS: Output places each learned rule in the correct scope — global rules in `~/.claude/rules/`, project rules in `.claude/rules/` — met: scope-to-location table is explicit; wrong-path-correction rule is universal so would be placed in `~/.claude/rules/`
- [x] PASS: Output presents transcript metrics — turns, corrections, reversals, correction rate — with actual counts derived from the transcript — met: Step 2 runs the analysis script which produces structured JSON; the Output Format table lists all four required metrics
- [x] PASS: Output's transcript file lookup uses the directory hash (working-path → hash) to locate the correct file in `~/.claude/projects/` — met: Step 1 bash code computes the hash and constructs the path; not assumed fixed
- [~] PARTIAL: Output classifies any pending signals from the signals queue and proposes regex patterns for correction phrases the existing patterns missed — partially met: Step 3 makes this mandatory and provides full pattern-writing rules with word-boundary guidance and three-message testing protocol; as a structural skill definition it cannot demonstrate the specific patterns the scenario would produce

## Notes

The skill is thorough and the two-path design (local rule immediately, upstream PR at threshold) is cleanly enforced in both the step ordering and the Rules section. The scope classification (universal vs project-specific) is the hardest judgment call in a retrospective skill and this definition provides concrete criteria. The PARTIAL scores reflect a structural limit of skill evaluation — the patterns Step 3 would generate for this scenario's correction phrases cannot be verified from the definition alone without execution. The definition is sound.

One observation: the trigger mapping at the top lists `latest` as running "Steps 1–4", which includes Step 3. Step 3 is also labelled mandatory within the step itself. Both are consistent, but the trigger table is the canonical entry point and the inclusion of Step 3 there matters — it closes a potential gap where an implementer might read `latest → Steps 1–4` and skip Step 3 thinking it's only for `signals` mode.
