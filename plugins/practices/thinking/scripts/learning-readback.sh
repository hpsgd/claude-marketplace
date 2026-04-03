#!/bin/bash
# Learning readback — runs on SessionStart (sync).
# Reads recent learnings and outputs them to stdout for context injection.
# Output appears as system context in the conversation.
#
# Budget: <2000 characters to avoid context bloat.

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
PROJECT_LEARNINGS="$PROJECT_DIR/.claude/learnings"
GLOBAL_LEARNINGS="$HOME/.claude/learnings"

output=""

# --- Recent correction signals (from classify-message.py) ---
SIGNALS_FILE="$PROJECT_LEARNINGS/signals/pending.jsonl"
if [ -f "$SIGNALS_FILE" ]; then
    # Count recent corrections (last 24 hours)
    RECENT_CORRECTIONS=$(python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta
cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
corrections = []
try:
    with open('$SIGNALS_FILE') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            d = json.loads(line)
            if d.get('timestamp', '') > cutoff and d.get('type') in ('correction', 'frustration'):
                corrections.append(d)
except: pass
if corrections:
    print(f'Recent corrections ({len(corrections)} in last 24h):')
    for c in corrections[-3:]:
        print(f'  - [{c[\"type\"]}] {c.get(\"reason\", \"\")} ({c.get(\"prompt_preview\", \"\")[:80]})')
" 2>/dev/null)

    if [ -n "$RECENT_CORRECTIONS" ]; then
        output="$output$RECENT_CORRECTIONS\n"
    fi
fi

# --- Recent session learnings ---
for learnings_dir in "$PROJECT_LEARNINGS/sessions" "$GLOBAL_LEARNINGS/sessions"; do
    [ -d "$learnings_dir" ] || continue

    # Find the 2 most recent analysis files
    RECENT=$(ls -t "$learnings_dir"/*.json 2>/dev/null | head -2)
    for f in $RECENT; do
        SUMMARY=$(python3 -c "
import json, sys
try:
    with open('$f') as fh:
        d = json.load(fh)
    m = d.get('metrics', {})
    c = m.get('corrections', {})
    total_c = c.get('total', 0)
    if total_c > 0:
        print(f'Session {d[\"session_id\"][:8]}...: {total_c} corrections (rate: {m.get(\"correction_rate\", 0):.0%})')
        for evt in d.get('events', [])[:2]:
            if evt.get('type') in ('immediate_correction', 'approach_change'):
                print(f'  - {evt.get(\"user_said\", \"\")[:100]}')
except: pass
" 2>/dev/null)

        if [ -n "$SUMMARY" ]; then
            output="$output$SUMMARY\n"
        fi
    done
done

# --- High-confidence wisdom ---
for wisdom_dir in "$PROJECT_DIR/.claude/wisdom" "$HOME/.claude/wisdom"; do
    [ -d "$wisdom_dir" ] || continue

    WISDOM=$(python3 -c "
import os, re
wisdom_dir = '$wisdom_dir'
principles = []
for f in os.listdir(wisdom_dir):
    if not f.endswith('.md'): continue
    with open(os.path.join(wisdom_dir, f)) as fh:
        for line in fh:
            m = re.search(r'\[CRYSTAL\s+(\d+)%\]\s+(.*)', line)
            if m and int(m.group(1)) >= 85:
                principles.append(f'  - [{f.replace(\".md\",\"\")}] {m.group(2).strip()} ({m.group(1)}%)')
if principles:
    print('High-confidence wisdom:')
    for p in principles[:5]:
        print(p)
" 2>/dev/null)

    if [ -n "$WISDOM" ]; then
        output="$output$WISDOM\n"
    fi
done

# Only output if we have something (keep context clean)
if [ -n "$output" ]; then
    echo "<learning-context>"
    echo -e "$output" | head -c 1900  # Hard budget limit
    echo "</learning-context>"
fi
