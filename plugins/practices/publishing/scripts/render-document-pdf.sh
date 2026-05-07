#!/usr/bin/env bash
# Wrapper for render-document-pdf.py that ensures xhtml2pdf and python-markdown
# are available. Both are pure-Python; the only catch is that svglib 1.6+ pulls
# pycairo (which needs the cairo system library), so we pin to svglib<1.6 via
# constraints.txt. xhtml2pdf only loads svglib lazily when the HTML contains
# SVG images — our markdown doesn't reference SVGs.
#
# This wrapper creates a venv at ~/.cache/turtlestack/publishing-document-pdf-venv
# on first run (~15s) and reuses it thereafter.
#
# Override the cache location with $TURTLESTACK_CACHE_DIR (used by tests).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RENDER="$SCRIPT_DIR/render-document-pdf.py"
CONSTRAINTS="$SCRIPT_DIR/constraints.txt"

CACHE_DIR="${TURTLESTACK_CACHE_DIR:-$HOME/.cache/turtlestack}"
VENV="$CACHE_DIR/publishing-document-pdf-venv"

if [ ! -x "$VENV/bin/python" ]; then
  mkdir -p "$CACHE_DIR"
  python3 -m venv "$VENV" >/dev/null
  "$VENV/bin/pip" install --quiet --disable-pip-version-check \
    --constraint "$CONSTRAINTS" \
    xhtml2pdf markdown
fi

exec "$VENV/bin/python" "$RENDER" "$@"
