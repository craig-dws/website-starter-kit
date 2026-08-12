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

**Normally ZilvaEdge does this for you.** Its `/new-site` command copies this kit to a new folder,
gives it fresh git history, and fills the handover pack from the client's own work: the approved
page copy into `content/`, the condensed strategy into `strategy-brief.md`, the style guide, brand
assets and design brief into `design-pack/`, and the client name into the bracket placeholders. It
refuses to scaffold a client whose pages have not been approved and pulled back from their Google
Doc, so a build folder never arrives holding stale copy.

Ask for it with "new site for [client]".

**By hand, when you need to.** Copy this kit to a new location for the client, give it its own git
history (copy the files then `git init`, do not clone, or the client's repo inherits every other
build's commits), then follow `START-HERE.md`. You will be filling the handover pack yourself; see
the "Where things live" table there for what belongs in it. The kit is lean and Breakdance-focused:
no Astro/Payload clutter, no old design stages, just what a build needs.
