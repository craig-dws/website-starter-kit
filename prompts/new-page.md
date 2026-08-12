# New page

Paste this into Claude Code (in the client folder) to build **one internal page**. Use it during the
internal-pages phase, once the design system is locked and the shared chrome (header/footer) is
built. For the first build or setup, use the guided or advanced prompt instead.

---

You are building one internal page. Work to `.claude/reference/build-standards.md`, the limits in
`.claude/reference/limitations.md`, and `.claude/reference/parallel-builds.md`. Staging only,
human-approved gates.

## Start
0. **Pull the latest** (`git pull`) so you have other sessions' and the other machine's work.
1. Read `.claude/CLAUDE.md`, `design/sitemap.md`, `build-standards.md`, `build-checklist.md` and
   `limitations.md`, and check `build-log/ACTIVE.md` for other active sessions.
2. Get these from me for the page (ask for any I have not given):
   - **Which page** and its **type** (condition / treatment / surgeon / content / other).
   - The **reference to match**: either the **Figma node id** of the type's reference design, OR, when
     there is no design, the **already-built sibling page of the same type** to copy the pattern from
     (e.g. the built Glaucoma page for a new condition page). Most pages after the first of a type have
     no design, so a built sibling is the usual reference. Identify a Figma frame by node id, never by name.
   - The **slug** (from the sitemap).
   - The **content**. Source it from `content/{slug}.md`, the approved copy ZilvaEdge released.
     **If there is no file for this page, stop.** Tell me to request the page from ZilvaEdge
     through ClickUp; it comes back as released content. Do not write the copy yourself and do
     not build the page on placeholder text meaning to swap it later. Microcopy is the only
     exception, meaning CTAs, button labels and short connective copy, and anything you write
     directly goes in `CONTENT_CHANGELOG.md` the same session.
3. **Claim it** in `build-log/ACTIVE.md` (what, which slug, the time, status active), so a parallel
   session does not collide.

## Build
- **Content-first from the reference**, adapted to this page's content. **Reuse the type's existing
  components and global classes, do not re-invent them.** When the reference is a **built sibling page**
  (no design), read its structure with `get-post-tree` and match it: the same sections and the same
  `.ees-*` classes, with the content deciding which sections appear and how many. When it is a Figma
  frame, build from that. Either way the **design system**, not a per-page drawing, is the source of the look.
- **If this is the first page of its type**, it establishes the type's shared components: build it
  **solo** (not in parallel), so the pattern is set before the rest fan out.
- **Do not write global settings, they are locked.** If the page genuinely needs a new shared
  component, stop and tell me rather than adding global classes mid-parallel.
- Apply the standards: **descriptive CSS classes**, **one Text element per body block**, images via
  `.claude/tools/optimize-and-upload.py` (referenced by URL, media binding is a known limit), SVGs
  inlined, hover and focus states, responsive from `get-breakpoints`, correct slug and SEO.
- **Images: if the image is not worked out, build a placeholder block, do not invent one.** Internal
  pages usually have no design, so their images are not decided yet. For each image slot, put a
  placeholder at the correct display size per `.claude/reference/image-placeholder.md` (holds the
  layout, says what image is needed), and list it under **Outstanding images** in the page record. Do
  not AI-generate images at build time. Real images are sourced in a separate pass afterwards
  (`prompts/source-images.md`). Only use an actual image now if the client already supplied a clear
  match, in which case optimise and upload it as normal.
- **Verify** (chrome-devtools MCP, headless): against a Figma frame, a screenshot diff; against a built
  sibling (no design), confirm the structure and components match the sibling and the full build
  checklist passes (one element per block, states, responsive, no overflow), since there is no frame to diff.

## Finish

Do these in order, then send me the report and nothing else.

1. **Record the page** in `build-log/pages/<slug>.md`. All the technical detail lives here, not in your
   message to me. Include the **Deferred passes** section (`deferred-passes.md`): image placeholders,
   internal links that 404 only because their target is not built yet, and a drafted SEO title and meta
   description. Record these once as expected, not as defects. (A link to a slug **not** in the sitemap,
   or an image slot with no placeholder, IS a defect, so flag those.)
2. **Release your claim** in `build-log/ACTIVE.md`.
3. **Commit and push** the page's files with a short message. One page per commit (see `git-workflow.md`).
4. **Check what is already built**, so the next-page suggestion is real: a file in `build-log/pages/`
   means that page is built; compare against the full list in `design/sitemap.md` to find genuinely
   unbuilt pages.
5. **Send me the report below.** Then stop.

### The report to send me

Use this exact shape. Write it for a non-developer: **plain language, no element ids, class names,
selector counts, percentages or jargon** (those stay in the page record).

```
## <Page name>

Status: <Complete and committed  |  Built, but N thing(s) need you first>

What I built: <one or two plain sentences. What the page is, and that it reuses the <type> pattern.>

Needs you:
- On this page: <plain actions only a human can do, or "Nothing.">
- On other pages: <"None." or e.g. "I changed the shared <thing>, so please re-check <page>.">

Routine, nothing to do now: <ONE line, e.g. "3 image placeholders and the SEO draft; handled by the image and SEO passes later.">

Next page:
Follow prompts/new-page.md. Page: <name> (<type>). Reference: the built <sibling> page. Slug: <slug>. Content: content/<slug>.md
```

Rules for the report:
- **Status first, and honest.** "Complete and committed" only when the build checklist passed and
  nothing on the page needs a person. Otherwise "Built, but N things need you first" and list them.
- **Needs you = genuine human actions only** (a decision to confirm, something only a person can do).
  If there is nothing, write "Nothing." Never pad it.
- **"Routine, nothing to do now" is ONE line.** It covers the ordinary deferred passes (image
  placeholders, the SEO draft, links to pages not built yet). **Do not explain what these are, I already
  know.** Only expand if something is genuinely unusual (for example no suitable placeholder was possible).
- **No internals in the report.** Element ids, `.ees-*` classes, counts and measurements belong in the
  page record, not the message to me.
- **Next page must be genuinely unbuilt** (from step 4), preferring the same type so components are
  reused. If several are equally next, give two or three triggers so I can choose or run them in
  parallel. If **every page is built**, replace the trigger with: "All pages are built. Next phase: run
  `source-images.md`, then `seo-meta.md`, then `review-and-changes.md`." Never suggest a page that
  already has a record, and do not start building it.
