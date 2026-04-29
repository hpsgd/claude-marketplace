# Test: Design a prompt for extracting action items from meeting transcripts

Scenario: Developer invokes the prompt-design skill to create a production prompt that extracts structured action items (owner, description, due date) from meeting transcript text.

## Prompt

Design a production prompt for extracting action items from meeting transcripts. Input is a meeting transcript (up to 3,000 words). Output should be a JSON array of action items, each with: `owner` (person's name), `description` (what they agreed to do), `due_date` (ISO date string or null if not mentioned), `confidence` (float 0-1). Volume: ~200 transcripts/day. Latency budget: p95 < 5s. Cost budget: < $0.03/request.

## Criteria

- [ ] PASS: Skill defines all six task properties before writing a single word of prompt: input format/size, output format/schema, constraints, volume, and latency budget
- [ ] PASS: Skill specifies evaluation criteria (accuracy, format compliance, hallucination rate, latency, cost) with pass thresholds BEFORE designing the prompt
- [ ] PASS: Skill specifies using JSON mode or function calling for structured output — not relying on "output as JSON" in prompt text
- [ ] PASS: Skill starts with a minimal prompt and adds instructions only when eval failures demand it
- [ ] PASS: Skill designs at least 5 test cases covering: 2 happy paths, 2 edge cases (no action items, ambiguous ownership), 1 adversarial (prompt injection attempt)
- [ ] PASS: Skill includes context grounding — instructions for when the transcript contains no action items (return empty array, not hallucinated items)
- [ ] PASS: Skill specifies version control strategy — prompt stored in repo with a changelog showing eval results per version
- [ ] PARTIAL: Skill includes output validation rules — schema validation on every response, length validation, and catch for validation failures
- [ ] PASS: Output follows the full format: task definition, eval criteria, prompt v1.0, output schema, test results table, safety measures, version history

## Output expectations

- [ ] PASS: Output's task definition restates the four input/output specifics from the prompt — 3,000-word transcript ceiling, 200 requests/day volume, p95 < 5s latency, $0.03/request cost budget — rather than generic placeholders
- [ ] PASS: Output's schema for each action item names all four required fields (`owner`, `description`, `due_date`, `confidence`) with correct types, where `due_date` is explicitly nullable (ISO date string or null) and `confidence` is a float in [0,1]
- [ ] PASS: Output's prompt instructs the model to return an empty array (not null, not a hallucinated item, not a prose apology) when the transcript contains no action items, and a test case verifies this behaviour
- [ ] PASS: Output's prompt body delimits the transcript with explicit boundaries (XML tags, triple quotes, or equivalent) so the transcript content cannot be confused with system instructions
- [ ] PASS: Output's adversarial test case uses a transcript that contains an embedded "ignore previous instructions" or role-override attempt within the meeting text, and the expected output is a normal action-item extraction that ignores the injection
- [ ] PASS: Output addresses ambiguous ownership (e.g. "someone should follow up", "the team will handle it") with a defined behaviour — either skip the item, lower the confidence below a stated threshold, or assign a sentinel owner — not silently guessing a name
- [ ] PASS: Output includes at least one test case probing relative date resolution (e.g. "by next Friday", "end of quarter") and specifies how the model should handle dates without an anchor reference date in the prompt
- [ ] PARTIAL: Output names a specific model (e.g. Claude Sonnet, GPT-4o-mini) and shows a back-of-envelope token/cost calculation demonstrating the design fits the $0.03/request budget at 3,000-word inputs
- [ ] PARTIAL: Output's eval set sizing matches the skill's minimum (50 examples) and describes how the 50 examples are sourced — real transcripts, synthetic, or a mix — rather than just asserting the number
