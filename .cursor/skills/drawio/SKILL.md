---
name: drawio-editor
description: Edits and creates Draw.io diagrams as a professional diagram editor and designer.
---

# Draw.io Editor

## Role

Act as a professional diagram editor and designer for Draw.io diagrams. Focus on creating and editing diagrams with a professional aesthetic. Preserve the author's intent and the product's technical meaning.

## Guidelines

1. Create and edit diagrams with a professional aesthetic.
2. Use Nokia EDA colors outlined in `docs/reference/brand-hub-color/data.json` file (path relative to the root of the repository).
3. Use the #101824 as the page's background color.
4. Use graphical elements from the https://github.com/nokia-eda/docs/blob/diagrams/styles.drawio file as well as color combinations and shapes.
5. Use icons when makes sense, ask if not sure, use SVG icons from `build/icons/*.svg` first (repo-relative path from the docs root, for example `build/icons/workflow.svg`), then Font Awesome if no suitable local icon exists, and embed them in the Draw.io XML.
6. Don't use the diagram name in the drawing, instead use the title in the diagram macros.
7. When a block contains the resource name and some supporting text, make the resource name contrast or bold, while the supporting text should be less prominent.
8. For lines prefer angled lines over curved lines. Prefer straight lines when possible.
9. Prefer uncompressed Draw.io XML (`<mxfile compressed="false">`) so diffs remain reviewable.
10. Keep text and template placeholders from the source content intact. Escape Draw.io labels as XML/HTML (`&lt;`, `&gt;`, `&quot;`) and prefer ASCII text unless the source requires a specific character.
11. Reuse repo diagram styling: dark panels, Google Sans, rounded cards, white or light-gray orthogonal connectors.
12. Use font size 14 at the minimum, unless the resulting diagram is too small to read.
13. When adding pages to the diagram, use [X] <name> as the page name, where X is the page number. Always add pages in the last position, so that the diagrams name containing the page number for previous diagrams is not changed. Page count starts with 0.
14. When creating blocks (shapes) try to use the same size and shape to keep the diagram consistent. When the text doesn't fit, make the block wider/higher, but then try to make sure it is not the only block with that size/shape.
15. When you are asked to create a flow diagram, use different colors for blocks on different levels of the flow. Use the colors from the Nokia EDA brand hub color palette.
16. Make sure lines are aligned with the blocks they connect to and are aligned between themselves when on the same horizontal or vertical line.
17. When certain blocks are grouped, group them with the underlying block of the faint background color.

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
