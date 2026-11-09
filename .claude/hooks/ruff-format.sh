#!/usr/bin/env bash
# PostToolUse hook: format a Python file with Ruff after Claude edits it.
# Never blocks Claude: always exits 0, problems only go to stderr.
# Ruff runs through uvx (no project dependency); the version is pinned on purpose.

file=$(python3 -c 'import sys, json; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))' 2>/dev/null)

case "$file" in
  "$CLAUDE_PROJECT_DIR"/*.py) ;;   # only Python files inside this project
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0

cd "$CLAUDE_PROJECT_DIR" || exit 0   # so ruff.toml is picked up
uvx ruff@0.17.4 format "$file" >&2 || echo "ruff format failed for $file (ignored)" >&2
exit 0
