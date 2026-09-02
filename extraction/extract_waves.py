#!/usr/bin/env python3
"""extract_waves.py -- extract GameplayManager wave config from scene files.

Reads (read-only) Res/Scenes/MapArena1-4.unity + PVPArena2/PVPArenaBR.unity,
finds the GameplayManager MonoBehaviour (script GUID b406b3ed...), and dumps
its data fields to extraction/gamedata-json/waves/maparena<N>.json.

Same rules as extract_gamedata.py: boilerplate strip, GUID refs resolved via
guid-map.json, description* flavor-text keys stripped, pure JSON output.
Raw scene YAML is never written out -- only the transformed data.

xpToNextLevel is a hex-encoded little-endian uint32 array (Unity int[]
serialization); it is decoded to an int list, raw kept under
xpToNextLevel_raw, with an explanation in _formatNotes.
"""
from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path

from extract_gamedata import (
    BHT,
    OUT,
    parse_unity_yaml,
    script_type_of,
    transform,
    unwrap_root,
    write_json,
)

JSON_OUT = OUT / "gamedata-json"
GUID_MAP_PATH = OUT / "guid-map.json"
SCENES = BHT / "Res" / "Scenes"

GAMEPLAY_MANAGER_GUID = "b406b3ed4ff83f348a9560da9f8ec080"
WAVEY_FIELD = re.compile(r"wave|spawn|boss|monster", re.I)

SCENE_FILES = [
    "MapArena1.unity",
    "MapArena2.unity",
    "MapArena3.unity",
    "MapArena4.unity",
    "PVPArena2.unity",
    "PVPArenaBR.unity",
]


def decode_hex_u32(hex_str: str):
    """Decode hex string as little-endian uint32 array; None if malformed."""
    try:
        raw = bytes.fromhex(hex_str)
    except ValueError:
        return None
    if not raw or len(raw) % 4:
        return None
    return list(struct.unpack(f"<{len(raw) // 4}I", raw))


def main():
    guid_map = json.loads(GUID_MAP_PATH.read_text(encoding="utf-8"))
    stripped_log = {}
    written = []
    failures = []
    report = []

    for scene_name in SCENE_FILES:
        scene = SCENES / scene_name
        map_key = scene_name[: -len(".unity")].lower()
        rel_scene = scene.relative_to(BHT).as_posix()
        try:
            docs = parse_unity_yaml(scene)
        except Exception as exc:  # noqa: BLE001
            failures.append((rel_scene, str(exc)))
            continue

        gm_docs = []
        additional = []
        for d in docs:
            if d["class_id"] != 114 or d["stripped"]:
                continue
            data = unwrap_root(d["data"])
            if not isinstance(data, dict):
                continue
            script_ref = data.get("m_Script") or {}
            sguid = script_ref.get("guid")
            if sguid == GAMEPLAY_MANAGER_GUID:
                gm_docs.append(data)
            else:
                fields = [k for k in data if not str(k).startswith("m_")]
                if any(WAVEY_FIELD.search(str(f)) for f in fields):
                    additional.append(data)

        if not gm_docs:
            report.append((map_key, "NO GameplayManager found"))
            continue
        if len(gm_docs) > 1:
            report.append((map_key, f"WARN: {len(gm_docs)} GameplayManager docs, using first"))

        log_key = f"waves/{map_key}.json"
        stripped = []
        gm = transform(gm_docs[0], guid_map, stripped)
        gm["_scriptType"] = script_type_of(gm, guid_map)
        gm["_sourceScene"] = rel_scene

        # Decode xpToNextLevel hex blob (Unity int[] as LE uint32 hex).
        xp = gm.get("xpToNextLevel")
        if isinstance(xp, str):
            decoded = decode_hex_u32(xp)
            if decoded is not None:
                gm["xpToNextLevel_raw"] = xp
                gm["xpToNextLevel"] = decoded
                gm.setdefault("_formatNotes", {})["xpToNextLevel"] = (
                    "Unity int[] serialized as hex little-endian uint32; "
                    "decoded to int list, raw hex kept in xpToNextLevel_raw"
                )
            else:
                gm.setdefault("_formatNotes", {})["xpToNextLevel"] = (
                    "raw Unity hex blob; not decodable as LE uint32 array"
                )

        if additional:
            comps = []
            for data in additional:
                t = transform(data, guid_map, stripped)
                t["_scriptType"] = script_type_of(t, guid_map)
                comps.append(t)
            gm["_additionalComponents"] = comps

        if stripped:
            stripped_log[log_key] = stripped

        waves = gm.get("waves") or []
        if not waves:
            # Empty-wave scene (PVP): no output file, just report.
            report.append(
                (map_key, f"empty waves (survivalTime={gm.get('survivalTime')}); skipped")
            )
            continue

        out_path = JSON_OUT / "waves" / f"{map_key}.json"
        write_json(out_path, gm)
        written.append(out_path)
        report.append(
            (
                map_key,
                f"waves={len(waves)} survivalTime={gm.get('survivalTime')} "
                f"maxLevel={gm.get('maxLevel')} additional={len(additional)}",
            )
        )

    # Update the shared stripped-keys log (merge, keyed by output path).
    log_path = OUT / "stripped-keys-log.json"
    if stripped_log:
        existing = {}
        if log_path.exists():
            existing = json.loads(log_path.read_text(encoding="utf-8"))
        existing.update(stripped_log)
        write_json(log_path, existing)

    for k, msg in report:
        print(f"{k}: {msg}")
    print(f"\nwritten: {len(written)}")
    for w in written:
        print(f"  {w.relative_to(JSON_OUT).as_posix()}")
    print(f"stripped-key files: {sorted(stripped_log)}")
    print(f"parse failures: {len(failures)}")
    for f, e in failures:
        print(f"  {f}: {e}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
