---
name: gutenberg-limits
description: The WordPress block editor's constraints as an instruction, so a page stays within what a block theme can build editably. Use when adding, rebuilding or editing pages on an existing client site built with Gutenberg blocks and a block theme (full site editing), rather than with Elementor or Breakdance. Covers how block markup is stored, theme.json as the token layer, block validation and the ACF blind spot, the REST API write path, and the ranked safe ways to write. A block theme is not a build target for new sites here; confirm theme-specific details on the real site rather than assuming them.
---

# Gutenberg and block theme limits

The third sibling to `breakdance-limits` and `elementor-limits`. It keeps a page buildable and
keeps an agent inside the safe envelope.

**A block theme is not one of the agency's build targets for a new site.** The agency builds new
sites on WordPress plus Breakdance. This skill exists for a different job: **adding or rebuilding
pages on an existing client site that is already built as a block theme.** Never propose a block
theme for a new build.

The project's builder file (`.claude/builders/block-theme.md`) holds the short version that loads
into every chat. This is the detail behind it.

## Recognising one

Check the rendered source of any page. A block theme site shows:

- Layout classes in the form `wp-block-group`, `wp-block-columns`, `wp-block-cover`,
  `wp-block-query`, and so on.
- `wp-block-template-part` wrappers around the header and footer.
- CSS custom properties in the form `--wp--preset--color--primary`.
- No `elementor-` classes and no `bde-` or `breakdance` classes.

If those are present, this skill applies and the other two do not.

## How a block theme stores content

This is the part that makes block themes materially safer than either page builder, and it is
worth understanding before touching anything.

| What | Where it lives | Format |
|------|----------------|--------|
| Page and post layout | The `post_content` column of the post | Block markup |
| Page templates | The `wp_template` post type | Block markup |
| Header, footer, reusable regions | The `wp_template_part` post type | Block markup |
| Navigation menus | The `wp_navigation` post type | Block markup |
| Synced patterns (reusable blocks) | The `wp_block` post type | Block markup |
| The token layer | `theme.json` in the theme, with user overrides in `wp_global_styles` | JSON |

**Block markup is plain HTML annotated with HTML comments.** A group block looks like this:

```html
<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group"><!-- wp:heading -->
<h2 class="wp-block-heading">Heading</h2>
<!-- /wp:heading --></div>
<!-- /wp:group -->
```

The JSON after the block name is the block's attributes. The HTML between the delimiters is the
saved output. **This is readable, diffable, portable text.** There is no opaque serialised blob to
reverse-engineer, which is the single biggest difference from Breakdance and from Elementor.

**Never hand-write PHP template files to produce layout.** In a block theme, templates are block
markup in the database or `.html` files in the theme. Adding PHP is a security risk and the editor
will not see it.

## theme.json is the token layer

`theme.json` defines the site's palette, typography scale, spacing scale and layout widths.
WordPress compiles them into CSS custom properties with a predictable naming shape:

- `--wp--preset--color--<slug>`
- `--wp--preset--font-family--<slug>`
- `--wp--preset--font-size--<slug>`
- `--wp--preset--spacing--<slug>`

Blocks reference these by slug, not by value. A paragraph coloured from the palette carries
`has-primary-color`, not a hex code.

This means **the token contract the agency requires already exists on any block theme site, and it
is machine-readable.** Read it before building. The presets can be read from the rendered CSS of any
public page without login access, which makes a first-pass inventory cheap.

**On an existing site the tokens are not yours to change.** Changing a `theme.json` value restyles
every page. That is a deliberate, human-approved act, never a side effect of adding a page.

**Never write a raw hex, font size or spacing value into block markup where a preset slug exists.**
That is the token rule in `.claude/CLAUDE.md`, and it applies here exactly as it does on every
builder.

## Block vocabulary

Three tiers, and you must know which tier each block on the page belongs to:

1. **Core blocks.** Shipped with WordPress. Group, Columns, Cover, Heading, Paragraph, Image,
   Buttons, List, Separator, Spacer, Query Loop, Navigation, Template Part, and the rest. Their
   markup is documented and stable across versions. Most of a typical block theme page is core
   blocks.
2. **Theme and plugin blocks.** Registered by the active theme or by a block library plugin. Their
   markup is specific to that theme or plugin and is only valid where it is installed and active.
3. **ACF blocks.** Registered through Advanced Custom Fields. **Their field data is stored as JSON
   in the block comment's attributes, under a `data` key**, and the output is rendered by a PHP
   template at display time. You cannot infer the field names from the rendered HTML. **You must
   read an existing instance of the block to learn its schema before writing a new one.**

**Enumerate the vocabulary before building, and compose only from it.** An agent with no inventory
falls back to the primitives it always knows and hand-nests them into a bespoke pile. It renders, it
matches nothing, and it reuses nothing. That failure is the same on every builder.

If the page needs something with no existing equivalent, such as a table, numbered steps or a run of
questions and answers the site has no pattern for, **stop and ask.** Do not improvise a bespoke
section to fill the gap.

## Block validation, the one failure mode that matters

WordPress checks saved block markup against what the block would generate now. When they disagree,
the editor shows **"This block contains unexpected or invalid content"** and offers to convert the
block to a plain HTML block.

Once a block is converted to HTML, **the client can no longer edit it as a block**. The page still
renders, so this failure is easy to miss on a visual check and easy for the client to hit weeks
later.

Three consequences:

- **Match the attribute shape exactly.** A missing or misspelled attribute, or markup that does not
  match the attributes, will invalidate the block.
- **Always open a written page in the editor and confirm no validation warnings** before calling it
  done. Rendering correctly is not sufficient evidence.
- **Pattern from an existing block instance** rather than writing markup from memory. The site's
  own saved markup is known-valid for the versions installed.

**Validation happens in the editor, not on save.** The REST API accepts invalid block markup without
complaint. Nothing flags it until someone opens the page in the editor, which is why that step is
the check.

**The editor check does not cover ACF blocks.** An ACF block's content is data in the block comment,
rendered by a PHP template when the page loads, not saved HTML. A misspelled field name is unlikely
to raise a validation warning; the field is more likely to render empty. For every ACF block,
confirm on the rendered page that each field actually shows its content. Confirm this behaviour on
the real site.

## The REST API is the first-party write path

This is the block theme's real advantage, and it is the direct answer to the question that
Breakdance never had a good answer for.

WordPress core exposes every part of the layout through its own REST API, gated by capability checks
and authenticated with an **Application Password**, which is a revocable per-person credential
generated on a user profile:

| Endpoint | What it reaches |
|----------|-----------------|
| `/wp/v2/pages`, `/wp/v2/posts`, and any custom post type | Page and post block markup |
| `/wp/v2/templates` | Page templates |
| `/wp/v2/template-parts` | Header, footer and reusable regions |
| `/wp/v2/navigation` | Menus |
| `/wp/v2/blocks` | Synced patterns |
| `/wp/v2/global-styles` | The user layer over `theme.json` |

Read the raw block markup with `?context=edit`, which returns `content.raw` rather than the rendered
HTML. This requires authentication; the public, unauthenticated response only gives you
`content.rendered`, which has the block comments stripped and is therefore not enough to learn a
block's attributes.

**No third-party plugin is needed, and no raw PHP execution surface has to be opened.** In this kit
the connection is `.claude/connections/wordpress-rest.md`, and its tool is
`.claude/tools/create-post.py`, which reads, snapshots and writes a page through these endpoints.

Confirm on each site that `/wp-json/` is reachable and that the templates endpoints are locked down
to authenticated administrators. A site that serves templates or global styles to an unauthenticated
request is misconfigured, and that is worth reporting.

## Moving a page between environments

Block markup is portable plain text, so a single page moves cleanly: its `content.raw` from one site
is valid on another running the same theme and block plugins. **A person does the move to the live
site**, pasting the markup into the editor's code view or by whatever route is recorded for the
project. No agent writes to the live site.

Two things do **not** travel and must be checked every time:

- **Media.** Images are referenced by attachment ID and URL. An ID that exists on the source may be a
  different image, or nothing, on the target. Confirm every image resolves, and re-upload where it
  does not.
- **Anything the block depends on.** A theme block, a plugin block or an ACF block needs that theme
  or plugin active on the target, at a compatible version, or the block will fail validation.

## The ways to target a block theme, ranked safest first

1. **The block editor's own interface**, driven by a human. Respects all validation. The baseline.
2. **REST API write of `post_content`**, patterned on an existing page's markup. First-party,
   permission-gated, no PHP execution. **This is the default agent path.**
3. **Read `content.raw`** to learn the site's vocabulary and a block's attribute schema. Read-only is
   always safe and is how the inventory is taken.
4. **REST API write to templates or template parts.** Same mechanism, but the blast radius is every
   page using that template. Snapshot first, ask first, and treat it as a change to shared
   infrastructure rather than a page edit.
5. **REST API write to global styles.** This is a token change. It restyles the whole site.
   Human-approved only, never a side effect.
6. **Direct database write to `post_content` (last resort).** Bypasses every check WordPress would
   run. There is almost never a reason, because the REST path exists. Recovery path first and
   human-reviewed.

Note what is absent from this list: there is no tier requiring a third-party plugin with full PHP and
filesystem privileges. Do not introduce one for a block theme site. It buys nothing here, and it
carries the blast radius the bridge connection's own rules warn about
(`.claude/connections/bridge.md`).

## Command and write safety

- **A snapshot of every existing page before it is overwritten, never waived.** `create-post.py`
  takes one itself before every update and refuses to write if it cannot. A brand new page on a
  disposable copy is the only case where the recovery path may be waived, recorded, per
  `.claude/CLAUDE.md`.
- **Check the public page after every write.** Caching plugins do not always purge after an API
  write, and the site will silently serve the old page. The check in `.claude/CLAUDE.md` catches it
  whichever plugin the site runs.
- **Never write to the live site.** Build on staging or a disposable copy; a person promotes.
- **Confirm the WordPress version, the theme version and every block-providing plugin version**, and
  pin them in the builder file.
- Where we introduce a new class of our own, the scope prefix convention in
  `.claude/reference/class-naming.md` applies. Where the site already has its own classes, **match
  the site**; do not rename the client's existing classes while adding or rebuilding a page.

## TODO (confirm on the real site, do not assume)

- The full block vocabulary in use, split into core, theme, plugin and ACF tiers.
- The attribute schema of every ACF block the page needs, read from an existing instance.
- Whether a misspelled ACF field renders empty with no warning, as expected.
- Whether the site uses synced patterns as reusable units, and which.
- The theme's `theme.json` token slugs and values.
- Which caching plugin is active, and whether it purges by itself after an API write.
- The REST base of every custom post type involved, from `/wp-json/wp/v2/types`.
- Whether the theme is commercially licensed, and whether the licence is current, before relying on
  theme blocks or theme updates.
