# build_provenance.py — generate legal/provenance.csv from extraction/asset-inventory.csv
# Rules derived from context/01 + web verification performed 2026-09-02 (see report).
import csv, os

BASE = os.path.dirname(os.path.abspath(__file__))          # extraction/
ROOT = os.path.dirname(BASE)                                # bullet-heaven/
INV = os.path.join(BASE, "asset-inventory.csv")
OUT = os.path.join(ROOT, "legal", "provenance.csv")

U_KAYKIT_SK = "https://github.com/KayKit-Game-Assets/KayKit-Character-Pack-Skeletons-1.0"
U_KAYKIT_AD = "https://github.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0"
U_KENNEY_MD = "https://kenney.nl/assets/mini-dungeon"
U_KENNEY_MA = "https://kenney.nl/assets/mini-arena"
U_KENNEY_PP = "https://kenney.nl/assets/particle-pack"
U_DAFONT_EE = "https://www.dafont.com/evil-empire.font"
U_DAFONT_AH = "https://www.dafont.com/ander-hedge.font"
U_LILITA = "https://raw.githubusercontent.com/google/fonts/main/ofl/lilitaone/LilitaOne-Regular.ttf"
U_NOTO = "https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/OFL.txt"
U_NILO = "https://github.com/ColinLeung-NiloCat/UnityURPToonLitShaderExample"
U_RHOS = "https://rhosgfx.itch.io/vector-ranks"
U_COD = "https://www.codester.com/items/55926/bullethell-elemental-template-unity"
U_PP_MON = "https://poly.pizza/bundle/Ultimate-Monsters-Bundle-5oyGWAmOB6"
U_QUAT = "https://quaternius.com/packs/ultimatemonsters.html"
U_INCO = "https://incompetech.com/music/royalty-free/full_list.php"
U_PIX = "https://pixabay.com/music/sneaky-at-the-park-afternoon-193011/"

REBUILD_NOTE = "rebuilt natively in Roblox; nothing imported"
EULA_B = "embed only, no standalone redistribution; upload Restricted"
N_MESH = "mesh <=20k tri, single UV, watertight; identical MeshId+TextureId for instancing"
N_RIG = "rigged mesh: use Roblox Importer (not bulk), <=4 bone influences/vertex, frozen transforms"
N_TEX = "texture <=1024px (Roblox downscales larger); OpenGL-normal convention if normal maps"
N_AUD = "audio <20MB, <7min, <=48kHz; private upload; ID-verified quota 2000/30d"
N_FONT = "upload TTF/OTF as custom font (FontFace); Roblox does not use TMP SDF assets"

NONPORTABLE = {"mat", "shader", "shadergraph", "controller", "prefab", "anim", "asset",
               "unity", "lighting", "mask", "spriteatlasv2", "rendertexture", "exr", "hlsl"}

# template files verified byte-identical (sha256) against KayKit repos, 2026-09-02
HASH_MATCH_ADVENTURERS_ACC = {  # basename set (accessories)
    "arrow.fbx","arrow_bundle.fbx","axe_1handed.fbx","axe_2handed.fbx","crossbow_1handed.fbx",
    "crossbow_2handed.fbx","dagger.fbx","mug_empty.fbx","mug_full.fbx","quiver.fbx",
    "shield_badge.fbx","shield_badge_color.fbx","shield_round.fbx","shield_round_barbarian.fbx",
    "shield_round_color.fbx","shield_spikes.fbx","shield_spikes_color.fbx","shield_square.fbx",
    "shield_square_color.fbx","smokebomb.fbx","spellbook_closed.fbx","spellbook_open.fbx",
    "staff.fbx","sword_1handed.fbx","sword_2handed.fbx","sword_2handed_color.fbx","wand.fbx"}
HASH_MATCH_ADVENTURERS_TEX = {"barbarian_texture.png","knight_texture.png","mage_texture.png","rogue_texture.png"}
SKELETON_TEX = "skeleton_texture.png"  # sha256-identical to KayKit Skeletons pack texture

def row(path, type_, license_, conf, url, path_choice, notes, verification):
    return {"path": path, "type": type_, "license": license_, "license_confidence": conf,
            "source_url": url, "chosen_path": path_choice, "roblox_import_notes": notes,
            "verification": verification}

def classify(r):
    p, fmt, type_ = r["path"], r["format"], r["type"]
    base = os.path.basename(p)
    out = None

    # ---------- ThirdPartyResources ----------
    if p.startswith("ThirdPartyResources/3DModels/KayKit - Adventurers/"):
        lic, conf, ver = "CC0", "high", "bundled-license"
        if fmt in NONPORTABLE:
            note = REBUILD_NOTE + "; Unity " + fmt + " wrapper around KayKit CC0 content (canonical content re-downloaded via Path A)"
            if fmt == "anim":
                note = REBUILD_NOTE + "; Unity .anim YAML not portable; identical clip name ships in KayKit packs' 95-animation set (verified); re-import clip from originals GLB/FBX"
            out = row(p, type_, lic, conf, U_KAYKIT_AD, "rebuild", note, ver)
        elif fmt == "fbx":
            if base in HASH_MATCH_ADVENTURERS_ACC:
                out = row(p, type_, lic, conf, U_KAYKIT_AD, "A",
                          "byte-identical (sha256) to KayKit Adventures repo original; use extraction/originals/kaykit-adventurers copy. " + N_MESH, "verified")
            elif base in ("barbarian.fbx","druid.fbx","engineer.fbx","knight.fbx","mage.fbx","rogue.fbx","rogue_hooded.fbx"):
                extra = " EXTRA-tier character (itch.io paid tier, still CC0)" if base in ("druid.fbx","engineer.fbx") else ""
                out = row(p, type_, lic, conf, U_KAYKIT_AD, "A",
                          "KayKit Adventures character" + extra + "; all 41 rig joints + mesh node names match repo GLB (verified); template FBX is animation-stripped re-export - use originals. " + N_RIG, "verified")
            else:  # potions, ammo_crate, druid_staff, engineer_Wrench, shotgun
                out = row(p, type_, lic, conf, U_KAYKIT_AD, "B",
                          "KayKit EXTRA/newer-tier accessory not in free GitHub 1.0 repo; bundled License.txt covers pack; use template copy or buy EXTRA tier. " + N_MESH, "bundled-license")
        elif fmt == "png":
            if base in HASH_MATCH_ADVENTURERS_TEX:
                out = row(p, type_, lic, conf, U_KAYKIT_AD, "A", "byte-identical (sha256) to KayKit repo gradient atlas. " + N_TEX, "verified")
            elif base.startswith(("druid_texture", "engineer_texture")) or "_alt_" in base:
                out = row(p, type_, lic, conf, U_KAYKIT_AD, "B", "KayKit EXTRA-tier texture variant (not in free repo); bundled License.txt covers pack. " + N_TEX, "bundled-license")
            else:
                out = row(p, type_, lic, conf, U_KAYKIT_AD, "B", "KayKit pack texture variant. " + N_TEX, "bundled-license")
        elif fmt == "txt":
            out = row(p, type_, lic, conf, U_KAYKIT_AD, "A", "pack license file; archived at legal/licenses/KayKit-Adventurers-bundled-in-template-CC0.txt", "verified")
    elif p.startswith("ThirdPartyResources/3DModels/MiniDungeon/"):
        if fmt in NONPORTABLE:
            out = row(p, type_, "CC0", "high", U_KENNEY_MD, "rebuild", REBUILD_NOTE + "; Unity " + fmt + " wrapper around Kenney CC0 content", "bundled-license")
        elif fmt in ("fbx", "png"):
            out = row(p, type_, "CC0", "high", U_KENNEY_MD, "A",
                      "Kenney Mini Dungeon (template bundles v1.5; re-downloaded v2.0 zip from kenney.nl, license CC0 both). " + (N_RIG if "character" in base else N_MESH), "verified")
        else:
            out = row(p, type_, "CC0", "high", U_KENNEY_MD, "A", "pack license file; archived at legal/licenses/Kenney-MiniDungeon-bundled-in-template-CC0.txt", "verified")
    elif p.startswith("ThirdPartyResources/3DModels/MiniArena/"):
        if fmt in NONPORTABLE:
            out = row(p, type_, "CC0", "high", U_KENNEY_MA, "rebuild", REBUILD_NOTE + "; Unity " + fmt + " wrapper around Kenney CC0 content", "bundled-license")
        elif fmt in ("fbx", "png"):
            out = row(p, type_, "CC0", "high", U_KENNEY_MA, "A",
                      "Kenney Mini Arena (v1.1 bundled; re-downloaded zip from kenney.nl, CC0). " + (N_RIG if "character" in base else N_MESH), "verified")
        else:
            out = row(p, type_, "CC0", "high", U_KENNEY_MA, "A", "pack license file; archived at legal/licenses/Kenney-MiniArena-bundled-in-template-CC0.txt", "verified")
    elif p.startswith("ThirdPartyResources/3DModels/Skeleton Mage/"):
        if fmt == "fbx":
            out = row(p, type_, "CC0", "high", U_KAYKIT_SK, "A",
                      "Skeleton_Mage = KayKit Skeletons pack (exact name; full deform-bone set + submesh names match repo GLB; texture sha256-identical). Template file is 27MB ASCII re-export - import from originals instead. " + N_RIG, "verified")
        elif fmt == "png":
            if base == SKELETON_TEX:
                out = row(p, type_, "CC0", "high", U_KAYKIT_SK, "A", "byte-identical (sha256) to KayKit Skeletons skeleton_texture.png. " + N_TEX, "verified")
            else:
                out = row(p, type_, "CC0", "medium", U_KAYKIT_SK, "B", "recolor variant of CC0 skeleton_texture made for template; embed-only as modified copy. " + N_TEX, "bundled-license")
        else:
            out = row(p, type_, "CC0", "high", U_KAYKIT_SK, "rebuild", REBUILD_NOTE + "; Unity " + fmt + " wrapper around KayKit CC0 content", "bundled-license")
    elif p.startswith("ThirdPartyResources/3DModels/Monsters/"):
        if fmt in NONPORTABLE:
            out = row(p, type_, "CC0", "medium", U_PP_MON, "rebuild", REBUILD_NOTE + "; Unity " + fmt + " wrapper around Quaternius CC0 content", "publisher-disclosure")
        elif fmt == "fbx":
            out = row(p, type_, "CC0", "medium", U_PP_MON + " ; " + U_QUAT, "B",
                      "matches Quaternius Ultimate Monsters naming (pack verified CC0); per-file page not fetched (poly.pizza Cloudflare); pack bulk download not attempted. Rigged: " + N_RIG, "unverified")
        else:
            out = row(p, type_, "CC0", "medium", U_PP_MON, "B", "monster gradient atlas, Quaternius pack style; per-file unverified. " + N_TEX, "unverified")
    elif p.startswith("ThirdPartyResources/3DModels/Misc/"):
        if fmt == "fbx":
            out = row(p, type_, "CC0", "low", U_COD, "B",
                      "no public original located for " + base + "; publisher disclosure covers ThirdPartyResources 3D models as poly.pizza CC0; re-verify before upload. " + N_MESH, "unverified")
        else:
            out = row(p, type_, "Unity-EULA", "high", U_COD, "rebuild", REBUILD_NOTE, "unverified")
    elif p.startswith("ThirdPartyResources/Characters/"):
        out = classify_characters(p, fmt, type_, base)
    elif p.startswith("ThirdPartyResources/Monsters/"):
        out = row(p, type_, "Unity-EULA", "high", U_COD, "rebuild",
                  REBUILD_NOTE + " (boss/monster prefab+skill wiring is template logic; monster meshes themselves are Quaternius CC0 - see 3DModels/Monsters)", "unverified")
    elif p.startswith("ThirdPartyResources/New UI/"):
        out = classify_newui(p, fmt, type_, base)
    elif p.startswith("ThirdPartyResources/Font/"):
        out = classify_fonts(p, fmt, type_, base)
    elif p.startswith("ThirdPartyResources/Audio/"):
        out = row(p, type_, "CC0 (per publisher disclosure), per-file unverified", "medium", U_COD, "B",
                  "freesound.org CC0 per publisher disclosure; anonymous per-file match failed (2026-09-02) - re-verify each file is CC0 (not CC-BY-NC) before Roblox upload. " + N_AUD, "unverified")
    elif p.startswith("ThirdPartyResources/Effects/"):
        out = row(p, type_, "Unity-EULA", "medium", U_COD, "B",
                  "VFX texture, no CC0/MIT source located; treated as BizachiCode-original. " + EULA_B + ". " + N_TEX, "unverified")
    elif p.startswith("ThirdPartyResources/Particle samples/"):
        if fmt in NONPORTABLE:
            out = row(p, type_, "CC0", "high", U_KENNEY_PP, "rebuild", REBUILD_NOTE + "; Unity " + fmt + " wrapper around Kenney CC0 sprite", "bundled-license")
        elif fmt == "png":
            out = row(p, type_, "CC0", "high", U_KENNEY_PP, "A", "Kenney Particle Pack sprite (re-downloaded zip, CC0); use as ParticleEmitter texture/flipbook, <=400 particles/s. " + N_TEX, "verified")
        else:
            out = row(p, type_, "CC0", "high", U_KENNEY_PP, "A", "pack license file; archived at legal/licenses/Kenney-ParticlePack-bundled-in-template-CC0.txt", "verified")
    elif p.startswith("ThirdPartyResources/Shaders/"):
        if fmt == "txt":
            out = row(p, type_, "MIT", "high", U_NILO, "A", "NiloToon MIT license; archived at legal/licenses/NiloToon-SimpleURPToonLit-MIT.txt", "verified")
        else:
            out = row(p, type_, "MIT", "high", U_NILO, "rebuild",
                      "SimpleURPToonLit (NiloToon, MIT) is Unity URP shader code - not portable; " + REBUILD_NOTE + " (toon look approximated with SurfaceAppearance/MaterialVariant)", "verified")
    elif p.startswith("ThirdPartyResources/ShurikenSkill/"):
        if fmt in ("fbx", "png"):
            out = row(p, type_, "CC0", "low", U_COD, "B",
                      "shuriken mesh/texture, no public original located; publisher disclosure covers ThirdPartyResources as poly.pizza CC0; re-verify before upload. " + N_MESH, "unverified")
        else:
            out = row(p, type_, "Unity-EULA", "high", U_COD, "rebuild", REBUILD_NOTE, "unverified")
    elif p.startswith("ThirdPartyResources/BoxEntity"):
        out = row(p, type_, "Unity-EULA", "high", U_COD, "rebuild", REBUILD_NOTE, "unverified")

    # ---------- Res/ (BizachiCode-original) ----------
    elif p.startswith("Res/Audio/Music/AudioClip_Music_Darkling"):
        out = row(p, type_, "CC-BY", "high", U_INCO, "A",
                  "'Darkling' Kevin MacLeod (incompetech), ISRC USUAN1700050, CC BY - attribution required or paid no-attribution license; consider CC0 replacement. " + N_AUD, "verified")
    elif p.startswith("Res/Audio/Music/AudioClip_Music_MorganaRides"):
        out = row(p, type_, "CC-BY", "high", U_INCO, "A",
                  "'Morgana Rides' Kevin MacLeod (incompetech), ISRC USUAN1800010, CC BY - attribution required or paid no-attribution license; consider CC0 replacement. " + N_AUD, "verified")
    elif p.startswith("Res/Audio/Ambient/at-the-park-afternoon"):
        out = row(p, type_, "Pixabay-Content", "high", U_PIX, "A",
                  "'At the Park (Afternoon)' by XtremeFreddy, Pixabay Music (Pixabay Content License: free commercial use, no standalone redistribution). " + N_AUD, "verified")
    elif p.startswith("Res/Audio/Ambient/AudioClip_Background-Ambient"):
        out = row(p, type_, "Unity-EULA", "low", U_COD, "B",
                  "34.5MB ambience EXCEEDS Roblox 20MB limit - recompress/replace; source not located. " + EULA_B + ". " + N_AUD, "unverified")
    elif p.startswith("Res/Audio/"):
        out = row(p, type_, "Unity-EULA", "low", U_COD, "B",
                  "SFX not covered by publisher disclosure (it names ThirdPartyResources/Audio only); no source located; treat as BizachiCode-original. " + EULA_B + ". " + N_AUD, "unverified")
    elif p == "Res/OldUI/Font/AnderHedgeRegular.ttf":
        out = row(p, type_, "unknown", "low", U_DAFONT_AH, "B",
                  "REPLACEMENT NEEDED: 'Ander Hedge' by Jayvee Enaguas is dafont '100% Free' freeware with no explicit cross-engine redistribution grant; replace with Evil Empire (OFL-1.1) or Lilita One (OFL). " + N_FONT, "unverified")
    elif p == "Res/OldUI/Font/AnderHedgeRegular SDF.asset":
        out = row(p, type_, "unknown", "low", U_DAFONT_AH, "rebuild",
                  REBUILD_NOTE + "; TMP SDF derived from Ander Hedge font - REPLACEMENT NEEDED (see .ttf row); Roblox uses raw font files, not SDF assets", "unverified")
    elif p.startswith("Res/"):
        if fmt == "psd":
            out = row(p, type_, "Unity-EULA", "high", U_COD, "B",
                      "flatten PSD to PNG/TGA before upload (Roblox accepts png/jpg/gif/tga/bmp). " + EULA_B, "n/a")
        elif fmt in NONPORTABLE:
            note = REBUILD_NOTE
            if p.startswith("Res/GameData/"):
                note += "; design data already extracted to extraction/gamedata-json (rebuild as Luau Config modules)"
            if fmt == "spriteatlasv2":
                note += "; sprite atlas is Unity packing metadata - the source PNGs carry the art"
            out = row(p, type_, "Unity-EULA", "high", U_COD, "rebuild", note, "n/a")
        else:  # png and any other portable format under Res/
            out = row(p, type_, "Unity-EULA", "high", U_COD, "B",
                      "BizachiCode-original. " + EULA_B + ". " + (N_TEX if fmt == "png" else ""), "n/a")

    if out is None:
        out = row(p, type_, "unknown", "low", "", "B", "REPLACEMENT NEEDED: unclassified by build_provenance rules", "unverified")
    return out

def classify_characters(p, fmt, type_, base):
    if fmt in NONPORTABLE:
        note = REBUILD_NOTE
        if fmt == "mat":
            note += "; Unity material referencing character texture (texture rows carry the real license)"
        elif fmt in ("controller",):
            note += "; Mecanim state machine - re-implement in Luau with AnimationTrack priority/loops"
        elif fmt == "asset":
            note += "; ScriptableObject skill data - rebuild as Luau Config (values already extracted to extraction/gamedata-json where applicable)"
        return row(p, type_, "Unity-EULA", "high", U_COD, "rebuild", note, "n/a")
    if fmt == "fbx":
        skel = {"Skeleton_Warrior.fbx", "Skeleton_Rogue.fbx"}
        if base in skel:
            return row(p, type_, "CC0", "high", U_KAYKIT_SK, "A",
                       "KayKit Skeletons pack character (exact name; deform-bone set + submesh names match repo GLB; texture sha256-identical). Template file is 27MB ASCII re-export - import from extraction/originals/kaykit-skeletons instead. " + N_RIG, "verified")
        near = {"Staff.fbx": "Skeleton_Staff.fbx (KayKit Skeletons)", "Blade.fbx": "Skeleton_Blade.fbx (KayKit Skeletons)",
                "Dagger 3.fbx": "dagger.fbx (KayKit Adventurers, hash differs = re-export)", "Sword.fbx": "sword_1handed.fbx (KayKit Adventurers, hash differs)"}
        if base in near:
            return row(p, type_, "CC0", "medium", U_KAYKIT_SK, "B",
                       "near-match to KayKit original " + near[base] + "; template file is a re-export; prefer Path A original from extraction/originals. " + N_MESH, "unverified")
        quat = {"Mushnub.fbx", "Slime.fbx", "Alien.fbx"}
        if base in quat:
            return row(p, type_, "CC0", "medium", U_PP_MON + " ; " + U_QUAT, "B",
                       "Quaternius Ultimate Monsters model (pack verified CC0; per-file page not fetched). " + N_RIG, "unverified")
        guess = {"Planet_11.fbx": ("likely a poly.pizza space/planet pack model; unverified", N_MESH),
                 "Blackhole.fbx": ("no public original located; possibly BizachiCode-original VFX mesh; unverified", N_MESH),
                 "Adventurer.fbx": ("rigged chibi character (playable 'Vincent'); no KayKit/Quaternius name match; publisher disclosure: poly.pizza CC0; unverified", N_RIG),
                 "Survival.fbx": ("rigged zombie-style character (Zombie_Atlas textures); no pack name match; publisher disclosure: poly.pizza CC0; unverified", N_RIG),
                 "Gun2.fbx": ("gun mesh for SkeletonGunner; no pack name match (cf. EXTRA-tier shotgun); unverified", N_MESH),
                 "Bullet.fbx": ("projectile mesh; no pack name match; unverified", N_MESH),
                 "Lazy Potion.fbx": ("FBX-SDK 2020 export (differs from KayKit Blender toolchain); no source located; unverified", N_MESH),
                 "PoisonPuddle.fbx": ("VFX mesh; no source located; unverified", N_MESH)}
        g, lim = guess.get(base, ("unmatched poly.pizza candidate; unverified", N_MESH))
        return row(p, type_, "CC0", "low", U_COD, "B",
                   g + "; publisher disclosure covers ThirdPartyResources models as CC0. " + lim, "unverified")
    if fmt == "png":
        if base == SKELETON_TEX:
            return row(p, type_, "CC0", "high", U_KAYKIT_SK, "A", "byte-identical (sha256) to KayKit Skeletons texture. " + N_TEX, "verified")
        if base.startswith("skeleton_texture"):
            return row(p, type_, "CC0", "medium", U_KAYKIT_SK, "B", "recolor variant of CC0 skeleton_texture (skin variant); embed-only as modified copy. " + N_TEX, "bundled-license")
        if base.startswith("Zombie_Atlas") or base == "Color.png":
            return row(p, type_, "CC0", "low", U_COD, "B", "character atlas, poly.pizza-sourced per disclosure; per-file unverified. " + N_TEX, "unverified")
        # skill icons / effect textures
        return row(p, type_, "Unity-EULA", "medium", U_COD, "B",
                   "skill icon / VFX texture, likely BizachiCode-original. " + EULA_B + ". " + N_TEX, "unverified")
    return row(p, type_, "unknown", "low", "", "B", "REPLACEMENT NEEDED: unclassified character file", "unverified")

def classify_newui(p, fmt, type_, base):
    if "/Ranks/" in p:
        if fmt == "txt":
            return row(p, type_, "CC0", "high", U_RHOS, "A", "RhosGFX Vector Ranks CC0 license; archived at legal/licenses/RhosGFX-VectorRanks-CC0.txt", "verified")
        if fmt == "png":
            return row(p, type_, "CC0", "high", U_RHOS, "B", "RhosGFX '[FREE] Vector Ranks' icon (CC0; bundled license in template; itch page verified). " + N_TEX, "verified")
        return row(p, type_, "CC0", "high", U_RHOS, "rebuild", REBUILD_NOTE, "verified")
    if base == "EvilEmpire.asset":
        return row(p, type_, "OFL-1.1", "high", U_DAFONT_EE, "rebuild",
                   "TMP SDF asset derived from 'Evil Empire' font (Tup Wanders); re-download OFL original (extraction/originals/font-evil-empire); " + N_FONT, "verified")
    if fmt == "spriteatlasv2":
        return row(p, type_, "MIT", "medium", U_COD, "rebuild", REBUILD_NOTE + "; Unity atlas packing metadata - source PNGs carry the art", "publisher-disclosure")
    if fmt == "png":
        return row(p, type_, "MIT", "medium", U_COD, "B",
                   "publisher disclosure: NewUI images MIT by Evghenii Conev (no public original located 2026-09-02); keep MIT notice + disclosure with repo; upload Restricted anyway. " + N_TEX, "publisher-disclosure")
    return row(p, type_, "MIT", "medium", U_COD, "rebuild", REBUILD_NOTE, "publisher-disclosure")

def classify_fonts(p, fmt, type_, base):
    if base == "LilitaOne-Regular.ttf":
        return row(p, type_, "OFL-1.1", "high", U_LILITA, "A",
                   "Lilita One by Juan Montoreano, SIL OFL 1.1 (google/fonts, re-downloaded); license at legal/licenses/LilitaOne-OFL.txt. " + N_FONT, "verified")
    if fmt == "ttf":  # Noto family
        return row(p, type_, "OFL-1.1", "high", U_NOTO, "A",
                   "Noto Sans family (Google), SIL OFL 1.1; OFL archived at legal/licenses/NotoSans-OFL.txt; current google/fonts ships variable-font variants - re-download per style as needed. " + N_FONT, "verified")
    if fmt == "txt":  # NotoSans range files
        return row(p, type_, "OFL-1.1", "medium", U_NOTO, "rebuild",
                   REBUILD_NOTE + "; TMP font-subsetting range list - Roblox does not subset fonts this way", "publisher-disclosure")
    # SDF assets + atlas PNGs (TMP-generated)
    return row(p, type_, "OFL-1.1", "high", U_LILITA if "Lilita" in base else U_NOTO, "rebuild",
               REBUILD_NOTE + "; TextMeshPro SDF font asset/atlas - Unity-only; Roblox imports the raw TTF/OTF (" + N_FONT + ")", "verified")

def main():
    rows = list(csv.DictReader(open(INV, encoding="utf-8")))
    out = [classify(r) for r in rows]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "type", "license", "license_confidence",
                                          "source_url", "chosen_path", "roblox_import_notes", "verification"])
        w.writeheader()
        w.writerows(out)
    # quick stats
    from collections import Counter
    print("rows:", len(out))
    print("license:", dict(Counter(r["license"] for r in out)))
    print("chosen_path:", dict(Counter(r["chosen_path"] for r in out)))
    print("verification:", dict(Counter(r["verification"] for r in out)))
    print("confidence:", dict(Counter(r["license_confidence"] for r in out)))

if __name__ == "__main__":
    main()
