---
name: global-blocks-audit
description: Find the sections that repeat across a site before any page is built, and decide for each one whether it belongs in a template, a global block, a documented pattern, or inline. Use once per build, after the design system is approved and before the first page or template is built. Reads the design and the content together, plus the existing site on a migration. Produces a register the whole build then works from. Build-target neutral; the mechanism differs by target but the decision does not.
---

# Global blocks audit

The pass that stops a CTA band being rebuilt on eleven pages.

Repeated sections are the most common source of avoidable rework on a site build. A
call to action, a testimonial row, an enquiry block, a related-links strip, a trust
bar: each looks like part of the page it is on, gets built inline, and then has to be
changed in eleven places when the client changes the phone number.

**Do this once, before the first page or template is built.** Extracting a shared
section after the fact means editing every page that already has it, re-verifying every
one, and hoping none drifted. Doing it first costs an hour.

## When it runs

After the design system is approved, before the first page or template is built. On a
build with a design-approval gate, that is immediately after it.

It is a **planning pass**, not a build pass. Nothing is written to the site. The output
is a register the rest of the build reads.

## What it reads

Three sources, and the point is reading them **together**. Each on its own misses
things the others catch.

1. **The design.** Every frame available, whether that is a design pack, Figma, or a
   written spec. Look for the same section drawn more than once.
2. **The content.** Every file in `content/`. Repeated copy is evidence a section
   repeats even when only one frame has been drawn. If the same call to action wording
   appears at the foot of six pages, that is a shared section whatever the design shows.
3. **The sitemap.** A section on two of today's pages that will be on nine once phase
   two lands is a shared section now, not later.
4. **On a migration, the existing live site.** If the old site carried an enquiry block
   on twelve pages, the new one almost certainly does too. This is evidence the design
   may not have caught up with.

## The decision, for each repeated section

Four outcomes. Getting the distinction right matters more than finding every candidate,
because the wrong choice creates work in both directions.

| If it appears | It becomes | Why |
|---|---|---|
| On **every page of one type** | **Part of that type's template** | It is chrome for that type. Putting it in the template means one place, and every page inherits it. Never drop a global block onto 300 pages one at a time |
| On **pages of different types**, identically | A **global block** | This is exactly what the mechanism is for. Edited once, reflected everywhere |
| On several pages, but **the content differs per page** | A **documented pattern**, or a global block with dynamic fields where the builder genuinely supports it | Prefer the pattern. A global block you have to fork later is worse than a pattern that was always meant to be copied |
| **Once** | **Inline** | Do not pre-emptively globalise. A block with one instance is indirection with no payoff |

### The threshold

- **Three or more identical appearances:** global block, or template part if they are all
  one type.
- **Two:** judgement. Default to a documented pattern unless they are certain to stay
  identical.
- **Planned appearances count**, where the sitemap says so and a person confirms it.

### What varies is the crux

Most candidates are not fully identical, and the useful question is not "does this
repeat" but **"what is the same and what changes"**.

Record both, explicitly, for every candidate. A section whose heading changes per page
but whose layout, buttons and styling do not is a pattern with one variable, and that is
a different build instruction from a block that is identical everywhere.

If you cannot state precisely what varies, you have not looked closely enough yet.

## The trap in the other direction

Over-globalising is a real failure, not a safe default.

- **A global block is edited once and changes everywhere.** If two instances later need
  to diverge, someone has to unpick it, usually under time pressure.
- **On a builder with a restricted client editing mode, this bites the client.** They
  edit the text of a shared section on one page, and it changes on every page it appears
  on, often without any warning in the interface. That is a support call and a loss of
  trust. Where a section is a global block, **say so in the handover notes** so the
  client knows before they find out.
- **Nested global blocks get confusing fast.** Prefer flat.

## The register

Write the findings to `build-log/GLOBAL-BLOCKS.md`, one row per candidate, and have a
person approve it before building starts. The build then reads it and reuses rather than
rebuilding.

Every row needs: a name, what it is, where it appears, what is identical, what varies,
the decision, and the status once it is built.

**A candidate that was considered and rejected stays in the register**, with the reason.
Otherwise the next person re-litigates it, or worse, quietly globalises it.

## What the build then does

Every page and template prompt checks the register **before** building a section:

- If the section is in the register as a **global block**, insert the existing block. Do
  not rebuild it, and do not build a similar-looking one.
- If it is a **template part**, it is already inherited. Do not add it to the page.
- If it is a **pattern**, copy the documented structure and change only what the register
  says varies.
- **If a section repeats and is not in the register, stop and say so.** The register was
  wrong, which is worth ten seconds now and an afternoon later. Add it rather than
  building the duplicate.

Build each global block **once, on its own, before the pages that use it**, and verify it
in isolation. A shared section built as a side effect of building a page inherits that
page's assumptions.

## Target notes

The decision above is target-neutral. Only the mechanism differs.

- **WordPress plus Breakdance:** global blocks are Breakdance Global Blocks; template
  parts live in the relevant Breakdance Template. Repeating content inside a block uses
  the Post Loop Builder rather than hand-built repetition.
- **Astro plus Payload:** global blocks are components; template parts live in the
  layout. Content that varies comes from Payload rather than from a forked component.

Do not let the mechanism drive the decision. If the right answer is a template part, it
is a template part on both targets.

## Rules

- Run it once, before the first page or template is built. Never after.
- Read the design, the content and the sitemap together, plus the live site on a
  migration.
- State what varies for every candidate. "It repeats" is not a finding.
- Prefer a pattern over a global block you will have to fork.
- Do not globalise a single instance.
- A rejected candidate stays in the register with its reason.
- A person approves the register before building starts. Nothing here is approved by AI.
- Flag every global block for the client handover notes, because editing one changes
  every page it is on.
