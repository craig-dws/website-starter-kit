# Alt text guidelines

How to write image alt text on a build. Alt text is a **WCAG 2.2 AA Level A** requirement
(missing or inadequate alt text is the most common failing cited in accessibility lawsuits)
and it also helps SEO. Write it well; do not put generic filler on everything.

## The test
For each image ask: **"what information would someone who cannot see this image miss?"**
That answer, in one or two clear phrases, is the alt text.

## Rules
- **Describe content and purpose.** Say what the image shows and why it is on the page, not a
  bare label. "Ophthalmologist performing a slit-lamp eye examination", not "eye".
- **Be specific, not generic.** Name what is depicted. For people, name them and their role
  where known: "Dr Gagan Khannah, cataract and refractive surgeon".
- **Concise.** Aim for ~125 characters, keep under ~200. Screen readers lose the listener past
  that. One or two phrases.
- **No "image of" / "photo of".** Screen readers already announce it is an image.
- **Decorative images get empty alt** (`alt=""`), never a missing alt attribute. An icon next
  to a heading that already names it (a cataracts icon beside a "Cataracts" heading) is
  decorative: empty alt, so it is not announced twice.
- **Functional images** (a linked logo, an icon button) describe the action or destination,
  not the picture: "Eastwood Eye Surgery home", not "logo".
- **Keywords only where natural and accurate.** Never keyword-stuff; it fails accessibility and
  Google discounts it.
- **Do not duplicate adjacent text.** If a caption already says it, the alt adds something or is
  empty.
- **Images of text**: put the actual text in the alt, or better, do not use images of text.

## Common cases on this kind of build
- **Team / staff photos**: "Dr [Name], [specialty] at [practice]".
- **Hero and section photos**: describe the scene and its relevance to the page.
- **Condition / treatment / feature icons next to a labelled heading**: decorative, empty alt.
- **Brand logo in the header** (usually links home): "[Practice] home".

## Where alt goes
Set it in **two** places, from the same source of truth (the design and content):
- the **media library** attachment (`--alt` on the upload script, or `--update <id> --alt`), and
- the **rendered image element** in the layout (the `alt` attribute in the html-to-page markup).
