# Heading scale — the single source

**Fill this in once, at the design-system stage, before the first page is built.** Every page on the
build then uses the same heading scale. It lives in global variables and is applied through the
shared classes below. **Do not invent per-page heading sizes, and do not style bare `<h1>`/`<h2>`
tags.**

Set [YYYY-MM-DD] from [the Figma frame / the design-system proposal]. Record any operator-approved
departure from the design here, with the date and the reason.

Replace `x-` below with the site's own `css_prefix`.

## The scale

| Class | Desktop | Tablet (<=[bp]) | Phone (<=[bp]) | Used for |
|---|---|---|---|---|
| `.x-h1` | [52 / 60] | [40 / 48] | [32 / 40] | Page title, once per page |
| `.x-h2` | [40 / 48] | [32 / 40] | [26 / 34] | Section headings |
| `.x-h3` | [30 / 36] | [26 / 34] | [24 / 32] | Sub-section and note headings |
| `.x-h4` | [24 / 28] | [24 / 28] | [22 / 28] | Card and callout headings |
| `.x-h5` | [20 / 28] | [20 / 28] | [20 / 28] | Card titles, FAQ questions, names |

There is no eyebrow style. A page carries no small uppercase label above a heading; the only words on
the page are the approved content (ZilvaEdge rule, 2026-10-19).

Sizes are `size / line-height` in px. Every value is a token (`--x-type-size-h2`,
`--x-type-size-h2-md`, `--x-type-size-h2-sm` and so on), never a literal.

The scale must be **strictly descending at every tier**, with no two levels ever the same size.
Write out the three rows and check them, because this is the failure that keeps happening:

- Desktop `[52 > 40 > 30 > 24 > 20 > 18]`
- Tablet `[40 > 32 > 26 > 24 > 20 > 18]`
- Phone `[32 > 26 > 24 > 22 > 20 > 18]`

(The last figure is body text, the same at every width.)

## Rules

1. **Apply the class, do not restyle the tag.** Use `<h2 class="x-h2">`. A heading with no scale
   class falls through to Breakdance's own global heading defaults, which will **not** match this
   scale unless you have explicitly closed that gap (see below).
2. **Semantic level and visual size are separate.** A card heading that must be an `<h3>` for
   document structure still takes `class="x-h5"` if that is its size in the design. Pick the tag
   for outline order and the class for size.
3. **One `<h1>` per page.**
4. **Never hardcode a size in a media query.** If a heading needs a different size at a breakpoint,
   it needs a token.
5. **All levels switch at the same breakpoints.** Do not let H1 change at one width and H2 at
   another.
6. **A colour or alignment variant is a separate modifier class** (`.x-h1--on-dark`), never a
   restatement of `.x-h1`, because `insert-stylesheet` replaces a selector wholesale.

## How this has gone wrong before, so it is not repeated

Three failures from real builds. Check for each before signing the design system off.

- **H2 was made to shrink by borrowing the H3 token.** The moment it shrank it landed exactly on
  H3, so on phone H2 and H3 were both the same size. Each level needs its own tokens at every tier.
- **H1 switched at 1119px while H2 switched at 1023px.** Between those two widths the H1 had
  already shrunk and the H2 had not, so both rendered at the same size and the hierarchy vanished.
- **Responsive sizes were left as literal px inside media queries** by an early page build, which
  broke the token rule invisibly: the page looked right and the scale was no longer a single source.

## Bare `h1`-`h6`: close the gap deliberately

Breakdance derives its own `h1`-`h6` sizes from a **modular scale**: `--bde-base-font-size`
multiplied by `--bde-font-size-ratio` once per level. That will not match a designed scale whose
steps are uneven, and **no single ratio can reproduce one**.

Left alone, any heading that slips through without a scale class renders at Breakdance's size, not
yours. **→** Add a `Design System` stylesheet collection restating the six tag rules against the
same tokens:

```
h1, .bde-h1 { font-size: var(--x-type-size-h1); line-height: var(--x-type-lh-h1) }
```

plus the two breakpoint overrides for each. The tokens stay the single source and the bare tags
simply read them. `selectors.css` loads after `global-settings.css`, and a tag rule ties
Breakdance's own tag rule on specificity, so the later one wins. Every `.x-h*` class still beats a
tag rule, so no built page moves.

Verify on a probe heading injected into a live page, and record the measured figures here.

**Rule 1 above still stands.** Apply the class. These tag rules are a safety net for a heading that
slips through without one, not a licence to stop using the classes.
