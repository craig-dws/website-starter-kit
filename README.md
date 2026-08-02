# Website Starter Kit

The agency's starter kit for one client's website on **WordPress plus Breakdance**, covering the whole
job in one place: **design through build**. Staging only, never production. One repo per client.

**Start with [START-HERE.md](START-HERE.md).** It runs in two phases:

- **Phase 1, Design** ([`design/`](design/)) — turn the brief into a homepage and a build-ready Figma
  design system, using Claude Design or Cowork, then export the tokens to Breakdance. The brief carries
  the strategy, so the design step designs to it.
- **Phase 2, Build** ([`prompts/`](prompts/)) — connect the Breakdance staging site to Claude Code, then
  build page by page, source images, add SEO, review, and run the pre-launch final check. Every
  lifecycle gate is approved by a human, never the AI.

## What's inside

| Folder | What it is |
|--------|------------|
| `design/` | The design workflow (three prompts) and the design standards it is held to |
| `prompts/` | The build prompts (guided/advanced, new-page, blog, images, SEO, review, final-check, ...) |
| `.claude/` | The client rules (`CLAUDE.md`), settings, hooks, skills, agents and tools for the build |
| `build-log/` | The durable audit trail (log, gates, decisions, per-page records) |
| `docs/` | The build runbook and best practices |
| `.github/` | CI checks (no committed secrets, house style, hook health) |

## Starting a new client build

Clone or copy this kit to a new location for the client, give it its own git history, then follow
`START-HERE.md`. The kit is lean and Breakdance-focused: no Astro/Payload clutter, no old design stages,
just what a build needs.
