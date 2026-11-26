# Commander portraits

Raza's compact card catalog is [atlas/index.json](atlas/index.json). Keep it beside its JPEG pages. Each record has four fields.

| Field | Meaning |
| --- | --- |
| `name` | Scryfall's card name, including both face names when present |
| `identity` | The card's colour identity, Scryfall's `color_identity`, as letters in WUBRG order (`["W","U","G"]`; `[]` for a colourless one). It counts the mana symbols in its rules text and its colour indicator as well as its cost. |
| `image` | An array of `[filename, x, y, width, height]` crops in face order. Coordinates are pixels from the top left of the named JPEG. The first entry is the primary art. |
| `avatar` | One circular crop per image, in matching face order. Each has `x`, `y`, `radius`, `width` and `height` in source pixels. |

Load the named page once and draw the indicated rectangle. For normalized texture coordinates, divide by that JPEG's actual width and height. The packer trims unused space at the right and bottom of each page.

Raza itself carries [atlas/index.bin](atlas/index.bin), the same catalog in a compact binary form (`compact_index` in [build_atlas.rain](build_atlas.rain) describes it), embedded in the program; it reads the pages from `atlas/` as it runs, as they're needed.

## Circular avatar framing

`avatar[i]` describes the circle to sample from `image[i]`. Its `x` and `y` locate the center from the top-left of the **original, unscaled art crop**; `radius` is in those same pixels. `width` and `height` are the original art dimensions. Every circle fits wholly inside its source. A double-faced card has a separate framing for each illustrated face.

To render a circular avatar, draw a disk. For each point `(u, v)` inside the unit disk (center 0, edges ±1), sample the atlas at:

```text
atlasX = tileX + (x + u * radius) * tileWidth  / width
atlasY = tileY + (y + v * radius) * tileHeight / height
```

The framing pass examined every original illustration. For recognizable faces, OpenCV's YuNet detector estimated the face bounds. The circle is centered near the chin or neck, with room for the head and shoulders. Close faces can share a circle. For illustrations without a confident face detection, U²-Net (u2netp) estimated the foreground silhouette. The framing favors a detailed area in its upper portion and uses a wider view for creatures, objects and scenery. Circular previews from a sample were visually reviewed, with hand corrections where the detector picked a prop, a secondary figure, or the wrong part of a creature.

The November 2026 pass framed 3,869 images across 3,754 cards. Visual review changed 101 of the proposed circles. Every final circle was checked against the original image dimensions.

[avatars.json](avatars.json) keeps the chosen circles keyed by the original artwork filename. To adjust a portrait, edit its entry and rebuild. Add an entry for each new art file when refreshing the catalog. Repacking at a different resolution reuses the same source-pixel framing.

## Where the source came from

The 26 November 2026 download contains 3,754 distinct cards and 3,869 JPEG art crops. The following procedure reconstructs the download using Scryfall's API. For a refresh, record the new cutoff date, query and bulk snapshot time alongside the results. Eligibility is live, so a later search can return a different list.

1. Search `https://api.scryfall.com/cards/search` with `q=game:paper legal:commander (is:commander or t:background)` and `unique=cards`. Follow each `next_page` and collect the distinct `oracle_id` values. The query includes Backgrounds that can be a second commander. API requests used the user agent `RazaCardCatalog/1.0`, accepted JSON and were spaced at least 160 ms apart.
2. Fetch the All Cards bulk descriptor from `https://api.scryfall.com/bulk-data/all-cards` and stream its gzipped JSON Lines download (`jsonl_download_uri`). The downloaded printing snapshot was dated 25 November 2026 at 22:22:43 UTC. It includes non-English printings. [Original printing snapshot](https://data.scryfall.io/all-cards/all-cards-20261125222243.jsonl.gz)
3. For each eligible Oracle ID, keep printings with `paper` in `games`, excluding oversized copies and releases after the cutoff. Pick the earliest `released_at`. For same-day ties prefer non-promo, non-variation, regular art, then English. Break remaining ties by set code, collector number and Scryfall printing ID.
4. Download the selected printing's `image_uris.art_crop` to `art/<printing-id>.jpg`. When images are supplied per face, use the faces' art crops in order and append `-1`, `-2`, etc. before the file extension. Record each printing's original card data and an `artwork` array, with `face`, `artist`, `source` and the relative `file` path for each crop, in the `cards` array of `commanders.json`.

The raw inputs belong beside this README as `commanders.json` and `art/`. Both paths are ignored by Git. The input catalog retains the original illustration credits and source URLs.

## Rebuild

The builder is a 'rain program, [build_atlas.rain](build_atlas.rain), with no other tools needed. Run this from the repository root (or from this folder, with `build_atlas.rain`).

```text
C:/rain/bin/rain.exe -release -run commanders/build_atlas.rain
```

The default build fits each illustration inside 320 × 320 pixels, preserving its aspect ratio and never enlarging it. Use `-max_edge:1024` to keep more detail, or `-output:build/commander-preview` to build a separate set (`-help` lists the options). Use one builder per output directory. The tool writes content-named pages before replacing the index, then removes obsolete pages it generated.

The packer sorts tiles by height and width and fits them into shelves on pages up to 2048 × 2048. Each crop is scaled by Image_Files' bicubic resampler and has an extruded edge for bilinear filtering. Tiles start on a 16-pixel JPEG block boundary. Pages use optimized baseline JPEG (Image_Files' `encode_jpeg`), quality 86, with 4:2:0 chroma subsampling.

On this catalog, 81 pages put 92.6% of the stored pixels inside art rectangles, and the default size-first order produced 86,590,669 JPEG bytes. Grouping equal-size tiles by average hue and brightness (`-palette_order`) saved 0.061% when measured with the earlier Python builder, on the same 81 pages. The default skips the extra image pass.
