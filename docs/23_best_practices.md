# 23. Best Practices: Web Design, Web Development, and AI for Web Dev

Status: v0.2 | Date: 21 July 2026 | Owners: Designer and Dev Lead

A consolidated reference of the standards this system expects, written to apply to **both build targets** (WordPress with Breakdance, and Astro with Payload). The workflows (03, 04), the target docs (08, 08b), the QA checklist (pilot artefact 08), and the scorecard (11) enforce these. This document is the single place they are explained.

Where a rule differs by target, both are given.

## Part A: Web design best practices

- **Design to a system, not to a page.** Every colour, size, and space comes from a token (see 22). No one-off hex values or arbitrary spacing. This is what makes AI translation reliable and sites consistent, on either target.
- **Use Auto Layout for everything.** Absolute positioning is banned except for deliberate z-index overlaps. Auto Layout maps cleanly to Breakdance's Layout Engine and to flex or grid in Astro components.
- **Design all three breakpoints explicitly.** Do not leave responsive behaviour to be guessed. State breakpoints and how elements reflow, stack, or hide.
- **Respect content reality.** Design with realistic content lengths, not perfect placeholder text, and note content-length assumptions so the build does not break with long headings.
- **Accessibility is a design responsibility.** Meet WCAG 2.2 AA at design time: colour contrast, visible focus states, logical heading order, labelled forms, meaningful alt text. Design the focus and error states, not just the happy path.
- **Design for the target's editing model.** On Breakdance, clients edit visually within Client Mode limits. On Astro plus Payload, clients edit structured fields and reorder blocks, they do not drag layout. Design so every routine client edit is a field change or a block reorder.
- **Keep it fast by design.** Avoid unnecessary custom fonts and heavy imagery. Performance starts with design choices, not just developer optimisation.
- **Clarity over cleverness.** Conventional, learnable interfaces beat novel ones for client marketing sites. Reduce cognitive load.

## Part B: Web development best practices

- **Preserve editability.** Text stays as text, not baked into images. On Breakdance use flexible containers so editors can change length and order. On Astro plus Payload keep the content model honest so an editor never needs a field the design cannot render.
- **Build from tokens.** The target's token layer (Breakdance Global Settings, or the Tailwind config and CSS custom properties in Astro) mirrors the Figma tokens. Never hardcode a colour or type value when a token exists. A hardcoded value is a defect on both targets.
- **Use native building blocks first.** On Breakdance: Section, Div, Columns, Post Loop Builder, and Global Blocks before Element Studio. On Astro: one component per Payload block type and per layout region, before reaching for bespoke one-offs.
- **Use dynamic data for anything repeating.** Blog cards, team members, and listings use the Breakdance Post Loop Builder, or a Payload collection rendered through an Astro component, never statically duplicated blocks.
- **One change surface at a time.** Run one AI session per site. Concurrent agents writing to the same Breakdance database, or the same repository branch, risk conflicting writes.
- **Back up before you write.** On Breakdance, bracket every database-affecting operation with a backup and a clear cache. On Astro plus Payload, work in version control so every change is diffable and revertible, and take a database snapshot before any content migration.
- **Test at every breakpoint and in real browsers.** Automated scans (Lighthouse, axe) assist but do not replace human testing.
- **Version control and staged deployment.** Work on staging, promote to production deliberately with a rollback plan. Never edit production directly. For Astro this is a Git deploy; for WordPress it is a backed-up migration.
- **Document deviations.** When the build must differ from the design, record it in the deviation register with a rationale. Never leave a silent difference.
- **Plan the publish path.** On Breakdance, content is live on save. On a static Astro site, a client edit in Payload must trigger a rebuild and redeploy (a publish webhook) or use on-demand rendering. Decide this per client.

## Part C: Using AI for web development (the rules that matter most)

- **AI proposes, humans dispose.** Every AI output is a draft. No AI output is approved by AI. This is the single most important rule in the whole system.
- **Scope prompts tightly.** The Figma get_design_context tool can exceed token limits on large pages. Work one frame or one page at a time, not whole files.
- **Reference tokens, never values.** Prompts must tell the agent to use established token names (Breakdance globals, or the Astro or CSS token layer), not to hardcode colours or spacing. This keeps output consistent and reusable.
- **Prefer the safer write surface.** On Breakdance the safest surfaces are WP-CLI settings and Global Settings JSON, and a differential merge is mandatory over a blind import. On Astro plus Payload the safest surface is editing version-controlled code and the schema, which is inherently safer because there is no raw-PHP execution.
- **Verify visually.** After the agent builds a page, capture a fresh screenshot (get_screenshot), compare it to Figma, have the agent patch, then clear cache or rebuild.
- **Use Code Connect on Target B.** It is the biggest accuracy lever for Figma-to-code, because it makes the agent reuse real components instead of inventing new ones. **It does not apply to Target A**: Code Connect binds Figma components to *code* components, and Breakdance elements are builder nodes in serialized JSON, so there is nothing to bind to. On Target A the equivalent is a reviewed, version-controlled Figma-to-Breakdance mapping table (see 07). Do not claim parity between the targets.
- **Treat the AI environment as privileged.** Novamira's execute-php has full site privileges and its sandbox is not a security boundary. Protect wp-config.php and production paths with permission rules and hooks, and keep the pipeline on staging only. The Astro plus Payload target avoids this class of risk entirely.
- **Do not over-trust the write path.** The mature, reliable half of the pipeline is reading from Figma and scaffolding. Writing full layouts into Breakdance is early-stage; keep it supervised. Writing Astro components is normal code work under normal review.
- **Keep context clean and per-client.** One Claude project per site. Never let one client's content or memory bleed into another's.
- **Measure quality, not draft speed.** A fast rough draft that takes hours to fix is not a win. Track defects, rework, and end-to-end delivery (see 11).
- **Prefer the governed path where it exists.** For WordPress, the core AI Client, Abilities API, and mcp-adapter are the governed options where they can do the job. For content, they beat raw PHP execution.
- **Log what breaks.** Every rejected output, manual rewrite, and workflow bypass goes in the decisions and failures log (21). That log is how v0.1 becomes a better v0.2.

## The three rules to remember if you forget everything else

- **AI never gets the final say.** A human approves at every gate.
- **Protect the environment.** Staging only for WordPress AI writes, back up before writes, differential merge never blind import, and no agent on production.
- **Token first, one page at a time, verified.** Everything comes from a token, built one frame or page at a time, and checked against the design.

## Related documents

- [08_breakdance_and_wordpress_plugin_stack.md](08_breakdance_and_wordpress_plugin_stack.md) - Target A specifics
- [08b_astro_payload_build_target.md](08b_astro_payload_build_target.md) - Target B specifics
- [11_test_and_measurement_scorecard.md](11_test_and_measurement_scorecard.md) - how these standards are measured
- [22_design_system_reuse_model.md](22_design_system_reuse_model.md) - the shared token model both targets use
