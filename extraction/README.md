# extraction/ — Unity template data dump & art provenance (W0-02)

Data extracted from the purchased **BulletHell Elemental Template** Unity project (v1.5.0,
read-only reference) to feed the Roblox rebuild. `gamedata-json/` is the raw material for
`src/shared/Config/` modules (W1-02); `asset-inventory.csv` + `legal/provenance.csv` settle
what art comes from CC0/MIT originals (Path A) vs template extraction (Path B).
License analysis: `roguelike-roblox/context/01` (execution pack).

## Public-repo rules (repo is PUBLIC since W0-02)

- **Flavor text stripped:** all `*description*`/`descriptionTranslated` fields (copyrighted
  template text) were removed from committed JSON — 180 keys across 97 files
  (`itemDescription` 46, `skillDescription` 29, `description` 10, `characterDescription` 7,
  `mapDescription` 5, plus translated variants; per-file key paths in the ignored
  `stripped-keys-log.json`, regenerate with `extract_gamedata.py`). Structure, IDs, and all
  numeric/tuning parameters are kept.
- **Path B (template-extracted) binaries are NEVER committed** — in a public repo that is
  standalone redistribution, a Unity Asset Store EULA §2.2.1.1 breach. Path B files stay
  local under ignored `extraction/` paths until uploaded to Roblox (Asset Privacy:
  "Restricted on creation", never Open Use — context/01 §11).
- `extraction/originals/` holds only re-downloaded **CC0/MIT/OFL** content (public anyway).
- No `.cs`, no Unity-serialized YAML (`.asset/.prefab/.unity/.controller/.anim`) is committed.

## gamedata-json/ — 158 files, 17 categories

GameData SOs (113) plus data found elsewhere under `Res/` (45):

| category | n | source folder |
|---|---|---|
| battlepassitems | 10 | Res/GameData/BattlePassItems |
| characterdata | 7 | Res/GameData/CharacterData |
| coupons | 3 | Res/GameData/Coupons |
| currencies | 5 | Res/GameData/Currencies |
| currenciesiapitem | 4 | Res/GameData/CurrenciesIAPItem |
| elementaltypes | 9 | Res/GameData/ElementalTypes |
| framedata | 11 | Res/GameData/FrameData |
| icondata | 8 | Res/GameData/IconData |
| mapinfo | 5 | Res/GameData/MapInfo |
| quests | 8 | Res/GameData/Quests |
| shopdata | 32 | Res/GameData/ShopData (incl. items/{armor,hat,pants,shoes}) |
| skillspeark | 2 | Res/GameData/SkillsPeark *(template's typo for Perk)* |
| statspearks | 9 | Res/GameData/StatsPearks |
| drops | 5 | Res/Drops/*.prefab (Gold/EXP/Health/Shield/CollectExp, DropEntity fields) |
| skills | 29 | Res/Skills + ThirdPartyResources/Characters/*/ skill SOs |
| monsters | 7 | ThirdPartyResources/Monsters/{Alien,Mushnub} skill SOs |
| waves | 4 | **extracted from scenes** — see below |

JSON conventions: Unity boilerplate keys removed; `_scriptType` = data-class filename
(e.g. `CharacterData.cs` — name only, no code was read); object refs resolved to
`{"$ref": "Assets/...", "fileID": n}` via `guid-map.json` (ignored, regenerable);
8 dangling refs keep `{"$ref": null, "guid": ...}`.

### Waves are scene-bound (finding)

No wave SO exists (confirmed by the template GitBook, "Create New Monster Wave": *"no
scriptable is needed, just select the GameplayManager"*). `waves/maparena1–4.json` were
extracted from `Res/Scenes/MapArena*.unity` GameplayManager components: `survivalTime`,
`waves[]` (`monsterPrefab` → resolved path, `spawnInterval`, `goldPerMonster`,
`xpPerMonster`, `waveDuration`, `spawnBossAfterWave`), `bossPrefab`, `maxLevel: 40`,
perk caps 5/5/5/5, `reviveSeconds: 20`, `reviveLimit: 1`, `winCondition`, and
`xpToNextLevel` (decoded: 40-entry uint32 curve, 200 → 19,947; total 177,511 XP to max,
identical on all maps). PVP scenes have `waves: []` (PVPArenaBR adds a disabled
BoxSpawner). **Data anomalies flagged, not fixed:** maparena4 `xpPerMonster` 1/1/2/3/1
(≠ gold 12/19/30, unlike maps 1–3); maps 3–4 never set `spawnBossAfterWave` (boss spawns
at survivalTime end by runtime logic).

### Battle pass — pack claim vs data (finding)

Pack docs claim "100 tiers, 10% XP growth/tier". The template ships **10 BattlePassItem
SOs** (`passId` 1–10) with **no XP-requirement fields anywhere** (GitBook confirms tiers
are manually listed in UIBattlePass). Treat 100-tier/10%-growth as a *design target* for
our own battle pass (W3-02), not template data.

### GitBook reconciliation

Docs list 17 scriptable/data topics — all covered: character, character-type, skill,
icon, frame, map-info, quest, iap-item, coupon, currency, shop-item, battlepass-item,
skillperk, statperk, monster-mob (prefab-based, resolved in waves), monster-wave (waves/),
dropentity (drops/). Addons (wheel-spin, lootbox, daily rewards, global chat) are
documented but not dumped — optional scene/addon features; the Roblox build reimplements
its own equivalents regardless.

## asset-inventory.csv + legal/provenance.csv — 1,653 rows each

Inventory: every file under `Res/` + `ThirdPartyResources/` (excluding vendored code
`Tools/`): texture 697, other 640, animation 132, mesh 122, audio 49, font 13.
Poly counts mostly `n/a` (binary FBX); 3 ASCII FBX parsed (Skeleton_Mage 2,820 /
Warrior 3,755 / Rogue 3,345 tri — all far under Roblox's 20k cap).

Provenance per row: license, source URL, Path A/B/rebuild, Roblox import notes.

- **By license:** Unity-EULA 798 · CC0 522 · MIT 234 · OFL-1.1 64 · CC0-per-disclosure
  (per-file unverified) 30 · CC-BY 2 · Pixabay-Content 1 · unknown 2 (both flagged).
- **By path:** A 206 · B 665 · rebuild 782. **124 rows `unverified`** — every one carries
  an explanatory note; audio re-verification is required before any Roblox upload.
- `legal/licenses/` holds 19 license/evidence files (downloaded originals + template-bundled
  copies + verification notes) — the DMCA counter-notice evidence pack (context/01 §11.2).

### Requires action before first Roblox upload

1. **2 music tracks are Kevin MacLeod CC-BY** ("Darkling", "Morgana Rides") — attribution
   required, not CC0. Decide: credit in-game or replace.
2. **1 ambience is Pixabay Content License** ("At the Park (Afternoon)") — review terms
   before use; replacement safest.
3. **REPLACEMENT NEEDED:** `Res/OldUI/Font/AnderHedgeRegular.ttf` (+SDF) — vague freeware;
   replace (Evil Empire / Lilita One already in originals/).
4. `AudioClip_Background-Ambient.wav` is 34.5 MB — over Roblox's 20 MB audio cap; needs
   re-encode/split.
5. 30 ThirdPartyResources/Audio files: CC0 per publisher disclosure, per-file unverified
   (template WAVs are re-encodes; no freesound entry could be duration/size matched).
   Re-verify or replace per file before upload.

## kaykit-diff.md — open item #1 RESOLVED

**The template's characters ARE KayKit packs (HIGH confidence)**: SHA-256-identical
texture, 27/48 accessories byte-identical, all deform bones + submesh names match,
95/95 animation clips name-match. Broader truth found: characters = KayKit **Skeletons +
Adventurers**, monsters = **Quaternius Ultimate Monsters (CC0)**, dungeon tiles = **Kenney
Mini Dungeon + Mini Arena (CC0, bundled licenses)**, rank icons = **RhosGFX Vector Ranks
(CC0)**, Evil Empire font = **OFL-1.1** (not CC0 as disclosed). Full evidence table in
`kaykit-diff.md`. **Discrepancy vs context/01 §2.1:** no "Modular Dungeon Kit (Henry
Boadle, MIT)" content exists in v1.5.0; NewUI is RhosGFX CC0, not Conev MIT — the store
disclosure predates the current art set.

## originals/ — Path A downloads (~242 MB, 655 files)

`kaykit-skeletons/`, `kaykit-adventurers/` (full GitHub repos incl. FBX+GLTF+LICENSE),
`dungeon-kit/kenney-mini-dungeon|arena/`, `particle-pack/` (Kenney CC0),
`font-evil-empire/` (OFL), `font-lilita-one/` (OFL, Google Fonts).
Skipped (no verified public original): NewUI images (ride on publisher MIT disclosure →
Path B), freesound audio (per-file match impossible — see above).

## Regenerating

`python extraction/extract_gamedata.py` · `extract_waves.py` · `build_inventory.py` ·
`build_provenance.py` — read-only against the Unity project; idempotent. Unity MCP was
unavailable to the agent toolchain this session (no `mcp__unityMCP__*` tools exposed);
conversion was scripted against the force-text YAML instead and spot-verified against
known field values.
