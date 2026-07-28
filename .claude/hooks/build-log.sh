#!/usr/bin/env bash
# PostToolUse (Bash): append database-affecting and deploy operations to the
# build log. Git already tracks every file change, but it does NOT track what an
# agent did to the WordPress database on staging. This hook captures exactly
# those hard-to-reconstruct events (Breakdance/WP DB writes, cache clears,
# deploys) so every build carries an audit trail, in the spirit of the
# snapshot-before-write rule. No jq dependency. Never blocks (always exit 0).
input="$(cat)"
cmd="$(printf '%s' "$input" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')"

# Only log meaningful build operations, not every shell command.
printf '%s' "$cmd" | grep -qE 'wp[[:space:]]+(breakdance|post|option|db|litespeed-purge)|import_settings|clear_cache|deploy' || exit 0

log="$CLAUDE_PROJECT_DIR/build-log/BUILD-LOG.md"
[ -d "$CLAUDE_PROJECT_DIR/build-log" ] || exit 0

ts="$(date '+%Y-%m-%d %H:%M:%S')"
short="$(printf '%s' "$cmd" | tr '|' '/' | cut -c1-160)"
# shellcheck disable=SC2016  # single-quoted printf format is intentional; the backticks are literal markdown
printf '| %s | auto | db-op | `%s` |\n' "$ts" "$short" >> "$log"
exit 0
