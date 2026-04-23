#!/usr/bin/env bash
#
# install-rules.sh — Syncs rule files from a marketplace plugin into the
# appropriate .claude/rules/ directory.
#
# If the plugin is enabled globally (~/.claude/settings.json), rules go to
# ~/.claude/rules/ ONLY — no project-level copy (global rules apply everywhere).
# If the plugin is enabled only in the project, rules go to <project>/.claude/rules/.
#
# Also cleans up:
# - Stale versioned files (e.g., 1.6.0--foo.md, 1.7.2--foo.md) from older installs
# - Plugin-prefixed files for rules that no longer exist in the source
# - Project-level duplicates when a plugin is globally enabled
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

set +e

GLOBAL_ENABLED=false
plugin_enabled_in "$HOME/.claude/settings.json" "$PLUGIN_NAME"
[[ $? -eq 0 ]] && GLOBAL_ENABLED=true

PROJECT_ENABLED=false
for settings_file in "$PROJECT_DIR/.claude/settings.json" "$PROJECT_DIR/.claude/settings.local.json"; do
  plugin_enabled_in "$settings_file" "$PLUGIN_NAME"
  if [[ $? -eq 0 ]]; then
    PROJECT_ENABLED=true
    break
  fi
done

set -e

# Global takes precedence — if enabled globally, only install there
TARGETS=()
if [[ "$GLOBAL_ENABLED" == "true" ]]; then
  TARGETS+=("$HOME/.claude/rules")
elif [[ "$PROJECT_ENABLED" == "true" ]]; then
  TARGETS+=("$PROJECT_DIR/.claude/rules")
else
  TARGETS+=("$PROJECT_DIR/.claude/rules")
fi

# Build list of expected filenames from source
EXPECTED_FILES=()
for rule_file in "$RULES_SRC"/*.md; do
  [[ -f "$rule_file" ]] || continue
  EXPECTED_FILES+=("${PLUGIN_NAME}--$(basename "$rule_file")")
done

# Helper: remove versioned copies of this plugin's rules from a directory
cleanup_versioned() {
  local dir="$1"
  [[ -d "$dir" ]] || return 0
  for rule_file in "$RULES_SRC"/*.md; do
    [[ -f "$rule_file" ]] || continue
    local filename
    filename="$(basename "$rule_file")"
    for versioned in "$dir"/[0-9]*.[0-9]*.[0-9]*--"${filename}"; do
      [[ -f "$versioned" ]] || continue
      rm "$versioned"
    done
  done
}

# Helper: remove plugin-prefixed rules that no longer exist in source
cleanup_stale() {
  local dir="$1"
  [[ -d "$dir" ]] || return 0
  for existing in "$dir"/"${PLUGIN_NAME}"--*.md; do
    [[ -f "$existing" ]] || continue
    local existing_name
    existing_name="$(basename "$existing")"
    local found=false
    for expected in "${EXPECTED_FILES[@]}"; do
      if [[ "$existing_name" == "$expected" ]]; then
        found=true
        break
      fi
    done
    if [[ "$found" == "false" ]]; then
      rm "$existing"
    fi
  done
}

# Install rules to each target
for RULES_DEST in "${TARGETS[@]}"; do
  mkdir -p "$RULES_DEST"

  for rule_file in "$RULES_SRC"/*.md; do
    [[ -f "$rule_file" ]] || continue

    filename="$(basename "$rule_file")"
    dest_file="${RULES_DEST}/${PLUGIN_NAME}--${filename}"

    if [[ ! -f "$dest_file" ]] || [[ "$rule_file" -nt "$dest_file" ]]; then
      cp "$rule_file" "$dest_file"
    fi
  done

  cleanup_stale "$RULES_DEST"
  cleanup_versioned "$RULES_DEST"
done

# If globally enabled, clean up any project-level copies (they're redundant)
if [[ "$GLOBAL_ENABLED" == "true" ]]; then
  PROJECT_RULES="$PROJECT_DIR/.claude/rules"
  if [[ -d "$PROJECT_RULES" ]]; then
    cleanup_stale "$PROJECT_RULES"
    # Also remove the plugin-prefixed files from project since global covers it
    for expected in "${EXPECTED_FILES[@]}"; do
      [[ -f "$PROJECT_RULES/$expected" ]] && rm "$PROJECT_RULES/$expected"
    done
    cleanup_versioned "$PROJECT_RULES"
  fi
fi
