"""Pack the local Scryfall catalog into Raza's commander portraits (Python 3 + Pillow)."""
import argparse
import colorsys
import hashlib
import json
import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image


ROOT = Path(__file__).resolve().parent
PAGE = 2048
BLOCK = 16  # JPEG 4:2:0 minimum coded unit. Keep adjacent art in separate units.


def tile_size(length):
    return (length + 2 + BLOCK - 1) // BLOCK * BLOCK


def describe(path, max_edge, palette):
    with Image.open(path) as src:
        scale = min(1, max_edge / max(src.size))
        size = tuple(max(1, round(side * scale)) for side in src.size)
        color = ()
        if palette:
            src.draft("RGB", (16, 16))
            rgb = src.convert("RGB").resize((1, 1), Image.Resampling.BOX).getpixel((0, 0))
            h, s, v = colorsys.rgb_to_hsv(*(n / 255 for n in rgb))
            color = (round(h * 12) % 12 if s > 0.12 else 12, round(v * 15), s)
    return size, color


def pack(sizes, colors):
    # Taller shelves first. Fill the existing shelf with the least height and
    # width left over, then start a shelf on the most nearly full fitting page.
    pages = []
    shelves = []
    order = sorted(sizes, key=lambda p: (-tile_size(sizes[p][1]), -tile_size(sizes[p][0]),
                                         colors[p], p))
    for path in order:
        w, h = map(tile_size, sizes[path])
        shelf = min((s for s in shelves if s[2] >= h and s[3] + w <= PAGE),
                    key=lambda s: (s[2] - h, PAGE - s[3] - w), default=None)
        if shelf is None:
            index = max((i for i, (used, _) in enumerate(pages) if used + h <= PAGE),
                        key=lambda i: pages[i][0], default=None)
            if index is None:
                index = len(pages)
                pages.append([0, []])
            shelf = [index, pages[index][0], h, 0]
            shelves.append(shelf)
            pages[index][0] += h
        index, y, _, x = shelf
        pages[index][1].append((path, x, y, w, h))
        shelf[3] += w
    return [tiles for _, tiles in pages]


def paste_tile(canvas, path, size, x, y, w, h):
    with Image.open(path) as src:
        art = src.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    aw, ah = size
    # Fill the whole padded tile with the nearest edge texels, including corners.
    strip = Image.new("RGB", (w, ah))
    strip.paste(art, (1, 0))
    strip.paste(art.crop((0, 0, 1, ah)), (0, 0))
    strip.paste(art.crop((aw - 1, 0, aw, ah)).resize((w - aw - 1, ah)), (aw + 1, 0))
    canvas.paste(strip, (x, y + 1))
    canvas.paste(strip.crop((0, 0, w, 1)), (x, y))
    canvas.paste(strip.crop((0, ah - 1, w, ah)).resize((w, h - ah - 1)), (x, y + ah + 1))


def build(output, max_edge, palette):
    raw = json.loads((ROOT / "commanders.json").read_bytes())
    cards = raw["cards"]
    if not cards or any(not card["artwork"] for card in cards):
        raise ValueError("Expected artwork for every commander")
    files = {entry["file"] for card in cards for entry in card["artwork"]}
    sizes, colors = {}, {}
    art_root = (ROOT / "art").resolve()
    for file in sorted(files):
        path = (ROOT / file).resolve()
        if not path.is_relative_to(art_root):
            raise ValueError(f"Artwork outside art/: {file}")
        sizes[file], colors[file] = describe(path, max_edge, palette)

    output.mkdir(parents=True, exist_ok=True)
    refs = {}
    pages = pack(sizes, colors)
    byte_count = pixels = 0
    with TemporaryDirectory(dir=output) as tmp:
        tmp = Path(tmp)
        for tiles in pages:
            width = max(x + w for _, x, y, w, h in tiles)
            height = max(y + h for _, x, y, w, h in tiles)
            pixels += width * height
            page = Image.new("RGB", (width, height))
            for file, x, y, w, h in tiles:
                paste_tile(page, ROOT / file, sizes[file], x, y, w, h)
            encoded = tmp / "page.jpg"
            page.save(encoded, quality=86, subsampling=2, optimize=True)
            data = encoded.read_bytes()
            byte_count += len(data)
            name = "atlas-" + hashlib.sha256(data).hexdigest()[:20] + ".jpg"
            os.replace(encoded, output / name)
            for file, x, y, w, h in tiles:
                refs[file] = [name, x + 1, y + 1, *sizes[file]]

        records = []
        for card in cards:
            cost = card.get("mana_cost")
            if cost is None:
                cost = " // ".join(f["mana_cost"] for f in card["card_faces"] if f.get("mana_cost"))
            records.append({"name": card["name"], "manacost": cost,
                            "image": [refs[a["file"]] for a in card["artwork"]]})
        manifest = tmp / "index.json"
        with manifest.open("w", encoding="utf-8", newline="\n") as f:
            f.write("[\n" + ",\n".join(json.dumps(c, ensure_ascii=False, separators=(",", ":"))
                                       for c in records) + "\n]\n")
        os.replace(manifest, output / "index.json")
    used = {ref[0] for ref in refs.values()}
    for path in output.glob("atlas-*.jpg"):
        if re.fullmatch(r"atlas-[0-9a-f]{20}\.jpg", path.name) and path.name not in used:
            path.unlink()
    occupancy = sum(w * h for w, h in sizes.values()) / pixels
    print(f"{len(cards)} cards, {len(files)} images, {len(pages)} pages, "
          f"{occupancy:.1%} art coverage, {byte_count:,} JPEG bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "atlas")
    parser.add_argument("--max-edge", type=int, default=320,
                        help="maximum portrait width or height in pixels (default 320)")
    parser.add_argument("--palette-order", action="store_true",
                        help="sort equally sized tiles by average color")
    args = parser.parse_args()
    if not 1 <= args.max_edge <= PAGE - 2:
        parser.error(f"--max-edge must be between 1 and {PAGE - 2}")
    output = args.output.resolve()
    if output == ROOT or output.is_relative_to((ROOT / "art").resolve()):
        parser.error("choose a separate atlas output directory")
    build(output, args.max_edge, args.palette_order)
