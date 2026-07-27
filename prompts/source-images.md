# Source images (post-build pass)

Paste this into Claude Code (in the client folder) to **find or create the real images and swap them
in for the placeholders**, once pages are built. This runs after the layout is settled, not during a
build, so images pour into a stable layout. It works from the **Outstanding images** lists in the
page records.

---

You are running the image-sourcing pass. Work to `.claude/reference/build-standards.md` ("Images" and
"Image sourcing") and `.claude/reference/image-placeholder.md`. Staging only, human-approved.

## Start
1. Read `.claude/CLAUDE.md`, `build-standards.md`, `image-placeholder.md` and `limitations.md`.
2. **Gather the punch-list.** Read every `build-log/pages/*.md` and collect all **Outstanding images**
   rows into one list: page, slot, subject, display size, supply size. Show it to me before sourcing.
3. Ask me **where the client gallery is** (a folder path or a link), or confirm there is none. Ask
   whether stock or AI generation is approved for the gaps, and any licensing constraint.

## Source (one image at a time, in this order)
For each outstanding image:
1. **Client gallery first.** If there is a gallery, search it for an image matching the slot's subject
   and orientation. Use it only if it genuinely fits; do not force a poor match.
2. **Else stock or AI**, if approved. Source or generate one fit for purpose and correctly licensed.
   Record the source and licence in the page record.
3. **Optimise and upload** with `.claude/tools/optimize-and-upload.py` (size to ~2x display width,
   compress), set descriptive alt per `alt-text-guidelines.md`. Every image goes through this,
   including AI-generated ones.
4. **Swap the placeholder for the image** in the page (referenced by URL, media binding is a known
   limit), verify the rendered HTML keeps the alt, and check the layout still holds at the slot size.
5. **Update the page record:** clear or tick the Outstanding-images row, note the source and licence.

## Finish
- **Stop for my review** with the before/after per page. Do not mass-replace without showing me.
- Leave any image I have not approved as a placeholder; a placeholder is a safe resting state.
- Note the human still needs to **bind the images to the media library in the builder** for `srcset`
  (the MCP cannot bind media, see `limitations.md`); flag which pages need that pass.
