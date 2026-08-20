# Design pack

**Everything the build needs from Figma, extracted once, so the developer never needs Figma access.**

Building a page means reading exact measurements, colours, structure and assets out of the design, and
that needs a Figma dev seat. A view seat lets a developer look at the design, which is worth having, but
not extract from it. So the person who has the dev seat runs `prompts/export-design-pack.md` once, when
the design is final, and commits the result here. The developer clones the repo and builds from these
files.

**When this folder is populated, it is the design source of truth for the build.** The build reads it
instead of calling Figma, and prompts stop asking for frame links.

**The test for "populated" is one file: `design-pack/MANIFEST.md` exists.** The export writes it last,
so if it is there the export finished. A folder holding only this README is not a pack, and the build
falls back to reading Figma.

## This folder has a second occupant

`design-pack/` is also where the **brand handover pack** lands: the style guide, the brand assets and
the design brief, put here by ZilvaEdge's `/new-site` scaffolder (see the repo `README.md`). That
arrives at the start of a project; the Figma extraction arrives at the end of the design phase.

The two coexist and do not overlap. The extraction only ever writes `MANIFEST.md`, `tokens/`,
`frames/` and `assets/`, so **anything else already in this folder is the brand pack and is left
alone.** If you are looking for the style guide, it is here at the top level, not inside those four.

## The one rule

**The pack is only correct while the design is unchanged.** It is a snapshot with a date on it, and the
build has no way to notice that the design moved underneath it. So:

- Export it **only when the design is approved and final**.
- **Any later design change means re-running the export and committing the new pack.** Nothing else
  re-syncs it, and a stale pack fails silently: the page gets built, it looks finished, and it is the
  old design.
- `MANIFEST.md` carries the export date. If it looks old and the design has moved on, stop and re-export
  rather than building on it.

## What is in here

```
design-pack/
  README.md          this file
  MANIFEST.md        what was exported, when, and what is missing
  tokens/
    tokens.json      the resolved design tokens, raw
    tokens.md        the same, grouped and readable, with Breakdance mapping flags
  frames/
    <page-slug>/
      frame.md              structure, tokens, assets, responsive notes, flags
      reference-desktop.png the image the built page is checked against
      reference-tablet.png  where the design has one
      reference-mobile.png  where the design has one
  assets/
    images/          raster images at source resolution, kebab-case, named from the design
    svg/             icons and logos as .svg markup
    manual/          mesh gradients and anything no tool can extract, supplied by hand
```

## How the build uses each part

| Part | What the build does with it |
|---|---|
| `tokens/` | Loads into Breakdance Global Settings. The `token-sync` skill reads this instead of Figma |
| `frames/<slug>/frame.md` | The page's structure and measurements. This replaces reading a Figma frame |
| `frames/<slug>/reference-*.png` | The image the built page is compared against, in place of a live Figma screenshot |
| `assets/images/` | Resized, compressed and uploaded at build time by `.claude/tools/optimize-and-upload.py`, using the display size recorded in `frame.md` |
| `assets/svg/` | Inlined into the layout. Never uploaded, because WordPress blocks SVG uploads |
| `assets/manual/` | Sampled to reproduce a mesh gradient as a CSS gradient token. **Never uploaded as an image** |

## Images are stored unoptimised, on purpose

The images here are at source resolution. They are **not** ready to go on a website and should not be
uploaded as they are. The build resizes each one to roughly twice its display width, compresses it, and
uploads it, using the display size recorded in the frame file. Optimising twice loses quality for
nothing, so the pack keeps the originals and the build does the one pass.

## Mesh gradients: the thing no tool can extract

A Figma mesh gradient, and other editor-only pattern fills, **export as the flat colour underneath**
through every route: the CSS export, the design context read, and Figma's own image render alike. This
is recorded in `.claude/reference/limitations.md`, where it cost one build about two days.

There is no fix, only a process. The designer flags mesh layers at handoff, the person with the Figma
seat exports each one by hand as a PNG into `assets/manual/`, and the frame file flags where it belongs.
The build then reproduces the wash as a CSS gradient token sampled from that PNG. **The PNG itself is
never uploaded to the site.**

## What the pack does not carry

Worth knowing before you rely on it.

- **Anything not exported.** A page with no frame folder cannot be built. `MANIFEST.md` lists the gaps
  against the sitemap; check it before starting.
- **Follow-up questions.** The frame files are thorough, but they are a fixed dump. Anything they did
  not capture has to come from the person with Figma access. A developer with a view seat can usually
  answer it by looking.
- **Page copy.** That is not a design artefact. It lives in `content/`, released by ZilvaEdge, and the
  rule that a page is not built without it is unchanged.

## If the pack is not here

An empty or missing `design-pack/` is not a fault. It means this build reads Figma directly, which is
the original path and still supported. The build prompts check for the pack and fall back to asking for
frame links when it is absent.

## See also

- `prompts/export-design-pack.md`, the prompt that fills this folder
- `design/reference/handoff-checklist.md`, the designer-side handover check
- `.claude/reference/limitations.md`, what Figma cannot export
- `.claude/reference/build-standards.md`, the naming and alt-text rules the pack follows
