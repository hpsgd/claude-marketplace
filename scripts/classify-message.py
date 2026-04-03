#!/usr/bin/env python3
"""Classify a user message for sentiment/correction signals.

Reads hook payload from stdin (UserPromptSubmit event).
Uses OpenRouter API with Haiku for fast AI classification.
Falls back to regex patterns if no API key is available.

Writes classified signals to .claude/learnings/signals/pending.jsonl
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# --- Fast regex pre-filter ---
# These catch obvious cases without needing AI inference.
# If none match, and we have an API key, we call the AI model.

CLEARLY_NOT_CORRECTION = [
    r"^(ok|okay|yes|y|yep|yeah|sure|go ahead|lgtm|ship it|commit|push|done|thanks|good|great|perfect|nice)\b",
    r"^/",  # Slash commands
    r"^\d+$",  # Pure numbers (could be ratings — handled separately)
]

CLEARLY_CORRECTION = [
    r"^no[,.\s]",
    r"\bthat'?s (not |wrong|incorrect)",
    r"\bstop (doing|that|it)",
    r"\bdon'?t (do|use|add|create|write|delete|remove|change)",
    r"\bnot what i (asked|meant|wanted|said)",
    r"\bi (already|just) (said|told|asked)",
    r"\bwhy (did you|are you|is it)",
]

CLEARLY_NOT_PATTERNS = [re.compile(p, re.IGNORECASE) for p in CLEARLY_NOT_CORRECTION]
CLEARLY_YES_PATTERNS = [re.compile(p, re.IGNORECASE) for p in CLEARLY_CORRECTION]


def classify_with_regex(prompt: str) -> dict | None:
    """Fast regex classification. Returns result or None if ambiguous."""
    if any(p.search(prompt) for p in CLEARLY_NOT_PATTERNS):
        return {"rating": 7, "type": "neutral", "confidence": "regex", "reason": "acceptance pattern"}

    if any(p.search(prompt) for p in CLEARLY_YES_PATTERNS):
        return {"rating": 3, "type": "correction", "confidence": "regex", "reason": "correction pattern"}

    return None  # Ambiguous — needs AI classification


def classify_with_ai(prompt: str, api_key: str) -> dict | None:
    """AI classification using OpenRouter (Haiku for speed)."""
    system_prompt = """You are a sentiment classifier for AI assistant interactions.
Classify the user's message as one of:
- CORRECTION: The user is correcting, rejecting, or redirecting the assistant's work
- FRUSTRATION: The user is frustrated or expressing dissatisfaction
- PRAISE: The user is expressing approval or satisfaction
- DIRECTION: The user is giving new instructions (neutral, not correcting)
- NEUTRAL: None of the above

Respond with ONLY a JSON object:
{"type": "correction|frustration|praise|direction|neutral", "rating": 1-10, "reason": "brief explanation"}

Rating scale: 1=very negative, 5=neutral, 10=very positive.
A correction is 2-4. Frustration is 1-3. Praise is 8-10. Direction is 5-6. Neutral is 5-7."""

    body = json.dumps({
        "model": "anthropic/claude-haiku-4-5-20251001",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Classify this message:\n\n{prompt[:500]}"},
        ],
        "max_tokens": 100,
        "temperature": 0,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            content = result["choices"][0]["message"]["content"]
            # Parse the JSON response
            return json.loads(content)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, TimeoutError):
        return None


def write_signal(signal: dict, project_dir: str):
    """Append a classified signal to the pending signals file."""
    signals_dir = Path(project_dir) / ".claude" / "learnings" / "signals"
    signals_dir.mkdir(parents=True, exist_ok=True)

    signals_file = signals_dir / "pending.jsonl"
    with open(signals_file, "a") as f:
        f.write(json.dumps(signal) + "\n")


def main():
    # Read hook payload from stdin
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = payload.get("prompt", "").strip()
    session_id = payload.get("session_id", "")
    cwd = payload.get("cwd", os.getcwd())

    # Skip very short messages and slash commands
    if len(prompt) < 4 or prompt.startswith("/"):
        sys.exit(0)

    # Skip messages that are clearly system-generated
    if prompt.startswith("<") and ">" in prompt[:50]:
        sys.exit(0)

    # Step 1: Try fast regex classification
    result = classify_with_regex(prompt)

    # Step 2: If ambiguous, try AI classification
    if result is None:
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        if api_key:
            result = classify_with_ai(prompt, api_key)

    # Step 3: If still unclassified, default to neutral
    if result is None:
        result = {"rating": 5, "type": "neutral", "confidence": "default", "reason": "unclassified"}

    # Only record non-neutral signals (corrections, frustration, praise)
    if result.get("type") in ("correction", "frustration", "praise"):
        signal = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "type": result["type"],
            "rating": result.get("rating", 5),
            "reason": result.get("reason", ""),
            "confidence": result.get("confidence", "ai"),
            "prompt_preview": prompt[:200],
        }
        write_signal(signal, cwd)


if __name__ == "__main__":
    main()
