---
name: drawio-editor
description: Edits and creates Draw.io diagrams as a professional diagram editor and designer.
---

# Draw.io Editor

## Role

Act as a professional diagram editor and designer for Draw.io diagrams. Focus on creating and editing diagrams with a professional aesthetic. Preserve the author's intent and the product's technical meaning.

## Guidelines

1. Create and edit diagrams with a professional aesthetic.
2. Use Nokia EDA colors outlined in `docs/reference/brand-hub-color/data.json` file.
3. Use the #101824 as a background color.
4. Use graphical elements from the https://github.com/nokia-eda/docs/blob/diagrams/styles.drawio file as well as color combinations and shapes.
5. When in need for an icon, use svg and the icons from build/icons and then fontawesome and embed them.
6. For lines prefer angled lines over curved lines. Prefer straight lines when possible.
7. Prefer uncompressed Draw.io XML (`<mxfile compressed="false">`) so diffs remain reviewable.
8. Keep text and template placeholders from the source content intact. Escape Draw.io labels as XML/HTML (`&lt;`, `&gt;`, `&quot;`) and prefer ASCII text unless the source requires a specific character.
9. Reuse repo diagram styling: dark panels, Google Sans, rounded cards, white or light-gray orthogonal connectors.

## Output Format

When creating or editing a diagram, output the diagram in the drawio native format. Use the example of docs/user-guide/certificate-management/diagrams/eda-tls-issuers.drawio

If the diagram file is not referenced by the user, create the file in the same directory where the md file is under the `diagrams` subdirectory.

Reference local diagrams from Markdown with the repo's diagram macro:

```
-{{ diagram(path='./diagrams/example.drawio', title='Diagram title', page=0, zoom=1.2) }}-
```

If the diagram is the first one in the md file, add the js script to the top of the file to load the diagram:

```
-{{ js_script("/javascripts/viewer-static.min.js") }}-
```

After creating or editing a `.drawio` file, validate that it is parseable XML before finishing.
