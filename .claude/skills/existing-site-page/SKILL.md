---
name: existing-site-page
description: Add a page to, or rebuild existing pages on, a client website that is already built and live, matching what the site already does rather than building from a design. Use when the job is on an existing Elementor site, an existing Breakdance 2.x site, an existing WordPress block theme (Gutenberg, full site editing) site, or an existing WPBakery site. Covers working on a copy that is never the live site, connecting through the project's chosen connection, taking a read-only inventory of the site's own patterns, building by patterning an existing page, rebuilding a page in place without losing its address, buttons or links, and handing the result to a person to put live. The inventory step is a hard stop and is the point of the procedure.
---

# Add or rebuild a page on an existing site

A different job from a new build, and it fails in a different way. There is no design system to
establish and no tokens to sync, because **the site already has them and the page has to match.**
The measure of success is that a visitor, and the client in the editor, cannot tell which page was
added or rebuilt later.

This procedure covers four builders:

- **Elementor.** Read `elementor-limits` alongside this.
- **Breakdance 2.x**, which has no native connection. Read `breakdance-limits`, where the ranked
  write methods and the absence of a sanctioned layout API apply just as they do on 3.0. On a
  Breakdance 3.0 site running the Agent Connector, use the normal build path in
  `prompts/new-page.md` instead: it is first-party, better proven and does not need any of this.
- **A WordPress block theme.** Read `gutenberg-limits`. This is the safest of the four: the layout
  is readable block markup and WordPress's own API writes it, with no third-party plugin.
- **WPBakery**, usually bundled with an older commercial theme. Read `wpbakery-limits`. Nearly as
  safe: the layout is shortcodes, readable plain text in the page's own content, and WordPress's own
  API writes it. What it lacks is any check on what is written, and its Design Options styling may
  need a person's Update click to rebuild.

**Identify which one before anything else**, from the rendered source of any page. `elementor-`
classes mean Elementor. `breakdance` or `bde-` classes mean Breakdance. `wp-block-` classes with
`wp-block-template-part` wrappers mean a block theme. `vc_row` and `wpb_` classes, with a "Powered by
WPBakery Page Builder" generator tag, mean WPBakery. It has to agree with the builder file loaded
into this project. If it does not, stop and say so: the wrong builder file means every rule loaded
into this chat is wrong.

It covers two jobs:

- **Adding a page**, which is the loop below.
- **Rebuilding existing pages in place**: the page keeps its address and gets new copy. That is a
  higher-risk job with its own rules, in "Rebuilding an existing page" further down, and its own
  prompt, `prompts/rebuild-existing-pages.md`.

## Which connection, and which tools exist

The project's connection file (`.claude/connections/`) says how each capability is done on this
site, and which builders it supports. Read it before starting. If it does not list this site's
builder, stop and ask.

- **Elementor and Breakdance 2.x** use **the bridge** (`connections/bridge.md`): a third-party plugin
  connected to a disposable local copy of the site. It is reverse-engineering an undocumented
  internal format, which is managed risk rather than removed risk. This procedure calls it "the
  bridge" rather than naming a vendor, so it stays swappable.
- **A block theme or WPBakery** uses **the WordPress REST API** (`connections/wordpress-rest.md`): the
  site's own built-in interface, with an Application Password. No plugin is installed. **Never install
  the bridge on a block theme or WPBakery site.** It would add full PHP execution reach for nothing the site's own
  API does not already do.

Say this plainly to yourself before starting, because getting it wrong wastes a session: **the
Breakdance 3.0 native tools do not exist on this path.** There is no `html-to-page`, no
`insert-stylesheet`, no `get-post-tree`, no `set-global-settings`, no `get-breakpoints`.

That means `.claude/reference/limitations.md` has to be read selectively rather than as a whole. Its
**Breakdance 3.0.0-beta.1 native MCP** section is about a different path and none of it applies
here. Its other sections still do, and are worth reading before you hit them:

- **WordPress:** SVG uploads are blocked by default, so SVGs are inlined.
- **Hosting firewall:** on the DWS staging host, a write whose content injects a `<script>` tag is
  refused with a 403. Do not tune the content to get past it.
- **Figma:** the mesh-gradient blind spot and the `get_metadata` truncation, on the minority of these
  jobs that come with a design.
- **Browser and QA:** the orphaned Chrome profile lock, lazy-loaded images not fetching in a capture,
  and `resize_page` clamping at about 512px.
- **Claude Code sessions:** no automatic lock between chats.

**The bridge is never installed on the live client site.** Not to read from it, not to "just make
one small change", not temporarily. It carries site-privileged abilities, its sandbox is not a
security boundary, and the whole safety model on that path is that it only ever touches a copy that
can be thrown away. This is the same rule as removing the Agent Connector before a staging site goes
live, and it is the shortcut most likely to be reached for when a transfer turns fiddly.

Two capabilities work the same on every path, because they go through WordPress rather than the
builder: `.claude/tools/optimize-and-upload.py` for media, and `.claude/tools/create-post.py` for
posts. Both use the WordPress REST interface with an Application Password and are builder-neutral.
On a block theme or WPBakery, `create-post.py` is also the layout path, because the post body is the
layout.

## The design source, when there is no design

Most of these jobs have no Figma frame, and that is expected rather than a shortfall. **The
reference is then an existing page of the same type on the site itself.** Sitting a new page next to
a built sibling and matching its structure is the correct method here, because on an existing site
the site's own pages *are* the design system. `.claude/design-source/existing-site.md` holds the
short version that loads into every chat.

Where a design file does exist, use it, but **take the inventory first anyway.** The page still gets
built from the site's existing components, not from new ones invented to chase a drawing.

## The inventory is a hard stop

This is the reason the procedure exists, so it is not a step to compress.

An agent with no inventory falls back to the primitives it always knows, meaning heading, text,
image and button, and hand-nests them into a bespoke pile. It renders. It matches nothing, reuses
nothing, and is miserable for the client to edit. **This has already happened on a real build.** It
is the same failure as emitting a raw hex value instead of a token name: the higher-level vocabulary
was right there and the agent never went and read it.

So the rule is absolute:

- **Enumerate what the site already has, and show it to the operator, before building anything.**
- **Compose only from that vocabulary.**
- **If something the page needs has no existing equivalent, stop and ask.** The usual ones are a
  table, a numbered list of steps, and a run of questions and answers, where the copy has them and
  the site has no pattern for them. Do not improvise a bespoke section to fill the gap, and do not
  add or change a global setting, token or shared part to make one possible.

A page built without the inventory is not a page that needs tidying up. It is a page that gets
thrown away.

## Where the words come from

The content rule does not relax because the site already exists. It is the same rule as everywhere
else in this kit, and it is in `.claude/CLAUDE.md`, `START-HERE.md` and `prompts/new-page.md`.

- **Build from the approved copy in `content/`**, one markdown file per page.
- **If there is no file for this page, stop.** Tell the operator to request it from ZilvaEdge through
  ClickUp, where it comes back as released content. Do not write the copy, and **do not build the
  page on placeholder text meaning to swap it later.** Improvised copy looks finished, passes a
  visual review, and is not found out until the client reads it.
- **Microcopy is the only exception**, meaning calls to action, button labels and short connective
  copy. Anything written directly goes in `CONTENT_CHANGELOG.md` in the same session.

An existing site raises one extra question the new-build path never has to ask: the site is live,
so its current pages already carry copy nobody in this repo released. That copy is read as a
**pattern to match in tone and structure**, and it is never lifted wholesale into a new page as a
substitute for released content.

## The loop, for adding a page

### 1. Work on a copy, never the live site

- **Elementor and Breakdance 2.x:** a copy of the **whole site** in a disposable local environment,
  using LocalWP, All-in-One WP Migration, or the host's own pull. A settings-only export is **not**
  enough: it carries the tokens and none of the page patterns that the inventory needs, and none of
  the version context.
- **Block theme or WPBakery:** a staging copy of the site is enough, and it works over HTTPS with no
  configuration change. A local copy works too.
- **Match the versions.** The copy runs the same builder or theme version and the same plugins as the
  live site. Version skew is the most common reason a finished page will not move cleanly at the end.
- **This is a human step.** The operator makes the copy; the build does not.

### 2. Connect to the copy, and only to the copy

Use the setup prompt the connection file names: `prompts/connect-bridge.md` for the bridge,
`prompts/connect-rest.md` for the WordPress REST API. Both arm what has to be armed alongside the
connection. Use them rather than improvising the sequence.

- On a LocalWP copy, Application Passwords need either HTTPS or
  `define( 'WP_ENVIRONMENT_TYPE', 'local' );` in `wp-config.php`, followed by a restart of the site
  so PHP reloads the file. **The build cannot do this.** `wp-config.php` is a protected path, denied
  in `.claude/settings.json` and blocked by the `.claude/hooks/block-protected-paths.sh` hook, so it
  is a human action in the Local interface. `START-HERE.md` has the full troubleshooting order,
  including the security-plugin trap that is the most common cause of the Application Password
  screen refusing.
- **A copied site often arrives with the bridge dormant.** Copying or migrating can leave its
  abilities switched off, its domain lock still pointing at the live domain, and safe mode engaged.
  `prompts/connect-bridge.md` walks through it. This has caught people out before.
- **Confirm the target before any write**, with the connection's "confirm the environment"
  capability. Show the operator what came back, with the site address visible in it. Do not write
  anything until the operator confirms it is the copy. A copy's address is evidence; a plausible
  assumption is not.

### 3. Take the inventory, read-only, and show it

Record all of this in the project before building, and put it in front of the operator in plain
words:

- The **builder and its version**, and whether the Pro tier is active. On a block theme: the
  WordPress version, the theme and child theme versions, and every block-providing plugin version.
  On WPBakery: the WordPress and WPBakery versions, whether WPBakery is bundled with the theme, the
  theme and child theme, every plugin that adds WPBakery elements, and whether the theme and each
  add-on are still sold and maintained.
- The **structure generation** in use. On Elementor, classic section-and-column or container. On
  Breakdance 2.x, how Sections, Divs and Columns are actually used on this site. On a block theme,
  which core layout blocks carry the structure, and which blocks are theme, plugin or ACF blocks
  rather than core. On WPBakery, which elements carry the structure, and which are WPBakery's own,
  the theme's or an add-on's.
- The **reusable units that already exist**: saved Templates, Global Widgets, Global Blocks, or on a
  block theme the template parts and synced patterns.
- The **token layer**, meaning the Elementor Kit's global colours and fonts, the Breakdance Global
  Settings, or on a block theme the `theme.json` presets. WPBakery has none to speak of: read the
  Design Options and classes the sibling pages use instead. **Read them. Do not change them.**
- **On a block theme, the attribute schema of every ACF block the page needs**, read from an existing
  instance's raw markup. ACF field data is JSON inside the block comment and is drawn by a PHP
  template, so it cannot be inferred from the rendered page. This needs the login, and it is the
  most commonly missed step.
- **On WPBakery, the raw shortcodes of every page on the site**, not only the reference page. They
  are the whole vocabulary: every element the site uses, in this version's exact syntax and this
  site's encoding. **Never write WPBakery from memory**; that has already produced wrong-version
  output on a real job. Also list any retired elements the site uses, which are never copied into
  new work.
- The **class naming the site already uses**, so the new page's classes look like they belong.
- The **breakpoints the site itself uses**.
- **One or two representative pages** of the type being added, read structurally in full, as the
  pattern to follow.

Then say plainly what vocabulary the site gives you to work with, and what the page needs that the
site has no equivalent for. That second list is the thing the operator has to make a decision about.

### 4. Build on the copy by patterning an existing page

- **Duplicate the closest existing page and adapt it.** Do not compose from bare elements. This is
  the constrained-patch-on-a-known-good-structure method, and it is far safer than a build from
  scratch. On a block theme that means taking the sibling's raw block markup and changing only the
  copy and the attributes that must change. On WPBakery a person duplicates the sibling in wp-admin
  first, so the new page keeps WPBakery's page settings and Design Options styling, then its
  shortcodes are updated with only the copy changed.
- Reuse the site's existing classes, components and spacing, and reference its existing tokens
  rather than introducing values.
- **Do not change global settings or tokens.** Restyling a global colour changes every page on the
  site. If the page genuinely needs a new shared component or a new token, stop and ask.
- Keep the client's editing experience consistent. The new page has to be editable the same way its
  siblings are, by the same person, in the same editor.
- Apply the standards in `.claude/reference/build-standards.md` that are not builder-specific:
  descriptive class names, one element per body block, hover and focus states, accessibility,
  sensible headings.

### Three standards that read differently on an existing site

These are deliberate departures from a literal reading of `build-standards.md`, not oversights. That
file is written for a site this kit is building from a design, and each of these three assumes
something that is not true here.

- **Breakpoints.** The standard says breakpoints come from `get-breakpoints` and that no `@media`
  query is invented. That tool does not exist on this path, so the breakpoints come from **the
  site's own**, read during the inventory. The underlying rule is unchanged: use the real ones, never
  invent one.
- **Slugs.** The standard sets an agency default of `about-<business-name>` and
  `contact-<business-name>`. That is a default for a site we are creating. On a live site the slug is
  a public URL with history and inbound links, so **match the convention the site already uses** and
  **never rename an existing page's slug**. If the client wants a slug that breaks their own pattern,
  that is their decision to make, with a redirect, and it is not a build decision.
- **Media binding.** The standard says images are referenced by URL rather than bound to the media
  library. That is a workaround for one proven Breakdance 3.0 beta defect and **the reason for it does
  not exist here.** Where the builder and the connection can bind an image to its attachment
  properly, do that, because it gives responsive sizing for free. On a block theme the image block
  binds by attachment id as a matter of course, and so does a WPBakery image element. On the bridge it is **unverified, so confirm it on the
  first image** rather than assuming either way.

### 5. Images

The process is the one in `.claude/reference/build-standards.md`, unchanged, with one addition that
only applies here.

- **With a design**, pull the asset from the design, rename it to a descriptive kebab-case filename,
  resize it to about twice its display width, compress it, then upload and reference it. Write alt
  text from what the design shows, and set it both at upload and on the rendered element per
  `.claude/reference/alt-text-guidelines.md`.
- **With no design**, which is the usual case here, build a **placeholder block** at the correct
  display size per `.claude/reference/image-placeholder.md`, and log it under Outstanding images in
  the page record. Do not invent an image and do not generate one at build time. Real images are
  sourced in the separate pass, `prompts/source-images.md`.
- **Where an existing image on the site is genuinely the right one for this page, reuse the
  attachment that is already there** rather than uploading a second copy. The upload tool cannot
  delete, so a duplicate stays on the site forever.
- **The addition that is specific to this path: media does not travel with a page.** Anything
  uploaded to the copy has to exist on the live site too, and the references repointed, or the page
  arrives with broken images. Decide how before the page moves, and say so in the report.

### 6. Verify on the copy

- **Open the page in the builder's own editor**, not just the rendered page, and confirm it is
  editable the way the builder file says. A page that renders but will not open cleanly has failed.
- **On a block theme this check is not a formality.** The site accepts invalid block markup without
  complaint; only the editor shows "This block contains unexpected or invalid content", and a block
  offered for conversion to HTML still renders correctly. Check every block. Then check every ACF
  field shows its content on the rendered page, because a wrong field name most likely renders
  empty with no warning. Opening the editor needs a login: until a person or a logged-in browser has
  done it, the page is "built, not verified".
- **On WPBakery nothing checks a shortcode when it is saved.** Confirm the rendered page shows no
  visible `[vc_` text, the page opens in the WPBakery backend editor as elements rather than raw
  text, and its `vc_custom_` Design Options rules are in the rendered page head with spacing that
  matches its siblings. If the styling is missing, a person opens the page in the WPBakery editor and
  clicks Update. The editor needs a login, so the same "built, not verified" rule applies.
- **Check the public page shows the new copy**, per `.claude/CLAUDE.md`.
- Check it at each of the site's own breakpoints.
- Compare it against its sibling pages and say honestly where it differs.

### 7. Prepare the move to the live site, then stop

The build prepares the move. **The build does not touch the live site.**

- **Elementor:** save the page as a Template and export the JSON. This is first-party and needs no
  raw write, and it is the clean path. Flag any images that will not resolve on the target and any
  Pro-only widgets used.
- **Block theme:** the page's raw block markup is the whole of it, and it is portable plain text. A
  person creates the page on the live site and pastes the markup into the editor's code view, or the
  project uses whatever route is recorded in `build-log/DECISIONS.md`. Flag any images that will not
  resolve on the live site, and every theme, plugin or ACF block the page depends on, which must be
  active there at the same version.
- **WPBakery:** the page's raw shortcodes are the whole of the layout, and they are portable plain
  text. A person duplicates the reference page on the live site, pastes the shortcodes into the
  duplicate's content *(confirm the editor route on the site)*, saves, then opens it in the WPBakery
  editor and clicks Update so the Design Options styling is rebuilt there. Remap every image ID to
  the live site's, and flag every theme or add-on element the page needs active there.
- **Breakdance 2.x:** there is no equally clean single-page export. Use Breakdance's own template or
  Global Block export where that fits. Copying the one new page's `_breakdance_data` postmeta across
  is the fallback, and it is the last-resort method in the `breakdance-limits` ranking, so it is
  recovery-path first and human-reviewed. A new page has no existing layout to destroy on the live
  site, which makes it lower risk than rebuilding one, but it is not no risk. **Confirm the exact
  export route on the real site rather than assuming one exists.**
- Hand the operator: what to back up on the live site first, the steps in order, and what to clear
  or regenerate afterwards, meaning the builder's cache or CSS, and the page cache.
- **Give every one of those steps as clicks in wp-admin.** `breakdance-limits` says to run
  `wp breakdance clear_cache` after a database write, and that is right, but it is a command line
  instruction and the operator here does not run commands. Find the equivalent in the builder's or
  the caching plugin's settings screen and give that. If no equivalent exists in the interface, say
  so plainly and flag that this step needs a developer, rather than handing over a command the
  operator cannot use.

### 8. A person promotes

**Promotion to the live site is a human, backed-up action.** No agent writes to a live client site,
ever. After the move the operator opens the page in the editor on the live site and confirms it is
still editable there.

## Rebuilding an existing page

The job the loop above is not: **existing pages keep their addresses and get new copy.** Nothing is
new, so everything written overwrites live layout. It needs the inventory above, and these rules on
top, which do not bend.

- **Snapshot every page before it is overwritten, with no waiver**, even on staging. On a block
  theme the connection's tool does it itself before every update and refuses to write if it cannot,
  and it can put a snapshot back. On a connection with no per-page snapshot, a person takes a backup
  before the first page and confirms it.
- **Never change a slug, a status or a parent.** The page keeps its address, stays published if it
  was, and stays where it sits in the site. A rebuild that moves a page is a different job, with
  redirects, and is not a build decision.
- **Read the page's current links before replacing anything.** Record every link on the page, its
  text and its full address. After the write, compare. Every link that was there is still there, or
  its removal is deliberate and named in the report.
- **Conversion buttons are preserved exactly.** Booking, enquiry, call and download buttons keep
  their address **including every query string and tracking parameter**, character for character.
  Their label only changes if the approved copy changes it. A booking link that loses its tracking
  still works, and the client's reporting silently goes wrong.
- **Leave what the copy does not cover.** SEO fields, the featured image, templates, template parts,
  menus and shared blocks are outside a page rebuild. If the copy seems to need one changed, stop
  and ask.
- **Rebuild inside the page's own structure.** The page's existing sections are the first pattern,
  its siblings the second. New copy that needs a section the site has no pattern for is a stop, as
  in the inventory rule.
- **One page, verified, then a pause for the operator after the first.** The first page settles the
  mapping from the copy to the site's patterns; the rest follow it.
- **How the rebuilt pages reach the live site is decided before the first write** and recorded in
  `build-log/DECISIONS.md`: page by page by a person, or a full staging-to-live migration by a
  person or the host. Either way it is a person, and the live site is backed up first.

## Recovery paths on this path

The kit's rule is a recovery path proportionate to what is at stake, and these jobs have two
environments with very different stakes.

- **On a disposable copy, adding a new page:** the copy is regenerable, so there is nothing to
  restore and a snapshot can be waived. Record the waiver.
- **Overwriting any page that already exists**, on a copy or on staging: snapshot it first, never
  waived.
- **On the live client site:** never waivable, no exceptions, and it is a full backup rather than
  builder revisions. This is a site with real traffic and real content, and it is the operator who
  takes the backup before anything is moved there.

## The audit trail

An existing-site page is logged like any other page in this kit.

- **Claim it** in `build-log/ACTIVE.md` before starting.
- **Record it** in `build-log/pages/<slug>.md` from `_TEMPLATE.md`, noting the builder, the
  connection and their versions, the reference page it patterned from, and the inventory findings.
  On a rebuild, also the snapshot file, the link comparison and the conversion buttons checked.
- **Log the move to the live site** in `build-log/BUILD-LOG.md`, including the backup taken on the
  live site and who took it.
- Anything written directly as copy goes in `CONTENT_CHANGELOG.md` the same session.

## Rules

- A copy or staging only. **Never an agent write to a live client site.**
- Confirm you are on the copy with the connection's "confirm the environment" capability before any
  write.
- Take the inventory first. Compose from what exists. Stop and ask rather than inventing.
- Do not change global settings or tokens while adding or rebuilding a page.
- Build from released content in `content/`. Microcopy is the only exception.
- One page at a time, verified before the next.
- On a rebuild: snapshot first, slug untouched, links compared, conversion buttons exact.
- Do not invent builder internals. Where you are unsure how a builder stores or moves something, say
  so and mark it to confirm.
- British and Australian English. No em dashes, no en dashes, no double hyphens in prose. No emojis.

## Confirm per site, do not assume

- The builder and version, and pin the copy to match.
- The connection for this project, and one verified "confirm the environment" call before any write.
- Whether the client's licence covers the Pro features any existing page relies on, for example
  Elementor Pro widgets, Breakdance Pro settings export, a commercial block theme's licence, or
  whether a bundled WPBakery can still be updated.
- The route that actually works for moving a page to the live site on this builder version.
- Whether media references survive the move, and what has to be repointed.
- On a block theme, which caching plugin is active and whether it purges by itself after an API
  write.
- On WPBakery, whether a save through the API rebuilds the Design Options styling, settled on the
  first page and recorded in `build-log/DECISIONS.md`.

## See also

- `prompts/existing-site-page.md` and `prompts/rebuild-existing-pages.md`, the paste-in jobs that run
  this
- the `elementor-limits`, `breakdance-limits`, `gutenberg-limits` and `wpbakery-limits` skills
- `prompts/new-page.md`, the different job: a new page on a site this kit built
- `.claude/reference/build-standards.md` and `.claude/reference/image-placeholder.md`
