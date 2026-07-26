#!/usr/bin/env bash
# PostToolUse (Bash): clear the Breakdance cache after a database-affecting command.
# Postmeta and settings writes do not refresh Breakdance's own cache, so staging
# can serve stale output until it is cleared. Runs after a Breakdance/WP DB write.
# No-ops safely when wp is absent. No hardcoded paths.
input="$(cat)"
cmd="$(printf '%s' "$input" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')"

command -v wp >/dev/null 2>&1 || exit 0

if printf '%s' "$cmd" | grep -qE 'breakdance[[:space:]]+(import_settings|replace_url)|wp[[:space:]]+(post|option|db)[[:space:]]'; then
  wp breakdance clear_cache 2>/dev/null && echo "Breakdance cache cleared after a DB-affecting operation."
fi
exit 0
