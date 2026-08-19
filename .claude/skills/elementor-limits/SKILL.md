---
name: elementor-limits
description: The Elementor builder's constraints as an instruction, so a page stays within what Elementor can build editably. Use when adding or editing a page on an existing client site already built in Elementor, or when deciding how an agent may safely touch Elementor. Covers how Elementor stores layout, the two structure generations, the token layer, the first-party template transfer path, and the ranked safe ways to write. Elementor is not a build target for new sites here; confirm every version-specific detail on the real site rather than assuming it.
---

# Elementor limits

The Elementor counterpart to the `breakdance-limits` skill. It keeps a page
buildable and keeps an agent inside the safe envelope.

**Elementor is not one of the agency's build targets for a new site.** The agency
builds new sites on WordPress plus Breakdance. This skill exists for a different
job: **adding or editing a page on an existing client site that is already built
in Elementor.** Never propose Elementor for a new build.

**Nothing on this page uses the Breakdance 3.0 native connection.** That path and
its tools (`html-to-page`, `insert-stylesheet`, `get-post-tree`,
`set-global-settings` and the rest) exist only on a Breakdance 3.0 site running
the Agent Connector. They do not exist on Elementor, and they do not exist on
Breakdance 2.x. On this path the layout-write capability is a third-party bridge
on a disposable local copy of the site, and everything in
`.claude/reference/limitations.md` about the Breakdance beta is about a different
path and does not apply here.

## How Elementor stores content

- Layout is **JSON in the `_elementor_data` postmeta** on each post or page. It is
  data, not template files. Never hand-write PHP templates to produce layout.
- Page-level settings sit in `_elementor_page_settings`.
- **Elementor generates a CSS file per post**, normally under
  `uploads/elementor/css/`. A database write that does not regenerate that CSS can
  render stale or unstyled. The manual fix is **Elementor > Tools > Regenerate CSS
  and Data** in wp-admin, which is a human click, not something the build runs.
- The active **Kit** holds the site-wide settings, meaning the Global Colours and
  Global Fonts under Site Settings. That is the token layer.

Confirm the exact CSS path and the exact wp-admin menu wording on the site in
front of you. Both have moved between Elementor versions.

## Element vocabulary

Elementor's structure has two generations, and one site can contain both:

- **Classic:** Section, then Column, then Widget.
- **Container:** Container, then Widget, with nested containers in place of the
  section and column pair. Later versions add a grid mode.

**Establish which generation the site uses before building anything**, by opening
a representative existing page and reading its structure. Match what the site
already does. Dropping containers into a section-and-column site produces a page
that does not match its siblings and that the client edits differently from every
other page, which is exactly the outcome this whole path exists to avoid.

Widgets are the atomic elements (Heading, Text Editor, Image, Button, Icon Box and
so on). **Templates** and, on the Pro tier, **Global Widgets** are the reusable
units. Whether this site actually uses either is a thing to find out, not assume.

## The lesson that matters most: compose, do not re-invent

An agent given no inventory falls back to the primitives it always knows, meaning
heading, text, image and button, and hand-nests them into a bespoke pile. The
result is one level above raw HTML. It renders, and it matches nothing, reuses
nothing, and is miserable to maintain. This is the same failure as writing a raw
hex value instead of a token name: the higher-level vocabulary existed and the
agent never went and read it.

**The site's own pages, templates and global widgets are the vocabulary.** Before
building anything:

1. **Enumerate what exists.** The saved Templates, any Global Widgets, and the
   structure of one or two representative pages of the type being added.
2. **Pattern from an existing page.** Duplicate the closest match and adapt it. Do
   not compose from bare widgets when a matching page already exists.
3. **If the page needs something with no existing equivalent, stop and ask.** Do
   not improvise a bespoke section to fill the gap.

The full procedure is in the `existing-site-page` skill. This is the reason it
exists.

## Design tokens on Elementor

- **Site Settings, meaning the Kit, is the token layer**: Global Colours and
  Global Fonts. That is the semantic tier, the same job Breakdance Global Settings
  does on the other target.
- Where a widget references a global colour or font it updates centrally. Where it
  carries a local override it does not. **Prefer a global reference every time.**
- On an existing site **the tokens already exist and are not yours to change.**
  Read them and use them. Changing a global colour restyles every page on the
  site, so it is a deliberate, human-approved act and never a side effect of
  adding one page.

## The transfer path, which is Elementor's real advantage

Elementor has a **first-party single-page transfer path**, which Breakdance lacks:

1. Save the finished page as a **Template**, using Save as Template on the page.
2. **Export that template as a JSON file.**
3. **Import the JSON** on the target site, under Templates and then Saved
   Templates.
4. Apply it to the target page, then regenerate CSS.

That moves one page without any raw database write and it is supported by the
vendor. **Prefer it over any postmeta copy.** It is the main reason an Elementor
page addition is materially lower risk than the Breakdance 2.x equivalent, and it
is why the Elementor site is the sensible one to run this path on first.

Check these every time, because each one has a way of surfacing only after the
import:

- **Images and media are referenced, not embedded.** An imported template can
  point at the source site's attachments. Confirm every image resolves on the
  target and re-upload the ones that do not.
- **Elementor Pro widgets inside a template need Pro active on the target.**
  Confirm the licence covers what the page uses before promising the transfer will
  work.
- **Version skew breaks imports.** Build on a copy running the same Elementor
  version, and the same Pro version, as the target.
- Whether the export carries page-level settings from `_elementor_page_settings`
  is version-dependent. **Confirm on the first real transfer** and record what you
  find, rather than assuming the page arrives fully configured.

## The ways to target Elementor, ranked safest first

Prefer the highest-ranked method that can do the job.

1. **Template export and import as JSON.** First-party, no raw write. The default.
2. **Elementor's own interface**, driven by a person, or by browser automation
   where that is genuinely needed. It respects the builder's own validation.
3. **Reading `_elementor_data`** to understand an existing page's structure.
   Read-only is always safe and it is how the site's vocabulary gets learnt.
4. **A constrained patch of `_elementor_data`** on a copy of a known-good page.
   Change values inside a structure that already works, never restructure.
   Recovery path first, human-reviewed.
5. **A raw `_elementor_data` write from scratch, as a last resort.** Highest risk.
   A malformed write destroys the layout. Recovery path first, human-reviewed, and
   regenerate CSS afterwards.

## Write safety

- **A recovery path exists before every write** that can affect the database. On
  the disposable local copy that can be the copy itself, since it is regenerable
  and there is nothing to restore. On the client's real site it is never waivable.
  See `.claude/CLAUDE.md` on recovery paths.
- **Regenerate CSS after any database write** to layout or to global settings, or
  the site can serve stale styling.
- **Purge the page cache as well** where a caching plugin is active. A postmeta
  write does not fire `save_post`, so an automatic purge may not happen.
- **Never write to the live site.** Build on the disposable local copy; a person
  promotes.
- Confirm the **Elementor version, and whether Pro is active**, before relying on
  any Pro-only feature.

## Images on an existing Elementor site

The agency image process does not change with the builder. The order is the same
one in `.claude/CLAUDE.md` and `.claude/reference/build-standards.md`:

- **Where the page has a design**, pull the asset from the Figma frame, rename it
  to a descriptive kebab-case filename derived from the design, resize it to about
  twice its display width, compress it, then upload it and reference it.
- **Where the page has no design**, which is the usual case on this path, build a
  placeholder block per `.claude/reference/image-placeholder.md` and log it under
  Outstanding images. Do not invent or generate an image at build time.
- **Uploading works the same way.** `.claude/tools/optimize-and-upload.py` posts to
  the WordPress media REST API with an Application Password. It is builder-neutral,
  so it works on an Elementor site exactly as it does on a Breakdance one, and it
  is scoped to media: it can create an attachment and it cannot delete one. It
  reads the site URL, username and password from the local Claude config, and
  accepts `WP_SITE_URL`, `WP_API_USERNAME` and `WP_API_PASSWORD` as overrides,
  which is how it is pointed at a local copy.
- **Media uploaded to the local copy does not travel with a template export.**
  Either upload the images to the target as a separate step and repoint them, or
  hand the named files to a person to upload in wp-admin. Decide which before the
  transfer, not after.
- SVGs are inlined rather than uploaded, because WordPress blocks SVG uploads by
  default.

## Do not assume, confirm on the real site

Record each of these in the client project once established. Do not hardcode any
of them from this file.

- Which structure generation the site uses, classic or container, and whether it
  mixes both.
- The Elementor version, the Elementor Pro version, and whether Pro is active.
  Pin the local copy to match.
- Whether the site uses saved Templates, Global Widgets, both, or neither, as its
  reusable units.
- The exact wp-admin path for Regenerate CSS and Data on this version.
- The bridge plugin's actual Elementor abilities on the licence in use. Novamira
  comes from the Dynamic Content for Elementor team, so Elementor coverage is
  plausible, but this repo's own docs confirm only core abilities plus a
  Breakdance specialisation (`docs/19_implementation_runbook.md`). **Verify against
  the installed plugin before relying on any Elementor-specific ability**, and if
  it turns out there is none, the honest answer is that the build is read-only on
  this site and the page is assembled another way.

## See also

- the `existing-site-page` skill, the procedure this one supports
- the `breakdance-limits` skill, the equivalent for the Breakdance target,
  including the Breakdance 3.0 native path that does not apply here
- `.claude/reference/build-standards.md`, the standards a page is held to whatever
  the builder
- `prompts/existing-site-page.md`, the paste-in job
