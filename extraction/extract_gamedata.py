#!/usr/bin/env python3
"""extract_gamedata.py -- Unity GameData ScriptableObject -> JSON converter.

Reads the READ-ONLY Unity template at "My project/Assets/BulletHellTemplate/"
and writes pure-JSON data dumps to bullet-heaven/extraction/gamedata-json/.

Outputs:
  extraction/guid-map.json           GUID -> project-relative asset path (Task 1)
  extraction/gamedata-json/...       one JSON per GameData .asset (Task 2)
  extraction/gamedata-json/skills/   extra game-data SOs found under Res/Skills
  extraction/gamedata-json/drops/    MonoBehaviour data from Res/Drops prefabs
  extraction/stripped-keys-log.json  flavor-text keys removed per file (legal)

No .cs file is ever opened; script identity comes from .meta GUID -> path only.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import yaml

UNITY_PROJECT = Path(r"C:/roguelike roblox/My project")
BHT = UNITY_PROJECT / "Assets" / "BulletHellTemplate"
OUT = Path(r"C:/roguelike roblox/bullet-heaven/extraction")
JSON_OUT = OUT / "gamedata-json"
GAMEDATA = BHT / "Res" / "GameData"
DROPS = BHT / "Res" / "Drops"

# Unity boilerplate keys dropped from every dumped MonoBehaviour document.
DROP_KEYS = {
    "m_ObjectHideFlags",
    "m_CorrespondingSourceObject",
    "m_PrefabInstance",
    "m_PrefabAsset",
    "m_GameObject",
    "m_Enabled",
    "m_EditorHideFlags",
    "m_EditorClassIdentifier",
}

REF_KEYS = {"fileID", "guid", "type"}

DOC_HEADER = re.compile(r"^--- !u!(\d+) &(-?\d+)( stripped)?[ \t]*$", re.M)
GUID_LINE = re.compile(r"^guid: ([0-9a-f]{32})\s*$", re.M)


# --------------------------------------------------------------------------
# YAML loading: SafeLoader + multi-constructor that ignores !u! tags.
# --------------------------------------------------------------------------
class UnityLoader(yaml.SafeLoader):
    """SafeLoader that constructs unknown !u! tags as plain YAML nodes."""


def _construct_unknown(loader: yaml.Loader, tag_suffix: str, node: yaml.Node):
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node, deep=True)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node, deep=True)
    return loader.construct_scalar(node)


# Both forms: bare local tag (!u!114) and %TAG-resolved form.
UnityLoader.add_multi_constructor("!u!", _construct_unknown)
UnityLoader.add_multi_constructor("tag:unity3d.com,2011:", _construct_unknown)


def parse_unity_yaml(path: Path):
    """Split a Unity YAML file into documents.

    Returns list of dicts: {class_id, anchor_id, stripped, data}.
    Parse errors raise; callers collect them.
    """
    text = path.read_text(encoding="utf-8")
    headers = list(DOC_HEADER.finditer(text))
    docs = []
    for i, m in enumerate(headers):
        start = m.start()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        chunk = text[start:end]
        # Remove Unity's non-standard " stripped" suffix (YAML syntax error).
        chunk = chunk.replace(" stripped\n", "\n", 1)
        # Re-declare the !u! tag handle per chunk (the %TAG directive lives at
        # the top of the original file, outside any chunk).
        chunk = "%TAG !u! tag:unity3d.com,2011:\n" + chunk
        data = yaml.load(chunk, Loader=UnityLoader)  # dup keys: last wins
        docs.append(
            {
                "class_id": int(m.group(1)),
                "anchor_id": int(m.group(2)),
                "stripped": bool(m.group(3)),
                "data": data,
            }
        )
    return docs


# --------------------------------------------------------------------------
# Task 1 -- GUID map from .meta files (never opens the referenced files).
# ThirdPartyResources/Tools is vendored code: excluded (off-limits).
# --------------------------------------------------------------------------
def build_guid_map():
    guid_map = {}
    for meta in BHT.rglob("*.meta"):
        rel = meta.relative_to(UNITY_PROJECT).as_posix()
        if rel.startswith("Assets/BulletHellTemplate/ThirdPartyResources/Tools/"):
            continue
        try:
            text = meta.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"WARN: cannot read {rel}: {exc}", file=sys.stderr)
            continue
        m = GUID_LINE.search(text)
        if not m:
            continue
        asset_path = rel[: -len(".meta")]
        guid_map[m.group(1)] = asset_path
    return guid_map


# --------------------------------------------------------------------------
# Transforms
# --------------------------------------------------------------------------
def is_ref_dict(d) -> bool:
    return isinstance(d, dict) and "fileID" in d and set(d.keys()) <= REF_KEYS


def convert_ref(d, guid_map):
    guid = d.get("guid")
    fid = d.get("fileID", 0)
    if not guid or fid == 0:
        return None
    path = guid_map.get(guid)
    if path:
        return {"$ref": path, "fileID": fid}
    return {"$ref": None, "guid": guid, "fileID": fid}


def transform(node, guid_map, stripped, path=""):
    if is_ref_dict(node):
        return convert_ref(node, guid_map)
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            kp = f"{path}.{k}" if path else str(k)
            if k in DROP_KEYS:
                continue
            if "description" in str(k).lower():  # flavor-text strip (legal)
                stripped.append(kp)
                continue
            out[k] = transform(v, guid_map, stripped, kp)
        return out
    if isinstance(node, list):
        return [
            transform(v, guid_map, stripped, f"{path}[{i}]")
            for i, v in enumerate(node)
        ]
    return node


def script_type_of(transformed_doc, guid_map):
    """_scriptType = basename of the .cs path resolved from m_Script guid."""
    ref = transformed_doc.get("m_Script")
    if isinstance(ref, dict):
        p = ref.get("$ref")
        if p:
            return p.rsplit("/", 1)[-1]
    return None


def unwrap_root(data):
    """Drop the Unity class-name root key (e.g. {"MonoBehaviour": {...}})."""
    if isinstance(data, dict) and len(data) == 1:
        inner = next(iter(data.values()))
        if isinstance(inner, dict):
            return inner
    return data


def dump_asset_docs(docs, guid_map, stripped_log, log_key):
    """Transform all class-114 docs of one file; returns JSON-ready object."""
    mono = [
        unwrap_root(d["data"])
        for d in docs
        if d["class_id"] == 114 and isinstance(unwrap_root(d["data"]), dict)
    ]
    if not mono:
        return None
    out = []
    for data in mono:
        stripped = []
        t = transform(data, guid_map, stripped)
        t["_scriptType"] = script_type_of(t, guid_map)
        if stripped:
            stripped_log[log_key] = stripped
        out.append(t)
    return out[0] if len(out) == 1 else out


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# --------------------------------------------------------------------------
def main():
    guid_map = build_guid_map()
    write_json(OUT / "guid-map.json", dict(sorted(guid_map.items())))
    print(f"guid-map: {len(guid_map)} guids")

    stripped_log = {}
    failures = []
    written = []  # (out_rel_path, category)
    unresolved_guids = set()

    def collect_unresolved(node):
        if isinstance(node, dict):
            if node.get("$ref") is None and "guid" in node:
                unresolved_guids.add(node["guid"])
            for v in node.values():
                collect_unresolved(v)
        elif isinstance(node, list):
            for v in node:
                collect_unresolved(v)

    def convert(asset: Path, out_path: Path, log_key: str):
        try:
            docs = parse_unity_yaml(asset)
        except Exception as exc:  # noqa: BLE001 - collect, report, fail loudly
            failures.append((asset.relative_to(BHT).as_posix(), str(exc)))
            return
        obj = dump_asset_docs(docs, guid_map, stripped_log, log_key)
        if obj is None:
            failures.append(
                (asset.relative_to(BHT).as_posix(), "no class-114 MonoBehaviour doc")
            )
            return
        collect_unresolved(obj)
        write_json(out_path, obj)
        written.append(out_path.relative_to(JSON_OUT).as_posix())

    # --- Task 2: all GameData assets ---
    for asset in sorted(GAMEDATA.rglob("*.asset")):
        rel = asset.relative_to(GAMEDATA)
        parts = list(rel.parts)
        category = parts[0].lower()
        sub = [p.lower() for p in parts[1:-1]]
        if sub and sub[0] == "shopdataitems":
            sub[0] = "items"
        out_path = JSON_OUT / category / Path(*sub) / (rel.stem + ".json")
        convert(asset, out_path, out_path.relative_to(JSON_OUT).as_posix())

    # --- Task 2 extra: game-data SOs elsewhere under Res/ and
    # ThirdPartyResources/ (Tools excluded -- vendored code, off-limits).
    # Rule: a .asset is game data iff its m_Script guid resolves to a project
    # script path under Assets/BulletHellTemplate/Core/ (URP/package scripts
    # don't). Binary engine artifacts (LightingData, NavMesh) are skipped.
    def extra_out_path(asset: Path):
        """(category, [subdirs]) for an extra game-data asset, or None."""
        if GAMEDATA in asset.parents:
            return None
        try:
            rel = asset.relative_to(BHT / "Res")
            return rel.parts[0].lower(), [p.lower() for p in rel.parts[1:-1]]
        except ValueError:
            pass
        rel = asset.relative_to(BHT / "ThirdPartyResources")
        parts = rel.parts
        if parts[0] == "Tools":
            return None
        if parts[0] == "Characters" and len(parts) >= 3:
            return "skills", [parts[1].lower().replace(" ", "_")]
        if parts[0] == "Monsters" and len(parts) >= 3:
            return "monsters", [parts[1].lower().replace(" ", "_")]
        return parts[0].lower(), [p.lower() for p in parts[1:-1]]

    extra_candidates = []

    def iter_assets(root: Path, prune: str | None = None):
        """Yield *.asset files; never descend into the pruned subdir."""
        for dirpath, dirnames, filenames in os.walk(root):
            if prune and Path(dirpath) == root and prune in dirnames:
                dirnames.remove(prune)
            for fn in filenames:
                if fn.endswith(".asset"):
                    yield Path(dirpath) / fn

    extra_roots = [(BHT / "Res", None), (BHT / "ThirdPartyResources", "Tools")]
    for root, prune in extra_roots:
        for asset in sorted(iter_assets(root, prune)):
            dest = extra_out_path(asset)
            if dest is None:
                continue
            rel_bht = asset.relative_to(BHT).as_posix()
            with asset.open("rb") as fh:
                magic = fh.read(5)
            if magic != b"%YAML":
                extra_candidates.append((rel_bht, "SKIPPED", "binary engine artifact"))
                continue
            try:
                docs = parse_unity_yaml(asset)
            except Exception as exc:  # noqa: BLE001
                failures.append((rel_bht, str(exc)))
                continue
            mono = [
                unwrap_root(d["data"])
                for d in docs
                if d["class_id"] == 114 and isinstance(unwrap_root(d["data"]), dict)
            ]
            if not mono:
                extra_candidates.append(
                    (rel_bht, "SKIPPED", "no MonoBehaviour (engine asset)")
                )
                continue
            script_ref = mono[0].get("m_Script") or {}
            spath = guid_map.get(script_ref.get("guid"), "")
            if spath.startswith("Assets/BulletHellTemplate/Core/"):
                top, sub = dest
                out_path = JSON_OUT / top / Path(*sub) / (asset.stem + ".json")
                convert(asset, out_path, out_path.relative_to(JSON_OUT).as_posix())
                extra_candidates.append((rel_bht, top, spath))
            else:
                extra_candidates.append((rel_bht, "SKIPPED", spath or "unresolved script"))

    # --- Task 2: drops from prefab MonoBehaviours ---
    for prefab in sorted(DROPS.glob("*.prefab")):
        out_path = JSON_OUT / "drops" / (prefab.stem + ".json")
        convert(prefab, out_path, out_path.relative_to(JSON_OUT).as_posix())

    write_json(OUT / "stripped-keys-log.json", stripped_log)

    # --- Verification: every written file must round-trip as valid JSON ---
    bad_json = []
    for w in written:
        p = JSON_OUT / w
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            bad_json.append((w, str(exc)))

    # --- Summary ---
    from collections import Counter

    cats = Counter(w.split("/")[0] for w in written)
    print("\n=== per-category counts ===")
    for c in sorted(cats):
        print(f"  {c}: {cats[c]}")
    print(f"  TOTAL: {len(written)}")
    print("\n=== extra .asset candidates under Res/ (outside GameData) ===")
    for rel, cat, spath in extra_candidates:
        print(f"  [{cat}] {rel}  (script: {spath})")
    print(f"\nunresolved guids referenced: {len(unresolved_guids)}")
    for g in sorted(unresolved_guids):
        print(f"  {g}")
    print(f"\nstripped-key files: {len(stripped_log)}")
    print(f"json round-trip failures: {len(bad_json)}")
    for w, e in bad_json:
        print(f"  {w}: {e}")
    print(f"parse failures: {len(failures)}")
    for f, e in failures:
        print(f"  {f}: {e}")
    return 1 if (failures or bad_json) else 0


if __name__ == "__main__":
    sys.exit(main())
