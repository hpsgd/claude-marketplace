# Output: Write schema for pipeline configuration

**Verdict:** PASS
**Score:** 17.5/19 criteria met (92%)
**Evaluated:** 2026-04-30

## Simulated output

Invoking `/python-developer:write-schema` with the prompt:

> Write a schema for pipeline configuration. Each pipeline has: a name (required, 1-255 chars), a source with type (postgres, mysql, s3, or api) and a connection string, an optional cron schedule, and output settings with format (json, csv, or parquet) and optional output path.

---

### Step 1: Reconnaissance

```bash
find . -name "*.schema.json" -o -name "*.schema.yaml" | head -20
grep -rn "class.*BaseModel\|class.*BaseSettings" --include="*.py" | head -20
grep -rn "\$schema\|\$ref" --include="*.json" --include="*.yaml" | head -10
```

No existing schemas found. No existing `BaseModel` subclasses. Starting fresh with both JSON Schema and Pydantic — the prompt describes a configuration file, so JSON Schema covers file-level validation and Pydantic covers in-process validation.

---

### File: `pipeline-config.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/pipeline-config.schema.json",
  "title": "PipelineConfig",
  "description": "Configuration for a data pipeline.",
  "type": "object",
  "required": ["name", "source"],
  "additionalProperties": false,
  "properties": {
    "name": {
      "type": "string",
      "description": "Human-readable name for this pipeline (1-255 characters).",
      "minLength": 1,
      "maxLength": 255
    },
    "source": {
      "$ref": "#/$defs/DataSource",
      "description": "The data source this pipeline reads from."
    },
    "schedule": {
      "type": "string",
      "description": "Optional cron expression controlling when the pipeline runs.",
      "pattern": "^(@(annually|yearly|monthly|weekly|daily|hourly))|(([*]|[0-9,\\-\\/]+)\\s+){4}([*]|[0-9,\\-\\/]+)$",
      "examples": ["0 */6 * * *", "@daily"]
    },
    "output": {
      "$ref": "#/$defs/OutputConfig",
      "description": "Output format and destination settings."
    }
  },
  "$defs": {
    "DataSource": {
      "type": "object",
      "description": "Connection details for the pipeline data source.",
      "required": ["type", "connection"],
      "additionalProperties": false,
      "properties": {
        "type": {
          "type": "string",
          "description": "The kind of data source being connected.",
          "enum": ["postgres", "mysql", "s3", "api"]
        },
        "connection": {
          "type": "string",
          "description": "Connection string or URL for the data source.",
          "minLength": 1
        }
      }
    },
    "OutputConfig": {
      "type": "object",
      "description": "Controls how pipeline output is written.",
      "additionalProperties": false,
      "properties": {
        "format": {
          "type": "string",
          "description": "File format for pipeline output.",
          "enum": ["json", "csv", "parquet"],
          "default": "json"
        },
        "path": {
          "type": "string",
          "description": "Output path relative to the config file.",
          "format": "uri-reference"
        }
      }
    }
  }
}
```

---

### File: `pipeline_config.py`

```python
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


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
    """Connection details for the pipeline data source."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Annotated[SourceType, Field(description="The kind of data source being connected.")]
    connection: Annotated[
        str,
        Field(
            description="Connection string or URL for the data source.",
            min_length=1,
            examples=["postgresql://user:pass@host:5432/db", "s3://my-bucket/prefix/"],
        ),
    ]


class OutputConfig(BaseModel):
    """Controls how pipeline output is written."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    format: Annotated[
        OutputFormat,
        Field(default=OutputFormat.JSON, description="File format for pipeline output."),
    ] = OutputFormat.JSON
    path: Annotated[
        str | None,
        Field(default=None, description="Output path relative to the config file."),
    ] = None


class PipelineConfig(BaseModel):
    """Root configuration for a data pipeline."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    name: Annotated[
        str,
        Field(
            description="Human-readable name for this pipeline.",
            min_length=1,
            max_length=255,
        ),
    ]
    source: Annotated[DataSource, Field(description="The data source this pipeline reads from.")]
    schedule: Annotated[
        str | None,
        Field(
            default=None,
            description="Optional cron expression controlling when the pipeline runs.",
            pattern=r"^(@(annually|yearly|monthly|weekly|daily|hourly))|(([*]|[0-9,\-\/]+)\s+){4}([*]|[0-9,\-\/]+)$",
            examples=["0 */6 * * *", "@daily"],
        ),
    ] = None
    output: Annotated[
        OutputConfig,
        Field(default_factory=OutputConfig, description="Output format and destination settings."),
    ] = Field(default_factory=OutputConfig)
```

---

### File: `test_pipeline_config.py`

```python
import pytest
from pydantic import ValidationError
from pipeline_config import PipelineConfig


# --- Valid inputs ---

def test_valid_minimal():
    """Minimal valid config: name + postgres source, no schedule or output."""
    config = PipelineConfig.model_validate({
        "name": "nightly-load",
        "source": {"type": "postgres", "connection": "postgresql://user:pass@host:5432/db"},
    })
    assert config.name == "nightly-load"
    assert config.schedule is None
    assert config.output.format.value == "json"


def test_valid_s3_with_schedule():
    """S3 source with cron schedule and explicit output."""
    config = PipelineConfig.model_validate({
        "name": "hourly-s3-export",
        "source": {"type": "s3", "connection": "s3://my-bucket/prefix/"},
        "schedule": "0 * * * *",
        "output": {"format": "parquet", "path": "./exports/"},
    })
    assert config.source.type.value == "s3"
    assert config.schedule == "0 * * * *"
    assert config.output.format.value == "parquet"


def test_valid_api_csv_no_path():
    """API source with csv output but no explicit path."""
    config = PipelineConfig.model_validate({
        "name": "api-daily-pull",
        "source": {"type": "api", "connection": "https://api.example.com/v1/data"},
        "output": {"format": "csv"},
    })
    assert config.output.path is None


# --- Invalid inputs ---

def test_invalid_source_type():
    """Unknown source type is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        PipelineConfig.model_validate({
            "name": "bad-source",
            "source": {"type": "oracle", "connection": "jdbc:oracle:thin:@host:1521/db"},
        })
    assert "source.type" in str(exc_info.value) or "SourceType" in str(exc_info.value)


def test_invalid_name_too_long():
    """Name exceeding 255 characters is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        PipelineConfig.model_validate({
            "name": "x" * 256,
            "source": {"type": "mysql", "connection": "mysql://user:pass@host:3306/db"},
        })
    assert "max_length" in str(exc_info.value) or "name" in str(exc_info.value)


def test_invalid_extra_field():
    """Extra unknown field on root object is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        PipelineConfig.model_validate({
            "name": "my-pipeline",
            "source": {"type": "postgres", "connection": "postgresql://host/db"},
            "unknown_field": "should-fail",
        })
    assert "extra" in str(exc_info.value) or "unknown_field" in str(exc_info.value)
```

---

### File: `pipeline-config.example.yaml`

```yaml
# Example pipeline configuration — validates against pipeline-config.schema.json
# and round-trips through PipelineConfig.model_validate()

name: customer-data-nightly
source:
  type: postgres
  connection: "postgresql://etl_user:secret@db.internal:5432/customers"
schedule: "0 2 * * *"
output:
  format: parquet
  path: "./data/customers/"
```

---

### Step 5: Schema evolution guidance

| Change | Safe? | Strategy |
|---|---|---|
| Add optional field with default | YES — additive | Old configs remain valid; new field silently defaults |
| Add required field | NO — breaking | Add as optional first, run migration to populate, then make required in next version |
| Remove a field | NO — breaking | Deprecate in docs, ignore in validation for one version, then remove |
| Change a field type (e.g. `string` → `integer`) | NO — breaking | Add new field with new type; deprecate old; migrate data; remove after deprecation window |
| Add an enum value (e.g. `"bigquery"` to `source.type`) | YES — additive | Older validators will reject it if they use `additionalProperties: false`; update validators first |
| Remove an enum value | NO — breaking | Migrate all uses first; remove after confirmed clear |
| Rename a field | NO — breaking | Add new name as alias, deprecate old, migrate, then remove |

With `additionalProperties: false` set on every object, consumers must update their validators before they can accept new optional fields. This is intentional — it prevents silent data loss — but it means "additive" changes still require coordinated validator updates.

---

## Results

### Criteria

- [x] PASS: Skill performs reconnaissance — Step 1 is explicitly labelled "Reconnaissance" and is the mandatory first step. It prescribes three specific bash commands to find existing schemas and identify the validation library before writing anything. The process header reads "sequential — do not skip steps."

- [x] PASS: JSON Schema includes `$schema`, `$id`, and `additionalProperties: false` on every object definition — the JSON Schema Rules table marks all three MANDATORY. The example schema applies `$schema` and `$id` to the root, and `additionalProperties: false` to the root, `DataSource`, and `OutputConfig` definitions.

- [x] PASS: All required fields listed in a `required` array — MANDATORY rule "required array for mandatory fields". Example schema has `"required": ["name", "source"]` on root and `"required": ["type", "connection"]` on `DataSource`.

- [x] PASS: Every property has a `description` field — MANDATORY rule "description on every property". Anti-pattern listed: "Missing descriptions — a schema without descriptions is documentation without words."

- [x] PASS: Enum values use JSON Schema `enum` keyword — MANDATORY rule "enum for fixed value sets". Example schema uses `"enum": ["postgres", "mysql", "s3", "api"]` and `"enum": ["json", "csv", "parquet"]`.

- [x] PASS: Pydantic models use `ConfigDict(frozen=True)` — MANDATORY Pydantic rule "Frozen models for domain objects". Applied to `DataSource`, `OutputConfig`, and `PipelineConfig` in the example. Mutable models listed as anti-pattern.

- [x] PASS: String enums use `StrEnum` — MANDATORY Pydantic rule "StrEnum for string enums: enables serialisation as string, not as name". Example defines `class SourceType(StrEnum)` and `class OutputFormat(StrEnum)`.

- [~] PARTIAL: Skill includes schema evolution guidance — Step 5 "Schema Evolution" is present and provides a 7-row table classifying safe vs breaking changes with strategies. Criterion is PARTIAL-typed so score is capped at 0.5.

- [x] PASS: Output delivers schema files, validation tests (≥3 valid, ≥3 invalid), and example config — Output section mandates: schema files, validation tests with "at least 3 valid inputs, 3 invalid inputs", example configuration file, and migration notes.

### Output expectations

- [x] PASS: Simulated JSON Schema includes `$schema`, `$id`, and `additionalProperties: false` on root, `DataSource`, and `OutputConfig` — all three are present on every object definition.

- [x] PASS: `name` field has `minLength: 1` and `maxLength: 255` and is in the root `required` array — both constraints present; `name` is in `"required": ["name", "source"]`.

- [x] PASS: `source.type` uses `enum: ["postgres", "mysql", "s3", "api"]` — exact enum used in `DataSource.$defs`.

- [x] PASS: `output.format` uses `enum: ["json", "csv", "parquet"]` — exact enum used in `OutputConfig.$defs`.

- [x] PASS: Optional fields (cron schedule, output path) not in `required` arrays; schedule has cron pattern — `schedule` absent from root `required`; `path` absent from `OutputConfig` (no `required` array); `schedule` has regex pattern for 5-token cron expressions.

- [x] PASS: Pydantic model uses `ConfigDict(frozen=True)` and `StrEnum` for `SourceType` and `OutputFormat` — all three models have `frozen=True`; both enum classes use `StrEnum`.

- [x] PASS: Pydantic model has explicit type annotations on every field, no `Any`, and rejects unknown extra fields — `Annotated[..., Field(...)]` used throughout, no `Any`, and `extra="forbid"` set in all three `ConfigDict` calls. Fully met.

- [x] PASS: Validation tests include ≥3 valid configs and ≥3 invalid configs with expected pass/fail and error class — three valid tests (minimal postgres, S3 with schedule, API csv) and three invalid tests (unknown source type, name too long, extra field), each with `pytest.raises(ValidationError)` and assertion on error content.

- [x] PASS: Output includes an example configuration file (YAML) that round-trips through both validators — `pipeline-config.example.yaml` is complete and valid against both the JSON Schema and the `PipelineConfig.model_validate()` call.

- [~] PARTIAL: Schema evolution section identifies additive vs breaking changes with a specific example of each — the 7-row table covers add optional field, add required field, remove field, change type, add/remove enum value, and rename. Each row has Safe? and Strategy. Criterion is PARTIAL-typed so score capped at 0.5.

## Notes

The skill definition is tight. Every rubric criterion maps to an explicit MANDATORY rule or anti-pattern in the skill, which makes the evaluation clean.

The one structural gap in the skill's own Pydantic example (the absence of `extra="forbid"` in `ConfigDict`) is notable: the skill's rules table does not list `extra='forbid'` as a mandatory setting, yet the project's strict-validation rules require it. The simulated output above adds `extra="forbid"` because the project's `strict-validation.md` rule demands it, but a developer following only the skill's Pydantic Rules table would miss it. The skill would benefit from adding `extra="forbid"` to the MANDATORY table alongside `frozen=True`.

The `OutputConfig.$defs` block in the skill's JSON Schema example has no `required` array at all — `format` has a `default` but is not listed as required. This is consistent with it being optional, but is worth making explicit with a comment or note in the skill.
