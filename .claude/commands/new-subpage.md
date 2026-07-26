---
description: Build one new subpage from a named Figma frame, tokens only, staging only
argument-hint: <page-name> <figma-frame>
allowed-tools: mcp__figma__get_design_context, mcp__figma__get_screenshot, Bash(wp breakdance clear_cache:*)
---

Build the single page "$1" on staging so it matches the Figma frame "$2".

Delegate to the builder-builder subagent. Enforce these rules:
- Scope to the frame "$2" only.
- Reference established token names; never hardcode values.
- Map Auto Layout to Section and Div; use the Post Loop Builder for repeating
  content (see the breakdance-limits skill).
- Call the project's bound layout-write capability, never a vendor tool by name.
- Snapshot before any write. Build only this one page.
- Then clear the builder cache and return the staging preview URL.

Then run a visual QA pass: screenshot the built page, compare to "$2", and patch
any layout discrepancy using token references only. Staging only; never
production.
