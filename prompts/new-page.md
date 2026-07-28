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
   - The **content** (I paste it or point to the source).
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
- Record the page in `build-log/pages/<slug>.md`, log the writes, and **release your claim** in
  `build-log/ACTIVE.md`.
- **Fill the Deferred passes section** (`.claude/reference/deferred-passes.md`): the Outstanding-images
  table (every placeholder), the internal links that 404 only because their target is not built yet
  (real sitemap slugs), and a drafted **SEO title and meta description** for this page. Record these
  **once, as expected-deferred**, and do not also list them as follow-ups or defects: they are
  resolved by `source-images.md`, by building the remaining pages, and by `seo-meta.md`. A link to a
  slug not in the sitemap, or an un-placeholdered empty image slot, IS a defect, so raise those.
- **Commit and push** the page's files (its record, content, any design or settings changes) with a
  short message. One page per commit: it is the recovery point and how the other machine gets your work
  (see `.claude/reference/git-workflow.md`).
- Stop for my review before the next page.
