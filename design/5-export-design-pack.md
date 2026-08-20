# 5. Export the design pack (so the build never needs Figma)

Run this **once, when the design is approved and final**, on the machine that has the Figma connection.
It pulls everything the build needs out of Figma and writes it into `design-pack/`, so the developer can
clone the repo and build the whole site without a Figma dev seat.

This is the **design-to-build handover step**. Everything before it is design; everything after it reads
the pack instead of Figma.

## Who runs this, and why

Building needs to read measurements, colours and structure out of Figma, and that needs a Figma dev
seat. A view seat lets a developer **look** at the design, which is genuinely useful, but not extract
from it. Rather than buy a seat per developer, the person who already has one runs this once and commits
the result.

**The pack is a snapshot, and that is safe here because the design is final when you run it.** If the
design changes afterwards, the pack is wrong and silently so, because the build has no way to notice.
Re-run this prompt after any design change and commit the new pack. Nothing else re-syncs it.

## Before you paste

- The design is **approved and final**. Do not run this mid-design.
- The **Figma connection is live** in Claude Code. Run `/mcp` and confirm it.
- You have a **Copy link to selection for every frame the build needs**, one per frame. Right-click the
  frame in Figma, choose Copy link to selection, and paste it. **Whole-file reads overflow on any real
  multi-page file**, so the export works frame by frame and there is no way around collecting the links.
- Any **mesh gradients exported by hand as PNGs**, ready to drop in. Mesh gradients and other
  editor-only fills are invisible to every extraction route, so no tool can pull them. That is a known
  limitation, not something to retry.

Paste the block below into **Claude Code**, in the client folder, with the Figma connection live.

---

You are exporting the approved Figma design into `design-pack/`, so that a developer with no Figma
access can build the entire site from this repository alone. This is a **read-only job on Figma** and a
**write-only job on the repo**. You do not touch any website, staging or otherwise.

Work to `.claude/reference/build-standards.md` for naming and alt text. Read
`.claude/reference/limitations.md` first, in particular what Figma cannot export.

I am a project manager, not a developer. I never run commands. You run everything; I paste links and
answer questions.

## Start

1. Read `.claude/CLAUDE.md`, `design/sitemap.md` if it exists, and `.claude/reference/limitations.md`.
2. **Ask me for the frame links, all at once.** Tell me to paste one line per frame in this shape, and
   give me the list of pages from the sitemap so I can work through it:

   ```
   <page-slug> | <desktop|tablet|mobile> | <Copy link to selection>
   ```

   Several lines can share a page slug where the design has separate desktop, tablet and mobile frames.
   **Identify every frame by the node id in its link, never by its name**, because names repeat.
3. **Ask me one question about mesh gradients:** which frames, if any, contain a mesh gradient or other
   editor-only fill. Tell me to drop the hand-exported PNGs into `design-pack/assets/manual/` and name
   each one after the section it belongs to. Do not attempt to extract them yourself and do not report
   the flat colour underneath as if it were the real fill.
4. Create the folder structure in `design-pack/` per `design-pack/README.md`.

## Export the tokens, once

Read the design tokens from Figma with the variable-definitions capability, scoped to the collection
rather than the whole file. Write two files:

- `design-pack/tokens/tokens.json`, the raw resolved tokens exactly as read.
- `design-pack/tokens/tokens.md`, the same thing grouped and readable: colour, typography, spacing,
  radius, effects, each with its token name and resolved value.

In `tokens.md`, **flag every token that has no clean home in Breakdance** rather than inventing a
mapping. Colour and typography map at the semantic tier, spacing maps only partially, and the component
tier has no clean home. Flagging it now saves the developer discovering it mid-build.

## Export each frame, one at a time

For every frame I gave you, in sitemap order. **Never widen a read to the whole file**; if a read
truncates or overflows, that is the frame being large, so tell me and move on rather than retrying the
same call.

1. **Read the design context** for that node id only.
2. **Take the screenshot** and save it as
   `design-pack/frames/<page-slug>/reference-<desktop|tablet|mobile>.png`.
3. **Pull the raster assets** in that frame. Save them at source resolution into
   `design-pack/assets/images/`, renamed to **descriptive, SEO-friendly, kebab-case filenames derived
   from what the image shows and its role**, never the Figma layer name and never a hash. Name by
   section where it helps. **Do not resize or compress them here**: the build does that at upload time,
   using the display size you are about to record, and doing it twice loses quality for nothing.
4. **Pull the SVGs** (icons and logos) into `design-pack/assets/svg/`, as `.svg` files with the same
   naming rule. These are inlined by the build, never uploaded, because WordPress blocks SVG uploads.
5. **Write `design-pack/frames/<page-slug>/frame.md`** with these sections:
   - **Source**: the node id, the frame's width, and the date read.
   - **Structure**: the sections top to bottom, and for each one its layout, spacing, and the elements
     it holds. Enough detail that someone can rebuild it without seeing Figma.
   - **Tokens used**: the token names, not the resolved values. Where the design uses a value that is
     not a token, record the value and **flag it as off-scale**, because it means the design system has
     a gap the developer will otherwise paper over with a hardcoded number.
   - **Assets**: a table of every image and SVG in this frame, with its saved filename, what it shows,
     its **display size in the design** and the **supply size** (twice the display width), and
     **proposed alt text** written from what the design shows. Content images get descriptive alt;
     decorative icons get empty alt. Follow `.claude/reference/alt-text-guidelines.md`.
   - **Responsive**: what changes between the desktop, tablet and mobile frames where they exist. Where
     only a desktop frame exists, say so plainly and say nothing more, because the build derives the
     responsive layer and records it for design review.
   - **Flags**: anything the developer must be told. Mesh gradients and the PNG supplied for each.
     Anything that did not export. Anything ambiguous. **An empty Flags section is a claim, so only
     write one when it is true.**

## Finish

1. **Write `design-pack/MANIFEST.md`**: the date exported, the Figma file, every frame exported with its
   node id, the token count, the asset count, and, separately and prominently, **what is missing**:
   frames on the sitemap with no link supplied, assets that failed to export, and mesh gradients still
   awaiting a hand-exported PNG.
2. **Check the pack against the sitemap.** Any page in `design/sitemap.md` with no frame folder is a gap.
   List them.
3. **Commit** `design-pack/` with a short message. Do not push without asking me.
4. **Send me the report below.** Then stop.

### The report to send me

```
## Design pack exported

Status: <Complete, the build can run without Figma  |  Exported, but N gap(s) need you first>

What is in it: <one or two plain sentences: how many pages, how many images, how many icons.>

Needs you:
- <plain actions only I can do, e.g. "3 mesh gradient PNGs for the home page hero", or "Nothing.">

Gaps against the sitemap: <"None." or the pages with no design frame supplied.>

Off-scale values found: <ONE line: how many, and that they are listed in the frame files. Or "None.">

Hand this to the developer:
Clone the repo, then follow prompts/guided-build.md. The design is in design-pack/, not Figma.
```

Rules for the report:

- **Status first, and honest.** "Complete" only when every sitemap page has a frame folder and nothing is
  waiting on me. A pack with holes in it is worse than no pack, because the developer trusts it.
- **Never say a frame exported when the read truncated.** Say what failed and which page it was on.
- **Do not list every asset in the report.** They are in the frame files. One count is enough.
- **No node ids, no hex values, no token names in the report.** Those live in the pack.

British and Australian English. No em dashes, no en dashes, no double hyphens in prose. No emojis.
