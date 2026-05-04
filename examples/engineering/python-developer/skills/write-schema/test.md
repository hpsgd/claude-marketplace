# Test: Write schema for pipeline configuration

Scenario: Developer invokes the write-schema skill to produce a JSON Schema and Pydantic model for a data pipeline configuration file. Pipelines have a name, a source (type + connection), optional schedule, and output settings.

## Prompt

Write a schema for pipeline configuration. Each pipeline has: a name (required, 1-255 chars), a source with type (postgres, mysql, s3, or api) and a connection string, an optional cron schedule, and output settings with format (json, csv, or parquet) and optional output path.

Implementation requirements (Pydantic v2 strict):

- **Reconnaissance section** at top — show commands run: `find . -name "*.py" -path "*schema*" -o -name "models.py"`, identify validation library (assume Pydantic v2 if not stated). Report results.
- **Pydantic models** with `model_config = ConfigDict(frozen=True, strict=True)` on every domain model.
- **String enums use `StrEnum`** (Python 3.11+) — not plain string literals or `Literal[...]`:
  ```python
  from enum import StrEnum
  class SourceType(StrEnum):
      POSTGRES = "postgres"
      MYSQL = "mysql"
      S3 = "s3"
      API = "api"
  ```
- **Schema evolution guidance section** at the end naming which changes are safe (additive — new optional fields, new enum values at the end) vs breaking (removing fields, renaming, changing types, reordering enums). Cite Pydantic's `model_validator` for migration helpers.
- **Cron schedule validation**: use `croniter` to validate the cron string at parse time, not just regex.
- **Connection string**: validate format per source type (e.g. `postgres://...`, `mysql://...`, `s3://bucket/prefix`, `https://...`).

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Skill performs reconnaissance — checks for existing schemas and identifies the validation library in use before writing
- [ ] PASS: JSON Schema includes `$schema`, `$id`, and `additionalProperties: false` on every object definition
- [ ] PASS: All required fields are listed in a `required` array — not left implicit
- [ ] PASS: Every property has a `description` field
- [ ] PASS: Enum values use the JSON Schema `enum` keyword — not free-text strings
- [ ] PASS: Pydantic models use `model_config = ConfigDict(frozen=True)` for domain objects
- [ ] PASS: String enums use `StrEnum` in the Pydantic model — not plain string literals
- [ ] PARTIAL: Skill includes schema evolution guidance — identifies which changes are safe (additive) vs breaking
- [ ] PASS: Output delivers schema files, validation tests (at least 3 valid and 3 invalid inputs), and an example configuration file

## Output expectations

- [ ] PASS: Output's JSON Schema includes `$schema`, `$id`, and `additionalProperties: false` on every object definition (root, `source`, `output`)
- [ ] PASS: Output's name field has a `minLength: 1` and `maxLength: 255` constraint matching the prompt's 1-255 char range, and is in the root `required` array
- [ ] PASS: Output's `source.type` uses an `enum` of exactly `["postgres", "mysql", "s3", "api"]` — not a free-text string with documentation alone
- [ ] PASS: Output's `output.format` uses an `enum` of exactly `["json", "csv", "parquet"]`
- [ ] PASS: Output's optional fields (cron schedule, output path) are NOT in the `required` array, and the schedule field's pattern validates a cron expression (5 or 6 space-separated tokens)
- [ ] PASS: Output's Pydantic model uses `model_config = ConfigDict(frozen=True)` for the domain config and uses `StrEnum` for `SourceType` and `OutputFormat` — not plain `Literal` strings
- [ ] PASS: Output's Pydantic model has explicit type annotations on every field (`Annotated[str, Field(...)]` or equivalent), no `Any`, and the model rejects unknown extra fields (`extra='forbid'`)
- [ ] PASS: Output's validation tests include at least 3 valid configs (one per source type, plus minimal vs full) and at least 3 invalid configs (unknown source type, name too long, extra unknown field) — each with the expected pass/fail and error class
- [ ] PASS: Output includes an example configuration file (YAML or JSON) that round-trips through both the JSON Schema validator and the Pydantic model
- [ ] PARTIAL: Output's schema evolution section identifies which changes are additive (new optional field, new enum value) vs breaking (renaming a field, narrowing a type) with a specific example of each
