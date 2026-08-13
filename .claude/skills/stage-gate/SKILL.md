---
name: stage-gate
description: The between-stages checklist that confirms one stage is genuinely finished before the next starts. Use at each lifecycle transition (brief to design, design to build, build to QA, QA to launch). Confirms the required human approval is recorded, the required artefacts exist, and authority is transferring cleanly. Content availability is checked as an advisory, never as a blocker; content reconciliation at launch is a Gate 3c condition.
---

# Stage gate

Every gate needs human approval, and authority transfers at gates rather than
silently (CLAUDE.md; docs/13; docs/25). This skill runs the checklist for a
transition, reports what is done and what is missing, and refuses to declare a
gate passed on the agent's own say-so. AI proposes, humans dispose.

Run it with the transition you are at. It reports; a human approves.

## The gates (docs/25)

### Gate: brief approved (Stage 0 to Stage 1)

- The brief exists in the client folder (site-brief skill), with goals,
  audience, sitemap, competitive summary, and the chosen build target recorded.
- Approved by: PM and client. Confirm the approval is recorded.
- Content: note the expected content source and whether it is present. This is
  advisory only. A missing or placeholder content source does not block the
  gate (CLAUDE.md, Content).

### Gate 1b: design system approved (the important one)

- Variable collections exist (primitive, semantic, component) with aliasing, per
  docs/22 and pilot-artefacts/03_figma_component_and_naming_standard.md.
- The design system checklist passes:
  pilot-artefacts/02_design_system_checklist.md.
- Approved by: Design Lead. This gate is the most-skipped and everything downstream
  inherits it. Do not wave it through.

### Gate 1d: dev-ready handoff accepted (Stage 1 to Stage 2)

- The handover contract is signed:
  pilot-artefacts/04_design_to_development_handover_contract.md.
- Named frames, token names, and breakpoints are present and consistent.
- Establish whether there is a design for every page, or a few reference designs plus a style
  guide, and record which. It determines how internal pages are built (see breakdance-limits).
- Check the design against `design/reference/design-for-build-checklist.md` (complete and correct
  variables, unique frame names, webfonts not system fonts, responsive frames, named sections). Flag
  any gaps to the designer before accepting the handoff.
- Approved by: Dev Lead. An incomplete handoff is rejected, not patched informally.

### Gate 2a: token sync verified

- Tokens were moved by differential merge, never a blind import (token-sync
  skill). A page rendered with the new tokens is spot-checked.
- Approved by: Dev Lead.

### Gates 2b and 2c: builds reviewed

- Homepage, then subpages, each built one at a time from one approved frame,
  each verified with a screenshot diff against Figma.
- Approved by: Designer and QA. Nothing AI-generated ships unreviewed.

### Gate 3a to 3c: QA, UAT, launch

- QA: breakpoints, cross-browser (Chrome DevTools MCP, headless), WCAG 2.2 AA
  (human-certified), Core Web Vitals, token and component adherence, design
  versus build diff. See pilot-artefacts/08_qa_and_accessibility_checklist.md.
- UAT: the client reviews the staging site. Triage feedback by class (docs/25):
  design changes go back to Figma; copy fixes are made on the site, because the
  site is what the client is signing off; new copy, a new page or a new section
  is requested from ZilvaEdge; bugs are fixed on site. Record the reviewed site
  state at the gate.
- Launch: backed up, rollback documented, promoted by a human. Approved by: PM.
- **Gate 3c precondition: content reconciliation complete.** Before launch can be
  signed, confirm the Doc has been refreshed to match the launched site, so
  ZilvaEdge's records and the site agree at the point authority transfers to the
  client. A release that disagrees with the site is caught by ZilvaEdge rather
  than applied silently, but reconciling here is what stops the client's first
  post-launch edit starting from stale copy. The PM also confirms
  `CONTENT_CHANGELOG.md` covers every copy change made during the build, because
  ZilvaEdge's reconciliation reports live copy with no changelog entry as the one
  finding that matters, and an incomplete log turns that signal into noise.

## Where changes go (so build and design do not drift)

Apply the change-class table in docs/25. The rule: if it changes the design it
goes back to Figma; if it changes copy already on the site it happens on the
site; if it needs new copy, a new page or a new section it is requested from
ZilvaEdge. A small on-site CSS nudge for a technical constraint is logged in the
deviation register.

On a regulated client (AHPRA and similar) the copy half is narrower: clinical
claims, outcome or benefit claims, practitioner qualifications and treatment or
service descriptions go back to ZilvaEdge, because the compliance check runs
before the Doc and a site edit never passes it. See `.claude/reference/build-standards.md`.

## The content check is advisory, not a blocker

This is about content **availability**, and it is a separate question from
reconciliation at launch below. Content is a pluggable input from any source and
never blocks a stage (CLAUDE.md). A missing or placeholder content source is not
a finding. If the project does not use the optional ZilvaEdge path, nothing is
missing and the check is skipped. Never make a build wait on content.

**During a build, do not prompt to pull.** A Doc that has moved on from the site
is the expected condition, not a finding: the site owns page copy through the
build (docs/13), so the Doc is meant to be behind it. Pulling would push older
text over newer site copy, and ZilvaEdge refuses that release anyway, so
prompting for it sends someone toward an action the tooling then blocks. The
skill never syncs automatically (docs/24, Section F2).

**At the launch gate, reconciliation is worth surfacing.** Gate 3c requires the
Doc to have been refreshed to match the launched site. Outstanding reconciliation
there is a real blocker, and it is the one place this check has something to
report. This does not contradict the advisory rule above: that rule is about
whether content exists to build with, this is about the Doc and the site agreeing
at the point authority transfers to the client.

## Rules

- Report status honestly: what is done, what is missing, what was skipped. If an
  approval is not recorded, the gate is not passed.
- Confirm a human has approved the gate. The skill does not approve; it prepares the
  approval.
- British and Australian English. No em dashes, no en dashes, no emojis.

## TODO (per project)

- The roles above are the defaults from docs/25 for who typically approves each gate.
  Recording a name is optional; the approval itself is what the gate needs.
