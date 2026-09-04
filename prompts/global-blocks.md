# Global blocks audit

Paste this into Claude Code, in the client folder, **once, after the design system is approved
and before the first page or template is built.** Run it in its own chat.

It finds the sections that repeat across the site and decides what each one becomes. Nothing is
written to the site; the output is a register the rest of the build works from.

Running this after pages are built does not work. Extracting a shared section afterwards means
editing every page that already has it, re-verifying every one, and hoping none drifted.

---

You are running the global blocks audit. Follow the `global-blocks-audit` skill, which holds
the decision rules, the thresholds and the traps. This is a **planning pass**: you write to the
repo and to nothing else.

## Start

1. **Pull the latest** (`git pull`).
2. Read `.claude/CLAUDE.md`, the sitemap, and the `global-blocks-audit` skill.
3. Confirm the design system is approved. If it is not, stop and tell me, because the register
   will name tokens and components that may still change.
4. Claim the work in `build-log/ACTIVE.md`.

## Read all the sources, together

Each on its own misses what the others catch, so do not stop after the first.

- **The design.** Every frame available: the design pack where one exists, otherwise Figma
  scoped one frame at a time, otherwise a written spec. Look for the same section drawn twice.
- **The content**, every file in `content/`. Repeated copy is evidence a section repeats even
  when only one frame has been drawn. The same call to action wording at the foot of six pages
  is a shared section whatever the design shows.
- **The sitemap.** A section on two pages today that will be on nine when the next phase lands
  is a shared section now.
- **On a migration, the existing live site.** If the old site carried an enquiry block on twelve
  pages, the new one almost certainly does. This is evidence the design may not have caught up
  with, so read it and raise the difference rather than assuming the design is complete.

Tell me which sources you actually read and which you could not, before you show me findings.
An audit that only read one frame is not an audit and should say so.

## For each candidate, decide

Use the table in the skill. Four outcomes: part of a type's template, a global block, a
documented pattern, or inline.

Two things to get right, because both create work when they are wrong:

- **Template part versus global block.** If a section is on every page of one type, it belongs
  in that type's template, so every page inherits it. Never drop a global block onto hundreds
  of pages one at a time.
- **What varies.** For every candidate, state precisely what is identical and what changes
  between instances. "It repeats" is not a finding. If you cannot say what varies, you have not
  looked closely enough yet. Where content differs per page, prefer a documented pattern over a
  global block you will later have to fork.

Do not globalise a single instance. Indirection with no payoff makes the site harder to edit,
not easier.

## Write the register

Fill in `build-log/GLOBAL-BLOCKS.md`:

- One row per candidate, with what it is, where it appears, what is identical, what varies, the
  decision, **and the class prefix that follows from it** per
  `.claude/reference/class-naming.md`. The decision and the prefix are the same call, so fill
  them in together rather than leaving the naming to be invented later, page by page.
- **Rejected candidates stay in the register with the reason.** Otherwise the next person
  re-litigates it or quietly globalises it.
- Fill in the client handover table. Every global block is edited once and changes every page it
  appears on, which is rarely obvious in a restricted client editing mode, and the client finds
  out by changing one page and altering six.

## Show me before you finish

Give me, in plain words and in this order:

1. **What is being shared, and roughly how much rework it saves.** Lead with this.
2. **Anything where you are unsure**, with your recommendation and what would tip it the other
   way.
3. **Anything the design does not cover** that the content or the live site says repeats. That
   is a gap in the design, not a build decision, and I may need to go back to the designer.

Then ask me to approve the register. **You do not approve it.** Nothing gets built until it is
approved, because every page after this reads it.

## Finish

1. Log the session in `build-log/BUILD-LOG.md` and record the decisions in
   `build-log/DECISIONS.md`.
2. Release your claim in `build-log/ACTIVE.md`.
3. Emit the handoff block per `.claude/reference/session-handoff.md`. The next session builds
   the global blocks themselves, **one at a time, on their own, before the pages that use
   them**, so each is verified in isolation rather than as a side effect of a page.
