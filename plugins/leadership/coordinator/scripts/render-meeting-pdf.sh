#!/usr/bin/env bash
# Wrapper for render-meeting-pdf.py that ensures reportlab is available.
#
# ReportLab is pure Python, but macOS system Python is externally-managed
# (PEP 668), so a venv is the portable path. This wrapper creates one in
# ~/.cache/turtlestack/coordinator-meeting-pdf-venv on first run, installs
# reportlab into it, and reuses it thereafter.
#
# Override the cache location with $TURTLESTACK_CACHE_DIR (used by tests).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RENDER="$SCRIPT_DIR/render-meeting-pdf.py"

CACHE_DIR="${TURTLESTACK_CACHE_DIR:-$HOME/.cache/turtlestack}"
VENV="$CACHE_DIR/coordinator-meeting-pdf-venv"

if [ ! -x "$VENV/bin/python" ]; then
  mkdir -p "$CACHE_DIR"
  python3 -m venv "$VENV" >/dev/null
  "$VENV/bin/pip" install --quiet --disable-pip-version-check reportlab
fi

exec "$VENV/bin/python" "$RENDER" "$@"
