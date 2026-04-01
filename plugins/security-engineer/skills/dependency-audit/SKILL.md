---
name: dependency-audit
description: Audit project dependencies for known vulnerabilities, outdated packages, and license issues.
argument-hint: "[project directory or package file to audit]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit dependencies for $ARGUMENTS.

## Process

1. Run the appropriate audit tool:
   - npm: `npm audit`
   - .NET: `dotnet list package --vulnerable`
   - Python: `pip-audit`
2. For each vulnerability: assess whether the vulnerable code path is actually reachable in your usage
3. Categorise: fix now (reachable, high severity), fix soon (reachable, lower severity), monitor (not reachable)
4. Check for outdated packages with available updates
5. Check for deprecated packages needing replacement

## Output

| Package | Current | Latest | CVE | Severity | Reachable? | Action |
|---|---|---|---|---|---|---|
