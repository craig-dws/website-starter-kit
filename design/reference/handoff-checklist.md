# Design Handoff Checklist

Project: [CLIENT]

Figma file: [LINK]

Designer: [NAME]

Date: [YYYY-MM-DD]

## Approved screens

- [ ] All required pages are present
- [ ] Desktop, tablet and mobile frames are present for key templates
- [ ] Every handoff frame is marked `Dev Ready`
- [ ] Client approval status is recorded

## Variables and components

- [ ] Approved variables are applied throughout
- [ ] No unexplained hardcoded or off-scale values remain
- [ ] Repeated elements use approved components
- [ ] Variants and states are complete
- [ ] Reusable and page-specific elements are identified
- [ ] No unexplained detached instances remain

## Responsive behaviour

- [ ] Breakpoints or target widths are recorded
- [ ] Column, order, scale and visibility changes are annotated
- [ ] Auto Layout and resizing behaviour are intentional
- [ ] Layouts can be expressed using normal flex or grid behaviour

## Interaction and accessibility

- [ ] Hover, focus, active and disabled states are defined where relevant
- [ ] Form states include empty, filled, focused, error, success and disabled where relevant
- [ ] Contrast evidence is recorded
- [ ] Labels and accessible-name intent are recorded
- [ ] Focus order or focus intent is clear
- [ ] Motion and reduced-motion behaviour are documented

## Content and assets

- [ ] Approved content is used or placeholder status is clearly marked
- [ ] Long-content and missing-content behaviour is documented
- [ ] Image crop, fit, ratio and fallback behaviour are documented
- [ ] Required logos, icons and images are supplied
- [ ] Export format and naming are clear

## Design pack (so the build needs no Figma seat)

- [ ] Mesh gradients and other editor-only fills are identified and flagged
- [ ] Each one is exported by hand as a PNG into `design-pack/assets/manual/`
- [ ] `prompts/export-design-pack.md` has been run against the final design
- [ ] `design-pack/MANIFEST.md` shows no gaps against the sitemap
- [ ] The pack is committed and pushed

## Documentation

- [ ] `DESIGN.md` is READY and matches Figma
- [ ] Component usage notes are present
- [ ] Open questions have an owner and due date
- [ ] Approved exceptions are recorded
- [ ] DiscoverWeb handoff audit passes

## Designer handoff

- [ ] READY FOR HANDOFF
- [ ] NOT READY

Blocking issues: [NONE OR LIST]

Designer confirmation: [NAME AND DATE]

Developer acceptance: [NAME AND DATE OR PENDING]

If the receiving Developer rejects the handoff, record the reason, fix the issue and rerun the checklist.
