# Design System Rules

These rules apply to the shared agency system and every client system.

## One shared system

Maintain one shared agency design system. Each client uses an Extended Collection that inherits the shared system and overrides only the approved brand values.

Do not fork the shared system. Do not rename an approved variable after it has been used.

## Three variable tiers

| Tier | Purpose | Examples |
|---|---|---|
| Primitive | Raw values without design intent | `blue-500`, `space-4`, `radius-lg` |
| Semantic | Meaning and brand role | `color/brand/primary`, `color/text/body`, `color/surface/card` |
| Component | Where the role is used | `button/background/default`, `card/border/default` |

Semantic variables alias Primitive variables. Component variables alias Semantic variables. A raw value must not appear above the Primitive tier.

## Variable naming

Use forward-slash grouping, lower case and hyphens for multi-word names.

| Group | Examples |
|---|---|
| Brand colour | `color/brand/primary`, `color/brand/secondary`, `color/brand/accent` |
| Surface colour | `color/surface/background`, `color/surface/card`, `color/surface/muted` |
| Text colour | `color/text/heading`, `color/text/body`, `color/text/muted`, `color/text/inverse` |
| State colour | `color/state/success`, `color/state/warning`, `color/state/error` |
| Spacing | `spacing/xs`, `spacing/sm`, `spacing/md`, `spacing/lg`, `spacing/xl`, `spacing/xxl` |
| Radius | `radius/sm`, `radius/md`, `radius/lg`, `radius/full` |

Do not invent a new name if an approved variable already expresses the same role.

## Typography

- Use a type scale based on a 16px root.
- Define approved roles for display, headings, body and utility text.
- Include family, size, weight, line height and letter spacing.
- Test wrapping, long headings and fallback fonts.

## Spacing, radius and elevation

- Use a consistent 4pt or 8pt spacing grid.
- Every gap and padding value must use the approved spacing scale.
- Use the smallest radius and elevation set that supports the design direction.
- Do not add a one-off value because it looks close enough.

## Components

- Name components `Category/Component/Variant`, such as `Button/Primary` and `Card/Feature`.
- Name variant properties clearly, such as `State`, `Size` and `Type`.
- Use variants for states instead of duplicate components.
- Build repeated elements as components.
- Use Auto Layout for master components and responsive sections.
- Set hug, fill and fixed resizing intentionally.
- Avoid detached instances.

## Required states

Interactive elements include the relevant states:

- default
- hover
- focus
- active or pressed
- disabled
- loading
- error and success where relevant

Focus states must be visible.

## Figma structure

Use these Figma pages:

- Cover
- Design System
- Components
- Desktop
- Tablet
- Mobile
- Archive

Name frames by page and size, such as `Home / Desktop` and `Services / Mobile`.

Use these status labels:

| Label | Meaning |
|---|---|
| WIP | Work in progress |
| For Review | Ready for Designer, Project Manager or client review |
| Approved | Approved design |
| Dev Ready | Handoff checklist complete |

## Prohibited practices

- Hardcoded colour values where an approved variable exists
- Manual spacing outside the approved scale
- Unnamed frames, layers, variables or components
- Detached instances without a recorded reason
- Absolute positioning except a deliberate documented overlap
- Client systems that duplicate or rename the shared base
