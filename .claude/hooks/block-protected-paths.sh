#!/usr/bin/env bash
# PreToolUse (Write|Edit): deny writes to protected paths and secret files.
# Target-neutral: blocks wp-config.php and wp-settings.php (Target A), any
# production or live path (both targets), and .env secret files (both targets,
# needed by Target B). A .env.example template is allowed. Exit 2 denies the
# call. No hardcoded machine paths; matches by suffix and basename.
input="$(cat)"
path="$(printf '%s' "$input" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | sed -E 's/.*"file_path"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')"

case "$path" in
  *wp-config.php|*wp-settings.php|*/production/*|*/live/*|*/prod/*)
    echo "Blocked: $path is a protected path and must not be edited by the agent." >&2
    exit 2
    ;;
esac

case "$(basename "$path")" in
  .env.example)
    exit 0
    ;;
  .env|.env.*)
    echo "Blocked: $path is a secret file. Secrets belong in environment references, not committed or agent-written files." >&2
    exit 2
    ;;
esac
exit 0
