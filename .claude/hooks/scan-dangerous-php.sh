#!/usr/bin/env bash
# PreToolUse (Write|Edit): block Writes that introduce dangerous PHP execution sinks.
# Scans only .php content for eval/exec/shell_exec/system/passthru/proc_open/popen.
# Exit 2 denies. This catches honest mistakes; it is not a security boundary
# (it cannot see mcp__*__execute-php calls). See docs/09.
input="$(cat)"
path="$(printf '%s' "$input" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | sed -E 's/.*"file_path"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')"

case "$path" in
  *.php) ;;
  *) exit 0 ;;
esac

content="$(printf '%s' "$input" | grep -oE '"(content|new_string)"[[:space:]]*:.*')"
if printf '%s' "$content" | grep -qiE '\b(eval|exec|shell_exec|system|passthru|proc_open|popen)[[:space:]]*\('; then
  echo "Blocked: dangerous PHP execution call detected in $path (eval/exec/shell_exec/system/passthru/proc_open/popen). Refactor to avoid it." >&2
  exit 2
fi
exit 0
