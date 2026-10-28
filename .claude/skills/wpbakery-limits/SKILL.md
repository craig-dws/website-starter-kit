---
name: wpbakery-limits
description: The WPBakery Page Builder's constraints as an instruction, so a page stays within what WPBakery can build editably. Use when adding, rebuilding or editing pages on an existing client site built with WPBakery (formerly Visual Composer), usually on an inherited theme that bundles it. Covers how shortcode layout is stored, reading the element vocabulary from the site rather than from memory, Design Options styling, theme and add-on elements, the REST API write path, and the ranked safe ways to write. WPBakery is not a build target for new sites here; confirm version-specific details on the real site rather than assuming them.
---

# WPBakery limits

The fourth sibling to `breakdance-limits`, `elementor-limits` and `gutenberg-limits`. It keeps a
page buildable and keeps an agent inside the safe envelope.

**WPBakery is not one of the agency's build targets for a new site.** The agency builds new sites on
WordPress plus Breakdance. This skill exists for a different job: **adding, rebuilding or editing
pages on an existing client site that is already built in WPBakery.** Never propose WPBakery for a
new build.

The project's builder file (`.claude/builders/wpbakery.md`) holds the short version that loads into
every chat. This is the detail behind it.

## Recognising one

Check the rendered source of any page. A WPBakery site shows:

- A meta tag: `generator" content="Powered by WPBakery Page Builder`.
- Layout classes `vc_row`, `wpb_row`, `vc_column`, `wpb_column`, `wpb_wrapper`, `wpb_text_column`,
  `wpb_content_element`.
- Assets loaded from `wp-content/plugins/js_composer/`. `js_composer` is the plugin's folder and
  internal name, a leftover of the Visual Composer era.
- Classes in the form `vc_custom_1478646169179` on elements. These are Design Options (below), and
  how widely they appear tells you how much per-element styling the site relies on.

If those are present, this skill applies and the other three limits skills do not.

## The lesson that matters most: never write WPBakery from memory

**This is the failure that has already happened on a real job.** A developer asked an AI to write
WPBakery layout without the site's own vocabulary in front of it, and the output did not match the
installed version.

The cause is structural, not bad luck. WPBakery has existed for over a decade under two names. A
model's memory of it blends many versions, invents parameters, and reaches for elements the site has
never had. It also knows nothing about the elements the site's theme and add-ons register, which on
an inherited site are often the ones that matter.

**So the vocabulary is read from the site, every time, and the model's memory is not a source.**

1. **The raw shortcodes of the site's own pages are the primary vocabulary.** Read every page
   through the connection, not only the reference page. Together they show every element the site
   actually uses, with this version's exact syntax and this site's encoding of the awkward
   parameters. Under the inventory rule, the page is composed only from these.
2. **The element registry is for anything beyond that.** WPBakery keeps a map of every element it
   knows, including the theme's and every add-on's, and every parameter each accepts. It is only
   needed when the page needs an element no existing page uses, which is a stop-and-ask anyway.
   Reaching it needs more than the REST connection: the WPBakery backend editor loads it into the
   page for a logged-in browser *(confirm on the installed version)*, or a developer exports it with
   WP-CLI. Do not guess it instead.

An element or parameter that appears in neither does not exist on this site. Do not use it.

## How WPBakery stores content

| What | Where it lives | Format |
|------|----------------|--------|
| Page layout | The page's own content (`post_content`) | Shortcodes |
| Design Options styling for the page's elements | `_wpb_shortcodes_custom_css` postmeta | CSS, generated from the shortcodes |
| Page-level custom CSS | `_wpb_post_custom_css` postmeta | CSS |
| Whether the page opens in the WPBakery editor | `_wpb_vc_js_status` postmeta | `true` or `false` |
| Global settings (colours, fonts, element defaults) | WPBakery's settings, plus the theme's own options panel | Options |

*(Confirm the postmeta names on the installed version before relying on them.)*

**Shortcodes are plain text in the page content.** A simple row looks like this:

```
[vc_row][vc_column width="1/2"][vc_column_text]<p>Text</p>[/vc_column_text][/vc_column][vc_column width="1/2"][vc_single_image image="123" img_size="large"][/vc_column][/vc_row]
```

This is readable, diffable text in the ordinary content field, with no hidden data tree to
reverse-engineer. That makes WPBakery far more workable for an agent than Breakdance or Elementor.
The price is that nothing checks it (below).

**Never hand-write PHP template files to produce layout.** The builder will not see them, and it is
a security risk.

## Syntax traps a model gets wrong

Check each against an existing instance on the site rather than trusting this list alone:

- **Nesting needs the inner variants.** A row inside a column is `[vc_row_inner][vc_column_inner]`,
  not a second `[vc_row][vc_column]`. Nesting the outer pair breaks the layout.
- **Column widths are fractions** (`width="1/2"`, `width="1/3"`), and a row's columns add up to one.
- **Images are attachment IDs**, not addresses (`image="123"`). An ID is only valid on the site it
  came from.
- **Some parameters are encoded.** Links are a URL-encoded, pipe-separated string such as
  `url:https%3A%2F%2F...|title:...|`. Raw HTML elements hold base64 content. Grouped parameters are
  URL-encoded JSON. WPBakery also escapes quotes and square brackets inside parameter values with its
  own backtick convention. **Copy the encoding from an existing instance of the same element**; never
  hand-roll it.
- **Accordions and tabs need a unique `tab_id`** on every section.
- **Retired elements still render.** Older sites often hold elements WPBakery has since replaced, such
  as the old `[vc_accordion]` (rendered with `wpb_accordion` classes), replaced by
  `[vc_tta_accordion]`. They display fine, but **never copy a retired element into a new page.** If
  the copy needs one and its replacement is used nowhere on the site, that is a stop-and-ask.

## Design Options, the failure to prove on every site

Most WPBakery sites style elements through **Design Options**: margins, padding, borders and
backgrounds set per element in the editor. Each is stored as a `css` parameter on the shortcode:

```
[vc_column_text css=".vc_custom_1478646169179{margin-bottom: 0px !important;}"]
```

The page does **not** load that styling from the shortcode. WPBakery collects it into the
`_wpb_shortcodes_custom_css` postmeta and prints it in the page head, and a person clicking Update in
the WPBakery editor rebuilds it.

**A save through the REST API does not rebuild it.** Proven on WPBakery 8.7.1 (SUFWB, 14 October
2026): after the home page was written through the connection, its head still printed the old page's
`vc_custom_` rules and none of the 16 new ones. A page written through the connection renders with
the right structure and the wrong spacing, which is easy to miss on a quick look.

Three refinements, all from the same build:

- **An empty page is the exception.** A page with no stored styling (a hub that never had a layout)
  printed all its Design Options straight after the API write, because WPBakery builds them from the
  layout when nothing is stored. A person's Update is still needed for the page CSS and script.
- **Changing only an `el_class` needs no Update.** Adding a class to a row's "Extra class name"
  through the connection left every Design Options rule printing.
- **Never leave the editor open across a write.** Update saves the whole page as the editor loaded
  it. On SUFWB an editor tab opened before a write saved the older layout back, undoing six card
  buttons. Reload the editor first; after every person's Update, compare the stored layout with the
  layout file.

So, on every site, on the first page:

1. Write the page through the connection.
2. Check its `vc_custom_` rules appear in the rendered page head.
3. If they do not, **a person reloads the page in the WPBakery backend editor and clicks Update**,
   which rebuilds them, and every later page gets the same step. Record which it was in
   `build-log/DECISIONS.md`.

Never hand-write `_wpb_shortcodes_custom_css` as a substitute.

## What the API cannot reach, and how to work around it

None of these is exposed through the REST API (only `footnotes` is in a page's `meta`). Each is a
person's paste or click, so the build hands over a file and then checks the result is printing.

| Setting | Where a person sets it | Scope |
|---------|------------------------|-------|
| Page Custom CSS | The page's WPBakery settings, Custom CSS | That page only |
| Page Custom JS | The page's WPBakery settings, Custom JS (footer box) | That page only |
| Additional CSS | Appearance, Customise, Additional CSS | Every page |
| Template | Page Attributes | That page |
| Theme title band | The theme's own page settings box | That page |

- **Keep every paste as a versioned file in the repo**, such as `build-log/layouts/page-custom-css.css`
  with a version line at the top. After the paste, read the public page and confirm the block prints
  **once** and no older version is left. On SUFWB a paste was reported done on two pages that still
  printed the previous version.
- **Prefer one class-scoped block in Additional CSS over per-page pastes** once the same rule is
  needed on more than a few pages. Scope it to opt-in classes the build adds (`page-banner`,
  `wg-split-top`, `wg-cards-wrap`), so pages the build does not touch are not restyled. A new page
  then just gets the class, with no paste at all. This is a recorded exception to "no site-wide CSS",
  justified by the scoping, so record each block in `build-log/DECISIONS.md`.
- **Paste Additional CSS before the page writes that depend on it**, or the pages show half-styled in
  between.
- **The template and the title band are separate settings.** On SUFWB, switching a page to the
  full-width WPBakery template left the theme's title band in place, printing a second h1. On every
  page not duplicated from a built page, check the body class and the h1 count after the write.

## Cascade traps, measured on a real site

- **WPBakery prints a page's Design Options after its Custom CSS.** A Custom CSS rule that targets a
  `vc_custom_` class with that class alone loses, even with `!important`. Use a more specific
  selector, such as `article section.content .vc_column-inner.vc_custom_...`.
- **When testing a rule by injecting it into the page, inject it where the real one will print.**
  Page Custom CSS goes first in the head; Additional CSS goes last. A test that injects in the wrong
  place passes rules that fail for real.
- **Break media queries at 991.98px and 767.98px**, not 991px and 767px. At exactly 991 and 767 the
  browser fell between the theme's rules and the build's, and neither applied.
- **`.wpb_wrapper` is `height:100%`**, so it fills its column. A vertical-centring check that measures
  the wrappers always passes; measure the text itself. On SUFWB that hid offsets of up to 72px.
- **A column with a border or background gets 35px top padding** from WPBakery's own stylesheet
  (`.vc_col-has-fill > .vc_column-inner`), so text beside a 1px divider starts lower than its
  neighbour.
- **The theme may force content link colours with `!important`**, beating a plain link rule. Match its
  wrapper and its `!important` to override it.
- **The theme's own brand colour may fail contrast as text.** Check every text colour on the site
  against WCAG AA before the first page, and decide once, using only colours already on the site,
  which may carry words and which only rules, panels and icons.

## Element traps

- **The current accordion is `[vc_tta_accordion]` with `[vc_tta_section]`**, and every section needs a
  new, unique `tab_id` in the form the editor writes (13 digits, a hyphen, then a short random code).
  If no page on the site uses it, a person adds one in the editor to a throwaway draft, the build reads
  its shortcode as the pattern, and the draft is deleted. Never write it from memory.
- **The WPBakery accordion changes the address bar on every click.** Its script writes `#<tab_id>` into
  the address and adds a browser history entry, so Back steps through FAQ questions. There is no
  setting to turn it off. The fix used on SUFWB is a small script in the page's Custom JS that empties
  the accordion's `changeLocationHash` function after load. Every page with an FAQ gets it.
- **A list that opens a text column** picks up the theme's top margin and pushes the column down. Give
  it `style="margin-top: 0;"`.
- **The theme's small button may print its label at 11px.** Check button label sizes on the first page.
- **Gravity Forms buttons and anchors.** The form's Submit button takes the theme accent, which may
  fail contrast; restyle it in the page CSS. A link to a form needs `scroll-margin-top` on the form so
  it lands below a fixed header.

## Duplicated pages carry more than the layout

A new page made with a duplicate page plugin (Yoast Duplicate Post on SUFWB) copies the reference
page's layout and settings, which is the point. It also:

- **leaves the slug empty and keeps the reference page's parent.** Set both through the connection;
- **copies the reference page's SEO title and meta description** (Rank Math, Yoast). Until the SEO
  pass the new page is an exact duplicate of its reference page to a search engine. List it in the
  page record and make sure the SEO pass replaces it before launch;
- **copies the banner photo**, which is often why that reference page was chosen. Check a banner
  photo's crop at 1280, 1024 and 768 before choosing it, because deeper banners cut faces.

**Cloned pages share Design Options class names.** On a site built by duplicating a template page,
many pages carry identical `vc_custom_` classes. That is normal and harmless, because each page holds
its own copy of the styling. Do not tidy them.

## New pages start as a duplicate

A page created from nothing through the API has none of WPBakery's page settings, so it may open in
the classic editor rather than the WPBakery one *(confirm)*. **A new page is therefore made by a
person duplicating its reference page in wp-admin** (with the site's duplicate page plugin if it has
one), then its content is replaced through the connection. The duplicate carries the reference
page's settings and its Design Options styling, and only the copy changes.

## Theme and add-on elements

An inherited WPBakery site usually has three tiers of element, and the inventory says which tier
each element on the page belongs to:

1. **WPBakery's own elements** (`vc_` and `wpb_` classes).
2. **Theme elements**, often registered by a companion functions plugin that ships with the theme.
   Only valid while that theme and plugin are active.
3. **Add-on bundles** that extend WPBakery with extra elements, usually from a third party.

Tiers 2 and 3 are where an abandoned theme or add-on bites. **Record whether the theme and each
add-on are still sold and maintained.** An element from an abandoned product works today, and nobody
will fix it if a WordPress update breaks it.

## Version, bundling and updates

- **WPBakery is often bundled with a commercial theme.** A bundled copy usually has its own licence
  registration and automatic updates switched off, and gets updates only through new theme releases.
  If the theme is abandoned, so is that route. A direct WPBakery licence is the only other one.
- **The operator may decide not to update WPBakery.** That is a legitimate call on an inherited site,
  and this skill works on any version, because the vocabulary is read from whatever is installed.
- **Known security issues in the installed version are reported, not fixed silently.** Record any
  that apply and what limits their exposure (for example, whether public account sign-up is closed),
  and let a person decide.
- **A WordPress core update on staging comes before the first write**, so the first-page proof covers
  both.
- WPBakery 9.0 (July 2026) rebuilt its settings system. Its vendor says existing pages keep working,
  but an older theme's or add-on's elements were never tested against it by their authors. **Any major
  WPBakery update is tested on a copy first.**

## Design tokens on WPBakery

WPBakery has no real token layer. Colours and fonts come from a mix of the theme's options panel and
stylesheet, WPBakery's own settings, and raw values typed into each element's Design Options.

- **Match the site's existing values rather than introducing new ones.** Copy the Design Options and
  classes of the equivalent element on the reference page.
- **Prefer the theme's classes** (an element's "Extra class name" field) over new per-element values
  where the theme provides them.
- **Do not change the theme's options or WPBakery's settings while working on a page.** Either one
  restyles the whole site.
- The token rule in `.claude/CLAUDE.md` still applies. On most WPBakery sites few tokens exist, so the
  working rule is: no value that does not already appear on a sibling page.
- Where this kit introduces a new class of its own, `.claude/reference/class-naming.md` applies.
  Where the site already has its own classes, **match the site**; never rename the client's classes.

## The write path

WPBakery has no documented layout-write interface for an outside agent. Version 8.3 lists an "API for
AI integration" in its release notes; what it exposes is unconfirmed, so do not assume it is a write
path. It is not needed: because the layout is ordinary page content, **WordPress's own REST API is
the write path**, the connection in `.claude/connections/wordpress-rest.md`, through
`.claude/tools/create-post.py`.

- Read with the connection's read capability, which returns the raw shortcodes. The public page is
  HTML with the shortcodes already expanded, and is useless for learning the syntax.
- Use an administrator's Application Password. A user without permission to post unfiltered HTML can
  have markup stripped from the content on save.
- Inherited sites often have a security plugin that blocks the REST API for logged-out visitors, and
  some also switch off Application Passwords. **Check this when connecting**, before planning around
  the API. The connection file lists what SUFWB had (Wordfence, Admin and Site Enhancements, and a
  theme shortcode that broke rendered reads).
- **Keep each page's layout as a file** (`build-log/layouts/<slug>-<id>.txt`) and send that file.
  Never build a layout to send from `--read` output captured by the shell: on Windows it doubles
  every line break, and WordPress stores them doubled. After any write, byte-compare the stored
  layout with the file.

**No third-party write plugin.** Never install the bridge on a WPBakery site. It would add full PHP
execution reach for nothing the site's own API does not already do.

## Moving a page between environments

Shortcodes are portable plain text, so a page moves as its raw content. Three things do not travel,
and the report names each one:

- **Media.** Attachment IDs differ between sites. Every `image=` and gallery ID is remapped to the
  live site's, and any missing image uploaded there.
- **Design Options styling.** Rebuilt on the live site the same way as on the copy.
- **Theme and add-on elements.** The same theme, functions plugin and add-ons are active on the live
  site, at the same versions.

**A person does the move to the live site**, backed up, as the `existing-site-page` skill describes.
No agent writes to the live site.

## The ways to target WPBakery, ranked safest first

1. **The WPBakery editor's own interface**, driven by a person. Rebuilds the Design Options styling
   itself. The baseline.
2. **Read the raw shortcodes** of the site's pages to learn its vocabulary. Read-only is always safe,
   and it is the step that prevents the wrong-version failure.
3. **Replace the copy on an existing page, or on a person's duplicate of one.** The structure is
   known-good and keeps its own Design Options, so only words change. **This is the default agent
   path**, for edits, rebuilds and new pages alike.
4. **Restructure a page** (add, remove or reorder rows and elements), using only elements and syntax
   already on the site. Then rebuild the Design Options styling and verify in the editor.
5. **A page written from nothing.** Same rules as tier 4, with nothing known-good to start from, and
   it may not open in the WPBakery editor at all. Snapshot first, and only with the operator's
   agreement.
6. **Direct database writes** to the page content or to WPBakery's postmeta. Never through this kit.
   The REST path exists.

## Command and write safety

- **Snapshot before every write** that overwrites a page. The connection's tool does it itself before
  every update.
- **Clear every cache layer after a write**: the caching plugin, and any CDN in front of the site that
  caches pages. Long cache lifetimes are common on these sites, and visitors can see the old page for
  days. The check in `.claude/CLAUDE.md` proves it worked.
- **Never write to the live site.** Staging or a disposable copy only; a person promotes.
- **Never change WPBakery's settings or the theme's options** while working on a page.
- Pin the WordPress, WPBakery, theme, child theme, functions plugin and add-on versions on the copy to
  match the live site.

## TODO (confirm on the real site, do not assume)

What SUFWB (WPBakery 8.7.1, October 2026) settled is noted against each. One site is evidence, not
proof for the next, so still confirm on the first page.

- The WPBakery version, and whether it is bundled with the theme or separately licensed.
- Every element in use, from the raw shortcodes of every page, split into WPBakery, theme and add-on
  tiers.
- Whether a REST API save rebuilds `_wpb_shortcodes_custom_css` on this version, or a person's Update
  click is needed per page. *SUFWB: it does not; Update needed, except on a page with no stored
  styling.*
- Whether a page created through the API, rather than duplicated, opens in the WPBakery editor.
  *SUFWB: not tested; every new page was a person's duplicate. Layouts written through the API into
  existing empty pages opened in the editor as elements.*
- Whether page Custom CSS, page Custom JS and Additional CSS can be written through the API. *SUFWB:
  none of them; a person pastes each.*
- Whether the theme's title band is a separate setting from the page template. *SUFWB: yes.*
- Whether the backend editor exposes the element registry to a logged-in browser, if the registry is
  ever needed.
- Whether a security plugin blocks the REST API or Application Passwords.
- Which retired elements exist on the site.
- Whether the theme and each add-on are still sold and maintained.
- Which cache layers are active, and how each is cleared.
