# Builder: Elementor

The rules for a site built in Elementor. They name no connection: how Claude reaches the site is
in the connection file.

Build target: an existing WordPress site built in Elementor. Not a target for a new build; we work
within the site as it is.

## Stack
- WordPress on [HOST - where it runs, e.g. hosting provider or server; informational, fill
  when known]
- Elementor (version [read from wp-admin > Plugins once connected, then pin it here]) and
  Elementor Pro ([version, or "not active"])
- Caching plugin: [CACHE_PLUGIN - read from wp-admin > Plugins; the connection file says who
  clears it]

Pin both Elementor versions on the copy the work happens on. Version skew is the most common
reason a finished page will not import on the live site.

## Layout
- Layout is **JSON in each page's `_elementor_data` postmeta**, with page settings in
  `_elementor_page_settings`. Never hand-write PHP templates to produce layout.
- Elementor also writes a **CSS file per page**. A database write that does not regenerate it can
  render stale or unstyled.
- Two structure generations exist, and one site can hold both: **classic** (Section, Column,
  Widget) and **container** (Container, Widget). Establish which this site uses before building,
  and match it.
- Reusable units: saved **Templates**, and on Pro, **Global Widgets**. Find out which this site
  actually uses; do not assume.

## Tokens
- The active **Kit** holds them: Site Settings > Global Colours and Global Fonts. Prefer a global
  reference over a local override every time.
- On an existing site the tokens are not ours to change. A change restyles every page.

## Verified as editable
- The page opens in the Elementor editor and every element is a native, editable widget, with
  no unknown-element errors.
- After the CSS is regenerated (**Elementor > Tools > Regenerate CSS and Data**, a person's click
  in wp-admin; confirm the menu wording on this version), the public page still renders correctly.

## Protected paths (do not edit)
- wp-config.php, wp-settings.php

## Limits skill
`elementor-limits`. Read it before the first write.

## Page copy
- `content/_live/` is the export of what the site actually says. Elementor keeps live copy in
  the database, so without it there is no git trace of a heading changed in the Elementor editor.

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| postmeta, `_elementor_data` | where WordPress stores the page layout in the database |
| Kit | Elementor's site-wide colours and fonts |
| Regenerate CSS | the wp-admin button that rebuilds Elementor's stored styling after a change |
