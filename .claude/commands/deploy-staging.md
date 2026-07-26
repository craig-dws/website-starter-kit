---
description: Sync tokens and clear caches to refresh the staging build
argument-hint: [optional note]
allowed-tools: mcp__figma__get_variable_defs, Bash(wp breakdance export_settings:*), Bash(wp breakdance clear_cache:*), Bash(wp breakdance status:*)
---

Refresh the staging build. Context note: $ARGUMENTS

Steps:
1. Run the token-sync skill to bring Breakdance global variables in line with
   the current Figma tokens: differential merge, human-reviewed diff, never a
   blind overwrite.
2. After the sync, run wp breakdance clear_cache.
3. Run wp breakdance status and report the result.

Do not import settings without showing the diff first, and never run
total_reset. The import step is human-gated by permission policy; propose the
merged file for a human to import. Staging only.
