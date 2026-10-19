# [CLIENT] Site Build

## Project overview
Website work for [CLIENT]. Staging is [STAGING_URL]. Production is [PRODUCTION_URL - recorded
for migration and launch only, never touched; fill at migration].

## Builder, connection and design source
Every rule that depends on how this site is built, how Claude reaches it, or where its design
comes from lives in one of the three files below. Only the three chosen for this project load.

@builders/[BUILDER].md
@connections/[CONNECTION].md
@design-source/[DESIGN_SOURCE].md

**Setup check, before any other work.** If any of those three lines still shows a word in
square brackets, its rules have not loaded, and this chat does not know how the site is built
or reached. Stop and ask the operator for the builder, the connection and the design source
(the choices and the supported combinations are in `START-HERE.md`), fill the lines in, and
ask them to open a fresh chat so the rules load. Then check the connection file's
**Supports** line. If it does not name this builder, stop and ask before anything else: that
combination has not been proven, and a guessed write path is how a layout gets destroyed.

## Capabilities
The rules here name capabilities, never tools. The connection file says how each one is done
on this site, and names the person who does it where the connection cannot.

| Capability | What it means |
|------------|---------------|
| Confirm the environment | Prove from the site's own answer which site Claude is connected to, before any write |
| Read a page's layout | Get a page's stored structure, not only what it looks like |
| Snapshot a page | Save a page's stored layout where it can be restored from, before it is overwritten |
| Write a page's layout | Create a page, or change one |
| Upload media | Add an image to the site's media library |
| Clear the cache | Make the public site show what was just written |
| Read the design tokens | Get the named colour, type and spacing values the site is built from |
| Write the design tokens | Change those values. It restyles every page, so only on a new build from an approved design, and never as a side effect |

**After every write, check that the public page shows it.** Open the page's public address,
logged out, and look for a sentence from the new copy. If it is missing, load the same address
with a throwaway query string on the end (`?check=1`), which most page caches do not serve
from. Present there but not at the plain address means a stale cache: clear it the way the
connection file says, then check again. Missing from both means the write did not land. Either
way the page is not done.

## Token source of truth
- Reference variables, never hardcoded hex or off-scale spacing.

## Images and SVGs
- **Crop to the box before uploading.** A photo is usually 4:3 landscape and the slot it goes in
  often is not, so the browser centre-crops it and nothing has chosen what to keep. Work out the box
  ratio from the design, compose the crop so the subject and any branding stay in frame, and save it
  at that ratio. Record what each crop keeps in the page record; one source used at two box ratios
  becomes two files. Never upscale to reach 2x. **Measure the crop loss on the rendered page rather
  than checking it by eye** (`.claude/reference/build-checklist.md`): on a past build the worst two
  cases, losing 37 and 35 per cent of the picture, were invisible to a visual review.
- **Alt text is accessibility, not just SEO, and there is a right strategy.** Content images
  (photos, meaningful graphics) get descriptive alt written from what the design shows.
  Decorative icons get empty alt or aria-hidden, they add no information. Set the media fields
  at upload with the script (`--alt`, and `--title`, `--caption`, `--description` where useful),
  AND set the alt on the rendered image element in the layout. Accessibility is a certified
  gate, so get this right rather than putting generic text on everything. Follow the rules in
  `.claude/reference/alt-text-guidelines.md`.
- **Keep placeholder images as placeholders.** A dummy or grey-silhouette image is not renamed
  after a real person; give it a placeholder name and flag it so the human supplies the real
  asset later.

## Page copy: this repo owns it during the build

During the build this repo owns page copy. ZilvaEdge does not edit released pages while the
build is live. The Google Doc will go stale during the build; that is expected, and it is
refreshed at launch when the PM runs ZilvaEdge's content reconciliation.

- `content/` holds the approved copy, one markdown file per page. Build pages from those
  files. **Refuse to build a page whose released content is missing**, and tell the operator
  to request it, rather than improvising copy. Improvised copy looks finished, passes a
  visual review, and is not found out until the client reads it.
- **Microcopy is the only direct-write exception**: CTAs, button labels, short connective
  copy. Two lines of copy do not go through the full ZilvaEdge pipeline.
- **Full new pages or sections are requested from ZilvaEdge through ClickUp** and arrive as
  released content in `content/`. Do not improvise a page.
- **Any edit to a file under `content/`, and any copy written directly into a page including
  microcopy, gets a line in `CONTENT_CHANGELOG.md` in the same session.** That log is what
  ZilvaEdge reads at launch to work out what changed and why. An unexplained change gets
  reported as needing attention later, so logging it now costs ten seconds and saves a
  conversation.

## Protected paths (do not edit)
- Anything under the production environment.
- .env and any secret-bearing file.

## Dos
- Work one page at a time and return a staging preview URL.

## Don'ts
- Do not run destructive shell commands (rm -rf, sudo).
- Never write to the live site. Staging, or a disposable copy of the site, only.
- Do not commit secrets. The connection file says where this project's site credential
  lives, and it is never in the repo.
- No eyebrow labels: no small uppercase label above a heading, even where the design frame
  draws one. The only words on a page are the approved content in `content/`. If the frame
  has them, leave them out and note it in the build log. (ZilvaEdge rule, 2026-10-19.)

## Build log
- Keep an audit trail in build-log/. The build-log.sh hook auto-records
  database-affecting commands; you record snapshots, gate approvals and milestones.
- Every gate in build-log/GATES.md needs a person's approval, never the AI's. Mark it
  Approved when approved; no need to record an owner name.
- Before a write that would lose real work, snapshot and log it. On a disposable empty
  site this may be waived by a recorded decision; reinstate before real work exists.

## House style
- British and Australian English. No em dashes, no en dashes, no double hyphens in
  prose (CLI flags in code are fine). No emojis.

## Reference
- The full agency system, its complete docs and the front-half creative skills live
  in the AI Web Design System repo, not here. Consult it for anything not covered by
  this project. This repo is one client build and stays lean by design.

## Talking to the operator
The person running this build is a project manager, not a developer, and never runs
commands. Explain each term below in plain words the first time it appears in a reply.

| Term | Say this instead |
|------|------------------|
| builder | the tool the site's pages are built in |
| connection | how Claude reaches the site to read and change it |
| design tokens | the named colour, type and spacing values the design is built from |

Every page report says which page it covers, which address to look at, and what needs a
human decision. Never ask the operator for something the design source or `content/`
already says.
