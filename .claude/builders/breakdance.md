# Builder: Breakdance

The rules for a site built in Breakdance. They name no connection: how Claude reaches the site
is in the connection file.

Build target: WordPress + Breakdance.

## Stack
- WordPress on [HOST - where it runs, e.g. hosting provider or server; informational, fill
  when known]
- Breakdance (version [read from wp-admin > Plugins once connected, then pin it here]) as
  the page builder

## Breakdance conventions
- Auto Layout maps to Section and Div; column arrangements map to Columns.
- Repeating content uses the Post Loop Builder.
- Never write raw PHP layout files. Build through Breakdance elements only.
- Never blind-import settings. Always export first, then differential merge.
- After any DB-affecting operation, clear the Breakdance cache the way the connection file says.
- Content lives in the _breakdance_data postmeta. Back it up before writes.
- Pin the Breakdance version on staging. Re-test the write path after any update.

## Layout, tokens and editability
- **Layout** is a structured tree in each page's `_breakdance_data` postmeta, not in the page's
  own content.
- **Tokens** live in Breakdance Global Settings (Global Colours, Typography Presets) and the
  global CSS variables.
- **Verified as editable** when the page opens in the Breakdance builder and every element is
  natively editable, with no unknown-element errors.
- **Limits skill:** `breakdance-limits`. Read it before the first write.

## Protected paths (do not edit)
- wp-config.php, wp-settings.php

## Don'ts
- Do not run wp breakdance total_reset.
- Do not run wp breakdance import_settings blind.

## Page copy
- `content/_live/` is the export of what the site actually says, and it is evidence rather
  than input. Breakdance keeps live copy in the database, so without it there is no git trace
  of a heading changed in the Breakdance UI.

## Reference
- Build runbooks and best practices are in docs/ (19 for the build runbook, 23 best practices).

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| postmeta, `_breakdance_data` | where WordPress stores the page layout in the database |
| differential merge | comparing settings and applying only the changes, rather than overwriting everything |
