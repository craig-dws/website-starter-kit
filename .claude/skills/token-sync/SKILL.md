---
name: token-sync
description: Sync Figma design tokens into Breakdance global variables on staging using a safe differential merge. Use when the design system tokens have changed and need to be reflected in the Breakdance build (Target A), or when the operator runs token-sync. Reads Figma variables, exports current Breakdance settings, merges without overwriting custom CSS or clamp() functions, imports, and clears cache. Do not rename this skill to design-sync; that name is reserved by Claude Design.
---

# Token sync

Sync the Figma design tokens into Breakdance global variables on the staging
site without destroying existing configuration. This is Target A. For Target B,
tokens live in code (see the token-to-code approach in docs/09).

**Do not rename this to design-sync.** Claude Design ships a first-party
`/design-sync` command that uploads a design system to Claude Design. A skill of
the same name would shadow it and break that upload (docs/09). Ours syncs Figma
tokens into Breakdance, which is a different job.

## Steps

1. Read the current design tokens from Figma with the Figma variable-definitions
   capability (get_variable_defs). Scope reads to the collection, not whole
   files.
2. Export the current Breakdance settings: `wp breakdance export_settings`.
3. Perform a differential merge:
   - Preserve every existing key.
   - Preserve all custom CSS exactly.
   - Preserve all clamp() functions exactly.
   - Add or update only the global variables the Figma tokens require.
4. Write the merged JSON to a new file and show the diff for review.
5. Pause for human approval of the diff before importing.
6. Import the merged settings: `wp breakdance import_settings <file>`.
7. Clear cache: `wp breakdance clear_cache`.
8. Verify: `wp breakdance status`, and spot-check a page rendered with the new
   tokens.

## Rules

- Never blind-overwrite settings. `import_settings` overwrites the whole config;
  only ever apply a reviewed differential merge. Never run `total_reset`.
- Snapshot the relevant postmeta and export current settings before importing.
  Our backup is the safety net.
- Reference variables, never hardcoded hex or off-scale spacing. Token names are
  identical across Figma, Breakdance, and any CSS custom properties; the naming
  bridge is the whole game (docs/22).
- Map only the tiers Breakdance can hold: colour and typography map at the
  semantic tier; spacing maps partially; the component tier has no clean home
  (docs/22). Flag any token with no clean Breakdance home rather than inventing a
  mapping.
- Staging only. Never run against production.
- British and Australian English. No em dashes, no en dashes, no emojis.

## TODO (per project)

- Confirm the Breakdance Pro licence is active before relying on
  export_settings and import_settings; they are Pro only.
- Record the pinned Breakdance version. A builder update requires re-testing the
  merge before it touches client work.
