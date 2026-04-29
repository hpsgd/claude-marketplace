# Test: Write schema for pipeline configuration

Scenario: Developer invokes the write-schema skill to produce a JSON Schema and Pydantic model for a data pipeline configuration file. Pipelines have a name, a source (type + connection), optional schedule, and output settings.

## Prompt

Write a schema for pipeline configuration. Each pipeline has: a name (required, 1-255 chars), a source with type (postgres, mysql, s3, or api) and a connection string, an optional cron schedule, and output settings with format (json, csv, or parquet) and optional output path.

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
