# Write schema for pipeline configuration

Developer invokes the write-schema skill to produce a JSON Schema and Pydantic model for a data pipeline configuration file. Pipelines have a name, a source (type + connection), optional schedule, and output settings.

## Prompt

> Write a schema for pipeline configuration. Each pipeline has: a name (required, 1-255 chars), a source with type (postgres, mysql, s3, or api) and a connection string, an optional cron schedule, and output settings with format (json, csv, or parquet) and optional output path.

```
Step 1 — Reconnaissance

$ find . -name "*.schema.json" -o -name "*.schema.yaml" | head -20
schemata/cost-evaluation.schema.json
schemata/organism.schema.json

$ grep -rn "class.*BaseModel\|class.*BaseSettings" --include="*.py" | head -20
src/config/models.py:class OrganismConfig(BaseModel):
src/config/models.py:class CostConfig(BaseModel):

$ grep -rn "\$schema\|\$ref" --include="*.json" --include="*.yaml" | head -10
schemata/cost-evaluation.schema.json:"$schema": "https://json-schema.org/draft/2020-12/schema"
schemata/cost-evaluation.schema.json:"$id": "https://example.com/schemata/cost-evaluation.schema.json"

Schema purpose: configuration validation (YAML/JSON config files).
Validation library: Pydantic v2 (BaseModel found), plus jsonschema for file validation.
Existing pattern: draft/2020-12, kebab-case filenames, additionalProperties: false throughout.
No existing pipeline schema — writing from scratch.
```

---

## Output

**schemata/pipeline-config.schema.json**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemata/pipeline-config.schema.json",
  "title": "PipelineConfig",
  "description": "Configuration for a data pipeline — defines source, schedule, and output settings.",
  "type": "object",
  "required": ["name", "source"],
  "additionalProperties": false,
  "properties": {
    "name": {
      "type": "string",
      "description": "Human-readable name for this pipeline. Used in logs and monitoring dashboards.",
      "minLength": 1,
      "maxLength": 255
    },
    "source": {
      "$ref": "#/$defs/DataSource"
    },
    "schedule": {
      "type": "string",
      "description": "Cron expression controlling when the pipeline runs. Omit for manually triggered pipelines.",
      "pattern": "^(@(annually|yearly|monthly|weekly|daily|hourly|reboot))|((\\*|[0-9,\\-\\/]+)\\s+){4}(\\*|[0-9,\\-\\/]+)$",
      "examples": ["0 */6 * * *", "@daily", "30 2 * * 1-5"]
    },
    "output": {
      "$ref": "#/$defs/OutputConfig"
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
          "description": "The category of data source, which determines how the connection string is interpreted.",
          "enum": ["postgres", "mysql", "s3", "api"]
        },
        "connection": {
          "type": "string",
          "description": "Connection string or URL for the data source. Format depends on type (e.g. postgresql://user:pass@host/db for postgres, s3://bucket/prefix for s3).",
          "minLength": 1
        }
      }
    },
    "OutputConfig": {
      "type": "object",
      "description": "Settings controlling how and where pipeline output is written.",
      "required": ["format"],
      "additionalProperties": false,
      "properties": {
        "format": {
          "type": "string",
          "description": "Serialisation format for pipeline output.",
          "enum": ["json", "csv", "parquet"],
          "default": "json"
        },
        "path": {
          "type": "string",
          "description": "Output destination path or URI. Supports local paths and cloud URIs (s3://, gs://). If omitted, output is written to the default location for this pipeline.",
          "examples": ["s3://my-bucket/outputs/", "/data/outputs/pipeline-results/"]
        }
      }
    }
  }
}
```

---

**src/config/pipeline.py**

```python
from __future__ import annotations

from enum import StrEnum

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

    model_config = ConfigDict(frozen=True)

    type: SourceType = Field(
        description="The category of data source."
    )
    connection: str = Field(
        description="Connection string or URL for the data source.",
        min_length=1,
        examples=["postgresql://user:pass@host:5432/db", "s3://bucket/prefix"],
    )


class OutputConfig(BaseModel):
    """Settings controlling how pipeline output is written."""

    model_config = ConfigDict(frozen=True)

    format: OutputFormat = Field(
        default=OutputFormat.JSON,
        description="Serialisation format for pipeline output.",
    )
    path: str | None = Field(
        default=None,
        description="Output destination path or URI. Omit to use the default location.",
    )


class PipelineConfig(BaseModel):
    """Root configuration for a data pipeline."""

    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
    )

    name: str = Field(
        description="Human-readable name for this pipeline.",
        min_length=1,
        max_length=255,
    )
    source: DataSource
    schedule: str | None = Field(
        default=None,
        description="Cron expression controlling when the pipeline runs.",
        pattern=r"^(@(annually|yearly|monthly|weekly|daily|hourly|reboot))"
                r"|(([\*]|[0-9,\-\/]+)\s+){4}([\*]|[0-9,\-\/]+)$",
        examples=["0 */6 * * *", "@daily"],
    )
    output: OutputConfig = Field(default_factory=OutputConfig)
```

---

**tests/test_pipeline_schema.py**

```python
import pytest
from pydantic import ValidationError
from src.config.pipeline import PipelineConfig, DataSource, OutputConfig, SourceType, OutputFormat

# --- Valid inputs ---

def test_minimal_valid_config():
    config = PipelineConfig(
        name="nightly-export",
        source=DataSource(type=SourceType.POSTGRES, connection="postgresql://user:pass@host/db"),
    )
    assert config.name == "nightly-export"
    assert config.output.format == OutputFormat.JSON


def test_full_config_with_schedule_and_output():
    config = PipelineConfig(
        name="hourly-s3-sync",
        source=DataSource(type=SourceType.S3, connection="s3://my-bucket/raw/"),
        schedule="0 * * * *",
        output=OutputConfig(format=OutputFormat.PARQUET, path="s3://my-bucket/processed/"),
    )
    assert config.schedule == "0 * * * *"
    assert config.output.format == OutputFormat.PARQUET


def test_api_source_with_csv_output():
    config = PipelineConfig(
        name="api-daily",
        source=DataSource(type=SourceType.API, connection="https://api.example.com/data"),
        output=OutputConfig(format=OutputFormat.CSV),
    )
    assert config.source.type == SourceType.API


# --- Invalid inputs ---

def test_missing_required_name_raises():
    with pytest.raises(ValidationError) as exc:
        PipelineConfig(
            source=DataSource(type=SourceType.POSTGRES, connection="postgresql://host/db")
        )
    assert "name" in str(exc.value)


def test_name_exceeds_max_length_raises():
    with pytest.raises(ValidationError):
        PipelineConfig(
            name="x" * 256,
            source=DataSource(type=SourceType.MYSQL, connection="mysql://host/db"),
        )


def test_invalid_source_type_raises():
    with pytest.raises(ValidationError):
        PipelineConfig(
            name="bad-source",
            source=DataSource(type="oracle", connection="oracle://host/db"),  # type: ignore
        )


def test_invalid_output_format_raises():
    with pytest.raises(ValidationError):
        PipelineConfig(
            name="bad-format",
            source=DataSource(type=SourceType.POSTGRES, connection="postgresql://host/db"),
            output=OutputConfig(format="xml"),  # type: ignore
        )


def test_empty_connection_string_raises():
    with pytest.raises(ValidationError):
        DataSource(type=SourceType.S3, connection="")


def test_frozen_config_is_immutable():
    config = PipelineConfig(
        name="immutable-test",
        source=DataSource(type=SourceType.POSTGRES, connection="postgresql://host/db"),
    )
    with pytest.raises(Exception):
        config.name = "changed"  # type: ignore
```

---

**examples/pipeline-config.example.yaml**

```yaml
# Example pipeline configuration
# Validate against: schemata/pipeline-config.schema.json

name: nightly-customer-export

source:
  type: postgres
  connection: "postgresql://etl_user:${DB_PASSWORD}@db.internal:5432/production"

schedule: "0 2 * * *"  # Run at 02:00 UTC daily

output:
  format: parquet
  path: "s3://data-warehouse/exports/customers/"
```

---

**Schema evolution guidance**

| Change type | Safe? | Strategy |
|---|---|---|
| Add optional field with default (`compress: bool = False`) | YES | Additive — existing configs remain valid |
| Add required field (`version`) | NO | Add as optional first, backfill existing configs, then require in next release |
| Remove field (`path`) | NO | Deprecate in docs for one release cycle, then remove |
| Change field type (`connection`: string → object) | NO | Add `connection_v2` as new field, migrate, then remove old |
| Add enum value (`source.type: bigquery`) | YES | Old validators ignore it; new validators accept it |
| Remove enum value (`source.type: mysql`) | NO | Requires migration of all MySQL-sourced pipelines first |
| Rename field | NO | Add new field, deprecate old, migrate in one release, remove in next |
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill performs reconnaissance — the simulated output opens with all three bash commands from Step 1 and explicitly identifies the schema purpose, validation library (Pydantic v2 + jsonschema), existing naming conventions, and that no pipeline schema exists yet.

- [x] PASS: JSON Schema includes `$schema`, `$id`, and `additionalProperties: false` on every object — the root object, `DataSource`, and `OutputConfig` all have `$schema` and `$id` on the root and `additionalProperties: false` on all three objects.

- [x] PASS: All required fields listed in `required` array — root object has `"required": ["name", "source"]`, `DataSource` has `"required": ["type", "connection"]`, `OutputConfig` has `"required": ["format"]`. No required field is left implicit.

- [x] PASS: Every property has a `description` field — every property across all three schema objects includes a `description`. The `path` property in `OutputConfig` has a particularly detailed description covering cloud URIs and the omit behaviour.

- [x] PASS: Enum values use JSON Schema `enum` keyword — `source.type` uses `"enum": ["postgres", "mysql", "s3", "api"]` and `output.format` uses `"enum": ["json", "csv", "parquet"]`. No free-text strings.

- [x] PASS: Pydantic models use `ConfigDict(frozen=True)` — `DataSource`, `OutputConfig`, and `PipelineConfig` all include `model_config = ConfigDict(frozen=True)`. The immutability test in the test suite also verifies this at runtime.

- [x] PASS: String enums use `StrEnum` — `SourceType(StrEnum)` and `OutputFormat(StrEnum)` are both defined this way.

- [~] PARTIAL: Skill includes schema evolution guidance — the simulated output includes a 7-row evolution table classifying all change types as safe or breaking with migration strategies. Directly matches the skill's Step 5 table. Score: 0.5 (PARTIAL ceiling per rubric).

- [x] PASS: Output delivers schema files, ≥3 valid and ≥3 invalid tests, and example config — 3 valid test cases (minimal, full, API+CSV), 5 invalid test cases (missing name, name too long, bad source type, bad output format, empty connection), plus a YAML example config.

### Notes

The simulated output includes one improvement over the SKILL.md example: `OutputConfig` adds `"required": ["format"]` which the skill's own example omits, making the simulated output slightly stricter than the template. That's a good sign — the skill's pattern is being applied thoughtfully rather than copied blindly.

The YAML example config uses an environment variable substitution (`${DB_PASSWORD}`) which is realistic for production use but isn't validated by the JSON Schema (which would fail on the raw string). Worth noting this in real usage — config loaders typically resolve env vars before schema validation.
