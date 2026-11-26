# Raza material atlas

`materials-v1.png` is original artwork generated for this project with the
built-in image-generation tool on 2026-11-23. No card scans or game assets
were used as inputs. The exact generation prompt is in `PROMPT.md`.

The image has four columns and two rows, without gutters. In row order:

| Tile | Material | Use |
| --- | --- | --- |
| 0 | Ivory vellum/mineral paper | White panel detail |
| 1 | Azure ripples and caustics | Not sampled (blue is procedural) |
| 2 | Dark obsidian | Black panel detail |
| 3 | Red fractured basalt | Red panel detail |
| 4 | Moss, fallen leaves and soil | Green panels |
| 5 | Brushed iron and rust | Colourless panels |
| 6 | Antique gold mineral grain | Multicolour panels; identity tint retained |
| 7 | Forest floor height & leaf gloss | Pixel-registered height (`.x`) and leaf-only gloss mask (`.y`) for green panels (`TILE_FOREST_BUMP`) |

`src/materials.rain` samples within each cell with an inset, avoiding colour bleed
from adjacent cells. Four overlapping sampling windows keep values continuous at tile joins
without reflecting recognisable leaves;
the artwork is not assumed to have mathematically seamless edges. The atlas
is embedded with `#data`, uploaded once at startup and released on exit.

Solid materials stay fixed in the player's coordinate frame. Blue's panels
are procedural and don't sample tile 1. Tile 7 carries a greyscale heightmap
generated directly from tile 4 so every leaf, clover cluster, moss cushion and
soil crevice aligns pixel-for-pixel across `layered_forest`'s base and overlay
layers when lit from above.

Rain's Draw module now exposes `draw_shader_image`: the same quad and typed
uniform block as `draw_shader`, plus typed texture/sampler bindings and one
bilinearly filtered image. Vulkan and OpenGL support it. Its GPU readback tests
alternate textures and uniforms with an ordinary draw between them.

## The forest

The forest uses the forest-floor tile in materials-v1.png as an opaque base
plus three offset copies with independently changing, detail-weighted
opacity masks and moving illumination (`layered_forest`). An earlier
experiment with a separate sheet of forest cutouts (materials-v2.png,
forest-components-v1.png) is no longer rendered; those files were removed
and remain in the repository's history.