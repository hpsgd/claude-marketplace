# Output: create-agent new specialist agent

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16.5/17.5 criteria met (94%) |
| **Evaluated** | 2026-04-29 |
| **Source** | `plugins/practices/plugin-curator/skills/create-agent/SKILL.md` |

## Results

### Criteria

- [x] PASS: Step 1 reads the agent template, CLAUDE.md, and marketplace.json before creating anything — Step 1 explicitly calls `Read` on all three in that order before any writes
- [x] PASS: Step 2 performs domain research before writing — Step 2 mandates identifying authoritative sources and documenting which standards are adopted; anti-pattern "Creating without researching" explicitly prohibits invented methodologies
- [x] PASS: All required directory structure is created: `.claude-plugin/`, `agents/`, `skills/`, and `templates/` if applicable — Step 3 creates all four via `mkdir -p`
- [x] PASS: Agent definition follows all mandatory sections: Core statement, Non-negotiable, Pre-Flight, Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration, Principles, What You Don't Do — Step 5 body-sections table lists all ten as mandatory with "Follow the agent template EXACTLY. Every section is mandatory."
- [x] PASS: Agent uses `sonnet` model — data-engineer is a specialist, not leadership — Step 5 frontmatter spec states "sonnet for specialists, opus for leadership"; anti-patterns section reinforces this explicitly
- [x] PASS: marketplace.json is updated with the new plugin entry including source path, description, version, category, and tags — Step 6 JSON template includes all five fields
- [x] PASS: All registry updates are completed — marketplace.json, README (3 places), coordinator RATSI, and relevant lead team listing — Steps 6–9 cover all four targets
- [~] PARTIAL: Verification step confirms JSON is valid, plugin count matches registry count, and no private references exist — Step 10 covers all three checks (Python JSON validation, find/python3 plugin count, grep for private refs); awarded 0.5 per PARTIAL type

### Output expectations

- [x] PASS: Output creates the directory structure under `plugins/engineering/data-engineer/` with `.claude-plugin/plugin.json`, `agents/data-engineer.md`, `skills/`, and `templates/` — Step 3 category table routes engineering agents correctly; `mkdir -p` pattern matches the expected paths
- [x] PASS: Output's `plugin.json` contains required metadata — name, description, version, source — and is valid JSON — Step 4 template includes all fields; Step 10 validates JSON
- [x] PASS: Output's `agents/data-engineer.md` contains all mandatory sections: Core statement through What You Don't Do — Step 5 mandates all ten sections
- [x] PASS: Output sets the model to `sonnet` in agent frontmatter — frontmatter spec and anti-patterns section both enforce this for specialists
- [x] PASS: Output's domain methodology references established frameworks — Step 2 requires identifying authoritative sources and existing standards, not invented terminology; "adopt existing standards, don't invent" is the stated principle
- [x] PASS: Output updates `marketplace.json` with the new plugin entry — Step 6 template covers name, source, description, version, category, tags
- [x] PASS: Output updates README.md in three places — Step 9 names all three explicitly: category install block, everything install block, agent table
- [x] PASS: Output updates the coordinator's RATSI table — Step 7 explicitly covers RATSI matrix updates with R/A/T/S/I role determination
- [x] PASS: Output's verification step shows command output confirming JSON validity, plugin count match, and no private references — Step 10 covers all three checks
- [~] PARTIAL: Output's data-engineer agent definition includes specific data engineering decision checkpoints — the skill mandates decision checkpoints (Step 5, audit checklist) and domain-specificity as a quality target, but does not require domain-specific checkpoint examples in the template or enforce it in the audit criteria; a contributor following the skill could produce generic checkpoints without violating any stated rule

## Notes

The skill is structurally strong. The ten-step sequential process, mandatory section enforcement, model assignment rules, and registry chain are all clearly specified.

Two gaps worth flagging beyond the rubric:

The `source` field example in Step 6 (`{category}/{agent-name}`) omits the `./plugins/` prefix shown in `CLAUDE.md` and the actual marketplace.json entries. A contributor following the template literally would produce a broken source path.

The private-refs grep in Step 10 uses `--include="*.md"`, so a private reference introduced into `plugin.json` would go undetected. Low risk given the template uses placeholders, but the scope could be widened to `--include="*.{md,json}"`.
