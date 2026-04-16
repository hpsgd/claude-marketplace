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
