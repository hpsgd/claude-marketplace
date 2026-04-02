---
description: Python language conventions and engineering standards
paths:
  - "**/*.py"
---

# Python Conventions

## Language settings
- Python 3.14+
- Style: [Ruff](https://docs.astral.sh/ruff) (all rule categories enabled by default), [mypy](https://mypy-lang.org) strict, 120 char lines
- Ruff categories are only disabled after explicit discussion and documentation. Use `# noqa` only after discussion — never silently

## Naming
- snake_case for functions, variables, modules
- PascalCase for classes
- UPPER_SNAKE_CASE for constants
- File naming: kebab-case for config/YAML files (e.g., `cost-evaluation.yaml`, not `cost_evaluation.yaml`)
- Module directories match domain concepts

## Type safety
- mypy strict mode — no `Any` without justification
- Pydantic models for dynamic schema generation (e.g., tool calling)
- Typed dataclasses over dicts for structured data
- Frozen dataclasses for immutable domain models
- Use `Protocol` for structural subtyping where interface abstraction is needed

## Testing hierarchy
BDD specs > Property-based > Unit. This is deliberate — BDD ensures behaviour matches intent, property-based catches edge cases, unit tests verify implementation.

1. **BDD specs** (pytest-bdd): Gherkin `.feature` files in `tests/features/`, step implementations in `tests/step_defs/`. Primary testing strategy. Features use business language; hide infrastructure in step defs.
2. **Property-based** (Hypothesis): For functions with large input spaces, data transformations, serialization round-trips.
3. **Unit tests**: For isolated logic, edge cases, error paths.

Targets: 98%+ coverage, 80%+ mutation kill rate.

## CLI
- Entry points via `python -m <package> run`
- Use `argparse` or `click` with clear subcommands
- Support `--validate` for dry-run diagnostics
- Support `--log-level` and `--trace` for observability

## Configuration
- YAML config files with JSON Schema validation (`$schema` field resolved relative to the file)
- Cross-file `$ref` resolution via the `referencing` library
- All references use explicit `{path: ...}` form — never bare strings
