#!/usr/bin/env bash
#
# install-rules.sh — Syncs rule files from a marketplace plugin into the
# appropriate .claude/rules/ directory.
#
# If the plugin is enabled globally (~/.claude/settings.json), rules go to ~/.claude/rules/
# If the plugin is enabled in the project, rules go to <project>/.claude/rules/
# If both, rules go to both.
#
# Usage: install-rules.sh <plugin-dir> [<target-project-dir>]
#
# Rules are namespaced to avoid conflicts:
#   plugins/coding-standards/rules/typescript.md
#   → .claude/rules/coding-standards--typescript.md

set -euo pipefail

PLUGIN_DIR="${1:?Usage: install-rules.sh <plugin-dir> [<target-project-dir>]}"
PROJECT_DIR="${2:-${CLAUDE_PROJECT_DIR:-$(pwd)}}"

RULES_SRC="${PLUGIN_DIR}/rules"

# Nothing to do if the plugin has no rules
if [[ ! -d "$RULES_SRC" ]]; then
  exit 0
fi

# Derive plugin name from the directory
PLUGIN_NAME="$(basename "$PLUGIN_DIR")"

# Determine which targets to install to
TARGETS=()

# Helper: check if plugin is enabled in a settings file
plugin_enabled_in() {
  local settings_file="$1"
  local plugin_name="$2"
  [[ -f "$settings_file" ]] || return 1
  local result
  result=$(python3 -c "
import json, sys
d = json.load(open(sys.argv[1]))
name = sys.argv[2]
for k, v in d.get('enabledPlugins', {}).items():
    if v and k.startswith(name + '@'):
        print('yes')
        sys.exit(0)
" "$settings_file" "$plugin_name" 2>/dev/null)
  [[ "$result" == "yes" ]]
}

# Temporarily disable errexit for checks (python3 exits non-zero when plugin not found)
set +e

# Check if plugin is globally enabled
plugin_enabled_in "$HOME/.claude/settings.json" "$PLUGIN_NAME"
[[ $? -eq 0 ]] && TARGETS+=("$HOME/.claude/rules")

# Check if plugin is enabled in project settings
PROJECT_ADDED=false
for settings_file in "$PROJECT_DIR/.claude/settings.json" "$PROJECT_DIR/.claude/settings.local.json"; do
  plugin_enabled_in "$settings_file" "$PLUGIN_NAME"
  if [[ $? -eq 0 ]]; then
    TARGETS+=("$PROJECT_DIR/.claude/rules")
    PROJECT_ADDED=true
    break
  fi
done

set -e

# Fallback: if we couldn't determine scope, install to project (backward compat)
if [[ ${#TARGETS[@]} -eq 0 ]]; then
  TARGETS+=("$PROJECT_DIR/.claude/rules")
fi

# Deduplicate targets
UNIQUE_TARGETS=$(printf '%s\n' "${TARGETS[@]}" | sort -u)

# Install rules to each target
for RULES_DEST in $UNIQUE_TARGETS; do
  mkdir -p "$RULES_DEST"

  for rule_file in "$RULES_SRC"/*.md; do
    [[ -f "$rule_file" ]] || continue

    filename="$(basename "$rule_file")"
    dest_file="${RULES_DEST}/${PLUGIN_NAME}--${filename}"

    if [[ ! -f "$dest_file" ]] || [[ "$rule_file" -nt "$dest_file" ]]; then
      cp "$rule_file" "$dest_file"
    fi
  done
done
