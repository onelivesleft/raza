# Forest components

Generated with the built-in image-generation tool on 2026-11-23, using
`materials-v1.png` as a reference. These are reconstructed cutouts matching
the forest tile, not exact segmentation masks of the original artwork.

## Prompt

Use case: background-extraction. Asset: transparent forest component sprite sheet for a game. Reference image is the existing material atlas; use ONLY the moss/leaf forest square at bottom left as style and material reference. Extract/reconstruct its richly textured natural forest-floor components as separate objects, retaining the photographic detail, muted olive/ochre greens, brown litter, moss fibres, veins and soft directional lighting. Output a square transparent PNG, precisely 2 columns by 2 rows of equal square cells, no grid lines. Top left: one generous branching fern frond. Top right: a loose sprig of broad woodland leaves. Bottom left: an irregular soft-edged patch of dense cushion moss with delicate strands. Bottom right: a small cluster of dry fallen oak leaves and thin twig. Each object entirely within its own cell with at least 8 percent transparent padding, no overlap between cells. Each fills most of its cell. Top-down camera, same scale of botanical detail as original forest. Actual transparent background between leaflets and around objects, no soil rectangle or backdrop, no labels, no text. These are natural textured cutouts, not vector icons or smooth stylised leaves.

## Packing

`forest-components-v1.png` is the original transparent 2×2 sheet: fern,
leaf sprig, moss, fallen oak leaves and twig. `materials-v2.png` preserves
every original atlas pixel in its top half and packs that sheet into the
bottom half. The renderer samples the components with their original aspect
ratio, independently places and fades each, adds contact shadows, and lights
the whole forest with drifting canopy light. Transparent alpha is retained.
