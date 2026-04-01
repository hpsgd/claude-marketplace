#!/usr/bin/env bash
#
# install-rules.sh — Syncs rule files from a marketplace plugin into the
# consuming project's .claude/rules/ directory.
#
# Usage: install-rules.sh <plugin-dir> <target-project-dir>
#
# Rules are namespaced to avoid conflicts:
#   plugins/coding-standards/rules/typescript.md
#   → .claude/rules/coding-standards--typescript.md

set -euo pipefail

PLUGIN_DIR="${1:?Usage: install-rules.sh <plugin-dir> <target-project-dir>}"
TARGET_DIR="${2:?Usage: install-rules.sh <plugin-dir> <target-project-dir>}"

RULES_SRC="${PLUGIN_DIR}/rules"
RULES_DEST="${TARGET_DIR}/.claude/rules"

# Nothing to do if the plugin has no rules
if [[ ! -d "$RULES_SRC" ]]; then
  exit 0
fi

PLUGIN_NAME="$(basename "$PLUGIN_DIR")"

mkdir -p "$RULES_DEST"

for rule_file in "$RULES_SRC"/*.md; do
  [[ -f "$rule_file" ]] || continue

  filename="$(basename "$rule_file")"
  dest_file="${RULES_DEST}/${PLUGIN_NAME}--${filename}"

  if [[ ! -f "$dest_file" ]] || [[ "$rule_file" -nt "$dest_file" ]]; then
    cp "$rule_file" "$dest_file"
  fi
done
