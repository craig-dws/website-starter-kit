# Add a page to an existing site

Paste this into Claude Code (in the client folder) to add **one page to a client website that is
already built and live**, in Elementor or in Breakdance 2.x. The page is built on a throwaway local
copy of the site, matched to what the site already does, and handed to you to put live yourself.

**Not this one if the site is a Breakdance 3.0 staging site this kit is building.** That is
`new-page.md`, which is first-party, better proven and much less work. The difference in one line:
`new-page.md` adds a page to a site **we are building**; this prompt adds a page to a site **that is
already live and was built by someone else, in a builder we cannot drive directly.**

## Before you paste

Four things have to be true, and all four are yours to do, not Claude's.

1. **A client folder for this site**, cloned from this starter kit. These jobs usually arrive for a
   site nobody here built, so there may be no folder yet. Make one, and use only the parts that
   apply: `content/` for the approved copy, `build-log/` for the record, and the prompts. The design
   phase, the sitemap and the token work are all skipped, because the site already has them. Do not
   run this job in a folder belonging to a different client.
2. **A throwaway local copy of the whole site**, normally in LocalWP. The whole site, not a settings
   export: Claude needs the site's existing pages to copy the pattern from, and the same builder
   version. Do not use a copy of just the theme or just the design settings.
   **Note what making the copy costs.** If the host has no one-click pull, taking a copy usually
   means installing a migration plugin on the live site to export it. That is a change to a live
   client site, so it is a decision to make on purpose, with the plugin removed afterwards, and not
   something to slide into on the way to the real job.
3. **The bridge plugin connected to that copy and nothing else.** Use `prompts/connect-bridge.md`,
   which walks the whole thing: the clone traps, the plugin settings, registering the connection and
   arming the safety guard. A copied site usually arrives with the bridge switched off and its domain
   lock still pointing at the live site, and that prompt handles both.
   **The bridge is never installed on the live site.**
4. **The approved copy for the new page in `content/`.** If it is not there, request it from
   ZilvaEdge first. Claude will refuse to build the page without it, which is deliberate.

---

You are adding one page to a client website that already exists and is live. Apply the
`existing-site-page` skill, plus `elementor-limits` or `breakdance-limits` for whichever builder this
site uses. Work to `.claude/reference/build-standards.md` for everything in it that is not specific
to a builder.

**The Breakdance 3.0 native tools do not exist on this job.** There is no `html-to-page`, no
`insert-stylesheet`, no `get-post-tree`, no `set-global-settings`, no `get-breakpoints`. The
Breakdance 3.0 beta section of `.claude/reference/limitations.md` describes that other path and does
not apply here; the WordPress, Figma, browser and session sections still do. On this job the write
path is a third-party bridge plugin connected to a local copy of the site. If you find yourself
reaching for a Breakdance 3.0 tool, you have the wrong prompt open.

**The bridge plugin never goes on the live site.** Not to read from it, not for one small change, not
temporarily. The entire safety model here is that it only ever touches a copy that can be deleted.

I am a project manager, not a developer. I never run commands and I never touch code. Anything that
needs a command, you run. Anything that needs a person, describe it as clicks in wp-admin or in
Local, and tell me plainly what I am looking at and why.

## Start

0. **Pull the latest** (`git pull`) so you have the other machine's work.
1. Read `.claude/CLAUDE.md`, `build-standards.md`, the `existing-site-page` skill and the limits
   skill for this site's builder. Check `build-log/ACTIVE.md` for other active sessions.
2. Get these from me, and **ask for any I have not given rather than guessing**:
   - **The site**, and **which builder** it uses.
   - **The local copy** you should be connected to, and my confirmation that it is the copy and not
     the live site.
   - **The page to add**, and its **type**.
   - **The reference**: either a design file, or, far more usually, **the existing page on the site
     that is closest to what this page should be**.
   - **The slug**, and where the page sits in the menu.
3. **Find the content.** It is `content/<slug>.md`, the approved copy ZilvaEdge released. **If there
   is no file for this page, stop and tell me to request it through ClickUp.** Do not write the copy
   yourself and do not build on placeholder text meaning to swap it later. Microcopy is the only
   exception, meaning calls to action, button labels and short connective copy, and anything you
   write directly goes in `CONTENT_CHANGELOG.md` the same session.
4. **Confirm you are on the copy.** Make **one read-only call** and show me what came back, with the
   site address visible in it. **Write nothing until I confirm it is the copy.** A local address is
   evidence. An assumption is not, and a page written into a live client site is not recoverable by
   apologising.
5. **Claim it** in `build-log/ACTIVE.md`.

## Inventory: stop here and show me

**This step is not optional and you do not build past it.** Everything is read-only. Nothing you find
here gets changed, least of all the global settings.

Read the site and enumerate:

- The **builder and its version**, and whether the Pro tier is active.
- The **structure generation** the site uses. On Elementor, classic section-and-column or container.
  On Breakdance, how Sections, Divs and Columns are actually used on this site.
- The **reusable units that already exist**: saved Templates, Global Widgets, Global Blocks.
- The **token layer**: the Elementor Kit's global colours and fonts, or the Breakdance Global
  Settings. Read them. Do not change them.
- The **class naming the site already uses**, so the new page looks like it belongs.
- The **breakpoints the site itself uses**.
- **The reference page, read structurally in full**, section by section, as the pattern to follow.

Then **stop and show me the inventory**, in plain language, before building anything. Say what
vocabulary the site gives you to work with, and separately, **what this page needs that the site has
no existing equivalent for.** That second list is the thing I have to decide about.

Why this is a hard stop: with no inventory you will fall back on the four elements you always know,
meaning heading, text, image and button, and hand-nest them into something bespoke. It will render.
It will match nothing, reuse nothing, and be miserable for the client to edit. **That has already
happened on a real build.** The site's own pages are the design system here, and you have to go and
read them before you can use them.

## Build, on the copy only

- **Duplicate the closest existing page and adapt it.** Do not compose the page from bare headings,
  text, images and buttons when a matching page already exists.
- Reuse the site's existing classes, components and spacing, and reference its existing tokens.
  Use its breakpoints, not invented ones.
- **If the page needs something with no existing equivalent, stop and ask me.** Do not improvise a
  bespoke section, and do not add or change a global setting to make one possible. Changing a global
  colour restyles every page on the site.
- Apply the standards that are not builder-specific: descriptive class names, one element per body
  block, hover and focus states, sensible heading order, contrast.
- **Three standards read differently here, and the `existing-site-page` skill explains why.**
  Breakpoints come from the site's own, read in the inventory, not from `get-breakpoints`, which
  does not exist here. The slug matches the convention this site already uses, and you never rename
  an existing page's slug, because it is a live URL. And bind images to the media library properly
  if the builder lets you, since the URL-reference workaround in `build-standards.md` exists only
  for a Breakdance 3.0 beta defect that is not present on this path. Tell me if binding does not
  work, rather than quietly falling back.
- **Images.** With a design, pull the asset from the Figma frame, rename it to a descriptive
  kebab-case filename from what the design shows, resize it to about twice its display width,
  compress it, then upload it with `.claude/tools/optimize-and-upload.py` and reference it. You run
  that script yourself; I never run Python. With no design, which is the usual case here, build a
  placeholder block at the correct display size per `.claude/reference/image-placeholder.md` and log
  it under Outstanding images. Do not invent an image or generate one at build time. Where the site
  already has the right image, reuse the existing attachment rather than uploading a second copy.
  SVGs are inlined, not uploaded. Set alt text per `.claude/reference/alt-text-guidelines.md`.
- **Recovery path.** The local copy is disposable and regenerable, so a snapshot can be waived here;
  record the waiver. On the live site later it is never waivable.

## Verify, on the copy

- **Open the page in the builder**, not just the rendered page, and confirm every element is
  natively editable with no unknown-element errors. A page that renders but will not open cleanly in
  the builder has failed, and I need to know that rather than read that it is finished.
- Check it at each of the site's own breakpoints.
- Compare it against its sibling pages and tell me honestly where it differs.

## Prepare the transfer, then stop

**You do not touch the live site. Ever.** You prepare the move and I make it.

- **Elementor:** save the page as a Template and export the JSON file. Tell me where the file is.
  Flag any images that will not resolve on the live site, and any Pro-only widgets the page uses.
- **Breakdance 2.x:** there is no equally clean single-page export. Work out the export route that
  actually exists on this version rather than assuming one, and tell me what you found. Say plainly
  if the only route left is copying the page's stored layout data across, because that is the
  riskiest method available and I need to decide, not discover.
- **Media does not travel with a page transfer.** Say which images need uploading to the live site
  separately, and what will break if they are not.
- Give me the steps in order: what to back up first, what to import, and what to clear or regenerate
  afterwards. **Every step as clicks in wp-admin.** I do not run commands. If a step genuinely has no
  interface equivalent and needs a command line, say so and flag that it needs a developer, rather
  than handing me something I cannot use.

## Finish

Do these in order, then send me the report and nothing else.

1. **Record the page** in `build-log/pages/<slug>.md` from `_TEMPLATE.md`. All the technical detail
   lives here, not in your message to me: the builder and version in place of a build target, the
   reference page it patterned from, the inventory findings, and the Deferred passes section
   (`deferred-passes.md`) with any image placeholders and the drafted SEO title and description.
2. **Release your claim** in `build-log/ACTIVE.md`.
3. **Commit and push** the page's files with a short message. One page per commit.
4. **Send me the report below.** Then stop.

### The report to send me

Use this exact shape. Write it for a non-developer: **plain language, no element ids, class names,
selector counts or percentages** (those stay in the page record).

```
## <Page name>  (<site>, <builder>)

Status: <Built on the copy and ready to transfer  |  Built, but N thing(s) need you first  |  Stopped, see below>

What I built: <one or two plain sentences. What the page is, and which existing page it copied the pattern from.>

Where it differs from its siblings: <plain sentences, or "Nowhere I can see.">

Needs you:
- Decisions: <things only you can decide, or "Nothing.">
- On the live site: <the transfer steps, numbered, in order. Start with the backup.>

Images: <"None outstanding." or: which images need uploading to the live site separately, and what breaks if they are not.>

Routine, nothing to do now: <ONE line, e.g. "2 image placeholders and the SEO draft; handled by the image and SEO passes later.">
```

Rules for the report:

- **Status first, and honest.** "Ready to transfer" only when the page opens cleanly in the builder
  on the copy and nothing on it needs a person. If you stopped at the inventory because the site has
  no equivalent for something, say **Stopped**, and lead with what you need from me.
- **The transfer steps are the main event.** Number them, put the backup first, and write them as
  clicks in wp-admin. I will be following them with the report open next to the screen.
- **"Needs you" is genuine human actions only.** If there is nothing, write "Nothing." Never pad it.
- **"Routine, nothing to do now" is ONE line.** It covers the ordinary deferred passes, meaning
  image placeholders and the SEO draft. Do not explain what those are, I already know.
- **No internals in the report.** Element ids, class names, counts and measurements belong in the
  page record.
- **Never report a page as ready when you could not open it in the builder.** Say what happened.
- **Do not suggest a next page.** These jobs arrive one at a time from the client, not from a
  sitemap.
