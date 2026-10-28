# Builder: WPBakery

The rules for a site built with the WPBakery Page Builder (formerly Visual Composer), usually
bundled with an older commercial theme. They name no connection: how Claude reaches the site is in
the connection file.

Build target: an existing WordPress site built in WPBakery. Not a target for a new build; we work
within the site as it is.

## Stack
- WordPress (version [read from wp-admin > Dashboard > Updates once connected, then pin it here])
  on [HOST - where it runs, e.g. hosting provider or server; informational, fill when known]
- WPBakery (version [read from wp-admin > Plugins, then pin it here]), and whether it came bundled
  with the theme or has its own licence: [BUNDLED_OR_LICENSED]
- Theme and child theme: [THEME - name and version of each, from wp-admin > Appearance > Themes],
  and whether the theme is still sold and maintained: [THEME_STATUS]
- Plugins that add WPBakery elements: [ELEMENT PLUGINS - the theme's companion functions plugin and
  every add-on bundle, with versions]
- Caching: [CACHE_PLUGIN - read from wp-admin > Plugins], plus any CDN in front of the site that
  caches pages [CDN - e.g. Cloudflare, or "none"]. The connection file says who clears them

Pin every version above on staging. **The operator may decide not to update WPBakery or the
theme**, which is a legitimate call on an inherited site: everything here works on whatever version
is installed, because the vocabulary is read from the site, not remembered. A bundled WPBakery
usually only updates through its theme, so an abandoned theme strands it.

## Layout
- A page's layout is **shortcodes in the page's own content**: plain text tags such as
  `[vc_row][vc_column width="1/2"][vc_column_text]...[/vc_column_text][/vc_column][/vc_row]`. It is
  readable, diffable plain text, not a hidden data blob.
- **Never write WPBakery from memory.** A model's memory blends a decade of versions and knows
  nothing of the theme's or add-ons' elements. That has already produced wrong-version output on a
  real job. The vocabulary is the raw shortcodes of the site's own pages, read through the
  connection, and nothing else.
- Each element's spacing, borders and backgrounds (Design Options) are stored on the shortcode, but
  the page loads them from a stylesheet WPBakery rebuilds when the page is saved in its editor.
  **A save through the connection does not rebuild it** (proven on WPBakery 8.7.1, SUFWB, October
  2026; confirm on the first page of each site). A page that already had styling keeps printing the
  old styling until a person clicks Update. An empty page with no stored styling is the exception:
  WPBakery builds it from the layout as the page renders.
- **Never leave the WPBakery editor open across a write through the connection.** Clicking Update
  saves the whole page as the editor loaded it, so a tab opened before the write puts the old layout
  back. The person reloads the editor before pasting CSS or clicking Update, and after every person's
  Update the stored layout is compared with the layout file.

## The person's steps on every page
The connection cannot reach these, so each page is "written, waiting on the developer" until a
person has done them, and the page record lists which apply:

1. **Reload the page in the WPBakery backend editor** (never an editor tab opened earlier).
2. **Paste the page Custom CSS** (page settings, Custom CSS), over any older version of the block.
3. **Paste the page Custom JS** when the page has a WPBakery accordion (see `wpbakery-limits`).
4. **Click Update**, then purge the page cache.
5. **Template and title band.** On a page not duplicated from a built page, set the full-width
   WPBakery template in Page Attributes and switch the theme's title band off in its page settings.
   They are separate settings, and the title band prints a second h1.

Site-wide CSS (Appearance, Customise, Additional CSS) is also a person's paste. Paste it **before**
any page write that depends on it.
- Older sites hold retired elements, such as the old accordion (`[vc_accordion]`, rendered with
  `wpb_accordion` classes). They still display. **Never copy a retired element into a new page.**
- **Never write PHP template files to produce layout**, and never change WPBakery's settings or the
  theme's options panel while working on a page. Either one restyles the whole site.

## Tokens
- WPBakery has no real token layer. The nearest things are the theme's options panel and stylesheet
  and WPBakery's own colour and font settings. Everything else is raw values typed into each
  element's Design Options.
- So **match the values the sibling pages already use**: copy the equivalent element's Design Options
  and classes from the reference page. Introduce no value that does not already appear on a sibling.
- On an existing site the tokens are not ours to change. A change restyles every page.

## Verified as editable
Rendering correctly is not evidence. Nothing checks a shortcode when it is saved, so a page is
verified only when all four are true:

1. **The rendered page shows no visible `[vc_` text** or any other bracketed tag. A malformed
   shortcode shows up there, or as a broken layout.
2. **It opens in the WPBakery backend editor as elements**, not as one block of raw text, and each
   element opens its settings window without error.
3. **The page's Design Options are styled.** Its `vc_custom_` rules are in the rendered page head,
   and its spacing matches its siblings. If they are missing, a person opens the page in the
   WPBakery editor and clicks Update, which rebuilds them. Never hand-write the stylesheet.
4. **The public page shows the new copy**, per the check in the core instructions.

Opening the editor needs a login. Until a person, or a logged-in browser, has done step 2, the page
is "built, not verified", and the report says so.

**Measure, do not eyeball.** "Verified" also means measured live, logged out, at 1280, 991, 768,
767, 380 and 320px: spacing, alignment and no sideways scroll. On SUFWB most of the fixes came from
measurements a screenshot would have passed.

## Protected paths (do not edit)
- wp-config.php, wp-settings.php
- The theme's own files and the theme's companion functions plugin. Changing them is a deliberate,
  human-approved job of its own, never part of building a page.

## Limits skill
`wpbakery-limits`. Read it before the first write.

## Page copy
- `content/_live/` is the export of what the site actually says. WPBakery keeps page copy in the
  database, so the export is the only git evidence of a change made in the editor.

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| WPBakery | the drag and drop page builder this site's pages are made in |
| shortcode | the page's layout, stored as plain text tags in square brackets |
| Design Options | the spacing, border and background settings on each element |
| backend editor | WPBakery's editing screen in wp-admin, where the page shows as blocks of elements |
| retired element | an old WPBakery element that still displays but is no longer offered for new pages |
| page Custom CSS | the styling box in one page's WPBakery settings, which affects only that page |
| Additional CSS | the site-wide styling box under Appearance, Customise, which affects every page |
| title band | the theme's band across the top of a page, carrying the page name as a heading |
