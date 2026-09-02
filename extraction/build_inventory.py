#!/usr/bin/env python3
"""build_inventory.py -- asset inventory CSV for the Unity template (Task 3).

Walks Assets/BulletHellTemplate/Res/ and ThirdPartyResources/ (excluding
ThirdPartyResources/Tools/ -- vendored code, off-limits; os.walk prunes it
without enumerating) and writes extraction/asset-inventory.csv.

poly_count is derived only for ASCII FBX files (count of negative indices in
PolygonVertexIndex blocks = polygon count); binary FBX -> n/a.
"""
from __future__ import annotations

import csv
import os
import re
from pathlib import Path

UNITY_PROJECT = Path(r"C:/roguelike roblox/My project")
BHT = UNITY_PROJECT / "Assets" / "BulletHellTemplate"
OUT_CSV = Path(r"C:/roguelike roblox/bullet-heaven/extraction/asset-inventory.csv")

TYPE_BY_EXT = {
    ".fbx": "mesh", ".obj": "mesh", ".gltf": "mesh", ".glb": "mesh",
    ".png": "texture", ".tga": "texture", ".psd": "texture",
    ".jpg": "texture", ".jpeg": "texture",
    ".wav": "audio", ".mp3": "audio", ".ogg": "audio",
    ".anim": "animation", ".controller": "animation",
    ".ttf": "font", ".otf": "font",
}

FBX_BINARY_MAGIC = b"Kaydara FBX Binary"
PVI_BLOCK = re.compile(r"PolygonVertexIndex:\s*\*\d+\s*\{(.*?)\}", re.S)
NEG_INT = re.compile(r"-\d+")


def fbx_poly_count(path: Path):
    """Polygon count for ASCII FBX; 'n/a' for binary or unreadable."""
    try:
        with path.open("rb") as fh:
            head = fh.read(64)
        if head.startswith(FBX_BINARY_MAGIC):
            return "n/a"
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "n/a"
    blocks = PVI_BLOCK.findall(text)
    if not blocks:
        return "n/a"
    return sum(len(NEG_INT.findall(b)) for b in blocks)


def notes_for(rel_posix: str, ext: str) -> str:
    low = rel_posix.lower()
    notes = []
    if "/new ui/" in low or "/oldui/" in low or "/uielements/" in low or low.startswith("res/ui/"):
        notes.append("ui")
    if ("/fx/" in low or "/effects/" in low or "/particle" in low) and ext in (
        ".png", ".tga", ".psd", ".jpg", ".jpeg",
    ):
        notes.append("vfx-texture")
    if "dungeon" in low:
        notes.append("dungeon-kit")
    if ("kaykit" in low or "/characters/" in low or "/monsters/" in low) and ext == ".fbx":
        notes.append("kaykit-candidate")
    return ";".join(notes)


def iter_files(root: Path, prune: str | None = None):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        if prune and Path(dirpath) == root and prune in dirnames:
            dirnames.remove(prune)  # never enumerate the off-limits subdir
        for fn in sorted(filenames):
            if fn.endswith(".meta"):
                continue
            yield Path(dirpath) / fn


def main():
    rows = []
    for root, prune in ((BHT / "Res", None), (BHT / "ThirdPartyResources", "Tools")):
        for p in iter_files(root, prune):
            rel = p.relative_to(BHT).as_posix()
            ext = p.suffix.lower()
            ftype = TYPE_BY_EXT.get(ext, "other")
            fmt = ext.lstrip(".")
            size = p.stat().st_size
            poly = fbx_poly_count(p) if ext == ".fbx" else "n/a"
            rows.append((rel, ftype, fmt, size, poly, notes_for(rel, ext)))

    rows.sort(key=lambda r: r[0])
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)  # QUOTE_MINIMAL: quotes fields containing commas
        w.writerow(["path", "type", "format", "size_bytes", "poly_count", "notes"])
        w.writerows(rows)

    from collections import Counter

    by_type = Counter(r[1] for r in rows)
    print(f"total rows: {len(rows)}")
    for t, n in sorted(by_type.items()):
        print(f"  {t}: {n}")
    polys = [(r[0], r[4]) for r in rows if r[4] != "n/a"]
    print(f"poly_count derivable: {len(polys)}")
    for name, pc in polys:
        print(f"  {name}: {pc}")


if __name__ == "__main__":
    main()
