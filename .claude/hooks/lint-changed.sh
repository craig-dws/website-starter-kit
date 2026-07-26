#!/usr/bin/env bash
# PostToolUse (Write|Edit): lint a changed PHP file. Report-only: it reports
# issues but exits 0 so the workflow continues. Change the final exit to 2 to
# make lint failures blocking. No-ops safely when phpcs is absent.
input="$(cat)"
path="$(printf '%s' "$input" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | sed -E 's/.*"file_path"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')"

case "$path" in
  *.php) ;;
  *) exit 0 ;;
esac

if command -v phpcs >/dev/null 2>&1 && [ -f "$path" ]; then
  phpcs --standard=WordPress "$path" || echo "phpcs reported issues in $path (review above)."
fi
exit 0
