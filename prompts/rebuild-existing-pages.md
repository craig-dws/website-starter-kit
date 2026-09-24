# Rebuild existing pages on an existing site

Paste this into Claude Code (in the client folder) to give **pages that already exist on a live
client site new copy, in place**. Each page keeps its address, stays where it is in the site, and
keeps its buttons and links working exactly as before. The work happens on a staging or local copy
of the site, one page at a time, and you put the result live yourself.

**This overwrites layout that exists today**, which makes it the riskiest job in this folder that
touches pages. Every page is snapshotted before it is changed, with no exceptions.

**Not this one** for a page that does not exist yet (`existing-site-page.md`), or for a site we are
building from a design (`new-page.md`).

## Before you paste

Four things have to be true, and all four are yours to do, not Claude's.

1. **A client folder for this site**, set up with this site's builder, its connection and the existing
   site as the design source (see `START-HERE.md`).
2. **A staging or local copy of the site, not the live site**, running the same versions as live.
3. **The connection to that copy**, set up with the prompt the connection file names
   (`prompts/connect-rest.md` on a block theme, `prompts/connect-bridge.md` on Elementor or
   Breakdance 2.x).
4. **The approved copy for every page in `content/`**, and the list of pages with their addresses
   (normally `page-structure.md` or `design/sitemap.md`). A page with no approved copy is skipped,
   not written.

---

You are rebuilding existing pages on a client website that is already live: each page keeps its
address and gets the new approved copy. Apply the `existing-site-page` skill, all of it, and
especially its **Rebuilding an existing page** section. Apply the limits skill the builder file
names. Work to `.claude/reference/build-standards.md` for everything in it that is not specific to a
builder.

I am a project manager, not a developer. I never run commands and I never touch code. Anything that
needs a command, you run. Anything that needs a person, describe it as clicks, and tell me plainly
what I am looking at and why.

## The rules that do not bend

- **Snapshot every page before it is overwritten.** No waiver, even on staging. If the connection
  cannot snapshot a page, a person takes a backup before the first write and tells you it is done.
- **Never change a page's slug, status or parent.** The address, the published state and the place in
  the site stay exactly as they are.
- **Read every link on the page before you replace anything**, and compare after. Nothing
  disappears without being named in the report.
- **Conversion buttons keep their address exactly**, including every query string and tracking
  parameter, character for character. Booking, enquiry, call and download buttons are the ones that
  matter. A booking link that loses its tracking still works, and the client's reporting silently
  goes wrong.
- **Leave everything the copy does not cover.** SEO fields, the featured image, templates, the header
  and footer, menus and shared blocks are not part of this job. If the copy seems to need one
  changed, stop and ask me.
- **Compose only from what the site already has.** If the copy needs something the site has no
  pattern for, such as a table, numbered steps or a run of questions and answers, stop and ask me.
- **Never the live site.** You write to the copy. I move the result.

## Start

0. **Pull the latest** (`git pull`) so you have the other machine's work.
1. Read `.claude/CLAUDE.md` and the builder, connection and design source files it loads, the
   `existing-site-page` skill and the builder's limits skill. Check `build-log/ACTIVE.md`.
2. **Check the builder.** Read the rendered source of any page on the copy and confirm it matches the
   builder file. If it does not, stop and tell me.
3. **Confirm you are on the copy**, with the connection's "confirm the environment" capability. Show
   me what came back, with the site address in it. **Write nothing until I confirm it is the copy.**
4. **Make the list.** Every page to rebuild: its name, its address on the copy, its id and kind of
   content (for example a page, or a custom post type such as services), and its file in
   `content/`. **A page with no approved copy is marked "skipped, no copy" and never written.** Show
   me the list.
5. **Ask me how the rebuilt pages reach the live site**, if `build-log/DECISIONS.md` does not
   already say: page by page by a person, or a whole staging-to-live move by a person or the host.
   Record the answer. It changes what you hand me at the end.
6. **Claim it** in `build-log/ACTIVE.md`.

## Inventory: stop here and show me

Take the inventory the `existing-site-page` skill describes, once, for the whole set of pages: the
versions, the blocks or elements the site uses and which tier each belongs to, the reusable parts,
the tokens (read, never changed), and on a block theme the settings of every ACF block these pages
use, read from an existing instance's raw markup.

Then, **for every page on the list**, read and record in its page record:

- Its current structure, section by section, from its stored layout.
- **Every link**: its text and its full address.
- **Every conversion button**: its label and its full address, query string included.
- Its slug, status and parent.

Then **map the copy onto the site's patterns**, page by page: which existing section each part of
the new copy goes into. **List everything the copy needs that the site has no pattern for.** Then
stop and show me, in plain language: the vocabulary the site gives you, the mapping, and the gaps.
The gaps are the thing I decide about.

## Rebuild, one page at a time, on the copy only

For each page, in order:

1. **Snapshot it.** Confirm the snapshot exists before going further.
2. **Build the new layout from the page's own current structure**, changing the copy and only the
   settings the copy needs. The page's existing sections are the first pattern, its siblings the
   second.
3. **Write it**, leaving the slug, status, parent and title alone unless the approved copy changes
   the title.
4. **Read it back and compare**, against the record you made in the inventory:
   - slug, status and parent unchanged;
   - every link still present, or its removal deliberate and noted;
   - every conversion button's address identical, character for character.
   Any difference you did not intend: **restore the snapshot and tell me.**
5. **Check the public page shows the new copy**, as `.claude/CLAUDE.md` describes.
6. **Verify it is still editable**, the way the builder file says. On a block theme that means no
   validation warning on any block in the editor and every ACF field showing its content. The editor
   needs a login: if you cannot open it, tell me exactly which page to open and what to look for.
7. **Record it** in `build-log/pages/<slug>.md`: the snapshot file, the link comparison, the buttons
   checked, and whether the editor check was done and by whom.

**After the first page, stop and show me.** It settles how the copy maps onto the site. The rest
follow it, one at a time, each verified before the next.

## Finish

1. **Release your claim** in `build-log/ACTIVE.md`.
2. **Commit and push** the page records and snapshots, one page per commit.
3. **Send me the report below.** Then stop.

### The report to send me

Plain language. No element ids, class names or counts beyond the ones below (the detail is in the
page records).

```
## Rebuild: <section or set of pages>  (<site>, <builder>)

Status: <All N rebuilt on the copy and verified  |  N rebuilt, M need you first  |  Stopped, see below>

Pages:
- <Page name>: <Rebuilt and verified | Rebuilt, editor check needed | Skipped, no copy | Stopped: reason>
  Links: <"All kept." or what was removed and why>. Buttons: <"All exact." or what differs>.

Needs you:
- Decisions: <things only you can decide, or "Nothing.">
- Editor checks: <which pages to open, and what to look for, or "None, all done.">
- On the live site: <the steps, numbered, in order, starting with the backup. Or, for a whole-site move, who does it and what to check afterwards.>

Routine, nothing to do now: <ONE line.>
```

Rules for the report:

- **Status first, and honest.** A page is only "verified" when the editor check is done. Until then
  it is "rebuilt, editor check needed".
- **Every page on the list appears**, including the skipped and stopped ones.
- **A lost link or a changed button address is never routine.** Name it on its page's line.
- **No internals.** Snapshot file names and the full link lists belong in the page records.
