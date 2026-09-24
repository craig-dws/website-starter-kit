# Builder: WordPress block theme

The rules for a site built with WordPress blocks and a block theme (Gutenberg, full site
editing), rather than with a page builder plugin. They name no connection: how Claude reaches the
site is in the connection file.

Build target: an existing WordPress block theme site. Not a target for a new build; we work
within the site as it is.

## Stack
- WordPress (version [read from wp-admin > Dashboard > Updates once connected, then pin it here])
  on [HOST - where it runs, e.g. hosting provider or server; informational, fill when known]
- Theme and child theme: [THEME - name and version of each, from wp-admin > Appearance > Themes]
- Block-providing plugins: [BLOCK PLUGINS - every plugin that registers blocks, with its version,
  including any ACF blocks plugin]
- Caching plugin: [CACHE_PLUGIN - read from wp-admin > Plugins; the connection file says who
  clears it]

Pin every version above on staging. A theme or block plugin update can change what a valid block
looks like, so re-test before relying on it.

## Layout
- A page's layout is **block markup in the page's own content**: ordinary HTML, with each block's
  name and settings written in an HTML comment around it (`<!-- wp:group {...} -->`). It is
  readable, diffable plain text, not a hidden data blob.
- Templates, template parts (the header, the footer, other shared regions), navigation menus and
  synced patterns (reusable blocks) are block markup too, each stored as its own kind of post.
- **A template, template part, menu or synced pattern is shared.** Changing one changes every
  page that uses it. That is not part of a page job: snapshot it and ask first.
- **Never write PHP template files to produce layout.** The editor cannot see them, and it is a
  security risk.

## Tokens
- `theme.json` in the theme defines the palette, type scale, spacing scale and layout widths,
  with any site-wide overrides stored in global styles. WordPress turns them into CSS custom
  properties named `--wp--preset--color--<slug>`, `--wp--preset--font-family--<slug>`,
  `--wp--preset--font-size--<slug>` and `--wp--preset--spacing--<slug>`, readable in the CSS of
  any public page.
- Blocks reference a preset by its slug (`has-primary-color`), never by value. **Never write a
  raw colour, font size or spacing value into block markup where a preset exists.**
- On an existing site the tokens are not ours to change. A change restyles every page.

## Verified as editable
Rendering correctly is not evidence. A page is verified only when all three are true:

1. **It opens in the block editor with no validation warning.** A block whose saved markup does
   not match what it expects shows "This block contains unexpected or invalid content" and is
   offered for conversion to plain HTML. The site accepts invalid markup without complaint, and
   a converted block still renders correctly, so the editor is the only place this shows. Check
   every block on the page, not just the first screen.
2. **Every ACF block shows every field.** An ACF block's content is data in the block comment,
   drawn by a PHP template when the page loads. A wrong field name most likely renders empty with
   no warning at all, so check each field's content is on the rendered page. *(Confirm this
   behaviour on the real site.)*
3. **The public page shows the new copy**, per the check in the core instructions.

Opening the editor needs a login. Until a person, or a logged-in browser, has done step 1, the
page is "built, not verified", and the report says so.

## Protected paths (do not edit)
- wp-config.php, wp-settings.php
- The theme's own files, including `theme.json` and its template files. Changing them is a
  deliberate, human-approved job of its own, never part of building a page.

## Limits skill
`gutenberg-limits`. Read it before the first write.

## Page copy
- `content/_live/` is the export of what the site actually says. A block theme keeps page copy in
  the database too, so the export is the only git evidence of a change made in the editor.

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| block theme | a WordPress site built from the editor's own blocks rather than a page builder plugin |
| block markup | the page's layout, stored as HTML with each block's settings in comments |
| `theme.json`, preset | the theme's file of named colours, sizes and spacing, and one named value from it |
| block validation warning | the editor saying a block's saved markup is wrong, which offers to turn it into uneditable HTML |
| ACF block | a custom block whose content is typed into fields, drawn by the theme when the page loads |
| template part | a shared region such as the header or footer, used on many pages |
