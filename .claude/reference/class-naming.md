# CSS class naming

The agency convention, for every site from September 2026.

**The prefix states the blast radius.** That is the whole point of it. A developer looking at
`sw-section` knows before they touch it that changing it changes every page. A developer
looking at `sc-quotes` knows it changes one section. Nobody has to go and find out.

## The five prefixes

Widest reach first.

| Prefix | Scope | Change it and | Example |
|---|---|---|---|
| `sw-` | **Sitewide** | every page changes | `sw-section`, `sw-container`, `sw-btn` |
| `gb-` | **Global block** | every page carrying that block changes | `gb-cta-band`, `gb-enquiry` |
| `wg-` | **Widget** | every instance of that component changes | `wg-quote-card`, `wg-product-card` |
| `pg-` | **Page only** | one page changes | `pg-home__hero`, `pg-about__team` |
| `sc-` | **Section only** | one section changes | `sc-quotes`, `sc-standards-table` |

`sw-` is the design system's own furniture: sections, containers, buttons, prose. `gb-` is a
specific reusable region that exists once and is placed on many pages. `wg-` is a reusable
component that can appear anywhere, many times, including several times on one page. `pg-` and
`sc-` are local.

## The rule that makes it work

**If a class needs to reach further than its prefix says, rename it.**

An `sc-` class that turns out to be needed on another page becomes `wg-` or `gb-`, and every
use is updated. It is a rename, not a quiet promotion.

A prefix that lies is worse than no prefix at all, because someone edits an `sc-` class
believing one section will change and breaks four pages. The prefix is only useful while it is
true.

## Where the prefix comes from

Not from taste. From `build-log/GLOBAL-BLOCKS.md`.

The global blocks audit already decides, before the first page is built, whether each repeating
section is a template part, a global block, a pattern, or inline. **That decision is the
prefix**, so the two are the same decision written twice:

| Register says | Prefix |
|---|---|
| template part, or design system furniture | `sw-` |
| global block | `gb-` |
| pattern, reused component | `wg-` |
| inline, on one page | `pg-` |
| inline, within one section | `sc-` |

Run the audit first. Then the naming follows from it rather than being invented per page.

## Multi-word names, children and variants

Hyphens between words. BEM for structure.

```
sc-quote-name              the block
sc-quote-name__title       a child element, double underscore
sc-quote-name__title--lg   a variant, double hyphen
```

The only underscores in a class are BEM's double underscore. Never use a single underscore as a
word separator, or the two meanings sit side by side and become unreadable.

Lower case throughout. No camelCase. No abbreviations a stranger would have to guess.

## State classes

State is unprefixed and uses `is-` or `has-`:

```
is-open   is-active   is-loading   has-error
```

**A state class is never styled on its own.** It is always qualified:
`.wg-quote-card.is-active`, never `.is-active`. Otherwise one state class collides across the
whole site.

## Why there is no client prefix

Earlier builds used a client initial, for example `ees-hero__copy`. **That is dropped.** On a
single-client site every class is that client's, so the prefix carried no information and used
up the slot that now carries scope, which is information.

Collision risk with the stack is low, because the vendors use their own prefixes: Breakdance
`bde-` and `breakdance-`, WooCommerce `woocommerce-` and `wc-`, Astra `ast-`, Elementor
`elementor-`. **Check once on the first build of a site** that none of the five collide with
anything the active theme or plugins ship, and record it. Do not assume, and do not re-check
every page.

## On Breakdance specifically

- `sw-`, `gb-` and `wg-` classes are **Breakdance global classes**, created once in the class
  list and reused. They are the reason the convention exists.
- `pg-` and `sc-` classes may be global classes too, but their names carry the promise that
  nothing else uses them.
- `insert-stylesheet` holds the design system layer. Selectors written there persist beyond any
  page, so a throwaway or superseded selector is removed with `delete-css-selectors` rather than
  left to accumulate.
- `html-to-page` **silently drops any class with no CSS rule of its own**, including a class
  written purely as a structural hook. Give every class at least one rule, or do not rely on it
  existing.

## Rules

- The prefix states the blast radius, and it must be true.
- Widening the reach of a class is a rename, applied everywhere it is used.
- The prefix comes from `build-log/GLOBAL-BLOCKS.md`, not from taste.
- Hyphens between words, `__` for a child, `--` for a variant, lower case.
- State classes are `is-` or `has-`, and never styled unqualified.
- No client prefix.
- Never a raw value where a token exists. Naming is not a substitute for tokens.
