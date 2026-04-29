# Result: Write SDK guide

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14.5/18 criteria met (81%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill requires a quickstart section that gets developers to a working example in 15 lines or fewer — Step 2 rules state "Under 15 lines of code" explicitly
- [x] PASS: Skill requires a method reference section documenting each public method with parameters, return types, and exceptions — Step 5 requires method tables with return types; error types are in Step 4's error table
- [x] PASS: Skill requires a research step — reading the actual SDK source before writing docs — Step 1 mandates Grep/Glob search of codebase before any writing
- [x] PASS: Skill requires installation instructions as a prerequisite before the quickstart — Step 2 template and the output format both place Installation before Quick start
- [x] PASS: All code examples must be syntactically correct and complete — no "..." placeholders in runnable code — Rules section: "Every code example must run. A code block that requires the reader to 'fill in the rest' is not an example."
- [x] PASS: Skill includes a quality checklist that verifies examples actually work — Step 6 has a dedicated quality checklist including "Every code example runs" and "Quick start works"
- [x] PASS: Skill covers common patterns section with real-world usage examples beyond the quickstart — Step 4 mandates a distinct "Common patterns" section with pagination, error handling, retry, and debugging as required subsections
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — all three fields present in frontmatter

### Output expectations

- [ ] FAIL: Output's quickstart section produces a working "first call" example in 15 lines or fewer of Python — install, import, instantiate client with API key from env, make one method call, print result — the skill requires under 15 lines and authentication, but does not require reading the API key from an environment variable; the example template only says "how to pass the API key or token" without mandating env-var sourcing
- [ ] FAIL: Output's installation instructions cover pip install plus supported Python versions and any system prerequisites — and verifies the install works (e.g. `python -c "import package; print(package.__version__)"`) — the skill requires version statement and install command but does not require an install-verification step
- [~] PARTIAL: Output's method reference documents each public method — signature with type annotations, parameter descriptions, return type, and exceptions raised — in a structured per-method format (not a flat list) — partially met: Step 5 requires grouping by resource and return types, but parameter descriptions per method and exceptions co-located with each method are not explicitly required; exceptions live in the Step 4 error table, not in the method reference
- [ ] FAIL: Output's code examples use real return-value handling — exception handling shown with SDK's specific exception types, not bare try/except — the skill requires an error type table with typed exceptions, but does not explicitly prohibit bare try/except in code examples or mandate that all error-handling examples use the specific exception classes
- [~] PARTIAL: Output's authentication section explains how the SDK reads credentials — env var by default, optional explicit constructor argument, and handling of missing credentials with the specific error raised — partially met: Step 3 requires env var documentation and constructor options, but the specific error raised on missing credentials is not required
- [~] PARTIAL: Output's common-patterns section shows real workflows — pagination iteration, batch operations, async usage if supported, retry/timeout configuration — beyond the quickstart — partially met: Step 4 requires pagination, retry, and timeout; batch operations and async are listed as optional additions "based on what the SDK actually supports," not mandatory
- [ ] FAIL: Output's quality checklist verifies each example runs by including the exact command (e.g. `python examples/quickstart.py`) and the expected output, with the rule that examples must be tested before publication — not met: Step 6 checklist checks whether examples run in principle but does not require documenting exact test commands or expected output, and does not state examples must be tested before publication
- [x] PASS: Output's code examples are complete and copy-pasteable — no `...` ellipsis in runnable code, no placeholder imports, all variables either defined or marked as user-supplied — met: rules explicitly prohibit incomplete code blocks
- [x] PASS: Output's quickstart instantiates the client without revealing the API key in the file — met: Step 2 rules require showing "how to pass the API key or token" and Step 3 shows env var alternatives; the existing output.md example uses a hardcoded key, but the skill itself does not prescribe hardcoded keys and the env-var pattern is shown in Step 3
- [~] PARTIAL: Output addresses the difference between sync and async client variants if the SDK supports both, or explicitly notes that the SDK is sync-only — partially met: async is mentioned as a possible optional pattern in Step 4 ("based on what the SDK actually supports") but the skill does not require a note when the SDK is sync-only

## Notes

The Criteria section is a clean pass — all 8 structural requirements are met. The gaps are concentrated in the output expectations tier. Key weaknesses:

1. The quality checklist (Step 6) is conceptual ("can they copy-paste and get a response?") rather than operational — no requirement for a reproducible test command or expected output makes it hard to enforce in practice.
2. Authentication coverage stops short of requiring the specific error raised on missing credentials, which is exactly what developers hit first when misconfiguring.
3. The method reference uses a table format that omits per-method parameter descriptions — developers can see the return type but not what each parameter means without reading source.
4. The quickstart does not mandate env-var credential sourcing, leaving the door open for hardcoded keys in examples (the existing output.md demonstrates this gap).
