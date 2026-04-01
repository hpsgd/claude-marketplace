---
name: write-schema
description: Write a JSON Schema or Pydantic model for configuration validation or API contracts.
argument-hint: "[config type or data structure to schema]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.py"
  - "**/*.json"
  - "**/*.yaml"
---

Write a schema for $ARGUMENTS.

## JSON Schema

- `$schema` field resolved relative to the YAML file
- Cross-file `$ref` resolution via the `referencing` library
- File paths use `format: uri-reference`
- Type references use `type_reference` (built-in name or file path)
- All references explicit `{path: ...}` form — never bare strings

## Pydantic model

- Frozen models for immutable domain objects
- `strict: true` and `additionalProperties: false` for tool calling schemas
- `openai.pydantic_function_tool()` for SDK integration
- Field names: `lower_snake_case`

## Output

The schema file with validation rules, constraints, and documentation comments.
