# Output: Write schema for pipeline configuration

**Verdict:** PARTIAL
**Score:** 17.5/19 criteria met (92%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill performs reconnaissance — Step 1 is labelled "Reconnaissance" and is the mandatory first step. It prescribes three specific bash commands to locate existing schemas and identify the validation library before writing anything. The process header reads "sequential — do not skip steps."

- [x] PASS: JSON Schema includes `$schema`, `$id`, and `additionalProperties: false` on every object — the JSON Schema Rules table marks all three as MANDATORY. The example schema applies `$schema` and `$id` to the root, and `additionalProperties: false` to the root, `DataSource`, and `OutputConfig` definitions.

- [x] PASS: All required fields listed in a `required` array — explicitly listed in the MANDATORY rules table as "required array for mandatory fields". The example schema has `"required": ["name", "source"]` on the root and `"required": ["type", "connection"]` on `DataSource`.

- [x] PASS: Every property has a `description` field — explicitly listed as a MANDATORY rule: "description on every property". Anti-pattern: "Missing descriptions — a schema without descriptions is documentation without words."

- [x] PASS: Enum values use JSON Schema `enum` keyword — MANDATORY rule "enum for fixed value sets". Example schema uses `"enum": ["postgres", "mysql", "s3", "api"]` and `"enum": ["json", "csv", "parquet"]` — no free-text strings.

- [x] PASS: Pydantic models use `ConfigDict(frozen=True)` — MANDATORY Pydantic rule "Frozen models for domain objects: `model_config = ConfigDict(frozen=True)`". Applied to `DataSource`, `OutputConfig`, and `PipelineConfig` in the example. Mutable Pydantic models also listed as an anti-pattern.

- [x] PASS: String enums use `StrEnum` — MANDATORY Pydantic rule "StrEnum for string enums: enables serialisation as string, not as name". Example defines `class SourceType(StrEnum)` and `class OutputFormat(StrEnum)`.

- [~] PARTIAL: Skill includes schema evolution guidance — Step 5 "Schema Evolution" is present and provides a 7-row table classifying safe vs breaking changes with specific strategies. Criterion is prefixed PARTIAL so score is capped at 0.5.

- [x] PASS: Output delivers schema files, validation tests (≥3 valid, ≥3 invalid), and example config — Output section mandates exactly: (1) schema files, (2) validation tests with "at least 3 valid inputs, 3 invalid inputs", (3) example configuration file, and (4) migration notes.

### Output expectations

- [x] PASS: JSON Schema includes `$schema`, `$id`, and `additionalProperties: false` on root, `source`, and `output` — the skill's example schema applies all three to the root, `DataSource` `$defs`, and `OutputConfig` `$defs`.

- [x] PASS: `name` field has `minLength: 1` and `maxLength: 255` and is in the root `required` array — example schema shows `"minLength": 1, "maxLength": 255` on `name` and `"required": ["name", "source"]` on the root object.

- [x] PASS: `source.type` uses `enum: ["postgres", "mysql", "s3", "api"]` — the skill's `DataSource` definition uses exactly `"enum": ["postgres", "mysql", "s3", "api"]`.

- [x] PASS: `output.format` uses `enum: ["json", "csv", "parquet"]` — the skill's `OutputConfig` definition uses exactly `"enum": ["json", "csv", "parquet"]`.

- [x] PASS: Optional fields (cron schedule, output path) not in `required` arrays; schedule field has cron pattern — `schedule` is absent from `"required": ["name", "source"]`, has a cron regex pattern. `path` under `OutputConfig` has no `required` array covering it.

- [x] PASS: Pydantic model uses `ConfigDict(frozen=True)` for domain config and `StrEnum` for `SourceType` and `OutputFormat` — all three models in the example have `frozen=True`; both enum classes use `StrEnum`.

- [~] PARTIAL: Pydantic model has explicit type annotations, no `Any`, and rejects unknown extra fields (`extra='forbid'`) — type annotations are present on every field, no `Any` used, `StrEnum` constrains enums. However, `extra='forbid'` is not set in any of the `ConfigDict` calls in the skill's Pydantic example. The model relies on `frozen=True` but does not explicitly reject extra fields at parse time. Partially met.

- [x] PASS: Validation tests include ≥3 valid configs and ≥3 invalid configs with expected pass/fail and error class — the Output section mandates "at least 3 valid inputs, 3 invalid inputs". The skill's Anti-Patterns section calls out "Schema without tests — validate that good inputs pass and bad inputs fail" reinforcing this requirement.

- [x] PASS: Output includes an example configuration file (YAML or JSON) that round-trips through both validators — Output section mandates "Example configuration file showing valid usage" as a required deliverable.

- [~] PARTIAL: Schema evolution section identifies additive vs breaking changes with a specific example of each — Step 5 provides a 7-row table covering add optional field, add required field, remove field, change type, add/remove enum value, and rename. Each row has a "Safe?" column and a strategy. Criterion is prefixed PARTIAL so score is capped at 0.5.

## Notes

The skill is well-structured against this rubric. Every Criteria-section criterion maps to an explicit MANDATORY rule in the skill, which means the evaluation is clean.

The one substantive gap is `extra='forbid'`. The skill's `ConfigDict` examples use `frozen=True` and `str_strip_whitespace=True` but never set `extra='forbid'`. In Pydantic v2, `frozen=True` does not prevent extra fields from being accepted at validation time — it only prevents mutation after construction. A consumer following the skill's example would produce models that silently accept extra fields, which contradicts the project's strict validation convention. Adding `extra='forbid'` to the `ConfigDict` table in the Pydantic Rules section would close this gap.

The `OutputConfig` `$defs` in the JSON Schema example omits a `required` array for `format`, which is consistent (it has a default) but leaves ambiguity about whether `format` is truly optional or just defaulted. The skill doesn't address this edge case.
