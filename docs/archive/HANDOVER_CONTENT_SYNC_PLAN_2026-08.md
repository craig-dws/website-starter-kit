---
doc_type: implementation_plan
created_date: 2026-08-07
status: proposed
companion_to: ZilvaEdge GOOGLE_ADS_AND_HANDOVER_PLAN_2026-08.md
purpose: Starter-kit changes so a build folder scaffolded by ZilvaEdge /new-site works out of the box - the handover pack layout, the content changelog convention, and the launch reconciliation step.
---

# Handover Pack and Content Sync Plan - Website Starter Kit Side

Small, mostly documentation. ZilvaEdge's `/new-site {Brand}` clones this kit and injects a handover
pack; the kit needs to expect it. The kit itself stays client-agnostic - nothing client-specific is
committed here, only the conventions and empty templates.

## K1. Document the handover pack (S)

- Add to START-HERE.md "Where things live":

  | Need | Location |
  |---|---|
  | Released page content (system of record during build) | `content/` |
  | Condensed strategy, audience, voice, page notes | `strategy-brief.md` |
  | Style guide, brand assets, design brief | `design-pack/` |
  | Page list and menu structure | `sitemap.md` |
  | Every content change made during the build | `CONTENT_CHANGELOG.md` |

- State the ownership rule in START-HERE.md and `.claude/CLAUDE.md`: **during the build this repo
  owns page copy.** ZilvaEdge does not edit released pages while the build is live; the Google Doc
  is expected to go stale and is refreshed at launch by ZE's `/content-reconcile`.
- Done when: a fresh reader of START-HERE.md knows where content comes from, who owns it during the
  build, and what happens to the Google Docs.

## K2. CONTENT_CHANGELOG.md template + logging rule (S)

- Add an empty `CONTENT_CHANGELOG.md` template: date, page, what changed, why, who. One line per
  change is enough - it exists so launch reconciliation knows exactly which pages to pull back.
- Rule in `.claude/CLAUDE.md`: any edit to files under `content/`, and any copy written directly
  into pages (including microcopy - CTAs, labels, short connective text), gets a changelog line in
  the same session. New full pages or sections are NOT written here - they are requested from
  ZilvaEdge via ClickUp and arrive through `/content-release`; microcopy is the only
  write-it-here exception.
- Done when: the template exists and the build prompts reference the rule.

## K3. Wire the pack into the build prompts (S-M)

- `guided-build.md` / `advanced-build.md` Stage 0: read `strategy-brief.md`, `sitemap.md` and
  `content/` as part of orientation; refuse to build a page whose released content is missing
  rather than improvising copy.
- `new-page.md`: source the page's copy from `content/`; if absent, stop and instruct the operator
  to request it from ZilvaEdge (per K2), except microcopy.
- `plan-changes.md` / `review-and-changes.md`: any change touching content also appends to
  CONTENT_CHANGELOG.md.
- Done when: a dry-run of guided-build Stage 0 on a scaffolded test folder orients from the pack,
  and new-page on a missing-content page stops with the correct instruction.

## K4. Launch reconciliation step (S)

- Add to `final-check.md` and `build-log/CLEANUP.md`: before launch sign-off, confirm
  CONTENT_CHANGELOG.md is complete, then hand to the PM to run ZilvaEdge `/content-reconcile`
  (pulls changed pages back and refreshes the Google Docs). Launch gate includes "reconciliation
  done" - the human approves it, as with every other gate.
- Done when: the final-check output includes the reconciliation item and CLEANUP.md lists it.

## Sequencing

K1 -> K2 -> K3 -> K4, roughly 2-3 sessions. K1/K2 can land now; K3 is best done alongside ZE's
`/new-site` (Z3) so the prompts are tested against a real scaffolded folder.

## Implementation prompt

Paste into Claude Code in this folder to begin:

```
Read START-HERE.md, then docs/HANDOVER_CONTENT_SYNC_PLAN_2026-08.md. We are implementing that
plan. This repo is the agency's starter kit template - keep it client-agnostic: conventions and
empty templates only, no client-specific content. British English, no em or en dashes.

Do K1 and K2 first (documentation and the changelog template), then K3 (wiring the handover pack
into the build prompts), then K4 (the launch reconciliation step in final-check and CLEANUP).
Keep edits to the build prompts minimal and consistent with their existing voice. At the end,
list every file you changed so I can review the diff before committing.
```
