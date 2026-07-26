#!/usr/bin/env bash
# PostToolUse (Bash): purge LiteSpeed cache after a database-affecting WP write.
#
# Why this exists (docs/24, Section E): `wp post meta update` does NOT fire the
# save_post hook. LiteSpeed Cache's automatic purge hangs off post-save hooks, so
# a scripted postmeta write (a title, alt text, a Rank Math field, Breakdance
# data) changes the database and still serves the OLD value to visitors and
# crawlers until the cache expires. That is a silent failure: the build looks
# done and is not. Every scripted write must end with an explicit purge.
#
# No-ops safely when wp or LiteSpeed is absent. No hardcoded paths.
input="$(cat)"
cmd="$(printf '%s' "$input" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')"

command -v wp >/dev/null 2>&1 || exit 0

# Targeted purge: pull the post id from `wp post meta update <id> ...`.
if printf '%s' "$cmd" | grep -qE 'wp[[:space:]]+post[[:space:]]+meta[[:space:]]+update'; then
  id="$(printf '%s' "$cmd" | sed -nE 's/.*wp[[:space:]]+post[[:space:]]+meta[[:space:]]+update[[:space:]]+([0-9]+).*/\1/p')"
  if [ -n "$id" ]; then
    wp litespeed-purge post_id "$id" 2>/dev/null && echo "LiteSpeed: purged post_id $id after postmeta write."
    exit 0
  fi
fi

# Sitewide changes (settings import, URL replace, option or db writes): purge all.
if printf '%s' "$cmd" | grep -qE 'breakdance[[:space:]]+(import_settings|replace_url)|wp[[:space:]]+(option|db)[[:space:]]'; then
  wp litespeed-purge all 2>/dev/null && echo "LiteSpeed: purged all after a sitewide change."
fi
exit 0
