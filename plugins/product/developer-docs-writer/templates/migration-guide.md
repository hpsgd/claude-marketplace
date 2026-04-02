# Migration Guide

## Version

- **From:** v[X.Y.Z]
- **To:** v[X.Y.Z]
- **Date:** [YYYY-MM-DD]

## Summary of Changes

[1-2 paragraph overview of what changed and why. Include motivation for the breaking changes.]

## Breaking Changes

| # | What Changed | Old Behaviour | New Behaviour | Action Required |
|---|-------------|---------------|---------------|-----------------|
| 1 | [API/config/schema change] | [Previous behaviour] | [New behaviour] | [What the developer must do] |
| 2 | | | | |
| 3 | | | | |

## Migration Steps

### Step 1 — [Description]

**Before:**
```
[old code or configuration]
```

**After:**
```
[new code or configuration]
```

### Step 2 — [Description]

**Before:**
```
[old code or configuration]
```

**After:**
```
[new code or configuration]
```

### Step 3 — [Description]

**Before:**
```
[old code or configuration]
```

**After:**
```
[new code or configuration]
```

## Deprecation Timeline

| Item | Deprecated In | Removed In | Replacement |
|------|:------------:|:----------:|-------------|
| [Feature/API] | v[X.Y] | v[X.Y] | [New approach] |
| | | | |

## Rollback Instructions

If you need to revert to the previous version:

1. [Step to revert dependency/package version]
2. [Step to restore old configuration]
3. [Step to re-run migrations or rebuild]
4. [Verification step]

> **Warning:** [Note any rollback limitations, e.g. database migrations that are not reversible.]

## Verification Checklist

- [ ] Updated dependency to v[X.Y.Z]
- [ ] Applied all code changes from migration steps above
- [ ] Updated configuration files
- [ ] Ran test suite — all tests pass
- [ ] Verified in staging environment
- [ ] Checked logs for deprecation warnings
- [ ] Reviewed API responses for changed fields
