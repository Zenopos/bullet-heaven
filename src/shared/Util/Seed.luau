--!strict
-- Seeded RNG helpers (context/02 §4: Util = seeded RNG, weighted tables, math).
-- Run seeds make a life's rolls reproducible server-side; the server owns every roll (AGENTS.md §1).

local Seed = {}

-- Returns a Random generator pinned to `seed`; same seed -> same sequence.
function Seed.rng(seed: number): Random
	return Random.new(seed)
end

return Seed
