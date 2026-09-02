# KayKit Visual/Name Diff — template characters & monsters vs KayKit packs

**Verdict: the template's characters ARE the KayKit Skeletons pack (confidence: HIGH) — and
more broadly the template's ThirdPartyResources 3D content is KayKit Character Packs
(Skeletons + Adventurers) plus Quaternius Ultimate Monsters, matching the publisher's
"CC0 / poly.pizza" disclosure.**

Evidence below is file-level, not vibes: SHA-256 byte equality, exact deformation-bone sets,
exact submesh names, and exact animation-clip name matches against the official KayKit
GitHub repos downloaded 2026-09-02 into `extraction/originals/`.

## Evidence summary

| Check | Result |
|---|---|
| `skeleton_texture.png` template vs KayKit Skeletons repo | **SHA-256 identical** (17037 B both) |
| Template `Models/Accessories/*.fbx` vs KayKit Adventures 1.0 repo `Assets/fbx/` | **27 of 48 byte-identical (SHA-256)**; 21 not in free repo (potions ×16, ammo_crate ×2, druid_staff, engineer_Wrench, shotgun) — these are KayKit **EXTRA-tier / later-version** items (itch.io EXTRA adds Engineer + Druid + accessories, still CC0) |
| Template skeleton FBX bone names vs `Skeleton_Mage.glb` skin joints | **All 23 template deform bones present** (`root, hips, spine, chest, upperarm.l, lowerarm.l, hand.l, handslot.l, head, upperleg.l, lowerleg.l, foot.l, toes.l, wrist.l …`); repo GLB adds only IK/control helper bones (18) |
| Template submesh names vs repo GLB mesh nodes | Exact: `Skeleton_Mage_Body/Eyes/Hat/Jaw/Skull/ArmLeft/ArmRight/LegLeft/LegRight` |
| Template `KayKit - Adventurers/Animations/*.anim` (95 Unity clips) vs Skeletons GLB animation names | **95 / 95 exact name matches** (Adventures 1.0 GLB alone covers 76; the Skeletons pack's 95-clip set covers all, incl. `Skeletons_Awaken_*`, `Death_C_Skeletons`) |
| Template `Characters/barbarian.fbx` vs Adventures `Barbarian.glb` | **41/41 joints + all mesh node names present** |
| Tri counts (inventory parse vs GLB) | Template ASCII FBX parse: Mage 2820 / Warrior 3755 / Rogue 3345; repo GLB totals: 4588 / 5934 / 5278 (GLB counts all submeshes; ratio ~1.6 constant across all three — same geometry, different export/counting) |
| Template FBX format note | Template skeleton FBX are 27 MB **ASCII FBX 7.3 re-exports**; KayKit originals are binary FBX (~22 MB) + GLB (~4.8 MB). **Import the originals, not the template files.** |

## The 3 parsed ASCII FBX leads (from the inventory)

| Template file | tri (inventory) | KayKit Skeletons repo match |
|---|---|---|
| `ThirdPartyResources/3DModels/Skeleton Mage/Skeleton_Mage.fbx` | 2820 | `Characters/fbx/Skeleton_Mage.fbx` — exact name; bones/submeshes/texture verified |
| `Characters/Skeleton Warrior/Models/Skeleton_Warrior.fbx` | 3755 | `Characters/fbx/Skeleton_Warrior.fbx` — exact name; verified as above |
| `Characters/SkeletonGunner/Models/Skeleton_Rogue.fbx` | 3345 | `Characters/fbx/Skeleton_Rogue.fbx` — exact name; verified as above |

All three names exist verbatim in the KayKit Skeletons Character Pack 1.0 repo
(`Skeleton_Mage`, `Skeleton_Minion`, `Skeleton_Rogue`, `Skeleton_Warrior`).

## poly.pizza naming comparison

- KayKit publishes the same packs on poly.pizza under the same display names
  ("Skeleton Mage", "Skeleton Warrior", "Skeleton Rogue", "Barbarian", "Knight" …) —
  the template simply kept the repo filenames (`Skeleton_Mage.fbx`, `barbarian.fbx`).
- The monster trio matches **Quaternius** (the other big poly.pizza CC0 author), not KayKit:
  `Mushnub.fbx` = Quaternius "Mushnub", `Alien.fbx` = "Alien", `Slime.fbx` = "Slime"/"Pink Slime",
  all in the verified CC0 **Ultimate Monsters Bundle**
  (https://poly.pizza/bundle/Ultimate-Monsters-Bundle-5oyGWAmOB6, fetched 2026-09-02).
  Per-model poly.pizza pages were not individually fetchable (Cloudflare anti-bot), so these
  three stay **pack-verified / per-file unverified**.
- The template's shared monster gradient atlas (`Atlas_Monsters.png`) matches Quaternius's
  single-atlas convention.

## Full diff table — 72 `kaykit-candidate` inventory rows + Skeleton_Mage.fbx

| Template path | file | Match status |
|---|---|---|
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/ammo_crate.fbx | ammo_crate.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/ammo_crate_withLid.fbx | ammo_crate_withlid.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/arrow.fbx | arrow.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/arrow_bundle.fbx | arrow_bundle.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/axe_1handed.fbx | axe_1handed.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/axe_2handed.fbx | axe_2handed.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/crossbow_1handed.fbx | crossbow_1handed.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/crossbow_2handed.fbx | crossbow_2handed.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/dagger.fbx | dagger.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/druid_staff.fbx | druid_staff.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/engineer_Wrench.fbx | engineer_wrench.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/mug_empty.fbx | mug_empty.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/mug_full.fbx | mug_full.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_huge_blue.fbx | potion_huge_blue.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_huge_green.fbx | potion_huge_green.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_huge_orange.fbx | potion_huge_orange.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_huge_red.fbx | potion_huge_red.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_large_blue.fbx | potion_large_blue.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_large_green.fbx | potion_large_green.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_large_orange.fbx | potion_large_orange.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_large_red.fbx | potion_large_red.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_medium_blue.fbx | potion_medium_blue.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_medium_green.fbx | potion_medium_green.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_medium_orange.fbx | potion_medium_orange.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_medium_red.fbx | potion_medium_red.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_small_blue.fbx | potion_small_blue.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_small_green.fbx | potion_small_green.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_small_orange.fbx | potion_small_orange.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/potion_small_red.fbx | potion_small_red.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/quiver.fbx | quiver.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shield_badge.fbx | shield_badge.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shield_badge_color.fbx | shield_badge_color.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shield_round.fbx | shield_round.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shield_round_barbarian.fbx | shield_round_barbarian.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shield_round_color.fbx | shield_round_color.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shield_spikes.fbx | shield_spikes.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shield_spikes_color.fbx | shield_spikes_color.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shield_square.fbx | shield_square.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shield_square_color.fbx | shield_square_color.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/shotgun.fbx | shotgun.fbx | KayKit EXTRA-tier / newer-version item (not in free GitHub 1.0) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/smokebomb.fbx | smokebomb.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/spellbook_closed.fbx | spellbook_closed.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/spellbook_open.fbx | spellbook_open.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/staff.fbx | staff.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/sword_1handed.fbx | sword_1handed.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/sword_2handed.fbx | sword_2handed.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/sword_2handed_color.fbx | sword_2handed_color.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Accessories/wand.fbx | wand.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Characters/barbarian.fbx | barbarian.fbx | EXACT name/rig match: Barbarian.fbx (41/41 joints + mesh names) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Characters/druid.fbx | druid.fbx | EXACT name/rig match: (EXTRA tier) (41/41 joints + mesh names) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Characters/engineer.fbx | engineer.fbx | EXACT name/rig match: (EXTRA tier) (41/41 joints + mesh names) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Characters/knight.fbx | knight.fbx | EXACT name/rig match: Knight.fbx (41/41 joints + mesh names) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Characters/mage.fbx | mage.fbx | EXACT name/rig match: Mage.fbx (41/41 joints + mesh names) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Characters/rogue.fbx | rogue.fbx | EXACT name/rig match: Rogue.fbx (41/41 joints + mesh names) |
| ThirdPartyResources/3DModels/KayKit - Adventurers/Models/Characters/rogue_hooded.fbx | rogue_hooded.fbx | EXACT name/rig match: RogueHooded.fbx (41/41 joints + mesh names) |
| ThirdPartyResources/3DModels/Monsters/Mushnub/Mushnub.fbx | mushnub.fbx | Quaternius Ultimate Monsters: "Mushnub" (pack verified CC0; per-file page not fetched) |
| ThirdPartyResources/3DModels/Monsters/PoisonAlien/Alien.fbx | alien.fbx | Quaternius Ultimate Monsters: "Alien" (pack verified CC0; per-file page not fetched) |
| ThirdPartyResources/3DModels/Monsters/Slime/Model/Slime.fbx | slime.fbx | Quaternius Ultimate Monsters: "Slime / Pink Slime" (pack verified CC0; per-file page not fetched) |
| ThirdPartyResources/Characters/Adventurer/Models/Adventurer.fbx | adventurer.fbx | NO MATCH in KayKit/Quaternius packs |
| ThirdPartyResources/Characters/Adventurer/Models/Dagger 3.fbx | dagger 3.fbx | NEAR: KayKit dagger.fbx (template re-export, size differs) |
| ThirdPartyResources/Characters/Mage/BackHole/Blackhole.fbx | blackhole.fbx | NO MATCH in KayKit/Quaternius packs |
| ThirdPartyResources/Characters/Mage/Orb/Planet_11.fbx | planet_11.fbx | NO MATCH in KayKit/Quaternius packs |
| ThirdPartyResources/Characters/Mage/Staff/Staff.fbx | staff.fbx | EXACT (sha256 byte-identical, KayKit Adventures repo) |
| ThirdPartyResources/Characters/Skeleton Warrior/Models/Skeleton_Warrior.fbx | skeleton_warrior.fbx | EXACT name; bone set + submesh names + texture sha256 match (KayKit Skeletons) |
| ThirdPartyResources/Characters/Skeleton Warrior/Models/Sword.fbx | sword.fbx | NEAR: KayKit sword_1handed.fbx (template re-export, size differs) |
| ThirdPartyResources/Characters/SkeletonAssasin/Blade.fbx | blade.fbx | NEAR: KayKit Skeleton_Blade.fbx (template re-export, size differs) |
| ThirdPartyResources/Characters/SkeletonGunner/Models/Bullet.fbx | bullet.fbx | NO MATCH in KayKit/Quaternius packs |
| ThirdPartyResources/Characters/SkeletonGunner/Models/Gun2.fbx | gun2.fbx | NO MATCH in KayKit/Quaternius packs |
| ThirdPartyResources/Characters/SkeletonGunner/Models/Skeleton_Rogue.fbx | skeleton_rogue.fbx | EXACT name; bone set + submesh names + texture sha256 match (KayKit Skeletons) |
| ThirdPartyResources/Characters/Survival/Models/Survival.fbx | survival.fbx | NO MATCH in KayKit/Quaternius packs |
| ThirdPartyResources/Characters/Survival/Poison/Lazy Potion.fbx | lazy potion.fbx | NO MATCH in KayKit/Quaternius packs |
| ThirdPartyResources/Characters/Survival/Poison/PoisonPuddle.fbx | poisonpuddle.fbx | NO MATCH in KayKit/Quaternius packs |
| ThirdPartyResources/3DModels/Skeleton Mage/Skeleton_Mage.fbx | skeleton_mage.fbx | EXACT name; bone set + submesh names + texture sha256 match (KayKit Skeletons) |

## Unmatched files (8) and what to do

All eight remain covered by the publisher disclosure ("3D Models: ThirdPartyResources = CC0,
poly.pizza") but could not be tied to a specific pack; `provenance.csv` marks them
`CC0, confidence low, verification unverified, chosen_path B`. Re-verify before upload or
substitute from `extraction/originals/`:

- `Adventurer.fbx` (playable "Vincent") — rigged chibi human; NOT in KayKit Adventures 1.0 or
  EXTRA tier (EXTRA = Engineer, Druid, big Barbarian). Closest public candidates: poly.pizza
  "Adventurer"-type models. If unverifiable, use KayKit Adventures Knight/Rogue as the base.
- `Survival.fbx` — zombie-style rigged character (own `Zombie_Atlas` textures).
- `Blackhole.fbx`, `Planet_11.fbx` — Mage skill VFX meshes; possibly BizachiCode-original.
- `Gun2.fbx`, `Bullet.fbx` — SkeletonGunner weapon/projectile meshes (cf. EXTRA-tier `shotgun.fbx`).
- `Lazy Potion.fbx` (note: FBX-SDK 2020 export — different toolchain from KayKit's Blender
  exports), `PoisonPuddle.fbx` — Survival skill props.

## Contradiction with context/01 §2.1 (resolved)

context/01 said "characters/enemies FBX = likely KayKit Skeletons pack (Medium confidence)" —
**confirmed at HIGH confidence**, with the amendment that the humanoid characters are the
KayKit **Adventurers** pack and the monsters are **Quaternius Ultimate Monsters**. The §2.1
"Modular Dungeon Kit (Henry Boadle, MIT)" entry maps to **no shipped files**; the real dungeon
content is Kenney Mini Dungeon / Mini Arena (CC0, bundled licenses).
