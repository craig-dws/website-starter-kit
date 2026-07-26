# Design-for-build checklist (for the designer)

How to set up a Figma design so the AI build gets it right the first time. Every item is here
because something in a real build was harder than it needed to be, the fix is "do it in the design."
This is a living checklist, add to it as we learn more.

## Design tokens (Figma variables) — the foundation
- Define a **complete, correct** set of Figma Local Variables for colours, type, spacing, radii,
  and the container/grid. The AI builds the design system from these; if they are missing or wrong
  it has to derive tokens from the pixels, which then no longer track the design.
- **One variable per role.** Do not leave variables empty, and never let a variable's name disagree
  with its value (e.g. a swatch named "61A3CF" that actually holds #6AB2E3).
  *(Eastwood: 8 variables, 2 empty, ~26 colours actually in use, one mis-named — so all tokens had
  to be re-derived from the frame.)*
- **No near-duplicate colours for the same role** (e.g. two slightly different blues for the same
  eyebrow-on-dark). Pick one, name it.
- Include the "boring" tokens too: **container width, gutter, section padding, card gap, radii,
  icon-tile size.** *(Eastwood used 1440 / 40 / 100 / 27 — put these in variables, not just pixels.)*

## Fonts
- Use **webfonts** (Google Fonts or a licensed webfont), **not system fonts.** Segoe UI, for
  example, is a Windows-only system font that does not load on the web and silently falls back.
  Name the intended brand font; if it is not a webfont, say what the web substitute should be.
  *(Eastwood's body was set in Segoe UI, substituted with Source Sans 3.)*

## Naming and labels
- **Unique, descriptive frame names.** Never two frames with the same name — the AI cannot tell
  which is current. *(Eastwood had two frames both named "Eastwood Eye Surgery-Home".)*
- **Name layers for their content and role**, not "Rectangle 1379". Image layers especially: the
  AI derives filenames and alt text from them, so `surgeon-dr-gagan-khannah` beats `imgRectangle1459`.
- **Name each section** clearly (Header, Hero, Our Approach, Footer, ...).

## Structure and grouping
- Use **Auto Layout / frames** for sections and components, not absolute positioning on a flat
  canvas. Auto Layout maps to how the site is built; a flat, absolutely-positioned canvas forces the
  AI to reconstruct the structure by eye. *(Eastwood was one flat 1920x8611 frame, no Auto Layout.)*
- Group the **header, footer and each section** as named frames.

## Responsive
- Provide **tablet and mobile frames**, not just desktop. If only desktop is drawn, the AI has to
  invent the responsive behaviour and you review guesses at the gate. *(Eastwood was desktop-only at
  1920, so the entire responsive layer was derived.)*
- Design the **mobile header** explicitly: as short as possible — the main bar on one row (logo, an
  icon-only CTA, the menu), and a utility bar, if used, on one row. Say what stays sticky.

## Interactive states
- Show **hover (and ideally focus) states**, or at least the hover colours, for menu items, buttons
  and links. Without them the build adds sensible defaults, but your intent is better. **Link hover
  must be distinct from the brand colour.**

## Images
- Name image layers descriptively (see Naming). **Mark placeholder images clearly** (a grey
  silhouette for a person whose photo is pending) so they are not mistaken for final.
- Provide the real images where you have them, export-ready.

## Comes with the design (from the designer or PM)
- A **definitive sitemap** (page list and menu structure), so the navigation can be built. The drawn
  nav and the sitemap must agree. *(Eastwood's sitemap arrived later and differed from the drawn header.)*
- The **build target** and any brand-font licences.

## House style
- British and Australian English in copy. No em dashes, no en dashes.
