# Test: Write SDK guide

Scenario: Testing whether the write-sdk-guide skill requires a quickstart under 15 lines, a method reference, and code examples that are complete and runnable.

## Prompt


/developer-docs-writer:write-sdk-guide for our Python SDK — it wraps our REST API and currently has no documentation beyond the README installation instructions.

## Criteria


- [ ] PASS: Skill requires a quickstart section that gets developers to a working example in 15 lines or fewer
- [ ] PASS: Skill requires a method reference section documenting each public method with parameters, return types, and exceptions
- [ ] PASS: Skill requires a research step — reading the actual SDK source before writing docs
- [ ] PASS: Skill requires installation instructions as a prerequisite before the quickstart
- [ ] PASS: All code examples must be syntactically correct and complete — no "..." placeholders in runnable code
- [ ] PASS: Skill includes a quality checklist that verifies examples actually work
- [ ] PARTIAL: Skill covers common patterns section with real-world usage examples beyond the quickstart — partial credit if examples are required but common patterns as a distinct section is not
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's quickstart section produces a working "first call" example in 15 lines or fewer of Python — install, import, instantiate client with API key from env, make one method call, print result
- [ ] PASS: Output's installation instructions cover `pip install <package>` plus the supported Python versions and any system prerequisites — and verifies the install works (e.g. `python -c "import package; print(package.__version__)"`)
- [ ] PASS: Output's method reference documents each public method — signature with type annotations, parameter descriptions, return type, and exceptions raised — in a structured per-method format (not a flat list)
- [ ] PASS: Output's code examples use real return-value handling — exception handling shown with the SDK's specific exception types, not bare `try/except` — so developers learn the right patterns
- [ ] PASS: Output's authentication section explains how the SDK reads credentials — env var by default, optional explicit constructor argument, and handling of missing credentials with the specific error raised
- [ ] PASS: Output's common-patterns section shows real workflows — pagination iteration, batch operations, async usage if supported, retry/timeout configuration — beyond the quickstart's single-call demo
- [ ] PASS: Output's quality checklist verifies each example runs by including the exact command (e.g. `python examples/quickstart.py`) and the expected output, with the rule that examples must be tested before publication
- [ ] PASS: Output's code examples are complete and copy-pasteable — no `...` ellipsis in runnable code, no placeholder imports, all variables either defined or marked as user-supplied with a clear convention
- [ ] PASS: Output's quickstart instantiates the client without revealing the API key in the file — e.g. `client = Client(api_key=os.environ['MYAPI_KEY'])` rather than a hardcoded string
- [ ] PARTIAL: Output addresses the difference between sync and async client variants if the SDK supports both, or explicitly notes that the SDK is sync-only
