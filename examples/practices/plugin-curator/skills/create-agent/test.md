# Test: create-agent new specialist agent

Scenario: A contributor asks the create-agent skill to create a new `data-engineer` agent for the engineering category, covering pipeline design, data modelling, and dbt workflows.

## Prompt

/create-agent data-engineer — responsible for data pipeline design, data modelling, dbt workflow orchestration, and data quality monitoring. Engineering category.

## Criteria

- [ ] PASS: Step 1 reads the agent template, CLAUDE.md, and marketplace.json before creating anything
- [ ] PASS: Step 2 performs domain research before writing — identifies established data engineering frameworks or methodologies being adopted (e.g., Medallion architecture, dbt best practices)
- [ ] PASS: All required directory structure is created: `.claude-plugin/`, `agents/`, `skills/`, and `templates/` if applicable
- [ ] PASS: Agent definition follows all mandatory sections: Core statement, Non-negotiable, Pre-Flight, Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration, Principles, What You Don't Do
- [ ] PASS: Agent uses `sonnet` model — data-engineer is a specialist, not leadership
- [ ] PASS: marketplace.json is updated with the new plugin entry including source path, description, version, category, and tags
- [ ] PASS: All registry updates are completed — marketplace.json, README (3 places), coordinator RATSI, and relevant lead team listing
- [ ] PARTIAL: Verification step confirms JSON is valid, plugin count matches registry count, and no private references exist in the new files

## Output expectations

- [ ] PASS: Output creates the directory structure under `plugins/engineering/data-engineer/` (engineering category from the prompt) with `.claude-plugin/plugin.json`, `agents/data-engineer.md`, `skills/`, and `templates/` — exact paths matching the project's nested category layout
- [ ] PASS: Output's `plugin.json` contains the required metadata — name, description, version, source — and is valid JSON, not pseudo-JSON
- [ ] PASS: Output's `agents/data-engineer.md` contains all mandatory sections: Core statement, Non-negotiable, Pre-Flight (with Step 1 reading CLAUDE.md), Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration, Principles, What You Don't Do
- [ ] PASS: Output sets the model to `sonnet` (specialist agent), not `opus`, in the agent frontmatter
- [ ] PASS: Output's domain methodology references established frameworks — Medallion architecture (bronze/silver/gold), dbt best practices, data contracts, lineage patterns — not invented terminology
- [ ] PASS: Output updates `marketplace.json` with the new plugin entry — name, source path (`./plugins/engineering/data-engineer`), description, version, category (`engineering`), tags
- [ ] PASS: Output updates the README.md (in three places per the prompt — main listing, category listing, and skill cross-reference if applicable) to register the new agent
- [ ] PASS: Output updates the coordinator's RATSI table (or equivalent dispatch reference) to include the data-engineer agent's responsibilities
- [ ] PASS: Output's verification step shows command output confirming JSON validity (`jq . marketplace.json`), the plugin count matches registry count, and no private references exist in the new files
- [ ] PARTIAL: Output's data-engineer agent definition includes specific data engineering decision checkpoints (e.g. "before introducing a new data warehouse vendor", "before changing partitioning strategy on a high-volume table") rather than generic checkpoints copied from another agent
