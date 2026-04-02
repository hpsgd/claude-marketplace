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

## Process (sequential — do not skip steps)

### Step 1: Reconnaissance

Before writing any schema:

1. **Identify the schema purpose:**
   - Configuration validation (YAML/JSON config files)
   - API contract (request/response shapes)
   - Tool calling (LLM function schemas)
   - Data interchange (between services)
   - Domain model (internal data structures)

2. **Check existing schemas:**
   ```bash
   find . -name "*.schema.json" -o -name "*.schema.yaml" | head -20
   grep -rn "class.*BaseModel\|class.*BaseSettings" --include="*.py" | head -20
   grep -rn "\$schema\|\$ref" --include="*.json" --include="*.yaml" | head -10
   ```

3. **Identify the validation library:**
   - JSON Schema with `jsonschema` or `referencing`
   - Pydantic v2 with `model_validate`
   - Both (Pydantic generates JSON Schema via `model_json_schema()`)

### Step 2: JSON Schema Design

#### Structure

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/my-config.schema.json",
  "title": "MyConfig",
  "description": "Configuration for the data pipeline.",
  "type": "object",
  "required": ["name", "source"],
  "additionalProperties": false,
  "properties": {
    "name": {
      "type": "string",
      "description": "Human-readable name for this configuration.",
      "minLength": 1,
      "maxLength": 255
    },
    "source": {
      "$ref": "#/$defs/DataSource"
    },
    "schedule": {
      "type": "string",
      "description": "Cron expression for scheduled execution.",
      "pattern": "^(@(annually|yearly|monthly|weekly|daily|hourly))|((\\*|[0-9,\\-\\/]+)\\s+){4}(\\*|[0-9,\\-\\/]+)$",
      "examples": ["0 */6 * * *", "@daily"]
    },
    "output": {
      "$ref": "#/$defs/OutputConfig",
      "default": { "format": "json", "compress": false }
    }
  },
  "$defs": {
    "DataSource": {
      "type": "object",
      "required": ["type", "connection"],
      "additionalProperties": false,
      "properties": {
        "type": {
          "type": "string",
          "enum": ["postgres", "mysql", "s3", "api"],
          "description": "The type of data source."
        },
        "connection": {
          "type": "string",
          "description": "Connection string or URL.",
          "format": "uri"
        }
      }
    },
    "OutputConfig": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "format": {
          "type": "string",
          "enum": ["json", "csv", "parquet"],
          "default": "json"
        },
        "compress": {
          "type": "boolean",
          "default": false
        },
        "path": {
          "type": "string",
          "format": "uri-reference",
          "description": "Output path relative to the config file."
        }
      }
    }
  }
}
```

#### JSON Schema Rules (MANDATORY)

| Rule | Rationale |
|---|---|
| `$schema` field on every root schema | Enables IDE validation and version clarity |
| `$id` field on every root schema | Enables cross-file `$ref` resolution |
| `additionalProperties: false` | Catches typos and prevents unexpected fields |
| `required` array for mandatory fields | Explicit about what must be provided |
| `description` on every property | Self-documenting schema |
| `examples` for complex formats | Helps consumers understand expected values |
| `format` for semantic types | `uri`, `uri-reference`, `date-time`, `email`, `uuid` |
| `enum` for fixed value sets | Prevents invalid values, enables IDE autocomplete |
| `default` for optional fields with sensible defaults | Documents the implicit behaviour |
| `$defs` for reusable types | Avoids duplication, enables `$ref` composition |

#### Cross-File References

```json
{
  "$ref": "./common/data-source.schema.json",
  "description": "The data source configuration."
}
```

**Resolution rules:**
- `$ref` paths are relative to the referencing file
- Use the `referencing` library for programmatic resolution
- All references use explicit `{"$ref": "path"}` form — never bare strings
- File paths use `format: uri-reference` — not `format: uri` (relative, not absolute)

#### Type References

For schemas that reference types by name or file path:

```json
{
  "type_reference": {
    "oneOf": [
      {
        "type": "string",
        "description": "Built-in type name",
        "enum": ["string", "integer", "boolean", "float", "datetime"]
      },
      {
        "type": "object",
        "required": ["path"],
        "properties": {
          "path": {
            "type": "string",
            "format": "uri-reference",
            "description": "Path to a schema file defining the type."
          }
        },
        "additionalProperties": false
      }
    ]
  }
}
```

**Rule:** Type references always use explicit `{"path": "..."}` form — never bare strings that could be ambiguous between a type name and a file path.

### Step 3: Pydantic Model Design

```python
from datetime import datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class SourceType(StrEnum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    S3 = "s3"
    API = "api"


class OutputFormat(StrEnum):
    JSON = "json"
    CSV = "csv"
    PARQUET = "parquet"


class DataSource(BaseModel):
    """Configuration for a data source connection."""

    model_config = ConfigDict(frozen=True)

    type: SourceType = Field(description="The type of data source.")
    connection: str = Field(
        description="Connection string or URL.",
        min_length=1,
        examples=["postgresql://user:pass@host:5432/db"],
    )


class OutputConfig(BaseModel):
    """Configuration for pipeline output."""

    model_config = ConfigDict(frozen=True)

    format: OutputFormat = Field(default=OutputFormat.JSON)
    compress: bool = Field(default=False)
    path: str | None = Field(
        default=None,
        description="Output path relative to the config file.",
    )


class PipelineConfig(BaseModel):
    """Root configuration for a data pipeline."""

    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
    )

    name: str = Field(
        description="Human-readable name for this configuration.",
        min_length=1,
        max_length=255,
    )
    source: DataSource
    schedule: str | None = Field(
        default=None,
        description="Cron expression for scheduled execution.",
        pattern=r"^(@(annually|yearly|monthly|weekly|daily|hourly))"
                r"|((\\*|[0-9,\-\/]+)\s+){4}(\\*|[0-9,\-\/]+)$",
        examples=["0 */6 * * *", "@daily"],
    )
    output: OutputConfig = Field(default_factory=OutputConfig)
```

#### Pydantic Rules (MANDATORY)

| Rule | Implementation |
|---|---|
| Frozen models for domain objects | `model_config = ConfigDict(frozen=True)` |
| `StrEnum` for string enums | Enables serialisation as string, not as name |
| `Field()` with description | Self-documenting, generates good JSON Schema |
| `min_length`/`max_length` for strings | Prevents empty strings and oversized inputs |
| Type annotations, not validation decorators | `str \| None` not `Optional[str]` with validator |
| `default_factory` for mutable defaults | Never `default=[]` or `default={}` |
| Strip whitespace | `str_strip_whitespace=True` in ConfigDict |
| Explicit `None` vs missing | Use `None` for optional with no default, `Field(default=X)` for optional with default |

#### Pydantic for Tool Calling / LLM Function Schemas

```python
from pydantic import BaseModel, Field, ConfigDict


class SearchParameters(BaseModel):
    """Parameters for the search tool."""

    model_config = ConfigDict(
        json_schema_extra={
            "strict": True,
            "additionalProperties": False,
        }
    )

    query: str = Field(description="The search query string.")
    max_results: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results to return.",
    )
    include_archived: bool = Field(
        default=False,
        description="Whether to include archived items in results.",
    )


# Generate JSON Schema for tool calling
schema = SearchParameters.model_json_schema()

# For OpenAI SDK integration
from openai.lib._pydantic import to_strict_json_schema
strict_schema = to_strict_json_schema(SearchParameters)
```

**Tool calling rules:**
- `strict: true` — no coercion, exact types required
- `additionalProperties: false` — reject unexpected fields
- Every field has a `description` — the LLM uses this to understand the parameter
- Default values are explicit — the LLM can see what happens if a parameter is omitted
- Use `ge`/`le`/`gt`/`lt` for numeric bounds — prevents nonsensical values
- `StrEnum` for categorical parameters — constrains the LLM's output

### Step 4: Validation Patterns

#### Custom Validators (Pydantic)

```python
from pydantic import model_validator, field_validator


class DateRangeConfig(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode='after')
    def validate_date_range(self) -> 'DateRangeConfig':
        if self.end_date < self.start_date:
            raise ValueError(
                f"end_date ({self.end_date}) must be after start_date ({self.start_date})"
            )
        return self


class ConnectionConfig(BaseModel):
    host: str
    port: int = Field(ge=1, le=65535)

    @field_validator('host')
    @classmethod
    def validate_host(cls, v: str) -> str:
        if v.startswith('http'):
            raise ValueError("host should not include protocol scheme (http/https)")
        return v.lower()
```

#### JSON Schema Conditional Validation

```json
{
  "if": {
    "properties": { "type": { "const": "s3" } }
  },
  "then": {
    "required": ["bucket", "region"],
    "properties": {
      "bucket": { "type": "string" },
      "region": { "type": "string", "enum": ["us-east-1", "eu-west-1"] }
    }
  }
}
```

### Step 5: Schema Evolution

Design schemas for forward compatibility:

| Change type | Safe? | Strategy |
|---|---|---|
| Add optional field with default | YES | Additive — old data still valid |
| Add required field | NO | Migration needed. Add as optional first, then require in next version |
| Remove field | NO | Deprecate first, remove in next version |
| Change field type | NO | New field with new type, deprecate old |
| Add enum value | YES | Additive — old consumers ignore unknown values |
| Remove enum value | NO | Migration needed |
| Rename field | NO | Add new field, deprecate old, migrate |

**Rules:**
- Schema versions are explicit (in `$id` or Pydantic model name)
- Breaking changes require a migration path documented in the schema or changelog
- `additionalProperties: false` means consumers must update to accept new fields (intentional strictness)

## Anti-Patterns (NEVER do these)

- **No `additionalProperties: false`** — typos silently accepted, no error feedback
- **`Any` or `object` types** — defeats the purpose of a schema. Be specific
- **Mutable Pydantic models** — use `frozen=True`. Schemas define data shapes, not mutable state
- **Bare string references** — `"source": "postgres"` could be a type name or a file path. Use explicit form
- **Missing descriptions** — a schema without descriptions is documentation without words
- **Inline validation logic** — complex validation belongs in validators, not in the schema definition
- **Schema without tests** — validate that good inputs pass and bad inputs fail. Test the schema itself

## Output

Deliver:
1. Schema file(s) — JSON Schema (`.schema.json`) or Pydantic models (`.py`)
2. Validation tests — at least 3 valid inputs, 3 invalid inputs
3. Example configuration file showing valid usage
4. Migration notes if replacing or evolving an existing schema
