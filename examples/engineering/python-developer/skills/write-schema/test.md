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
