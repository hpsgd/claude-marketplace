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

# --- Fast regex pre-filter ---
# Catches obvious cases. Ambiguous messages get queued for Claude
# to classify during the retrospective (which IS Claude).

CLEARLY_NOT_CORRECTION = [
    r"^(ok|okay|yes|y|yep|yeah|sure|go ahead|lgtm|ship it|commit|push|done|thanks|good|great|perfect|nice)\b",
    r"^/",  # Slash commands
    r"^!",  # Shell escapes
]

CLEARLY_CORRECTION = [
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

CLEARLY_PRAISE = [
    r"\b(excellent|brilliant|amazing|awesome|fantastic|wonderful)\b",
    r"\bthat'?s (exactly|precisely|perfect)",
    r"\bgreat (work|job)\b",
    r"\bwell done\b",
    r"\blove (it|this|that)\b",
]

APPROACH_CHANGE = [
    r"\bdifferent approach",
    r"\bchange (of |in )?direction",
    r"\bslight change",
    r"\bscrap (that|this)",
    r"\bstart over",
    r"\bon second thought",
    r"\bactually[,.]?\s+(let'?s|i think|i'?d)",
]

CLEARLY_NOT_PATTERNS = [re.compile(p, re.IGNORECASE) for p in CLEARLY_NOT_CORRECTION]
CLEARLY_YES_PATTERNS = [re.compile(p, re.IGNORECASE) for p in CLEARLY_CORRECTION]
PRAISE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in CLEARLY_PRAISE]
APPROACH_PATTERNS = [re.compile(p, re.IGNORECASE) for p in APPROACH_CHANGE]


def classify(prompt: str) -> dict | None:
    """Fast regex classification. Returns result or None if ambiguous."""
    if any(p.search(prompt) for p in CLEARLY_NOT_PATTERNS):
        return None  # Clearly not interesting — don't record at all

    if any(p.search(prompt) for p in CLEARLY_YES_PATTERNS):
        return {"rating": 3, "type": "correction", "confidence": "regex"}

    if any(p.search(prompt) for p in PRAISE_PATTERNS):
        return {"rating": 9, "type": "praise", "confidence": "regex"}

    if any(p.search(prompt) for p in APPROACH_PATTERNS):
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

    result = classify(prompt)

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
