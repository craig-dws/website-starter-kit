# Image placeholder

When a page is built without its imagery worked out (any page built without a design, or a design
whose images are not final), **do not invent an image, AI-generate one at build time, or leave the
slot empty and let the layout collapse.** Build a **placeholder block** in the image's slot, at the
correct display dimensions, that says what image is needed. Image sourcing is a **separate pass after
the build** (see `build-standards.md` "Image sourcing" and `prompts/source-images.md`).

The placeholder does three jobs:
1. **Holds the layout.** It occupies the real slot at the real display size, so nothing shifts when
   the final image drops in.
2. **Documents the need in place.** A reviewer sees exactly what image goes here, at what size, and
   that it is outstanding, without cross-referencing a list.
3. **Feeds the sourcing pass.** Every placeholder is also logged in the page record under
   **Outstanding images**, so the post-build pass has a punch-list.

## What it looks like

A dashed-border block, unmistakably a placeholder, sized to the image's slot, containing:
- A small **PLACEHOLDER** eyebrow.
- A **short title**: what the image is (`Glaucoma anatomy diagram`).
- A **one-line description**: what it should show and where it comes from
  (`Awaiting artwork from the designer: the optic nerve head and the drainage angle.`), plus
  **Requested `YYYY-MM-DD`**.
- A **dimensions line**: `<display W x H> display, <2x W x H> supplied` (the size shown on the page,
  and the size to supply, which is 2x for retina).

Build it with the site's own tokens so it reads as part of the build, but keep the dashed border and
the PLACEHOLDER label so it is never mistaken for finished work.

## The block (adapt class prefix to the client)

One Text/HTML element, not a stack of containers. Sized by aspect ratio so it matches the final image.

```html
<div class="ph" style="aspect-ratio: 980 / 468;">
  <div class="ph__inner">
    <p class="ph__eyebrow">PLACEHOLDER</p>
    <p class="ph__title">Glaucoma anatomy diagram</p>
    <p class="ph__desc">Awaiting artwork: the optic nerve head and the drainage angle. Requested 2026-07-27.</p>
    <p class="ph__dims">980 x 468 display, 1960 x 936 supplied</p>
  </div>
</div>
```

```css
.ph { display: grid; place-items: center; width: 100%;
  border: 2px dashed var(--c-border, #9db8d6); border-radius: var(--radius-lg, 16px);
  background: var(--c-surface-2, #eef4fb); text-align: center; }
.ph__inner { padding: var(--space-6, 2rem); max-width: 40ch; }
.ph__eyebrow { font-size: .75rem; letter-spacing: .08em; text-transform: uppercase;
  color: var(--c-primary, #2f6fb0); margin: 0 0 .5rem; }
.ph__title { font-size: clamp(1.25rem, 3vw, 2rem); font-weight: 700;
  color: var(--c-heading, #1c2b3a); margin: 0 0 .5rem; }
.ph__desc { color: var(--c-text-muted, #4a5a6a); margin: 0 0 .75rem; }
.ph__dims { font-size: .8rem; color: var(--c-text-subtle, #7a8a9a); margin: 0; }
```

Use the client's real token names where they exist; the fallbacks above are only so the block still
renders if a token is missing. Match the aspect-ratio to the slot each time.

## Every placeholder gets logged

In the page record (`build-log/pages/<slug>.md`), under **Outstanding images**, one row per
placeholder: what it is, the slot, display size, supply size, and requested date. This is the
punch-list the sourcing pass works from.

## See also
- `build-standards.md` — Images, and the "Image sourcing" post-build pass.
- `prompts/source-images.md` — the pass that finds or creates the real images and swaps them in.
- `limitations.md` — why images are URL-referenced, not media-bound, on the Breakdance beta.
