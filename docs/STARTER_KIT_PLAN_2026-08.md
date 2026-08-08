---
doc_type: implementation_plan
created_date: 2026-08-08
status: current
repo: website-starter-kit
supersedes: HANDOVER_CONTENT_SYNC_PLAN_2026-08.md, which was drafted and stored in the ZilvaEdge repo rather than here and is now archived there at Planning/archive/
companion_plans: ZilvaEdge Planning/ZE_PLAN_2026-08.md, reporting-portal planning/PORTAL_PLAN_2026-08.md
purpose: Starter-kit changes so a build folder scaffolded by ZilvaEdge works out of the box - the handover pack layout, the content changelog, the live content export that makes reconciliation verifiable, prompt wiring, and the launch-gate reconciliation item.
---

# Starter Kit Plan, August 2026

This plan is self-contained. A session working in this repo can implement it without opening the
other two repos.

Most of it is documentation and prompt wiring. One task, K5, is real new mechanism and it is the
most important thing in the plan.

**The kit stays client-agnostic throughout.** Conventions and empty templates only. Nothing
client-specific is ever committed here.

## 1. What is being connected, and why this repo is involved

Three systems are being joined up. This repo is the third.

| System | What it does | Its relationship to this repo |
|---|---|---|
| ZilvaEdge | Strategy, research and content production. Writes the copy, runs the quality gates, owns the Google Docs the client edits. | Clones this kit into a new client folder and injects a handover pack. Later pulls content changes back out. |
| Reports Portal | Monthly client reporting on Neon Postgres. | No relationship to this repo at all. Ignore it. |
| This kit | The template a client site is built from. WordPress plus Breakdance, staging only. | Receives the handover pack, owns page copy during the build, reports what changed. |

The lifecycle this plan supports:

1. ZilvaEdge writes page copy, the client's editor approves it in a Google Doc, and ZilvaEdge pulls
   it back to markdown. That pulled-back markdown is what "released" means.
2. ZilvaEdge runs `/new-site {Brand}`, which clones this kit into a new client folder and drops in
   the released content plus a strategy brief, a design pack and a sitemap.
3. The web team builds. **During the build, the website repo owns page copy.** ZilvaEdge does not
   edit released pages. The Google Doc is expected to go stale, and that is fine.
4. At launch, and monthly during long builds, ZilvaEdge runs `/content-reconcile`: it reads what
   changed during the build, pulls it back, and refreshes the Google Docs so they match the site.

Step 4 only works if this repo can tell it what changed. That is what this plan delivers.

## 2. The problem this plan actually has to solve

The original draft assumed ZilvaEdge could work out what changed during a build by diffing the
repo's `content/` folder in git.

**That assumption does not hold for this repo, and the reason is structural.**

This is a WordPress and Breakdance build. Page layout and copy live as structured JSON in the
`_breakdance_data` postmeta field on each post, edited through the Breakdance MCP tools or the
builder UI. There are no page files in the repo. When a developer fixes a heading or rewrites a
paragraph in Breakdance, **nothing changes in git**. A diff of `content/` shows only what somebody
remembered to also write back into a markdown file.

So a reconciliation built on the `content/` diff would silently miss exactly the changes it exists
to catch. The Google Docs would then be refreshed to something that is not what the live site says,
and everyone downstream would trust them.

The fix is two inputs with different jobs:

| Input | What it is | What it is good for |
|---|---|---|
| `content/` | The released copy ZilvaEdge handed over | The baseline. What the page was supposed to say. |
| `content/_live/` | An export of what the pages actually say now, from WordPress | The evidence. What the page does say. |
| `CONTENT_CHANGELOG.md` | Human notes, one line per change | The reason. Why it changed, and who decided. |

`content/_live/` is task K5. It is the difference between reconciliation that is verified and
reconciliation that is self-reported.

## 3. A path decision to make first

The prompts already reference a content location, and it is not the one ZilvaEdge will use.

`prompts/final-check.md` reads `design/content/site-facts.md` and `design/content/site-content.md`,
plus `design/sitemap.md`. Those are per-client files that do not exist in the generic kit. Meanwhile
ZilvaEdge's `/new-site` scaffolds into `content/` and `sitemap.md` at the repo root.

Pick one and make it consistent. **The recommendation is root-level `content/` and `sitemap.md`**,
for three reasons: it is what the companion ZilvaEdge command produces, content is not a design
artefact and does not belong under `design/`, and a root-level `content/` folder is where a
developer looks first.

That means K3 also repoints `final-check.md` from `design/content/` to `content/`. Note it in
`build-log/DECISIONS.md` so nobody re-splits it later.

If Craig prefers `design/content/`, then ZilvaEdge's `/new-site` changes instead and this repo
leaves the prompts alone. Either way, decide before K1, because K1 documents the answer.

## 4. The tasks

### K1. Document the handover pack

Add to `START-HERE.md`, in the "Where things live" table:

| Need | Location |
|---|---|
| Released page content, the baseline for the build | `content/` |
| What the pages actually say now, exported from the site | `content/_live/` |
| Condensed strategy, audience, voice, page notes | `strategy-brief.md` |
| Style guide, brand assets, design brief | `design-pack/` |
| Page list and menu structure | `sitemap.md` |
| Every content change made during the build | `CONTENT_CHANGELOG.md` |

Also state the ownership rule, in both `START-HERE.md` and `.claude/CLAUDE.md`:

> During the build this repo owns page copy. ZilvaEdge does not edit released pages while the build
> is live. The Google Doc will go stale during the build; that is expected, and it is refreshed at
> launch when the PM runs ZilvaEdge's content reconciliation.

Say plainly that a build folder arrives with this pack already populated, so a builder who finds a
missing piece knows it is a handover problem to raise, not something to improvise around.

**Done when:** a fresh reader of `START-HERE.md` can say where content comes from, who owns it
during the build, what happens to the Google Docs, and what `content/_live/` is for.

### K2. The CONTENT_CHANGELOG template and the logging rule

Add an empty `CONTENT_CHANGELOG.md` at the repo root. Keep it trivial to fill in, because a
changelog that costs effort does not get filled in:

```markdown
# Content Changelog

Every content change made during this build. One line each. This is how the copy that was written
here gets back to ZilvaEdge at launch.

New pages and sections are NOT written here. They are requested from ZilvaEdge through ClickUp and
arrive as released content. Microcopy is the only exception, see below.

| Date | Page | What changed | Why | Who |
|---|---|---|---|---|
```

Add the rule to `.claude/CLAUDE.md`:

- Any edit to a file under `content/`, and any copy written directly into a page including
  microcopy, gets a changelog line in the same session.
- **Microcopy is the only direct-write exception**: CTAs, button labels, short connective copy. Two
  lines of copy do not go through the full ZilvaEdge pipeline.
- Full new pages or sections are requested from ZilvaEdge through ClickUp and arrive as released
  content in `content/`. Do not improvise a page.

Cross-link it from `build-log/README.md`, since `build-log/` is where the durable session memory
already lives and that is where a builder resuming a session looks.

**Done when:** the template exists, the rule is in `.claude/CLAUDE.md`, and `build-log/README.md`
points at it.

### K3. Wire the handover pack into the build prompts

Prompts in this repo are pasted into Claude Code by hand, not invoked as slash commands. Keep every
edit minimal and in each prompt's existing voice.

- **`guided-build.md` and `advanced-build.md`, Stage 0 orientation.** Read `strategy-brief.md`,
  `sitemap.md` and `content/` as part of reorienting. **Refuse to build a page whose released
  content is missing**, rather than improvising copy. Improvised copy is the single most expensive
  thing that can happen here: it looks finished, it passes a visual review, and nobody finds out it
  was invented until the client reads it.
- **`new-page.md`.** Source the page's copy from `content/`. If it is absent, stop and tell the
  operator to request it from ZilvaEdge, per K2. Microcopy excepted.
- **`plan-changes.md` and `review-and-changes.md`.** Any change touching content also appends to
  `CONTENT_CHANGELOG.md` in the same session.
- **`final-check.md`.** Repoint from `design/content/` to `content/`, per the section 3 decision.

**Done when:** a dry run of `guided-build.md` Stage 0 against a scaffolded test folder orients fully
from the pack, and `new-page.md` pointed at a page with no released content stops with the right
instruction instead of writing something.

### K4. The launch-gate reconciliation item

This repo already has a real gate system: Gates 1 to 8 in `build-log/GATES.md`, with Gate 8 as
launch, and the finer-grained Gates 1b through 3c in `.claude/skills/stage-gate/SKILL.md` where 3c
is launch. The rule throughout is that a person approves a gate and the AI never does. Reconciliation
fits that rule exactly, so add it as a gate item rather than inventing a parallel mechanism.

- **`build-log/GATES.md`, Gate 8.** Add a precondition: content reconciliation complete. The PM
  confirms `CONTENT_CHANGELOG.md` is complete and has run ZilvaEdge's content reconciliation, so the
  Google Docs match the launched site.
- **`.claude/skills/stage-gate/SKILL.md`, Gate 3c.** Same item, same wording.
- **`prompts/final-check.md`.** Add to the pre-launch sweep: confirm `CONTENT_CHANGELOG.md` covers
  every change visible in `content/_live/`, and report any change with no changelog entry. This
  prompt reports and does not fix, which is the correct behaviour here too.
- **`prompts/triage-final-check.md`.** Reconciliation gaps are launch blockers, so they belong in
  the fix plan rather than the deferred list.
- **`build-log/CLEANUP.md`.** Add the reconciliation handoff to the end-of-build punch list.

**Done when:** the final-check output includes the reconciliation item, `CLEANUP.md` lists it, and
Gate 8 cannot be signed without it.

### K5. Export live page content to `content/_live/`

**This task is not in the draft plan. It is what makes reconciliation trustworthy rather than
hopeful.** See section 2 for why it is necessary.

Add a new prompt, `prompts/export-content.md`, that dumps what the site actually says into the repo.

- For each page in `sitemap.md`, read the live page through the Breakdance MCP tools already
  connected for the build, and write its visible text to `content/_live/{slug}.md`.
- **Text only.** Headings in order, paragraphs, list items, button and link labels. No layout JSON,
  no styling, no Breakdance structure. The output is for a human diff and for ZilvaEdge to read, so
  a stable, boring, predictable shape matters far more than fidelity to the builder's internals.
- **Deterministic ordering.** The same unchanged page must produce a byte-identical file on every
  run. If the export reorders anything between runs, every diff becomes noise and the whole
  mechanism is worthless within a fortnight.
- Write a header into each file recording the export date and the page ID it came from.
- Commit the export. The commit is the evidence.

When to run it: after any session that changed page copy, and always as part of `final-check.md`
before launch. Add it to `prompts/README.md` in the rough order-over-a-project list, between
`review-and-changes.md` and `final-check.md`.

Note for whoever builds this: blog posts are ordinary WordPress posts in `post_content` rendered
through one shared Breakdance template, not per-post layouts. Export those from `post_content`
directly. Do not try to read them the same way as Breakdance pages.

**Done when:** running the export on a built site produces one readable markdown file per page,
running it twice with no changes produces no git diff at all, and changing one heading in Breakdance
and re-running produces a one-line diff that names the change.

### K6. Note the kit's own boundaries for the scaffolding command

Small, and it saves the ZilvaEdge side from guessing.

`.claude/CLAUDE.md` here is a template using bracket placeholders: `[CLIENT]`, `[STAGING_URL]`,
`[PRODUCTION_URL]`, `[FIGMA FILE...]`, `[HOST]`, and a choice bracket for the starting condition.
The same style appears in `build-log/BUILD-LOG.md`, `DECISIONS.md`, `GATES.md` and several
`design/reference/` checklists.

Add a short section to `START-HERE.md` listing every placeholder in the kit and which ones a
scaffolding command can fill automatically versus which need a human. `[STAGING_URL]` and `[HOST]`
cannot be known at scaffold time and must stay as brackets, visibly outstanding, rather than being
filled with a plausible guess.

Also record in `README.md` that a new client site is now normally created by ZilvaEdge's `/new-site`
command rather than by hand, while keeping the existing manual copy instructions for when someone
needs to do it directly.

**Done when:** the placeholder list is complete and accurate against a grep of the repo, and a
reader knows which fields arrive filled.

## 5. Sequencing

```
section 3 decision   content/ or design/content/, decide before anything else
K1  document the pack
K2  changelog template and rule
K5  live content export        <- the load-bearing one, do it early
K3  wire into the prompts
K6  placeholder inventory
K4  launch gate item
```

K1 and K2 are documentation and can land immediately. **K5 should come before K3 and K4**, even
though the draft put its equivalent work last, because both of those tasks reference
`content/_live/` and it is easier to wire in something that exists.

K3 is best done alongside ZilvaEdge shipping its `/new-site` command, so the prompts can be tested
against a real scaffolded folder rather than an imagined one.

Roughly 4 to 5 sessions.

## 6. Dependencies with the other repos

**Nothing in this plan is blocked on another repo.** Every task here can be done today.

What the other side is waiting on:

| ZilvaEdge task | Waits for | Why |
|---|---|---|
| `/new-site` scaffolding | K1, K2 | The scaffold has to land in a kit that documents and expects the pack |
| `/content-reconcile` | K2, K5 | It reads `CONTENT_CHANGELOG.md` for the reason and `content/_live/` for the evidence |

The Reports Portal has no relationship with this repo in either direction.

One point of etiquette worth stating, because it will come up. ZilvaEdge's content release commits
into a client's website repo but deliberately **does not push**. The web team pulls, or the operator
pushes on purpose. Nobody's working tree gets rearranged underneath them by a scheduled job.

## 7. Implementation prompt

Paste into Claude Code opened in this repo.

```
Read START-HERE.md, then docs/STARTER_KIT_PLAN_2026-08.md. We are implementing that plan.

This repo is the agency's starter kit template. Keep it client-agnostic: conventions and empty
templates only, never client-specific content. British English, no em dashes, no en dashes, no
double hyphens. Keep edits to the build prompts minimal and in their existing voice.

First, ask me to settle the section 3 path decision: released content at root-level content/ and
sitemap.md, which is what the companion ZilvaEdge command produces, or under design/content/ where
final-check.md currently looks. K1 documents whichever I choose, so do not start until I answer.

Then K1 and K2, the handover pack documentation and the CONTENT_CHANGELOG template.

Then K5, the live content export to content/_live/. This is the important one. This is a WordPress
and Breakdance build, so page copy lives in the _breakdance_data postmeta field and never in a repo
file. A developer editing a heading in the Breakdance UI leaves no git evidence at all, which means
reconciliation based on a content/ diff would miss precisely the changes it exists to catch. The
export is what makes it verifiable. Text only, deterministic ordering, byte-identical output for an
unchanged page. Do not skip the determinism requirement; without it every diff becomes noise.

Then K3, K6 and K4.

At the end of each session, list every file you changed so I can review the diff before committing.
```
