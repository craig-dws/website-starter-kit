---
name: discoverweb-design-standard
description: Audit a Figma design, design system, or pre-handoff file against the DiscoverWeb agency standard, covering token naming, base-kit rules, banned practices, anti-AI-look constraints, and British and Australian house style. Use during design-system work and before handoff.
---

# DiscoverWeb design standard

> **Single-file markdown edition.** This is the whole standard in one markdown file: the audit skill
> followed by its four reference documents, inlined, and the Cowork setup notes at the end. Use it when
> the packaged `.skill` / `.zip` will not import into your Cowork. Load it as the agency
> design-consistency standard, or paste it in as project instructions.

Version 1.1 | This is the approved DiscoverWeb design standard packaged for Claude Cowork. Re-issue whenever the agency standard or shared design system changes.

## What this is

The agency's design-consistency bar for Cowork. It does one job: audit a design, a design system, or a pre-handoff Figma file against the agency standard, and report honestly what passes and what fails.

It is build neutral. Never phrase a check as a search for a platform-specific class or configuration value.

## What this skill does NOT do (use the Design plugin instead)

Do not rebuild what Anthropic's Design plugin already provides. When the task is generic, defer to those commands and say so:

- Generic hardcoded-value and naming-drift scanning of a Figma file: `/design-system`.
- General design critique: `/design-critique`.
- Generic WCAG 2.2 AA review: `/accessibility-review`. In our system a human certifies accessibility, so treat any scan as assistance, not a certificate.
- UX copy and handoff packaging: `/ux-copy`, `/design-handoff`.

This skill adds only the agency-specific layer on top: our token naming standard, our base-kit rules, our banned practices, our anti-AI-look constraints, and our house style.

## Prerequisites and setup

This skill is most useful when Claude can read the actual Figma canvas. If the person has not set up their tools, give them the setup steps rather than proceeding blind. The steps are in the "Setup" section at the end of this file. In short:

- The person should have the Design plugin and the Figma plugin installed in Cowork, from claude.com/plugins. The Figma plugin needs a paid Figma Dev or Full seat, and it is what lets Claude read and check the canvas.
- If either is missing, walk them through installing it (see Setup below), then continue.

## Two modes, and say which one you are in

State the mode at the top of every audit, because it sets what you can and cannot verify.

- **Canvas mode**: the Figma plugin is connected and you can inspect the file, its variables, and its bindings. All checks below apply.
- **Screenshot or description mode**: you only have an image or a written description. You can do the visual anti-AI-look checks and visible house-style checks. You cannot verify variable bindings, token names, off-scale spacing, or detached instances. Say plainly which checks you could not run, and do not imply a full audit.

## The audit

Report item by item, PASS or FAIL, naming the specific frame, layer, or token. Do not be reassuring. A miss here costs the developer a day. This structure mirrors the agency's pre-handoff self-check so the two feel like one system.

1. **Tokens.** Any hardcoded hex, any off-scale spacing, any typography not bound to a variable. List every instance with its location. This is the most common failure. The naming and scale definitions are in the Naming standard below. The rule that every colour, type, and spacing decision must resolve to a named token comes from the House style below.

2. **Naming.** Any token, component, or variant that breaks the standard. Check variable names and grouping, the spacing and radius scale names, the text-style names, and the `Category/Component/Variant` component pattern. Full tables in the Naming standard below.

3. **Components.** Loose one-off elements that should be components. Components missing variants or states. Auto Layout used on every master component. See the Naming standard below.

4. **States.** Every interactive element with default, hover, focus, active, and disabled. Focus states are mandatory and must be visible. Form states: empty, filled, focused, error, success.

5. **Responsive.** Desktop, tablet, and mobile present for key templates. Exact breakpoint values recorded. Per-section notes on what changes: columns, order, scale, hidden elements.

6. **Accessibility.** Contrast recorded for every text-on-background pair against WCAG 2.2 AA. Accessible names for icons, buttons, and fields. Reduced-motion behaviour noted. Remember a human certifies accessibility; you assist.

7. **Structure.** Any layout that cannot be expressed as flex or grid. Flag it, because it will not build cleanly on either target.

8. **Labels.** Every frame carries a status label (WIP, For Review, Approved, or Dev Ready), and Dev Ready only where it passes.

9. **Content assumptions.** Any layout that breaks when text length changes, and whether the content-length assumption is stated.

10. **Banned practices.** Hardcoded hex in fills or styles, absolute positioning except a documented z-index overlap, manual pixel spacing outside the scale, detached component instances, and unnamed layers, frames, or components. Full list in the Naming standard below.

11. **Anti-AI-look.** Run the five constraints in the Anti-AI-look checklist below, and reject the named generic looks. Report each constraint PASS or FAIL against its pass criteria.

12. **House style.** The design's own copy in British and Australian English, no em dashes, no en dashes, no emojis unless the brand explicitly calls for them. See House style below.

## The anti-AI-look pass

Apply the five constraints in the Anti-AI-look checklist below: spatial rhythm not uniform padding, intentional asymmetry not centred symmetry, unexpected hierarchy not conventional order, colour nuance not default primary and secondary, and constraint-driven creativity. Reject the named generic looks: the warm cream plus serif plus terracotta combination, the near-black plus acid-green look, the hairline-ruled broadsheet layout, everything centred and symmetric with uniform padding, conventional-only hierarchy, and default blues and generic greys standing in for a brand palette.

## Finish every audit with

- A blunt list of what must be fixed before handoff.
- What is acceptable to hand over with a note.
- Your verdict: would this file be accepted or rejected.

## Pass thresholds

- The five anti-AI constraints: five of five must pass.
- Banned practices: zero instances. A single hardcoded hex or off-scale value is a defect, not a detail.
- If items 1 to 3 fail, the file is not Dev Ready regardless of the rest.

## v2: base-kit adherence (switch on once the base kit exists)

These checks are ready but dormant until the agency base kit is built and you have its token list. When you have pasted the base kit's semantic token names into the Token model below (or into the conversation), also check:

- The client file is a Figma Extended Collection that inherits the base kit and overrides only colour, typography family, and radius.
- The base is not forked, and no token is renamed. Token names are an API; once a name ships, changing it breaks every client.
- The three-tier aliasing is intact: semantic aliases primitive, component aliases semantic, and no raw value sits above the primitive tier.
- Semantic is the only per-client brand knob; component structure does not change when the brand does.

The model and its rules are in the Token model below. Until the base kit exists, run v1 (items 1 to 12) only, and say that base-kit adherence was not checked because the base kit was not supplied.

## Rules for you

- The agency standard wins over your general design knowledge. If they disagree, say so and follow the standard.
- Ask rather than assume when a check is ambiguous.
- British and Australian English. No em dashes, no en dashes, no emojis, in your output as well as in the design.
- Never invent a token name. If a needed name is not in the standard, flag it and ask.

---

# Reference material

The four documents the audit refers to, inlined so this is one self-contained file.

## Naming standard and banned practices

The conventions every project must follow. This keeps Figma files machine-readable for the AI workflow and consistent across designers and clients. Source: the agency Figma Component and Naming Standard.

### Variable naming

Forward-slash grouping and semantic names. Lower case, hyphen for multi-word.

| Group | Example names |
|-------|---------------|
| Colour, brand | color/brand/primary, color/brand/secondary, color/brand/accent |
| Colour, surface | color/surface/background, color/surface/card, color/surface/muted |
| Colour, text | color/text/heading, color/text/body, color/text/muted, color/text/inverse |
| Colour, state | color/state/success, color/state/warning, color/state/error |
| Spacing | spacing/xs, spacing/sm, spacing/md, spacing/lg, spacing/xl, spacing/xxl |
| Radius | radius/sm, radius/md, radius/lg, radius/full |

Spacing scale sits on a 4pt or 8pt grid. Record the base value in the Variables collection.

### Text style names

| Style | Use |
|-------|-----|
| H1 to H6 | Heading levels, one H1 per page |
| Body Large | Intro or lead paragraphs |
| Body Medium | Default body text |
| Body Small | Captions, helper text, fine print |

Type sizes are set in rem, based on a 16px root.

### Component naming

- Pattern: Category/Component/Variant, for example Button/Primary, Button/Secondary, Card/Feature, Nav/Header.
- Use variants for states (Default, Hover, Active, Disabled) rather than duplicate components.
- Name variant properties clearly (State, Size, Type).

### Auto Layout

- All master components use Auto Layout.
- Use spacing tokens for gaps and padding, never manual pixel values.
- Set resizing behaviour (hug, fill, fixed) intentionally on each frame.

### Page and frame naming

- Figma pages: Cover, Design System, Components, Desktop, Tablet, Mobile, Archive.
- Frames named after the page or section, for example Home, About, Services, Contact.
- Breakpoint suffix where relevant, for example Home / Desktop, Home / Mobile.

### Status labels

Apply a status label to each screen frame.

| Label | Meaning |
|-------|---------|
| WIP | Work in progress, not ready for review |
| For Review | Ready for internal or client review |
| Approved | Signed off, ready for handover |
| Dev Ready | Handover contract complete, ready to build |

### Banned practices

- Hardcoded hex values in fills or styles. Use colour tokens.
- Absolute positioning, except a deliberate z-index overlap that is documented.
- Manual pixel spacing outside the spacing scale.
- Detached component instances.
- Unnamed layers, frames, or components. No default "Frame 123" names.

## House style

Source: CLAUDE.md, the project constitution.

### Language and typography in copy

- British and Australian English.
- No em dashes, no en dashes, no double hyphens in prose.
- No emojis, unless the brand explicitly calls for them.
- This applies to the design's own copy and to the audit output you produce.

### Copy is design material

Write real words, not lorem ipsum, where content exists. Design against realistic content lengths, and note the content-length assumption so the build does not break with a long heading.

### Token-first, non-negotiable

- Every colour, type, and spacing decision references a token name, so a reviewer and an agent can check it. Without a token name there is no definition of "right".
- No hardcoded colour, type, or spacing value where a token exists. A hardcoded value is a defect.

### Quality floor

- Responsive at the project's defined breakpoints.
- Visible keyboard focus on every interactive element.
- Reduced-motion respected. Ambient animation reads as AI-generated.
- WCAG 2.2 AA. Automated scans assist; a human certifies accessibility.

## Token model and base-kit rules

The model that makes one agency kit serve many clients. Source: the agency Design-System Reuse Model (docs 22).

### The decision

Maintain one shared agency base kit and layer a per-client brand theme on top of it. Do not build a bespoke design system per client. "Custom" client sites come from swapping the brand token layer (colour, typography families, radius, and a small set of brand-specific components) on an unchanging shared foundation (spacing scale, type ramp, component structure, naming). Reserve a fully bespoke system only for a flagship build where the layout paradigm itself is the deliverable.

### The three-tier token model

```
Tier 1  PRIMITIVE   raw values, no meaning        blue-500, space-4, radius-lg
   |  (aliased by)
   v
Tier 2  SEMANTIC    intent, the brand knob         color/brand/primary, color/surface/background
   |  (aliased by)
   v
Tier 3  COMPONENT   where it is used               button/background/default, card/border/default
```

- Primitive is what a value is. Shared across all clients. Rarely changes.
- Semantic is what a value means. This is the per-client brand knob. Retheme a client by changing semantic (and where needed primitive) values only.
- Component is where a value is used. Aliases the semantic layer. Structure stays identical across clients, so a component never changes when the brand does.

Never a raw value above tier 1. Semantic aliases primitive, component aliases semantic.

### How it maps in Figma

- Model each tier as a Figma Variable Collection, using aliasing so the semantic layer references primitives by name and the component layer references semantics by name.
- Use Extended Collections as the mechanism for "one agency kit, swap per client". Publish the base kit as a collection. Each client is an Extended Collection that inherits the base and overrides only the values that differ (colour, typography family, radius). The client collection stays tied to the parent, so improvements to the base propagate.
- Use modes within a collection for axes inside a single brand (light and dark, breakpoints), not as the primary brand switch.

### The base-kit adherence checks (v2)

Switch these on once the agency base kit is built. Paste the base kit's semantic token names below, then the audit can verify a client file against them.

- The client file is an Extended Collection that inherits the base kit and overrides only colour, typography family, and radius.
- The base is not forked, and no token is renamed. Token names are an API; once a name ships, changing it breaks every client.
- The three-tier aliasing is intact, and no raw value sits above the primitive tier.
- Semantic is the only per-client brand knob; component structure does not change when the brand does.

#### Base kit token list (paste here when the base kit exists)

Not yet supplied. Until this list is filled in, run v1 checks only and state that base-kit adherence was not checked.

## Anti-AI-look checklist

Five constraints that prevent the generic AI look by making the design deviate intentionally from AI statistical defaults. For every constraint, the definition of right is a token. If a spacing, colour, or type decision cannot be named as a token, there is nothing to check it against. Source: the agency anti-ai-design-checklist and web-design skills.

### The named generic looks to reject

These betray AI output. Reject them on sight:

- The warm cream plus serif plus terracotta combination.
- The near-black plus acid-green look.
- The hairline-ruled broadsheet layout.
- Everything centred and symmetric, 50/50 splits, uniform padding everywhere.
- Conventional hierarchy only, where the heading is always biggest and the call to action always boldest.
- Default blues and generic greys standing in for a brand palette.

### Constraint 1: spatial rhythm, not uniform padding

Vary spacing intentionally to create rhythm and hierarchy. A hero breathes more than a footer.

Pass criteria:
- At least three distinct spacing tokens used within a single section.
- Spacing progression follows an intentional rhythm, not one repeated value.
- Some asymmetric spacing is applied to create visual interest.

### Constraint 2: intentional asymmetry, not centred symmetry

Place key elements off centre, or use unbalanced layouts, to create energy.

Pass criteria:
- Hero section is not centred (left aligned or offset).
- At least one 60/40 or 70/30 split is present.
- The key call to action is positioned intentionally off centre.

Human judgement is needed to tell intentional asymmetry from accidental imbalance.

### Constraint 3: unexpected hierarchy, not conventional order

Subvert at least one conventional hierarchy expectation on purpose.

Pass criteria:
- At least one deliberate hierarchy inversion is present.
- The inversion serves an intentional creative concept, not randomness.
- Semantic structure and heading order remain correct for accessibility. Visual inversion must never break the heading order assistive technology relies on.

### Constraint 4: colour nuance, not default primary and secondary

Use brand-specific colour values, defined and named as tokens, traceable to the brand or to the grounded metaphor.

Pass criteria:
- No reliance on the stock default primary blue or default neutral grey.
- At least two brand-specific colour tokens are defined and named.
- The palette is traceable to brand guidelines or to the grounded metaphor. A colour with no rationale is a red flag.

### Constraint 5: constraint-driven creativity

Show evidence of working within an intentional constraint to solve a creative challenge, so the constraint adds conceptual value rather than only removing something. A "do not use X" instruction that just leaves a gap is a fail.

Pass criteria:
- At least one major constraint is identified and documented, with its source.
- The creative solution adds conceptual value, it does not just subtract.
- The solution is integrated into the design concept and expressed through tokens.

Human judgement is needed to decide whether the constraint truly acted as a catalyst.

### Anti-AI-look pass threshold

All five constraints must pass. If fewer than five pass, return to design refinement before handoff.

---

# Setup: plugins and Figma connector

### Using this standard in Cowork

If your Cowork supports uploading a skill, use the packaged file. If it does not (or the `.skill` will not import), use **this markdown file** instead: add it as project instructions or knowledge, or paste it into the conversation as the agency design standard. The content is identical.

### Install the required plugins

1. In Cowork, open `Customize`.
2. Open `Plugins`, then select `Browse plugins`.
3. Install the Design plugin.
4. Install the Figma plugin from `Anthropic & Partners`.
5. Confirm both plugins are enabled.

### Configure the Figma connector

1. In Cowork, open `Customize`, then `Plugins`.
2. Open the installed Figma plugin and select its `Connectors` tab.
3. Open the included Figma connector and select `Connect` or `Configure`.
4. Sign in with the Figma account used for agency work and approve the requested access.

The Design plugin supplies general design, accessibility and handoff checks. The Figma plugin supplies Figma skills and the MCP connection. Without an authenticated Figma connector, the skill can check only the supplied screenshots or descriptions and must state that limitation.

### Test the setup

Connect a safe Figma practice file and ask:

```text
Run the DiscoverWeb design-standard skill over this Figma practice file. Do not change
the file. State whether you inspected the live canvas or only a screenshot, then report
PASS or FAIL and list any check you could not perform.
```

The setup passes when Claude identifies the standard, reads the Figma source and returns the audit mode and result without changing the file.
