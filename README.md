# bullet-heaven

Hardcore bullet-heaven roguelike native to Roblox (Luau, Rojo/Wally/Rokit toolchain).

Death is the progression mechanic: full wipe per life; what survives is the boss-quota-gated
Legacy Vault of mirrored traits and account-permanent island conquests.

**Power past the frontier can't be bought.**

## Toolchain

Tool versions are pinned in `rokit.toml`; run `rokit install` once per machine.
Libraries are Wally packages pinned in `wally.toml`; run `wally install`, then
`rojo sourcemap > sourcemap.json` and `wally-package-types --sourcemap sourcemap.json Packages/`.

Quality gates (all must exit 0 before any commit):

```sh
stylua --check src tests
selene src tests
luau-lsp analyze --platform roblox --definitions tools/globalTypes.d.luau --sourcemap sourcemap.json --ignore "tools/globalTypes.d.luau" .
rojo build -o place.rbxl
```

Dev loop: `rojo serve` + the Rojo plugin in Studio. Never edit synced scripts inside Studio.
