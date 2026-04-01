---
name: data-model
description: Design a data model — entities, relationships, constraints, and access patterns.
argument-hint: "[domain or feature to model]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Design a data model for $ARGUMENTS.

## Process

1. **Entities** — what are the core objects? What uniquely identifies each?
2. **Relationships** — how do entities relate? One-to-many, many-to-many, hierarchical ownership?
3. **Access patterns** — how will data be queried? Optimise the schema for the most common reads
4. **Constraints** — required fields, uniqueness, referential integrity, valid value ranges
5. **Evolution** — how will the schema change? Design for additive changes (new fields are safe, removed fields need migration)

## Principles

- Normalise for writes, denormalise for reads (if needed)
- Each fact has exactly one authoritative source
- Immutable events: once written, event data doesn't change (corrections are new events)
- Schema evolution: additive changes are safe, breaking changes need migration plans
- Privacy by design: don't collect what you don't need, document retention policies

## Output

An entity-relationship description, schema definition (SQL CREATE or equivalent), and notes on access patterns and evolution strategy.
