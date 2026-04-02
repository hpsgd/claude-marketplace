---
description: Strict validation principles — applies across all languages and frameworks
---

# Strict Validation

## Philosophy

[Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/). Convert unstructured input into structured, type-safe data at the boundary. Start strict, relax only when a proven need arises. Tightening validation after bad data exists in production is hard or impossible.

## Language-specific settings

### TypeScript
- Always set `strict: true` in `tsconfig.json` — never disable individual strict flags
- Use [Zod](https://zod.dev/) with `.strict()` for runtime validation of external input
- Never use `any` — prefer `unknown` and narrow with a parser

### Python
- Use [Pydantic](https://docs.pydantic.dev/latest/concepts/strict_mode/) with `model_config = ConfigDict(strict=True)` — no implicit coercion
- Enable mypy strict mode (`--strict`) in CI
- Use `Annotated` types with Pydantic validators for domain constraints

### .NET
- Enable nullable reference types (`<Nullable>enable</Nullable>`) in every project
- Use FluentValidation for request validation — never rely on manual null checks
- Prefer `required` properties over nullable ones

### JSON Schema
- Always set `additionalProperties: false` on every object schema
- Use `required` for all mandatory fields — never assume defaults

## API strictness

- Define separate request and response schemas — never reuse the same model for both
- Reject unknown fields in request bodies (strict deserialization)
- Reject unknown query parameters — return 400, not a silent ignore
- Validate path parameters against expected patterns (UUIDs, slugs, numeric IDs)

## Database strictness

- `NOT NULL` by default — add `NULL` only when the business domain requires absence
- Use `CHECK` constraints for value ranges and invariants
- Prefer enum types or lookup tables over unconstrained strings
- Enforce foreign keys — never rely on application-level referential integrity alone
- Add unique constraints for natural keys, not just surrogate primary keys

## Config strictness

- Define a typed config schema — never read raw environment variables deep in the codebase
- Validate all config at startup — fail fast with a clear error, not lazily at first use
- Distinguish between missing config (crash) and optional config (explicit default)

## Domain primitives

- Wrap business concepts in value objects: `EmailAddress` not `string`, `Money` not `decimal`, `OrderId` not `int`
- Validate invariants in the constructor — an invalid value object cannot exist
- Use the type system to make illegal states unrepresentable
