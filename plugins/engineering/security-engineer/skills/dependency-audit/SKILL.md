---
name: dependency-audit
description: Audit project dependencies for known vulnerabilities, outdated packages, and license issues.
argument-hint: "[project directory or package file to audit]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit dependencies for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Inventory

Before running audit tools, understand the dependency landscape:

1. **Identify all dependency manifests:**
   ```bash
   find . -name "package.json" -o -name "*.csproj" -o -name "requirements*.txt" -o -name "pyproject.toml" -o -name "Pipfile" -o -name "go.mod" -o -name "Cargo.toml" | grep -v node_modules | grep -v .git
   ```

2. **Count direct vs transitive dependencies:**
   - Direct: dependencies you chose to include
   - Transitive: dependencies of your dependencies (you don't control these)

3. **Identify dependency age:**
   - When was each direct dependency last updated?
   - Are any dependencies unmaintained (no release in 12+ months)?
   - Are any deprecated with a recommended replacement?

### Step 2: Vulnerability Scan

Run the appropriate audit tool for each stack:

```bash
# Node.js
npm audit --json 2>/dev/null | head -100
# or
npx audit-ci --config audit-ci.jsonc

# .NET
dotnet list package --vulnerable --include-transitive

# Python
pip-audit --format=json 2>/dev/null
# or
safety check --json

# Go
govulncheck ./...

# Rust
cargo audit
```

**Rules:**
- Run the audit tool with JSON output when available — structured data is easier to triage
- If the audit tool fails to run, note the error and attempt an alternative
- Capture the full output — do not truncate vulnerability lists

### Step 3: Reachability Analysis (MANDATORY for each vulnerability)

Not every CVE is a real risk. For EACH vulnerability found:

**Question 1: Is the vulnerable code path reachable?**
- Read the CVE description — what specific function or feature is affected?
- Search the codebase: is that function imported and called?
- Check transitive dependency chains — are you using the parent package in a way that triggers the vulnerable path?

```bash
# Example: Check if a specific vulnerable function is used
grep -rn "import.*vulnerable-function\|require.*vulnerable-package" --include="*.ts" --include="*.py" --include="*.cs"
```

**Question 2: Is the vulnerability exploitable in this context?**
- Does the CVE require network access that the package doesn't have in your deployment?
- Does the CVE require user input that the package never receives in your usage?
- Is the CVE only exploitable in a specific environment (e.g., Windows-only, browser-only)?

**Question 3: What is the actual impact?**
- Remote Code Execution (RCE) — CRITICAL regardless
- Data exposure — severity depends on what data
- Denial of Service — severity depends on availability requirements
- Information disclosure — severity depends on what information

### Step 4: Triage Categories

Classify every vulnerability into one of four categories:

| Category | Criteria | Action | Timeline |
|---|---|---|---|
| **Fix now** | Reachable, HIGH/CRITICAL severity, fix available | Upgrade or patch immediately | Today |
| **Fix soon** | Reachable, MEDIUM severity, or fix requires planning/testing | Schedule fix | This sprint |
| **Monitor** | Not reachable in current usage, LOW severity, or no fix available | Track for changes, reassess quarterly | Next review |
| **Accept** | Assessed as non-exploitable in this context, documented risk acceptance | Document with owner and expiry | Review in 90 days |

**Rules:**
- Every "Accept" has an owner and a review date. Accepted risks don't disappear — they're re-evaluated
- "Fix now" means stop what you're doing and fix it. Not "add to backlog"
- If a vulnerability has no fix available and IS reachable, evaluate workarounds (remove the dependency, add input validation upstream, use an alternative)
- Use [SLSA](https://slsa.dev/) (Supply-chain Levels for Software Artifacts) as the framework for verifying supply chain integrity — assess dependencies against SLSA levels for build provenance and source integrity

### Step 5: CVE Assessment Detail

For each HIGH or CRITICAL vulnerability, document:

```markdown
### CVE-XXXX-XXXXX: [Package Name]

- **Package:** [name]@[version]
- **Fixed in:** [version] (or "no fix available")
- **CVSS:** [score] ([vector string])
- **Attack vector:** [network/adjacent/local/physical]
- **Description:** [1-2 sentences from the CVE]
- **Reachable:** [YES/NO — with evidence]
  - Import chain: [your code] -> [package A] -> [vulnerable function]
  - Used in: `file:line` — [description of usage]
- **Exploitability in this context:** [assessment]
- **Recommended action:** [upgrade to X.Y.Z / remove dependency / add workaround / accept with justification]
```

### Step 6: Outdated and Deprecated Package Check

Beyond vulnerabilities, check for maintenance risks:

```bash
# Node.js — check for outdated packages
npm outdated

# .NET — check for newer versions
dotnet list package --outdated

# Python — check for outdated packages
pip list --outdated
```

For each outdated package:

| Risk level | Criteria |
|---|---|
| **High** | Major version behind, package is a critical dependency (auth, crypto, framework) |
| **Medium** | Minor version behind, or package has security-relevant function |
| **Low** | Patch version behind, or package is a dev-only dependency |
| **Deprecated** | Package marked deprecated — find and evaluate replacement |

### Step 7: License Compliance (if applicable)

```bash
# Node.js
npx license-checker --summary

# Python
pip-licenses --format=table
```

Flag any licenses incompatible with the project's license:
- **Copyleft (GPL, AGPL)** — may require open-sourcing your code. Legal review required
- **Non-commercial** — not permitted for commercial projects
- **No license** — unknown terms. Legal risk. Avoid

## Anti-Patterns (NEVER do these)

- **Running `npm audit fix` blindly** — auto-fix can introduce breaking changes. Triage first, fix deliberately
- **Ignoring transitive vulnerabilities** — you chose the parent package. Its vulnerabilities are your problem
- **Suppressing without documenting** — audit suppressions must have a reason, an owner, and an expiry date
- **"No vulnerabilities found" without evidence** — show the audit tool output. Prove the tool ran
- **Treating all CVEs as equal** — a CRITICAL RCE in a reachable path is not the same as a LOW info-disclosure in an unused function
- **Outdated audit database** — ensure the audit tool's vulnerability database is up to date before running

## Output Format

```markdown
## Dependency Audit: [project]

### Summary
- **Total dependencies:** [direct] direct, [transitive] transitive
- **Vulnerabilities found:** [X critical, Y high, Z medium, W low]
- **Outdated packages:** [count]
- **Deprecated packages:** [count]
- **Recommendation:** [ship / fix first / block]

### Vulnerability Report

| # | Package | Version | CVE | CVSS | Severity | Reachable | Fix available | Category |
|---|---|---|---|---|---|---|---|---|
| 1 | lodash | 4.17.20 | CVE-2021-23337 | 7.2 | HIGH | YES | 4.17.21 | Fix now |
| 2 | tar | 6.1.0 | CVE-2021-37701 | 8.6 | CRITICAL | NO | 6.1.9 | Monitor |

### CVE Details
[Detailed assessment for each HIGH/CRITICAL — see Step 5 template]

### Outdated Packages

| Package | Current | Latest | Risk | Notes |
|---|---|---|---|---|
| [name] | [ver] | [ver] | [High/Medium/Low] | [reason] |

### Deprecated Packages

| Package | Replacement | Migration effort |
|---|---|---|
| [name] | [alternative] | [estimate] |

### License Issues

| Package | License | Compatibility | Action |
|---|---|---|---|
| [name] | [license] | [compatible/review/incompatible] | [action] |

### Actions

| # | Action | Category | Priority | Owner | Deadline |
|---|---|---|---|---|---|
| 1 | Upgrade lodash to 4.17.21 | Fix now | P0 | [name] | Today |
| 2 | Evaluate tar upgrade | Monitor | P2 | [name] | Next review |

### Audit Evidence
- **Tool:** [npm audit / pip-audit / dotnet list package --vulnerable]
- **Database version:** [date of vulnerability database]
- **Command output:** [summary or link to full output]
```

## Related Skills

- `/security-engineer:threat-model` — dependency vulnerabilities are attack surface. Feed high-severity findings into the threat model.
- `/security-engineer:security-review` — when a vulnerable dependency is used in security-sensitive code, review the usage patterns.
