# Raza material atlas

`materials-v1.png` is original artwork generated for this project with the
built-in image-generation tool on 2026-11-23. No card scans or game assets
were used as inputs. The exact generation prompt is in `PROMPT.md`.

The image has four columns and two rows, without gutters. In row order:

| Tile | Material | Use |
| --- | --- | --- |
| 0 | Ivory vellum/mineral paper | White panel detail |
| 1 | Azure ripples and caustics | Blue panels, water bodies and attacks |
| 2 | Dark obsidian | Black panel detail |
| 3 | Red fractured basalt | Red panel detail |
| 4 | Moss, fallen leaves and soil | Green panels |
| 5 | Brushed iron and rust | Colourless panels |
| 6 | Antique gold mineral grain | Multicolour panels; identity tint retained |
| 7 | Neutral smoke filaments | Animated fire and wind density |

`materials.rain` samples within each cell with an inset, avoiding colour bleed
from adjacent cells. Four overlapping sampling windows keep values continuous at tile joins
without reflecting recognisable leaves;
the artwork is not assumed to have mathematically seamless edges. The atlas
is embedded with `#data`, uploaded once at startup and released on exit.

Solid materials stay fixed in the player's coordinate frame. Water drifts;
fire and wind combine two moving scales of the neutral tile. Shaders retain
the silhouettes, lighting, stirring, attack timing and fading. Later eras
use finer detail and a quieter texture contribution.

Rain's Draw module now exposes `draw_shader_image`: the same quad and typed
uniform block as `draw_shader`, plus typed texture/sampler bindings and one
bilinearly filtered image. Vulkan and OpenGL support it. Its GPU readback tests
alternate textures and uniforms with an ordinary draw between them.

## Layered forest atlas

materials-v2.png retains the original atlas pixels in its top half and adds the transparent forest-components-v1.png sheet below. The four reconstructed components (fern, leaf sprig, moss and fallen litter) are placed, rotated, shaded and faded independently. See FOREST-PROMPT.md for the built-in generation prompt and packing layout. The shader uses the packed atlas for every material, including hybrid panels.

The layered cutout atlas is retained as an unused art reference. The current forest uses the original forest-floor tile in materials-v1.png as an opaque base plus three offset copies with independently changing, detail-weighted opacity masks and moving illumination. Separate cutouts and procedural plant silhouettes are no longer rendered.