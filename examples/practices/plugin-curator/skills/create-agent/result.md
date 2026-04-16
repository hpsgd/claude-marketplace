# Create agent new specialist agent

A contributor asks the create-agent skill to create a new `data-engineer` agent for the engineering category, covering pipeline design, data modelling, and dbt workflows.

## Prompt

> /create-agent data-engineer — responsible for data pipeline design, data modelling, dbt workflow orchestration, and data quality monitoring. Engineering category.

```markdown
[Step 1: Reading templates and conventions]
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/agent-template.md") ✓
Read(file_path="CLAUDE.md") ✓
Read(file_path=".claude-plugin/marketplace.json") ✓

[Step 2: Domain research]
Researching data engineering standards:

## Output

- Medallion architecture (Bronze/Silver/Gold) — Databricks standard for lakehouse design
- dbt — industry standard for SQL-based transformation, testing, and lineage
- Apache Airflow / Prefect — pipeline orchestration
- Great Expectations / dbt tests — data quality frameworks
- Kimball vs Inmon modelling methodologies

Adopting: Medallion architecture for storage design, dbt for transformation methodology.

[Step 3: Creating directory structure]
mkdir -p plugins/engineering/data-engineer/.claude-plugin
mkdir -p plugins/engineering/data-engineer/agents
mkdir -p plugins/engineering/data-engineer/skills
mkdir -p plugins/engineering/data-engineer/templates

[Step 4: Writing plugin.json] ✓

[Step 5: Writing agent definition]
plugins/engineering/data-engineer/agents/data-engineer.md ✓ (218 lines)
Sections: Core statement, Non-negotiable, Pre-Flight, Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration, Principles, What You Don't Do

[Steps 6–9: Registry updates]
marketplace.json: added data-engineer entry ✓
Coordinator RATSI: added to "data pipeline" and "analytics" rows ✓
CTO agent team listing: added data-engineer ✓
README: category install block ✓, everything block ✓, agent table ✓

[Step 10: Verification]
JSON valid: plugin.json ✓, marketplace.json ✓
Dirs: 24 | Registry: 24 → match ✓
grep private refs: 0 matches ✓

### Created: data-engineer

#### Files Created
- `plugins/engineering/data-engineer/.claude-plugin/plugin.json`
- `plugins/engineering/data-engineer/agents/data-engineer.md`
- `plugins/engineering/data-engineer/skills/`
- `plugins/engineering/data-engineer/templates/`

#### Registry Updates
- marketplace.json: ✅ added
- README: ✅ install commands + agent table
- Coordinator RATSI: ✅ data-pipeline and analytics rows
- Lead (cto): ✅ team listing updated

#### Quality Score
- **Lines:** 218
- **Agent audit score:** 14/15
- **Model:** sonnet

#### Verification
- JSON valid: ✅
- Plugin count matches: ✅
- No private refs: ✅
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (93.75%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Step 1 reads agent template, CLAUDE.md, and marketplace.json — Step 1 provides three explicit `Read()` calls in sequence: `agent-template.md`, `CLAUDE.md`, and `.claude-plugin/marketplace.json`. The step is labelled "sequential — do not skip steps" and is the first action before any writing.
- [x] PASS: Step 2 performs domain research before writing — Step 2 "Research best practices" states "Before writing anything, research the established standards and frameworks for this agent's domain." It enumerates three sub-steps: identify authoritative sources, document which standards are being adopted and why, and plan domain-specific templates. The Anti-Patterns section names "Creating without researching" as a failure mode.
- [x] PASS: All required directory structure created — Step 3 includes four explicit `mkdir -p` commands: `.claude-plugin`, `agents`, `skills`, and `templates` (with the note "if agent produces artefacts"). All four are present.
- [x] PASS: Agent definition follows all mandatory sections — Step 5's body sections table lists all 10 sections as mandatory: Core statement, Non-negotiable, Pre-Flight, Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration, Principles, What You Don't Do. Each row includes a "Key requirements" column. The skill states "Follow the agent template EXACTLY. Every section is mandatory."
- [x] PASS: Agent uses sonnet — Step 5 frontmatter section shows `model: {sonnet for specialists, opus for leadership}`. The Anti-Patterns section explicitly calls out "Forgetting model assignment" as a failure mode. data-engineer is a specialist; sonnet is the correct assignment.
- [x] PASS: marketplace.json updated with required fields — Step 6 defines the JSON entry format with all required fields explicit: name, source, description, version, category, and tags.
- [x] PASS: All registry updates completed — Steps 6–9 cover exactly the four targets in the criterion: marketplace.json (Step 6), coordinator RATSI (Step 7), relevant lead team listing (Step 8), README at 3 places (Step 9 — "Category install block", "Everything install block", "Agent table"). All targets accounted for.
- [~] PARTIAL: Verification confirms JSON valid, count match, no private refs — Step 10 provides bash commands for all three checks. The private-references grep uses `--include="*.md"` and would not catch a private reference introduced into a `.json` file. The plugin.json template in Step 4 uses `[author or organisation name]` as a generic placeholder, so the risk is lower than it was previously, but the grep scope remains narrower than ideal. PARTIAL ceiling applies per criterion prefix.

## Notes

No changes to this skill since previous evaluation. Verdict unchanged at PASS (93.75%). The one persistent gap is the private-refs grep covering only `.md` files: a contributor who manually introduces a private reference into `plugin.json` would pass verification. This is noted but does not affect the verdict given the PARTIAL ceiling.
