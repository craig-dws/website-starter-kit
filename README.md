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

## Files shared with the AI Web Design System

These files are copies of the design system's. **Change them there first, then sync the wording across
verbatim**, so the two repos cannot drift. A few carry a deliberate kit-only difference: keep it
through the sync rather than letting a verbatim copy delete it.

| File | Intended difference from the design system's copy |
|------|---------------------------------------------------|
| `docs/19_implementation_runbook.md` | None, byte-identical |
| `docs/23_best_practices.md` | None, byte-identical |
| `.claude/agents/keyword-researcher.md` | None, byte-identical |
| `.claude/agents/content-optimizer.md` | One bullet under Scope and honesty: a site-versus-Doc difference during a build is expected and is not reported, and the one reportable case is live copy with no `CONTENT_CHANGELOG.md` entry |
| `.claude/reference/build-standards.md` | The `See also` path, which is `design/reference/design-for-build-checklist.md` here |
| `.claude/skills/stage-gate/SKILL.md` | Two: that same checklist path, and a sentence in the Gate 3c precondition requiring the PM to confirm `CONTENT_CHANGELOG.md` is complete |
| `.claude/skills/gutenberg-limits/SKILL.md` | Ported from the design system's copy at commit `7cff249`. Kit differences: the description and intro cover rebuilding pages as well as adding them; cross-references point at kit files (`.claude/CLAUDE.md`, `class-naming.md`, `connections/`) instead of the design system's docs 18, 24 and 28 and its prohibition numbers; moving a page to the live site is done by a person; every existing page is snapshotted before it is overwritten, never waived; the page cache is checked with the core's public-page check; "stop and ask" names a table, numbered steps and a run of questions and answers; one extra TODO line for ACF field behaviour and one for REST bases |
| `.claude/skills/existing-site-page/SKILL.md` | Not a copy: the kit's own version, written for the kit's operator and audit trail (claims, page records, `CONTENT_CHANGELOG.md`, report shape), connection-neutral through `.claude/connections/`, and with a "Rebuilding an existing page" section the design system's copy does not have. Sync the three-builder facts in both directions by hand |

**The changelog differences do not go upstream.** The design system treats ZilvaEdge as one optional
content source and deliberately never names `CONTENT_CHANGELOG.md`, because the changelog is part of
the ZilvaEdge handover pack this kit ships. The generic condition belongs there, the operational one
belongs here. `build-log/GATES.md` Gate 8 carries the same requirement, so the skill and the gate
tracker agree.

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
no Astro/Payload clutter, no old design stages, just what a build needs. Other builders arrive as one
file each in `.claude/builders/` and `.claude/connections/`, and only the chosen ones load, so a
Breakdance client never reads them (`START-HERE.md`, "Three choices"). When copying by hand, Claude
asks for the builder, the connection and the design source in the first chat.
