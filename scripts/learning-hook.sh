#!/bin/bash
# Learning hook — runs on SessionStart to analyse the previous session.
# Called by the thinking plugin's SessionStart hook.
#
# Finds the most recently completed session transcript for this project
# and runs analyse-session.py on it if not already analysed.

set -euo pipefail

PLUGIN_ROOT="${1:-}"
PROJECT_DIR="${2:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ANALYSE_SCRIPT="$SCRIPT_DIR/analyse-session.py"

# Determine the project hash directory for transcripts
PROJECT_HASH_DIR=""
CLAUDE_PROJECTS_DIR="$HOME/.claude/projects"

if [ ! -d "$CLAUDE_PROJECTS_DIR" ]; then
    exit 0
fi

# The project hash is the project path with / replaced by -
PROJECT_PATH_HASH=$(echo "$PROJECT_DIR" | sed 's|^/||; s|/|-|g')
PROJECT_HASH_DIR="$CLAUDE_PROJECTS_DIR/-$PROJECT_PATH_HASH"

if [ ! -d "$PROJECT_HASH_DIR" ]; then
    exit 0
fi

# Find the most recent JSONL file that is NOT the current session
# Sort by modification time, skip files modified in the last 60 seconds (likely current session)
CURRENT_TIME=$(date +%s)
LATEST_JSONL=""
LATEST_MTIME=0

for jsonl in "$PROJECT_HASH_DIR"/*.jsonl; do
    [ -f "$jsonl" ] || continue
    MTIME=$(stat -f %m "$jsonl" 2>/dev/null || stat -c %Y "$jsonl" 2>/dev/null || echo 0)
    AGE=$((CURRENT_TIME - MTIME))

    # Skip files modified in the last 60 seconds (likely the current session being written to)
    if [ "$AGE" -lt 60 ]; then
        continue
    fi

    if [ "$MTIME" -gt "$LATEST_MTIME" ]; then
        LATEST_MTIME=$MTIME
        LATEST_JSONL=$jsonl
    fi
done

if [ -z "$LATEST_JSONL" ]; then
    exit 0
fi

# Check if already analysed
SESSION_ID=$(basename "$LATEST_JSONL" .jsonl)
PROJECT_LEARNINGS="$PROJECT_DIR/.claude/learnings"
GLOBAL_LEARNINGS="$HOME/.claude/learnings"

if [ -f "$PROJECT_LEARNINGS/sessions/$SESSION_ID.json" ] || \
   [ -f "$GLOBAL_LEARNINGS/sessions/$SESSION_ID.json" ]; then
    exit 0  # Already analysed
fi

# Run analysis
if [ -f "$ANALYSE_SCRIPT" ]; then
    python3 "$ANALYSE_SCRIPT" "$LATEST_JSONL" \
        --project-dir "$PROJECT_LEARNINGS" \
        --global-dir "$GLOBAL_LEARNINGS" \
        >/dev/null 2>&1 || true
fi
