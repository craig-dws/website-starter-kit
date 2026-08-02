# Design workflow

The design half of a build, kept lean. The **brief** (from ZilvaEdge) already carries the strategy,
audience, voice, page notes, brand colours, fonts and constraints, so the design step turns the brief
into a homepage and a build-ready Figma **design system**, it does not re-do strategy.

There are **two paths to the same result**. Run both on the same brief to see which you prefer, then
standardise on the winner.

## Path A — Claude Design, then Claude Code (best for a build-ready system)
1. **`1-design-in-claude-design.md`** — Claude Design designs the homepage from the brief.
2. **`2-systematise-in-claude-code.md`** — its "transfer to Claude Code" prompt, plus our standard, has
   Claude Code build the Figma design system (three-tier tokens, components with hover, Breakdance
   structure, QA) and produce the Breakdance token export.

## Path B — Cowork (one tool, end to end, gives responsive frames)
- **`3-design-in-cowork.md`** — Cowork designs the homepage plus tablet and mobile, and builds the
  design system, in Figma, in one place.

## Then, either path
3. **Polish in Figma** and approve (one design gate).
4. **Internal pages** — feed the polished homepage and system back to Design or Cowork.
5. **Token export to Breakdance Global Settings** hands over to the build side (`new-page`, etc.).

## The checks (guardrails, not stages)
All three prompts point at the same standards in `reference/`:
- `design-for-build-checklist.md` — is the Figma build-ready.
- the design-system rules, quality standard and anti-AI-look / house-style audit
  (`discoverweb-design-standard` skill).
- WCAG 2.2 AA contrast (the brief flags where a bright accent fails on white).

That is the whole design process: **brief in, homepage and a tokenised Figma design system out, checked
against the standards, exported to Breakdance.**
