# DESIGN.md Guide

## What DESIGN.md is

`DESIGN.md` is the readable record of the approved client design system. It explains the design intent, how approved variables and components should be used, and which approaches are deliberately excluded.

Figma remains the approved visual source. `DESIGN.md` must match Figma and point back to it.

## Ownership

- The Project Manager supplies the approved brief, assets, references and blank template.
- The Designer creates, verifies and maintains `DESIGN.md`.
- The Project Manager records that the file and approval evidence exist.
- The Developer confirms that the handoff is sufficiently clear to build.

## Two passes

### Pass A after visual-direction approval

Record:

- purpose and intended audience response
- approved design thesis
- observable design principles
- deliberate exclusions
- intended colour, typography, layout, imagery, shape and motion approach
- concrete do and do not guidance

Keep the status `DRAFT`. Mark details that require completed Figma work as `[PENDING AFTER FIGMA]`.

### Pass B after the client design system is complete

Verify the draft against Figma and add:

- exact approved variable names and resolved values
- typography roles and styles
- layout and responsive rules
- component purposes, variants, states and content limits
- imagery, icon and motion rules
- Figma source, collection names and verification date
- approval and change history

Remove every placeholder and pending marker before marking the file `READY`.

## Include

- concrete, observable guidance
- exact approved names and sources
- responsive and content-resilience behaviour
- design-time accessibility requirements
- do and do not examples
- known limitations and approved exceptions

## Do not include

- passwords, credentials or personal information
- a copy of the full client brief or research pack
- abandoned concepts or unapproved directions
- guessed values or renamed variables
- vague phrases such as `modern and clean` without observable rules
- claims that an automated audit certifies accessibility or design quality

## Updating the file

When an approved design decision changes:

1. Update Figma.
2. Update `DESIGN.md`.
3. Record the change and date.
4. Rerun the affected checklist and approval step.

Keep `DESIGN.md` concise enough for the Designer to review after every change.
