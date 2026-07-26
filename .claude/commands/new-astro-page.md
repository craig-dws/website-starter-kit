---
description: Build one new Astro page from a named Figma frame, wired to Payload (Target B)
argument-hint: <page-name> <figma-frame>
allowed-tools: mcp__figma__get_design_context, mcp__figma__get_screenshot, mcp__figma__get_code_connect_map, Read, Write, Edit, Bash(npm run:*)
---

Build the single Astro page "$1" so it matches the Figma frame "$2".

Delegate to the astro-component-builder subagent. Enforce these rules:
- Scope to the frame "$2" only.
- Reference code tokens by name; never hardcode values.
- Use Code Connect where components are mapped.
- Build one component per block type; wire content from Payload.
- Commit only this one page. Never touch production.

Then run the project check (astro check or eslint) and a visual QA pass:
screenshot the built page, compare to "$2", and patch any discrepancy using
token references only. Leave the change for human review in Git.
