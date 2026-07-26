---
name: anti-ai-design-checklist
description: Five constraints that prevent the generic AI look in website designs by making designs deviate intentionally from AI statistical defaults. Use for design quality reviews, the creative-quality gate, client feedback sessions, design system audits, and pre-production design approval. Target neutral, so it applies whether the build target is WordPress plus Breakdance or Astro plus Payload. Checks are expressed against token names and the rendered design, not against any single stack.
---

# Anti-AI Design Checklist

## Overview

**Purpose:** Define five constraints that prevent the generic AI look in website designs through intentional deviation from AI statistical defaults.

**When to use:** Design quality reviews, the creative-quality gate, client feedback sessions, design system audits, pre-production design approval.

This skill is complementary to the web-design skill, not a duplicate of it. The web-design skill drives the build of a page against tokens; this skill supplies the creative-quality bar that the design and its tokens must clear. The web-design skill references this checklist at its quality gate. Keep the two in sync rather than restating one inside the other.

**Target neutral.** These are design principles, not stack rules. A constraint is checked against the design's token names and the rendered result. It does not matter whether the tokens are later applied through Breakdance controls, through a component library, or through a code-owned theme. Never phrase a check as a search for a vendor-specific class or config value.

---

## The problem: AI aesthetic homogenisation

### Why AI designs look generic

**Visual red flags:**
- Default colour schemes: a stock primary blue, a stock neutral grey, chosen because they are statistically common rather than because a token defines them
- Generic typography: default system or web-safe faces at standard weights, with no considered type scale
- Uniform spacing: one padding value repeated everywhere with no rhythm
- Centred layouts: hero sections always centred, symmetric column grids
- Rounded corners everywhere: a single default radius applied without intent
- Stock imagery: smiling diverse teams, generic office spaces, abstract geometric backgrounds

**Process red flags:**
- Skipping the design concept phase and going brief straight to build
- Single-pass design with no iteration or refinement
- No creative metaphor or visual anchor
- Treating constraints as filters (do not use X) instead of creative catalysts

**Root cause:** AI models optimise for the most likely visual patterns in their training data. Most likely equals statistical average equals generic, homogeneous output.

---

## The solution: constraint as creativity

**Core principle:** Non-generic design emerges from intentional constraints that counteract AI statistical defaults. Each constraint forces creative problem solving that prevents convergence to generic patterns.

For every constraint below, the definition of right is a token. If a spacing, colour or type decision cannot be named as a token, there is nothing for an agent or a reviewer to check it against. Check the constraint two ways: read the token specification (are the intended values defined and named), and inspect the rendered design (does the eye see the intended effect).

---

## Constraint 1: spatial rhythm, not uniform padding

### The AI default trap

One spacing value repeated for every section, every gap and every gutter. Even spacing between all elements produces a predictable, flat visual flow.

### The anti-AI constraint

**Requirement:** Vary spacing intentionally to create visual rhythm and guide the eye.

**Design principle:** Rhythm creates interest, emphasis and hierarchy through spacing contrast.

**Key techniques:**
- Vary vertical spacing by section importance: a hero breathes more than a footer
- Progressive gaps as the viewport widens, rather than one fixed gap at every breakpoint
- Asymmetric padding: more room on one side of a column than the other to create tension
- Whitespace clustering: group related content tightly, then leave a large gap at a section break

**How to check:**
- Read the spacing scale in the token specification. There should be a graded set of named spacing tokens, not a single value used everywhere.
- Confirm the design applies at least three different spacing tokens within a single section.
- Confirm the spacing progression follows an intentional rhythm rather than looking random.
- Inspect the rendered design: the spacing should read as deliberate pacing, with clear grouping and clear breaks.

**Pass criteria:**
- At least three distinct spacing tokens used within a single section
- Spacing progression follows an intentional rhythm
- Some asymmetric spacing is applied to create visual interest

---

## Constraint 2: intentional asymmetry, not centred symmetry

### The AI default trap

Hero sections with centred text and a centred call to action. Two column layouts always split fifty fifty. Everything justified to the centre, producing perfect left to right symmetry that feels static.

### The anti-AI constraint

**Requirement:** Place key elements off centre, or use unbalanced layouts, to create energy.

**Design principle:** Asymmetry reads as visual energy, modernity and intent. Perfect symmetry reads as static and predictable.

**Key techniques:**
- Sixty forty or seventy thirty splits rather than fifty fifty
- Offset content that starts a column or two in from the grid edge, not always at the first column
- Left aligned calls to action rather than centred
- Staggered vertical alignment: alternate the content and image sides from section to section
- Deliberate overlap or layering to break a rigid grid

**How to check:**
- Inspect the rendered hero: it should not default to centred text with a centred button.
- Confirm at least one primary split is sixty forty or seventy thirty, not fifty fifty.
- Confirm the key call to action is positioned with intent rather than dropped in the centre.

**Pass criteria:**
- Hero section is not centred (left aligned or offset layout)
- At least one sixty forty or seventy thirty split is present
- The key call to action is positioned intentionally off centre

**Manual review required:** Human judgement is needed to tell intentional asymmetry from accidental imbalance.

---

## Constraint 3: unexpected hierarchy, not conventional order

### The AI default trap

Headings always descend in size from first to last. Primary content always sits above secondary. The call to action is always the largest, boldest element. The information order never varies from logo, navigation, hero, features, call to action, footer.

### The anti-AI constraint

**Requirement:** Subvert at least one conventional hierarchy expectation to challenge the viewer's assumptions.

**Design principle:** Unexpected hierarchy creates memorable moments and guides attention in non-linear ways.

**Key techniques:**
- Invert the visual weight: a small eyebrow label above a very large statement line, where the statement is the true anchor
- De-emphasise the call to action: a small, understated control instead of a bold button, with prominence coming from position and colour
- Let a large body statement act as the hero element, with a small heading above it
- Establish prominence through colour and position, not only through type size

**How to check:**
- Confirm the type scale tokens allow this: there should be enough named steps to invert weight deliberately.
- Confirm at least one section inverts the conventional hierarchy on purpose.
- Confirm the semantic document structure remains correct even where the visual order differs. Visual inversion must never break the heading order that assistive technology relies on. Accessibility is certified by a human.

**Pass criteria:**
- At least one deliberate hierarchy inversion is present
- The inversion serves an intentional creative concept, not randomness
- Semantic structure and heading order remain correct for accessibility

**Manual review required:** Design judgement is needed to evaluate intent and brand alignment.

---

## Constraint 4: colour nuance, not default primary and secondary

### The AI default trap

A stock primary blue and a stock neutral grey, chosen because they are the statistically common defaults rather than because the brand calls for them. High saturation mid-scale colours. Predictable pairings such as blue with white or blue with grey. The give-away is a palette that no token names and that could belong to any site.

### The anti-AI constraint

**Requirement:** Use brand-specific colour values, defined and named as tokens, traceable to the brand or to the grounded metaphor.

**Design principle:** Colour distinctiveness drives brand recognition. Default palettes are invisible branding.

**Key techniques:**
- Name colours by role and brand, such as primary, accent or a descriptive brand name, so the token carries meaning
- Use nuanced neutrals with a slight temperature, warm or cool, rather than a flat default grey
- Favour lower saturation for large surfaces and reserve stronger colour for accents
- Choose less obvious pairings, for example a warm accent against a cool neutral
- Consider multi-stop gradients where a single flat fill would read as generic

**How to check:**
- Read the colour tokens in the specification. Every colour used in the design must resolve to a named token.
- Confirm the palette is not the stock default primary and neutral. There should be at least two brand-specific colour tokens defined.
- Trace each brand colour back to the brand guidelines or the grounded metaphor. A colour with no rationale is a red flag.
- Inspect the rendered design: the palette should feel specific to this brand, not interchangeable with any competitor.

**Pass criteria:**
- No reliance on the stock default primary blue or default neutral grey
- At least two brand-specific colour tokens are defined and named
- The palette is traceable to brand guidelines or to the grounded metaphor

---

## Constraint 5: constraint-driven creativity

### The AI default trap

Constraints treated as filters. A do not use X instruction produces a subtractive design, a template with the forbidden element removed and nothing added in its place. There is no evidence of creative problem solving and the constraint never becomes part of the concept.

### The anti-AI constraint

**Requirement:** Show evidence of working within an intentional constraint to solve a creative challenge, so the constraint adds conceptual value rather than merely removing something.

**Design principle:** Constraints are catalysts for innovation. The best designs turn a limitation into a strength.

**Worked example:**

Constraint: evoke trust and collaboration without using photographs of people.

Weak response: fall back on generic abstract shapes. Forgettable and template-like.

Strong response: reframe the constraint as the seed of a metaphor. Represent collaboration through an abstract connected-node motif, where nodes stand for people and the connections stand for coordination. The constraint now drives a distinctive visual system rather than leaving a gap. The colours and motion of that motif are all defined as tokens, so the treatment is checkable and reusable.

**How to check:**
- Confirm at least one major constraint is identified and written down, with its source, for example the project constitution or the brand guidelines.
- Confirm the creative solution adds conceptual value rather than only removing a forbidden element.
- Confirm the solution is integrated into the grounded metaphor and expressed through tokens.
- Confirm the reasoning is recorded in the design artefacts.

**Pass criteria:**
- At least one major constraint is identified and documented
- The creative solution adds conceptual value, it does not just subtract
- The solution is integrated into the grounded metaphor
- The design documentation shows intentional, constraint-driven reasoning

**Manual review required:** Human judgement is needed to decide whether the constraint truly acted as a catalyst.

**Evidence checklist:**

```markdown
Constraint identified: [state the constraint]
- Source: [project constitution, brand guidelines, compliance document]

Creative puzzle defined: [reframe the constraint as a challenge]
- Example: how to evoke trust without showing people

Creative solution implemented: [describe the novel approach]

Integration with metaphor: [show the connection to the grounded metaphor]

Result: [impact on design uniqueness]
```

---

## Complete quality checklist

Use this checklist at the creative-quality gate.

### Pre-flight checks (before implementation)

- [ ] **Grounded metaphor exists:** the design has a clear creative metaphor traceable to brand documents
- [ ] **Keywords cited:** the metaphor derives from five to seven source keywords with citations
- [ ] **Metaphor grounding verified:** traceability of metaphor elements to source keywords is confirmed

### The five anti-AI constraints

- [ ] **Constraint 1, spatial rhythm**
  - [ ] At least three distinct spacing tokens within a single section
  - [ ] Spacing follows an intentional rhythm, not a uniform value
  - [ ] Some asymmetric spacing is applied
- [ ] **Constraint 2, intentional asymmetry**
  - [ ] Hero section is not centred
  - [ ] At least one sixty forty or seventy thirty split
  - [ ] Key call to action positioned off centre
- [ ] **Constraint 3, unexpected hierarchy**
  - [ ] At least one deliberate hierarchy inversion
  - [ ] Serves an intentional creative concept
  - [ ] Semantic structure and heading order remain correct
- [ ] **Constraint 4, colour nuance**
  - [ ] No reliance on the stock default primary or neutral
  - [ ] At least two brand-specific colour tokens defined
  - [ ] Colours traceable to brand or metaphor
- [ ] **Constraint 5, constraint-driven creativity**
  - [ ] Major constraint identified and documented
  - [ ] Creative solution adds conceptual value
  - [ ] Integrated into the grounded metaphor
  - [ ] Reasoning documented in the design artefacts

### Post-implementation checks

- [ ] **Mood board integration:** visual references from research are incorporated
- [ ] **Token traceability:** every colour, type and spacing decision resolves to a named token
- [ ] **Semantic structure:** correct heading order and accessible markup
- [ ] **Accessibility:** WCAG 2.2 AA contrast verified by a human
- [ ] **No generic stock:** no generic stock photos of smiling teams or abstract backgrounds

### Pass threshold

- All five anti-AI constraints: five of five must pass
- Pre-flight checks: three of three must pass
- Post-implementation: at least four of five must pass

If fewer than twelve of the thirteen total checks pass, return to the design refinement phase.

---

## Integration with other skills

**Prerequisites:**
- `grounded-metaphor-generation`: the metaphor must exist before these constraints can be applied
- `agentic-rag-methodology`: constraints are extracted from source documents by targeted retrieval

**Complementary:**
- The web-design skill: references this checklist at its creative-quality gate rather than restating it

**Workflow:**
```
Grounded metaphor generated ->
Anti-AI design checklist applied (this skill) ->
Design validated at the creative-quality gate ->
Handed to the web-design skill for the build
```
