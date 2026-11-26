# Commander portraits

Raza's compact card catalog is [atlas/index.json](atlas/index.json). Keep it beside its JPEG pages. Each record has three fields.

| Field | Meaning |
| --- | --- |
| `name` | Scryfall's card name, including both face names when present |
| `manacost` | The mana cost in Scryfall notation, such as `{2}{G}{U}`. When the printing gives costs per face, nonempty costs appear in face order separated by ` // `. An empty string means the card has no mana cost. |
| `image` | An array of `[filename, x, y, width, height]` crops in face order. Coordinates are pixels from the top left of the named JPEG. The first entry is the primary art. |

Load the named page once and draw the indicated rectangle. For normalized texture coordinates, divide by that JPEG's actual width and height. The packer trims unused space at the right and bottom of each page.

## Where the source came from

The 26 November 2026 download contains 3,754 distinct cards and 3,869 JPEG art crops. The following procedure reconstructs the download using Scryfall's API. For a refresh, record the new cutoff date, query and bulk snapshot time alongside the results. Eligibility is live, so a later search can return a different list.

1. Search `https://api.scryfall.com/cards/search` with `q=game:paper legal:commander (is:commander or t:background)` and `unique=cards`. Follow each `next_page` and collect the distinct `oracle_id` values. The query includes Backgrounds that can be a second commander. API requests used the user agent `RazaCardCatalog/1.0`, accepted JSON and were spaced at least 160 ms apart.
2. Fetch the All Cards bulk descriptor from `https://api.scryfall.com/bulk-data/all-cards` and stream its gzipped JSON Lines download (`jsonl_download_uri`). The downloaded printing snapshot was dated 25 November 2026 at 22:22:43 UTC. It includes non-English printings. [Original printing snapshot](https://data.scryfall.io/all-cards/all-cards-20261125222243.jsonl.gz)
3. For each eligible Oracle ID, keep printings with `paper` in `games`, excluding oversized copies and releases after the cutoff. Pick the earliest `released_at`. For same-day ties prefer non-promo, non-variation, regular art, then English. Break remaining ties by set code, collector number and Scryfall printing ID.
4. Download the selected printing's `image_uris.art_crop` to `art/<printing-id>.jpg`. When images are supplied per face, use the faces' art crops in order and append `-1`, `-2`, etc. before the file extension. Record each printing's original card data and an `artwork` array, with `face`, `artist`, `source` and the relative `file` path for each crop, in the `cards` array of `commanders.json`.

The raw inputs belong beside this README as `commanders.json` and `art/`. Both paths are ignored by Git. The input catalog retains the original illustration credits and source URLs.

## Rebuild

With Python 3.9+ and Pillow installed, run this from the repository root.

```text
python commanders/build_atlas.py
```

The default build fits each illustration inside 320 × 320 pixels, preserving its aspect ratio and never enlarging it. Use `--max-edge 1024` to keep more detail, or `--output build/commander-preview` to build a separate set. Use one builder per output directory. The tool writes content-named pages before replacing the index, then removes obsolete pages it generated.

The packer sorts tiles by height and width and fits them into shelves on pages up to 2048 × 2048. Each crop has an extruded edge for bilinear filtering. Tiles start on a 16-pixel JPEG block boundary. Pages use optimized baseline JPEG, quality 86, with 4:2:0 chroma subsampling.

On this catalog, 81 pages put 92.6% of the stored pixels inside art rectangles. The default size-first order produced 90,021,063 JPEG bytes. Grouping equal-size tiles by average hue and brightness (`--palette-order`) produced 89,966,447 bytes on the same 81 pages, a saving of 54,616 bytes (0.061%). The default skips the extra image pass.
