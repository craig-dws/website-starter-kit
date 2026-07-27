# Design-for-build checklist (for the designer)

How to set up a Figma design so the AI build gets it right the first time. Every item is here
because something in a real build was harder than it needed to be, the fix is "do it in the design."
This is a living checklist, add to it as we learn more.

## What the build works out itself, so we do not ask you
You know the design; the build knows what a WordPress/Breakdance build needs. So the build sets
sensible defaults for the things below, grounded in your tokens and standard practice, and only
asks you for genuine design judgement. Supply any of these if you have an opinion; if not, the build
fills them and you review the result at the gate.

- **A standard contact form** — built with the site's form plugin (Gravity Forms), styled to the
  tokens. Only an unusual form (multi-step, conditional, calculated) needs a drawn spec.
- **Focus states** — a visible focus indicator on every interactive element, derived from the brand
  and hover tokens, to meet WCAG 2.2 AA. Draw them only if you want a specific treatment.
- **A spacing scale** — derived from the section paddings and gaps already in the design.
- **Inline link states** — rest and hover from the tokens (hover kept distinct from the brand) plus
  a focus state, unless you specify them.
- **Dark surface colours** — derived from the dark sections in the design if not named as swatches.
- **Responsive collapse** — where tablet and mobile frames are not supplied, standard collapse
  patterns per breakpoint, reviewed on the rendered pages. Supplying the frames is still better,
  this is the fallback.
- **Card, panel and icon defaults** — from the patterns already in the design.

What still genuinely needs you: the **design tokens/variables**, the **fonts**, the **page-type
reference designs**, **unique frame names and clear structure**, and anything where the look is a
real brand decision rather than a mechanical default. That is judgement the build should not make.

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

## A style guide, and what a complete one contains
- **Supply a style guide frame.** It is the single most useful thing after the tokens themselves,
  because it states each value's **role** ("eyebrow text for dark background"), which a page
  drawing never does. Without one, every token is inferred from pixels.
  *(Eastwood's arrived after the home page was built. It certified the type scale, eight colours
  and both button gradients, all of which matched, and it settled two questions that had been open
  since the first day.)*
- A complete style guide covers: the **type scale with line heights**; **every colour with its
  role**, including the **dark surfaces**, which are the ones most often left out; **buttons in
  default, hover and focus** on each surface they appear on; **inline link states**, rest, hover,
  visited, focus; **cards and panels** (radius, border on light and on dark, padding, hover);
  a **spacing scale**; **form fields** (label, input, select, textarea, required, error, success);
  and **icon rules** (stroke weight, sizes, colour on light versus dark).
  *(Eastwood's style guide had type, eight colours and buttons. Everything else in that list is
  still derived, and forms are the biggest single thing being invented from scratch.)*
- **Hover states are the highest-value thing in it.** They cannot be inferred from a static page
  drawing at all, so without them the build authors its own and you are approving guesses.
  *(Eastwood: the build's outline-button hover was a soft white wash; the style guide, when it
  arrived, showed an inversion, the button filling with its own border colour. Materially
  different, and only caught because the two were diffed.)*
- **A style guide does not replace tablet and mobile frames.** It says what things look like, not
  how they reflow. *(Eastwood's was desktop only, and drawn at 1366 while the page frames were
  1920, so it contributed nothing to the responsive layer.)*
- **Keep the style guide internally consistent, and consistent with the page frames.** If it
  contradicts itself the build has to pick, and it will pick without you.
  *(Eastwood: the style guide specified Source Sans 3 but drew its own button labels in Segoe UI,
  and gave the light button's label colour as #092E46 in one place and #173445 in another.)*

## Fonts
- Use **webfonts** (Google Fonts or a licensed webfont), **not system fonts.** Segoe UI, for
  example, is a Windows-only system font that does not load on the web and silently falls back.
  Name the intended brand font; if it is not a webfont, say what the web substitute should be.
- **The style guide and the page frames must name the same fonts.** If they disagree the build
  cannot tell which is intent and which is an accident.
  *(Eastwood: the home frame was set in Segoe UI, the style guide specified Source Sans 3. The
  build substituted Source Sans 3 on licensing grounds and only found out days later that this was
  the designer's specification all along, so a decision was taken twice for no reason.)*

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
- **Say which handoff mode this is:** a design for every page, or a few reference designs plus a
  style guide. They produce different builds and the answer must be recorded before internal pages
  start. If it is reference designs, supply **one frame per page type**, not one frame in total.
  *(Eastwood is ~30 pages: one internal content page, one condition, one treatment, one surgeon
  biography and one contact page covers all of them. The mode went unrecorded until 2026-07-27.)*

## House style
- British and Australian English in copy. No em dashes, no en dashes.
