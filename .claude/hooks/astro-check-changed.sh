#!/usr/bin/env bash
# PostToolUse (Write|Edit): check a changed Astro or TypeScript file (Target B).
# Report-only: reports issues but exits 0 so the workflow continues. Change the
# final exit to 2 to make failures blocking. No-ops safely when the toolchain is
# absent (for example on a Target A project). No hardcoded paths.
input="$(cat)"
path="$(printf '%s' "$input" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | sed -E 's/.*"file_path"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')"

case "$path" in
  *.astro|*.ts|*.tsx) ;;
  *) exit 0 ;;
esac

# Prefer the project's own astro check if available; fall back to eslint. Only
# run inside a project that actually has the toolchain, so this is a no-op here.
if [ -f package.json ] && command -v npx >/dev/null 2>&1; then
  if grep -q '"astro"' package.json 2>/dev/null; then
    npx --no-install astro check 2>/dev/null || echo "astro check reported issues (review above)."
  elif command -v eslint >/dev/null 2>&1 || npx --no-install eslint --version >/dev/null 2>&1; then
    npx --no-install eslint "$path" 2>/dev/null || echo "eslint reported issues in $path (review above)."
  fi
fi
exit 0
