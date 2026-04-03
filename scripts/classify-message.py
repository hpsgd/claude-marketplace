#!/usr/bin/env python3
"""Classify a user message for sentiment/correction signals.

Reads hook payload from stdin (UserPromptSubmit event).
Uses fast regex for obvious cases (corrections, praise).
Queues ambiguous messages for later classification by Claude
during the retrospective analysis (which runs inside Claude
and doesn't need an external API).

Writes to .claude/learnings/signals/pending.jsonl
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Seed patterns (hardcoded baseline) ---
# These are the starting set. The retrospective skill adds learned
# patterns to .claude/learnings/signals/patterns.json at runtime.

SEED_NOT_CORRECTION = [
    r"^(ok|okay|yes|y|yep|yeah|sure|go ahead|lgtm|ship it|commit|push|done|thanks|good|great|perfect|nice)\b",
    r"^/",  # Slash commands
    r"^!",  # Shell escapes
]

SEED_CORRECTION = [
    r"^no[,.\s]",
    r"\bthat'?s (not |wrong|incorrect)",
    r"\bstop (doing|that|it)",
    r"\bdon'?t (do|use|add|create|write|delete|remove|change)",
    r"\bnot what i (asked|meant|wanted|said)",
    r"\bi (already|just) (said|told|asked)",
    r"\bwhy (did you|are you|is it)\b.*\?",
    r"\bwrong\b",
    r"\bnot that\b",
]

SEED_PRAISE = [
    r"\b(excellent|brilliant|amazing|awesome|fantastic|wonderful)\b",
    r"\bthat'?s (exactly|precisely|perfect)",
    r"\bgreat (work|job)\b",
    r"\bwell done\b",
    r"\blove (it|this|that)\b",
]

SEED_APPROACH_CHANGE = [
    r"\bdifferent approach",
    r"\bchange (of |in )?direction",
    r"\bslight change",
    r"\bscrap (that|this)",
    r"\bstart over",
    r"\bon second thought",
    r"\bactually[,.]?\s+(let'?s|i think|i'?d)",
]


def load_patterns(project_dir: str) -> dict[str, list[re.Pattern]]:
    """Load seed patterns + any learned patterns from the project.

    Learned patterns live in .claude/learnings/signals/patterns.json:
    {
        "correction": ["\\bfeels (arbitrary|wrong)\\b", ...],
        "praise": [...],
        "approach_change": [...],
        "not_correction": [...]
    }
    """
    learned = {"correction": [], "praise": [], "approach_change": [], "not_correction": []}

    patterns_file = Path(project_dir) / ".claude" / "learnings" / "signals" / "patterns.json"
    if patterns_file.exists():
        try:
            with open(patterns_file) as f:
                data = json.load(f)
            for key in learned:
                for p in data.get(key, []):
                    try:
                        re.compile(p, re.IGNORECASE)  # Validate before using
                        learned[key].append(p)
                    except re.error:
                        pass  # Skip invalid patterns
        except (json.JSONDecodeError, OSError):
            pass

    # Combine seed + learned, compile
    return {
        "not_correction": [re.compile(p, re.IGNORECASE) for p in SEED_NOT_CORRECTION + learned["not_correction"]],
        "correction": [re.compile(p, re.IGNORECASE) for p in SEED_CORRECTION + learned["correction"]],
        "praise": [re.compile(p, re.IGNORECASE) for p in SEED_PRAISE + learned["praise"]],
        "approach_change": [re.compile(p, re.IGNORECASE) for p in SEED_APPROACH_CHANGE + learned["approach_change"]],
    }


def classify(prompt: str, patterns: dict[str, list[re.Pattern]]) -> dict | None:
    """Fast regex classification. Returns result or None if ambiguous."""
    if any(p.search(prompt) for p in patterns["not_correction"]):
        return None  # Clearly not interesting — don't record at all

    if any(p.search(prompt) for p in patterns["correction"]):
        return {"rating": 3, "type": "correction", "confidence": "regex"}

    if any(p.search(prompt) for p in patterns["praise"]):
        return {"rating": 9, "type": "praise", "confidence": "regex"}

    if any(p.search(prompt) for p in patterns["approach_change"]):
        return {"rating": 4, "type": "approach_change", "confidence": "regex"}

    # Ambiguous — queue for Claude to classify during retrospective
    if len(prompt) > 20:  # Skip very short messages
        return {"rating": 5, "type": "unclassified", "confidence": "needs_review"}

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

    # Skip very short messages and commands
    if len(prompt) < 4 or prompt.startswith("/") or prompt.startswith("!"):
        sys.exit(0)

    # Skip system-generated messages (XML tags)
    if prompt.startswith("<") and ">" in prompt[:50]:
        sys.exit(0)

    # Load seed + learned patterns
    patterns = load_patterns(cwd)

    result = classify(prompt, patterns)

    if result is None:
        sys.exit(0)  # Not interesting or clearly positive — skip

    signal = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "type": result["type"],
        "rating": result["rating"],
        "confidence": result["confidence"],
        "prompt_preview": prompt[:300],
    }
    write_signal(signal, cwd)


if __name__ == "__main__":
    main()
