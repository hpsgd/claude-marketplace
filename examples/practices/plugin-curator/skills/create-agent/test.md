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
