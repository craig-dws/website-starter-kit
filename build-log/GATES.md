# Gates — [CLIENT]

A gate is a checkpoint that needs a person's approval before the next stage starts. The AI
never approves a gate; a person does. Mark it Approved once it has been approved. You do not
need to name who owns it, just approve the work when it is right.

| # | Gate | Status | Date | Note |
|---|------|--------|------|------|
| 1 | Brief approved | Not yet | | |
| 2 | Design approved and handed to build | Not yet | | designed and approved internally before it reaches this repo |
| 3 | Build's design system approved | Not yet | | tokens and responsive the build derived, approved before building pages on them |
| 4 | Build complete on staging | Not yet | | |
| 5 | Accessibility passed (WCAG 2.2 AA) | Not yet | | |
| 6 | SEO / performance / AI-readiness QA | Not yet | | |
| 7 | Client UAT sign-off | Not yet | | |
| 8 | Launch approved (backed up, to production) | Not yet | | needs content reconciliation complete |

**Status:** Not yet | In progress | Approved | Blocked.

Notes:
- Your flow is design, internal approval, then handoff to build. So by the time a design
  reaches this repo it is already approved. Gate 2 just confirms that.
- Gate 3 covers anything the build had to derive that the design did not specify, for example
  a responsive scale for breakpoints that were never drawn. Approve it before building pages.
- Gate 7: UAT feedback is on the built site, which is what the client is reviewing.
  Copy fixes are made on the site and mirrored into `content/{slug}.md`, and logged in
  `CONTENT_CHANGELOG.md`. Substantial new pages or sections are requested from ZilvaEdge.
- Gate 8 is the single authority-transfer point, to production, backed up, by a person.
- **Gate 8 has a precondition: content reconciliation is complete.** Before it can be approved,
  the PM confirms `CONTENT_CHANGELOG.md` covers every copy change made during the build, and has
  run ZilvaEdge's content reconciliation so the client's Google Docs match the launched site.
  Without it the Docs stay frozen at whatever was approved months earlier, and the first person
  to notice is usually the client. `prompts/final-check.md` reports the gaps; closing them is the
  PM's, with ZilvaEdge.
