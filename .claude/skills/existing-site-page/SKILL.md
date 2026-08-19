---
name: existing-site-page
description: Add a page to a client website that is already built and live, matching what the site already does, rather than building from a design. Use when the job is a new page on an existing Elementor site or an existing Breakdance 2.x site, neither of which has the Breakdance 3.0 native connection. Covers copying the whole site to a disposable local environment, connecting the bridge to that copy only, taking a read-only inventory of the site's own patterns, building by patterning an existing page, and transferring only the finished page. The inventory step is a hard stop and is the point of the procedure.
---

# Add a page to an existing site

A different job from a new build, and it fails in a different way. There is no
design system to establish and no tokens to sync, because **the site already has
them and the new page has to match.** The measure of success is that a visitor,
and the client in the builder, cannot tell which page was added later.

This procedure covers **Elementor** and **Breakdance 2.x**. Neither has the
Breakdance 3.0 native connection. On a Breakdance 3.0 site running the Agent
Connector, use the normal build path in `prompts/new-page.md` instead: it is
first-party, better proven and does not need any of this.

Read the builder's own limits alongside this: the `elementor-limits` skill, or the
`breakdance-limits` skill for a 2.x site, where the ranked write methods and the
absence of a sanctioned layout API apply just as they do on 3.0.

## Which tools exist on this path, and which do not

Say this plainly to yourself before starting, because getting it wrong wastes a
session. **The Breakdance 3.0 native tools do not exist here.** There is no
`html-to-page`, no `insert-stylesheet`, no `get-post-tree`, no
`set-global-settings`, no `get-breakpoints`.

That means `.claude/reference/limitations.md` has to be read selectively rather
than as a whole. Its **Breakdance 3.0.0-beta.1 native MCP** section is about a
different path and none of it applies here. Its other sections still do, and are
worth reading before you hit them:

- **WordPress:** SVG uploads are blocked by default, so SVGs are inlined.
- **Figma:** the mesh-gradient blind spot and the `get_metadata` truncation, on
  the minority of these jobs that come with a design.
- **Browser and QA:** the orphaned Chrome profile lock, lazy-loaded images not
  fetching in a capture, and `resize_page` clamping at about 512px.
- **Claude Code sessions:** no automatic lock between chats.

What exists here instead is a **third-party bridge plugin** connected to a
disposable local copy of the site. It is reverse-engineering an undocumented
internal format, which is managed risk rather than removed risk. The binding is
recorded in the project, and this procedure calls it "the bridge" rather than
naming a vendor, so it stays swappable.

**The bridge is never installed on the live client site.** Not to read from it,
not to "just make one small change", not temporarily. It carries site-privileged
abilities, its sandbox is not a security boundary, and the whole safety model here
is that it only ever touches a copy that can be thrown away. This is the same rule
as removing the Agent Connector before a staging site goes live, and it is the
shortcut most likely to be reached for when a transfer turns fiddly.

Two capabilities are unaffected by any of this and work as normal, because they go
through WordPress rather than the builder: `.claude/tools/optimize-and-upload.py`
for media, and `.claude/tools/create-post.py` for posts. Both use the WordPress
REST interface with an Application Password and are builder-neutral.

## The design source, when there is no design

Most of these jobs have no Figma frame, and that is expected rather than a
shortfall. **The reference is then an existing page of the same type on the site
itself.** Sitting a new page next to a built sibling and matching its structure is
the correct method here, because on an existing site the site's own pages *are*
the design system. This is the same instinct as `prompts/new-page.md`, which
already treats a built sibling as the normal reference once the first page of a
type exists.

Where a design file does exist, use it, but **take the inventory first anyway.**
The page still gets built from the site's existing components, not from new ones
invented to chase a drawing.

## The inventory is a hard stop

This is the reason the procedure exists, so it is not a step to compress.

An agent with no inventory falls back to the primitives it always knows, meaning
heading, text, image and button, and hand-nests them into a bespoke pile. It
renders. It matches nothing, reuses nothing, and is miserable for the client to
edit. **This has already happened on a real build.** It is the same failure as
emitting a raw hex value instead of a token name: the higher-level vocabulary was
right there and the agent never went and read it.

So the rule is absolute:

- **Enumerate what the site already has, and show it to the operator, before
  building anything.**
- **Compose only from that vocabulary.**
- **If something the page needs has no existing equivalent, stop and ask.** Do not
  improvise a bespoke section to fill the gap, and do not add or change a global
  setting to make one possible.

A page built without the inventory is not a page that needs tidying up. It is a
page that gets thrown away.

## Where the words come from

The content rule does not relax because the site already exists. It is the same
rule as everywhere else in this kit, and it is in `.claude/CLAUDE.md`,
`START-HERE.md` and `prompts/new-page.md`.

- **Build from the approved copy in `content/`**, one markdown file per page.
- **If there is no file for this page, stop.** Tell the operator to request it from
  ZilvaEdge through ClickUp, where it comes back as released content. Do not write
  the copy, and **do not build the page on placeholder text meaning to swap it
  later.** Improvised copy looks finished, passes a visual review, and is not found
  out until the client reads it.
- **Microcopy is the only exception**, meaning calls to action, button labels and
  short connective copy. Anything written directly goes in `CONTENT_CHANGELOG.md`
  in the same session.

An existing site raises one extra question the new-build path never has to ask:
the site is live, so its current pages already carry copy nobody in this repo
released. That copy is read as a **pattern to match in tone and structure**, and
it is never lifted wholesale into a new page as a substitute for released content.

## The loop

### 1. Copy the whole site to a disposable local environment

- Copy the **whole site**, using LocalWP, or All-in-One WP Migration, or the host's
  own pull. A settings-only export is **not** enough: it carries the tokens and
  none of the page patterns that the inventory needs, and none of the version
  context.
- **Match the versions.** The copy runs the same builder version, the same theme
  and the same plugins as the live site. Version skew is the most common reason a
  finished page will not import cleanly at the end.
- **This is a human step.** The operator makes the copy; the build does not.

### 2. Connect the bridge to the copy, and only to the copy

- On a LocalWP copy, Application Passwords need either HTTPS or
  `define( 'WP_ENVIRONMENT_TYPE', 'local' );` in `wp-config.php`, followed by a
  restart of the site so PHP reloads the file. **The build cannot do this.**
  `wp-config.php` is a protected path, denied in `.claude/settings.json` and
  blocked by the `.claude/hooks/block-protected-paths.sh` hook, so it is a human action in the
  Local interface. `START-HERE.md` has the full troubleshooting order, including
  the security-plugin trap that is the most common cause of the Application
  Password screen refusing.
- **A copied site often arrives with the bridge dormant.** Copying or migrating can
  leave its abilities switched off, its domain lock still pointing at the live
  domain, and safe mode engaged. Re-open the plugin's settings, re-enable the
  abilities, point the domain lock at the local address, confirm safe mode is set
  for the intended work, then regenerate the Application Password. This is written
  up in `docs/19_implementation_runbook.md` and it has caught people out before.
- **Confirm the target before any write.** Make **one read-only call** and show the
  operator what came back, with the site URL or home URL visible in it. Do not
  write anything until the operator confirms it is the copy. A local address is
  evidence; a plausible assumption is not.

### 3. Take the inventory, read-only, and show it

Record all of this in the project before building, and put it in front of the
operator in plain words:

- The **builder and its version**, and whether the Pro tier is active.
- The **structure generation** in use. On Elementor, classic section-and-column or
  container. On Breakdance 2.x, how Sections, Divs and Columns are actually used on
  this site.
- The **reusable units that already exist**: saved Templates, Global Widgets,
  Global Blocks, whatever this site has.
- The **token layer**, meaning the Elementor Kit's global colours and fonts, or the
  Breakdance Global Settings. **Read them. Do not change them.**
- The **class naming the site already uses**, so the new page's classes look like
  they belong.
- **One or two representative pages** of the type being added, read structurally in
  full, as the pattern to follow.

Then say plainly what vocabulary the site gives you to work with, and what the page
needs that the site has no equivalent for. That second list is the thing the
operator has to make a decision about.

### 4. Build on the copy by patterning an existing page

- **Duplicate the closest existing page and adapt it.** Do not compose from bare
  elements. This is the constrained-patch-on-a-known-good-structure method, and it
  is far safer than a build from scratch.
- Reuse the site's existing classes, components and spacing, and reference its
  existing tokens rather than introducing values.
- **Do not change global settings or tokens.** Restyling a global colour changes
  every page on the site. If the page genuinely needs a new shared component or a
  new token, stop and ask.
- Keep the client's editing experience consistent. The new page has to be editable
  the same way its siblings are, by the same person, in the same builder.
- Apply the standards in `.claude/reference/build-standards.md` that are not
  builder-specific: descriptive class names, one element per body block, hover and
  focus states, accessibility, sensible headings.

### Three standards that read differently on an existing site

These are deliberate departures from a literal reading of `build-standards.md`,
not oversights. That file is written for a site this kit is building from a
design, and each of these three assumes something that is not true here.

- **Breakpoints.** The standard says breakpoints come from `get-breakpoints` and
  that no `@media` query is invented. That tool does not exist on this path, so the
  breakpoints come from **the site's own**, read during the inventory. The
  underlying rule is unchanged: use the real ones, never invent one.
- **Slugs.** The standard sets an agency default of `about-<business-name>` and
  `contact-<business-name>`. That is a default for a site we are creating. On a live
  site the slug is a public URL with history and inbound links, so **match the
  convention the site already uses** and **never rename an existing page's slug**.
  If the client wants a slug that breaks their own pattern, that is their decision
  to make, with a redirect, and it is not a build decision.
- **Media binding.** The standard says images are referenced by URL rather than
  bound to the media library. That is a workaround for one proven Breakdance 3.0
  beta defect and **the reason for it does not exist here.** Where the builder and
  the bridge can bind an image to its attachment properly, do that, because it
  gives responsive sizing for free. Whether the bridge can bind media on this
  builder is **unverified, so confirm it on the first image** rather than assuming
  either way.

### 5. Images

The process is the one in `.claude/CLAUDE.md`, unchanged, with one addition that
only applies here.

- **With a design**, pull the asset from the Figma frame, rename it from the design
  to a descriptive kebab-case filename, resize it to about twice its display width,
  compress it, then upload and reference it. Write alt text from what the design
  shows, and set it both at upload and on the rendered element per
  `.claude/reference/alt-text-guidelines.md`.
- **With no design**, which is the usual case here, build a **placeholder block**
  at the correct display size per `.claude/reference/image-placeholder.md`, and log
  it under Outstanding images in the page record. Do not invent an image and do not
  generate one at build time. Real images are sourced in the separate pass,
  `prompts/source-images.md`.
- **Where an existing image on the site is genuinely the right one for this page,
  reuse the attachment that is already there** rather than uploading a second copy.
  The upload tool cannot delete, so a duplicate stays on the site forever.
- **The addition that is specific to this path: media does not travel with a page
  transfer.** Anything uploaded to the local copy has to be uploaded to the live
  site separately and the references repointed, or the page arrives with broken
  images. Decide how before the transfer, and say so in the report.

### 6. Verify on the copy

- **Open the page in the builder**, not just the rendered page, and confirm every
  element is natively editable with no unknown-element errors. A page that renders
  but will not open cleanly in the builder has failed.
- Check it at each of the site's own breakpoints.
- Compare it against its sibling pages and say honestly where it differs.

### 7. Prepare the transfer, then stop

The build prepares the transfer. **The build does not touch the live site.**

- **Elementor:** save the page as a Template and export the JSON. This is
  first-party and needs no raw write, and it is the clean path. Flag any images
  that will not resolve on the target and any Pro-only widgets used.
- **Breakdance 2.x:** there is no equally clean single-page export. Use
  Breakdance's own template or Global Block export where that fits. Copying the one
  new page's `_breakdance_data` postmeta across is the fallback, and it is the
  last-resort method in the `breakdance-limits` ranking, so it is recovery-path
  first and human-reviewed. Because the page is **new** there is no existing layout
  to destroy, which makes it lower risk than editing an existing page, but it is not
  no risk. **Confirm the exact export route on the real site rather than assuming
  one exists.**
- Hand the operator: what to back up on the live site first, the import steps in
  order, and what to clear or regenerate afterwards, meaning the builder cache, the
  page cache, and on Elementor the Regenerate CSS and Data action.
- **Give every one of those steps as clicks in wp-admin.** `breakdance-limits` says
  to run `wp breakdance clear_cache` after a database write, and that is right, but
  it is a command line instruction and the operator here does not run commands. On
  a Breakdance 2.x live site, find the equivalent cache clear in the Breakdance
  settings screen and give that. If no equivalent exists in the interface, say so
  plainly and flag that this step needs a developer, rather than handing over a
  command the operator cannot use.

### 8. A person promotes

**Promotion to the live site is a human, backed-up action.** No agent writes to a
live client site, ever. After the transfer the operator opens the page in the
builder on the live site and confirms it is still natively editable there.

## Recovery paths on this path

The kit's rule is a recovery path proportionate to what is at stake, and this job
has two environments with very different stakes.

- **On the disposable local copy:** the copy is regenerable, so there is nothing to
  restore and a snapshot can be waived. Record the waiver.
- **On the live client site:** never waivable, no exceptions, and it is a full
  backup rather than builder revisions. This is a site with real traffic and real
  content, and it is the operator who takes the backup before importing.

## The audit trail

An existing-site page is logged like any other page in this kit.

- **Claim it** in `build-log/ACTIVE.md` before starting.
- **Record it** in `build-log/pages/<slug>.md` from `_TEMPLATE.md`, noting the
  builder and version in place of a build target, the reference page it patterned
  from, and the inventory findings.
- **Log the transfer** in `build-log/BUILD-LOG.md`, including the backup taken on
  the live site and who took it.
- Anything written directly as copy goes in `CONTENT_CHANGELOG.md` the same
  session.

## Rules

- The local copy only. **Never an agent write to a live client site.**
- Confirm you are on the copy with one read-only call before any write.
- Take the inventory first. Compose from what exists. Stop and ask rather than
  inventing.
- Do not change global settings or tokens while adding a page.
- Build from released content in `content/`. Microcopy is the only exception.
- One page at a time, verified before the next.
- Do not invent builder internals. Where you are unsure how a builder stores or
  moves something, say so and mark it to confirm.
- British and Australian English. No em dashes, no en dashes, no double hyphens in
  prose. No emojis.

## Confirm per site, do not assume

- The builder and version, and pin the local copy to match.
- The bridge binding for this project, and one verified read-only call before any
  write.
- Whether the client's licence covers the Pro features any existing page relies on,
  for example Elementor Pro widgets or Breakdance Pro settings export.
- The single-page export route that actually works on this builder version.
- Whether media references survive the transfer, and what has to be repointed.

## See also

- `prompts/existing-site-page.md`, the paste-in job that runs this
- the `elementor-limits` skill, and the `breakdance-limits` skill
- `prompts/new-page.md`, the different job: a new page on a site this kit built
- `.claude/reference/build-standards.md` and `.claude/reference/image-placeholder.md`
